# Setup traps

Each fault below happened on a real setup. The fix is the one that worked.

## 1. Postgres port 5432 is taken

A local Postgres can already listen on 5432. The container starts, but the app talks to the local one. `db:migrate` then fails with `role "phone_farm" does not exist`.

Fix: add `POSTGRES_PORT=5433` to `.env` and change the port in `DATABASE_URL` to 5433. Run `docker compose down`, then `npm run db:up`.

## 2. OrbStack stops and Postgres goes with it

OrbStack quit during a long session. `web` and `worker` then crashed with `connect ECONNREFUSED 127.0.0.1:5433`. The log ended with a blank line and the Node version, with no clear message.

Fix: run `orbctl start`, then `npm run db:up`, then restart `worker` and `web`. Check `docker ps` first when a process dies silently.

## 3. The repo points at a missing Xcode

`src/devices/wda/xcode-env.ts` defaults to `/Applications/Xcode_26.2.app`. If that path is missing, `xcodebuild` fails with `missing DEVELOPER_DIR path`.

Fix: add `XCODE_DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer` to `.env`.

## 4. The WDA patch does not apply

`Patches/appium-webdriveragent-8.9.1-absolute-touch.patch` failed on a clean WDA tree. macOS `patch` printed `File to patch:` and ignored four hunks. Two defects caused this:

- The hunk header for the large insert declared 139 lines. The hunk held 149.
- The patch used `request.modificationDate` on a `PHAssetCreationRequest`. That property does not exist. The build fails with `property 'modificationDate' not found`.

Fix, in this order:

1. Delete the `request.modificationDate` line from the patch.
2. Set the line count in the large hunk header to the real count. Move the new-file start of each later hunk by the same difference.
3. Check with `git apply --unidiff-zero -p0 --check <patch>`.
4. Reinstall the driver (`rm -rf .appium2`, then `npm run appium:install-driver`) so the tree is clean. Then run `wda:prepare`.

A failed first run can leave a half-patched tree. Always start from a clean tree.

## 5. A stale port forward holds port 8100

An old `ios forward 8100 8100` process from go-ios held the port for days. WDA retried with `The port #8100 is occupied by an other process`.

Fix: find it with `lsof -nP -iTCP:8100`. Stop it if it is yours.

## 6. API writes return "Cross-origin write blocked"

Every non-GET request needs an `Origin` header equal to the request host, or a `Bearer` token. `curl` sends no `Origin`.

Fix: send `-H "Origin: http://127.0.0.1:3000"` and call the same host. `localhost` in the URL with an `127.0.0.1` Origin also failed.

## 7. Display Zoom breaks the tap map

An iPhone 12 Pro Max with Display Zoom on reported 375 by 812 points to WDA. The registration check warned: the chosen map expected 390 by 844. Taps then land in the wrong place.

Fix: turn Display Zoom off (Settings, Display & Brightness, Display Zoom, Standard). Then pick the map that matches the new screen size. The repo ships maps for iPhone 8, X, 13/14 and 17 Pro. A 12 Pro Max has no map of its own.

## Also

- WDA signing needs the login keychain. Run `wda:prepare` from Terminal.app, not SSH.
- Keep `mobile-mcp` and the farm off the same phone at the same time. A `mobile-mcp` screenshot failed with `failed to parse screenshot response` while the farm held WDA on port 8100.
- The repo keeps a stored passcode in `devices.json` as plain text. The file is git-ignored and mode `0600`. That does not stop a local reader or a backup. Prefer Auto-Lock set to Never on a dedicated test phone. Store a passcode only for a phone that holds nothing private.
- Never put a real UDID, team ID or passcode in an issue, a PR or an `.env` example you share.
