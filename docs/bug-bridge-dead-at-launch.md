# Bug: the AE MCP bridge is dead after every After Effects launch

Written 2 Oct 2026 after a long session that did **not** fix it. Everything
below is measured on this machine unless marked *hypothesis*. The point of
this file is that a fresh reader can see the evidence without re-collecting it.

## Symptom

After launching After Effects (double-clicking `symphonyOTD.aep`), every MCP
tool times out: `check-bridge` returns `"Timed out waiting for bridge result for
command 'ping'"`. `ae_command.json` sits at `"status": "pending"` and
`ae_mcp_result.json` says `"waiting"`. The **only** recovery that has ever
worked is, in AE: panel flyout `☰ ▸ Close Panel`, then `Window ▸
mcp-bridge-auto.jsx`. After that the bridge works for the rest of the session.
Matthew also reports that reopening sometimes fails with an AE message about a
modal dialog being open, though no dialog is visible.

The project's `CLAUDE.md` and `docs/reel-cards.md` have accumulated four
separate "looks like a closed panel" causes (locked session, laptop on
battery, sleep, panel actually shut). This session's finding is that the
launch case is a fifth and probably the most common, and that none of the
in-script fixes attempted so far reach it.

## The machinery

- MCP server: `C:\Users\mlorenzon\Documents\after-effects-mcp` (clone of
  `https://github.com/a-y-ibrahim/after-effects-mcp`, local `main` at
  v1.7.4 = `8d78eab`; upstream is 26 commits ahead at v1.13.0 — none of them
  touch the poll loop, and the repo has **zero issues filed**). Claude
  Desktop runs `node …\after-effects-mcp\build\index.js`.
- Bridge folder: `C:\Users\mlorenzon\AppData\Local\ae-mcp-bridge\`
  (`ae_command.json`, `ae_mcp_result.json`; new this session:
  `ae_heartbeat.json`, `ae_bridge_log.txt`).
- Panel script: `src/scripts/mcp-bridge-auto.jsx` (build copies it verbatim to
  `build/scripts/`; `npm run install-bridge` copies that to
  `%APPDATA%\Adobe\After Effects\26.0\Scripts\ScriptUI Panels\` and `…\26.5\…`).
  AE 26.5 is the live version (`AfterFX.exe` 26.5, prefs under `…\26.5\`).
- The poll loop, in that file: `startCommandChecker()` does
  `app.scheduleTask("checkForCommands()", 250, true)` and stashes the id in
  `$.global.mcpCheckTaskId`; `checkForCommands()` reads `ae_command.json`,
  dedups on `commandId`, calls `executeCommand()`, which writes
  `ae_mcp_result.json`. Search those function names; line numbers moved
  during the session.
- The panel is saved in the workspace
  (`%APPDATA%\Adobe\After Effects\26.5\ModifiedWorkspaces\UserWorkspace.xml`
  names `mcp-bridge-auto`), so AE restores and runs it at every launch.

## What was measured

### No modal exists

Enumerating all top-level windows of the `AfterFX` process while the bridge
was dead: 23 windows, **zero** of class `#32770` (visible or hidden), main
window `IsWindowEnabled = true`. AE idle at 0.02 cores, session unlocked, on
mains. So the "modal" AE complains about when the panel is reopened is not a
window anyone can dismiss.

### The restored panel runs its script to completion — and its timer never fires

With logging added (`ae_bridge_log.txt`, written by `logToPanel`) and a
heartbeat (`ae_heartbeat.json`, rewritten every ~2 s by `checkForCommands`):

| Launch | Log | Heartbeat |
|---|---|---|
| 09:55:00 | `MCP Bridge Auto started` … `Ignoring pre-existing command` | one beat at 09:55:00, `mode: panel, taskId: 2` — **never updated again** |
| 10:07:43 | same | one beat, `taskId: 3`, never again |
| 10:18:11 | same, plus `startup script loaded from …\26.5\Scripts\Startup\mcp-bridge-startup.jsx; panel found` | one beat, `taskId: 3`, never again |

So at launch the panel script completes, `startCommandChecker` runs,
`app.scheduleTask` returns a valid id, and the task **fires zero times**.
When the same file is re-run via `Window ▸ mcp-bridge-auto.jsx` after launch,
the task fires every 250 ms (this is the known-good recovery).

The restored panel is also drawn **blank** — a `PrintWindow` capture at 09:19
showed the `mcp-bridge-auto` panel frame in the bottom-right dock with no
checkbox, no log, no buttons — even though the script that adds those widgets
ran to completion. Not re-checked after the later launches.

### A Startup script's timer does not fire either

