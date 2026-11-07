---
name: agents-on-boxes
description: "Run agent work on an ascii.dev Box instead of the laptop, so jobs run in parallel without competing for local RAM and CPU. Covers box-work and the SessionStart/SessionEnd automation, what a Box arrives with (repo, secrets, six agent CLIs), the three independent stops that keep cost bounded, box-guard for Boxes created with --no-auto-stop, and what T3 Code can and cannot do. Use when asked to run work on a Box, parallelize agents, offload a build, avoid OOMing the laptop, or wire T3 Code to a sandbox."
argument-hint: the repo and the work you want to run remotely
---

# Agents on Boxes

Run the work on a remote machine instead of the laptop. This is not the same as
attaching a Box to a worktree: attaching keeps a Box *in sync* with a checkout,
this runs the *job* there.

> **Scope: personal repos only.** ascii.dev is a third-party provider. Never put
> Mozilla, work, or proprietary source on a Box. `box-work` refuses any remote
> that is not `itsryanarmani/*`.

## Decide honestly: is a Box the right tool?

A Box is 4 vCPU / 8 GB. A 12-core / 36 GB laptop beats it on any single task.
**One Box is slower. Ten Boxes are faster, and the laptop stays free.** If the
job is one quick edit, do it locally. Reach for a Box when you want several
jobs at once, or when a build would otherwise fight your editor for RAM.

Limits that actually bind, in order:

1. **50 starts per hour.** This bites long before anything else. Keep Boxes warm
   and reuse them rather than starting one per task — reuse is ~4s, a cold start
   is ~100s.
2. 100 concurrent Boxes.
3. Cost: $0.036/h. Ten Boxes for an hour is 36 cents. Billing is per running
   second; environments and snapshots are free.

## The commands

```sh
box-work <repo>                      # start or reuse; syncs your uncommitted edits
box-work <repo> --agent pi "brief"   # run one agent on the Box, headless
box-work <repo> --ssh                # a shell on the Box
box-work <repo> --stop
box-work --list / --stop-all
```

Supported agents: `pi`, `muse`, `kimi`, `codex`, `gemini`.

**Never a bare `claude` on a Box.** ascii injects its own
`CLAUDE_CODE_OAUTH_TOKEN`, which silently bills the wrong subscription. Each
wrapper pins its own `CLAUDE_CONFIG_DIR` and exits non-zero rather than fall
through to the injected token. That refusal is load-bearing.

## What a Box arrives with

From one shared `agent-roster-ready` snapshot plus the repo's own `box env`,
with nothing uploaded from the laptop:

- the repo cloned at its default branch
- the gitignored env files `.crabbox-secrets` declares
- `TURBO_API` / `TURBO_TOKEN` / `TURBO_TEAM`
- all six agent CLIs

Measured on private-repo-c4e6: 123,159 files, the 221-key
`apps/website/.env.local`, 3 `TURBO_*` vars, 1.9 GB of installed
`node_modules`.

## It is automatic — SessionStart warms one for you

`box-session` hangs off the agent harness's own hooks, wired in
`~/.claude-personal{,-1,-2}/settings.json`:

```
SessionStart -> box-session start   # warms a Box in the background
SessionEnd   -> box-session end     # stops it
```

Two gates keep this honest:

- **Opt-in per repo.** No `.crabbox-default-on` at the repo root, no Box, no
  cost.
- **Non-blocking.** The hook forks and returns in 0.38s. A session must never
  wait on a ~100s cold start. By the time you have read the diff the Box is up,
  and `box-work` then reuses it in ~4s.

## Three independent stops, which is the right number

Something that bills by the second should not depend on one mechanism:

1. the `SessionEnd` hook,
2. the 60-minute default TTL,
3. hourly `box-reap`, which measures CPU and honours `~/.box-reap-keep`.

**Never reap on `state`.** A Box pegged at 100% CPU still reports `idle`.

## box-guard: the failure that has no call-site fix

