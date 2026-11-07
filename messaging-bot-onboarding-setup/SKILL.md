---
name: messaging-bot-onboarding-setup
description: "Use when wiring or debugging inbound messaging bots (iMessage/Sendblue, Telegram, WhatsApp Cloud API, Slack, Discord) where a cold DM starts onboarding, especially when real inbounds get 401s or the bot never replies while synthetic tests pass."
---

# Messaging-bot onboarding setup

A cold handle DMs a number → the app greets, gets consent, provisions a handle-anchored
account, and hands off. Every platform delivers those inbounds to an HTTP webhook that must
**authenticate the delivery** before acting. The auth is always the same shape — and the same
shape fails the same way in production.

## When to use

- **Triggers:** 'imessage bot 401', 'sendblue signing secret', 'telegram onboarding not firing', 'set up whatsapp cloud api', 'whatsapp phone number id', 'why does the bot never reply', 'verify the telegram webhook', 'messaging bot setup'.
- The shared-secret webhook pattern and its top failure: the provider dashboard's secret field is empty, so every real inbound 401s. Per platform: the header, the dashboard field or API call, the env var name and the verify handshake.
- The Telegram bare /start gap (a connect-help intercept swallows it before onboarding); creating or reusing a Meta app for WhatsApp (use case, test vs production number, business verification, the five WHATSAPP_ env vars).
- End-to-end checks with a synthetic signed webhook POST plus a DB row check instead of trusting a 200.

## The shared-secret pattern (learn this first)

Each provider signs its webhook deliveries with a secret **you** configure in their dashboard/API.
It arrives in a request header. The app compares it (constant-time) to a secret in its own deployed
env. Match → process; mismatch/absent → **401**.

**The #1 production failure: the provider's secret field is left EMPTY.** Then the provider sends
**no** header (or an empty one), the app compares it against a non-empty deployed secret, and it
**401s every real inbound** — while your synthetic tests pass, because your test sends the deployed
secret in the header. Symptom: "the bot never replies," webhook is registered, no errors visible,
but zero onboarding rows in the DB.

**Fix:** generate ONE secret, set it on **both** sides — the app env (all deploy targets) **and**
the provider dashboard field. If either side is empty or they differ, every inbound 401s.

| Platform | Secret header (provider → app) | Where you set it (provider side) | App env var |
|---|---|---|---|
| iMessage (Sendblue) | `sb-signing-secret` | Sendblue dashboard → Webhooks → **Global Secret** (or per-webhook Secret). Optional field → often left blank → 401. | `SENDBLUE_WEBHOOK_SECRET` |
| Telegram | `x-telegram-bot-api-secret-token` | `setWebhook` call, `secret_token` param | `TELEGRAM_WEBHOOK_SECRET` |
| WhatsApp (Cloud API) | GET verify: `hub.verify_token`; POST auth: `x-hub-signature-256` (HMAC-SHA256 of body) | Meta app → WhatsApp → Configuration → Webhook: **Verify token** field (matches env); the HMAC key is the **App Secret** (App settings → Basic) | `WHATSAPP_VERIFY_TOKEN` (handshake) + `WHATSAPP_APP_SECRET` (HMAC) |

Generate + deploy a shared secret (Cloudflare Workers example — see the companion
`set-messaging-webhook-key.sh` in itsryanarmani/scripts):

```bash
SECRET="sbwh_$(openssl rand -hex 24)"
# app side: env file + every worker that serves the webhook
# ...edit .env.local, then:
printf '%s' "$SECRET" | npx wrangler secret put SENDBLUE_WEBHOOK_SECRET --name <staging-worker>
printf '%s' "$SECRET" | npx wrangler secret put SENDBLUE_WEBHOOK_SECRET --name <prod-worker>
# provider side: paste $SECRET into the dashboard field and SAVE
```

## Telegram: the bare-`/start` cold-onboarding gap

Telegram's **Start button sends exactly `/start`** (no payload). A common webhook shape intercepts
any `/start` and routes it to the *connect* deep-link handler, which for a bare `/start` replies a
static "go to Settings to connect" help and returns — so a brand-new user **never reaches
conversational onboarding**. Onboarding then only fires if the user's *first* message is non-`/start`
text, which real users don't do.

