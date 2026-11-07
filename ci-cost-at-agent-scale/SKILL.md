---
name: ci-cost-at-agent-scale
description: "Use when agent-generated PRs make CI expensive or slow. Audit repeated jobs, qualify local and deployment proof, preserve production checks, drain idle capacity, and verify total cost. Covers scheduler versus compute placement and review proof without paid inference."
---

# ci-cost-at-agent-scale

CI economics break differently when agents open the pull requests. The fix is almost never the
one people reach for first.

## When to use this

**Trigger if:**
- Agents, review bots, or a worker fleet open most of the pull requests.
- CI runs number in the hundreds per day, or jobs sit queued behind each other.
- Someone has proposed switching runner providers, or hosting CI on a sandbox platform.

**Don't bother if:** a handful of humans open a handful of PRs a day. At that volume the bill is
noise and the audit costs more than it saves.

**Use a sibling instead** when the problem is latency rather than spend. Start at
[ci-speed-diagnosis](../ci-speed-diagnosis/SKILL.md), the entry point of this family; it routes to
[ci-build-speed](../ci-build-speed/SKILL.md), [e2e-ci-economics](../e2e-ci-economics/SKILL.md) and
[high-volume-ci-optimization](../high-volume-ci-optimization/SKILL.md) for the levers.

## The core asymmetry

A human PR costs one pipeline. An agentic PR costs **one pipeline per `synchronize` event**, and
nobody budgets for the extra ones because they land somewhere else.

Every bot commit — a review bot's auto-fix, a formatter, a changelog stamp — is a real commit on
the branch. GitHub raises `synchronize`. **Every** workflow triggering on `pull_request` runs
again. A review bot with a 3-cycle fix budget, in a repo with five `pull_request` workflows:

```
1 agent push        ->  5 runs
3 bot fix commits   -> 15 runs
                       20 runs for one pull request
```

The bot's own workflow appears once in that tally. The other 15 runs are charged to your test,
lint, build and e2e workflows, which is why the multiplier survives so many cost reviews.

**Second asymmetry, and the one that actually bites:** at agent scale you hit the
**concurrent-job ceiling** before the minutes bill hurts. GitHub-hosted private repos cap around
20 concurrent jobs on Free and 60 on Team. Past that, agents queue — and a queued check blocks
the agent that opened the PR, so throughput collapses while the invoice still looks fine. Cutting
per-minute price does nothing for this. Only moving runners into infrastructure you control does.

## Audit before you change anything

Never accept a "CI is expensive" premise without these numbers. Most proposed migrations die here.

```bash
# Run volume and the real window (do NOT extrapolate from a dense burst --
# check the min/max timestamps before you multiply anything out)
gh run list -L 300 --json createdAt,headBranch,name,event,conclusion \
  --jq '[.[].createdAt] | (min), (max), length'

# Where the runs come from. Group by workflow + event + outcome.
gh run list -L 300 --json name,event,conclusion \
  --jq '.[] | .name+" | "+.event+" | "+(.conclusion//"running")' | sort | uniq -c | sort -rn

# The actual bill. Needs the `user` scope, which gh does not request by default.
gh auth refresh -h github.com -s user
gh api /users/<owner>/settings/billing/actions
```

**Do not trust the per-run timing API.** `/actions/runs/<id>/timing` returns
`total_ms: 0` often enough that a whole sample can read as zero billable minutes on a private
repo with real spend. Use the billing endpoint for money and run counts for volume.

What the grouping tells you: a workflow appearing under both `pull_request` and `push` for the
same branch is duplicated triggers. A high `cancelled` count is missing supersession. A workflow
with many runs and nothing to show for them is the next section.

## Prove savings before fleet rollout

