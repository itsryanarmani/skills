# What else actually moves deliverability

The warm-up program in this skill is one input among several. This is a survey
of the rest, with an honest strength-of-evidence rating for each, because most
published warm-up advice is folklore repeated between vendors who sell warm-up
services.

Ratings used below:

- **documented** — a mailbox provider or standards body states it
- **industry** — widely practised, plausible mechanism, no provider confirmation
- **folklore** — repeated often, mechanism weak or unproven

## Meet the bulk sender requirements before you need to

**documented.** Google's sender requirements are the clearest published bar, and
they are not negotiable once you cross the threshold.

Every sender, at any volume, must have SPF or DKIM, valid forward and reverse
DNS, TLS, RFC 5322-conformant messages, and a spam rate under 0.30%.

Bulk senders — 5,000+ messages a day to Gmail — must additionally have SPF, DKIM
**and** DMARC, with the From: domain aligned to the SPF or DKIM domain. DMARC may
sit at `p=none` to satisfy the rule. Marketing and subscribed mail must support
one-click unsubscribe: both `List-Unsubscribe: <URL>` and
`List-Unsubscribe-Post: List-Unsubscribe=One-Click` (RFC 8058, RFC 2369).

The spam-rate figure is the one to internalise: **0.30% is the ceiling and 0.10%
is the recommendation**, measured in Postmaster Tools. That is roughly three
complaints per thousand. A warm-up cannot buy headroom against it — the only
thing that keeps you under it is mailing people who want the mail.

Yahoo published a parallel set of requirements on the same timeline. Build to
Google's and you generally satisfy both.

## Google Postmaster Tools

**documented, and the single highest-value item here.** It is the only place you
see Gmail's own verdict: spam rate, domain and IP reputation, authentication
pass rates, encryption, and delivery errors.

Two caveats that catch people out. It reports on a **DKIM-authenticated domain**,
so authentication has to work before you see anything. And it needs volume —
several hundred messages a day to Gmail before most charts populate. A warm-up
at 100/day will show little, which is itself worth knowing before you conclude
the dashboard is broken.

Set it up at the start, not when something goes wrong. The data is not
backfilled.

## Microsoft SNDS and JMRP

**documented, conditional.** Smart Network Data Services reports what Outlook and
Hotmail see from your sending IPs, and the Junk Mail Reporting Program is
Microsoft's complaint feedback loop.

Both are **IP-based**. On a shared provider IP you do not control the IP, cannot
register it, and the data is not yours — so for most people on a managed sending
service these are not available. They matter when you run a dedicated IP.

## Feedback loops generally

**documented.** A feedback loop tells you which recipients marked your mail as
spam so you can suppress them immediately. Yahoo, Microsoft and several others
run them; Google does not offer a per-message FBL, only aggregate rates in
Postmaster Tools.

Acting on an FBL is not optional politeness. A complainer you keep mailing
complains again, and complaint rate is the metric with the hardest threshold
attached to it.

## Authentication beyond the basics

**MTA-STS and TLS-RPT — industry, low effort, do it.** MTA-STS tells sending
servers to require TLS to your domain; TLS-RPT gets you reports when that fails.
The deliverability effect is small. The security effect is real, and both are
static DNS plus a hosted policy file.

**ARC — documented, but not something you deploy.** Authenticated Received Chain
preserves authentication results across forwarding. It matters to the
intermediaries that forward your mail, not to you as the originator.

**DANE — industry, niche.** Requires DNSSEC. Relevant for some European and
government receivers. Not a general deliverability lever.

**BIMI — documented, with a real price.** Your logo beside the message in
supporting clients. It requires DMARC at enforcement (`p=quarantine` or
`p=reject`), and for Gmail a Verified Mark Certificate, which costs real money
annually and needs a registered trademark. Treat it as brand work with a
deliverability side effect, not as a deliverability tactic. It does not rescue a
domain with a bad reputation.

**Read your DMARC aggregate reports.** `rua=` gives you XML from receivers
showing who is sending as your domain and whether it authenticates. This is how
you discover a forgotten system mailing as you, or a subdomain failing
alignment, before a receiver draws its own conclusion.

## Recipient diversity, and why one provider is not enough

**industry, and the most commonly ignored limit.** Every mailbox provider filters
differently. A warm-up measured entirely at Gmail tells you about Gmail.

Plus addressing makes this worse in a way that is easy to miss: `you+a@gmail.com`
and `you+b@gmail.com` are one mailbox at one provider. You get parallel sends and
no diversity at all.

