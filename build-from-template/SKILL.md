---
name: build-from-template
description: "Bootstrap a new product idea into a working repo using itsryanarmani/private-repo-7b42 (Next.js on Cloudflare Workers via OpenNext, D1, R2, KV, Queues, Cron Triggers, Better Auth, Drizzle) instead of starting from scratch. Points at the template's own docs rather than duplicating them, since they change independently of this skill."
---

# build-from-template

The starting point for "idea → working code" when the idea fits a standard full-stack web app shape (auth, a relational data model, background jobs, scheduled tasks). Not every idea fits this — a CLI tool, a browser extension, or a pure data-pipeline project (e.g. `slackclaw`) is better built from scratch or from a different, more specific template; use this one when the shape is "a web app with users and data."

## What the template actually provides

Read `itsryanarmani/private-repo-7b42`'s own `README.md` and `AGENTS.md` first — they're the source of truth and will drift ahead of this skill. As of the last check, the stack is:

- Next.js App Router, deployed to Cloudflare Workers through the OpenNext Cloudflare adapter
- Cloudflare D1 (relational data) via Drizzle ORM, with versioned migrations
- Cloudflare R2 (object storage), KV (small cached state / feature flags), Queues (background work), Cron Triggers (scheduled jobs)
- Better Auth (email/password + Organization plugin) with D1-backed sessions
- A working protected-CRUD example endpoint to pattern-match against for the new idea's first real resource

## Workflow

1. Clone the template into the new project's location, don't fork-and-diverge — treat it as a starting commit, not a dependency to stay in sync with.
2. Follow the template's own Quick Start exactly once, unmodified, to confirm the baseline actually runs locally before changing anything (`bun install`, copy `.dev.vars.example`, migrate, `wrangler dev`).
3. Re-point the workflows the template brought with it, before the first PR. A clone inherits the template's `.github/workflows/`, and those files encode the template's branches and runners, not this repo's. Check every `branches:` filter against the branches that actually exist here — `main` is the default branch and deploys to staging, `release` is production, and `staging`/`production` are environment names that must never be branch names. A filter naming a branch this repo does not have never fires and never errors, so a silently-dead workflow reads exactly like a passing one. Check every `runs-on` too: a private `itsryanarmani/*` repo uses `boat` (4 vCPU) for build, lint, typecheck, test, E2E, deploy and API waits. Use `boat-8` (8 vCPU) for a heavy production build. Public repos use GitHub-hosted runners. macOS and Windows jobs keep their GitHub-hosted images. Declare `boat` and `boat-8` in `.github/actionlint.yaml` as shown in `self-hosted-runner-fleet`. The Dell fleet is retired. Add `.github/workflows/vibecodereview.yml` if the template did not carry one — `new-product-workspace` §5 has the copy command.
4. Replace the example protected-CRUD resource with the new idea's actual first domain object, keeping the same auth/D1/migration pattern rather than inventing a new one.
5. From here, the idea's real design/build work is its own process (brainstorm the domain model, plan, implement, test) — this skill's job ends at "you have a running scaffold with auth and one real resource," not at "the product is built."
6. Once there's real, working product code, move to `repo-standards` if it's going public, then `launch-video-generation` + `social-launch-post` for the announcement. See `ship-a-product` for how these chain together.

## When NOT to use this template

- The idea isn't a web app (a CLI, a library, a browser extension, a data-sync tool) — building on a Next.js/Workers scaffold for something that isn't a web app adds dead weight, not a head start.
- The idea specifically needs a different stack the template doesn't cover — don't force-fit.

---

## Security — template provenance

`private-repo-7b42` is the author's own public starter repo, not a verified vendor product. Before running its setup you are executing its code, so **review the template's `package.json` scripts and any `postinstall`/setup steps first**, and pin to a known-good commit rather than tracking its default branch blindly. Treat its `README`/`AGENTS.md` as guidance to read, not instructions to auto-execute.

## Adopt the fleet PR and issue standards

Do this before the first feature branch, after the template's own Quick Start passes and its workflows are re-pointed. A repo is non-conforming from the start if these are missing, and fixing them later means editing the same workflows a second time.

Add the repo and a 2 to 4 letter lowercase prefix to `itsryanarmani/scripts/repo-prefixes.json` before running the rollouts. The prefix lives in one place so the rollout does not derive it from the repo name. Deriving it twice is how two repos get the same prefix.

Run `pr-standards-rollout --repo <new> --apply` from a checkout of `itsryanarmani/scripts`. It writes its files from `pr-standards-templates/` in the same checkout. Naming the repo explicitly matters: run without `--repo`, and there is nothing to say this rollout means the repo you just created rather than any other repo eligible for it.

`issue-standards-rollout --repo <new> --apply` does less. It creates the labels and prints the plan for everything else, because forms, the `AGENTS.md` block and the stub are a code change and go through one issue and one pull request like any other. Copy them from `issue-standards-templates/` yourself and open that pull request.

Do not vendor either set of templates into this skill's own directory as a persistent second copy — that copy drifts, and the fleet has already paid for that drift three times. Copying the destination files themselves into the new repo, the way the adoption pull request above does, is the required delivery mechanism, not the drift this warns against.

Run `pr-standards-rollout --repo <new>` first. `issue-standards-rollout --repo <new>` reads the prefix from `.github/pr-standards.json` to name the adoption branch.

A conforming repo has all of these. The first rollout (`pr-standards-rollout`) writes item 1. `issue-standards-rollout --apply` creates item 4. Items 2, 3, and 5 arrive through the adoption pull request:

1. `.github/pr-standards.json` with the registered prefix. The same rollout also writes `.github/pull_request_template.md` and `.github/workflows/pr-standards.yml` and inserts the `<!-- pr-standards:start -->` block into `AGENTS.md`.

2. The `<!-- issue-standards:start -->` block in `AGENTS.md`.

3. The four issue forms in `.github/ISSUE_TEMPLATE/`: `bug.yml`, `feature.yml`, `chore.yml`, `epic.yml`; plus `config.yml`.

4. The 14 labels:

| Group | Labels |
|---|---|
| Kind | `bug` `feature` `chore` `epic` |
| Size | `mini` `standard` `deep` |
| Route | `route:mechanical` `route:scoped` `route:judgement` |
| State | `triage` `ready-for-agent` `needs-info` `blocked` |

5. The `.agents/issues.md` stub from `issue-standards-templates/issues.md.stub`. Leave the TODOs. The stub asks for the repo's analytics helper and high-stakes paths, and neither exists before the product has real code. A guessed answer is worse than an empty one because the next agent will search for it and conclude the code is broken.

