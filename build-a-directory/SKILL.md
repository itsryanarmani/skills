---
name: build-a-directory
description: "Turn one niche into a monetized, SEO- and GEO-ready listing directory on Cloudflare from a directory template. Covers the niche test (global reach, open data under a lawful licence, a payer, a free tool), a read-only keyword domain check with a hard no-purchase gate, cloning the template and changing only config, data and brand, importing listings behind a thin-content gate, free tools, Stripe tiers, staging on main and production on release, the Google Search Console + Bing + IndexNow launch with the search-console CLI, and the GEO checks with a geoaeo audit. Use when someone asks to 'build a directory', 'start a niche directory', 'launch a listings site', 'pick a directory niche', or 'make a directory for <niche>'. Hands off to the sibling skills that own each stage."
---

# build-a-directory

This skill takes one niche to a live listing directory that earns money and
that search engines and answer engines can find. One template runs many
directories. Each directory changes only three things: its config, its data,
and its brand. If a new directory needs a code change in the app, the change
belongs in the template.

The work runs in nine stages. Do them in order. Each stage has a stop
condition. Do not start the next stage until the current stage passes.

| Stage | Output | Owner of the detail |
|---|---|---|
| 1. Niche | One niche that passes four tests | this skill, then [validate-an-idea](../validate-an-idea/SKILL.md) |
| 2. Domain | A shortlist with prices, no purchase | [cloudflare-domain-launch](../cloudflare-domain-launch/SKILL.md) |
| 3. Clone | A repo with new config, data and brand | [build-from-template](../build-from-template/SKILL.md) |
| 4. Listings | Imported rows with a source and a licence | this skill |
| 5. Free tools | One or more tool pages | [marketing-site](../marketing-site/SKILL.md) |
| 6. Money | Stripe tiers in test mode | [saas-billing-stripe](../saas-billing-stripe/SKILL.md) |
| 7. Environments | Staging on `main`, production on `release` | [branch-deploy-convention](../branch-deploy-convention/SKILL.md) |
| 8. Search launch | Google, Bing and IndexNow have the sitemap | [launch-seo](../launch-seo/SKILL.md) |
| 9. GEO | A passing `geoaeo audit` | [geo-aeo](../geo-aeo/SKILL.md) |

## When not to use it

- The site has no repeated entity with a place, such as a blog or a SaaS
  marketing site. Use [marketing-site](../marketing-site/SKILL.md).
- The only data source is a site whose terms forbid copying. Stop at stage 1.
- The product is a web app with users as the main surface. Use
  [build-from-template](../build-from-template/SKILL.md).

## Safety gates

- **Never buy a domain** until the owner says "buy it" in the same turn. Show
  the domain and the price first. A registration is a charge that you cannot
  easily undo.
- **Never import data without a licence record.** Each source needs a URL, a
  licence name, and a refresh cadence before its first row lands.
- **Never make staging or a Preview indexable.** Only production on the apex
  domain is indexable.
- **Never switch Stripe to live mode** without the owner's approval. Build and
  test every tier in test mode.
- **Never commit Cloudflare account IDs, resource IDs, or tokens.** Keep
  placeholders in Wrangler files and fill them at deploy time.

## 1. Pick the niche

A niche must pass all four tests. One failure means a different niche.

