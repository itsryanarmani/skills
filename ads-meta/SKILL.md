---
name: ads-meta
description: "Use when wiring Meta Pixel plus Conversions API purchase tracking, building a Custom Audience or Lookalike, debugging zero or phantom Purchase events, or when the Meta Ads MCP will not authenticate in Claude Code or a token returns no ad accounts."
---

# ads-meta

Meta conversion tracking has two halves — a client-side **Pixel** (fires in the browser on page load and on purchase) and a server-side **Conversions API (CAPI)** call (fires from your backend after the charge actually happens, e.g. a payment webhook). Ship both together with a shared dedup key, or purchases get double-counted.

## When to use

- **Triggers:** 'Meta pixel', 'Conversions API', 'CAPI', 'Purchase events missing', 'phantom Purchase on signup', 'Lookalike audience', 'Meta Ads MCP URL Blocked', 'System User token', 'empty adaccounts'.
- Client Pixel (fbq base plus Purchase) and server CAPI (Graph /{pixel-id}/events) with a shared event_id dedup key; the unset CAPI token that silently no-ops; firing on hashed-email match, not fbclid, so organic purchases report; advanced matching.
- App-capability 400s (Advanced Access for ads_management, promotable Page); Lookalikes from a hashed-email Custom Audience (USER_PROVIDED_ONLY, EMAIL_SHA256, 100 matched-user floor); a Purchase on free signup is usually the Automatic Events setting; verification via Graph stats and last_fired_time.
- Meta Ads MCP in the CLI: the hosted mcp.facebook.com/ads OAuth fails with 'URL Blocked / redirect_uris not registered' (works only on claude.ai web or Desktop); the token fix with pipeboard-co/meta-ads-mcp and META_ACCESS_TOKEN; the Business Settings path to a non-expiring System User token (app role, scopes with SMS 2FA, ad-account assignment).

## Setup, in order

