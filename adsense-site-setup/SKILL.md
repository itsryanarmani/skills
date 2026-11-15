---
name: adsense-site-setup
description: "Create or reactivate a Google AdSense account and connect a live site for display ads — account chooser and reactivation, payments and tax gates, add-site and ownership proof (meta tag and ads.txt preferred), pre-verify with adsense-check, review and rejection recovery, consent-gated slots after approval, and browse/handoff rules for the AdSense UI. Use when a site needs AdSense display income and the account is new, dormant, or missing the domain."
---

# adsense-site-setup

You use this skill when a production site should earn display-ad income through
Google AdSense and the publisher account is missing, dormant, or not yet linked
to that domain. You finish with ownership proof deployed, review requested, and
a clear record of site status in private project notes.

Facts below are **Observed** (from a signed-in session on 2026-11-14) or
**Documented, verify** (from Google's published behavior; confirm in the live
UI before you rely on them).

## When to use it, and when not

Use this skill for a live site that needs Google display-ad income and you can
edit its HTML, `ads.txt`, and consent behavior.

Do not use it when traffic is far below roughly 10,000 sessions per month unless
the owner explicitly wants AdSense anyway. **Documented, verify:** at that scale,
income is often only a few dollars a month.

This skill does not cover higher-traffic ad networks. **Documented, verify:**
Mediavine and Raptive typically require much higher minimums (often roughly 50,000
sessions and 100,000 pageviews per month). Check each network's current thresholds
before you steer a site there.

## Before you start (checklist)

Confirm all of the following before you open AdSense:

- The site is live on a public domain you control.
- It has real content pages, a privacy policy, an about page, and a contact page.
- It is not marked "under construction" and does not show a full login wall to
  Google's crawlers.
- **Documented, verify:** one Google account should own one AdSense publisher
  identity; many sites can sit in that single account, and each site is reviewed
  on its own.
- The legal name and address on the payments profile must match bank and tax
  records the owner will use.
- **Documented, verify:** if the site shows ads to visitors in the EEA, the UK,
  or Switzerland, Google may require a certified consent management platform.
