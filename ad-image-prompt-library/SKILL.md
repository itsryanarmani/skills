---
name: ad-image-prompt-library
description: "A copy-paste LIBRARY of proven ad-creative recipes in two families — Part A: HTML-mockup ad formats that render cheap and pixel-exact via HTML/CSS → screenshot with NO image/video model (the high-performing 'iOS Ads' family: iMessage chat-reveal, Apple Notes reveal, ChatGPT chat-reveal, WhatsApp chat-style, iPhone lock-screen notification), each with why-it-performs + the UI elements to reproduce + a fill-in content template; Part B: AI-image-gen prompt skeletons for gpt-image / Nano-Banana-style models (photo-of-a-screen hyper-realism, Instagram pop-out / 3D frame-break, stepping-out-of-the-phone optical illusion, cinematic character board, isometric figurine, OOTD mirror-selfie collage, anime GTA-style poster grid), plus the universal realism levers (SLCT), text-in-quotes rule, and negative-prompt hygiene. Every recipe generic + reusable with [PLACEHOLDERS]. Use when you need a starting prompt/format for an ad creative; pair with ad-creative-generation (image-model mechanics + QA) and ad-creative-templates (HTML→screenshot pipeline)."
---

# ad-image-prompt-library

A library of copy-paste **ad-creative recipes**, in two families:

- **Part A — HTML-mockup ad formats.** Cheap, pixel-exact, deterministic. Render as HTML/CSS → headless screenshot, **no image/video model**. Every character correct, every hex exact. Build these with the `ad-creative-templates` pipeline (one template + a data row → many variants).
- **Part B — AI-image-gen prompt templates.** Reusable prompt skeletons for a `gpt-image` / Nano-Banana / GPT-Image-style model. Run these through the `ad-creative-generation` mechanics (endpoint choice, reference-image rules, vision-QA loop).

Everything here is generic — swap the `[PLACEHOLDERS]` for your product, palette, and copy. **Truthfulness still applies:** no fabricated quotes/reviews/ratings, no impersonation of a real person or platform, only real features (see `ad-creative-templates` §6).

For candid, phone-photo style statics (12 prompt templates, overlay and CTA rules, policy checklist, A/B test plan), read [organic-static-ads.md](organic-static-ads.md).

## Which format for which goal (selector)

| Goal | Reach for |
|---|---|
| Cheapest, correct text, ships today, no model | Part A — any HTML mockup (start with iMessage or lock-screen) |
| "Feels native, not an ad" / curiosity scroll-stopper | Part A — iMessage / ChatGPT / WhatsApp chat-reveal |
| List-y "things nobody told me about X" hook | Part A — Apple Notes reveal |
| Glanceable pain→relief in 1 second | Part A — iPhone lock-screen notification |
| Photoreal product / lifestyle / person, real texture | Part B — photo-of-a-screen, or `ad-creative-generation` §3 |
| Scroll-stopping "breaks the frame" gimmick | Part B — Instagram pop-out / stepping-out-of-the-phone |
| Character / cast / persona showcase | Part B — cinematic character board / isometric figurine |
| Aesthetic mood / lifestyle collage / fandom | Part B — OOTD collage / anime GTA poster grid |

Rule of thumb: **if the creative is text-, UI-, or logo-heavy, it's Part A** (a model garbles it). If it's a photoreal scene or a stylized character, it's Part B.

---

# PART A — HTML-mockup ad formats ("iOS Ads" family)

These are the **highest-performing cheap format**: they render pixel-exact from HTML/CSS, cost ~nothing per variant, and win because —

- **Low cognitive load** — people read these exact UIs (Messages, Notes, ChatGPT, WhatsApp, the lock screen) dozens of times a day; the brain parses them with zero effort.
- **Native / non-ad feel** — they look like a screenshot a friend sent, not a branded ad, so they slip past ad-blindness.
- **Curiosity** — watching someone *type* (typing indicator, a half-written note, a streaming answer) pulls the eye and holds it to the reveal.

