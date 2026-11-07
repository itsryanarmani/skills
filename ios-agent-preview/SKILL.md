---
name: ios-agent-preview
description: "Use when you need to see an iOS app running without driving Xcode by hand — streaming a simulator to a phone or browser, installing on a real device, or wiring macOS CI. Starts from the question that decides everything: whether the Apple Developer account is free or paid, because most sideloading tools silently require the paid program and fail late. Covers simmer, the free-account ceiling, Namespace macOS runners, xcodegen, and the traps that each cost a real cycle. Triggers: 'see the app on my phone', 'preview iOS without a cable', 'stream the simulator', 'iOS CI', 'sideload', 'TestFlight alternative', 'ad-hoc install'."
---

# Seeing an iOS app without driving Xcode by hand

## Verify membership, access, and signing separately

Confirm active Apple Developer Program membership in the developer account.
Check the selected team, membership status, and renewal date.
If account access is unavailable, record membership as unknown.
Do not infer membership from local certificates or provisioning profiles.

Next, check App Store Connect access and the user's role.
An expired membership or an unsigned agreement can block program resources.
The Account Holder must review and accept new agreements.
Do not accept legal agreements on the owner's behalf.

Finally, inspect local signing assets when the chosen workflow needs them:

```bash
security find-identity -v -p codesigning
```

This command reports local signing identities. It does not report membership.
Avoid publishing identity names or private account details in evidence.

Paid teams can use cloud-managed distribution certificates without a local
Apple Distribution identity. Check cloud signing permissions separately.
A signing failure can indicate missing access, rather than free membership.
Do not create duplicate certificates or revoke working assets to test this.

Record three separate results: membership, account access, and signing.
Use verified, blocked, or unknown for each result.
Prove signing with a successful export for the intended distribution method.
A development-signed archive alone does not prove TestFlight readiness.
Export or upload only within the user's existing authorization.

Sources checked November 6, 2026:
[cloud-managed certificates](https://developer.apple.com/help/account/certificates/cloud-managed-certificates/),
[access issues](https://developer.apple.com/help/account/access/resolving-access-issues/),
and [roles](https://developer.apple.com/help/account/access/roles/).

After verifying membership, choose the supported route:

| Route | Needs | Free account |
|---|---|---|
| Sign-and-serve install page (Sqim and similar) | ad-hoc provisioning | **No** |
| TestFlight, App Store Connect automation | paid program | **No** |
| Any ad-hoc or UDID-registered install | paid program | **No** |
| Streaming a simulator | nothing | **Yes** |
| Xcode, cable, Run | free identity, 7-day profile | **Yes** |

A free account still reaches a real device: connect once, press Run, and Xcode
does wireless debugging on the same network afterwards. The profile expires
after seven days.

## Streaming a simulator, which needs no signing at all

[`simmer`](https://github.com/joshdholtz/simmer) streams a booted simulator to a
browser and relays touch back.

```bash
brew install joshdholtz/tap/simmer
simmer --port 8901 --mode fast --quality 95 --fps 30
```

Four traps, in the order they bite:

1. **`--mode auto` hangs on "starting simmer…" forever**, because the `compat`
   path wants `idb-companion` and it is usually not installed. Use `--mode fast`,
   which captures through Quartz.
2. **`xcrun simctl boot` boots headlessly.** Quartz needs a real window, so the
   streamable list comes back empty and the picker looks broken. Run
   `open -a Simulator`.
3. **The picker lists devices it can boot, not devices that are booted.** A
   device you booted yourself vanishes from it. These are two different sets:
   check the streamable endpoint against the bootable one before concluding
   anything is wrong.
4. **Accessibility cannot attach to a launchd-parented CLI binary.** Screen
   recording grants fine, so video works, but touch relay may never work. Adding
   the binary by hand under Privacy & Security is the only lever and it can still
   report false.

For access from outside the network, tunnel it. On ngrok's free tier the first
request shows an interstitial the user must tap through — that blank page is not
a broken link:

```bash
ngrok http 8901
```

**Know what a stream cannot tell you.** It is video plus a touch relay. Good for
art, layout and flow. Useless for judging input latency, because the stream adds
its own. If latency is what you are evaluating, use a real device.

## Generate the Xcode project, do not commit it

Use [xcodegen](https://github.com/yonaskolb/XcodeGen) with a `project.yml` and
**gitignore the `.xcodeproj`**. Committing both leaves two sources of truth for
one target, and they drift silently.

```bash
xcodegen generate --spec app/project.yml
xcodebuild -project app/MyApp.xcodeproj -scheme MyApp \
  -destination 'platform=iOS Simulator,name=iPhone 17' build
```

## macOS CI

Cheap runner fleets are Linux, so an iOS build needs a macOS runner.
[Namespace](https://namespace.so) has them on Apple Silicon:

```yaml
runs-on: nscloud-macos-tahoe-arm64-6x14   # shapes: 6x14, 12x28, 12x56
```

Two findings worth keeping:

- **Namespace runner profiles cannot be macOS.** `nsc github profile create --os`
  accepts only `ubuntu-*`. Put the standard label in `runs-on` directly.
- **`nsc create --selectors macos.version=26.x` returns a Linux k3s cluster.** It
  reports success. A selector naming something that does not apply never errors,
  so verify what you got rather than trusting the exit code.

Do not let CI stop at a successful compile. Boot, launch, and confirm the process
is still alive seconds later, because a crash on launch still returns success
from `simctl launch`:

```bash
xcrun simctl bootstatus 'iPhone 17' -b
xcrun simctl install booted path/to/App.app
xcrun simctl launch --terminate-running-process booted com.example.app
xcrun simctl io booted screenshot proof.png
```

Upload that screenshot as a CI artifact so a reviewer sees the app ran, rather
than only that it built.

## Other tools, and what each is actually for

- [App-Store-Connect-CLI](https://github.com/rorkai/App-Store-Connect-CLI) —
  scriptable TestFlight, builds, submissions, screenshots. Paid program only. Its
  API key can submit apps in your name, so keep it out of the repository.
- [vphone-cli](https://github.com/Lakr233/vphone-cli) — scripted iOS VMs on the
  Mac. Never reaches a phone.
- [agent-simulator](https://github.com/jasonkneen/agent-simulator) — a simulator
  in a browser an agent can **inspect**. Inspection is the point: an agent that
  reads the view tree asserts on state rather than on pixels.
- `npx serve-sim` — accessibility-tree inspector for a running app.
- <https://reactnativefeel.com/sim> — simulator tooling reference.
- [Apple HIG](https://developer.apple.com/design/human-interface-guidelines) —
  read Games and Accessibility before designing any on-screen control.

## On-device AI

Apple's Foundation Models framework runs a small model on the device at zero
inference cost. It is Swift only, so React Native needs a native module, and it
is missing on older hardware. Every feature built on it needs a fallback, and
nothing load-bearing should depend on it.
