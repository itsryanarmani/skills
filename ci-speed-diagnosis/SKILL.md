---
name: ci-speed-diagnosis
description: "Use when CI is slow even though the optimizations are already on (a remote cache, a green actions/cache step, a sharded suite), to find why they do nothing before adding more."
---

# ci-speed-diagnosis

A slow pipeline usually has the right optimisations already. They are configured, they report
green, and they do nothing. **Diagnose the silence first. Add levers last.** Each defect below
was found this way, and each one hid behind a green check.

## When to use this

- **Triggers:** 'CI is still slow', 'the cache never hits', 'Remote caching disabled', 'our cache is empty', 'CI cache quota is full', 'make CI faster', 'why did that optimisation not help'.

**Use this skill** when someone already added caching, a remote cache, or sharding, and CI is
still slow. Also use it before you buy a bigger runner.

**This skill is the entry point of the CI family.** It finds the constraint. The siblings hold the
levers. Route by what you already know:

| You know | Go to |
| --- | --- |
| nothing yet — CI is just slow | stay here, and run the steps below |
| the pipeline has no caching at all | [ci-build-speed](../ci-build-speed/SKILL.md) |
| the long pole is a browser E2E job | [e2e-ci-economics](../e2e-ci-economics/SKILL.md) |
| the proposal is affected-test selection, report reading, or a relocated build | [ci-selective-evidence](../ci-selective-evidence/SKILL.md) |
| jobs are on the wrong runner tier, or queueing behind each other | [high-volume-ci-optimization](../high-volume-ci-optimization/SKILL.md) |
| the suite runs on every pull request — the trigger is the repeated cost | [ci-cost-at-agent-scale](../ci-cost-at-agent-scale/SKILL.md) |
| the problem is spend, and agents open most of the pull requests | [ci-cost-at-agent-scale](../ci-cost-at-agent-scale/SKILL.md) |
| the constraint is named and you must pick a tactic with its measured cost and trap | [ci-speed-and-cost](../ci-speed-and-cost/SKILL.md) |
| you are setting up the host itself | [self-hosted-runner-fleet](../self-hosted-runner-fleet/SKILL.md) |

## Match CI conditions before local checks

A step command alone does not reproduce CI. Match its execution conditions before benchmarking or diagnosing a failure.

1. Read the workflow at the tested revision. Resolve inherited settings from reusable workflows, composite actions, matrix entries, and package scripts.
2. Record the effective workflow, job, and step environment, including `CI`, `NODE_OPTIONS`, and service URL variable names.
   Supply values privately. Never copy secrets into logs or public evidence.
   Check whether `ci:local` includes these settings; a script name does not prove that it does.
3. Record the working directory, lockfile, tool versions, and browser installation.
   Check which binaries `PATH` and `bunx` actually select. Setup action versions alone do not prove command resolution.
4. Match CPU, available memory, heap limits, disk space, and test worker counts to the CI job.
   An 8 GB Box does not reproduce a 16 GB runner.
   A 2 GB Node heap does not match a CI step that sets `NODE_OPTIONS=--max-old-space-size=4096`.
5. Start the declared services with matching versions, ports, and local credentials.
   Confirm readiness with a positive control, such as a successful database query from the test context, before running dependent checks.
   A missing PostgreSQL service or test URL cannot establish a source regression.

Preserve the first failure logs, tested revision, command, resource readings, and non-secret configuration evidence.
Correct missing local conditions before changing source code or workflow limits.
Retry only the affected checks to diagnose the mismatch. Keep their results beside the original failure evidence.
Then run the complete required local gate with matching conditions before every push.
Report unresolved differences. Attribute a failure to source only after the relevant execution conditions match.

For trigger changes, affected tests, build reuse, and post-merge experiments, read
[Choose and verify a CI optimization](references/optimization-decisions.md).
It gives the shared evidence and recovery rules before a sibling changes execution.

## Diagnose in this order

Do not skip a step. Each one stops you from optimising a job that does not matter.

1. **Name the metric.** Report queue time, execution time, and summed machine-seconds separately.
   Record push-to-gate latency too. Jobs can overlap or wait on dependencies.
   Machine-seconds measure compute use. Billed cost also depends on rates, rounding, and included minutes.
   `ci-pr-latency` reports run-created-to-last-finish latency and summed job durations. Its latency includes waits.
   It does not split queue time or report billed cost. Its money label is not billing evidence.
   Read run `created_at` and job `started_at`/`completed_at` timestamps from the Actions API.
   Execution is `completed_at - started_at`. Run creation to job start includes dependency waits and scheduling delay.
   Separate dependency waits before labeling the remaining wait as queue time. Mark unknown splits as unknown.
   Use billing records for money.
