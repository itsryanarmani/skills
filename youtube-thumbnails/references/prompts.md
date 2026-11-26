# Prompts

## The pose prompt

`thumbnail-poses` builds each prompt from one base and one pose line:

```text
Use the man in the reference photos exactly: same face, hair, clothes.
Photorealistic 16:9 YouTube thumbnail photo. Soft even studio lighting.
He fills the right 45% of the frame from the waist up; the left half is empty
clean background reserved for text. No text, no logos, no watermark, no extra
props unless stated. Flat solid studio background colour: <colour>. Pose: <pose>.
```

Set the person with `--who`, `--he`, `--his`, `--him`. Keep "no text". Keep the empty left half.

## The 25 poses

Tag, background, pose line. The best expression for each is in `tactics.md`.

| Tag | Background | Pose |
| --- | --- | --- |
| pointing | vivid orange | points toward the empty left side, friendly look |
| surprised | royal blue | wide eyes, hand on cheek |
| thumbsup | bright yellow | big smile, thumbs up |
| armscrossed | charcoal | arms crossed, calm smile |
| card | warm cream | holds a blank card up |
| thinking | forest green | hand on chin, eyes up and left |
| presenting | purple | both palms up toward the left |
| waving | teal | waves hello |
| finger | red | leans in, one finger raised |
| candid | light grey | relaxed natural laugh |
| shocked | royal blue | mouth open, hands up by the face |
| sad | deep navy | downturned mouth, slumped shoulders |
| headhands | orange | both hands on top of the head |
| pointup | bright yellow | points straight up |
| pointcam | magenta | points at the camera, smirk |
| facepalm | charcoal | one hand over the face |
| mindblown | teal | hands open beside the head |
| shush | deep purple | finger on lips |
| fistpump | green | fist in the air, big smile |
| shrug | cream | palms up, half smile |
| skeptical | light blue | one brow up, head tilted |
| angry | red | furrowed brows, fist |
| laugh | light grey | big natural laugh |
| frame | dark green | hands framing a screen |
| pleading | soft pink | hands pressed together |

## Prompts for images with no person

Use these for a background, an object, or a scene. Ask for negative space for
text and no embedded type.

- "Clean 16:9 composition, restrained natural palette, realistic contrast, one
  clear subject on the right, empty space on the left, no text, no logos."
- Split: "Left side dark and messy, right side bright and tidy, clear dividing line
  in the centre, high contrast." (before and after)
- Object: "One hero object, dramatic rim light, dark gradient background, shallow
  depth of field." (product or tool)
- Scene: "Overhead flat lay of a tidy desk with a laptop, warm light, bright clean
  background." (tutorial)

Do not ask the model to draw the title. Draw it in the page.

## When a pose fails

| Problem | Fix |
| --- | --- |
| A different face | Add a clearer front reference. Rerun the tag with `--force`. |
| Extra or missing fingers | Rerun the tag. Pick a pose with hands low or out of frame. |
| Gradient or vignette | Rerun. The page still reads the colour from the top-left pixel. |
| Text or a logo appears | Rerun and repeat "no text, no logos" at the end of the prompt. |
| Person too small or too far left | Add "fills the right 45 percent, waist up" again. |
