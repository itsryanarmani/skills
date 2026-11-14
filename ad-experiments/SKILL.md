---
name: ad-experiments
description: "Run paid-ad experiments on a small budget so you learn WHICH variable drives signups and WHY — hyper-specific one-audience×one-geo×one-creative experiments driven by a written hypothesis, proving the cheapest measurable conversion (free signup) before the expensive one (paid), and judging results on server-side truth reconciled against payment-provider ground truth rather than dashboard vanity metrics. Also covers sizing the budget to the metric you can actually read (a $50 test reads CPC/CTR, not a conversion rate), a controlled UTM taxonomy for landing-page attribution, seeding platform lookalikes from your own hashed-email user list (minimum sizes, match-loss, graceful under-size handling), and the human-authorization boundary around exporting user PII to an ad network. Platform-agnostic methodology that pairs with the ads-google, ads-meta, and ads-reddit tracking/setup skills. Use when planning a paid-ad test, structuring ad experiments, sizing a budget, building a lookalike/seed audience, or deciding what to measure and how to read the result."
---

# ad-experiments

How to run paid-ad experiments on a small budget so you learn *which* variable drives signups and *why*, instead of dumping the budget into one broad campaign and reading a dashboard. Platform-agnostic — pairs with the `ads-google`, `ads-meta`, and `ads-reddit` skills, which cover the tracking and campaign setup for each channel.

## Run hyper-specific experiments

- Test **one narrow audience × one geo × one creative per experiment** (e.g. "photographers in `<city>`", "restaurants in `<city>`") — not a broad "everyone, everywhere" campaign. A broad campaign averages every variable together, so a win or loss tells you nothing about *why*; a narrow experiment isolates the one thing that moved.
- Each experiment starts from a **written hypothesis** ("`<this audience>` in `<this geo>` will sign up from `<this angle>`"), tunes its settings deliberately to test that hypothesis, and measures against a **denominator** — clicks → signups, not raw impressions or spend.
- **Keep the winners, kill the losers, iterate.** The point of narrowness is a clean attribution of cause: feed what won into the next round and vary one more thing.

## Prove the cheapest conversion first

- Optimize toward the **cheapest measurable conversion** (a free signup) before you optimize toward the expensive one (a paid subscription). A small budget can produce enough free signups to read a funnel; it usually can't produce enough paid conversions to learn anything from.
- This also matches the bidding reality: conversion-optimized delivery needs conversion *volume* to work (Google Smart Bidding, Meta's learning phase, Reddit's conversion optimization all need conversions to learn — see the per-platform skills), and the cheap conversion is the one you can actually generate enough of.

## Verify against server-side truth

