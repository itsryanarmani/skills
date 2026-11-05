# Cost cuts, one by one

This file lists each cost cut that was tried on a fleet of about 50 Next.js sites
on Workers (OpenNext, D1, KV). `SKILL.md` has the method and the ranking.

Each entry has four parts:

1. **Signal.** What to search for in a repo.
2. **Change.** What to do.
3. **Proof.** The number and how to measure it. MEASURED means billing data,
   analytics or a test run. ESTIMATE means a calculation.
4. **Trap.** What fails, or the counter-example.

Never present a target or an ESTIMATE as a measured saving. If an entry has no
number, the entry says so. Compare the SAME hours across days before you credit
any change. Traffic moves the meters more than most code changes do.

## Workers CPU

### Turn off Wrangler `minify`

- **Signal.** `git grep -n "minify" -- '*wrangler*'`. The signal is `minify: true`. Wrangler's default is false.
- **Change.** Set `minify: false` on one site. Read `cpuTime` from the tail.
- **Proof.** Local cold CPU fell 32% to 42% (MEASURED, local workerd).
  A small production A/B on cold requests (4 on the old bundle, 5 on the new one)
  showed a large drop (MEASURED, small samples, not reproducible from the kept logs).
  Fleet CPU per request did NOT change: 71.5 ms on both days, same hours (MEASURED).
  Treat the saving as **unconfirmed**.
- **Trap.** Cold samples are few and noisy. Fleet CPU per request depends on the
  hour of day. Compare the same hours across days before you credit the change.

### Cut bytes in the server bundle

- **Signal.** The handler file is large. The one measured here was 25.7 MB. Run `ls -l .open-next/server-functions/*/handler.mjs`.
- **Change.** Find modules that the bundler copied into each route group. Share them.
- **Proof.** About 55% of a 642 ms first request was V8 compile time for a 25.7 MB
  handler (MEASURED, local profile). Measure with `wrangler tail --format json`
  and read `cpuTime`.
- **Trap.** Lazy `import()` does not help. OpenNext inlines dynamic imports.

### Fewer requests cut CPU by the same share

- **Signal.** CPU per request is flat while requests fall.
- **Change.** Cut requests (see Workers requests below).
- **Proof.** Requests fell from 1,475,049 to 710,688 in the same hours on two days.
  CPU fell by the same share (MEASURED). The drop came from fewer requests,
  not from cheaper requests.
- **Trap.** Do not credit a code change for a drop that traffic explains.

## Workers requests

### Turn off RSC prefetch on public links

- **Signal.** `git grep -n "<Link" -- '*.tsx'` with no `prefetch={false}`.
  In logs, many URLs carry `?_rsc=`.
- **Change.** Make the shared `Link` component default to `prefetch={false}`.
- **Proof.** `_rsc` requests fell from 9% of one site's traffic to 0 (MEASURED).
  Count them with `httpRequestsAdaptiveGroups`, filtered on the query string.
- **Trap.** Prefetch is a user feature. Turn it off only on public pages that
  bots visit.

### Refuse a bare `_rsc` request

- **Signal.** The Worker entry has no check for the `RSC` header.
- **Change.** A request with `?_rsc=` and no `RSC` header gets 404 with
  `Cache-Control: no-store`. Put the check first, before cache and render.
  Cover GET and HEAD.
- **Proof.** No number was measured for this change alone. Count 404 responses
  with the `_rsc` parameter before and after, in the same hours.
- **Trap.** A real router request sends both. Test that a real request still
  gets 200.

### Block an empty `User-Agent` on the edge

- **Signal.** Analytics show one IP, or one empty user agent, with a large share
  of a zone's requests.
- **Change.** A zone custom rule that blocks an empty `User-Agent` outside `/api/`.
  Use a stable rule `ref`. `SKILL.md` has the safe steps.
- **Proof.** One IP with an empty user agent sent 43% of one site's requests, and
  another sent 60% of a second site's (MEASURED, analytics). Count blocked
  requests in `httpRequestsAdaptiveGroups` by action.
- **Trap.** A `PUT` to the entrypoint replaces all custom rules. Save the old set
  first. Check for an uptime monitor, a webhook or a health check that sends no
  user agent. These can sit outside `/api/`.

