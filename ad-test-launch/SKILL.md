---
name: ad-test-launch
description: "Use when launching a small paid-social test (a few hundred dollars or less) for a service or product and you need the whole path: research the category's ads, model cost and allowable CAC, write persona hypotheses, build UTMs and per-persona landing pages, render static creatives, create the platform objects paused, and gate going live. Covers what a tiny budget can and cannot prove, the targeting-floor and default-geo traps, lifetime budgets and flight dates, monitoring a live test with verdicts and a kill gate, an experiment log, and a read-out. Meta first; the method holds for other platforms."
---

# ad-test-launch

A runbook for a small paid-social test, from research to read-out. It sequences
other skills and adds what they do not cover: sizing, structure, platform setup
and the go-live gate. Pairs with `ad-experiments` (method), `ad-landing-tracking`
(click ids, UTMs, first-touch), `ad-research-to-creative` (turning research into
creative), `ad-creative-templates` (rendering), `ads-meta` (pixel and server events)
and `ad-auto-optimizer` (running it).

The tools: `ad-creatives-render` renders static creatives from a spec.
`meta-ad-test` creates the Meta objects paused from a plan file, then activates,
pauses or reports on them. Run either with no arguments to read its usage.

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
5. Cap scraper spend before you start: set a currency, a maximum charge and a
   request limit. A pass costs well under 5 in credit. Never save a key.

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

Start each hypothesis from the trigger: the event that makes this buyer need
the service now, and the decision it blocks. Write a table before any copy:
buyer, trigger event, the decision stuck behind it, what the service gives
them, and the hook. Examples of a trigger: a claim stalls and the file
disagrees with the treating doctor, a hearing date is close and the file needs
an expert report, an employee is off work longer than planned. Treat this as a hypothesis to test: an ad
aimed at the trigger ("Disputed claim? Get an independent opinion.") may draw
more of the right clicks than one aimed at the service in general. Attention is short: name the thing, the speed and the
price in a few words, not the process.

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
- A max age of 65 means 65 and older on Meta. Use 64 to stop at 64. With the
  platform's automatic audience on, age is only a hint it may expand past. In
  one live test set to 25-65 with it on, 79% of the spend reached people 65 and
  over, outside the audience the plan named. To hold an age limit, turn the
  automatic audience off and set the max to 64, then read the ad set back to
  confirm, because some platform expansion options can stay on. The trade-off:
  job-title hints then act as a hard filter, so drop them or check the delivery
  estimate first, and let the copy do the filtering.
- An Instagram placement needs an Instagram identity on the Page. With the
  automatic audience on the platform quietly skips Instagram, so a test can run
  for days with no Instagram delivery and no error. Turn the automatic audience
  off and every ad errors ("Page Backed Instagram profile is being created")
  and spend stops. Use Facebook only, or connect an account first.
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
- The page must repeat every claim the ad makes. An ad that promises a speed or
  a price its page never mentions loses trust. Before a
  claim goes live, the owner confirms exactly what it counts (referral to
  appointment, or referral to report) and you hold proof that covers the
  claim's scope, market, conditions and date, for example a dated price
  comparison for a "best price". If you cannot back a comparative claim, leave
  it out. Put the same words on the page. Owner approval is not platform or
  legal approval: check the platform's policies and the local advertising rules
  for the sector (health and legal services are restricted) before it runs.
- Keep the page focused: the logo and one call-to-action button in the header,
  no site menu, no navigation footer. Make it a per-page setting so a page can
  keep the full header when that suits it. Keep what must stay: a form that
  collects personal details needs an accessible privacy policy link beside it,
  so add one line under the form when you remove the footer, and keep any
  disclosure your sector or platform requires.
- Taxonomy: `utm_source` is the platform, `utm_medium` is `paid_social`,
  `utm_campaign` is `<site>_<yymm>_<geo>_<test>`, `utm_content` is the ad id,
  `utm_term` is the persona. Lowercase, underscores. Add the platform's own ids
  through its macros so site rows join to platform rows. On Meta, set the whole
  string in the creative's `url_tags`.
- Never put a name, an email or a case detail in a UTM.