2. **Name the critical path.** Trace job dependencies and queue waits through the final required check.
   Write the per-job medians down. A win outside that path buys machine time only.
   Tool: `ci-job-timings`. **Also check whether the long pole can fail the run.** A job with
   `continue-on-error: true` gates nothing, so time spent there buys nothing — see
   [e2e-ci-economics](../e2e-ci-economics/SKILL.md), where the longest job in two pipelines was
   exactly that.
3. **Prove the caches save time.** Compare cache overhead with a clean install, as described below.
   Read the job logs for payload size, primary-key hit rate, and
   remote-cache state. A cache that restores 0 bytes still prints a green success line.
   Tool: `ci-cache-health`. **A primary-key hit is not proof the build used it** — a build tool
   can discard a correctly restored, correctly sized pack over a build dependency the key
   missed (see the checklist below). `ci-cache-health` cannot see that decision; it happens
   inside the build tool, after the restore succeeds. Cross-check against `ci-job-timings`: a
   reported hit next to a duration matching the cold-build baseline is the tell.
4. **Read the guards inside the long-pole job.** See the next section. This is where the time
   usually is.
5. **Only now add a lever.** Spend on the critical path, in the sibling that owns it:
   `ci-build-speed` for the build, `e2e-ci-economics` for a browser suite,
   `high-volume-ci-optimization` for job placement, `ci-selective-evidence`
   for affected-test selection, report reading, and relocated builds.

## Compare cache cost with a clean install

A successful cache restore can cost more than the work it avoids. A high hit rate does not prove a saving.

1. Record archive bytes, restore time, decompression time, install time, and post-job save time.
   If restore time includes decompression, record that boundary. Do not count decompression twice.
2. Compare restore plus install plus save with a clean install on the same runner type.
   Include cache misses and unchanged-key hits. An unchanged-key hit usually skips saving.
3. Use the same commit, lockfile, package manager version, and install flags for both paths.
   Start each clean measurement without `node_modules` or a package store.
4. Inspect the cache path before restoring it. Preloaded runners can hold packages from unrelated projects.
   Measure directory bytes and archive bytes separately. Record whether the store belongs to the job or the image.
