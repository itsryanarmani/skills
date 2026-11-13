# Image prompts and the lo-fi degrade

The prompt rule that worked, then the exact prompts, then the ffmpeg recipes
that make a clean generation look like a 2000s camera-roll photo.

## Policy first

- Housing ads (listings, foreclosures, rentals) run in the Housing Special Ad
  Category on Meta. Use no audience exclusions. US Fair Housing Act ad rules
  apply too.
- Do not copy the race, age or gender of the example people. Choose the
  people on purpose and vary them across a batch. Do not pair one group with
  distress scenes such as notices on doors or locked doors.
- A fake security-camera still can look like real footage. Do not present it
  as a real event.

## The prompt order rule

Write every image prompt in this order:

1. **Camera and era first.** Name the device, the year, the lens behavior.
   This sets the whole image: "Photo taken on a 2004 point-and-shoot digital
   camera, direct flash, 640x480 look." The era decides the flaws for you.
2. **Subject and moment.** Who, what they are doing, the one thing the viewer
   should notice. Ordinary people, ordinary rooms, slightly worn clothes.
   Unglamorous beats aspirational for this format.
3. **Flaws.** Motion blur, off-center framing, thumb at the edge of frame,
   blown highlights, crushed shadows, noise, compression, slightly crooked.
   Pick the flaws that match the camera you named.
4. **Negatives.** A fixed tail: "No logos, readable text, watermark, studio
   light, HDR, perfect skin, kids, celebrities, or brands." Add "Correct
   five-finger hands" when a hand is prominent — models still mangle hands,
   but the phrase helps.

Why this order works: camera-first anchors the model to a real distribution
of photos (grunge, flash, bad composition) instead of its default "good photo"
prior. Subject-second keeps the ad relevant. Flaws-third sells the realism.
Negatives-last fences off the failure modes.

## Exact prompts that worked

These are verbatim from a 12-ad batch that shipped (model
`bytedance/seedream-v5.5` (as of 2026-11-12), 1.5k resolution, 9:16 then cropped). Swap the
subject for your niche; keep the structure.

**Stooped figure + mail (2004 point-and-shoot):**

```
Photo taken on a 2004 point-and-shoot digital camera, direct flash, 640x480
look. Ordinary unglamorous woman about 48 [vary the person on purpose], messy bun, no makeup, faded
navy sweatshirt, slumped on a cracked ranch-house stoop holding blank
envelopes. Weeds, blank paper taped to the door, subject centered. Motion
blur, off-center, thumb at the edge, overexposed flash, blown highlights,
crushed shadows, noise, compression, slightly crooked. No logos, readable
text, watermark, studio light, HDR, perfect skin, kids, celebrities, or
brands.
```

**Nervous selfie at a locked door (2011 iPhone 4 front camera):**

```
2011 iPhone 4 front-camera selfie, slightly out of focus. Ordinary
unglamorous man about 32 [vary the person on purpose], short hair, gray hoodie, laughing nervously
with his mouth half open, standing too close to a scuffed brown door on a
vinyl-sided house. One correct five-finger hand holding the phone at the
bottom, subject centered. Soft focus, off-center, overexposed LED flash,
blown highlights, crushed shadows, noise, compression, slightly crooked. No
logos, readable text, watermark, studio light, HDR, perfect skin, kids,
celebrities, or brands.
```

**Drive-by mansion through a car window:**

```
Blurry phone photo taken through a car window. Huge stone mansion with
columns and a circular driveway, seen from the street as the car rolls
past, no people. Dirty glass, windshield reflection, black weatherstrip at
the left, rain smear, overgrown median. House centered. Motion blur,
off-center, thumb at the edge, blown highlights on the stone, crushed
shadows, noise, compression, slightly crooked. No logos, readable text,
watermark, studio light, HDR, cinematic grading, kids, celebrities, or
brands.
```

**Night-vision doorbell still:**

```
Screenshot of a doorbell/security camera still, fisheye, night vision.
Grainy green monochrome porch from a camera above the door. Ordinary
unglamorous woman about 35 [vary the person on purpose] in a dark jacket looking at a completely
blank white sheet taped to the door, zero letters, zero signature. Fisheye
warps the rails. No timestamp, no date, no camera brand. Subject centered.
Off-center, blown porch-light, crushed shadows, heavy noise, compression,
slightly crooked. Correct five-finger hands. No logos, readable text,
watermark, studio light, HDR, perfect skin, kids, celebrities, or brands.
```

