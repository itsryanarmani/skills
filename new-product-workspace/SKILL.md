---
name: new-product-workspace
description: "Scaffold a brand-new product from zero: pick a name, confirm the .com is free, create the git repo, and lay out a local workspace that keeps brand assets, docs, and code side by side while the code stays a clean standalone repo. Use at the very start of a new product, before any building — it produces the empty container that ship-a-product then fills. Triggers: 'start a new product', 'set up a repo and local folder for X', 'new project workspace', 'scaffold a new product'."
---

# new-product-workspace

The first step of a new product: a name, a repo, and a place to keep everything.
This skill only creates the empty container. Hand off to `ship-a-product` for the
build → launch stages, and to `cloudflare-domain-launch` when it is time to
actually buy the domain and host a site.

## 1. Name it, and confirm the domain is free

Pick a short, brandable name. Confirm the `.com` (or `.ai`/`.app`) is actually
available and priced before committing — a name whose domain is taken is a name
you will regret.

- Registry truth for `.com`: Verisign RDAP. `404` = available, `200` = taken.
  `curl -s -o /dev/null -w "%{http_code}" https://rdap.verisign.com/com/v1/domain/<name>.com`
- Availability **and price** in one call: Cloudflare Registrar
  `POST /accounts/{account_id}/registrar/domain-check` with
  `{"domains": ["<name>.com", "<name>.ai", "<name>.app"]}`. Returns
  `registrable` plus `registration_cost` / `renewal_cost` per extension.

Popular mail/inbox/triage dictionary words are almost all squatted on `.com`.
Reach for a coinage or a compound early, and check a batch of 15–20 at once.

Do not register the domain here unless the user asks. Checking is free;
buying is a decision the user makes.

## 2. Create the repo

```bash
gh repo create <owner>/<name> --private --description "<one line>"
```

Private by default for an unlaunched product — flip to public later. Seed a
minimal `README.md` (name, one-paragraph pitch, `Status: 0→1.`) so the repo is
not empty.

## 3. The local workspace layout

One container folder per product. The code lives **inside** it as its own repo,
so the code stays clean while brand and research material sit alongside:

```
<product>/
├── branding/          logo, colors, type, brand guidelines
└── code/
    └── <repo>/         the git repo (this is the only tracked git repo)
```

Add these only when there is something to put in them (do not pre-create empty
scaffolding):

```
├── assets/            shared images, exports, media
├── content/           copy, posts, docs drafts
└── research/          prior art, notes, competitive scans
```

The container itself is **not** a git repo — only `code/<repo>/` is. This keeps
`git status` inside the code clean and lets brand/research files live next to
the code without ever being committed to it.

## 4. First commit when a pre-push guard blocks main

Some setups run a local pre-push hook that blocks any direct push to `main`.
For the very first commit to a fresh empty repo there is no PR to make, so seed
`main` on the remote through the API instead of pushing:

```bash
# from inside code/<repo>/
b64=$(base64 -i README.md)
gh api -X PUT repos/<owner>/<name>/contents/README.md \
  -f message="Initial commit: <name> README" \
  -f content="$b64"
git fetch origin main
git branch --set-upstream-to=origin/main main
```

After this, normal work goes through feature branches and PRs.

## 5. Repo conventions every new repo starts with

Set these before the first feature branch. Fixing them later means editing
workflows that have already run, or workflows that never ran at all.

**Branch model.** `main` is the default branch and deploys to the **staging**
environment. `release` is production. `staging` and `production` are environment
names and must never be used as branch names. Create `release` off `main` when
the product first needs a production deploy.

**A branch filter naming a branch you do not have never fires, and never
errors.** A workflow with `on: push: branches: [staging]` in a repo whose
branches are `main` and `release` simply never runs. There is no failure and no
run, so nothing reports it. Every time you add or copy a workflow, read its
`branches:` filter against the branches that actually exist (`git branch -r`).

**CI runners.** Private `itsryanarmani/*` repos use the warm Boat JIT pool.
Public repos use GitHub-hosted runners because fork PRs run untrusted code.
macOS and Windows jobs keep their GitHub-hosted images. The Dell fleet is
retired. JIT runners get only the labels passed; do not add `self-hosted`.
Declare `boat` and `boat-8` in `.github/actionlint.yaml`; see
[self-hosted-runner-fleet](../self-hosted-runner-fleet/SKILL.md).

| Job | `runs-on` |
| --- | --- |
| build, lint, typecheck, test, E2E, deploy | `boat` |
| heavy Next.js production build | `boat-8` |
| waits on an external API (LLM review, notify, deploy trigger, secret scan) | `boat` |

