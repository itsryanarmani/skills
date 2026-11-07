---
name: zapier-integration
description: "Build, validate, push, and submit a Zapier integration (a code CLI connector under integrations/zapier/) and get it accepted into the Zapier App Directory. Use when creating a new Zapier app, debugging one whose triggers/searches/actions 401 or return nothing, running zapier validate/push/promote, filling the Platform-UI review questionnaire, or figuring out why Submit-for-review is blocked. Covers the whole path plus the traps that each cost a round-trip: the imperative-auth beforeRequest bug (that validate can't catch), the exact-core-version pin, dropdown-must-be-a-trigger, search-needs-a-field, the CHANGELOG + Developer-ToS promote gates, and the real submission wall — every trigger/action/search needs a live tested Zap AND S001 needs 3 distinct real users with turned-on Zaps (unfakeable). Sibling of connector-directory-submission (that one is the cross-platform directory router; this is Zapier-deep). Verified end-to-end 2026-08 taking Content Rabbit's app to review."
---

# Building a Zapier integration

Zapier is **CLI-first**: the `zapier-platform-cli` (`zapier`) builds/pushes/submits a
connector whose source lives in `integrations/zapier/` (`index.js`, `authentication.js`,
`triggers/`, `searches/`, `creates/`). But the *submission* is NOT CLI-only — it's gated
on live-usage validation you satisfy in the browser. Read this before writing the first
file; command-level playbook is `itsryanarmani/scripts` `scripts/zapier/README.md`.

## The one bug that wastes a day: auth is imperative

**Zapier does not auto-attach the connection's auth to your requests.** Unlike Make (base
`authorization`), n8n (credential `authenticate`), or Pipedream (app `_makeRequest`) —
which attach auth declaratively — Zapier applies auth **only where you wire it**. The
`authentication.test` request you write to check credentials is *separate*; a header
hardcoded there does NOT authenticate your triggers/searches/creates.

Symptom: **connect succeeds, every real call 401s** (`"API key missing"`). It ships broken
for every user, and **`zapier validate` never flags it** (it checks structure, not live
calls). Wire it once, globally, in `index.js`:

```js
const addBearerAuth = (request, z, bundle) => {
  if (bundle.authData?.api_key) {
    request.headers = request.headers || {};
    request.headers.Authorization = `Bearer ${bundle.authData.api_key}`;
  }
  return request;
};
module.exports = { /* … */ beforeRequest: [addBearerAuth], /* … */ };
```

**Rule: after `validate` passes, run ONE real operational request (a Zap-editor Test)
before trusting the connector.** That's the only thing that catches missing auth.

Also: **don't add auth fields the API key already scopes.** If the key is bound to one
tenant server-side, a second "Account/Team/Workspace ID" field is dead weight — never
sent, only feeds the connection label. Ask for the key alone.

## Build → submit, the command sequence

```bash
cd integrations/zapier
zapier login                       # once per machine
zapier validate                    # 0 errors required
zapier register "<Title>" \        # creates app + writes .zapierapprc (gitignore it)
  --desc "<Name> is a …" \         # MUST start "<Name> is a" (M002); ≤140 chars
  --url "https://<homepage>" \     # REQUIRED flag or register drops to a broken prompt
  --audience global --role employee \  # role must be employee/contractor, NOT user (M003)
  --category <c> --yes
zapier push                        # bundle + upload as a version
zapier promote <version> --yes     # = submit-for-review (there is no `zapier submit`)
```

### Structural traps (each bounced a `validate`/`promote` run)

- **Core version EXACT, matching the CLI major.** `zapier-platform-core: "^16.0.1"` fails
  ("must depend on an exact version"). CLI 17.x → pin `"17.8.0"`. No `^`/`~`.
- **A dynamic ID dropdown must reference a TRIGGER, not a search (D005).** Make a **hidden
  trigger** (`display.hidden:true`) returning `{id,name}[]` and point `dynamic:` at it.
  Searches back *Find* actions; hidden triggers back dropdowns.
