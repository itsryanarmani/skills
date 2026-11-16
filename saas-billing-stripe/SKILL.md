---
name: saas-billing-stripe
description: "Use when a human needs to subscribe to a SaaS and pay on a recurring Stripe plan, or when the ask mentions 'Stripe subscriptions', 'monthly billing', 'recurring payments', 'subscription checkout', 'customer portal', 'failed subscription payments', or 'dunning' for a web product. Do not use for PPP or country-based pricing, agent-to-API payments, or an agent buying goods."
---

# SaaS Billing with Stripe

The default for a new SaaS is a server-created Stripe Checkout Session in `subscription` mode.
It gives you recurring billing, authentication, taxes, and hosted checkout with less code. Stripe
recommends Checkout Sessions for most integrations. [Checkout Sessions API](https://docs.stripe.com/payments/checkout-sessions)
For pricing strategy, read [regional-pricing-stripe](../regional-pricing-stripe/SKILL.md). Do not
re-teach PPP, currency tiers, or `tax_behavior` here.

## 1. Choose the checkout surface

### Checkout Session: default for a new SaaS

Create the Session on the server, then redirect the browser to its Stripe-hosted `url`. Use
`POST /v1/checkout/sessions` with `mode=subscription` and a server-selected recurring Price in
`line_items`. Set `success_url` for the return path. [Checkout Session API reference](https://docs.stripe.com/api/checkout/sessions)

This path handles subscription creation, payment method collection, customer authentication,
and Checkout state. A success page is not proof that your database has received the webhook.
Use embedded Checkout only when the product needs the form inside its own page. It still uses
Checkout Sessions, but it adds frontend state and deployment work.

### Payment Link: right for a fixed, reusable sales link

Use a Payment Link when the same recurring product can be sold from a Dashboard URL, email, QR
code, or buy button. A recurring Price creates a subscription from the link. [Create a payment link](https://docs.stripe.com/payment-links/create)

It is a poor default when your app must bind checkout to the signed-in account, select a plan
from app state, or start an entitlement workflow. The link is reusable by anyone who receives it.

### Elements: right when the checkout UI is a product requirement

Use Stripe Elements when the team must own the payment form, layout, or field interaction. Use
Checkout Sessions with Elements for the higher-level flow where possible. Choose Payment Intents
only when the app must own tax, discounts, subscriptions, and currency conversion. [Stripe Elements](https://docs.stripe.com/payments/elements)

Elements tokenizes payment details so they do not reach your server. It does not remove the need
for server-side Price selection, subscription webhooks, or access control.

## 2. Model the subscription lifecycle

Stripe sends a subscription `status`. Store the customer ID, subscription ID, status, and mapping
to your Better Auth user in D1. Your app database is the read model for access checks. [Subscription object](https://docs.stripe.com/api/subscriptions/object)
Use this access policy unless the product has a documented grace-period policy:

- `trialing`: allow access during the trial.
- `active`: allow access. This means the subscription is in good standing, not that every old
  invoice is paid.
- `past_due`: show a payment warning. Allow only a short, explicit grace period if the product
  accepts that risk. Do not treat it as permanently active.
- `canceled`: deny access. This is terminal, and the subscription cannot be updated.
- `paused`: deny access until the customer adds a payment method and resumes the subscription.

Also deny `unpaid`, `incomplete`, and `incomplete_expired` by default. A trial is the `trialing`
status. `paused` differs from pausing invoice collection. [Subscription webhooks](https://docs.stripe.com/billing/subscriptions/webhooks)

Run the access check on the server for every protected request, or in protecting middleware. Read
the status from D1. Never accept `plan=pro`, `isPaid=true`, or browser-stored subscription status.

Do not grant access from the checkout return page. The page can poll your server for the local
record while the webhook is still in flight.

## 3. Make webhooks the source of truth

Stripe retries failed deliveries, can repeat events, and does not guarantee event order. Return a
fast `2xx` after durable recording, then process the event in a queue or short background task. [Webhook delivery behavior](https://docs.stripe.com/webhooks)

### Verify the raw request body first

This is the most common Stripe integration bug: `request.json()` or JSON parsing changes the
payload, so verification fails. Read `await request.text()` exactly once. Verify that raw string
with `Stripe-Signature` before parsing the event. [Resolve signature errors](https://docs.stripe.com/webhooks/signature?lang=node)
Cloudflare Workers does not provide Node’s crypto runtime. The Node SDK’s synchronous
`constructEvent` path needs Node crypto. Use the Fetch HTTP client and Web Crypto provider, then
await `constructEventAsync`:

```ts
const stripe = new Stripe(env.STRIPE_SECRET_KEY, {
  httpClient: Stripe.createFetchHttpClient(),
});

const rawBody = await request.text();
const signature = request.headers.get("Stripe-Signature");
const event = await stripe.webhooks.constructEventAsync(
  rawBody,
  signature,
  env.STRIPE_WEBHOOK_SECRET,
  undefined,
  Stripe.createSubtleCryptoProvider(),
);
```
The official runtime example uses `request.text()` and `constructEventAsync`. [stripe-node Deno webhook example](https://github.com/stripe/stripe-node/blob/master/examples/webhook-signing/deno/main.ts)

Reject a missing header, a bad signature, or a bad payload with `400`. Do not log the webhook
secret or the full customer payload.

### Make delivery idempotent

Create a D1 table with a unique Stripe event ID. Insert before side effects. If the event exists,
return `200` without granting access or sending another email. Upsert the subscription row. Some
duplicate business notifications have different event IDs, so make updates safe for subscription
ID and event type too.

### Handle useful events only

Start with these events:

- `checkout.session.completed`: connect the Stripe customer and subscription to the local user.
- `customer.subscription.created`: create or upsert the subscription record.
- `customer.subscription.updated`: store status, plan, trial, and cancellation changes.
- `customer.subscription.deleted`: revoke access and mark the record canceled.
- `customer.subscription.paused` and `customer.subscription.resumed`: change access when a trial
  ends without a payment method or the customer later resumes.
- `invoice.paid`: record successful recurring collection and extend any local billing marker.
- `invoice.payment_failed`: mark the subscription at risk and direct the customer to billing.

Treat `customer.subscription.trial_will_end` as a reminder event, not an access decision. Treat
`invoice.upcoming` as advisory. Do not subscribe to every event, or let `charge.*` and
`payment_intent.*` become a second billing state machine unless the chosen integration needs them.

The ordering trap is real: `checkout.session.completed` can arrive after
`customer.subscription.created`. Do not require checkout before saving the subscription. Use stable
metadata or a pending checkout row to join both events. Retrieve missing objects by ID and retry
the join later. [Subscription webhook events](https://docs.stripe.com/billing/subscriptions/webhooks)

## 4. Use the Customer Portal

The Customer Portal is the cheapest way to avoid building billing settings. Enable its features
in the Dashboard, then create a short-lived session on your server when an authenticated user
clicks “Manage billing”. It supports payment methods, plan changes, cancellation, and invoice
history. [Customer Portal](https://docs.stripe.com/customer-management)
Create the session with `POST /v1/billing_portal/sessions`, passing the server-side `customer`
ID and a `return_url` when the Dashboard has no default. Redirect to the returned `url`. Never
accept a customer ID from the browser. [Create a portal session](https://docs.stripe.com/customer-management/integrate-customer-portal)

Configure allowed products, cancellation behavior, and proration in the Portal settings. Keep
your webhook handler as the authority after an upgrade, downgrade, or cancellation.

For a product-specific cancellation experience, follow the
[subscription cancellation flow](references/subscription-cancellation.md).
It defines the screens, site-specific reasons, editable admin settings, billing
actions, and E2E evidence. Keep the existing cancellation path available while
adding optional help and retention offers.

## 5. Configure dunning before launch

Failed renewals cause involuntary churn. Smart Retries and recovery emails are Dashboard
configuration, not a first-pass cron job. Enable Smart Retries, set failed-payment emails, and
choose what happens after retries exhaust. [Revenue recovery](https://docs.stripe.com/billing/revenue-recovery)

Handle `invoice.payment_failed` in the app so the customer sees a clear billing warning. Stripe
can expose the next retry time in `next_payment_attempt` on that event when dunning is enabled.
Do not revoke access on the first transient failure unless the product explicitly requires it.
Do not promise access forever while the subscription stays `past_due` or becomes `unpaid`.

## 6. Keep test mode and live mode separate

Use separate server secrets, publishable keys, webhook endpoints, signing secrets, and Price IDs.
Test keys use `pk_test_` and `sk_test_`; live keys use `pk_live_` and `sk_live_`. Objects in one
mode cannot be used in the other. [API keys and modes](https://docs.stripe.com/keys)

Set separate environment values such as `STRIPE_PRICE_PRO_MONTHLY_TEST` and
`STRIPE_PRICE_PRO_MONTHLY_LIVE`, or use separate secret stores per deployment. A test-mode Price
ID sent with a live key is not a live catalog object. Checkout creation fails instead of creating
the intended subscription. [Manage products and Prices](https://docs.stripe.com/products-prices/manage-prices)

Use separate test and production webhook URLs. Each endpoint has its own `whsec_` secret. Check
the event’s `livemode` value at the boundary, and keep test events out of the production D1
database. Switching API keys alone is not a go-live plan.

## 7. Decide on Stripe Tax

Stripe Tax is worth enabling for a SaaS that sells across jurisdictions and wants Stripe to
calculate indirect tax during Checkout. It uses seller location, customer location, product type,
and customer status. Enable `automatic_tax[enabled]=true`, then add registrations and tax codes.
[Calculate tax](https://docs.stripe.com/tax/calculating)

Stripe Tax does not register the business everywhere, replace tax advice, or automatically file
and remit every return. Registration and filing remain separate responsibilities unless you buy an
eligible service. It also has unsupported products and territories.
[Set up Stripe Tax](https://docs.stripe.com/tax/set-up), [file and remit](https://docs.stripe.com/tax/filing)

For the one-way `tax_behavior` decision, read [regional-pricing-stripe](../regional-pricing-stripe/SKILL.md).

## 8. Keep prices and amounts server-controlled

The browser may request a catalog key such as `pro_monthly`. It must never choose a Stripe Price
ID, amount, currency, or plan entitlement. Resolve that key through your own server catalog for
the current environment. Create the Checkout Session with the resolved recurring Price.

Do not trust a client-sent amount when creating a Payment Link, Checkout Session, subscription,
or portal action. The Stripe secret key stays in Workers secrets. The publishable key may reach
the browser, but it cannot decide what the server bills.

## Checklist

1. Choose a server-created Checkout Session in `subscription` mode for the default SaaS flow.
2. Use Payment Links only for fixed, reusable links. Use Elements only when custom UI justifies it.
3. Store Stripe IDs and status in D1, and gate access server-side from that local record.
4. Allow `trialing` and `active`; define and time-box any `past_due` grace period.
5. Read the raw webhook body, verify `Stripe-Signature`, and use `constructEventAsync` on Workers.
6. Record event IDs uniquely, make subscription updates idempotent, and tolerate reordering.
7. Handle subscription, invoice, and checkout events needed by the access model only.
8. Use the Customer Portal for payment methods, plan changes, cancellation, and invoice history.
9. Enable Smart Retries and failed-payment emails before the first live subscription.
10. Separate test and live keys, endpoints, secrets, Price IDs, and D1 data.
11. Enable Stripe Tax only after checking registrations, tax codes, and filing responsibility.
12. Resolve every billable Price server-side from the environment-specific catalog.

## Related

- `pricing-page` — what to charge and how to present it. This skill collects the
  money; that one decides the number.
- `regional-pricing-stripe` — when the price varies by market.
- `lifecycle-email` — carries the dunning mail this skill depends on.
- `unit-economics` — whether the revenue this collects covers what acquisition cost.
