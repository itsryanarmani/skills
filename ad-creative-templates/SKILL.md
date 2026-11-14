---
name: ad-creative-templates
description: "Produce pixel-perfect, text-precise, on-brand ad creatives at scale with the HTML/CSS-template → headless-screenshot approach — many data-driven versions from one template. Covers when to template vs AI-gen (text/UI/logo-heavy => template), a catalog of high-performing ad STYLES to template (testimonial-quote+feature-pills, iMessage/social-native convo, bold-text-on-color, product-UI-in-context, discount/offer overlay, founder/UGC, review-card, big-stat), rendering via Playwright/Puppeteer to feed (1080x1080) and story (1080x1920) sizes, keeping brand logo/colors exact, and the TRUTHFULNESS rule (real data only — no fabricated testimonials/reviews/ratings, only real product features). Use for text/UI-heavy ad creative at scale; pair with ad-creative-generation for photoreal scenes."
---

# ad-creative-templates

Pixel-perfect, text-precise, on-brand ad creatives at scale by rendering **HTML/CSS templates to PNG with a headless browser**. One template + a row of data → dozens of on-brand versions, every character correct, every hex exact. This is the text/UI/logo-heavy half of ad creative; the photoreal-scene half is `ad-creative-generation`.

## 1. Template vs AI-gen — decide per creative

- **Template it** when the creative is **text-, UI-, logo-, or data-heavy**: exact headlines, a real logo, star ratings, review cards, feature pills, iMessage/chat bubbles, dashboards, pricing tables, precise brand color, or 50 data-driven variants. The DOM renders these *correctly, every time* — an AI image model garbles them (see `ad-creative-generation` §4).
- **AI-gen it** when the creative is a **photoreal scene / lifestyle / product-in-context / mood backdrop** with little or no exact text. See `ad-creative-generation`.
- **Combine** when useful: AI-gen the photoreal backdrop, then lay the exact HTML text/logo/card on top (as a CSS `background-image`, composited before screenshot).

The test: *does correctness of text, a logo, a rating, or UI matter?* → template.

## 2. The pipeline

1. **One HTML/CSS template per style**, parameterized by data (a headline, a quote, a name, a price, an image URL, brand tokens). Handlebars/JSX/plain template literals — anything that fills slots.
2. **A data source** — a row per creative (CSV/JSON/sheet). N rows = N creatives, no design tool.
3. **Render headless** — Playwright or Puppeteer loads the template at a fixed viewport, waits for fonts/images, screenshots the element (or full page) to PNG.
4. **Sizes as viewports**, not resizes — render each size natively (§4).
5. **Name + store** deterministically, same as any creative batch (`style__size__vNN.png`).

Minimal render (Playwright, Node):

```js
const { chromium } = require('playwright');

async function render({ html, width, height, out }) {
  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width, height },
    deviceScaleFactor: 2, // 2x = crisp text/retina
  });
  await page.setContent(html, { waitUntil: 'networkidle' }); // fonts + images loaded
  await page.screenshot({ path: out }); // element.screenshot() to crop to the ad
  await browser.close();
}
// feed sizes: 1080x1080 (square), 1080x1920 (story), 1200x628 (landscape)
```

`ponytail:` one `render()` + a data loop covers the whole batch — no per-style renderer, no framework. Add a queue only if volume actually needs it.

## 3. Catalog of high-performing ad STYLES to template

Each is a template because each is text/UI/logo-heavy. Build the ones your campaign needs.