5. For a cold Bun benchmark, set [`BUN_INSTALL_CACHE_DIR`](https://bun.sh/docs/pm/global-cache) to a fresh directory under `RUNNER_TEMP`.
   Leave it empty before install. Do not clear a shared runner store.
   Use a fresh job store in production only when the pilot shows a slower restore or preloaded store.
   For explicit restore or save on an ephemeral runner, use the same directory as install.
   Keep a scoped persistent warm store when measurements favor it. Keep it outside the workspace and `RUNNER_TEMP`.
   Follow [persistent runner cache rules](../high-volume-ci-optimization/SKILL.md#caches-must-live-outside-the-workspace).
   Do not archive the persistent store with `actions/cache`.
6. Pilot the smaller cache or uncached install in CI. Keep the existing tests and failure checks.
   Compare repeated successful runs before a wider rollout. An isolated install benchmark does not prove a CI speedup.

Record the run URLs, runner type, cache state, sample count, and measurement window with each result.
Keep private repository details in private evidence. Publish only results approved for public use.

## The bug shape that repeats: one host's mitigation, every host's cost

This was the single most common defect. Someone measures a real constraint on one machine,
writes a mitigation, and applies it unconditionally. The mitigation then runs on machines that
never had the constraint, where it is pure cost.

Four instances in one codebase:

| Guard | Written for | Cost where it does not apply |
| --- | --- | --- |
| `config.cache = false`, gated on `!dev` | an 8 GB container | kills the webpack cache on a 31 GB runner |
| `--max-old-space-size=6144` | a small container | caps the heap far below available memory |
| `cpus: 1` worker cap | a contended host | serialises a build that has cores to spare |
| a swap-creation step | a runner with no swap | writes a swapfile nothing reads |

**Symptom to look for:** a guard whose comment explains a real constraint that does not exist on
the machine now running it. The comment is usually true and usually stale.

**Rule:** gate a mitigation on the constraint, measured at run time — available memory, core
count, free disk. Do not gate it on `!dev`, on a branch name, or on a number someone typed once.

## The silent-defect checklist

| Defect | What you see | Fix |
| --- | --- | --- |
| The secret holds an empty value | one grey line, `Remote caching disabled`, then cold misses forever | Set it from a file: `gh secret set NAME -R owner/repo < file`. `--body -` does **not** read stdin. It stores the literal string `-`. |
| The task runner runs tasks in strict env mode | a nested `turbo run` never caches, because `TURBO_*` is stripped from child processes | Declare the variables in `globalPassThroughEnv`. Pass-through values do not join the cache key — a dummy token gives an identical task hash. |
| The output glob sweeps the incremental cache | `.next/**` includes `.next/cache`, so the artifact reaches 1.2 GB and its upload fails without an error. The task can then never hit. | Exclude it: `!.next/cache/**`. This took one artifact from 1.2 GB to 9.1 MB, and the job from 204s to 34s. |
| The cache server buffers the whole body | uploads over roughly 20–30 MB fail | Stream `request.body` to storage instead of `await request.arrayBuffer()`. A 50 MB object then round-trips byte-identical. |
| The deployed server is behind its source | the fix is in `main`, and production still fails | **A fix in `main` is not a fix in production.** Deploy, then re-verify against the live URL. One build stayed stale for two hours behind the fixed source. |
| Caches are ref-scoped and saved on every PR | the quota fills with byte-identical copies of one key. One repo held 9.11 GB against the 10 GB limit, of which 7 GB was duplicates. | Gate `actions/cache/save` to the default branch. Let pull requests restore through `restore-keys`. |
| Every `restore-keys` level embeds the lockfile hash | a dependency bump invalidates the primary key **and its only fallback** together | Keep one fallback level that does not depend on the lockfile. |
| Prettier runs with the default `--cache-strategy metadata` | the cache never hits in CI, because it compares mtime and `actions/checkout` rewrites every mtime | Use `--cache-strategy content`. |
| `outputFileTracingExcludes` is keyed on `"*"` | a second, mis-rooted trace pass re-reads 368 MB of JSON across 610 manifests and drops zero entries | Key it on `"next-server"`. |
| The cache key is missing a build dependency (e.g. a config file) | an exact primary-key hit, yet the build compiles fully cold, because the tool sees the dependency changed and discards the pack. The save step then skips (it gated correctly on `cache-hit != 'true'`), so the stale entry never repairs itself | Put every input the build tool treats as a dependency into the key. See [ci-build-speed](../ci-build-speed/SKILL.md#1-cache-everything-biggest-safe-win-near-zero-risk) for the full incident. |

## Measurement discipline

**Measure a CI change in CI.** A laptop understated an I/O-bound win by 6x — 20s locally against
65–70s in CI, because a laptop NVMe hides 368 MB of JSON reads. Contention lies in the other
direction: a baseline taken while parallel agents drove the machine to load 65–160 read 1071s for
a suite that runs in 125–131s on a quiet machine, an 8x inflation.

**When CI is unavailable, record wall time and CPU time (user+sys) separately.**
Record host load too. Downloads, disk waits, and decompression can dominate cache work.
CPU time alone cannot measure that overhead. Mark the result as an isolated benchmark.

**Verify behaviour, not inventory.** The cache-list API showed no entries while the job logs
proved the same caches saved and restored correctly. A log line is ground truth. A listing API is
a claim.

**Say which number you bought.** A change off the critical path buys machine time, not latency.
Both are valid. Claiming the wrong one is not.

**Parallelism beats per-job speed.** A self-hosted host was the fastest tier per job — 43s median
against 50s hosted — and still lost. It ran a fixed number of runner services, so everything else
queued: 46–52s median queue against 2s hosted.

**Sharding does not make a suite faster on its own.** Three shards took about 150s against about
128s in a single process, because every shard pays the fixed setup cost in full. Sharding buys
overlap with other checks, and survival under load: at load ~280, one process took 1090s against
301s for three shards.

## What good looks like

One campaign over four pipelines, all measured before and after: CI wall clock fell 82%, 46% and
32% on three repositories, and the local pre-push gate fell 51%. Almost none of that came from a
new lever. It came from making the configured ones actually run.

## Tools

`ci-pr-latency`, `ci-job-timings`, `ci-cache-health` and `ci-runner-audit` in
[pooriaarab/scripts](https://github.com/pooriaarab/scripts) cover steps 1 to 3 and job placement.
Run them in that order.

## Release pipelines share capacity

Trace the release gate through the final deployment, including other workflows on the same runner pool.
A fast deployment command can still wait behind unrelated test shards.

- Record overlapping queue, pull-request, release, and deployment runs.
- Separate dependency waits from scheduling delays. Do not label the entire pre-start interval as runner queue time.
- Check actual concurrent jobs against available slots. A matrix limit does not create runner capacity.
- Remove a job dependency only when the downstream job reads no upstream output or required side effect.
- Preserve the final gate's dependencies when independent build and planning jobs start together.
- Report the cost of queue caps. A permanent cap also slows merges when the pool is idle.
- Compare merge latency and release latency together before keeping a capacity change.

Parallel side-worker deployments need independent build directories and no ordering dependency.
Wait for every child process, including siblings of a failed child. Name each failed worker and return failure.
Prove this with an early failing child and a slower successful sibling.
Do not start live smoke checks after a failed deployment.

Check tests that inspect workflow text after shell changes, including quoting changes.
A passing workflow parser does not prove those assertions still pass.

Use the [release measurement runbook](https://github.com/pooriaarab/scripts/blob/main/ci-release-evidence.md)
to record comparable runs. Keep estimates separate from observed release results.
