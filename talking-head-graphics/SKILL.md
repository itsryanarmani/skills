---
name: talking-head-graphics
description: "Use to turn a finished talking-head video (application, pitch, explainer; 1-3 min) into a Vox-style edit: your video morphs into a rounded side panel, one visual per beat sits on a torn-paper sheet, big words sit behind the speaker, sound effects and loudness are balanced, one colour grade. Local tools plus HyperFrames. Use when asked for graphics, b-roll, motion graphics, a Vox or paper-collage look, text behind the speaker, or a larger side panel instead of a small circle. Run talking-head-edit first."
---

# talking-head-graphics

Adds graphics to a talking-head cut that is already tight. Run `talking-head-edit`
first, then this. The look follows the paper-collage style of public Vox-style
explainers: torn paper, tape, one flat colour per beat. A public
skill that makes a whole film from generated clips is `alisa0808/vox-director`
(MIT). This skill keeps the real footage and adds graphics on top.

Measured November 2026 on one 99 s, 1080p, 30 fps cut (Apple M3 Pro laptop,
HyperFrames 0.9.91, `-q looks`): prep about 1 min, a full-length cutout 16 min
(per-window cutouts: about 10 s per second of window), build 1 s, render 3.5 min
with one worker. Six paper-cut images from a GPT image model at the listed $0.06
each came to $0.36 (1024 x 1024). These come from one run on the author's laptop and are not a benchmark; no
log of it is saved.

## Run it

```bash
S=/path/to/skills/talking-head-graphics/scripts   # this skill's scripts folder
bash "$S/prep.sh" in-edited.mp4 proj                # project, seekable base video, word times, sound effects
# put white SVG logos in proj/assets/logos (cdn.simpleicons.org/<brand>/ffffff)
# put paper-cut images in proj/assets/gen (see "Images")
cp "$S/build.py" proj/build.py                      # then edit its timeline block with times from proj/words.json
python3 proj/build.py proj                        # writes proj/index.html and proj/windows.txt
bash "$S/cutouts.sh" in-edited.mp4 proj             # one short cutout per text-behind window
(cd proj && npx -y hyperframes@0.9.91 snapshot --at 5,10,20 --no-end)   # look before you render
bash "$S/render.sh" proj final.mp4 --pace 1.05 --end SECONDS   # render, grade, voice, trim, verdict (exit 0 = pass)
bash "$S/e2e.sh"                                    # 35 checks with stub tools, about 3 min; exit 0 = pass
```

`build.py` is a worked example. Its times, words and numbers are placeholders:
replace them. The output length comes from `assets/base.mp4`; a timeline that runs
past it is refused. `--end SECONDS` is the last good second of the base video (omit
it to keep the whole film). Never invent a number or a logo. Use the speaker's own numbers
and public logos only.

## Rules that made it work

1. **One visual at a time.** A beat shows one thing. Copies of one object (four
   logo tiles for four subscriptions) count as one, and so do two things that
   are one idea (a logo and its count). The next visual replaces
   the last. A first draft with 4 to 6 objects per scene was called "childish".
2. **The speaker stays, always on the same side.** While a visual plays, the
   video morphs into a rounded rectangle on the right quarter (530 x 900 px,
   radius 40, no border, soft shadow). Never switch sides: the speaker asked
   for one fixed side. A long pause between beats returns to full frame. A sheet stays on screen
   until the next sheet covers it, so an empty panel never shows. A small
   circle in a corner was too small.
3. **Show, do not tell.** Use as little text as possible. A beat about
   downloads shows the logo and the number, nothing else. Use a paper-cut image
   for an idea (a rocket for "accelerator", a crowd for "users"). Words stay
   only when they are the content (a title, a name, a term).
4. **One style for every graphic.** Paper-cut images, flat logo tiles and type
   only. A glossy emoji-like bulb beside a logo tile read as two mismatched
   visuals. If an image does not match, drop it.
5. **Morph, do not cut.** Animate `clip-path` on a wrapper and `x`, `y`, `scale`
   on an inner wrapper. Never move the media element itself.
6. **Few colours, one accent, one grade.** Two sheet colours (cream and muted
   blue; add charcoal only for a dark beat) and ink. One accent, used for the number that matters. Grade
   the whole film in the last pass (see "Colour grade").