- **Our rule (not Google's):** never load an ad script before consent.

## Check whether an account already exists

1. Open the AdSense start flow and choose **Get started**. Read the Google
   account chooser. **Documented, verify:** several accounts can appear; pick the
   one that should receive payments.
2. **Observed:** an old account can still exist but show as deactivated. The home
   page then says the account was deactivated because it is inactive, with a
   **Reactivate account** button.
3. **Observed:** reactivation completed with no phone prompt in that session. The
   home page then showed three cards: Payments (**We've got your info**), Ads
   (optional), and Sites (**Connect your site to AdSense**, required).
4. **Documented, verify:** Google may still ask for phone verification or a fresh
   site submission after reactivation in other cases.

## New account: every question AdSense asks

**Documented, verify** for this entire section unless a future run updates it.

Walk the owner through each screen. You do not type bank or tax identifiers.

| Stage | What AdSense asks |
| --- | --- |
| Sign-up | Website URL, account email, whether to receive customized help, country or territory, acceptance of AdSense terms |
| Payments profile | Account type (individual or business), name and address, phone number and SMS PIN |
| Tax | Non-US publishers often complete W-8BEN or similar under Payments → Manage settings → Tax info; Canada may use treaty fields |
| Payout | Payment method (bank transfer is common) |
| Address PIN | A PIN card by post may be required after earnings pass a small threshold |
| Threshold | Payment threshold is a fixed amount that varies by currency |

Tell the owner that payment, tax, and phone decisions are theirs alone. Use
`handoff()` before any tax form, bank detail, or SMS PIN entry.

## Add the site

1. On the onboarding **Sites** card or in **Sites**, choose **Add site**.
2. Enter the bare domain (`example.com`) with no `https://` prefix. **Observed:**
   the dialog has one **Website** field.
3. **Observed:** after save, the domain appears in a site selector at the top of
   the home page.
4. **Documented, verify:** add the apex domain; check whether a subdomain needs
   its own entry before you rely on one listing for all hosts.

## Connect the site (ownership proof)

1. On the Sites card, press **Let's go** to start ownership proof.
2. **Observed:** in that session, **Let's go** did not respond to automated clicks
   (role-based click and coordinate click). The page did not change. A person must
   press the button, or you retry in a fresh browser session later.
3. **Documented, verify:** AdSense then offers three proof options:
   - (a) AdSense code snippet in `<head>` (loads ad-related script).
   - (b) An `ads.txt` authorization line on the root domain.
   - (c) A meta tag in `<head>` on the home page.

**Prefer (c) and (b) together before approval. Avoid (a) until the site is
approved**, because the snippet loads ad script and may conflict with your
consent rule.

Meta tag (home page `<head>`, no script load):

```html
<meta name="google-adsense-account" content="ca-pub-0000000000000000">
```

`ads.txt` at the site root (`/ads.txt`), HTTP 200, `Content-Type: text/plain`,
one line, no redirect to another domain:

```text
google.com, pub-0000000000000000, DIRECT, f08c47fec0942fa0
```

The last field is **Documented, verify:** Google's published certification
authority id for AdSense.

## Check the site before you press Verify

**Observed:** running the checker before **Verify** catches wrong content types and
redirects that AdSense would reject.

Run the public helper:

```bash
adsense-check <domain> <publisher-id>
```

The `adsense-check` script lives in the shared scripts repository (`scripts`
tree). It reports pass or fail for `ads.txt` and the meta tag, including HTTP
status codes.

Fix any failure before you continue. Wrong content type or a redirect is the
usual cause.

## Request review and wait

1. In AdSense, press **Verify**, then **Request review**.
2. **Documented, verify:** review can take from a few days to a few weeks.
3. **Documented, verify:** expect statuses such as **Getting ready**, **Needs
   attention**, **Ready**, and **Requires action**.
4. Do not add ad slots while the site is under review.

## If the site is rejected

1. Read the reason on the **Sites** page.
2. **Documented, verify:** common reasons include low value or thin content,
   site down or unreachable, navigation problems, duplicate or scraped content,
   policy violations, or site not ready.
3. Fix the underlying cause, then request review again.
4. Record the rejection reason in private project notes. Thin directory sites with
   many near-empty pages are at higher risk; improve the strongest content section
   first.

Approval timing and earnings are not guaranteed. Do not state an outcome as fact.

## After approval

- Add ad slots only through a consent-gated component that renders nothing before
  consent and reserves height to limit layout shift.
- Do not show ads on private or signed-in-only pages.
- **Documented, verify:** never click your own ads or ask others to; invalid
  traffic can lead to account closure.
- Block scrapers and headless crawlers at the edge where you can, so invalid
  traffic is less likely to count against the account.

## Driving the browser

**Observed:** the AdSense UI trusts the person's existing Google session when you
use signed-in Chrome through the `browse` tool.

Use the person's signed-in Chrome through the `browse` tool so existing Google
sessions stay available.

- Write one Playwright step at a time. After each step, read the page (`snapshot()`,
  the URL, a heading).
- Never solve a captcha.
- Use `handoff()` for sign-in, 2FA, passkey, phone codes, and anything involving
  payment or tax details.
- Do not raise or reorder the person's windows.
- Close every tab you open and delete the browse session when you finish.

## Troubleshooting

**Observed:** the rows below match failures from the 2026-11-14 AdSense setup run
and from **Documented, verify** publisher help articles.

| Symptom | Likely cause | What to do |
| --- | --- | --- |
| **Let's go** does nothing | Automated click ignored | Hand off to the person, or retry in a fresh session |
| Verify cannot find the tag | Cached home page, tag only on inner pages, or wrong deploy environment | Purge cache, put proof on the canonical home URL, redeploy production |
| `ads.txt` not found | 404, wrong path, or redirect | Serve `/ads.txt` on the apex with status 200 and no cross-domain redirect |
| `ads.txt` wrong content type | Host serves HTML or JSON | Force `text/plain` for `/ads.txt` |
| Account deactivated | Long inactivity | Use **Reactivate account**, then continue site setup |
| Site rejected: low value content | Thin or duplicate pages | Add substantive content, wait, request review again |
| Payments blocked | Missing tax info or address PIN | Complete Payments settings; hand off for tax and PIN mail |

## What to record afterward

**Observed:** a short private ledger prevents duplicate site submissions and speeds
up re-review after a rejection.

In private project notes only (not in this repository), record:

- Publisher id (`ca-pub-0000000000000000` placeholder format in docs; use the real
  id locally).
- Date each site was added.
- Current site status.
- Any rejection reason and the fix you applied.