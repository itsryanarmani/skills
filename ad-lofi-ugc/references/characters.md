# The consistent synthetic character

One recurring person across many stills and clips, without drift. The method
is boring on purpose: fix every variable except the scene.

## 1. Write the character bible once

One paragraph, fixed fields: age range, build, hair (style + color),
marks (freckles, brows), outfit (garment + color + fabric), signature prop,
voice (pitch, pace, accent). Paste the **same paragraph verbatim** into every
image prompt and every image-to-video prompt. Never paraphrase between shots —
drift comes from re-describing the character differently.

Template:

```
<NAME>, a fictional <person> in their <late 20s>, <build>, <hair
style+color>, <marks>, no makeup, wearing <garment> over <underlayer> and
<bottoms>, <one accessory>, holding <prop> and <prop2>.
```

Example (genericized from the run that produced it):

```
A fictional woman in her late 20s, athletic build, shoulder-length
dark-brown wavy hair, light freckles across her nose, no makeup, wearing an
olive-green oversized hoodie over a white tee and black joggers, one white
wireless earbud in her right ear, holding a yellow legal pad and a black
pen.
```

One recurring character fixes one demographic. In a housing campaign, vary the
character across ad sets. See the policy note in `prompts-images.md`.

The character is synthetic. No real person, no real name needed.
The character is never a past customer. The voiceover never describes a
result the person got. A first-person selfie or voiceover from a synthetic
"customer" is an implied testimonial, and the FTC fake-reviews rule and Meta
policy treat it that way. Frame comedy skits as dramatizations. Label any
person who could pass as real as AI-generated, every time.

## 2. Generate an anchor contact sheet first

Before any scene or video shot, generate one small contact sheet: front
portrait, three-quarter, profile, one full-body shot — same outfit, same
lighting. Approve it once. Then:

- Image-to-image/edit pipelines: pass the approved anchor as the reference
  image and ask only for the scene change.
- Video models with image input: feed the anchor or a per-shot still as the
  first frame. First-frame conditioning is the biggest consistency lever —
  always prefer it over text-to-video for a recurring character.

## 3. Lock the variables, vary only the scene

Hold constant across all prompts: outfit, hairstyle, background palette,
camera height (eye level or slight wide), aspect ratio, and the camera/era
style if the whole batch shares one. Change only: location detail,
expression, prop position, action. Each changed variable is a drift
opportunity.

## 4. Fixed negative block

Append the same short block to every prompt:

```
No logos, readable text, watermark, studio light, HDR, perfect skin, kids,
celebrities, or brands. Same face, same outfit, correct five-finger hands.
```

## 5. Verify before animating

For each still, compare against the anchor: face shape, hairline, outfit
color, prop. A side-by-side contact sheet or a cheap vision-model pass
catches drift while regeneration is still one call. Reject and retry with
the anchor attached — do not re-roll blind.

## 6. Chain last frames shot-to-shot

Within one video, the character never "re-enters":

- Take the **last frame of shot N** (extracted from the real rendered clip,
  not a designed still).
- Use it as the `image` (first frame) input for shot N+1.
- Set shot N+1's `last_image` to that shot's designed still, so the clip
  morphs onto the intended composition.
- Keep every shot's last frame on disk. A failed shot regenerates from its
  predecessor's frame, not from scratch.

This is how pose, lighting and wardrobe carry over by construction instead of
by prompt luck.

## 7. Voice is separate from face

Pick one TTS voice once; reuse the same voice id for every clip and every
re-take. Write lines at the same pace — short sentences, roughly 2.5 words
per second. If a line is re-voiced, regenerate the whole shot's audio; never
splice two takes of the same line.

## 8. When drift still happens

- Reduce the shot's novelty: simpler background, fewer props, character
  closer to camera (face fills more of the frame = easier to match).
- Switch the shot to a format that needs the face less: over-the-shoulder,
  hands-and-object, screen-with-voiceover.
- Keep the anchor contact sheet as a permanent reference attachment if the
  tool supports persistent characters.

## Per-shot checklist

- [ ] Character paragraph pasted verbatim (not reworded)
- [ ] Anchor image attached as reference / first frame
- [ ] Only scene variables changed
- [ ] Fixed negative block appended
- [ ] No generated text — captions added in edit
- [ ] Vision-check pass before image-to-video
- [ ] Same TTS voice id as the rest of the pack
