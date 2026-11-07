---
name: repo-standards
description: "Bring a repository up to the repo standard: the README's front door and spine, the files around it, the About panel, the social preview, real images, and translations. Covers the parts a checker cannot do -- deciding what image proves the thing works, capturing it, the browser-only social-preview upload, and fanning the work across a fleet. Also carries the branch-protection and public-history-rewrite mechanics, with the gotchas that each cost a round trip."
---

# repo-standards

The standard itself lives in
[`itsryanarmani/scripts/repo-standards.md`](https://github.com/itsryanarmani/scripts/blob/main/repo-standards.md).
Read it once. Do not restate it here and do not paraphrase it into a README.
This skill is the procedure for satisfying it, and the parts of the job no
program can finish.

Its rule, so you know what you are aiming at:

> One sentence. One command. One screen. Nothing in it that is not true.

## When to use this

- A repo is going public.
- A README is stale, thin, or was written by an agent in a hurry.
- You are rolling the standard across more than one repo.
- Someone asks why a repo has no license, no topics, or a grey link preview.

## One repo, in order

Do not reorder these. Steps 1 and 2 decide everything after them, and doing
them last means rewriting the rest.

### 1. Find out what the repo actually is

Read the code, not the old README. An agent that writes the pitch from the old
README launders whatever was wrong into the new one.

Then pick the kind: `cli`, `library`, `app`, `collection`, or `infrastructure`.
The kind decides the section deltas and the images, so getting it wrong wastes
the rest of the work.

### 2. Write the one sentence

Under 120 characters. What it does, and for whom. This sentence is the README's
pitch and the About panel's description, unchanged in both.

Write it before anything else. If you cannot write it, the repo does more than
one thing, and no README will hide that.

### 3. Check the current state

```bash
repo-standards readme .
```

Fix what it reports before you add anything new. Most repos fail on shape, not
on content, and shape is cheap.

### 4. Get the images

This is the step that gets skipped, and it is the one a reader notices. See
[Images](#images) below.

### 5. Write the README

Start from the matching template in
`itsryanarmani/scripts/repo-standards-templates/`. Fill every `__PLACEHOLDER__`.
Delete the instruction comment at the top first, so you cannot ship it.

### 6. Verify every command in it

Run them. All of them, in a clean directory, as a stranger would.

This is the rule the checker cannot enforce and the one that matters most. A
quick start that works only because your machine already has the service
running is the most common defect in this fleet's READMEs, and it is invisible
to everyone who could have caught it.

### 7. Set the About panel

```bash
gh repo edit itsryanarmani/<repo> \
  --description "<the same sentence>" \
  --homepage "https://<live url>" \
  --add-topic <topic> --add-topic <topic> --add-topic <topic> --add-topic <topic>
```

Four to twelve topics. On a repo with no stars, topics are the only discovery
surface GitHub gives you, and most public repos in this fleet had none.

Topic names on a private repo are public. Do not name an unshipped product.

### 8. The license

Every repo, public or private. GitHub cannot serve a default one, because a
license has to travel with the clone. Everything else in the community health
set comes from [`itsryanarmani/.github`](https://github.com/itsryanarmani/.github)
and must not be copied into the repo.

### 9. The social preview

See [The social preview](#the-social-preview). It ends in a browser. Leave it
last so it does not block the rest.

## Images

A generated banner is decoration. A screenshot of the product doing its job is
evidence. Spend the effort on the second one.

### An app

Capture the real interface with `agent-browser`. Run it headed when a login,
a passkey prompt, or a one-time code stands between you and the screen you
want. Headless strands you: the agent tells you to click something in a window
that was never drawn, and nothing errors.

Capture the state that proves the product works, not the empty state. An empty
dashboard is a screenshot of nothing.

Log into a seeded or demo account, not one holding real customer data. This
step runs after `pre-public-repo-audit` in the pipeline, so nothing it commits
gets swept by that skill's PII/secret sweeps. A screenshot of a real logged-in
account bakes emails, names, internal hostnames or keys into a committed,
public image before anyone scans for them. If the only account available holds
real data, redact the frame before committing, or run `pre-public-repo-audit`'s
PII sweep again over the new image.

### A CLI

Capture the real terminal, running the command people actually run, with its
real output. Not a mock, not a hand-written transcript. A recorded terminal
beats a still image, and both beat a logo.

The same PII/secret risk from the app section applies here: this step runs
after `pre-public-repo-audit`, so nothing sweeps a committed capture. A real
terminal's output can carry an absolute laptop path, an internal hostname, or
an env var the command echoed back. Redact the frame before committing, or run
`pre-public-repo-audit`'s PII sweep again over the new image.

### A library

No screenshots. The code example above the fold is the image.

### A banner, when you need one

`wavespeed run <model> --input prompt="..."` generates one. It is identity, not
proof, so keep it plain and do not let it make a claim the software does not
support. Never generate a picture of the product interface: an image model
garbles text and UI, and a fake screenshot of your own app is the one image
that destroys a reader's trust completely.

### Where they go

`assets/`, committed, linked relatively. Not a `github.com/user-attachments`
URL. Attachments serve anonymous readers today and are not a git object, so
nothing promises they still resolve next year. Attachments are for pull request
proof. The repo is for the README.

Under 500 KB each. Alt text on every one, describing the image rather than the
project.

Serve a hero image in both colour schemes or it vanishes for half the readers:

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.png"/>
  <img src="assets/hero-light.png" alt="Search results, ranked by score" width="900"/>
</picture>
```

## The social preview

The 1280x640 card GitHub serves when the URL is pasted into Slack, X, LinkedIn
or Discord. Without one, the preview is a grey card with an avatar on it.

Read the current state:

```bash
gh api graphql -f query='{repository(owner:"itsryanarmani",name:"skills"){
  openGraphImageUrl usesCustomOpenGraphImage }}'
```

**There is no API that sets it.** GraphQL exposes the field for reading only,
and there is no REST endpoint. The website upload paths that circulate in
scripts and Actions (`/upload/policies/repository-images`) are browser session
endpoints: a `gh` token sent to them comes back `logged_in=no` with a 404 or a
422. Anything that claims to automate this is driving a browser.

So:

1. Generate or export the image at 1280x640.
2. Commit it to `assets/og.png`. That copy is the source of truth and survives
   the next step being skipped.
3. Upload it in the browser, under Settings, Social preview.

Skip this entirely on private repos. GitHub does not serve a private repo's
card to the places a preview is read, so the upload cannot reach the audience
it exists for.

## Translations

Public repos only, into `docs/translations/<iso-639-1>.md`, produced by
`private-repo-0218` rather than by hand or a one-off script per repo.

Every translated file starts with the commit it was made from:

```
<!-- translated-from: 4d8c7a6 -->
```

Without that line nobody can tell a current translation from one describing a
version you deleted. A stale translation is worse than none, because the reader
cannot tell which they are holding.

## Many repos at once

One repo at a time is the wrong shape for a fleet. Batch it.

1. **Measure first.** `standards-coverage --missing readme` names the repos that
   need work. Do not start from a list you assembled by hand.
2. **Group by kind.** All the CLIs together, all the apps together. The judgement
   about what makes a good CLI README is the expensive part, and it transfers
   across a group. It does not transfer from a CLI to an app.
3. **One issue and one pull request per repo.** The size cap is per pull request
   and a README rewrite plus images is not small. A single pull request touching
   nine repos cannot be reviewed and cannot be reverted.
4. **Delegate the writing, keep the judgement.** A worker can fill a template,
   run the checker, and fix what it reports. Deciding whether the sentence is
   true, and whether the screenshot shows the product working, stays with you.
5. **Judge a delegated job on its diff, never on its exit code.** Workers in this
   roster have exited zero having written nothing.
6. **Do the browser steps in one pass at the end**, once every image is committed.
   Batching them is the difference between one browser session and thirty.

## Branch protection, when a repo goes public

On a solo repo, GitHub's default permissions already stop anyone else merging:
write access is required, and only the owner has it. Confirm what you actually
have before adding anything:

```bash
gh api repos/<owner>/<repo>/collaborators --jq '.[].login'
```

So protection is not preventing unauthorised merges. It is making the intent
explicit and future-proofing for a second collaborator.

**Create `.github/CODEOWNERS` before you rely on it.** Unlike CODE_OF_CONDUCT,
CONTRIBUTING and the other community health files, GitHub's org-wide `.github`
defaults do not cover CODEOWNERS — it has to live in the repo itself. Add
`* @<owner>` if the file is not already there.

**`CODEOWNERS` alone does not gate merges.** It requests a review. It only
becomes a gate once a protection rule adds "require review from code owners"
and restricts who can push. Say that in `CONTRIBUTING.md` rather than implying
the file is enough on its own.

**Set protection with a JSON body, not flags.** Nested objects and real booleans
do not survive `-f`, which sends `"true"` as a string and gets rejected:

```bash
gh api --method PUT repos/<owner>/<repo>/branches/main/protection \
  -H "Accept: application/vnd.github+json" --input protection.json
```

```json
{
  "required_status_checks": { "strict": true, "contexts": ["test"] },
  "enforce_admins": false,
  "required_pull_request_reviews": {
    "required_approving_review_count": 0,
    "require_code_owner_reviews": true
  },
  "restrictions": null,
  "required_linear_history": false,
  "allow_force_pushes": false,
  "allow_deletions": false
}
```

Set `required_approving_review_count: 0` on a solo repo. Requiring one approval
locks the owner out of merging their own work without a second account.

**`allow_force_pushes: false` blocks admins too.** `enforce_admins: false` lets
an admin bypass required reviews and status checks. It does not touch the
force-push restriction. The owner gets a real `GH006: Cannot force-push to this
branch` from GitHub. To rewrite history once, PUT the protection with
`allow_force_pushes: true`, push, then PUT it back. Do not leave it open.

Branch protection and rulesets are unavailable on private repos on GitHub Free.
The API returns 403. Public repos on the same account can be gated today.

## Scrubbing something from public history

When a commit message, a file, or a reference has to leave history that is
already pushed:

1. `git-filter-repo --force --message-callback '<python>' --blob-callback '<python>'`
   rewrites messages and content in one pass. It removes the `origin` remote as
   a safety measure. Re-add it afterwards.
2. Every downstream SHA changes, including on branches you did not touch. Any
   branch or pull request based on the old history shows as diverged. Expect to
   recreate them rather than fast-forward.
3. The force-push is where branch protection and local git safety hooks both
   gate. A git-safety hook may require a person to run the push, by design.
4. **A PR description is not in git history.** GitHub stores it separately, so
   rewriting commits does not touch it. Sweep the working tree, `git log --all
   --grep`, and every open, closed and merged pull request body. Edit one with:

   ```bash
   gh api --method PATCH repos/<owner>/<repo>/pulls/<n> -f body="..."
   ```

## The traps, each of which cost a round trip

- **A shields.io badge on a private repo renders `repo not found`.** It does not
  fail, it renders a grey badge that reads as a dead project. Shields will not
  accept a token, and a token in a badge URL is a leaked token. Private repos
  take static badges or none.
- **`community/profile` never reports a security policy.** There is no `security`
  key in its `files` object, inherited or local, while `/security/policy` serves
  the file correctly. Anything built on that endpoint reports the whole fleet as
  having no policy, forever.
- **The `.github` defaults repo must be public.** A private one inherits to
  nothing, silently.
- **A repo's own file beats the default, and for issue templates the override is
  total.** Any local `.github/ISSUE_TEMPLATE` content makes GitHub ignore the
  defaults rather than merge them.
- **Run the humanizer before you ship a README.** Bold inline-header bullets and
  em dashes doing a comma's job are what a technical reader notices first on a
  project's front door.
