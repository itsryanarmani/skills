---
name: agent-lint-guardrails
description: "Use when setting up or tightening automatic code-quality guardrails on a repo where agents open most of the pull requests — cyclomatic-complexity budgets, file/function size caps, the React 'deslop' hook bans, and a coverage ratchet. Rules that are draconian for a human are the right ceiling for an agent: they cap the blast radius of vibe-coded churn and keep diffs reviewable. Covers the oxlint config, the warn-first-then-ratchet rollout strategy that lets budgets ship green across a whole fleet at once, and the hard gotchas (oxlint has no no-restricted-syntax, parse errors can't be downgraded, most repos have Allow-auto-merge off). Triggers: 'add lint budgets', 'cyclomatic complexity limit', 'oxlint', 'deslop', 'ban useEffect/useState', 'coverage ratchet', 'lint rules for agents', 'stop the slop', 'roll lint to all my repos'."
---

# agent-lint-guardrails

Rules too strict for a human are the right ceiling for an agent. An agent will happily write a
300-line function with a cyclomatic complexity of 40; a human reviewer will not catch it at 2am
across 40 repos. So move the ceiling into the linter, run it in CI, and let the agent self-correct
before the PR ever reaches you.

## The budgets (oxlint)

Use **oxlint** (`oxc`, https://oxc.rs) — one fast binary, no plugin install, runs in CI and
pre-commit. Default agent budgets:

| Rule | Cap | Why |
|---|---|---|
| `complexity` | 10 | one function, one job — split, don't raise the cap |
| `max-lines` | 300 | a file over 300 lines is two files |
| `max-lines-per-function` | 50 | a function over 50 lines hides its own bugs |
| `max-params` | 4 | more than 4 params → pass an object |
| `max-depth` | 4 | deep nesting is un-reviewable |
| `max-nested-callbacks` | 4 | same |
| coverage | ratchet | every PR must not lower codecov; new code carries tests |

The canonical `.oxlintrc.json` + workflow live in `~/oxlint-rollout/` on the author's machine.

## Calibrate cleanup rules before enforcement

Record the repository's pinned linter and compiler versions before changing a rule.
Write accepted and rejected fixtures before changing code or configuration.
A cleanup rule must reject measured failures and accept valid code.
Keep each fixture's source, expected result, actual exit status, and tool version.
Run the fixtures through the same command that the repository gate uses.

| Rule area | Accepted cases to preserve | Rejected cases to detect |
|---|---|---|
| Unused bindings | Public exports, type references, required initializer effects | Private bindings with proved unused values |
| Duplicate imports | Type-only imports, import attributes, distinct module contracts | Redundant runtime imports with the same contract |
| Unreachable code | Valid branches, intentional compiler checks, required cleanup | Statements after an unconditional exit |
| Dependency use | CSS imports, package exports, build tools, peer and type contracts | Packages with no supported consumer |

A rejected valid import blocks that rule's enforcement.
Keep its fixture and report the limitation. Do not rewrite valid code to satisfy a false positive.
A missing source reference does not prove that a binding or dependency is unused.
Check entry points, tests, public exports, runtime registration, and string-based calls separately.
Retain uncertain uses until their reachability is resolved.

Remove a binding only when required initializer effects remain.
Run the existing caller E2Es and required builds after each cleanup group.
Save changed source and the failed result before restoring a failed group.
Keep source restoration separate from generated-data and runtime restoration.
Generate profile-specific test data in an explicit setup step.
Check that test commands preserve that prepared input and all other tracked source.
Restore the original fixture after the profile completes, including when a check fails.

React hook restrictions below express style policy. They do not prove unused code or duplicate behavior.

## Ship it warn-first, then ratchet — the only way to fan out

Strict-as-**error** is a trap for an existing fleet. Measured on one real repo (private-repo-4944, 702 TS
files): strict budgets produced **~470 blocking errors** — 266 complexity, 121 long-function, 42
big-file, plus hundreds of `correctness`/`perf` category errors. Multiply across 40 repos and you
have a multi-week refactor campaign, not a rollout — and every PR red-CIs and blocks its own merge.

Ship existing size and complexity budgets as `warn` while measuring their violations.
Promote one rule when its calibration cases pass and its existing violations are resolved.
A calibrated correctness rule may start at `error` when the repository already passes it.
Keep advisory counts separate from required checks. Apply every repository review and merge gate.

## Three gotchas that will bite you (all learned the hard way)

1. **oxlint has NO `no-restricted-syntax`.** The React "deslop" hook bans (below) CANNOT ride on
   oxlint — the config fails to parse with `Rule 'no-restricted-syntax' not found`. Budgets live in
   oxlint; the React bans live in **eslint**. Two linters, two jobs.
2. **Parse errors can't be downgraded by config.** oxlint keeps a couple of parser-level errors
   (`Empty parenthesized expression`, missing-semicolon on some TSX) at error severity no matter
   what `categories` say — so the job exits 1 even in an all-`warn` config.
   Validate configuration and parsing before the rollout. Keep the linter's real exit status.
   Do not use `|| true` in a required gate. Report advisory measurements separately.
3. **Most personal repos have "Allow auto-merge" OFF.** `gh pr merge --auto` then fails. Either the
   PR is immediately mergeable (direct `--squash`) or it is BLOCKED by a required review — do NOT
   admin-bypass a required review to land a lint config; that defeats the guardrail. Leave it for
   the one-click approval.

## React feature code — the deslop ban-list (eslint, warn-first)

In **feature** code, derive state; do not store it. Ban via eslint `no-restricted-syntax`
(CallExpression selectors) at `warn`, then flip to `error`:

- No `useState` / `useEffect` / `useLayoutEffect` / `useReducer` / `useSyncExternalStore` — derive
  from the backend + URL params; load data through a loader-initiated `useQuery` (tanstack router
  `preload="instant"` makes the route instant).
- No `useMemo` / `useCallback` — the React Compiler handles memoization.
- No overzealous destructuring; no type casting outside tests.

These are style, not correctness — an `eslint-disable` with a one-line reason is the rare escape
hatch, never the default fix.

## Rollout mechanics (fleet-scale)

- **Fan-out unit = 2 self-contained files** (`.oxlintrc.json` + a standalone `oxlint.yml` that runs
  `bunx oxlint` on `boat` for private `itsryanarmani/*` repos, or `ubuntu-latest`
  for public repos), independent of each repo's existing
  turbo/eslint pipeline. Uniform, minimal blast radius, no per-repo bespoke wiring.
- **No local clone needed** — create the branch and both files through the `gh` contents API
  (the token needs `workflow` scope; a git *push* of a workflow file works, but the contents-API
  edit of a workflow is classifier-gated, so patch workflows via clone+push).
- **Skip forks and empty scaffolds.** `isFork==true` → never lint someone else's code. A 3–4 KB
  repo is an empty scaffold — skip it.
- **Deploy guard before merge.** Check whether the PR's base branch has a deploy/release workflow
  triggered by push to it. Read the actual trigger, target environment, and repository shipping rules.
  Do not infer the environment from a branch name. A push to `main` can deploy production.
  Complete required local checks, independent review, and any required Preview walk before merge.
  Do not create or retarget deployment branches to fit an assumed convention.
- **Check the trigger against the branches that exist.** A `branches:` filter naming a branch the
  repo does not have never fires and never errors, so a fanned-out workflow can land in dozens of
  repos and run in none of them. Read `git branch -r` (or the repo's default branch from the API)
  before you trust a green fan-out.

## Beyond lint — the fuller agentic guardrail stack

Lint budgets are one layer. The complete stack for high-quality agent-authored code:

1. **Lint budgets** (this skill) — complexity, size, deslop.
2. **Coverage ratchet** — a CI gate that fails when a PR lowers coverage; new code carries tests.
3. **Asset/bundle byte budget** — a size check on built JS/CSS so an agent can't 3× the bundle.
4. **Typecheck as a required check** — `tsc --noEmit`, no `any` (oxlint `no-explicit-any`).
5. **Secret + dependency scanning** — gitleaks on every PR; Dependabot/`bun update` cadence.
6. **A review gate** — an LLM council or `claude-review` that must approve, plus one human click on
   protected branches. Do not let agents bypass it.
7. **CI economics** — at agent PR volume, add concurrency-cancel + path filters (see the
   `ci-cost-at-agent-scale` skill) before the bill surprises you.

Roll each out the same way: warn/advisory first across the fleet, then ratchet to blocking per repo.

## Related

- [pr-standards](../pr-standards/SKILL.md) — the pull-request rule these budgets keep a PR inside: one issue, one concern, under 500 lines, with proof of the work.