`box new --no-auto-stop` leaves `archiveAfter: null`. Nothing will ever stop
that Box. Five accumulated here in one afternoon, all idle at load 0.00, on
track for ~$155/month.

You cannot fix this at the call site. `box` is a plain binary that any agent,
script or session can invoke, and the zsh `box()` wrapper only exists in an
interactive shell. A convention that every caller must remember is not a
control. So repair the state instead of policing callers:

```sh
box-guard              # report Boxes with no deadline
box-guard --apply      # give each one a deadline (runs hourly from box-reap-cron)
```

`box extend --ttl` sets the remaining lifetime on a **running** Box in place. It
does not stop, restart or disturb it, so it cannot interrupt real work.

`box resume` is *not* the cause — it preserves whatever TTL the Box had.
Verified: create with `--ttl 900`, stop, resume, `archiveAfter` still set.

## T3 Code: what it can and cannot do

**A T3 thread always runs the agent on the laptop.** T3 shells out to provider
CLIs on its own disk, so there is no per-thread Box to arrange. Pointing a
provider `binaryPath` at a Box wrapper gives a green thread that changed
nothing.

The attach is also a `git()` shell function in `~/.zshrc`, and a shell function
exists only in an interactive zsh:

```text
zsh -ic 'whence -w git'   ->  git: function
zsh  -c 'whence -w git'   ->  git: command
```

T3 creates worktrees from a Node child process, so that wrapper never fires.
`runOnWorktreeCreate` in `t3.json` would not help either — T3 sessions here run
in the main checkout, and `~/.t3/worktrees` is empty.

Two real options:

- **Use `box-work` instead of a T3 thread** for heavy or parallel jobs. Tested.
- **Run the whole T3 server on a Box**, reached over `box host`. Then T3's own
  disk *is* the Box. One Box for all threads, not one per repo. See
  `t3-code-on-a-box.md` in `itsryanarmani/scripts`.

## Give `box exec` one shell-safe word

This trap has bitten four separate times in one session, and every time the
call still reported success.

`box exec` joins argv into a shell command string. So:

- A payload interpolated into `bash -lc "...$VAR"` is mangled — a 43k-char blob
  arrived as **one byte**, exit 0.
- A multi-word brief passed raw arrives as its **first word only**. The agent
  then asks a clarifying question and does nothing.
- A **newline inside an argument** ends the line and the next field runs as a
  command (`bash: docs/space: No such file or directory`).

Pass a payload as its own argv word, and base64 anything multi-line. The ceiling
is the box-side `ARG_MAX`, about 128 KiB: 130,000 chars arrive intact, 150,000
gives `E2BIG`.

## Watch the timings, not the exit codes

The expensive failures are silent. `box-fast-attach` once fell back to a full
tree upload because a helper was missing on the Box: exit 0, no warning, **50x
slower**.

```sh
box-perf-check <repo>              # compare against a baseline
box-perf-check <repo> --baseline   # record one
```

`com.pooriaarab.box-perf` runs it weekly. Caught a planted regression cleanly:
`delta 13.15s vs 1.43s baseline (9.2x)`.

**The probe must be a git-TRACKED file.** `box-fast-attach` reads
`git status --untracked-files=no`, so an untracked probe is invisible and the
measurement silently degrades into a second no-op — the same class of bug the
check exists to catch.

## Where the tools live

All in `itsryanarmani/scripts`: `box-work`, `box-session`, `box-guard`,
`box-fast-attach`, `box-unpack.sh`, `box-git-sync.sh`, `box-reap`,
`box-reap-cron`, `box-perf-check`, `box-perf-cron`, `box-env-provision`,
`box-repo-audit`, plus the launchd plists. Background and measurements are in
`box-warm-start.md` and `box-cost-discipline.md`.

Which worker CLIs sign in on a Box, and the traps: `worker-logins.md`.

Related: `ascii-box` for the Box platform itself, `crabbox-worktree` for the
per-worktree attach path, `superset-fanout` for choosing a parallelism model.
