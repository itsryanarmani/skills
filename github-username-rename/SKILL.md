---
name: github-username-rename
description: "Use when a GitHub login changes and every repo, workflow, script and doc that names the old owner must be updated, in bulk, with agents. Covers what the rename breaks and when, how to survey every repo (code search lags, so shallow-clone and grep), the list of strings to change and the longer list that must not change (domains, npm scopes, App slugs, cloud resource names, local paths, registry namespaces), a shared brief for parallel workers, one PR per repo under the size cap, review, merge order, and the checks that prove nothing is left. Triggers: 'I changed my GitHub username', 'rename GitHub org references', 'update all repos to the new owner', 'old username still in workflows', 'fleet rename PRs'."
---

# github-username-rename

A GitHub login change breaks some things at once and others later.

- GitHub does not redirect `uses:` references to actions and reusable workflows.
  They can fail as soon as the rename lands. Fix them first.
- Profile links return 404 at once.
- GitHub redirects repository pages, `git` remotes and the API from the old login.
  That redirect ends if someone registers the old login and creates a repo with
  the same name. After that, a reference that still names the old login points at
  their code. A workflow `uses:` line is the worst case, because it runs that code.

So the job has a deadline you cannot see. Do it soon, and do it in bulk.

## What the rename touches

| Place | Behaviour after the rename |
| --- | --- |
| `git` remotes, clone URLs | Redirect while the old login stays free. Fix them anyway, with `git remote set-url`. |
| `gh` login and token | The token keeps working. `gh api user` shows the new login. The keyring label may keep the old name. |
| `uses: owner/repo@ref` | Not redirected. Can fail now. Runs foreign code if the old login is claimed. Fix first. |
| GitHub Pages | The old `owner.github.io` URL stops. Update it. |
| Packages on `ghcr.io/<owner>` | The old path is not redirected. Check each image. |
| GitHub Apps and installations | They follow the account. The App slug does not change. |
| Self-hosted runners and brokers | Registered to `owner/repo`. Check the registration and any owner constant in the broker. |
| MCP registry names `io.github.<owner>/*` | Tied to the login. They need a re-publish. Do not edit them in a rename PR. |
| Marketplaces, `npx skills add owner/repo`, docs | Update the text. Repository redirects keep old text working for now. |

## Step 1: survey with a clone, not code search

Code search lags a rename. A search for the old name returned zero hits for a
fleet that had thousands. Do not trust it.

1. List the repos: `gh repo list <new-owner> --limit 300 --json name,isArchived,isFork`.
2. Shallow-clone each one: `gh repo clone <new-owner>/<repo> <dir> -- --depth 1`.
3. Count hits, without lockfiles: `git grep -I -c -i <old> -- . ':!*lock*'`.
4. Run clones in parallel (12 at a time works). Retry failures once; they are
   rate limits, not missing repos.

Write the counts to a file. You need it to split the work and to prove the end state.

## Step 2: sort the hits

Most hits are not GitHub references. Tally the shapes before you write a rule.
A rename across 140 repos found these classes:

**Change**
- `github.com/<old>`, `github.com:<old>`, `api.github.com/repos/<old>`,
  `raw.githubusercontent.com/<old>`, `<old>.github.io`
- `uses: <old>/<repo>@ref` (keep the ref)
- `owner/repo` slugs: `gh -R`, `--repo`, `--owner`, `repository:` fields
- package metadata URLs (`repository`, `homepage`, `bugs`)
- `ghcr.io/<old>` image paths, only after the image exists under the new owner and a
  pull works (see Step 6). Until then leave the reference and report it.
- GitHub user mentions and `CODEOWNERS` entries

**Leave**
- your own domain, and emails on it
- npm scopes and published package names
- GitHub App slugs and the folders that hold their keys
- cloud project IDs, Cloudflare, Stripe, Firebase and bucket names
- environment variable and secret names, bundle IDs
- local paths such as `~/Documents/<old>`
- social handles and bio text
- `io.github.<old>` registry names (re-publish separately)
- lockfiles, changelog history, snapshots and fixtures that quote old text

When a hit is unclear, leave it and list it with `file:line`. A skipped hit costs
one more PR. A wrong change can take a deploy down.

