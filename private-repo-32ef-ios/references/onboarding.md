# Add one iPhone to the farm

Do these steps in order for each phone. Tick each box. Do not skip a check.
Each phone needs its own account, its own SIM or Wi-Fi, and its own local WDA port.

## A. Before you plug in

- [ ] Use a throwaway account on the phone. See [detection](detection.md).
- [ ] Note the model, iOS version and screen size in points (Settings, General, About).
- [ ] Charge the phone to 50 percent or more.
- [ ] Use a data cable. A charge-only cable shows no device.
- [ ] Use a powered USB hub or a direct Mac port. See [multi-device](multi-device.md).

## B. Phone settings (by hand, once)

- [ ] Turn on Developer Mode: Settings, Privacy & Security, Developer Mode. Restart.
- [ ] Set Auto-Lock to Never: Settings, Display & Brightness, Auto-Lock.
- [ ] Keep Display Zoom on Default. Record the size you get.
- [ ] Cancel any Exchange or password alert that covers Settings.
- [ ] Sign in to TikTok and Instagram on the throwaway account. Dismiss every pop-up.
- [ ] Turn off Life Recorder or any app that records audio.
- [ ] Plug in. Unlock. Tap Trust. Enter the passcode.

## C. Mac checks

- [ ] `xcrun devicectl list devices` shows the phone as `connected`.
- [ ] Copy its UDID.
- [ ] `./private-repo-32ef status` shows the farm up.
- [ ] `./private-repo-32ef apply-patch --check` says the patches apply or are applied.

## D. Screen profile

- [ ] Find the screen size in points. Look it up in `src/devices/coordinates.ts`.
- [ ] If the size has no profile, add one. Scale `iphone13` and tap-test the rail.
      Use the table in [live learnings](live-learnings.md) as the method.
- [ ] Test search, comment and share by tapping. Check each result on a screenshot.
- [ ] Set `coordinateProfile` for this UDID in `devices.json`.
- [ ] The tab bar y is not the scaled value on a tall phone. Tap-test home and profile.

## E. WDA

- [ ] Give the phone its own port: `wdaLocalPort` in `devices.json`. Use 8101 for phone two.
- [ ] Run `npm run wda:prepare` in the farm. It builds and signs WDA for the phone.
- [ ] Start one supervisor per phone. Never start two for the same phone.
- [ ] `curl http://127.0.0.1:<port>/status` shows `ready: true`.
- [ ] `./private-repo-32ef doctor <udid>` ends with no `NOT` or `FAILED` line.
- [ ] The screenshot is padded to the full size (see doctor output).

## F. Register

- [ ] `./private-repo-32ef register <udid>` finishes with `finalized`.
- [ ] Add the TikTok and Instagram handles in `devices.json` (mode 0600).
- [ ] Dashboard shows the phone as online.

## G. First run (passive)

- [ ] 3-minute doomscroll with likes, saves and comments off.
- [ ] Log shows `recoveries=0` and every screen read as `fyp`.
- [ ] Then enable one action at a time. Keep like rate low. Check the result in the app.

## H. Record it

- [ ] Add the UDID, model, size, profile and port to your device list.
- [ ] Write new traps in [live learnings](live-learnings.md).

Not yet tested: a second phone on the same Mac. Check that two Appium sessions run side
by side, and that `wda-service` hands each phone its own port.
