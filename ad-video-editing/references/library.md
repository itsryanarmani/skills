# OpenFilm CC0 library

OpenFilm (MIT code) ships a free media library under `library/` in its
repo: sound effects, music, transitions, camera motions, effects,
filters, text looks, stickers and templates. Verified on disk and via
its CLI on 2026-11-12.

## What it contains (verified counts)

| Kind | On disk | Notes |
|---|---|---|
| Bundled SFX | 21 `.m4a` in `library/sounds/` | whoosh, boom, hit, riser, ding, pop, click… local files, copy directly |
| SFX + music catalogs | ~6,600 entries | metadata in `search.json`; files download on `--take` |
| Transitions | 61 dirs | dissolve, dip-black, glitch, ink, light-leak, whip-family… |
| Motions | 64 dirs | `cut-whip-*`, `cut-zoom-through`, `in-whip`, `loop-ken-burns`… punch-in/whip vocabulary, each with `preview.mp4` |
| Effects / filters | 71 / 66 | grain, vignette, light-leak, VHS; color grades |
| Text / stickers | 148 looks + ~1,600 rows | titles, karaoke cue styling; 1,587 emoji (MIT) + arrows |

`library/search.json` holds 8,744 rows; each carries id, keywords and
descriptions in several languages, so search works in any language.

## License (quoted from `library/LICENSE.md`)

> "Everything in OpenFilm's library can be used in any film, commercial or
> not, changed and shared, with no need to credit anyone. … These are
> dedicated to the public domain under CC0 1.0."

Exception: `stickers/emoji/` are Microsoft Fluent Emoji under MIT — keep
`library/LICENSE.md` with any copied assets.

## How to use it

Preferred path for our pipeline: copy the `library/` tree once into our
assets area, then search our own copy — no runtime dependency on their
CLI.

To search with their CLI (verified working, offline for bundled files):

```bash
CLI="node <vendor>/openfilm/src/packages/openfilm/bin/openfilm.mjs"
$CLI get sfx-search --prompt "whoosh impact" --limit 8
$CLI get sfx-search --prompt "cash register" --sec 1 --limit 5
$CLI get transition --prompt "quick whip left"
$CLI get effect --prompt "punch in zoom"     # motions live under `effect`
$CLI get music-search --prompt "tense drone" --sec 15
```

- Bundled hits print a local `hear it:` path — copy the file.
- Catalog hits print `openfilm/audio/sfx/<slug>.mp3` and "its file is not
  on this computer". `--take <id>` downloads the file into a project's
  `assets/` — free and CC0, but a network call that needs a project
  (`openfilm open` makes one). **Not re-run** here; search output only.
- There is no `get motion-search` verb; motions come back from
  `get effect` (verified: `in-zoom`, `loop-ken-burns`).
- `npx openfilm@latest` is a moving tag. Pin a source checkout or version.

## Environment isolation (verified)

First `open`/`look`/`render` downloads a ~94 MB headless Chromium and
ffmpeg into the browsers path. Without `OPENFILM_LIBRARY`, projects land
in `~/Movies/OpenFilm/Projects`. Keep everything inside a vendor dir:

```bash
export OPENFILM_HOME=<vendor>/openfilm/home
export OPENFILM_LIBRARY=<vendor>/openfilm/projects
export PLAYWRIGHT_BROWSERS_PATH=<vendor>/openfilm/browsers
export OPENFILM_NO_BROWSER=1
export OPENFILM_NO_UPDATE_CHECK=1
```

`openfilm doctor` reports what is missing. `npm install` in
`packages/openfilm` runs a `prepare` script that builds the Studio UI
(vite, ~19 s) — expected, registry-only.

## Placement rules for ads

- Whoosh/transition on a cut lands **on** the cut frame or up to ~0.1 s
  before it; an impact lands on the payoff word, not the cut.
- Keep SFX under voice: about 0.35 linear gain is OpenFilm's own default;
  our measured bed sat -1.4 to -3.6 dB under voice.
- One transition family per ad. Whip cuts plus glitch plus ink reads as
  noise.
