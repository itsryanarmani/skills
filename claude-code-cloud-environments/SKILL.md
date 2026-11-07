---
name: claude-code-cloud-environments
description: "Create, verify, share and smoke-test claude.ai/code cloud environments (name, network level, environment variables, setup script) for a set of repositories, and repeat the same setup on another Claude account. These environments have no API or CLI, so the work drives the web dialog through agent-browser with the cc-cloud-env script. Covers picking the network level, which variables are safe to store, setup-script rules (it runs as root in the parent of the repo), the org-share trap, and a smoke test that proves the environment works. Use when someone asks to 'set up claude code cloud environments', 'create a cloud environment for my repo', 'make claude on the web run my project', 'copy my cloud environments to another account', or 'why does my cloud session have no node_modules'."
---

# claude-code-cloud-environments

A claude.ai/code cloud environment holds four settings: a name, a network
level, environment variables, and a setup script. A session that picks the
environment starts in a fresh container with those settings applied.

There is no API, CLI, or slash command that creates one. `/remote-env` only
selects a default. The `/v1/environments` API belongs to Managed Agents, a
different product. The only way in is the web dialog, so this skill drives that
dialog with `agent-browser` and the `cc-cloud-env` script.

## When not to use it

- The task is to run an agent on a VM you control. Use
  [cloud-agent-execution](../cloud-agent-execution/SKILL.md).
- You only need to change one value once. Edit it by hand in the dialog.

## Safety gates

- **Treat every variable as readable.** Anyone who can use the environment can
  read its variables and its setup script. Store public configuration and
  throwaway secrets only.
- **Share last.** Sharing with the organization is one way in the dialog. A
  shared environment becomes read-only there, and later edits need admin
  settings. Finish and test the configuration first.
- **Keep the spec outside every repo.** It names your repositories and holds
  secrets. A public repo must never contain it.

## Prerequisites

- `agent-browser` with a session connected to a Chrome that is logged in to the
  target claude.ai account. See [agent-browser-profiles](../agent-browser-profiles/SKILL.md).
  Use headed mode for the login, because a headless login strands you at a
  window that does not exist.
- The `cc-cloud-env` script from
  [itsryanarmani/scripts](https://github.com/itsryanarmani/scripts).
- The GitHub app is connected to the account, so the cloud session can clone
  your private repositories.

## Workflow

### 1. Write the spec

One directory per environment, kept outside any repo:

```text
<spec-root>/<env-name>/spec.json   {"network": "none|trusted|full|custom", "includeDefaults": true}
<spec-root>/<env-name>/env         KEY=value lines
<spec-root>/<env-name>/setup.sh    the setup script
<spec-root>/<env-name>/domains     one domain per line (custom network only)
```

Pick the network level with this table.

| Level | Choose it when |
|---|---|
| None | The task needs no outside access. Rare. |
| Trusted | Installs come only from common package registries. |
| Full | Setup downloads from many hosts, such as a language installer, a browser download, or a deploy API. Simplest, and fine for a repo you own. |
| Custom | You want a tight list. Keep `includeDefaults` on and add only the extra hosts. |

If you are unsure, choose Full for your own repositories. Choose Custom when
the repository is shared with people you do not control.

### 2. Choose the variables

Set these:

- Public configuration, such as a local URL or a feature flag.
- Test-mode keys from your own account.
- Freshly generated throwaway secrets. Never copy a real one.

Never set these:

- Live payment keys, cloud account tokens, registrar tokens, database tokens.
- Signing keystores, SMS or email provider keys.
- A remote-cache token for a shared build cache.
- A token that mirrors your own GitHub login.

### 3. Write the setup script

The script runs as root, in the parent of the repository, not inside it. Know
these rules before you write it.

1. **Find the repository first.** The working directory is the parent. The clone
   already exists at setup time, one level down. Search for it by lockfile:

   ```bash
   ROOT=""
   for d in /home/user/*/; do [ -f "${d}bun.lock" ] && ROOT="${d%/}" && break; done
   cd "$ROOT"
   ```

   A script that tests for the lockfile in the current directory skips the
   install without any error. This is the most common failure.
2. **Always exit 0, and log.** Send output to a file with
   `exec > /tmp/cc-setup.log 2>&1`, so a failed step is easy to read later.
3. **Stay under five minutes.** A long script slows every new session.
4. **Pin the toolchain only when the image differs.** The image already carries
   Node and a recent Bun. Install a pinned Bun only when the repository
   requires a different version.
5. **Install browsers with the project's own Playwright.**
   `bunx playwright install --with-deps chromium` fetches the version the
   project locks.

### 4. Apply and check

```bash
cc-cloud-env apply <spec-root>
cc-cloud-env check <spec-root>
```

`apply` creates each environment, or updates it when the name exists. `check`
reopens each one and compares network, variables, script, and (for Custom)
domains. Add a name to run a single environment. Add `--session <name>` to
use another browser session.

### 5. Smoke-test in a real session

`check` proves the dialog saved your values. It does not prove the environment
works. Start a real session in each environment with a read-only prompt:

> Read-only smoke test. Do not edit, commit or push. Report PASS or FAIL with
> one line of evidence each: the tail of `/tmp/cc-setup.log`; whether
> `node_modules` exists; the Playwright version and where the browsers are;
> the project's typecheck command; the Bun and Node versions.

Read the evidence, not the summary. Fix the script, apply, and run the smoke
test again until it passes.

### 6. Share with the organization

```bash
cc-cloud-env share <spec-root>
```

This clicks Share, ticks the acknowledgement, and confirms. Verify the result
in the organization's admin settings, under Cloud environments.

### 7. Repeat on another account

Log in to the other account in its own browser profile, connect a second
`agent-browser` session to it, and run the same commands with
`--session <name>`. Keep one spec root per account, because the variables
differ. A copy of an environment on a second account is a new environment.

## Known traps

| Symptom | Cause | Fix |
|---|---|---|
| Setup ran, but `node_modules` is missing | Lockfile test ran in the parent directory | Find the repo root, as in step 3 |
| `turbo: command not found` | Dependencies never installed | Same fix |
| Typecheck fails with `SELF_SIGNED_CERT_IN_CHAIN` | The session proxy signs TLS with its own CA. Turborepo strict mode drops `NODE_EXTRA_CA_CERTS` before it reaches the task | Add `NODE_EXTRA_CA_CERTS` to `globalPassThroughEnv` in `turbo.json`. Run with `--env-mode=loose` to confirm |
| `~/.cache/ms-playwright` is empty | Browsers live in `/opt/pw-browsers` here | Not a fault. Playwright finds them |
| `bun install` works, so is the proxy blocking installs? | No | Package installs work through the proxy |
| Edit dialog never opens, or shows "Cloud environment" | The environment is shared with the organization | Edit it in admin settings, or archive it and apply again |
| The Cloud submenu does not open | Hover is flaky | The script opens it with the keyboard. Do the same by hand: focus the item, press the right arrow |
| `fill` prints Done but the field is empty | The element reference is stale | Take a fresh snapshot before every action |

## Archive and clean up

There is no delete. `cc-cloud-env archive <name>` archives an environment. It
uses admin settings when the environment is shared.

## Verify the tooling itself

`cc-cloud-env-e2e` in the scripts repo runs the whole lifecycle on one
throwaway environment: create, check, update, a deliberate mismatch, share,
archive. It prints a PASS or FAIL line per step. Run it after any change to the
script or after the claude.ai dialog changes.
