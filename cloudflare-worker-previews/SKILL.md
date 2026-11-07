---
name: cloudflare-worker-previews
description: Configure Cloudflare Worker pull-request Previews with safe bindings, predictable URLs, live verification, cleanup, and authenticated test-user access.
---

# Cloudflare Worker Previews

Create one stable Preview per pull request. Name it from the PR-standard branch.
Verify the deployed URL before merge, then delete it when the PR closes.

Worker Previews are a private beta in Wrangler 4.127.1. Pin that exact version
in CI. Recheck the commands and beta limitations before changing the pin.

## Establish the contract

Inspect every Wrangler file and deployment workflow first. Record all variables,
secrets, bindings, Durable Objects, Containers, Workflows, services, queues,
routes, Cron Triggers, runtime settings, and Wrangler environments.

Use this Preview contract:

- Use the complete PR branch name as `--name`.
- Require the repository's PR-standard pattern before deployment.
- Keep the URL stable across commits to the same branch.
- Do not rename a branch while its Preview exists.
- Use `<branch>.preview.example.com` when the Worker has a custom domain.
- Use `<branch>.preview.staging.example.com` only when that hierarchy is intentional.
- Verify the live URL, including authentication, before merge.
- Upsert one marked PR comment with the URL and verification result.
- Delete the Preview when the PR closes.

For example, branch `or-111-fix-login` becomes
`or-111-fix-login.preview.example.com`.

If a branch must be renamed, delete the old Preview by its old branch name first.
Later pull-request events expose only the new name and cannot infer the orphan.

## Configure Preview settings

Production variables, secrets, bindings, and runtime settings do not enter a
Preview automatically. Add required non-secret settings under `previews`.
Provision Preview secrets separately.

Keep `assets`, `compatibility_date`, `compatibility_flags`, and `placement` at
the top level. Put Preview-specific observability, limits, logpush, definitions,
and tail consumers under `previews` when they differ.

Never bind a Preview to production data or credentials without explicit approval.
Use staging resources containing disposable or synthetic data.

```jsonc
{
  "vars": { "APP_ENV": "production" },
  "r2_buckets": [{ "binding": "UPLOADS", "bucket_name": "uploads-production" }],
  "previews": {
    "vars": { "APP_ENV": "preview" },
    "r2_buckets": [{ "binding": "UPLOADS", "bucket_name": "uploads-staging" }]
  }
}
```

Resource IDs and names still select real account resources. Two Previews using
one staging ID share its data. Create per-PR resources when destructive tests,
migrations, or parallel test isolation require them.

| Resource | Preview behavior |
|---|---|
| KV, D1, R2, Vectorize, Hyperdrive | Shared when IDs or names match |
| Analytics Engine, Pipelines, Secrets Store | Shared when targets match |
| Queue producers | Send to the named queue |
| Workflows | Share instances when the Workflow name matches |
| Static assets | Uploaded from the branch for each Preview |
| Same-Worker Durable Objects | Isolated namespace and storage per Preview |
| Same-Worker Containers | Isolated namespace and instances per Preview |

For a Workflow, use a distinct staging Workflow name when instance isolation
matters. Cloudflare does not create separate account resources for each Preview.

## Handle Durable Objects and Containers

Same-Worker Durable Objects isolate automatically when the binding omits
`script_name`. State persists across updates to one Preview. Preview deletion
deletes its Durable Object namespace.

Prefer `ctx.exports` for same-Worker calls. If code reads `env.COUNTER`, repeat
that binding under `previews.durable_objects.bindings`. Missing it can cause 1101.

A binding with `script_name` reaches that Worker's production Durable Object.
It never selects a matching Preview.

Declare container configuration under `previews.containers`. Also repeat its
Durable Object binding when code reads the container from `env`.

Container cleanup is incomplete. After deleting a Preview, list container apps.
Delete only apps matching `<worker>_<preview>_`; never match the Worker alone.

## Handle current gaps

- Service bindings reach the bound Worker's production deployment.
- Same-Worker calls should use `ctx.exports` where possible.
- Queue producers work, but Preview queue consumers do not.
- Cron Triggers invoke production, not Preview `scheduled()` handlers.
- Production routes and custom domains do not redirect traffic to a Preview.
- Use a test-only HTTP route for scheduled logic when appropriate.
- Use staging Workers for multi-Worker end-to-end tests.

Fail the rollout when these gaps would send tests into production.

## Configure names and custom domains

Pass the validated branch name explicitly:

```sh
npx --yes wrangler@4.127.1 preview --name "$BRANCH_NAME" --json
```

Do not replace the branch name with `pr-123`. The PR-standard name carries the
issue number and readable slug.

For a custom zone, reserve `preview.example.com` as the Preview base hostname.
Enable it for Preview traffic in the dashboard. Cloudflare creates wildcard DNS
and TLS for `*.preview.example.com`.

When Wrangler owns the custom-domain route, configure the setting there. A later
Wrangler deploy can overwrite a dashboard-only setting.

```jsonc
{
  "routes": [{
    "pattern": "preview.example.com",
    "custom_domain": true,
    "previews_enabled": true
  }]
}
```

That route also serves production traffic at `preview.example.com`. Preview
traffic uses `<branch>.preview.example.com`.

Issue the wildcard certificate before relying on the first PR. Certificate
issuance can lag behind Preview creation.

`<branch>.preview.staging.example.com` adds another hostname level. Confirm the
certificate covers it. Advanced Certificate Manager with Total TLS may be needed.

Keep `workers.dev` Preview URLs enabled as a diagnostic host when policy allows.
At least one host type must remain enabled.

## Configure credentials and test users

Create a narrow Cloudflare token with Workers Scripts Write and only the resource
permissions required by the Preview bindings. Keep it outside any job that can
execute pull-request code.

