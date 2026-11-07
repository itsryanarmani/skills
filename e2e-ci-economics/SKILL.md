---
name: e2e-ci-economics
description: "Use when a browser E2E suite (Playwright, Cypress, WebdriverIO) is the slowest thing in CI, or someone proposes another browser in the matrix, more workers, caching the suite, or `continue-on-error`."
---

# e2e-ci-economics

An E2E leg is the most expensive check you run and the easiest one to stop believing. **Every leg
on the pull-request path must gate something. A leg that gates nothing belongs on a schedule.**

Two repositories built from one template were cut 85% and 83% in one campaign. In both, the
dominant defect was in the E2E suite, not elsewhere in the pipeline.

## When to use this

- **Triggers:** 'E2E is slow', 'the e2e job takes forever', 'add WebKit to the matrix', 'raise Playwright workers', 'shard the e2e suite', 'cache the e2e job', 'mark e2e continue-on-error', 'e2e is flaky', 'e2e has been red on main', 'the e2e test fails but the endpoint works'.

**Use this skill** when the long pole is a browser E2E job, or before you change the browser
matrix, the worker count, the shard count, or the `continue-on-error` flag.

**Diagnose first with [ci-speed-diagnosis](../ci-speed-diagnosis/SKILL.md)** — it tells you whether
the E2E leg is the critical path. Come here only after it is. **Use a sibling instead** for build
and cache levers ([ci-build-speed](../ci-build-speed/SKILL.md)), runner tiers and fixed-port service
containers ([high-volume-ci-optimization](../high-volume-ci-optimization/SKILL.md)), or spend and
queueing ([ci-cost-at-agent-scale](../ci-cost-at-agent-scale/SKILL.md)).

## A non-gating job must never sit on the critical path

`continue-on-error: true` is a written statement that you do not trust the result. A job that
runs on every push and cannot fail the run is the worst of the three states, and it is invisible,
because the run stays green.

| State | Runs on every PR | Can fail the run | Verdict |
| --- | --- | --- | --- |
| Trusted gate | yes | yes | correct — remove the flag |
| Scheduled signal | no, nightly or `workflow_dispatch` | yes, and it alerts | correct — move it off the PR path |
| The half-state | yes | no | wrong — pay every time, learn nothing |

**Measured.** One browser leg carried `continue-on-error: true` and ran roughly twice as long as
any other job in the workflow. It was the critical path in 7 of 7 runs on the first repository
and 7 of 8 on the second. The slowest job in both pipelines gated nothing.

**Decide, then act.** Do you trust the result? Remove the flag and let it gate. Do you not trust
it? Move it to `schedule` or `workflow_dispatch`. Never leave it in the middle.

## The expensive suite runs on the commit that ships, not the pull request

Two-step CI is the fleet rule: the pull request stays cheap, and the full
suite runs on `push` to `main` and `release` — against the code that will
actually merge. A browser leg on the PR path needs a better reason than "it
is the test we have". Measured 2026-10-24: private-repo-0a63's Worker preview on every
pull request cost 243 wall-clock minutes across 33 runs in a 22.2-hour window
— about 117 boat-hours a day at 1,000 pull requests, plus a preview database
per branch. Its keep/drop table for every workflow lives in
[ci-cost-at-agent-scale](../ci-cost-at-agent-scale/SKILL.md).

The pattern already exists in a multi-site monorepo: its four-shard Playwright smoke runs only
on `release` refs and on pull requests that target `release`. That is the
shape to copy — the suite gates the ref that ships. Heavy browser suites that
already run after Deploy on `main` stay there. **Never cancel a long suite to
buy latency** — a run killed before it finishes is coverage that never lands.
Collapse pending runs instead: the in-flight run completes and the newest
pending run replaces the older one.

## Gate on a minimal browser set. Run the full matrix nightly.

Browser matrix cost multiplies. Three browsers times a full suite is three full suites, and the
per-browser catch rate is not equal. Chromium and Firefox catch nearly everything. WebKit catches a
real class of defect, but a narrow one. So gate on the minimal set on every pull request — two
engines is a normal answer — and run the full matrix nightly, with an alert on failure. This is the
same trade as the table above. Cut the browser you would have marked non-gating.

## Shard the suite. Do not raise `workers` on shared state.

A suite pinned to `workers: 1` on CI looks like free speed waiting to be claimed. It is not.

