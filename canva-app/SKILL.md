---
name: canva-app
description: "Use when building or submitting a Canva app on the Canva Apps SDK: exporting the design, calling an external API, and working out why the Developer Portal will not let you submit to the App Marketplace."
---

# Building and submitting a Canva app

A Canva app is a **React app that runs in an iframe inside the Canva editor**, built on the
**Canva Apps SDK** (`@canva/app-ui-kit`, `@canva/design`, `@canva/intents`, `@canva/platform`).
It is a thin frontend over your own API: the SDK gives you the design content and the UI kit,
you supply the logic. The command-level playbook is in `itsryanarmani/scripts`
`scripts/canva-app/README.md`.

## When to use

- **Triggers:** 'build a Canva app', 'Canva Apps SDK', 'export the Canva design', 'publish to the Canva App Marketplace', 'Canva app review rejected', 'Canva translation required'.
- Submission needs an uploaded JSON of translated UI strings (an empty one is rejected), so every string goes through react-intl. Portal forms save on blur and silently revert the last field.
- Canva's eslint plugin forbids raw <img> and <input>; scopes must match the SDK calls; the final gate is a legal attestation and ID documents only the account owner can complete.
- Siblings: figma-plugin, adobe-express-addon, shopify-app, connector-directory-submission.

## The gate that actually blocks submission: translations

**Canva will not accept an app for review until it uploads a JSON file of its UI strings for
translation, and it rejects an empty file.** This is the single most expensive thing to
discover late, because clearing it is not a config change — it is a pass over every screen.

So every user-facing string has to go through react-intl from the start:

- `<FormattedMessage defaultMessage description />` in JSX.
- `intl.formatMessage({ defaultMessage, description })` wherever a plain `string` is required
  — `Button` children, `placeholder`, `label`, `alt`, and any message you write into error
  state. The UI kit types several of these as `string`, so `<FormattedMessage>` will not
  compile there.
- Give every message a `description`. That is the translator note, and Canva asks for it.
- Interpolate with named ICU placeholders, not template literals: `"Scheduled for {when}"`,
  not `` `Scheduled for ${when}` ``. A translator has to be able to move the value.

`app-scripts extract-translations` generates the file with hashed ids. **Run it after `build`,
not before** — `build` cleans `dist/`, so generating first silently deletes the JSON.

Scaffolds ship `@canva/app-i18n-kit` and `react-intl` as dependencies and wrap the tree in
`AppI18nProvider`, which makes an un-internationalised app look wired up when it is not.
`extract-translations` reporting `0 messages` is the tell.

## Run Canva's own lint — it is the pre-review checklist

Install `@canva/app-eslint-plugin` and define `lint` and `format:check` scripts, then run
`npx @canva/cli@latest apps doctor`. Doctor runs those two scripts and **skips them silently
if they are undefined**, so a project without them gets a clean bill of health that means
nothing.

Two of the plugin's rules map straight onto rejection reasons:

- **`formatjs/no-literal-string-in-jsx`** — catches strings that never reached the
  translation file. Expect it to find several after a manual i18n pass; alt text, handle
  prefixes and loading states are easy to miss.
- **`react/forbid-elements`** — raw `<img>` and form `<input>` are disallowed by the design
  guidelines. Use the kit: `ImageCard` for thumbnails, `DateInput mode="datetime"` for a
  datetime field (there is no separate date+time pairing needed), `Avatar photo` for a small
  brand mark. Reach for `ImageCard` only where a card is the right semantics — it is a large
  selectable surface with hover affordances, wrong for a decorative logo.

Pin `eslint` to `^9`; the plugin peers on `^9.23` and will not resolve against 10. Its shared
config also pulls in `eslint-plugin-jest`, and `jest/no-deprecated-functions` fails to *load*
without a jest install to read a version from — turn that one rule off if the app has no tests.

Canva's config may also disagree with your repo's. It wants a loose `!= null`; a repo with
`eqeqeq: error` wants `!==`. Restructure to narrow on truthiness rather than picking a side.

## Intents decide where the app can appear — and one of them blocks release

An app registers **intents**: plug-in contracts that surface it on different Canva
surfaces. Three are stable and shippable:

| Intent | What it gets you | Surfaces |
|---|---|---|
| Design Editor | your panel inside the editor | Editor |
| Data Connector | pull live external data into a design (`getDataTable` + a selection UI) | Editor, Canva AI |
| Content Publisher | your platform as a native publish destination (`getPublishConfiguration`, settings UI, preview UI, `publishContent`) | Editor |

**URL Expander is a preview intent — enabling it makes the app unreleasable.** Canva's
docs are explicit: you cannot release a public app that uses a preview intent until it
is stable. Worse, `prepareUrlExpander` does not exist on the `latest` SDK at all — the
`asset` entrypoint is an empty `export {}` — it ships only under the `preview`/`beta`
dist-tag, which can be an *older* version than `latest`. So "just turn it on" means
downgrading the SDK **and** giving up public listing. Check `npm view @canva/intents
dist-tags` and grep the installed `.d.ts` for `prepare*` before promising an intent.

Register every intent **synchronously at load**, and do not render UI immediately.

Content Publisher hands you **URLs**, not bytes: each `outputMedia[].files[].url` is a
short-lived link you fetch yourself. Cache the created record against the submission
(settings + the exact file URLs) so a retry resumes at the publish step — Canva lets the
user retry, and a naive handler creates a duplicate every time.

## The SDK calls, and the scopes they do not need

Export the open design with **`requestExport`** from `@canva/design`. It opens Canva's own
export dialog and resolves to `{ status, exportBlobs }`:

- Handle the non-`"completed"` status — that is the user closing the dialog. Distinguish it
  from a failure; returning `null` for "cancelled" beats throwing an error you then parse.
- A multi-page design yields several blobs. Fetch each blob's `url` for its bytes.
- There is no synchronous "give me the PNG" getter. (`createRenditions` is the *Adobe Express*
  add-on API — different product, easy to conflate.)

**`requestExport`, `requestOpenExternalUrl` and `prepareDesignEditor` are all user-mediated
and need no scope at all.** The Scopes page lists things like brand kit and brand template
access; leave every one off unless you call it. Declaring an unused scope is a documented
rejection reason, and generic advice to "declare design read and asset upload" is wrong for
an export-and-post app.

Likewise the **Authentication** page is for third-party OAuth providers. An app that
authenticates by having the user paste your API key leaves it empty.

## What the current portal does and does not have

The nav is: Code upload · Intents · Scopes · Webhooks · Authentication · Compatibility ·
Security · Developer profile · Collaborators · App listing details · Testing instructions ·
App status.

