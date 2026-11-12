# Running ads across a fleet of sites

Use this when one template runs many sites and any of them can take a paid test.

## Status table

Keep one row per site in a private operations file. Never in a public repo.

| Site | Store live | Free product | Paid product | Page registered | Landing pages live | Restricted |
|---|---|---|---|---|---|---|
| example-sheds | yes | sizing guide | plan pack | yes | 3 of 3 | no |
| example-loans | yes | rate checklist | none | no | 0 of 2 | yes |

- **Store live:** the catalog loads on production.
- **Free product:** the lead magnet the ad offers.
- **Paid product:** what the funnel sells after the lead.
- **Page registered:** the ad platform Page exists and a validate-only creative
  call passes. See [meta-api-traps.md](meta-api-traps.md).
- **Landing pages live:** count of ad pages that answer 200 on production.
- **Restricted:** the offer falls in a special ad category or a sensitive area,
  such as credit, housing, health or employment.

## Restricted sites

- Exclude a restricted site from batch launches by default. The tool skips any
  row with `Restricted: yes`.
- Launch a restricted site only one at a time, with the category declared and
  the copy reviewed against the category rules.

## Readiness order

Do the steps in this order. Stop at the first one that fails.

1. Landing pages answer 200 on production.
2. The Page has a profile photo, cover, bio, website link and category. Run
   `fb-page-polish` first. The auto-posts are hidden, and three starter posts
   from the site's own text show on the Page. See `local-business-profiles`,
   page-trust.md.
3. Dry run of the launch plan. Read every payload.
4. Create everything paused. Read every object back.
5. Live Lead check: one fake sign-up fires the browser and server Lead with one
   event id. See `ad-landing-tracking`.
6. The owner approves the spend. Activate.
7. Next day: check Events Manager for the events and the dedup. Say what is
   still unproven.
