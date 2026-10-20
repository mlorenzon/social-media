# social-media

Matthew's social-media content and strategy: the research behind what gets
made, the pipelines that make it, and the reading of what worked. The first
strand is the *Symphony of the Day* reels — After Effects collector cards
driven programmatically over GEOlayers 3 historical maps. The second is the
*Beethoven's Health* reel, built from the quotation research in the Obsidian
vault. The format research that serves both is here too.

## Contents

| Path | What it is |
|---|---|
| [`docs/format-research.md`](docs/format-research.md) | The process for studying a reel format from a machine that cannot play video: choosing references, reading them, deriving and testing findings |
| [`docs/history-education-formats.md`](docs/history-education-formats.md) | The first study: twelve history, music and art reels read, and the six things the ones that worked share |
| [`docs/beethoven-health-reel.md`](docs/beethoven-health-reel.md) | The Beethoven's Health reel: brief, what the research settled, the 1801 pilot, next steps |
| [`docs/reel-cards.md`](docs/reel-cards.md) | The Symphony of the Day overlay card system — daily workflow, data schema, how to adapt a card, and the traps |
| [`docs/reel-edit.md`](docs/reel-edit.md) | The recorded take → the finished Symphony of the Day reel |
| [`docs/research-engine.md`](docs/research-engine.md) | Researching a symphony to a sourced record; Zotero; the vault note |
| [`docs/geolayers-3-via-mcp.md`](docs/geolayers-3-via-mcp.md) | How to drive GEOlayers 3 from the AE MCP connector — what's scriptable, what isn't, working recipes, and the traps |
| `scripts/watch_reel.py` | Reads a reference reel: download, frame sheets, transcript, `read.md` |
| `scripts/prepare_work.py` | Gathers one symphony's data: Wikidata dates, a Commons portrait, place coordinates, the right basemap year |
| `scripts/sotd.jsx` | Builds the cards and the reel in After Effects, and drives the map |
| `data/watched/*/read.md` | One per reference reel read — the platform's numbers, caption and transcript |
| `data/works/*.json` | One file per symphony — the only thing After Effects reads |
| `data/research/*.json` | The sourced research record per symphony |
| `data/periods.json` | The artistic-period timeline shown on the back card |
| `data/clip_region.py` | Clips a historical-basemaps world GeoJSON to a bounding box and simplifies it |

## Reading a reference reel

```bash
python scripts/watch_reel.py https://www.instagram.com/reel/<id>/ --as <name>
```

Writes `data/watched/<name>/`: a contact sheet (one frame every 3 s), an
opening strip (the first 12 s, larger), and `read.md` with the platform's
numbers, the caption and a timestamped transcript. One at a time. The reading
itself goes in the study document; see `docs/format-research.md`.

## Making a Symphony of the Day reel

Two commands per work. The first gathers the data, the second builds the comps:

```bash
python scripts/prepare_work.py --composer "Johannes Brahms" \
  --title "Symphony No. 4 in E minor, Op. 98" --year 1885 --place "Mürzzuschlag"
```

```
$.evalFile(new File("<repo>/scripts/sotd.jsx"));
SOTD.buildWork("brahms-no-4");
```

Then aim the map and freeze it — see [`docs/reel-cards.md`](docs/reel-cards.md)
for the full sequence and for why freezing is not optional.

## Getting the map data

The basemaps are not in this repo (~73 MB). Fetch them from
[aourednik/historical-basemaps](https://github.com/aourednik/historical-basemaps)
(GPL-3.0, WGS 84) into `data/historical-basemaps/geojson/`, then clip to the
region you need:

```bash
python data/clip_region.py 1783
```

Writes `data/clipped/europe_1783.geojson`. Defaults to a Europe bounding box of
`[-25, 34, 45, 72]`; override with `--bbox W S E N` and `--tolerance`.

Clip wider than you intend to display — the clip leaves straight edges along the
bounding box, and they need to sit off-frame.

## Working with the AE project

`symphonyOTD.aep` is deliberately not tracked, and neither are the downloaded
portraits or baked map stills — the scripts above regenerate all of it from the
work JSON, which is tracked. The documentation covers rebuilding a mapcomp from
scratch, including the one step that has to be done by hand in the GEOlayers
panel.

## The name

This repo was `symphony-of-the-day` until 19 October 2026, when the Beethoven's
Health reel and the format research made it a broader social-media project.
GitHub redirects the old name. The *series* keeps its name everywhere it is the
series being named — `sotd.jsx`, `SOTD.*`, the `/sotd` commands, the Zotero
collection and the vault folder — because those name the reels, not the repo.