**PR review.** Every repo gets `.github/workflows/vibecodereview.yml`, which
calls `itsryanarmani/vibecodereview@v1`. Copy the current canonical file instead of
retyping it:

```bash
mkdir -p .github/workflows
gh api repos/itsryanarmani/private-repo-f304/contents/.github/workflows/vibecodereview.yml \
  --jq .content | base64 -d > .github/workflows/vibecodereview.yml
```

Secrets it reads: `CLAUDE_CODE_OAUTH_TOKEN`, `CLAUDE_CODE_OAUTH_TOKEN_2`,
`OPENAI_API_KEY`, `GEMINI_API_KEY`, `MOONSHOT_API_KEY`, `OPENROUTER_API_KEY`.
Only `OPENROUTER_API_KEY` is strictly required. The action falls back to
OpenRouter for any council member whose native key is missing or rejected.

## 6. Hand off

The workspace is now ready. Next:

- Building the product → `ship-a-product` (it sequences build → open-source prep
  → site → launch).
- Buying the domain and hosting a site → `cloudflare-domain-launch`.
- Generating the brand system that fills `branding/` → `saas-brand-system`.

## Checklist

- [ ] Name chosen; `.com` (or alt TLD) confirmed available + priced.
- [ ] `gh repo create` done (private unless told otherwise).
- [ ] `README.md` seeded; `main` exists on the remote.
- [ ] Local `<product>/{branding/,code/<repo>/}` container created.
- [ ] `release` understood as the production branch; no branch named `staging`
      or `production`.
- [ ] `.github/workflows/vibecodereview.yml` copied from `private-repo-f304`;
      `OPENROUTER_API_KEY` set.
- [ ] Every `runs-on` matches repo visibility and OS; every `branches:` filter names a
      branch that exists.
- [ ] Domain **not** purchased unless the user asked.

## Adopt the fleet PR and issue standards

Do this before the first feature branch. A repo is non-conforming from the start if these are missing, and fixing them later means editing the same workflows a second time.

Add the repo and a 2 to 4 letter lowercase prefix to `itsryanarmani/scripts/repo-prefixes.json` before running the rollouts. The prefix lives in one place so the rollout does not derive it from the repo name. Deriving it twice is how two repos get the same prefix.

Run `pr-standards-rollout --repo <new> --apply` from a checkout of `itsryanarmani/scripts`. It writes its files from `pr-standards-templates/` in the same checkout. Naming the repo explicitly matters: run without `--repo`, and there is nothing to say this rollout means the repo you just created rather than any other repo eligible for it.

`issue-standards-rollout --repo <new> --apply` does less. It creates the labels and prints the plan for everything else, because forms, the `AGENTS.md` block and the stub are a code change and go through one issue and one pull request like any other. Copy them from `issue-standards-templates/` yourself and open that pull request.

Do not vendor either set of templates into this skill's own directory as a persistent second copy — that copy drifts, and the fleet has already paid for that drift three times. Copying the destination files themselves into the new repo, the way the adoption pull request above does, is the required delivery mechanism, not the drift this warns against.

Run `pr-standards-rollout --repo <new>` first. `issue-standards-rollout --repo <new>` reads the prefix from `.github/pr-standards.json` to name the adoption branch.

A conforming repo has all of these. The first rollout (`pr-standards-rollout`) writes item 1. `issue-standards-rollout --apply` creates item 4. Items 2, 3, and 5 arrive through the adoption pull request:

1. `.github/pr-standards.json` with the registered prefix. The same rollout also writes `.github/pull_request_template.md` and `.github/workflows/pr-standards.yml` and inserts the `<!-- pr-standards:start -->` block into `AGENTS.md`.

2. The `<!-- issue-standards:start -->` block in `AGENTS.md`.

3. The four issue forms in `.github/ISSUE_TEMPLATE/`: `bug.yml`, `feature.yml`, `chore.yml`, `epic.yml`; plus `config.yml`.

4. The 14 labels:

| Group | Labels |
|---|---|
| Kind | `bug` `feature` `chore` `epic` |
| Size | `mini` `standard` `deep` |
| Route | `route:mechanical` `route:scoped` `route:judgement` |
| State | `triage` `ready-for-agent` `needs-info` `blocked` |

5. The `.agents/issues.md` stub from `issue-standards-templates/issues.md.stub`. Leave the TODOs. The stub asks for the repo's analytics helper and high-stakes paths, and neither exists before the product has real code. A guessed answer is worse than an empty one because the next agent will search for it and conclude the code is broken.

