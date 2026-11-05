---
name: cloudflare-worker-cost-cut
description: Cut the Cloudflare bill of a fleet of Next.js sites on Workers (OpenNext, D1, KV). Use when the bill is high, Worker CPU, KV writes or D1 rows read dominate usage, or you must roll the same savings out to many repos. Covers measuring each meter, the levers ranked by value, and the process traps from a real cut.
---

# Cloudflare Worker fleet cost cut

Measure each meter first. Then change the code that drives the biggest meter.
Keep a measured saving apart from a target. A target is a plan, not a result.

Read `cloudflare-cost-audit` first for the billing baseline. This skill covers
what to change after the baseline exists, and how to roll it out to many repos.

Read [optimizations.md](optimizations.md) for each measured cut, grouped by meter.
Each entry gives the signal to search for, the change, the proof and the trap.

## The meters and what they cost

Allowances are per account, shared by every Worker in it. Check current prices before you
quote a number.

| Meter | Price over the allowance | Allowance |
|---|---|---|
| Worker requests | $0.30 per million | 10M |
| Worker CPU | $0.02 per million ms | 30M ms |
| D1 rows read | $0.001 per million | 25B |
| D1 rows written | $1 per million | 50M |
| KV writes | $5 per million | 1M |
| KV reads | $0.50 per million | 10M |
| KV storage | $0.50 per GB | 1 GB |
| Durable Object requests | $0.15 per million | 1M |

One KV write costs about as much as reading 5,000 D1 rows ($0.000005 against
$0.000000001 a row). Weigh a change in both directions: a change that saves a write but
adds 10,000 row reads loses money. A cached read also costs the KV read fee, about 500 row
reads. Net rows saved per hit = rows saved per read minus 500. Reads to pay back one write =
5,000 divided by that net (ESTIMATE). Saving 1,000 rows a read needs about 10 reads in the
window. A bigger load pays back sooner. `optimizations.md` shows the arithmetic.

KV writes per hour is the check for any KV change. Query `kvOperationsAdaptiveGroups`
with the dimension `datetimeHour`. A test found no write spike after a fleet deploy.
So the idea that a deploy empties the data cache and causes a write wave is not supported.

To find which D1 queries read the rows, query `d1QueriesAdaptiveGroups` and sort by rows
read. Families found: a category-tree CTE with `json_each`, a full scan of one table, and
per-request COUNT facets. See `optimizations.md`.

In the fleet this was learned on, the order was: Worker CPU, KV writes, D1 rows read,
requests, KV reads, containers, Durable Objects, subscriptions. Rank yours before you act.

## Measure first

1. **Billing API.** `accounts/{id}/billable-usage?from=YYYY-MM-DD&to=YYYY-MM-DD` returns daily rows.
   - Each row is ONE DAY of use and that day's cost (`ConsumedQuantity`, `BilledCost`). Cloudflare
     applies the monthly free allowance to the cumulated quantity, so a day that crosses the
     allowance shows a part-free cost. Sum `BilledCost` per day and per service line.
   - The feed returns only the NEW billing period's rows when `from` lies inside the old period, and `to`
     is exclusive. Ask 35 days back and one day past the end, then keep the days you want.
   - A new billing period (`BillingPeriodStart` changes) restores the allowance. The first day of a
     period looks cheaper than it is. Do not compare it with the last day of the old period.
   - The newest day is published late and in pieces. A partial day shows only some lines, often
     D1 first and Workers CPU and KV writes later. Mark it `partial`. Never call a partial sum a
     daily total.
   - Check the feed against analytics. A full-day D1 analytics sum matched the bill to the row
     (63,325,168,002 against 63,325,168,224: 222 rows apart, under one part in 100 million), and Workers CPU matched within 0.01% (576,338,444 ms against 576,290,354 ms billed). Analytics gives usage, not cost: to get cost, apply the monthly allowance to the period's cumulated quantity. Once they agree,
     analytics usage can stand in for the bill's usage on a day the feed has not published.
2. **GraphQL analytics** gives the same day as usage, not dollars. Useful datasets:
   `workersInvocationsAdaptive` (requests, CPU), `d1AnalyticsAdaptiveGroups` and
   `d1QueriesAdaptiveGroups` (rows read, per query), `kvOperationsAdaptiveGroups`
   (reads, writes, deletes per namespace), `httpRequestsAdaptiveGroups` (per zone).
   Group by namespace or script, then map ids to names with the list APIs.
3. **Per request CPU.** `wrangler tail --format json` shows `cpuTime`, `wallTime`,
   request headers, status and `scriptVersion`. Sample one site for a few minutes per
   path. Workers Observability can also read logs.
