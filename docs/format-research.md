# Format research: reading reels we cannot watch

How to study a reference reel from a machine with no video player and no
social-media login, what twelve of them showed on 19 October 2026, and the six
things the ones that worked have in common. The project this was done for is
[`beethoven-health-reel.md`](beethoven-health-reel.md); this file is the
reusable half.

```
URL  →  watch_reel.py  →  data/watched/<name>/contact.jpg   the structure
                                            /open.jpg      the hook
                                            /read.md       numbers, caption, transcript
                                                 ↓
                              a reading, written here, in ## The set
```

## Why this works at all

A model cannot press play, but a reel is a short, highly structured object, and
three cheap derivatives recover most of what matters about it:

- **A contact sheet** — one frame every 3 s, four across. It shows the cut
  structure at a glance: when the face gives way to the object, where the text
  lands, whether the last third is a payoff or a tail. At 270 px a 3-minute
  reel still fits one image.
- **An opening strip** — the first 12 s at one frame every 2 s, larger. The
  contact sheet is too small to read captions; the opening strip is where the
  hook line and the caption *style* (case, tier, position) can actually be
  read.
- **A transcript** — faster-whisper `small.en`, with segment times. Unlike the
  take pipeline, we do not know the script in advance, so here the words are
  the point. English speech over music transcribes cleanly; a performance clip
  comes back nearly empty, which tells you what kind of video it is.

The metadata yt-dlp returns gives likes, comments and the caption on every
platform, and views on TikTok and YouTube. **Instagram exposes no view count
and no reach** — the only source for those is the account's own Insights
export, which is how the 3.5M / 2.1M / 35.8 s figures for `pianopi-practice`
were obtained.

```bash
python scripts/watch_reel.py <url> --as <name>
```

One at a time. The reading — what the structure is doing — is written by hand
into this file; `read.md` is the evidence it points at.

## What a reading records

For each video: platform numbers with the date they were read; length; a
timed table of beats (what is on screen, what is said); caption style; and
then the judgement — where the payoff lands, what the object is, what the
viewer is given to do. The judgement is inference and is labelled as such.
Numbers from a search agent rather than from the video page are labelled too:
one agent-reported hook (`abrami-winter`, "published with a poem") turned out
not to be in the video at all.

## The set

Twelve read on 19 Oct 2026. Lengths from ffprobe; counts from the platform
page that day unless noted. Each has a `data/watched/<name>/read.md`.

| name | What | Platform, posted | Length | Numbers |
|---|---|---|---|---|
| `pianopi-practice` | Matthew: Raspberry Pi gates the Wi-Fi on piano practice | IG, 1 Apr 2025 | 0:46 | 3.5M views, 2.1M reach, 35.8 s avg watch, 203K likes, 70K shares, 16K saves, 1.8K comments (Insights) |
| `martines-sinfonia` | Matthew: first symphony by a female composer | TikTok, 7 Oct 2026 | 0:41 | 1.2K views, 62 likes, 0 comments |
| `fry-pinhole` | Hannah Fry: pinhole trick for perfect vision | IG, 15 Jul 2026 | 2:08 | 234K likes, 4.4K comments |
| `porter-talc` | K Porter: talcum-powder cap, "Mechanical Engineering Part of the Day" | IG, 15 Oct 2026 | 3:39 | 324 likes at 4 days |
| `neely-chechnya` | Adam Neely: what Chechnya's tempo ban really does | YT Short, 11 Apr 2024 | 0:46 | 1.26M views, 62K likes, 1.1K comments |
| `anderson-crab-canon` | Taylor Anderson: Bach's crab canon, forwards and backwards | TikTok, 26 Jun 2023 | 2:15 | 1.4M views, 176K likes, 1.26K comments (account ~38K) |
| `abrami-winter` | Esther Abrami: Vivaldi *Winter* live | TikTok, 13 Oct 2025 | 1:13 | 3.4M views, 238K likes |
| `collier-diminished` | Jacob Collier: diminished chords as four-way crossroads | YT Short, 6 May 2026 | 1:16 | 1.84M views, 59K likes |
| `gaze-swing` | The Gaze: Fragonard, *The Swing* | TikTok, 11 Oct 2023 | 1:20 | 5.3M views, 1.1M likes, 2.2K comments |
| `gaze-calvary` | The Gaze: Bruegel, *Procession to Calvary* | TikTok, 20 Dec 2025 | 1:19 | 2.8M views, 437K likes |
| `tatyana-inferno` | Tatyana (About Art): Dante's circles in painting | TikTok, 14 Jun 2025 | 1:38 | 2.3M views, 197K likes |
| `letterslive-mozart` | Letters Live: Ferdinand Kingsley reads Mozart to Constanze | TikTok, 12 Oct 2023 | 2:15 | 1.2M views, 139K likes |

### `pianopi-practice` — the reference

35.8 s average watch on 46 s is ~78% retention; 70K shares on 2.1M reached is
3.3% sends-per-reach, the signal Instagram names for non-follower
distribution. Likes/reach 9.7%, saves 0.8%.

