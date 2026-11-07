# GitHub Actions trust boundary

Treat every pull request as untrusted. Same-repository branches can change
workflows, helpers, dependencies, install scripts, builds, and migrations.

## Hard guard

Never expose Cloudflare, Access, GitHub write, staging, production, or reusable
application credentials to a job that executes PR-controlled content.

A same-repository PR can add workflows that reference available secrets or use
the repository's default `GITHUB_TOKEN` permissions. Set that default read-only.
A later trusted deploy job does not remove either path.

Use a branch-restricted environment when the repository plan supports it.
Otherwise, keep all sensitive credentials outside the source repository. Use a
trusted broker or local controller.

## Build without secrets

Run installs, tests, generators, and builds in a secret-free `pull_request` job.
Grant read-only contents access. Disable persisted checkout credentials.

```yaml
name: Worker Preview Build
on:
  pull_request:
    types: [opened, synchronize, reopened]
permissions:
  contents: read
jobs:
  build:
    if: github.event.pull_request.head.repo.full_name == github.repository
    runs-on: ${{ github.event.repository.private && 'boat-8' || 'ubuntu-latest' }}
    steps:
      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262
        with:
          ref: ${{ github.event.pull_request.head.sha }}
          persist-credentials: false
      # Install, test, build, and write preview-artifact/record.json here.
      - uses: actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02
        with:
          name: worker-preview-bundle
          path: preview-artifact
          if-no-files-found: error
          retention-days: 2
          compression-level: 0
```

The record must contain the PR number and exact head SHA. Upload only deployable
Worker bytes, assets, allowlisted SQL, and that record. Do not upload source,
Wrangler configuration, package metadata, executable tools, or scripts.

## Deploy through trusted code

Bootstrap the deployer onto the default branch before enabling the build. Run it
from `workflow_run`, or let an external controller poll successful build runs.

The trusted deployer must:

1. Require one successful `pull_request` run with the exact workflow name.
2. Query GitHub for the repository, open PR, branch, and current head SHA.
3. Reject forks, stale runs, closed PRs, and invalid branch names.
4. Require one fixed-name, unexpired artifact from that run.
5. Download outside the trusted checkout and verify GitHub's SHA-256 digest.
6. Reject traversal, backslashes, duplicates, links, special files, and excess size.
7. Check out only trusted default-branch deployment code.
8. Never execute code or tools from the artifact or pull-request checkout.
9. Render Wrangler configuration from a trusted allowlisted template.
10. Derive Worker, resource, domain, and Preview names from trusted data.

Use `--ignore-base-config`. This prevents dashboard Preview Base settings from
adding unreviewed bindings or reusable secrets.

```sh
npx --yes wrangler@4.127.1 preview "$BUNDLE" \
  --config "$TRUSTED_CONFIG" --worker-name "$WORKER_NAME" \
  --name "$BRANCH_NAME" --ignore-base-config --json
```

Set `no_bundle: true` for a plain bundle. Set `find_additional_modules: false`
unless the artifact contract lists fixed modules. Never accept configuration,
bindings, routes, domains, IDs, commands, or environment names from the artifact.

Treat SQL as inert input. Send allowlisted files only to that PR's isolated D1
through fixed trusted commands. Never interpolate SQL into a shell program.

## Prevent stale deployment races

Serialize provision, deploy, verification, and cleanup under one PR-scoped lock.
Disable cancellation for this lifecycle lock.

Revalidate the open PR and exact head SHA immediately before each mutation.
Revalidate them again before publishing success. A late run must not recreate a
Preview after cleanup or publish a stale URL.

## Publish a real merge gate

`workflow_run` uses the default branch SHA. Its job result does not gate the PR
head automatically. The trusted reporter must publish a check or commit status
against the revalidated PR head SHA.

A PR-controlled workflow can reuse a check name. Require trusted provenance.
Prefer a dedicated controller GitHub App as the expected source. An organization
required workflow is another option. Without either, verify provenance manually.

## Limit credentials and deployed secrets

Separate mutation, Access validation, live verification, and PR reporting duties.
Give each process only its required credential.

Generate Better Auth keys, BYOK keys, and test passwords per PR. PR code can read
every secret bound to its Worker, so all Preview application secrets must be
disposable and narrow.

Prefer one exact-host Access application and service token per PR when the
controller manages Access. Keep its human policy until Worker deletion. Revoke
short-lived verification tokens after use, then recreate them for later commits.

Never send a production smoke identity to a Preview. Run production smoke checks
only after merge through a separate trusted workflow.

## Verify and clean up

The trusted smoke harness must verify the exact returned URL, anonymous Access
denial, Preview-only Access, health, application auth, isolated state, indexing
headers, `robots.txt`, canonicals, feeds, sitemaps, and `llms.txt`.

Delete the exact Worker Preview first. Then delete recorded Access and data
resources. Treat absent targets as success. Stop if a live identity differs from
the manifest.

Use deterministic PR names. Persist ownership after each mutation. Preserve the
last valid manifest until all owned resources are gone. Mark the URL expired only
after cleanup passes.

## Skip-when-secrets-not-configured gate

When a workflow depends on secrets that may not be set (new repo, fork, or
infrastructure still being wired), gate the job so CI stays green instead of
failing. Emit `configured=true|false` once; guard every downstream step with
the same `if`.

```yaml
- id: preview_gate
  name: Skip when preview secrets are not configured
  env:
    CLOUDFLARE_PREVIEW_API_TOKEN: ${{ secrets.CLOUDFLARE_PREVIEW_API_TOKEN }}
    CF_PREVIEW_HOST_SUFFIX: ${{ vars.CF_PREVIEW_HOST_SUFFIX }}
    PREVIEW_BYOK_ENCRYPTION_KEY: ${{ secrets.PREVIEW_BYOK_ENCRYPTION_KEY }}
  run: |
    if [[ -n "$CLOUDFLARE_PREVIEW_API_TOKEN" && -n "$CF_PREVIEW_HOST_SUFFIX" \
          && -n "$PREVIEW_BYOK_ENCRYPTION_KEY" ]]; then
      echo "configured=true" >> "$GITHUB_OUTPUT"
    else
      echo "configured=false" >> "$GITHUB_OUTPUT"
      echo "::notice title=Preview skipped::Worker Preview secrets are not configured yet. \
Set CLOUDFLARE_PREVIEW_API_TOKEN, CF_PREVIEW_HOST_SUFFIX, and \
PREVIEW_BYOK_ENCRYPTION_KEY, then re-run."
    fi

- name: Provision / deploy / verify
  if: steps.preview_gate.outputs.configured == 'true'
  run: ...
```

### Rules

1. **One gate at the top.** Check the union of every value the job needs in a
   single step — a missing host suffix is as broken as a missing token.
2. **Guard every downstream step** with `if: steps.<id>.outputs.configured == 'true'`.
3. **Use `::notice`**, not `::warning` or `::error`, so the job stays green and
   the skip is visible in the log without a yellow/red banner.
4. **Keep a fork/ownership guard** so the workflow never tries to provision when
   secrets are unavailable by design:
   `github.event.pull_request.head.repo.full_name == github.repository`.

Working example: private-repo-4ed5
[`worker-preview.yml`](https://github.com/itsryanarmani/private-repo-4ed5/tree/main/.github/workflows/worker-preview.yml).
