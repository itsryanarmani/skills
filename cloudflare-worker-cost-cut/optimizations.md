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

- **Signal.** `git grep -n "minify" -- '*wrangler*'`. The signal is `minify: true`.
- **Change.** Set `minify: false` on one site. Read `cpuTime` from the tail.
- **Proof.** Local cold CPU fell 32% to 42% (MEASURED, local workerd).
  A small production A/B (4 cold requests on the old bundle, 5 on the new) showed a
  large drop. It is MEASURED, but the samples are few and the kept logs cannot
  reproduce it.
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

### Pin one site's Worker to a region (a switch, not a default)

Smart Placement did nothing here: `cf-placement` answered `local-<colo>` from a client in Vancouver, so each
data centre still started its own cold isolate. A cold first request cost about 1.3 s of wall time and about
1,000 ms of CPU; a warm one cost 14 to 28 ms (measured on a Boat box with real data and a fresh D1).

Change: an optional per-site variable (`PRODUCTION_PLACEMENT_REGION`, like `aws:us-west-2`) that the render
script writes as `env.production.placement.region` for the app Worker only. Unset keeps Smart Placement.
Pick the region nearest the site's D1 primary (`wrangler d1 info`). Roll it out one site at a time.

Result (MEASURED, CPU per request from hourly analytics, before against the first full pinned hour):
memorycarehomes 159 to 86 ms, adhdevaluations 141 to 88, itinagents 157 to 129, mriprices 332 to 370 and
mcpdirectory 210 to 206 (no change), sleepstudies 196 to 344 (worse, so I unpinned it). An unpinned control
stayed flat (36 to 40 ms). On itinagents wall p90 fell from 1,693 to 708 ms and no request failed.
It helps some sites and not others. Do not roll it out to the whole fleet from tail samples.

Traps:
- Compare like hours across days and keep an unpinned control. Time of day moved CPU per request 33 to 50%
  on unpinned sites in the same window.
- The pin applies to every request, not only cache misses, and the Cache API moves with the Worker.
- An earlier test that set a region through the API rewrote it as `mode: targeted`, and the home page went
  from 0.2 s to 3.3 s. A change made by config at deploy did not. Save the old setting and undo it at once if
  latency rises. To undo: delete the variable and redeploy (`wrangler rollback` may keep the pin: UNCERTAIN).
- A bundle-size test (append 10 or 20 MB of never-called code to the handler) moved the first request only
  from about 1.26 s to about 1.35 s. That test was weak: 7 of 15 runs got the local 429 and measured nothing,
  each arm had one or two valid samples, and dead functions may be parsed lazily. Treat "fewer bytes will fix
  cold starts" as unproven until you run a clean slope test with a fresh D1 per run.

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

### Name the crawlers that cost money, and block the ones that ignore you

Signal: a live tail shows the same few user agents on the slowest requests. Split the tail by crawler NAME,
not by family. `cf-traffic-probe ua-cpu <tail files>` does it. A family such as "other bot" hid QlyzeBot,
which was 33% of the sampled CPU on six heavy sites (MEASURED, 1,035 requests in 10 minutes). Check each
site apart: all 284 QlyzeBot requests in a later sample hit ONE site, not six.

Change, in three layers:
1. **`robots.txt` lists.** Block SEO-tool crawlers (SemrushBot, AhrefsBot, MJ12bot, DotBot, BLEXBot,
   DataForSeoBot, serpstatbot) and crawlers that send nothing back (QlyzeBot, Bytespider, CCBot,
   Reflectionbot, ElevenlabsCrawler, meta-externalagent and others). Keep Googlebot, bingbot, Applebot,
   the answer engines (OAI-SearchBot, PerplexityBot, Claude-SearchBot), GPTBot and ClaudeBot, and the
   link-preview bots. Keep PetalBot out: it is a search engine. A crawler must sit in one group only.
2. **Facet URLs.** Disallow `/search?*category=`, `tier=`, `country=`, `region=`, `city=` and `sort=`.
   A tail showed GPTBot sending about one `/search` request a second to two sites (85 to 88% of their
   requests), and every URL was a facet toggle link. Leave `/search?q=` open if your schema uses it.
3. **An edge rule for the ones that ignore `robots.txt`.** One custom firewall rule per zone:
   `lower(http.user_agent) contains "qlyzebot" or ...`, action block. It runs before any Worker, so a
   blocked request costs no request and no CPU. Rule, script and test: `scripts/ops/waf-bots.py` in the
   directory repo (plan, apply, remove; idempotent by description).