- Judge an experiment on **server-side conversions** (GA4 / the platform's own server-side event counts) reconciled against **payment-provider ground truth** — actual succeeded charges or created accounts — never dashboard vanity metrics alone. Ad dashboards over-report; your payment provider and your own database don't.
- A conversion count of **0 over a window that predates your tracking deploy** is expected, not a result. Check the deploy date before drawing any conclusion.

## The learning arc — where the lever actually is

Run experiments in this order; each stage tells you where the *next* bottleneck lives:

1. **Cold targeting rarely reads.** Cold interest/keyword targeting on a small budget gives thin CTR and usually 0 measurable signups — not enough signal to conclude anything. Don't keep feeding a cold campaign hoping it warms up; it won't at this budget.
2. **Warm lookalike fixes engagement.** Build a lookalike seeded off your *highest-value existing users* and it typically delivers **4–5× the CTR at a lower CPC** than cold. If your problem was clicks, this solves it.
3. **Then the bottleneck moves downstream.** Warm, engaged traffic can still convert to **0 signups** — which means the problem was never the audience, it's the **message and the landing page**. Say it plainly: once warm CTR is healthy, *targeting is solved; conversion is the lever.* Stop tuning audiences and start testing messages/LPs.

Most wasted ad spend comes from tuning the stage you already solved. Diagnose which stage you're in before spending.

## Isolate one variable — the message test

- To test **message/angle**, hold the audience **constant** (same lookalike) and vary **only** the creative angle, each pointing at its **own dedicated landing page** built for that angle. Tag every angle with distinct UTMs and read per-ad breakdown so attribution is clean. Changing audience *and* message at once tells you nothing about which moved the result.
- Swapping a creative to iterate: do it while spend is still ~0 so you don't discard a learning read.

## Truthfulness gate (do this BEFORE writing any angle)

- **Audit what the product actually does before you write copy.** Never advertise a capability the product lacks — it's false advertising even when it's beautiful market whitespace, and it tanks conversion when the click meets a page that can't deliver.
- The winning angle is the intersection: **(competitor-message whitespace) ∩ (what you can truthfully deliver).** A market-gap tool may surface "analytics dashboard" or "online store" as gaps, but if the product only *connects a third-party analytics tag* or only *embeds a third-party store*, those angles are OUT — pick something real.

## Competitor-intel loop (finds the angle)

- Scrape competitors' live ads from the platform's public ad library, and extract each ad's **angle / promise / outcome**. Where **everyone says the same thing** (e.g. "AI builds your site, fast, cheap") you've found message saturation — sameness is why nobody's click is *yours*.
- Your opening is a **differentiated, truthful** angle no one else runs. A **brand/trust differentiator a competitor structurally cannot copy** (who you're made by, a privacy stance) is the strongest kind, because it's not a feature they can ship next sprint.

## Spend discipline

- **Feasibility-test an unproven platform cheap first** (a ~$50 "does it even serve and get clicks" run) before committing real budget — especially one with a fragile audience-upload path.
- **Set hard per-platform caps.** Where a platform's *campaign* budget floor is high, cap at the *ad-group* level instead (see `ads-reddit`).
- **Scale the winner, not the average.** Once one angle/arm wins, put budget there — don't keep spending equally across the losers to "be fair" to them.
- **Kill-gate:** pause an ad/arm when **(spend ≥ threshold) AND (CTR < floor)** (e.g. spent ≥ $30 and CTR < 0.5%). Wire it into a monitor, don't eyeball it.
## Size the budget to the metric you're actually reading

- A small ($50-scale) test buys a **CPC/CTR read, not a conversion rate.** A readable conversion/signup rate needs ~**25-30 conversion events** — often **$300-750 per arm** depending on CPC. Budgeting $50 and expecting a signup-rate answer is the most common way a test produces nothing readable: size the budget to the metric you're trying to read.
- Add **kill-gates**: cut an arm at ~50% of its planned spend if its CPC/CTR is ~2x worse than the best arm — don't let a clear loser burn its full budget before you react.

## UTM taxonomy for landing-page attribution

A controlled vocabulary so every lead is machine-parseable and experiments stay comparable:

- `utm_source` = platform, `utm_medium` = channel, `utm_campaign` = `{exp}_{platform}_{vertical}_{geo}`, `utm_content` = `{creative}_{angle}_{format}`, `utm_term` = `{targeting}`.
- Also capture the platform click ids (`gclid` / `fbclid` / `rdt_cid`) and an `lp_variant` param.
- **Store both the raw query string and the parsed fields on the lead** — raw is your audit trail when the taxonomy changes underneath you.
- **Move one dimension per experiment against a baseline.** Never grid-search the whole combinatorial space — you can't afford the arms and can't attribute the win.

## Seed lookalikes from your own users

You can't build a platform "lookalike" from nothing — you upload a seed list of your own users (hashed emails) and the platform finds similar people.

- **Meta** = Custom Audience → Lookalike. **Google** = Customer Match list + optimized targeting / value-based Smart Bidding (Google's classic "similar audiences" was deprecated, so there is no lookalike *object* — expansion is a bidding behavior). **Reddit has no usable email-match audience product — skip it for lookalikes.** Per-platform wiring lives in `ads-meta` / `ads-google`; the methodology is here.
- **Hash every email identically before upload: trim → lowercase → SHA-256 hex.** Mismatched normalization silently tanks the match rate.
- **Minimum sizes gate serving, and match loss shrinks your seed below its raw count.** Meta needs ≥100 *matched* users (a raw seed near 100 usually fails after a ~50-70% match rate); Google Customer Match needs ~1,000 members to serve. A tiny high-value seed (paying customers only) is often too small to serve at all — a larger high-intent segment (signups, trials) is the better practical seed. Size the seed to clear the floor *after* match loss.
- **Handle under-size per-segment, never abort the run.** Create the audience anyway, catch the lookalike/serve rejection as a per-segment warning, and keep going — one small segment must not abort a multi-segment upload.

## Exporting user PII to an ad network is a human-authorization boundary

Seeding a lookalike sends your customers' (hashed) emails to a third party, and it may require opening a data path in prod. Treat that as a human decision, not an automated one:

- **Build the machinery inert** — an empty seed produces zero outbound calls — and expose a **human-run one-off trigger script** for the actual export. Never wire the export into an endpoint, cron, or startup path.
- If the ad-ops service must read your product's user warehouse to build the seed, grant **least-privilege and cross-project**: dataset-level READER on the source warehouse + a job-runner role on the consumer's *own* project. A project-wide grant is more access than the job needs.

See the per-platform skills for wiring up that server-side tracking and campaign setup: `ads-google`, `ads-meta`, `ads-reddit`.

## Ranked Meta ad formats — cross-reference
For the 12 ranked formats, ROAS ranking table, WaveSpeed model picks, and creative rules, see [`ad-creative-templates/impulse-formats.md`](../ad-creative-templates/impulse-formats.md). That shared reference contains the launch-first rotation rule (first wave: Notes, iMessage, blurred guide screenshot + lo-fi UGC selfie; first swaps: us-vs-them and whiteboard; second wave: Zack D and stickman). Kill gate from `impulse-formats.md` §2: judge on CTR, CPC, and landing-page views; do not claim ROAS winner until Stripe purchases or verified leads exist. If CTR healthy and sales/leads zero, stop swapping formats and fix the landing page. Budget sizing: $50 test reads CPC/CTR, not ROAS (needs ~25-30 conversions, often $300-750 per arm).
