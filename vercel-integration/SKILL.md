---
name: vercel-integration
description: "Build and submit a Vercel integration (an OAuth integration + config UI + deploy-webhook handler under integrations/<name>/) and list it in the Vercel Marketplace. Use when creating a Vercel integration, wiring Vercel OAuth, handling a deploy-success event to trigger an external action, building the configuration UI, or fixing the Node/TS build. Covers the whole path plus the traps: a Vercel integration is an OAuth app plus a webhook/event handler (a deploy 'ready' event → an external action), the client secret + config live in the Vercel integration console, and deploy webhooks must be signature-verified before acting. Audience is developers — social-publishing fit is narrow; the useful hook is 'announce on successful deploy'. Sibling of the other integration skills (webflow-app, shopify-app). Triggers: 'build a Vercel integration', 'Vercel Marketplace', 'Vercel OAuth', 'deploy webhook', 'announce on deploy', 'Vercel integration console'."
---

# Building a Vercel integration

A Vercel integration is an **OAuth app + a configuration UI + a webhook/event handler**, listed in the **Vercel Marketplace**. Source lives in `integrations/<name>/`. Thin server over your own backend. The natural hook: **on a successful deploy, draft a social announcement**. Playbook: `itsryanarmani/scripts` `scripts/vercel-integration/README.md`.

## The trap: verify the deploy webhook before acting

Vercel posts deploy events (`deployment.created`, `deployment.succeeded`/`ready`) to your webhook URL. **Verify the signature** (the integration's client secret / webhook signing) before doing anything — an unverified handler will fire on spoofed or replayed payloads. Only act on the "ready/succeeded" event, and dedupe by deployment id.

## The other traps

1. **OAuth authorizes Vercel, your API needs its own key.** The Vercel token is for Vercel's API; carry your own credential separately (stored per-installation in the integration's config store).
2. **Client secret + config UI URL are console-owned** — set them in the Vercel integration console; placeholders break install.
3. **Node/TS build** — if it emits ESM under NodeNext, relative imports need `.js` extensions (TS2835), same as any Node ESM server.
4. **Developer audience** — a social-publishing integration on Vercel is a narrow fit; keep the value crisp ("announce your release") rather than a full dashboard.

## Build path

- OAuth callback + config UI + `/webhooks` (verify signature → on deploy-ready, draft a post via your API, `platformType` string).
- `npm run build` (tsc / your bundler).

## Submission — Vercel Marketplace

**Submittable: portal-review.** Register the integration in the **Vercel integration console** (OAuth scopes, redirect, config URL, webhook URL) → submit for marketplace review.

**Silent-rejection gotchas:** unverified webhooks; assuming the Vercel token authorizes your API; unclear value for a dev audience. TBD — confirm current console submission steps at first submission.

## Parity checklist

OAuth connect · store + validate your API key · verify + handle a deploy webhook · draft a post (`platformType`) · surface success/error.

## Related skills
- `webflow-app` — the other OAuth + webhook site/deploy integration.
- `shopify-app` — OAuth + event-driven commerce app.
