---
name: affiliate-network-signup
description: "Sign up to affiliate networks such as Awin, CJ and Impact by browser automation, for one owner and many sites. Use when you apply to an affiliate network, a signup form reports an error the site may not deserve, a legal Accept button stays disabled, a login page drops the browser tool's connection, a network says the email already has an account, or two-step verification shows only a QR code. Not for a second legal entity or a second payout currency, which can need its own account."
---

# affiliate-network-signup

Open one account per network and use it for every site the owner has. A signup
form asks for one site URL. Give it one live site. Add the others inside the
account after approval. The exception is a separate legal entity or payout
currency: that can need its own account, so ask the owner.

This skill covers Awin, CJ and Impact, because an agent has signed up to each.
Do not add steps for a network nobody has logged in to.

For the browser itself, use [agent-browser-profiles](../agent-browser-profiles/SKILL.md)
and [agent-browser-consoles](../agent-browser-consoles/SKILL.md). This skill
adds only what is specific to affiliate networks.

## Ask the owner first

- Legal name, country, mailing address, phone number.
- Which live site to apply with.
- A yes for each legal agreement you will accept for them. Record it. A yes for
  one network does not cover the next.

Never invent an identity field.

**Stop at any page that asks for a bank, tax or ID number.** Hand the page to
the owner. You may enter these values only when the owner has told you to, and
only when they reach you through a secret input that never shows in chat or in a
log. Never take them from a chat message.

## Order of work

1. Search the owner's mailbox for the network's name. An old account on the same
   email is common. Impact answers "Looks like you've already signed up with
   this email". Sign in to the old account and read what it needs, such as a
   payout warning. Do not reset its password without the owner's yes: the reset
   breaks the password the owner saved.
2. Use a clean automation browser with its own profile for logins. An
   extension-driven browser attached to the owner's Chrome dropped its debugger
   on login pages. Each call then failed with `Target page, context or browser
   has been closed`.
3. Generate one password per network. Store it in a mode 600 file that Git
   ignores. Never print it. To give it to a person, point to the file. A
   clipboard copy also reaches clipboard history and, on macOS, the owner's
   other devices, so clearing it after two minutes does not remove every copy.
4. Fill one step at a time and wait. A slow network took 15 to 25 seconds per
   step. Read the page again before you click a second time.
5. Verify each email from the mailbox: search by sender and the last ten
   minutes, then open the link without printing it.
6. Turn on two-step verification before the owner enters payout details.
7. Add the owner's other sites inside the account.

## The gates, per network (verified November 2026)

| Network | Gate | What cleared it |
|---------|------|-----------------|
| Awin | Company name of three or more characters | An individual used their own name. |
| Awin | A primary promotional type and at least one sector | Mark one type as primary. Tick a sector. |
| Awin | "The URL needs to be publicly accessible" | See [A false error](#a-false-error-is-not-proof-the-site-is-blocked). |
| CJ | reCAPTCHA v2 checkbox | One click passed with no image challenge. |
| CJ | Three legal Accept buttons, disabled | After the owner's recorded yes, open each agreement's link. The button then enabled. |
| CJ | Sign-in page after the agreements | Sign in by hand, or use the clean browser. |
| Impact | A required phone number | Ask the owner. |
| Impact | Password rule: at least eight characters, a digit, one of `! @ # $ % & ?` | Generate to the rule. |

## A false error is not proof the site is blocked

A form can say a URL is not publicly accessible while the site returns 200 to
every client you try. Do not edit firewall rules or the site on that message.
Check three things first:

1. The URL format. Try the scheme, the `www` form and a trailing slash.
2. The CDN's security or firewall events for the attempt window, as well as its
   request log. A blocked request can show in one and not the other, and full
   request logs can need a paid plan.
3. Whether a request from the network arrived at all. Filter out your own
   network and the CDN's own traffic, then look for a row.

In one recorded run, no request arrived, and the owner's own click on the same
form passed. A score check on the automated browser is the likely cause there.
It is a likely cause, not a rule. If a real request was blocked, fix that.

Check that the log can see a positive case before you trust an empty result.
Request a page yourself and find your own row.

## Two-step verification that shows only a QR code

Awin showed this: an email link, then a QR code with no text secret.

1. Request the setup email. Open its link in the clean browser.
2. Screenshot the QR code. Do not open or view the image: it holds the secret.
3. Decode it and pipe the `otpauth://totp/` URI straight into the `totp` helper
   from the [scripts repository](https://github.com/itsryanarmani/scripts/blob/main/totp):
   `totp save accounts.env PREFIX`. On macOS the Vision framework reads QR
   codes.
4. Delete the screenshot.
5. Enter `totp code accounts.env PREFIX` in the one-time code box.
6. Save the recovery code in the same file before you confirm that you saved it.

The secret is the account. Keep the file out of Git, out of chat and out of
logs.

## Check each stage yourself

A tool that prints `Done` has not proved anything. Treat a stage as passed only
when you see its effect:

- Signup: the network's approval email, or a signed-in dashboard heading.
- Email: the confirmation page, not the click.
- Agreements: each one reads Accepted.
- Two-step verification: the code box accepts a fresh code and a recovery code
  page follows.
- A site added: it appears as a heading in the account's site list.

## Stop and report

Stop when a page asks for a bank, tax or ID number, when a legal agreement has
no recorded yes, when a CAPTCHA has an image challenge and the owner is away,
or when the network says an account exists and you have no sign-in. Say what
the page asks for and what you need.
