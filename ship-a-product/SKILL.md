---
name: ship-a-product
description: "Orchestrator: sequence idea -> working code -> open-source-ready repo -> discoverable live site -> launch video -> published announcement, with optional Product Hunt launch. Points at the stage skills rather than duplicating them -- use this to decide which stage you're in and which skill to invoke next, not as a rigid must-do-all-in-order pipeline."
---

# ship-a-product

The stages, in order, each with its own dedicated skill. Not every project needs every stage — enter wherever the project actually is.

```
-1. validate-an-idea       idea -> evidence that someone wants it, or a documented kill. Do this BEFORE naming or scaffolding: a name and a repo are cheap, but the weeks spent building the wrong thing are not. Skip only when the demand is already proven.
0. name-a-product          idea -> a name that is available, memorable and conflict-free, with the domain registered (check competing COMPANIES before domains; a domain sweep will happily hand you variants that sit inside a funded competitor's brand) -- skip only if the name is already settled
1. build-from-template     idea -> a running scaffold (web-app-shaped ideas only; skip for CLIs/libraries/extensions)
2. (your own build process) scaffold -> real working product (brainstorm/plan/implement/test -- not a single skill, it's the actual engineering work)
2a. pre-public-repo-audit  working code -> confirmed clean of leaked secrets, laptop paths and PII before visibility flips public -- going public has no undo, so run this immediately before stage 3
3. repo-standards          working code -> a repo ready for public visibility (README to standard, LICENSE, images, About panel, branch protection)
3a. auth-and-tenancy       scaffold -> the tenancy decision made before the first schema lands. Is the paying customer a person or an organisation? Retrofitting organisations onto a single-user product is one of the most expensive migrations a small product ever does, so decide it here even if the UI never shows it.
3b. saas-billing-stripe    working product -> a product that can charge a human (Checkout subscription, webhooks as source of truth, Customer Portal, dunning) -- only if the product charges money; skip for a free tool or an OSS library. Do this BEFORE the announcement: a launch that cannot take payment wastes the traffic it earns. Use `pricing-page` to decide the value metric, the tiers and how they are presented, and `regional-pricing-stripe` if prices vary by market.
4. launch-seo              live site -> discoverable by search + shareable (sitemap, robots.txt, OG/Twitter meta, sitemap submission to Google Search Console + Bing + Yandex) -- only if there's a hosted site; skip for CLI-only/library-only projects with no deployed site
5. geo-aeo                 live site -> quotable by AI answer engines + usable by agents (llms.txt/llms-full.txt, markdown mirrors, schema.org JSON-LD, WebMCP manifest, answer-first copy, programmatic entity pages, free tools) -- only if there's a hosted site; run right after launch-seo
5a. website-directory-submission live site -> listed for backlinks + traffic + GEO (tiered free web directories, submission packet, remote-MCP-server listings for sites with a hosted /mcp endpoint) -- only if there's a hosted site; run right after geo-aeo
6. launch-analytics        live site -> measurable (GA4 client + server, Microsoft Clarity; enforces the GA4 + Clarity + Search Console rule for any domain) -- only if there's a hosted site
7. launch-video-generation storyboard -> a real launch/announcement video
8. social-launch-post      video + copy -> a draft ready to publish across X/LinkedIn/Threads/Bluesky/Mastodon
9. product-hunt-launch     significant release -> reviewed Product Hunt draft, assets, launch-day runbook, recap
```

## After stage 9: the launch is not the finish line

This pipeline ends at the announcement, and that is deliberate -- it is a launch
orchestrator, not a growth one. But a launch with no loop behind it decays. Two
skills own what comes next, and neither is optional for a product meant to earn:

- `product-analytics` -- activation, funnel, retention and cohorts. `launch-analytics`
  (stage 6) measures traffic; this measures whether anyone came back. Instrument the
  activation event before the announcement, or the launch spike arrives unmeasured and
  cannot be analysed later.
