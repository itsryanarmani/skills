---
name: ad-landing-tracking
description: "Track a paid ad click from landing page to payment: click-id and UTM allowlist, first-touch cookie, ids carried through checkout into payment metadata, one shared event id for browser and server dedup, variant pages keyed by a fixed slug, UTM naming, safe reports, dry-run spend scripts, and a paused-first launch. Use when you build or audit ad landing pages, attribution capture, or a small paid test, and conversions do not match clicks."
---

# ad-landing-tracking

Capture every click id once, keep it until the sale, and send it back to the ad platform with one shared event id.

This skill covers the page and the pipe. For the event taxonomy and platform adapters, use [ad-conversion-hub](../ad-conversion-hub/SKILL.md). For hypothesis design and budgets, use [ad-experiments](../ad-experiments/SKILL.md).

## Use it when

- You build a landing page for paid traffic.
- Platform conversions are lower than your own counts.
- You add a variant page or a new platform to a working setup.

Do not use it to pick a platform or write ad copy.

## Rules that never bend

- Allowlist the params you keep. Drop the rest.
- Write the cookie on the first touch and on new params only.
- Read ids at the purchase click. Do not stamp them at signup.
- Use one event id in the browser and on the server. Make it once.
- Show unknown as unknown. Never show it as zero.
- Run every spend or upload script as a dry run first.
- Launch every ad paused. A person activates it.

## Workflow

1. **Capture.** Keep click ids and UTM fields in two lists. Build one allowlist from both. Store the first value per allowlisted param. Never store the raw query string. Details: [identifiers-and-cookies.md](references/identifiers-and-cookies.md).
2. **Carry.** Put the allowlisted params on the CTA link, in storage, and into checkout metadata. Read them back in the payment webhook. Details: same file.
3. **Send.** Make one event id once: derive it from a stable key, or create it in the browser and send it to the server. Use each platform's exact field name. Details: [events-and-dedup.md](references/events-and-dedup.md).
4. **Vary.** Serve each variant at a fixed slug. Put the arm in the UTM fields and a `variant` param. Details: [variants-and-naming.md](references/variants-and-naming.md).
5. **Read.** Use one metric window for all channels. Keep the last good report. Details: [reporting-and-launch.md](references/reporting-and-launch.md).
6. **Launch.** Follow the checklist below.

## Launch checklist for a small test

Stop at the first item that fails.

1. Fire a test event from the browser and one from the server. Use the platform's test id. Confirm both appear and merge into one event.
2. Click a live ad URL. Confirm the cookie holds the click id and the UTM fields.
3. Buy through checkout with a test card. Confirm the webhook reads the click id from the payment metadata.
4. Check the spend cap. Use a lifetime or total cap where the platform has one. Otherwise set a daily budget times the days, with an end date. Also set a hard account spend limit. A daily budget alone is not a cap.
5. Create the ad paused. Read back targeting, link and budget. Compare with your plan. Activate only if all match.
6. Wait for the stop rule's minimum clicks. Do not read results before that.
7. Read the first result on one metric window. Check unknown cells before you read the zeros.

## Failure notes

| Symptom | Likely cause | Fix |
|---|---|---|
| Click id missing after a redirect | The redirect response did not set the cookie | Set the cookie on every response path |
| Events count twice in the platform | Event ids differ, or a field name has the wrong case | Use the shared id and the exact name per side |
| Fast bounces never appear in analytics | First page view fires after hydration | Send it from the inline init script |
| Page shows `{{token}}` | A token had no value | Replace it with a default or empty text |
| Leads vanish with no error | Login check covers the lead API | Exempt the public lead API and test as anonymous |
| Report went blank | Every row failed to measure | Keep the last good report |

## What we could not find

The source review found no sample-size rule, no power analysis, no significance test and no bandit. The only stop rule is a floor on spend, conversions and return. It is not a test of significance.

For measurement design, see the measurement guide when it lands.

Unproven here: page speed budgets, cache lifetimes for ad pages, and any ranking of page structures.
