---
name: cloudflare-cost-audit
description: Audit Cloudflare spending across services and reduce D1 row costs. Use for unexpected bills, costly SQL, preview resource growth, or proposed table consolidation. Report a dollar figure only from the latest cumulative usage row. Keep MEASURED savings separate from TARGET estimates.
---

# Cloudflare cost audit

Attribute the bill before changing the schema. Keep savings targets separate from measured savings.

## Report dollars from the latest cumulative row

Do not sum daily rows of the billable-usage feed. The feed holds cumulative and overlapping rows. A per-day sum can look like a large daily bill and still mean nothing.

Use the latest cumulative row per service, subscription, zone, and billing period. Report a dollar figure only from that reduction.

Keep two columns. Never call a target a measured saving.

| Column | Meaning |
| --- | --- |
| MEASURED | Dollars from the latest cumulative row. Reconcile them to the invoice when the invoice exists. |
| TARGET | A plan estimate. It is not a saving. |

The billing feed lags. It can have no rows after a change. Wait for new data before you claim a saving.

## Price the meter before the fix

Compute dollars per unit before you pick a fix. One KV write can cost about as much as 5,000 D1 rows read. A cache that writes once per long-tail key can cost more than the query it saves.

These paths drive a bill of this shape: facet `COUNT` scans, per-request server render, and visitor-driven cache writes. Fix them in this order:

1. Pause the costly search.
2. Stop the staging workload.
3. Precompute the counts.
4. Serve static pages.
5. Add one budget guard in front of HTTP, the CLI, and MCP.

Put the guard at the shared entry point. Every interface reaches that point, so one limit covers every path.

## Establish the baseline

1. Read the repository rules and Cloudflare binding configuration.
2. Load credentials through the approved credential tool into process environment variables.
3. Save raw responses outside Git in a private directory.
4. Record the account, UTC interval, billing period, currency, and collection time.
5. Collect invoices, subscriptions, and usage for every paid service.
6. Record missing permissions and unavailable metrics as gaps.

Complete this stage when each charge has a service owner or an explicit investigation gap.
Resource counts alone cannot explain a bill.

## Collect complete evidence

Use the installed `cloudflare-cost-audit` command for D1 inventory, row analytics,
and an optional raw current-period billing snapshot.
Run `cloudflare-cost-audit --help` and read the command contract supplied with the tool.
It does not audit all Cloudflare services or calculate invoices.

- Follow actual pagination metadata, including cursors and next-page fields.
- Treat requested page size as a request, not proof of completion.
- Fail when GraphQL results reach the selected limit.
- Include historical database IDs in analytics attribution.
- Treat inventory collection as a nontransactional snapshot.
- Map resources to repository, environment, branch, and last known owner.

Keep billable `rowsRead` and `rowsWritten` separate from SQL query counts.
Match usage to its billing interval before calculating a cost estimate.
The calendar month and subscription period can differ.

Do not sum daily rows. Follow "Report dollars from the latest cumulative row" above.
Group by service, subscription, zone, billing period, and currency when those fields exist.
High-water charges can repeat across days. Reconcile MEASURED amounts against the invoice.
Label a TARGET as a plan estimate. It is not a measured saving.

Complete this stage when every inventory page and analytics limit has an explicit completion check.

## Measure expensive paths

1. Rank databases by billable rows, then map expensive queries to application callers.
2. Capture the query, parameters, result size, query plan, row counters, and latency.
3. Use representative data and the same workload for each comparison.
4. Inspect repeated aggregate scans, broad updates, polling, imports, and cron jobs.
5. Inspect indexes, triggers, FTS maintenance, and conflict updates for write amplification.
6. Separate request overhead from database execution time before changing batching.
7. Capture row counters for statements invoked through `.run()`, `.first()`, `.all()`, and each `.batch()` result.
   Instrument execution when a return type does not expose metadata.
8. Keep calls, reads, writes, R2 PUTs, and result correctness as separate measures.
   Inspect actual query plans when fewer calls increase read work.
9. Freeze source and workload, warm both arms, alternate paired runs, and retain every sample and failure.
   Recheck source identity after collection and record timing interference.
10. Report read-cost and latency tradeoffs separately.
    Keep local service measurements distinct from HTTP latency, production observations, and invoice savings.

Prefer bounded queries, selective indexes, fewer repeated scans, and writes that skip unchanged rows.
Measure each proposal before broad schema changes.
An index can lower read costs while increasing write costs.

Complete this stage with a reproducible before-and-after artifact for each changed query path.
Record billable rows, latency, workload size, and result equivalence.

## Change structure only with evidence

List every table, reader, writer, foreign key, trigger, index, and retention requirement.
Treat an empty or unfamiliar table as unclassified until its owners are checked.

For JSON or JSONB proposals, probe supported functions on the target D1 engine.
Measure filtering, indexing, updates, row counters, and migration effects with representative records.
Keep independently queried or constrained fields searchable and enforce their invariants.
Choose structure from access patterns and measured costs, not table count.

Before removal, export the affected data and restore it into an isolated database.
Compare row counts and important relationships after restoration.
Prepare rollback steps and identify the deployment that stops old writes.
Do not delete data until restoration succeeds and callers no longer depend on it.

Complete this stage when migration, restoration, and the application flow pass on an isolated copy.

## Control recurring waste

Check preview creation, close-event cleanup, failed-build cleanup, and age-based retention.
Bind cleanup to verified resource ownership. Preserve active environments and shared bindings.
Measure retained resource cost separately from historical usage.
Removing a database does not reverse its earlier charges.

For container changes, prove actual running-to-stopped state through the provider API.
A skipped cron log proves skipped dispatch, not sleep or lower billed usage.
Record the installed SDK version and the last observed reset before timing inactivity.
A reset can renew an in-memory timer without changing the deployed Worker version.
Keep setup, reset observation, positive wake tests, and cleanup inside one fixed experiment budget.
Keep Preview app checks separate from isolated lifecycle timing and production savings measurements.

For temporary resources, use the bounded cleanup procedure supplied with your audit tools.
Require an independent deadline guard, durable ownership, and exact resource absence checks.
Complete the experiment only after exact owned resources are absent or cleanup remains explicitly incomplete.

Use the repository's PR review, local CI, preview walk, and release procedure.
Report measured savings after equivalent observation intervals.
Do not claim a saving until the billing feed has a new cumulative row.
Include remaining gaps and costs that the change cannot affect.

Primary references:
[D1 billing](https://developers.cloudflare.com/d1/observability/billing/),
[D1 metrics](https://developers.cloudflare.com/d1/observability/metrics-analytics/),
[billable usage](https://developers.cloudflare.com/api/resources/billing/subresources/usage/methods/paygo/).
