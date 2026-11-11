---
name: landing-page
description: "Design or level up a marketing landing page that converts — section architecture, interaction/effect vocabulary, and review gates. Use when building a new landing/marketing page from scratch, revamping an existing one, auditing a page for missing conversion anatomy (weak hero, no proof, buried CTA), or deciding which motion/effect belongs where. Covers CREATE and LEVEL-UP modes; pairs with the impeccable design skill for craft."
---

# landing-page

A landing page has ONE job: move a visitor from attention to action. This skill is the
map — what sections a converting page is made of, where proof and CTAs go, which
interactions earn their weight, and how to review the result. It is a **reference, not a
generator**: it tells you what to build and how to judge it. The actual pixels/motion come
from the **impeccable** skill (aesthetic direction, craft-floor, the review commands) — invoke
that for the visual world; use this for the landing-specific structure it doesn't own.

**Scope:** this skill is one page. When the product needs a *site* — a page per
audience, per use case, per competitor, a free-tools channel, a mega-menu shell —
that is **marketing-site**, which owns the content model those pages are generated
from. Build the home page here; generate the other fifty there.

For funnel-type blueprints and benchmarks counted from 54 public pages, see **landing-page-blueprints**.

## Two modes — name yours first

1. **CREATE new** — intake → aesthetic direction → section plan → build → review gates.
2. **LEVEL-UP existing** — audit current sections against the taxonomy (which are missing?
   which are weak?), score each section *individually*, run the review gates, apply targeted
   upgrades. A strong hero with a buried CTA still loses — grade section by section, not the
   page as one blob.

The rest of this skill serves both. CREATE reads it top-to-bottom; LEVEL-UP uses §A/§F as a
scorecard and §B–D as the upgrade menu.

## Non-negotiables (both modes)

- **Honor the brand/design system that exists.** If the product has tokens, a theme, a
  DESIGN.md — the page is built IN that world, not a fresh aesthetic. Never hardcode colors a
  themed system would flip (light/dark); use its variables. Redesigning a branded product's
  landing toward your own taste is failure.
- **No invented proof.** No fabricated testimonials, user counts, star ratings, benchmarks, or
  logos you don't have rights to. True capabilities are fair game; where a testimonial-shaped
  slot has no real quote, use a product-truth statement instead of a fake one.
- **Progressive enhancement.** Content lives in the DOM and reads with JS/CDN failed. Motion
  only *enhances*. `prefers-reduced-motion: reduce` disables transforms/loops and shows final
  states. One primary action visible above the fold on every breakpoint.
- **Responsive to three targets** — desktop (≥1024), tablet portrait (768), mobile (≤480).
  Fluid type via `clamp()`. No horizontal scroll, ever.
- **Preserve product contracts.** Pricing/localization hooks, analytics attributes, form
  actions, auth links — restyle freely, but keep the data contract and its fallbacks intact.

---

## A. SECTION TAXONOMY (conversion anatomy)

Average converting page ≈ 6 sections (from scored corpora of hundreds of pages). Range: 3–4
for a single-offer page, 10+ for enterprise. Narrative arc: **attention → clarity → trust →
action.** Each section does exactly ONE job — if you can't name its job, cut or merge it.

1. **Header / nav** — logo, minimal links, one CTA. Sticky; hairline on scroll. Mobile: logo +
   CTA, links collapse.
2. **Hero** — eyebrow/kicker, H1 that states the *value* (not the product name), one-line
   benefit subhead, ONE primary CTA above the fold, one focused visual. The 5-second test:
   a stranger should know *what this is* and *is it for me*. No competing primary buttons.
3. **Problem** — name the pain in the reader's own words (optional; strong for cold traffic).
4. **Solution / USP** — the offer as resolution; why you over the alternatives.
5. **How it works** — 2–4 numbered steps. Airy; one authored icon per step.
6. **Features / benefits** — 3–5 items, **benefit-led** (function → outcome), each with an
   icon. Clarity beats catalogue. Bento/featured-card layout reads richer than a flat grid.
7. **Social proof** — three flavors: named testimonial (name/role/company), logo bar, hard
   numbers. Distribute it (see below), don't dump one block.
8. **Comparison table** — vs. alternatives (enterprise / considered purchases).
9. **Pricing** — transparent tiers; say what each dollar buys. Feature the intended plan.
10. **FAQ** — objection handling, accordion, `aria-expanded`. 4–6 items answering the real
    hesitations (price, privacy, platform limits, commitment).
11. **CTA block** — the highest-contrast moment on the page; repeat the primary action.
12. **Footer** — lean: privacy / terms / contact / repeat CTA.

