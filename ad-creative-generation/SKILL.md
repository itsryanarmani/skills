---
name: ad-creative-generation
description: "Generate ad-creative IMAGES with an AI image model (gpt-image-1 style) — the generations vs edits endpoints, feeding a brand logo + a competitor ad as STYLE references via edits (recreate the style, never clone people or marks), prompt patterns for photoreal lifestyle/product-in-context ads, the hard rule that image models GARBLE exact text/logos/UI (so review-cards, pills, iMessage belong in HTML templates not gen), a VISUAL-QA loop that passes each render to a vision model to catch defects and auto-regenerates failures, and batch/library organization. Model-agnostic. Use when producing photoreal ad creatives at scale from an image model; pair with ad-creative-templates for text/UI-heavy styles."
---

# ad-creative-generation

How to generate ad-creative **images** with an AI image model (examples use a gpt-image-1-style API: a `generations` endpoint and an `edits` endpoint that accepts reference images). Model-agnostic. This skill is for the **photoreal / lifestyle / product-in-context** half of ad creative. The text/UI/logo-heavy half (review cards, pills, iMessage, bold-text-on-color) belongs in HTML templates — see `ad-creative-templates` and §4 below.

## 1. Pick the endpoint first

Two different tools:

- **`generations` (text → image)** — a brand-new scene from a prompt. Product hero shots, lifestyle scenes, abstract/backdrop art, poster backgrounds.
- **`edits` (text + reference image(s) → image)** — modify or compose from inputs while preserving something. Use it to: place a real product photo into a new scene, apply a *style* from a reference, relight/recompose, or composite multiple inputs.

Rule of thumb: no real asset to preserve → `generations`. A real product photo / logo / style you must honor → `edits`.

## 2. Reference images: logo + a competitor ad as STYLE

`edits` takes reference images. Two useful ones for ads:

- **The real product photo or brand logo** — so the render shows *your* thing, not a hallucinated look-alike.
- **A competitor ad you admire** — as a **style reference only**.

Index and describe each input by position, and say how they interact:

> "Image 1: the product. Image 2: a style reference. Recreate the *composition, palette, lighting and mood* of Image 2 as an original scene featuring Image 1. Do NOT copy any text, logo, face, person, or trademark from Image 2 — style only."

**The hard rule on style references — recreate, don't clone.** Borrow layout / color / lighting / mood. Never reproduce another brand's marks, copy, or the identifiable people in their ad. Cloning a competitor's logo or model is a legal and trust problem, not a creative one. State the exclusions explicitly in the prompt ("no logos, no trademarks, no text, no recognizable faces from the reference").

For the **brand logo**, treat it as a protected element ("preserve the logo in Image 1 exactly — do not restyle, recolor, or redraw it") — but still verify it in QA (§5). Image models are unreliable on exact marks even from a reference; if the logo must be pixel-exact, don't gen it — composite it in a template (§4).

## 3. Prompt patterns for photoreal ads

Anchor believability with **photography language**, and structure every prompt the same way. A compact, borrowed-and-proven order:

