---
name: youtube-thumbnails
description: "Use to design and export YouTube thumbnails (1280x720) that show a real person: pick a popular layout, generate many poses of the person (shocked, sad, pointing, hand on head and more), draw exact text over them, test at phone size, and check the file. Covers the 20 common thumbnail formats, expression and colour rules, checklists, and a pose prompt library. Use when asked for a thumbnail, a video cover, better click-through, thumbnail styles to choose from, or thumbnails for many videos at once."
---

# youtube-thumbnails

A thumbnail has one job: make the right person click. This skill goes from a few
reference photos to checked 1280x720 files. The model makes the photos. The page
draws the text, so no word is ever misspelled. A person picks the layout.

For the video itself use `talking-head-edit`. For ad images use
`ad-creative-generation`. This skill does not upload anything.

## Run it

Needs `wavespeed` (key in `WAVESPEED_API_KEY`), Chrome, and optionally `ffmpeg`.
The scripts are `thumbnail-poses` and `thumbnail-export` in the scripts repo.
The gallery page is in `assets/gallery/` (its `README.md` shows the folder and `config.example.json` the items).

```bash
mkdir -p gallery/poses
cp assets/gallery/index.html gallery/                    # the template
cp assets/gallery/config.example.json gallery/config.json   # then edit: one item per video
thumbnail-poses --dry-run --out gallery/poses            # prompts and cost, no network
thumbnail-poses --ref front.jpg --ref smile.jpg --out gallery/poses --yes
python3 -m http.server 8765 --directory gallery          # open http://127.0.0.1:8765/
thumbnail-export --gallery gallery --out thumbs --layout 5 --item all
```

For anyone other than a man, add `--who "the woman" --he she --his her --him her`
to `thumbnail-poses`. Layouts above 24 need a transparent `gallery/cutout.png`.
`thumbnail-export` fails a thumbnail when the page reports a problem (unknown
layout, missing pose, text too small), so read every row.

## Cost

About $0.07 per pose, $1.75 for all 25 (a pose that writes no file is retried once, so at worst twice that). Layouts and export are free (local
Chrome). Measured November 2026 on `openai/gpt-image-2/edit`; 15 poses took under 10
minutes with 3 parallel runs. A second model, `google/nano-banana-2/edit`, cost
the same. In one side-by-side sample (n=1) it looked less like the person, so
compare both on your own photos before a large batch.

## What the agent does

1. **Read the video's one idea** and its title. The thumbnail must not repeat the
   title. It adds a feeling or a question the title cannot.
2. **Get two or three reference photos** with different expressions and a clear
   front view. Say that they will be uploaded to WaveSpeed and ask before `--yes`.
3. **Generate poses** with `thumbnail-poses`. Look at every pose at full size
   against the checklist in `references/checklists.md`. Redo a bad tag with
   `--force --tags TAG`.
4. **Open the gallery** for one real item. Show the person the 34 layouts, the
   pose strip, and the 120 px test. Do not pick for them. Let them choose a
   layout and optionally one pose for all.
5. **Export** with `thumbnail-export` for all items. Read the JSON lines. Every
   row must say `"ok": true`.
6. **Look at three exports at full size** and one at 120 px. Then hand the files
   over. Upload only when the person asks.

## Hard rules

- 1280x720, 16:9, at most 2 MB, PNG or JPEG.
- One idea, one focal point. Text is at most four words (six at the very most),
  bold, high contrast, and readable at 120 px wide.
- Three colours at most. Face fills 30 to 50 percent of the frame.
- Nothing important in the bottom-right corner (the duration badge) or the very
  edge. Keep the bottom-left clear too (chapter marker).
- **The model never writes text.** Image models misspell. The gallery page draws
  every word from `config.json`.
- Do not copy another creator's thumbnail. Take the format, not the artwork.

## Boundaries

- Generated poses are not photographs. Use your own face, or a person who agreed
  in writing. Do not show an event that did not happen as if it did, and do not
  make a false claim about a person, product or result.
- A real cutout (`cutout.png`, a transparent PNG made from real footage) keeps
  the original pixels. Prefer it when the thumbnail must show a real moment.
- Do not upload, publish or send anything without the owner's go-ahead.

## References

- `references/formats.md`: the 20 popular formats and how each maps to a layout.
- `references/tactics.md`: expressions, colour pairs, text, composition, tests.
- `references/checklists.md`: before, per pose, per layout, export, upload.
- `references/prompts.md`: the 25 pose prompts and prompts for no-person images.
- `references/inspiration.md`: where the rules come from and where to look.
