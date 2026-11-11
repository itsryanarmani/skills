---
name: ad-conversion-hub
description: "Design and operate a shared ad-conversion hub for multiple ad platforms — canonical event taxonomy, consent gating, SHA-256 identity hashing, stable client/server deduplication, first-party click-id capture, platform adapter secrets, absent-secret no-ops, retry and failure isolation, server-side proof, and reconciliation against payment-provider truth. Use when a product sends one purchase, signup, lead, or subscription event to Google, Meta, Reddit, Microsoft, TikTok, LinkedIn, Pinterest, DSP, regional, CTV, or emerging ad platforms."
---

# ad-conversion-hub

Use one canonical event in the product. Adapt it at the platform edge.

The hub owns business truth. A platform skill owns vendor syntax. This split
keeps checkout code free from vendor-specific fields and makes a new adapter a
small change.

## Flow

```text
payment provider webhook
        |
        v
canonical event -> consent gate -> identity normalizer -> adapter fan-out
        |                  |                 |
        |                  |                 +--> client/server dedup key
        |                  +--------------------> hashed identifiers only
        +----------------------------------------> payment-provider event ID
                                                     |
                                                     v
                                         platform event + durable dispatch log
```

The payment provider is the source of truth for a successful charge. Ad
platform dashboards are attribution views. They are not the ledger.

## Canonical event taxonomy

Keep the event names stable across products and vendors:

| Canonical event | When it fires | Required fields |
|---|---|---|
| `page_view` | A page or SPA route loads | `event_id`, `occurred_at`, `page_url` |
| `view_content` | A meaningful product or plan view occurs | `event_id`, `content_id` |
| `lead` | A user submits a qualified lead form | `event_id`, `lead_id` |
| `signup` | An account is created | `event_id`, `user_id` |
| `begin_checkout` | A checkout session starts | `event_id`, `checkout_id`, `currency` |
| `purchase` | The payment provider confirms a charge | `event_id`, `order_id`, `value`, `currency` |
| `subscription_start` | A paid subscription becomes active | `event_id`, `subscription_id`, `value`, `currency` |
| `refund` | A payment provider records a refund | `event_id`, `order_id`, `value`, `currency` |

Use the payment-provider transaction ID for `event_id` when possible. With Stripe Checkout, use the payment session id for both the browser and the server copy, so the two paths share one id. Use a
separate event ID for a refund. Do not reuse the purchase ID for a later event.

## Event ladder for a small ad test (relay names)

The taxonomy above is the vendor-neutral model. A conversion relay and a
multi-site directory template use these names. Map them once, and keep the map in one file.

| Relay name | Meta event | Fires when | How the two copies share one id |
|---|---|---|---|
| `page_view` | PageView | A page loads | Browser pixel only. The server has no matching event |
| `view_content` | ViewContent | A product or guide page is viewed | The page script makes the id, queues the pixel event and posts the id to a server beacon (the page may be cached) |
| `lead` | Lead | A visitor gives an email for a free guide | The server makes the id when the claim is stored and sends its copy. A short cookie with only the id lets the next page send the browser copy |
| `checkout_created` | InitiateCheckout | A paid checkout starts | The browser makes the id on submit, the form posts it, and the server reuses it |
| `purchase` | Purchase | The payment provider confirms | The payment session id is the event id for both copies |

`checkout_created` here is `begin_checkout` in the table above. Pick one name
per project and say so in the code.

The `purchase` browser copy fires on the page the buyer returns to. That address
holds the payment session id, which is an id and not an access token. Send it only
when the order is paid, read from the server, and never from a page whose address
holds a download or access token. The server copy needs no page at all.

Tweaks that matter on a small budget:

- **Send every event except PageView twice, with one id.** Send it from the browser pixel and
  from the server. Meta keeps one when both carry the same event name and the
  same `event_id`, and both reach the same pixel within 48 hours. A different
  name, a different id, a different pixel or a copy that arrives after 48 hours
  counts twice, so a buyer who returns later can produce a second Purchase. The
  browser copy can be lost to an ad blocker, and the page can leave before it
  sends.
- **Make the id where the event starts.** The browser fires `InitiateCheckout`
  on submit, before the server creates the payment session, so the browser
  cannot know the session id. Let the browser make the id and post it, and let
  the server reuse it for its copy. Accept it only if it matches a strict
  pattern, and fall back to an id built from the session when it is missing.