**Subject → Setting → Light/Look → Camera → Technical.** (The "SLCT"-style skeleton from open ad-prompt guides — fill each slot, don't free-associate.)

- **Product-in-context (lifestyle):** the product in a real environment, in use. "A [product] on a sunlit kitchen counter, morning light from a window at left, shallow depth of field, 50mm, eye-level medium close-up." Real environment > floating-on-white when the goal is *desirability*.
- **UGC / founder ad:** unpolished, phone-shot realism. "Handheld phone photo, slightly imperfect framing, natural indoor light, honest and unposed. Real skin texture, everyday detail. No studio polish, no heavy retouching, no glamorization." The tells of an *ad* (perfect studio light, glossy retouch) are exactly what kills UGC performance — forbid them. For the camera-and-era-first prompt order plus the ffmpeg degrade that makes a generation read as a real 2000s camera-roll photo, see `ad-lofi-ugc`.
- **Testimonial / social-proof scene:** a believable person in a real setting — but **do not render the quote, stars, or name as image text** (it will garble; §4). Generate the *scene*, overlay the words in a template.
- **Photoreal realism dials:** name the lens (50mm), the light ("soft coastal daylight"), the framing (eye-level), and ask for real texture explicitly ("visible pores, weathered materials, worn everyday detail"). Set `quality="high"` when realism matters.

**Hallucination-prevention rules** (borrowed, they generalize): keep the scene spatially clear, cap the number of distinct entities, specify exact quantities ("two bottles," not "some"), prefer positive descriptions over stacked negatives for *content* (negatives are still right for *style/medium*, e.g. "not a photo of a screen"), and ground in real-world references.

## 4. The hard rule: image models GARBLE exact text, logos, and UI

This is the single most important line in this skill. AI image models **cannot be trusted** to render:

- **Exact text** — headlines drift, misspell, invent trailing words. Anything longer than a few big words is a coin flip.
- **Exact logos / trademarks** — essentially always hallucinated, even from a reference input.
- **Real UI** — review cards, rating pills, feature chips, iMessage/chat bubbles, dashboards, pricing tables. Dense, precise, must-be-correct.

So the division of labor is:

- **AI-gen** → the photoreal backdrop, the lifestyle scene, the product-in-context, the mood. Big display words *only* if you'll QA them hard (and even then, prefer a template).
- **HTML template** (`ad-creative-templates`) → anything with exact text, a logo, stars/ratings, review cards, pills, iMessage bubbles, precise brand color, or UI. Render those as HTML → screenshot for pixel-precision, then (optionally) composite the gen'd scene behind them.

If a style is "text-on-color" or "a review card" or "an iMessage thread" — **stop, it's a template, not a gen.** Don't burn regeneration rounds fighting the model for correct text.

## 5. The VISUAL-QA loop (generate → vision-check → auto-regenerate)

Never ship a batch straight from the generator. After each render, pass the image to a **vision model** (e.g. gpt-4o-class) with a defect checklist and let it gate the image:

Prompt the vision model to return structured JSON — `{ "pass": bool, "defects": [...] }` — checking for:

- **Garbled / cut-off / misspelled text** (any text present that isn't crisp and correct).
- **Warped anatomy** — extra or fused fingers, broken hands, distorted faces, impossible limbs.
- **Warped objects** — melted/incoherent product, bent laptop, nonsense UI on a screen.
- **Wrong or unwanted logos/marks** — a hallucinated brand, or the reference brand's mark cloned in.
- **Off-brand color**, obvious AI artifacts, cropped-off key subject, or a subject that doesn't match the brief.

Then:

1. **Generate** N candidates for each slot.
2. **Vision-QA each** → `pass` / `fail` + defect list.
3. **Auto-regenerate failures**, feeding the defect list back into the prompt ("previous attempt had a warped left hand — render hands clearly, one visible, resting flat").
4. **Cap the retries** (e.g. 3) so a hopeless prompt doesn't loop forever — if it can't pass in 3, the style is probably a template job (§4).
5. A human eyeballs the survivors before spend.

Score the QA **honestly** — a wrong word is a fail, not a "close enough." A generous grader makes the loop a no-op.

## 6. Batch & library organization

Generating ad creative is a batch job, not a one-off:

- **One matrix, many cells.** A run = {angles} × {formats/sizes} × {N variants}. Keep the axes explicit so you know what you tested.
- **Deterministic filenames** encoding the cell: `angle-founder__size-1080x1080__v03.png`. You'll thank yourself when reading results.
- **Keep the recipe with the image** — store the prompt, seed (if the model exposes one), endpoint, and reference inputs as sidecar metadata, so a winner is reproducible and a loser is diagnosable.
- **Separate `raw/` (all candidates) from `passed/` (survived QA) from `shipped/`** (went live). Never let a QA-failed render leak into a campaign.
- **Feed winners forward.** The angle/style that converts seeds the next batch — same as `ad-experiments`.

## 7. Checklist — one ad-creative batch

- [ ] Decide per creative: photoreal scene → this skill; exact text/logo/UI/review-card/iMessage → `ad-creative-templates`.
- [ ] Pick endpoint: new scene → `generations`; preserve a real product/logo or apply a reference style → `edits`.
- [ ] Reference images indexed + described; style references marked "style only — no marks, no text, no faces."
- [ ] Prompts built Subject→Setting→Light→Camera→Technical; photography language for realism; UGC = forbid studio polish.
- [ ] No exact text / logos / UI asked of the generator (those are templates).
- [ ] Generate N per cell → vision-QA each (garbled text, warped hands/faces/objects, wrong/unwanted logos, off-brand color) → auto-regenerate fails, retry cap ~3.
- [ ] Deterministic filenames; prompt+refs stored as sidecar metadata; `raw/` → `passed/` → `shipped/` separated.
- [ ] Human review before spend; feed winners into the next batch.

## 8. Match the platform's aspect ratio + the brand, exactly

- **Recreate at the reference ad's NATIVE aspect ratio, not a default square.** A 9:16 story ad recreated as 1:1 reads instantly as off/amateur. Map to the model's nearest size: portrait ≈ story/reels (e.g. 1024×1536), square = feed (1024×1024), landscape (1536×1024). Detect the source ratio (or decide the placement) *before* generating.
- **Put the exact brand hexes in the prompt.** Left unspecified, the model drifts to generic palettes. Name them ("brand violet #7542E4 / #9059FF, coral #FF4F5E accent — use for text highlights, buttons, accents"). Consistent color across a batch is what makes it look like one brand, not stock.
- **Recreate the STYLE, never the CLAIM.** Borrow a competitor ad's composition/energy/shot-type, but keep YOUR truthful headline and offer. Never reproduce their feature claim, their discount ("70% off"), or a benefit your product can't deliver — that's how a style-swipe turns into a false ad. (See `ad-experiments` truthfulness gate.)
- **New, different people.** Instruct "invent entirely new people who do not resemble the reference" — style-transfer models will otherwise echo the source person's face/pose.

### Practical: QA request bodies go in a FILE, not a CLI arg
Passing a base64 image inline as a shell arg (e.g. `curl -d "$(...)"`) blows up with **`Argument list too long`** — a 1 MB image is ~1.4 MB of argv, past `ARG_MAX`. Write the JSON body to a temp file and `curl -d @body.json`. Same for any base64 you feed the vision-QA call.

## Anti-patterns

- **Asking the generator for correct headlines, logos, stars, or a review card.** It garbles them. Template those.
- **Recreating a vertical ad as a square** — or any ratio that doesn't match the placement. Match the native ratio.
- **Leaving brand colors to the model.** Off-brand palette every time. Name the hexes.
- **Swiping the competitor's claim, not just their style.** Style yes, claim no — keep your own truthful offer.
- **Cloning a competitor's logo, copy, or the people in their ad.** Style-reference means style — recreate, never reproduce marks or faces.
- **Trusting a gen'd logo because you passed a reference.** Still unreliable. Verify in QA or composite the real logo.
- **Shipping a batch without vision-QA.** Warped hands and garbled text go live and burn spend.
- **Grading QA generously.** A wrong word is a fail. Honest gate or no gate.
- **Looping forever on a text-heavy render.** After ~3 fails, it's a template job — switch.
- **Losing the recipe.** No stored prompt/refs = a winner you can't reproduce and a loser you can't diagnose.

Pairs with: `ad-creative-templates` (text/UI/logo-heavy styles), `ad-lofi-ugc` (lo-fi UGC stills + video: camera-first prompts, ffmpeg degrade, character chaining, muted-first sound, QA gates), `ad-experiments` (which creative to test and how to read the result), `high-fidelity-ui-image-gen` (the same gen-vs-screenshot tradeoff for UI).
