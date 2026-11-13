---
name: ad-video-styles
description: "Use when you need a short paid-social VIDEO ad for a service and want a proven structure with exact prompts: a photo-motion feed video (4:5, one still animated, static headline panel under it) or a call-out story video (9:16, about 15 s, three generated shots, burned captions, end card). Covers how to pick a style from a viral-video library, the detailed shot and caption prompts, the ffmpeg build, costs, and the failures that cost money the first time (animated text, base64 bodies, captions over hands, faces that look at the camera)."
---

# ad-video-styles

Two video ad styles with prompts you can paste. Both ran in a small paid-social
test for a B2B service. Both are built from generated footage and a static
overlay, so the type is always sharp and the cost stays near one dollar a video.

Pairs with `ad-research-to-creative` (what to say), `ad-video-scripts` (longer
scripts), `ad-creative-templates` (static versions of the same ads) and
`ad-test-launch` (where the finished video goes).

## 0. Pick the style before you write anything

Open a library of viral short-form videos (DarkUGC is a free one, with an MCP
server) and sort by views. Look for the structure, not the topic. Two structures
carried over to a B2B service:

| Structure seen | Why it works | Use it for |
|---|---|---|
| Niche call-out in the first second ("All <buyers>, ATTENTION") then a quick demo | The right viewer self-selects at once and everyone else scrolls | Story video, section 2 |
| A trap or twist: the obvious answer is wrong | The viewer stays for the payoff | A later style; needs a writer |

Copy the structure. Never copy the clip, the face, the words or the music. The
library is inspiration, not footage to reuse.

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
work, eyes on the task>. Dressing: <three small believable objects>. Light:
<window light plus one warm lamp, slightly mixed>. Shot on a full-frame camera,
35mm at f/2.8, slightly below eye level, candid documentary look, unretouched
skin with pores. NOT WANTED: nobody looks at the camera, no text, no lettering,
no logo, no badge, no plastic skin, no studio polish.
```

### Step 2: the motion prompt (image-to-video)

```
Subtle documentary motion: <one small action that fits the photo, for example
the doctor slowly turns a page>, small natural head movement, warm lamp flicker,
slow gentle push-in. Nobody looks at the camera. No text.
```

Settings that worked: model `bytedance/seedance-v1-pro-fast/image-to-video` on
WaveSpeed, `duration` 5, `resolution` 480p. The clip returns at 480x608 (4:5).
Cost: about USD 0.085 per clip.

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

Add to every shot: No text, no lettering, no logos, nobody looks at the camera,
no handshake, no patient, no brand.
```

Settings that worked: model `bytedance/seedance-v1.5-pro/text-to-video-fast` on
WaveSpeed, `aspect_ratio` `9:16`, `duration` 5, `resolution` 720p. Cost: about
USD 0.35 per shot, so about USD 1.05 for the video (measured from the balance
before and after).

### Captions and end card

Render each caption as a transparent 1080x1920 PNG with a headless browser. Do not
use ffmpeg `drawtext`: fonts and kerning are poor. Layout that worked: a filled
pill tag (44 px, white on the brand colour) above a 112 px serif line (white, soft
dark shadow), left aligned, 60 px side margin, top of the block at y 1180 so it
sits in the lower third. The end card is a solid background with the same type.

### Assemble

```bash
# 4 s of each shot with its caption
ffmpeg -y -i sN-raw.mp4 -i capN.png -filter_complex \
 "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=24,trim=duration=4,setpts=PTS-STARTPTS[v];[v][1:v]overlay=0:0,format=yuv420p[o]" \
 -map "[o]" -t 4 -c:v libx264 -crf 20 segN.mp4
# 3 s end card, then join
ffmpeg -y -loop 1 -t 3 -i endcard.png -vf "fps=24,format=yuv420p" -c:v libx264 -crf 20 seg4.mp4
ffmpeg -y -f concat -safe 0 -i list.txt -c copy -movflags +faststart story.mp4
```

## 3. Rules for the people in the footage

- They are generated, unnamed people at work. They are illustrations, not staff
  or clients. Never put a name, title, credential or "our doctors" next to a face.
- Nobody looks at the camera, nobody speaks a claim, no patient is shown.
- No logo or brand on any device, garment or wall. Ask for plain devices.
- Check the platform's rule on labelling AI-made people. Label if it applies.

## 4. Failures that cost time or money

| Failure | What happened | Fix |
|---|---|---|
| Animating the finished ad | Lettering warped and melted | Animate the photo only; add the panel after |
| Sending the image inline | `curl -d "$body"` died: argument too long | Write the JSON to a file and use `-d @file` |
| Captions over the hands | The caption hid the action in shot 3 | Move the block up or shorten the line; check one frame per shot |
| Small wallet on the model gateway | A second gateway had USD 0.86 left, too little for the top model | Read the balance before each batch; use the cheaper model for tests |
| A fake "screen" in the footage | The model drew a browser with unreadable text | Angle screens away or crop them; the ask is "no lettering" |
| Rebuild wipes work | A script re-ran every paid call | Skip a shot when its raw file already exists |

## 5. Before it goes live

1. Look at one frame per shot at full size.
2. Confirm every claim in the caption with the owner and keep the proof.
3. Add UTMs and the ad id to the link, as in `ad-test-launch`.
4. Add the video as a new ad in a new test; never edit a live ad.
