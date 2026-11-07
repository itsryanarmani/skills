---
name: personal-credentials
description: The personal credential fleet — four Claude Pro/Max subscriptions on one macOS machine, their config dirs and shell launchers, the private-repo-4944 personal profile that auto-routes them, CodexBar's token store, the ~/.secrets vault layout (OAuth pairs + merged password exports for agents), Instinct vault seeding via browser-personal, and the claude-subs-resync command that repairs drift when private-repo-4944 reports "no healthy subscription account". Load when asked to switch between Claude personal accounts, when cswap/private-repo-4944 auto-pick fails with 403 or "no healthy", when adding a new Claude subscription, when T3 Code provider instances need diagnosing, or when seeding credentials into an agent-facing vault.
---

# Personal Credentials Fleet

One machine, five Claude identities: a work config (`~/.claude`, metered API
key) and four personal Pro/Max subscriptions (`~/.claude-personal{,-1,-2,-3}`).
This skill maps where each credential lives, which consumers read it, and how
to repair drift — all without re-login as long as the keychain session is alive.

**Privacy rule for this skill:** the repo copy names account IDs and file
paths only. Email↔account bindings and all secrets live in the private files
below — never copy them into this repo or public PRs.

## The account map

| Account ID | Config dir | Notes |
|---|---|---|
| `work` | `~/.claude` | Metered API key (`ANTHROPIC_API_KEY`), not a subscription |
| `personal` | `~/.claude-personal` | Pro/Max sub 1 — auto-picker's primary (first configured) |
| `personal-1` | `~/.claude-personal-1` | sub 2 — inference-only token, see caveat below |
| `personal-2` | `~/.claude-personal-2` | sub 3 |
| `personal-3` | `~/.claude-personal-3` | sub 4 |

The email↔account binding is private; it lives in
`~/.config/claude-subs/accounts.json` (consumed by `claude-subs-resync`) and in
the login records inside each config dir.

## Two token classes — the distinction that breaks people

- **Setup-token** (`sk-ant-oat03-…`, `scope: user:inference`): can run
  inference but **cannot** query `api.anthropic.com/api/oauth/usage` — the
  probe gets HTTP 403, so any consumer that health-checks accounts marks the
  account dead. `personal-1` holds only this.
- **Fullscope OAuth session** (access + refresh + `expiresAt`, stored by
  Claude Code itself in the macOS Keychain under service
  `Claude Code-credentials-<sha256(absolute config-dir path)[:8]>`, blob field
  `claudeAiOauth`): inference **and** usage readable. `personal`, `personal-2`,
  `personal-3` have live ones.

On macOS the keychain is single-slot per config dir — `CLAUDE_CONFIG_DIR`
alone does NOT switch the billed account inside one terminal. Only
injecting the account's token (`CLAUDE_CODE_OAUTH_TOKEN`) or keychain session
does. All launchers below inject.

## Consumers

### Shell launchers (`~/.zshrc`)

- `claude-personal`, `claude-personal-1/-2/-3`, `claude-personal-as <id>` —
  named launch, each sets `CLAUDE_CONFIG_DIR` + `CLAUDE_CODE_OAUTH_TOKEN`.
- `cswap <id>` — alias for the same; bare `cswap` prints `claude-subs` status.
- `claude` → `claude-personal-auto` →
  `private-repo-4944 exec claude --account auto` on the personal profile; falls back
  to `private-repo-4944 pick-account anthropic` then `personal`.
- `claude-subs`, `claude-subs-pick`, `claude-subs-resync` — status, picker,
  drift repair (see below).

### T3 Code (`~/.t3/userdata/settings.json`)

`providerInstances` → each maps to a wrapper in `~/.local/bin/claude-t3-*`
that injects that account's token + config dir and **fails closed** if the
token is missing (never falls through to the wrong sub). Caveat: threads
started on the bare `claudeAgent` provider (no instance) land on the shared
keychain → one sub silently. The `claude_work` instance burns the work
metered API key — check the workdir before picking it.

### private-repo-4944 personal profile (`~/.private-repo-4944-personal`)

- `config.toml` → `[providers.anthropic] accounts = [{id, label}, …]`
- `secrets.json` → per-account OAuth blob at key
  `anthropic:<id>:oauth` → `{accessToken, refreshToken, expiresAt, scope,
  obtainedAt}`
- `state/usage.json` → per-account `{subscriptionStatus, lastFetchError,
  nextPollAt, utilization5h, utilization7d}`

