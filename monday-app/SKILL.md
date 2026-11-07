---
name: monday-app
description: "Build and submit a monday.com app (a React board/item view under integrations/<name>/ built on the monday apps SDK) and list it in the monday marketplace. Use when creating a monday app, building a board or item view, wiring monday OAuth/session, turning a board row into an external action, or fixing a Vite build where import.meta.env is untyped. Covers the whole path plus the traps: a monday view runs embedded in the board (monday-sdk-js / @mondaycom/apps-sdk gives context + a session token, not authorization for YOUR API), and a Vite+TS app reading import.meta.env needs src/vite-env.d.ts or tsc fails. Sibling of the other integration skills (wix-app, airtable-extension). Triggers: 'build a monday.com app', 'monday apps SDK', 'monday board/item view', 'monday marketplace', 'monday OAuth', 'import.meta.env untyped'."
---

# Building a monday.com app

A monday.com app is commonly a **board or item view** — a React app embedded in a monday board, built on the **monday apps SDK** (`monday-sdk-js` for context/API, `@mondaycom/apps-sdk` for server bits). Source lives in `integrations/<name>/`. Thin frontend over your own backend. Playbook: `itsryanarmani/scripts` `scripts/monday-app/README.md`.

## The trap: monday's session token ≠ your API's auth

`monday.get("context")` + the session token identify the user/board and authorize **monday's** API. Your own API still needs its **own** key, stored per-installation. Don't send monday's token to your backend expecting it to authorize.

## The other traps

1. **`import.meta.env` untyped** — a Vite + TS app needs `src/vite-env.d.ts` with `/// <reference types="vite/client" />`, or `tsc` errors TS2339 "Property 'env' does not exist on type 'ImportMeta'".
2. **The view is an embedded iframe** — fetch only your allow-listed origin; the board context arrives via `monday.listen("context")`.
3. **App features + scopes are dashboard-owned** — declare the view feature + OAuth scopes in the monday Developer Center; a placeholder app id breaks on install.

## Build path

- React view listening to monday context; `npm run build` (`tsc --noEmit && vite build`).
- Row/item → your API create call (`platformType` string); write status back to a column if useful.

## Submission — monday marketplace

**Submittable: portal-review**

No marketplace-upload API. `@mondaydotcomorg/apps-cli` / monday-code deploy *code*;
you publish a shareable install link, then submit a **web form** (Developer Center
→ **Submit app** → Submission form; also `forms.monday.com` — exact form id:
verify). Review is a human team on a shared monday board (first reply within **72
business hours**). Account is free; the app needs a **public hosting URL** (your
host or monday code). Apps built primarily with no-code / "vibe code" are **not
eligible**. Docs: `developer.monday.com/apps/docs/submit-your-app`.

1. `apps.developer.monday.com` → create the app → declare features, OAuth scopes,
   and the view hosting URL. Request only the scopes you use.
2. **Share** tab → publish the app (produces an `auth.monday.com` install link
   the form requires).
3. Listing copy: name ≤30 chars, no emoji, do **not** start with "monday" /
   "monday.com"; short description ≤60 chars; long description 200–2,000 chars
   (listing-page checklist also says 200–2,500 — verify); up to 10 keywords +
   ≤3 categories; plan names/bullets if you monetize.
4. Graphics: **192×192** JPG/PNG app icon + developer icon, **592×348** app-card
   image, **3–5 gallery images at 1920×960**, promo video **≤120 s / 50 MB**
   (guidelines prefer 30–60 s HD MP4 — verify). Public **privacy-policy** + **ToS**
   URLs under the same legal entity; support email on a domain you prove you own
   (JSON well-known — see privacy/security checklist).
5. Submit the form. Review covers product, engineering, **Burp scan of every
   domain**, encrypted tokens, documented scopes, PII handling, and listing
   assets. Fix flags on the shared board; they re-review. SOC2/ISO is optional
   (Shield Badge only). Paid apps bill through monday (rev-share often quoted
   0% until $200k lifetime, then 85/15 — verify).

**Silent-rejection gotchas:** no-code / AI-generated primary codebase; duplicate
of an existing marketplace app / no unique value; sending monday's session token
to your API; over-broad scopes; name that uses the monday trademark; failed Burp
scan; secrets in the repo; missing ToS/privacy; support email on a domain you
don't own; wrong asset dimensions. Exact form URL + current video length: (verify).

## Parity checklist

read board/item context · paste + validate your API key · row → scheduled post (`platformType`) · list posts · surface success/error.

## Related skills
- `monday-app-submission` — the Developer Center half: version locking, branding edits, the install link, and the ~25-field submission form.
- `wix-app`, `airtable-extension` — sibling embedded productivity-tool apps; same OAuth/session-vs-key split.