A realistic seed set spans Gmail, Outlook and Hotmail, Yahoo, at least one
corporate Microsoft 365 or Google Workspace tenant — which is what your actual
B2B recipients use — and a regional provider if you sell into one. The corporate
tenant matters most for B2B and is the hardest to arrange, because corporate
filters are stricter and entirely invisible from a consumer seed.

## Engagement, and which signals are worthless

**industry, with a large folklore fringe.**

Receivers weigh things that are hard to fake: replies, a message moved out of
spam, a sender added to contacts, a thread with genuine back-and-forth, and mail
that is opened and not deleted quickly. Conversely, a message deleted unread,
left unopened for a long time, or marked spam counts against you.

What does not help: open-pixel tracking as a reputation signal — it is your
metric, not the receiver's, and image proxying makes it unreliable anyway.
Neither does clicking your own links.

**Reciprocal warm-up networks and mailbox pods are the tactic to refuse.** These
are services where many accounts mail each other, mark everything important, and
drag it out of spam. The mechanism is real, which is exactly the problem: it is
manufactured engagement between accounts with no genuine relationship, it is
detectable as a pattern, and it breaches the acceptable use terms of the mailbox
providers involved. The downside is not a warning — it is the reputation of the
domain you are trying to build. Do not use one, and if a vendor's warm-up product
works this way, that is what you are buying.

The engagement loop in this skill is deliberately narrower: mailboxes the
operator owns, real replies, modest volume, and honest accounting of what that
does and does not prove.

## Domain and IP history

**industry, and cheap to check before you commit.**

Before you build on a domain, check it: how long it has been registered, whether
it was previously used for spam, and whether it appears on the major blocklists
(Spamhaus, SURBL, URIBL among others). A domain bought cheaply on the aftermarket
can arrive with a reputation you did not earn.

Give a domain a little age before its first campaign. A domain registered days
ago is itself a weak negative signal, since throwaway domains are registered and
burnt constantly.

On shared versus dedicated IPs: shared is right for low volume, because a
dedicated IP with too little traffic never establishes a reputation at all.
Dedicated becomes worth it at sustained volume, and then SNDS and IP warming
enter the picture.

## Content and infrastructure hygiene

**industry, mostly obvious once stated.**

Link domains are reputation-bearing. Do not use public URL shorteners — they are
heavily abused and you inherit that. Prefer links on your own domain.

If you use a tracking domain, use a custom one that is yours, not a shared ESP
tracking domain, and ensure it resolves and serves over HTTPS.

Host images somewhere stable and on a domain that is not itself blocklisted.
Keep a real text/plain part alongside the HTML.

Make unsubscribe work and make it obvious. A person who cannot find the
unsubscribe marks you as spam instead, which is the outcome with the hard
threshold attached.

## List hygiene before the first campaign

**industry, high value, do it once properly.**

Verify addresses before the first send — a hard bounce rate that spikes on
campaign one is the fastest way to undo a warm-up. Validation services catch
syntax errors, dead domains and known traps.

Send to your most engaged recipients first, then widen. Suppress non-responders
after a few attempts.

Never buy or scrape a list. Beyond the legal position — and in Canada, CASL makes
this a consent problem before it is a deliverability problem — bought lists carry
spam traps, and a spam trap hit does immediate blocklist damage that no warm-up
undoes.

## Inbound variety from real services

**industry.** Mailboxes that only ever receive warm-up mail from sibling domains
have a thin inbound history. Real accounts at real services add a third-party
senders' view of the domain — different IPs, different ESPs, different content
shapes — without mailing a single additional person.

Legitimate sources, all of which email on their own schedule once an account
exists:

- **Account and notification mail from tools you actually use.** Developer and
  agentic platforms registerable from a CLI send welcome, verification, alert
  and digest mail from their own infrastructure. A `hello@` mailbox that
  holds real accounts receives real third-party traffic.
- **Newsletters and changelogs you would read anyway.** Permission-based,
  relevant, reversible. The companion scripts (`confirm-subscriptions.mjs`,
  `validate-newsletters.mjs`) exist to prove the subscription mail actually
  arrives and to audit the list, not to bulk-subscribe.
