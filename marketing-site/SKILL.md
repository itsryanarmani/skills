---
name: marketing-site
description: "Use when a product with one thin landing page needs a whole public site: page families per audience, use case, module or competitor, programmatic SEO pages, a mega-menu shell, free browser tools and real lead forms, with tests that guard every claim."
---

# marketing-site

One landing page is a page. Twenty is a system. This skill is about the system:
the content model that generates the pages, the shell that holds them, and the
tests that stop the copy claiming things that are not true.

**Worked example:** `itsryanarmani/private-repo-f304` PR #45 — 60 pages, 26 free tools, 73
browser tests, built in one session from a seven-competitor audit.

## When to use

- **Triggers:** 'pages for each use case', '/partners', 'a page per competitor', 'programmatic SEO pages', 'a site like <competitor>', 'scale the marketing site'.
- Starts from a competitor design audit; covers the content model, the animated shell and full-taxonomy footer, copy discipline for generated pages, and brand assets with no design tools.
- Seven failures: a registry that drifts from its pages, prerendered routes that 404 only in production, delegated copy with invented numbers, staging getting indexed, a reveal wrapper that blanks the hero, an unwired title template, and a merged PR that never reaches production because main deploys to staging.
- Stops where landing-page, impeccable, geo-aeo and saas-brand-system begin.

## What this owns, and what it does not

| Need | Skill |
|---|---|
| Section anatomy of one page, conversion review gates | **landing-page** |
| Pixels, motion, craft floor, the design review | **impeccable** |
| Brand exploration and the full kit | **saas-brand-system** |
| llms.txt, JSON-LD types, WebMCP, answer-first structure | **geo-aeo** |
| sitemap, robots, OG, favicon at first launch | **launch-seo** |
| Logo and colour drift across header, footer, favicon, OG | **verify-branding** |
| Removing AI tells from prose | **humanizer** |
| Deploying it | **deploy-app-cloudflare** |

This skill owns the layer none of them do: **how many pages exist, where they
come from, and how they stay honest.**

Read `landing-page` before building the home page. Read this before building the
other fifty.

---

## 1. The brief comes from an audit, not from taste

Do not start from a moodboard. Spend the first hour reading competitors, and
write down what they *do not* do. That list is the brief.

Fetch five to eight sites: the direct competitors, the adjacent category, and
one company whose site is simply good. For each, record the nav taxonomy and its
dropdown children, the hero headline verbatim, every homepage section in order,
the CTA wording, the proof (numbers, logos, certificates), and the full footer
link taxonomy.

Then answer six questions:

1. **What page families does everyone have?** If all of them segment by audience
   and none by feature, that is the axis.
2. **What does nobody publish?** Price, security posture, a real changelog. Gaps
   are cheap differentiation.
3. **What does nobody serve?** Answer engines, agents, free tools.
4. **What is the proof pattern?** Counted numbers plus certificates, usually.
5. **What is the best site doing that the others are not?** Usually one template
   repeated across four axes.
6. **What should you refuse to copy?** Rotating hero carousels, stock doctors,
   demo-only funnels.

Write it to `docs/NN-competitor-design-audit.md` with the date and the URLs.
Every design decision afterwards cites a row in it. This is also the artifact
that stops a later reviewer relitigating the layout on taste.

**In the private-repo-f304 audit:** the three direct software competitors ran one-page
websites, none of the seven published a price or an `llms.txt`, and only one had
free tools which it hid in a resources menu. That single page of findings
determined the entire build.

---

## 2. One typed record renders one page

This is the whole architecture. Everything else follows from it.

```
content/marketing/
  types.ts            the shape every page family satisfies
  audiences.ts        6 records  →  /for/[slug]
  use-cases.ts        7 records  →  /use-cases/[slug]
  platform.ts         6 records  →  /platform/[slug]
  comparisons.ts      4 records  →  /compare/[slug]
  tool-pages/*.ts     one file per tool  →  /tools/[slug]
  registry.ts         resolves a slug in ANY family to a link
```

The type is the contract. Keep it small enough that a record is writable in
twenty minutes and rich enough that the page does not look like a form letter:

```ts
export interface MarketingPageContent {
  slug: string;
  name: string;          // nav and card label
  headline: string;      // the h1 — speak to the reader, not about the product
  subhead: string;
  metaTitle: string;     // no site-name suffix; the title template adds it
  metaDescription: string;
  keywords: string[];
  eyebrow: string;
  problem: { headline: string; body: string; pains: string[] };
  benefits: Benefit[];
  steps?: Step[];
  stats?: Stat[];        // every stat carries a `source`
  faqs: FaqItem[];
  related?: string[];    // slugs in any family
  tools?: string[];
}
```

**Why it pays.** A new audience is a data change, not a component. Four families
share one template, one metadata factory, one set of JSON-LD builders. The
sitemap, `llms.txt`, and the footer all read the same registry, so they cannot
disagree about what exists.

**The rule that makes cross-linking survive.** `related` names slugs across
families, and the resolver *drops unknown slugs silently*:

```ts
export function relatedLinksFor(slugs: string[] = []): RelatedLink[] {
  return slugs
    .map((slug) => bySlug.get(slug))
    .filter((e): e is RegistryEntry => Boolean(e))
    .map(({ href, title, body, meta }) => ({ href, title, body, meta }));
}
```

Without that, writing content referencing a page you have not built yet breaks
the build, so authors stop cross-linking. With it, you can write the links first
and let the pages catch up.

### One route registry, not three lists

Sitemap, `llms.txt`, and any nav sanity test read **one** `publicRoutes()`
function. The failure this prevents is real and quiet: a page that exists, is
linked in the footer, and is absent from the sitemap.

For file-per-record families, generate the index rather than hand-maintaining
it, and make the generator **fail when a slug has a content record without a
component, or the reverse.** That mismatch produces a live page with no tool on
it, and nothing else catches it.

---

## 3. The shell

**Header.** Three behaviours are worth the code:

- Transparent over the hero, blurred bar after ~12px of scroll. A hard edge on
  load cuts the hero art.
- Mega menus that open on hover **and on focus**, with a ~90ms close delay so a
  diagonal mouse path from trigger to panel does not dismiss the panel. Escape
  closes. `aria-expanded` and `aria-haspopup` on the trigger.
- Long link lists wrap to two columns. A single column of seven items makes a
  panel that towers over the page.

Mobile is a `<details>` accordion drawer, not a copy of the mega menu. Lock body
scroll behind it.

**Footer.** This is the page-family map, so it is large on purpose: one column
per family plus company and legal. It is also the honest answer to "how many
pages does this site have" — if a family is not in the footer, ask why it exists.

**Reveal on scroll must fail open.** A wrapper that starts at `opacity-0` and is
shown by an IntersectionObserver hides the entire site when JavaScript fails.
Tag the element and add one rule:

```html
<noscript>
  <style>[data-reveal]{opacity:1!important;transform:none!important}</style>
</noscript>
```

---

## 3b. The home page section vocabulary

A shell and a content model do not make a home page feel like the reference.
This is the section set worth copying, in order, and what each one is *for*.
Missing three of these is the difference between "structured" and "good".

| Section | Its job | The mistake |
|---|---|---|
| **Hero with a live artefact** | Show the product working in the first viewport | A static screenshot, or a stock illustration |
| **Marquee of what it replaces** | Name the tools on their desk today, struck through | Listing your features instead of their tabs |
| **Scrubber** | Let the visitor click through the workflow, one stage at a time | A static numbered row that says the same thing |
| **Problem block** | The pain in their words, numbered, in their voice | Your solution wearing a problem's clothes |
| **Stats row** | Two or three numbers, each with its source under it | An unsourced number, which is worse than none |
| **Card grid to the page families** | The only place the generated pages are visible from the home page | Building the families and never linking them |
| **Free tools grid** | Something usable before the form | Hiding the tools in a resources menu |
| **Comparison table** | The honest matrix against the alternatives | A matrix where you win every row |
| **FAQ** | The six questions sales answers every week | Questions nobody asked, written for keywords |
| **Inverted CTA band** | One tonal shift that says the page is over | A fifth identical section with a button in it |

Two rules make the set cohere:

- **Every band gets an eyebrow.** A short uppercase label above the heading, so
  a scanner can tell the sections apart without reading them.
- **Alternate the ground.** Default, muted, default. A page of identical bands
  reads as one long section however good each one is.

**The card grid is the one most often skipped**, and it is the one that makes
the page families worth building. If a visitor cannot reach `/for/insurers` from
the home page, the only thing that will ever find it is a crawler.

### Scrubber panels earn their place

