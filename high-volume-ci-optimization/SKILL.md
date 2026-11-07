---
name: high-volume-ci-optimization
description: "Use when many agent-generated PRs per hour across many repos make CI feel slow or expensive, and you need it instant and cheap on infrastructure anyone can reproduce. Covers a warm Boat JIT pool, collapsing job fan-out, host-local caches outside the workspace, in-job parallelism caps, fixed-port services, duplicate-work filters, affected-only builds, a remote cache, cache-masking hazards, timing APIs, pool wall-time cost, and security invariants. Cross-references self-hosted-runner-fleet for host setup rather than repeating it."
---

# High-volume CI optimization

Use the warm Boat pool for private Linux CI. Keep public repos on GitHub-hosted
runners. This skill covers job placement and cost. Pool setup lives in
[self-hosted-runner-fleet](../self-hosted-runner-fleet/SKILL.md).

**Measure before you place.** [ci-speed-diagnosis](../ci-speed-diagnosis/SKILL.md) is the entry point of this family. It names the critical path, so you move the job that matters instead of the job you noticed. Moving a job that is not on the critical path buys machine time only.

## Runner placement

| Job | Runner |
| --- | --- |
| Private build, lint, typecheck, test, E2E and deploy | `boat` (4 vCPU, 8 GB) |
| Private heavy production build | `boat-8` (8 vCPU, 16 GB) |
| Public repo jobs | GitHub-hosted `ubuntu-latest` |
| macOS and Windows jobs | Existing GitHub-hosted image |

Choose verification triggers before adding capacity. For repeated main CI,
paid waiting jobs, native integration fees, or review inference, use
[the development and release policy](references/development-and-release.md).

Run one JIT runner at a time on each always-on Box. Keep package caches,
Playwright browsers and Docker images between jobs. The broker hands JIT
configs to the agent and keeps the GitHub token off the Boxes. A start-limited
provider cannot supply a fresh VM for every job in a burst.

JIT runners get only the labels passed, without `self-hosted`. Use `boat` or
`boat-8` alone. Declare both in `.github/actionlint.yaml`; see the pool skill.
The pool code is in progress in `itsryanarmani/scripts` #508 and #509. Confirm
capacity before changing workflows. Check queue delay and idle cost together.

The retired desktop was fast per job but had a fixed service count and host
outages. Those measurements do not predict Boat queue delay. A pool still has
a capacity limit: N Boxes run at most N jobs at once. Measure recent runs.

## The job fan-out tax

A repo with 8 CI jobs pays checkout and dependency install 8 times. On one shared host that is the dominant cost, not the tests.

Collapse those jobs into one job and use the monorepo task runner's own parallelism (`turbo run lint test build --concurrency=...`, `nx run-many`, and the equivalent). One checkout, one install, then the tool fans out across packages inside the same workspace. The host already has the bytes. Extra GitHub jobs only re-download them.

Job names are the required status checks. If branch protection requires `lint`, `typecheck`, and `build`, collapsing them into `ci` leaves every PR stuck on "waiting for status" until you update the required checks in the same change. Treat the protection update as part of the workflow diff, not a follow-up.

Do not collapse jobs that must run on different tiers. A SARIF upload and a compile job do not belong in the same `runs-on`. Collapse within a tier.

## Caches must live outside the workspace

`actions/checkout` cleans the workspace. Keep caches outside it. On Boat,
keep `~/.bun`, Playwright browser downloads and Docker images warm. Set task
cache paths outside the checkout. Clean leftover containers after each job.
Do not run several agents on one Box or delete caches during workspace cleanup.

`runner.environment` cannot separate two self-hosted fleets. It reads `self-hosted` for a spare box and for managed cloud runners. If you use it in a cache key, both fleets share one cache. A native addon built against one kernel restores onto the other and fails. Key on distro plus kernel release instead, for example `runner.os` plus `uname -r`.

## Do not use actions/cache on a self-hosted runner

`actions/cache` uploads to the provider and downloads back, which is slower than reading `/opt/ci-cache` on the same disk, and it consumes the repository's 10 GB cache quota. On a self-hosted host the local directory is the cache. Skip the action.

