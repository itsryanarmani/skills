---
name: ad-video-styles
description: "Use when you need a short paid-social VIDEO ad for a service and want a previously used structure with exact prompts: a photo-motion feed video (4:5, one still animated, static headline panel under it), a call-out story video (9:16, about 15 s, three generated shots, burned captions, end card), or a lo-fi story with two recurring characters, an action hook, per-line voice and a Hyperframes post edit. Covers how to pick a style from a viral-video library, the detailed shot and caption prompts, the ffmpeg build, costs, and the failures that cost money the first time (animated text, base64 bodies, captions over hands, faces that look at the camera)."
---

# ad-video-styles

Two video ad styles with prompts you can paste. Both were used in a small paid-social
test for a B2B service. No results are claimed here: the test had not read out when this
was written. Both are built from generated footage and a static overlay, so the type
comes from a browser render, not from the video model, and the cost stayed near one
dollar a video.

Pairs with `ad-research-to-creative` (what to say), `ad-video-scripts` (longer
scripts), `ad-creative-templates` (static versions of the same ads) and
`ad-test-launch` (where the finished video goes).

**Hard rule: do not show a finished video to anyone until `scripts/video-ad-check.py` exits 0.** Section 6 says
how. Looking at a few frames is not a check: a video once went out with its captions a full second ahead of
the voice because nobody measured it.

## 0. Pick the style before you write anything

Before you open any library of viral short-form videos, read its terms and robots.txt. As read by the
owner in Nov 2026, the DarkUGC terms forbid scraping and any automated access, including bots, scripts,
headless browsers and AI agents, and its robots.txt disallows `/api/`. The exception for agents is the MCP
server the site names, used with an account the owner signs in to. So: an agent uses that MCP server and
nothing else on that site. Do not fetch its pages or API with a tool, do not fake a User-Agent or Referer to
pass a block, and do not save or quote its counts. If a request is blocked, stop. A person can still browse
the site by hand.

Other sources you can use as a starting point, each under its own license or terms: open-source hook and
prompt repositories (for example `rediumvex/viral-hooks-skill` and `Reviral-ai/awesome-ai-ugc-ad-prompts`)
and the Meta Ad Library API. Look for the structure, not the topic. Two structures carried over to a B2B service:

| Structure seen | Intended effect (not measured here) | Use it for |
|---|---|---|
| Niche call-out in the first second ("All <buyers>, ATTENTION") then a quick demo | The right viewer should self-select at once and others scroll on | Story video, section 2 |
| A trap or twist: the obvious answer is wrong | The viewer should stay for the payoff | A later style; needs a writer |

Copy the structure. Never copy the clip, the face, the words or the music. A library is
inspiration, not footage to reuse.

State one claim per video, and only claims the owner has confirmed. A video
that says "in 2 weeks" must match what the service delivers.

## 1. Style A: photo-motion feed video (4:5, 5 s)

One still photo of a person at work, animated slightly, with the static
headline panel stacked underneath. Use it when you already have a still ad that
works and want a moving version for the feed.

Do not animate the finished ad. An image-to-video model warps lettering. Animate
the photo alone and add the panel afterwards.

### Step 1: the photo

Use a photo with no text, no logo, nobody looking at the camera, and a screen
or paper angled away. Prompt pattern for the photo (image model):

```
A <age> <person>, <ethnicity>, <hair and clothes with one worn detail>, <doing the
work>. Eyes stay on the task, no direct eye contact with the camera. Dressing: <three small believable objects>. Light:
<window light plus one warm lamp, slightly mixed>. Shot on a full-frame camera,
35mm at f/2.8, slightly below eye level, candid documentary look, unretouched
skin with pores. NOT WANTED: no text, no lettering, no logo, no badge, no plastic skin, no studio polish.
```

### Step 2: the motion prompt (image-to-video)

```
Subtle documentary motion: <one small action that fits the photo, for example
the doctor slowly turns a page>, small natural head movement, warm lamp flicker,
slow gentle push-in. Nobody looks at the camera. No text.
```

Settings that worked: model `bytedance/seedance-v1-pro-fast/image-to-video` on
WaveSpeed, `duration` 5, `resolution` 480p, with a 4:5 input photo. One observed output was 480x608, which is
close to 4:5: run `ffprobe` on the clip and adjust the crop before you stack.
Cost: about USD 0.085 per clip, read from the gateway balance in Nov 2026. It excludes
retries and the still photo.

### Step 3: stack the panel

