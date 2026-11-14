---
name: affiliate-network-signup
description: "Sign up to affiliate networks such as Awin, CJ and Impact by browser automation, for one owner and many sites, without false errors, dead buttons or lost logins. Use when you apply to an affiliate network, a signup form reports an error the site does not deserve, a legal Accept button stays disabled, a login page drops the browser tool's connection, a network says the email already has an account, or two-step verification shows only a QR code."
---

# affiliate-network-signup

Open one account per network and use it for every site the owner has. A signup
form asks for one site URL. Give it one live site. Add the others inside the
account after approval. Do not open a second account because a second site
exists.

This skill covers Awin, CJ and Impact, because an agent has signed up to each.
Do not add steps for a network nobody has logged in to.

## Ask the owner first

- Legal name, country, mailing address, phone number.
- Which live site to apply with.
- A yes for each legal agreement you will accept for them. A yes for one network
  does not cover the next.

Never invent an identity field. Never enter a bank, tax or ID number. Stop at
those pages and ask the owner to enter them or to give you the values.

## Order of work

1. Search the owner's mailbox for the network's name. An old account on the same
   email is common. Impact answers "Looks like you've already signed up with
   this email" and the old account can hold a payout warning. Sign in to it.
   Do not reset its password without the owner's yes: the reset breaks the
   password the owner saved.
2. Use a clean automation browser with its own profile for logins. An
   extension-driven browser attached to the owner's Chrome drops its debugger on
   a login page when a password manager adds a frame. Every call then fails
   with `Target page, context or browser has been closed`.
3. Generate one password per network. Store it in a mode 600 file that Git
   ignores. Never print it. To give it to a person, put it on the clipboard and
   clear the clipboard after two minutes.
4. Fill one step at a time. Take a snapshot, fill by reference, confirm the
   next button is enabled, click, then wait. A slow network takes 15 to 25
   seconds per step. Read the page again before you click a second time.
5. Verify each email from the mailbox: search by sender and the last ten
   minutes, then open the link without printing it.
6. Turn on two-step verification before you enter payout details.
7. Add the owner's other sites inside the account.

## The gates, per network

| Network | Gate | What clears it |
|---------|------|----------------|
| Awin | Company name of three or more characters | An individual uses their own name. |
| Awin | A primary promotional type and at least one sector | Mark one type as primary. Tick a sector. |
| Awin | "The URL needs to be publicly accessible" | See [A false error](#a-false-error-is-not-a-reason-to-change-the-site). |
| CJ | reCAPTCHA v2 checkbox | One click passed with no image challenge. |
| CJ | Three legal Accept buttons, disabled | Open each agreement's link first. The button then enables. |
| CJ | Sign-in page after the agreements | Sign in by hand, or use the clean browser. |
| Impact | A required phone number | Ask the owner. |
| Impact | Password rule: eight characters, a digit, one of `! @ # $ % & ?` | Generate to the rule. |

## A false error is not a reason to change the site

A form can say a URL is not publicly accessible while the site returns 200 to
every client you try. Do not edit firewall rules or the site on that message.
Read the zone's request log for the attempt window, filter out your own network
and the CDN's own traffic, and look for a request from the network you are
applying to. If none arrived, the site was never blocked. The score check
behind the form is the likely cause, and a person's click passes it. Ask the
owner to click the button once.

Check that the log can see a positive case before you trust an empty result.
Request a page yourself and find your own row.

## Two-step verification that shows only a QR code

1. Request the setup email. Open its link in the clean browser.
2. Screenshot the QR code and decode it to an `otpauth://totp/` URI. On macOS
   the Vision framework reads QR codes. Write the URI to a private file.
3. Store the secret with the `totp` helper from the public scripts repository:
   `totp save accounts.env PREFIX < uri.txt`. Delete `uri.txt`.
4. Enter `totp code accounts.env PREFIX` in the one-time code box.
5. Save the recovery code in the same file before you confirm that you saved it.

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
