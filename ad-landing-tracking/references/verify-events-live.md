# Verify pixel and server events on a live page

An automated check that shows zero pixel events can be wrong. Prove the
instrument can see a positive case first.

## Why an automated browser sees nothing

- The pixel sends nothing when `navigator.webdriver` is true.
- A tracker blocker or a privacy extension also stops it.
- So a default headless run shows zero events, even when the page works.

## A clean check

1. Start a clean headless profile with no extensions.
2. Launch with `--disable-blink-features=AutomationControlled`.
3. Override `navigator.webdriver` to `false` before any page script runs.
4. Load the page. Set the consent cookie in the page, then reload. Use the
   site's real consent cookie name and value.
5. Capture every request to the pixel endpoint. Record the event name and the
   event id.
6. Submit the form with a fake lead. Record the event id the server returns.
7. Pass when the browser Lead id equals the server id. Save the names, ids and
   statuses in a JSON file. Do not save tokens or personal data.

## Dedup

- The platform merges a browser and a server event only when the event name
  AND the event id are the same.
- The server sends `Lead` only on a first sign-up. It returns the event id.
  It uses the id the browser sent, if any, or a stable key. See
  [events-and-dedup.md](events-and-dedup.md).
- The browser fires its copy of `Lead` only when the server returned an id.
  A repeat sign-up returns no id, so neither side sends a second Lead.

## Reporting lag

- The ads overview and the pixel stats lag by hours, up to a day.
- A server test event shows in Test Events only while a test session is open.
- So plan the platform check for the next day. In the same-day report, list
  what is proven (requests sent, ids match) and what is not (the platform
  received and merged them).