Render the static ad once as a 1080x1350 PNG. The top 800 px is the photo, the
bottom 550 px is the panel. Cut the panel and stack it under the clip:

```bash
ffmpeg -y -i clip.mp4 -loop 1 -i static-ad.png \
  -filter_complex "[0:v]scale=1080:-2,crop=1080:800:0:<y>[top];[1:v]crop=1080:550:0:800[bot];[top][bot]vstack=inputs=2,format=yuv420p[v]" \
  -map "[v]" -t 5 -r 24 -c:v libx264 -crf 20 -movflags +faststart out.mp4
```

`<y>` is the crop offset that keeps the face in frame, usually 160 to 170. The
480p source is upscaled, so it looks soft on a large screen. That is fine in the
feed.

## 2. Style B: call-out story video (9:16, about 15 s)

New footage, not a moving still. Three generated shots, a burned caption on each,
and a 3 s end card. No speech and no logo, so it works with sound off.

### Structure

| Time | Shot | Caption (small tag, then big line) |
|---|---|---|
| 0 to 4 s | The buyer at the moment of the problem | "For <buyers>" then "ATTENTION" |
| 4 to 8 s | The expert doing the service | "Need an" then "<service name>?" |
| 8 to 12 s | The fix: the buyer finishes the one-step action and relaxes | "<one proof point>" then "<one claim>." |
| 12 to 15 s | End card, static | headline, two chips, button, address |

### Shot prompts (text-to-video)

Keep one sentence of action, one of light, one of camera, then the not-wanted
list. Replace the bracketed words.

```
Shot 1: A [buyer role] in [her/his] [age range] at an office desk, tired, flipping
through a thick stack of printed pages with a highlighter, a cold coffee beside
[her/him], overcast window light plus overhead fluorescents, handheld documentary
camera, slow push-in.

Shot 2: A [expert role] in [his/her] [age range] in a quiet office examining
[the evidence object] on a wall light box, then turning to write notes on a paper
pad at the desk, warm lamp light, handheld documentary camera.

Shot 3: Close view of a person at a desk finishing an online form on a laptop with
the screen angled away from the camera, then leaning back and exhaling with
relief, soft daylight, handheld documentary camera.

Add to every shot: No text, no lettering, no logos, eyes stay on the task and no
direct eye contact with the camera, no handshake, no patient, no brand.
```

Settings that worked: model `bytedance/seedance-v1.5-pro/text-to-video-fast` on
WaveSpeed, `aspect_ratio` `9:16`, `duration` 5, `resolution` 720p. Cost: about
USD 0.35 per shot, so about USD 1.05 for the video (read from the gateway balance
before and after, Nov 2026; it excludes retries and captions). Prices change, and a gateway can retire or
silently swap a model: check the model page and its availability before a batch, and
confirm the model id in the job result.

### Captions and end card

Render each caption as a transparent 1080x1920 PNG with a headless browser. We prefer this
to ffmpeg `drawtext` because it gives web fonts, balanced line breaks and a text shadow
in one place. Layout that worked: a filled
pill tag (44 px, white on the brand colour) above a 112 px serif line (white, soft
dark shadow), left aligned, 60 px side margin, top of the block at y 1180 so it
sits in the lower third. The end card is a solid background with the same type. Render it at exactly 1080x1920.

### Assemble

Every segment must share size (1080x1920), frame rate (24), pixel format (yuv420p) and
codec, or the stream-copy join breaks.

```bash
# 4 s of each shot with its caption: s1-raw.mp4 + cap1.png, s2-raw.mp4 + cap2.png, ...
for i in 1 2 3; do
  ffmpeg -y -i "s$i-raw.mp4" -i "cap$i.png" -filter_complex \
   "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=24,trim=duration=4,setpts=PTS-STARTPTS[v];[v][1:v]overlay=0:0,format=yuv420p[o]" \
   -map "[o]" -t 4 -c:v libx264 -crf 20 "seg$i.mp4"
done
# 3 s end card (a 1080x1920 PNG)
ffmpeg -y -loop 1 -t 3 -i endcard.png -vf "fps=24,format=yuv420p" -c:v libx264 -crf 20 seg4.mp4
# join
printf "file 'seg1.mp4'\nfile 'seg2.mp4'\nfile 'seg3.mp4'\nfile 'seg4.mp4'\n" > list.txt
ffmpeg -y -f concat -safe 0 -i list.txt -c copy -movflags +faststart story.mp4
ffprobe -v error -show_entries stream=width,height,r_frame_rate:format=duration -of default=nw=1 story.mp4
```

