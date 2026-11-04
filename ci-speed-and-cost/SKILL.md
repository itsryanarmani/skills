---
name: ci-speed-and-cost
description: "Use when CI is slow or costs too much and you want tactics that were measured on a large private fleet, with the trap beside each one. Covers measuring runner minutes, swapping the type checker, judging a cache, gating a test matrix on a cheap check, step timeouts, red scheduled suites, affected-only tests, runner pools, local push gates, and fleet-wide rollout. Triggers: 'speed up CI', 'cut CI cost', 'CI is slow', 'runner minutes', 'cache made it slower', 'flaky scheduled run', 'which CI change pays'."
---

# ci-speed-and-cost

Twelve tactics from a one-day campaign to make CI faster and cheaper on a fleet of about 120
private repositories. Each one has its measured result and its trap. Some results are losses.
They are here on purpose.

Most of the gain did not come from where we expected it. The type checker paid the most.
Two caches lost time. Runner pinning saved almost nothing.

## When to use this

- **Triggers:** 'speed up CI', 'cut CI cost', 'CI is slow', 'runner minutes', 'the cache made it
  slower', 'flaky scheduled run', 'which CI change pays'.
- **This is not the entry point.** Start at [ci-speed-diagnosis](../ci-speed-diagnosis/SKILL.md).
  It finds the constraint. Come here when you must choose a tactic and want its measured cost.
- **Siblings own the detail:** [ci-build-speed](../ci-build-speed/SKILL.md) for the build,
  [ci-selective-evidence](../ci-selective-evidence/SKILL.md) for test selection,
  [ci-cost-at-agent-scale](../ci-cost-at-agent-scale/SKILL.md) for trigger and spend,
  [high-volume-ci-optimization](../high-volume-ci-optimization/SKILL.md) for job placement.

## What paid and what did not

| Tactic | Measured result | Verdict |
| --- | --- | --- |
| Rust port of the TypeScript compiler | typecheck 34.5 s to 2.5 s on the runner | Paid the most |
| Gate the matrix on the cheap check | about 780 runner-minutes avoided in 20 runs | Paid |
| Step timeout on network steps | about 70 runner-minutes saved on one hang | Paid |
| Compiler cache for a per-site deploy | net -35 s per site | Lost |
| Browser-binary cache | about 0 s saved, 272 MB written | Lost |
| Dependency-cache restore | 17-18 s against 7.7 s clean install | Lost |
| Five cheap gates in parallel | 8-9 s saved | Marginal |
| Blobless clone on a depth-1 checkout | 0 s saved | No gain |
| Runner pinning across the fleet | 3 jobs in 2 of 44 eligible repos | Small |

## 1. Measure first

Pull the last 100 to 150 runs of each workflow. Split every job into **wait**, **setup** and **run**.

- **Round up and label.** Billing rounds each job up to whole minutes. Do the same and write
  `estimated` beside the total. Real billing records are the only source for money.
- **Do not call a dependency wait a queue.** A "queue" column that counts time behind `needs`
  jobs is not pool starvation. Subtract the dependency wait first.
- **Dedupe re-runs.** A re-run attempt copies the passed jobs with new ids and the same runner
  and timestamps. Dedupe on name, runner, start and end. One sample counted 75 runner-minutes twice.
- **Report two percentiles.** Show success-only values beside all-outcome values. Cancelled
  jobs end early and pull the median down.

Baseline example: one repo showed about 12,400 estimated runner-minutes in the sample window.
Its check job had p50 66 s over all outcomes and 59 s over successes only.

## 2. Swap the type checker

A Rust port of the TypeScript compiler cut the typecheck step from 34.5 s to 2.5 s on the CI
runner, and from 62 s to 4-6 s on a laptop. The cheap-check job fell from about 88 s to 26 s.
Because the step is fast, the push gate can run the real project typecheck.

**Trap: a false green.** The port uses newer library defaults. One `lib` setting omitted the
iterable DOM types, and the port accepted code the old compiler rejected.

1. Pin the `lib` setting explicitly. Do not inherit the default.
2. Inject known errors. Compare the code, file and line under both compilers.
3. Write the verified compiler version to a stamp file.
4. Make the local gate fail when the lockfile version differs from the stamp.
   A new version needs a fresh parity run.

## 3. A cache is a loss when restore costs more than rebuild

Measure restore time on the real runner before you add a cache.

| Cache | Restore | Work saved | Net |
| --- | --- | --- | --- |
| Compiler cache, per-site deploy | median 24 s (range 6-70 s) | about 8 s of build | -35 s per site |
| Browser binary | not recorded | install step median 4 s on warm boxes | about 0 s, and a 272 MB entry written |
| Dependencies | 17-18 s | clean install from a warm package store: 7.7 s | loss |

Two design rules for any cache that stays:

- **Never key on the commit SHA when many jobs write.** 43 jobs at 240 MB each wrote about
  10 GB per push. The repo held 11.4 GB against a 10 GB quota. Eviction then removed the useful
  caches too. Use one writer per push, or one entry per day.
- **A branch ref can read the default branch's cache scope but cannot write to it.** A cache
  that only pull-request runs save is invisible to every other branch. Save from the default branch.

## 4. Gate the expensive matrix on the cheap check

Use `needs: [check]` on the matrix. Do **not** add `always()`.

**Measured.** About 780 runner-minutes of an 8-shard suite ran after a failed cheap check, in
one sample of 20 runs.

- **Cost:** the cheap job's time now sits in front of the matrix. Keep that job short (see tactic 2).
- **Trap: a final gate that passes on skipped jobs.** A skipped shard is not a passed shard.
  Make the last required job fail unless every upstream result is `success`.