### Pause search jobs, staging and idle sites

- **Signal.** Cron triggers or sync jobs that run on sites with no users.
- **Change.** Pause them. Shut down staging that nobody reads.
- **Proof.** One big drop (D1 reads from 97B to 2.5B a day) came from a search
  pause, 12 hours before the code changes that we first credited (MEASURED).
- **Trap.** A per-minute cron on every site was a small share of CPU (about 1%,
  ESTIMATE). Measure before you spend work on a cron.

## KV writes

KV writes per hour is the check for any KV change. Query
`kvOperationsAdaptiveGroups` with the dimension `datetimeHour`. Filter on
`actionType` write. Compare the same hours across days.

Measured here: about 40,000 writes an hour on one day, and about 9,500 an hour
from 04:00 UTC on the next day (MEASURED). The fall came before the minify change
and the city page change below. No cut was tied to it. A test found no write spike
after a fleet deploy (MEASURED). So the idea that a deploy empties the data cache
and causes a write wave is not supported.

### Skip the data cache for long-tail keys

- **Signal.** `git grep -n "unstable_cache\|cachedIf" -- '*.ts' '*.tsx'`. Look
  for key arrays that hold a request value: filters, a page number above 1, or
  free text.
- **Change.** Cache only head pages. Call the loader directly for the tail.
  Each put to the incremental cache is a billed KV write.
- **Proof.** 98% of geo page requests were unique within 3 minutes (MEASURED).
  In a key sample from the two largest writers, 99% of keys were data-cache
  entries (MEASURED). Writes divided by keys were 1.04 and 2.14.
- **Trap.** Check every caller of a cache rule you change. A first version made a
  head page's nearby search uncached. Pass an explicit head flag from that page.

### A city page is long tail, not head

- **Signal.** A page keyed by place that many places share, with a cache call
  for each place.
- **Change.** Treat the place page as long tail. Keep the cache on the listing
  page's shared block.
- **Proof.** A cold city page wrote 3 to 5 KV entries (3 once the region keys
  were warm). It saved about 9 D1 queries per later hit (MEASURED, test run).
  The sum (ESTIMATE): 3 to 5 writes at 5,000 row reads each cost 15,000 to 25,000
  row reads. Each hit saves about 9 queries of 319 rows, about 2,900 rows, minus
  the 500-row read fee, so about 2,400 net. The entry needs about 6 to 11 hits in
  its window. A city page rarely gets that many, so it is long tail.
- **Counter-example.** The listing page reads the same block on every visit. It
  keeps its cache. Apply the break-even rule below to decide.

### Break-even rule: write to KV or read from D1

- **Signal.** A new cache entry that stores a D1 result.
- **Rule.** One KV write costs $0.000005. One D1 row read costs $0.000000001.
  So one write equals 5,000 row reads ($0.000005 / $0.000000001).
  Each cached read costs the KV read fee: $0.0000005, about 500 row reads.
  Net rows saved per hit = rows saved per read minus 500.
  Writes to pay back = 5,000 / net rows saved per hit.
  A D1 read query read 319 rows on average (MEASURED: 7,952,705 queries read
  2,533,957,103 rows in one day). An entry that saves about 1,000 rows a read
  (about 3 queries) nets 500 and needs about 10 reads in its window. An entry
  that saves about 16 queries (about 5,100 rows) nets 4,600 and needs about 1.1.
  So the bigger the load, the fewer reads you need.
- **Proof.** The arithmetic above, from the price table (ESTIMATE for your own
  load size). Measure your own rows per query with `d1QueriesAdaptiveGroups`.
- **Trap.** The window starts at the write. A key read once is a loss.

### Set a per-site data cache window

- **Signal.** A constant cache window shared by data and pages.
- **Change.** Read the window from one setting per site. Default 300 seconds.
  Clamp it between 60 and 86400. Add a revalidate route for imports.
- **Proof.** No saving was measured for this change alone. A longer window helps
  little when keys are mostly distinct (writes divided by keys was 1.04 and 2.14).
  Check writes per hour before and after.
- **Trap.** Audit every write path for a revalidate call before you lengthen the
  window.

## KV reads