## 3. Style C: lo-fi story with two recurring characters (9:16, about 15 s)

Use it when you want a story, not a moving still. It is organic and handheld on purpose: no logo, no
designed layout, ordinary generated people caught mid-moment, one plain caption per shot. The owner rejected polished
text-on-card ads in an earlier round and chose this direction; no performance result is claimed here.

### Structure: shock, then a turn, then one clear answer

| Time | Beat | Rule |
|---|---|---|
| 0 to 3 s | A real accident or shock, in action (a slip and a crash, a laugh, a cry) | The first 2 s must show it. Speed the clip up 2 to 2.5x so the whole event fits. |
| 3 to 9 s | The turn: time passes and two sources disagree | One sentence per cut. Name who is who with a sketch label. |
| 9 to 13 s | The one-step action (a form, a call) and relief | Same two people. |
| 13 to 16 s | The one claim the owner confirmed, then the address | Hold the last line at least 2 s. |

Use 8 to 10 cuts. Each shot runs 1.2 to 2.1 s. Zoom-punch on every cut.

### Script: plain, short, spoken

Write like a person talking to a friend, in short active sentences (ASD-STE100 style), then strip
announcer phrasing. Lines of 1 to 3 seconds each beat one long paragraph. Make it personal and give it one
thread: one narrator who is in the story, a clock that moves ("That was March." "It's July."), and a
cross-cut that ties the scenes together (the narrator is on the phone, the other character is on the
phone). A list of unrelated scenes reads as disconnected, even when each looks good.

```
I watched Dave go down. / I ran to him. That was March. / It's July. Still on the phone. /
His doctor says he can't work. / The file says he can. / So I sent one form. /
<service name>. <confirmed claim>.
```

### Every cut must make sense

A cut needs a reason a viewer can follow: the action continues, the place changes with a clear cause, or the narrator
says what we are looking at. A running woman cut to a close-up of her face while the voice said "That was March" read as stuck
and confused. Cutting to her kneeling beside the man on the floor (the moment itself) worked. Step through every cut and ask
what the viewer thinks happened between the two frames.

### Two characters that stay the same

1. Make one reference portrait per character with the image model. Give each a fixed look: age, hair,
   one loud garment (an orange vest, a teal blouse), a plain lanyard with a blank card.
2. Make every scene with an image-edit model (for example `bytedance/seedream-v5.5/edit` on WaveSpeed,
   about USD 0.03) and pass the reference portrait(s) as `images`. Prompt: "Person 1 is the person in
   reference image 1: keep their exact face, hair, age and clothes", then the scene. Scenes with both
   characters pass both references in order.
3. Prompt the hook still as the peak of the action ("both feet in the air, boxes toppling"), then animate it.

Without references the same "person" changed in every shot and viewers could not tell who the last
actor was.

### Voice: human, per line, picked by measurement, not sped up

You cannot hear the take, so measure it. A system voice (macOS `say`) was robotic, and even a good model
read the hook line flat: its pitch range was 3.7 semitones. Lively takes of the same line measured 7 to 15.

1. Use an expressive model with emotion tags (for example `elevenlabs/eleven-v3` through a model gateway that bills by
   character; a line of about 40 characters cost well under one cent). Give every line its own specific tag
   (`[shaken, quiet]`, `[tired]`, `[flat, bitter]`, `[relieved, softly]`). Generate each line as its own file so it lands on its cut.
2. Do not use breath or sound tags such as `[exhales]` or `[sighs]` at the start of a line. They came back as a 0.7 s
   breath that delayed the first word, and once as the spoken word "huh".
3. Generate 3 takes per line, clean each (below), and measure it with `scripts/prosody.py`. Keep the take with the widest pitch
   range that passes: range 6 semitones or more, no pause over 0.5 s, no unvoiced lead-in over 0.35 s. `scripts/pick-voice.py`
   does the loop and caches takes by line, voice and model, so a changed line never reuses old audio. Its lead-in trim only
   cuts an unvoiced start over 0.35 s, so a hard "s" or "f" keeps its start.
4. Clean each take: cut silence at both ends, squeeze any silence inside the line to 0.07 s, and cut a lead-in breath.
   Squeezing is what removes the dead air between a line's sentences:
   `silenceremove=start_periods=1:start_threshold=-40dB:start_silence=0.03,silenceremove=stop_periods=-1:stop_duration=0.18:stop_threshold=-40dB:stop_silence=0.07,areverse,silenceremove=start_periods=1:start_threshold=-40dB:start_silence=0.03,areverse`