A scrubber whose panel only holds a paragraph is a worse accordion. Give it two
columns: the explanation, and a small artefact that changes with the stage — a
mock record with status dots, a before-and-after pair, the step list with the
current one marked. The panel is the reason to click.

---

## 4. Copy discipline

Generated pages fail in a specific way: they read like a form letter, and they
invent numbers. Two rules fix both.

**Every number carries its source, in the data.** Not in a footnote — in the
`Stat` type, rendered under the figure. If a page has no sourced number, it has
no stats section. Give whoever writes the content a fixed table of approved
figures with their sources, and forbid anything else. This is the single
highest-leverage constraint when delegating copy.

**Ban the vocabulary before writing, not after.** Hand the writer the list:
*streamline, seamless, robust, leverage, empower, unlock, comprehensive,
cutting-edge, holistic, ecosystem, delve, foster, showcase, boasts, stands as,
serves as, underscores, in today's, effortless, peace of mind.* Plus the
constructions: negative parallelism ("not just X, it's Y"), rule-of-three
padding, empty present-participle tails ("...ensuring accuracy"), em dashes.

Then `grep` for them in CI or before commit. A regex over the content directory
catches in one second what a read-through misses.

Run the result through **humanizer**. Pair with ASD-STE100 if the house style is
plain technical English: short sentences, active voice, one idea each.

### Comparison pages are where sites lie

The pattern that works, and the reason to build them at all:

- Every claim about a competitor comes from **their own public site**, with the
  date you read it.
- "Not published" means you could not find it, **not** that it does not exist.
  Say so on the page.
- Every page names **what they are genuinely better at** and **who should pick
  them instead of you**, in their own block, not buried.
- Invite correction: "if we have this wrong, write to us."

A comparison page that only flatters you is read as marketing and trusted as
marketing. One that concedes two rows is read as a review.

---

## 5. Free tools are the organic channel

Purely client-side calculators and generators. No account, no upload, nothing
leaves the browser. They rank for the queries your audience types *just before*
doing the job by hand.

**Picking them:** find the calculation your user currently does in a
spreadsheet, and the deadline they currently track on a sticky note. Twenty to
thirty is a channel; five is a gesture.

**The page skeleton**, which is also what makes them rank: hero, the widget,
four how-it-works steps, three or four explainer blocks of real body copy, a
FAQ, related tools, one CTA. The widget alone ranks for nothing — the six
hundred words under it do the work.

**Engineering rules:**

- One file per tool for the content, one component of the same name, wired by
  the generator in §2.
- No `Math.random()` or `new Date()` at module scope or in a `useState`
  initialiser. On a prerendered page the build date gets baked into the HTML and
  then disagrees with the browser. Use a mount-safe hook that returns `null` on
  first render.
- Load each widget by dynamic import so a visitor to one tool does not download
  the other twenty-five. Assert it in a test.
- Anything taking pasted text gets a visible "remove identifiers first" warning.

**Where a tool touches law, money, or safety, narrow it deliberately.** Ship the
reference with its citation and let the tool do the arithmetic, not the
judgement. A deadline tool should present an editable window sourced from the
letter in front of the user, not assert a number that changes by jurisdiction
and by year. Say plainly what it is not.

---

## 6. Forms

One endpoint behind every form, discriminated by `kind`. Contact, demo, partner,
newsletter, and the quote form are the same POST.

- **Turnstile that fails closed in production** and passes in development. A
  missing secret in production is a hard 500, not a silent bypass.
- **A honeypot field** hidden off-screen and from assistive tech. A filled one
  gets a success response so the bot stops retrying.
- **Zod at the edge**, with field-level errors returned.
- **Tell the user it worked only once the internal notification is queued.** If
  the queue is unavailable, say so and give them the email address. A form that
  reports success and drops the lead is worse than no form.

Never ship a `mailto:` form. It loses every visitor without a configured mail
client, and it stores nothing.

---

## 7. Brand assets with no design tools

On macOS you do not need Illustrator or a paid renderer:

```bash
# SVG → PNG at any size
qlmanage -t -s 1024 -o outdir mark.svg     # writes mark.svg.png
sips -Z 512 icon-512.png                   # resize in place
sips -c 630 1200 og-image.png              # crop to an exact box
```

Author the mark as SVG, generate `favicon.svg`, 16/32/180/192/512 PNGs, a
maskable variant with ~78% inset, and a 1200×630 OG card. Keep the source SVGs
next to the exports so the set regenerates instead of being traced.

