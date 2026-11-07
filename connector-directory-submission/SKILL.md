---
name: connector-directory-submission
description: "Use when an n8n node, Make app, Pipedream component, Zapier integration, Claude Code plugin or ChatGPT/Codex Apps-SDK app should be listed on its public directory or marketplace. MCP servers go to mcp-directory-submission."
---

# Connector directory submission

The product ships one isolated `integrations/<name>/` package per platform. Each targets a **different** kind of directory with a different gate. Unlike MCP directories (where local/stdio is fine almost everywhere), connector directories split hard on npm-index vs monorepo-PR vs paid/partner-reviewed vs hosted-endpoint. Know the bucket before you spend effort.

**The core asymmetry vs MCP**: npm auto-indexing gets you *installable* on n8n and *distributable* as a Claude plugin with zero human review — but the **verified badge / public directory listing** on n8n, Make, Zapier, and ChatGPT all require review, and two of them (Zapier, Make partner) gate on real usage or partner status you can't fake. Ship the installable version first; the badge is a slow second lap.

## When to use

- **Triggers:** 'submit my n8n node', 'get the connector verified', 'publish to the Make apps directory', 'PR our Pipedream components', 'list our Zapier app', 'distribute the Claude Code plugin', 'submit the ChatGPT app', 'connector directory submission'.
- Which destinations index a plain npm package (n8n), which are a PR into a vendor monorepo (Pipedream), which are a dev-portal review with a partner or active-user gate (Make, Zapier, ChatGPT), and which are a git repo users add (Claude Code plugins).
- Per platform: the field that gates discovery (n8n keyword and n8n object, Pipedream component key, plugin.json and marketplace.json), the real entry point (npm, developers.make.com, PipedreamHQ/pipedream PR, zapier.com/app/developer, /plugin marketplace add, platform.openai.com/plugins), auth quirks, review gates and silent rejections.
- What a hosted-endpoint requirement (a ChatGPT app needs a public /mcp URL) or a private repo blocks.

## Buckets — check this first

| Gate | Destinations | What "listed" means |
|---|---|---|
| **npm auto-index, no review** | n8n community node (unverified) | Installable via Settings → Community Nodes the moment it's on npm with the right keyword. Not in node search. |
| **Git repo users add, no central directory** | Claude Code plugin | Distributed by a marketplace repo (`/plugin marketplace add owner/repo`). No official central listing to submit to (yet). |
| **PR into a vendor monorepo** | Pipedream components | Merged PR to `PipedreamHQ/pipedream` → appears in the Pipedream app registry. Free, but human-reviewed. |
| **Dev-portal review, free badge** | n8n **verified** node, Make apps directory | Submit → vendor QA → badge + in-app search visibility. No paid tier, but real review + real requirements. |
| **Dev-portal review, usage/partner gate** | Zapier public app | Publish → 90-day Beta → auto-public only after **50 active users + 10 Zap templates** (waivable by embedding). |
| **Hosted MCP + OAuth 2.1 REQUIRED** | ChatGPT / Codex Apps-SDK app · Anthropic **Claude Connectors Directory** | Both need a public `/mcp` URL **and per-user OAuth** — a client-presented Bearer API key is *not* accepted. One OAuth build unblocks *both*. See §5 + §7. |
| **Namespace verify, no review** | Official **MCP Registry** (`registry.modelcontextprotocol.io`) | Publish `server.json` under a namespace you can prove (GitHub OIDC or DNS). Feeds Anthropic/Smithery/PulseMCP/Docker/GitHub. See §8. |
| **No directory exists** | opencode, openclaw, hermes, other agent CLIs | They consume MCP via config (URL or stdio) — nothing to submit to. Registry + npm + hosted URL covers them. See §9. |

Do the zero-review ones first (npm publish for n8n, push the Claude plugin marketplace repo, publish `server.json` to the MCP Registry). They cost nothing and are live immediately. Save the usage-gated, hosting-gated, and OAuth-gated ones for last.

**The OAuth asymmetry (read before ChatGPT or Claude Connectors):** a hosted MCP endpoint that authenticates with a raw `Authorization: Bearer <api-key>` works for Codex CLI, the SDK, and any config-driven client — but **ChatGPT and the Claude Connectors Directory cannot present a custom API key.** They speak OAuth 2.1 only (per-user login + consent). So the gate for those two is not "is there a hosted endpoint" but "does the endpoint support OAuth." Build OAuth **additively** (keep the API-key path) and one effort lists on both.

---