KV reads were $1.00 on the day KV writes were $5.00 (MEASURED, billing feed). No
read cut was measured in this work. Do not cut reads at the cost of writes or D1.

### Serve the sitemap index from KV, stale-safe

- **Signal.** The sitemap index runs a count query on each request.
- **Change.** Store the index in KV. Serve a fresh copy with no D1 read. Serve a
  stale copy at once and rebuild in the background. Serve a degraded copy built
  from config if nothing is stored. Mark it and send `no-store`.
- **Proof.** Not measured as a separate number. It moves reads from D1 to KV. Weigh
  it with the break-even rule. One KV read costs $0.0000005, a tenth of a write.
- **Trap.** Never let the edge cache store the degraded copy.

## D1 rows read

### Find the query families first

- **Signal.** You do not know which queries read the rows.
- **Change.** Group by query. Query `d1QueriesAdaptiveGroups` for a time window.
  Use the dimensions `query`, `databaseId`. Sum `rowsRead` and `count`. Sort by
  rows read. Map database ids to names with the D1 list API.
- **Proof.** Families found in one 16-hour window (MEASURED):
  - A category-tree recursive CTE with `json_each(?)` and `MATERIALIZED`:
    173M rows, 166k runs, six databases, 550 to 190,000 rows a run.
  - A full-row licences select: 65M rows, 11k runs, one database, about
    9,400 rows a run. This is a full scan.
  - A listing rows page: 52M rows, 4k runs.
  - Five facet-count queries (country, region, tier, total) on one database:
    about 140M rows, about 185k runs, about 255 rows a run each.
- **Trap.** Rows per run, not run count, shows the scan. A query with few runs can
  read the most rows.

### Put a row budget at the Worker entry

- **Signal.** No code counts rows read per request.
- **Change.** Count rows read per request. Run the guard in log-only mode first.
  Then set a cap for each route from the measured maximum rows. Exempt a route by
  that number, not only the sitemap.
- **Proof.** No saving was measured for the guard alone. Measure with the top
  queries from `d1QueriesAdaptiveGroups`, same hours.
- **Trap.** One query family read up to 190,000 rows in one run (MEASURED, see
  the families above). A cap below the real maximum of a route sends 503 on a
  valid page or sitemap build.

### Store facet counts at import

- **Signal.** `git grep -n "COUNT(\*)" -- '*.ts'` in browse and facet code that
  runs per request.
- **Change.** Write counts to a table at import. Browse pages read stored counts.
- **Proof.** The five per-request facet queries above read about 140M rows in
  16 hours (MEASURED). Re-run the query-family report after the change.
- **Trap.** Counts go stale unless every write path updates them. Test that.

### Sitemap: skip counts that one shard answers

- **Signal.** The sitemap index runs a group count for every shard.
- **Change.** Compare a cheap upper bound, such as the published listing count,
  with the shard size. Run the heavy count only when the bound is larger.
- **Proof.** One build ran nine queries of 300,000 to 693,000 rows each, 1 to
  1.7 s each, and other requests queued behind them (MEASURED, one incident).
- **Trap.** D1 runs queries one after another. Find the one heavy burst before you
  blame the row cap.

### Index a full scan

- **Signal.** A family with thousands of rows read per run on a table with a
  filter (see the families above).
- **Change.** Add an index on the filter column, or select fewer columns.
  Check the plan with `EXPLAIN QUERY PLAN`.
- **Proof.** No fix was measured in this work. Re-run the family report after the
  change. Rows per run must fall.
- **Trap.** An index adds rows written on every insert. D1 rows written cost
  $1 per million, a thousand times a read.

## Observability

### Stop routine per-request logs

- **Signal.** The Wrangler config has an `observability` block with no
  `"invocation_logs": false`. Workers Logs then holds one invocation log per request.
- **Change.** Set `"observability": { "enabled": true, "logs": { "enabled": true,
  "invocation_logs": false } }`. Errors stay in Workers Logs.
- **Proof.** No saving was measured in this work. Count log events per day in
  Workers Observability before and after, same hours.
- **Trap.** An `env` block that turns invocation logs back on overrides the top
  level. Keep the log line that names a cause for a refusal. You need it to
  find a heavy burst later.