1. **Meta Events Manager → create a dataset / pixel.** The pixel id is a numeric string, safe to expose client-side (it's not a secret).
2. **Generate a CAPI access token** — Events Manager → your dataset → Settings → **Conversions API → Generate access token**. This *is* a secret; server-side only.
3. Attach a **promotable Facebook Page** to the ad account (needed later for creating ads).

## Client-side Pixel

Standard `fbq` base + a `Purchase` event on the confirmation page:

```html
<script>
!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,
document,'script','https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '<PIXEL_ID>');
fbq('track', 'PageView');
</script>
```

Fire the purchase with an **`event_id`** — this is the dedup key that pairs with the server event:

```js
fbq('track', 'Purchase', { value: 25, currency: 'USD' }, { eventID: '<shared-dedup-id>' });
```

Note the client SDK's param is **`eventID`** (in the fourth options arg); the server CAPI payload below uses **`event_id`**. Same value, different casing — don't typo one into the other.

## Server-side Conversions API (Graph)

```
POST https://graph.facebook.com/v19.0/{pixel-id}/events?access_token=<CAPI_ACCESS_TOKEN>
Content-Type: application/json
```

```json
{
  "data": [{
    "event_name": "Purchase",
    "event_time": 1700000000,
    "event_id": "<shared-dedup-id>",
    "action_source": "website",
    "user_data": {
      "em": ["<sha256 of lowercased-trimmed email>"],
      "external_id": ["<sha256 of your stable user id>"],
      "client_ip_address": "<request ip>",
      "client_user_agent": "<request user-agent>",
      "fbc": "<_fbc cookie value, only if present>",
      "fbp": "<_fbp cookie value, if present>"
    },
    "custom_data": {
      "value": 25,
      "currency": "USD",
      "content_ids": ["plan_pro"],
      "content_type": "product"
    }
  }]
}
```

- `event_time` is epoch **seconds** (not milliseconds).
- **If the CAPI access token is unset, the call silently no-ops** — 0 server events, no throw. This is the #1 pitfall. An `if (!token) return` guard makes it worse: the code runs, the guard takes the empty branch, nothing is sent.
- Always add **`client_ip_address` + `client_user_agent`** server-side — they materially improve match rate and are only available on the server.

## Do NOT gate CAPI on a click id

Fire the server event on **hashed-email match (`em`)**, not on the presence of `fbclid`/`fbc`. If you only fire when a Facebook click id is present, every **organic/direct/email/SEO purchase never reports** — which is most of them for many apps.

- Include `fbc`/`fbclid` **only when present** (it sharpens attribution for ad-driven purchases) but never make it a *requirement* for firing.
- `fbclid` from the landing-page URL survives via Meta's own **`_fbc` cookie** (the Pixel writes it), so read `_fbc` server-side rather than trying to thread the raw `fbclid` through your whole checkout.

## Match quality (advanced matching)

- **Advanced matching** — hashed email `em` and `external_id` (your stable user id, hashed) — is what lets Meta attribute a server event to a real person. Send whatever you have; more identifiers = higher match quality score in Events Manager.
- Hash `em`/`external_id` with **SHA-256 after lowercasing and trimming**; never send raw PII.
- `content_ids` + `content_type` on `custom_data` improve catalog/dynamic-ads attribution.

## App-capability pitfalls (creating ads via the API)

- Uploading ad images (`POST /act_{ad-account-id}/adimages`) and creating ads can **400 with "(#3) Application does not have the capability"** until your app has **Advanced Access for `ads_management`** — or you run the calls as a user who has a role on the ad account (Standard/dev-mode access only covers app-role users). Request Advanced Access in the App Review flow, or test as an app-role user first.
- A **promotable Facebook Page must be attached to the ad account** — ad creation fails without one.
- **Escape hatch — use the official hosted ads MCP.** A self-built app on the **Limited** Marketing API tier keeps hitting `(#3)` on campaign/ad create, and getting **Advanced Access requires App Review + Business Verification** (days, frequently stalls). Meta's **official hosted ads MCP endpoint** uses standard Business-account OAuth and **bypasses the app-review/capability gate entirely** — you create and manage campaigns without owning a reviewed app. If you're blocked on `(#3)`, stop fighting App Review and drive the official MCP instead. **BUT in Claude Code CLI the official MCP's OAuth is broken** — see the next section; use a token-based MCP there.

## Meta Ads MCP in Claude Code — token auth, not OAuth

The **official hosted MCP** (`https://mcp.facebook.com/ads`) authenticates fine from **claude.ai web** and **Claude Desktop** but **fails from the Claude Code CLI**. The CLI uses Dynamic Client Registration (RFC 7591) with a **localhost loopback redirect** (`http://localhost:<port>/callback`); Meta's OAuth client only whitelists the fixed claude.ai / Desktop redirect URIs. The handshake dies before login with **"URL Blocked … redirect URI is not whitelisted"** (a.k.a. `redirect_uris are not registered for this client`). It is server-side (Meta's app config) — no CLI flag fixes it. Confirmed open in many claude-code issues.

**Fix for the CLI: run a token-based MCP that talks straight to the Graph API** — no OAuth redirect, so no whitelist to fail. `pipeboard-co/meta-ads-mcp` reads `META_ACCESS_TOKEN` with highest precedence and, when set, **bypasses Pipeboard's proxy** and hits Meta directly (verify: `auth.py` checks the env var first). `byadsco/meta-ads-mcp` (Node, `npx @byadsco/meta-ads-mcp --transport stdio`) is an equivalent. Global config in `~/.claude.json` → applies to every worktree; use an absolute interpreter path (Claude Code gives spawned MCP servers a minimal PATH):

```json
"meta-ads": {
  "type": "stdio",
  "command": "/opt/homebrew/bin/pipx",
  "args": ["run", "meta-ads-mcp"],
  "env": { "META_ACCESS_TOKEN": "${META_ACCESS_TOKEN}" }
}
```

`${META_ACCESS_TOKEN}` expands from Claude Code's **own process env** at MCP launch — so `export` it in `~/.zshrc` and **fully restart Claude Code** (a running session won't see a zshrc edit). Never hardcode a work-account token into `~/.claude.json` if you can export it instead.

### Mint a non-expiring System User token (Business Settings clickpath)

A System User token never expires and is the right credential for a headless MCP. Meta gates it behind a **three-layer chain — each is a prerequisite for the next**, and the token-generation wizard blocks at layer 1 with **"No permissions available — Assign an app role to the system user"** if you skip it:

1. **App role on the system user.** Business Settings → **Accounts → Apps** → your app → **Assign people** → check the **system user** → toggle **Manage app (Full control)** → **Assign**. (The picker lists system users alongside people. Assigning *yourself* to the app does nothing for the system user — this is the common trap.) This is what unlocks the token wizard at all.
2. **Token scopes.** Back on **Users → System users** → select the system user → **Generate token** → pick the app → expiration **Never** → **Assign permissions**: check `ads_read` + `ads_management` (+ `business_management` for account-level). → **Generate token**. Meta then demands an **SMS 2FA code** to the account phone before it mints the token — a human must enter it; this step can't be automated. Copy the token immediately (shown once).
3. **Ad-account assignment.** Accounts → **Ad accounts** → the account → **Assign people** → check the system user → **Manage ad accounts (Full access)** → **Assign**. Without this, `me/adaccounts` returns `{"data":[]}` — the token generates fine but every ads call sees no account.

`account_id` visibility is layer 3, *not* layer 2 — a valid token that returns an empty `adaccounts` list means the ad account isn't assigned yet, not that the token is bad.

### Verify the token end-to-end (Graph, before trusting the MCP)

```
GET /v21.0/me?fields=id,name                          → {"id":"…","name":"<system user name>"}   (token valid)
GET /v21.0/me/adaccounts?fields=name,account_id,account_status,currency
                                                       → data[] populated with account_status:1  (layer 3 done)
```

If `me` works but `adaccounts` is `[]`, go back and do layer 3. Store the token in `~/.zshrc` (for the MCP) and any app's gitignored `.env.local` (as a labelled stash) — never commit it.

## Campaign + audience setup (lookalike, small budget)

- **Lookalike:** create a custom audience seeded off your **highest-value users**, then a **1%-of-country lookalike** from it. Set **`targeting_automation.advantage_audience = 0`** to keep it a *hard* lookalike — otherwise Meta quietly broadens delivery beyond the lookalike.
- **Budget hard-stop:** a campaign-level **`spend_cap`** (with CBO) is a **native hard stop** — no external budget-reaper cron needed. Two gotchas: (1) you **can't lower `spend_cap` below already-pending charges** (the error quotes the current floor, often a few dollars above your target); (2) **editing `spend_cap` / budget / targeting auto-pauses the campaign/ad set** — you must re-activate it after any such edit.
- **Creatives are immutable.** To swap an ad's image/copy you **create a new creative + new ad**, activate it, and pause the old — there is no in-place edit. Do the swap while spend is ~0 to avoid losing a read.
- **`ads_create_ad` takes no status arg** — it's born PAUSED; activate as a separate call.
- **`ads_update_entity` cannot delete** — it force-pauses (returns `status_forced_to_paused`). A true delete needs the Ads Manager UI.

## Bake tracking + dynamic macros into the creative at create time

A creative's **link, `url_tags`, media, copy, and CTA are immutable** — creative-update only changes name/status/labels. To change any of them you create a **new creative**, which **resets the ad's learning phase**. So get tracking right up front: put UTMs and **dynamic URL macros** in `url_tags` when creating the creative, e.g.

```
utm_source=meta&utm_medium=paid_social&utm_campaign={{campaign.name}}&utm_content={{ad.name}}&utm_term={{adset.name}}&utm_placement={{placement}}&src={{site_source_name}}
```

Meta expands the `{{...}}` macros on every click — auto-tagging each ad and capturing **placement** (feed / reels / stories), attribution you're otherwise blind to. (This is the tracking counterpart to "creatives are immutable" above: swap the whole creative to fix a bad tag, so don't ship a bad tag.)

## Per-surface creative optimization

This applies to all social ad platforms. Make one creative for each placement and build it for that surface. Never use one asset everywhere.

- **Reels / Stories:** Use full-bleed 9:16 creative. Design for sound-on viewing, a native or UGC feel, and a hook in the first ~1 second.
- **Feed:** Use 4:5 or 1:1 creative. Make it thumb-stopping but legible with muted playback.
- **Right column / Audience Network:** Create their own variants with smaller ratios suited to those placements.
- **Across all placements:** Make the creative feel native, not ad-like. It should read as content, not a banner. Prefer video first.

## More API/launch gotchas (each one bites)