Proof (MEASURED): SemrushBot fell from 128 events to 2 in 7 minutes after the `robots.txt` change.
QlyzeBot, ElevenlabsCrawler, Bytespider and Reflectionbot still made 49.5% of requests on six sites
three hours later, so they ignore `robots.txt`. After the edge rule a 200-second tail of the busiest site
showed 0 QlyzeBot requests (it had been 284 of 326).

Traps:
- `robots.txt` stops only polite crawlers. Crawlers cache it for up to a day. Measure, then add the edge rule.
- A Free zone allows 5 custom rules, the `contains` operator and `lower()`, but no regex. The token needs
  Zone WAF edit. Count the rule slots before you add a second rule.
- GraphQL on a Free zone has no client ASN and no query string field. Ask for status, country and agent.
- The edge cannot tell a real browser from a faked one. Amazonbot and Googlebot also hit blocked facet URLs
  (about 96,000 `/search` 503s a day on six zones); that costs about $0.03 a day, so leave it.
- Add the rule to the site launch step, or the next site starts unprotected.

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
and the city page change below. No cut was tied to it. The hourly reading showed no
write spike after a fleet deploy (MEASURED). So the idea that a deploy empties the
data cache and causes a write wave is not supported.

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

- **Signal.** A cache call whose key holds a place slug (a city or a street), one
  call for each place. Search: `git grep -n -E "unstable_cache|cachedIf" -- '*.ts' '*.tsx'`,
  then read each key for a city, a region or a street.
- **Change.** Treat the place page as long tail. Keep the cache on the listing
  page's shared block.
- **Proof.** A cold city page wrote 3 to 5 KV entries (3 once the region keys
  were warm). It saved about 9 D1 queries per later hit (MEASURED, test run).
  The sum (ESTIMATE): 3 to 5 writes at 5,000 row reads each cost 15,000 to 25,000
  row reads. Assume a later hit reads 3 to 5 entries (the number of entries a hit
  reads was not measured), so it pays the read fee 3 to 5 times: 1,500 to 2,500 row
  reads. Each hit saves about 9 queries of 319 rows, 2,871 rows. The net is 371 to
  1,371 rows a hit. The writes need about 11 to 67 hits in the window, or about 40 if
  a warm page writes 3 entries and reads 5. A city page rarely gets that many, so it
  is long tail.
- **Counter-example.** The listing page reads the same block on every visit. It
  keeps its cache. Apply the break-even rule below to decide.

### Break-even rule: write to KV or read from D1

- **Signal.** A new cache entry that stores a D1 result.
- **Rule.** One KV write costs $0.000005. One D1 row read costs $0.000000001.
  So one write equals 5,000 row reads ($0.000005 / $0.000000001).
  Each cached read costs the KV read fee: $0.0000005, about 500 row reads.
  Net rows saved per hit = rows saved per read minus 500.
  Reads to pay back one write = 5,000 / net rows saved per hit. For W entries written
  and N entries read per hit: hits needed = W x 5,000 / (rows saved - N x 500).
  A D1 read query read 319 rows on average (MEASURED: 7,952,705 queries read
  2,533,957,103 rows in one day). An entry that saves about 1,000 rows a read
  (about 3 queries) nets 500 and needs about 10 reads in its window. An entry
  that saves about 16 queries (about 5,100 rows) nets 4,600 and needs about 1.1.
  So the bigger the load, the fewer reads you need.
- **Proof.** The arithmetic above, from the price table (ESTIMATE for your own
  load size). Measure your own rows per query with `d1QueriesAdaptiveGroups`.
- **Trap.** The window starts at the write. A key read once is a loss.

### Do not raise the data cache window as the fix (a lesson from a closed PR)

I proposed one hour instead of 300 s for every production site. The hub review showed the premise was wrong,
and I closed the PR. Three facts: KV writes had already fallen from 255,179 (5 Nov) to 172,728 (6 Nov) before
the change, so a before and after check would have credited it with a drop that had already happened. The
per-route budget (`e2e/cost-budget.json`) shows a first view writes 2 to 6 keys and a repeat writes 0, so
most writes are first views of long-tail keys that a longer window cannot remove. And the change would have
made docs and an import message false. Find the writers first (the listing page's "nearby" block is keyed per
city), apply the break-even rule to each, and compare the same UTC hours after the deploy.

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

### Read the KV cache through the regional Cache API