4. **Per site spread.** Writes per request varied 40 times between sites (0.09 to 2.15).
   A fleet average hides the two or three sites that make half the bill. Rank by site.
5. **Heavy tail.** Ask analytics for `quantiles { cpuTimeP50 cpuTimeP99 }` per script. CPU minus
   (requests times the script's own p50), divided by all CPU, is the heavy-tail share. A share
   above 50% means a few requests cost far more than the rest. On this fleet it was 71%, and the
   likely cause was cold starts (inferred from the cold and warm samples; see lever 0). A trivial request that costs a second or more of CPU, such
   as a redirect or a health check, is the signature.
6. **Cold versus warm, measured on the real Worker.** Run `wrangler tail <script> --format json`
   in the background. Send a request with a unique query string to a quiet site, again two
   seconds later, and again after a pause. Read `cpuTime` for each from the tail by URL. The
   first request of an isolate cost 917 ms, the next 48 ms, and a request that landed in a new
   isolate cost 992 ms. Local measurement alone misled us: it measured the warm path.
7. **Compare like with like.** Compare the same hour of the day, before and after.
   Traffic and bots change a day-on-day comparison. Find the hour a step happened and set it
   against the merge and deploy times. Our big drop (D1 reads 97B to 2.5B a day) happened 12
   hours before the PRs that we first credited. The cause was a search pause.
8. A usage-based run rate is an estimate. A billing row is a measurement. Label each.

## Levers, ranked by value

Apply them in this order. Each has the meter it cuts. Measure before and after each one; the
measured effects below are from one fleet and may differ on yours.

### 0. Cut what a cold start costs (CPU)

On a fleet of many small Workers, cold starts can be most of the CPU bill. Check the heavy-tail
share first (Measure, item 5). Here it was 71% of all CPU: a cold request cost about 920 to 990 ms
and a warm one about 50 ms, so the bill followed (number of cold starts) times (cost of one).
Each site is its own Worker and each Cloudflare location starts its own isolate, so you mostly cannot
cut how often they start (fewer, larger Workers would share isolates, which is a bigger change). You can cut what a start costs.
- **Bytes are the main lever.** In a fresh local process the first request had a median of 589 ms (the next 20 had 6.6 ms). In a profiled first request of 642 ms, about 350 ms (55%) was V8 compiling the 25.7 MB OpenNext handler (a plain Node compile took 290 to 300 ms, about 11.5 ms per MB) and the rest was real start-up work.

  Lazy `import()` does not help: OpenNext inlines dynamic imports into the same file.
- **Find what fills the bundle.** On this fleet Turbopack copied shared modules into each route group
  (zod core 20 times, an app schema module 20 times), better-auth, drizzle and kysely were bundled
  once per rsc and ssr layer, and a 0.94 MB block of legacy encoding tables came from Next's body
  parser. Try a webpack build, which shares chunks. Keep client-only libraries (maps, editors) out
  of server-evaluated code.
- **Test `minify` (unconfirmed).** One local sample found the first request about 40% cheaper with
  Wrangler's `minify` off (530 ms against 900 ms), at the price of a larger gzip. That sample came from a different local build
  than the 589 ms median above (one with `minify` on, one with it off), so do not compare the two numbers. That goes against
  the bytes lever above. A small production A/B on cold requests (4 on the old bundle, 5 on the
  new one) showed a large drop (MEASURED, small samples, not reproducible from the kept logs).
  But fleet CPU per request did not change: 71.5 ms on both days, same hours (MEASURED).
  Keep it unconfirmed.
  Compare the same hours across days before you credit a change. Deploy it to one
  site and read `cpuTime` from the tail before you roll it out.
- **Do not pin a region on a live Worker as a fix.** We tried an explicit placement region through
  the API to put every request in one place and keep one warm isolate. The API rewrote it as
  `mode: targeted` and the home page went from 0.2 s to 3.3 s. Smart Placement was already on. Save
  the current placement setting before any change and restore it at once if latency rises. In that
  test the home page took 3.3 to 3.8 s; test on a copy first.

### 1. Stop bot and router noise (CPU, requests, D1)

- **Turn off link prefetch.** Next prefetches RSC payloads for every visible link. Bots and
  crawlers multiply it. Make the shared `Link` component default to `prefetch={false}`.
  Measured on one site: `_rsc` requests fell from 9% of traffic to 0.
- **Refuse a bare `_rsc` request.** A real router request sends `?_rsc=` and an `RSC`
  header. A request with the parameter and no header is a bot replay. Answer 404 with
  `Cache-Control: no-store` before the cache and before any render, for GET and HEAD.
  Put the guard first in the Worker entry. A WAF rule is cheaper still, but it needs a token
  with Zone WAF permission (see the token bullet below).
- **Pause staging and search jobs.** Staging sweeps and search jobs burn requests with no user. A
  per-minute cron for every site was a small share of CPU on this fleet (about 1%, ESTIMATE),
  so measure before you spend a PR on it.

- **Block a client by what it sends, on the Cloudflare edge, before the Worker runs.** Traffic was very
  concentrated: one IP with an empty `User-Agent` sent 43% of a site's requests and another 60% of a
  second site's. A zone custom rule `(http.user_agent eq "" and not starts_with(http.request.uri.path, "/api/"))`
  with action `block` stops them with no Worker run. Do it safely, zone by zone:
  1. Check analytics first for empty-user-agent traffic outside `/api/` that you want. Examples are
     an uptime monitor, a webhook and a health check. They can send no user agent.
  2. `GET /zones/{id}/rulesets/phases/http_request_firewall_custom/entrypoint` and save the answer to
     a file. A `PUT` to that entrypoint REPLACES every custom rule on the zone: send back all the
     existing rules plus yours, or add yours with `POST .../rulesets/{ruleset_id}/rules`. The free plan
     allows 5 custom rules per zone; check there is room.
  If the GET returns 404 (a zone with no custom rules yet), create the entrypoint with a `PUT` that holds
  only your rule.
  3. Give the rule a stable `ref` so it can be found and removed later, and record the zones.
  4. To undo, `DELETE .../rulesets/{ruleset_id}/rules/{rule_id}` for the rule with your `ref`, or `PUT` the
     saved entrypoint back.
  5. Verify on each zone: an empty user agent gets 403, a normal request and the AI crawlers you want
     get 200, and `/api/` still answers.

  The free plan refuses a custom block response ("not entitled to use a custom response"), so a block
  cannot carry a pointer to your API; use the Worker for that.
- **Do not block AI crawlers by user agent if your product tells owners to let them in.** Our own
  audit tool told site owners to let GPTBot, ClaudeBot and similar agents reach the homepage.
  Rate-limit by behaviour, or leave them.
- **The token needs permission.** The fleet token had no WAF permission (`request is not authorized`).
  All 50 token slots were in use. Do not revoke a live deploy token to make room. Prefer a separate,
  narrow WAF token when a slot is free. If none is free, extend the existing zone-wide policy of the
  token that already has zone access, with a token that can edit tokens: `PUT /user/tokens/{id}`
  REPLACES the whole token, so (1) `GET` the full token object and save it to a file; (2) send back
  the same object with only `Zone WAF Read` and `Zone WAF Write` added to a policy that already covers
  all zones, keeping `name`, `status`, `condition` (IP limits), `not_before` and `expires_on` exactly (look up the
  group ids with `GET /user/tokens/permission_groups`; a policy names groups by id); (3) read it
  back and compare name, status, condition, expiry and every permission by NAME, not by position
  (the API reorders policies); (4) to undo, `PUT` the saved object. Verify the token still works.
  Note that this gives that token WAF write on every zone: that is the cost of not using a new token.

### 2. Cut KV writes (KV writes)

KV writes in an OpenNext app come from the incremental cache. Each cache miss writes an
entry. Pages that are `force-dynamic` still write the data cache through `unstable_cache`.

- **Do not cache the long tail.** A key built from the full filter JSON, a page number above
  1, a free-text query or a rare place and category pair is read once, if ever. Measured:
  98% of geo page requests were unique within 3 minutes. Call the loader directly for these.
  Keep the cache for head pages that many visitors read.
- **Use fewer, coarser keys.** Merge small counts that one page reads together. Do not merge
  if a head key grows past about 25 KB or if the data has different invalidation.
- **Raise the data cache window.** A short window rewrites long-lived keys every few
  minutes. If data changes only by import and every write path calls `revalidateTag`, use a
  day. Keep the edge page cache window separate. A constant shared by both turns a data
  decision into a stale page decision. The KV retention must be at least the window.
- **Skip a write when the value is unchanged.** Read the stored value first. A read costs a
  tenth of a write. Refresh the entry before it is about half its retention age, or a
  valid entry can expire while it is in use.
- **Audit every write path** before you lengthen a window: claim, edit, tier change,
  import, delete, admin tools, webhooks. Each must call the revalidate helper.
- **Add a check** to local CI that fails when a new cached key embeds `JSON.stringify` of a
  free-form object without an explicit opt-in comment. Without it the pattern returns.

### 3. Cut D1 rows read (D1 rows read)

- **Put a per-request row budget** at the Worker entry. Count rows read per request. Run it in
  log-only mode first. Then set a cap for each route from the measured maximum rows. One query
  family read up to 190,000 rows in one run. A cap below the real maximum turns a valid page or
  sitemap build into a 503.
- **Store counts at import.** Counts for facets, places and categories rarely change. Write
  them to a table when you import. Do not compute them with a group query per request.
- **Beware head-of-line blocking.** D1 runs queries one after another. One sitemap build ran
  nine queries that read 300,000 to 693,000 rows each and took 1 to 1.7 s each. Every other
  request queued behind them and was refused as overloaded. Find the one heavy burst; do
  not blame the row cap without a log line that names the cause.
- **Prove a count needs no query.** The sitemap index needs only the shard count.
  A cheap upper bound, such as the published listing count, proves one shard. Run the heavy
  count only when the bound exceeds the shard size.
- **Cache the sitemap index** in KV with a hash. Serve a fresh copy with no D1 read. Serve a
  stale copy at once and rebuild in the background behind a short lock. If the build fails and
  nothing is stored, serve a degraded index built from config alone, with a header that
  marks it and `no-store`. Never let the edge cache store the degraded copy.

### 4. Cut warm Worker CPU (CPU)

Do this after lever 0. Measure on cold, uncached pages in production (a unique query string per
request, read `cpuTime` from `wrangler tail`), not on a warm local server.
- A markdown page cost about 24 ms against about 67 ms for HTML on cold pages (median), so serving
  markdown to AI agents would save about 40 ms a request. That is an estimate of about $0.04 a day
  on a site where AI crawlers were 42% of requests (the 40 ms comes from a small cold sample). An older sample had said 8 to 12 times; it compared different pages. Do not
  build a feature on a saving you have not measured on matched pages.
- Cutting the HTML and RSC payload by 42% and 68% left warm render time about 10% lower, measured locally on demo data. Payload
  bytes are not CPU. They cost bandwidth, which Workers do not bill.
- Dynamic `robots.txt` and `llms.txt` cost about 200 ms a hit on one site, but this too was mostly
  cold start; serving static files helps only for files that were not edge cached.


### 5. Publish the long tail as static files (CPU, requests, D1, KV)

Workers Static Assets serve files with no Worker run. Requests for static assets are free.
This removes the CPU, the D1 reads and the KV write for those pages.

- Pilot on one site first. Learn the limits before a full build: file count, total size,
  and generation time (estimated 2.2 to 5.7 hours serial for one large site).
- Use `_headers` for cache headers and a trailing slash rule so URLs match the dynamic ones.
- Keep dynamic routes for pages that need data per visitor.

## Process traps (rolled out as checks where possible)

- **Honest targets.** An adversarial review refuted a "$50 a month" claim: the run rate was
  about $520 a month. Say what is measured, what is an estimate and what is a target.
- **Judge a delegated job on its diff.** A worker can exit 0 and write nothing. Rerun the
  tests yourself. A test that cannot fail proves nothing. Mutation-test it: break the code
  on purpose and watch the test fail, then restore the code.
- **Write the failing test first** and show it fail. Register tests with
  `if (!REMOTE) { ... }`. A repo policy may reject `test.skip`.
- **Do not trust "completed".** Check the exit code of every build and test.
- **E2E hygiene.** Two worktrees run on the same default ports and collide. Pass your own
  ports. A Miniflare cache that is not empty can fail a spec with `STALE`: clear it between
  runs. Production-build test servers set `ENVIRONMENT=production`, so a test hook gated on
  "not production" never runs there.
- **Test hooks in production code** need a guard that no Worker secret can turn on, and a
  local CI check that scans configs for the hook name.
- **Do not rerun an old run's failed deploy jobs.** They can redeploy an older commit. A
  newer push redeploys. A `fetch failed` in a deploy job was transient.
- **Merge gate.** Read both the reviews and the review comments. Check the review is for
  the head SHA, that the SHA has its own check runs and that no Critical or Major is open.
  Merge with `--match-head-commit`.
- **Prompts.** Pass a long prompt to a CLI by stdin. A variadic `--allowedTools` flag
  swallows a prompt given as an argument: `claude -p --allowedTools A B C "prompt"` reads the
  prompt as a tool name. Write prompt files with the Write tool, since a
  hook can block prompt text typed in a shell.
- **Commit messages with a dollar sign.** In double quotes, `$0.000025` becomes
  `/bin/zsh.000025`. Use single quotes.
- **GraphQL errors in `gh`.** `gh pr edit` and `gh pr review` can fail with a GraphQL error.
  Use the REST API: `gh api -X PATCH repos/OWNER/REPO/pulls/N -F body=@file`, and
  `POST repos/OWNER/REPO/pulls/N/reviews`.
- **Assert the one counter that proves the claim.** A spec that compares D1 read counts
  between two views can pass for other reasons. Assert the counter for the query you
  changed, such as the listing query count.
- **Review the callers of a cache rule you change.** A cache rule that skips the long tail
  can make a head page uncached if that page shares the key shape.
- **A review gate may read plain lines.** A gate can match `Reviewed-by:` and `Verdict:`
  lines only. A bold verdict line is not matched.
- **Sandboxes (Boat).** A box needs the right language runtime version, the site setting,
  and a real copy of any folder that is a symlink in the repo. Agent logins inside a box can
  expire. A new repository may need its environment created first, and the repo list may need
  a refresh in the dashboard.
- **Billing reads need a clear window.** A frozen feed is often a misread: check the row
  date, not only the number.

### Traps from running many workers at once

- **Write briefs with a file tool or a quoted heredoc (`<<'EOF'`).** An unquoted heredoc runs every
  backticked command in the brief in your own shell and leaves the worker a brief with holes.
- **In zsh, `set -- $var` does not split words.** Use a function with explicit arguments or an array.
- **`pkill -f` kills other jobs.** Kill by process id. Killing the wrapper of a CLI agent does not
  kill the agent: find live agents by their working directory (`lsof -p <pid> | grep cwd`) before you
  start a second one in the same worktree, or the two collide and both stop.
- **One log file per run.** A later run that writes the same log file overwrites or interleaves with
  an earlier one that is still alive.
- **Disk and worktrees.** A full disk (125 MiB free) made hooks fail closed and worktree creation fail
  silently; a failed `cd` then ran `bun install` in the main checkout. Check `df` when anything fails
  oddly. Worktree folders can disappear; keep every branch pushed and rebuild from the remote.
- **A Playwright spec in serial mode hides later tests after the first failure.** Run each new test
  alone against the old source when you prove it fails there, and print `did not run` counts.
- **Phone numbers or ids derived from a run id collide across specs in one run**, and a new check
  that reads the shared table then refuses a number another spec opted out. Give each spec its own prefix.
- **A spec that writes its result artifact in `afterAll` loses it on a retry** (a fresh worker
  overwrites the file). Write one file per test, inside the test.
- **Admin routes answer 404 to an anonymous caller and 401 to a bad token.** Do not guess 401.
- **A merge gate counts an unanswered bot comment as a block.** Reply, even if the code is fixed.
- **Migration numbers collide.** Other sessions take the next number within the hour. Check main's
  migration list right before each merge, drop your SQL, journal and snapshot, and regenerate with
  the generator so the snapshot chain stays right. Check the SQL is byte for byte the same.
- **Never edit `.github/workflows/` in a cost PR** where a policy check demands an owner label, and do
  not delete test files where a check forbids it. Find another route.
- **Check for `gh` in a command that has an unset variable.** `$G pr view` with `$G` empty ran an
  unrelated `pr` program and printed a file instead of failing.

## What it adds up to

Do the arithmetic before you promise a number. On this fleet, with 3.8M Worker requests a day, the
request fee alone was about $1 a day ($0.30 per million over 10M a month), before CPU, KV, D1 or
containers. A $50 a month target needs most requests answered without a Worker run: static assets,
an edge block, or fewer visitors. State the floor your levers can reach, with a label that says it is an
estimate, and report measured days beside it.

## Rolling out to many repos

1. Run `cf-usage-report` for the account. Rank the namespaces and the sites. (Both tools are in the
   scripts repo; without them, use the billing call and the GraphQL queries in Measure first, items 1 and 2.)
2. Run `cf-cost-scan` over every repo. It lists which levers each repo still lacks.
3. Do one repo end to end. Prove the saving in the next billing row.
4. Open one issue and one PR per lever per repo, under 500 lines each. Do not batch levers.
5. After each deploy, compare the same hour of usage. Record MEASURED and TARGET apart.
6. Add the local CI checks to each repo so the pattern does not return.

## Done when

- Each lever has a PR, a failing test shown first and a passing run.
- The next billing row, not an estimate, shows the change, or the report says it is not yet known.
- The rollout table lists every repo with each lever marked done, not needed, or open.