- **`LANDING_PAGE_VIEWS` optimization under `OUTCOME_TRAFFIC` rejects `promoted_object{pixel_id}`** ("Promoted Object Invalid") — omit `promoted_object` for that combo.
- **CTA `GET_STARTED` is rejected for some Pages** → `SIGN_UP` works.
- **The image-upload endpoint may be un-rolled-out for an account** → skip it and pass **`image_url`** to creative-create; Meta server-fetches the image.
- **Payment method must be on the AD ACCOUNT**, not just the business portfolio — otherwise delivery fails with **"No Payment Method" (subcode 1359188)** even though a card is "on the account" at the portfolio level.
- **`location_types` is deprecated (2026) — the geo "unpublished edits" red herring.** Specifying `home` / `recent` / `traveling_in` in `geo_locations.location_types` trips a soft **draft-validation** error (Meta code `#1870194`, surfaced as "Unpublished edits" when you open the ad-set editor). It is **NOT delivery-blocking** — the errors endpoint returns empty and the ad set keeps serving; the editor just spawns a draft that re-flags it. **Fix:** set `geo_locations` with `countries` only and **OMIT `location_types`** (Meta applies its current single default). Partial values like `["home","recent"]` don't clear it — `recent` is also a removed option.

## Custom Audience → Lookalike (seeding from your own users)

To target people similar to your users, upload a **Custom Audience** of hashed emails, then build a **Lookalike** from it:

- **Custom Audience:** `customer_file_source = USER_PROVIDED_ONLY`, schema `EMAIL_SHA256`, members = emails normalized (trim + lowercase) then SHA-256 hex.
- **Lookalike:** `subtype = LOOKALIKE`, `origin_audience_id = <the custom audience>`, and a `lookalike_spec` with country + ratio (`0.01` = top 1%, the closest match).
- **A lookalike needs ≥100 *matched* users in the seed to serve.** After a ~50-70% match rate, a raw seed near 100 fails the size floor — size the seed above it. Catch the under-size rejection per-segment; don't let one small seed abort a multi-segment run. Seed-sizing strategy and the PII-export authorization boundary are in `ad-experiments`.

## A "Purchase on free signup" is usually a console setting, not your code

Before hunting for a stray `fbq('track','Purchase')`: a real CAPI Purchase only fires on a confirmed paid charge. A Purchase that misfires on a *free* signup almost always comes from Meta's **Automatic Events / Advanced Matching** setting (Events Manager → dataset → Settings) synthesizing a Purchase from price text on the page — not from your code. **Check that console toggle first;** turning off automatic-event detection stops the phantom Purchase with no code change.

## Detecting delivery-blocking errors (don't trust the entity read)

The standard ad-entity read returns `effective_status` (e.g. `ACTIVE`) plus the targeting object but does **NOT** surface review/validation warnings — an ad set can read `ACTIVE` + valid targeting while the UI shows a publish/review error. To catch real blockers, query the dedicated **errors endpoint** (`ads_get_errors` / the entity's `issues_info` / `recommendations`), not just the entity fields. Poll it in any delivery monitor. An **empty** errors response = no real blocker — e.g. the `location_types` draft-validation nag above reads as an editor warning but never appears here.

## Verification (server-side truth, not "the pixel is on the page")

- **`GET /{pixel-id}?fields=last_fired_time`** — confirms the pixel/dataset fired *anything* recently.
- **`GET /{pixel-id}/stats?aggregation=event`** — counts by event type, and **includes CAPI** server events. This is authoritative. If you see only `PageView` and **no `Purchase`**, the purchase event isn't firing — regardless of what the browser looks like.
- Prefer these over the Events Manager UI's "Test Events" tab when you need a durable count rather than a live poke.

## Browser caveat

Some automation/headless browsers (and privacy tooling) **block `fbevents.js`**, so the Pixel looks dead in your test tooling while working fine in real browsers. Don't conclude the Pixel is broken from a headless run — **always cross-check server-side** via `/stats`.

## Small-budget campaign setup (cross-platform)

- On a small test budget with **no conversion history, don't pick a conversion-optimized objective yet** — Meta's delivery has a **learning phase** that needs a steady flow of conversions to optimize, which a small budget won't produce, so it never learns. Start with a traffic/click objective to fill the funnel, and move to conversion optimization once real conversions accumulate. (Same trap as Google Smart Bidding's learning phase.)
- Run **one narrow audience × geo × creative per experiment**, prove the **cheapest conversion (free signup) first**, and judge results on server-side truth (`/stats` + payment provider), not the dashboard. See the `ad-experiments` skill for the full methodology.

