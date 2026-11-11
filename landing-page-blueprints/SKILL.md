---
name: landing-page-blueprints
description: "Pick a landing-page blueprint (webinar sign-up, lead-magnet opt-in, long course sale, event registration) from patterns counted across 54 public creator pages, then adapt it honestly for a small business with no testimonials. Use when planning the structure, length, proof and urgency of a page before design, or when you need benchmarks with sample sizes instead of folklore. Not a conversion guide: the data holds no conversion rates."
---

# landing-page-blueprints

Use this skill to choose a page structure and its length, proof and ask before you design or write copy. It answers "what do pages of this type usually contain?" It does not answer "what converts?" For section anatomy and visual craft, use `landing-page`.

## Source and limits

54 landing pages from the public SwipePages creator gallery (https://swipepages.com/landing-page-inspiration/industry/creator/). Credit SwipePages as the source of the pages. This skill copies no page copy or images.

- Evidence is one full-page desktop screenshot per page. No live page, no mobile view, no clicks, no video, no forms behind buttons.
- 14 of 54 captures have blank or cut areas, and 3 stop at a 23,040 px cap (script count). Their lengths are lower bounds.
- The gallery's own text contradicted the screenshot on 25 of 54 pages (hand count from the batch notes, not script output). This skill trusts the screenshots.
- The pages are about a year old. Word counts are estimates by eye, within about 15-20%.
- There is no conversion data. Everything here is a pattern of what exists, not proof of what converts.
- Claims on the pages (income, student counts, reviews) were recorded, not verified.

## Method

1. Name the one action you want and what the visitor gets for it. Free first step, paid product, or a call.
2. Match it to a funnel type in `references/funnel-types.md`. Types with fewer than 4 pages have no blueprint: do not generalise from them.
3. Start from that type's section order and its benchmarks (median with n). Treat them as a starting range, not a target.
4. Check each section against `references/patterns.md`. Note the counter-examples before you copy a pattern.
5. Choose proof and persuasion with `references/psychology-levers.md`, then apply `references/honest-adaptation.md` to remove anything you cannot back with a fact you can show.
6. Ship one page, then change one thing at a time with `references/measurement.md`.

## Rules

- Copy the structure, never the wording or the images.
- Every claim on your page needs a source a visitor can check. If you cannot show it, cut it.
- No fake scarcity, no countdown timer that resets, no struck-through price you never charged.
- No income or result claims. The data shows these on about half of the pages, and they carry legal and trust risk.
- Cite benchmarks with n. A median of 3 pages is an anecdote.
- Rerun `python3 -I tools/aggregate_teardowns.py --table data/teardown-summary.csv` to recheck the table numbers. The JSON inputs are not shipped, so the lever, section and testimonial counts cannot be rerun from this repo.

## Files

| File | Use |
|---|---|
| `references/funnel-types.md` | One blueprint per type with 4+ pages |
| `references/patterns.md` | 15 numbered patterns, n of 54, counter-examples |
| `references/psychology-levers.md` | Lever, mechanism, risk, honest use |
| `references/honest-adaptation.md` | A small guide business with no testimonials |
| `references/measurement.md` | One-change tests, URL variants, sample size |
| `tools/aggregate_teardowns.py` | Counts and medians (stdlib Python) |
| `data/teardown-summary.csv` | One row per page for the table numbers |