- **A test makes too few purchases.** Meta learns from about 50 optimization
  events an ad set a week. A small test buys few purchases: at an assumed
  $1.50 a click and a 1% click-to-purchase rate, $300 buys about 200 clicks and
  about 2 purchases. Replace both numbers with your own. Optimize for `lead` only if the offer has a real free step (an
  opt-in that leads to the paid offer) and you can measure how many Leads buy.
  Cheap Leads that never buy are a false win. With no such step, optimize for
  `checkout_created`, and move to `purchase` when the volume is there.
- **Read price and title from the server.** A beacon route must never trust a
  value from the client. Read both from the product catalog.
- **No database read per page view.** A read on every view adds cost and latency
  and defeats edge caching of the page. Take the data from a static catalog.
- **Keep the consent rules for every event.** No consent, no event. A privacy
  opt-out (GPC or DNT) means no event. A token page (a purchase link, an
  unsubscribe link) sends nothing. A health or other sensitive site sends no ad
  events at all.
- **Keep emails and access tokens out of ad events.** Do not put them in an event,
  in a URL the pixel sends, or in the cookie that carries an event id between two
  pages. That cookie holds only the id, lives a few minutes, and the next page
  clears it. A page whose own address holds a token (a purchase link, an
  unsubscribe link) sends no events at all.
- **One pixel for many sites mixes the signal.** Add the site and product to
  each event, and filter audiences by URL. A pixel for each site is cleaner.
- **A failed send never blocks.** Log fixed words only. Do not log relay text,
  an email or a click id.
- **Check the pixel, not the page.** `GET /{pixel_id}/stats?aggregation=event&start_time=<unix>&end_time=<unix>`
  with a read token shows event counts. A pixel that shows 6 PageViews in a
  week has no signal. Set `META_TEST_EVENT_CODE` and watch the Test events tab
  before you spend.
- **Business verification.** An unverified portfolio has fewer system users and
  lower limits. Reading the verification status needs the
  `business_management` permission. A marketing token lacks it. Check in the
  Business settings Security centre.

## Event envelope

The hub stores a normalized envelope before dispatch:

```ts
type CanonicalAdEvent = {
  event_id: string;
  event_name:
    | 'page_view'
    | 'view_content'
    | 'lead'
    | 'signup'
    | 'begin_checkout'
    | 'purchase'
    | 'subscription_start'
    | 'refund';
  occurred_at: string; // ISO 8601 UTC
  source: 'browser' | 'server' | 'webhook' | 'offline';
  order_id?: string;
  checkout_id?: string;
  subscription_id?: string;
  user_id?: string;
  value?: number;
  currency?: string;
  page_url?: string;
  click_ids?: Record<string, string>;
  identity?: {
    email?: string;
    phone?: string;
    ip_address?: string;
    user_agent?: string;
  };
  consent: {
    ad_user_data: boolean;
    ad_personalization: boolean;
    measurement: boolean;
  };
  items?: Array<{
    item_id: string;
    quantity?: number;
    price?: number;
  }>;
};
```

Reject an event that has no stable `event_id`, no `event_name`, or no consent
decision. Do not reject a purchase only because it has no ad click ID.

## Consent gate

Apply consent before hashing or dispatch:

1. Read the consent record that belongs to the user and event time.
2. Require `measurement: true` before sending any ad event.
3. Require `ad_user_data: true` before sending hashed email, phone, or external IDs.
4. Require `ad_personalization: true` before adding a user to a retargeting or lookalike audience.
5. Keep a reason when the hub skips an adapter.

Consent does not mean that every platform may receive every field. Each adapter
must reduce the envelope to the fields allowed by its current official docs.

## Identity normalization and hashing

Normalize email as `trim → lowercase → UTF-8 → SHA-256 hex`. Normalize phone with
the platform's current country-code rules before hashing. Do not hash an already
hashed value a second time.

```ts
function sha256Email(email: string): string {
  const normalized = email.trim().toLowerCase();
  return sha256Hex(normalized);
}
```

Keep raw identifiers inside the server boundary. The adapter receives a
short-lived normalized value or a hash. It must not log either one.

## Click IDs

Capture the platform click ID on first landing when it appears in the URL.
Persist it in first-party storage with a defined retention period. Keep the
first-touch and most-recent value separately when the platform supports both.

Never use a click ID as the condition for sending a server purchase. Organic,
direct, email, and SEO purchases still provide useful measurement and can match
through hashed identity or first-party identifiers.

Each adapter owns its click-ID name. Examples include `gclid`, `fbclid` or
`fbc`, `msclkid`, `ttclid`, `qclid`, and platform-specific values. Confirm every
name against the platform's official docs before adding it to the hub.

## Adapter contract