## 1. n8n community node — npm keyword now, verified badge later

Two laps: **(a) installable** the instant it's on npm (needs the `n8n-nodes-` name + the
`n8n-community-node-package` keyword + the `n8n` object with compiled `dist/` paths — miss
one and n8n ignores it), **(b) the verified badge** via a Creator Portal review (hard
cutoffs: npm provenance from 2026-05-01, zero runtime deps, the scanner, English-only).

**Full n8n build + publish + verify playbook** → invoke the **`n8n-integration`** skill
(the three package.json fields, the npm automation-token/2FA/`--ignore-scripts` gotchas,
the declarative credential `authenticate` auth, and every verified-badge requirement).

---

## 2. Make (Integromat) app — dev-portal build + QA review

Make apps aren't an npm package — the `app.json` is the *export* of an app that lives in
Make's builder; you push it component-by-component (SDK Apps API), then request a QA review.

**Full Make build + submit playbook** → invoke the **`make-integration`** skill: the
SDK-API push (`scripts/make/publish-app.py`), the component model + exact API facts
(versioned vs unversioned endpoints, typeIds, section PUTs), the **Cloudflare `1010`
User-Agent trap** (not a rate limit), the review prereqs (one Universal module, pagination,
typed dates, sanitized secrets), and the review gates (a scenario PER module, 512×512 logo,
the Tally follow-up form, permanent publish, novelty requirement).

---

## 3. Pipedream components — PR into PipedreamHQ/pipedream