- **Announce lists joined by email.** Every serious list system still accepts
  a subscribe message, and web signup forms are mostly CAPTCHA-gated anyway —
  the mailbox emails the join address itself, which is also an outbound send
  the domain gets credit for. `subscribe-sweep.mjs` does this: each mailbox
  joins two of eight low-volume announce lists by hash (sourcehut, GNU,
  Debian, Apache, Python, GCC, Golang, PostgreSQL), the seed Gmail is polled
  for the confirmation, and it is completed in-band — mailman/ezmlm/smartlist
  lists get a Subject-preserving reply, pgLister-style lists get their link
  visited. Confirm exchanges are real two-way threads and the announce
  traffic then arrives a few times a month indefinitely. Web-endpoint notes
  from live probes: Substack, beehiiv and Buttondown are all bot-gated; the
  send-based route has no gate at all.
- **Service notifications with volume control.** Repository watches, issue
  digests, forum summaries — sources whose cadence you can tune from the
  account side.
- **Calendar invites.** An `.ics` attachment or a real invite is a different
  message shape and opens a second thread type. Vary the formats warm-up
  mail takes so the traffic is not one template forever.

CLI-signup services are the useful sub-category: the whole flow runs in a
terminal, the verification email lands in the warm-up mailbox (where the
inbound worker and gog can both read it), and the finished account then
produces ongoing notification mail. As of late 2026, reported options
include Cloudinary (`cld agent signup`), CoreGit, Berth, Bird
(`bird auth signup`), Whisper Security (curl-based), Molar
(`molar agent signup`), Pantheon (`pantheon signup`), Linq (`linq signup`),
Arcoa, Beryl, Smoketest (`smoketest auth signup`), PincerPay
(`npx @pincerpay/cli signup`), Kite Passport (`kpass signup init`),
here.now (REST `request-code`/`verify-code`), and Cosmic
(`agent-signup`/`agent-verify` CLI). Most email a 6-digit OTP or a
verification link.

Verified working end to end (REST, OTP or creds confirmed live). The
sweep signs every mailbox up for all fifteen:

| Service | Signup | Verify | Notes |
|---|---|---|---|
| here.now | `POST /api/auth/agent/request-code` | `POST /api/auth/agent/verify-code` | `XXXX-XXXX` code; aggressive per-IP rate limit, honor `retry_after` |
| Cosmic | `cosmic agent-signup` CLI | `cosmic agent-verify` CLI | 6-digit code; spam-foldered; scanners burn links fast; rejects some domains as disposable |
| AgentMail | `POST api.agentmail.to/v0/agent/sign-up` | `POST /v0/agent/verify` (bearer) | Returns API key at signup; 6-digit OTP, 24 h TTL; unverified inboxes can only mail the human |
| Inkbox | `POST inkbox.ai/api/v1/agent-signup/` | `POST .../verify` (`X-API-Key`) | Needs `note_to_human`; key + mailbox issued at signup; 48 h code TTL |
| Recoupable | `POST api.recoupable.dev/api/agents/signup` | `POST /api/agents/verify` | `.com` hosts redirect to `.dev`; `agent+` addresses can return the key immediately |
| Cloudinary | `POST api.cloudinary.com/v1_1/provisioning/agents/accounts` | link in email | Needs `agent_framework`, `agent_llm_model`, `agent_goal`; returns `CLOUDINARY_URL` at once |
| Tinysend | `POST id.tinysend.com/agent/auth` (`anonymous`) | `POST /agent/auth/claim/complete` | auth.md flow: anonymous register, then `claim` emails a 6-digit OTP |
| ClawdMail | `POST app.clawdmail.ai/api/v1/agents/register` | none needed | Anonymous register gives inbox + key; the agent then emails its own human |
| Chronary | `POST api.chronary.ai/v1/agent/sign-up` | `POST /v1/agent/verify` (bearer) | Needs `tos_version` from `GET /v1/auth/terms/current`; resend drops the key, verify dies with it |
| Agentboxd | `GET`+`POST api.agentboxd.com/v1/signup{,/challenge}` | `POST /v1/signup/claim` | SHA-256 proof-of-work (~1 s at difficulty 21), then claim emails the owner |
| MailboxKit | `POST mailboxkit.com/api/v1/register` | owner email | Key + `@agent.mailboxkit.com` inbox at once, verification mail to owner |
| Agentpub | `POST agentpub.io/api/auth/agent/request-code` | `POST .../verify-code` | `LLLL-DDDD` code shape; same flow as here.now |
| General Compute | `POST api.generalcompute.com/v1/public/agent-signups` | `POST .../{signupId}/verify` | 15-min 6-digit code; a second signup returns no `signupId` (terminal) |
| Didit | `POST apx.didit.me/auth/v2/programmatic/register/` | `POST .../verify-email/` | Needs a generated password (stored with the key); 10-min 6-char alphanumeric code; verify returns a JSON array |
| Whisper | `POST console.whisper.security/api/signup` | `POST /api/signup/verify` | `signup_id` + 15-min 6-digit code; `attribution` block required |