5. Place the lines 0.04 s apart. Gaps of 0.15 s plus pauses inside lines read as dead air.
6. Do not speed the voice up: speed up the picture, not the voice.
7. An audio-listening model scored every take 7 to 9 of 10 and could not tell them apart. Do not use it as the judge.

### Cuts and captions come from the voice, never from the picture

Build the timeline backwards from the audio so sync holds by construction:

1. Generate each line, trim edge silence, and place every line on one clean voice track at a known start time.
2. Run speech-to-text on that clean track for word times (`npx hyperframes transcribe voice.wav --json`).
   It often reports the first word at 0.0 s after leading silence: anchor each line's first word to its placed start.
3. Check that the spoken words equal the script words. Stop if they differ.
4. Cut on phrase starts (a cut about 0.05 s before the first word of a phrase). Captions are the spoken words in
   chunks of 2 to 3 words, each from its first word to the next chunk. Never caption a whole line early.
5. Write a manifest for the checker as you build (section 6).

### Post edit with Hyperframes (HTML to MP4)

Hyperframes renders a composition written in HTML with `data-*` timing and one paused GSAP timeline.
Run `npx hyperframes lint`, then `npx hyperframes check`, then
`npx hyperframes render --quality high --output out.mp4` (about 40 to 50 s for 16 s of 1080x1920 on an
Apple-silicon laptop).
What to know:

- Put each `<video>` directly under the root. A `<video>` inside a wrapper that has its own `data-start` is an
  error (`video_nested_in_timed_element`); an untimed wrapper is allowed. Put the zoom on the video element itself.
- Retime with `data-playback-rate` on the clip (2.5 for the hook). Audio is separate `<audio>` clips.
- Captions, labels and arrows are separate top-level timed elements. Give them explicit `z-index`.
- A `local()` font fell back to a serif in the renderer. Ship an open hand-drawn font file (for example
  Permanent Marker, OFL) in `assets/` and load it with `@font-face`.
- Keep overlays sparse. Sketch arrows on every cut read as too much: use no arrows, and at most two small
  marker labels that say who is who the first time each person appears. If you must draw one arrow, aim it: a guessed one pointed at
  an empty hallway.
- `check` flagged three labels as "occluded" that were clearly visible in the render. Treat that flag as a
  hint: confirm on rendered frames before you change anything.
- No whooshes on cuts. They sat too loud next to the voice. Keep one crash and thud on the hook and a very quiet room tone (volume 0.25). The checker fails any non-voice sound within 12 dB of the voice after the first 1.6 s.
- No dark bar behind the captions: white text with a black outline reads fine, and the bar looked heavy.
- Never let a clip run past its own length. A hook clip sped up 2.5x froze for its last 0.3 s. Check `start + duration x rate` against the clip length in the build, and fail the build if it does not fit.
- Sound effects need no stock library: pink noise through a lowpass for a crash, a 55 Hz sine for a thud,
  a short highpassed noise burst for each cut. Use licensed music from the ad platform at upload.

### QA that caught real problems

| Check | What it caught |
|---|---|
| First and last frame of every clip | A phantom camera grew in a hand. Fix: re-run with "hands stay resting in her lap, nothing in her hands". |
| One frame per cut in the render | An arrow aimed at empty floor; a label font that fell back to a serif. |
| Mute test | Every beat needs a caption so the story reads without sound. |
| Cost meter | Image-to-video clips (`wan-2.2/i2v-480p-ultra-fast`, 5 s, 480p) cost USD 0.05 to 0.09 each, measured from the balance in Nov 2026. Log every call and set a hard cap in the script. |

Label it as a dramatization with AI-generated people and voice. Never present it as a testimonial.

## 4. Rules for the people in the footage

- They are generated, unnamed people at work. They are illustrations, not staff
  or clients. Never put a real person's name, a credential or "our doctors" next to a face. In a labelled dramatization, a fictional first name and a role tag ("me. HR.") for a character is fine.
- Nobody looks at the camera, nobody speaks a claim, no patient is shown.
- No logo or brand on any device, garment or wall. Ask for plain devices.
- Check the platform's rule on labelling AI-made people. Label if it applies.

## 5. Failures that cost time or money