- `lifecycle-email` -- welcome and activation sequences, trial-ending, abandoned
  checkout, dunning, win-back. Triggered from the events `product-analytics` defines,
  and it carries the dunning mail that `saas-billing-stripe` depends on.
- `incidents` -- error tracking, an uptime check and one alert channel a human
  actually reads. A product nobody is watching fails silently, and the first
  report is a churned customer.
- `support-inbox` -- the other half of finding out something is wrong, and the
  cheapest source of product truth there is.
- `dependency-hygiene` -- the slow failure. A product you cannot rebuild is
  already broken; you just do not know yet.
- `grow-a-product` -- the orchestrator for all of the above. It sequences the
  growth loop the way this skill sequences the launch, and it is where to go
  once stage 9 is done.

## Conventions every repo in this pipeline starts with

Set once, at stage 0/1, by `new-product-workspace` (§5). They are listed here so
a stage that scaffolds a workflow does not reinvent them:

- `main` is the default branch and deploys to the **staging** environment;
  `release` is production. `staging` and `production` are environment names,
  never branch names.
- Private `itsryanarmani/*` repos use `boat` for build, lint, typecheck, test,
  E2E, deploy and API waits. Use `boat-8` for a heavy production build.
  Public repos use GitHub-hosted runners. macOS and Windows jobs keep their
  GitHub-hosted images. The Dell fleet is retired.
- Every repo carries `.github/workflows/vibecodereview.yml`
  (`itsryanarmani/vibecodereview@v1`).
- **A workflow trigger naming a branch the repo does not have never fires and
  never errors.** Whenever a stage adds or copies a workflow, check its
  `branches:` filter against the branches that exist.

## Deciding where to enter

- **No name yet, or renaming an existing product?** Start at `name-a-product`. Do this before scaffolding — the name decides the repo name, the package scope, and the domain, and changing it later is a multi-thousand-file rename plus a Cloudflare/GCP cutover. Note that GCP project IDs are immutable, so a late rename can never fully complete.
- **Have an idea, no code yet, and it's web-app-shaped?** Start at `build-from-template`.
- **Have an idea that isn't a web app, or already know the shape doesn't fit a template?** Skip straight to building it (brainstorm → plan → implement, following whatever process/skills the codebase and toolchain call for), then rejoin at stage 3.
- **Already have working code, just need to go public?** Run `pre-public-repo-audit` first, then `repo-standards`.
- **Repo's public and there's a hosted site (docs/marketing/product)?** Run `launch-seo` then `launch-analytics` before announcing it — a search-invisible, bare-link-preview, un-measured launch undercuts the announcement and leaves you blind to whether it worked.
- **No hosted site (CLI/library only)?** Skip `launch-seo` and `launch-analytics`, go straight to `launch-video-generation`.
- **Site's discoverable already, need to announce it?** Start at `launch-video-generation`.
- **Have a video already, just need the post?** Start at `social-launch-post`.
- **Need a Product Hunt launch or relaunch?** Use `product-hunt-launch` after the release is real and the Product Hunt theme is significant enough to justify a launch.

## What this skill does NOT replace

Stage 2 — actually building the product — is real engineering work, not a template-fill exercise. Use the project's normal process for that (brainstorming, TDD, code review, whatever the codebase's own conventions are). This orchestrator exists to make sure the *surrounding* stages (repo hygiene, announcement, distribution) don't get skipped or reinvented each time, not to compress the actual build into a checklist.

## Cost/delegation shape across all stages

Every stage below benefits from the same pattern: judgment (architecture decisions, creative direction, what to say in the announcement) stays with the highest-tier model available; mechanical execution (writing boilerplate config files, running generation scripts, extracting content into structured data) delegates to a cheaper model. `launch-video-generation`'s fidelity-ladder idea (§6 there — free wireframe review before any paid step) generalizes: don't spend real time or money on a later stage until the earlier one is actually approved. Confirm the repo's OSS-ready before spending on a launch video; confirm the video's approved before spending on cross-platform posting; confirm a Product Hunt theme is significant and policy-compliant before creating a launch draft.
