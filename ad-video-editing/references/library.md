# OpenFilm CC0 library

OpenFilm (MIT code) ships a free media library in its repo at
`packages/openfilm/library/`: SFX, music, transitions, camera motions,
effects, filters, text looks, stickers, templates. Verified on disk and
via CLI on 2026-11-12. Paths below are relative to `packages/openfilm/`.

## What it contains (verified counts)

Two counts — do not mix: **on disk** = folders/files in `library/`;
**catalog** = `search.json` rows (8,744), incl. downloadable entries not on disk.

| Kind | On disk | Catalog rows | Notes |
|---|---|---|---|
| Bundled SFX | 21 `.m4a` in `library/sounds/` | 20 | whoosh, boom, hit, riser, ding, pop, click… local files, copy directly |
| SFX + music catalogs | — | ~6,600 | metadata in `search.json`; files download on `--take` |
| Transitions | 61 dirs | 61 | dissolve, dip-black, glitch, ink, light-leak, whip-family… |
| Motions | 64 dirs | 64 | `cut-whip-*`, `cut-zoom-through`, `in-whip`, `loop-ken-burns`… punch-in/whip vocabulary, each with `preview.mp4` |
| Effects | 71 dirs | 70 | grain, vignette, light-leak, VHS |
| Filters | 1 dir (`layer`) + sample stills | 66 | color-grade looks; most ship as catalog entries, not folders |
| Text looks | 78 folders | 148 `text/` rows | titles, karaoke cue styling; counts include motion/out rows, so they differ |
| Stickers | 57 dirs | 1,643 | 1,587 emoji (MIT) + arrows |

`search.json` rows carry id, keywords and descriptions in several languages — search works in any language.

## License (quoted from `library/LICENSE.md`)

> "Everything in OpenFilm's library can be used in any film, commercial or
> not, changed and shared, with no need to credit anyone. … These are
> dedicated to the public domain under CC0 1.0."

Exception: `stickers/emoji/` are Microsoft Fluent Emoji under MIT — keep `library/LICENSE.md` with copied assets.

## How to use it

Preferred path: copy the `library/` tree once into our assets area and
search our own copy — no runtime dependency on their CLI. Their CLI
(verified working, offline for bundled files):

```bash
CLI="node <vendor>/openfilm/src/packages/openfilm/bin/openfilm.mjs"
$CLI get sfx-search --prompt "whoosh impact" --limit 8
$CLI get sfx-search --prompt "cash register" --sec 1 --limit 5
$CLI get transition --prompt "quick whip left"
$CLI get effect --prompt "punch in zoom"     # motions live under `effect`
$CLI get music-search --prompt "tense drone" --sec 15
```

- Bundled hits print a local `hear it:` path — copy the file. Catalog
  hits print `openfilm/audio/sfx/<slug>.mp3` and "its file is not on
  this computer"; `--take <id>` downloads into a project's `assets/`
  (free, CC0, network call needing a project — `openfilm open` makes
  one). **Not re-run** here; search output only.
- No `get motion-search` verb — motions come from `get effect`
  (verified: `in-zoom`, `loop-ken-burns`). `npx openfilm@latest` is a
  moving tag; pin a source checkout or version.

## Environment isolation (verified)

First `open`/`look`/`render` downloads a ~94 MB headless Chromium and
ffmpeg; without `OPENFILM_LIBRARY`, projects land in
`~/Movies/OpenFilm/Projects`. Keep everything inside a vendor dir:

```bash
export OPENFILM_HOME=<vendor>/openfilm/home
export OPENFILM_LIBRARY=<vendor>/openfilm/projects
export PLAYWRIGHT_BROWSERS_PATH=<vendor>/openfilm/browsers
export OPENFILM_NO_BROWSER=1
export OPENFILM_NO_UPDATE_CHECK=1
```

`openfilm doctor` reports what is missing. `npm install` in
`packages/openfilm` runs a `prepare` build of the Studio UI (vite, ~19 s) — expected.

## Placement rules for ads

- Whoosh/transition on a cut lands **on** the cut frame or ~0.1 s before
  it; an impact lands on the payoff word, not the cut. SFX go on events
  and reveals only — see `pacing.md` for placement and levels.
- One transition family per ad. Whip cuts plus glitch plus ink reads as
  noise.
