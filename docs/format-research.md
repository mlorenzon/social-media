# Format research: how to study a reel format

A repeatable process for deciding how to make a piece of social content by
reading what already works, from a machine that cannot play video and has no
platform login. It is the method only. Each study it produces is its own
document, named for its lane:

| Study | Lane | Date |
|---|---|---|
| [`history-education-formats.md`](history-education-formats.md) | History, music and art explainers | 19 Oct 2026 |

Add a row when you finish one. The first study was run for
[`beethoven-health-reel.md`](beethoven-health-reel.md).

```
question + lane
     ↓
pick references (hit, miss, your own, a control)
     ↓
watch_reel.py <url> --as <name>  →  data/watched/<name>/ contact.jpg  open.jpg  read.md
     ↓
a reading per reel  →  compared side by side  →  what the hits share
     ↓
tested against the brief  →  one hypothesis per thing you can still change
```

## When to use it

Before committing a format to a series, or when a post has surprised you in
either direction. Not for choosing a topic, and not a substitute for posting:
twelve reels give you hypotheses, and only your own account can test them.

## 1. Write the question down first

A study with no question reads twelve reels and finds twelve reels. Write, at
the top of the study document:

- **Question.** One sentence: what makes *this kind* of piece hold viewers and
  get sent on?
- **Lane.** Subject, who is speaking, to whom, from what material.
- **What you can change.** Hook, structure, caption style, length, whether a
  face is on screen, the sound. Findings that touch none of these are trivia.
- **Evidence grade.** What the study can and cannot establish (see step 5).

## 2. Choose the references

Aim for 8–12. The mix matters more than the count:

| Kind | Why it is there |
|---|---|
| **Your own best** | The one format your audience has already proved. Counts from your Insights export, not the public page. |
| **Your own miss, same lane** | The negative control. The most useful single reel in a set, because it holds everything constant except what went wrong. |
| **Hits in the lane** | What works for the audience you want. |
| **Hits from adjacent lanes** | Expert explainers, other subjects. They show which mechanics are portable and which belong to the subject. |
| **A control from a different mechanic** | A performance clip, a trend format. It marks the edge of what this lane's findings apply to. |

Use someone else's counts only for what the platform exposes (step 5). **A
search agent can find candidates; it cannot read them.** Agents report from
captions, press and tag pages, and one confidently described a hook that was
not in the video. Treat every agent find as a URL to read, never as a reading.

## 3. Read each one

```bash
python scripts/watch_reel.py <url> --as <name>
```

One at a time. It writes `data/watched/<name>/`:

- **`contact.jpg`** — a frame every 3 s, four across. The structure at a
  glance: when the face gives way to the object, where text lands, whether the
  last third is a payoff or a tail.
- **`open.jpg`** — the first 12 s at a frame every 2 s, larger. The contact
  sheet is too small to read captions; this is where the hook line and the
  caption *style* (case, tiers, position) are read.
- **`read.md`** — the platform's numbers, the caption, and a timestamped
  faster-whisper transcript. `read.md` is tracked; downloads and images are
  not, and regenerate from the URL recorded in it.

Then open the two images and `read.md` together and write the reading.

### What a reading records

For each video, in the study document:

1. **Numbers and the date they were read.** Platform, posted date, length.
2. **A timed table of beats**: what is on screen, what is said, at what second.
   Only for reels worth the detail; one paragraph is enough for the rest.
3. **Caption style**: case, tiers, position, colour.
4. **The judgement**: where the payoff lands, what the visible evidence is,
   what the viewer is given to do. **Labelled as inference.**
5. **Anything you could not read**, and why (a blocked transcript, a missing
   count).

### Questions to ask of every reel

These are the ones the first study kept returning to; replace them when a
study shows they are the wrong ones.

- What is the first line, and is it a question that the next sentence answers?
- What is *in the viewer's hands* by second 5: an object, a claim, a task?
- What is the visible evidence? Something the viewer could check.
- How many separate payoffs are there, and when does the last one land?
- What does the viewer get to *do* (comment, try, send)?
- Is there anything that says what this series is before a word is heard?
- Is sound the proof, the wallpaper or the joke?

## 4. Compare, then derive

Put the reels in one table with the questions as columns. A pattern counts
only if it appears in the hits **and its absence appears in the miss**. Write
each finding as a claim a reel could fail:

> The payoff is in the first line, and it is not a question.

not as advice:

> Use a strong hook.

Note findings that held only in one lane separately from ones that held
across lanes; the second kind is portable, the first is not.

## 5. Grade the evidence honestly

- **Read from the video:** structure, wording, caption style, timings. Solid.
- **Platform counts:** true on the date read, and different by platform.
  YouTube and TikTok expose views; Instagram exposes likes and comments and
  *never* views or reach to a downloader. Compare reach only across platforms
  that expose it, or from your own Insights.
- **Why a reel travelled:** inference from a handful of examples, not a
  measured effect. State it that way.
- **Shelf life:** formats and humour registers date quickly. Put the study date
  on it and re-run before leaning on it after about three months.

## 6. Turn it into a test

A study ends in hypotheses for the brief, each with a way to be wrong.
Instagram's Trial Reels (shown to non-followers first, auto-shared if they
perform) are the cheap way to test two cuts of one idea without spending the
audience you already have. Log what was tried and what happened in the study
document, so the next study starts from your own results rather than from other
people's.

## Setup

`watch_reel.py` re-runs itself inside `.venv-asr/`, which holds faster-whisper
and yt-dlp:

```bash
python -m venv .venv-asr
.venv-asr/Scripts/python -m pip install faster-whisper "yt-dlp[default,curl-cffi]"
```

(`bin/python` on Linux and the Pi.) Run reels **sequentially**; see the first
trap.

## Traps

- **Do not run two transcriptions at once on the Pi.** 4 GB holds one `small.en`
  model; the second is killed (exit 137) without a message, and so is anything
  else running in that shell.
- **`pkill -f faster_whisper` kills the shell about to run it**, because the
  heredoc containing the import is on that shell's command line. The job dies
  with exit 144 and nothing in the output says why.
- **TikTok needs `curl-cffi`** (`yt-dlp[default,curl-cffi]`) or every download
  fails with "Unexpected response from webpage request". Instagram and YouTube
  work without a login for public posts; Instagram *profile* pages render to
  nothing, so counts have to come from the post or from Insights.
- **Instagram's `view_count` is `None` in yt-dlp.** Views and reach exist only
  in the account's own Insights export. Likes and comments are exposed.
- **yt-dlp reads stdin.** Looping over a URL list with `while read` feeds it
  the list and it swallows the remaining URLs. Redirect its stdin from
  `/dev/null`.
- **The contact sheet cannot be read for captions.** That is what `open.jpg`
  is for.
- **`tile` with more input frames than cells is an error, not a second image**
  ("Cannot write more than one file with the same name"). `-frames:v 1` is the
  fix and is already in the script.
- **Whisper's transcript of a performance clip is nearly empty.** That is a
  finding (the clip has no explanation in it), not a failure to fix with a
  bigger model.
- **A single-run transcript can be killed for memory** on the Pi (one reel in
  the first study was read from frames alone). Say so in the reading rather
  than leaving a gap.