### Social-proof PLACEMENT (distributed by visitor mindset, not one block)

- **Above fold:** one best testimonial line OR a "trusted by N" counter.
- **Beside the CTA button:** ratings, review counts, trust badges — hesitation peaks here.
- **Mid-page (after features):** case studies, detailed testimonials — proof it works.
- **Near pricing/checkout:** security/compliance badges, big-number metrics — risk fear peaks.
- **Footer:** award badges, logo bars — final confidence.
Rule: 3–4 proof *types*, each placed where its stage's doubt lives.

---

## B. INTERACTION / ANIMATION ARCHETYPES

Motion is orchestrated once in the page's grammar — not scattered hovers. Pick a signature.

1. **Hero entrance** — timeline: eyebrow → headline (word/line stagger) → subhead → CTA rise.
   Set initial states FIRST (no flash of unstyled/jumping content).
2. **Mouse parallax** — layers shift on mousemove for hero depth (back / mid / content).
3. **Scroll-trigger stagger** — cards/sections fade+rise on enter, staggered. Visible if JS off.
4. **Scroll-scrubbed cinematic** (Apple-style) — scroll position drives a timeline/video/camera.
   "The camera moves, scroll drives time." Heavy; use only when the story needs it.
5. **Floating decorative shapes** — CSS keyframes (cheaper than JS for indefinite loops).
6. **Interaction states** (per element, non-negotiable): hover / active / disabled / focus /
   loading / validation. A page missing disabled+focus+loading states is unfinished.
7. **Hover lift** — feature cards.
8. **Signature product demo** — the strongest hero move: show the product *doing its job*
   in-page (a self-typing input, a live toggle, a before/after) instead of a static screenshot.

**Restraint rule: 1–2 signature effects per page, max.** More reads as AI-slop. Everything
degrades under reduced-motion.

---

## C. EFFECT CATALOG (by JOB, not by library)

Organize by what the effect *does*. Named exemplars exist across Magic UI / Aceternity /
Originkit — pick by job, implement in the page's own world.

- **Backgrounds (ambient, behind content):** dot/grid/retro/flickering grids, aurora, meteors,
  shooting-stars, beams (+collision), ripple, spotlight, lamp, noise-texture, vortex.
- **Hero focal / scroll-driven:** hero-parallax, container/macbook scroll, sticky-scroll-reveal,
  tracing-beam, scroll-progress, scroll-velocity, scroll-scrubbed cinematic.
- **Text (headline/eyebrow — use ONE):** text-generate, typewriter, flip/rotate-words,
  text-reveal, hyper/scramble, shiny/gradient/aurora text, number-ticker, highlight-marker.
- **Cards (features/proof/pricing):** bento-grid, 3d-card, card-hover/spotlight/glare, comet,
  expandable, focus-cards, infinite-moving-cards (logo/testimonial marquee), border-beam/shine.
- **Buttons/CTA:** shimmer, rainbow, ripple, pulsating, **magnetic**, moving-border,
  hover-border-gradient, interactive-hover, stateful (loading built in).
- **Nav:** floating-navbar, resizable-navbar, floating-dock, sticky-banner.
- **Media/device mocks:** safari/iphone/android frames, hero-video-dialog, before/after compare,
  lens (zoom), cards-carousel.
- **Data/trust visuals:** globe, world-map, timeline, orbiting-circles, icon-cloud,
  avatar-circles, marquee (logo bar), tweet-card.
- **Pointer/cursor:** following-pointer, pointer-highlight, cursor glow (pointer:fine only).

**Section blocks = the level-up shortcut.** Magic UI / Aceternity ship whole pre-built
Hero/Features/Pricing section blocks (shadcn-style `add` — source lands in your repo, deps
auto). Faster than authoring from zero when the aesthetic fits.

---

## D. STYLE / AESTHETIC

- **Tone axis:** Professional / Playful / Authoritative / Minimal. Commit to one.
- **Brand exists?** Extract its tokens and build inside them. Stop reading this bullet.
- **No brand yet? Adopt a finished direction before you invent one.** The
  [`brand-router`](../brand-router/SKILL.md) suite carries **twenty** directions, and each one
  already specifies its landing-page surface with committed hex values, audited contrast, a
  named motion, and the failure mode that kills it. Run the router to pick; it surveys what
  you actually publish and recommends a kit rather than a single style. Adopting one is
  hours; generating a fresh world is days and starts unaudited.

  Three routes, and they are not interchangeable:

  | Route | Use when | Output |
  |---|---|---|
  | [`brand-router`](../brand-router/SKILL.md) → a direction | A direction in the catalog fits | Finished tokens and twelve surfaces, already audited |
  | `saas-brand-system` | The brand does not exist and nothing in the catalog fits | N prototypes, judged, then expanded |
  | `impeccable` aesthetic-direction | You only need this one page to have a point of view | A direction for the page, not the brand |

  **Prototype before you commit.** Render two or three candidate directions as standalone
  pages with real product copy, then pick from the rendered result. A direction reads
  completely differently as a page than as a description, and this step is cheap.

