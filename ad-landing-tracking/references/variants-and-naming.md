# Variant pages and naming

## Variant pages

- Serve each variant at a stable path slug. Fix the slug after the first publish. Live ad URLs must never break.
- Resolve the page by slug, not by campaign id. Carry the arm in `utm_campaign`, `utm_content` and a `variant` param. The path survives a campaign rename. The params do the attributing.
- Use one slug and one campaign tag per arm. Give each arm its own audience, creative, page and UTM set. Cost per conversion then reads per arm with no join.
- Resolve an ad's destination in this order: the ad's approved variant URL, then the campaign default. Old ads keep working with no migration.
- Ship one fixed template first. Prove the data model. Add template choice later.
- To test a hero, keep the copy identical and change one element. Then the result has one cause.
- After approval, any edit to copy, links or experiment fields cancels the approval. Hash the approved content as a snapshot. Report results by snapshot period, so a mid-flight edit does not taint earlier data.

## Copy tokens

- Personalize with tokens such as `{{utm_content}}`. Run one substitution pass over every text field, not only the headline. A half-personalized page breaks message match.
- Never show an unresolved token. Replace it with an empty string or a default.
- Clean free-value tokens such as industry, location or offer before render. Strip control characters, collapse spaces, cap near 80 characters. The value comes straight from the URL.
- Build the token pattern from the token lists. Do not keep a second typed list. A new token then cannot be added in one place and missed in the other.
- Keep the editable fields narrow: headline, subhead, CTA label, proof points, objections, legal note, hero image. Block raw HTML and customer scripts until you have a vetted allowlist.
- Pick a hero image from a token with a curated map. Fall back to the static hero. Put a timeout and a rate limit on any generated image.

## Page content

- Make the headline echo the ad. Keep one primary action.
- Use an inline form with a clear CTA mode. Fire a tracked event on submit. The lead is then captured with its attribution.
- Add proof points, an objections list and one trust line.
- Normalize a visitor-typed website at the trust boundary. Allow only `http` or `https`. Reject user info and hosts without a dot. Never store the raw value.

## Indexing and caching

- Send `noindex` as a response header and in page metadata on every ad page. Ad pages are thin and near copies, and they should not compete with your main pages in search.
- Send `no-store` and `noindex` on preview routes. Do not record conversions in preview.
- Keep published page assets cacheable.

## Naming

| Field | Pattern | Made-up example |
|---|---|---|
| `utm_source` | the platform | `meta` |
| `utm_medium` | the traffic type | `paid_social` |
| `utm_campaign` | `{experiment}_{platform}_{vertical}_{geo}` | `e07_meta_bakery_uk` |
| `utm_content` | `{creative}_{angle}_{format}` | `fieldnotes_savings_video` |
| `utm_term` | the audience seed | `lookalike_buyers` |

- Use lowercase words with underscores. One spelling means one row in every report.
- Parse `utm_campaign` and `utm_content` loosely. Never reject a tag that does not parse. Keep the raw string. Old tags still work.
- Make one experiment one themed campaign. Make each angle one ad group with a short label. This matches how platforms report.
- Use `utm_campaign` from the final URL as the report join key. Fall back to the campaign name.
