# Auth Setup Runbook

Step-by-step auth for every organizer-suite CLI. Run each section in **your own terminal** (not inside Claude Code) so you can see browser prompts and keychain dialogs.

---

## Quick status check

```bash
# verify auth state of each CLI
gog auth doctor                    # gog
spogo auth status                  # spogo
xurl auth status                   # xurl
birdclaw auth status               # birdclaw
remindctl status                   # remindctl
imsg chats 2>&1 | head -3          # imsg (will succeed if FDA granted)
```

---

## 1. Apple Reminders — `remindctl` ✅

**Status:** typically auto-authorizes on first run via macOS prompt.

```bash
# Check
remindctl status
# → "Reminders access: Full access"

# If not authorized:
remindctl authorize
```

If access shows "Restricted" or "Denied":
- System Settings → Privacy & Security → Reminders → enable for your terminal app

---

## 2. iMessage — `imsg`

**Status:** needs **Full Disk Access** for the parent process (Claude.app, Terminal.app, iTerm, etc.).

### Steps

1. Open **System Settings → Privacy & Security → Full Disk Access**
   ```bash
   open "x-apple.systempreferences:com.apple.preference.security?Privacy_AllFiles"
   ```
2. Click **+** and add:
   - `/Applications/Claude.app` (the desktop wrapper)
   - `/Users/<you>/.local/bin/claude` (the CLI binary, optional but useful)
   - The terminal app you'll use for manual runs (e.g. `/System/Applications/Utilities/Terminal.app`, `/Applications/iTerm.app`, `/Applications/Warp.app`, `/Applications/Ghostty.app`)
3. **Quit Claude.app fully (⌘Q)** and reopen. macOS only honors new FDA grants for processes started *after* the grant.
4. Verify:
   ```bash
   imsg chats | head -3
   # Should list recent conversations, not "authorization denied"
   ```

### Recovery

If `imsg` still says "authorization denied" after granting + restarting:
- Check Activity Monitor — make sure the *new* Claude Code process is the one talking (not a stale child).
- Try running `imsg chats` from `Terminal.app` directly to isolate — if Terminal works but Claude Code doesn't, the issue is parent-process inheritance and you may need to add the lower-level `claude` CLI binary explicitly.

---

## 3. Spotify — `spogo`

**Status:** uses browser cookies via `sweetcookie`. Two paths.

### Path A — automatic cookie import (Chrome / Safari)

