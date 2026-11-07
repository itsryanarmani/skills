# Choose where CI proof runs

Use this reference when broad CI repeats work already done locally or during
deployment. Use the [scripts runbook](https://github.com/itsryanarmani/scripts/blob/main/ci-cost-controls.md)
for commands, pool drains, billing evidence, and the cutover checklist.

## Keep the scheduler and compute choices separate

GitHub Actions can schedule private jobs on a warm Boat pool. The native Boat
CI integration is separate. Verify pool hooks, labels, and a real job before
suspending that integration. Keep public fork code off private runners.

Keep private builds on the qualified pool. Consider small hosted metadata jobs
from their measured cost. Read current billing rules and account usage before
changing placement. A hosted exception does not authorize a fleet migration.

## Qualify the development path

1. Verify the local push gate covers the changed inputs.
2. Retain cheap secret and PR policy checks.
3. Confirm deployment builds the actual revision and runs its smoke checks.
4. Remove the repeated generic build and wait from that development path.
5. Keep broad checks available manually and on required production candidates.
6. Verify a real merged deployment before reporting cutover complete.

Keep required operator walks and independent reviews. Bind proof to the exact
revision and external dependency inputs. Local proof alone does not establish
that concurrent changes compose. Keep checks on the actual production candidate.

Use short branches and small changes. Merge additive migrations first. Use
feature flags for incomplete flows. Share site rules through code and config.
Keep PRs as concise evidence records under the repository's existing rules.
Test results are repeatable evidence, not formal proof of every behavior.

## Preserve production guards

Bind a production result to both its branch and revision. A green development
run on the same revision does not satisfy a production suite.

When development deliberately skips a wait, handle skipped dependencies
explicitly. Accept that skip only on the qualified development branch. Block
production on a skipped, failed, or cancelled wait. Block new deployment stages
on workflow cancellation. Preserve planner failures, required canary failures,
empty matrices, environment restrictions, migrations, and serialization.

Keep queue candidate verification where a queue exists. Choose a queue from
measured contention and integration risk. Use an event-driven handoff when it
preserves the same production checks without holding a runner for polling.

## Isolate deployment work in shared pools

Broker claim order does not reserve a GitHub job. GitHub can assign another
matching job to a JIT runner in the same repository. Use an exclusive job label
when deployments must avoid browser work. Issue the runner with only that label.

Keep pool request labels separate from job queue labels. Reject mixed labels
that the issued runner cannot satisfy. Bound priority so ordinary jobs continue
to progress. Preserve FIFO order within each class, retry backoff, active leases,
private-repository checks, and completed-parent checks.

Verify the actual registered runner labels and useful job result. A successful
code deployment does not prove that a live Durable Object uses the new version.
Check a positive behavior before activating workflows that require the change.
The [broker runbook](https://github.com/itsryanarmani/scripts/tree/main/workers/boat-runners)
describes one implementation. It does not establish capacity for another fleet.

Retire obsolete checks after verifying their revision is included in the current
candidate and they no longer gate delivery. Inspect active jobs before cancelling
a run. Preserve required candidate checks and active deployments.

## Keep proof without paid review calls

Disable inference workflows and their label triggers when paid review is not
authorized. Verify that every matching active workflow is disabled. Retain a
deterministic gate for reviewer identity, verdict, and evidence. Confirm that
the gate exists before claiming that PR standards enforce review proof.

Run a required independent review through an authorized seat or hub. Record its
identity and verdict. Do not revoke a shared model key until its consumers are
mapped. Tests and workflow policy changes still need their existing review.

## Drain capacity without losing useful work

Stop automatic resume loops before stopping idle campaign machines. Use a
supported drain mechanism to pause new leases. Check actual worker processes
and leases immediately before stopping a machine. Restore acquisition on error.

Provider state `idle` is insufficient. A JIT runner can execute another job
besides the job that obtained its lease. Preserve active workers and independent
leases. Check stopped-file retention and snapshot allowances.

Default new task machines to the smallest qualified size with a bounded TTL.
Keep larger machines for measured resource needs. Verify useful work on the
retained pool. Measure queue delay and idle cost after each capacity change.

## Report separate results

Record machine time, starts, snapshot charges, review inference, and hosted
storage. Record plan credit and wallet settings separately. Count included
compute once. Keep raw evidence private.

Report delivery latency, occupied machine seconds, and billed cost separately.
Reducing job work frees capacity; fixed pool cost falls only when online time
or machine count falls. A short observed rate is not a monthly invoice result.
Keep retry failures visible. Preserve the previous plan for rollback.

Batch recurring site probes when they share a runtime. Keep per-site receipts,
bounded concurrency, and child deadlines. Missing or incomplete evidence stays
unknown or failed; it never becomes a pass.
