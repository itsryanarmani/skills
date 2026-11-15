---
name: adsense-site-setup
description: "Create or reactivate Google AdSense, connect a live site with meta tag and ads.txt proof, run adsense-check (or a manual fetch) before Verify, and request review with consent-gated slots only after approval; use when the account is new, dormant, or missing the domain."
---

# adsense-site-setup

You use this skill when a production site should earn display-ad income through
Google AdSense and the publisher account is missing, dormant, or not yet linked
to that domain. You finish with ownership proof deployed, review requested, and
a clear record of site status in private project notes.

Facts below are **Observed** (from a signed-in session on 2026-11-14) or
**Documented, verify** (from Google's published behavior; confirm in the live
UI before you rely on them). **Our rule** marks fleet policy, not a Google fact.

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
- **Our rule:** never load an ad script before consent.

## Check whether an account already exists

1. **Documented, verify:** open the AdSense start flow, choose **Get started**, and
   read the Google account chooser; several accounts can appear, so pick the one
   that should receive payments.
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

**Our rule:** payment, tax, and phone decisions are the owner's alone. Use
`handoff()` (see **Driving the browser**) before any tax form, bank detail, or
SMS PIN entry.

## Add the site

1. **Documented, verify:** on the onboarding **Sites** card or in **Sites**, choose
   **Add site**.
2. **Observed:** the dialog has one **Website** field and **Save**. Enter the bare
   domain (`example.com`) with no `https://` prefix.
3. **Observed:** after save, the domain appears in a site selector at the top of
   the home page.
4. **Documented, verify:** add the apex domain; check whether a subdomain needs
   its own entry before you rely on one listing for all hosts.

## Connect the site (ownership proof)

1. **Documented, verify:** on the onboarding **Sites** card, press **Let's go** to
   open the site detail page.
2. **Observed:** in one automated session, **Let's go** did not respond to a
   role-based click or a coordinate click. In a fresh session, scrolling the
   button into view and clicking with **force** worked on the first try. Try a
   fresh session, scroll into view, then a forced click. If it still does nothing,
   hand off to the person.
3. **Observed:** the site detail page shows the site name, a status chip
   **Requires review**, a **Delete site** button, and the line **Your site needs
   review**.
4. **Observed:** the **Verify site ownership** section has **Select verification
   method** and three radio options in this order:
   - **AdSense code snippet** (selected by default)
   - **Ads.txt snippet**
   - **Meta tag**

**Our rule:** prefer meta tag and `ads.txt` together before approval. Avoid the
AdSense code snippet until the site is approved, because it loads ad script and may
conflict with your consent rule.

5. **Observed:** **AdSense code snippet** shows a script tag to paste between the
   `head` tags on each page, a **Copy** link, a checkbox **I've placed the
   code**, and a **Verify** button:

```html
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-0000000000000000" crossorigin="anonymous"></script>
```

6. **Observed:** **Meta tag** shows a meta element to paste between the `head` tags
   on each page, **Copy**, checkbox **I've placed the HTML meta tag**, and
   **Verify**:

```html
<meta name="google-adsense-account" content="ca-pub-0000000000000000">
```

7. **Observed:** **Ads.txt snippet** shows the line below for the site root
   `ads.txt` file (if a file already exists, paste the line into each file),
   **Copy**, checkbox **I've published the ads.txt file**, and **Verify**:

```text
google.com, pub-0000000000000000, DIRECT, f08c47fec0942fa0
```

8. **Observed:** below verification, a collapsed **Request review** step appears on
   the site detail page.

**Our rule:** deploy meta tag and `ads.txt` on production before you tick the
checkboxes in the UI. Serve `/ads.txt` with HTTP 200, `Content-Type: text/plain`,
and no redirect to another host.

## Check the site before you press Verify

**Observed:** each verification method shows a confirmation checkbox and a
**Verify** button.

**Documented, verify:** Google runs the ownership check only after you tick the
checkbox and press **Verify**.

Before you tick and press **Verify** in the UI, run the companion `adsense-check`
script from the scripts repository against production when it is published:

```bash
adsense-check <domain> <publisher-id>
```

Until that script is published, check by hand: fetch `/ads.txt` and the home page
and compare them to the formats above (status code, `text/plain` for `ads.txt`, meta
tag in `<head>`).

**Observed:** on the sites list, a newly added site can show **Approval status**
**Requires review** and **Ads.txt status** **Not found** before you publish
`ads.txt`.

## Request review and wait

1. **Documented, verify:** after ownership **Verify** succeeds, open the collapsed
   **Request review** step on the site detail page and submit the review request.
2. **Observed:** the sites table lists columns **Site URL**, **Approval status**,
   **Status details**, **Ads.txt status**, **Last updated**, and **Action**. Filter
   chips include **Ready**, **Getting ready**, **Requires review**, and **Needs
   attention**.
3. **Documented, verify:** what happens immediately after **Verify** succeeds, the
   **Request review** form fields, how long review takes, and typical rejection
   reasons were not captured in the 2026-11-14 session. Confirm in the live UI
   before you quote timing or outcomes.
4. **Our rule:** do not add ad slots while the site is under review.

## If the site is rejected

1. **Documented, verify:** read the reason on the **Sites** page.
2. **Documented, verify:** common reasons include low value or thin content, site
   down or unreachable, navigation problems, duplicate or scraped content, policy
   violations, or site not ready.
3. **Documented, verify:** fix the underlying cause, then request review again.
4. **Our rule:** record the rejection reason in private project notes. Thin
   directory sites with many near-empty pages are at higher risk; improve the
   strongest content section first.

Approval timing and earnings are not guaranteed. Do not state an outcome as fact.

## After approval

- **Our rule:** add ad slots only through a consent-gated component that renders
  nothing before consent and reserves height to limit layout shift.
- **Our rule:** do not show ads on private or signed-in-only pages.
- **Documented, verify:** never click your own ads or ask others to; invalid
  traffic can lead to account closure.
- **Our rule:** block scrapers and headless crawlers at the edge where you can, so
  invalid traffic is less likely to count against the account.

## Driving the browser

The `browse` tool drives the person's signed-in Chrome through a browser
extension. `handoff()` pauses automation so the person can finish sign-in, 2FA, or
payment steps. `snapshot()` returns an accessibility tree you read before the next
action.

Use the person's signed-in Chrome through `browse` so existing Google sessions stay
available.

- Write one Playwright step at a time. After each step, read the page (`snapshot()`,
  the URL, a heading).
- Never solve a captcha.
- Use `handoff()` for sign-in, 2FA, passkey, phone codes, and anything involving
  payment or tax details.
- Do not raise or reorder the person's windows.
- Close every tab you open and delete the browse session when you finish.

## Troubleshooting

The **Let's go** row is **Observed**; other rows are **Documented, verify**.

| Symptom | Likely cause | What to do |
| --- | --- | --- |
| **Let's go** does nothing | Stale session or click before scroll | Fresh browse session, scroll into view, forced click; hand off if it still fails |
| Verify cannot find the tag | Cached home page, tag only on inner pages, or wrong deploy environment | Purge cache, put proof on the canonical home URL, redeploy production |
| `ads.txt` not found | 404, wrong path, or redirect | Serve `/ads.txt` on the apex with status 200 and no cross-domain redirect |
| `ads.txt` wrong content type | Host serves HTML or JSON | Force `text/plain` for `/ads.txt` |
| Account deactivated | Long inactivity | Use **Reactivate account**, then continue site setup |
| Site rejected: low value content | Thin or duplicate pages | Add substantive content, wait, request review again |
| Payments blocked | Missing tax info or address PIN | Complete Payments settings; hand off for tax and PIN mail |

## What to record afterward

**Our rule:** keep a short private ledger of publisher id, dates, and status so you
do not double-submit sites and you can retry review with context.

In private project notes only (not in this repository), record:

- Publisher id (`ca-pub-0000000000000000` placeholder format in docs; use the real
  id locally).
- Date each site was added.
- Current site status.
- Any rejection reason and the fix you applied.