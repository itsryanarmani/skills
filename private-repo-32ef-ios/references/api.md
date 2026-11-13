# API

Base URL: `http://127.0.0.1:3000`. Send `Origin: http://127.0.0.1:3000` on every write. See [setup traps](setup-traps.md), item 6.

## Register a phone

Find the phone: `GET /api/devices/discovered`. It lists `udid`, `name`, `osVersion` and `productType`.

Then call these in order. `<udid>` is the registration id.

| Step | Call |
| --- | --- |
| Create | `POST /api/device-registrations` with `{"udid":"<udid>"}` |
| Refresh | `POST /api/device-registrations/<udid>/actions/refresh` |
| Prepare | `POST .../actions/prepare` (starts WDA and Appium) |
| Edit | `PATCH /api/device-registrations/<udid>` with `name`, `coordinateProfile`, `tiktokAccounts`, `instagramAccounts` or `passcode` |
| Verify | `POST .../actions/verify` |
| Finish | `POST .../actions/finalize` |

Rules:

- Only one action runs at a time. A second call returns `A registration action is already running`. Poll `GET /api/device-registrations/<udid>` until `busy` is `false`.
- `PATCH` also waits while an action runs. Send it when `busy` is `false`.
- `finalize` needs `canFinalize: true`. The `accounts` check must pass. It needs at least one account name.
- The accounts check took about four minutes in one run.
- Checks: `host`, `connection`, `signing`, `developer`, `wda`, `appium`, `video`, `touch`, `tiktok`, `instagram`, `accounts`.

## Look at the phone

- `GET /api/devices` — registered phones and connection state.
- `GET http://localhost:8100/screenshot` — base64 PNG in `value`.
- `GET http://localhost:8100/window/size` — the size WDA reports.
- `POST /api/devices/<udid>/remote/action` with `{"type":"home"}`. Other types: `lock`, `wake`, `unlock`, `tap`, `swipe`, `volumeUp`, `volumeDown`.
- Remote actions return `409` while a task runs.
- `home` on a locked phone fails with `device was not, or could not be, unlocked`. `unlock` needs the stored passcode.

## Run a task

```sh
curl -s -X POST http://127.0.0.1:3000/api/schedules \
  -H 'content-type: application/json' -H 'Origin: http://127.0.0.1:3000' \
  -d '{"deviceUdid":"<udid>","timing":{"kind":"now"},
       "task":{"pluginId":"com.git-agni.tiktok","taskType":"doomscroll","taskVersion":1,
       "payload":{"durationMinutes":3,"personality":"casual","likeEnabled":false,"saveEnabled":false}}}'
```

- `personality`: `skimmer`, `casual`, `engaged` or `dialed`.
- `durationMinutes`: 1 to 180.
- `timing.kind`: `now`, `once`, `daily`, `weekly` or `interval`.
- Poll `GET /api/executions` and `GET /api/executions/<id>`. The log is in `logs`.
- Stop a run with `POST /api/executions/<id>/stop`. The call returns `running` first. Poll until the status is `stopped`.
- Task types: TikTok `doomscroll`, `doomscroll-following`, `workflow-replay`, `post`, `pipeline-drain`. Instagram `doomscroll`, `doomscroll-following`, `cold-dms`, `post`. LinkedIn `cold-connect`, `connect`.
- Treat `post`, `cold-dms`, comments and `connect` as irreversible. See the gates in `SKILL.md`.
