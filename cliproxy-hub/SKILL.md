---
name: cliproxy-hub
description: Run one always-on CLIProxyAPI hub on a home machine and point Claude Code and Codex on every other host at it over Tailscale. Load when a host needs Claude, Codex or Grok access without its own login, when the hub shows "token expired", "unauthorized" or a 426 version error, when a client gets 503 auth_unavailable, when adding a seat, or when a Boat box that uses the hub hides a secret, a clone error, or a dead login. Based on Theo's CLIProxyAPI guide.
---

# CLIProxyAPI hub

One home machine holds every Claude, Codex and xAI login. Every other host calls that
machine over Tailscale. Source guide:
https://gist.github.com/t3dotgg/59a521d2ee8d70aaf90e280c175072af

Tool: `cliproxy-hub` in pooriaarab/scripts.

## Two hard rules

1. Claude seats run in Claude Code only. Codex seats run in Codex only.
   A tool uses the hub by running Claude Code or Codex on its host. Do not call the
   hub from any other tool with a Claude or Codex seat.
2. The hub is a home machine. Never a VPS or a datacenter host. Never serve
   other people's traffic with these seats.

The guide says a ban is possible. Tell the user this before you start.

## Set up the hub

1. Install and start: `brew install cliproxyapi && brew services start cliproxyapi`.
2. In the config, bind `host: "127.0.0.1"`, set `api-keys`, and set a management `secret-key`.
3. Put the hub on the tailnet. Run this in a real Terminal window, not from an agent
   shell. The macOS Tailscale app refuses `serve` from an agent shell. HTTPS must be
   on in the Tailscale admin console.

   ```sh
   cliproxy-hub serve
   ```

4. Keep the hub awake. A sleeping hub stops every client.

   ```sh
   sudo pmset -c sleep 0
   ```

   `-c` applies on power only, and the Mac still sleeps when you close the lid. Turn on automatic
   login so the service starts again after a reboot.
5. Keep the hub up to date. An old build sends an old Grok CLI version, and xAI returns
   `426 ... CLI version is outdated`. Run `brew upgrade cliproxyapi` and
   `brew services restart cliproxyapi`. Seats survive the upgrade.

## Check health

```sh
cliproxy-hub check
```

`/v1/models` lists models even when every seat is dead. Trust the `seats:` lines.
A client call to a dead seat returns `503 auth_unavailable`.

## Log in or repair a seat

A seat dies when its refresh token expires or is revoked. Log in again on the hub
machine, one seat at a time:

```sh
tail -f /dev/null | cliproxyapi -claude-login -no-browser   # Claude
tail -f /dev/null | cliproxyapi -codex-login -no-browser    # Codex
tail -f /dev/null | cliproxyapi -xai-login -no-browser      # xAI (Grok)
```

The `tail -f /dev/null |` part keeps stdin open. Without it the login exits when stdin
closes and the browser callback finds nothing.

Rules that each cost a failed attempt:

- Use the Chrome profile that matches the seat. A wrong profile adds a seat for the wrong account.
- Close every old `localhost:54545` (Claude) or `localhost:1455` (Codex) tab first. A stale tab
  retries its old callback and the login stops with `State mismatch`.
- Open each link once. A link works only with the login process that printed it.
- Finish within about 5 minutes. The login times out.
- After the login, run `cliproxy-hub check` and confirm the seat shows `ok`.
- Move a retired seat file out of `~/.cli-proxy-api`. Do not delete it.

## Point a client host at the hub

Every client host needs Tailscale on the same tailnet and a Claude Code or Codex install.

1. Put the hub URL and key on the host. Write the key to a 0600 file. Never paste it in chat.
2. Run:

```sh
export HUB_URL="https://<hub>.<tailnet>.ts.net:8317"
export HUB_KEY_FILE=~/.hub-key
cliproxy-hub verify
cliproxy-hub client claude    # writes ~/.claude-hub/settings.json
cliproxy-hub client codex     # writes ~/.codex-hub/config.toml
```