**There is no allow-listed-fetch-domains field.** Older guidance treats that as the #1 trap;
the setting is not in the portal today, and Security is read-only identifiers (App ID and the
app origin, the latter being what you feed your backend's CORS policy). If a request from
inside the app fails, debug it as runtime CSP rather than hunting for a portal toggle that
does not exist.

**Compatibility** is where reach is decided: `Public` vs restricted to your team, Standard
format (usually locked on) vs Flexible format for variable-length designs like docs, and
Desktop-and-Mobile vs Desktop-only. Mobile is reviewed against a separate set of guidelines
— shipping a dense multi-tab panel as Desktop-only is the lower-risk first submission.

## Submission

Portal-review, free. There is no publish CLI; `@canva/cli` covers
`create/list/link/preview/doctor/migrate/config` only. Cap: **5 submissions per day**.

Order that avoids rework: bundle → translations → scopes/auth → compatibility → listing text
→ listing media → links → testing instructions → submit.

**Listing constraints.** App name ≤18 characters, short description ≤50, description ≤200.
No marketing claims ("the best", "most popular"), no acronyms or abbreviations, end each
sentence with punctuation, and no full stop on a single-sentence short description. They run
a spellcheck.

**Listing media.** Icon exactly 512×512 PNG, 1:1, full-bleed, **no alpha channel and no
rounded corners** — the rounded icon most brand kits ship as the app/PWA icon is precisely
what gets rejected, so render from a square unclipped source. Featured image 2400×1800 (4:3),
plus up to 2 additional. The guideline asks the featured image to show the app's **features,
outputs or UI** — a wordmark on a brand field satisfies the dimensions and misses the point;
a faithful mock of the app's own panel does not.

Stripping alpha needs a real rasteriser. `sips` renders SVG to PNG but always keeps an alpha
channel, and a JPEG round-trip adds visible artifacts to flat brand colour. Use sharp's
`.flatten({ background })`.

**Links.** Site, terms, privacy and support URLs. Curl all four first — a dead link is a
rejection, and the path you assume (`/terms-of-service`) is often not the one that is live
(`/terms`).

**Testing instructions.** Overview, steps, and login details. A reviewer starts with none of
your state, so auth has to be self-service in-app and the listing has to say so. For an
API-key app there is no email or password: put the key in the password field and explain in
"Additional details" that it is pasted on the app's connect screen. Issue a **sandbox key**
whose writes are simulated, so a reviewer exercising the flow cannot post to a real account
or incur a charge.

## The last three gates need the account owner

Submission stays blocked on items no developer can complete on someone else's behalf:

1. **Your details** — legal entity name, address, phone, identity documents, registration
   number.
2. **A compliance attestation** — a checkbox confirming the app complies with applicable laws,
   next to one confirming authority to sign legal agreements on behalf of the organisation.
3. **A public app walkthrough video link** — must play with no sign-in.

Budget for these separately. Everything else can be finished and verified first; these three
are a handoff, not a task.

## Portal quirks that each cost a round-trip

- **The forms save on blur, not on input.** Fill a field, move focus off it, wait for "All
  changes saved". Filling the last field in a form and navigating away reverts it to the
  placeholder — which then surfaces as "Provide a Description" on App status even though you
  typed one. Re-read every form after filling it.
- **File inputs clear themselves after the app reads them.** `input.files.length` returns to
  0 on a *successful* upload, so assert on the filename and "Saved" label in the UI instead.
  Treating 0 as failure sends you debugging a working upload.
- **The bundler does not typecheck.** `app-scripts build` succeeds over broken types. If the
  build script was ever wrong, `tsc --noEmit` has never run — expect a pile of real errors the
  first time it does.
- **`@canva/cli` has no `build` and no `start`.** Both live in `@canva/app-scripts`
  (`dev`, `build`, `extract-translations`). A `package.json` calling `@canva/cli apps build`
  looks plausible, fails, and hides every type error behind the failure.
- **Pin Node 20.** `app-scripts` declares `node>=22` but builds fine on 20, and the sibling
  marketplace CLIs (`vsce`, `ovsx`, Coda `packs`) segfault on 22+.
- **`apps config pull` needs `canva login`.** An interactive browser login, so `canva-app.json`
  cannot be fetched in an unattended run.

## Parity checklist (prove in a real Canva session before submitting)

export the open design · handle a cancelled export · handle a multi-page export · upload the
rendition · create the downstream action · surface success and error in the app UI ·
authenticate from a clean state · `extract-translations` emits every visible string.

## The portal autosaves, and its "saved" indicator lies

There is no Save button on the portal's settings pages. Two consequences that will burn you:

- **The "All changes saved" text is a page-global indicator, not per-field confirmation.**
  It can read "saved" while the field you just typed was silently discarded. The only
  trustworthy check is **reload the page and re-read the value**. Do this after every
  edit you care about.
- **The address input is an autocomplete, not a text field.** Free text is thrown away
  with "Please choose an address from the list or add an address manually". Use the
  **Add Manually** control — it is a *link*, not a `<button>` — and fill the structured
  subfields. Omitting the post code leaves the whole identity block invalid, which then
  silently blocks the compliance checkbox with no visible error.
- **The compliance checkbox issues no network request when clicked.** It is local state
  that is only persisted as part of the identity payload, so it cannot be driven
  reliably by automation — budget a human click for it.

## Developer verification publishes real PII

Before a public release the portal demands identity verification: legal name, email,
phone, address, and a **government-issued photo ID** (5MB cap). Canva states that on
release your **name, email, phone number and address are displayed in the Apps
Marketplace listing** to satisfy trader law (EU). Consequences:

- Register with a **business/registered address**, never a home address — this is
  public and permanent.
- Use a role address (`hello@`/`support@`) you actually monitor, not a personal mailbox,
  and never a separate employer's work address on a personal product.
- Choose Company vs Individual to match whatever entity your published privacy policy
  and terms already name, or the declaration contradicts your own legal pages.

## Related skills

- `adobe-express-addon` — the same "design → export → do something" shape; note its SDK uses
  `createRenditions`, which is the API most often misattributed to Canva.
- `figma-plugin` — same shape again, different sandbox rules.
- `connector-directory-submission` — the cross-marketplace submission router.
