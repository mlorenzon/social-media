#!/usr/bin/env python3
"""Read a reference reel without being able to watch it.

    python scripts/watch_reel.py https://www.instagram.com/reel/DH5UDWLS65I/ --as pianopi
    python scripts/watch_reel.py https://www.tiktok.com/@thegaze_/video/7288741268429999393 --as gaze-swing
    python scripts/watch_reel.py --as gaze-swing --no-download     # re-read a file already here

Downloads the video into `data/watched/<name>/`, then turns it into the three
things a model (or a person in a hurry) can take in without pressing play:

  contact.jpg   one frame every 3 s, tiled four across — the structure: who is
                on screen, when it cuts to the object, where the text appears
  open.jpg      the first 12 s at one frame every 2 s, larger — the hook and
                the caption style, which the contact sheet is too small to show
  read.md       the platform's own numbers (likes, comments, views where the
                platform exposes them), the caption, and a timestamped
                transcript from faster-whisper

`read.md` is the tracked artefact; everything else in the folder is a download
and is ignored. The reading itself — what the structure is doing and why it
works — goes in the study document (see `docs/format-research.md`), not here.

The transcript is a transcript here, not a clock: unlike `take_transcribe.py`
we do not know the script in advance, so the words are the point and `small.en`
is good enough for English speech over music. Lyrics and performance clips
come back nearly empty, which is itself the finding.

Same environment as `take_transcribe.py`: `.venv-asr/` holds faster-whisper and
yt-dlp, the model caches into `data/.cache/whisper/`, and this script re-runs
itself inside that venv. Build it once:

    python -m venv .venv-asr
    .venv-asr/Scripts/python -m pip install faster-whisper "yt-dlp[default,curl-cffi]"

(`bin/python` on Linux and the Pi.) `curl-cffi` is what lets yt-dlp impersonate
a browser, which TikTok has required since 2024; without it the download fails
with "Unexpected response from webpage request".
"""
import argparse
import datetime as dt
import json
import math
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
WATCHED = os.path.join(ROOT, "data", "watched")
MODEL_CACHE = os.path.join(ROOT, "data", ".cache", "whisper")
VENV_PYTHONS = (os.path.join(ROOT, ".venv-asr", "Scripts", "python.exe"),
                os.path.join(ROOT, ".venv-asr", "bin", "python"))

DEFAULT_MODEL = "small.en"
ASR_RATE = 16000

# The contact sheet: a frame every 3 s is enough to see every cut in a reel
# under two minutes, and 270 px wide keeps a 3-minute video's sheet under the
# size an image reader will take whole. The opening strip is the first 12 s at
# twice the rate and larger, because the hook is where the decisions are.
CONTACT_EVERY_S, CONTACT_W, CONTACT_COLS = 3, 270, 4
OPEN_SECONDS, OPEN_EVERY_S, OPEN_W = 12, 2, 360


def relaunch_in_venv():
    """Re-run this script with the ASR venv's interpreter (see take_transcribe.py)."""
    for python in VENV_PYTHONS:
        if os.path.exists(python):
            sys.exit(subprocess.call([python, os.path.abspath(__file__)] + sys.argv[1:]))
    sys.exit("No ASR environment. Build it once, no admin needed:\n"
             "    python -m venv .venv-asr\n"
             "    .venv-asr/Scripts/python -m pip install faster-whisper \"yt-dlp[default,curl-cffi]\"")


def download(url, folder, name):
    """Fetch the video and its metadata with yt-dlp. Returns the mp4 path."""
    import yt_dlp
    opts = {
        "outtmpl": os.path.join(folder, name + ".%(ext)s"),
        "format": "bv*[height<=1080]+ba/b",
        "merge_output_format": "mp4",
        "writeinfojson": True,
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "noprogress": True,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])
    mp4 = os.path.join(folder, name + ".mp4")
    if not os.path.exists(mp4):
        sys.exit("download finished but %s is not there — check the folder" % mp4)
    return mp4


def media_duration(path):
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=nw=1:nk=1", path])
    return float(out.strip())


def contact_sheet(mp4, dur, dst):
    rows = max(1, math.ceil(math.ceil(dur / CONTACT_EVERY_S) / CONTACT_COLS))
    vf = "fps=1/%d,scale=%d:-1,tile=%dx%d" % (CONTACT_EVERY_S, CONTACT_W, CONTACT_COLS, rows)
    # -frames:v 1: tile emits one image per full grid, and a second, partial
    # grid is an error for a single-image output, not a second file.
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", mp4,
                           "-vf", vf, "-frames:v", "1", dst])


def opening_strip(mp4, dur, dst):
    n = max(1, math.ceil(min(dur, OPEN_SECONDS) / OPEN_EVERY_S))
    vf = "select='lt(t,%d)',fps=1/%d,scale=%d:-1,tile=%dx1" % (OPEN_SECONDS, OPEN_EVERY_S, OPEN_W, n)
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", mp4,
                           "-vf", vf, "-frames:v", "1", dst])