Cloud and vendor-hosted jobs still need a cache they can see. That is the remote cache in [A remote cache is the cross-tier multiplier](#a-remote-cache-is-the-cross-tier-multiplier), not `actions/cache` round-tripping through the same host that already has the files.

## Cap in-job parallelism

Set task concurrency and test workers within the Box's CPU and memory limits.
A default Box has 4 vCPU and 8 GB. A large Box has 8 vCPU and 16 GB. More workers
can cause memory failures without reducing latency. Measure before raising caps.

## Fixed-port service containers

One job per Box permits fixed-port `services:` containers. Separate Boxes have
separate port spaces. Stop leftover containers before the next runner starts.
Do not put several runners on one Box to increase concurrency.

Review every `sudo`, absolute path and cache key when moving a workflow. Boxes
persist. Steps that delete toolchains, recreate swap or change kernel settings
can break later jobs. Remove disposable-VM cleanup steps before the move.

## Pool concurrency

One Box runs one job. Add pool capacity only after measuring queue delay,
CPU use and idle cost. Extra runner services on one Box do not create capacity.
Track offline Boxes and broker dispatch failures. A label with no live matching
runner leaves jobs queued. Re-measure after each change.

## Stop paying for duplicate work

Skip the run when the diff cannot affect the result.

Use `paths-ignore` for docs-only changes so a markdown edit does not rebuild the app. Keep secret scanners out of that ignore list. A credential in a `.md` file is still a credential.

Compare PR and merged-source verification before removing duplicate runs. A passing PR does not prove that concurrent changes compose. Keep coverage of the actual source that can reach deployment.

For a qualified development path, run the local gate before push and build
and smoke the actual deployment. Keep cheap PR policy checks. Broad remote CI
can remain manual and required for production promotion or queue candidates.
Bind production checks to their branch and exact revision. Preserve environment
restrictions and integration coverage. Use [the shared policy](references/development-and-release.md)
before removing a wait or changing skipped dependencies.

Where this path is not qualified, retain the existing broad checks while
measuring repeated work. The historical baseline and audit procedure live in
[ci-cost-at-agent-scale](../ci-cost-at-agent-scale/SKILL.md).

Choose a merge queue from measured contention and integration risk, not PR count alone.
Use the [merge and Preview throughput procedure](merge-and-preview-throughput.md)
before changing queues, publication locks, or Preview requirements.

A private merge queue on this personal account needs a paid organization plan —
rulesets and branch protection answer 403 "Upgrade to GitHub Pro". Where broad default-branch CI remains required, a busy repo can collapse
pending runs the way deployments do:

```yaml
concurrency:
  group: ci-main-${{ github.workflow }}
  cancel-in-progress: false
```

The in-flight run completes; the newest pending run replaces the older pending
one. Never cancel a long suite that would then never finish. The next step on
a repo that lands faster than the suite is a real batch: test the stack once,
bisect only on failure. A quiet repo still needs verification matched to its production inputs.

## Only run what changed

Use the task runner's affected-only filter against the base branch so untouched packages never build. `turbo run build --filter=...[origin/main]`, `nx affected -t build`, and the equivalent, all need a fetch deep enough to see the merge base (`fetch-depth: 0` or a shallow fetch of the base ref).

This is the monorepo counterpart of collapsing jobs. Fan-out tax is paying install eight times. Affected-only is paying compile for eight packages when one file changed. Do both.

Affected-only selection needs a full reference run on matching inputs.
Trigger changes do not qualify selection. The coverage controls live in
[ci-selective-evidence](../ci-selective-evidence/SKILL.md). The task runner
already in the repo is enough; one example monorepo runs Wireit. Do not adopt Nx, Bazel,
or Turborepo for this alone.

Compare against the merge base, not against the moving tip of the default branch. A long-lived branch compared to `origin/main` looks like it touched everything main landed since it forked.

## Sharding has a floor, and it is the fixed cost

Measured on a 3-way sharded suite: each shard took 207s wall, of which only 22 to 33s was test execution. The rest was checkout, dependency install and module loading. Every shard pays that fixed cost in full.

Adding shards multiplies the fixed cost and divides an already small number. Cut the per-shard fixed cost first, then shard further only when test execution dominates wall time.

A browser E2E shard has a much higher floor, because it boots a server as well. One suite paid about 92s of cold dev-server compile per leg, so a third shard bought about 30s for 50% more machine time. Measure the floor per suite. [e2e-ci-economics](../e2e-ci-economics/SKILL.md) carries the E2E rules, including why raising the worker count is not an alternative to sharding.

## A remote cache is the cross-tier multiplier

A cache on one host does nothing for cloud runners. A shared remote cache (the task runner's remote cache on object storage you already pay for) makes every tier warm: the self-hosted host, the ephemeral VM, and a laptop running the same tasks.

Without it, a job on a different Box rebuilds work already cached elsewhere. Point the task runner remote-cache URL at the same bucket from each Box. Keep a local cache outside the checkout for the first hit. The remote cache shares results across Boxes.

**Before you wire the credentials into a workflow, ask two questions, not one.** A sweep of 19 candidate workflows for a missing remote-cache env block found 19 correct skips. The near-miss: one workflow genuinely ran the task runner, but both its tasks were pinned `cache: false` — correctly, since a cache hit on a `*:fix` task would skip the fix and still report success. Wiring the credentials in would have let it reach a cache it could never legitimately read. So confirm both: does the tool run here, **and** are these specific tasks cacheable.

## Cache masking is a real hazard

A pipeline that passes only because of a cache hit can hide broken code until something busts the cache. Verify with one cache-busting run before trusting a green result.

A cache-bust is a run with the remote cache disabled, the local cache directory moved aside, or a dummy input that changes the task hash. Do it on the default branch on a schedule, and once on any change that touches toolchain versions, Dockerfiles, or task-runner config. The scheduled cold run is what makes a masked break show up on a known cadence instead of on an unrelated PR.

## Measure before optimizing

Billable minutes per run come from `GET /repos/{owner}/{repo}/actions/runs/{run_id}/timing`. Job wall time and which runner served it come from the jobs endpoint (`GET /repos/{owner}/{repo}/actions/runs/{run_id}/jobs`).

Billable minutes read zero once the work moved to self-hosted runners, so cost comparisons must use wall time. A self-hosted run that finishes in 90 seconds and reports `$0` is not free if it queued behind load average 30 for 30 minutes. Record `runner_name`, job `started_at` / `completed_at`, and host load, not only the timing endpoint's billable field.

Pull a sample of recent runs before changing labels. If the long pole is already a 40-second lint job on a warm host, collapsing jobs will not change how PRs feel. If the long pole is eight serial checkouts, it will.

## Measure two numbers, never one

Track two numbers. Never collapse them into one.

- **Latency** - wall clock, run created to last job finished, queue included. What a person waiting on a PR feels.
- **Machine seconds** - sum of each job duration. Useful work; pool billing also includes idle wall time.

They move independently. Collapsing job fan-out cuts machine seconds and barely touches latency. Adding runners cuts latency and does not touch machine seconds. A single CI time number hides which one moved, so you cannot tell whether a change did what you thought.

One repo over one day of tiering:

```
BEFORE  latency_p50=1261s  p95=5316s  machine_p50=3752s
AFTER   latency_p50= 416s  p95=1192s  machine_p50=2488s
```

Latency fell 67 percent. Machine seconds fell only 34 percent. Most of the work moved tiers rather than disappeared. To cut machine seconds, add a cache. A different runner does not cut it.

## Cost comparison

Prices measured 2026-10-11:

| Provider | 2 vCPU / hour | 4 vCPU / hour | 8 vCPU / hour |
| --- | --- | --- | --- |
| Boat | $0.018 | $0.036 | $0.072 |
| Ubicloud (comparison) | $0.075 | $0.15 | $0.30 |

An always-on pool bills wall time, not job time. Include idle Boxes in the cost.
$1 buys 100,000 Box-seconds. N default Boxes cost N × $0.036 per hour online.
Boat holds private checkouts, so confirm the provider meets the repo's data rules.
Public repos use free GitHub-hosted runners and do not enter this pool.

## Security invariants

- Never copy secret values onto a self-hosted host. The provider injects repository secrets into trusted self-hosted jobs. A secret that lives in a file on the host is a secret that survives the job and is visible to every later job on that runner.
- Never point a public repo at a self-hosted runner. A fork pull request would execute untrusted code on your hardware. Public repos stay on GitHub-hosted runners.
- Keep comment-triggered workflows vendor-hosted, because they execute text an attacker can supply. A persistent host with a warm checkout is the wrong place for `@bot do this`.
- Keep SARIF-upload scanners vendor-hosted. The upload step cannot resolve paths from a self-hosted workspace: it treats the runner home as the artifact root, and a workspace under `/opt/actions-runner` is not a child of that home.

The same split is in [self-hosted-runner-fleet](../self-hosted-runner-fleet/SKILL.md) under "Decide what moves." Follow it here when a cost change argues for moving a job that those rules leave hosted.