Use [ci-speed-diagnosis](../ci-speed-diagnosis/SKILL.md#compare-cache-cost-with-a-clean-install) to compare cache overhead with a clean install.
Record queue time, execution time, summed machine-seconds, and billed cost as separate results.
A faster install does not prove a faster gate. A lower compute total does not prove a lower bill.

Run one real task through each chosen agent provider before dispatching fleet work.
A provider in a catalog can still reject work because its quota is exhausted.
Stop dispatching to that provider after a quota rejection. Resume after access or quota changes.

Keep required tests, secret scans, reviews, and preview checks before merge.
A new CI engine or scheduled post-merge suite must preserve those gates.
Pilot one repository first. Report measured results before applying the change elsewhere.
Do not present a target such as 5–10x as an achieved result.

## Match verification to the delivery path

Qualify the local gate and actual deployment checks before removing repeated
remote work. Keep PRs cheap. Broad remote suites can stay manual and required
on production candidates or queue refs, rather than every main update.

Use [the shared development and release policy](../high-volume-ci-optimization/references/development-and-release.md)
for the cutover checks. It covers exact production inputs, skipped waits,
cancellation, safe pool drains, review proof, and billing limits. Where the
local and deployment path is not qualified, retain broad checks while measuring.

### Historical baseline

Measured 2026-10-24, wall-clock minutes on the `boat` runner label — not billed
minutes, so the GitHub invoice does not move when these runs stop:

| Repo, window | On `pull_request` | On `push` to `main`/`release` |
|---|---|---|
| Multi-site monorepo, 16.9 h | CI 161 min / 22 runs (median ~129 s); jscpd ~10 min; vibecodereview 28 min / 23 runs | CI 88 min / 8 runs |
| Single-app repo, 22.2 h | unit-tests 120 min / 23 runs (median 266 s); Worker Preview 243 min / 33 runs | unit-tests 46 min / 11 runs |

At 1,000 pull requests a day, one single-app-sized suite per PR is about 73–87
boat-hours; a 7-minute preview per PR is about 117 boat-hours plus a preview
database per branch. The ratio was about two PR runs per main run, and the
main run is still paid.

### Current placement decisions

| Work | Placement after qualification |
| --- | --- |
| Secret scan and deterministic PR policy | Keep cheap checks on the PR |
| Lint, typecheck, and existing tests | Local gate before push; broad remote runs on required production candidates or manual dispatch |
| Generic build before a real deployment build | Remove the repeated development build after proving equivalent input coverage |
| Paid review inference | Disable workflows and label callers; keep deterministic review proof |
| Browser smoke | Keep actual deployment and production checks |
| Worker preview | Run when required for the change; retain operator rules |

**Retain required Worker previews.** Follow the repository's operator rules
for visible changes and third-party behavior. A preview can verify authentication,
API contracts, and integration behavior as well as pages. Keep that evidence
bound to the current revision. Use labels or path gates only where they preserve
those requirements. Metadata edits do not need a new application deployment.

**Agents run the cheap loop locally.** Lint, typecheck, and unit tests run in
the checkout the agent already has, before the pull request opens. The deployment checks the merged revision. Broad production checks verify the
candidate that can ship.

**Agents are not the referee.** An agent under pressure will skip a test or
edit the workflow so the check looks green. Add a `pull_request_target` job
that runs its script from `main`, not from the PR branch, and fails when the
diff deletes a test, adds a `skip` or `.only`, or edits `.github/workflows`
without a human label such as `policy-change`. The honest limit: this
personal account cannot enforce it — rulesets and branch protection on the
private repos return 403 "Upgrade to GitHub Pro", and a private merge queue
needs a paid organization plan on top. The red check stops an honest agent.
It does not stop an agent allowed to merge its own red pull request.

**Preserve production verification.** A qualified development deployment can
skip its repeated CI wait. Production still needs a successful required suite
on the production branch at the exact revision. A result from another branch
is insufficient. Handle skipped dependencies and cancellation explicitly.
Keep canary order, migrations, environment restrictions, smoke checks, and
serialization. A revert cannot undo sent email or every migration.

Keep queues where measured contention and integration risk justify them. For
broad checks that remain required, let the in-flight run finish and supersede
older pending runs. Never cancel an active production deployment for capacity.

Affected-only test selection is a later step, not the first move. It needs a
full reference run on matching inputs — the controls in
[ci-selective-evidence](../ci-selective-evidence/SKILL.md) are what qualify
it — and it does not require adopting Nx, Bazel, or Turborepo. The example monorepo
already runs Wireit.

## Ship first, verify after

This section is an opt-in alternative to the "Preserve production verification" rule above. It
replaces a required suite at the production revision with checks after the deploy. Use it only when
all of these hold: the owner chose it; code rollback is a complete undo (no sent email, payment, or
destructive migration); the agent's own pre-push gate is enforced; and the pipeline has a canary,
live smoke checks, and automatic rollback. Measured contention must show that the gate cost more
than the bad changes it caught. Merge volume alone does not show that. When any condition fails,
keep the gate. One pilot used this shape. Report your own measured numbers before you roll it to
more repos. Do not quote the pilot's numbers as yours.

**Measure first. Two findings changed the plan.**
- **Wait beat run time.** In the last gated release run, test shards ran 6 to 10 minutes and each
  waited 20 to 48 minutes for a runner. The release path took 59 minutes. A busy account queues
  every job behind every other job, so the first fix is fewer jobs, not faster jobs.
- **Cost followed job count.** A median 15-second job bills about what a one-minute job bills,
  because the box start dominates. Merge steps into one job. Do not add a job to save a minute.
- Group by workflow and event before you decide. In the pilot, scheduled probes were 46% of all
  jobs. Check the default branch first: another agent had already moved them to a one-core hosted
  runner.

**The shape that worked.**
1. The agent proves the change on its own machine. The pre-push gate is the only blocking *CI* check.
   Keep every other rule that applies before merge: required reviews, secret scans, and Worker
   preview walks for user-visible changes. Drop one only if the owner replaces that rule in writing.
2. A push to the trunk deploys production. No staging stage, no release branch, no CI wait. The
   review and preview rules above still run before that push lands.
3. Diff from the last *successful* deploy run, not from the previous push. A deploy run that a newer
   push replaced while it waited deploys nothing, and a previous-push base then loses its changes.
4. Deploy a canary first. Run a live smoke and a read-only browser smoke on its real host. Fan out
   to the rest only when both pass.
5. Roll back by itself. A failed live check after the app went live calls the platform's version
   rollback, re-checks health, and opens an issue. Add a manual rollback workflow that builds
   nothing and takes one unit per run.
6. CI becomes a net. Run the cheap checks on every trunk push, batched: a concurrency group that
   does not cancel keeps one run going and one waiting, and a newer push replaces an older waiting
   one. Run the full end-to-end suite on a schedule. A red result opens an issue.
7. Write migrations as expand, then contract. A rollback restores code and leaves the schema, so
   old code must run on the new schema. Two pushes are not two deploys: a newer push can replace a
   pending run. Contract only after the compatible code reached every target, and keep every
   version you could roll back to compatible with the contracted schema.
8. Keep staging as a manual dispatch input and write a "bring staging back" note. Removal is then a
   switch, not a loss.

**What went wrong, so you can skip it.**
- **Gating to save pennies.** Two reviews each found that a small saving removed real coverage:
  cleaning up previews only for labelled pull requests (about 17 small jobs saved in two days, and a
  race that left a preview live), and dropping the push secret scan (direct pushes become the main
  path, so the push scan matters more). Both were reverted. Cut a gate only when the saving is large
  and no live window is left.
- **One concurrency group for two event types.** A scheduled run and a push share a ref. Put the
  event name in the group key, or the long scheduled suite blocks the push checks.
- **An unrun deploy command.** Run each deploy step's real command against its real target before
  you ship it. The pilot's first deploy failed because a tool rejected a flag, so every deploy failed
  at the same step until the command was fixed. The rollback worked, and that was luck, not a check.
- **An unproved rollback.** The rollback step cannot be tested without a real deploy. Run a rollback
  drill on a low-traffic unit before you rely on it.
- **A reviewer that never says done.** An adversarial review keeps finding narrower windows. Set the
  bar first: a Major needs a realistic sequence that leaves harm and no recovery path.
- **Local tooling traps.** A symlinked sibling dependency folder sits outside the bundler's root, so
  copy it. Build caches survive a reinstall, so clear them. A guard hook that matches command text
  can fire on a heredoc that only *mentions* a push, so write documents with an editor tool.

## Fix in this order

Each rung is cheaper and lower-risk than the one below it. Stop when the pain stops.

### 1. Delete work that produces nothing

The highest-yield bug in this class: a **deploy workflow that triggers on `pull_request` while
every one of its steps is gated on the branch ref.**

```yaml
on:
  pull_request:        # <- fires
jobs:
  deploy:
    steps:
      - run: ./deploy.sh
        if: github.ref == 'refs/heads/main'   # <- never true on a PR
```

Each PR pays full checkout, toolchain setup and dependency install — the slow part — then skips
every real step and exits green. It looks healthy in the UI. Grep for it:

```bash
# workflows that trigger on pull_request AND ref-gate their steps
grep -l "pull_request" .github/workflows/*.yml \
  | xargs grep -l "github.ref == 'refs/heads/"
```

**While you are in there, check every step for a gate.** These workflows usually have one step
someone forgot to gate — a cache purge, a notification, a metrics push — and it has been firing
on every pull request for months. That is a correctness bug wearing a cost bug's clothes, and
it is the reason this rung comes first.

### 2. Concurrency groups

Supersession. Without a group, pushing to a PR leaves the old run going and starts another
beside it. At agent scale, where bots push repeatedly, this is the difference between one
pipeline and four.

```yaml
concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true
```

| Workflow kind | `cancel-in-progress` |
|---|---|
| test, lint, typecheck, build, scan, review | `true` |
| deploy, migrations, release, publish | `false`, or no group at all |

**Never cancel a deploy.** A run killed partway through a migration is worse than a queued one.
And skip the group entirely on release-tag publish workflows — they fire once, so it buys nothing.

### 3. Path filters on the heavy suites

A docs-only PR should not run a 20-minute e2e suite. Agents generate a lot of docs-only PRs.

A path filter cuts the runs. It does not cut what one run costs. For that, and for the question of
whether the suite gates anything at all, see [e2e-ci-economics](../e2e-ci-economics/SKILL.md).

```yaml
on:
  pull_request:
    paths-ignore:
      - "**.md"
      - "docs/**"
```

Three rules:

- **Never path-filter a secret scanner.** A credential lands in a markdown file as easily as in
  source.
- **Check for required status checks first.** A filtered-out check never reports, and a *required*
  check that never reports leaves the PR stuck on "waiting for status" forever. Either use a
  companion skip-job that reports success, or confirm the check is not required.
- Keep the ignore list identical across workflows. Mixed lists mean one workflow's opinion of
  "docs-only" disagrees with another's.

### 4. Share the build cache

The biggest per-run win on a monorepo, and it needs no provider change. Agentic PRs usually touch
one package; without a shared cache every runner rebuilds the whole graph. Point the build tool's
remote cache at object storage you already pay for.

**The trap:** a warm cache masks base drift. A PR can pass entirely from cache while `main` is
broken, and the breakage surfaces later on an unrelated PR that happens to bust the cache. Keep a
scheduled cache-cold run on the default branch so drift surfaces on a schedule instead of
ambushing whoever pushes next.

### 5. Change runners — price decides this, not queue time

For Boat CI, first apply the [qualification rules](boat-ci-qualification.md).
Read them before changing labels, snapshots, pool capacity, or job isolation.


Use the warm Boat JIT pool for private `itsryanarmani/*` Linux CI. Use `boat`
for build, lint, typecheck, test, E2E, and deploy. Remove avoidable polling
before adding capacity. Use `boat-8` for a
heavy production build. Public repos and macOS/Windows jobs stay GitHub-hosted.

```yaml
runs-on: boat
```

Prices measured 2026-10-11:

| Provider | 2 vCPU / hour | 4 vCPU / hour | 8 vCPU / hour |
| --- | --- | --- | --- |
| Boat | $0.018 (4 GB) | $0.036 (8 GB) | $0.072 (16 GB) |
| Ubicloud (comparison) | $0.075 | $0.15 | $0.30 |

Boat's 4 vCPU rate is 24% of the comparison rate. An always-on pool bills
wall time, not job time. Include idle Boxes in the cost. $1 buys 100,000
Box-seconds. N default Boxes cost N × $0.036 × hours online.

Keep Boxes warm; run one JIT runner at a time on each. The broker holds the
GitHub token and hands configs to the Box agent. JIT labels do not include
`self-hosted` unless passed. See [self-hosted-runner-fleet](../self-hosted-runner-fleet/SKILL.md)
for pool setup and actionlint labels. These components are in progress in
`itsryanarmani/scripts` #508 and #509; a label edit alone does not create capacity.

### Historical managed-runner comparison

The arm and queue measurements below came from the retired Ubicloud setup.
They are comparison data, not Boat sizing or dispatch instructions. Measure
Boat queue delay and memory use before changing pool size.

**Do not move to arm64 for a PR gate. It is measurably more expensive.** The pricing table
makes it look free: Ubicloud arm64 costs *exactly the same per minute* as x64 at every tier, an
arm vCPU is a **dedicated physical core** while two x64 vCPUs **share** one, so
`ubicloud-standard-2-arm` has the same core count as `ubicloud-standard-4` at half the price.
That reasoning is right about core *count* and wrong about core *throughput*.

Measured, same repo, same commit, re-run twice to rule out a cold cache:

| Step | x64 `standard-4` | arm `standard-2-arm` |
|---|---|---|
| `npm ci` | 2s | 6s |
| `tsc -b` | 5s | 15s |
| `eslint` | 4s | 11s |
| `vitest run` | 10s | 47s |
| **Job total** | **32s median** | **92s** |
| **Cost per run** | **$0.00133** | **$0.00192 (+44%)** |

Ampere Altra Q80-30 (Neoverse N1, 3.0 GHz) delivers roughly **a third of an x64 core** on
single-threaded Node/TypeScript work. Billing is per wall-clock minute, so a half-price tier
that runs 2.9x longer costs **44% more**, and the PR waits three times as long.

**Arm is worth it only when the job is wall-clock-insensitive and genuinely parallel across
cores** — a nightly, or a matrix leg nobody is waiting on. Never for a gate.

Before any tier drop, x64 or arm, **grep the workflow for `--max-old-space-size`**. Arm gives
3GB per vCPU against x64's 4GB, so 4 vCPU is 12GB, not 16GB. A job asking for a 12288MB heap
cannot survive a drop to `ubicloud-standard-4-arm`.

If you do move a batch job, the real arm64 blockers, in the order worth checking: **`puppeteer`
as a real dependency under npm** (its postinstall fetches Chrome for Testing, which has no
`linux-arm64` build at all — under bun it is inert unless listed in `trustedDependencies`);
Tauri or any `--target x86_64-*`; Docker steps on amd64-only images; an arch string hardcoded in
a `curl` release URL. **Playwright is not a blocker** — 1.58+ ships linux-arm64 for chromium,
firefox and webkit. Most prebuilt-binary packages are fine: check the lockfile for the
`-linux-arm64` sibling of each `-linux-x64` package.

Other managed runners (Blacksmith, Depot, Namespace, WarpBuild) sit in the same band and are
also a label swap; some require a GitHub **org**, so check before planning on a personal
account. A licensed self-hosted fleet (RunsOn and similar) or your own always-on box goes
lower still, at the cost of owning patching and isolation yourself.

**The honest cost of moving: about 17s more queue time per job.** Measured queue time to pick
up a job, same repos, same week:

| Runner | n | Median queue | p90 |
|---|---|---|---|
| `ubuntu-latest` | 131 | **2s** | 4s |
| `ubicloud-standard-4` | 40 | 19s | 30s |
| `ubicloud-standard-2` | 27 | 19s | 25s |

That 17s is real — say it plainly rather than claiming a managed runner starts faster. It is
just a much smaller number than a 6x price gap plus round-up waste, so it is not a reason to
keep short jobs on the expensive runner. **A latency measurement without a cost measurement is
half an answer** — this same table, read alone, argues the other way, and did once already.

**Exceptions — keep these on GitHub-hosted:** public repos, macOS/iOS or Windows, an action that only works
on the GitHub-hosted image, or preinstalled software a managed runner doesn't carry. If the
driver is queueing rather than price, only a provider running in **your own** infrastructure
lifts the concurrency ceiling — a cheaper managed runner usually carries its own limit too.

Sample size decides the queue number too. An 8-sample measurement put `ubuntu-latest` queue at
164s and nearly moved 46 repos on that basis; 131 samples put it at 2s. **Take more than 100
samples before a fleet-wide migration.** A cold-start outlier dominates a small sample, and
queue time is exactly the metric that produces them.

**Recency decides it too.** A fleet audit ranked roughly 15 repos at the top on 400–880s
medians. Every one was **n=1, from a burst rollout nine days earlier**, and none had run CI
since. Optimizing them would have moved nothing. Before you trust any per-repo ranking, check
when each sample last ran — a median over one stale observation is not a median.

## Agent sandboxes need a runner control plane

This proposal recurs, so it gets its own section. E2B, Daytona, Modal, Vercel Sandbox and
Cloudflare's Sandbox SDK are **compute primitives**: call an API, get a container, run code, tear
it down. What they do not have:

- no `runs-on:` label — GitHub does not know they exist
- no job dispatch, no just-in-time runner registration
- no secrets injection, no artifacts, no build cache, no matrix, no PR status checks, no log UI

To use one as CI you write: webhook listener → mint a JIT runner token → boot the sandbox →
install the runner agent → register → run → tear down → ship logs. **That control plane is
precisely the product the managed-runner vendors sell.** Compare the full pool wall-time cost before choosing the compute provider.
Boat uses this pattern with warm Boxes instead of a fresh sandbox per job.

They also tend to be sized for short-lived agent tasks, not builds. Check the disk ceiling before
anything else — a serverless container platform capping at tens of gigabytes of *ephemeral* disk
cannot hold one monorepo checkout with dependencies installed, let alone cache it between runs.

Sandboxes are the right tool for **executing code you do not trust** — agent-generated snippets,
user submissions, per-task blast radius. Keep them for that.

## Also fix the bot that multiplies everything

Whatever review or fix bot runs on your PRs, two settings dominate its cost:

- **Its fix-cycle budget.** Each auto-fix commit is another `synchronize` and another full
  pipeline. Past the second pass the bot is usually arguing with itself. Set the budget to 1 or 2
  on busy repos.
- **How it counts its own commits.** A loop guard that matches any `*[bot]` author will count an
  unrelated bot's commit sitting at HEAD and silently stop fixing. Guards should match the bot's
  own committer identity.

And the structural lever, which beats every tuning knob above: **fewer, larger PRs.** Batching a
fleet's output into one PR per logical change cuts the multiplier at the source instead of making
each multiplied run cheaper.

## Per-author CI credentials on GitHub Actions

A repo owner wants contributor B's CI runs off his personal AI subscription tokens. GitHub
offers no per-user secret for this. Secrets are repository-scoped: a workflow triggered by
contributor B still reads the repo's secrets. Adding secrets needs ADMIN — a collaborator
with write/push access cannot add their own.

Route by author with a ternary. It works reliably:

```yaml
env:
  AI_API_KEY: ${{ github.actor == 'someone' && secrets.KEY_SOMEONE || secrets.KEY_DEFAULT }}
```

Prefer this over dynamic `secrets[format(...)]` indexing. Its behaviour in step-level
`with:`/`env:` could not be confirmed from GitHub's documentation.

Know what routing buys. It buys spend attribution: each author's runs bill their own token.
It does not buy isolation. The owner still stores every contributor's token. For a same-repo
(non-fork) `pull_request`, GitHub runs the workflow file as committed on the PR branch with
full secrets access — a push-access collaborator can edit the workflow to reference any
secret. An `if: actor == owner` guard is cosmetic, not a boundary.

The only platform-enforced boundary is fork-based contribution: forked `pull_request` runs
get zero base-repo secrets. Environments with required reviewers would impose a real gate,
but on a private repo that protection rule needs **Enterprise**. Pro and Team buy you
environments on a private repo, not the protection rules that would gate them.

Use author routing for attribution on a trusted team. Require forks for untrusted
contributors. Never present routing as isolation.

## Gotchas

| Symptom | Cause |
|---|---|
| A sampled set of runs reports 0 billable minutes on a paid private repo | The per-run timing API is unreliable. Use the billing endpoint. |
| Extrapolated monthly minutes look absurd | The sample window was a dense burst. Always read min/max timestamps before multiplying. |
| `gh api .../settings/billing/actions` returns 404 | The token lacks the `user` scope. `gh auth refresh -h github.com -s user`. |
| Branch protection API returns 403 on a private repo | Required status checks need a paid plan. Also means path filters cannot deadlock a check — verify rather than assume. |
| A new PR gets no workflow runs at all, while other branches do | GitHub scheduling lag, which can exceed five minutes under load. Confirm with an empty commit before diagnosing the diff. |
| Workflow triggers look fine locally but behave differently in CI | You read the file from a stale branch. For `pull_request`, read the workflow as it exists on the base and head refs, not from your working tree. |
| A `push: branches: [main]` workflow has never once run | The repo has no `main` branch. Nothing reports this — a trigger that never fires produces no failure and no run to notice the absence of. Check every `branches:` filter against branches that actually exist. |
| CI is green on every PR, but the production branch is never gated | The filter is `pull_request: branches: [main]` in a repo that also has `release`. It fires, so it looks healthy — it just never fires for the branch that matters. List every deployable branch in the filter, not only the default one. |
| A move to arm64 raised the bill and slowed the gate | Arm cores are ~3x slower per thread on Node work, and billing is per wall-clock minute. Equal core count is not equal core speed. Pilot and measure before rolling out. |
| A cost-audit script silently returns nothing | BSD `xargs` has no `-a`; `xargs -I{}` drops tab-delimited fields. Test the pipeline on one input before fanning out. |
