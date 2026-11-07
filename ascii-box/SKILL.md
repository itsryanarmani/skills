---
name: ascii-box
description: "Use ascii.dev Boxes for fast, correctly-configured build environments on personal repos — one Box per worktree via crabbox. Covers warm snapshots with node_modules, per-repo box env for Turborepo remote cache, the box-warm-shim for --from/--environment, TTL vs idle reaping, and trade-offs around snapshot limits, plaintext env listing, and zero-data-retention. Use when asked about ascii.dev, Boxes, box env, warm boxes, crabbox ascii-box provider, or turbo remote cache on personal repos."
---

# ascii-box

Boxes are remote Ubuntu VMs from ascii.dev. crabbox attaches one Box per git worktree so an agent gets a ready build environment. The goal is fast, correctly-configured build environments for a high-volume agent fleet. Provision is already fast. The real bottlenecks are worktree sync and dependency install.

> **Scope: personal repos only.** ascii.dev is a third-party provider. Never put Mozilla, work, or proprietary source on a Box. This skill applies only under `~/Documents/Personal` and personal GitHub repos.

## Why this exists

A Box used to take ~77s to become useful and came up misconfigured. The brief assumed provisioning was the bottleneck and that a warm image would cut it to ~1s. Provision was never the bottleneck. A real `git worktree add` on private-repo-4ed5 (693 files, 3.9 MiB) breaks down as:

```
lease (box new + provision) ....... 14.3s
bootstrap ......................... 10.1s
sync .............................. 48.7s   <-- the real cost
    rsync 19.7 | ssh 7.6 | finalize 4.5 | git_seed 4.0
    manifest_write 4.1 | fingerprint_remote 3.7 | prune 3.7
command (apt check + bun install) . 14.9s   (bun install itself 7.2s)
-------------------------------------------
total ............................. 1m16.8s
end to end ........................ 1m38.3s
```

Two thirds of the wait is rsyncing the worktree. Dependency install is 15s of 77s. A snapshot that only caches `node_modules` fixes the smaller half. The work below fixes the misconfiguration and that smaller half, and shows where the next win lives.

A warm Box is slower to first usable command, not faster:

| Box | ready | first usable command |
| --- | --- | --- |
| cold (`base`) | 0.8–1.3s | 2.0–2.6s |
| warm (`--from` a 651 MB snapshot) | 0.9–1.0s | 6.6–9.1s |

Measured 2026-08-28 on real hardware. Three cold runs: ready 1.0s/1.3s/0.8s, first command 2.1s/2.6s/2.0s. Three warm runs: ready 0.9–1.0s, first command 6.6–9.1s. Restoring the filesystem costs time. The warm Box wins overall because it skips install entirely, not because it boots faster. `ready` is not a number you can do work in.

## Steps to repeat

### 1. Measure where time goes

Run a real `git worktree add` that fires the crabbox hook. Record lease, bootstrap, sync (with rsync/ssh/finalize/git_seed/manifest_write/fingerprint_remote/prune), and command phases separately. Do not trust `ready` alone. Measure first usable command.

### 2. Fix secrets so the Box configures correctly

crabbox copies gitignored files to the Box before it installs. With no `.crabbox-secrets` manifest it copies the worktree root only. Content Rabbit then got the 5-key root `.env.local` but not the 221-key `apps/website/.env.local`. The Box installed cleanly and failed at runtime.

Create `.crabbox-secrets` in the repo root. It lists paths only. It holds no values. It is committed.

| Repo | manifest contents |
| --- | --- |
| private-repo-c4e6 | `.env.local`, `apps/website/.env.local` |
| private-repo-4ed5 | `.env.local`, `backend/.dev.vars` |
| private-repo-f304 | `.env.local`, `apps/web/.env.local`, `apps/web/cloudflare/app-worker/.dev.vars` |
| private-repo-5073 | `.env.local` |

Two judgement calls:

- `private-repo-4ed5` `backend/.env.local` stays out. It holds live Stripe keys and the production BYOK encryption key. Nothing in `backend/src` or `scripts/` reads its six names. The runtime reads the unsuffixed names from `.dev.vars`. A build Box does not need it, and a Box is a third-party VM.
- `private-repo-f304` lists two files with identical contents (`apps/web/.env.local` and `apps/web/cloudflare/app-worker/.dev.vars`). Next.js reads one. Wrangler reads the other. Drop either and one runtime misconfigures.

### 3. Make the Turborepo remote cache actually hit — `box env` per repo is the main mechanism

The credentials already reach the Box inside the root `.env.local`, but nothing exports them and the remote script never runs turbo. Every build is cold.

`box env` is how a Box gets a repo, its env files, and its credentials with nothing uploaded from the laptop. Three commands:

- `box env add-repo <env> <owner/repo> --branch <b>` — clones the repo into every new Box.
- `box env set-file <env> <in-box-path> --from <local file>` — writes a gitignored env file in.
- `box env set-var <env> KEY=VALUE` — sets an environment variable.

Create one named `box env` per repo. It carries `TURBO_API`, `TURBO_TOKEN`, and `TURBO_TEAM`. Verify the Box receives them in its environment.

Credentials are two separate switches, and they deserve opposite answers:

- `--box-credentials false` — always. These let a Box create and control other Boxes, which is the escalation that actually matters.
- `--agents-credentials true` — if you want to run agents there. I set this to `false` first, and it made every repo Box useless for delegated work: the agent CLI logins live in the separate `agent-roster` environment, so a Box started from a repo environment had no muse, pi, gemini or codex at all. Copy `agent-roster`'s five secret files into the repo environment (`box-env-provision --with-agents`) and turn the flag on. This does widen the blast radius, and it is a deliberate trade: the keys are already stored on ascii under `agent-roster`, so copying them does not hand them to anyone new — it only means more Boxes carry them. One `box new --environment private-repo-c4e6` then gives, with nothing uploaded from the laptop, in 8.4–10.7s: the repo cloned (5,870 files, on main), root `.env.local` with 7 keys, `apps/website/.env.local` with 221 keys, and 3 `TURBO_*` variables. 61 private repos now have an environment. Provision all with `box-env-provision --all --private-only` in `itsryanarmani/scripts`.

Proof on a real Box:

| Run | state | result |
| --- | --- | --- |
| A | as crabbox leaves it today | `Remote caching disabled` · 0 cached · 6.022s |
| B | `TURBO_*` exported | `Remote caching enabled` · miss, populates remote · 6.718s |
| C | local `.turbo` deleted first | 2 cache hits from remote · 605ms · `FULL TURBO` |

Run C deletes the local cache first, so the hit can only come from the remote. It is 10x faster.

### 4. Let crabbox start Boxes from a warm snapshot

crabbox shells out to `box` but forwards only three ascii-box settings: `-ascii-box-base-url`, `-ascii-box-cli`, `-ascii-box-workdir`. There is no way to pass `--environment` or `--from`. Every crabbox warmup starts from the bare `base` image no matter what snapshots exist.

`scripts/box-warm-shim` stands in for the `box` binary. It injects `--environment` and `--from` on `new` and passes every other subcommand through untouched. No crabbox change is needed. Wire it with `-ascii-box-cli`:

```sh
# crabbox config points at the shim instead of the real box binary
-ascii-box-cli /path/to/scripts/box-warm-shim
```

The shim pins the Box to the repo's environment (for example `private-repo-4ed5` v5) and to its named snapshot (for example `private-repo-4ed5-ready`). Verified end to end: Box pinned to environment `private-repo-4ed5` v5, 732 MB of `node_modules` restored, `TURBO_*` present, warmup 17.1s.

### 5. Stop reinstalling what the base image already has

