---
name: make-integration
description: "Build, push, and submit a Make (Integromat) custom app and get it into the public Make apps directory. Use when creating a Make app from a bundled app.json, pushing it via the SDK Apps API, debugging a 403/1010 push failure, wiring the Universal module + pagination + typed dates that public review requires, or building the per-module review scenarios. Covers the SDK-API push path (scripts/make/publish-app.py), the component model (base/connection/modules/webhooks/rpcs), the exact API facts (versioned vs unversioned endpoints, typeIds, section PUTs), the Cloudflare 1010 User-Agent trap, and the review gates (Universal module, 512x512 logo, a scenario PER module, the Tally follow-up form, permanent publish). Sibling of connector-directory-submission (the cross-platform router) and zapier-integration. Verified 2026-08."
---

# Building a Make (Integromat) app

A Make app is NOT an npm package — the `app.json` in `integrations/make/` is the
*export* of an app that lives in Make's own builder. You push it component-by-component,
then request a QA review to list it publicly. Command-level tool + full API notes:
`itsryanarmani/scripts` `scripts/make/README.md` + `publish-app.py`.

## Push the app — prefer the SDK API (an agent can push the whole thing)

**There is no one-shot "import the whole `app.json`" in Make.** (The Make DevTool Chrome
extension has NO "Import app" tool — old READMEs saying "DevTool → Import app" are stale.)
A custom app is stored as separate components — Base + each Connection/Module/Webhook/RPC.
The bundled `app.json`'s top-level keys (`base`, `connection`, `modules[]`, `webhooks[]`,
`rpcs[]`) map 1:1 to those components.

**The SDK Apps API creates every component programmatically** — the fastest, least-error
path, and what an agent should reach for. `scripts/make/publish-app.py` does it:

```bash
# Create the app *shell* + one connection in the UI first, then:
MAKE_TOKEN=… python3 publish-app.py --app <slug> --app-json app.json --zone us1.make.com
```

API facts baked in (all easy to get wrong):
- Auth header is `Authorization: Token <token>` (not Bearer). Token scopes:
  `sdk-apps:read` + `sdk-apps:write`.
- **Modules & RPCs are versioned** (`/api/v2/sdk/apps/{app}/{ver}/modules`); **webhooks
  and connections are NOT** (`/apps/{app}/webhooks`, sections at
  `/apps/webhooks/{name}/{section}`; `/apps/{app}/connections`).
- Module `typeId`: 4 action, 9 search, 10 instant-trigger, 12 universal. Set sections with
  `PUT …/{name}/{api|expect|interface|samples}` (raw JSON; `api`←communication,
  `expect`←mappable params).
- **HTTP 403 body `error code: 1010` is NOT a rate limit — it's Cloudflare blocking the
  default `Python-urllib` User-Agent.** curl passes, urllib doesn't; the real
  `x-ratelimit` is 10000 and untouched. Fix = send a normal `User-Agent` (`curl/8.4.0`)
  and the whole app pushes in one clean run. Don't chase a phantom quota.
- attach/detach reference the connection as `{{account.apiKey}}` (not `{{connection.*}}`)
  and don't inherit base → write them with an absolute URL + explicit header. Make
  **auto-names** created webhooks → capture the real name from the create response to link
  instant-trigger modules.

**Manual fallbacks** (when you can't script): the **Make Apps Editor for VS Code**
(`Integromat.apps-sdk`) edits each component as JSON (add an SDK environment with the
zone API URL + your key); or the in-browser builder → **Create custom app** makes only the
shell (name `^[a-z][0-9a-z-]+[0-9a-z]$`, 3–30 chars), then the app's `+` menu creates each
Connection/Webhook/Module/RPC. The Connection **doesn't inherit base** → its Communication
URL must be absolute.

## What `app.json` must contain to PASS public review

The private app works with far less; the *public review* has hard prereqs (source:
`developers.make.com/custom-apps-documentation/app-review/prerequisites` — the checklist
drifts, re-check it):
- **Exactly one Universal module** — a generic HTTP-passthrough (relative `url` + `method`
  select). The single-file format has no `kind:"universal"`, so author it as
  `"kind":"action"` and set the type to **Universal** in the editor after import. Keep the
  URL **relative** (Make rejects universal modules where the user can set the host — pin
  the host in `base.baseUrl`).
- **`limit` + pagination on every list/search module** (single-item getters don't need
  it; a client-side `limit` cap is fine where the API doesn't paginate — note it).
- **Typed dates** — every date field uses `"type":"date"`, not text.
- **Sanitized secrets** — `base.log.sanitize` (and `connection.log.sanitize`) must list
  `request.headers.authorization`.
- **Real interfaces + labels + descriptions** on every module, matching the API response.

## Submit for the public directory (developers.make.com → Request app review)

On the app's **Review** page: link the service's **API docs**, paste a **scenario URL per
module** each showing a successful run, add the error scenario, logo, categories → **Request
review**. Make's QA reads the code; if it passes they publish to all users. Track by the
email subject `App review: <YourAppName>`.

Gates / gotchas:
- **Novelty:** the app must connect to a service Make doesn't already integrate, or it's
  refused as a duplicate.
- **The scenarios are the real, NON-automatable work.** One field PER MODULE — a separate
  Make scenario URL showing a successful run — plus one for a deliberate API error. A
  32-module app = 33 hand-built, hand-run scenarios. The SDK API builds the app but can't
  make scenarios meaningfully pass, and write-modules act for real. You CAN create the
  scenario *shells* via the Scenarios API (`POST /api/v2/scenarios?confirmed=true`,
  blueprint ref `app#{app}:{module}`, real numeric teamId or you get `IM002`,
  `scenarios:write` scope — `scripts/make/create-review-scenarios.py`), but the connection
  is UI-only and runs are manual. Toggle **every module "visible"** first; run scenarios
  right before requesting (logs expire).
- **Publish is PERMANENT (no unpublish)** — only Publish when ready to do all the above.
- **A Tally follow-up form GATES the review** — after Request, Make emails "Externally
  developed apps on Make"; the review doesn't proceed until it's submitted. Asks: vendor
  relationship (first-party = "direct vendor / ISV"), company, homepage, optional square
  PNG logo, partnership contact (email/name/phone — phone is a masked tel input, type a
  leading `1`), support contact, category+subcategory, two attestations (trademark,
  external T&C). Watch the inbox.
- Review form needs a **512×512 PNG logo (≤500 kB)**, support email, categories, trademark
  + external-terms confirmations.
- Until approved the app is **private/unlisted** (usable by you) — normal, not a failure.