Every platform adapter has the same shape:

```ts
type AdAdapter = {
  platform: string;
  requiredSecrets: string[];
  dispatch(event: CanonicalAdEvent): Promise<{
    status: 'sent' | 'skipped' | 'failed';
    request_id?: string;
    reason?: string;
  }>;
};
```

Use the shared secret names from the platform skill. The usual convention is:

```text
<PLATFORM>_PIXEL_ID   public client identifier
<PLATFORM>_TAG_ID     public tag or data-source identifier
<PLATFORM>_CAPI_TOKEN  server conversion credential
<PLATFORM>_ACCESS_TOKEN server API credential
```

A missing required secret returns `skipped`. It does not throw. A 4xx or 5xx
response returns `failed`, records a redacted error, and does not fail the
payment webhook.

## Client and server deduplication

If the browser and server send one event, both must carry the same event ID.
Some platforms use `eventID`, `event_id`, `conversionId`, or another casing.
The adapter translates the field. The hub does not change the value.

Keep a dispatch record with:

- canonical `event_id`;
- platform name;
- adapter event name;
- first attempt time;
- response status and request ID;
- redacted error code;
- retry count.

Do not retry a request when the vendor may have accepted it and the response was
lost, unless the vendor documents idempotency. If the vendor supports a test
event mode, use it before production dispatch.

## Retry policy

- Retry network timeouts and 5xx responses with bounded exponential backoff.
- Do not retry 400, 401, 403, or policy errors without changing the request or credential.
- Honor `Retry-After` when the vendor sends it.
- Cap retries so a webhook cannot run past its provider timeout.
- Move exhausted events to a durable dead-letter queue.
- Replay only after checking the vendor's deduplication rule.

## Verification

Verification has three layers:

1. **Request proof:** the adapter receives a documented success response.
2. **Platform proof:** the official test-event view, event history, read endpoint,
or reporting API shows the event.
3. **Business proof:** the platform result is reconciled with payment-provider
succeeded charges, refunds, and subscription state.

Do not call a pixel network request proof. Do not call a 200 response platform
proof. Do not call an attributed conversion count business proof.

## Testing checklist

Test each adapter with:

- a purchase with consent and a click ID;
- a purchase with consent and no click ID;
- a purchase without ad-user-data consent;
- a duplicate delivery with the same event ID;
- an absent token;
- a 401 response;
- a timeout followed by a replay;
- a refund after a purchase;
- a currency and value edge case;
- a successful payment with a failed ad dispatch.

The last case must show a successful payment and a retryable ad failure. The ad
integration must never roll back the payment.

## Security

Keep server tokens in the deployment secret store. Do not put them in client
bundles, URLs, logs, analytics payloads, screenshots, or pull requests. Load
vendor scripts only from the official HTTPS origin documented by each platform.

Limit access to raw identity data. Delete temporary normalized identifiers after
dispatch. Record consent and retention decisions with the event metadata.

## Pairing

Use the platform-specific `*-ads` skill for vendor endpoints and console steps.
Use `ad-experiments` for hypothesis design, seed sizing, and budget control.
Use `ads-google`, `ads-meta`, and `ads-reddit` as detailed examples of adapter
pitfalls and server-side verification.

## Shipped as a package

Productize this hub as an npm package — the SDK +
CLI + MCP form of this skill, so a consumer runs `npm i <your-package>` instead of re-implementing
the flow. Learnings from the extraction, reusable here:

- **Namespaced client surface** (Stripe/Segment shape): `createClient()` reads secrets from
  env → `ads.conversions.track(event)` returns a per-destination result array `{ platform,
  ok, error }[]`; `ads.destinations.list()` / `.verify()`.
- **Adapters throw, the client isolates.** Each dispatcher throws on non-2xx; the client
  wraps with retry + captures per-destination so one platform's failure never blocks the
  rest. (Do NOT copy the fire-and-forget swallow model from an in-request backend — see
  `agentic-cli-npm-package` §6.)
- **`verify` ≠ `check`.** `check` = secrets present; `verify` = hit the platform API to prove
  the token works. Ship a per-platform optional `verify(secrets)` alongside each `dispatch`.
- **The registry is the seam.** `PLATFORMS[key] = { dispatch, verify?, support, requiredSecrets }`,
  append-only so parallel platform PRs never conflict. `support: real-capi | offline-upload |
  pixel-only` — no platform is a silent no-op.
- **Per-platform runbook** (`docs/platforms/<key>.md`): create-account → where each token comes
  from → verify → event mapping → troubleshooting. Pairs with `agent-harness-docs`.