## Cross-cutting lessons (the ones that actually bite)

- **Timing:** a Purchase count of **0 over a window that predates the tracking deploy** is expected, not a bug. Check the deploy date before debugging — there are no events from before the Pixel existed.
- **Build-scoped env:** if the pixel id / CAPI token are baked into a generated module at **build time** (common on serverless/edge), setting them in your dashboard does *nothing* until the next deploy. **Redeploy after adding** — match wherever your other working analytics secrets are imported from rather than assuming a runtime `process.env` read works.
- **Ground truth:** cross-check Meta's server-side event counts (`/stats`) against your **payment provider's actual succeeded-charge count**. Real succeeded charges > 0 with Meta Purchase events = 0 means tracking is broken, full stop — the payment provider is the source of truth, the Pixel/CAPI is the thing under test.
- **Silent failure is the norm:** these integrations fail by **sending nothing** (an early return on a missing access token, a click-id gate that never matches organic traffic), not by throwing. Verify with server-side truth — `/stats`, `last_fired_time`, the payment provider — never "I saw fbq load in the browser."

## Common pitfalls

- CAPI access token unset → server events silently no-op (0 events, no error).
- Gating CAPI on `fbclid`/`fbc` → organic and direct purchases never report; fire on hashed `em` instead, add `fbc` only when present.
- Mismatched dedup key casing — client `eventID` vs server `event_id`, same value.
- `event_time` in milliseconds instead of seconds.
- Sending raw (unhashed) email or user id in `user_data` — always SHA-256, lowercased + trimmed.
- Concluding the Pixel is dead from a headless/automation browser that blocks `fbevents.js` — cross-check `/stats` server-side.
- `(#3) capability` 400s on `/adimages` or ad creation because the app lacks Advanced Access for `ads_management`, or no promotable Page is attached.
- Trusting `effective_status: ACTIVE` from the entity read — it hides review/validation warnings; poll the errors endpoint (`ads_get_errors` / `issues_info` / `recommendations`) for real blockers.
- `location_types: [home/recent/...]` → `#1870194` "Unpublished edits" draft nag (deprecated in 2026, **not** delivery-blocking); set `geo_locations.countries` only and omit `location_types`.
- Editing a creative's link / `url_tags` / media / copy / CTA in place — those fields are immutable (update only touches name/status/labels); you must make a new creative, which resets learning. Bake UTMs + `{{...}}` macros into `url_tags` at create.

---

## Security — the Pixel is the official first-party vendor script

`https://connect.facebook.net/en_US/fbevents.js` is Meta's own first-party Pixel bootstrap — the standard, required loader every Meta advertiser embeds, not arbitrary third-party code. Load it only from the official `connect.facebook.net` origin over HTTPS (never a mirror or CDN copy). The CAPI access token stays server-side in an env var — no secret is placed in the client snippet.

## Hub conventions and official references

Use the shared conversion-hub contract: emit one canonical event, use a stable
`event_id`, send the event after the payment provider confirms the charge, and
make an absent `META_PIXEL_ID` or `META_CAPI_TOKEN` a logged no-op. Keep the
platform adapter product-agnostic. See `ad-conversion-hub` and `ad-experiments`
for canonical events, consent, hashing, seed sizing, and ground-truth checks.

Official references checked 2026-08-11:

- [Meta Conversions API](https://developers.facebook.com/docs/marketing-api/conversions-api/)
- [Meta Pixel](https://developers.facebook.com/docs/meta-pixel/)
- [Custom Audiences](https://developers.facebook.com/docs/marketing-api/audiences/)

## Ranked Meta ad formats — cross-reference
For the 12 ranked formats, ROAS ranking table, WaveSpeed model picks, and creative rules, see [`ad-creative-templates/impulse-formats.md`](../ad-creative-templates/impulse-formats.md). That shared reference contains the honesty rules (no fabricated testimonials, no deceptive pricing, no fake interface, no invented stats). Tracking setup cross-references the honesty rules: no fake buttons, fake notification badges, or fake platform marks. Meta's current rules on labelling AI-generated images checked before launch.