7. **Paper sheets, and one effect at a time.** Each scene is one torn sheet (a
   coloured torn polygon with paper grain, a soft shadow and two tape pieces; the
   edges boil between three hand-cut variants on a 12 fps grid) with the
   visuals that play on it. No decorative dots or shapes: a halftone patch under
   a logo "did not make sense" and distracted. A scene change is the sheet and
   the speaker panel moving together. Then a pause (0.25 s after the sheet has
   settled). Then the visuals fade in on the stable sheet. Inside a scene only the
   visuals change, by fade, and never at the same time as the sheet. The sheet
   always comes in from the right and leaves to the left. When three things moved
   at once (sheet, graphic and a text exit), the speaker found it too much.
   `build.py` refuses a timeline that breaks this (see "Review checklist").
8. **Continuity for numbers.** A growth claim is one counter and one line that
   draws from the start value to the end value, not two separate bars.
9. **Text behind the speaker** only for 2 or 3 big words, between the video and
   a cutout of the person. A window must start after the panel has morphed back
   to full frame (`build.py` enforces 0.7 s), or two copies of the speaker show.
   Check that 30 to 55% of the word is covered. One line is better than two.
10. **Real logos on ink tiles.** Show a brand only when the speaker names it.
    For a company with no logo in the library, use its name as type.
11. **Sound.** Effects from `earshot make` (no model, no network). A soft `paper`
    page turn (0.16 to 0.2) when a sheet moves and the deep `whoosh_big` (0.12) on the
    first big word, with a soft `coin` on a second one. No `tick` or `pop`: the speaker found the transition sounds too
    high and too loud next to the voice. `data-volume` scales the effect file, so
    measure the result; a loud effect can still mask a quiet word. `render.sh`
    targets -14 LUFS (the speaker found -16 quiet) and passes only within 1 LU of
    the target and at or below -1.0 dB peak.
12. **Opening: the name and nothing else.** A name tag bottom left. A role line or
    a big title word behind the speaker is a distraction.
13. **Pace first, clone last.** For energy use `render.sh --pace 1.05` (pitch
    kept) and the built-in presence boost. A cloned voice needs lip-sync over the
    whole film (about $8 for 99 s if the listed $0.084 of one lip-sync model is per second; unit not verified) and a synthetic voice on a real face must be
    labelled. Ask before you do it.
14. **End before the speaker looks away.** Look at the last 2 s of frames and set
    `--end` to the last frame where they still look at the camera.

## Before you build: storyboard, 30 s test, three questions

Adopted from public projects (ideas only; see "Sources"):

1. **Write a storyboard table first**, one row per spoken phrase: the phrase, the
   one visual, what it does on screen, the sound. No table, no project. Delete
   any row where the visual only repeats the words.
2. **Render a 30 s test first** (`render.sh --end 30`). Show it. Build the rest
   only after approval. For a batch of videos, approve the look once, then reuse it.
3. **Three questions on the test, captions covered:** what is this, what is it
   doing, what did I learn? A vague answer means the visual is wrong.

## Sources

I read their docs and style files and adapted the ideas. No code was copied.

- `cth9191/animate` (MIT), cut-paper style: torn edges with soft shadows, paper
  grain, and text on paper tags (never bare type). Adopted: sheets with grain, text
  on paper tags, one wall colour per scene.
- `Vincentwei1021/mg-styles-15` (MIT), collage prompt: motion held on a 12 fps grid
  with 1 to 2 px jitter, paper and scissor sounds, mastered to -14 LUFS and
  -1 dBTP. Adopted: the 12 fps edge boil, the paper-page sound, the loudness target.
- `HeyChengC/vibe-knowledge-film` (GitHub shows no machine-readable licence, so ideas only): storyboard before
  build, a 30 s test first, a three-question self-review.
- `showheyohtaki/motion-prompt` (MIT): a vocabulary for camera moves and effects.
  Not adopted: constant camera motion works against "one effect at a time".
- Not used: `pixelfx` (pixel art), `huashu-motion` (generates a whole film),
  `story-studio` (Jianying draft), `video-editor-skills` (needs paid DaVinci Resolve
  and bars commercial use).

## Colour grade

`render.sh` grades once, on the finished render, so the video and the graphics
match. The first grade (contrast up, saturation down, a vignette, grain) made the
speaker's under-eyes dark and the speaker looked tired. The current one keeps blacks
near 0 so logo tiles stay black, lifts only the mid-shadows (a curve
through 0.12 to 0.17 and 0.25 to 0.33), adds saturation 1.08 and a warm
`colorbalance`. Always compare a face crop of the original and the graded frame
before you accept a grade: the eyes and the skin must look lively.

