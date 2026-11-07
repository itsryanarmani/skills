---
name: registrar-transfer-to-cloudflare
description: "Transfer a domain from Namecheap to Cloudflare Registrar end to end from the CLI: zone and DNSSEC preconditions, privacy off and unlock through the Namecheap API, the EPP code that has no API, the Cloudflare transfer-in call, approval of the confirmation mail through the Gmail CLI, and the status poll. Use for any domain move to Cloudflare Registrar. The fleet script domain-transfer-to-cloudflare in itsryanarmani/scripts runs this flow."
---

# registrar-transfer-to-cloudflare

Auth: Cloudflare `Authorization: Bearer $CLOUDFLARE_API_TOKEN`, base
`https://api.cloudflare.com/client/v4`. Namecheap API takes `ApiUser`,
`ApiKey`, `UserName`, and `ClientIp` on every call. Keep every key in an
env file with mode `600`. Print key names only, never values.

## 1. Check the preconditions

- The domain needs an active zone in the target Cloudflare account.
  Add the domain and move the name servers first when the zone is absent.
- DNSSEC must be off: `GET /zones/{zone_id}/dnssec` shows `disabled`.
- The account needs a default payment method and a default registrant
  contact. Set both in the dashboard once. The API cannot set the contact.

## 2. Prepare at Namecheap

- Turn API Access on: Profile, then Tools, then API Access.
  Add the machine IP to the allow list. A call from a new IP fails.
- Read the domain: `namecheap.domains.getInfo`. Note the WhoisGuard ID.
- Turn privacy off: `namecheap.whoisguard.disable` with that ID.
- Unlock: `namecheap.domains.setRegistrarLock` with
  `LockAction=UNLOCK`. The `RegistrarLockStatus` form fails with error
  2015278 and the domain stays locked. Verify with
  `namecheap.domains.getRegistrarLock`: the status shows `false`.

## 3. Get the EPP code

No API returns the code. Open Domain List, then Manage, then Sharing
and Transfer, then Get Auth Code. Read the code at a prompt. Never
write the code to disk. Never print the code.

## 4. Start the Cloudflare transfer

Encode the code in base64. Send
`POST /accounts/{account_id}/registrar/registrations/{domain}/transfer-in`
with `{"auth_code": "<base64>", "auto_renew": true}`. HTTP `202` means
the transfer started. The charge lands at completion, adds one year,
and is not refundable. Name the price and get a clear yes before the call.

## 5. Approve the confirmation mail

The losing registrar mails a confirmation request. With no action, the
transfer waits about five days. To speed the move:

1. Search mail with the Gmail CLI: `gog gmail search` for the transfer
   confirmation subject. Read the raw message and decode the HTML part.
2. Take the `ProcessOutgoingTransfer/<guid>` link from the HTML.
3. Open `https://transfer.registrar-servers.com/OutgoingTransfer/Approve?id=<guid>`.
   The page answers `Approve completed successfully`.
4. Mark the mail as read.

## 6. Poll to the end

Poll `GET /accounts/{account_id}/registrar/registrations/{domain}/transfer-in-status`.
The state shows `awaiting_approval` until the registry releases the
domain, then the registrar field in
`GET /accounts/{account_id}/registrar/domains/{domain}` shows Cloudflare.
Whois lags the API. Trust the API over whois in the first hour.

## Related

- `domain-transfer-to-cloudflare` in itsryanarmani/scripts runs this flow.
- `cloudflare-domain-launch` covers a new domain buy and a Pages site.