Camera/era styles that worked, reuse them freely:

- `2004 point-and-shoot digital camera, direct flash, 640x480 look`
- `2011 iPhone 4 front-camera selfie, slightly out of focus`
- `2009 flip-phone camera photo, grainy, soft focus`
- `disposable film camera, flash, red-eye, light leak`
- `blurry phone photo taken through a car window`
- `screenshot of a doorbell/security camera still, fisheye, night vision`
- `photo of a printed notice on a door taken at an angle with a phone`

## The degrade: stills

The generation is only half the look. Every still gets crushed through
ffmpeg so it reads as a real old photo. Order matters:

1. Tiny rotation (1–3 degrees) so the horizon is crooked. Rotation exposes
   black corners. Crop the centre 90% right after the rotate to remove them.
   A 93% crop still leaves a dark corner at 3 degrees (measured). Scaling
   up and cropping to the same size does NOT remove them.
2. Scale down to ~720 px wide (the "old camera" resolution crush).
3. Slight blur + grain.
4. Desaturate, crush contrast a touch.
5. JPEG re-encode at quality 40–60, then decode back to PNG so the
   compression artifacts are baked into the pixels.
6. Scale back up to 1080×1920 (or your target) and crop.

The 4:5 feed crop is a tighter crop of the same crushed 9:16 still, not a
second generation. Keep a per-concept `crop_y` offset so faces and the key
object stay in frame.

```python
# Concept fields per still: rotate_deg (1-3), jpeg_q (40-60), n (variant int)
# Example values: blur=0.8, noise=18, sat=0.8
import math
deg, blur, noise, sat = 2.0, 0.8, 18, 0.8
angle = deg * math.pi / 180
vf_9 = (
    f"rotate={angle}:c=black:ow=iw:oh=ih,"
    f"crop=iw*0.90:ih*0.90,"                    # removes the black corners
    f"scale=720:-2,"
    f"gblur=sigma={blur},"                      # 0.7-1.0
    f"noise=alls={noise}:allf=t+u,"            # 14-26
    f"eq=saturation={sat}:contrast=0.93:gamma=0.97:brightness=-0.02,"  # sat 0.78-0.84
    f"scale=1080:1920:force_original_aspect_ratio=increase,"
    f"crop=1080:1920"
)
# ffmpeg -i src.png -vf "<vf_9>" -frames:v 1 -q:v <8..15> tmp.jpg
# ffmpeg -i tmp.jpg -frames:v 1 out_9x16.png        # bake artifacts in
# ffmpeg -i out_9x16.png -vf "crop=1080:1350:0:<crop_y>" -frames:v 1 out_4x5.png
```

JPEG quality 40–60 maps to ffmpeg `-q:v` roughly 8–15 (lower = better). The mapping is approximate and unverified. Vary
`rotate_deg`, `jpeg_q`, `noise` and `sat` slightly per ad so a 12-ad batch
does not look like one photo duplicated.

## The degrade: video

Same idea on moving footage, as one ffmpeg filter chain. This recipe produced
the shipped clips:

```text
scale=540:-2,
scale=1180:2084,
crop=1080:1920:x='45+10*sin(t*11.3)+4*sin(t*5.7)':y='82+8*cos(t*9.1)+3*sin(t*3.7)',
scale=1080:1920,
noise=alls=9:allf=t+u,
gblur=sigma=0.55,
eq=saturation=0.74:contrast=0.96:brightness=-0.01,
format=yuv420p,setsar=1
```

Read it as: crush to 540 px wide, blow back up past the frame, then crop with
a slow sinusoidal jitter — that jitter is the handheld shake and the reason
for the overscan. Then grain, blur, desaturate, encode. Tune the `sin`/`cos`
frequencies and amplitudes to taste; keep the shake subtle.

## Text rule (repeated because it cost money)

Image models garble text. "Blank white sheet" prompts still produced readable
junk letters on two of three tries for one ad. Do not ask for "a sign that
says X" or "a notice with text". Ask for "a completely blank white sheet, zero
letters, zero signature" — and even then, assume some renders fail and QA
them. All readable text (captions, headlines, end cards) is painted in HTML
via headless Chrome to a transparent PNG and overlaid with ffmpeg, or burned
in a later pass. ffmpeg `drawtext` was not compiled into the local binary on
the run machine; the Chrome-PNG path gives exact letters and web fonts.
