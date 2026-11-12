---
name: agent-browser-consoles
description: "Drive real ad and cloud consoles with agent-browser. Use when browser-attach returns about:blank instead of attaching, synthetic clicks do nothing on React/Angular consoles, a chip input silently fails to save, Google Ads controls hide in shadow DOM, two buttons share one label, innerText disagrees with the screen, a setup gates on a legal attestation, or an OAuth app registers successfully and is still blocked."
---

# agent-browser-consoles

Drive real advertising and cloud consoles with `agent-browser`.
These traps are not obvious from the CLI help.
Each one cost several wasted turns to rediscover.

Applies to Google Ads, Meta Events Manager, Reddit Ads, LinkedIn, GA4,
Google Cloud Console, and the Spotify developer dashboard.

## 1. Confirm which browser you drive

`browser-attach` fails silently.
The daily Chrome runs without `--remote-debugging-port`.
Chrome accepts that flag at launch only.
`browser-attach` does not error.
It launches its own browser and returns a plausible `about:blank`.

Always confirm the process before you drive it:

```sh
lsof -nP -iTCP -sTCP:LISTEN | grep -i google   # pid + port
curl -s http://localhost:9334/json/list        # should show YOUR page
```

A listener on 9222 is not proof of a DevTools endpoint.
One such listener answered `404` for `/json`.

## 2. Use the clone as the working route

Run `~/.agent-browser/bin/browser-clone-setup.sh personal`.
Then launch real Chrome on `~/.agent-browser/real-profiles/personal` with `--remote-debugging-port=9334`.
The clone is read-only on the source profile.
It is idempotent.
It carries live Google, Meta Business, LinkedIn, and Reddit sessions.
It needs no browser restart.

See [agent-browser-profiles](../agent-browser-profiles/SKILL.md) for the
`AGENT_BROWSER_AUTO_CONNECT` setting and the isolated-profile-vs-clone
tradeoff this step builds on.

## 3. Prefer snapshot refs over synthetic DOM events

Synthetic DOM events do nothing on React/Angular consoles.
On Reddit Ads signup dropdowns, `element.click()`, the native value setter plus `input`/`change` events, and a full dispatched `pointerdown/mousedown/mouseup/click` sequence all failed silently.
The value never changed.
No error was raised.
Only `agent-browser click "@ref"` against a ref from `agent-browser snapshot` worked.
Use refs for anything that must actually commit.

## 4. Pierce shadow DOM in Google Ads

Google Ads renders inside shadow DOM.
`document.querySelectorAll` cannot see its controls.
`agent-browser click "text=View token"` reports the element does not exist, even when the text appears in `document.body.innerText`.
Walk through shadow roots:

```js
function walk(root, out){
  var els = root.querySelectorAll('*');
  for (var i=0;i<els.length;i++){
    var e = els[i];
    if (e.shadowRoot) walk(e.shadowRoot, out);
    if (e.children.length===0 && /view token/i.test(e.textContent||'')) out.push(e);
  }
  return out;
}
```

## 5. Read the page before clicking a button by its label

Meta's Conversions API setup has two buttons both labelled "Generate access token".
One sits inside a Dataset Quality API modal.
One sits below the "without Dataset Quality API" radio.
The modal path is irreversible.
It states that once a dataset is configured for Quality API, opting out is not available.
It preselected a different dataset than the one open in the list.
Anchor on the surrounding control.
Assert the target id before any click that commits.

## 6. Screenshot when text parsing disagrees with reality

Several times `innerText` said one thing and the rendered page said another.
A stale currency value.
A dialog that looked closed.
Take one screenshot.
It resolves each case faster than more `eval` calls.

## 7. Stop at attestations

Never make a legal statement on the operator's behalf.
GA4's Measurement Protocol panel gates on "I have the necessary privacy disclosures and rights from my end users".
Reddit's signup gates on a similar statement.
An agent cannot truthfully assert that.
Detect the attestation.
Stop.
Name the exact click the owner must make.
Reddit's currency choice is similar: it "cannot be changed after sign up", so ask rather than default.

## 8. There is no `mouse click`; compose it

When refs and shadow-piercing both fail, fall back to a real pointer.
`agent-browser mouse click` does not exist — the subcommands are `move`, `down`, `up`, `wheel`.
Compose the click, using coordinates read from the element itself:

```sh
agent-browser eval "(function(){var e=/* find it */; var r=e.getBoundingClientRect();
  return Math.round(r.x+r.width/2)+' '+Math.round(r.y+r.height/2);})()"
agent-browser mouse move <x> <y>
agent-browser mouse down
agent-browser mouse up
```

This opened a Meta collapsible that ignored `element.click()` and had no snapshot ref.

## 9. Curly apostrophes break text selectors

`agent-browser click "text=Confirm your server's events..."` fails when the page uses `’` (U+2019)
rather than `'`. The failure reads as a missing element, not an encoding problem.
Match on a substring that stops before the apostrophe, or find the node by regex in `eval`
and click it by coordinates.

## 10. Chip inputs do not commit on a synthetic Enter

Google Cloud Console takes emails as chips. Test users, and the developer
contact on the Branding page, both use one.

Setting `input.value` and dispatching `input` does not create a chip. A
dispatched `KeyboardEvent` for Enter does not either. The field looks filled.
The Save button may even enable. Nothing persists.

Type real keystrokes and end with a comma:

```sh
agent-browser click "@e67"
agent-browser type "@e67" "someone@example.com,"
```

**Always reload and re-read after Save.** The console shows the value you typed
whether or not it saved. On the Audience page the grid read `No rows to
display` after three separate saves that all looked successful.

This is section 3 again, in a harder form: the write appears to work.

## 11. Google restricted scopes need a project of their own

Some APIs use restricted scopes. Google Health is one. Restricted scopes need
verification before an app in production may request them. An unverified app
returns `Error 403: access_denied` with "has not completed the Google
verification process".

Publishing status `Testing` exempts approved test users from verification. So
the personal-use route is Testing plus your own address as a test user.

**Do not flip an existing project to Testing.** A shared project usually
already runs other OAuth clients in production, and the switch breaks them.
Create a separate project instead:

```sh
gcloud projects create <id> --name="<name>"
gcloud services enable <service>.googleapis.com --project=<id>
```

Two costs to state up front. In Testing with an External app, refresh tokens
expire after **7 days**. And the consent screen refuses to work at all until
every required Branding field is set, which is where section 10 bites.

## 12. Verify the service id; the obvious name is often wrong

`gcloud services enable googlehealth.googleapis.com` returns PERMISSION_DENIED.
The service is `health.googleapis.com`. The error says "not found or permission
denied", which reads like an access problem rather than a wrong name.

Confirm the id from the console URL for the API's library page before trusting
a guess.

## 13. Deleting an OAuth client does not clear the list

Google soft-deletes OAuth clients. The confirm dialog links to "deleted
credentials". After confirming, the client still appears in the Clients grid on
reload.

Do not read that as a failed delete and retry. Check the deleted-credentials
view instead.

## 14. Registering an app can succeed and still leave you blocked

Spotify let the app be created, then refused every Web API call: the owner
needs Premium. The checkbox for Web API was disabled at creation time, which
was the only signal, and it is easy to miss.

Read the app's status page after creating it. Do not treat "created" as
"working".

Spotify also stopped accepting `localhost` in a redirect URI. Use
`http://127.0.0.1:<port>/callback`.

## 15. Match headed vs headless to whether a human is in the loop

agent-browser defaults to headless (`headless=new`). No window is drawn. That
is correct for the common case: reading a page, extracting data, downloading a
file, a background sync. A human is not needed, so a window is waste.

It is wrong the moment a person must see or touch the page:

- a login form they complete
- a passkey or Touch ID prompt (a passkey cannot be replayed by the agent; the
  person authorises it at the machine)
- a 2FA, SafeKey, or one-time code
- a CAPTCHA or a "prove you are human" interstitial
- any step where the user is watching and will click

Run those headed: `--headed`, or `AGENT_BROWSER_HEADED=1`. A headless run of a
login task strands the user — they are told to "log in in the window" and there
is no window. That failure is silent; nothing errors.

Confirm the mode before handing off. `ps aux | grep 'headless=new'` must return
nothing for a headed session. `osascript -e 'tell application "Google Chrome"
to count windows'` should be non-zero. Do not trust the `--headed` flag alone;
a stale headless process from an earlier run can still be driving the tab.

Rule of thumb: if the next sentence to the user is "do X in the browser," it
must be headed first.

## 16. Facebook's Page editor

The Page editor has its own traps: a welcome dialog that blocks clicks, a
session left acting as a Page after a failed run, and a picture endpoint that
reports a silhouette for a real photo. See
`local-business-profiles/references/page-trust.md`, section 3.
