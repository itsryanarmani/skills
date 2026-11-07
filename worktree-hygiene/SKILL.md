---
name: worktree-hygiene
description: Prune worktrees whose branches already merged. Use on prune worktrees, stale worktrees, clean up worktrees, or worktree cleanup requests.
---

# Worktree hygiene

Remove merged worktrees. Stop scratch buildup.

## Set up scratch ignores

Before listing worktrees, check whether the repo's `.gitignore` already
contains the patterns in `worktree-scratch.gitignore`. If not, append that
block to the repo's `.gitignore` and commit it. Skip this step if the repo
has no `.gitignore` write access; note that in the report instead.

## List worktrees

List all worktrees for the repo.
Read branch and path for each entry.

## Check merge state

For each linked worktree, check its branch.
Treat a branch as merged when any test passes:

- The branch appears in `git branch --merged` against the repo's default
  branch (usually `origin/main`; confirm it rather than assuming `main` when
  the repo uses something else, e.g. `master` or `release`).
- Its PR state reads merged, and the PR's merged head SHA matches the
  branch's current tip (or the tip is an ancestor of that merge commit).
- Its PR shows a merge timestamp, with the same tip check.

Always pass `--repo <owner/name>`, taken from `origin`, to every `gh` call.
Without it, `gh` uses its own default repo. On 2026-10-21 that was
`private-repo-297b` while the checkout was `private-repo-ba8a`, so the lookup read
the wrong repo's PRs.

A PR closed without merging is not merge evidence. Treat "closed" alone as no
evidence, the same as no PR at all. A merged PR whose head SHA predates the
branch's current tip is also not evidence for the current tip: commits pushed
after the merge are unmerged work, so re-check ancestry against the current
tip before treating the worktree as safe to remove.

Skip branches with no merge evidence.
Never guess merge state.

## Check cleanliness

Read worktree status, including ignored files (`git status --porcelain
--ignored`). A plain status without `--ignored` misses ignored-but-uncommitted
files, such as a `.env.local` a repo's own `.gitignore` already hides, and
treating that empty output as clean would delete them unreviewed.
Treat empty status output as clean.
Treat status with only scratch files as clean.
Scratch files are WORKER_BRIEF.md, CONTINUE.md, BRIEF.md, and
WORKER_RESULT.md.
Treat any other uncommitted file as real.

Treat an ignored file as real too, except these regenerable paths:
`node_modules`, `.next`, `.open-next`, `.turbo`, `.wrangler`, `.cache`,
`.parcel-cache`, `.pytest_cache`, `.venv`, `__pycache__`, `dist`, `build`,
`target`, `coverage`, `.DS_Store`. A strict "any ignored file is real" rule sends
every JS worktree to needs-review, because every one holds `node_modules`. A
`.env.local`, `.dev.vars` or key file is never regenerable.

## Check for a live process

Before removal, list the working directory of every running process
(`lsof -d cwd -Fn`). Skip a worktree when any process runs in it or below it. An
agent session may be working there with a clean tree. Report it under skipped.

## Remove safe worktrees

Remove merged and clean worktrees with the git worktree remove command.
For a merged worktree with only scratch files, delete those scratch files
first, then remove the worktree the same way. Plain `git worktree remove`
refuses a worktree that still has untracked files, and scratch files are
untracked until the repo's `.gitignore` picks up the patterns in
`worktree-scratch.gitignore`, so deleting them first keeps this path off
`--force`.
Report each removal.

## Salvage real changes

Never delete a worktree with real uncommitted changes.
Ignored files never get committed or pushed here: they're excluded on
purpose (often secrets or local config), so their mere presence is
needs-review — leave the worktree untouched rather than force-adding them.
Before committing what remains, scan both file names and file contents for
likely secrets: names like `.env*`, `*.pem`, `*_key`, `*credentials*`,
`*secret*`; and content patterns like API keys, private-key headers, bearer
tokens, and connection strings with embedded passwords. If any match, stop,
leave the worktree untouched, and report it as needs-review with the suspect
paths instead of committing or pushing.
Otherwise commit those changes to a salvage branch.
Push the salvage branch.
Once the push succeeds, the changes live on the remote, so remove the
worktree the same way as a clean one. Report it under needs-review, not
removed, naming the salvage branch: the directory is gone, but the salvaged
commit still needs a human to look at it and decide what to do with it.

## Safety rule

Never run rm -rf when the remove command fails.
Verify each directory is a genuine linked worktree first.
Read its absolute git dir.
The path must contain "/worktrees/".
If the git dir equals "<dir>/.git", it is a main clone.
Skip main clones. Never delete them.

## Report

Report three counts: removed, skipped, needs-review.
List each path under its count.

## Implementation

The script `prune-merged-worktrees.sh` in `itsryanarmani/scripts` implements this
workflow for one repo. It runs dry-run by default. Pass `--apply` to remove.

## Run it on a schedule

Do not rely on remembering. `disk-hygiene` in `itsryanarmani/scripts` runs the
prune script on every repo under `$DISK_HYGIENE_ROOTS` (default
`~/Documents/Personal`). When free space is under `$DISK_HYGIENE_THRESHOLD_GIB`
(default 200), it also clears caches that rebuild: npm, bun, pnpm, Homebrew,
Xcode DerivedData and iOS DeviceSupport, Playwright browsers. It logs free space
before and after to `~/.local/state/disk-hygiene/log`, and exits 3 when space is
still short.

Install the launchd agent once with `disk-hygiene-install`. It runs
`disk-hygiene --apply` every 6 hours. launchd cannot read `~/Documents` until
`/bin/bash` has Full Disk Access (System Settings > Privacy & Security > Full
Disk Access). The installer detects the block and says so.

Read the log after a run. Every worktree under needs-review waits for a human.

## What frees space

Measured on 2026-10-21, on one Mac with 222 GiB free:

- Removing 112 merged worktrees freed about 78 GiB.
- Deleting 426 idle `node_modules` directories freed about 3 GiB. APFS shares
  blocks between copies, so `du` overstates the gain. Do not spend effort here.
- The rest of the disk was apps, Homebrew, model folders and personal data. No
  script should delete those. Ask first.
