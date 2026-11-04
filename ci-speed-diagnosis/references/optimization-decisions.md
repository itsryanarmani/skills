# Choose and verify a CI optimization

Use this guide after measuring the constraint with [ci-speed-diagnosis](../SKILL.md).
Change one policy or execution layer at a time. Keep the existing gates until their replacement is approved and verified.
This guide records reusable lessons. It does not claim a measured speed or cost gain for another repository.

## Record the baseline

Collect a matched sample before changing triggers, runners, caches, or test selection.
Record source revisions, workload, runner capacity, tool versions, cache state, and sampling dates.
Use at least three matched comparisons for an initial experiment. Report the sample size and its limits.

Keep these measures separate:

- Critical-path latency, including queue time and serial dependencies.
- Aggregate machine seconds across all jobs, including failed attempts.
- Billed usage, including idle pool capacity, cloud services, artifact storage, and review tokens.
- Cost per successfully released change, including repair work and unsuccessful candidates.
- Quality: escaped defects, seeded-fault detection, retries, rollback rate, and time with broken main.

Report p50 and p95 latency only when the sample supports them. Three runs cannot establish reliable tail latency.
A zero GitHub bill for a self-hosted job does not mean zero cost.
A smaller test inventory does not prove a runtime gain. A faster job does not prove a faster release.

## Put expensive work at the right point

First inventory every trigger. Removing PR events does not remove work triggered by pushes to main.
Distinguish these policies before choosing one:

| Policy | Benefit to test | Quality cost to measure |
| --- | --- | --- |
| Cheap checks on pushes; expensive checks at merge intent | Fewer obsolete builds and reviews | Later feedback on expensive failures |
| Broad checks after merge; validated candidate before deployment | Less waiting before landing | Broken main and harder fault isolation |
| Checks only at release | Fewer execution windows | Long feedback delays and larger failure batches |
| LLM review without runtime checks | Less deterministic test work | Unproven defect detection and repair cost |

Start with cheap feedback on editing pushes and expensive validation at merge intent.
Keep focused authentication, isolation, permission, payment, and migration checks before merge initially.
Allow a PR to serve as an automatic change record. Manual ceremony and runtime verification are separate decisions.

For a main-only Cloudflare Preview policy, remove PR Preview triggers only after approving the replacement verification path.
Deploy staging from main. Test an immutable release candidate before production deployment.
Record the exact source, integrated base, review revision, artifact digest, deployment identity, and test results.
An older PR approval does not establish the correctness of a different integrated candidate.
Keep existing PR Preview operator requirements until the scoped policy change replaces them explicitly.

