# Qualify Boat CI changes

Use this reference when moving CI to Boat or changing an existing Boat pool.
The [scripts runbook](https://github.com/pooriaarab/scripts/blob/main/boat-runners.md)
owns setup commands, restore details, and recovery procedures.
Read its implementation gaps before operating the pool.

Sources checked: 2026-10-16. Documentation establishes an interface, not a
successful deployment. Record the installed CLI and pool commit separately.

## Choose the execution model

Start with one sandbox per job for a bounded pilot. Export reports before
cleanup. Keep cleanup unconditional and give the sandbox a finite lifetime.
Use a pool when measured queue demand and account start limits justify reuse.
Use a new JIT runner for each job, even when its machine remains warm.

Start sizing near four vCPUs per job. Treat this as a trial budget.
Measure CPU, memory, queue delay, and explicit test worker counts.
A process can report more CPUs than its assigned CPU set permits.

Scale from queued jobs and usable capacity, with a spending ceiling.
Count a machine only after its readiness checks pass.
Reserve account starts for replacement capacity. Check the current
[limits API](https://docs.boat.dev/api/v1) before a burst.

An idle-state label does not prove that a machine has no active job.
Use leases, process state, and a heartbeat to stop idle machines.
A controller needs both an independent lifetime safeguard and recovery tests.
The existing pool disables automatic stopping; audit its actual safeguards.

## Qualify restored machines

Every normal snapshot restore can download file content after readiness.
Wait for `hydrated: true` before heavy builds or cache writes.
Use a bounded wait and reject degraded health. Record the wait separately.
A hydration percentage is not a completion signal.
See Boat's [readiness contract](https://docs.boat.dev/readiness).

Build runner snapshots from a fresh base. Keep job workspaces out of snapshots.
Verify persistent tool and browser paths after restore.
Check locale, Git, package installation, service PATH, and Docker image retention.
Use the runbook for these checks and their failure symptoms.

Measure any targeted page-cache warming after hydration.
Do not count warm reads as free time or promise a fixed hydration duration.
Run the pilot after a real restore, not only on the image-building machine.

## Prove job isolation

Use separate job state for concurrent consumers: HOME, writable caches,
workspace, database, ports, credentials, and process ownership.
Keep compiler paths stable where cache identity requires them.
Stable paths do not permit concurrent writes to the same job state.

Write failure controls before changing the executor.
Prove that one consumer cannot read another consumer's seeded data.
Prove the positive case through the real application and database.
Record expected case identities, actual outcomes, and cleanup evidence.
A supervisor exit alone does not prove that child processes are gone.

On a reused machine, check sparse checkout, old services, and writable state.
A failed cleanup must prevent that machine from accepting another job.
Do not describe a persistent pool as disposable isolation.

## Remove work only after proving equivalence

Audit the slow tests before adding shards. Check setup cost and shared state.
Use [E2E economics](../e2e-ci-economics/SKILL.md) for that decision.
Parallel execution can increase wall time when each shard rebuilds the app.

Run affected-test selection beside the full suite first.
Compare actual file coverage, case identity, duplicate counts, and outcomes.
Inject a real failure in affected code. Both paths must detect it.
Refuse unknown reports, incomplete runs, unexplained skips, and missing files.
Keep full execution when dependency edges or changed inputs remain unknown.
Agent suggestions can propose selection; measured coverage must authorize it.

Reuse a build only when all relevant inputs match.
Include source, lockfiles, configuration, tool versions, environment, and paths.
Separate runtime values only after proving they do not affect compiled output.
Test two independent consumers after the producer becomes unavailable.
Preserve payload hashes and link targets. Reject links into the producer.

Cancel superseded verification jobs. Fence stale deployment work by commit.
Preserve migration and release ordering. Keep the existing merge gates while
qualifying selection, reuse, or scheduled verification.
Apply the [existing merge gates](SKILL.md#prove-savings-before-fleet-rollout).

## Report comparable results

Record queue, restore, hydration, setup, build, test, export, and cleanup time.
Include machine idle time, failed starts, storage, and transfer in cost estimates.
Measure cache restore plus save against a fresh install on that provider.
Keep a cache only when its full measured cost is useful.

Use several matched runs on the same commit, toolchain, and machine size.
Report sample size, dates, medians, spread, and any regressions.
Separate local proof, Boat proof, historical samples, estimates, and invoices.
A faster test phase is not an equal reduction in total CI time.

Report both ratios explicitly:

- Speed ratio: comparable old elapsed time divided by new elapsed time.
- Cost ratio: comparable old total cost divided by new total cost.

The supplied October 2026 experience report contains observations from other
repositories. Its timings, region, and bandwidth are not this campaign's results.
Remeasure those properties before making a deployment or cost decision.

Stop at a failed qualification. Preserve its command, raw reports, exact inputs,
and result. File a reproducible issue before expanding the rollout.
Do not buy capacity or send a vendor report without the owner's authorization.
