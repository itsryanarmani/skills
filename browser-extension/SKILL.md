---
name: browser-extension
description: "Use when building, QA'ing or publishing a Manifest V3 browser extension: one manifest for Firefox and Chrome, CSP fixes for workers and wasm, on-device AI, content-script text insertion, storage, and store submission to AMO, Chrome Web Store, Edge, Opera, Whale or Safari."
---

# Cross-Browser Web Extension: Build & Ship

**One codebase, two stores.** A Manifest V3 extension runs on both Firefox and Chrome if you keep the browser differences in the manifest, not the code. This skill is the build layout, the CSP traps that cost the most time, and the exact submission flow per browser.

Describe-only: this documents the approach and the gotchas. Write the actual extension code in the target repo.

---

## When to use

- **Triggers:** 'build a browser/Firefox/Chrome extension', 'MV3 extension', 'submit to AMO', 'publish to Chrome Web Store', 'web-ext', 'sign my add-on', 'extension CSP blocks my worker/wasm', 'local AI in an extension', 'reply/post button disabled after inserting text', 'execCommand insertText', 'content script into X/LinkedIn composer', 'chrome.storage.sync keeps restoring old token', 'test/QA a loaded extension', 'drive extension with browser automation', 'chrome ignores --load-extension', 'submit to Edge Add-ons', 'Microsoft Partner Center extension', 'publish to Opera', 'Naver Whale store', 'safari-web-extension-converter', 'port my extension to Safari', 'which stores can I publish my extension to', 'SharedArrayBuffer in extension', 'manifest sandbox key', 'BiDi screenshot moz-extension', 'AMO throttled', 'container leaks WebRTC'.
- The one-manifest-two-browsers layout; CSP rules that break WebAssembly and web workers, and the same-origin-worker fix; on-device AI via Firefox `browser.trial.ml` and Chrome's Prompt API; `web-ext` build and lint.
- Store flows: AMO with its mandatory 2FA/AAL2 gate, the Chrome Web Store, Edge Add-ons (free, Partner Center, REST submission API for CI), Opera and Naver Whale (same zip, dashboard only), and why Safari is a rewrite (Xcode app, $99/yr program, no `offscreen` or `sidePanel`).
- After the build: text into Draft.js/Quill/Lexical composers when the send button stays disabled, per-device auth state (storage.local vs sync, self-heal, sign-up races), and QA of an unpacked extension with browser automation.
- Firefox agent-extension facts: no SharedArrayBuffer in extension pages, the `sandbox` key and its CSP trap, event pages that unload with a port open, WebRTC that escapes `webRequest` and `proxy`, WebDriver BiDi QA of `moz-extension:` pages, and AMO signing in CI (per-account throttle, re-runnable release).

## 1. Project layout

Keep source in one folder (e.g. `src/`) so the package root is unambiguous:

```
src/
  manifest.json         # the only file with browser-specific keys
  background.js         # shared logic — loaded by BOTH browsers (see §3)
  <ui>.html / <ui>.js   # popup / options / full pages
  assets/               # icons (16/32/48/96/128 png), images
  vendor/               # third-party libs, vendored (no CDN — CSP blocks it)
package.json            # scripts: build, lint, start, test
```

Icons: ship `16, 32, 48, 96, 128` px PNGs. If you author a logo as SVG, rasterize to those sizes as a build step (a headless browser rendering the SVG at each size works and needs no image toolchain).

---

## 2. The manifest is where browsers differ

Both stores read `manifest_version: 3`, but each ignores keys it doesn't understand — exploit that to ship one manifest:

- **Firefox-only:** `browser_specific_settings.gecko` — set `id` (e.g. `name@author`), `strict_min_version`, and (required by AMO now) `data_collection_permissions.required` (use `["none"]` if you collect nothing).
- **Background script (the #1 cross-browser gotcha):** Chrome MV3 wants `background.service_worker`; Firefox MV3 wants `background.scripts`. Declare **both**, pointing at the same file:
  ```json
  "background": { "service_worker": "background.js", "scripts": ["background.js"] }
  ```
  `web-ext lint` warns `background.service_worker is not supported` — that warning is expected and harmless; each browser reads its own key.
- **API namespace in code:** Firefox exposes `browser.*` (promises); Chrome exposes `chrome.*` (callbacks, plus a partial `browser` in newer versions). Start every file with `const api = globalThis.browser ?? globalThis.chrome;` and use promise-style APIs (Chrome MV3 supports them).
- **Permissions:** put anything not always needed in `optional_permissions` and request it at runtime **from a user gesture** (a click) — some permissions (like Firefox's `trialML`) are only grantable that way.

---

## 3. CSP: the traps that eat a day each

MV3 extension pages run under a strict Content-Security-Policy. Two things break silently:

- **WebAssembly** needs `'wasm-unsafe-eval'` in `script-src`. Without it, any wasm library fails to instantiate.
- **Web workers from `blob:` URLs are blocked.** Many libraries (map renderers, parsers) spawn their worker from a `blob:`. The extension CSP `worker-src` does not allow `blob:` and you generally can't add it. **Fix:** use the library's "CSP build" if it has one — it ships the worker as a *separate file* you load same-origin via `worker-src 'self'` and a `setWorkerUrl(api.runtime.getURL("vendor/thing-worker.js"))`-style call. No CSP build? Vendor the worker file yourself and point the library at it. Never rely on `blob:` workers.
- **Declare CSP explicitly** so dev tooling doesn't fight you:
  ```json
  "content_security_policy": {
    "extension_pages": "script-src 'self' 'wasm-unsafe-eval'; worker-src 'self'; object-src 'self'; connect-src 'self' https://api.example.com; img-src 'self' data: blob:"
  }
  ```
  Add each remote origin your extension actually fetches to `connect-src` (and `img-src`), and mirror them in `host_permissions`. Everything else stays `'self'`.
- **No CDN. Vendor everything.** `script-src 'self'` blocks remote scripts — copy libraries into `vendor/`. This also makes review faster and the package self-contained.
- **`web-ext run` (dev) replaces your CSP** with a looser dev one, which can *hide* a blob-worker failure that then reappears in the packaged build. Always verify the real thing by loading the built package (temporary add-on / load-unpacked), not just `web-ext run`.

---

## 4. On-device AI (optional, but the whole pitch for some extensions)

Both browsers now ship local models — zero inference cost, nothing leaves the device.

- **Firefox — `browser.trial.ml`** (FF 142+; text-generation needs Nightly with `browser.ml.enable=true` and `extensions.experiments.enabled=true`). Request the `trialML` optional permission from a user gesture, then `createEngine({ modelHub, taskName, modelId, dtype })` + `runEngine({ args })`. Model must come from a **blessed HF org** (Mozilla / Xenova). A known-working small combo: `Xenova/Qwen1.5-0.5B-Chat` with `dtype: "q4"`. First run downloads the model (slow, shows progress); cache it.
- **Chrome — built-in Prompt API** (`LanguageModel` / `window.ai`). Different API, same idea.
- **Design for absence.** These are gated/experimental. Build a capability probe with a graceful floor: `mock → Firefox trial.ml → Chrome Prompt API → deterministic heuristic`. The extension must stay fully usable when no model is available — never hard-depend on the model.
- **Safety pattern for generated content:** if a model emits config/params, validate against a schema and run through your own interpreter. Never `eval` model output or let it execute as code.

---

## 5. Build, lint, test

Use Mozilla's **`web-ext`** (works for Chrome packaging too):

```
web-ext build   --source-dir src   # → web-ext-artifacts/<name>-<version>.zip  (this is the upload)
web-ext lint    --source-dir src   # 0 errors; the dual-background warning is expected
web-ext run     --source-dir src   # scratch Firefox with the extension loaded (dev CSP — see §3)
```

- **Firefox dev install:** `about:debugging#/runtime/this-firefox` → *Load Temporary Add-on* → pick `src/manifest.json` (gone on restart).
- **Chrome dev install:** `chrome://extensions` → *Developer mode* → *Load unpacked* → select `src/`.
- **e2e:** drive the built extension with a browser-automation tool; assert no console errors and that dangerous actions (closing tabs, network writes) hold their safety invariants. Keep generators deterministic (seed instead of `Math.random`/`Date`) so tests are stable.

---

## 6. Submit to Firefox (AMO — addons.mozilla.org)

It's a multi-step wizard. In order:

1. **Create a Firefox add-on developer account** at addons.mozilla.org.
2. **2FA is mandatory to submit.** AMO submission requires an `AAL2` (two-factor) session. If the account has no 2FA, Mozilla forces `inline_totp_setup` mid-flow: scan the QR with an authenticator app, enter the 6-digit code, and **save the recovery codes** before continuing. There is no way around this gate — an automation agent cannot complete it for the user; the human must do the TOTP step.
3. **Distribution agreement** — Developer Hub → *Submit a New Add-on* → tick both agreement checkboxes → Accept.
4. **Listed vs unlisted** — a genuine fork in the road, confirm with the user before committing:
   - *Listed* — public on AMO, discoverable, Mozilla reviews it.
   - *Unlisted* — Mozilla only signs it; you self-distribute the signed file (needs `update_url` in the manifest for auto-updates). Still installs cleanly.
5. **Upload** `web-ext-artifacts/<name>-<version>.zip`. AMO auto-runs validation. **"Validated with no errors and N warnings" is fine to proceed** — warnings don't block. The dual-background (`service_worker is not supported`) and "Unsafe assignment to innerHTML" warnings are expected; they're flagged as "issues that can lead to rejections" but the reviewer-notes disclosure (step 8) covers them.
6. **Compatibility** — tick the target apps (Firefox desktop; add *Firefox for Android* only if it actually works there — WebGL/experimental-API extensions usually don't).
7. **"Do you need to submit source code?"** — answer **No** if you use no minifier / bundler (webpack) / template engine / transpiler. Hand-written, as-shipped source = No. (AMO asks this both before *and* after the details form — answer consistently.)
8. **Details form** — name and summary are pre-filled from the manifest `name`/`description`. Add a longer description, pick **category** (e.g. Games & Entertainment), choose a **license** (an OSS license, or *All Rights Reserved* for a closed/private codebase — changeable later), optional privacy policy, and **Notes to Reviewer**. In the notes disclose everything a reviewer would otherwise flag: runtime network access and why (no-key host, no user data), vendored libraries **with licenses** (BSD/MIT), no build step, an explanation for each validation warning, any dangerous-looking permission (e.g. `tabs`) and its safety model, and how to test any gated feature (e.g. on-device AI needs Nightly + a pref; otherwise it falls back). Honesty here is the difference between fast approval and a round-trip.
9. **Submit Version** → the second source-code question → **Finish**. You land on "Version Submitted ✨". Publication takes up to ~24h, longer if selected for manual review; a confirmation email follows. Mozilla **signs** it — signed add-ons install in one click and auto-update.

**Pause before "Submit Version"** if driving via automation — that's the irreversible public step. Let the user do auth/2FA, approve listed-vs-unlisted, and okay the final button.

*Automation note:* AMO's radio inputs (distribution, source-code, license) are custom-styled — a coordinate/ref click often won't register; use a semantic `check`/label action, and click the wizard's `Continue`/`Submit` buttons via a role locator (scroll into view first). Verify each `checked=true` before advancing.

---

### The AMO upload throttle

AMO limits how many uploads one account makes in a period. A batch of new add-ons hits it fast.

- **It covers new uploads on every route.** The API (`web-ext sign`) answers `Request was throttled.
  Expected available in N seconds`. The web form ("Submit a New Add-on") validates the file, then refuses it
  with "You have submitted too many uploads recently." The browser is not a way past it.
- **Retrying while throttled makes the wait longer.** On one run, three tries 15 minutes apart moved the
  window from about 4 hours to about 13.7 hours. Make one try when the window opens; do not loop.
- **Edits to an existing version are not limited the same way.** When an API `PATCH` of `source` on a
  version was throttled, the version page's **Source code** field and **Save Changes** accepted the same
  zip at once. Use the form for source, notes and listing edits while uploads are blocked.
- **Make CI safe to re-run.** Before `web-ext sign`, check whether AMO already has this exact version
  (listed); skip the upload if it does. Then a manual upload and a CI retry cannot submit one version twice.

## 7. Submit to Chrome (Chrome Web Store)

The **same zip** works — Chrome reads `manifest_version`, `background.service_worker`, `content_security_policy.extension_pages`, `permissions`, `icons`, and **ignores the Firefox-only keys** (`browser_specific_settings`, `background.scripts`). No separate Chrome package needed.

1. One-time developer registration at the Chrome Web Store Developer Dashboard (**US$5**, once, covers all your items). Sign in with the Google account you want to own the listing.
2. Dashboard → **Add a new item** → **Select file** → upload the zip. **This creates a private draft — it does NOT publish.** Publishing is a separate *Submit for review* click after the listing is complete, so uploading is safe.
3. **Store listing tab** — title + summary auto-fill from the manifest. Fill **Description**, **Category**, **Language**, and upload the **Store icon** (128×128) + **Screenshots** (≥1 at exactly **1280×800** or 640×400; AMO lets you skip screenshots, Chrome does not). Promo tiles (small 440×280, marquee 1400×560) are optional.
4. **Privacy tab** (stricter than AMO, and the usual rejection cause). Every field here is required:
   - **Single-purpose description** — one sentence (Chrome enforces the single-purpose policy).
   - **Per-permission justification** — a separate box for *each* permission **and** for host permissions; write one line each. Unjustified/over-broad permissions stall review.
   - **"Are you using remote code?"** — **No** if you vendor everything and run no `eval`/remote `<script>`/external module (wasm bundled in the package is *not* remote code). Answering Yes forces an extra justification.
   - **Data usage** — leave every data-type box unchecked if you collect nothing, but you **must still tick the three certification checkboxes** (no-sell, single-purpose-use, no-creditworthiness).
   - **Privacy policy URL — required even when you collect no data.** Host a short policy (a `PRIVACY.md` in a public repo works — use its github.com blob URL) and paste it.
5. **Submit for review.** Chrome doesn't "sign" like AMO — approved items just go live. Use *"Why can't I submit?"* to list remaining required fields.

### Real-run quirks (cost hours; automate around them)

- **Material dropdowns resist synthetic clicks.** Category/Language are Angular Material selects — clicking the overlay option often doesn't register. **Keyboard typeahead works:** focus the trigger, type the option's first letter(s), `Enter`. For a variant (e.g. "English (United States)") type the letter then `ArrowDown` to the variant before `Enter`. Radios/checkboxes: use a semantic `check` action, not a coordinate click.
- **Icon input is static and targetable; screenshot/promo drop-zones are NOT.** The store-icon `<input type=file>` exists in the DOM (`upload` / `setInputFiles` works). The screenshot & promo zones spawn their file input **only on click, via a native file chooser** — a plain `setInputFiles`-on-a-static-input tool can't reach them. To automate screenshots you need a real **file-chooser handler** (`page.waitForEvent('filechooser')` around the click, then `setFiles`) over a **TCP** CDP connection — or a human drags the files. A multi-file upload aimed at the single-file icon input silently stalls at "0%".
- **Screenshot upload resists CLI automation; the human drag is the practical path.** Clicking the screenshots drop-zone *does* materialize the file inputs (a `get count "input[type=file]"` jumps 0→N), but a one-shot `upload`/`setInputFiles` hits a **detach race** — Angular re-renders the input between resolve and set-files (`Object id doesn't reference a Node`). Only the *static* icon input uploads cleanly this way. A robust Playwright **Locator** `setInputFiles` (auto-waits through the detach) needs a **TCP** CDP endpoint — but **Chrome 136+ ignores `--remote-debugging-port` on the default/logged-in profile** (only a custom `--user-data-dir` gets a port), and agent-browser connects over a pipe with no file-chooser command. Net: have the user drag the screenshots in, then the agent clicks **Submit for review**. (The Submit button un-disables and the "Why can't I submit?" link disappears once all required fields — incl. ≥1 screenshot — are set.)
- **Wrong-Google-account trap.** The listing is owned by one Google account. In a multi-account/SSO Chrome (e.g. a work + personal setup) the console silently resolves to the wrong account and **redirects to `/devconsole/register`** — that redirect means "not the owner account," not "not registered." `?authuser=` switching is unreliable; the fix is selecting the right account/profile in the browser. Managed (work) accounts can't own a personal listing.
- Uploading the package trips "publish to a public registry" guards in agentic setups even though it only creates a private draft — get explicit user go-ahead; let the user do the Google login and $5 payment.

### Resubmission after a permissions rejection

- **Check whether the fix already landed before rebuilding.** A merged-but-unshipped fix branch plus a stale submitted zip is a common state — the rejection may cite permissions already removed in git. Audit before cutting anything: `grep -rn "chrome.<api>" src/` per permission (`chrome.scripting`, `chrome.system`, …), and re-audit every remaining permission as the rectification notice demands.
- **`grep src/` lies when a non-entry file matches — audit the BUILT entry, not all source.** Chrome's static check reads the *packaged* service worker / content scripts, i.e. only what the webpack/vite entry actually pulls in. An **orphaned file** (a stale `background.ts` next to the real `background/index.ts`, a dead util) can reference `chrome.alarms`/`chrome.webNavigation` and satisfy `grep -rn chrome.alarms src/` while the built bundle never touches them → "requesting but not using" rejection despite a source match. So: read the entry map (`config.entry` / vite input), grep only the files it reaches (or grep `build/static/js/*.js` after a build), and delete the orphan so the phantom reference can't mislead the next audit. (Chrome's internal code for this is "Purple Potassium" = excessive/unused permissions.)
- **`clipboardWrite` is usually removable.** `navigator.clipboard.writeText()` behind a user-gesture (a click handler) needs **no** permission in an extension page; the permission is only for writes *outside* a gesture or `execCommand('copy')` in a worker. If your only clipboard use is a "Copy" button → drop the permission. (`chrome.notifications`, by contrast, *does* need `"notifications"` — an undeclared `chrome.notifications.create` silently no-ops, so guard it or declare it; missing-permission is a broken feature, not a rejection.)
- **Static `content_scripts` do NOT need matching `host_permissions`.** Injection is authorized by `content_scripts.matches`. `host_permissions` is only for cross-origin `fetch` from the worker/content script, `chrome.scripting`, cookies, or `tabs.query({url})`. Duplicating every content-script host into `host_permissions` is permission-creep reviewers flag — keep in `host_permissions` only the origins you actually `fetch` (e.g. image CDNs for vision) or query by URL.
- **You get ONE appeal per violation, and resubmit-spam risks the whole Google account.** Repeatedly re-uploading without fixing the root cause can suspend related Google services (the automated system reads it as evasion). So root-cause first, fix once, resubmit once. Only appeal (item detail page → Appeal) if you're certain the rejection is wrong and you can cite the exact code path that uses the permission.
- **Bump the version.** CWS rejects an upload whose version is ≤ any previously uploaded version, *including rejected drafts* (1.0 rejected → upload 1.0.1). Rebuild so the packaged `manifest.json` carries both the new version and the narrowed permissions; verify with `unzip -p pkg.zip manifest.json`.
- **The Privacy tab regenerates from the new manifest.** Per-permission justification boxes for removed permissions vanish on their own — no manual cleanup. But any box left at `0/1,000` keeps **Submit for review** disabled (a previously-empty `sidePanel` box is the usual culprit). Fill the textarea (native value setter + `input`/`change` events), click **Save draft**, and only then does Submit un-disable.
- **Don't re-upload while a draft is pending review** unless you mean to — the new package replaces the version under review and restarts the queue.

### Driving the CWS dashboard without CDP (macOS: AppleScript + in-page JS)

When agent-browser `--auto-connect` reports "No running Chrome instance found" (Chrome wasn't launched with `--remote-debugging-port`, and Chrome 136+ ignores that flag on the default/logged-in profile):

- **Clicking "Allow" on Chrome's "Allow remote debugging?" dialog does NOT fix `--auto-connect`** — it still finds no instance. Dismiss the dialogs (each connection attempt spawns one) and take a different path.
- **AppleScript is the fast path.** GUI-AX automation (click-by-element-id tools) runs ~1 min/action on large Chrome windows; `osascript` is instant: enumerate `windows` and `URL of active tab of window id N`, open pages with `make new tab at end of tabs with properties {URL:"…"}`, and run page JS via `execute active tab of window id N javascript "…"` (requires View → Developer → **Allow JavaScript from Apple Events**). With in-page JS you drive the Angular console directly: click buttons matched by `textContent`, read `btn.disabled`, fill textareas via the native setter + events.
- **Profile selection without guessing:** the devconsole URL opens in the *last-active* profile — often the wrong one (see the account trap above). Instead find the window whose tabs prove the right Google session (e.g. an open Gmail tab for the owner account) and `make new tab` *in that window*; a clean load (no `/register` redirect) confirms the owner account.
- **Zip upload without the native file chooser.** The chooser is painful to automate, and `fetch('http://localhost:…')` from the page trips Chrome's local-network permission prompt ("wants to access other apps and services on this device"). Skip the network entirely: `base64` the zip, inject it into `window.__b64` in ~200 KB chunks via repeated `execute javascript`, then in-page: `atob → Uint8Array → new File([bytes], name, {type:'application/zip'}) → DataTransfer → input.files = dt.files → dispatchEvent(new Event('change',{bubbles:true}))` targeting `input[type=file][accept*=".zip"]`. Angular may **clear `input.files` as it consumes them**, so `files[0]` can be undefined immediately after — that's success, not failure. Verify on the **Package** tab that the draft shows the new version + permissions.
- **Confirm submission on the Status tab** ("This draft is pending review") — the header badge lags behind the actual state.

---

## 7b. The other stores (Edge, Opera, Whale — and why not Safari)

Chrome and Firefox are not the whole map. Three more stores take the package you
already built; the fourth is a different product wearing the same name.

| Store | Cost | Takes the Chromium zip as-is? | API? | Verdict |
|---|---|---|---|---|
| **Microsoft Edge Add-ons** | Free | Yes | **Yes** — REST | Do it. Best ratio in the table. |
| **Opera Add-ons** | Free | Yes | No, dashboard only | Cheap. Slow review. |
| **Naver Whale** | Free | Yes | No | Only if you want Korean reach. |
| **Safari** | **$99/yr** | **No** — needs an Xcode app wrapper | App Store Connect | Usually no. See below. |

Brave, Vivaldi, Arc and most Chromium forks install **from the Chrome Web Store**.
There is nothing to submit to them. Chrome + Edge + Firefox covers nearly everyone.

### Microsoft Edge Add-ons

Register in **Partner Center** (`partner.microsoft.com/dashboard/microsoftedge`).
No fee, unlike Chrome's $5.

Edge is Chromium, so the same zip uploads unchanged — including `offscreen`, which
Edge supports. Do not rebuild.

It has a **REST submission API**, which is the reason to prioritise it: it slots
into the same CI job as §13 rather than becoming a manual step forever. Auth is an
Azure AD client-credentials pair (client id + secret + an access-token URL) scoped
to a product id, not the Google OAuth dance. Broadly: POST the package to a draft,
poll the operation until it reports complete, then POST publish. Treat the exact
endpoint shape as **unverified here** and read the current Partner Center API docs
before wiring it — Microsoft has revised this API at least once.

Known friction, in rough order of how much time it costs:
- Partner Center account creation is slower than Chrome's. It can require identity
  verification before the first submission, so start it early rather than on the day
  you want to ship.
- The listing form is separate from the package upload; both must be complete before
  Submit enables, with the same silent-greyed-button behaviour as Chrome (§12).

### Opera Add-ons

`addons.opera.com/developer/`. Free, Chromium, same zip.

Dashboard-only — no publish API, so it stays a manual step. Review is human and
historically slower than Chrome's. Opera also asks for its own listing assets rather
than reusing the Chrome ones.

### Naver Whale

`store.whale.naver.com`. Chromium, same zip, needs a Naver account.

Expect the listing to want Korean copy. Worth it only if Korean users are a real
target, otherwise it is a listing you will not maintain.

### Safari — read this before agreeing to it

Safari "web extensions" share the WebExtension API surface but **not the delivery
model**. `xcrun safari-web-extension-converter <ext-dir>` generates an **Xcode
project** that wraps the extension inside a macOS or iOS app. You then ship that app
through the App Store, which needs the **Apple Developer Program at $99/yr**.

So it is not a repackage. It is a second product with its own build toolchain,
signing identity, review queue and release cadence.

Two API gaps decide it for most extensions, and they are the ones MV3 pushed people
onto in the first place:

- **No `offscreen` API.** This is Chrome-specific. Any extension using an offscreen
  document to hold something an MV3 service worker cannot — `RTCPeerConnection` is
  the common case, because a worker can be killed mid-session — has no equivalent on
  Safari and needs its architecture changed, not ported.
- **No `sidePanel` API.** Chrome's `side_panel` and Firefox's `sidebar_action` both
  have no Safari counterpart. A side-panel-shaped product has no home there.

Check both against your own manifest before quoting a timeline. If either appears,
Safari is a rewrite wearing the costume of a port. Say so plainly and early — it is a
much cheaper conversation before the Apple Developer purchase than after.

---

## 8. Pass review the first time (pre-submission audit)

Run this audit **before** uploading. It separates the warnings that are fine from the ones that get you rejected.

### Your own code (grep it — these are the real blockers)

```
git grep -nE "eval\(|new Function|document\.write|innerHTML|<script|importScripts|https?://(?!localhost)" -- src ':(exclude)src/vendor/*'
```
- **No `eval` / `new Function` / `document.write`** — hard rejection on both stores.
- **`innerHTML` only with static or sanitized strings.** Dynamic `innerHTML` is an AMO warning and a Chrome risk. Prefer `textContent` / `createElement` / DOM APIs; for SVG/vector rendering build nodes, don't string-concat user/model data into markup.
- **No remote code.** No CDN `<script>`, no `import` from a URL, no `fetch()`-then-`eval`. Every `fetch` must target an **extension-local** asset or a **declared** `host_permissions` origin. Chrome's "Are you using remote code?" is **No** only if this holds (bundled wasm is *not* remote code).

### Third-party libraries (the usual Chrome snag)

- **Ship readable source, not obfuscated.** Chrome bans obfuscated code and reviewers flag heavily-**minified** vendored files (a 700 KB, 6-line `*.min.js`). Minified *public* libraries are usually accepted, but to be bulletproof **vendor the library's non-minified build** (or a CSP/ESM build that ships readable) and keep its `LICENSE`. A readable `three.module.js` passes without question; a one-line minified blob invites "please provide unminified source."
- List every vendored lib + license in the reviewer notes (AMO) / justifications (Chrome).

### AMO (`web-ext lint`) — which warnings are benign

- `"/background/service_worker" is unsupported and ignored on Firefox` — **expected** (the dual-background cross-browser trick). Ignore.
- `Unsafe assignment to innerHTML` **inside a vendored lib** (e.g. MapLibre) — a warning, not an error; AMO passes with it. The same warning **in your own code** — fix it.
- Target **0 errors**; warnings don't block submission but each one a *human* reviewer sees is a chance to look closer, so minimize them.

### Chrome Web Store policy gates (beyond the linter)

- **Single purpose** — one narrow, honestly-stated purpose. Feature sprawl that needs broad permissions gets rejected.
- **Minimal permissions**, each justified; prefer `activeTab` + `optional_permissions` over broad host access. Unused permission in the manifest = rejection.
- **CSP** — `'wasm-unsafe-eval'` is allowed; `'unsafe-eval'` is not. No remote `script-src`.
- **Data honesty** — the data-use disclosures must match what the code actually does; a privacy-policy URL is required even at zero data.
- **Assets present** — 128×128 icon + ≥1 screenshot at exactly 1280×800.

### Common rejection causes (both stores)

Obfuscated/minified-only code · remote code execution · permissions with no user-visible feature · privacy policy missing/contradicting behavior · single-purpose violation · screenshots that don't show the real product.

---

## 9. Content-script insertion into rich editors (the disabled-button trap)

Social composers are React-controlled contenteditables (X = Draft.js, LinkedIn = Quill, many apps = Lexical). Setting `el.textContent = text` mutates the DOM *behind* the editor's model: the text **shows** but the editor's internal state stays empty, so the Post/Send button stays **disabled** and nothing can be submitted. The insertion looks like it worked and silently isn't postable.

Fix — activate, then insert with a **trusted** edit command:

1. **Click the composer to activate/focus it.** These editors only start tracking input once the field is active.
2. Insert via `document.execCommand('insertText', false, text)`. This fires a *trusted* `beforeinput`/`input` event the editor processes to update its model → the button enables. To clear existing content first, use `execCommand('selectAll')` + `execCommand('delete')` — **never** `textContent = ''`.

A synthetic `el.dispatchEvent(new InputEvent('beforeinput', …))` alone does **not** insert text (untrusted events don't perform the edit). `execCommand` is deprecated but remains the reliable cross-editor path for programmatic insertion into a contenteditable the page controls.

---

## 10. Per-device session state: `storage.local`, not `storage.sync`

Auth tokens and per-device session ids belong in `chrome.storage.local`. `chrome.storage.sync` replicates to the user's account cloud and keeps **restoring** whatever is there — so a corrupted or mismatched value becomes permanently stuck across reloads and reinstalls, and a self-heal can never persist.

- A common corruption source: a **race** where several content-script instances (one per injected post/widget) each auto-sign-up on first page load, and two different sign-ups interleave their writes (token from A, workspace/id from B) → a mismatched pair that 401/403s forever.
- De-dupe concurrent sign-ups with a single shared **in-flight promise**: check-and-set the promise with **no `await` between the check and the assignment** so it's atomic on the single-threaded event loop; all callers await the same request.
- Add a **self-heal**: on a 401/403 from an authed call, clear the cached session and re-auth once. This only sticks if the session lives in `storage.local` (see above).

---

## 11. QA a loaded (unpacked) extension via browser automation

- **Chrome ignores `--load-extension`** on a normal profile (anti-abuse); the flag was removed around Chrome 137 and confirmed still inert on 152. `--enable-unsafe-extension-debugging` does **not** bring it back — verified: only Chrome's built-in extension targets appear over CDP, none for yours. Do not spend time on flags. Load once via `chrome://extensions` → Developer mode → Load unpacked; it persists across restarts. To pick up a rebuild without GUI, **quit + relaunch** the browser — the unpacked registration persists.
- A DOM-automation tool that connects **through an installed helper extension** can drive content injected into normal web pages, but usually **cannot open `chrome://` or `chrome-extension://`** pages (the extension's own popup/side panel). Drive those with screen automation, or design the test to avoid them.
- Screen-automation focus is unreliable when several terminal/agent windows compete for foreground (clicks/keystrokes land in the wrong window). **Activate the target app deterministically via the OS scripting layer first** (macOS: `osascript -e 'tell application "Google Chrome" to activate'`, then open the URL), and confirm the intended window is frontmost before acting.
- **Fastest way to seed a known-good session into a content script for a test:** create a valid session against the API, then set the token/id into the **page origin's `localStorage`** (content scripts read page `localStorage`, and a well-written client uses it as a fallback) — sidesteps the extension's `chrome://`-only storage UI entirely.
- **Coordinate scaling:** a DOM tool's screenshot is often a fixed fraction of CSS-viewport pixels. Measure the ratio once (a known element's `getBoundingClientRect` vs its position in the screenshot) and scale click coordinates by it, or clicks miss.
- **Scripted HTTP clients get bot-blocked** by some CDNs (e.g. a Cloudflare `1010`). Send a real browser `User-Agent` and the site's expected `Origin` header.
## 12. Resubmitting a rejected Chrome item (hard-won, 2026-07)

- **"Privacy policy does not contain necessary information" (User Data Privacy violation)** is the most common rejection. The privacy-policy URL must (a) actually RESOLVE — a dead / placeholder / unconfigured-`www.` host returns nothing and fails review — and (b) comprehensively disclose: what data is collected, how it's used, storage/retention, and **every** third party it's shared with (AI providers, payment processor, hosting). Omission of any section = rejection. Fix: serve a real `/privacy` page on a reachable domain (a Cloudflare Worker route returning HTML works fine) and point the listing at it.
- **"Homepage URL is not reachable"** silently disables the Submit button (greyed, no obvious reason). Store listing → Additional fields → Homepage URL must resolve (200). Use the live apex, not an unconfigured `www.` or a staging host. The **"Why can't I submit?"** link enumerates exactly these blockers — always click it first.
- **Resubmit the SAME item** (same item id) — fix the cited issue → Save draft → Submit for review. Don't create a new item. Bump the package version only if you're uploading new code (not needed for a listing/privacy-only fix).

### Driving the dashboard with agent-browser

Edit pages are path-routed: `…/devconsole/<pub>/<itemid>/edit/{status,package,listing,privacy,distribution}` — navigate directly instead of clicking tabs. `Status` shows the rejection reason verbatim; snapshot→`@ref`→`fill`/`click`/`upload`. **Google multi-account gotcha:** the Web Store may default to the wrong (e.g. work) account and show "Register / Pay $5" — the real dev account must be picked via the avatar switcher; `?authuser=<email>` in the URL does NOT switch it, and a fresh nav can bounce to "Verify it's you" (password/2FA — the human must clear it, an agent cannot).

### Monitor-until-approved loop

Review takes days–weeks. Set a **durable cloud schedule** (claude.ai routine + Gmail connector, via the `schedule` skill) to check the inbox daily for the verdict and report approved / rejected+reason. The cloud agent **cannot resubmit** — that needs the developer's logged-in local browser — so it alerts; the fix + resubmit happens in a local session (fast once this flow is known).

---

## Checklist

- [ ] `src/manifest.json` MV3; dual `background` (service_worker + scripts); `gecko.id` + `strict_min_version` + `data_collection_permissions`.
- [ ] Code uses `globalThis.browser ?? globalThis.chrome`, promise-style, optional perms behind a user gesture.
- [ ] CSP declares `'wasm-unsafe-eval'` if wasm; workers same-origin (`worker-src 'self'`, no `blob:`); remote origins in `connect-src`/`img-src` + `host_permissions`; libs vendored, no CDN.
- [ ] Local-AI path (if any) probes capability and degrades to a working floor; model output validated, never `eval`'d.
- [ ] `web-ext lint` clean (dual-background warning expected); built package verified as loaded add-on, not just `web-ext run`.
- [ ] AMO: 2FA set up (human), agreement accepted, listed/unlisted confirmed, reviewer notes cover network + licenses.
- [ ] Chrome: $5 registration done, same zip uploaded as a draft, screenshots added, single-purpose + per-permission justifications + data-use disclosure filled, then Submit for review.
- [ ] Pre-submission audit (§8): own code free of `eval`/dynamic-`innerHTML`/remote code; vendored libs shipped **unminified** + licensed; `web-ext lint` 0 errors; minimal justified permissions; privacy policy URL live.
- [ ] Content-script insertion (§9): activate the field, insert via `execCommand('insertText')` (not `textContent`), and confirm the target's Post/Send button actually **enables**.
- [ ] Session state (§10): tokens in `storage.local` not `sync`; concurrent auto-sign-ups de-duped via one in-flight promise; self-heal (clear + re-auth) on 401/403.
- [ ] Other stores (§7b): Edge submitted (free, same zip, has an API — wire it into §13); Opera/Whale decided; Safari explicitly ruled in or out against the `offscreen`/`sidePanel` gaps.
- [ ] QA (§11): loaded via `chrome://extensions` (not `--load-extension`); target app activated deterministically before automation; screenshot→click coordinates scaled; test HTTP calls send a browser UA + `Origin`.

---

## 13. CI publish via Chrome Web Store API (GitHub Actions)

Once an extension is stable enough to ship from CI, use the Chrome Web Store Publish API so every `release` push publishes both the Worker backend and the extension from the same commit.

### Workflow pattern (see [`publish-extension.yml`](https://github.com/itsryanarmani/private-repo-4ed5/tree/main/.github/workflows/publish-extension.yml) for a working example)

```yaml
name: Publish extension
on:
  push:
    branches: [release]
    paths:
      - 'apps/extension/**'
      - '.github/workflows/publish-extension.yml'

jobs:
  publish:
    runs-on: ${{ github.event.repository.private && 'boat' || 'ubuntu-latest' }}
    steps:
      - uses: actions/checkout@v7
      - uses: oven-sh/setup-bun@v2
      - run: bun install && bun run build
      - name: Package
        run: cd build && zip -qrX ../extension.zip .
      - name: Upload and publish
        env:
          CHROME_WEBSTORE_EXTENSION_ID: ${{ vars.CHROME_WEBSTORE_EXTENSION_ID }}
          CHROME_WEBSTORE_CLIENT_ID: ${{ secrets.CHROME_WEBSTORE_CLIENT_ID }}
          CHROME_WEBSTORE_CLIENT_SECRET: ${{ secrets.CHROME_WEBSTORE_CLIENT_SECRET }}
          CHROME_WEBSTORE_REFRESH_TOKEN: ${{ secrets.CHROME_WEBSTORE_REFRESH_TOKEN }}
          EXTENSION_ZIP: extension.zip
        run: node scripts/publish-extension.mjs
```

### Credentials

| Name | Kind | Purpose |
|------|------|--------|
| `CHROME_WEBSTORE_EXTENSION_ID` | repository **variable** | public item id from the store URL |
| `CHROME_WEBSTORE_CLIENT_ID` | **secret** | OAuth Desktop app client id |
| `CHROME_WEBSTORE_CLIENT_SECRET` | **secret** | OAuth Desktop app client secret |
| `CHROME_WEBSTORE_REFRESH_TOKEN` | **secret** | long-lived token from the consent flow |

Minting the OAuth triple is a one-time browser session — the consent screen cannot be automated:

1. Enable **Chrome Web Store API** in Google Cloud Console.
2. Create an **OAuth client ID** of type **Desktop app**. (A Web client will be refused — Google shut down `urn:ietf:wg:oauth:2.0:oob`.)
3. Start a local listener (`nc -l 8080`) and open the auth URL in the browser signed in as the listing owner. Include `&access_type=offline&prompt=consent` — without `prompt=consent` the refresh token is returned only on the very first authorization.
4. The redirect dumps `?code=...` into `nc`. Exchange it:
   ```sh
   curl -s https://oauth2.googleapis.com/token \
     -d client_id=<ID> -d client_secret=<SECRET> \
     -d code=<CODE> -d grant_type=authorization_code \
     -d redirect_uri=http://localhost:8080
   ```
5. Store the four values with `gh secret set` / `gh variable set`.

The refresh token does not expire on a timer but is revoked if the owner changes their password or removes the app's access. When the job starts failing at "OAuth token exchange", repeat from step 3.

### Idempotency (skip when version matches)

The publish script reads the store's current version before uploading. If it matches the built version the job is a no-op — a `release` push that only changes the backend stays green instead of failing on "version already exists". Bump `manifest.json` to publish again.

### Version landmine

If your build toolchain injects a four-part version like `${version}.${Date.now()}` into the built manifest (e.g. a watch-mode reloader), Chrome will reject it — the fourth part exceeds the 65535-per-part limit. Guard: check the built manifest version shape (1–4 dot-separated integers, each between 0 and 65535, no leading zeros on non-zero components) before uploading, so bad builds fail locally with a readable error instead of remotely with a status code.

---

## 14. Firefox-only facts for agent extensions

Each fact below cost a build or a review round on Firefox 153 to 157. Set
`strict_min_version` to the current ESR and feature-detect anything newer.

### Platform limits

- **No `SharedArrayBuffer` in extension pages.** Firefox ignores the
  `cross_origin_embedder_policy` and `cross_origin_opener_policy` manifest keys
  (bug 1673477). WASM threads do not work there. Use single-thread WASM, or run
  the threaded code on an `https:` page that sends COOP and COEP, and talk to it
  with `postMessage`.
- **The MV3 background is an event page with a DOM.** There is no service
  worker and no `offscreen`. The page unloads after about 30 seconds idle. In
  testing on Firefox 157, an open `runtime.Port` from a sidebar did not keep it
  loaded. Save state in
  `storage.session` or `storage.local`, and wake the page with `alarms`. A model
  loaded in the event page goes away with it.
- **No `debugger` permission and no CDP.** Synthetic events from
  `scripting.executeScript` have `isTrusted: false`. For trusted input, drive
  Firefox from an outside helper over WebDriver BiDi.
- **`scripting.executeScript({ func })` sends the function as source text.**
  The function must be self-contained. Pass data in `args`.

### The `sandbox` manifest key

Firefox 157 honoured this key in testing. Check MDN compatibility data for the
first version that supports it. `sandbox.pages` plus `content_security_policy.sandbox` gives a page an opaque
origin, no extension APIs, `eval`, and its own CSP. `connect-src 'none'` makes it
a no-network room.

**Caution:** the manifest sandbox CSP applies only when the host iframe has no
`sandbox` attribute. With the attribute, Firefox 157 dropped the manifest CSP,
and `fetch`, `XMLHttpRequest` and `WebSocket` reached a local probe server. Put
the same policy in a `<meta http-equiv="Content-Security-Policy">` tag in the
sandbox page, and keep it in every mode. Firefox 153 ignores the key: have the
page check at start that its origin is opaque and that `browser` is absent, and
refuse to run if not. `web-ext lint` then warns `UNSUPPORTED_BY_MIN_VERSION` for
the key. Allow that one warning by code in your lint script, not all warnings.

### Containers and network isolation

- Containers (`contextualIdentities`) and `cookieStoreId` work in `tabs`,
  `cookies`, `browsingData.remove`, and `proxy.onRequest`. This is how you give
  an agent one site's login in its own cookie jar.
- **Warning:** WebRTC escapes both `webRequest` and `proxy.onRequest`. A page in
  the container can open an `RTCPeerConnection` to a STUN or TURN server and
  send UDP that neither guard sees. Turn off
  `privacy.network.peerConnectionEnabled` while the isolated task runs, and give
  the old value back after. The setting is browser-wide.
- A speculative `<link rel="preconnect">` skips `webRequest`. Route blocked
  hosts in `proxy.onRequest` to a `socks` proxy that does not exist, with
  `proxyDNS: true`. `proxyDNS` applies only to `socks` and `socks4` proxies.
  Turn off `privacy.network.networkPredictionEnabled` to stop DNS prefetch.
- If `privacy.*.set()` answers `false` (a policy or another extension controls
  it), refuse the task. Do not run with the channel open.
- If the user removes host access in `about:addons`, Firefox stops sending
  requests to your blocking listeners and they all pass. Check
  `permissions.contains({ origins: ["<all_urls>"] })` before the task, and stop
  every task on `permissions.onRemoved`.
- A blocking `webRequest` listener that throws lets the request pass. Catch
  inside the listener and cancel.

### Tabs

`tabs.group` and `tabGroups` put each agent task in a named group. Both worked
in testing on Firefox 157. Feature-detect them before use.
`tabs.hide` (permission `tabHide`) keeps agent tabs out of the strip.

### Test with WebDriver BiDi

- Start Firefox with `-remote-allow-system-access`, or BiDi refuses
  `moz-extension:` pages.
- BiDi sends no navigation events for `moz-extension:` pages, so a Puppeteer
  `goto()` never resolves. Poll `location.href` and `document.readyState`.
- BiDi cannot screenshot a `moz-extension:` page ("unsupported operation").
  For PR proof, serve the built page over `http://localhost` with a stub
  `browser` object that returns the real state your E2E test read, then
  screenshot that. Or screenshot a normal web page the extension changes. Say
  in the PR which one you used.

### AMO rules that block a submission

- `data_collection_permissions` is required for new add-ons. Page text sent to
  the user's own model key counts: declare `websiteContent` under `optional`.
- AMO allows the `userScripts` API only for user-script managers. Never run
  model-written JavaScript. Bundle the action functions and pass data as `args`.
- Extensions must not relax a page's CSP, also through `filterResponseData`.

### Sign with AMO in CI

`web-ext sign --channel=unlisted --api-key="$AMO_JWT_ISSUER" --api-secret="$AMO_JWT_SECRET"`
signs the `.xpi` for a GitHub release. Fail the step with a clear message when
either secret is empty.

- **AMO throttles new add-on submissions per account.** The error says
  `Expected available in N seconds`. N was 873 on the first try and 4169 on a
  later one, so signing 17 new add-ons took hours.
- **Make the release re-runnable.** If the job publishes to npm before it
  signs, a re-run stops at `npm publish`, because npm refuses a version twice.
  Skip the publish when `npm view "$NAME@$VER" version` succeeds. Then
  `gh run rerun <id> --failed` reaches the signing step.
- To retry many repos, read N from `gh run view <id> --log-failed`, wait N plus
  a margin, then re-run. Stop on a failure that has no `available in` line.
