---
name: wix-app
description: "Build and submit a Wix app (a React dashboard page under integrations/<name>/ built on the Wix SDK) and list it in the Wix App Market. Use when creating a Wix app, building an embedded dashboard page, wiring Wix OAuth, calling an external API from the dashboard, or fixing a Vite build where import.meta.env is untyped. Covers the whole path plus the traps: a Wix dashboard app is an embedded page (Wix SDK / @wix/dashboard) authorized by Wix OAuth for Wix data — your own API still needs its own key — and a Vite+TS app that reads import.meta.env MUST ship a src/vite-env.d.ts with `/// <reference types=\"vite/client\" />` or tsc errors 'Property env does not exist on ImportMeta'. Sibling of the other integration skills (canva-app, monday-app, shopify-app). Triggers: 'build a Wix app', 'Wix SDK', 'Wix dashboard page', 'Wix App Market', 'import.meta.env has no env property', 'Wix OAuth'."
---

# Building a Wix app

A Wix app is commonly an **embedded dashboard page** — a React app the site owner opens in their Wix dashboard, built on the **Wix SDK** (`@wix/sdk`, `@wix/dashboard`). Source lives in `integrations/<name>/`. Thin frontend over your own backend. Playbook: `itsryanarmani/scripts` `scripts/wix-app/README.md`.

## The trap that fails the build: `import.meta.env` is untyped without vite-env.d.ts

A Vite + TypeScript app that reads `import.meta.env.VITE_*` needs `src/vite-env.d.ts` containing `/// <reference types="vite/client" />`. Miss it and `tsc` fails with **TS2339 "Property 'env' does not exist on type 'ImportMeta'"**. Vite scaffolds this file; a hand-built or worker-built app often omits it. Add the one-line reference.

## The other traps

1. **Wix OAuth authorizes Wix data, not your API.** OAuth to Wix identifies the site/instance; your own API still needs its own key, stored per-installation.
2. **Embedded page = host CSP.** Fetch only your allow-listed origin from the dashboard iframe.
3. **App ID + redirect are Dev-Center-owned** — copy the real values from the Wix Dev Center; placeholders break on install.
4. **tsconfig include** — if `vite.config.ts` is in both the app tsconfig `include` and a composite node tsconfig, tsc errors TS6305; keep `vite.config.ts` only in the node project, `include: ["src"]` for the app.

## Build path

- React dashboard page on `@wix/dashboard`; `npm run build` (`tsc --noEmit && vite build`).
- Compose/schedule a post via your API (`platformType` string); read Wix context from the SDK.

## Submission — Wix App Market

**Submittable: portal-review**

No marketplace-upload API. `@wix/cli` / Blocks deploy *code*; the listing is
portal-only: App Dashboard (`dev.wix.com`) → clear blockers → **Submit & Publish**.
That runs an automated AI review; leftover blockers must be fixed **and
resubmitted** (appeals via Wix support). Self-managed apps need a **public HTTPS
dashboard URL**; CLI/Blocks apps are hosted by Wix. Account is free; paid apps
must use **Wix Billing** + a finished payout account. Docs:
`dev.wix.com/docs/build-apps/launch-your-app`.

1. Create the app in the Dev Center. Register OAuth, permissions, and the
   dashboard-page URL (or deploy via the Wix CLI). Host over HTTPS.
2. **App Profile → App Info**: name (no "Wix", no other-brand affiliation),
   teaser, **1000×1000** 24-bit sRGB PNG icon, ≥3 feature bullets + description,
   optional Wix demo-site URL, **terms & conditions URL** (shown on consent).
3. **App Profile → Media**: 5–6 images, **≥1200×900 (4:3)** JPG/PNG (one main
   image with name + tagline); optional YouTube promo (not a tutorial); optional
   540×360 promo banner (no text/logo).
4. **Company Info**: company logo (square PNG/JPG), name ≤23 chars, address,
   website, **privacy-policy URL**. For paid apps, set pricing and finish
   payout-account setup first. Leave a **live demo account + credentials** in
   the review notes — keep it active for as long as the app is listed.
5. Clear every dashboard blocker, then **Submit & Publish**. Refresh until the
   AI review passes (or new blockers appear — those only clear on resubmit).

**Silent-rejection gotchas:** AI blockers you fixed locally but didn't resubmit;
dead demo account; name/teaser that implies Wix endorsement or another brand;
paid app that bypasses Wix Billing; missing T&Cs/privacy URL; over-broad
permissions; browser-native popups (use Wix modals — OAuth excepted); ads /
"powered by" / redirects to other stores; basic setup (fonts, colors, SEO,
GDPR, accessibility) not kept free. Human-review fallback SLA `(verify)`.

## Parity checklist

OAuth/instance context · paste + validate your API key · create/schedule a post (`platformType`) · list posts · surface success/error.

## Related skills
- `monday-app`, `canva-app` — sibling embedded dashboard/iframe apps with the same OAuth-vs-key split.
