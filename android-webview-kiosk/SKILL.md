---
name: android-webview-kiosk
description: "Build and operate a locked-down Android WebView kiosk app on a dedicated touch panel — no Android Studio, no Play Store. Covers the minimal single-Activity WebView shell, the lockdown ladder (immersive + gesture exclusion up to device-owner + startLockTask), bundling web content for fully offline operation, the hot-update path that avoids APK reinstalls (filesDir + run-as push + reload intent), the WebView renderer bad-state that only a reboot clears, and wireless-debugging persistence. Use when putting a web app on a wall-mounted or countertop Android panel."
---

# Android WebView kiosk

A WebView wrapper is the fastest way to put a finished web app onto a dedicated
Android touch panel. The app is one Activity, one WebView, and all content
bundled in `assets/`. What follows is the layout that works, the update path
that avoids the renderer trap, and the failure modes that each cost a reboot
before they were understood.

Companion scripts: `webview-kiosk-build` and `webview-kiosk-update` in
itsryanarmani/scripts.

## The app shell

One Activity. Programmatic WebView, no layout XML needed:

```java
web = new WebView(this);
WebSettings s = web.getSettings();
s.setJavaScriptEnabled(true);
s.setDomStorageEnabled(true);
s.setSupportZoom(false);
s.setBuiltInZoomControls(false);
s.setLoadWithOverviewMode(true);
s.setUseWideViewPort(true);
s.setAllowFileAccess(true);
setContentView(web);
```

Manifest essentials on the Activity: `configChanges="orientation|screenSize|keyboardHidden"`
(no Activity churn on rotation), `launchMode="singleTask"` (intents reach the
running instance — required for the reload trick below), and `HOME` +
`DEFAULT` categories if the app should be selectable as the launcher.

`android:debuggable="true"` on `<application>` is what makes `run-as` work,
which the update path below depends on — but it also leaves the app sandbox
fully readable/writable (including an `adb backup` of `filesDir`) to any host
already paired over the wireless-debugging transport this skill keeps armed.
Scope it to the updatable demo shell only. The device-owner build is
permanently un-updatable except by reflashing (see the frozen-build trap
below), so ship it non-debuggable — a debug flag baked into an undeletable
build is a backdoor that no later change can patch out.

## Lockdown ladder, weakest to strongest

1. **Immersive sticky** — hides status/nav bars; a swipe reveals them briefly.
2. **Zoom off** — `setSupportZoom(false)` + viewport meta
   `user-scalable=no` on every page. Do both; either alone leaks.
3. **Back is in-app navigation** — `onBackPressed()` calls `web.goBack()`;
   never let it reach `super` while there is history.
4. **Gesture exclusion** — `setSystemGestureExclusionRects()` covering the
   screen edges stops swipe-from-edge = system Back (the gesture that looks
   like the app "going back on its own").
5. **Screen pinning / lock task** — `startLockTask()`. Without device-owner
   the user sees "swipe up & hold to unpin"; with device-owner it is a real
   lock. `dpm set-device-owner` only works on a device with zero accounts and
   no existing owner — check `adb shell dumpsys account` first.
6. **Device owner** — the app's AdminReceiver as owner enables the lock-task
   allowlist, keyguard disable, and status-bar control. Also makes the app
   **undeletable and un-updatable except with the same signing key.**

## The frozen-build trap (worst failure here)

A device-owner app signed with a keystore you lose — or rebuilt with a
different one — can never be updated, disabled, or uninstalled without a
factory reset. `pm disable` answers `Cannot disable a protected package`.

- Generate the keystore once, store it **outside** `build/` (a `rm -rf build`
   between builds is all it takes to lose it), and vault it in a secrets
   manager — never commit it. It is the only key that can ever sign a
   replacement for an undeletable device-owner app; anyone with repo read
   access (now or from a future leak of the history) could sign and install
   an arbitrary APK with it.
- Keep the first signed APK. If the on-device build predates a feature, that
   build is what the panel runs forever.