Signal: KV reads are about 1.9M a day and the same few keys are read on every page view. On a Boat box one
render of the home page made 6 KV gets, and a repeat made 6 again.

Change: wrap the incremental cache in OpenNext's `withRegionalCache` in `short-lived` mode (60 s). A repeat
read in the same data centre then comes from the free Cache API. A repeat made 0 KV gets.

Traps:
- On Next 16 the wrapper re-reads KV in the background on every hit by default. Set
  `shouldLazilyUpdateOnCacheHit: false` and `bypassTagCacheOnCacheHit: false`, or the cost stays.
- The tag cache is still checked on each read, so `revalidateTag` keeps working. Run the specs that write
  and then read on the cached server (admin writes, menu items, guides, shared D1). The review asked for them.
- Gate it on the same switch as the page cache (`EDGE_CACHE=on`), so a test server that clears KV keys behind
  the cache keeps working. `RegionalCache.delete` builds its key without the cache type, so a deleted fetch
  entry can stay up to a minute.
- Ceiling: the KV read line was about $1 a day. Check KV reads per namespace for the same hours after the
  deploy, and check that KV writes do not rise.

### Serve the sitemap index from KV, stale-safe

- **Signal.** The sitemap index runs a count query on each request.
- **Change.** Store the index in KV. Serve a fresh copy with no D1 read. Serve a
  stale copy at once and rebuild in the background. Serve a degraded copy built
  from config if nothing is stored. Mark it and send `no-store`.
- **Proof.** Not measured as a separate number. It moves reads from D1 to KV. Weigh
  it with the break-even rule. One KV read costs $0.0000005, a tenth of a write.
- **Trap.** Never let the edge cache store the degraded copy.

## KV storage

### Find legacy cache entries, and swap the namespace

Signal: the KV storage line ($0.50 per GB-month over 1 GB) was about $0.50 a day. `cf-traffic-probe kv-storage`
showed 38.5 GB in 564 namespaces, 34 GB of it cache entries (`inc-cache`). My first reading said 2.8 GB because
the query returned only part of the rows. Raise the limit and check the row count.

Cause: runtime cache writes got a 24-hour expiry on 22 Oct, but entries written before that never expire, and
each deploy uses a new build id prefix, so the old entries are never read again. In a sample of 5,000 keys from
two big namespaces, none had an expiry. A deploy seeds only about 8 files (145 KB), so deploys are not the cause.

Change: do not delete millions of keys. Each delete is a write operation at $5 per million, about $12 for 2.4M
keys. Create a fresh namespace, point the site's variable at it, deploy, and delete the old namespace later.
Deleting a namespace is one call and free. Five sites held 19.8 GB.

Traps:
- Analytics namespace ids have dashes. The REST list has none. Strip them before you match, or every name
  comes back "not listed".
- Keep the old namespace until the next deploy of that site has succeeded. A failed deploy rolls back to the
  previous version, and that version is bound to the old namespace.
- Staging and preview namespaces of other projects in the same account can hold gigabytes too. Report them to
  their owner.
- A billing line can arrive in lumps: KV writes showed $5.00 on days over one million writes and $0.00 on a day
  with 255,000. Compare analytics counts, not single billing rows.

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
  Then give each route its own cap, set from the measured maximum rows of that
  route. A route that goes over its cap still gets a 503.
- **Proof.** No saving was measured for the guard alone. Measure with the top
  queries from `d1QueriesAdaptiveGroups`, same hours.
- **Trap.** One query family read up to 190,000 rows in one run (MEASURED, see
  the families above). A cap below the real maximum of a route sends 503 on a
  valid page or sitemap build.

### Store facet counts at import

- **Signal.** `git grep -n -i "count(\*)" -- '*.ts' '*.tsx'` in browse and facet code that
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
  `"invocation_logs": false`, or no `observability` block at all.
  The Cloudflare docs say observability defaults to on for new Workers.
  Workers Logs then holds one invocation log per request.
- **Change.** Set `"observability": { "enabled": true, "logs": { "enabled": true,
  "invocation_logs": false } }`. Errors stay in Workers Logs.
- **Proof.** No saving was measured in this work. Count log events per day in
  Workers Observability before and after, same hours.
- **Trap.** An `env` block that sets invocation logs on again overrides the top
  level. The Cloudflare docs set observability per environment, so check the
  rendered config of each environment.
  Keep the log line that names a cause for a refusal. You need it to find a heavy
  burst later.
