# More than one phone

Status: these are **general expectations**. This skill's author set up one phone. Nothing here was tested with two.

## Hardware

- Use direct USB ports or one **powered** USB hub. An unpowered hub can drop phones under charge and data load.
- Use data-capable cables. A charge-only cable shows no device.
- The app also needs the phone unlocked and trusted. Do this once per phone.
- Expect USB bandwidth and the Mac's CPU to limit the count. Live video from many phones at once is the heaviest part. Lower `MJPEG_SCALING_FACTOR` in `.env` to cut it.

## Per phone, once

1. Connect by USB. Unlock. Tap **Trust**.
2. Turn on Developer Mode (Settings, Privacy & Security). Restart.
3. Turn Display Zoom off. Set Auto-Lock to Never or store the passcode.
4. Check `xcrun xctrace list devices`. The phone must be under **Devices**, not **Devices Offline**.
5. Register it. See [API](api.md).

## Signing

- A paid team can sign WDA for many devices. A free team fits one, per the repo docs.
- Build WDA for every registered phone: `npm run wda:prepare -- --all`. Or one phone: `npm run wda:prepare -- --udid <udid>`.

## Ports

- Each phone needs its own `wdaLocalPort` and `mjpegLocalPort` in `devices.json`. The defaults are 8100 and 9100.
- Two phones on one port break both. After you register the second phone, open `devices.json` and check that the ports differ. The registration wizard has fields for both ports. Whether it picks free ones itself is not verified.
- Remember the stale-forward fault: a forgotten forward on 8100 blocks WDA. See [setup traps](setup-traps.md).

## Running tasks

- The API has a queue per phone (`POST /api/devices/<udid>/queue/clear`). Tasks for one phone wait for each other. Phones run in parallel.
- Remote input is blocked while a task runs on that phone.
- Use a different account on each phone. Do not share one account across phones.

## Always-on Mac

- `deploy/setup-mac-mini.sh` in the repo sets up a Mac mini. It installs Node and Postgres with Homebrew and writes `.env`. Run it from a graphical session. Read it before you run it. It runs `brew` and `sudo`.
- Wrap `appium`, `wda:service`, `worker` and `web` in `launchd` agents. The repo has examples in `deploy/launchd`.
- Keep Docker or OrbStack running if Postgres lives in it. See [setup traps](setup-traps.md), item 2.