def transcribe(mp4, wav, model_name):
    from faster_whisper import WhisperModel
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", mp4,
                           "-vn", "-ac", "1", "-ar", str(ASR_RATE), "-c:a", "pcm_s16le", wav])
    # int8 on the CPU: a one-minute reel decodes in under a minute on a Pi 5,
    # and in seconds on the laptop. Do not run two of these at once on the Pi —
    # 4 GB is enough for one model, and the second is killed without a message.
    model = WhisperModel(model_name, device="cpu", compute_type="int8",
                         download_root=MODEL_CACHE)
    segments, _info = model.transcribe(wav, beam_size=5)
    return [(float(s.start), float(s.end), s.text.strip()) for s in segments if s.text.strip()]


def platform_numbers(info):
    """The counts the platform exposes, as it exposes them.

    Instagram gives likes and comments but no view count to yt-dlp; TikTok and
    YouTube give views too. A missing number is reported missing, never
    estimated — the Insights export is the only source for Instagram reach.
    """
    rows = []
    for key, label in (("view_count", "views"), ("like_count", "likes"),
                       ("comment_count", "comments"), ("repost_count", "reposts")):
        v = info.get(key)
        rows.append((label, "{:,}".format(v) if isinstance(v, int) else "not exposed"))
    return rows


def write_read(path, name, url, info, dur, segments, model_name):
    posted = info.get("upload_date") or ""
    if len(posted) == 8:
        posted = "%s-%s-%s" % (posted[:4], posted[4:6], posted[6:])
    who = info.get("uploader") or info.get("channel") or info.get("uploader_id") or ""
    caption = (info.get("description") or "").strip()
    lines = ["# %s" % name, "",
             "*Read by `scripts/watch_reel.py` on %s: frames and a `%s` transcript, not a viewing. "
             "Counts are what the platform exposed at that moment.*" % (dt.date.today().isoformat(), model_name),
             "",
             "| | |", "|---|---|",
             "| URL | %s |" % url,
             "| Account | %s |" % who,
             "| Posted | %s |" % posted,
             "| Length | %d:%02d (%.1f s) |" % (dur // 60, round(dur % 60), dur)]
    for label, value in platform_numbers(info):
        lines.append("| %s | %s |" % (label.capitalize(), value))
    lines += ["", "## Caption", "", caption.replace("\n", "  \n") or "*(none)*", "",
              "## Transcript", ""]
    if segments:
        lines.append("| From | To | Said |")
        lines.append("|---|---|---|")
        for s, e, text in segments:
            lines.append("| %5.1f | %5.1f | %s |" % (s, e, text.replace("|", "\\|")))
    else:
        lines.append("*Nothing heard — a performance or text-only clip. Read the frames.*")
    lines += ["", "## Frames", "", "`contact.jpg` one frame every %d s; `open.jpg` the first %d s at one every %d s. "
              "Both regenerate from the download." % (CONTACT_EVERY_S, OPEN_SECONDS, OPEN_EVERY_S), ""]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url", nargs="?", help="Instagram reel, TikTok video or YouTube Short")
    ap.add_argument("--as", dest="name", required=True,
                    help="folder name under data/watched/, e.g. gaze-swing")
    ap.add_argument("--no-download", action="store_true",
                    help="reuse data/watched/<name>/<name>.mp4 and its info.json")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    args = ap.parse_args()

    try:
        import faster_whisper  # noqa: F401
        import yt_dlp  # noqa: F401
    except ImportError:
        relaunch_in_venv()
        return

    folder = os.path.join(WATCHED, args.name)
    os.makedirs(folder, exist_ok=True)
    mp4 = os.path.join(folder, args.name + ".mp4")
    info_path = os.path.join(folder, args.name + ".info.json")

    if args.no_download:
        if not os.path.exists(mp4):
            sys.exit("no download to reuse at %s" % mp4)
    else:
        if not args.url:
            sys.exit("give a URL, or --no-download to re-read an existing one")
        download(args.url, folder, args.name)

    with open(info_path, encoding="utf-8") as fh:
        info = json.load(fh)
    url = args.url or info.get("webpage_url") or ""
    dur = media_duration(mp4)
    print("  video  %s (%.1f s)" % (os.path.basename(mp4), dur))

    contact_sheet(mp4, dur, os.path.join(folder, "contact.jpg"))
    opening_strip(mp4, dur, os.path.join(folder, "open.jpg"))
    print("  frames contact.jpg, open.jpg")

    segments = transcribe(mp4, os.path.join(folder, "asr.wav"), args.model)
    for s, e, text in segments:
        print("  [%5.1f-%5.1f] %s" % (s, e, text))
    if not segments:
        print("  heard  nothing — performance clip, or text-only")

    read = os.path.join(folder, "read.md")
    write_read(read, args.name, url, info, dur, segments, args.model)
    print("  wrote  %s" % os.path.relpath(read, ROOT).replace("\\", "/"))


if __name__ == "__main__":
    main()