## Images

Make paper-cut images with a text-to-image model on a pure white background,
then key the white: `ffmpeg -vf "format=rgba,colorkey=0xFFFFFF:0.16:0.10"`. Use
this for coloured objects. The automatic person cutout removed a blue box and a
purple laptop from two images, so use it for people only. Prompt: "Layered
paper-cut collage illustration, soft shadows between layers, muted palette of
cream, warm grey, charcoal and one terracotta accent, one centered subject, pure
white background, no text." `mix-blend-mode: multiply` did not render, so key the
white out of the file.

## Traps

- **Check disk first.** The default render stores every frame on disk. With under
  5 GB free on the temp disk (or 1 GB on the output disk) `render.sh` uses
  `--workers 1`, which streams into the encoder (2,979 frames in 3.5 min in the
  measured run).
- **Read `check` from its saved report.** `check --json` prints about 600
  progress lines. Read the JSON path it names and count issues by `code`.
  `nested_structure_needs_subcomposition` is a style warning, not an error.
- **GSAP `fromTo` draws its start values at once.** For a shared element that
  moves many times, every later move then shows its start state at time 0 (a
  stray panel before the first beat). Add `immediateRender:false` to those
  state moves only, and `gsap.set` the first state. One-shot entrances keep the
  default so they start hidden.
- **The cutout is slow.** About 10 s per second of video on a laptop CPU. It runs
  only on the text-behind windows. A GPU machine helps only if `remove-background
  --info` lists `cuda` (the pinned version may need `HYPERFRAMES_CUDA=1`; not
  verified here).
- **Fonts.** `build.py` uses Inter by name. The HyperFrames compiler adds the
  font files at render. A `local()` `@font-face` fails on another machine.
- **Last line.** `check` warns when "Thank you" holds under 2 s. It is the
  speaker's own last word, so leave it.

## Review checklist (run before you show a draft)

- Text is on a paper tag, not bare on the sheet, and every number is the speaker's own.
  Enforced by `paper_craft_details_are_present` for big and number text; labels inside a
  diagram (the Venn circles, the chart's axis label) may be bare. The same check covers
  sheet grain, the 12 fps boil, and content centred beside the panel.
- The 30 s test was shown and approved before the full render.

Each line was a real complaint. `build.py` and the tests enforce the ones marked.

- Opening shows only the name. (rule 12)
- No decorative dots or shapes. (rule 7)
- One effect at a time: sheet and panel together, then a pause, then fade-in
  visuals. Enforced: `pace_visual_waits_for_sheet`, `pace_sheet_waits_for_last_visual`,
  `pace_visuals_do_not_overlap`, `pace_visual_gone_before_sheet_leaves`.
- After the return to full frame starts (the morph takes 0.65 s), wait 0.7 s before the
  next scene and 1 s before a word appears behind the speaker. Enforced: `pace_wait_after_return_to_full`,
  `pace_word_waits_after_morph`, `pace_cutout_starts_after_morph`.
- The speaker shows once, always on the right. Enforced: `build_refuses_bad_windows`
  (a cutout never overlaps a morph or the panel). Also look at frames at each scene change.
- The word behind the speaker appears on the spoken word. (rule 9)
- Under-eyes and skin look lively after the grade. (Colour grade)
- Transition sounds are deep and quiet; the voice is at -14 LUFS. (rule 11)
- The film ends before the speaker looks away. (rule 14)
- Every scene, visual and element id is unique, and no visual runs past the video. Enforced: `build_refuses_duplicate_ids`, `build_refuses_duplicate_element_ids`, `build_refuses_visual_past_the_video`.
- Logos only for named brands. (rule 10)

## Verify the skill

`bash "$S/e2e.sh"` runs 35 checks with stub tools. `python3 "$S/mutate.py"` removes 40
fixes and rules one at a time from a copy and shows that the check named for each
fails (about 25 minutes). A stub cannot show real render quality: look at a
snapshot before you render.

## Cost

Per video: a handful of images, no model tokens for the render. The model reads
the word times once and writes the beat list. Most tokens go to re-reading a long
session, so start a new session for each video.