| Test | Pass | Fail |
|---|---|---|
| Global reach | The entity exists in many countries, such as pottery studios or funeral homes | The entity exists under one national law only |
| Open data | A source with a licence that permits reuse, such as [OpenStreetMap](https://www.openstreetmap.org/copyright) (ODbL, attribution and share-alike) or [Wikidata](https://www.wikidata.org/wiki/Wikidata:Licensing) (CC0) | The only source is a map app or a review site whose terms forbid copying |
| A payer | Listed businesses pay for a badge, a better placement, or leads | Nobody would pay to stand out |
| A free tool | Searchers need a calculation, a check, or a lookup for this niche | The niche has no question that a tool can answer |

Write the result as one line per test, with the source URL and the licence
name. Read the licence text itself. A summary on a blog is not proof.

A share-alike licence binds the whole database. If you build listings from
OpenStreetMap, your listings database must also be under the ODbL, and each
page must credit OpenStreetMap. Your paid tiers then sell placement and
leads, not the data.

**Stop condition:** all four tests pass, and each data source has a licence
that permits your use. Then run [validate-an-idea](../validate-an-idea/SKILL.md)
if the payer test rests on a guess.

**Failure note:** do not scrape Google Maps or a review site. The
[Google Maps Platform terms](https://cloud.google.com/maps-platform/terms)
forbid scraping and building a database from its content. A directory built on
copied data can be removed at any time.

## 2. Check keyword domains

Pick names that match the search keyword, such as `<niche>finder` or
`<niche>-near`. Keep the country out of the name, so the site can grow into
new countries.

Run the read-only availability check from
[cloudflare-domain-launch](../cloudflare-domain-launch/SKILL.md) §1
(`POST /accounts/{account_id}/registrar/domain-check`). It returns each
domain's availability and price, and it buys nothing.

Show the owner a table of domain, available, first-year price, and renewal
price. Cloudflare Registrar sells at cost, so the renewal price matters as much
as the first year.

**Stop condition:** the owner makes one of two decisions. Either the owner
picks a domain and says to buy it, or the owner defers the purchase. If the
owner defers, continue with a placeholder domain. The template runs locally
without a real one. Stage 7 needs the real domain, so the purchase gate moves
there.

## 3. Clone the template and swap the three parts

Clone your directory template into a new repo. Treat it as a starting commit,
not a dependency. Run the template's own quick start once, unchanged, before you
edit anything. A baseline that fails before your changes is the template's bug.

Then change only these three parts:

| Part | What changes |
|---|---|
| Config | ID, name, domain, niche, the entity name (singular and plural, plus its schema.org type), geography, typed attributes, filter facets, completeness rules, tiers, SEO and FAQ copy templates, free tools, and data sources. Turn off the demo flag. |
| Data | The category taxonomy and the listings file. |
| Brand | Theme tokens, logo, OG image, and a `DESIGN.md`. See [design-context](../design-context/SKILL.md) and [directory-fleet-ui](../directory-fleet-ui/SKILL.md) for preset + `/design` workflow. |

Keep the app code free of niche words and brand values. Read them from the
config. Build every public URL from the template's path helper, not from string
literals. A literal URL breaks when the geography changes.

Plan for more than one country, currency and language from the first commit.
A one-country URL shape is hard to change after search engines index it.

**Stop condition:** the template's local end-to-end smoke passes on your data,
and it writes its report artifact.

## 4. Import the listings

Each source in the config needs a key, a URL, a licence, a refresh cadence and
a note. Keep that record in the database too, so each listing traces back to
its source.

Import rules:

- Give each row a stable source ID. A rerun must update a row, not add a
  duplicate.
- Record each import run with its source, its row counts and its issues.
- Keep typed attribute values typed. A price is a money value with a currency,
  not free text.
- Run the import again until it passes with zero errors. Then check the counts
  against the source.

**Thin-content gate:** score each listing for completeness. A listing with a
missing required field, or a score below the minimum, is `noindex`. It stays on
the site for visitors but stays out of the sitemap. Thin pages at scale can
pull down the rank of the whole domain.

**Stop condition:** the import passes, each listing has a source, and the
sitemap leaves out every listing below the gate.

## 5. Add free tools

A free tool is a small calculator, checker, generator or lookup page. It earns
search traffic that listing pages cannot, and it can capture leads.

For each tool, set a slug, a title, a one-line description, a kind, and one
primary keyword. Build the tool so it works without sign-in. Put the answer
above the fold.

**Stop condition:** each tool page renders, answers one question, and appears
in the sitemap. [marketing-site](../marketing-site/SKILL.md) owns the tool
channel in depth.

## 6. Set up the tiers

A directory earns money in four ways. Turn on only the ways that the niche
supports.

| Way | Who pays | What they get |
|---|---|---|
| Verified | The listed business | A badge, edit rights, and leads |
| Featured | The listed business | A higher place on city pages |
| Sponsored | Any business in the niche | A fixed slot on one city or category page |
| Leads | The listed business | A fee per visitor message |

Model each paid tier as a Stripe Price with a stable `lookup_key`, monthly and
annual where it fits. Use the lookup key in code, not a Price ID. A lookup key
survives a price change, but a hard-coded Price ID does not.

Build the claim flow before the paid tiers. A business must prove that it owns
a listing, for example through an email on the listing's domain, before it can
pay to change that listing.

**Stop condition:** each tier completes a test-mode checkout, and the webhook
sets the tier on the right listing. [saas-billing-stripe](../saas-billing-stripe/SKILL.md)
owns checkout, webhooks and dunning.

## 7. Deploy staging and production

**Gate:** this stage needs the real domain on Cloudflare. If the owner has not
said to buy it, stop here and ask.

| Environment | Branch | Host | Indexable |
|---|---|---|---|
| Preview | pull request | Worker Preview URL | No |
| Staging | `main` | `staging.<domain>` | No |
| Production | `release` | `<domain>`, with `www` redirected to it | Yes |

Ship to production with a fast-forward merge of `main` into `release`, so
that `release` points at the same commit as `main`. Never push other commits
to `release` by hand. [branch-deploy-convention](../branch-deploy-convention/SKILL.md)
explains why a branch filter that names a missing branch fails without an error.

Name each Cloudflare resource `<id>-<resource>-<env>`. Keep real IDs in GitHub
variables. Scope the deploy token to one account and one zone.

Verify each environment after its first deploy:

```bash
curl -s https://staging.<domain>/robots.txt          # expect: Disallow: /
curl -sI https://staging.<domain>/ | grep -i x-robots # expect: noindex
curl -s https://<domain>/robots.txt                   # expect: a Sitemap: line
```

**Stop condition:** staging blocks crawlers, production allows them, and
production serves `/sitemap.xml` and `/llms.txt` with status 200.

## 8. Launch into search engines

Use the `search-console` CLI from
[itsryanarmani/clis](https://github.com/itsryanarmani/clis/tree/main/search-console).
It verifies the domain over DNS, adds it to Google Search Console and Bing
Webmaster Tools, submits the sitemap, and sends the sitemap URLs to IndexNow.
Every step is safe to run again.

As of 2026-10-01, its README says that the CLI has passed E2E tests against
fake servers but has not yet run against the live APIs. Run `--dry-run` first.

Build it once:

```bash
git clone https://github.com/itsryanarmani/clis.git
cd clis/search-console && make build      # binary: bin/search-console
export PATH="$PWD/bin:$PATH"              # so the commands below find it
```

Do the one-time setup from its README: a Google OAuth client of type Desktop
app with the consent screen set to In production, then
`search-console auth google`, a `BING_WEBMASTER_API_KEY`, and a
`CLOUDFLARE_API_TOKEN` with Zone Read and DNS Edit. Check the setup with
`search-console auth status --check`.

Then check, dry-run, and launch:

```bash
search-console sitemap check https://<domain>/sitemap.xml
search-console launch <domain> --sitemap https://<domain>/sitemap.xml \
  --cloudflare-zone auto --dry-run
search-console launch <domain> --sitemap https://<domain>/sitemap.xml \
  --cloudflare-zone auto
```

**IndexNow takes two runs.** The first `launch` writes `<key>.txt` to
`--key-dir`, and the `indexnow` step fails with `the key file is not
reachable`. Commit that file to the site's static files and ship it through `release`,
so that `https://<domain>/<key>.txt` returns 200. A staging deploy is not
enough, because IndexNow reads the key from the production host. Then run
`launch` again. The finished steps pass again, and the `indexnow`
step sends the URLs. Google does not take IndexNow. It reads the sitemap.

Exit code 4 means DNS was not ready before `--wait` ended. Run the command
again. Do not delete the TXT or CNAME records.

**Stop condition:** each row of the `launch` table shows `pass`.

## 9. Run the GEO checks

Answer engines quote pages that answer first and that they can parse. Check
each page type (home, country, region, city, category, listing, tool):

- **Answer-first sentence.** The first sentence under the H1 answers the
  page's question with a number, for example "There are 14 pottery studios
  in Austin, Texas." Build it from a copy template with real counts.
- **FAQ schema.** Put `FAQPage` JSON-LD on city pages, with questions that
  the page answers. Since
  [August 2023](https://developers.google.com/search/blog/2023/08/howto-faq-changes),
  Google shows FAQ rich results only for authoritative government and health
  sites. Answer engines still read the
  markup, so keep it accurate.
- **Entity schema.** Put `LocalBusiness` JSON-LD, or the type from the config,
  on each listing page, plus `BreadcrumbList` on each page.
- **`llms.txt`.** Serve a short map of the site at `/llms.txt`.
- **A markdown copy of each listing.** Serve a plain markdown version of
  each indexable listing page and link it from `llms.txt`.

Then audit production with [geoaeo](https://www.npmjs.com/package/geoaeo):

```bash
npx -y geoaeo audit https://<domain>
npx -y geoaeo audit https://<domain> --ci --min-score 90   # exits non-zero below 90
```

The report lists each check as `PASS` or `FAIL`, then the top fixes. Fix the
top fixes first. [geo-aeo](../geo-aeo/SKILL.md) explains each artifact.

**Stop condition:** the audit passes `--ci --min-score 90`, or each remaining
`FAIL` has a written reason.

## Done

The directory is done when all of these are true:

- [ ] The niche passed four tests, and each source has a licence record.
- [ ] The owner approved the domain purchase.
- [ ] The app code has no niche or brand values.
- [ ] The local end-to-end smoke passes on real data.
- [ ] Listings below the completeness gate are `noindex`.
- [ ] Each paid tier completes a Stripe test-mode checkout.
- [ ] Staging and Previews are `noindex`. Production is indexable.
- [ ] The `search-console launch` table is all `pass`.
- [ ] `geoaeo audit --ci` passes on production.

Next, measure traffic with [launch-analytics](../launch-analytics/SKILL.md).
