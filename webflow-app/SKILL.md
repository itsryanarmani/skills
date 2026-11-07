---
name: webflow-app
description: "Build and submit a Webflow app (a Designer extension + an OAuth/webhook server under integrations/<name>/) and list it in the Webflow marketplace. Use when creating a Webflow app, wiring OAuth to Webflow, handling a CMS-publish webhook to trigger an external action, building the Designer-extension panel, or fixing a NodeNext server build that rejects extensionless imports. Covers the whole path plus the traps: a Webflow app is usually TWO programs — a Designer extension (iframe UI, bundler resolution) and a Data-client/server (OAuth + webhooks, Node ESM) — and the server half, compiled with module/moduleResolution NodeNext, REQUIRES explicit .js extensions on every relative import (including dynamic import()) or tsc errors TS2835. Sibling of the other integration skills (shopify-app, wix-app). Triggers: 'build a Webflow app', 'Webflow Designer extension', 'Webflow OAuth', 'CMS publish webhook', 'TS2835 needs explicit file extensions', 'publish to the Webflow marketplace'."
---

# Building a Webflow app

A Webflow app is commonly **two programs in one package**: a **Designer extension** (an iframe panel in the Webflow Designer, bundled by Vite) and a **Data client / server** (OAuth + CMS webhooks, run as Node ESM). Source lives in `integrations/<name>/` with two build targets. Thin frontend + thin backend over your own API. Playbook: `itsryanarmani/scripts` `scripts/webflow-app/README.md`.

## The trap that wastes a build: NodeNext demands `.js` on every relative import

The server (`tsconfig.server.json` with `"module": "NodeNext"`, `"moduleResolution": "NodeNext"`, real `outDir` emit for Node) enforces **explicit file extensions on relative imports** — `import { x } from "./config.js"`, not `"./config"`. Miss one and `tsc` fails with **TS2835** ("Relative import paths need explicit file extensions…"). It bites **static AND dynamic** imports (`await import("../storage.js")`). Do NOT "fix" it by switching the server to bundler resolution — the emitted ESM runs under Node, where the extensions are required at runtime too. Add the `.js` extensions.

## The other traps

1. **Two tsconfigs, two resolutions.** The Designer half uses `"moduleResolution": "bundler"` (Vite, no extensions); the server half uses NodeNext (extensions required). Don't cross the wires.
2. **OAuth + webhook secrets are app-owned.** The client ID/secret + webhook signing secret come from the Webflow app registration; verify the webhook signature server-side before acting.
3. **The Designer extension is a sandboxed iframe** — external fetches follow the host CSP; call only your own origin, store the key per-site.

## Build path

- `build: build:designer (vite) && build:server (tsc -p tsconfig.server.json)`.
- Designer panel: compose/trigger from the Designer. Server: OAuth callback + `/webhooks` (CMS item publish → draft a post via your API, `platformType` string) + a proxy to your API.
- Point the Vite `outDir` INSIDE the package (a `../../dist` outDir writes to the repo root — a wart; keep build output local).

## Submission — Webflow marketplace

**Submittable: portal-review.** Register the app in the Webflow developer dashboard (scopes, OAuth redirect, webhook URL) → submit for marketplace review. Provide the hosted server URL.

**Silent-rejection gotchas:** TS2835 (above); unverified webhook signatures; a Vite `outDir` escaping the package. TBD — confirm current scopes + review SLA at first submission.

## Parity checklist

OAuth connect · verify + handle a CMS-publish webhook · draft a post (`platformType`) · list posts · Designer-panel compose · surface success/error.

## Related skills
- `shopify-app` — the other OAuth+webhook commerce/site app.
- `wix-app`, `canva-app` — sibling iframe dashboard/embed apps.
