# Events and dedup

## One shared event id

Make the id once. Both sides must send the same string. Use one of two ways.

1. **Stable key.** When the event has a stable key, derive the id from it on both sides, such as `signup:<user id>` or `purchase:<order id>`. No id needs to travel in the request.
2. **Created once.** When no stable key exists, such as a lead with no account, make a random id once in the browser. Send it to the server in the request body. The server reuses it and never makes its own.

Never make a random or time-based id on each side separately. The two strings differ, and the platform counts two events.

## Exact field names

A wrong case means no dedup.

| Platform | Browser field | Server field |
|---|---|---|
| Meta | `eventID` | `event_id` |
| Reddit | `conversionId` | `conversion_id` |

- Use one closed list of event names. Share it between browser code and server code. A typo or a case change silently breaks dedup.
- Check dedup in each platform's test tool. Do not assume it works.

## Hashing and failure

- Lowercase and trim an email. Hash it with SHA-256 before it leaves the device or the server. Hash the external id too. Do advanced matching on the server. Raw personal data does not belong in pixel calls.
- Wrap each pixel call in its own `try`/`catch`. Log failures. Do nothing when the pixel is not loaded. One blocked pixel must not stop the others or break the page.
- Put a timeout on every server-side conversion call. A slow platform must not hold a serverless function open.

## First page view and pixels

- Send the first page view from the inline analytics init script. Do not send it from an effect that runs after hydration. Skip the first client-side mount. Fast ad bounces leave before hydration and record nothing.
- Load ad pixels as inline scripts that run before hydration, but only after the consent check passes. Use the same consent rule as [ad-conversion-hub](../../ad-conversion-hub/SKILL.md): no ad event without `measurement: true`, and no hashed identity without `ad_user_data: true`. Where the law needs opt-in, load no ad pixel before consent. Queue the first page view and send it after consent.

## Raw events

- Store raw events apart from daily totals. Raw rows support audit and replay. Totals feed dashboards.
- Dedupe by workspace, goal, visitor key and a time window.
- Add rate limits, bot filters and replay protection before you trust the numbers.
- Do not store direct personal data in raw rows. Prefer hashed or pseudonymous visitor keys. Define retention and deletion first.

## Offline conversion import

1. Key each upload by click id, conversion action and order id. One click can lead to repeat purchases or to several conversion actions. Send the time in UTC, in the platform's format. Set a unique order id per conversion action. Google's upload guide calls it the way to prevent duplicate imports, and it rejects repeats of the same order id.
2. Turn on partial failure. Map each error back to its row by index. One bad row must not block the batch.
3. Skip rows with no click id. Skip rows with a bad timestamp. Log both counts, so a skipped row is visible.
4. Use the conversion category your API version accepts. A generic value can be rejected where a specific one works. Enums change between versions. Record the version you tested, and run a dry run first.
5. Run the script as a dry run by default. See [reporting-and-launch.md](reporting-and-launch.md).