- **Testimonial quote + feature pills** — a real customer quote, attributed name/role/photo, plus a row of "pills" (rounded chips) naming real features. Exact text, exact logo, exact color → template, always.
- **iMessage / social-native conversation** — a chat thread (bubbles, timestamps, typing dots) or a native-post mimic (a tweet/DM/notification). Reads as native content, not an ad. Precise UI chrome → template. (Truthfulness: §6.)
- **Bold-text-on-color** — one punchy line of huge type on a flat brand-color field. Dead simple, high-contrast, high-performing. The whole creative *is* exact text + exact hex → the model's worst case, the template's easiest.
- **Product-UI-in-context** — a real screenshot of the product UI placed in a device frame / browser chrome / clean backdrop. Use a *real* screenshot (see `app-screenshots`), not a gen'd UI.
- **Discount / offer overlay** — "30% OFF", a code, an expiry, a CTA, over a product shot or flat color. Numbers and codes must be exact → template.
- **Founder / UGC** — a founder headshot or phone-shot photo + a short handwritten-feeling caption + light chrome. (Photo can be AI-gen'd per `ad-creative-generation`; the caption/logo overlay is the template.)
- **Review card** — an App Store / G2 / Trustpilot-style card: stars, reviewer, verified badge, quote. Stars + exact copy → template. (Truthfulness: §6.)
- **Big-stat** — one dominant number ("2M+ users", "4.9★") with a short label. The number must be exact and real → template.

## 4. Sizes — render each natively

Render at the target viewport; don't design one size and rescale (rescaling softens text and breaks layout).

- **Feed / square: 1080×1080.**
- **Story / vertical: 1080×1920** (also Reels/TikTok).
- **Landscape: 1200×628** (feed link, some placements).

Use responsive CSS (flex/grid, relative units, clamp) so one template reflows across all three, or keep a per-size layout block. `deviceScaleFactor: 2` for crisp output. Confirm safe-margins for platform UI overlays on story (top/bottom ~250px can be covered by the platform's own chrome).

## 5. Keep brand logo & colors EXACT

The whole reason to template is correctness — don't undo it:

- **Logo = the real asset file** (SVG preferred, else high-res PNG), referenced in the template. Never a redrawn or AI-gen'd approximation.
- **Colors = exact brand hex/tokens**, ideally CSS custom properties (`--brand: #XXXXXX`) so every template shares one source of truth. No look-alikes.
- **Fonts = the real brand font**, `@font-face`-loaded and *awaited* before screenshot (a race here ships a fallback-font creative). `document.fonts.ready` or `waitUntil: 'networkidle'`.
- **Pin a font stack fallback** anyway, so a font miss degrades gracefully instead of shipping Times New Roman.

## 6. The truthfulness rule (non-negotiable)

Templates make fabrication *easy and beautiful* — which is exactly the trap. Real data only:

- **No fabricated testimonials, reviews, ratings, or quotes.** A testimonial/review-card/iMessage style may only show words a real customer actually said, and stars/ratings that are real and defensible. Never frame an AI-generated or made-up statement as a real customer quote.
- **No invented stats.** A big-stat or offer creative uses real, current, defensible numbers ("2M+ users" only if true today).
- **Only advertise real product features.** Feature pills, screenshots, and claims must reflect what the product actually does — advertising a capability it lacks is false advertising and tanks conversion when the click meets a page that can't deliver (see `ad-experiments`).
- **Social-native mimics stay honest.** An iMessage/tweet-style ad may *look* native, but its factual content must be real, and it must not impersonate a real person or a real platform's endorsement.

If the real data isn't there, the honest move is a different style — not a plausible-looking fabrication.

## 7. Checklist — a template-driven ad batch

- [ ] Per creative: text/UI/logo/data-heavy → template; photoreal scene → `ad-creative-generation`.
- [ ] One parameterized HTML/CSS template per style; data source = one row per creative.
- [ ] Real logo asset (SVG), exact brand hex as CSS tokens, real brand font `@font-face`-loaded and awaited.
- [ ] Render headless (Playwright/Puppeteer), `deviceScaleFactor: 2`, wait for fonts+images before screenshot.
- [ ] Render each size natively — 1080×1080, 1080×1920, 1200×628 — not rescaled; respect story safe-margins.
- [ ] Truthfulness: real quotes/reviews/ratings/stats only; only real features; no impersonation.
- [ ] Deterministic filenames (`style__size__vNN.png`); keep the data row with the render.
- [ ] Human review before spend; feed winners into the next batch (`ad-experiments`).

## Anti-patterns

- **AI-gen'ing text/logos/review-cards/iMessage** because it "looks close." It garbles — that's what templates are for.
- **Screenshotting before fonts/images load.** Ships a fallback-font, missing-image creative. Await readiness.
- **Designing one size and rescaling.** Softens text, breaks layout. Render each size natively.
- **A redrawn or gen'd "logo."** Use the real asset file, exact hex, or the whole point is lost.
- **Fabricated testimonials/reviews/ratings/stats,** or advertising a feature the product lacks. Real data only — legal risk and conversion killer.
- **A bespoke renderer per style.** One `render()` + a data loop. Add machinery only when volume proves you need it.

Pairs with: `ad-creative-generation` (photoreal scenes, and the gen-vs-template rule), `app-screenshots` (capturing real product UI to drop into product-UI-in-context ads), `ad-experiments` (which styles/angles to test and how to judge them).

## Ranked Meta ad formats — cross-reference
For the 12 ranked formats, ROAS ranking table, WaveSpeed model picks, and creative rules, see [`impulse-formats.md`](impulse-formats.md). That shared reference contains the ranked table, launch-first rotation rule, WaveSpeed CLI usage (key from `WAVESPEED_API_KEY` only), and the creative rules (blurry lo-fi 2000s phone-photo people; no header/footer/logo; never text-only; plain STE-100 copy; no invented testimonials). The iMessage/Notes/ChatGPT HTML templates in Part A remain the canonical pipeline for text/UI-heavy styles.