Reproduce the platform chrome **faithfully** — a wrong font, a fake battery icon, or off spacing breaks the "this is real" illusion instantly. Render each at feed `1080×1080` and story `1080×1920` (see `ad-creative-templates` §4). Below, each format lists: what it is · why it performs · key UI to reproduce · fill-in template.

## A1 — iMessage chat-reveal

- **What it is:** a fake iMessage thread where a short conversation reveals the product — a question/pain, a recommendation, and a tappable product link card.
- **Why it performs:** the most-read UI on iOS; blue/grey bubbles read as a *real* text from a friend recommending something → maximum native feel + social proof by proxy.
- **Key UI to reproduce faithfully:**
  - Contact header: back chevron, centered contact avatar + `[NAME]`, top status bar (time, signal, wifi, battery).
  - Bubbles: incoming = **grey** left-aligned, outgoing = **iMessage blue (#3B7DFF-ish gradient)** right-aligned, rounded ~18px with the little tail on the last of a run.
  - Optional **typing indicator** (three grey animated dots in a bubble) as the last incoming — the curiosity beat.
  - A **link-preview card** (rounded, thumbnail + title + domain) for the product URL.
  - Bottom **iMessage input bar**: rounded "iMessage" field, camera/plus icon left, a grey ↑ send arrow right.
- **Fill-in template:**
  ```
  Header: [FRIEND_NAME]
  Grey (them): "[PAIN / QUESTION, e.g. ugh still can't find a [CATEGORY] that [DESIRED OUTCOME]]"
  Blue (you):  "omg just use [PRODUCT]"
  Blue (you):  "[ONE-LINE WHY — real benefit]"
  Link card:   [THUMBNAIL] · "[PRODUCT] — [TAGLINE]" · [DOMAIN]
  Grey (them): "wait this is exactly what I needed 😍"
  [typing indicator on them, optional]
  ```

## A2 — Apple Notes reveal

- **What it is:** a single Apple Notes note titled like a listicle hook ("Things nobody told me about `[X]`"), with a few bullet lines, a blinking cursor, and the Notes formatting toolbar + keyboard visible.
- **Why it performs:** reads as a private, honest jot — not marketing. The listicle title promises value; the visible cursor/keyboard says "being written right now," which is the curiosity hook.
- **Key UI to reproduce faithfully:**
  - Notes header: back to folders (yellow chevron `Notes`), share icon, compose icon; date/time line under the title in grey.
  - **Title line** bold + larger; body in the Notes body font; a **text cursor** (thin blue I-beam) at the current line.
  - **Formatting toolbar** row above the keyboard (Aa format, checklist, camera, pencil/markup).
  - The **iOS keyboard** at the bottom (QWERTY, spacebar, blue return) — or the predictive-text strip alone for a tighter crop.
- **Fill-in template:**
  ```
  Title: Things nobody told me about [TOPIC / PAIN]
  [DATE • TIME]
  • [MYTH or mistake people make]
  • [The thing that actually worked → mentions [PRODUCT] naturally]
  • [Concrete result / number, real]
  • [cursor here|]
  ```

## A3 — ChatGPT chat-reveal

- **What it is:** a mock ChatGPT thread — a user question in a grey bubble, then a "streaming" assistant answer with a short intro line and bullets that recommend/explain the product.
- **Why it performs:** AI answers are read as neutral, authoritative "research," so a recommendation inside one carries borrowed credibility; the mid-stream cursor sells "it's answering right now."
- **Key UI to reproduce faithfully:**
  - Top bar: `ChatGPT` title (or model name), new-chat/menu icons.
  - **User turn:** right/grey rounded bubble with the question (ChatGPT web shows user messages in a light bubble; mobile similar).
  - **Assistant turn:** the ✦/logo avatar, left-aligned answer, a one-line intro then a **markdown bullet list**; optional bold lead-ins per bullet.
  - A **streaming caret** (▍) at the end of the last line, or a "Stop generating" pill, for the live feel.
  - Bottom **composer**: rounded "Ask anything" field, mic + send icons.
- **Fill-in template:**
  ```
  User (grey): "best [CATEGORY] for [SPECIFIC USE-CASE / CONSTRAINT]?"
  Assistant:
    Great question — here are the top options:
    • **[PRODUCT]** — [why it fits the constraint, real].
    • [Honest alt / criterion] ...
    • [Honest alt / criterion] ...
    For [USE-CASE], [PRODUCT] is usually the best starting point.▍
  ```

## A4 — WhatsApp chat-style

- **What it is:** a WhatsApp thread themed around a "breakup with the pain" bit — the pain is personified and "leaves the chat," with a product image shared in the thread.
- **Why it performs:** the green WhatsApp chrome is instantly familiar; the "`[Pain]` has left the chat" system line is a native meme format that reads as funny/organic, not salesy.
- **Key UI to reproduce faithfully:**
  - Header: **green (#075E54 / #128C7E) bar**, back arrow, contact avatar + `[NAME]`, and the **"online" / "last seen today at [TIME]"** subtitle.
  - Chat background = WhatsApp's faint doodle wallpaper; bubbles: incoming **white**, outgoing **light-green (#DCF8C6)**, with a tiny time + **double blue tick** on outgoing.
  - A **shared product image** bubble (thumbnail + caption).
  - A centered grey **system message** pill: `"[PAIN] has left the chat"` / `"[PAIN] was removed"`.
  - Bottom **type-a-message bar**: rounded field, emoji + attach + camera icons, a green mic/send button.
- **Fill-in template:**
  ```
  Header: [PRODUCT or FRIEND] — online
  White (them): "still dealing with [PAIN]?"
  Green (you):  "not anymore lol"
  Green (you):  [product image] "[PRODUCT] fixed it — [real benefit]"
  — system —   "[PAIN] has left the chat"
  White (them): "sending this to everyone 😭"
  ```

## A5 — iPhone lock-screen notification

- **What it is:** an iPhone lock screen — big clock + date over a scenic wallpaper — with a stack of notification banners (each with an app icon) that tell a micro pain→relief story. Shot to look like a **raw screenshot**.
- **Why it performs:** the single most-seen screen on earth; a notification is glanceable in <1s and feels like a real alert, not an ad. Stacked banners let you sequence a tiny narrative.
- **Key UI to reproduce faithfully:**
  - **Time** (huge, SF font) + **date line** above it; lock icon at top; flashlight + camera buttons bottom corners (optional).
  - A **scenic wallpaper** (mountain/beach/gradient) — keep it real-photo, slightly soft.
  - **Notification bubbles**: frosted-glass rounded rectangles, each = rounded **app icon** + bold `[APP NAME]` + relative time (`now` / `2m ago`) + one/two lines of message text; stack 2–3, newest on top, slight overlap on the bottom one.
  - Raw-screenshot look: real status bar (carrier, 5G, battery %), no drop-shadow "ad polish," no added frame.
- **Fill-in template:**
  ```
  9:41   Monday, [DATE]
  [wallpaper: scenic photo]
  [🔔 app icon] [PRODUCT]        now
     "[Push copy: benefit / social proof, e.g. '[N] people started [OUTCOME] today']"
  [💬 app icon] [FRIEND]         2m ago
     "have you tried [PRODUCT]?? game changer"
  [📅 app icon] Reminders        8m ago
     "Stop [PAIN] — try [PRODUCT]"
  ```

---

# PART B — AI-image-gen prompt templates

Skeletons for a text→image / image-edit model. Fill the `[placeholders]`, then run through `ad-creative-generation` (pick `generations` vs `edits`, index reference images, vision-QA every render). **Do not ask these for exact headlines, logos, or real UI** — that's Part A.

## Universal realism levers

- **SLCT** — every prompt fills four slots, no free-associating: **S**ubject (who/what, exact count), **L**ighting (source, direction, quality — "soft window light from left"), **C**amera (lens + framing — "35mm, eye-level, medium close-up"), **T**echnical (medium, film/sensor look, texture — "shot on phone, visible grain, real skin pores"). Naming the lens + light is what tips a render from "AI" to "photo."
- **Text-in-quotes = literal on-image text.** Put any words you actually want rendered **in double quotes** in the prompt (`the sign reads "[EXACT TEXT]"`). Keep it to a few big words — models still garble long strings, so anything precise belongs in a Part-A template.
- **Identity-lock (when using a reference photo of a person/product):** state `keep the exact same face/identity/product as the reference — do not restyle, age, slim, or beautify; same features, same proportions`. Prevents the model drifting the subject into a generic look-alike.
- **Negative-prompt hygiene:** use negatives for **style/medium/defects**, not for content ("no content" is unreliable). A reusable baseline: `no extra fingers, no fused hands, no warped face, no garbled text, no watermark, no logo, no studio polish, no plastic skin, no oversaturation, no duplicated limbs`.

## B1 — Photo-of-a-screen hyper-realism

- **When to use:** you want a "someone snapped a photo of their phone/laptop showing `[SCENE]`" look — the anti-polish, maximally-believable UGC vibe (also the base for faking a screenshot inside a real environment).
- **Prompt skeleton (JSON-style keeps the model on-spec):**
  ```
  {
    "shot": "this is a PHOTO OF A SCREEN, not a screenshot — a phone/monitor physically photographed by another camera",
    "subject": "[DEVICE] displaying [SCENE / CONTENT]",
    "screen_realism": ["visible RGB sub-pixel grid", "faint moiré banding", "screen glare / reflection", "dust specks and fingerprint smudges on the glass", "slight off-axis angle", "backlight glow at edges"],
    "environment": "[real setting — desk, hand-held, café table], ambient [LIGHT]",
    "camera": "[35mm / phone camera], [framing], natural handheld imperfection",
    "technical": "real photo, natural grain, NO studio polish, NO perfect crop",
    "identity_lock": "[if a product/person is shown: keep it exactly as reference]",
    "negative": "no crisp digital screenshot, no perfect pixels, no clean UI export, no vector sharpness, no studio lighting, no garbled text"
  }
  ```

## B2 — Instagram pop-out / 3D frame-break

- **When to use:** scroll-stopping "subject bursts out of the post" gimmick for a feed placement.
- **Prompt skeleton:**
  ```
  A centered white Instagram post frame on a plain [BG COLOR] background, with the standard IG UI: heart / comment / share row, "[N] likes", username "[HANDLE]", and caption "[SHORT CAPTION]".
  [SUBJECT] is photographed inside the post but POPS OUT — [head / hand / product] breaks past the white border into 3D, casting a soft drop shadow onto the frame; a hand grips the edge of the frame.
  Lighting: [soft studio / directional]. Camera: [50mm, slight low angle]. Technical: photoreal, crisp subject, realistic shadow + depth.
  Negative: no warped hands on the frame edge, no garbled UI text, no duplicated icons.
  ```

## B3 — Optical-illusion "stepping out of the phone"

- **When to use:** surreal attention-grab — the subject is literally climbing out of a phone screen.
- **Prompt skeleton:**
  ```
  A large [PHONE] lying/standing on [SURFACE]. [SUBJECT]'s torso emerges UP and OUT of the screen in full 3D, while their legs are still flat ON the screen showing the phone's camera-app UI (shutter button, mode strip) around them — a seamless optical illusion.
  Handwritten annotations / arrows around the scene reading "[SHORT LABEL]".
  Lighting [L], camera [C, slight top-down], photoreal composite, believable shadow where body meets glass.
  Negative: no melted body, no broken perspective, no garbled UI, no extra limbs.
  ```

## B4 — Cinematic character board

- **When to use:** a premium "cast sheet" for a persona, mascot, or feature line-up.
- **Prompt skeleton:**
  ```
  A dark premium character sheet with thin gold borders, laid out as panels.
  Hero panel: [CHARACTER] full-body, [pose], dramatic [L] lighting.
  Surrounding smaller panels: multiple views (front / 3-4 / profile / back) and 3-4 facial EXPRESSIONS (neutral, smiling, focused, surprised).
  A vertical PALETTE STRIP of the character's key colors down one side.
  Small handwritten-style labels "[NAME]", "[TRAIT]". Style: cinematic, cohesive, high-detail concept-art.
  Negative: inconsistent character across panels, garbled labels, mismatched colors.
  ```

## B5 — Isometric figurine

- **When to use:** a cute collectible-toy render of a person/mascot — high shareability.
- **Prompt skeleton:**
  ```
  A miniature full-body ISOMETRIC realistic figurine of [SUBJECT / this person], [outfit / props], standing on a small round base, on a plain white background, soft even studio light, sharp focus, 4K, product-render look.
  [identity-lock if from a reference photo]
  Negative: no full-size human, no busy background, no warped face, no extra base clutter.
  ```

## B6 — OOTD / mirror-selfie Pinterest collage

- **When to use:** aesthetic lifestyle / fashion / mood board that reads as organic Pinterest content.
- **Prompt skeleton:**
  ```
  A 4-image collage (2x2), Pinterest / moodboard aesthetic: [SUBJECT] in [OUTFIT / SETTING] — one mirror-selfie holding a phone, one detail shot, one full-body, one candid.
  Overlay a music-player widget (album art "[TRACK]", play bar, artist "[ARTIST]") on one tile.
  Look: desaturated muted tones, visible film grain, soft natural light, [palette]. Cohesive edit across all four.
  Negative: oversaturation, mismatched lighting between tiles, garbled widget text, warped hands on the phone.
  ```

## B7 — Anime / GTA-style poster grid

- **When to use:** a stylized fandom/hype poster — a hero center panel ringed by vignette panels.
- **Prompt skeleton:**
  ```
  A [anime cel-shaded / GTA loading-screen illustrated] poster grid: one large CENTER panel of [HERO SUBJECT / scene], surrounded by smaller vignette panels (side characters, objects, locations, close-ups).
  Bold black gutters between panels; a [PALETTE] color scheme with a palette strip along the bottom edge.
  Optional title text "[TITLE]" in the [style]'s signature lettering.
  Style: high-contrast, dynamic, cohesive [anime / GTA] art direction.
  Negative: muddy panels, garbled title, inconsistent art style between panels.
  ```

---

## Anti-patterns

- **Asking a Part-B model for the Part-A stuff** — an iMessage thread, a lock-screen, exact push copy, a real logo. It garbles the chrome and the text. Those are HTML mockups.
- **Sloppy platform chrome in Part A** — a fake battery icon, wrong bubble color, missing typing indicator, off font. The whole edge is "this looks real"; a tell kills it.
- **Long literal text in a Part-B prompt.** Quotes help for a few big words; anything precise still drifts — template it.
- **Skipping identity-lock** when a real person/product is the reference — the model drifts them into a generic look-alike.
- **Fabricated social proof.** A fake testimonial in an iMessage/ChatGPT reveal, invented likes/reviews, impersonating a real person or platform. Real data only (`ad-creative-templates` §6).
- **Shipping without QA.** Part A: eyeball the chrome at 1:1. Part B: run the vision-QA loop (`ad-creative-generation` §5).

Pairs with: `ad-creative-templates` (the HTML→screenshot pipeline that renders every Part-A format, + the truthfulness rule), `ad-creative-generation` (image-model endpoints, reference-image rules, and the vision-QA loop for every Part-B render), `ad-experiments` (which format/angle to test and how to judge the result), `high-fidelity-ui-image-gen` (the gen-vs-screenshot fidelity tradeoff), `app-screenshots` (capturing real product UI to drop into a mockup).