## 7. Creatives

- Template text, UI and logo-heavy creatives (`ad-creative-templates`). Do not
  let an image model draw words.
- By default use only claims the site already makes: no superlatives, no figures
  without a source, no testimonials, no head counts. An owner may confirm a
  claim such as a turnaround or a best price for the ads. Then keep the proof on
  file and put the claim on the page too (see section 6). Mock UIs show roles,
  not made-up names.
- Write direct creatives that name the service in plain words, with the speed
  and the price as short chips, and one trigger per ad. A process headline
  ("Status is a lookup, not a chase") that never says what the service is fails
  a skimming buyer. Test a changed creative against its twin: same headline
  and page, one change, so the result reads cleanly.
- Photos of people can lift attention, but generated people are unnamed
  illustration, not staff or customers. Show unnamed professionals at work, not
  looking at the camera, with no patient in frame, no name, title, credential
  or "our team" beside a face, and no accreditation badge. Screens and papers
  angled away so no text reads. Check the full-size render for a brand mark on a
  device, a shirt or a bezel, and for garbled text, and regenerate or paint it
  out. Label each creative's people as illustration wherever you show it, and
  check the whole creative does not suggest they are real providers. Set a
  spend cap before you generate: one model cost a fraction of a dollar per image
  in 2026, plus retries.
- Check the render, not the template. Tight display-font tracking runs words
  together. A headline that says "name" must show names.
- Render the story ratio with the platform's safe zones: leave about 250 px at
  the top and 340 px at the bottom free of text and buttons.
- Build more creatives than you launch. Keep the rest as the next stage's tests.
- Do not name or imply the viewer's personal hardship, such as debt, a lost
  home or a health problem. Write about the offer. Platforms reject it, and it
  targets people at a weak moment.
- Quote every claim from a source the site already cites, or from proof the
  owner holds for a claim they confirmed. Keep the source or the proof note in
  the plan next to the line.
- Have a separate reviewer read the copy and the code diff. It ranks findings
  by severity and lists what it could not verify. The author does not review
  their own work.

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
- Follow the tool rules in [launch-tooling.md](references/launch-tooling.md):
  rate-limit backoff, duplicate guard, full read-back, `python3 -I`.
- Check the Meta API traps in [meta-api-traps.md](references/meta-api-traps.md)
  before the first create: budget sharing, Instagram identity, special ad
  categories, account currency, Page access.

## 9. Go-live gate

1. Every landing page answers 200 on production. A merge to a staging branch
   does not ship it.
2. A form submit stores the UTMs. Test it once with a fake lead.
3. Run the Page polish (`fb-page-polish`) before the first ad. People tap the
   Page name before they click. Hide the two auto-posts. Post three starter
   posts as the Page, then count them on the Page to prove they went up. See
   `local-business-profiles`, page-trust.md, sections 6 to 8.
4. The owner approves the spend in words, for this test.
5. Activate with the approval flag. Do not edit the ad set mid-flight: each
   significant edit restarts learning.
6. Read the real state back. A success reply from the platform is not proof.
   Ask each object for its effective status. Ads may sit in review for a while.
7. Start the monitor (step 10) the same hour. Pause an ad at its kill gate.
8. The next day, check the platform's event manager. Reports lag by up to a
   day. Until then, say which events are unproven.

Platform traps seen on a first run:

- Meta allows one call per object every 30 seconds. Setting the flight and then
  the status on the same ad set in a row fails with a rate-limit error. Wait,
  then retry.
- Meta locks a start time that is under 15 minutes away. Set the flight once
  and keep the saved dates if the lock answers.
- A half-activated test can spend. If any step fails, pause every object again
  and say so. Then read the statuses before you retry.

## Swapping ads on a live test

After the first read you often replace ads. Do it so the test is never
empty and the cap does not change:

- Add the new ads to the same ad set, live. The platform reviews an ad when it
  goes live, and an unreviewed ad does not deliver. The old ads keep running
  meanwhile. The budget stays the same cap and the ads share it.
- Retire the old ads only after every new ad is approved and active. If one new
  ad is rejected, retire nothing and read the reason first.