Never run `sed s/<old>/<new>/` over a repo. The domain and the App slug both
contain the old name.

## Step 3: brief the workers

Write one shared brief file. Each worker reads it and gets a list of repos.
The brief holds the change list, the leave list, the PR rules, and the report format.
Keep the brief in a file, not in each prompt, so the rules cannot drift.

Batch by size:

- Repos with a few hits each: 25 to 30 repos per worker.
- Medium repos: about 10 per worker.
- Each large repo: its own worker. Large repos need several PRs.

Use a mid-tier model for the edits. Use a different, stronger model for review.

## Step 4: one PR per repo

Each repo gets its own issue and PR. Follow the repo's PR standard: issue first,
branch `<prefix>-<issue>-rename-github-owner`, one concern, under 500 counted
lines. Read the prefix from the repo's config. Do not guess it.

Split a large repo by top-level directory. Each PR gets its own issue.

Put evidence under "How I verified": the count of GitHub-form hits before and
after, and the list of hits you left on purpose.

Workers open PRs. Workers do not merge.

## Step 5: review and merge

1. One reviewer reads each PR diff. A batch reviewer can cover many identical PRs.
   The reviewer checks that no "leave" class was changed.
2. Read the review and the CI result at the head commit.
3. Merge from your own session with the head SHA pinned:
   `gh pr merge <n> --squash --match-head-commit <sha>`. Merge one PR at a time per repo.
   Parallel merges into one repo fail with "Base branch was modified". Retry those one by one.
   A body edit re-runs the PR-standards check, so add the review section first and wait.
4. A repo that deploys on every push to `main` needs a green deploy check first.
5. Never edit a `release` branch in a rename PR. Promote main to release the
   normal way afterwards.

## Step 6: prove nothing is left

Re-run the survey on a fresh clone of each default branch. The only hits left
should be the "leave" class. Save the final list of skipped hits. Then handle the
parts that no PR can fix:

- re-publish MCP registry entries under the new login
- re-register runners and check broker owner constants
- move `ghcr.io` images first, check a pull, then change the references that use them
- update the `gh` keyring label and any saved config that names the old login
- keep the old login unclaimed, if GitHub allows it, until all of this is done

## Check the diff with a script, not only by eye

Workers report what they meant to do. Check what they did. For each PR, pair every removed
line with its added line. A pure rename means the added line equals the removed line with
only the owner changed. Flag every PR where it does not. Also flag any changed occurrence
that sits next to `.com`, `-name`, `_`, `@`, `io.github.` or a path. This found, in one run:
a registry name changed after the worker had reported it as skipped, formatter noise that a
pre-commit hook added to six PRs, and whole-file rewrites of historical records.

Then check every `<new-owner>/<repo>` string the PRs add: `gh api repos/<new-owner>/<repo>`.
A name that fails is one of three things. A placeholder or fixture (ignore it). A repo that
never existed (it was dead before the rename). Or an alias: the old name was a redirect to a
repo that was renamed earlier. For an alias, the simple substitution breaks the link. Use the
real repo name. Check the old form to tell the cases apart: `gh api repos/<old-owner>/<repo>`.

## Failure modes seen

- Code search returned zero hits while thousands existed. Clone and grep.
- A blind replace would have changed a domain, a cloud project ID and an App slug.
- A pre-push hook crashed under a newer Node than the repo uses. Report it; do not skip it silently.
- A repo's pre-commit formatter reformatted tables and quotes inside a rename PR. Fix such a PR
  by writing the exact file content through the contents API, which runs no hooks.
- A running service stored the old owner in state (a lease file, a saved repo name). The new
  owner check rejected it. For a live system, accept both owners for a fixed period and write the
  removal date next to the code. Check saved state before you merge a change to an owner constant.
- Two agents opened rename PRs for one repo in the same minute. List open PRs before you start,
  and close the duplicate.
- Some repos had no PR-standards file. Open a prefix-less PR on the default branch there.
  Do not invent a prefix.
- A repo with an invalid PR prefix cannot take a PR until its config is fixed. Fix that first, in its own PR.
- A repo whose `main` already fails lint shows a red check that the rename did not cause. Say so in the PR.
