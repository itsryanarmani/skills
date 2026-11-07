---
name: github-app-per-repo-fleet
description: >-
  Use when agents make high-volume GitHub API calls against one itsryanarmani private repository.
  Choose per-repo App tokens, personal gh access, or sec-fleet access.
  Check permissions, token scope, pushes, and merge gates without publishing the private registry.
---

# GitHub App per-repo fleet

Use one dedicated App for sustained GitHub API work on one private repository.
Install that App on the target repository only.
Each installation has its own primary API budget.
New tokens from the same installation share that budget.
Secondary rate limits still apply.

## Choose the credential

| Work | Credential |
| --- | --- |
| Many agents or repeated API calls against one private repository | Dedicated per-repo App installation token |
| Short manual tasks, user-only endpoints, or an authorized merge | Personal `gh` login |
| Shared fleet work across repositories under existing authority | Existing `sec-fleet` token |

Do not drain personal `gh` access with repeated fleet queries.
Do not use `sec-fleet` as the default for sustained work on one repository.
Keep merges on the personal account.
Do not let unattended agents hold merge credentials.

The private registry lives in your private operations repository only.
Read it to find the target repository and its `<short>` name.
Never publish that mapping or list other private repository names here.
Never copy private registry content into this public skill.

## Read the scripts guides

Read the [per-repo fleet guide](https://github.com/itsryanarmani/scripts/blob/main/github-app-per-repo-fleet.md).
That guide lands with the scripts fleet PR.
Until merge, follow [github-apps.md](https://github.com/itsryanarmani/scripts/blob/main/github-apps.md) plus `./gh-app`.

The same PR adds [gh-app-per-repo-rollout](https://github.com/itsryanarmani/scripts/blob/main/gh-app-per-repo-rollout).
Use its documented interface after merge.
Do not assume rollout options before reading its help and guide.

Run the following commands from a `itsryanarmani/scripts` checkout.
Use its [gh-app helper](https://github.com/itsryanarmani/scripts/blob/main/gh-app) for App creation, installation, and token minting.

## Create and install

Check the private registry before creating an App.
Reuse the target repository's existing App when its permissions fit.
GitHub limits an organization to 100 registered Apps.
Prefer one App per high-volume private repository within that limit.
Wave 1 is live for three repositories; wave 2 uses the private manifest TSV and
`batch-plan` / `batch-status` on `gh-app-per-repo-rollout` (see the scripts guide).
Do not create a new App for each agent or token renewal.

Replace `<short>` with the private registry value.
The App slug is `pooriaarab-<short>-fleet`.
The local credential directory is `pooriaarab-<short>-fleet-app`.

```sh
./gh-app create --name 'pooriaarab-<short>-fleet-app' \
  --perm contents=write \
  --perm pull_requests=write \
  --perm issues=write \
  --perm workflows=write \
  --perm actions=read \
  --perm checks=read \
  --perm statuses=read
./gh-app install 'pooriaarab-<short>-fleet' --owner itsryanarmani
```

Complete the creation form in the personal browser.
Confirm the returned `APP_SLUG` matches the registry before installation.
Choose only the target repository during installation.
These permissions match `sec-fleet`; repository access covers only the target.
Do not grant administration access or select all repositories.

Keep keys under `~/Documents/Personal/.secrets/`.
Use directory mode `0700` and file mode `0600`.
Never print, commit, attach, or copy keys into a worker checkout.
Keep App IDs and installation details in the private registry.

## Mint and verify

`gh-app token` writes a secret to stdout.
Capture it in `GH_TOKEN`; never run it alone.
Replace `REPO` with the target repository name.
Run this block in Bash or Zsh after replacing `<short>` and `REPO`.

```sh
(
  set -eu
  set +x
  GH_TOKEN="$(./gh-app token 'pooriaarab-<short>-fleet-app')"
  test -n "$GH_TOKEN"
  export GH_TOKEN
  gh api installation/repositories \
    --jq '{total_count, repositories: [.repositories[].full_name]}'
  gh api repos/itsryanarmani/REPO --jq '{full_name, private}'
  gh api rate_limit --jq '{core: .resources.core, graphql: .resources.graphql}'
  gh pr list --repo itsryanarmani/REPO --limit 10
)
```

Proceed only when the installation reports exactly one repository: the private target.
Check the target identity before any write.
Record budget, reset time, and expiry without recording the token.
Installation tokens expire after one hour.
Reuse one token until renewal is needed.
Stop repeated requests on rate-limit responses.
Respect `Retry-After` and the reported reset time.
Do not rotate credentials to bypass secondary limits.

For a single command, use this form:

```sh
GH_TOKEN="$(./gh-app token 'pooriaarab-<short>-fleet-app')" \
  gh pr list --repo itsryanarmani/REPO --limit 10
```

`GH_TOKEN` controls `gh`; it does not configure plain `git push`.
Use the approved Git credential helper from the fleet guide.
Never put a token in a remote URL or command argument.
Do not claim an App push succeeds until a real push confirms its identity and result.

## Check before agent pushes and before merge

Before each push:

- [ ] Read repository rules and claim the issue before creating its branch.
- [ ] Confirm the App slug, installation, sole target repository, and required permissions.
- [ ] Confirm Git uses the intended credential without printing it.
- [ ] Run the repository's local CI before every push.
- [ ] Inspect the diff for unrelated changes, secrets, and private registry content.
- [ ] Verify branch rules and the permitted push path.
- [ ] Push the branch and open or update one PR for one issue.

Before merge:

- [ ] Confirm required workflows run for the App's bot identity.
- [ ] Check owner-only workflow conditions and fork approval rules when checks do not start.
- [ ] Confirm all required checks pass on the current head.
- [ ] Obtain one LLM review marked `APPROVED`.
- [ ] Attach real verification evidence under `## How I verified`.
- [ ] Walk the Cloudflare Worker Preview for visible changes or third-party integration changes, when repository rules require it.
- [ ] Record the Preview URL and response status codes.
- [ ] Use the authorized personal account for merge.

Do not bypass a missing review, failed check, or branch rule by changing credentials.

See GitHub's [installation authentication](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/authenticating-as-a-github-app-installation)
and [rate limits](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api) for endpoint support and budget rules.