**Route `/start` to the connect handler only when it carries a deep-link payload (`/start <code>`)
OR the chat is not private.** A **bare `/start` in a private chat** must fall through to the normal
dispatch, which routes an unknown handle into onboarding and a linked chat to the agent. (iMessage
has no `/start` equivalent — its first inbound text goes straight to onboarding, so it's unaffected.
Audit Slack/Discord/WhatsApp for the same "command/help intercept returns before onboarding" shape.)

## WhatsApp: create or reuse the Meta app

- **Reuse over create.** WhatsApp is a **use case** you add to an existing app under the same
  business portfolio, not necessarily a new app. developers.facebook.com/apps → open an app in the
  business → Dashboard → **Add use cases** → **"Connect with customers through WhatsApp"** → Save.
  Adding the use case is clean (no ToS wall); the ToS gate comes at Step 1.
- **Step 1 "Try it out" — test number.** Provisions a throwaway number + temp token (max 5
  recipients, token expires). Clicking **Continue** here **accepts** "Facebook Terms for WhatsApp
  Business" + "Meta Hosting Terms for Cloud API" — a terms acceptance, so get explicit user
  authorization first. The free test number can silently fail to provision if the business portfolio
  has no verified payment method — don't loop on the Claim button; it's a Meta-side gate.
- **Step 2 "Production setup"** — register a **real** phone number + generate a **permanent System
  User access token** (the temp token is useless for prod).
- **Step 3 "Business verification"** — required for production messaging; can take days. User-gated.
- **The 5 env vars the app needs** (owner-supplied): `WHATSAPP_PHONE_NUMBER_ID`,
  `WHATSAPP_BUSINESS_ACCOUNT_ID` (both non-secret IDs, from WhatsApp → API Setup),
  `WHATSAPP_ACCESS_TOKEN` (permanent System User token), `WHATSAPP_APP_SECRET` (App settings →
  Basic), `WHATSAPP_VERIFY_TOKEN` (you invent it; must match the webhook Verify token field).
- Graph API version pins in code (e.g. `v25.0`); callback URL is the app's
  `/api/v1/integrations/whatsapp/webhook`. The Phone Number ID is **not** the phone number — it's a
  separate numeric ID on the API Setup page.

## Flow 2: attach an email in chat

After a channel-first (email-less) account onboards, the owner attaches an email **in chat** to
also sign in on the web and land in the **same** account. `initiateEmailAttach` / `confirmEmailAttach`:
call without a code to mail a 6-digit code, then call again with the code to finish.

The idiom differs by bot architecture:

- **LLM-agent bots** (telegram, imessage, slack): expose an `attach_email` agent tool.
- **Command/dispatch bots** (discord, whatsapp): a deterministic command — discord
  `/attach_email <email> [code]`; whatsapp `attach email <addr> [code]`. WhatsApp's MCP tools are
  API-key-scoped and can't carry a `userId`, so attach must be a non-LLM command.

**Security gate (identical across every bot, non-negotiable):** the `userId` is always the
**server-resolved channel identity** — taken from the signature-verified sender, never from message
text or a model tool-arg. Drop any model-smuggled `userId`. Expose attach **only** in an
authenticated 1:1 DM so a group/guild participant can never claim the owner's account:

| Bot | 1:1-DM gate |
|---|---|
| telegram / imessage | `canClaimAccount` |
| discord | refuse when `guildId` is set |
| slack | `channel_type === 'im'` only |
| whatsapp | the sender's own `wa_id`-keyed account |

