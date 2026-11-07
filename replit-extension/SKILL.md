---
name: replit-extension
description: "Build and submit a Replit Extension (a React tool panel under integrations/<name>/ built on the Replit Extensions API) and list it in the Replit Extensions store. Use when creating a Replit extension, building a workspace tool panel, calling an external API from the extension, or fixing type errors where a typed API-result wrapper doesn't match the SDK's actual return. Covers the whole path plus the traps: the extension is a React panel in the Replit workspace (@replit/extensions), and a hand-rolled `unwrap`/`ApiResult` helper that over-specifies the shape of a client method's return (e.g. asserting `data: T[]` when the client returns `{ data?: T[] }`) produces cascading TS2352/TS2345 errors — narrow at the call site instead. Sibling of the other integration skills (raycast-extension, browser-extension). Triggers: 'build a Replit extension', 'Replit Extensions API', '@replit/extensions', 'Replit extensions store', 'my API-result type does not match the SDK return'."
---

# Building a Replit Extension

A Replit Extension is a **React tool panel inside the Replit workspace**, built on the **Replit Extensions API** (`@replit/extensions`). Source lives in `integrations/<name>/`. Thin frontend over your own backend — useful for "announce a shipped Repl" flows. Playbook: `itsryanarmani/scripts` `scripts/replit-extension/README.md`.

## The trap that cascades: over-typed result wrappers

A local helper that asserts a client method returns exactly `{ data: T[] }` — when the SDK actually returns `{ data?: T[] | undefined }` or `T[] | { data: T[] }` — produces a wall of **TS2352 / TS2345** "not comparable / not assignable" errors that cascade through every caller. Fix the shape at the boundary: type the wrapper to the SDK's *actual* return (optional/union), and narrow with `Array.isArray(x) ? x : x.data ?? []` at the call site. Don't paper it with `any`.

## The other traps

1. **`import.meta.env` untyped** — Vite + TS needs `src/vite-env.d.ts` with the `vite/client` reference (TS2339 otherwise).
2. **Workspace panel, not a page** — the extension mounts in Replit's tool dock; store the API key in the extension's own storage, per-user.
3. **Manifest/config** declares the tool + permissions; a placeholder id runs in dev but not published.

## Build path

- React panel on `@replit/extensions` (New Post / Queue / Accounts commands map well); `npm run build`.
- Compose/schedule a post via your API (`platformType` string); list upcoming posts.

## Submission — Replit Extensions store

**Submittable: portal-review.** Develop against the extension dev tools, then publish to the **Replit Extensions store** for review. Note the audience is developers — social-publishing fit is narrow; scope the value accordingly.

**Silent-rejection gotchas:** over-typed wrappers; missing `vite-env.d.ts`; unclear value for a dev audience. TBD — confirm current store submission steps at first submission.

## Parity checklist

paste + validate your API key · compose + schedule a post (`platformType`) · list posts · surface success/error.

## Related skills
- `raycast-extension` — the other developer-power-user command surface.
- `browser-extension` — sibling per-device-storage tool.
