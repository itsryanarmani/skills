---
name: agent-pr-standards
description: "Use when setting up or tightening pull-request rules on a repo where agents open most of the PRs, or when an agent is about to open one. Teaches the one-issue one-PR one-concern under-500-lines standard, why 500 is a design constraint that forces decomposition before the agent writes, why generated files are excluded from the count, the four layers (PreToolUse hook, pre-push hook, CI check, review-council scope lens), the GitHub Free gap that leaves red CI as a signal rather than a gate, and the fleet rollout that must itself obey the standard. Sibling to agent-lint-guardrails (code shape vs change shape). Triggers: 'PR is too big', 'unreviewable PR', 'one issue one PR', '500 line cap', 'agent opened a giant PR', 'PR standards', 'drive-by AI PR', 'Assisted-by trailer', 'roll out PR standards', 'cap agent PRs'."
---

# agent-pr-standards

Generation cost collapsed to near zero in 2026. Review cost did not move. That
asymmetry is the whole reason this standard exists. An agent will open a 20,000-line
PR against no agreed scope in minutes. The only thing standing between that PR and
`main` is your attention, and attention does not scale with the fleet.

## The field already voted

Public projects hit the same wall and wrote the same shape of rule.

- Ghostty, January 2026: zero-tolerance for drive-by AI PRs not tied to an
  accepted issue. No issue, no work. That is why the issue number is the join key.
- llama.cpp tightened its policy six times in four months and limited new
  contributors to one open PR at a time. Review queue is the scarce resource.
- curl shut down its HackerOne bounty in January 2026 after the valid-report rate
  fell below 5%. Unreviewable PRs are the same failure mode: noise drowning signal.
- The Linux kernel requires an `Assisted-by: AGENT:MODEL` trailer and reserves
  `Signed-off-by:` for humans, so later you can tell which agent produced which
  class of defect.

## The rule

One issue. One PR. One concern. Under 500 lines.

The issue number ties the branch, the title, the body, and the merged commit to
one agreed piece of work.

### Branch

```
<prefix>-<issue>-<slug>
cr-142-fix-onboarding-drop-off
```

| Part | Rule |
|---|---|
| `prefix` | 2-4 lowercase letters, one per repo, from `.github/pr-standards.json` |
| `issue` | a GitHub issue that exists and is open. No issue, no branch. |
| `slug` | `[a-z0-9]+(-[a-z0-9]+)*`, 3-48 characters. Names the change, not the file. |

Full pattern: `^[a-z]{2,4}-[0-9]+-[a-z0-9]+(-[a-z0-9]+)*$`

Never checked: `main`, `release`, `refactor`, `release/*`, `gh-pages`,
`dependabot/*`, `renovate/*`.

### Title

```
[CR-142] Fix onboarding drop-off on step three
```

The tag is the uppercase prefix and the same issue number as the branch. The
subject after the tag is imperative, 10-50 characters, no trailing period, starts
with a capital letter. Rejected openers, because they are not imperative: `Added`,
`Fixed`, `Updated`, `Removed`, `Changed`, `Refactored`, `Implemented`, and any
`-ing` first word. No emoji. No conventional-commit prefix. The tag already
carries the scope.

### Body

Four things, all required:

```
Closes #142

## What
One to three sentences. What changed, in plain words.

## Why
The problem from issue #142, and why this is the fix.

## How I verified
bun test        -> 214 passed
bun run build   -> clean

Assisted-by: claude-personal:claude-opus-5
```

Exactly one `Closes #N` / `Fixes #N`, matching the branch issue. Two closing
references means two concerns, which means two PRs. `## How I verified` must name
a command and its result. `N/A`, `TODO`, `tested locally`, and an unedited
template comment all fail. A body under 120 characters fails. A description that
only restates the diff is not a description.

## Why 500, not 1000

500 is roughly one reviewable sitting. It is a design constraint that forces
decomposition before the agent writes, not a nuisance after. A 1000-line cap
still looks like a cap, and an agent will fill it. The number is small enough
that the split happens at planning time, when it is cheap, instead of at review
time, when it is you.

If a change genuinely cannot be split, say so out loud. The only way past the
cap is the `oversized-approved` label, applied by the repo owner. An agent cannot
clear its own PR. Hard caps next to it: more than 40 counted files fails, more than 500 counted
lines fails, exactly one closing issue reference, and a warning at 3 top-level
directories. Say whether the boundary is inclusive; "under 500" and a table
saying `500` are not the same rule.

Count every closing keyword, not only the one you documented. GitHub closes an
issue on `close`, `closes`, `closed`, `fix`, `fixes`, `fixed`, `resolve`,
`resolves` and `resolved`. A check that counts only `Closes` waves through
`Closes #1` plus `Fixes #2`, which is two concerns wearing one coat.

Every cap above is a mechanical proxy. Whether a PR really does one thing is a
judgement for the review-council scope lens, and no regex can make it.

## Why generated files do not count

A cap that punishes an agent for a lockfile it did not write teaches the agent
to distrust the cap. Once it distrusts the cap, it looks for escapes instead of
splitting the work. Lockfiles, build output, snapshots, generated sources,
minified assets, sourcemaps, migrations, and binary media are excluded. The 500
is for the lines a reviewer has to read.

Keep the list per repo, because what counts as generated differs by stack and
some entries are judgement rather than fact. A hand-written migration is real
code that deserves review; most migrations are scaffolded and are not. Default
to excluding the category, let a repo narrow it, and report both totals so the
exclusion stays visible rather than becoming a place to hide.