| Time | Beat |
|---|---|
| 0–2 s | Face, spoken: "My kid is going to hate me for this." No on-screen question. |
| 2–15 s | Mechanism over object close-ups: breadboard on the keys, the bar graph, "when he's done 10 minutes, the internet turns on", cut to the router. |
| 15–30 s | The kid, labelled *Denial stage → Anger stage → Bargaining stage*; off-camera: "if you play faster, it doesn't actually make time go faster." |
| 30–46 s | *Acceptance*; "Yeah, you did it!"; the celebration. |

Big centred word-by-word captions with a smaller sub-line; domestic light; no
cuts to speak of. A promise at 0 s paid at 40 s, about something people argue
about (screen time), with a specific object as proof.

### `martines-sinfonia` — the negative

Talking head, bookshelf, wired earbuds, same caption style, two cutaways
(Mozart portrait, the Martines manuscript), one text gag ("[listening
intensifies]"). 1.2K views on a fresh account is roughly TikTok's seed test;
62 likes on 1,224 is 5%; **0 comments is the tell.** The hook is a question —
"What does the first symphony by a female composer sound like?" — and the next
line answers it: "Like a classical symphony, because it was composed in 1770."
Curiosity opened and closed inside ten seconds, then 30 s of taxonomy
(overture vs symphony vs sinfonia), which is correction-shaped information
nobody sends to a friend. The best line — partied with Mozart, Haydn in her
attic — is spent in four seconds.

### `fry-pinhole`

| Time | Beat |
|---|---|
| 0–4 s | Instruction to the viewer: "If you wear glasses, take them off… I want to show you a trick to give you perfect vision again." Blurred-glasses graphic over her face at 2 s. |
| 4–21 s | The trick, done to camera; the viewer does it too. **Payoff by 15 s, in the viewer's own eye.** |
| 21–26 s | "Tell me in the comments how the text has suddenly become crystal clear." → 4.4K comments. |
| 26–76 s | The physics, in flat two-colour eye diagrams. |
| 76–119 s | Three "by the way" extensions: camera aperture, squinting, the optician's pinhole disc. |
| 119–128 s | Callback joke: "you'll look like a plonker, but you'll see them judging you in perfect focus." |

Captions one line, sentence case, small, lower third. Same post-it wall every
time.

### `porter-talc`

Persistent two-line title card the whole way: "Mechanical Engineering Part of
the Day / Talcum Powder Stack (per request)". Object in hand, face half in
frame, phone camera, no cuts. Thesis by 29–37 s: "it's not just the packaging
tape, it's the only thing standing between shipping vibration and a bag of
powder everywhere." Mechanism walked through on the object; closes on a
catchphrase: "Tolerance stacking, learn it." Serif captions, two tiers; the
post caption restates the thesis in one line. 3:39 long.

### `neely-chechnya`

| Time | Beat |
|---|---|
| 0–5 s | Title card top-centre. Line one is the news fact: music banned under 80 and over 116 bpm. |
| 5–11 s | "But not because they wanted to avoid music that was too fast or too slow, like how many news organizations reported." Guardian, CNN, NPR headlines on screen. |
| 11–26 s | Proof: lezginka wedding footage, a bar of 6/8 highlighted beat by beat, the half-time argument. |
| 26–37 s | The range bans foreign dance music while keeping their own. Moscow Times headline, figures highlighted. |
| 37–46 s | Coda joke: footwork at 160 half-times to 80, "so who knows, Chechen footwork?" |

Captions centred, sentence case, two lines. **The sources are on screen as
screenshots** — a correction with stakes and visible evidence is a payoff, not a
lecture.

### `anderson-crab-canon`

Opens on a question — "Did you know Bach wrote a piece that can be played
forwards, backwards and upside down at the same time?" — but the question *is*
the payoff; the claim is the reveal. No face. Scrolling score with bouncing
balls, then a Möbius-strip animation for retrograde inversion. The length is
the demonstration: the canon forwards, then both ways, then inverted. Small
sentence-case captions; ends sincere ("the absolute genius of Bach"). A 1.4M
hit from a ~38K account.

### `abrami-winter` — the control

Not an explainer. Overlays: "pov: it's 1700 and Vivaldi drops this banger",
"not ready for the reaction of the audience at the end", "the screams", then a
tour-date plug and a story about a little girl with a sign. A performance clip
with an emotional beat — the biggest number in the set, and the lane this
project is not in. The research agent's reported hook ("published with a poem")
is not in the video.

### `collier-diminished` (frames only; the transcript was killed twice for memory on the Pi)

Live stage clip from a talk. Chord names appear as coloured overlays as he
sings them; the audience sings the resolutions; "hero stories", "four-way
crossroads", "and resolve to the Major", "how cool is that!" A metaphor stated
first, then the audience makes the proof with their own voices — the pinhole
trick in musical form.

### `gaze-swing` and `gaze-calvary`