crabbox apt-installs `curl git build-essential python3 pkg-config` and then installs bun. The base image ships `node` 24, `bun` 1.3.14, `git`, `gh`, `gcc`, `make`, `python3`, `pkg-config`, `rg`, `jq`, `docker`, `ffmpeg`, Chrome, plus Go, Rust, Java, Ruby and PHP. It looks like crabbox wastes time apt-installing that on every attach. It does not: the step is guarded by `command -v curl / git / gcc`, all three are present, and it never fires. Verified on a real Box. There is nothing to cut here, and it is worth recording because it is the obvious-looking optimisation that turns out not to exist.

### 6. Build the warm snapshot (scrubbed)

A snapshot is a filesystem image. It outlives a key rotation. Scrub secrets before you save. The `private-repo-4ed5-ready` snapshot was scrubbed of `.env.local` and `.dev.vars` first. The environment injects config at boot instead. A Box deployed from it has no secret files and full `node_modules`.

Refresh by saving the same name again. The name points at the new state and the old artifact is released. Boxes already deployed from it stay up. If a re-save fails, the name still deploys the last good save.

Content Rabbit has no warm snapshot yet. The repo now clones from the GitHub app directly (see Gotchas), so seed the snapshot from a Box — no laptop push needed.

## Trade-offs — be honest and two-sided

**Environments and snapshots cost nothing.** `box limits` exposes no storage quota, no snapshot quota and no byte counter; every billing field it returns is time-based. Billing is per running second. A `box new` with no `--ttl` reports `ttlSeconds: 3600` and archives exactly 60.0 minutes after creation, so a forgotten Box costs about $0.036 at most.

**Warm is slower to first command, faster to ready-to-build.** Cold `base` reaches first usable command in 2.0–2.6s. Warm from a 651 MB snapshot needs 6.6–9.1s to the same point, even though `ready` looks similar (0.8–1.3s cold vs 0.9–1.0s warm). The win comes from skipping `bun install` (7.2s) and the rest of the command phase (14.9s), not from a faster boot. Quote `ready` and you mislead.

**Zero-data-retention and named snapshots are mutually exclusive.** Enabling ZDR deletes existing named snapshots and blocks creating new ones. It also queues every archived Box for deletion. Deletion operations that are already accepted cannot be cancelled. Disabling ZDR only affects future archives. You must choose. This repo keeps snapshots and leaves ZDR off. Backing data for a removed snapshot is held for at least six hours so signed upload URLs expire.

**`box env list` prints stored secret files in plaintext.** Anyone who can run the CLI can read them. That is why repo environments carry `TURBO_*` only. App secrets stay out of Box environments and travel per-run over the crabbox sync path instead.

**Webhooks cannot drive idle-reaping.** `box webhook` fires on `ready`, `error`, `archived`, and `hydrated` only. There is no idle or activity event. Do not wire webhooks to reap idle Boxes. The existing `box-reap` stays the mechanism: it does not reap on Box state (a Box at 100% CPU still reports `idle`), it measures CPU and load and prefers a heartbeat file.

**Max 10 named snapshots per account.** One per repo works. One per worktree does not. With four repos, four names fit. With dozens of worktrees, the cap forces churn. Plan `box_20` also caps starts, not just concurrency: 100 concurrent, 50 starts/hour, 150/day. The hourly start ceiling limits an agent fleet before concurrency does. Check `box limits` (`starts.hour.remaining`) before any fan-out.

**Auto-stop is a TTL, not an idle timer.** Default is 1 hour — `box new` with no `--ttl` reports `ttlSeconds: 3600` and archives exactly 60.0 minutes after creation — max 30 days (2592000s). The timer counts from creation or resume, never from last activity. A Box with a 1 hour TTL stops one hour after it started, even mid-work. At expiry it stops and snapshots. It is not deleted. Nothing stops a Box for being unused unless you call `box stop`. `--no-auto-stop` disables the TTL and the Box runs until you stop it. Default forgotten Box costs about $0.036 at most (per-second billing).

## Setup scripts do not work — both routes are dead ends

Neither documented way to run per-repo setup on a Box works today. Verified 2026-08-28:

- **`setupScript` on an environment's repo entry.** The field exists in the API response. `PUT /api/box/v1/environments/{id}` with it populated returns **200 and `environment.updated`**, and the field reads back empty. A clean success that changed nothing. There is no `--setup-script` flag on `box env add-repo`.
- **`box new --setup-file <path>`.** `setupStatus` stayed `pending` indefinitely, `setupError` stayed null, the script never ran, and `node_modules` was never installed. It also made the Box **6x slower to first usable command — 52.7s against 8.5s without the flag**.

Do the work yourself after boot instead. `box exec` is verified and takes ~1.2s, and `box exec --detach` runs past the 600s cap. That is what `box-git-sync.sh` does: fetch the commit, then `bun install`, then write a lockfile-hash marker so the next attach skips the install.

## Gotchas that cost real time

- **`sizeBytes` on a named snapshot is not the restored size.** `private-repo-4ed5-ready` reports 32,830 bytes and restores 651 MB. Snapshots are incremental deltas on a chain. The first is a full base; each later one stores only what changed, compressed and deduped. `sizeBytes` is the compressed delta. Restore reassembles the full tree through the chain. Deploy from the snapshot and look; do not judge by that number.

- **The ascii GitHub token is a scoped app token — this changed 2026-08-28.** It previously saw 44 public repos and 0 private ones, so `box env add-repo` and in-box `gh repo clone` failed with 404 for every private repo. It now sees 64 private repos. In-box clone speeds measured: private-repo-c4e6 (5,863 files) 3.23s, private-repo-4ed5 1.06s, private-repo-f304 1.15s. `bun install` for private-repo-c4e6 9.80s, producing 1.9 GB of `node_modules`. New private repos still need connecting in the ascii dashboard before `add-repo` or `gh clone` can see them.

- **T3 Code threads get no Box, and that is correct.** The attach is a `git()` shell function in `~/.zshrc` that intercepts `git worktree add`. A shell function only exists in an interactive zsh: `zsh -ic 'whence -w git'` prints `git: function`, `zsh -c 'whence -w git'` prints `git: command`. T3 creates its worktrees from a Node child process, so the wrapper never fires. Independently, T3 runs git, diffs and terminals on its own disk, so an attached Box would sit idle and bill while the agent worked locally. Do not auto-attach on T3 worktree creation. Run `box-fast-attach` deliberately when you want a remote build. T3's own hook would be a `t3.json` at the repo root with a `scripts[]` entry marked `runOnWorktreeCreate: true` — documented, untested here.

- **The shim has two silent traps.** crabbox calls `box --no-update --json --api-url https://ascii.dev new --ttl 900`. The subcommand is not `$1`. A naive "first bare word" scan picks up `https://ascii.dev`, the value of `--api-url`. The shim then passes through and you get a cold Box that looks fine. Also crabbox runs `box` with `HOME` pointed at its own state directory, so `$HOME/.ascii/bin/box` does not exist. Resolve the real home from the OS user.

- **A green exit proves nothing here.** Three separate steps exited 0 while doing nothing: the shim passing through on a mis-parsed subcommand, `box new --json` emitting JSONL that a single-object parser drops (which leaked three billing Boxes), and the pi+OpenRouter grok worker producing zero bytes in 20 minutes. Always verify by inspecting the result: check the Box is pinned to the expected environment, that `node_modules` restored, and that `TURBO_*` is present.

- **`--type large` is twice the price and not measurably faster.** Do not use it for build Boxes.

- **`box host` URL+token identity is stable across stop/resume, but you must re-issue `host <port>` after a resume to re-register.** `box forward` is an ephemeral local TCP tunnel. It does not survive a resume. Neither matters for an unattended build Box.

## What to wire and what to skip

Worth wiring:

- `box env` — one named environment per repo. Already done for all four repos.
- `box snapshot` / `--from` — the dependency cache. Real win, via the shim.
- `box exec --detach` — runs past the 600s exec cap. Poll with `--status <pid>`, logs at `~/.ascii/processes/<pid>.log`. Detached processes do not survive stop/resume/fork; for durable work use a systemd service.
- `box scp` — simplest way to push a file to a Box.
- `box limits` — check `starts.hour.remaining` before any fan-out.