| Failure | What happened | Fix |
|---|---|---|
| Animating the finished ad | Lettering warped and melted | Animate the photo only; add the panel after |
| Sending the image inline | `curl -d "$body"` died: argument too long | Write the JSON to a file and use `-d @file` |
| Captions over the hands | The caption hid the action in shot 3 | Move the block up or shorten the line; watch the whole video |
| Small wallet on the model gateway | A second gateway had USD 0.86 left, too little for the top model | Read the balance before each batch; use the cheaper model for tests |
| A fake "screen" in the footage | The model drew a browser with unreadable text | Angle screens away or crop them; the ask is "no lettering" |
| Rebuild wipes work | A script re-ran every paid call | Skip a shot when its raw file already exists |

## 6. Checks before you hand over a video

`scripts/video-ad-check.py` fails the video unless every check passes. Run it on the final render with the
manifest the build wrote and the transcript of the CLEAN voice track:

```bash
python3 scripts/video-ad-check.py out.mp4 --manifest manifest.json --transcript voice.transcript.json
python3 scripts/prosody.py t1.wav t2.wav    # for the voice takes: pitch range, pauses and lead-in, fails a flat or gappy take (needs numpy)
bash scripts/test.sh    # the checker's own failure cases (needs ffmpeg)
```

The manifest holds `duration`, `size`, `allow` (confirmed claims such as `"2 weeks"`), `muted` (true only for a
video with no voice) and lists of `shots`, `voice` lines, `captions`, `labels` and `arrows`, each with `start`, `end`
and text. The transcript is required for any video with a voice. The checker measures:

| Check | Fails when |
|---|---|
| `size`, `duration`, `audio-present` | the size differs from the manifest, the length differs by over 0.3 s, or there is no audio (unless `muted`) |
| `cut-pace`, `hook-cut` | a shot runs over 3 s or under 0.8 s, the average is over 2.5 s, or the first shot is over 2.5 s |
| `no-freeze` | the picture freezes for 0.25 s or more (a clip was sped up or cut past its own length), or the analysis fails to run |
| `hook-motion` | the first 2 s barely move (mean frame change under 15; a sped-up fall measured 21, the slow cut 13) |
| `voice-present` | no voice lines and not `muted`, or the voice is not at least 6 dB above the gaps (and above -45 dB) in its window |
| `voice-onset` | the voice in the rendered audio starts more than 0.30 s from the manifest (level threshold is 12 dB under the median voice level, never below -50 dB, so speech with no gaps works) |
| `dead-air` | a gap between voice lines is over 0.45 s, or the rendered audio is silent for over 0.5 s inside a line, including a silent tail |
| `sfx-level` | after the first 1.6 s, a non-voice sound comes within 12 dB of the voice outside the spoken lines; pass `--sfx effects.wav` (the effects track alone) to measure inside them too, because the mix cannot show it |
| `audio-level` | the peak is above -1 dB or the mean is below -35 dB |
| `caption-length`, `sync-manifest` | a caption has over 6 words, starts more than 0.25 s from its voice line, or ends more than 0.15 s before the line ends |
| `mute-coverage` | the captions for a spoken line do not spell it word for word, or are on screen for under 85% of it (overlaps are not double counted) |
| `sync-transcript` | no transcript; the spoken words differ from the script; the captions skip a spoken word, leave the end of the speech uncaptioned, or say something else; or a caption is more than 0.35 s from its words (captions that share no word with the voice, such as an address end card, are skipped) |
| `overlay-density`, `label-hold` | more than 2 labels or 1 arrow, or a label is on screen under 1 s |
| `claims` | after removing each phrase in `allow`, a caption still has a digit, percent sign, dollar sign, or the word guarantee or risk-free |

Rules for whoever runs it:

- A FAIL means fix the build and render again. Do not edit the manifest to match a wrong video, and do not lower a
  threshold to pass.
- The transcript is not optional: no transcript is a FAIL, not a skip.
- The checker cannot see everything. After it passes, still step through the cuts and look for an object that
  appears or vanishes, an arrow or label aimed at the wrong thing, and scenes that do not follow each other.
- Hand over only the file that passed, and say which checks ran.

## 7. Before it goes live

1. Watch each finished video start to end at full size, and step through every cut. One
   frame per shot misses short distortions, stray text and captions that cover the hands.
   Check size, length and caption placement.
2. Confirm every claim in the caption with the owner and keep the proof.
3. Add UTMs and the ad id to the link, as in `ad-test-launch`.
4. Add the video as a new ad in a new test; never edit a live ad.