[Anthropic's source-control account](https://www.anthropic.com/engineering/redesigning-source-control)
examines post-merge, pre-deployment verification. It retains automated tests, review, simulations, and telemetry.
Treat it as a design to evaluate against the repository's failures and recovery needs.
It does not establish equivalent quality for an LLM-only workflow in another codebase.

Batch or coalesce obsolete candidates before expensive work. Cancel superseded tests and builds.
Keep publication and migration steps serialized where shared state requires it.
Never cancel a live publication or migration without its documented recovery procedure.
A canary and rollback limit some failures. They cannot reverse every destructive database change.

Use this illustrative compute model:

```text
ratio = n(C + H) / (nC + kH)
n = editing pushes; C = cheap work; H = expensive work; k = final candidate attempts
```

With eight pushes, one final attempt, and 90% expensive work, the modeled ratio is 4.71.
At 98% expensive work, it is 7.02. These are modeled compute reductions, not achieved dollar or latency gains.
Failures, repairs, unequal runner rates, tokens, and cloud fees change the result.

## Level 1: make caching earn its cost

Follow [ci-build-speed](../../ci-build-speed/SKILL.md) for build-cache configuration.
Measure restore, extraction, save, upload, and cold-install time separately.
Compare an exact hit, a miss, and a fresh install on the actual runner.
A green cache step proves neither useful bytes nor reuse by the build tool.

Include the lockfile, relevant configuration, toolchain, platform, and build environment in keys as required by the tool.
Distinguish dependency downloads from compiled outputs. Their compatibility rules differ.
Do not archive the Bun download store merely because another package manager benefits from that pattern.
Retain a cache only when its measured benefit exceeds transfer, extraction, eviction, and maintenance costs.

Keep local persistent stores on fast storage when the trust and cleanup rules permit it.
Keep package stores and workspaces on the same filesystem when installation relies on hardlinks.
Verify the pinned package-manager version's behavior. Cross-filesystem copies can erase the expected gain.
Choose regional object storage only after measuring latency and its full bill.
Retain a scheduled cold verification to detect failures hidden by warm caches.

## Level 3: remove work without removing detection

### Select affected tests

Build selection from the actual base and candidate revisions. Fetch enough history to resolve their relationship.
Include transitive imports, shared setup, configuration, migrations, and generated inputs.
Unknown files, unresolved dependencies, and invalid selection reports must expand to full verification or stop the run.
Never interpret missing or malformed evidence as an empty affected set.

Run selected and full suites in advisory mode before making selection authoritative.
Seed production-shaped faults before implementation. Confirm both paths detect the same intended failures.
Include a corrupt selection control that the validator refuses.
Preserve identities, skips, retries, failures, counts, exit status, raw reports, and source hashes.
Do not claim equivalence from aggregate counts alone.

LLMs can propose affected tests and write missing tests. Validate those proposals through execution.
An approved diff or passing simulation does not prove that the real CLI path works.
Keep broader scheduled verification and an explicit fallback while the dependency map matures.

### Isolate browser execution

Use [e2e-ci-economics](../../e2e-ci-economics/SKILL.md) for browser coverage and sharding decisions.
Give parallel workers separate application processes, database state, ports, users, and artifact directories.
Set worker counts explicitly. Runtime CPU discovery can exceed the job's assigned capacity.

Prove a shared-state negative control fails at the intended assertion after both workers authenticate successfully.
Then prove the same flow passes with isolated state.
A startup error or failed login is not evidence that isolation detection works.
Use stable business assertions rather than timing-dependent element positions.

Measure boot, migration, build, install, and test time separately.
Additional shards multiply setup costs. Parallel execution can cost more and finish later.
Audit duplicated tests, weak assertions, hidden skips, retries, and unobserved failures before adding workers.

### Build once only when inputs match

Record inputs before the producer build. Reject input drift during the build before publishing the artifact.
Do not retroactively seal an existing output as proof of the inputs that produced it.

Bind source identity to actual bytes, file modes, and symlink text. A clean Git index alone is insufficient.
Include tool versions, platform, configuration, canonical compile environment, and relevant dependency inputs.
Use a versioned manifest with deterministic deep serialization that preserves array order.
Reject old protocols explicitly. Test nested tampering: shallow key whitelists can silently omit nested input fields.

Validate consumer inputs before copying outputs or installing dependencies.
Compare known environment values and canonical environment-file content, not only allowed variable names.
Reject unknown compile inputs. Protect secret values in evidence; hashes of low-entropy values can also disclose information.

Resolve and validate physical paths before writing. Reject output links that escape or redirect the destination.
Test dangling links before directory creation, nested link targets, file modes, and changed source bytes.
Keep outside-target sentinel files unchanged in refusal controls.

Move the producer path away before starting consumers. Verify complete output closure and relative WASM or native-module imports.
Run the real business browser cohort against both consumers. Include the shared-database negative control.
Test the actual supported OS and pinned tools. Darwin success does not qualify Linux automatically.
Compare repeated complete baseline and reuse runs, including copying, installation, startup, testing, and cleanup.

## Capacity and runner reliability

Use [self-hosted-runner-fleet](../../self-hosted-runner-fleet/SKILL.md) for the current fleet contract.
Use [high-volume-ci-optimization](../../high-volume-ci-optimization/SKILL.md) for placement and fan-out costs.
Check their current platform sections before applying historical host advice.

Preinstall matching tools when setup dominates. Consolidate tiny jobs when repeated checkout and installation dominate.
Use smaller checkouts only after confirming that selection and builds retain their required history and files.
Separate lightweight checks, heavy builds, and Docker work when their resource needs conflict.
Scale capacity from queue delay, active demand, and idle cost. Do not oversubscribe without contention and flake measurements.

For Boat, use the maintained [runner runbook](https://github.com/pooriaarab/scripts/blob/main/boat-runners.md).
Check the current provider contract before copying API fields or pricing.
Confirm hydration and an accepted running state before heavy work. Reject degraded health; handle an omitted optional health field.
Keep snapshots small and exclude job workspaces and secrets, including new files that ignore rules do not cover.
Retain bounded TTL protection and respect account start limits.

Keep runner sessions ephemeral where supported. A reused machine is not a fresh-machine trust boundary.
Use separate job homes, a stable checkout layout, explicit locale, and consistent Playwright install/runtime paths.
Verify recent Git, noninteractive package installation, service PATH, and stale sparse-checkout cleanup.
Keep Linux tool and browser dependencies in the snapshot or image recipe.

Bound process observation and cleanup. Track owned process groups and preserve diagnostics through refactors.
A successful signal send is not proof of termination. Verify a live positive case before trusting absence.
Treat ESRCH as absence. Treat EPERM as uncertainty; quarantine the resource instead of claiming cleanup.
Retry infrastructure loss separately from real test failures. Preserve the original exit status and reports.

## Level 5: pilot policy changes with recovery

Define a small, reversible cohort. Keep unrelated applications on their existing policy.
Specify the exact landing, staging, candidate-testing, and production gates before changing triggers.
Use immutable candidates so that tests, review, and deployment refer to the same content.
Make failed candidate publication impossible. Keep clear ownership for repair and rollback.

Count failed attempts, review tokens, cloud charges, and repair effort in cost per successfully released change.
Record edit-to-feedback, ready-to-merge latency, broken-main duration, escapes, and rollback outcomes.
Compare against matched baseline traffic. Do not replace missing quality observations with an invented score.

Stop expansion when detection falls, cleanup is uncertain, artifact identity differs, or repair cost exceeds the declared budget.
Keep the last working policy available. Document each exception and its recovery procedure.
A recurring agent audit can propose improvements; it must not silently change gates, buy capacity, or retry genuine failures.
Creating an audit prompt alone does not create a running schedule.

For execution tools and measurement commands, use the linked skills and
[pooriaarab/scripts](https://github.com/pooriaarab/scripts).
Keep private source, host details, credentials, and personal data out of public examples and proof artifacts.
