# Study real thumbnails, then recreate one

Rules from opinion go stale. This reference says how to collect real, recent
thumbnails with their numbers, how to read them without fooling yourself, and
how to recreate a reference with your own person and words.

## 1. Collect

Use `thumbnail-dataset` (scripts repo). It searches the official YouTube Data API
read-only, and writes `dataset.jsonl`, `dataset.csv` and `thumbs/<id>.jpg`.

```bash
thumbnail-dataset --out data --queries-file queries.txt --max 30 --published-after <a year ago> --dry-run
thumbnail-dataset --out data --queries-file queries.txt --max 30 --published-after <a year ago>
```

- Write 20 to 30 queries from your niche, plus a few from the format names in
  `formats.md` ("I tried every", "the ugly truth about").
- Sort by `viewCount`, then judge by `outlier` (views over subscribers) and
  `views_per_day`. A video that beats its own channel says more about its
  thumbnail than raw views do.
- The images are other people's work. Keep them local, for study. Do not
  republish them and do not commit them.

## 2. Clean

- **Drop vertical Shorts.** The API cannot tell a 61 to 180 s Short from a video.
  Their thumbnails are 9:16 clips letterboxed into 16:9, with blurred or dark
  sides. In a first run, 106 of 562 thumbnails were these, and 50 of the first
  120 "top" picks. Flag them: the sides have far less edge detail than the
  centre (mean edge energy under 0.35 of the centre's) and the duration is under
  about 190 s. Look at the flagged ones; a dark slide can trip it.
- Keep the label set balanced: the biggest over-performers and the biggest
  under-performers, not the middle.

## 3. Label

Label each thumbnail with one schema: `format` (the 20 in `formats.md`, plus
`face_plus_big_text`, `object_or_scene_only`, `other`), `has_face`, `expression`,
`face_size`, `face_side`, the exact `text`, `word_count`, `text_position`,
`text_colors`, `dominant_colors`, `bg_type`, `contrast`, `elements`, `hook_type`.
Use a vision model, or cheap subagents that read numbered contact sheets of 12
thumbnails. Validate every value against the allowed list. Spot-check a sheet by
eye: do not trust labels you did not look at.

## 4. Read it as hints

First study (November 2026): 562 thumbnails from 424 channels, 225 labelled
(120 top, 105 bottom outliers, vertical Shorts removed). The labels came from a
small model reading contact sheets, and their accuracy was not measured.
"Top share" is top divided by top plus bottom, from raw counts; the groups differ in size (120 against 105).

| Feature | Top / bottom | Top share |
| --- | --- | --- |
| Story hook ("my layoff journey", "I quit at 53") | 16 / 2 | 89% |
| News headline layout | 1 / 10 | 9% |
| Photo background | 83 / 52 | 61% |
| Studio background | 5 / 17 | 23% |
| No text at all | 12 / 2 | 86% |
| Text at the bottom of the frame | 12 / 29 | 29% |
| Medium-size face | 30 / 52 | 37% |
| Face in the centre | 32 / 44 | 42% |
| Logos present | 40 / 60 | 40% |
| Red text | 22 / 43 | 34% |
| Orange, brown or yellow in the palette | 27 / 13, 16 / 7, 27 / 16 | 63 to 70% |
| A face at all | 93 / 96 | 49% |

What this suggests, and no more: personal and story thumbnails over-performed
their channels; heavy branding, news banners, studio sets and red text under-
performed; text low in the frame (where the duration badge sits) did badly.

What it does not show. The bottom group is mostly large, polished channels, so
"polished" may just mean "big". The top group has small channels with one lucky
video. Topic and title are not controlled. The counts are small. **A face did not
beat no face in this sample**, which is a reason to test your own, not to drop
faces. Repeat the study on your niche before you change a rule.

## 5. Recreate a reference

Goal: learn why it works by building the same composition with your own person
and words, never to copy it.

1. Pick a reference with a clear layout (top outlier, short text, a face).
2. Give the image model three inputs: two or three photos of your person
   (identity) and the reference (composition only).
3. Prompt: copy the layout, colour palette, background style, face size and side,
   expression and the kind of props. Do **not** copy the person, logos, brands,
   artwork or any words. Keep the area where text sits as clean background. No text.
4. Lay your own words on top with a script, not the model: pick the text box from
   the label (`text_position`), fit the font to the box, and choose the colour
   from the box's brightness (dark words on a dark area are unreadable). Draw a
   stroke in the opposite tone.
5. Compare the pair at full size and at 120 px. Look for copied artwork.

What a first run of 10 showed. The model transfers composition, palette, pose and
expression well (a hand-on-window pose, pointing at a document, a raised finger).
It copied one small icon from a reference until told not to, so look at every
result for borrowed artwork and redo it. Words laid on afterwards were exact, but
the first pass put dark text on a dark area, which the brightness check fixed.
Keep the recreations local, beside the originals, for study.
