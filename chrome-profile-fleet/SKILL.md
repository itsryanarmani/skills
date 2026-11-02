---
name: chrome-profile-fleet
description: "Run a fleet of Chrome profiles — one profile per online identity (work, personal, per-subscription, per-domain) — and wire each identity's mailbox into one primary Gmail. Covers safe Local State editing (browser fully quit, backup first), the process-name collision between real Chrome and bundled automation browsers, a naming convention that keeps the avatar picker unambiguous, the three mailbox shapes (hosted mailbox, routed alias, plus-alias), Gmail send-as through Google's own SMTP servers or a provider's own SMTP (app password vs api_token transports, SPF/DKIM alignment, why DMARC p=reject rejects unaligned send-as, and why sendAs.create is Workspace-only so consumer adds go through the UI), and Cloudflare Email Routing constraints (one rule per address, one action per rule, catch-all fallback, verified destinations). Use when separating browser identities, adding Chrome profiles from the CLI, consolidating several addresses into one Gmail, or deciding where a per-domain mailbox should land."
---

# Chrome profile fleet

One Chrome profile per online identity. Each profile keeps its own cookies,
sessions, sync, and saved state, so identities never mix. Typical identities:
a work account, a personal account, one profile per paid AI subscription, one
profile per product domain that has its own login surface.

Pair each profile with a mailbox the identity can use, and consolidate those
mailboxes into one primary inbox so mail never has to be checked in more than
one place.

## How profiles exist on disk

Chrome stores profile metadata in `Local State` inside the user-data
directory — on macOS `~/Library/Application Support/Google/Chrome/Local State`,
a single JSON file. `profile.info_cache` maps a directory name (`Default`,
`Profile 1`, `Profile 2`, …) to its display name, signed-in user, avatar, and
flags. The profile itself is a directory next to it (`Profile 3/`) that Chrome
populates on first use.

Two consequences:

- A profile's display name lives only in `Local State`. Signing in with a
  Google account later overwrites it with the GAIA name — sign-in after
  naming, not before.
- `is_using_default_name` must be `false` on entries you name, or Chrome
  treats the name as auto-generated and free to replace.

## Safe-edit rules for Local State

1. Back up `Local State` before touching it.
2. Quit the browser completely. A running Chrome holds `Local State` in
   memory and rewrites it on exit — edits made while it runs are silently
   clobbered.
3. `pgrep "Google Chrome"` is not proof the browser is down. Bundled
   automation Chromes (agent-browser, Chrome-for-Testing, E2E runners) share
   the process name but use their own user-data dirs — they can stay running.
   Filter by the real app path (`/Applications/Google Chrome.app` on macOS).
4. Add the `info_cache` entry and create the empty profile directory, then
   relaunch and re-read `Local State` to confirm the entry survived.

A graceful quit (`osascript -e 'tell application "Google Chrome" to quit'`)
can stall on a confirm dialog or unsaved state. A terminated main process
leaves the crashed-exit flag set, and the next launch shows the "Restore
pages?" infobar — which is also the reliable way to get all tabs back when
"Continue where you left off" is not set.

Open one profile from a shell:

```sh
open -na "Google Chrome" --args --profile-directory="Profile 3"
```

## Naming convention

`Purpose (email)` — for example `Work (person@corp.com)` or
`Claude 2 (person@product.io)`. The email in parentheses makes the avatar
picker unambiguous when several profiles belong to the same person. This
matters most for subscription profiles, where the distinguishing feature of
the profile is which account's session it holds.

## The three mailbox shapes

Each identity needs a mailbox. They come in three shapes, and the shape
decides what "receive in one inbox" means:

- **Hosted mailbox** (Zoho, Fastmail, hosted-provider webmail): a real
  account with a login. To consolidate, set forwarding inside the provider's
  settings, or use Gmail's "Check mail from other accounts" (POP3) if the
  plan allows POP3 — free tiers often disable it.
- **Routed alias** (Cloudflare Email Routing or equivalent): no mailbox at
  all — an MX-level rule sends mail to a destination or a Worker. To
  consolidate, change the rule's action to forward to the primary inbox. To
  consolidate *and* keep the worker copy is impossible — see the one-rule
  constraint below.
- **Plus-alias** (`name+tag@gmail.com`): not a sign-in identity. Mail lands
  in the base Gmail automatically; send-as works with the base account's
  SMTP credentials; verification codes come straight back to the same
  inbox. This is the cheapest extra identity that exists.