A same-repository pull request can add a workflow that names any repository or
organization secret available to that repository. A later trusted `workflow_run`
job does not remove that exposure. Do not store Preview credentials in the source
repository when autonomous branches can change workflows.

Use one of these credential boundaries:

- A branch-restricted GitHub environment, when the repository plan supports it.
- A trusted controller or broker outside the source repository.
- A local trusted controller using OS-protected credentials.

The source repository may store non-secret IDs as variables. It must hold no
Cloudflare mutation, Access, application, staging, or production credentials
when it lacks a branch-restricted environment.

See [cloudflare-agent-credentials](../cloudflare-agent-credentials/SKILL.md) when
the token does not exist. Verify the token before installing it.

Preview application secrets never inherit production values. Generate disposable,
per-PR values where possible. Scope each value to one Preview:

```sh
npx --yes wrangler@4.127.1 preview secret put SECRET_NAME --name "$BRANCH_NAME"
```

Do not put a reusable secret in Preview Base. Every deployed PR could read it.

Authenticated apps require a dedicated Preview test user. Prefer one generated
identity per PR in that PR's isolated data store. Otherwise, use a least-privilege
staging identity that is resettable and excluded from customer data.

Exercise the complete authenticated flow against the live URL. Include sign-in,
session persistence, and one permission-sensitive action. Test outer Cloudflare
Access separately from application authentication.

Maintain separate smoke users for production checks. Never point a Preview at
production authentication merely because the staging test user is missing.

## Block indexing and discovery

Treat every Preview as public internet traffic unless Cloudflare Access protects it.
Robots controls are not an authentication or authorization boundary.

Return `X-Robots-Tag: noindex, nofollow, noarchive, nosnippet, noimageindex,
noai, noimageai` on every Preview response. Render matching page metadata. Serve
this `robots.txt`:

```text
User-agent: *
Content-Signal: search=no, ai-input=no, ai-train=no
Disallow: /
```

Exclude Preview hosts from sitemaps, feeds, IndexNow, and canonical URL discovery.
Do not publish Preview URLs in `llms.txt`. The robots rule and Content Signals ask
compliant search and AI crawlers not to use the Preview. These controls are
voluntary. Keep Cloudflare Access enabled, and keep secrets and production data
isolated because crawlers and attackers can ignore them.

Verify the response header, page metadata, and `robots.txt` against the live URL.
Verify that `sitemap.xml`, feeds, `llms.txt`, and submission jobs omit Preview URLs.

## Automate and gate

Read [references/github-actions.md](references/github-actions.md) when adding the
GitHub Actions workflow. Adapt its install, build, health, and authenticated checks
to the repository.

The verification job must consume Wrangler's returned URL. It must not reconstruct
the URL and assume deployment succeeded.

Make the live verification job a required check where repository settings allow.
Otherwise, the designated merger must treat a red or missing check as blocking.

Add the live URL and verification result to the PR's `How I verified` section.
The sticky comment does not replace that proof.

Treat same-repository pull requests as untrusted too. They can change workflows,
helpers, dependencies, install scripts, and build configuration.

Never expose Cloudflare, Access, GitHub write, or reusable application credentials
to a job that executes PR-controlled content. Build without secrets. Deploy the
final bundle through trusted code that treats it only as data.

Forked pull requests must not receive secrets. Never use `pull_request_target` or
privileged `workflow_run` jobs to execute pull-request code.

### Skip when preview secrets are not configured

When the preview infrastructure is new (or the repo is a fork where secrets are
unavailable), gate the workflow so it stays green instead of failing:

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
```

Every downstream step is guarded with `if: steps.preview_gate.outputs.configured == 'true'`.
A `::notice` is used rather than `::warning` or `::error` so the job stays green.
Also guard against forks so the workflow never attempts to provision resources it
could not authenticate to. Replace `<your-org>` with the actual GitHub org:

```yaml
if: >-
  github.event.action != 'closed' &&
  github.event.pull_request.head.repo.full_name == github.repository &&
  github.repository_owner == '<your-org>'
```

See the `private-repo-4ed5` [`worker-preview.yml`](https://github.com/itsryanarmani/private-repo-4ed5/tree/main/.github/workflows/worker-preview.yml)
for a complete example that checks the three values at the top, then guards every
provision/deploy/verify/cleanup step with the same `configured` output.

## Delete the Preview

Delete by the same validated branch name when the PR closes:

```sh
npx --yes wrangler@4.127.1 preview delete \
  --name "$BRANCH_NAME" --skip-confirmation
```

Also delete any per-PR resources created outside the Preview system. Review exact
resource names before deletion.

A deleted custom Preview hostname can fall back to the base Worker and return 200.
Use the successful delete command as proof. Mark the PR comment as expired.

## Source of truth

These beta documents can change:

- [Get started](https://worker-previews-docs-2.preview.developers.cloudflare.com/workers/previews/get-started/)
- [Configuration](https://worker-previews-docs-2.preview.developers.cloudflare.com/workers/previews/configuration/)
- [Resources and isolation](https://worker-previews-docs-2.preview.developers.cloudflare.com/workers/previews/resources/)
- [Custom domains](https://worker-previews-docs-2.preview.developers.cloudflare.com/workers/previews/custom-domains/)
- [Limitations](https://worker-previews-docs-2.preview.developers.cloudflare.com/workers/previews/limitations/)
- [Automation examples](https://worker-previews-docs-2.preview.developers.cloudflare.com/workers/previews/automation-examples/)

## Related

- [pr-standards](../pr-standards/SKILL.md) defines the branch name and proof contract.
- [branch-deploy-convention](../branch-deploy-convention/SKILL.md) defines staging and production branches.
