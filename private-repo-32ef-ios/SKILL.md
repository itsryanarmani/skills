---
name: private-repo-32ef-ios
description: "Use when setting up or running Phone Farm iOS (kevs-ios-agents): a Mac that drives real iPhones through WebDriverAgent and Appium to run TikTok and Instagram tasks. Covers setup traps, the registration and task API, detection risk, and more than one phone."
---

# Phone Farm iOS

Drive real iPhones from a Mac with [kevs-ios-agents](https://github.com/kevinbadi/kevs-ios-agents). The app signs WebDriverAgent (WDA), starts Appium, and runs scheduled TikTok and Instagram tasks. It uses real devices and real apps. It is not an emulator.

This skill is the WDA and Appium path. For the ESP32 USB mouse path, use `iphone-agent`.

## When to use it

- You want to run a scheduled task on a phone that stays plugged into the Mac.
- You need the exact steps and the faults that cost time on a live setup.
- You want to know if TikTok or Instagram can detect the automation.

## Decide first

1. Use a **paid** Apple Developer team. The WDA profile lasted one year on the paid team here. The repo docs say a free team expires weekly and fits one device.
2. Use a **throwaway** account. Automation breaks both platforms' terms. Read [detection](references/detection.md).
3. Set **Auto-Lock to Never** on the phone before the first run. Check the screenshot size first. A phone larger than 375x812 gives cropped screenshots in Default mode. See [live learnings](references/live-learnings.md).
4. Prefer Auto-Lock set to Never on a dedicated test phone. If the phone must lock, the farm needs a stored passcode to unlock it. The repo stores it as plain text in `devices.json`. See [setup traps](references/setup-traps.md).

## Workflow

1. Clone the repo into its own folder. Run `npm install`.
2. Fix the setup traps in [setup traps](references/setup-traps.md). Do this before `wda:prepare`.
3. Start Postgres. Run `npm run db:migrate`.
4. Run `npm run wda:prepare -- --udid <udid>` from a graphical session, not bare SSH. Wait for `** TEST BUILD SUCCEEDED **`.
5. Start four processes: `appium`, `wda:service`, `worker`, `web`. Each is `npm run <name>`.
6. Register the phone. Use the dashboard at `http://127.0.0.1:3000/devices/register` or the API in [API](references/api.md).
7. Run one short task with likes and saves off. Read the execution log.

## Verify

- `curl localhost:3000/api/devices` lists the phone.
- `curl localhost:8100/status` returns the WDA build.
- Run a 3-minute task. Check `videosViewed`, `swipes` and `recoveries` in the last log line. Many recoveries mean the tap map does not fit the screen.
- Judge the run on the log and a screenshot from `localhost:8100/screenshot`. Do not judge it on the exit code.

## Stop and ask

- Stop before a task that posts, comments, sends a DM, or follows. Ask the owner first.
- Stop if the account is the owner's real account.
- Do not store a passcode, a UDID, a team ID or a username in a PR or an issue.

## References

- [Onboard a phone](references/onboarding.md) — one checklist for each new iPhone.
- [Setup traps](references/setup-traps.md) — seven faults and their fixes.
- [API](references/api.md) — registration flow, remote actions, task payload.
- [Detection](references/detection.md) — what the platforms can see. Untested.
- [More than one phone](references/multi-device.md) — hubs, ports, and an always-on Mac.
- [Observed run](references/observed-run.md) — the first TikTok warmup and why it failed.
- [Live learnings](references/live-learnings.md) — cropped screenshots, `devicectl` launch, human-like swipes.
