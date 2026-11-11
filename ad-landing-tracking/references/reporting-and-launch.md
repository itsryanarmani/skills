# Reporting, safety and launch

## Reading results

- Optimize for cost per paid conversion. Use a free signup as the early signal and a purchase as the final goal. Signup gives volume sooner. Purchase gives truth.
- Model an experiment as one hypothesis plus one arm per variant. Record the outcome (confirmed or not, and why) and the next hypothesis.
- Read arm metrics from the platform at read time. Do not store a second copy. A copy drifts.
- Take revenue from your payment or analytics source. A platform's conversion value is a proxy.
- Keep unknown different from zero. Use a null count when a stage was not measured. A false zero looks like a real result.
- Do not overwrite a good report with a blank one when every row failed to measure. The last good snapshot beats an empty one.
- Put all channels on the same metric window before you compare them. Print the window in each proposal. A 30-day number against a lifetime number picks the wrong winner.
- Clamp the end date of the current week to today. Mark that week partial. A future end date can fail or return empty, and a partial week looks low.
- Cap parallel reads on the analytics API. The GA4 Data API allows about 10 concurrent requests per property.
- Name a winner only with a minimum spend, a minimum number of conversions and a minimum return on spend. Name a loser only with enough spend and either zero conversions or a low return. These are floors, not a significance test.
- Test that each metrics reader returns every field the decision needs. One reader that cannot compute return would make every arm a loser.
- Use an exhaustive `switch` over channels when you build action payloads. A missed branch once sent the wrong field name for one channel.

## After volume exists

- Once volume exists, set the ad set goal to the conversion your server API already sends. Do not leave it on clicks or page views.
- Build a retargeting audience from site visitors. Build an upsell audience from free users minus paid users. They are cheap and high intent.

## Approval and spend

- Make every spend or upload script a dry run by default. Require a typed confirmation value to run for real. Print counts: scanned, skipped, would upload.
- Launch real spend only from a script a person runs. Never from cron or CI.
- Create each ad paused. Read back targeting, link and budget. Compare with your plan. Activate only if all match.
- Let a loop propose actions. A human approves. Claim each approved action inside one database transaction before it runs, so two approvals cannot both spend.
- Get owner and policy approval before a page goes on a launchable ad. Get legal approval for claims, prices, guarantees and comparisons.
- Block a page from a live ad while it is draft, rejected, archived or changed since approval.
- When you build a Reddit login flow, request a permanent token. Use HTTP Basic auth on the token exchange. Without both, no refresh token is issued and the exchange is rejected.
