---
name: chatgpt-business-claim
description: "Claim a verified Businesses in ChatGPT profile for each site of a multi-site directory monorepo, using DNS TXT verification on Cloudflare. Covers the Business Hub flow, the exact TXT record shape, the 30-minute challenge expiry, the stop rules that keep you from claiming someone else's business, and a script that repeats the flow per site. Use when a site needs a verified ChatGPT business profile, a blue check, or Business Hub access."
---

# Claim a ChatGPT business profile

Businesses in ChatGPT launched in beta on 2026-11-10. A verified profile lets a
site owner edit business details, add a product feed, and create a Business
Agent. The Hub is at `chatgpt.com/business-hub`.

Facts below come from one real claim on 2026-11-10. The Hub is in beta, so
re-check the screens if a step differs.

**Use when:** a site you own needs a verified profile and its DNS is on
Cloudflare.

## What a claim does

A claim says you control the domain. It ties the profile to your OpenAI account
and accepts the Businesses in ChatGPT Terms. Do it only for domains you own.
There is no bulk API. Each site is one pass through the Hub.

## The flow

1. Search the Hub for the site name. **Stop if a business matches.** A match
   means a profile already exists, and it may belong to someone else.
2. Select "Create '<name>'". Accept the terms dialog ("Get started").
3. Choose how customers use the business. "Through a service" is marked coming
   soon. A site that sells through its own pages fits "Through an online store".
   This is a factual claim about the business, so confirm it per site.
4. Enter the site URL and continue.
5. The Hub shows a TXT record:

   | Field | Value |
   | --- | --- |
   | Type | `TXT` |
   | Name | `openai-business-profile.<domain>` |
   | Value | `openai-business-profile=<one-time token>` |

   **The challenge expires about 30 minutes after it appears.** Add the record
   in that window.
6. Add the record with a TTL of 60. Check it with
   `dig +short TXT openai-business-profile.<domain>`.
7. Select "Verify domain". Success moves the page to "Help people get to know
   <name>", which asks for a category. Finish the profile by hand.

## Script

`chatgpt-business-claim.mjs` in the scripts repo runs steps 1 to 7.

```sh
# List sites: id, name, domain
node chatgpt-business-claim.mjs plan <repo-dir>

# Dry run: names the sites and writes nothing
node chatgpt-business-claim.mjs claim <repo-dir> <site>

# Real claim, one site at a time
CLOUDFLARE_API_TOKEN=... node chatgpt-business-claim.mjs claim <repo-dir> <site> --yes
```

It needs the `browse` CLI attached to a browser that is signed in to ChatGPT, and
a Cloudflare token that can edit DNS on the zone. It exits non-zero if any
claim does not verify. It writes `e2e-artifacts/chatgpt-business-claim/result.json`
with the site, domain and stage. The file has no token and no TXT value.

The script has no "all sites" mode on purpose. Name each site.

## Stop rules

- **Hub match:** the script stops with `hub-has-match`. Review by hand.
- **No challenge found:** the Hub UI changed. Update the selectors.
- **Verify failed:** DNS may not have settled. Run again once `dig` shows the
  record. A repeat run replaces the record and does not add a second one.
- **Never** commit a token, a TXT value or a signed-in browser profile.

## Not covered

Category, hours, address and product feeds are set in the Hub after
verification. Business Agents are limited to eligible US ecommerce and online
service businesses at launch, and verification alone does not grant one.