- **Every search needs ≥1 input field (D009).** Empty `inputFields:[]` fails — add a
  filter field and actually use it.
- **`register` needs `--url`** or an interactive prompt throws `ERR_USE_AFTER_CLOSE` under
  a pipe. It also **updates** an existing app when `.zapierapprc` is present + `--yes`.
- **`promote` requires a `CHANGELOG.md`** with a user-facing `## <version>` entry in the
  pushed source. Add it, `push` again, then promote.
- **Metadata gates:** description starts "`<Name>` is a…" (M002), role employee/contractor
  (M003), a **logo** (M004 — Platform-UI upload only, no CLI). Fix via `register` update +
  the UI.
- **U001 Developer-ToS:** promote pre-checks pass but fail on `meta.tos_agreement`; a human
  accepts the ToS once at `zapier.com/app/developer`. Then re-run.
- **`.zapierapprc`** links the dir to the app id — gitignore it with `.env`/`build/`.
- **Keep hard-coded API paths current** — a product API rename 404s every call silently.

## The submission wall (this is what actually blocks you)

Metadata + the questionnaire are necessary but **not sufficient**. Both `zapier promote`
and the Platform-UI "Submit for review" refuse until the app clears a list of blocking
**Publishing tasks** — and two kinds of them can't be cleared by writing code:

1. **A successful task per action (T001/T002/T004/T005 + S002).** Every trigger, search,
   and create must have produced ≥1 successful task. A zero-Zap app can't submit. **Clear
   it cheaply: a Zap-editor "Test" of each step satisfies it — NO publish/turn-on needed.**
   Connect the account once (a human pastes the key — agents are prohibited from typing
   credentials into fields — but it's one-time and every step reuses the connection), seed
   data via the product API so triggers poll and write-actions have targets, then build a
   **few** Zaps that chain many steps and Test each. (Click dropdown options by element
   **ref**, not coordinates — coord clicks silently no-op in Zapier's editor.)

2. **S001 — "at least 3 users with live Zaps" — is UNFAKEABLE.** It needs **3 distinct
   Zapier accounts**, each with a **turned-on (live)** Zap using the app that has run. One
   account's editor tests can NEVER clear it. This gates the Submit button (the CLI
   `promote` lists S001 in its failures too). So **solo automation cannot reach a
   submittable state** — plan for it up front:
   - Fastest controllable path: 3 people (separate Zapier accounts) open the **private-app
     invite link** (Sharing page → `zapier.com/developer/public-invite/<appId>/<token>/`),
     build one trivial Zap (e.g. New-record trigger → "Email by Zapier"), and **turn it
     on**. Share one throwaway API key for the connect.
   - Organic path: the in-product **Zapier embed** onboards real early users.
   - Triggers needing a real event to poll (e.g. "new webhook delivery") also may not
     clear by testing — expect 1–2 residual items and note them.

## The review questionnaire (Platform UI → Publishing, 5 sections)

Gates the Submit button; fill all, pick the version, tick confirm:
1. **Readiness & API ownership** — own-domain? No (if it's your API); production
   endpoints? Yes; users pay extra? usually No.
2. **Test account for reviewers** — Zapier **mandates the username be
   `integration-testing@zapier.com`** + a password. Passwordless (OTP) product: create
   that exact account (reviewers own that inbox → they receive the login code), set a
   throwaway password, and put the API key + connection id in Notes.
3. **App details** — publicly-launched, homepage, API-docs URL, a required primary color.
4. **Contacts** — dropdowns list only **integration-team admins**; add teammates via
   Manage team first if needed.
5. **Compliance** — company country, sensitive-values No, financial No, third-party-APIs
   (Yes if the product calls other platforms' APIs → then a required field naming the API
   owners + affirming permission), Zapier-branding No.

## Beta → public directory (the later gate)

Passing review lands the app in **Beta**. Public listing needs **50 active users AND ≥10
published Zap templates**, OR **a single in-product Zapier embed** (waives the 50-user
rule). Author the ~10 templates early — they double as the app page's flows showcase.