Requires Chrome's Safe Storage keychain access. Works in **regular Terminal.app** but blocked under Claude Code's process tree (the keychain prompt can't show).

1. Make sure you're logged into https://open.spotify.com in Chrome.
2. In **Terminal.app** (not Claude Code), run:
   ```bash
   spogo auth import --browser chrome
   ```
3. macOS will prompt for keychain access — click **Always Allow**.
4. Verify:
   ```bash
   spogo auth status
   # → "Cookies: 3 (file)" with sp_dc, sp_t, sp_key
   spogo library playlists list --plain | head
   # → Lists your playlists. If 429, wait 15 min (rate limit) and retry.
   ```

### Path B — manual paste (works anywhere)

If keychain is blocking automatic import:

1. Open https://open.spotify.com in Chrome (logged in).
2. Open DevTools (⌥⌘I) → **Application** tab → **Cookies → https://open.spotify.com**.
3. Copy these three cookie values:
   - `sp_dc` (the big one — required)
   - `sp_t` (the device cookie)
   - `sp_key` (optional but helpful)
4. Run:
   ```bash
   spogo auth paste
   # Paste each cookie value when prompted
   ```
5. Verify with `spogo library playlists list --plain | head`.

### Known issue: `library` endpoints return 429

If `search` works but `library` returns 429, the cookies are partially valid. Causes:
- Logged-out session in Chrome since cookies were copied → re-login + re-paste.
- Residual rate-limit from earlier failed attempts → wait ~15 min.
- Stale `sp_dc` cookie → log out + log back in to refresh, then re-paste.

---

## 4. X / Twitter — `xurl`

**Status:** needs an **X Developer app** registered to your account. The OAuth2 flow uses *your* personal app's `client_id`.

### One-time setup: register the app

1. Go to https://developer.x.com (or https://developer.twitter.com).
2. Sign up for the **Free tier** (limited but sufficient for personal bookmarks/likes/timeline reads). Approval is instant for most accounts.
3. Create a project + app. Note the **Client ID** and **Client Secret**.
4. In the app settings, configure:
   - **App permissions:** Read (Read+Write if you want to bookmark/unbookmark via xurl).
   - **Type of App:** Native App (uses PKCE, no secret needed at runtime).
   - **Callback URL:** `http://127.0.0.1:8080/callback` (xurl's default).
   - **Website URL:** anything (e.g. https://github.com/<you>).

### Configure xurl with the app

1. Register the app (NAME is positional; flags carry the credentials):
   ```bash
   xurl auth apps add <app-name> \
     --client-id <client_id> \
     --client-secret <client_secret> \
     --redirect-uri http://127.0.0.1:8080/callback
   # Example: xurl auth apps add <your-app-name> --client-id SXdx... --client-secret nfpp...
   ```
2. Set as default:
   ```bash
   xurl auth default <app-name>
   ```
3. (Optional) Set the bearer token for app-only reads:
   ```bash
   xurl auth app --bearer-token <bearer_token>
   ```
4. Run OAuth2 user flow (for user-context endpoints like bookmarks, likes, mentions):
   ```bash
   xurl auth oauth2 <your_x_handle>
   # Username is POSITIONAL — no -u flag. Browser opens, you authorize,
   # xurl captures the callback automatically.
   ```
5. Verify:
   ```bash
   xurl auth status
   xurl whoami
   # → should print your X profile JSON
   ```

### After xurl works, wire it to birdclaw

**Heads-up:** `birdclaw` ships with a pre-seeded "default account" pointing at `@steipete` (the maintainer). If you don't update it, every sync hits a hardcoded user ID that doesn't match your auth and fails with:

> `The id query parameter value [25401953] must be the same as the authenticating user [<yours>]`

Fix with one SQL command after running `birdclaw init`:

```bash
# Get your numeric X user ID from xurl
USER_ID=$(xurl whoami | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['id'])")
HANDLE="@your_x_handle"  # with the leading @

sqlite3 ~/.birdclaw/birdclaw.sqlite "UPDATE accounts SET name='<Your Name>', handle='${HANDLE}', external_user_id='${USER_ID}' WHERE id='acct_primary';"
```

Then sync:

```bash
birdclaw sync bookmarks --mode xurl --all --max-pages 100
birdclaw sync likes --mode xurl --limit 200
sqlite3 ~/.birdclaw/birdclaw.sqlite "SELECT kind, COUNT(*) FROM tweet_collections WHERE account_id='acct_primary' GROUP BY kind;"
# → bookmarks|<N>
#   likes|<M>
```

### Known errors

| Error | Cause | Fix |
|---|---|---|
| `client_id=&` in OAuth URL | Skipped `xurl auth apps add` | Re-run `xurl auth apps add NAME --client-id ...` |
| `Error: unknown shorthand flag: 'u'` on `xurl auth oauth2 -u <handle>` | `-u` is not a flag for this subcommand | Drop the `-u` — username is positional: `xurl auth oauth2 <handle>` |
| `spawn /Users/.../Projects/bird/bird ENOENT` from birdclaw | `--mode auto` tries the unreleased `bird` tool first | Use `--mode xurl` explicitly |
| `Error: Unknown account: <handle>` from birdclaw | The default account row still points at @steipete | See SQL fix above |
| `must be the same as the authenticating user` from birdclaw | Same as above — seed account mismatch | Same SQL fix |

---

## 5. Google Suite — `gog` (Gmail/Calendar/Drive/Contacts/Tasks/etc.)

**Status:** OAuth credentials are pre-loaded but no token yet. One-time auth flow per Google account.

### Prerequisites (one-time, per machine)

1. Switch to macOS keychain backend (more reliable than file keyring):
   ```bash
   echo '{"keyring_backend": "keychain"}' > ~/Library/Application\ Support/gogcli/config.json
   gog auth doctor
   # status should be "warn" (only warning: no tokens yet)
   ```

### Auth a Google account

Run **in Terminal.app**, not Claude Code (you need the browser to redirect back to a local port that this terminal session is listening on):

```bash
gog auth add your-email@gmail.com
# Browser opens. Sign in, click through consent screen. Wait for callback.
```

If the browser doesn't open automatically, copy the URL printed by the command and paste into Chrome.

### Verify

```bash
gog auth list
gog auth doctor
gog --account=your-email@gmail.com gmail labels list --plain | head
# → Should list Gmail labels for that account
```

### Multi-account

Repeat `gog auth add <email>` for each Google account (e.g. work + personal). Use `--account=<email>` on every subsequent call to pick which account.

---

## 6. X archive (alternative to live xurl) — `birdclaw`

**Status:** initialized at `~/.birdclaw/`. If `xurl` setup is too painful, you can import an archive.

> **Note:** for live sync via xurl (the typical path), see [Section 4 → After xurl works, wire it to birdclaw](#after-xurl-works-wire-it-to-birdclaw) — including the **seed-account SQL fix** (default account row points at @steipete out-of-the-box and must be updated to your handle).

### Path A — archive import (no API needed)

1. Request an archive at https://x.com/settings/your_data — takes ~24h to prepare.
2. Download the `.zip` archive when ready.
3. Import:
   ```bash
   birdclaw archive find
   # Lists detected archives in ~/Downloads etc.
   birdclaw import
   ```
4. After import, all bookmarks/likes/tweets are in `~/.birdclaw/birdclaw.sqlite`. Live sync still requires xurl.

### Path B — live sync (needs xurl, see section 4)

```bash
birdclaw sync bookmarks
birdclaw sync likes
birdclaw sync mentions
```

---

## 7. WhatsApp — `wacli` / `wacrawl`

**Status:** needs WhatsApp account auth. Runs a local server on macOS that pairs with your phone.

```bash
wacli init
# Scans QR code on phone (WhatsApp → Linked Devices → Link a Device)
wacli status
```

For data archaeology (full message history with encryption):
```bash
wacrawl --help
# See repo for one-time setup; depends on local WhatsApp Desktop installation
```

---

## 8. Discord — `discrawl`

**Status:** needs a **Discord bot token** for any server you want to crawl.

```bash
# 1. Create a bot at https://discord.com/developers/applications
# 2. Copy the bot token from the Bot tab
export DISCORD_BOT_TOKEN="your-bot-token"
discrawl doctor
discrawl init
discrawl sync --full
```

For read-only DM/saved-items work, the bot needs to be added to relevant servers; DMs are inherently restricted to user tokens (which are TOS-violating to use programmatically) — for personal DM cleanup, use the official Discord app.

---

## 9. Slack — Slack Web API (no CLI yet)

**Status:** `slackclaw` repo created at https://github.com/itsryanarmani/slackclaw but not yet implemented. Until then:

1. Create a Slack app at https://api.slack.com/apps.
2. Add scopes: `users.profile:read`, `conversations.read`, `conversations.history`, `conversations.write`, `bookmarks.read`.
3. Install to your workspace, copy the User OAuth Token (`xoxp-...`).
4. Use it in scripts directly (curl + jq) until `slackclaw` ships.

---

## 10. LinkedIn / Instagram / Threads

**Status:** repos created (`linkedinclaw`, `instaclaw`, `threadsclaw`) but not yet implemented. All three need browser-cookie scrapers in steipete's `*claw` style.

Until those ship, manual export paths:
- **LinkedIn**: Settings → Data Privacy → Get a copy of your data.
- **Instagram**: Meta Account Center → Your Information → Download your information.
- **Threads**: Same as Instagram (shared Meta account).

---

## 11. GitHub — `gh`

**Status:** GitHub's official CLI. Usually already authed if you've used it.

```bash
gh auth status
# If not authed:
gh auth login
# To add scopes for delete_repo (needed by the github organizer skill):
gh auth refresh -s delete_repo
```

---

## Auth state cheatsheet (paste-friendly)

```bash
# Run all checks at once
echo "=== gog ===" && gog auth doctor 2>&1 | tail -3
echo "=== spogo ===" && spogo auth status 2>&1 | head -3
echo "=== xurl ===" && xurl auth status 2>&1 | head -3
echo "=== birdclaw ===" && birdclaw auth status 2>&1 | head -3
echo "=== remindctl ===" && remindctl status 2>&1 | head -1
echo "=== imsg ===" && imsg chats 2>&1 | head -1
echo "=== gh ===" && gh auth status 2>&1 | head -3
```

---

## When ready to run organizers

After all the relevant auths are green, any session can:

```bash
# Pick a surface and follow the corresponding skill
# org-spotify-playlist/SKILL.md
# org-x-bookmarks/SKILL.md
# org-imessage/SKILL.md
# org-gcal/SKILL.md
# ... etc
```

Or invoke the `org-life-organizer` master skill to get a recommended sequence.
