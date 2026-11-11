---
name: ad-test-launch
description: "Use when launching a small paid-social test (a few hundred dollars or less) for a service or product and you need the whole path: research the category's ads, model cost and allowable CAC, write persona hypotheses, build UTMs and per-persona landing pages, render static creatives, create the platform objects paused, and gate going live. Covers what a tiny budget can and cannot prove, the targeting-floor and default-geo traps, lifetime budgets and flight dates, and a read-out. Meta first; the method holds for other platforms."
---

# ad-test-launch

A runbook for a small paid-social test, from research to read-out. It sequences
other skills and adds what they do not cover: sizing, structure, platform setup
and the go-live gate. Pairs with `ad-experiments` (method), `ad-landing-tracking`
(click ids, UTMs, first-touch), `ad-research-to-creative` (turning research into
creative), `ad-creative-templates` (rendering), `ads-meta` (pixel and server events)
and `ad-auto-optimizer` (running it).

The tools: `ad-creatives-render` renders static creatives from a spec.
`meta-ad-test` creates the Meta objects paused from a plan file, then activates
or pauses them.

## 0. Decide what the budget can read

Do this before anything else. It sets the whole design.

- At about 2.70 per click, 100 buys about 37 clicks. Expect under one form
  submit. Zero submits is the most likely single outcome. That is not a failure.
- A small test reads click cost, click-through and landing-page loss. It does
  not read a conversion rate. Telling a 2.6% submit rate from 1.0% needs about
  1,000 landing views per arm.
- A conversion objective needs about 50 events per ad set per week. At this size
  use the traffic objective and count conversions on your own server.
- Write the pass, marginal and fail thresholds for spend delivered, cost per
  click, click-through, click-to-view loss and landing views before you spend.

## 1. Research the category's ads

1. Search the platform's public ad library through a scraper or a data proxy.
   Keyword search matches ad body text, so it returns noise. Look up known
   advertiser pages by id instead, and discover them from the noise.
2. In a B2B niche, expect the direct competitors to run no ads. Then widen to
   the advertisers who sell to the same buyer's customers.
3. Record per advertiser: formats, hooks, call to action, landing page, UTM
   habits. Count by format. Save a few creatives locally.
4. Write down the white space: the audience nobody addresses. In a test with a
   thin audience, that is the angle.
5. Cap scraper spend. A pass costs well under 5 in credit. Never save a key.

## 2. Model cost and allowable CAC

- Build a funnel table with pessimistic, base and optimistic columns: CPM, CTR,
  clicks, landing views, submit rate, qualified rate, closed rate. Mark every
  figure SOURCED (with URL and year) or ASSUMPTION.
- Use B2B benchmarks for cold audiences, not the flattering vertical medians.
  Medians for lead forms fall inside a year and often disagree with their own
  CPC and conversion rate. Cross-check them.
- Allowable CAC is gross profit per client over a year, divided by 3.
  Gross profit per case is margin minus the labour and infrastructure to
  deliver it. Label unverified internal figures as such.
- State the stage gates: a small first stage, a second sized to read
  creative and audience, a third sized to read a submit rate. Add a stop rule.

## 3. Structure

One campaign, one ad set, one ad per persona. More ad sets split a small budget
into cells with under 15 clicks each. Use a lifetime budget with an end date so
the platform cannot spend past the cap. Limit placements to the feeds in the
creative's native ratio.

## 4. Personas and hypotheses

Write one line per ad before it runs:

> `<persona>` in `<geo>` will click `<angle>` at `<CTR>` and `<CPC>`, and submit
> at `<rate>` of landing views. Stop if `<kill gate>`.

Give each ad a kill gate, for example "stop at 20 spent with fewer than 4 link
clicks". Keep the personas, hypotheses, copy, expected metrics and links in one
plan file. Generate everything else from it.

## 5. Targeting

- Job-title audiences in a single region can fall under the platform's
  reporting floor (1,000 people on Meta). Check the delivery estimate before
  you build on a title. A hard filter at that size saturates in a day.
- Use titles as audience suggestions with the platform's automatic audience on,
  or widen the region. Put the persona in the ad's first words so the copy
  filters the people the targeting cannot.
- Detailed-targeting exclusions are gone on new Meta campaigns. Location, age,
  language and custom-audience exclusions remain.
- Do not upload a customer or prospect list as a seed without the owner's
  explicit approval. It sends personal data to a third party.
- Health and sensitive-service ads must not state or imply the viewer has a
  condition. Write about the service and the professional buyer.

## 6. Landing pages and UTMs

Follow `ad-landing-tracking`. Test-specific rules:

- One page per persona. The ad, the page headline and the form say the same thing.
- Put the form on the landing page. A second page drops the query string.
  When the form reads the URL's query, the UTMs reach the lead row even when the
  visitor declines cookies. The pixel and click ids still need consent.
- Keep the pages out of the index and the sitemap.
- Taxonomy: `utm_source` is the platform, `utm_medium` is `paid_social`,
  `utm_campaign` is `<site>_<yymm>_<geo>_<test>`, `utm_content` is the ad id,
  `utm_term` is the persona. Lowercase, underscores. Add the platform's own ids
  through its macros so site rows join to platform rows. On Meta, set the whole
  string in the creative's `url_tags`.
- Never put a name, an email or a case detail in a UTM.

## 7. Creatives

- Template text, UI and logo-heavy creatives (`ad-creative-templates`). Do not
  let an image model draw words.
- Use only claims the site already makes. No superlatives, no figures without a
  source, no testimonials, no head counts. Mock UIs show roles, not made-up names.
- Check the render, not the template. Tight display-font tracking runs words
  together. A headline that says "name" must show names.
- Render the story ratio with the platform's safe zones: leave about 250 px at
  the top and 340 px at the bottom free of text and buttons.
- Build more creatives than you launch. Keep the rest as the next stage's tests.

## 8. Create the objects paused

- Run the plan's dry run first. It prints payloads and sends nothing.
- Create everything PAUSED. Roll back the campaign if any step fails.
- Set the flight dates when you go live, not when you create. A paused ad set
  keeps its end date, so a late start shortens the flight.
- Opt out of creative enhancements when copy is regulated. Otherwise the
  platform may rewrite the words.
- Refuse a plan with no geo, no lifetime cap or no hypothesis. A tool that
  defaults the geo to another country spends money in the wrong place.
- Set the Page, pixel and account from the environment. Never print a token.

## 9. Go-live gate

1. Every landing page answers 200 on production. A merge to a staging branch
   does not ship it.
2. A form submit stores the UTMs. Test it once with a fake lead.
3. The owner approves the spend in words, for this test.
4. Activate with the approval flag. Do not edit the ad set mid-flight: each
   significant edit restarts learning.
5. Check delivery after a day. Pause an ad at its kill gate.

## 10. Read-out

Report impressions, reach, frequency, CPM, link clicks, CTR, CPC, landing views,
click-to-view loss, form starts and submits. Join platform rows to server rows by
the UTM and the ad id. Check each submit by hand for fit. Compare to the
thresholds from step 0. Then apply the levers in order: creative, audience,
landing page, offer, bidding.
