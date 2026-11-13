# Per-person send access: the send-gate worker

How to let a teammate send as `name@yourdomain.com` without handing them a
Cloudflare API token.

## Why not a token

Cloudflare's `Email Sending Write` permission is account-wide. Any token with
it can send as any address on any onboarded domain — there is no per-mailbox
scope in the token model. Gmail "Send mail as" accepts only SMTP credentials,
and Cloudflare's SMTP endpoint (`smtp.mx.cloudflare.net`) accepts only those
account-wide tokens, so the Gmail path cannot be narrowed below "send as
anything on the account."

## The gate

`workers/email-send-gate/` in `pooriaarab/scripts` is a Worker that holds the
send power instead:

- One `send_email` binding per person, pinned with
  `allowed_sender_addresses` — the platform refuses any other From address,
  so enforcement is not code-level.
- One opaque key per person in `KEYS_JSON` (a `wrangler secret`). The worker
  maps key -> binding and calls `env.BINDING.send(...)`.
- `POST /send` with `Authorization: Bearer <key>` and JSON
  `{to, subject, text, html?, reply_to?}`. Errors: 401 bad key, 400 missing
  fields, 502 upstream failure. `GET /health` for liveness.
- Revocation = delete one key. Audit = Worker logs. No token value ever
  leaves the account.

## Adding a person

1. Copy a `send_email` entry in `wrangler.jsonc`, set
   `allowed_sender_addresses` to their address.
2. Add their key to `KEYS_JSON`.
3. `wrangler deploy`.

## When to use which

- Scripts/programmatic sends by a teammate or an app: send-gate worker.
- A real human mailbox used daily (full inbox, mobile apps): hosted mailbox
  (Zoho/Fastmail/Workspace) or Mailflare on the account — see the Mailflare
  option; do not hand out tokens for this either.
- Gmail "Send mail as" on Cloudflare SMTP: only possible with the
  account-wide `Email Sending Write` token — mint it per person, name it
  (`ali-email-send`), keep it send-only, and accept that it is a deterrent
  boundary, not an enforcement boundary. The verification email landing in
  the admin inbox is what actually binds them to their own address.
