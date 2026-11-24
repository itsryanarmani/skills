---
name: talking-head-graphics
description: "Use to turn a finished talking-head video (application, pitch, explainer; 1-3 min) into a Vox-style edit: your video morphs into a rounded side panel, one visual per beat sits on a torn-paper sheet, big words sit behind the speaker, sound effects and loudness are balanced, one colour grade. Local tools plus HyperFrames. Use when asked for graphics, b-roll, motion graphics, a Vox or paper-collage look, text behind the speaker, or a larger side panel instead of a small circle. Run talking-head-edit first."
---

# talking-head-graphics

Adds graphics to a talking-head cut that is already tight. Run `talking-head-edit`
first, then this. The look follows the paper-collage style of public Vox-style
explainers: torn paper, tape, halftone dots, one flat colour per beat. A public
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
bash $S/prep.sh in-edited.mp4 proj                # project, seekable base video, word times, sound effects
# put white SVG logos in proj/assets/logos (cdn.simpleicons.org/<brand>/ffffff)
# put paper-cut images in proj/assets/gen (see "Images")
cp $S/build.py proj/build.py                      # then edit its timeline block with times from proj/words.json
python3 proj/build.py proj                        # writes proj/index.html and proj/windows.txt
bash $S/cutouts.sh in-edited.mp4 proj             # one short cutout per text-behind window
(cd proj && npx -y hyperframes@0.9.91 snapshot --at 5,10,20 --no-end)   # look before you render
bash $S/render.sh proj final.mp4                  # render, grade, loudness, verdict (exit 0 = pass)
bash $S/e2e.sh                                    # 14 checks with stub tools, about 100 s; exit 0 = pass
```

`build.py` is a worked example. Its times, words and numbers are placeholders:
replace them. The output length comes from `assets/base.mp4`, and anything past
it is dropped. Never invent a number or a logo. Use the speaker's own numbers
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
6. **Few colours, one accent, one grade.** Three sheet colours (cream, muted
   blue, charcoal) and ink. One accent, used for the number that matters. Grade
   the whole film in the last pass (see "Colour grade").
7. **Paper sheets.** Each visual lands on a torn sheet: a white outer polygon, a
   coloured inner polygon, a halftone patch, two tape pieces. The sheet slides in
   from alternating sides. This is the transition.
8. **Continuity for numbers.** A growth claim is one counter and one line that
   draws from the start value to the end value, not two separate bars.
9. **Text behind the speaker** only for 2 or 3 big words, between the video and
   a cutout of the person. A window must start after the panel has morphed back
   to full frame (`build.py` enforces 0.7 s), or two copies of the speaker show.
   Check that 30 to 55% of the word is covered. One line is better than two.
10. **Real logos on ink tiles.** Show a brand only when the speaker names it.
    For a company with no logo in the library, use its name as type.
11. **Sound.** Effects from `earshot make` (no model, no network). `data-volume`
    scales the effect file, so it is not a level against the voice: `earshot make` prints each
    effect's loudness (-14 to -19 LUFS for these), so 0.2 to 0.3 puts them about 8
    to 17 dB under a -16 LUFS voice. Measure it. A loud effect can still mask a quiet
    word. `render.sh` normalises to -16 LUFS and passes only within 1 LU of that and at or
    below -1.0 dB peak.

## Colour grade

`render.sh` grades once, on the finished render, so the video and the graphics
match: `eq=contrast=1.06:saturation=0.86:gamma=0.98`, a warm `colorbalance`,
light grain and a small vignette. It lowers saturation about 14% and warms the
shadows. The cold blue of an office background clashes with the paper colours
without it.

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
- **Short beats.** `build.py` shortens a content entrance for a beat under
  about 1.35 s (the sheet entrance stays 0.85 s). Leave no gap with an empty panel between
  two beats.
- **The cutout is slow.** About 10 s per second of video on a laptop CPU. It runs
  only on the text-behind windows. A GPU machine helps only if `remove-background
  --info` lists `cuda` (the pinned version may need `HYPERFRAMES_CUDA=1`; not
  verified here).
- **Fonts.** `build.py` uses Inter by name. The HyperFrames compiler adds the
  font files at render. A `local()` `@font-face` fails on another machine.
- **Last line.** `check` warns when "Thank you" holds under 2 s. It is the
  speaker's own last word, so leave it.

## Verify the skill

`bash $S/e2e.sh` runs 14 checks with stub tools. `python3 $S/mutate.py` removes 12
fixes one at a time from a copy and shows that the check named for each fails
(about 6 minutes): the morph guard, the shift recheck, the base-length probe,
the image path, `immediateRender`, the window refusal, the measurement step, the
verdict target, the length check, the last-line read, the stdin guard and the
cutout failure. A stub cannot show real render quality: look at a
snapshot before you render.

## Cost

Per video: a handful of images, no model tokens for the render. The model reads
the word times once and writes the beat list. Most tokens go to re-reading a long
session, so start a new session for each video.
