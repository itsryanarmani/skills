---
name: iphone-ble-bridge
description: "Control real iPhones from a Mac with no cable, no Developer Mode and no WebDriverAgent. An ESP32-S3 board acts as a Bluetooth mouse and keyboard, and iOS AssistiveTouch turns the pointer into touches. Covers pairing several phones to one board, the command protocol, Home and App Switcher button mapping, pointer calibration, and the NimBLE limits that drop the oldest phone when a third one pairs. Use when an iPhone must be driven by taps, swipes and typing and the WDA route is blocked, or when more than two phones share one board."
---

# iPhone BLE bridge

An ESP32-S3 shows up to each iPhone as a Bluetooth mouse and keyboard. AssistiveTouch **Perform Touch Gestures** turns pointer clicks and drags into touches. The Mac talks to the board over USB serial.

**Use when:** you must drive an iPhone and WebDriverAgent is blocked (no Developer Mode, iOS 16 with no usable developer image, no cable).

Firmware, build script and the full doc: `pooriaarab/private-repo-32ef` (`hardware/`, `docs/ble-bridge.md`). CLI: `pooriaarab/scripts` (`ble-bridge`).

## Set up one phone

1. Settings → Accessibility → Touch → AssistiveTouch: on. Perform Touch Gestures: on. Tracking Sensitivity: maximum.
2. Devices → Bluetooth Devices → the board (`Pad xxxx`) → accept the prompt.
3. Map the extra buttons. Open Devices → the board → Customize Additional Buttons. Send `@<slot> rclick`, then pick **Home**. Send `@<slot> mclick`, then pick **App Switcher**.

If the phone says "pairing unsuccessful", forget the board in AssistiveTouch Devices and in Settings → Bluetooth, then pair again.

## Commands

One line per command. Prefix `@<slot>` to pick a phone. The board answers `ok` or `err <why>`.

`ping`, `list`, `log`, `home`, `move dx dy`, `press`, `release`, `click`, `rclick`, `mclick`, `scroll v h`, `type text`, `key cmd+space`, `forget`.

`rclick` is Home and `mclick` is App Switcher after the mapping. Spotlight and `cmd+h` do not leave an app such as TikTok, so use `rclick`.

## Pointer scale

After `home`, one count moves the pointer about 12.7 px (x) and 12.55 px (y) in a 608x1080 mirror frame. To reach frame point (X, Y): `home`, then `move round(X/12.7) round(Y/12.55)`.

Wheel `scroll` is very slow. Drag instead: `press`, short `move` steps, `release`. Use 7 to 20 counts per drag. Larger drags overshoot because of momentum.

## Why a third phone drops the first

The stock NimBLE settings hold three phones. These limits all cause it, and each needs its own fix:

- The connection limit, the bond store and the client-feature store are 3.
- The L2CAP channel pool is `3 x connections`. At three links no channel is free, advertising stops (`adv=0`), and new phones see "pairing unsuccessful".

Flags fail in three ways, and each one wasted a flash cycle:

- `-DCONFIG_BT_NIMBLE_MAX_*` loses to the core's `sdkconfig.h`. Set the `MYNEWT_VAL_*` macros.
- The connection macro has no `#ifndef` guard in `esp_nimble_cfg.h`. Add the guard.
- `compiler.cpp.extra_flags` does not reach the library's C files. Set `compiler.c.extra_flags` too.

Use `hardware/build.sh` in private-repo-32ef. It does all three. To check a flag, preprocess one library file with the build's flags and read the macro.

## Status

Verified: five phones linked at once on one board. Each slot answered `ping` and a pointer `move`. At five links the board shows `adv=0`. This is normal. For more than five phones, add a second board.

Whether apps can detect this input path is not proven. Start with passive actions.