**Don't drive the attach step through a chat message in an automated e2e.** It routes through the
LLM agent, which may skip `attach_email` on a given turn (observed: a freshly-onboarded account's
next message didn't trigger the tool). Prove the attach **mechanics** deterministically through the
tRPC/API surface (or a direct function call) with a real session; leave "the LLM invokes the tool"
to real-app testing.

## e2e-verify a bot for real (don't trust a 200)

A registered webhook returning `{ok:true}` proves nothing about onboarding. Verify the whole chain:

1. **Synthetic signed POST** to the *deployed* webhook, mimicking a real cold inbound, with the
   secret header set to the deployed secret. Use a clearly-fake external id you can clean up.
2. **Check the DB**, not the HTTP status: query the onboarding-state table for a row keyed on
   `(source, external_id)`. A row (e.g. `step=awaiting_choice`) proves dispatch → onboarding ran.
   No row after a 200 = the chain no-ops somewhere (an intercept, a wrong env, or prod behind main).
3. **Negative test:** same POST with a wrong secret must **401**.
4. **Right environment:** onboarding merged to `main` deploys to **staging** automatically; **prod**
   often deploys from a `release` branch and can lag. A real inbound hits prod — if prod predates
   the onboarding merge, prod drops cold users silently even though staging works. Check the row on
   the env the webhook actually points at.
5. **Clean up** your synthetic rows afterward (`DELETE ... WHERE external_id IN (...)`).

Example (Telegram, private chat, plain text triggers onboarding; `/start` may not — see the gap
above):

```bash
SECRET=$(grep -E '^TELEGRAM_WEBHOOK_SECRET=' .env.local | cut -d= -f2-)
curl -s -o /dev/null -w "%{http_code}\n" -X POST "https://<host>/api/v1/integrations/telegram/webhook" \
  -H "Content-Type: application/json" \
  -H "x-telegram-bot-api-secret-token: ${SECRET}" \
  -d '{"update_id":99900001,"message":{"message_id":1,"date":1,"chat":{"id":99900001,"type":"private","first_name":"E2E"},"from":{"id":99900001,"is_bot":false,"first_name":"E2E"},"text":"hi"}}'
# then: wrangler d1 execute <db> --remote --command \
#   "SELECT source,external_id,step FROM bot_onboarding_state WHERE external_id='99900001';"
```

### The two-step replay, proven live

Fire two inbounds in sequence and check the DB effect after each (proven on Telegram against prod):

1. **Inbound 1** (`"hi"` from a fresh handle) → the shared onboarding machine writes a
   `bot_onboarding_state` row (columns `source`, `external_id`, `step`, `attempts`, `data`,
   `update_counter`) with `step='awaiting_choice'`.
2. **Inbound 2** (text `NEW`) → provisions a real email-less account and a **verified**
   `external_identity` row (`platform`, `external_id`, `user_id`, `verified=1`), then **deletes** the
   onboarding row. Text `LINK` instead takes the link-to-existing-web-account branch.

`handleUnrecognizedInbound` (the onboarding machine) is **shared by all 5 bots**, so proving it live
on ONE forgeable platform proves the whole pipeline. Per-platform code is only the webhook adapter —
unit-test each of those.

**Reading prod D1 without wrangler D1 access:** POST to the Cloudflare D1 HTTP API
`POST /accounts/{acc}/d1/database/{dbid}/query` with `{sql, params}` and a token that has D1 read.
**SQL string literals need SINGLE quotes** — double quotes are SQLite identifiers, so
`WHERE external_id="99900001"` matches nothing and returns zero rows with no error.

### Which platforms you can forge for a synthetic e2e

You can replay a signed inbound only when **you** hold the signing secret:

| Platform | Forge? | How |
|---|---|---|
| Telegram | yes | static header `x-telegram-bot-api-secret-token` = deployed secret |
| iMessage (Sendblue) | yes | HMAC with `sb-signing-secret` |
| Slack | yes | `X-Slack-Signature: v0=` + `HMAC_SHA256(signingSecret, "v0:{ts}:{body}")`, header `X-Slack-Request-Timestamp` within 300s of now |
| WhatsApp | yes | `x-hub-signature-256: sha256=` + `HMAC_SHA256(appSecret, body)` |
| Discord | **no** | Discord signs each interaction with Ed25519 and holds the private key; the app only verifies with Discord's public key. A synthetic Discord inbound is impossible — cover Discord with unit tests + real-app testing. |

**Scoping caveat:** Telegram and iMessage/Sendblue are global-number bots — any DM onboards, so a
signed POST is a complete sim. Slack needs the app installed in a workspace (a team integration must
exist for the bot token to reply) and WhatsApp needs the business number configured, so their
synthetic onboarding needs a real installed workspace/number, not a signed POST alone.
