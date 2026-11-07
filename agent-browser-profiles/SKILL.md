---
name: agent-browser-profiles
description: "Run agent-browser automation in isolated per-context browsers (for example work vs personal) so profiles never mix and Chrome stops showing the 'Allow remote debugging' prompt. Covers the AGENT_BROWSER_AUTO_CONNECT pitfall, the isolated-profile vs real-Chrome-clone tradeoff, and the macOS keychain / Chrome-136 / device-bound-cookie constraints. Use when agent-browser attaches to the wrong Chrome, keeps prompting for remote debugging, ignores --profile, or when you need separate logged-in browsers for separate contexts."
---

# agent-browser work/personal profiles

Keep separate automation browsers for separate contexts. Each runs on its own
profile. They never mix. And Chrome stops showing the "Allow remote debugging"
prompt.

Implementation lives in `itsryanarmani/scripts` (`scripts/agent-browser/`). This
skill describes when and how to use it.

## First, fix AUTO_CONNECT

Set `AGENT_BROWSER_AUTO_CONNECT=0` in your shell config.

With `AGENT_BROWSER_AUTO_CONNECT=1`, `agent-browser` attaches every call to your
daily Chrome and ignores `--profile`. Chrome 136 then shows the "Allow remote
debugging" prompt again and again, and automation lands in the wrong profile.
Set the value to `0` to make `agent-browser` isolated by default. Opt into
attaching to your daily Chrome only with a dedicated command.

If automation keeps hitting the prompt or ignores `--profile`, check this
setting first.

## Choose an approach

**Fresh isolated profile.** A clean Chrome-for-Testing profile. You log in once;
the login persists. No prompts. Use it for a site you can sign into again.

**Real Chrome on a clone.** The real Chrome binary runs on a copy of one real
profile. You keep your existing logins. No prompt. Use it when you cannot or do
not want to sign in again. Give each clone its own port.

Rule of thumb: use a fresh profile when a re-login is cheap. Use a clone when you
need existing logins to carry over.

## Constraints to know

- **Keychain.** Chrome-for-Testing uses a separate macOS Keychain entry. Cookies
  from your real Chrome do not decrypt inside it. Do not copy cookies into
  Chrome-for-Testing. The clone approach works instead, because real Chrome
  shares one keychain key across any user-data directory.
- **Chrome 136.** Chrome 136 blocks remote debugging on the Default profile and
  ignores the port there. Launch real Chrome with the debug flag on a distinct
  user-data directory to stay prompt-free. The prompt fires only when you attach
  to a running user session.
- **Device-bound cookies (DBSC).** Google binds web session cookies to the
  device. So Google-owned sites, such as Gmail, can still need one sign-in inside
  a clone. Other sites usually carry over.

## Separation contract

Each clone holds exactly one source profile. So one context never sees another
context's logins. Give each clone its own directory and its own port.

## Commands (shape only)

Set up shell functions like these. See `itsryanarmani/scripts` for the real script
and full examples.

```sh
export AGENT_BROWSER_AUTO_CONNECT=0
browser-work       # fresh isolated profile, work context
browser-personal   # fresh isolated profile, personal context
browser-work-real  # real Chrome on a work clone (existing logins)
browser-attach     # opt into driving your daily Chrome
```

## Driving a form once you are in

Picking the browser is half of it. Filling a form and knowing whether it worked
is the other half, and every failure there is silent: `fill` on an unbound ref,
a click on a disabled button, and a loop that narrates its own success all
report `✓ Done` while doing nothing.

See [references/driving-forms.md](references/driving-forms.md).