## Four layers, two jobs

Local layers exist for speed. CI is the authority. Neither replaces the other.

| Layer | Runs | What it actually buys | Bypass |
|---|---|---|---|
| Agent `PreToolUse` hook | at the tool call | a bad branch, before the branch exists | another agent |
| `pre-push` git hook | before the push | a bad branch, before GitHub sees it | `--no-verify` |
| `pr-standards.yml` in CI | on every PR | size, body, issue, title. The record. | ignoring red |
| Review-council scope lens | on every PR | the "is this atomic" call no regex can make | ignoring the review |

## The honest gap, and it is narrower than "pay GitHub"

Whether any check can be made mandatory depends on plan AND visibility:

| Repo | Rulesets and required checks on GitHub Free |
|---|---|
| Public | Available. Turn them on today, at no cost. |
| Private, personal account | Needs GitHub Pro |
| Private, organization | Needs GitHub Team or Enterprise |

So a mixed fleet gets a mixed answer, and "we are on Free, so we cannot gate
anything" is the wrong conclusion. Gate every public repo now. Measure rather
than assume: `gh api repos/OWNER/NAME/rulesets` returns `[]` where rulesets are
available and `403 Upgrade to GitHub Pro` where they are not.

Where nothing can be required, red CI is a signal and not a gate. A human can
merge a red PR, and an agent that watches merge history will copy that. The two
local layers then carry the weight, but be precise about what they buy: they are
the fastest feedback and they stop the bad state before it reaches the server,
yet `git push --no-verify` skips the git hook and another agent's harness never
loaded the PreToolUse hook at all. They are early feedback, not a boundary. The
only real boundary is a required check on the remote. Treat `--no-verify` as a
review event, not a convenience flag.

## Rollout

Borrow the pattern that already worked in
[agent-lint-guardrails](../agent-lint-guardrails/SKILL.md). Fan out four
self-contained artifacts: `.github/pr-standards.json`, a pull request template,
a standalone `pr-standards.yml` workflow, and a marked block in `AGENTS.md`.
Keep the workflow independent of each repo's existing pipeline. The `AGENTS.md`
block is how the non-Claude fleet members learn the rule, and it belongs between
markers so a re-run updates it instead of appending a second copy.

If the workflow fetches the checker from one central repo rather than vendoring
it, be clear about the trade. One copy means one place to fix a rule. It also
means a mutable branch runs in every repo at once, with a token, which is a real
supply-chain surface even when you own the repo. Track the branch while the
rules are still moving; pin a full 40-character commit SHA once they settle. Skip forks (`isFork==true` means
never install this on someone else's process). Skip empty scaffolds. A 3-4 KB
repo has no PRs to shape.

The `workflow` token scope gotcha still applies. A git push of a workflow file
works. A contents-API edit of a workflow is classifier-gated, so patch workflows
via clone and push.

The rollout itself must obey the standard it installs. That means an issue per
repo before the PR that adds the check. A fleet-wide "add PR standards" PR
against no issue is the first violation, and agents copy what they see.

## The one knob, and how it goes wrong

`allowChoreEscape` lets a `chore/<slug>` branch skip the issue requirement, for
dependency bumps and CI fixes where the issue costs more than it saves. Start
with it off so the decision stays visible.

It must skip the issue requirement and NOTHING else. A chore branch still has to
satisfy every title and body rule. This is easy to get wrong: implement the
escape as "there is no issue number, so skip the checks that need one" and it
silently disables the title and body rules too, turning the knob into a way to
opt out of the whole standard. Ask any implementation to prove otherwise with a
test.

## Review and merge traps in a fleet

These came from one day of agent-written CI changes. Every pull request got a fresh-context
review. Each row is a defect that happened.

| Trap | Rule |
| --- | --- |
| A reviewer starts a background job and ends its turn | Run commands in the foreground. Write the verdict in the same turn. A review that waits on a background job ends with no verdict |
| A reviewer reads the diff and approves | Make the reviewer mutation-test any check the PR adds. Break each rule in a scratch copy and require red |
| A projected saving goes into the PR body | Quote measured results only. One projection read 11.9 minutes, then 3 to 4, then a net loss |
| An automation labels its own PR and merges a newer head than the one it approved | Read the head SHA right before the merge. Pass `--match-head-commit`. Never let an agent apply the gate label |
| A test writes a placeholder git identity into the shared repo config | Worktrees share that config, so every worker's commits carried it. Pass identity per command, use a temp repo, never run `git config` |
| A squash merge adds a `Co-authored-by` trailer for each other commit author | Pass an explicit merge message |
| A presence-claim hook sees a different identity than the worker's shell | Claim under the identity the hook computes |
| A usage limit kills a worker mid-task | Keep every task resumable: an issue, a branch and a claim. Re-route the task to another worker |
| A lock is held by a dead process | Release it with the tool's own release command. Never edit the lock file |

## Sibling layers

Lint budgets cap the shape of the code. This skill caps the shape of the change.
Run both. See [agent-lint-guardrails](../agent-lint-guardrails/SKILL.md).

Once PRs are small and frequent, silent CI (a cache that reports green and does
nothing) becomes the next tax. Start at
[ci-speed-diagnosis](../ci-speed-diagnosis/SKILL.md) before adding more pipeline.