- **Cost to run is the filter that actually binds.** Every direction declares it, and a brand
  dies of upkeep far more often than of ugliness. `swiss`, `terminal`, `spec`, `porcelain`,
  `broadsheet`, `manuscript`, `plaque` and `buildspace` are the cheap ones — reachable by one
  person publishing weekly. `risograph`, `arcade`, `flyer` and `aurora` need real craft per
  asset; pick one of those only if a designer is in the loop.

- **Whatever you pick, apply it as a direction and not as a palette.** Swapping hex values
  while leaving centred heroes, soft shadows and rounded cards in place produces a recoloured
  template, not a brand. The section *form* is most of the direction: `swiss` is flush left on
  a visible twelve-column grid with radius 0 and exactly one red element, and none of that is
  a colour.
- **AI house-style tells to avoid** (they read as slop): cream + serif + terracotta/amber;
  navy + teal + Inter; purple→indigo gradients on everything; emoji as icons; three fonts.
  Run impeccable's slop-check.
- **One spacing rhythm** (e.g. 8px base). More space above a heading than below it. Vary
  density across the page — dense hero → airy how-it-works → dense pricing → quiet FAQ → punch.

---

## E. WORKFLOW

**Greenfield:** intake → aesthetic direction → section plan → build → review gates.
**Brand-aware:** design-system extract → section plan in-world → build → review gates.

**Intake (ask ONE at a time, then commit — don't over-interview):**
- Q1 What's the product, in one line? What's the single action you want?
- Q2 Who's the visitor — technical / business / consumer / internal?
- Q3 Brand overrides — existing tokens, colors, fonts, logo? (If yes, extract, don't invent.)
- Q4 Tone — which point on the axis?
After Q4, commit and build. No concept survives contact with a fifth question.

---

## F. REVIEW GATES (LEVEL-UP leans hardest here)

Run these before shipping. In a codebase with impeccable installed, these ARE its commands —
invoke them rather than re-deriving. Score each section on its own.

- **Section coverage** — every taxonomy job present or deliberately, defensibly absent.
- **Accessibility** — semantic landmarks, keyboard path, visible focus, `aria-expanded` on
  accordions, alt/aria-label on icons+logo, contrast ≥ 4.5:1 body, reduced-motion honored.
  (impeccable `audit`.)
- **AI-slop check** — the house-style tells above; over-effected pages. (impeccable, slop pass.)
- **Hierarchy & rhythm** — size/weight/color hierarchy + one spacing scale. (impeccable.)
- **Interaction states** — hover/active/disabled/focus/loading/validation all present.
- **Responsive** — 1024 / 768 / 480, no horizontal scroll, primary CTA above fold each.
- **Conversion sanity** — 5-second test on the hero; one primary action per viewport; proof
  placed by mindset (§A); CTA is the highest-contrast element.
- **Copy honesty** — no fabricated proof; claims are true and specific.

---

## G. OUTSIDE REFERENCES

The project's own design system decides first. Reach for these only where the
system has not decided, and fetch the real content before citing one — never
imitate a page you could not read. Report which reference you used and what
changed. The full catalog lives in `ui-variant-lab`.

- **styles.refero.design** — named `DESIGN.md` directions from real sites; the
  fastest way to pick an aesthetic direction.
- **VoltAgent/awesome-design-md** — open-source `DESIGN.md` set for ~74 brands.
- **minimal.gallery** — curated minimal sites for restraint baselines.
- **component.gallery** — how ~95 design systems handle a given component.
- **microkit.co** — MIT micro-interactions on the shadcn registry.
- **aicss.dev** — agent-UI component taxonomy (Pro source; use the taxonomy).
- **kinetics.colorion.co** — spring-physics motion recipes.
- **jakubkrehel/skills** — `better-*` interface skills: typography, colors,
  layout, accessibility, writing, review.

---

## H. HANDOFF NOTE

When you finish, state: which sections you built/upgraded, the one or two signature interactions
you chose and why, which review gates passed, and anything you were unsure about (a claim you
couldn't verify, a section you cut). Don't over-explain — a defended simplification is still a
simplification.