The registry IS the monorepo — publishing = a merged PR to `PipedreamHQ/pipedream` under
`components/` (ES-modules only, globally-unique namespaced component keys, per-component
metadata + annotations, auth centralized in the app file's `_makeRequest`/`_headers()`).

**Full Pipedream build + PR playbook** → invoke the **`pipedream-integration`** skill (the
exact directory layout, the key convention, required metadata, the app-file auth pattern,
and the fork→branch→PR-to-master + CI-lint flow).

---

## 4. Claude Code plugin — a marketplace repo, no central directory

Honest framing: **there is no single official central directory to "submit" a Claude Code plugin to.** Distribution *is* a public git repo (a "marketplace") that users add by name. Anthropic runs an official curated marketplace (`anthropics/claude-plugins-official`) but you don't self-serve into it — you ship your own marketplace repo and share the add command.

### The two manifests

`.claude-plugin/plugin.json` in the plugin dir:

```json
{
  "name": "contentrabbit",
  "description": "Schedule and manage Content Rabbit posts from Claude Code",
  "version": "1.0.0",
  "author": { "name": "Pooria" }
}
```

`.claude-plugin/marketplace.json` at the repo root (the catalog):

```json
{
  "name": "contentrabbit",
  "owner": { "name": "Pooria" },
  "plugins": [
    { "name": "contentrabbit", "source": "./integrations/claude-plugin", "description": "…" }
  ]
}
```

`version` in plugin.json controls updates — bump it every release or users never pull changes. `source` can be a relative path (plugin lives in this repo) or a git ref.

### Distribute

Push the repo public. Users run:

```
/plugin marketplace add <owner>/<repo>
/plugin install contentrabbit@contentrabbit
```

Updates: you push; users run `/plugin marketplace update`. That's the whole distribution mechanism — the "listing" is the README + the add command.

### Where to actually get discovered

Since there's no official submission form, reach = community aggregators. These drift; verify each is live before spending time:
- Community plugin-hub sites and "awesome-claude-code" style lists (README PRs, same shape as awesome-mcp-servers).
- The docs (`code.claude.com/docs/en/plugin-marketplaces`, `.../discover-plugins`) describe creating/adding marketplaces; there is no self-serve path into the Anthropic-curated list documented — treat inclusion there as out of your control.

`server.json` in the plugin bundles an MCP server — if you also want *that* listed on MCP directories, that's the **mcp-directory-submission** skill, a separate effort.

---

## 5. ChatGPT / Codex app (Apps SDK) — HOSTED `/mcp` + OAuth 2.1 REQUIRED

**Read this first: the real gate is OAuth, not hosting.** The submission portal requires a **public production `/mcp` URL** the reviewer can reach *and* that URL must authenticate each end user via **OAuth 2.1** — ChatGPT cannot send a custom API key or a machine-to-machine token. So a Bearer-API-key-only MCP server is reachable but **still not listable**: a reviewer (and Scan Tools) can't connect an account to it.

To unblock, the MCP host needs, additively (keep the API-key path for Codex/CLI/SDK):
- `GET /.well-known/oauth-protected-resource` (RFC 9728) naming the auth server + scopes + resource.
- `GET /.well-known/oauth-authorization-server` (RFC 8414) with PKCE `S256` and client registration via CIMD (`client_id_metadata_document_supported`) or DCR (RFC 7591).
- Authorize + token endpoints with a consent flow that mints tokens the `/mcp` route accepts, token `aud` = the MCP resource URL.
- A `WWW-Authenticate` challenge on 401 + per-tool `securitySchemes`.

**Codex CLI is NOT blocked** — it sends the API key via `bearer_token_env_var`, and the stdio `.mcp.json` variant works in the ChatGPT desktop app through a local marketplace. Only the *hosted public listing* needs OAuth. Everything below applies once OAuth exists.

The Apps SDK is in **beta**. Submission portal: **`platform.openai.com/plugins`**.

Prerequisites:
- An org role with **"Apps Management"** (plugin-submission) write access.
- Completed **identity verification** (individual or business) in the OpenAI Platform for the publishing name.
- The MCP server on a **public, production** URL (not localhost, not a tunnel that dies).

Submission steps (type **"With MCP"**):
1. Provide the production `/mcp` URL (Universal type for most).
2. Portal **scans** your tools + metadata.
3. **Verify the domain** — host the challenge token at `/.well-known/openai-apps-challenge`.
4. Define exact **CSP domains** your UI fetches from.
5. Provide **reviewer demo credentials** if auth is required — no MFA/SMS/email-confirmation on that account.
6. Add **5 positive + 3 negative** test cases with expected behavior.
7. Release notes + policy attestations → **Submit for Review**. Review ≠ publish; you choose when to publish after approval.

Once published it appears in the **Plugins Directory shared by ChatGPT and Codex** — the same listing serves both, so Codex consumes it automatically; no separate Codex submission. Tool `annotations` (`readOnlyHint`/`destructiveHint`/`openWorldHint`) must match real behavior or review fails. Guidelines: `developers.openai.com/apps-sdk/app-submission-guidelines`; flow: `developers.openai.com/plugins/deploy/submission`.

---

## 6. Zapier — dev-portal review + a usage gate you can't fake

Build in the **Platform UI** (browser) or the **Zapier Platform CLI** (local, version-controlled) — same Developer Platform, the repo's `integrations/zapier/` is the CLI form.

Submit: log in to **`zapier.com/app/developer`** → pick the integration → Integration Home → **Publish** → fill the form → **Submit for Review**. A Zapier developer reaches out within ~1 week. The app then enters **Beta** and appears in the app directory (`zapier.com/apps`) with a beta tag.

The gate that matters:
- **Beta lasts 90 days, and public listing is auto-granted only after 50 active users + ≥10 published Zap templates.** "Active" = the user has your app in a turned-on Zap. A daily job checks and auto-launches when you qualify.
- **Waiver**: embed Zapier in-product behind login and Zapier waives the 50-user requirement — a single signup through an embedded tool exits Beta the next business day and unlocks Partner Program benefits. For a brand-new app with no user base, the embed route is the realistic path to public.

Note the harder floor than "~1 week": even the *initial* submit is blocked until **S001 — 3 distinct Zapier accounts each have a turned-on (live) Zap using the app** (plus a successful task per trigger/action/search). A cold, zero-Zap app **cannot be submitted at all** by one developer — this, not the questionnaire, is the wall. Docs: `docs.zapier.com/platform/publish/public-integration`.

**Full Zapier depth lives in its own skill** → invoke **`zapier-integration`** for: the imperative-auth `beforeRequest` bug that `validate` can't catch (connect passes, every real call 401s), the exact-core-version pin, dropdown-must-be-a-trigger (D005), search-needs-a-field (D009), the `register --url` / `CHANGELOG` / U001-ToS / metadata (M002/M003/M004) traps, the "editor-Test clears a task without publishing" trick, the 3-users-with-live-Zaps (S001) wall + how to clear it (invite-link 3 accounts, or the embed), and the 5-section review questionnaire (incl. the mandated `integration-testing@zapier.com` reviewer account). Command-level playbook: `itsryanarmani/scripts` `scripts/zapier/README.md`.

---

## 7. Anthropic Claude Connectors Directory — self-serve in claude.ai, OAuth-gated

**Distinct from §4.** §4 is the *Claude Code plugin* marketplace (a git repo users add). This is the **Connectors Directory** inside **claude.ai** — the curated list of remote MCP servers a Claude user adds with one click. It IS self-serve, and acceptance is itself the "verified" status.

Same OAuth 2.1 requirement as ChatGPT (§5) — build it once, submit to both. On top of OAuth:
- **Public privacy policy URL** — a missing/incomplete one is an *immediate* rejection. Non-negotiable.
- **Per-tool annotations** — every tool marked read-only vs destructive (`destructiveHint`); wrong write-annotations fail review.
- **Public docs URL** (one help page or post is enough) + **≥3 example prompts** exercising different tools.
- **Test account** with realistic sample data the reviewer logs into, **server logo + favicon**, and confirmation of **HTTPS + Origin-header validation**.
- You submit through the portal from a **Team or Enterprise** Claude org.

Submit inside claude.ai (Settings → the connectors/submission surface). Escalations: `mcp-review@anthropic.com`. Policy + FAQ: `support.anthropic.com` MCP directory articles; building/submission: `claude.com/docs/connectors/building/submission`.

---

## 8. Official MCP Registry — the vendor-neutral hub

`registry.modelcontextprotocol.io` is the open, neutral directory. Publishing here is the highest-leverage single step: its consumers include **Anthropic, Smithery, PulseMCP, Docker Hub, and GitHub**, so one publish fans out to many surfaces.

- Publish the same `server.json` the plugin bundles.
- **Namespace must be one you can prove** — either `io.github.<org>/<server>` (verified via GitHub OIDC, easiest) or reverse-DNS `com.<yourdomain>/<server>` (DNS TXT or HTTP challenge). **GOTCHA**: don't let the manifest's namespace drift from a domain you don't control — e.g. `ai.contentrabbit/...` fails if the live domain is `contentrabbitai.com`; use `io.github.<owner>/...` or `com.contentrabbitai/...` to match what you can actually verify.
- Registry also verifies **package ownership** (you control the referenced npm package) and restricts base URLs to trusted public registries.
- Publish via the registry CLI/API (namespace auth is the gate, not human review).

This is a **no-review, namespace-verify** step — do it early alongside the npm publish.

---

## 9. Other agent harnesses (opencode, openclaw, hermes, …) — no directory to submit to

These consume MCP servers via **config** (a local stdio command or a remote URL) — they have **no curated store or submission form**. Don't spend effort hunting for one. Coverage for the entire long tail = (a) the stdio npm package, (b) the hosted URL, and (c) being in the Official MCP Registry (§8), which many clients read from. Ship those three, then add a short `## Add to any MCP client` snippet (the URL + the `npx` stdio command) to the connector README — that snippet *is* the "submission" for every config-driven harness.

---

## Verify the connector actually works before you submit anything

A listing for a connector that errors on the first real call is worse than no listing. Each platform has a local test path — run it against the exact package/manifest you're about to submit:

- **n8n**: install the compiled package into a local n8n and run a real node + trigger. `npm install /path/to/n8n-nodes-contentrabbit` into `~/.n8n/custom` (or link it), restart n8n, drop the node into a workflow, execute against staging. Also run `npx @n8n/scan-community-package <pkg>` — it's the same scanner verification uses, so a local pass predicts the review.
- **Make**: import via the VS Code extension into a real Make environment, build a scenario using your modules, run it once. The review *requires* working example scenarios anyway, so this doubles as submission prep.
- **Pipedream**: run the component locally with the Pipedream CLI (`pd`) before the PR — deploy a source, trigger it, run an action. CI will lint, but lint doesn't prove the API call works.
- **Claude Code plugin**: `/plugin marketplace add ./integrations/claude-plugin` (local path) then `/plugin install …` and exercise the commands/skills before pushing public. Copied plugins can't reach files outside their own dir (`../shared`) — a local install catches that.
- **ChatGPT app**: hit your hosted `/mcp` with an MCP `initialize`→`tools/list` handshake (same check as the MCP skill) before pointing the portal at it. The portal's tool scan fails loudly if the endpoint is down or the tool schema is malformed.
- **Zapier**: `zapier test` / `zapier validate` in the CLI, and run the auth + a trigger + an action in the Platform UI's built-in tester against a staging account.

## Order of operations for a batch

Cheapest / no-review first, usage-gated and hosting-gated last:

1. **npm-publish the n8n node** with the keyword + `n8n` field. Installable immediately, zero review. (Do the provenance GitHub Action *now* if you'll ever want the badge — retrofitting a local publish means a version bump and re-publish.)
2. **Push the Claude Code plugin marketplace repo public.** Live the moment it's pushed; no submission. Share the `/plugin marketplace add` command.
3. **Publish `server.json` to the Official MCP Registry** (§8) under a verifiable namespace. No human review, fans out to Anthropic/Smithery/PulseMCP/Docker/GitHub.
4. **Open the Pipedream monorepo PR.** One PR, all components, correct `key`s, green CI. Then it waits on human review — start it early because merge latency is out of your hands.
5. **Import + request review on the Make app.** Needs working example scenarios built first; QA review follows.
6. **Submit the n8n verified badge** via the Creator Portal — only after the provenance-published package is on npm and the scanner passes.
7. **Publish the Zapier app** → Beta in ~1 week, but plan the embed/usage path for public.
8. **Build OAuth 2.1 on the MCP host — the shared unlock for ChatGPT (§5) + Claude Connectors (§7).** LAST and biggest: a real auth-server build, not a portal click. Once it ships + deploys, submit to both directories (mostly browser/portal steps + assets). Don't sequence 1–7 behind it.

Steps 1–3 are instant and parallel (no review). 4–8 each need a browser sign-in, a PR review, an example scenario, or the OAuth build — none batch-automate, so treat them as independent tracks.

## Blocked / private-repo cautions (mirror the MCP skill)

- **Private repos break the human-reviewed listings.** Pipedream is a *public* monorepo PR — the code goes public regardless. Make/Zapier/ChatGPT reviewers and the Claude marketplace all link to or fetch from your repo; a private repo means dead "view source" links and a Claude marketplace nobody can `add`. If you flip a connector repo public to list it, **audit history for secrets first** (API keys, `.env`, tokens across all branches — going public is irreversible and exposes full history), same as the MCP skill's going-public checklist.
- **ChatGPT + Claude Connectors are OAuth-gated** — see §5/§7. A hosted `/mcp` that only accepts a client-presented API key is reachable but not listable on either; the unlock is OAuth 2.1, and it's one build for both. Don't promise these two until the OAuth server ships.
- **Novelty walls**: Make refuses an app for a service it already integrates; n8n refuses a node that duplicates an existing one. Check the target directory for an existing Content Rabbit connector before building the submission.
- **Usage walls**: Zapier's public (non-Beta) listing needs 50 active users or an embed — a cold app never auto-goes-public on merit alone. Set expectations: "listed in Beta" ≠ "in the public directory."

## Auth quirks per portal

An agent can *start* these and open the URL, but a human completes any OAuth/identity step:
- **npm** (n8n): standard `npm login` / automation token. For the verified badge, the publish must run in **GitHub Actions with provenance** — so the token lives in repo secrets, not your laptop.
- **n8n Creator Portal**: separate sign-in from npm; the portal is the submission surface.
- **Make**: a **Make API key** (from your Make account) pasted into the VS Code extension, zone-specific API URL. Review is a form, no extra auth.
- **Pipedream**: GitHub PR — just your GitHub login. CLI needs `pd login` for local testing.
- **Claude Code plugin**: none — it's a public git repo.
- **ChatGPT**: OpenAI Platform login + **completed identity verification** + "Apps Management" role. The identity check is a real KYC step and the slow part. Plus the OAuth server (§5) must be live before the portal can connect.
- **Claude Connectors Directory**: a **Team/Enterprise** claude.ai org to submit; the connector's own **OAuth 2.1** for per-user auth; a public **privacy policy** (hard reject if absent) + reviewer test account.
- **MCP Registry**: namespace proof only — **GitHub OIDC** (`io.github.<org>/…`, automatic in an Actions publish) or a **DNS/HTTP challenge** on your domain (`com.<domain>/…`). No login-gated review.
- **Zapier**: `zapier.com/app/developer` login; CLI `zapier login`.

## Skip / dead

- **No central Claude Code plugin directory to submit to** — distribution is your marketplace repo; the Anthropic-curated list isn't self-serve. Don't hunt for a submission form.
- **Zapier "public directory" as a quick win** — it isn't; it's a 50-user/embed gate behind a 90-day Beta. List in Beta, but don't treat public as same-day.
- **ChatGPT / Claude Connectors on a Bearer-key-only MCP** — reachable but not listable; the gate is OAuth 2.1, not hosting. Skip both until the OAuth server ships (§5/§7).
- **Hunting for an opencode/openclaw/hermes "directory"** — none exists (§9). The MCP Registry + npm + hosted URL is the coverage; don't look for a per-harness form.
- **Make app for an already-integrated service** — refused as duplicate; don't build the submission.