## Gmail send-as recipe

Two transports work; pick per domain.

**Option A — Google's own servers.** No per-domain SMTP account required:

1. Create a Gmail **app password** on the primary account
   (`myaccount.google.com/apppasswords`, requires 2FA).
2. Authorize Google's servers on the alias domain: add
   `include:_spf.google.com` to the domain's apex SPF record.
   Gmail's send-as puts the alias in the envelope-From, so receivers check
   the alias domain's SPF against Google's IPs.
3. This step is not optional on strict domains. If the alias domain
   publishes `p=reject` DMARC, a send-as message whose SPF and DKIM are both
   unaligned gets rejected outright. The SPF include is the only alignment
   available — consumer Gmail cannot DKIM-sign with the alias domain.
4. SMTP server `smtp.gmail.com`, port 587, username = the primary Gmail
   address, password = the app password.

**Option B — the domain's own provider SMTP.** Better deliverability when
the provider signs domain DKIM. Example for Cloudflare Email Service:
`smtp.mx.cloudflare.net`, port 465 SSL, username is the literal string
`api_token`, password is an API token with the Email Sending permission.
The domain must be onboarded for sending — the tell is a
`cf2024-1._domainkey` TXT on the zone (the account-wide sending DKIM key;
copy it from any onboarded zone if missing). Aligned DKIM + aligned SPF
satisfies `p=reject` DMARC with no Google SPF include needed.

Either way:

5. Gmail → Settings → Accounts and Import → Send mail as → Add another
   email address, fill the SMTP fields, submit.
6. Google emails a verification link to the alias. It must land somewhere
   you read — a forward rule, a hosted mailbox you can open, or a worker
   inbox you can query. Have that path ready before clicking verify.

**API caveat:** `users.settings.sendAs.create` is restricted to Workspace
accounts with domain-wide delegation — on consumer Gmail the call fails
with `Access restricted to service accounts`. List/get work on any
account, so CLI tools can verify state but cannot create aliases; the add
flow must go through the Gmail UI (automatable with a browser agent: the
popup fields are `cfn`=name, `cfa`=email, `cfss`=server, `cfsp`=port,
`cfsl`=username, `cfsw`=password).

## Cloudflare Email Routing constraints

When aliases route through Cloudflare Email Routing:

- **One rule per address.** Creating a second rule for the same recipient
  fails with `Duplicated Zone rule`. A single address cannot both forward
  and trigger a Worker — pick one action per address.
- **One action per rule.** The `actions` array accepts exactly one entry
  (`forward`, `worker`, or `drop`). Dual delivery needs a Worker that calls
  `forward()` itself, not two rules or two actions.
- **Catch-all is a fallback.** It applies only when no custom rule matches.
  Changing one address's custom rule does not affect other addresses.
- **Destinations must be verified.** A forward rule can only target an
  address already verified under the account's Email Routing destination
  list.
- **Subaddressing falls back to the base rule.** `name+tag@domain` resolves
  via the `name@domain` rule — you cannot give a plus-alias a different
  action.
- Changing a rule is a one-call `PUT` with the rule id; flipping the action
  back is equally cheap, which makes per-alias receive-destination changes
  a routine operation.

## A send-as alias can go stale and still look verified

Gmail stores the SMTP password inside each alias. If the provider token
rotates, or the alias still points at an old provider, Gmail keeps listing it
as verified. The first real message bounces with
`535 Authentication credentials invalid`, and the bounce arrives in about 45
seconds.

Test every alias with a real message, not with the settings page. Send one
message from each alias to your own inbox and search for a bounce from
`mailer-daemon`. Fix a stale alias with Settings, Accounts and Import, edit
info, then re-enter the server, port and password. Never trust the "verified"
status alone.

## Watch out

- A domain that routes through Cloudflare can still have a *different*
  outbound sender set (Email Service Workers, an ESP). Adding Google's SPF
  include is additive — keep every existing `include:` and the terminal
  `all` mechanism.
- SPF records returned by the Cloudflare API may come back wrapped in
  literal quotes (`"v=spf1 ..."`). Match on the unquoted content or the
  record looks missing and you patch nothing.
- The MX destination and the SPF authorization are unrelated: mail can land
  at a hosted provider while Google is authorized to send for the domain.
- Email verification codes are the easy part to forget — decide where the
  code lands before adding the send-as, not after.