- `meta-ad-test --add` creates the plan's new ads in the existing ad set and
  `meta-ad-test --retire old --after new` pauses the old ones, refusing until
  the new ones are active. The tool checks status only: the swap itself still
  needs the owner's approval first. Never retire an ad as its own replacement, and never add an ad
  that was already retired.
- Never raise the budget, add an ad set, or edit a live ad to fix a read. A
  swap changes the creatives only.

## 10. Monitor

Do not leave a live test unwatched. Run the tool's report on a schedule: every
three to six hours for the first two days, then daily. It only reads, so it is
safe to automate. Keep the scheduled job's copy of the tool at a stable path
that nothing cleans up. A job that called the tool from a temporary worktree
failed the first time that folder was removed.

The report gives each ad a verdict:

| Verdict | Meaning |
|---|---|
| WAIT | No delivery, or under 1,000 impressions. Say nothing yet. |
| ON TRACK | Click-through is inside the range the plan expected. |
| LEADING | Click-through is above the range. |
| WATCH | Click-through is below the range on enough impressions. |
| KILL | The ad hit its kill gate: spent the stated amount with too few link clicks. |

Rules for acting on it:

- The kill gate is the owner's rule, written in the plan before the spend. The
  tool may pause an ad that hit it, with the explicit apply flag. A gate it
  cannot parse is flagged, never acted on.
- Any change that raises spend, adds an ad set, or edits a live object needs the
  owner. Pausing a failing ad does not.
- With under about 15 clicks per ad, differences in click-through and cost per
  click are noise. Do not call a winner on them.
- Check the first hour: impressions above zero, no ad rejected, spend moving.
- Read delivery by age and by placement in the first hours, not only by ad.
  Compare it with the plan. If most of the spend reached people outside the
  audience the plan named, click-through from that group says little about the
  audience you meant to reach, so fix the audience before you judge a creative.
  Where you can, judge on qualified leads, not clicks. `meta-ad-test --report`
  prints the share of impressions in age bands wholly outside the live range,
  a lower bound, and warns above 20%.
- After any targeting change, count only whole days after it. That report reads
  whole days (`--since DATE`), so the day of the change mixes old and new
  delivery. Use an hourly breakdown if you need to cut the day.
- After an edit, read each ad's status and its issue text, not just whether the
  call succeeded. A successful edit can leave every ad erroring and spend at
  zero.

## 11. Experiment log and the optimise loop

Each ad is an experiment. Keep one record per ad in the plan: the hypothesis,
the expected range, and after the run an outcome (confirmed, refuted or inconclusive, and why; for inconclusive, say what evidence is missing)
and a next hypothesis. A test that ends without a next hypothesis taught
nothing. The reserve creatives you did not launch are the first candidates.

Run the loop in this order. Change one thing at a time:

1. Creative: keep the leading angle, retire the failing one, test its reserve.
2. Audience: widen or narrow only when click-through differs across audiences
   with enough clicks to read.
3. Landing page: if clicks are fine and landing views are low, fix speed and
   the first screen. If views are fine and submits are low, fix the form.
4. Offer and bidding last. Move to a conversion objective only when you can feed
   it about 50 events per ad set per week.

Cheaper later stages: retarget site visitors who did not submit, then build a
look-alike from your own customers. A customer list sends personal data to a
third party, so it needs the owner's explicit approval.

Report cost per qualified lead, and work out cost per customer from the
referral-to-customer rate before you raise spend. Join platform rows to server
rows by UTM and ad id so each ad has its own funnel.

## 12. Many sites

When one template runs many sites, keep a per-site status table, exclude
restricted sites from batch launches, and follow one readiness order. See
[fleet-readiness.md](references/fleet-readiness.md).

## 13. Read-out

Report impressions, reach, frequency, CPM, link clicks, CTR, CPC, landing views,
click-to-view loss, form starts and submits. Join platform rows to server rows by
the UTM and the ad id. Check each submit by hand for fit. Compare to the
thresholds from step 0. Then apply the levers in order: creative, audience,
landing page, offer, bidding.
