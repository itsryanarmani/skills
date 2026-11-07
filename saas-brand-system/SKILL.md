---
name: saas-brand-system
description: Explore many distinct, fully-tokenized brand/design-system directions for a product as self-contained HTML prototypes, review them in a browser, pick one, then expand the winner into a full SaaS brand kit (logo suite, favicon/OG set, tokens, components, guidelines). Use when a user wants branding, a design system, a rebrand, a landing-page visual world, or asks to "make it look world-class / enterprise but fun / evoke emotion".
user-invocable: true
argument-hint: "[product name or path] (optional)"
---

# SaaS Brand System

Design a brand the way a good studio does: generate several **radically distinct**
directions, judge them on real screens, pick one, then build the full kit. Do not
hand-polish a single safe idea — breadth first, then depth on the winner.

The engine is **parallel fan-out**: spin up N sub-agents, each building ONE complete,
self-contained, 100%-tokenized HTML design-system prototype in a different direction.
Every prototype obeys one shared contract so they are comparable and mergeable. You (the
main model) own the *art direction* and the *pick*; sub-agents own the *typing*.

## When to use

- "Give me branding / a design system / a rebrand for X."
- "Make the site world-class / enterprise but fun / 2026 / evoke emotion."
- "Show me a few directions to pick from."
- Any time the answer is a *visual identity*, not one component.

## Workflow

### Phase 0 — Frame it (cheap, do first)

1. Read the product truth: what it does, who it's for, one canonical code sample or
   screenshot. Reuse the product's own words (CONTEXT.md / README) in copy.
2. Look at the incumbent design (tokens, CSS, a component) if one exists — it is
   evidence and anti-reference, not a starting point.
3. Ask the user ~3 decisions before spending: **direction(s)**, **boldness**
   (loud/experimental ↔ refined/restrained), **imagery** (typographic/CSS-SVG only vs
   generated raster art), **scope** (prototypes-to-pick vs straight to build). Use
   `AskUserQuestion` with concrete previews. A wrong-vibe guess wastes the whole build.

### Phase 1 — Fan out N direction prototypes (the core)

1. Write the shared contract once: `references/requirements-contract.md` — copy it to a
   scratchpad `REQUIREMENTS.md`. It pins: single self-contained `.html`, 100% tokenized
   `:root`, light+dark with persisted toggle, the full **Button Lab** (primary/secondary/
   tertiary/ghost/link × default/hover/active/focus/disabled + sizes), required sections,
   motion + reduced-motion, a11y, responsive. This contract is what makes N outputs
   comparable and later mergeable into one system.
2. Pick directions from `references/style-catalog.md` (14 proven, emotion-tagged worlds
   with palettes, fonts, signature device). Each direction MUST target a distinct emotion.
3. Launch one sub-agent per direction **in parallel, in a single message**. Each brief =
   "read REQUIREMENTS.md" + the catalog entry's art direction (concrete oklch palette,
   Google-Fonts pairing, signature visual, button spec, emotion target) + an exact output
   path. In-harness `general-purpose` agents are the reliable default (they use the Write
   tool — no sandbox/CLI-flake). Keep to the session's workflow-size guideline (batches of
   ~4–10). See `references/direction-brief-template.md`.
4. Sub-agents return a path + 3-line concept + fonts/palette. Do not read the full files.

### Phase 2 — Review in a browser (you, the judge)

1. `file://` is blocked by the claude-in-chrome extension. Serve instead:
   `cd <prototypes-dir> && (python3 -m http.server 8747 &)` then navigate to
   `http://localhost:8747/<name>.html`. Serving over http also loads Google Fonts, so
   screenshots show true type.
2. Resize to 1440×900, screenshot hero + fan-out + **Button Lab** for each. On fast scroll,
   scroll-reveal (IntersectionObserver) content can be caught mid-fade — `wait 1s` and
   re-screenshot before judging "empty section".
3. Build a scratchpad `index.html` linking all prototypes so the user can browse them.
   The user is usually on the same machine → hand them the `localhost:8747` URLs directly.

### Phase 3 — Pick + hybridize

Recommend, don't just survey. Score against the brief's emotion + audience. Offer hybrids
("direction A's structure + direction B's color"). Let the user pick via `AskUserQuestion`.

### Phase 4 — Build the full brand kit for the winner

Only now spend on depth. Expand the picked direction into a real SaaS brand system per
`references/brand-kit-checklist.md`: **logo suite** (lockups, mark, mono, inverse,
clearspace/min-size), **favicon + app-icon set** (exact sizes), **OG/social**, foundations
(tokens/type/space/motion), component library, guidelines page. In a real app, wire fonts
via the framework (e.g. `next/font`) — never a raw CDN link in production.

## Gotchas (learned)

- **Artifact/CSP blocks external hosts** — a published Artifact cannot load Google Fonts
  `<link>`, CDN JS, or remote images (fonts silently fall back). For a faithful shareable
  preview either inline `@font-face` as base64 or serve over localhost; in the shipped app
  use the framework font loader.
- **`file://` is blocked** in claude-in-chrome → always serve over http.
- **Judge from true-font screenshots**, not from an Artifact preview, when typography is
  part of the decision.
- **Don't build depth before the pick.** Logo suites / favicons for every direction is
  wasted work — one winner, then the kit.
- **Delegation:** GLM/z.ai and other third-party worker CLIs are personal-repos only and
  can be balance/throttle-dead; in-harness sub-agents are the reliable path for the
  taste-critical prototype round. Save CLI delegation for the bulk framework
  implementation after the pick.

## Related skills

- **`name-a-product`** — choose and clear the name, and register the domain, before any of this. Prerequisite.
- **`verify-branding`** — audit logo/colour consistency once the kit ships. Next step.
- **`vibebrand`** — npm package (not a skill) productizing this workflow: 14 emotion-tagged directions, oklch light+dark tokens, font pairings, generative logos, parametric mascot, CLI + SDK. `github.com/itsryanarmani/vibebrand`.

This skill owns the *identity* (directions → tokens → logo/favicon/OG → guidelines). Hand off:

- **`landing-page`** — once a brand is picked, design the marketing page's conversion anatomy
  *inside* the chosen tokens (it points back here when no brand exists yet).
- **`html-prototyper`** — prototype a new feature inside an *existing* brand's look; it points
  here when there is no brand/design system to extract yet.
- **`impeccable`** — the craft floor for any single surface (visual hierarchy, motion, a11y).
- **`storybook-to-design-system`** — once the components ship, surface them as a live in-app
  design-system gallery.
- **`brand-router`** — once a direction is picked, the twenty-one-direction suite runs it across a person's non-web surfaces (voice, Instagram carousels, YouTube thumbnails and edit style, LinkedIn, podcast, decks). Product identity here; whole-person consistency there. See [`../brand-router/README.md`](../brand-router/README.md).
- **`high-fidelity-ui-image-gen`** — AI mockups of a direction before/without building the HTML.

## References

- `references/requirements-contract.md` — the shared per-prototype contract (copy to REQUIREMENTS.md)
- `references/style-catalog.md` — 14 emotion-tagged brand directions (palette/font/signature)
- `references/direction-brief-template.md` — the per-sub-agent brief shape
- `references/brand-kit-checklist.md` — everything a shipped SaaS brand needs
