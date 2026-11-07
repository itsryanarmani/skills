---
name: figma-plugin
description: "Use when building or debugging a Figma plugin (code.js sandbox plus ui.html iframe): export a frame and call an API, decide where fetch runs, set networkAccess.allowedDomains, or store a key in figma.clientStorage. Publishing is figma-plugin-submission."
---

# Building a Figma plugin

A Figma plugin is **two programs talking over `postMessage`**: `code.js` runs in Figma's plugin sandbox (no DOM, no `window`) and `ui.html` runs in an iframe (full DOM). `manifest.json` declares both (`main`, `ui`) plus `networkAccess.allowedDomains`. Source lives in `integrations/figma-plugin/`. It is a thin frontend over your own backend — your product's SDK or public REST API. Read this before the first file; the command-level playbook is in `itsryanarmani/scripts` `scripts/figma-plugin/README.md`. To publish to Community, use `figma-plugin-submission`.

## When to use

- **Triggers:** 'build a Figma plugin', 'Figma Plugin API', 'exportAsync', 'figma.clientStorage', 'networkAccess allowedDomains', 'my Figma plugin fetch fails'.
- The two-context split: the sandbox has no DOM but no CORS; the iframe has DOM and full CORS. Every external origin must be in networkAccess.allowedDomains.
- The sandbox has no FormData or Blob, so multipart uploads are hand-built byte arrays; the UI ships as one HTML file inlined via __html__; export is async via exportAsync.
- Siblings: figma-plugin-submission, canva-app, browser-extension, shopify-app, connector-directory-submission.

## The trap that wastes a day: fetch in the wrong context

The two contexts have **opposite network rules**:

- `code.js` (sandbox): `fetch` exists and **CORS is not enforced** — but there is **no DOM**: no `FormData`, no `Blob`, no `FileReader`, no `URL.createObjectURL`.
- `ui.html` (iframe): full DOM, but `fetch` is an ordinary browser fetch — **CORS applies**.

If your API sends no CORS headers (most don't), a browser-side fetch from the UI is blocked and the failure looks like a generic network error with no useful console message. Put **every** API call in the sandbox; the UI sends intents over `parent.postMessage` / `figma.ui.postMessage` and renders the results. Keep the API key sandbox-side too (`figma.clientStorage`) so the secret never enters the iframe.

**Rule:** before debugging "my request fails," check which side runs the fetch. If the API has no CORS headers, the fetch belongs in `code.js`.

## The manifest is the contract

Everything Figma needs to know lives in `manifest.json` — and everything reviewers check is derived from it:

```json
{
  "name": "<Plugin name>",
  "api": "1.0.0",
  "main": "code.js",
  "ui": "ui.html",
  "editorType": ["figma"],
  "networkAccess": {
    "allowedDomains": ["https://api.example.com", "https://uploads.example-cdn.com"],
    "reasoning": "Plain-English sentence per origin: what is fetched and why. Shown to reviewers."
  }
}
```

`main` and `ui` are **build outputs**, not sources — write TypeScript in `src/` and compile. Mint a plugin `id` into this file before `figma.clientStorage` will work; see `figma-plugin-submission`. Both output files are typically git-ignored; rebuild after pulling.

## The other traps that each cost a round-trip

1. **Every origin must be allow-listed in `networkAccess.allowedDomains`.** Exact origins with scheme (`https://api.example.com`) — including CDN upload hosts and any image/thumbnail hosts the UI renders. `networkAccess.reasoning` is required alongside the list and is shown to reviewers. A missing domain fails at runtime, not at build time.
2. **No multipart helpers in the sandbox.** Build `multipart/form-data` bodies by hand with `TextEncoder` + `Uint8Array` and a boundary string (see `example.ts`).
3. **The UI ships as ONE self-contained HTML file.** `figma.showUI(__html__)` loads the compiled `ui.html`; the build step inlines the bundled JS into a `<script>` placeholder in the HTML template. No external scripts or stylesheets unless their origin is allow-listed.
4. **Export is async.** `node.exportAsync({ format: "PNG", constraint: { type: "SCALE", value: n } })` returns a Promise of `Uint8Array`. There is no synchronous getter — await it.
5. **`figma.clientStorage` needs a plugin ID in the manifest.** Mint it before first publish — see `figma-plugin-submission`. Do not wait for Community to assign one.
6. **`editorType` gates where the plugin loads.** `["figma"]` loads only in Figma design. Add `"figjam"` or `"dev"` only if the plugin actually supports them — reviewers check.

## Build path

- esbuild: `src/code.ts → code.js` (bundle, IIFE, target `es2017` for the sandbox runtime); `src/ui.ts` bundled and inlined into `ui.html`. Types come from `@figma/plugin-typings`.
- Define one typed message union per direction (UI→sandbox intents, sandbox→UI results) with a `requestId` to correlate async replies — a bare `postMessage` free-for-all does not scale past two buttons.
- Dev loop: Figma desktop app → **Plugins → Development → Import plugin from manifest…** → select `manifest.json` → run from **Plugins → Development**. Re-run the plugin after each rebuild; there is no hot reload.
- State: `figma.clientStorage` persists per-user per-device (API keys, preferences) and is readable only from the sandbox. It throws without a plugin `id`; see `figma-plugin-submission`. React to selection changes with `figma.on("selectionchange", …)` and push the new selection to the UI; use `figma.notify(...)` for transient success toasts.
- Debugging: sandbox logs appear in the desktop app's **Plugins → Development → Open console**; UI iframe logs need the iframe devtools. If a log line never appears, suspect the other context.
- API calls: your product's SDK or public REST API, always from the sandbox. Keep business logic server-side; the plugin is a thin client.

## Submission — Figma Community

The Community publish path is the `figma-plugin-submission` skill: minting a plugin ID so `figma.clientStorage` works, listing assets, Data security, and first publish. This skill stops at a working local plugin.

## Parity checklist (prove in a real Figma session before publishing)

select a frame · export PNG · upload to your API · create the downstream action · surface success/error in the plugin UI · authenticate from a clean state (empty `clientStorage`).

## Related skills

- `figma-plugin-submission` — the Community publish path: plugin ID / `clientStorage`, listing assets, Data security.
- `canva-app` — the same "design → export → do something" shape on Canva; different SDK, portal-held allow-list instead of a manifest field.
- `browser-extension` — another split-context/CSP surface; the message-passing lesson rhymes.
- `connector-directory-submission` — the cross-marketplace submission router.
