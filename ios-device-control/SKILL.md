---
name: ios-device-control
description: "Use when an agent must operate a real iPhone from a Mac: open apps, read the screen, tap, type, scroll and take screenshots, for example to read Settings or check an app. Sets up WebDriverAgent with go-ios and mobile-mcp over USB, and lists the traps that each cost a real cycle on iOS 27. Never unlocks the phone and never enters a passcode. Triggers: 'give the agent access to my iPhone', 'control my phone from the Mac', 'tap through Settings on my iPhone', 'mobile-mcp real device'."
---

# Control a real iPhone from a Mac

An agent drives a USB iPhone through **WebDriverAgent**, a test app that runs on
the phone and answers HTTP on port 8100. It taps, types, swipes, launches apps
and returns the screen's element tree. **go-ios** opens the tunnel that iOS 17
and later need. **mobile-mcp** exposes the same actions as MCP tools.

**Stop point:** the agent never unlocks the phone and never types a passcode.
The owner unlocks it. Ask before any tap that changes a setting, sends a
message, buys, or deletes.

## Decide the route

| Route | What you get | Cost |
|---|---|---|
| WebDriverAgent + go-ios | Taps, typing, element tree, app launch | Xcode build, developer signing |
| + mobile-mcp | The same, as MCP tools in the agent | One `mcp add` |
| `xcrun devicectl device capture screenshot` alone | Screenshots, no input | Developer Mode on |
| iPhone Mirroring + Mac input injection | Taps through a Mac window | Same Apple ID on both, phone locked |

WebDriverAgent cannot read another app's private files. It sees only what is
on the screen.

## Requirements

- Xcode signed in to a developer account: **Xcode > Settings > Accounts**. A
  free account signs for 7 days, so rebuild weekly. A paid account signs for a
  year. Check: `security find-identity -v -p codesigning`.
- The team ID is the `OU` of the Apple Development certificate:
  `security find-certificate -c "Apple Development" -p | openssl x509 -noout -subject`.
- Developer Mode on the phone, the phone on USB, and "Trust This Computer"
  accepted.
- `npm install -g go-ios` (provides `ios`), `brew install libimobiledevice`.

## Set up

The `iphone-wda` script in
[itsryanarmani/scripts](https://github.com/itsryanarmani/scripts) does every step:

```sh
IPHONE_WDA_TEAM=<team id> iphone-wda up   # build, install, tunnel, forward, wait
iphone-wda open com.apple.Preferences
iphone-wda tree                           # type | label | value per element
iphone-wda find General                   # drag until visible, then tap
iphone-wda shot screen.png
```

By hand, the same steps are:

1. Clone `appium/WebDriverAgent` into its own directory.
2. `xcodebuild build-for-testing -scheme WebDriverAgentRunner -destination id=<udid>
   -allowProvisioningUpdates DEVELOPMENT_TEAM=<team> PRODUCT_BUNDLE_IDENTIFIER=com.<you>.WebDriverAgentRunner`.
   The stock bundle ID belongs to another team and fails signing.
3. `ios tunnel start --userspace` in the background. No sudo needed.
4. `xcodebuild test-without-building -xctestrun <file> -destination id=<udid>` in
   the background. The log prints `ServerURLHere->http://<ip>:8100`.
5. `ios forward 8100 8100`, then `curl localhost:8100/status`.

Add mobile-mcp, pinned:

```sh
CLAUDE_CONFIG_DIR=<config dir> command claude mcp add mobile-mcp -s user -- npx -y @mobilenext/mobile-mcp@<version>
```

mobile-mcp finds real devices through go-ios and expects WebDriverAgent on port
8100. Its tools load only in a new agent session.

## Traps

Each of these cost a cycle on a real iPhone running iOS 27.

| Symptom | Cause | Fix |
|---|---|---|
| `Unable to log in with account ... login details were rejected` | Xcode's saved account session expired | The owner signs in again in Xcode > Settings > Accounts |
| `Unlock <name> to Continue` in the test log | The phone is locked | The owner unlocks it; the run continues by itself |
| `/wda/locked` is false but app launch fails with `could not be unlocked` | `/wda/locked` reports the screen is on, not that the passcode was entered | Test unlock by launching an app, as `iphone-wda wait` does |
| A Settings row is missing from the tree | Settings builds rows lazily, and `/wda/swipe` did not scroll it | Drag by coordinates (`/wda/dragfromtoforduration`) until the row appears |
| An alert covers the screen but `/alert/dismiss` says no alert is open | A system alert, such as an account password prompt, is outside the app's tree | Screenshot, then tap the button by point. Points are pixels divided by the screen scale |
| `App-prefs:` URL opens Settings > Apps | iOS 27 no longer routes those paths | Navigate by taps |
| Settings search finds no result for a page | Search does not index every page | Navigate by taps |
| A tap by label opened the wrong page | A label match hit a row in another list | Use exact labels, and check the navigation bar after each tap |
| `claude mcp add` wrote to another account's config | A `claude` shell function picked a different `CLAUDE_CONFIG_DIR` | Run `command claude` with `CLAUDE_CONFIG_DIR` set |
| `idevicescreenshot` fails with `Invalid service` | It needs a developer disk image it cannot mount | Use `xcrun devicectl device capture screenshot` |

## Verify

- `curl -s localhost:8100/status` shows `"ready" : true`.
- `iphone-wda open com.apple.Preferences` then `iphone-wda tree` prints the
  Settings rows.
- A screenshot shows the screen you expect.

## Related skills

- [`org-iphone-storage`](../org-iphone-storage/SKILL.md) uses this to read
  Settings > General > iPhone Storage.
- [`ios-agent-preview`](../ios-agent-preview/SKILL.md) covers simulators and
  installing your own app.
- [`macos-input-injection`](../macos-input-injection/SKILL.md) covers the
  iPhone Mirroring route.