**The failure mode:** if an account's `secrets.json` entry holds a setup-token,
the usage probe 403s → `lastFetchError: "http-403"` → `subscriptionStatus:
"unknown"` → `pick-account` denies every candidate → auto falls back to
`personal` forever. Worse, `nextPollAt` backoff blocks re-polling, so it
self-heals only after the backoff expires. Rank order is `[tierRank,
healthScore, familyMatchBoost, costScore]` — utilization only moves an account
through tiers (active → near-limit at the configured proactive threshold,
default 90%), so among healthy accounts the FIRST configured wins; auto does
not pick the least-used.

### CodexBar (`~/.codexbar/config.json`)

`providers[]` → find the one with `id == "claude"` (never index by position —
array order changes) → `tokenAccounts.accounts[]` →
`{label, accessToken, refreshToken, expiresAt}` per account. CodexBar keeps
its own token copies — it drifts from private-repo-4944 when either refreshes.

## The secrets vault (`~/Documents/Personal/.secrets`, all 0600)

| File | Contents |
|---|---|
| `claude-oauth.env` | `CLAUDE_OAUTH_<EMAIL>` access vars + `CLAUDE_OAUTH_REFRESH_<EMAIL>` + `CLAUDE_OAUTH_EXPIRES_<EMAIL>` companions per fullscope account |
| `passwords.csv` / `passwords-chrome.csv` | Raw Apple Passwords.app + Chrome exports (interchange format) |
| `passwords.json` | Merged canonical store, deduped on (host, username, password): `{title, url, host, username, password, otpauth?}` — otpauth TOTP seeds are what let an agent log into 2FA sites unattended |

Plus `~/.agents/.env.local` → `CLAUDE_CODE_OAUTH_TOKEN{,_2,_3,_4}` setup-tokens
(the launchers' injection source).

**Refresh tokens rotate on each use.** If Claude Code refreshes its keychain
pair, every downstream copy (private-repo-4944, CodexBar, `.secrets`) eventually
revokes. That drift is the recurring failure — see the repair below.

## Repair: `claude-subs-resync`

`~/.local/bin/claude-subs-resync` (source: `itsryanarmani/scripts` repo). Per
account in `~/.config/claude-subs/accounts.json`:

1. Reads the live Keychain session for the account's config dir.
2. Access token still fresh → copies the pair downstream as-is (no rotation,
   no rate-limit). Expired/near-expiry → refreshes against
   `platform.claude.com/v1/oauth/token` (public Claude Code client_id) and
   writes the new pair back into the keychain too, so Claude Code stays
   consistent.
3. Writes the pair to private-repo-4944 `secrets.json`, CodexBar `config.json`, and
   `.secrets/claude-oauth.env`.
4. Clears `nextPollAt`/`lastFetchError` in `usage.json` so the poller
   re-measures immediately.
5. Prints per-account 5h/7d utilization as proof. `--check` = read-only.

Run it when `private-repo-4944 pick-account anthropic` errors with
`no healthy subscription account remains`, when `claude-subs` shows
`subscriptionStatus: unknown`, or after any `claude` re-login (a login writes
a new keychain session; resync propagates it). If the keychain session itself
is dead (`--check` shows `no OAuth session`), the only fix is one interactive
login: `claude-personal-login <id>` → `/login` in that session. Everything
else repairs without a browser.

## Instinct vault (`app.instinct.com/vault`)

The agent-facing vault: Logins / Cards / Personal info / Agent items. Sign-in
is phone-number + SMS OTP — do it ONCE headed in the personal clone
(`browser-personal` opens it, port 9334, session `personal-real`); the session
persists in the clone.

Seeding entries: `instinct-vault-fill` (same scripts repo) drives the
Add-login dialog from a local `entries.json`. Two encoded traps:
a11y-ref clicks drop silently on this app (icon badges break textContent
equality — clicks go through DOM eval by aria-label), and the dialog's
textboxes render async (retry until they exist). Skips entries already in the
vault; never logs secrets.

**What goes in** (the assistant acts on these): airlines/hotels/loyalty,
utilities, telecom, shopping, streaming, event/reservation sites.
**What stays out:** money movement (bank/brokerage/crypto — agent error is
irreversible), employer credentials, identity anchors (primary email,
Google/Apple), infra (github/cloudflare/stripe admin), family members'
accounts, gov portals — unless explicitly asked. Also opt out of shared-data
training in Instinct settings before filling.

## Known limitations

- `personal-1` is inference-only (setup-token): `cswap personal-1` and T3's
  named instance work, but auto never picks it (unmeasurable → "unknown" →
  denied). Promoting it needs one `/login` inside `claude-personal-1`.
- The account map, secrets, and exports in this doc are real paths on this
  machine; everything in the repo copies is parameterized — do not inline
  them back into public source.
