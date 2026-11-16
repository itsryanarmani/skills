---
name: ads-linkedin
description: "Set up LinkedIn Ads with a self-serve Campaign Manager account, the Insight Tag, and LinkedIn Conversions API — including direct non-expiring token access, approved partner OAuth, SHA-256 email matching, li_fat_id capture, eventId deduplication, conversion-rule settings, and Campaign Manager verification. Use when wiring LinkedIn signup, lead, checkout, purchase, or subscription tracking, fixing low match rates, or launching a B2B paid test."
---

# LinkedIn Ads

LinkedIn Ads has a self-serve ad account and a real Conversions API. Create and
associate a conversion rule, then send confirmed events.

Use [ad-conversion-hub](../ad-conversion-hub/SKILL.md) for the canonical event
envelope, consent gate, identity rules, retry policy, and adapter contract.
## Account and access

Campaign Manager is self-serve. Select **For Business → Advertise** in
LinkedIn, then create an ad account. A Business Manager account requires an
admin. The creator gets account manager and billing admin access. Currency
cannot change later. LinkedIn says the same of the Company Page once set, but
you can add a Page to an account that has none. A Company Page is required for
full features.
See [Create an ad account](https://www.linkedin.com/help/lms/answer/a422205).

### Create the ad account in the browser

Verified 2026-11-16 in a signed-in Chrome. Do each step in order.

1. Open `https://www.linkedin.com/campaignmanager/accounts`.
2. Select **Create account**. A dialog opens.
3. Enter the account name. The field is prefilled, so replace the value.
4. Choose the currency. You cannot change it later. Match the currency of the
   card that will pay.
5. Open **Associate a LinkedIn Page**. Type the Page name to search. Choose the
   Page. You can also save without one and add it later (see the traps).
6. Tick **I agree to the LinkedIn Ads Agreement and Advertising Guidelines**.
7. Select **Save**. LinkedIn opens the campaign setup page. The URL holds the new
   account ID: `/campaignmanager/accounts/<ACCOUNT_ID>/campaigns/new/setup`.

The new account has the status **On hold: payment method required**. No ad runs
until a person adds a card under **Billing**. An agent must not enter card details.

Traps:

- The Escape key closes the whole dialog and discards the fields. To close the
  Page list, select another field instead.
- The Page list shows only about ten Pages. A Page you administer can be
  missing from it. Type the name to search before you create a new Page.
- A Page you do not administer never appears. Ask its admin to add you.
- To add a Page to an account that has none, open the accounts list, hover the
  row, select **Edit**, choose the Page under **Associate a LinkedIn Page**, and
  select **Update account**. Verified on a live account.

For a direct advertiser integration, use **Data → Signals Manager → Direct API
→ Generate access token**. This route needs no developer application. The
token does not expire and appears once. Store it at once. See [CAPI access](https://learn.microsoft.com/en-us/linkedin/marketing/conversions/getting-access-conversions?view=li-lms-2026-08).

For a product serving several advertisers, request the Conversions API product
for a developer app. LinkedIn reviews the business details and use case. A Page
super admin must verify the app. Partner OAuth uses `rw_conversions` and
`r_ads`; the member needs a non-`VIEWER` role. See [partner access](https://learn.microsoft.com/en-us/linkedin/marketing/conversions/getting-access-conversions?view=li-lms-2026-08) and [the API workflow](https://learn.microsoft.com/en-us/linkedin/marketing/conversions/conversions-workflow?view=li-lms-2026-08).

LinkedIn defines no environment-variable names. This skill uses the hub
convention:

```text
LINKEDIN_TAG_ID                public Insight Tag partner ID
LINKEDIN_ACCOUNT_URN           urn:li:sponsoredAccount:<id>
LINKEDIN_CAPI_TOKEN             server-only direct or OAuth bearer token
LINKEDIN_CAPI_CONVERSION_URN    urn:lla:llaPartnerConversion:<id>
LINKEDIN_INSIGHT_CONVERSION_ID  browser conversion rule ID
LINKEDIN_VERSION                value for the Linkedin-Version header
```
## Client-side Insight Tag

Create the tag under **Data → Signals Manager → Insight Tag**. Copy its partner
ID. Load it on every eligible page in the global footer, just before `</body>`.
See [Insight Tag conversion tracking](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/conversion-tracking?view=li-lms-2026-08).

```html
<script type="text/javascript">
  _linkedin_partner_id = "<LINKEDIN_TAG_ID>";
  window._linkedin_data_partner_ids = window._linkedin_data_partner_ids || [];
  window._linkedin_data_partner_ids.push(_linkedin_partner_id);
</script>
<script type="text/javascript">
  (function (l) {
    if (!l) {
      window.lintrk = function (a, b) { window.lintrk.q.push([a, b]); };
      window.lintrk.q = [];
    }
    var s = document.getElementsByTagName("script")[0];
    var b = document.createElement("script");
    b.type = "text/javascript"; b.async = true;
    b.src = "https://snap.licdn.com/li.lms-analytics/insight.min.js";
    s.parentNode.insertBefore(b, s);
  })(window.lintrk);
</script>
<noscript><img height="1" width="1" style="display:none" alt=""
  src="https://px.ads.linkedin.com/collect/?pid=<LINKEDIN_TAG_ID>&fmt=gif" /></noscript>
```

For a page-load conversion, set the shared ID before the base tag:

```html
<script>window._linkedin_event_id = "<CANONICAL_EVENT_ID>";</script>
```

For an event-specific conversion, pass the same ID to `lintrk`:

```js
window.lintrk("track", {
  conversion_id: "<LINKEDIN_INSIGHT_CONVERSION_ID>",
  event_id: canonicalEvent.event_id,
});
```
## Rule setup and event mapping

The streaming payload has no free-form event name. The conversion rule's
`type` supplies the LinkedIn event name. Create a rule per type. Use separate
browser and server rules when you enable deduplication.

| Hub event | LinkedIn rule type | Send when |
|---|---|---|
| `page_view` | `KEY_PAGE_VIEW` | Important page only |
| `view_content` | `VIEW_CONTENT` | Meaningful product or plan view |
| `lead` | `LEAD` | Qualified lead submission |
| `signup` | `SIGN_UP` or `COMPLETE_SIGNUP` | Account or registration completes |
| `begin_checkout` | `START_CHECKOUT` | Checkout starts |
| `purchase` | `PURCHASE` | Payment provider confirms a charge |
| `subscription_start` | `SUBSCRIBE` | Paid subscription activates |
| `refund` | Do not dispatch | Reconcile with payment truth |

These types are in the [CAPI schema](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/conversions-api-schema?view=li-lms-2026-08). LinkedIn documents no `REFUND` type.

Create a CAPI rule:

```http
POST https://api.linkedin.com/rest/conversions?autoAssociationType=ALL_CAMPAIGNS
Authorization: Bearer <LINKEDIN_CAPI_TOKEN>
Content-Type: application/json
Linkedin-Version: <LINKEDIN_VERSION>
X-Restli-Protocol-Version: 2.0.0
```

```json
{
  "name": "CAPI purchase",
  "account": "urn:li:sponsoredAccount:<ACCOUNT_ID>",
  "conversionMethod": "CONVERSIONS_API",
  "postClickAttributionWindowSize": 90,
  "viewThroughAttributionWindowSize": 30,
  "attributionType": "LAST_TOUCH_BY_CAMPAIGN",
  "type": "PURCHASE"
}
```

Save the returned ID as `urn:lla:llaPartnerConversion:<id>`. Without automatic
association, use the Campaign Conversions API or Campaign Manager UI. LinkedIn
only attributes to associated campaigns. See [Conversions API](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/conversions-api?view=li-lms-2026-08).

## Server-side Conversions API

Send the confirmed event to `POST https://api.linkedin.com/rest/conversionEvents`
with the same bearer and version headers above:

```json
{
  "conversion": "urn:lla:llaPartnerConversion:<CONVERSION_ID>",
  "conversionHappenedAt": 1730017211229,
  "conversionValue": { "currencyCode": "USD", "amount": "25.00" },
  "user": { "userIds": [
    { "idType": "SHA256_EMAIL", "idValue": "<SHA256_EMAIL_HEX>" },
    { "idType": "LINKEDIN_FIRST_PARTY_ADS_TRACKING_UUID", "idValue": "<LI_FAT_ID>" }
  ]},
  "eventId": "<CANONICAL_EVENT_ID>"
}
```

`conversion`, `conversionHappenedAt`, and `user` are the event fields. The
timestamp is epoch milliseconds and must be within 90 days. The value amount is
a decimal string. At least one valid identity is required unless another valid
user field supplies identity. A successful single event returns `201 Created`.
See [the event schema](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/conversions-api-schema?view=li-lms-2026-08).

Batch requests use `X-RestLi-Method: BATCH_CREATE` and allow 5,000 events. Use
the hub's bounded retry and dead-letter policy. Do not replay an uncertain
request unless the dispatch record and `eventId` rule make it safe. See [CAPI FAQ](https://learn.microsoft.com/en-us/linkedin/marketing/conversions/conversions-faq?view=li-lms-2026-08).

## Identity and consent

- Require `measurement: true` in the hub before any LinkedIn event.
- Require `ad_user_data: true` before hashed email, IP, or external IDs.
- Remove email whitespace, lowercase it, then SHA-256 hash it. Send lowercase
  hexadecimal text. Do not hash an existing hash again.
- Supported IDs include `SHA256_EMAIL`, `LINKEDIN_FIRST_PARTY_ADS_TRACKING_UUID`,
  `ACXIOM_ID`, `PLAINTEXT_IP_ADDRESS`, `SHA256_IP_ADDRESS`, and `GOOGLE_AID`.
- Plain and hashed IP IDs support IPv4 only. `userInfo` is plain text and needs
  both `firstName` and `lastName`. `externalIds` accepts one advertiser ID.
- LinkedIn preserves a matched external-ID mapping for one year across ad
  accounts in the same Business Manager. Pair it with a standard ID first.

The hub owns normalization and consent. LinkedIn also prohibits the Insight Tag
on pages that collect sensitive health or financial data. See [privacy guidance](https://www.linkedin.com/help/lms/answer/a515671).

## Click ID and first-party cookie

Enable **Enhanced conversion tracking** for the Insight Tag. LinkedIn then adds
`li_fat_id` to ad landing URLs. Capture it on first landing and persist first-
touch and latest values in first-party storage. The cookie lasts 30 days from
the latest qualifying ad click. Send it to CAPI as
`LINKEDIN_FIRST_PARTY_ADS_TRACKING_UUID`. Parsing only the URL can limit view-
through attribution; reading the cookie supports it. Do not require a click ID
before sending a server purchase. See [Enabling Click IDs](https://learn.microsoft.com/en-us/linkedin/marketing/conversions/enabling-first-party-cookies?view=li-lms-2026-08).

New tags enable first-party tracking by default. Check
`firstPartyTrackingEnabled` when the cookie or `li_fat_id` is absent. Campaign
Manager and the partial update API can change this setting.

## Deduplication

LinkedIn reconciles browser and server copies with `eventId`.

1. Create a browser Insight Tag rule and a server CAPI rule for the action.
2. Put the same hub `event_id` in browser `event_id` and server `eventId`.
3. Set `_linkedin_event_id` before the page-load tag, or pass `event_id` to
   `lintrk` for an event-specific conversion.
4. Check both conversion breakdowns. For the same account and ID, LinkedIn
   counts the Insight Tag copy and discards the CAPI twin.

See [LinkedIn deduplication](https://learn.microsoft.com/en-us/linkedin/marketing/conversions/deduplication?view=li-lms-2026-08). The event ID is not the conversion rule URN.

## Campaign Manager settings that override code

- `enabled=false` stops a rule from matching events.
- `conversionMethod` must be `CONVERSIONS_API` for server rules.
- No campaign association means no campaign attribution.
- The rule controls attribution windows and model. Current CAPI defaults are
  30 days post-click and 7 days view-through. Supported windows include 1, 7,
  30, and 90 days; 365 days is limited to some types.
- `DYNAMIC`, `FIXED`, and `NO_VALUE` control reported conversion value.
- A blocked Insight Tag domain sends no downstream conversion or audience signal.
- Website Actions can create conversions that stay inactive until approved.

See [rule settings](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/conversions-api-schema?view=li-lms-2026-08) and [Website Actions](https://www.linkedin.com/help/lms/answer/a1441293?lang=en-US).

## Verification

1. **Request proof:** record the redacted event response. `201 Created` proves
   request acceptance, not attribution.
2. **Platform proof:** in Campaign Manager, open **Measurement → Conversion
   Tracking**. Check the CAPI rule status and match rate. `Active` with a good
   match rate shows receipt and identity matching. `Low Match Rate` shows poor
   identity matching. Read active CAPI rules with `GET /rest/conversions`,
   filtering `enabled=true` and `conversionMethod=CONVERSIONS_API`.
3. **Business proof:** open **Conversions & Leads**, break down by conversion,
   and reconcile counts and value with succeeded charges.

For the tag, query `GET https://api.linkedin.com/rest/insightTagDomains?q=account&account=<ENCODED_ACCOUNT_URN>`. Domains can take 5–10 minutes to populate after a visit. See [tag verification](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/conversion-tracking?view=li-lms-2026-08) and [CAPI measurement](https://learn.microsoft.com/en-us/linkedin/marketing/conversions/conversions-usecase?view=li-lms-2026-08).

## Common pitfalls and security

- Use `urn:li:sponsoredAccount:<id>` for the account and
  `urn:lla:llaPartnerConversion:<id>` for the rule.
- Use epoch milliseconds, not seconds. Use `eventId`, not `event_id`, in CAPI.
- Do not send raw email, an uppercase hash, or a double-hashed email.
- Do not create a new browser and server ID for one event.
- Do not send only `li_fat_id`; organic and direct events still matter.
- Do not treat `201`, a live tag request, or an active campaign as attribution.
- Recheck rule status, domain status, campaign association, member role, and
  `rw_conversions`/`r_ads` after any access change.
- Keep `LINKEDIN_CAPI_TOKEN` server-side. Never put it in browser code, URLs,
  logs, screenshots, or commits. Use HTTPS, redact bearer tokens, apply the hub
  consent gate, and delete temporary normalized identifiers after dispatch.

## Official sources checked (2026-08-28)

- [Account](https://www.linkedin.com/help/lms/answer/a422205) · [CAPI access](https://learn.microsoft.com/en-us/linkedin/marketing/conversions/getting-access-conversions?view=li-lms-2026-08) · [CAPI](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/conversions-api?view=li-lms-2026-08)
- [Schema](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/conversions-api-schema?view=li-lms-2026-08) · [Click IDs](https://learn.microsoft.com/en-us/linkedin/marketing/conversions/enabling-first-party-cookies?view=li-lms-2026-08) · [Deduplication](https://learn.microsoft.com/en-us/linkedin/marketing/conversions/deduplication?view=li-lms-2026-08)
- [Insight Tag](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/conversion-tracking?view=li-lms-2026-08) · [CAPI measurement](https://learn.microsoft.com/en-us/linkedin/marketing/conversions/conversions-usecase?view=li-lms-2026-08) · [Privacy](https://www.linkedin.com/help/lms/answer/a515671)