No face, ever. The painting is the whole frame, panned and zoomed; the voice
is dry and close. Captions are two-tier — a huge typographic keyword ("delic",
"ohlalaaaaa", "contrasts", "but where is christ?") over a small body line — on
a house colour (hot pink for Fragonard, dark green for Bruegel) that also
carries the title cards and the painter's portrait. Yellow annotation lines and
circles drawn on the painting as evidence.

*The Swing* opens with the painting speaking — "I'm losing my shoe." — then
"Meet The Swing… colourful and frivolous at first sight, but also harbouring
some deliciously dark secrets", details in sequence each with a small joke ("or
maybe he's just a big fan of slippers"), and a closing question: "Which man
will catch your fall?"

*Calvary* opens on the gore — "if you zoom in far enough, you'll discover a man
hanging from the gallows. And here, another one." — and is built on a refrain,
"But where is Christ?", three times with a wrong candidate each, until "Here."
at 50 s. Then the turn to sincerity: a painting about how easy it is to stand
and stare. Undercut first, sincere last.

### `tatyana-inferno`

Green-screen talking head, paintings behind her with artist/date labels,
all-caps captions with yellow keyword highlights. "Where would you end up?" is
a question but a participatory one — the viewer places themself. List
structure, circles one to five, cliffhanger to part two.

### `letterslive-mozart`

A man at a festival lectern reading a letter, with cutaways to the crowd
laughing. The letter is funny on its own ("good day, Stanzel… little
turned-up-nosed little bagatelle"), the reading performs it (voices, pauses,
the slow "no, no, no"), and the laughter cutaways give permission to laugh. The
post caption sets the register: "So Mozart was pretty into his wife… 👀".

## The six things the ones that worked share

Derived from the set; none of the music or art examples broke them.

1. **The payoff is in the first line, and it is not a question.** "My kid is
   going to hate me for this." "I want to show you a trick." "Talcum Powder
   Stack." A fact plus "but" (Neely). A claim so odd that stating it is the
   reveal (Anderson). The one question-hook that failed (`martines-sinfonia`)
   answered itself in the next sentence; the ones that worked (Tatyana, Fry's
   instruction) make the viewer *do* something.
2. **Visible evidence.** A breadboard, fingers, a talc bottle; screenshotted
   headlines; the score; a yellow circle on the painting; the audience
   singing. The negative had two cutaway images and nothing in hand.
3. **Thesis early, depth after — and the depth is more small payoffs.** All
   the long ones (2:08, 3:39, 2:15) hold because each layer after the payoff
   pays again (Fry's three "by the ways"; the refrain in *Calvary*). The brand
   data's 45–60 s peak is an average over brands, not a ceiling for this.
4. **Series framing that says what this is before a word is heard.** Porter's
   title card; Fry's wall; Neely's title; The Gaze's house colour and type.
   The one-off hits (Anderson) had none and stayed one-offs.
5. **A built-in reason to comment.** Fry asks outright; Porter's "(per
   request)" shows the loop; Neely corrects the press; the pianopi reel was an
   argument about screen time. Zero comments means nothing was at stake.
6. **Captions are quiet.** Sentence-case single lines, or The Gaze's
   keyword-plus-body. None of the big ones use the all-caps word-by-word of
   `martines-sinfonia`. The register is "person explaining", not "edit".

Two things the music and art examples added:

- **The music is the proof and plays under the explanation** (Anderson,
  Collier, Neely's dance footage). It is never wallpaper, and never the joke.
- **A faceless piece can win if the design system and voice are strong and the
  images *are* the content** (The Gaze, 5.3M). What makes a faceless history
  slideshow read as slop is a synthetic voice over wallpaper images, not the
  absence of a face.

## Traps

- **Do not run two transcriptions at once on the Pi.** 4 GB holds one
  `small.en` model; the second is killed (exit 137) without a message, and so
  is anything else running in that shell. Run the batch sequentially.
- **`pkill -f faster_whisper` kills the shell that is about to run it**, because
  the heredoc containing the import is on that shell's command line. The job
  dies with exit 144 and nothing in the output says why.
- **TikTok needs `curl-cffi`** (`yt-dlp[default,curl-cffi]`) or every download
  fails with "Unexpected response from webpage request". Instagram and YouTube
  work without login for public posts; Instagram *profile* pages do not render
  to anything, so counts have to come from the post or from Insights.
- **Instagram's `view_count` is `None` in yt-dlp.** Views and reach exist only
  in the account's own Insights export. Likes and comments are exposed.
- **The contact sheet cannot be read for captions.** That is what `open.jpg`
  is for; a one-row tile of larger frames over the first 12 s.
- **`tile` with more input frames than cells is an error, not a second
  image** — "Cannot write more than one file with the same name". `-frames:v 1`
  is the fix and is in the script.
- **A search agent's description of a video is not the video.** Agents read
  captions, press and tag pages, and one reported a hook that was not there.
  Treat an agent's find as a URL to read, never as a reading.
- **Whisper's transcript of a performance clip is nearly empty.** That is a
  finding (the clip has no explanation in it), not a failure to fix with a
  bigger model.
