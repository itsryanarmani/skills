# Measurement

The 54 pages hold no conversion data, so the only way to learn what works for your page is to test it. Change one thing at a time.

## Test setup

1. **One change per test.** Headline, hero image, button label, or page length. Never two. If two change, you cannot say which one moved the result.
2. **One variant per URL parameter.** Serve the same page at one address and switch content on `?v=a` or `?v=b`. Keep the default page equal to `a`. Do not split by time (week one versus week two): the traffic differs.
3. **Split by assignment, not by choice.** Give each visitor one variant at random and keep it for the visit.
4. **Name sources with `utm_content`.** Pattern: `<test>-<variant>`, lowercase, no spaces, for example `hero-a` and `hero-b`. Keep `utm_source` and `utm_medium` for the channel. Write each name in a log before the test starts.
5. **Count one outcome.** For an opt-in page, a completed sign-up. Count it on your server, not in a platform dashboard.
6. **Fix the stop rule first.** Decide the sample per arm before you start. Do not stop early on a good-looking gap.

## Sample size

Per arm: **n ≈ 16·p(1−p) / δ²**

- `p` is your baseline conversion rate (for example 0.20).
- `δ` is the smallest absolute change you care about (for example 0.05).
- The factor 16 gives about 80% power at a 5% significance level for a two-arm comparison. It is a rule of thumb.

| Baseline p | Change δ | n per arm |
|---|---|---|
| 0.20 | 0.05 | 1,024 |
| 0.20 | 0.10 | 256 |
| 0.10 | 0.03 | 1,600 |
| 0.40 | 0.10 | 384 |

Check the arithmetic: 16 × 0.2 × 0.8 / 0.05² = 2.56 / 0.0025 = 1,024.

## What low traffic can and cannot learn

- **Can:** large effects. At p = 0.20 a change of 0.10 needs about 256 visitors per arm. A rewrite that doubles sign-ups shows in a few hundred visits.
- **Can:** whether the page works at all, which tracking events fire, and where visitors drop (use step counts, not rates).
- **Cannot:** small effects. A 1-point change on a 10% page needs thousands of visitors per arm. Do not read it from 200 visits.
- **Cannot:** paid-product conversion on low volume. A paid step has a low rate, so even a large relative lift is a tiny absolute change. Test the free step first.
- **Absolute versus relative.** For a fixed absolute change δ, n rises with p up to 50%: a 2-point change needs 3,600 per arm at p = 10% and 6,400 at p = 20%. For a relative lift r, δ = r·p and n ≈ 16(1−p)/(r²·p), which falls as p rises: a 20% lift needs 3,600 per arm at p = 10% and 1,600 at p = 20%. Say which kind of change you mean before you plan.
- If you cannot reach the sample size in a reasonable time, test a bolder change, not a finer one.
- A single result is a lead, not proof. Repeat a win once before you keep it.

## Log

Keep one line per test: date, change, variant names, `utm_content` values, planned n per arm, outcome, decision.
