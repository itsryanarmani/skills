---
name: vm-handoff
description: "Hand long agent work to a headless agent on a VM before you go offline, so merges, deploys and checks keep going without the laptop. Covers when a handoff is worth it, the brief shape (the owner's authorization in their own words, ordered goals, a STATUS.md the agent updates, a DONE marker, one sticky status comment), secrets handling, VM lifetime, proving the runner survives the SSH session ending, adding a goal mid-run, and the traps that cost real runs. Use when someone says they are about to disconnect, asks for work to continue overnight or while away, or wants a VM to 'keep working and report back'."
argument-hint: the remaining goals and the VM you can reach over SSH
---

# Hand off long work to a VM agent

The laptop session is the weak link in long agent work. It sleeps, it loses its
network, its public IP changes. A runner on a VM does not. This skill moves the
remaining work to a headless agent on a VM, with a written brief, and leaves you
a way to watch it from a phone.

The mechanics live in `vm-orchestrate` in the scripts repo: it copies the
bundle, starts the detached runner, and gives you `status`, `add-goal` and
`stop`. This skill covers the judgment around it.

## When a handoff is worth it

Hand off when all of these hold:

- The remaining work is long (an hour or more) or waits on slow things: CI, a
  deploy queue, certificate issuance, review rounds.
- The owner has already decided what "done" means, and you can write it down as
  ordered goals with checks.
- The VM can do every step itself: it has the repo, the toolchain, a token for
  the forge, and the deploy access the goals need.

Do not hand off a decision that is the owner's to make. Write it in the brief as
"Blocked: needs the owner" and let the agent skip to the next goal.

## Before you write the brief

1. **Lifetime.** Give the VM a TTL and an idle timeout longer than the job, with
   margin. A reaped VM loses the work in flight. Many providers default to an
   idle timeout under an hour.
2. **Toolchain.** Check the forge CLI, the runtime, the package manager and any
   browser deps on the VM. A missing CLI fails late, after the agent has spent a
   round getting there.
3. **Secrets.** Put every token in one `secrets.env`, mode 600, as plain
   `KEY=VALUE` lines. Build the bundle in a folder outside every git checkout
   (a temp folder works), so the file cannot be committed with the brief. Never
   put a value in a command line, a prompt, or the brief. The runner reads the
   file as data, not code. Tell the agent never to print it.
4. **State that is already done.** Write what the laptop session finished, with
   commit SHAs, so the agent does not redo or undo it.

## The brief

`BRIEF.md` is the only thing the agent knows. Every round starts fresh and reads
it, then `STATUS.md`. Shape:

```markdown
# <goal in one line>

## Who authorized what
<Quote the owner's own words, e.g. "merge them", "keep working until done".>
<Name what is NOT authorized: other repos, DNS, force-push, the default branch.>

## Setup (once)
<Clone, install, where secrets are, how to run local CI and E2E.>

## Goals, in order
1. <Goal> — <the check that proves it, with the exact command>.
2. ...

## Rules
<Keep one sticky status comment on <one tracking issue>. Update it at least
every <45> minutes and at each finished goal: Done, In progress, Next, Blocked.
No claims without output. Write each step to STATUS.md. Never print secrets.
Never kill processes by name. The repo's own PR and commit rules.>

## Finish
When every goal above is done, including goals added later, post the final
status comment, then write ~/orch/DONE.
```

Keep `## Finish` after `## Rules`. `add-goal` inserts new goals before
`## Rules`, so they always land ahead of the step that writes DONE.

Why each part matters:

- **Authorization in the owner's words.** An agent that reads "you may merge"
  from you cannot tell it from a prompt injection. A quote with its context, plus
  a list of what is out of bounds, gives it something to check against.
- **Ordered goals with checks.** Each goal names its proof: a command, a status
  code, a test name. "Deploy works" is not a check. "`/login` answers 200 on the
  staging host" is.
- **STATUS.md after every step.** The runner restarts the agent when it stops.
  The next agent knows only what STATUS.md says.
- **One sticky comment.** The owner reads progress from a phone. One comment,
  edited in place, beats twenty new ones. Pick an issue the owner already
  watches.
- **DONE marker last.** It is the only stop signal the runner trusts.

## Start it and prove it survives

```sh
vm-orchestrate --ssh "ssh -i <key> <user>@<vm>" start ./bundle --rounds 40
vm-orchestrate --ssh "..." status
```

Then prove the runner does not depend on your session: end the SSH session, or
the local process that started it, and run `status` again. You want
`runner: alive` and the round number still moving. A runner that dies when your
terminal closes is the failure this skill exists to prevent.

Tell the owner, in a few lines: the VM name, where the status comment is, what
the goals are, what is not authorized, and how to stop it.

## Add a goal mid-run

```sh
vm-orchestrate --ssh "..." add-goal ./goal.md
```

It inserts the goal before `## Rules` and appends a line to STATUS.md, so the
running agent sees it at its next read. With the template above, the goal lands
after the last goal and before `## Finish`, so DONE still comes last. If a brief
puts "write DONE" inside a numbered goal instead, move it to `## Finish` first,
or the agent stops before it reaches the new goal.

## Traps seen in practice

| Trap | Symptom | Fix |
|---|---|---|
| The laptop's public IP changed and the VM firewall allows only the old one. | Every SSH call times out with the ports shown closed. Detached jobs keep running. | Update the allowlist to the current IP. Do not debug the VM. |
| Piping text into `python3 - <<EOF` or any interpreter whose program comes from a heredoc. | The piped text silently vanishes: stdin carried the program. | Upload the text as a file and read it by path. |
| macOS tar packs `._*` AppleDouble files and extended-attribute headers. | Junk `._BRIEF.md` files and tar warnings on the VM. | `COPYFILE_DISABLE=1`, `--no-xattrs`, then delete `._*` on the VM. |
| A VM lease claimed by one local folder refuses a copy run from another. | "claimed by repo ..." errors. | Run the copy from the claiming folder, or reclaim on purpose. |
| A sync tool copies files but never deletes a file that moved. | Phantom failures: duplicate routes, typecheck errors in files that no longer exist. | Delete the old path and build caches (for example `.next/`) on the VM after a rename. |
| A stale CLI login wins over valid default credentials. | "credentials are no longer valid" while the cloud SDK works. | Run the CLI with a throwaway config folder so it falls back to the default credentials. |
| An agent's patch fails to apply because the VM folder held an older copy of an output file. | "No such file" on apply; the work exists only in the patch. | Read the result from the patch itself; clean output folders before each run. |
| The remote start command keeps the SSH channel open. | `start` hangs until the job ends. | Point the remote shell's own descriptors at `/dev/null` before it starts the runner. |
| A check that cannot fail. | A green test that never saw the defect. | Break the guard once and watch the test fail before you trust it. |
| `pkill node` or any kill by name. | The agent kills its own runtime, or another agent's. | Kill by PID file only. |

## Limits

- The agent works from committed state. Push work in progress before the
  handoff, or it is invisible on the VM.
- A runner cannot detect that its VM is about to be reaped. Lifetime is your
  job, before the start.
- Merges done under a written waiver are still merges. The brief must say which
  ones, and the agent must record the waiver on each one.

## Related

- [agents-on-boxes](../agents-on-boxes/SKILL.md) runs short parallel jobs on
  Boxes. This skill is for one long job that must outlive the laptop session.
- [crabbox-worktree](../crabbox-worktree/SKILL.md) keeps a VM in sync with a
  worktree for builds.
