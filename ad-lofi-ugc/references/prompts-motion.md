# Image-to-video motion prompts

How to animate a lo-fi still without the model inventing a new video.

## The core rule: keep motion small

The still already carries the look. The video model's only job is to make it
breathe like phone footage. Every prompt that worked asked for one small
motion and then fenced off everything else.

Working pattern:

```
<one small motion>, <one small secondary motion>, <camera texture>,
<film-look descriptor>, one continuous shot, no walking, no cuts
```

Then, when the scene has a phone, a person holding an object, or anything the
model could morph, add explicit negatives:

```
Do not add a person. Do not add a phone. Do not cut. Do not zoom in.
```

## Motion prompts that shipped

From a 5-clip batch (`wavespeed-ai/wan-2.2/i2v-480p-ultra-fast` (as of 2026-11-12), 5 s, 480p,
9:16 stills as first frame). All passed QA.

**Person holding still, slow push-in:**

```
tiny handheld camera shake, very slow push-in toward the blank white yard
sign, she keeps pointing at the sign and stands still, grass barely moves,
grainy flip-phone video, one continuous shot, no walking, no cuts
```

**Selfie, small reaction:**

```
tiny handheld selfie shake, he slightly turns his head toward the camera
with a nervous laugh, natural blink, phone stays in his hand, grainy iPhone
4 front-camera video, one continuous shot, no walking, no cuts
```

**Drive-by through a window (the hard case — needed the long negative block):**

```
Keep this exact composition the whole time: looking through a dirty car
side window at a stone mansion. The car rolls slowly so trees, a metal
fence, weeds, and the road slide past the window. Raindrops stay on the
glass. A thumb stays at the bottom edge. The mansion stays in frame. Do not
add a person. Do not add a phone. Do not cut. Do not zoom in. Tiny handheld
shake only.
```

**Second drive-by, shorter form:**

```
handheld phone shot through a dirty car window at dusk, slow drive-by, a
streetlight streak slides on the glass, the brick mansion windows stay lit,
passing trees, tiny camera shake, one continuous shot, no people, no cuts
```

**Person standing in a scene:**

```
tiny handheld camera shake, very slow push-in, she stands still in the
weeds facing the house, grass barely moving, grainy flip-phone video, she
does not turn around, one continuous shot, no walking into the house, no
cuts
```

## What to keep small

- **Camera motion**: tiny shake, very slow push-in, slight drift. The degrade
  pass adds its own sinusoidal jitter — do not double up on shake.
- **Subject motion**: one gesture (pointing, a laugh, a blink, looking down).
  The subject mostly holds still.
- **Environment motion**: grass "barely moves", trees slide past because the
  car moves, rain stays on glass.
- **Duration**: 5 s clips worked well. Short clips mean less time for the
  model to drift.
- **Resolution**: 480p i2v was enough; the degrade pass hides the softness.
  Upscaling happens in the degrade, not in the model.

## What to avoid

Each of these caused a real failure:

- **Walking, running, entering a building** — invites morphs and new people.
  If the story needs movement, cut to a new shot instead.
- **Cuts or scene changes inside one clip** — the model smears them.
- **Zooms** — warps faces and hands.
- **Anything that adds a hand, phone, person or prop not in the still** —
  the model will invent one, and it will be wrong. Name the held objects in
  the prompt ("phone stays in his hand") and then say "do not add a phone".
- **Text in any form** — the model paints garbled lettering on signs, phones
  and UI. Keep text out of the still and out of the prompt.
- **Big emotional performances** — crying, dancing, fast gestures break
  character consistency and anatomy. Small tells (a nervous laugh, a deadpan
  stare) survive; big ones do not.
- **Prompting the degrade** — do not ask the video model for "grainy" or
  "VHS". The still's era does that; the degrade does it again for free.

## Shot chaining

For multi-shot videos, do not text-to-video each shot. Chain:

- Shot 1: `image` = designed still.
- Shot N>1: `image` = the **last frame of clip N-1** (the real rendered
  frame, not a guess), `last_image` = shot N's designed still. The clip
  morphs from the previous ending onto the intended composition, so the
  character and lighting carry over.
- Save every shot's last frame to disk. If a shot fails QA, regenerate it
  from its predecessor's frame, not from scratch.

See `characters.md` for the full method.