Rejected or dead leads from live probes: CoreGit (`AUTH_EMAIL_NOT_ALLOWED`
on our domains), Molar (endpoint gone), PincerPay (TTY-only interactive
flow). Several names in the raw list never resolved to a real signup surface.

Treat that list as leads, not gospel — CLIs and flags drift. Verify each
signup command on the service's own docs before running it against a warm-up
mailbox, and confirm the OTP mail actually arrived before trusting the
account exists. The same rfc822msgid discipline applies: a signup flow whose
verification email never landed produced no inbound value.

The fleet runs this sweep as `signup-sweep` in `itsryanarmani/scripts`: it walks
every warmup domain config, signs each identity up for every service,
requests the code, polls Gmail for the OTP, verifies, and stores the
credential under `~/.local/state` (never in a repo). Three operational
lessons from live runs are baked into it and worth knowing by hand:

- **OTP mail is routinely spam-foldered.** Verification senders score poorly
  on a fresh domain, so a default Gmail search sees nothing even when the
  mail arrived. Search with `in:anywhere` or the sweep finds no codes.
- **Inbox scanners burn one-time codes.** Claim links and some codes are
  consumed by mail-security pre-fetchers sitting on the message, sometimes
  within a minute of delivery. Verify as soon as the mail lands — a code
  polled minutes later can already be dead, and the fix is speed, not
  retries.
- **A mailbox can hold several live codes.** Re-requests stack OTP mails;
  extracting from whichever message sorts last grabs an older, dead code.
  Take the newest matching message only.

Keep the same discipline as the rest of the program: real accounts, modest
counts, and the ability to unsubscribe or delete. Subscribing a warmed mailbox
to bulk mail nobody wants re-creates the engagement-pod pattern under a
friendlier name, and the receiving ESPs read it the same way.

## Seed-list and inbox-placement services

**industry, useful, not a substitute.** Services like these maintain seed
mailboxes across many providers and report where your mail lands. They give you
the recipient diversity that is otherwise hard to assemble.

Two honest limits. Seed mailboxes have no engagement history, so they do not
predict placement for a real recipient who opens and replies to you. And they
cost money for something you partly get free by seeding your own accounts. Worth
it when you are about to spend real money on a campaign; not worth it to watch a
warm-up tick over.

## Third-party inbound: what pilots proved (2026-10-10)

**industry, with receipts.** The program earns mail from real third parties
rather than only mailing itself. Each source below was probed live before any
sweep was allowed to touch it; the pilot-gate convention in the sweeps exists
so this list stays honest.

Proven, running:

- **Agent-service signups** (`signup-sweep.py`, 15 adapters). OTP/verify mail
  plus ongoing notifications per mailbox. Newest adapter: FormSubmit, whose
  full loop was piloted live — ajax submit, activation mail, link click,
  delivered forward — including the finding that its endpoint refuses calls
  without web Origin/Referer headers.
- **Announce lists** (`subscribe-sweep.mjs`). Subscribe-by-email with in-band
  confirms. Newest: ubuntu-security-announce (classic mailman reply-confirm).
- **On-demand notification drips** (`notify-sweep.mjs`). Re-submits each
  mailbox's activated FormSubmit endpoint on a slow rotation; a real third
  party mails the mailbox on demand.

Probed and parked, with the reason:

- **Blogtrottr** (RSS-to-email): subscribe form demands a Turnstile challenge.
- **Substack**: direct API answers 200 and never mails; the browser funnel
  completes end to end with no captcha but produced zero mail in 40+ minutes.
  Retest before scaling, not during.
- **Google Alerts**: needs a Google session per mailbox; no automation path.
- **Talkwalker, beehiiv, Ghost pubs, status pages**: JS apps, 403s, or moved
  endpoints — nothing curl-reachable at probe time.
- **Have I Been Pwned notifications**: Turnstile on the notify flow.
- **High-volume discussion lists** (python-list joins fine by email): dozens
  of mails a day flood a mailbox instead of warming it. Announce-only stays
  the rule.

## What to do first

If you do four things, do these:

1. Meet the bulk sender requirements now, at whatever volume you are at.
2. Turn on Postmaster Tools and read the spam rate against the 0.10% target.
3. Get seed mailboxes at more than one provider, including one corporate tenant.
4. Verify the list before the first real campaign.

Everything else on this page is smaller than any of those.