Raising `workers` puts two workers on **one dev server and one local database**. That is the
contamination the per-browser job layout already prevents. Sharding into separate jobs keeps
one server and one database per shard.

Isolated workers are the one exception: a count above one is acceptable only with proved
independent mutable resources — separate databases, sessions, ports, homes, and resource
ownership where each applies. See
[ci-selective-evidence](../ci-selective-evidence/SKILL.md#workers-are-isolation-claims-not-speed-claims)
for the qualification. Workers that share a mutable resource stay unsafe; a
shared server alone, with no shared mutable state, does not make them unsafe.

**Verify the test count is identical before and after.** One split ran 33 + 32 = 65 tests, against
65 before. A shard flag that silently drops tests reports faster and proves less.

## Fixed cost sets the floor on sharding

Each shard pays the whole setup cost again. Measure it before you choose a shard count.

**Measured.** Each E2E leg paid about 92s of cold dev-server compile before the first test ran. So
a third shard bought only about 30s of latency for 50% more machine time.

**Rule.** Shard until the fixed cost dominates, then stop. **Write the fixed cost in the workflow,
next to the shard count**, so the next person knows where the floor is.
[high-volume-ci-optimization](../high-volume-ci-optimization/SKILL.md#sharding-has-a-floor-and-it-is-the-fixed-cost)
measures the same floor on a unit suite.

## Never put an E2E result in a task-runner cache

This is not a gap to close. It is a category error.

A task runner caches a **deterministic output keyed on source inputs**. An E2E result is not a
function of the source. It boots a server, reads a real database, and drives a browser. Caching a
pass would cache an assertion about a **running system**, keyed on **files**. The first time the
system breaks without the files changing, you get a green check for a broken system.

**Do not wrap an E2E task in a cached task-runner target to make CI faster.** Mark it uncacheable
and leave it uncacheable.

**Useful consequence:** E2E timings are always genuinely cold, so they are the honest number to
quote when you report a CI change. Everything else may be reading a cache.

## E2E fails quietly more than any other check

**Measured.** One repository's E2E suite was failing on the default branch across all three
browser jobs, on one spec, on a single object-match assertion. Nobody noticed.

Put that next to the non-gating leg above and the pattern is one pattern: **nobody reads a checks
list.** So do not rely on it. Alert explicitly on a default-branch E2E failure, into the channel the
team already watches. This is the check that earns a page, because it is the one that stays red for
weeks. Alert on the nightly full-matrix failure too — a nightly job nobody watches is a job you
deleted.

## Address a collection member by a stable key, never by index

A positional assertion is correct only while nothing is ever prepended. Nothing guarantees that.

**Measured.** A spec asserted on entry `[0]` of a discovery endpoint that returns an array of
entries. A later change prepended a new entry, which legitimately carries a different shape. The
assertion silently retargeted onto that new object and failed on a property the object was never
meant to have. The endpoint was healthy throughout. The spec stayed red for six days.

Three properties make this E2E-shaped rather than a generic testing nit.

- **The error message actively misleads.** An object-match mismatch reads as "the API returned the
  wrong data". Proving the application was correct took reading the endpoint, `git log --follow` on
  both sides, and bracketing CI history to one commit. An engineer who trusts the message repairs a
  healthy endpoint.
- **Nothing carried the signal to a person** — the same defect as the section above.
- **E2E assertions are the ones that get forgotten,** because they live furthest from the code that
  changed. The change that broke this one repaired the matching unit test for exactly this reason,
  then missed the E2E spec. A sibling suite already encoded the new contract while this one rotted.

**Rule.** Look the entry up by its anchor, id, name or URL. Then assert on what you found.

**Establish which side moved before you change either.** `git log --follow` on the spec and on the
implementation answers it in seconds, and the commit that changed the shape usually says what it
intended.

**Fix it stronger than you found it.** The repair replaced one indexed assertion with a lookup of
all five entries by anchor, and added an assertion for the new entry's own shape. That is strictly
stronger than what it replaced, and faster to reason about. A stale expectation is an opportunity to
make a test un-shiftable, not just green.

## Report a retry-pass. Do not absorb it.

`retries: 2` on CI is reasonable. Silent retries are not.

Retries turn an environment problem into what looks like a test problem. **Measured:** two tests
that were flaky on the baseline runner passed first try on a faster one. The tests were fine. The
machine was slow.

**Rule.** A test that only passes on retry is a reported result, not a green one. Print the
retry-pass list in the job summary. Check the runner before you touch the test.

## What you can enforce, and what you cannot

Be honest about the boundary. Two of these you can write today. One you cannot write at all.
One you could build, and should not build yet.

**Enforceable statically, today.** "No job may set `continue-on-error: true` while it triggers on
`pull_request` or `push`." That is a pure YAML predicate, so a short `yq` check in a pre-commit hook
or its own CI job expresses it. It over-flags a cheap non-gating job as well as an expensive one.
That is correct — the half-state is what you are banning, at any price.

A second static rule is writable but noisier: flag an index expression inside an assertion, for
example `expect(x[0])`, in the E2E spec directory only. Scope it there. In a unit test on a fixture
you control, an index is fine.

**Enforceable as an agent rule, in prose.** Put this in the repository rules file:

> Never add `continue-on-error: true` to a job that runs on every push. Either remove the flag and
> let the job gate, or move the job to `schedule` / `workflow_dispatch`. Never add a browser to a
> pull-request matrix; add it to the nightly matrix. Never raise the E2E worker count on shared
> state to make a shard faster — isolated workers need proved independent mutable state first.
> Never assert on a collection member by index; look it up by a stable key. When a
> test fails after a shape change, establish which side moved before you change either.

**Not enforceable by a workflow linter.** `actionlint` has a fixed rule set and no custom-rule
plugin. It validates syntax, expressions, shell, and action inputs. It has no run timings, so
"this job is non-gating **and** on the critical path" is outside what it can see. Do not invent
this rule for it.

**A timing tool could carry the check. Do not build it speculatively.** `ci-job-timings` in
[itsryanarmani/scripts](https://github.com/itsryanarmani/scripts) already ranks jobs by median duration and
knows which workflow file each job came from. The gating half needs a local checkout to read the
YAML, plus name matching from a rendered matrix job (`e2e (webkit)`) back to its YAML key (`e2e`).
That is real work for a check you can already do by hand:

```bash
grep -rn "continue-on-error" .github/workflows/   # which jobs gate nothing
ci-job-timings owner/repo                         # which job is the long pole
```

Build the automated version when you run the check across many repositories on a schedule, and not
before.

## The order

1. **Confirm the E2E leg is the critical path** (`ci-speed-diagnosis`). If it is not, stop.
2. **Resolve every `continue-on-error` job.** Gate it or schedule it. Usually this is the whole win.
3. **Cut the pull-request browser matrix to the gating set.** Move the rest to nightly.
4. **Measure the fixed per-shard cost.** Shard while it pays. Record the floor.
5. **Alert on default-branch and nightly failures.**
6. **Surface retry-passes.**
7. **Replace every indexed assertion with a key lookup.** Do it before the array grows.

## Shared local database ownership

Several local worker processes can open the same SQLite files while each believes it owns the database.
Reads can then fail under mixed traffic, even when each server passes alone.
Treat database-busy and session-token errors as evidence to investigate shared state before adding retries.

1. Record which processes open each state directory. Include CLI helpers, seed scripts, import commands, and side workers.
2. Compare one server alone, mixed traffic with shared files, and a controlled alternative with separate ownership.
3. Keep request counts, status counts, durations, and database errors in repeatable artifacts.
4. Prove the logger captures a deliberate error before drawing conclusions from empty logs.
5. Preserve cross-host writes if tests depend on them. Separate state copies change that contract.
6. Test one emulator runtime as an option when several server variants must share one logical database.
7. Seed before the runtime opens the database. Route later helpers through that runtime instead of opening another SQLite owner.

A single runtime is a design to validate, not a universal emulator feature.
Verify the installed emulator's multi-port support, bindings, assets, environment variables, and self references.
Preserve client-address headers when a test supplies them. Check default client identity when it does not.
Keep any query helper test-only and bound to loopback. Never add it to the production bundle.
Preserve SQL splitting, result shapes, and error propagation when replacing CLI helpers.

Faster database calls can expose existing rate limits in authentication tests.
Give independent simulated clients independent identities. Keep one identity where the test verifies a per-client limit.
Measure send and verification calls separately before changing pacing.
Do not weaken production limits or hide failures with retries to make the faster suite pass.

Retest cross-host write visibility, mixed reads and writes, authentication, imports, and environment-specific behavior.
Then measure the complete suite in CI. A helper benchmark does not establish release savings.
