---
name: monday-app-submission
description: "Drive a monday.com app from created to marketplace-submitted through the monday Developer Center UI. Use when you need to edit an existing monday app's branding (name, icon, app color), promote a version, generate the shareable install link, or fill the marketplace submission form. Carries the traps that cost real time and are not in monday's docs: the app management URL only works in its long form (a bare /apps/manage/<appId> looks like a wrong app id but is not), a Live version is locked so branding changes require a New version draft, the icon crop dialog opens zoomed in and silently crops square logos, the submission form is a ~25-field workform in an iframe where Demo Link and How-to-use Link are required, and renaming the account URL logs out every user including your automation session. Sibling of monday-app (the build path). Triggers: 'submit monday app', 'monday marketplace submission', 'monday app version locked', 'monday Developer Center', 'monday install link', 'monday app icon cropped', 'monday promote to live'."
---

# Submitting a monday.com app through the Developer Center

The build path (view, OAuth, hosting) is the `monday-app` skill. This skill is
the part that happens in the monday **Developer Center** UI once the app exists:
editing branding, versioning, the install link, and the marketplace submission
form. Everything below was verified by hand in the Developer Center; none of it
is in monday's docs.

Companion script: `itsryanarmani/scripts` `scripts/monday-app/check-app.mjs` —
verifies the install link and the reviewer credentials from the CLI before you
submit.

## 1. The app management URL only works in its long form

The app management URL must be the full form:

```
https://<account>.monday.com/apps/manage/<appId>/app_versions/<versionId>/sections/<section>
```

A bare `/apps/manage/<appId>` returns "We couldn't find the content you were
looking for". That error looks like a wrong app id, but it is not: the app id is
fine, the URL is just too short. If you are driving the Developer Center with a
browser agent, always navigate to the full URL (appId + versionId + section).

## 2. A Live version is locked; edit through a new Draft

Once a version's status is **Live**, its branding fields are read-only: Name,
Short description, App color, and the icon. You cannot edit them in place.

To change anything:

1. Click **New version**. This creates a **Draft** you can edit freely, while
   the old Live version keeps serving existing users.
2. Make your edits in the Draft.
3. Click **Promote to live**. The new version becomes Live and is itself
   locked. Repeat the cycle for the next change.

## 3. The icon crop dialog opens zoomed in

The app icon is uploaded through a **"+ Add app icon"** control that opens a
crop dialog with a zoom slider (an `input[type=range]`). The dialog opens
zoomed **in**, so a square logo gets cropped to its centre and you ship a
cropped icon without noticing. Move the slider to its **minimum** before saving.

**App color is a separate field from the icon.** Changing one does not change
the other. If both are wrong, fix both.

## 4. Renaming the account URL logs everyone out — do it last

Renaming the account URL (Administration > General > Profile) **logs out every
user in the account**, including your automation/browser session. If a clean
URL matters (e.g. the account is `somethingrandom.monday.com` and reviewers
will see the domain), do the rename **last**, after any submission is finished,
and be ready to log back in and re-authenticate any agent session. monday
redirects the old URL for 30 days.

## 5. The submission form: a ~25-field workform in an iframe

The marketplace submission form is a **monday workform rendered in an IFRAME
inside the Developer Center**, not a separate page. If you are driving it with
a browser agent, you must reach into the iframe's document; the parent page's
DOM does not contain the fields.

It has roughly **25 fields**, far more than the 9 commonly documented.
Required fields include:

- Entity Website
- Technical Point of Contact
- Business Point of Contact Email
- Support Address
- App Short Description
- App Long Description
- Keywords
- App Features
- "Does your APP contains AI capabilities?"
- Value Proposition and Use Cases
- Feature Names
- Categories
- OAuth Scopes
- Personal Data Use
- Privacy Policy
- Terms of Service
- Pricing Model
- Installation Link
- App ID
- How to use Link
- Demo Link
- Credentials for review purpose

**The Demo Link and the How-to-use Link are REQUIRED.** A demo recording cannot
be produced at the end of the session on demand — **record the demo before you
start filling the form**, and have the how-to-use URL ready. Do not open the
form until both exist.

## 6. The install link and confirming a client id is live

The shareable install link is:

```
https://auth.monday.com/oauth2/authorize?client_id=<clientId>&response_type=install
```

The **Client ID is on the General settings page** of the app in the Developer
Center.

You can confirm a client id is actually live without a browser: follow the
install URL with redirects disabled and assert the response is a **302** whose
`oauth_payload_token` is a JWT whose payload decodes to that same client id.
This is exactly what `check-app.mjs` (companion script, above) does.

## 7. Test the reviewer credentials immediately before submitting

Reviewers need **working credentials** (the "Credentials for review purpose"
field). A previously working key had **expired silently between sessions**.
Test the key immediately before submitting — not at the start of the session,
not yesterday. `check-app.mjs` does this too (asserts `GET /posts` and
`GET /accounts` return 200 with the bearer key).

## Sequence that avoids the traps

1. App exists and is Live; you need branding changes.
2. Click **New version** (Draft).
3. Upload the icon; move the zoom slider to minimum before saving. Set App
   color separately. Fix Name and Short description.
4. Verify the Client ID on the General settings page; run `check-app.mjs`
   against it.
5. **Record the demo video and write the how-to-use page** — required form
   fields.
6. Test the reviewer API key; paste it into the form.
7. Fill the ~25-field workform inside the iframe (see the field list above).
8. Submit; re-check the shared review board.
9. **Only now**, if you still want it, rename the account URL — it logs out
   everyone, including you.

## Related skills
- `monday-app` — the build path: board/item view, monday apps SDK, OAuth/session
  token vs your API key, the submission form's documented rules.
- `canva-app` — sibling marketplace playbook with the same verify-by-reload
  discipline for portal UIs that autosave.