`qlmanage` pads to a square. Author an OG card on a **square canvas** with the
content in the middle 630px band, then centre-crop — trying to crop a 1200×630
render will fight you.

Pass the whole set to **verify-branding** afterwards.

---

## 8. Tests that guard the claims

Ordinary coverage is not the point. Write the tests that fail when the *site
starts lying*.

| Test | What it catches |
|---|---|
| Walk every URL in the sitemap, assert 200 | A page in the registry that does not render |
| Assert the calculator's output sits inside the band the page cites | A model that drifts from its own sources |
| Assert no rate appears where policy says not to publish one | A figure creeping back in |
| Assert one `<h1>`, a canonical, an OG image on each page type | A metadata regression |
| Parse every JSON-LD block, assert the types | Invalid structured data |
| Assert a tool page loads no other tool's code | Code-splitting silently regressing |
| Assert `robots.txt` disallows a non-canonical host | Staging getting indexed |

**Run them against a production build, not the dev server.** A dev server
compiles routes on demand, so a parallel suite walking forty pages times out on
compilation rather than on anything real — and you spend an hour debugging a
non-bug. Point the runner at `next build && next start`.

Extract any model with domain numbers into its own module so its bands can be
asserted without a browser.

---

## The seven failures that cost real time

**1. The registry drifts from the pages.** A content record with no component
ships a page with an empty slot; a component with no record is dead code.
Generate the registry and fail the generator on a mismatch.

**2. Prerendered routes 404 only in production.** On Cloudflare, OpenNext keeps
prerendered HTML in the KV incremental cache, not in the asset bundle. Plain
`wrangler deploy` never populates it, so every `generateStaticParams` page 404s
while every static page works, and local `next start` is perfectly green. Run
`opennextjs-cloudflare populateCache remote` before deploying, never set
`dynamicParams = false` on those routes, and smoke-check live URLs in the deploy
job. See **deploy-app-cloudflare**.

**3. Delegated copy invents plausible numbers.** Every factual defect in the
private-repo-f304 build came from generated content that looked right: a cost model at
twice the band it cited, a tax rate eighteen months stale, a subprocessor list
naming a vendor the repo had already dropped. Check each figure against the
source it names, not against plausibility.

**4. Staging gets indexed.** A publicly reachable staging host serving
`index, follow` competes with production. Render `robots.txt` per request and
disallow everything unless the request host is the canonical one — one build is
deployed to both environments, so the host is the only runtime difference.

**5. Reveal-on-scroll leaves the page blank.** A wrapper that starts at
`opacity-0` and waits for an IntersectionObserver will never show content that
was already on screen at mount if the observer does not fire, and a hero is
always on screen at mount. Show anything already in the viewport immediately,
keep a timeout as a failsafe, and add the `noscript` rule. A late reveal is
cosmetic; a blank hero is not.

**6. The title template is never wired.** Defining `title.template` in a
metadata factory does nothing until the root layout actually exports it. Symptom:
every page title is missing the site name and no favicon is linked. One test on
`<title>` catches it.

**7. Merged is not live.** A green PR merged to `main` is not a fix in front of
users. `main` deploys to the staging environment and production is promoted only from
the `release` branch, so the live site keeps serving the old page while every
check is green and the PR reads as done. Before reporting a site fix as shipped,
read the deploy workflow's `on.push.branches`, then fetch the production URL and
assert the thing you changed is actually in the response. Treat the promotion as
a separate, outward-facing step: it needs its own decision, not a merge.

---

## Order of work

1. Competitor audit → `docs/NN-competitor-design-audit.md`
2. Brand assets (**saas-brand-system**, then §7 for the export pipeline)
3. `types.ts`, the metadata factory, the JSON-LD builders, `publicRoutes()`
4. Shell: header, footer, section primitives
5. Home page: the section set in §3b, with **landing-page** for conversion
   anatomy and **impeccable** for craft
6. One content family end to end, and only then the rest
7. Free tools engine, then the tools
8. Forms and the lead endpoint
9. **geo-aeo** for llms.txt, markdown twins, and the answer-engine robots rules
10. Copy pass: banned-word grep, then **humanizer**
11. The guard tests in §8
12. Deploy, then check the live URLs before calling it done

Steps 6 and 7 are where delegation pays: the families and the tools are
high-volume and well-specified. Give each agent the type file, one finished
record as the exemplar, the approved-figures table, and the banned-word list.
Then review every number.