`src/scripts/mcp-bridge-startup.jsx` (new) was installed to
`%APPDATA%\Adobe\After Effects\26.5\Scripts\Startup\`. The log proves AE
**does** run user-level Startup scripts (`startup script loaded from …`,
10:18:11) — contrary to several forum posts. It scheduled two one-shots
(`app.scheduleTask(code, 4000, false)` and `20000`), each of which would have
logged `startup task fired`. Neither line ever appeared.

### The decisive experiment: launch with no project (10:41, 2 Oct)

AE launched from the Start menu at 10:41:48, with the `.aep` opened afterwards
(the window title showed it open by 10:42:36; exactly when and by whom — the
Home screen's recent list, or AE reopening it — is not recorded, ask Matthew).
Log and heartbeat:

```
10:41:54  startup script loaded … panel found
10:41:54  MCP Bridge Auto started                      (the restored panel, as before)
10:41:58  startup task fired; last beat 1737 ms ago -> loop alive, nothing to do
```

That "last beat 1737 ms ago" is a beat at ~10:41:56.8, which is **not** the
forced beat `startCommandChecker` writes at 10:41:54 — it was written by a
real tick of the restored panel's repeating task. The heartbeat file's final
timestamp is 10:41:58.592, another real tick. So **after a bare launch, the
restored panel's timer ticks normally** — the one thing it had never done in
three project-file launches.

Then every scheduled task died at once at 10:41:58.6: no heartbeat after that,
and the Startup script's 20 s one-shot (due ~10:42:14, logs unconditionally)
never fired. The project was open shortly after. `check-bridge` at 10:42:36
timed out as usual.

Revised conclusion: **opening a project kills every pending `app.scheduleTask`,
one-shot or repeating, whenever it was registered.** Launching AE by
double-clicking the `.aep` simply does this at the earliest possible moment,
so every timer the panel or a Startup script registers is dead on arrival.
Reopening the panel from the Window menu works because it registers a new
timer *after* the load. This matches the Adobe forum reports that scheduleTask
"stops working whenever an AE window pops up" (the project-load progress
dialog is such a window) and that startup scripts misbehave specifically when
AE is launched by opening a project. It also explains the `CLAUDE.md` traps:
the crash-repair dialog, the Replace Footage dialog, and probably the
lock/sleep cases are the same kill, by other dialogs.

Still unverified: whether *dismissing* a later dialog mid-session also kills
the timer (the Replace Footage note in `docs/reel-cards.md` says the bridge
recovered after Cancel — if true, only some dialogs kill it, or the load
dialog is special).

### The CEP extension is found, started, and refused

`cep/` (new) is a CEP extension with a `Type=Custom`, `AutoVisible=false`,
`StartOn=applicationActivate` headless instance whose Chromium `setInterval`
would call `checkForCommands()` via `evalScript` — the Premiere MCP on this
machine uses exactly this pattern (`%APPDATA%\Adobe\CEP\extensions\MCPBridgeCEP`,
host PPRO only) and its headless instance does start at Premiere launch.
Installed to `%APPDATA%\Adobe\CEP\extensions\com.after-effects-mcp.bridge\`.

`%TEMP%\CEP12-AEFT.log` on the 10:18 launch:

```
10:18:12:470 : ERROR Signature verification failed for extension com.after-effects-mcp.bridge.headless
10:18:45:981 : ERROR Signature verification failed for extension com.after-effects-mcp.bridge.headless
10:20:59:567 : ERROR Signature verification failed for extension com.after-effects-mcp.bridge.headless
```

So `StartOn` fires (three attempts), but CEP 12 (`CEPHtmlEngine.exe` 12.0.1)
refuses the unsigned extension **even though** `HKCU\Software\Adobe\CSXS.9`
through `CSXS.14` all have `PlayerDebugMode = "1"` of type `REG_SZ`, which is
the documented way to allow unsigned extensions. Both other CEP extensions on
the machine (GEOlayers 3, MCPBridgeCEP) are signed (`META-INF/signatures.xml`),
so debug mode has possibly never actually worked here. **Not investigated:**
whether CEP 12 moved or renamed the debug flag, whether a `.debug` file is
required, or whether self-signing with `ZXPSignCmd` is the simpler route.
This is where the session stopped.

## Fix candidates, given the above

1. **Re-arm the timer at the end of every command.** In
   `executeCommand`'s success and error paths (or in `checkForCommands`'s
   `finally`), call `startCommandChecker()` again after any command that could
   have shown a dialog — or simply after every command; it costs one
   `cancelTask` + `scheduleTask`. Then the daily procedure is: launch AE bare,
   the restored panel's timer ticks, open the project **through the bridge**
   (`app.open(new File("…/symphonyOTD.aep"))` via `execute-script`), and the
   re-arm after that command outlives the load dialog. Nothing in-script can
   recover from a dialog AE opens on its own (launch-by-file), so launching
   bare becomes the rule. `SOTD` could grow an `openProject()` that does this.
2. **Make the CEP extension load.** Its Chromium timer is not an
   `app.scheduleTask` and would survive the load dialog, which makes
   double-clicking the `.aep` safe again. It is currently refused by signature
   verification despite `PlayerDebugMode = "1"` (REG_SZ) on CSXS 9–14 — see
   above. Untried: a `.debug` file in the extension folder, checking whether
   CEP 12 reads `HKCU\Software\Adobe\CSXS.12` at all on this build (both other
   extensions here are signed, so debug mode is unproven on this machine), or
   self-signing with `ZXPSignCmd -selfSignedCert` + `-sign`, which needs no
   admin.
3. **Procedural only:** launch AE from the Start menu, then reopen the panel
   once the project is open. Same clicks as today, but now explicable.

## Other things worth one check each

1. **Click `Check for Commands Now`** on the restored (possibly blank) panel
   while a ping is pending. If it answers, the engine and the panel's scope are
   fine and only the timer is dead; if it does nothing, the restored panel's
   script scope is broken in a way the log does not show.
3. **Minimal repro** of the timer claim, independent of the bridge: a
   three-line Startup script `app.scheduleTask('…write a file…', 3000, false)`.
   If it fires, something in the bridge's launch path is at fault, not AE.
4. **`Pref_WARN_WHEN_RUNNING_SCRIPTS = 01`** in `…\26.5\Adobe After Effects
   26.5 Prefs.txt` — unknown meaning, untested; possibly a suppressed prompt
   that holds the first script of a session.
5. The ES3 engine: the panel file's top-level `var` declarations are only
   global if AE evaluates a restored ScriptUI panel at global scope. If a
   restored panel is evaluated in a private scope, `scheduleTask("checkForCommands()")`
   would throw `checkForCommands is undefined` on every tick and AE would
   cancel it — silently, because the task string, not the panel, is what
   failed. A task string of `$.global.mcpTick()` with the function stored on
   `$.global` would survive that. Nothing in the logs rules this in or out.

## State left on the machine

All on branch `headless-bridge` in `C:\Users\mlorenzon\Documents\after-effects-mcp`
(4 commits, not pushed; `main` untouched):

- `src/scripts/mcp-bridge-auto.jsx`: poll loop no longer touches widgets
  (auto-run flag in `$.global.mcpAutoRun`, `setStatus()` and `logToPanel()`
  never throw, `isChecking` reset in `finally`), writes `ae_heartbeat.json`
  and `ae_bridge_log.txt`, skips `scheduleTask` when
  `$.global.mcpExternalTicker` is set. **This part is believed good and is
  what the Window ▸ reopen recovery now runs.**
- `src/scripts/mcp-bridge-startup.jsx`: logs on load, re-arms on a stale
  heartbeat. Proven to load and (on a bare launch) to fire; useless against
  the project-load kill, which is after it. Its one real contribution is the
  log line that made the 10:41 experiment readable.
- `cep/`: the CEP extension; refused by signature verification.
- `install-bridge.js`: also copies the Startup script (user folders) and the
  CEP extension; warns if `PlayerDebugMode` is off.

Installed copies: both `%APPDATA%\Adobe\After Effects\{26.0,26.5}\Scripts\ScriptUI Panels\mcp-bridge-auto.jsx`
and `…\Scripts\Startup\mcp-bridge-startup.jsx`, and
`%APPDATA%\Adobe\CEP\extensions\com.after-effects-mcp.bridge\`. To revert to
stock: `git checkout main && npm run build && npm run install-bridge` in the
MCP repo, delete the two Startup copies and the CEP folder.

Unrelated and also uncommitted in **this** repo: `scripts/sotd.jsx` carries the
new landscape card (`SOTD.buildLandscapeWork(slug)`, `CFG.land`), syntax-checked
but never built, because the bridge was never up.

## Sources consulted

- [Adobe Community — need an ExtendScript timer](https://community.adobe.com/t5/after-effects-discussions/need-an-extendscript-timer/m-p/6117454/highlight/true) (scheduleTask stops when an AE window pops up)
- [Adobe Community — crashes at startup executing startup scripts](https://community.adobe.com/t5/after-effects-discussions/after-effects-crashes-at-startup-executing-startup-shutdown-scripts/td-p/10420940) (startup-script trouble specific to launching by opening a project)
- [Adobe Community — scheduleTask while a modal dialog is waiting](https://community.adobe.com/t5/after-effects-discussions/what-can-be-done-to-app-scheduletask-while-the-modal-dialog-is-waiting-for-a-response/m-p/14060375)
- [Creative COW — AE Startup Script](https://creativecow.net/forums/thread/ae-startup-script/)
- `About the Startup folder.txt` in `C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\Scripts\Startup\` ("Scripting shares a global environment")