Not worth wiring, with reasons:

- `box webhook` — no idle event. Cannot drive reaping. That was the only reason to want it.
- `box data-retention` — mutually exclusive with named snapshots. The snapshots are worth more than delete-on-stop.
- `box host` / `box forward` — useful for a human debugging a dev server, not for an unattended build Box. `forward` does not survive a resume.
- `box org` / `box team` — single-user personal account, one wallet. Nothing to scope.
- `box desktop` — no use for a build Box.
- `box api-key` — one key already exists and works. Rotate, do not automate.

## Attaching a worktree in ~1.5s

Measured 2026-08-28 on real hardware. The old path (crabbox) takes ~84s end to end: ~13s lease, ~10s bootstrap, ~43s sync, ~9s install. The sync is rsync wrapped in fingerprint/git-seed/manifest-write/prune/finalize passes costing ~21.6s of FIXED per-run bookkeeping that does not shrink when you change one file. `box-fast-attach` in `itsryanarmani/scripts` is faster: it detects the Box already has the repo, has the Box fetch your HEAD commit itself, then overlays only uncommitted files. Box ready 10.7s, first attach 27.6s, every attach after that 1.69/1.78s.

Transport round trips against a running Box:

| transport | round trip |
| --- | --- |
| `box exec` | 1.2s |
| `box ssh` | 5.2s |
| `box scp` | 6.1s |

`box exec` is HTTPS and needs no SSH and no open port.

`box exec` joins argv into a shell string. Pass one shell-safe word per argument. Never interpolate a payload into `bash -lc "...$VAR"` — a 43k-char blob arrived as ONE byte and still exited 0. A newline inside an argument ends the line and the next field runs as a command. Base64 anything multi-line. As its own argv word, 130,000 chars arrive intact and 150,000 fails with `E2BIG: argument list too long`. The ceiling is the box-side `ARG_MAX`, about 128 KiB. Pass a payload as an argument, never interpolate it into a `-c` string. Also `box exec "$ID" -- bash -c "test -d '$D/.git' && echo yes || echo no"` always answered "no" even with the directory present; use the exit code of a plain `test -d "$D/.git"` instead.

Detecting what changed cost more than sending it. Hashing 694 files with one `shasum` process each took 8.4s locally against 0.6s of real work on the Box. Ask git instead (`git status --porcelain` plus `git diff --name-only <last-sha> HEAD`).

Tool: `box-fast-attach` plus `box-unpack.sh` in `itsryanarmani/scripts`.

Safety:

- Pass a payload as an argv word, not inside `-c`.
- `box exec` runs the command on the Box, so an environment variable exported around the local `box` process never reaches it — that silently skipped every file deletion while still reporting success.

## Security

- `box env list` prints secret-file contents in plaintext. Keep app secrets out of environments.
- Every repo environment sets `--box-credentials false --agents-credentials false`. A build Box needs neither the Box CLI credentials nor the agent logins. One compromised Box otherwise exposes the whole personal AI spend surface.
- Scrub secrets before snapshotting. The environment injects config at boot.
- ZDR and snapshots are mutually exclusive. This account leaves ZDR off.

## Still open

- Content Rabbit has no warm snapshot. The GitHub connection now works (clone in 3.23s), so seed the snapshot directly from a Box.
- The 49s rsync is untouched. It is the dominant cost by a wide margin. A snapshot that already contains the repo checkout would turn the full sync into a delta. That is the next real win, and it is bigger than the install saving just banked.
- The shim is not yet wired into `crabbox-attach.sh` for every repo.

## References

- Docs: `https://docs.ascii.dev/box/` — `quickstart`, `long-running-tasks`, `snapshots`, `environments`, `data-retention`, `webhooks`, `hosting`, `machines`, `billing`, `cli-reference`, `faq`
- Shim: `scripts/box-warm-shim` in this repo
- Related skill: `crabbox-worktree` for the per-worktree attach, sync, and sweep lifecycle