- Treat a device-owner build as a one-shot artifact: get the content right,
   or make the device-owner shell load remote/mutable content from day one.

The pragmatic split that fell out of this: one frozen device-owner build as
the lockdown proof, one normal debuggable app as the updatable demo shell.

## Offline operation

Bundle everything under `assets/` and load `file:///android_asset/…`. Sweep
the source for external URLs first (`grep -rE 'https?://'` on the web root) —
one CDN font or image breaks the offline claim silently.

`file://` rules on API 30+:

- `file:///sdcard/…` is hard-blocked for WebViews regardless of
  `MANAGE_EXTERNAL_STORAGE` or runtime grants. Do not bother.
- `file://` + the app's own `filesDir` **works** — that is the update path.

## The update path (no reinstall, no reboot)

The app resolves its start page like this:

```java
File upd = new File(getFilesDir(), "kiosk/index.html");
web.loadUrl(upd.exists()
    ? "file://" + upd.getAbsolutePath()
    : "file:///android_asset/index.html");
```

To push new content:

```bash
adb push <webroot> /data/local/tmp/kiosk-push
adb shell "run-as <pkg> sh -c 'rm -rf files/kiosk && cp -r /data/local/tmp/kiosk-push files/kiosk'"
adb shell am start -n <pkg>/.MainActivity --ez reload true
```

`singleTask` delivers that intent to the running Activity as `onNewIntent`;
call `web.loadUrl(...)` there. The running WebView re-navigates in place — no
new process, no renderer bind, no bad state. `webview-kiosk-update` wraps
this.

**Never `am force-stop` or `install -r` for a content update.** Both can kill
the WebView renderer mid-association and trigger the bad-state below. That is
the entire reason this path exists.

## The renderer bad-state

Symptom: app launches to a white screen, activity stays resumed, no crash.
Logcat shows `cr_ChildProcessConn: Failed to establish the service
connection` and often Mali/GPU alloc errors.

Cause: `install -r` or `force-stop` while a WebView renderer was attached can
leave the package's child-process binding poisoned in AMS. A self-heal that
`recreate()`s the Activity does **not** fix it — the flag is package-level,
not view-level. Only a reboot (or a long idle) clears it.

Rules that follow:

- After any `install -r`, reboot the panel once before judging anything.
- All routine updates go through the reload-intent path instead.
- Keep a small self-heal (reload the URL after N seconds without
  `onPageFinished`) for genuine slow starts, but bound it — three retries of
  a dead bind just logs three failures.

## Wireless debugging on a panel

- The mDNS/TLS transport (`adb-<serial>._adb-tls-connect._tcp`) survives
  reboots; the raw `:5555` listener usually does not. Connect through the
  mDNS name, not the IP.
- The *toggle* can still come back off. `settings put global
  adb_wifi_enabled 1` re-arms it on some builds — set it before any planned
  reboot.
- Keep a USB-C cable within reach. One dead transport day costs more than the
  cable.

## Command-line build pipeline

`javac` + `d8` + `aapt2` + `zipalign` + `apksigner` from the Android
command-line tools package build a signed APK with zero Gradle. Roughly:

1. `aapt2 compile --dir res` + `aapt2 link -A assets --java gen` → base APK + R.java
2. `javac -classpath android.jar` sources + R.java → classes
3. `d8` → classes.dex, `zip -u` into the APK
4. `zipalign` → `apksigner sign` with the persisted keystore

`webview-kiosk-build` in itsryanarmani/scripts is this pipeline parameterized on
an app directory.

## Panel checklist

- Portrait AND landscape screenshots on the real panel, not just desktop —
  `justify-content:center` main regions clip tall content in short viewports;
  use a top-aligned variant on long pages.
- Touch targets ≥ 48dp effective, labels `white-space:nowrap` where wrapping
  breaks the layout.
- A hidden staff exit (N-tap or long-press on a brand element → PIN) — the
  demo always needs a way out that a user can't find.
- Inactivity reset in the page layer: clear `sessionStorage`, route to the
  attract screen. The attract screen is the privacy boundary.