- **Test the controller.** For a merge-queue controller, feed it fake job lists. Skipped shards
  must count as incomplete.

## 5. Set step timeouts on network steps

One hung dependency install used the whole 75-minute job timeout. A 5-minute step timeout would
have saved about 70 runner-minutes. The longest healthy install in recent runs was 46 s, so
5 minutes leaves headroom.

Measure the longest healthy run before you choose the number. Set it on installs, downloads and
any step that waits on a remote service.

## 6. Scheduled suites: classify before you optimise

Of the last 20 scheduled runs of an 8-shard suite, 19 were red. That cost about 718 estimated
runner-minutes a day, and about 676 of them ran in red runs. The causes were mostly test failures
on stale commits, plus one runner hang. None was infrastructure alone.

1. **Classify each failure:** infrastructure, real failure, flake, or build. Fix by class.
2. **A "skip if nothing changed" rule must demand a green gate.** The last gate must be a
   SUCCESS and younger than 24 hours. Otherwise a red gate suppresses every re-run.
3. **Keep one forced full run each day.**
4. **Expect no saving while the suite is red.** Replayed on the real history, the skip applied
   0 of 20 times. The saving appears only after the suite is green.

## 7. Affected-only test selection

Use a deterministic path-to-test map. Widen to the full suite on any of these:

- an unknown path or a shared root;
- a config file, a lockfile or a workflow file;
- a new, deleted or renamed spec;
- an empty diff or a bad base.

Replayed on 60 commits, only 8 narrowed. That is the correct result. A selector that narrows
often is probably wrong.

**Test the skip logic.** Write the failure modes first. Hide a server change next to a docs
change and assert that the selector widens. Then mutation-test the check: break each rule in a
scratch copy and require a red result. 22 of 22 mutants went red. The first version let 4 live.
Review found one false skip: data files under a site folder that a spec reads through a path join.
See [ci-selective-evidence](../ci-selective-evidence/SKILL.md) for the controls.

## 8. What did not pay

| Idea | Result | Why |
| --- | --- | --- |
| Run five cheap gates in parallel | 8-9 s saved | The task runner already cached lint and test |
| Blobless clone | 0 s on a depth-1 checkout | Nothing to skip. Unsafe where rename detection or history scanners read old blobs |
| An LLM test selector | stays in shadow mode | It cannot show what it skipped |

## 9. Runners

A big-runner pool starved. Median queue wait was 32.8 min (p90 215 min). The small pool had
0.2 min.

- **Use the small runner** unless a job is CPU-bound.
- **Give tiny required jobs their own lane.** A policy check or secret scan queued 25 minutes or
  more behind heavy jobs on the same pool, for a job that runs in seconds. Move them to a
  hosted runner, or to a separate pool.

## 10. The local push gate

| Trap | Fix |
| --- | --- |
| A pre-push hook that typechecks only changed files passes a renamed export that breaks an unchanged importer (reproduced) | Run the real project typecheck once it is fast |
| Git cannot list the pushed files (unknown remote sha, shallow clone) | Fail closed. Never pass on an empty list |
| A repo-local hooks path set while a global path or hooks already exist | Do not set it. It silently disables the others |
| An installer that writes into the shared hooks folder from a worktree | Never do it during development. An unmerged installer linked hooks to a worktree and blocked every other worker's push |
| A fresh worktree needs a sibling `file:` dependency | Make a real copy. A symlink resolves outside the bundler root and the build fails. Never commit the copy |
| The gate prints only the failed step | Print the cause: the missing sibling, the stale generated file |
| A generated file (a host list) went stale on the default branch and blocked every push | Fix generated files in their own tiny PR |

## 11. Roll out from one place

A free plan has no org rulesets and no required workflows. Put the shared logic in one private
repo as reusable workflows and composite actions. Private reusable workflows work across your own
private repos once that repo's Actions access allows the same owner. Prove it first with a
throwaway probe repo.

A sync tool opens **one reviewed PR per repo** from named, idempotent codemods.

| Rule | Reason |
| --- | --- |
| Dry run by default | A first run must change nothing |
| Cap repos per run (default 5). Require an explicit flag above it | Limits the blast radius |
| Read each repo's PR prefix. Never guess | A wrong prefix fails that repo's own checks |
| Skip archived and public repos | Archived repos reject pushes. Public repos need review of what leaks |
| Never run target repo code or scripts | Validate with a YAML parse and a workflow linter only |
| Give the validator an environment **allowlist** | "Strip the tokens" misses the one you forgot |
| Pin runners from an **allowlist**: safe triggers, read-only permissions, no environment, no secrets, no OIDC or contents-write, no deploy, release, publish, agent or comment job names | A deny list lets the unexpected through |
| Treat a missing `permissions` block as **not** read-only | The default token may write |
| Refuse a closed rollout PR unless forced | A person closed it for a reason |
| After a PR-create timeout, re-query before cleanup | The PR may exist |
| Run a mutation harness on the tool | 41 of 41 mutants went red |

**Payoff.** Runner pinning moved 3 jobs in 2 of 44 eligible repos. The fleet gain was in shared
steps (the install timeout, check-before-matrix) and in the audit. See
[ci-runner-indirection](../ci-runner-indirection/SKILL.md) for the one-variable pattern.

## 12. Process traps

- **Do not quote a projection as a result.** One projected saving read 11.9 minutes, then 3 to 4
  minutes on a closer look, then a net loss when measured in CI. Projections were wrong three times.
- **Review and merge traps for agent fleets** (fresh-context review, mutation-testing reviewers,
  pinning the head SHA at merge, shared git config, squash trailers, claim identity, resumable
  work, lock release) are in [agent-pr-standards](../agent-pr-standards/SKILL.md).
