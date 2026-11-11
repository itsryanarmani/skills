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

Use the payment-provider transaction ID for `event_id` when possible. Use a
separate event ID for a refund. Do not reuse the purchase ID for a later event.

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
Use [ad-landing-tracking](../ad-landing-tracking/SKILL.md) for click-id capture, first-touch cookies, and landing page setup.
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
