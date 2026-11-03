---
name: black-october-hardening
description: Audit and harden a Mac during a browser and Electron patch window. Use when Chrome or Electron ships security fixes and you must find every old Chromium on the machine, update or remove the apps that bundle it, and close the local exposure that makes a browser bug worse. Triggers - 'black october', 'electron patch', 'old chromium', 'harden my mac', 'security audit of this machine'.
---

# Black October hardening

Every Electron app and every automation browser ships its own copy of Chromium.
Updating Chrome fixes one copy. The others stay old until you find them.

## Run the audit

The script lives in `pooriaarab/scripts`. It is read-only.

```bash
./black-october-audit --json /tmp/black-october.json
```

It exits 1 when a check fails. The JSON holds versions, app names, port numbers and
counts. It holds no URLs, headers, process arguments or secret values.

Set the floors for the current window:

```bash
./black-october-audit --min-chrome 156.0.8078.73 \
  --electron-floors "43:43.8.6 44:44.10.1 45:45.2.1"
```

## What each check means

| Check | Why it matters |
|---|---|
| `chrome.system` | Chrome auto-updates, but only after a relaunch. |
| `electron.<app>` | The app bundles its own Chromium. Only the vendor can update it. |
| `chromium.cache` | Playwright, Puppeteer and agent browsers keep old builds for months. |
| `browser.debug` | A remote debugging port gives any local process full control of that browser, with its cookies. |
| `net.listen` | A listener on all interfaces is reachable from the local network. |
| `macos.*` | SIP, FileVault, the firewall and Gatekeeper limit what a browser exploit can reach. |
| `secrets.perms` | Keys and token files must be readable only by the owner (mode 600). |
| `tooling.*` | Outdated Homebrew and npm tools carry their own bugs. |

## Fix order

1. **Update Electron apps that have a patched line.** Open the app. Check its version
   with the audit. Brew does not manage most of them.
2. **Remove apps on an unpatched line** that you do not need. Move them to the Trash,
   so you can undo it. Keep their data until you confirm nothing needs it.
3. **Delete old Chromium caches.** Use the cutoff, not the folder name. Playwright
   names folders by revision, so read the real version first.
4. **Point automation at system Chrome.** For the Playwright MCP, add
   `--browser chrome --sandbox` to its args.
5. **Turn on the firewall.** `sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on`
6. **Close debug ports** you do not use. Start Chrome with a dedicated profile when you
   need one.
7. **Run the audit again** and keep the JSON as the proof.

## Traps from the first run

- **The cache comes back.** A project that pins an old `@playwright/test` downloads its
  old Chromium again on the next test run. Upgrade Playwright in that project, then
  delete the cache.
- **Do not delete a build in use.** Check `ps` first. Wait for the run to end.
- **A plugin file is not permanent.** A marketplace update overwrites a plugin's
  `.mcp.json`. Define the server at user scope for a lasting change.
- **Old lines have no fix.** Electron 42 and below get no patch in this window.
  The only options are a new vendor release or removing the app.
- **Known-hosts files are public.** Do not flag them as secret files.
- **An absence proves nothing.** The audit has a positive case. Run it with
  `--min-chrome 999.0.0.0` and confirm it fails.