3. Start the tools with the second config dir. The normal install stays unchanged:

```sh
CLAUDE_CONFIG_DIR=~/.claude-hub claude
CODEX_HOME=~/.codex-hub codex
```

Pass `--config-dir` or `--codex-home` to replace the normal config instead. The script
backs up the old file first.

A client on a datacenter host is fine, because only the hub talks to Anthropic and
OpenAI. Never log in to a seat on a client host.

## Tools that cannot use the hub

The hub only serves Claude, Codex, xAI, Kimi and Antigravity seats. Cursor, Devin and
Muse keep their own logins on each host: `cursor-agent login`, `devin auth login`,
`muse login`. They print a code or a link for a browser. A tool that calls models
directly never receives a Claude or Codex seat. It runs Claude Code or Codex.

## T3 Code

T3 Code uses the CLI config of the machine that runs the provider. For Codex, choose
"Use existing CLI". "Continue with ChatGPT" does not use the hub.

## Prompt for an agent on a client host

Copy this to the agent on a new host. Fill in the hub URL.

```text
Set this host up as a client of our CLIProxyAPI hub. Rules: Claude seats run only in
Claude Code and Codex seats run only in Codex. Never print, paste or commit the hub key.
Never log in to a Claude or Codex seat on this host. Do not edit the normal ~/.claude
or ~/.codex config.

1. Read the cliproxy-hub skill in pooriaarab/skills and use cliproxy-hub from
   pooriaarab/scripts.
2. Check Tailscale is on the same tailnet as the hub: tailscale status.
3. Put the key I give you in a 0600 file. Set HUB_URL and HUB_KEY_FILE.
4. Run: cliproxy-hub verify. Expect "hub reachable".
5. Run: cliproxy-hub client claude and cliproxy-hub client codex.
6. Test once with each tool: CLAUDE_CONFIG_DIR=~/.claude-hub claude -p "say ok" and
   CODEX_HOME=~/.codex-hub codex exec "say ok".
7. Report which commands passed. If one failed, quote the error and stop.
```

## Verify from a client

```sh
cliproxy-hub verify
```

Expect `hub reachable: N models`. Then send one small request with each tool.

## Traps

These traps apply when you make a Boat box that uses the hub (`boat-hub`).

- `boat env list` prints secret values. Do not run it raw in an agent session. Print the `name` fields only.
- `boat env add-repo` changes the environment. A probe that adds a repo leaves it there. Probe in a throwaway environment, then delete that environment.
- The connected-repo list can be stale. Boat can reject a newer repo with "not found in your connected GitHub repos". Open the dashboard. Go to Environment, then GitHub repositories, then Add Repository, then Refresh. A new login does not fix this. A change to the GitHub app permissions does not fix this.
- A box made with `--from <snapshot>` can skip environment injection. It then has no GitHub login and no repo clone. A box made without `--from` had both. Test that snapshot path with one canary box before you rely on it.
- `boat-hub warm` can hide a clone error and then wait five minutes. The hide was `|| true` with the output discarded. Capture the error and print it.
- Agent logins inside a box expire. A queued prompt can stay "queued" with no process and no error. Run a one-word canary prompt first. Check that an agent process exists. Then fan out.
- Check the trial limits and the wallet with `boat onboard --json` before you make several boxes.
- Delete idle boxes. They bill the wallet.
- `set -- $var` does not split in zsh. Pass explicit arguments, or use `${=var}`.
- `PATH` differs in a background shell. `gh` and `boat` can be missing there. Export `PATH` in that command.
- A delegate task runs in that thread's own project. From a scratch folder with no repo, it cannot make a worktree. Make the worktree yourself. Run the worker CLI in that worktree.
- Judge a worker on its diff and on its pull request. Do not judge it on its exit code.
