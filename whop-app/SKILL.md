---
name: whop-app
description: "Build and submit a Whop app (a React app under integrations/whop-app/ embedded as an iframe view inside a Whop, built on the Whop SDK) and list it on the Whop App Store. Use when creating a Whop app, embedding a tool inside a creator's Whop, wiring 'Sign in with Whop' (OAuth 2.1 + PKCE), calling an external API from the embed, or figuring out the dev-proxy → versioned-build → review submission. Covers the whole path plus the traps: the app runs in a Whop iframe (the Whop user context comes from the SDK, but any OTHER service — your own API — needs its own auth/key, Whop's OAuth does not authorize it), the App ID + redirect are dashboard-owned, and apps can charge money (Whop takes a cut). Sibling of the other integration skills (canva-app, shopify-app, wix-app). Triggers: 'build a Whop app', 'Whop SDK', 'Sign in with Whop', 'publish to the Whop App Store', 'Whop dev proxy', 'my Whop app can't reach my API'."
---

# Building a Whop app

A Whop app is a **React app embedded as an iframe view inside a Whop** (a creator's community/storefront), built on the **Whop SDK** (`@whop/react`, `@whop/iframe`, `@whop/api`/`@whop/sdk`). Source lives in `integrations/whop-app/`. Thin frontend over your own backend. Command-level playbook: `itsryanarmani/scripts` `scripts/whop-app/README.md`.

## The trap that wastes a day: Whop auth ≠ your service's auth

"Sign in with Whop" (OAuth 2.1 + PKCE) tells you **who the Whop user is** and what they've purchased. It does **not** authorize calls to any *other* service. If your app calls your own API, that API needs its **own** credential (a team API key, or your own OAuth) — carried separately. Wiring Whop login and expecting your API calls to be authorized is the classic first-day mistake: Whop identifies, your key authorizes.

## The other traps

1. **App ID + redirect URLs are dashboard-owned.** The app's ID and OAuth redirect/callback URLs live in the Whop dashboard; a placeholder ID runs in the dev proxy but breaks on install/submit. Copy the real values in early.
2. **The embed is an iframe** — external fetches follow the host CSP; keep all calls to your own allow-listed origin, and store the user's key per-installation (not globally).
3. **Apps can charge money** — Whop handles billing and takes a cut; if you gate features by plan, read entitlement from the Whop SDK, don't reinvent it.
4. **Inline-style/JSX typing** — the Whop UI kit is strict; cast web-only CSS props (e.g. `WebkitBoxOrient`) to a real `CSSProperties` value, not `as unknown as string` (that fails `tsc`).

## Build path

- Scaffold from Whop's app template; run the **dev proxy** (`whop-proxy` / the SDK's dev command) so the local app loads inside a real Whop for testing.
- UI: React + the Whop SDK hooks for user/entitlement context. Business logic stays server-side.
- `npm run build` produces the bundle/app served at your hosted URL (Whop embeds a URL, not a static upload).

## Submission — Whop App Store

**Submittable: API**

Scriptable create + ship. REST: `POST https://api.whop.com/api/v1/apps` (name,
`company_id`, HTTPS `base_url`, `route`, `icon`, `redirect_uris`),
`PATCH /apps/{id}` (`description`, `app_store_description`, `icon`, `status`),
`POST /files` then `POST /app_builds` (`attachment`, `checksum`, `platform: web`),
`POST /app_builds/{id}/promote` (draft builds enter review first). CLI:
`whop apps deploy` (build + typecheck + upload + promote; `--preview` skips live).
Dashboard: `whop.com/dashboard/developer`. Account is free. The iframe app needs a
**public HTTPS `base_url`** (or a `*.whop.app` hosted site) — Whop embeds your
URL. Discovery/`status` live needs name + icon + description. Monetized apps bill
through Whop (dev rev-share often quoted 10–30% plus platform cut — verify).

1. Create the app (dashboard or `POST /apps`) → copy the real App ID + OAuth
   redirects. Set Hosting paths (experience `/experiences/[experienceId]`,
   dashboard `/dashboard/[companyId]` as needed).
2. Point `base_url` at your public HTTPS origin. Test inside a real Whop via
   `whop-proxy` / `whop apps dev`.
3. Fill store metadata (`PATCH /apps/{id}` or the dashboard): name, short
   description, longer `app_store_description`, **icon** (file upload; exact px:
   verify). Screenshots / 10–20 s demo video if the listing UI asks `(verify)`.
4. Upload a versioned web build (`POST /app_builds` or `whop apps deploy`).
5. Promote (`POST /app_builds/{id}/promote` or `whop apps builds promote <id>`).
   Unapproved builds go to review; an approved build becomes the production
   App Store version. "Verified" is a separate endorsement, not automatic.

**Silent-rejection gotchas:** placeholder App ID / redirect; assuming Whop OAuth
authorizes *your* API; `base_url` that isn't reachable HTTPS; promoting a build
whose view types don't match the hosted paths; unpaid entitlement flow that
doesn't read Whop access; listing with no icon/description so discovery stays
off. Review SLA + current icon/screenshot spec: (verify).

## Parity checklist (prove in a real Whop embed)

Sign in with Whop · read the user/entitlement context · authenticate your own API separately · create/schedule a post (`platformType` string) · list posts · surface success/error.

## Related skills
- `canva-app`, `wix-app` — other iframe-embedded marketplace apps; the "host identifies, your key authorizes" split recurs.
- `shopify-app` — the other marketplace with a real business/billing gate.
