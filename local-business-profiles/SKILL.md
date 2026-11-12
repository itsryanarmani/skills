---
name: local-business-profiles
description: "Create a Google Business Profile for a service-area business with no public address, and a Facebook Page for the same site: the screen-by-screen order, the traps that cost time on the first run (a prompt that links the new profile to an unrelated business, suggestion lists that cover the next field, a half-finished draft that comes back, a description Google rejects for a price or a URL, a verification step that asks for an address, a Facebook form that does nothing when the account is rate limited), the minimum Page trust setup before ads (profile photo, cover, bio, link, category, built with fb-page-polish), the eligibility check to do before running it over many sites, and the gbp-create script in itsryanarmani/scripts that runs the same steps. Use when a live site needs a local listing, when someone asks for a Google Business Profile or Facebook Page for a site, or after website-directory-submission for a site that serves a local area."
---

# local-business-profiles

A local listing gives a site one more place to be found. Creating one by hand
is about ten screens of clicks. Google documents a Business Profile API, but it
needs separate API access, so this skill drives the public sign-up screens. It
records the order and the traps so the next run goes fast. The `gbp-create`
script in `itsryanarmani/scripts` runs the same steps for Google.

## 0. Check eligibility first

Google lists businesses that meet customers in person or travel to them. Its
guidelines exclude online-only businesses. A site that only publishes
information is not a business Google will list, even if the form accepts a
service area. Google can suspend a profile that does not match a real, eligible
business.

Before you create anything, check each business against Google's current
guidelines for representing a business. Make one profile per eligible business,
not one per site. If a business already has a profile, claim that one and do not
create a second. Duplicates are prohibited.

For a fleet, do one business first. Wait until Google verifies or refuses it.
Only then do the next ones.

Do not make up an address. The verification screen says the address stays
hidden from the public and that post office boxes are not eligible. If the
business has no address it can use, stop at "Verify Later" and ask a person.

## 1. Prepare the packet once

One entry per eligible business. Keep the file outside any repo.

- **Name.** The name the site uses everywhere else.
- **Category.** Pick one of Google's own category names. It must match word
  for word, so type a few letters in the form first and copy what Google offers.
- **Website.** The production `https://` address.
- **Service areas.** Place names, such as a city and province.
- **Description.** Plain text, 750 characters at most. No URL, no domain name,
  no price and no phone number. Google rejected one text that had a price and
  a URL. It does not say which part it dislikes, so leave all of them out.

## 2. Google Business Profile, screen by screen

Use a Chrome that is signed in to the right Google account, driven with
agent-browser. Open `https://business.google.com/create`.

| Screen | What to do |
|---|---|
| Search ("Find and manage your business") | Some sessions start here. Click "Add your business to Google". |
| Confirm your business | Google offers to link the new profile to a business the account already has. Choose "This profile is for another business". |
| Start building your Business Profile | Type the name. Check the suggestion list for an existing profile of this business (section 3). If there is none, take "Create a business with this name". Type the category and take Google's matching option. |
| Do you want to add a location customers can visit | Choose No. |
| Where do you serve your customers | Type each area and take the first suggestion. |
| Contact details | Add the website. Leave the phone empty unless the business has a public number. Click Next. Google creates the profile here. |
| Mailing address to verify | Choose "Verify Later" unless a person has a real address to give. |
| Hours | Skip unless the business has set hours. |
| Description | Paste the description. If the page does not move on, look for an "Invalid value" message by the field. With none, check the connection before you change the text. |
| Storefront photo, photos, Workspace offer | Skip. |
| Your edits will be visible once you're verified | Click Continue. |

After the last screen the profile exists and is hidden. The list at
`https://business.google.com/locations` shows it as Unverified. Verification
is a person's job. The options on offer depend on the account and the business.

## 3. Traps, and what to do

- **A suggestion list covers the next field.** The name field opens a list
  that sits over the category field. The options other than "Create a business
  with this name" are existing businesses. One of them may be this business.
  Look at them by hand. If one is this business, claim it and do not create a
  second profile. Never claim a business that is not yours. `gbp-create` stops
  when the list shows any other option.
- **The category list does not open.** The wizard keeps a half-finished draft.
  A reopened form can arrive with the category already set. Click "Clear
  category", then type again.
- **A click fails with "covered by".** A list is still closing. Wait one
  second and click again.
- **Element references change after every click.** Take a fresh snapshot
  before each action. Do not reuse a reference from an earlier screen.
- **A rerun can make a second profile.** Google does not warn about a
  duplicate name. Keep a ledger and save a "pending" entry before the click
  that creates the profile. Stop on a pending entry until a person has checked
  the list. `gbp-create` does this.
- **Stop on the first error.** A script that carries on after a failure
  can make a second profile.

## 4. Facebook Page

The form is `https://www.facebook.com/pages/create`. It has a name, a category
and an optional bio. Language School and similar categories appear in the list
as you type. Choose one and clear any stray text from the category box.

The Create Page button can do nothing, with no message in the page text that an
agent can read. In one run it was Facebook's rate limit. A person saw "You have
attempted to create too many Pages recently". The account already managed many
Pages, and the run had tried the button several times.
Do this instead:

1. Make one attempt. Take a screenshot. If the page did not change, stop.
2. Do not click again. More attempts may lengthen the block.
3. Open the Pages list and check that no duplicate was made.
4. Ask a person to click the button on a later day. The limit is a few new
   Pages per day. See [page-trust.md](references/page-trust.md).

Add the logo, the cover image, the About text and the website link after the
Page exists. Then link the Page from the site's `sameAs` data. That markup is
optional, but it ties the Page to the site.

Before the Page runs ads, give it the minimum trust setup: profile photo,
cover, bio, website link and category. Build them from the site's brand with
`fb-page-polish`. See [page-trust.md](references/page-trust.md).

## 5. The script

`gbp-create` in `itsryanarmani/scripts` runs section 2 for every entry in a JSON
spec.

```bash
gbp-create plan   specs/sites.json          # checks the spec, opens no browser
gbp-create create specs/sites.json "Example Site" --session <name>
gbp-create create specs/sites.json --session <name> --stop-before-submit
```

The spec is a JSON array of `{name, category, website, areas, description}`.
`plan` rejects a description with a URL, domain name, price or phone number.
`create` keeps a ledger next to the spec. It skips a finished name and stops on
an unfinished one. `--stop-before-submit` fills the screens before Google makes
the profile and stops one click before it. `--allow-similar` goes on when Google
lists businesses with a similar name. `gbp-create-e2e --session <name>` checks
the flow up to that click.

Run `create` on one profile first, and watch it. The screens after Google
makes the profile have been run by hand but not by the script's live test.

## 6. Done means

- The profile shows in the Business Profile list with the right name and area.
- It has no address on it.
- A person has finished verification, and the list shows it as Verified.
- If the site uses `sameAs` data, it links to the profile's public page, once
  that page exists.
