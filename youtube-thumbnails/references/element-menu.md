# The element menu and the interview

Adapted from the open `youtube-thumbnail` skill in
https://github.com/hassancs91/claude-youtube-editor (read November 2026). It
renders thumbnails with an image model that also draws the text. Ours draws the
text itself, so some of its failure modes do not apply to us and are marked.

## The baseline look: always on, never asked

Every thumbnail, whatever the choices below: high contrast (deep darks or clean
brights, never flat), vibrant colour with one accent doing the work, a clear
hierarchy of at most three steps (headline, hero object, face), a big positive
face, and a clean finish with no clutter. The source says a before and after
comparison on views favoured the bold, high-contrast, hierarchical frame over the
flat one by about 4.4 times. That is one guide's before-and-after, not ours.

Our own study (`dataset-and-recreation.md`) found story and personal thumbnails
over-performing heavy branding, so "vibrant" must not become "loud and branded".

## The element menu: opt-in, one at a time

Start with one text element. Each text block you add must earn its place; the
source tried a full kit of headline, sticker, check strip and tag and the creator
rejected it as too much text.

| Element | What it is | Cost |
| --- | --- | --- |
| `single-hook` | One huge word or number | The default |
| `tiered-headline` | Small context line over a huge power line | One more text block |
| `sticker` | Tilted badge, two short words at most, an arrow to the hero | Garbles in a model; fine if the page draws it |
| `checkstrip` | A strip of three checked benefits | Busy; three micro-texts |
| `glow-burst` | Light and particles from the hero | Cheap, usually worth it |
| `results-fan` | Cards fanning out from the hero | Busy frame |
| `real-logo`, `real-app-screen` | A real logo or screenshot as a reference image | An extra reference; micro-text blurs at browse size |

Environments (pick one): dark studio (neon on black), real office (a candid
look anchored to a real room), bright graphic (a saturated studio composite).

## The interview: ask before you generate

One round of questions, skipping what the request already says:

1. Environment: dark studio, real office or bright graphic.
2. Text budget: `single-hook` (recommended), a headline plus one accent, or the
   full kit (warn that it is busy).
3. Extras: glow, results, a real logo, a real screen, a prop, or none.
4. Accent colour.

Then repeat the exact words back and check them against the locked title:
thumbnail text never repeats title words.

## Honesty and loudness

- **Promise only what the video keeps.** A thumbnail that bets on something the
  video does not deliver costs trust and, over time, clicks.
- Thumbnails are deliberately louder than the in-video brand. Do not tone one
  down to match the video.

## Iterate with letters and numbers

A new concept gets a new letter (A, B, C). A restyle of the same idea bumps the
number (A2, A3). Keep one test slot per letter family. Before you overwrite a
file keep the old one as `-v1`. Hold the random seed to iterate with a stable
composition, change it to explore, and change one thing at a time. After each
accepted render rebuild a labelled contact sheet so the set stays comparable at
browse-wall size.

## Verify every render before showing it

Read the image back and check: the hook is spelled right and legible, the face
reads as the creator, one focal element dominates, the expression is positive
and the colours vivid, the hands have five fingers and no phantom limbs, no stray
lettering in sub-images, hardware has no brand, the screen or props match the
real product, and the file is 16:9 under 2 MB. Fix and redo before the owner sees
it; flag anything borderline.

## Failure modes from that source

| Symptom | Fix |
| --- | --- |
| A badge word is garbled | Not an issue for us: the page draws the words. With a model, two short words and spell them letter by letter. |
| A laptop or phone shows a brand | Ask for a generic device, plain bezel, no logos or lettering. |
| Skin has a colour cast from a screen | Name the light: warm skin tones preserved, a faint cool glow from the screen. |
| A double or clone looks like a stranger | Say that both people in the image are this exact person; give the double a different material. |
| An office looks generic | Describe the real room in the reference photo and say to match it. |
| The word is spelled right but looks pasted on | Add a texture, a soft outer glow and a hard drop shadow. |
