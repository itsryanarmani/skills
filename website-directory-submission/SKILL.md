---
name: website-directory-submission
description: "Submit a live website to free web directories for SEO backlinks, referral traffic, and GEO/AI visibility — the tiered directory table (launch platforms, startup directories, SaaS directories, review sites, AI-tool directories) with DR, link type, cost, and gate per directory, the one submission packet prepared once and pasted everywhere, the order of operations (tier-1 first, GitHub-based submissions as PRs, human-gated forms last), plus the MCP-directory path for sites that ship a hosted /mcp endpoint (remote-only registry publish, awesome-remote-mcp-servers, Glama, mcp.so), free launchpads, awesome lists, API catalogs, dataset hosts and profile sites, the method for finding niche backlinks per site (associations, awesome lists, dataset hosts, resource-page curators), verified per-niche free sources by site category, a table of what failed or blocked, listed-on badges, A2A registry registration, the outreach policy pointer, the per-site submission ledger, and a registry CSV of every directory tried with a fast run recipe. Use when a site is live and needs directory backlinks, when someone asks 'where should we list this', or after launch-seo/geo-aeo in the ship-a-product pipeline."
---

# website-directory-submission

A live site with no backlink profile ranks for nothing. Directory submissions
fix the cold start: each listing is one backlink plus a trickle of referral
traffic, and the AI-tool directories double as GEO surface (they feed the
answer engines that cite tools). This skill is the directory counterpart to
`launch-seo` (search consoles) and `geo-aeo` (quotability): same stage of the
pipeline, different destinations.

Run this after `launch-seo` + `geo-aeo`, once the site is live with real pages.
A submission that points at a staging URL, a thin shell, or a 404 is worse
than no submission — directories reject it and some never let you resubmit.

## 0. Prepare the packet once, paste it everywhere

Every directory asks for the same fields. Write them once, keep them in the
repo (see `scripts/directory-submission` in `itsryanarmani/scripts` for the
generator), and paste per directory:

- **Name** (site name, no superlatives)
- **Tagline** (one line, ≤60 chars — most forms cap it)
- **Short description** (≤260 chars)
- **Long description** (≤500 chars, what it does + who it is for)
- **URL** (production canonical, `https://`, no trailing slash unless the site serves one)
- **Category** (closest fit per directory taxonomy)
- **Tags** (3–5, lowercase, no spam)
- **Contact email** (a monitored alias, not a personal inbox)
- **Logo** (PNG ≥256px; some directories want 400×400)
- **Screenshots** (2–4 real product pixels, 1270×760 or the directory's size — never mockups presented as UI)
- **Pricing** (Free / Freemium / Paid + one line)
- **Socials** (X, GitHub, LinkedIn — only accounts that exist)

Track every submission: directory, date, status, approval ETA. Most take 1–4
weeks. A `submissions.csv` next to the packet is enough.

## 1. Tier 1 — do these first (DR 60+, free tier)

Tier 1 carries ~80% of the SEO value. DR figures below are approximate (Ahrefs,
mid-2026) and drift — re-check before you quote them anywhere that matters.

### Launch platforms

| Directory | DR | Link | Free tier | Gate / note |
|---|---|---|---|---|
| [Product Hunt](https://www.producthunt.com) | 91 | nofollow, high authority | Free | Full launch ops — see `product-hunt-launch`. One launch per product per ~6 months. |
| [BetaList](https://betalist.com/submit) | 67 | dofollow | Free / $129 featured | Pre-launch or recently launched only. Older products get rejected. |
| [Peerlist Launchpad](https://peerlist.io) | 64 | nofollow | Free | Weekly launchpad (Wed–Sun). Dev/design audience. |
| [TinyLaunch](https://www.tinylaunch.com) | 55 | conditional dofollow | Free + paid tier | Low friction, quick approval. |

### Startup directories

| Directory | DR | Link | Free tier | Gate / note |
|---|---|---|---|---|
| [Crunchbase](https://www.crunchbase.com) | 93 | nofollow, very high authority | Free basic profile | Social auth required. Investor-facing credibility. |
| [F6S](https://www.f6s.com) | 72 | dofollow | Free | Startup ecosystem profile; also unlocks accelerator/program discovery. |
| [StartupRanking](https://www.startupranking.com) | 60 | conditional dofollow | Free + paid tier | Rank-based; traffic-linked after listing. |
| [StartupBlink](https://www.startupblink.com) | 56 | dofollow | Free | Global startup map entry. |
| [StartupStash](https://startupstash.com) | 55 | dofollow | Free | Curated; needs a real product page. |

### SaaS / software directories

| Directory | DR | Link | Free tier | Gate / note |
|---|---|---|---|---|
| [AlternativeTo](https://alternativeto.net) | 76 | dofollow | Free / paid boost | List as an alternative to named competitors. Ranks for "alternative to X". |
| [SaaSHub](https://www.saashub.com) | 76 | dofollow | Free / paid boost | Register, then submit. Comparison traffic. |
| [Slant](https://slant.co) | 58 | nofollow | Free | Community-curated comparisons; answer honestly. |
| [Alternative.me](https://alternative.me) | 55 | dofollow | Free | Lighter-weight AlternativeTo. |
| [SaaSWorthy](https://www.saasworthy.com) | 52 | dofollow | Free + paid tier | Vendor form, quick listing. |
| [SoftwareSuggest](https://www.softwaresuggest.com) | 53 | dofollow | Free + paid tier | Category-gated; pick the closest software category. |
| [Crozdesk](https://crozdesk.com) | 51 | dofollow | Free + paid tier | Ranking-based software discovery. |

### Review sites (high friction, high authority)

| Directory | DR | Link | Free tier | Gate / note |
|---|---|---|---|---|
| [Capterra](https://www.capterra.com) | 93 | nofollow | Free + paid leads | Gartner Digital Markets. One vendor onboarding flows to Capterra + GetApp + Software Advice — do it once, get three listings. |
| [SourceForge](https://sourceforge.net) | 93 | dofollow | Free | Legacy but trusted. Claim + complete the profile. |
| [G2](https://www.g2.com) | 92 | nofollow | Free basic profile | Needs verified-user reviews for visibility; list first, drive reviews later. |
| [TrustRadius](https://www.trustradius.com) | 85 | nofollow | Free + paid tier | Review-gated like G2. |
| [Trustpilot](https://www.trustpilot.com) | 92 | nofollow | Free | Company reviews; invite real users only. |
| [GetApp](https://www.getapp.com) | 76 | nofollow | Free + paid tier | Same Gartner vendor flow as Capterra. |
| [Software Advice](https://www.softwareadvice.com) | 66 | nofollow | Free | Third Gartner property, same flow. |

## 2. AI-tool / GEO directories

These matter twice: backlinks for SEO plus citations for answer engines. Only
submit products with a genuine AI surface (an MCP endpoint, an agent-ready API,
or AI features) — a plain CRUD site listed as an "AI tool" gets removed and
burns the account.

| Directory | DR | Link | Free tier | Gate / note |
|---|---|---|---|---|
| [There's An AI For That](https://theresanaiforthat.com) | 62 | dofollow | Free + $49 featured | Largest AI directory. Free tier is slow; featured jumps the queue. |
| [FutureTools](https://futuretools.io) | 55 | dofollow | Free | Matt Wolfe's directory; curated, AI-only. |
| [PeerPush](https://peerpush.net) | 50 | dofollow | Free | GEO-friendly: structured data for AI readers. |
| [Futurepedia](https://www.futurepedia.io) | 42 | conditional dofollow | Free + paid tier | Large index, freemium listing. |
| [AIToolkit](https://aitoolkit.org) | 35 | dofollow | Free | Quick approval. |
| [Dang.ai](https://dang.ai) | 35 | dofollow | Free | Simple submit form. |
| [TopApps.ai](https://topapps.ai) | 30 | dofollow | Free | AI app index. |
| [aitools.fyi](https://aitools.fyi) | 27 | dofollow | Free | Long tail, fast listing. |
| [Easy With AI](https://easywithai.com) | 27 | dofollow | Free | Long tail, fast listing. |
| [altern.ai](https://altern.ai) | unverified | unverified | Free | Sign in with GitHub or Google, then submit at `/maker/submit/start`. Fees not shown on the page we read. |
| [AI Tools Directory](https://aitoolsdirectory.com) | unverified | unverified | Free + paid fast track | No account. A person reviews every tool, with no promise to publish. End-user AI tools only, clear pricing, no crypto. Not the same site as aitoolsdirectory.net. |

### Added in round 2 (checked 2026-10-22)

Round 2 read each submit page. No form was submitted. Every row has a free
tier. Skip the paid tiers. "Unverified" means the page does not show the link
type, so treat it as nofollow until you check the live listing.

| Directory | Link | Gate / note |
|---|---|---|
| [AI Tools Marketer](https://aitoolsmarketer.com/submit/) | unverified | Free listing, or a paid 24-hour launch ($39 and $49). Form, no account. |
| [AI Tools Hunt](https://aitoolshunt.com/submit-ai-tool/) | unverified | Free listing, "not guaranteed". A $15 priority review is optional: skip it. |
| [AI Directory](https://aidirectory.website/submit) | unverified | Free listings go live after approval. A paid plan or a badge skips the queue. |
| [ShowMeBest AI](https://showmebest.ai/submit) | unverified | Free basic listing. Premium tiers cost $9.99 and $49.99: skip them. |
| [AI Super Smart](https://www.aisupersmart.com/submit-tool/) | unverified | Free to submit. The form takes about a minute. |
| [DeepLaunch](https://deeplaunch.io/submit) | unverified | Free basic listing. The featured listing is paid. |
| [Dynamite AI](https://www.dynamite-ai.com/submit) | unverified | Free to list. A 24-hour fast track is paid. The form wants an image, a category and pricing. |
| [List Your Tool](https://www.listyourtool.com/submit-tool) | unverified | Free. A team reviews each submission. |
| [Spiff Store](https://spiff.store/submit-tool/) | unverified | Lists AI tools and APIs. The free listing waits about 2 months. A $15 tier skips the wait. |
| [AI Respo](https://airespo.com/submit-tool/) | unverified | Free account. Manual review, listed within 30 days. No paid featured slots. |
| [AI Corner](https://aicorner.net/submit-tool) | unverified | Free account. 14-day review. The portal is marked "Under Progress", so the form may change. |
| [AIToolex](https://aitoolex.com/submit-ai-tool) | dofollow (site-stated) | Free account. The free plan is dofollow during a "domain authority building phase". Review within a week. |
| [aitools.inc](https://aitools.inc/submit) | unverified | Free queue of 30-90 days with no placement promise. External Typeform. The $129 Fast Lane is optional: skip it. |
| [AI Agents Listing](https://aiagentslisting.com/submit) | unverified | Free after sign-in. Lists AI agents, MCP servers and agent skills. Sponsor slots are paid. |
| [Not Human Search](https://nothumansearch.ai/submit) | unverified | No account. Submit the homepage URL. A crawler checks `/llms.txt`, OpenAPI, MCP, robots and schema. It ranks by readiness, not payment. |

## 3. Long tail — batch second (dofollow, free)

Lower DR each, near-zero marginal cost once the packet exists. Work top-down
by DR; stop when the approval rate drops below the time cost.

Launch: [Uneed](https://www.uneed.best) (DR 32) · [Fazier](https://fazier.com)
(DR 45) · [Launched.io](https://launched.io) (DR 35) · [Open Launch](https://openlaunch.ai)
(DR 30) · [Launch Vault](https://www.launchvault.dev) (DR 30) ·
[NextGen Tools](https://www.nxgntools.com) (DR 25).
[MicroLaunch](https://microlaunch.net) went paid-only in 2026-11 — the launch
dialog offers Pro ($39) and Plus ($79) only, no free queue. Skip it.

Uneed's free path is a waiting line, not instant: the product needs a logo
uploaded on the Media tab before "Schedule your launch" enables, then "Join
the free waiting line" queues ~13 months out. Its `join-waiting-line` endpoint
429s after a burst of rapid clicks — space joins minutes apart, and upload the
logo by dispatching a synthetic `drop` event with a `DataTransfer` if the file
input is hidden. Free accounts hold ONE scheduled launch at a time — a second
join errors "upgrade to Pro for parallel launches", so a multi-site fleet needs
one account per site (or a paid plan). Fazier's free launch gates behind three approved comments on
other products plus its badge embedded in the homepage HTML — Verify Badge
fetches the page and looks for the embed anchor, so the site needs the chip
deployed before the check passes. Remote badge images count against the site
CSP: add the badge origin to `img-src` (submitby.ai, fazier.com) or the
security-headers E2E fails on the blocked image. Its Google OAuth popup is also blocked for
untrusted synthetic clicks; sign up by email and click the Gmail verify link,
or invoke the React `onClick` prop directly to force the OAuth navigation.

Startup: [SideProjectors](https://www.sideprojectors.com) (DR 45) ·
[StartupBuffer](https://startupbuffer.com) (DR 44) · [Launching Next](https://www.launchingnext.com)
(DR 43) · [PitchWall](https://pitchwall.co) (DA 48) · [StartupBase](https://startupbase.io)
(DR 35) · [10words](https://10words.io) (DR 20, 10-word pitch) ·
[Startups FYI](https://www.startups.fyi) (DA 19) · [FeedMyStartup](https://feedmystartup.com)
(DR 18) · [PromoteProject](https://promoteproject.com) (DR 15).

SaaS: [GoodFirms](https://www.goodfirms.co) (DA 55) · [Serchen](https://www.serchen.com)
(DA 49) · [SoftwareWorld](https://www.softwareworld.co) (DR 40) · [ToolSalad](https://toolsalad.com)
(DR 35) · [Hive Index](https://thehiveindex.com) (DA 31).

### Launchpads with a free queue (checked 2026-10-21)

No form was submitted for this list. The link type is what the site states or
what one sample page showed. Treat "unverified" as nofollow until you check
the live listing. Most free queues ask for the launchpad's badge on your
homepage, so add the badge to the page before you file. Skip every paid tier.

| Launchpad | Link | Gate / note |
|---|---|---|
| [Startup Dope](https://startupdope.com) | dofollow (site-stated) | No account. Review takes 7-14 business days. Product only. |
| [Neeed Directory](https://neeed.directory) | dofollow after badge check | Live at once after an automatic check. Sample link was plain `noopener`. |
| [LaunchIt](https://launchit.fast) | dofollow (site-stated) | Free page with no end date. Earliest free slot was about two months out. |
| [ScrollLaunch](https://www.scrolllaunch.com) | dofollow while the badge stays | Up to 25 free listings a week. Also runs a ranked list of 1,000+ directories. |
| [Dofollow.Tools](https://dofollow.tools) | dofollow while the badge stays | Five free slots a day for the whole site. 7-day queue. |
| [Turbo0](https://turbo0.com) | dofollow (site-stated) | Login needed. Asks for DR above 10 on your site and a backlink to Turbo0. |
| [SaaSCity](https://saascity.io) | dofollow after badge check | Free queue shown as about 329 days. A sample page without the badge was nofollow. |
| [LaunchIgniter](https://launchigniter.com) | dofollow for top 3 only | Badge required. Other links on the page are `sponsored`. |
| [Startup Fame](https://startupfa.me) | unverified | Badge required, review about 7 days. A sample page showed `nofollow`. |
| [Solo Launches](https://sololaunches.com) | dofollow for top 3 only | Up to five launches a day. |
| [OpenHunts](https://openhunts.com) | dofollow for top 3 only | Queue shown as about 60 weeks. A badge skips the queue. |
| [Shipstry](https://shipstry.com) | nofollow | One free submission a month. A badge unlocks dofollow. |
| [LaunchKoala](https://launchkoala.com) | nofollow | Value is traffic and a citation, not link equity. |
| [bunny.directory](https://bunny.directory) | unverified | A person reviews in about 2 working days. A sample link was nofollow. |
| [Tiny Startups](https://www.tinystartups.com) | unverified | Hand-approved. The page does not state a free-only path. Decline every upgrade. |
| [Forg.to](https://forg.to) | unverified | Builder network with a launchpad. No pricing page. |
| [DevHunt](https://devhunt.org) | mixed | Weekly dev-tool launches. Submit needs a login. Free launch not stated. |

### Launch and startup lists, round 2 (checked 2026-10-22)

Read from the submit pages. No form was submitted. "Sign-in" is what the free
path needs. A Google or GitHub sign-in uses a person's identity, so use an
account that belongs to the site owner. Skip every paid pin and every Premium
tier.

| Directory | Link | Sign-in | Gate / note |
|---|---|---|---|
| [Clapstorm](https://www.clapstorm.com/submit) | dofollow | Google, GitHub or email | No review. Live in the current or next weekly round. |
| [Lifto](https://liftoapp.com/submit) | dofollow | Google | Review took about 2 hours when checked. Each post needs a demo video or a picture carousel. |
| [ToolsNoCode](https://toolsnocode.com/) | dofollow | Google | Published at once. AI and no-code tools only. |
| [Startup Europe](https://startupeurope.net/) | dofollow | Email or Google | Any country works. Live when saved. reCAPTCHA on the email sign-up. |
| [BusinessHunt](https://businesshunt.co/) | dofollow | Email | Free business page, public when saved. The launchpad is paid only. |
| [IndieHunt](https://indiehunt.io/submit) | unverified | Email, Google or GitHub | Free launch runs 7 days from the next Monday, 08:00 UTC. Premium costs $19. |
| [StrictSeal](https://strictseal.com/submit) | unverified | Google | Tested by hand, 1 day to 3 weeks. Needs a logo and one screenshot. Rejects AI media generators and idea validators. |
| [GreenRocket](https://greenrocket.app/create) | unverified | Email link | At most 10 launches a day. The link gets a `ref` parameter. |
| [VoteKicker](https://votekicker.com/submit) | unverified | Google | Live on submit. The URL field takes 120 characters at most. The form asks if content is AI-generated. |
| [Indie-Builds](https://indie-builds.com/submit) | unverified | Google | Tagline up to 80 characters, description up to 500. Reviewed first. Not the same site as indiebuilds.co. |
| [IndieHacker.Tools](https://www.indiehacker.tools/list-indie-tool) | unverified | None | Tally form. A person adds the entry. |
| [Unloc Tools](https://unloc.tools/submit) | unverified | None | The free listing stays in review until approved. |
| [WebCatalog](https://webcatalog.io/en/apps/submit) | unverified | Google | Name and URL only. A review builds the listing. Apps only. |
| [Betabound](https://betabound.com/announce/) | unverified | None | Beta announcements only. "Not all submissions will be posted." |
| [InventList](https://inventlist.com/submit) | unverified | Google, GitHub or X | Put the free InventList badge on your site first. The listing stays private until approved. |
| [EarlyHunt](https://earlyhunt.com/submit) | nofollow | Account | Badge required. The top 3 can earn dofollow. |
| [SaaSPA.ge](https://www.saaspa.ge/submit) | nofollow | Google | Free weekly board with 200 spots. Dofollow needs its badge, a paid plan or a top-3 finish. |
| [Resource.fyi](https://resource.fyi/) | nofollow | Google | Schedule 7 or more days ahead. Three free slots a day. |
| [TechDirectory.io](https://www.techdirectory.io/get-listed) | nofollow | Email, reCAPTCHA | Basic profile live at once. Featured plans are paid. |
| [Make.rs](https://make.rs/) | nofollow | Email link | Live at once. Adds a `ref` parameter. |
| [CloudFindr](https://www.cloudfindr.co/list-your-app) | nofollow (sponsored) | Email code | B2B software. Tagline up to 60 characters, logo at least 400 by 400. The $2 plan adds dofollow: skip it. |
| [Viesearch](https://viesearch.com/submit) | dofollow | Email confirm | Human-edited. 975 sites waited on 2026-10-04, and over 82 percent of free listings were rejected. Low odds. |

## 4. MCP directories — for sites with a hosted /mcp endpoint

A directory site that ships a Streamable HTTP MCP endpoint (like the
private-repo-297b `/mcp` route) is listable as a **remote MCP server** — no
npm package needed. Verify the endpoint first with a real `initialize` →
`tools/list` handshake against the production URL; a listing for a dead
endpoint is worse than none.

| Directory | Entry point | Gate / note |
|---|---|---|
| Official MCP registry | `server.json` with `remotes[]` → `mcp-publisher publish` | Remote-only is supported: `{"type": "streamable-http", "url": "https://site/mcp"}`. DNS login checks a TXT at the **apex** domain (not `_mcp.`): `v=MCPv1; k=ed25519; p=<base64 pubkey>`. `description` must be ≤100 chars and the registry JWT expires fast — login, then publish immediately. Highest leverage — PulseMCP/Glama auto-ingest from it. See `mcp-directory-submission` §1. |
| [awesome-remote-mcp-servers](https://github.com/punkpeye/awesome-remote-mcp-servers) | GitHub PR to the README | Specifically for hosted/remote servers — where punkpeye's list redirects remote-only entries. Entry = name + URL + Glama connector badge + one-line description under the closest category, alphabetical. |
| [Glama](https://glama.ai/mcp/servers) | "Add Server" → "Hosted endpoint" tab | GitHub OAuth login. Remote endpoints use the second tab — the first ("Runs from source") demands a public repo + Dockerfile and silently fails validation on a URL. A "pending review" email per server is the authoritative confirmation. |
| [mcp.so](https://mcp.so) | GitHub issue on `chatmcp/mcpso` | Fill the template: name, description, repo URL, client-config JSON block. Issues queue for human review. |
| [Smithery](https://smithery.ai/new) | Web flow, URL method | For already-hosted servers. GitHub OAuth login → slug + upstream URL → step 2 "Skip" needs real mouse events (`mousedown`+`click`+`mouseup`; a plain `.click()` no-ops) → lands on `/servers/<ns>/<slug>/releases` with SUCCESS. The public page 200s immediately. |
| [mcpservers.org](https://mcpservers.org) | Site submit flow | Community index; check the current submit path before spending time. |
| [FindMCP](https://findmcp.dev/submit) | Public form | Low friction. |
| [MCP Hunt](https://mcp-hunt.com) | Site submit flow | Launch-style MCP index. |
| [mcp.directory](https://mcp.directory) | Claim auto-listing | Check for an existing auto-generated entry first. |
| [Cline MCP Marketplace](https://github.com/cline/mcp-marketplace) | GitHub issue | Needs a 400×400 PNG logo; quality-gated on traction. Defer for brand-new servers. |
| PulseMCP | — | Submissions paused (mid-2026); ingests the official registry. Publish to the registry and wait. |
| [awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) | GitHub PR | Use the ☁️ cloud-hosted marker for remote-only servers. See `mcp-directory-submission` §2. |
| [mcp.tc](https://mcp.tc) | `POST https://mcp.tc/submit` | JSON `{url, note}`, no account; a person reviews before the link goes live. |
| [AllMCPs](https://allmcps.com) | `/submit` wizard (the .io domain is dead) | URL → details → wait for the Cloudflare Turnstile to show "Success!" (submitting earlier no-ops silently) → "Submit to AllMCPs". The form is React-controlled: eval-setter fills change the DOM but not React state, so the submit handler reads empty values and silently no-ops (zero network calls). Drive it with `agent-browser fill` / real CDP input, and verify with a `fetch` hook on `/api/submit` returning 200 — "in the queue" is static marketing text, not a success signal. A newsletter modal can also wipe the fields mid-flow; close it and re-check values. A confirmation email arrives per submission. Has a hosted-endpoint field and an agent prompt on the page. |
| [402.ad](https://402.ad) | `POST /v1/submit` | $0.10 USDC via x402 for the programmatic path, or a free form with questions. |
| [MCPCentral](https://mcpcentral.io) | `npx mcp-submit` | The CLI also files mcp.so issues and awesome-list PRs for local stdio servers; remote endpoints file the API rows directly. |
| [Docker MCP Registry](https://github.com/docker/mcp-registry) | GitHub PR | Needs a Dockerfile — only worth it for packaged servers. |
| [appcypher/awesome-mcp-servers](https://github.com/appcypher/awesome-mcp-servers) | GitHub PR | One PR per suggestion, added at the bottom of the category; installable servers, not remote-only. |
| [MCP Market](https://mcpmarket.com) | Paste the GitHub repo URL | Free tier lists in 4-6 weeks. Skip the $29 tier. Login need not stated. |
| [TensorBlock awesome-mcp-servers](https://github.com/TensorBlock/awesome-mcp-servers) | GitHub PR or the "Add MCP server" issue form | One bullet in `docs/<category>.md`. Needs a repo URL. Merged daily as of 2026-10-21. |
| [awesome-mcp-devtools](https://github.com/punkpeye/awesome-mcp-devtools) | GitHub PR | Tools for building MCP only (inspectors, SDKs, testing). Not for a site with a `/mcp` endpoint. |

Full per-directory mechanics (manifest schemas, CLI login quirks, the
`mcpName`/100-char traps for packaged servers) live in
`mcp-directory-submission` — this skill only adds the remote-server table and
the order. A remote-only server skips every npm/`mcpName`/MCPB step there.

## 5. Order of operations

1. **Packet first.** Write the §0 packet from real site copy. No placeholders —
   a submitted placeholder ships to a directory you do not control.
2. **Tier 1 web (§1).** DR 60+ first; Gartner triple as one onboarding.
3. **Registry + GitHub-based MCP (§4).** `server.json` → publish; one PR per
   awesome list; mcp.so issue. No human login beyond GitHub.
4. **AI/GEO directories (§2)** if the product has a real AI surface.
5. **Long tail (§3)** in DR order, batched.
6. **Human-gated forms last**: Product Hunt (see `product-hunt-launch`),
   BetaList, review-site profiles, Glama/Smithery logins. An agent prepares
   every field and asset; a human completes the logged-in submit — or an
   agent drives the owner's already-logged-in browser profile
   (`browser-personal`), which passes OAuth and Turnstile gates a clean
   session never will.
7. **Channels outside the tier tables (§7)** wherever they fit — cheap to
   file, disproportionately GEO-friendly.
8. **Lists, API catalogs, datasets and profiles (§8, §9)**, then the
   per-niche targets (§10, §12). Record every result in the ledger (§11).
9. **Badges and A2A (§14)** after the pages deploy. Send pitches only through
   the outreach queue (§15).

## 6. Gotchas

- **BetaList recency.** Only pre-launch or recently launched products. An
  established site gets rejected — do not burn the slot.
- **Product Hunt cadence.** Same product/root domain needs ~6 months plus a
  significant update between launches. Directory sister sites on different
  domains are separate products; the same domain twice is a relaunch.
- **Reciprocal-link traps.** Some long-tail directories (e.g. AITop10.tools
  free tier) require a backlink from your site. Trade carefully — a sitewide
  footer link to a low-quality directory costs more than the listing earns.
- **Gartner triple.** Capterra, GetApp, and Software Advice share one vendor
  onboarding. Do it once, claim all three; do not submit three times.
- **Review-gated sites.** G2/TrustRadius/Capterra listings without reviews are
  near-invisible. List, then drive a small number of honest verified-user
  reviews — never incentivized, never fake.
- **Category fit.** A listing under the wrong category earns no clicks and
  reads as spam. Pick the closest real category on each directory; skip the
  directory if none fits.
- **One account per directory.** Most directories ban duplicate listings from
  second accounts. Sister sites submit from the same account as separate
  products, never as duplicates of each other.
- **Resubmission bans.** Some directories never let you resubmit a rejected
  URL. Verify the site (200, real content, production canonical) before the
  first submit.

## 7. Channels outside the tier tables

Smaller surfaces that sit next to the numbered tiers. Cheap to file and
disproportionately GEO-friendly, so file them on every launch.

- **Human-edited web directories.** [Curlie](https://curlie.org) (DR 82, the
  DMOZ successor) still confers a real dofollow link. The free account at
  `/public/applypublic` plus email verification is fully automatable, but a
  directory listing requires a human volunteer-editor application — stop at
  the verified account and hand that step to the owner.
  [Jasmine](https://www.jasminedirectory.com) (DR 62) is paid-only now; skip
  on a free-lane run.
- **llms.txt registries.** If the site serves `/llms.txt`, file
  [llms-txt-hub](https://github.com/thedaviddias/llms-txt-hub) (a PR adds one
  MDX under `packages/content/data/websites/`),
  [directory.llmstxt.cloud](https://directory.llmstxt.cloud/submit) (Cloudflare
  Turnstile auto-passes in a real browser profile — the result is "You're on
  the waitlist!", so list it as pending), and
  [llmstxt.site](https://llmstxt.site/submit) (form + contact email). GEO
  surface, not backlinks. Three more: [Awesome-llms-txt](https://github.com/SecretiveShell/Awesome-llms-txt)
  (PR with one bullet, `[domain](https://domain/llms.txt)`),
  [llms-text.com](https://llms-text.com/directory) (free form; the
  `llms.txt` must be live), and [llmstxt.studio](https://llmstxt.studio/registry)
  (no form: it crawls domains, so publish a valid `/llms.txt` and wait).
- **Indie search engines.** [Mojeek](https://www.mojeek.com),
  [Wiby](https://wiby.me/submit/) (image captcha — securimage distortion is
  heavy; about 1 in 12 screenshot reads land, so budget real retry time.
  Always reload the whole page for a fresh code — the in-form reload link
  desyncs the session image from the accepted answer; keep `worksafe`
  checked),
  [Marginalia](https://marginalia-search.com),
  and [Entireweb](https://www.entireweb.com/free_submission/) are independent
  crawl paths, not Google. `GET https://web.archive.org/save/<url>` snapshots
  the site into the largest public archive with no account (a 302 is success).
  Four more, checked 2026-10-21: [Yandex Webmaster](https://webmaster.yandex.com/welcome/)
  and [Naver Search Advisor](https://searchadvisor.naver.com/) (verify the
  site, then submit the sitemap; Naver has a Korean-only UI and matters only
  for a Korean audience), [ExactSeek](https://www.exactseek.com) (free form
  that opts you into a newsletter and replies with a verification email), and
  [Search My Site](https://searchmysite.net) (independent sites only; the
  free tier is a 30-day trial, so check what it reverts to). [Kagi Small
  Web](https://github.com/kagisearch/smallweb) takes a personal blog feed by
  PR: add two unlisted sites with your own, English only, no ads, no
  LLM-written posts. It links your feed, so it is not a backlink.
- **Agent-submittable APIs.** [submitby.ai](https://submitby.ai) (MCP tool or
  `POST /api/v1/submissions`; free with their badge on the site or $4.99.
  The `Idempotency-Key` goes in an HTTP header, not the body; the platform
  value is `web`. Save the returned `control_token` — it is unrecoverable.
  Deploy the badge into server-rendered HTML, then `POST
  /api/v1/submissions/:id/verify` with the token as Bearer — clean
  submissions publish within minutes),
  [directree](https://www.directree.io) (its agent API only updates
  already-claimed listings — not a first-submission path),
  [justlaunch](https://justlaunch.org) (paid REST API across ~35 platforms),
  [Launch Llama](https://tools.launchllama.co) (MCP opens drafts; the founder
  finishes the submit), [AI Directories](https://www.aidirectori.es) (partner
  key and fee, AI tools only), [A2A Registry](https://a2aregistry.org)
  (publish an agent card at `/.well-known/agent-card.json`, then `POST
  {wellKnownURI}` to `/api/agents/register`; live agents only, checked every
  30 minutes).
- **Agent & bot platform directories.** If the site ships a hosted `/mcp`,
  these put it inside the assistants themselves — the highest-GEO surface on
  this list. Each needs an account on the platform (a paid plan for two of
  them), and two need a small asset built first:
  - [Claude Connectors Directory](https://claude.ai/directory/manage) —
    submit the remote MCP server through the developer portal, choose "MCP
    connector". Anyone on a paid Claude plan can submit. Anthropic reviews,
    then lists it as a Community connector reachable from every Claude
    surface. Public docs link required by publish date; test every tool in
    the MCP Inspector first — reviewers exercise them.
    - Automate it with `scripts/claude-connector/submit.mjs` in
      itsryanarmani/scripts: one JSON config per site, `--dry-run`,
      `--status`, `--publish`. It drives the 10-step wizard
      (connection → tools → listing → use cases → company → auth →
      data handling → test & launch → compliance → review) in
      browser-personal Chrome, resumes mid-draft, and refuses to print
      DONE unless the wizard confirms the state.
    - Server-side trap: the wizard's probe sends *its*
      `mcp-protocol-version` header on `initialize`. A server that 400s
      unknown headers there reads as "0 Tools" and cannot proceed.
      Negotiate via `params.protocolVersion` on `initialize`; enforce
      the header only on later requests (fleet fix:
      private-repo-297b#275).
    - States: `In review` → `Ready to publish` → `Published (done)`.
      The publish confirmation is a `position:fixed` alertdialog —
      invisible to `offsetParent` checks — and its button needs the
      full mouse-event dispatch, not a bare `.click()`. `--publish`
      handles both.
  - [ChatGPT plugin directory](https://chatgpt.com/plugins) — submit via the
    OpenAI Platform dashboard → Plugins → "Upload new or existing plugin".
    Verified developer identity required. The package is a ZIP containing
    `<slug>-plugin/.mcp.json` (one remote server, `"type": "http"`) and
    `.codex-plugin/plugin.json` (author + interface + the
    `extensions.com.openai` review block: 5 positive + 3 negative test
    cases, `commerce`, release notes). `itsryanarmani/scripts`
    `scripts/chatgpt-plugin/build.mjs` builds it from a site config.
    - Validator traps: `interface.shortDescription` ≤ 30 chars,
      `displayName` must carry the domain brand (`Example.fyi` — a bare
      noun fails "name too generic"), no pricing words ("free", "$") in
      `longDescription`, `logo`+`composerIcon` paths to a bundled square
      icon (SVG allowed), all four listing URLs (`websiteURL`,
      `supportURL`, `privacyPolicyURL`, `termsOfServiceURL`).
    - Domain verification serves a plain-text token at
      `/.well-known/openai-apps-challenge`. Sites on Workers **custom
      domains** can't serve it from a zone route (custom domains bypass
      routes) — a zone *redirect rule* runs first, so 302 to a workers.dev
      URL that returns the token. `setup-challenge.sh` next to the builder
      automates it.
    - Ordering: upload → Connect → verify domain → Connect/Continue →
      tool scan → Submit for review (six attestations). The submit call
      400s "wait for the attached app's review" until the app-level review
      finishes (~10–30 min); retry, then `In review`. One MCP URL per org
      — delete stale drafts via More plugin actions → Delete plugin.
  - [cursor.directory](https://cursor.directory/mcp/new) — GitHub or Google
    OAuth, then a short form (name, description, install-instructions URL,
    optional Cursor deep link). Lists remote MCP servers directly. A
    repo-root `.mcp.json` also makes the `/plugins/new` auto-detect path
    work.
  - Grok bot templates — create the bot inside Grok first (X Premium), grab
    the `https://x.ai/bot/…` template link, then file the directories:
    [grokbots.best](https://grokbots.best) has a JSON API
    (`POST /api/bots/submit` with `link`, optional `categories`,
    `integrations`; 409 = already listed),
    [templatebot.lol](https://templatebot.lol) has an agent API
    (`POST /api/agent/templates`), [grokbot.wtf](https://grokbot.wtf) is a
    PR to `keshav-exe/bot-directory`, and [grok-bot.app](https://grok-bot.app)
    is a human-reviewed form.
    - Bot creation flow (grok.com, signed in): sidebar **Bots → New bot**,
      name it the domain (`Example.fyi`), then chat it its persona: "Here
      is how you work, permanently: you are the assistant for
      example.fyi… Save this as your standing instruction." The bot
      browses the live site while it works — expect it to flag real
      inconsistencies (ours caught a "US directory" label on a site that
      also lists UK homes).
    - Template export: **More → Create template** posts a canned message;
      the bot builds the template asynchronously (~30s) and drops a card
      with an **Unpublished** badge. A first message before the persona
      lands makes an empty v1 — publish only after the instruction is in.
      The **Publish** button is a human click the bot cannot do; **Copy
      Link** then writes `x.ai/bot/<id>` to the clipboard.
    - Field/enum traps: grokbots.best rejects `categories` values outside
      its enum ("directory" → 400; "Productivity" accepted);
      templatebot.lol wants `shareUrl`, not `link`; grokbot.wtf scaffolds
      entries via `pnpm template:new` then `pnpm template:check` +
      `template:verify-shares --slug`; grok-bot.app's form has fixed
      categories (Research/Engineering/Product/Content/Operations) and
      separate fields for job, standing instructions, source URL, share
      URL.
  - [Poe](https://poe.com/create_bot) — a prompt bot (instructions pointing
    at the site or its `/mcp`) publishes immediately at `poe.com/<handle>`;
    no review for basic bots. Browser-gated by a Poe account.
  - The pattern generalizes: platform-native surfaces (plugin stores,
    connector directories, bot marketplaces) outrank any web directory for
    GEO, but each requires the platform's own account and usually a
    platform-native asset — an app manifest, a bot template link, a plugin
    bundle. Budget the asset build before the submission.

The canonical machine-readable list — every tier above plus these channels,
with a `method` field per entry — lives in `itsryanarmani/scripts` at
`scripts/directory-submission/directories.json`. `check.mjs` next to it
lists entries, probes their liveness, and prints a per-domain plan. New
directories go there first; the template's `data/directories.json` is a
synced copy. The fleet's directory repo keeps the working catalog and the
per-site ledger (§11).

## 8. GitHub lists, API catalogs and datasets

Checked 2026-10-21. GitHub lists give a nofollow link by platform default, so
the value is the human and agent traffic that reads the list, plus a citation
that answer engines pick up. Read the list's contributing rules first. Several
lists auto-close a PR that breaks the format.

### Awesome lists

| List | Gate / note |
|---|---|
| [kyrolabs/awesome-agents](https://github.com/kyrolabs/awesome-agents) | PR at the bottom of `readme.md`. Open source, English, agent-related, active. New GitHub accounts are auto-closed. |
| [Jenqyang/Awesome-AI-Agents](https://github.com/Jenqyang/Awesome-AI-Agents) | One entry per PR. Needs a visible OSI licence and a full README. No hype words. |
| [steven2358/awesome-generative-ai](https://github.com/steven2358/awesome-generative-ai) | Main list wants about 1,000 followers. Otherwise use the Discoveries list. Reviewed in order of arrival. |
| [steel-dev/awesome-web-agents](https://github.com/steel-dev/awesome-web-agents) | PR titled `Add: name`. Fill the PR template, including affiliation. Web-agent tools only. |
| [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | Web issue form only, so a human submits. Resource must be 14 days old with active work, or have 100 stars. |
| [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | PR titled `Add skill: author/skill-name`. Public repo with a `SKILL.md` and real use. |
| [xpaysh/awesome-x402](https://github.com/xpaysh/awesome-x402) | One resource per PR. x402 only. Automated link check. Last merge was 2026-07-28. |
| [ai-boost/awesome-a2a](https://github.com/ai-boost/awesome-a2a) | PR must edit `README.md` and `README_zh.md`. A2A protocol resources only. |
| [restyler/awesome-sandbox](https://github.com/restyler/awesome-sandbox) | Code sandboxes for AI. Issue or PR, no format rules. |
| [zhuima/awesome-cloudflare](https://github.com/zhuima/awesome-cloudflare) | Projects built on Cloudflare. Chinese README. Intro says open source. |
| [awesome-selfhosted-data](https://github.com/awesome-selfhosted/awesome-selfhosted-data) | PR adds `software/<name>.yml`. Needs a FOSS licence and a release older than 4 months. LLM-written PRs are banned. |
| [serpapi/awesome-seo-tools](https://github.com/serpapi/awesome-seo-tools) | Must be an SEO tool, extension or API. One sentence, at the bottom of a category. |
| [markodenic/web-development-resources](https://github.com/markodenic/web-development-resources) | One resource per PR. Fully free or a free tier. Skips categories with 10 or more items. |
| [sacridini/Awesome-Geospatial](https://github.com/sacridini/Awesome-Geospatial) | For map and mobility data. No contributing file. Has Data Sources sections. |
| [toolsdk-ai/toolsdk-mcp-registry](https://github.com/toolsdk-ai/toolsdk-mcp-registry) | PR adds a package or a remote MCP server. Needs a working server. Read `docs/CONTRIBUTING.md`. Merged 2026-10-16. |
| [hashgraph-online/awesome-ai-plugins](https://github.com/hashgraph-online/awesome-ai-plugins) | PR with one line. Native MCP servers go under a topic and start with `MCP server: `. The source README must show install and MCP config. Merged 2026-10-21. |
| [Anil-matcha/awesome-agent-apis](https://github.com/Anil-matcha/awesome-agent-apis) | PR adds `providers/<name>.yaml`. The provider must be self-serve and publicly priced or free. The PR needs a live test with a real key. |
| [ikaijua/Awesome-AITools](https://github.com/ikaijua/Awesome-AITools) | Issue, or a row in both `README.md` and `README-CN.md`. Niche tools may be refused. Merged 2026-10-21. |
| [okhosting/awesome-open-data](https://github.com/okhosting/awesome-open-data) | MIT list of open datasets. No contributing file. Add one line under the right topic and check open PRs first. |

### Lists the fleet filed to (2026-10-24)

The fleet filed 78 PRs and issues to these lists in one run. The full records
(entry format, PR title style, repo checks, links) are in
`itsryanarmani/scripts`, `scripts/directory-submit/specs/github-lists.jsonl`, with
a how-to in `scripts/directory-submit/github-lists/README.md`. Look a list up
with `python3 specs/lookup.py <name>`.

| List | What it takes and what happened |
|---|---|
| [aiagenta2z/ai-agent-marketplace](https://github.com/aiagenta2z/ai-agent-marketplace) | PR edits `AGENT.md`. Filed 2 open. |
| [AIAnytime/Awesome-MCP-Servers](https://github.com/AIAnytime/Awesome-MCP-Servers) | PR edits `README.md`, `servers/agentsandboxes.json`. One entry per PR. Filed 3 open. |
| [Albertchamberlain/Awesome-MCP](https://github.com/Albertchamberlain/Awesome-MCP) | PR edits `README.md`, `data/catalog.yaml`. One entry per PR. Says AI helped. Filed 3 open. |
| [cloudflare/templates](https://github.com/cloudflare/templates) | Prepared, not filed: weak fit. Read the repo's rules before you try. |
| [RitualDev-Lab/DevShelf](https://github.com/RitualDev-Lab/DevShelf) | Issue with the form fields. One entry per PR. Filed 3 open. |
| [auscaster/stompstart-startup-list](https://github.com/auscaster/stompstart-startup-list) | PR edits `startups/agentsandboxes.yaml`. One entry per PR. Filed 3 open. |
| [joshephan/awesome-agent-apis](https://github.com/joshephan/awesome-agent-apis) | PR edits `README.md`. Filed 2 open. |
| [backblaze-labs/awesome-agent-infrastructure](https://github.com/backblaze-labs/awesome-agent-infrastructure) | PR edits `entries.yaml`. Filed 1 open. |
| [michielhdoteth/awesome-ai-agent-tools](https://github.com/michielhdoteth/awesome-ai-agent-tools) | PR edits `mcps/catalog.json`. Says AI helped. Filed 1 merged, 1 open. |
| [rdmgator12/awesome-claude-connectors](https://github.com/rdmgator12/awesome-claude-connectors) | Not filed. Site is not in Anthropic's official Connectors Directory; the list only tracks official-directory connectors. |
| [theoephraim/awesome-cloudflare-selfhosted](https://github.com/theoephraim/awesome-cloudflare-selfhosted) | Not filed. Issue form requires a public repo with a Cloudflare deploy config; the directory template repo |
| [marceloboeira/awesome-expat](https://github.com/marceloboeira/awesome-expat) | PR edits `README.md`, `content/links/us/moving/driving-schools.yaml`. Filed 3 open. |
| [blockrunai/awesome-finance-mcp](https://github.com/blockrunai/awesome-finance-mcp) | Not filed. List requires a public GitHub repo for the server; the site only publishes a hosted MCP endpoint. |
| [Vaquill-AI/awesome-legaltech](https://github.com/Vaquill-AI/awesome-legaltech) | PR edits `README.md`. Says AI helped. Filed 1 open. |
| [openstatusHQ/awesome-openapi](https://github.com/openstatusHQ/awesome-openapi) | PR edits `README.md`. One entry per PR. Filed 3 open. |
| [jivoi/awesome-osint](https://github.com/jivoi/awesome-osint) | Not filed. CONTRIBUTING bans PRs from LLMs/agents; PR would be closed |
| [dspinellis/awesome-rest-apis](https://github.com/dspinellis/awesome-rest-apis) | PR edits `README.md`. One entry per PR. Filed 3 open. |
| [MobilityData/awesome-transit](https://github.com/MobilityData/awesome-transit) | PR edits `README.md`. Filed 1 open. |
| [ahmet/awesome-web3](https://github.com/ahmet/awesome-web3) | PR edits `README.md`. Says AI helped. Filed 1 open. |
| [brandonhimpfen/awesome-apis](https://github.com/brandonhimpfen/awesome-apis) | PR edits `README.md`. One entry per PR. Filed 3 closed. |
| [brandonhimpfen/awesome-journalism](https://github.com/brandonhimpfen/awesome-journalism) | PR edits `README.md`. Filed 3 closed. |
| [brandonhimpfen/awesome-open-governance](https://github.com/brandonhimpfen/awesome-open-governance) | PR edits `README.md`. Filed 1 closed. |
| [npstorey/civic-ai-tools](https://github.com/npstorey/civic-ai-tools) | Issue with the form fields. One entry per PR. Filed 3 open. |
| [collabnix/awesome-mcp-lists](https://github.com/collabnix/awesome-mcp-lists) | PR edits `README.md`. One entry per PR. Filed 3 open. |
| [datenoio/dataportals-registry](https://github.com/datenoio/dataportals-registry) | Prepared, not filed: weak fit. Read the repo's rules before you try. |
| [wdhdev/free-for-life](https://github.com/wdhdev/free-for-life) | PR edits `data/APIs_Data_and_ML.md`. One entry per PR. Says AI helped. Filed 3 open. |
| [jentic/jentic-public-apis](https://github.com/jentic/jentic-public-apis) | Issue with the form fields. One entry per PR. Filed 3 open. |
| [lobstercare/mcp-hub](https://github.com/lobstercare/mcp-hub) | PR edits `README.md`. One entry per PR. Says AI helped. Filed 3 open. |
| [marcelscruz/public-apis](https://github.com/marcelscruz/public-apis) | PR edits `README.md`. One entry per PR. Filed 3 open. |
| [mcpHQ/awesome-mcp-servers](https://github.com/mcpHQ/awesome-mcp-servers) | PR edits `README.md`, `data/servers.json`. One entry per PR. Filed 3 open. |
| [mcpmux/mcp-servers](https://github.com/mcpmux/mcp-servers) | PR edits `servers/fyi.agentsandboxes.json`. One entry per PR. Filed 3 open. |
| [ngongcm/public-api-list](https://github.com/ngongcm/public-api-list) | PR edits `README.md`. One entry per PR. Filed 3 open. |
| [pab1it0/awesome-a2a](https://github.com/pab1it0/awesome-a2a) | PR edits `README.md`. One entry per PR. Filed 3 open. |
| [soxoj/awesome-osint-mcp-servers](https://github.com/soxoj/awesome-osint-mcp-servers) | PR edits `README.md`. Filed 1 open. |
| [sylviangth/awesome-remote-mcp-servers](https://github.com/sylviangth/awesome-remote-mcp-servers) | PR edits `README.md`. One entry per PR. Filed 3 open. |
| [tools-collection/apis-collection](https://github.com/tools-collection/apis-collection) | Issue with the form fields. One entry per PR. Filed 3 open. |
| [venelinkochev/apifinder](https://github.com/venelinkochev/apifinder) | PR edits `README.md`. One entry per PR. Says AI helped. Filed 3 open. |

Lessons: one maintainer declined 7 of 7 entries and asked for proof of data
freshness and independent adoption. One list bans PRs from agents in its
`CONTRIBUTING`, so read that file before you file. A list that wants a public
repo for the server does not take a hosted-only MCP endpoint.

### API catalogs

| Catalog | Gate / note |
|---|---|
| [public-apis](https://github.com/public-apis/public-apis) | PR with one table row. Free public API only. Description 100 characters or fewer. Has an MCP section. Merged daily. |
| [public-api-lists](https://github.com/public-api-lists/public-api-lists) | Five-column row, alphabetical, five entries per PR at most. Automated format check. |
| [APIs.guru](https://apis.guru/add-api/) | Anonymous form. Needs a stable URL to an OpenAPI, Swagger or Postman definition. PRs are closed. |
| [apis.io](https://apis.io) | Form or email. A person reviews. One company per submission. |
| [API Tracker](https://www.apitracker.io) | Form builds an email to Apideck. Takes an API or an MCP server. |
| [Postman API Network](https://learning.postman.com/docs/postman-api-network/overview/) | Make a workspace public with a collection. Needs a real callable API. |

### Dataset hosts

Use these only when the site publishes a cleaned extract of its public data.
A directory page is not a dataset. Zenodo, Hugging Face and Mendeley are one
workflow with three upload forms, not three separate wins.

| Host | Gate / note |
|---|---|
| [Google Dataset Search](https://developers.google.com/search/docs/appearance/structured-data/dataset) | No form. Add schema.org `Dataset` JSON-LD: `name`, `description` of 50-5000 characters, `distribution.contentUrl`. Check it in the Rich Results Test. Keep the page crawlable and in the sitemap. Indexing takes days. |
| [Zenodo](https://about.zenodo.org/policies/) | Free account (GitHub or ORCID login). Up to 50 GB a record. Gives a DOI. Out-of-scope content is removed later. |
| [Hugging Face Datasets](https://huggingface.co/docs/hub/datasets-adding) | Free account. Public dataset repo with a dataset card where the site link goes. |
| [Mendeley Data](https://data.mendeley.com/) | Free account. Research data focus. Gives a DOI. Size limit not stated. |
| [awesome-public-datasets](https://github.com/awesomedata/apd-core) | The README is generated. Fork `apd-core`, add a file under `core/<Category>/`, run `tests/testing.sh`. Direct download with no login. |
| [DataPortals.org](https://www.dataportals.org) | "Add a Portal" opens a GitHub issue. For open-data portal sites. |
| [Digital Public Goods Registry](https://www.digitalpublicgoods.net) | Application form for open-source, open-data and open-AI projects. Reviewed against nine indicators, about 30 days. An authorised representative applies. It renews each year. |
| [DoltHub](https://www.dolthub.com/) | Docs say "We host public data for free". A free account creates a public database. The pricing page did not load, so paid limits are unconfirmed. |
| [Internet Archive](https://archive.org/upload) | Free account. Upload only data you may share. No review queue. The item description can carry a source link. |

## 9. Profiles and communities

Profiles earn entity signals more than link equity. Communities punish
promotion, so read the rules page before you post.

| Surface | Link | Gate / note |
|---|---|---|
| [about.me](https://about.me), [Gravatar](https://gravatar.com), [GitHub](https://github.com), [GitLab](https://gitlab.com), [sourcehut](https://sr.ht) | nofollow (sampled) | Free profile with a website field. Use `rel="me"` links to tie accounts to the site. |
| [Open Collective](https://opencollective.com) | nofollow (sampled) | Needs a project that fits their rules. |
| [WordPress.org profile](https://profiles.wordpress.org) | no `rel` on one sample | The link may be nofollow for new accounts. Check after you save. |
| [Stack Overflow profile](https://stackoverflow.com), [Linktree](https://linktr.ee) | unverified | Result differs by account. Do not drop links in answers. |
| [Show HN](https://news.ycombinator.com/showhn.html) | nofollow | Must be something people can try. No landing pages. Never ask for upvotes. |
| [Lobsters](https://lobste.rs/about) | nofollow | Invite only. Self-promotion stays under about a quarter of your activity. |
| [DEV Community](https://dev.to/terms), [Hashnode](https://hashnode.com) | dofollow (sampled) | Post useful articles in good faith. Disclose affiliate links and AI help. |
| [HackerNoon](https://hackernoon.com/new) | unverified | Editorial review. Write about the niche, not an ad. |
| [daily.dev](https://docs.daily.dev/how-to-get-featured/) | unverified | Squads, source suggestions (established publications only) or direct posts. |
| [Showwcase](https://www.showwcase.com/) | unverified | Developer profile. Low priority. |
| [Featured.com](https://featured.com) | unverified | Free plan, about 2-3 media requests a week. The page does not say an answer earns a link. Paid plans start at $29 a month: skip. |
| [SourceBottle](https://www.sourcebottle.com) | unverified | Free expert profile in an expert directory. Replying to requests may need a paid plan, so read the pricing page. Strong in AU, UK, CA and US. |
| [Source of Sources](https://www.sourceofsources.com) | unverified | Free daily email of media requests. Name and email only. Spam replies get you removed. |

Indie Hackers, Medium, Peerlist, Reddit and Quora returned 403 to our fetch tool.
Read their rules in a logged-in browser before you plan anything there. Do not
list Reddit or Quora as posting targets (section 12).

## 10. Niche backlinks: how to find them per site

A directory site for one niche (pet cremation, doulas, credit unions) needs
links from places that already serve that niche. The general tables above do
not do this. Build the list per site, by hand, with this method. The result
for each site goes into the catalog (see section 11), not into this file.

### The method

1. **Industry associations and trade bodies.** Look for a "resources", "links"
   or "partners" page. Many keep these for paying members. Skip those. Keep the
   ones where a non-member can suggest a link by form or one email.
2. **Awesome lists that take PRs.** Search GitHub for `awesome-<niche>` and
   `awesome-<niche>-datasets`. Then run the merge-recency check before you
   write anything:
   ```sh
   gh pr list -R <owner>/<repo> --state merged --limit 5 --json mergedAt,author
   gh pr list -R <owner>/<repo> --state open --limit 20
   ```
   Keep the list only if an outside PR merged in the last three months. A list
   with a pile of open PRs and no recent merge is dead. Read `CONTRIBUTING.md`:
   some lists auto-close a PR for format, and some take tools only.
3. **Dataset hosts.** If the site holds public data, publish a cleaned extract
   on Zenodo (gets a DOI), Hugging Face or Mendeley, with the site link on the
   dataset card. Add schema.org `Dataset` markup to the page that offers the
   same data so Google Dataset Search finds it (section 8).
4. **Resource-page curators.** University library guides, state and county
   pages, nonprofits and public-health sites keep link lists. Find the page,
   then send one plain note that names the page, says what the site adds, and
   links one useful page. One note per page. No follow-ups, no template blast.
5. **Suggest-a-resource forms.** A named form with no account is the best
   route. Fill it with the packet from section 0, in the editor's words.
6. **Re-check the date.** Every entry below was fetched on 2026-10-21. A merge
   date, a form or a free listing can change in a month. Open the page again
   before you file.

### What to skip

- **Paid or sponsored listings.** Fees, "featured" boxes, per-state fees, a
  card hold for a free tier.
- **Member-only directories.** An association locator that needs dues.
- **Link sellers and lead-sale sites.** They sell the link you want to earn.
- **Reddit self-promotion** without reading the subreddit rules first. Most
  ban it. Read the rules in a browser, then decide.
- **Dead or hijacked domains.** Two niche sites on our first pass had been
  taken over by spam. Open the page before you trust the name.
- **Awesome lists with no merge in months**, and lists that take tools only
  when you are a directory.

### Best verified targets by niche family

The exact per-site lists live in your own fleet's catalog. These are the
strongest entries from round 1. Round 2 added more in section 12. A "pitch" has no formal route, so send
one polite note and expect a low hit rate.

**Health and sensitive topics** (eating disorders, fertility, doulas, peptide
clinics, psilocybin). Nearly every association directory is paid or
member-only. Expect short lists.

- Doulas: Chisholm Legacy Project resource hub (anonymous submit form), New
  Mexico Doula Association directory ("Suggest a New Listing"), NASHP doula
  Medicaid tracker (editorial, email).
- Fertility: Northwestern Galter Library guide (email for additions), Inova
  Library OB/GYN toolkit ("Suggest a New Resource" form, may be staff-only),
  `geniusrise/awesome-healthcare-datasets` (merged PRs on 2026-10-07, dataset
  only).
- Peptide and longevity: `mafiaguy/awesome-biohacking` (merged PRs on
  2026-10-21), `seeker89/awesome-biohacking`, Curlie (volunteer editor).
- Psilocybin: Psychedelic Alpha law and policy tracker (email corrections),
  Berkeley Center for the Science of Psychedelics (contact form, no reply
  promised), Chacruna and Zendo Project (one note each).
- Eating disorders: the Western Washington University body image resource list
  (plain email), Intuitive Eating resources page (contact form). MedlinePlus
  rejects sites whose main purpose is selling, so do not pitch it.

**Finance** (credit unions, fintech, payments).

- Credit unions: `ashishb/personal-finance-awesome` (merged daily), the League
  of Credit Unions financial education guide (editorial review), the NCUA
  website feedback form (no account), `andenick/bank-data-dictionary` (issue).
- Payments and fintech: `jplock/awesome-fintech` (active, company list).

**Legal, immigration and housing** (immigration help, foreclosure listings,
French for PR).

- Immigration help: law library guides at Illinois, Minnesota, New Mexico, USC
  and Nova Southeastern (one email each to the reference desk), Immigration
  Advocates Network (pitch).
- Foreclosure: PALawHELP (feedback form), Texas State Law Library (question
  form), LLRX (editor form), `etewiah/awesome-real-estate` (PR), Civic Tech Field Guide
  (submit form, moderation unconfirmed).
- French for PR: `gbroques/awesome-french` (PR, but seven PRs sat open), MERLOT
  (free account), Lexilogos (contact form, welcomes suggestions), Le Point du
  FLE (email to the editor).

**AI and agents** (agent sandboxes, agent wallets, x402, robotic services).

- `Haustorium12/gold-402` (best odds: external PRs merged 2026-10-22, one
  entry per PR), `Merit-Systems/awesome-agentic-commerce`,
  `solana-foundation/awesome-solana-ai`, `xpaysh/awesome-x402`.
- Sandboxes: `ianwieds/awesome-agent-sandboxes` (new list, strict automated
  rules), `webcoyote/awesome-AI-sandbox`, `arjan/awesome-agent-sandboxes`.
- Skip `awesome-account-abstraction` (weak fit) and the archived Base
  ecosystem form.

**Consumer services** (pet cremation, sober bars, dating coaches, driving
schools, auctions).

- Pet cremation: Love, Baxter Pet End-of-Life Directory ($0 to join), Pet-Loss.net
  (basic listing is free, skip the $25 box), Green Pet-Burial Society, RedRover,
  The Ralph Site.
- Sober bars: Zero Proof Nation global map (form, needs a short blurb), The
  Sober Curator rolodex (free, bot check). OpenStreetMap for each venue.
- Dating coaches: IMCB Find a Matchmaker, SwipeStats services catalog (editor
  approves each entry), Trusted Matchmakers. Life Coach Hub lists you but gives
  no website link on the free tier, so skip it for backlinks.
- Driving schools: DSAA resources page (email), Road Safety Knowledge Centre
  (self-assess, then submit). Others are pitches with low odds.
- Auctions: NAA and NALLOA resource pages, state surplus-property pages, and
  public library "government auctions" pages (all pitches).

**Civic and open data** (robotaxis, auctions, public records).

- Robotaxis: CCAM-TAC invites website suggestions by email, ITS America
  automated vehicle resources (one email), the EU connected driving knowledge
  base (email, not the Turnstile form).
- Maps and data: `osmlab/awesome-openstreetmap`, the OSM wiki service lists
  (free account), Civic Tech Field Guide, DataPortals.org, awesome-public-datasets.

## 11. Working with the ledger

Each site used to keep its own `submissions.csv`. The fleet now keeps one
ledger, because the cost is per channel (one login, one rate limit, one
repository), not per site. The runner lives in the fleet's directory repo.

- **One catalog row per target.** A target is one directory, in
  `sites/_shared/data/directories.json`. The row has a name, a tier and a
  `method` (`api`, `github-pr`, `github-issue`, `form-anon`, `form-account`,
  `form-oauth`, `form-captcha`, `pitch`, `crawl` and a few more). Never list a
  target twice. Add a `skip` of `paid` or `human` when an agent must not run it.
- **Scope a niche target to its own site.** A pet cremation list must not go
  to the other sites. The catalog row carries a `sites` allowlist naming the
  sites that may receive it. The runner on `main` does not read that field
  yet, so also pass `--sites a,b,c` on every run of a niche target.
- **A pair with no ledger row is todo.** The ledger is `submissions/ledger.csv`
  with the columns `target, site, status, date, proof, retry_after, reason`.
- **Four statuses:** `submitted` (filed, waiting), `live` (listed in public),
  `blocked` (needs a reason, may carry a `retry_after` date) and `skipped`
  (needs a reason). Put a URL or a note in `proof`.

```sh
bun scripts/submissions.ts report              # per target: done, blocked, skipped, todo, why
bun scripts/submissions.ts run "<target name>" # one driver call for every pending site
bun scripts/submissions.ts import-csv <site> <old submissions.csv>
```

`run` calls the target's driver once with all pending sites, so one login or
one PR serves all of them. A second run never files a pair that already has a
row, except a blocked row whose `retry_after` date has passed.

Rules that each came from a real failure:

- **Do not solve captchas.** Record the pair as `blocked` with the reason, and
  hand it to a person.
- **No paid placements.** Mark the target `skip: paid`. Do not enter a card.
- **No outreach campaigns.** One plain suggestion per page. No follow-up
  sequences, no bulk email.
- **A human clicks the GitHub OAuth authorize button.** Cloudflare and
  claude.ai logins also need a human. Prepare every field, then hand off.
- **One browser driver at a time.** Two drivers on one Chrome profile or one
  debug port fight over the same tabs and sessions.
- **Verify on the application's own list.** A loop that prints "submitted"
  proves nothing, and a click on a disabled button also prints success. After a
  run, open the directory's own list or status page, or read the network
  response, and compare before and after. A "pending review" email counts as
  proof. A static "in the queue" message does not.

## 12. Per-niche free backlink sources (round 2)

Round 2 read each page on 2026-10-22. No form was submitted. These add to the
round-1 targets in section 10. Use the method there to find more.

Read the access rule before you act:

- **Form** or **PR** or **Issue**: a named route. File it with the packet.
- **Pitch**: no formal route. One plain note to a person, who decides. The
  submission pipeline never sends a pitch (section 15).
- **Account**: a free account is needed. A person writes any post.

An awesome list stays in only if an outside PR merged in the last three
months. Round 2 dropped four health lists for that reason. The rules in
section 10 still apply: no paid, member-only or link-selling sites.

### All niches

| Source | Type | Access rule |
|---|---|---|
| Money, Law, Medical Sciences, Expatriates and Interpersonal Skills Stack Exchange | Stack Exchange | Account. Read `/help/promotion` first. Disclose your affiliation. Answer on-topic questions only, with sources. Overt promotion is voted down, and links are nofollow for new users. |
| [Data Is Plural](https://www.data-is-plural.com/) | newsletter | Pitch. The criteria page says to email dataset suggestions to the author. The dataset must be free, public, documented, downloadable in bulk or by API, and state its terms. |
| Featured.com, SourceBottle, Source of Sources | journalist platform | Account or email sign-up. Free plans only. See section 9. |
| [Wikidata](https://www.wikidata.org/) | wiki | Account. Neutral edits with a source only. A new external-ID property needs a proposal and notability. This is an entity signal, not a link. |

### Agents, sandboxes and wallets

| Source | Type | Access rule |
|---|---|---|
| [awesome-ai-agents-2026](https://github.com/ARUNAGIRINATHAN-K/awesome-ai-agents-2026) | awesome list | Issue form. Name, URL, type, tier, category and one sentence with no hype. Outside PRs merged in recent weeks. |
| [awesome-ai-agents-directories](https://github.com/DirectorySurf/awesome-ai-agents-directories) | awesome list | PR with one line. Slow: 8 outside PRs wait. Fit is partial for an infrastructure index. |
| [awesome-agentic-payments](https://github.com/Pink-Agentic-Payments/awesome-agentic-payments) | awesome list | PR. The link must return 200, be about agent payments, and carry a quote from the page. One factual line, alphabetical. Run by a vendor. |
| [awesome-agent-sandbox](https://github.com/yanmxa/awesome-agent-sandbox) | awesome list | PR under Related Projects. Strict one-line format. Low traction. |
| [The Rundown AI](https://www.therundown.ai/submit) | newsletter | Form, no account. Use "Recommend a Tool". The newsletter feature route is paid: skip it. |
| [Agent Community](https://agentcommunity.org/) | association | Account. Free membership. Members can appear on a map. List the project only. |
| GitHub Discussions "Show and tell" in `kubernetes-sigs/agent-sandbox`, `firecracker-microvm/firecracker`, `google/gvisor`, `microsandbox/microsandbox`, `google-agentic-commerce/AP2`, `google-agentic-commerce/a2a-x402` and `agentic-commerce-protocol/agentic-commerce-protocol` | forum | Account. Outside people posted there in Sept and Oct 2026. One neutral, on-topic post for each project. Maintainers may moderate. |
| Ethereum Magicians threads on ERC-8004, ERC-8183, ERC-8427 and the agent mandate ERCs | forum | Account. Replies must add to the spec discussion. The forum flags bare link drops. |

### Credit unions

| Source | Type | Access rule |
|---|---|---|
| [Vermont Treasurer clearinghouse](https://www.vermonttreasurer.gov/content/financial-literacy/clearinghouse/) | gov | Pitch. The page says to tell them about other providers. Free or low-cost education in Vermont only. |
| [NYPL personal finance guide](https://libguides.nypl.org/personalfinance/banking) | library guide | Pitch through Ask NYPL. A librarian decides. |
| [OCC CDFI resource directory](https://occ.gov/topics/consumers-and-communities/community-affairs/resource-directories/cdfi-and-cd-bank/index-cdfi-and-cd-bank-resource-directory.html) and [Inclusiv](https://www.inclusiv.org/) | gov, nonprofit | Pitch. Only the CDFI credit union angle fits. Low reply rate. |

### Dating, doulas, fertility, peptides and eating disorders

| Source | Type | Access rule |
|---|---|---|
| [Marriage.com guest post](https://www.marriage.com/submit-relationship-guest-post/) | guest post | Form. Unpaid. Nofollow link and a profile page. Needs original text, a 65-character title, a headshot and a bio. Live within 2 weeks. |
| [Skadate dating blog](https://www.skadate.com/we-are-accepting-guest-posts/) | guest post | Pitch by email. Original piece of 1,000+ words, one bio link. The page shows a crypto banner, so check quality first. |
| [The Birth Companions directory](https://www.thebirthcompanions.com/family-resources) | directory | Form, no account. No fee stated. Meant for birth-friendly providers. |
| [MMHLA BIPOC resource list](https://www.mmhla.org/articles/maternal-and-mental-health-resources-for-bipoc-women-mothers-and-birthing-people) | nonprofit | Pitch. The page gives the email subject line to use. |
| [MCH Digital Library](https://www.mchlibrary.org) | library guide | Pitch. The FAQ invites suggestions and promises no inclusion. |
| [Pitt Community College doula guide](https://libguides.pittcc.edu/doula) | library guide | Pitch to the reference desk. |
| [Allina Health OB/GYN guide](https://allina.libguides.com/ObstetricsGynecology) | library guide | Pitch. The page asks for suggestions. A hospital library may prefer clinical or government sources. |
| [Awesome Women's Health Resources](https://github.com/mshreyes/awesome-womens-health-resources) | awesome list | PR. Edit `resources.json`, run `build_readme.py`, pass the vetting checklist: institutional publisher, cited evidence, no commercial site. Nofollow. |
| [Awesome Digital Health](https://github.com/brandonhimpfen/awesome-digital-health) | awesome list | PR. Selective: 1 of 5 recent PRs merged. Declines entries added for promotion. |
| [BC Children's and Women's family library, eating disorders guide](https://cw-bc.libguides.com/ED) | library guide | Pitch. Canadian scope, so the fit is partial. |
| [Fight Aging!](https://www.fightaging.org/) | newsletter | Pitch. The site says commercial offers likely get no reply. Zero cost, low odds. |

### Immigration and French for PR

| Source | Type | Access rule |
|---|---|---|
| [LawHelp Minnesota](https://www.lawhelpmn.org/contact) | legal aid directory | Form, no account. The page asks for organizations that give free or low-cost legal help. Minnesota only. |
| [Ohio Legal Help](https://www.ohiolegalhelp.org/topic/other-immigration-resources) | legal aid directory | Pitch by contact form. Links on the page are nofollow. |
| [Law Library of Louisiana](https://lasc.libguides.com/immigration/resources) and [Minnesota State Law Library](https://mncourts.libguides.com/immigration/for-attorneys) | library guide | Pitch to the reference desk. Both guides give an email for questions. |
| [Dalhousie immigration law guide](https://dal.ca.libguides.com/immigration-law) | library guide | Pitch to the named librarian. Lead with IRCC language-test evidence. |
| [Camosun French learning guide](https://camosun.libguides.com/frenchlanguagelearning) and [StFX French websites](https://stfx.libguides.com/modernlanguages/french_websites) | library guide | Pitch to the liaison librarian. The Camosun guide has no test-prep section, so pitch that gap. |
| [Immigrer.com forum](https://forum.immigrer.com/) threads on TCF and TEF | forum | A guest can reply and register later. The usage rules were not read in full. Keep a reply factual. A person writes it. |

### Foreclosure and auctions

| Source | Type | Access rule |
|---|---|---|
| [Georgia AG consumer education](https://consumered.georgia.gov/your-home/foreclosure/housing-counseling) | gov | Form, no account. The feedback type "Not enough info on a subject" fits. Staff decide. |
| [California Courts Self-Help](https://selfhelp.courts.ca.gov/foreclosures/resources) | gov | Feedback box on each page. A human check guards it, so a person sends it. |
| [WashingtonLawHelp](https://www.washingtonlawhelp.org/en/contact) and [Seattle Office of Housing](https://seattle.gov/housing/homeowners/foreclosure-prevention) | legal aid, gov | Pitch. Keep it short. Cities rarely link outside sites. |
| [datasets/awesome-data](https://github.com/datasets/awesome-data) | awesome list, data portal | PR. Each entry needs a description, a licence and a `datapackage.json`. PRs merged in Aug 2026. |
| [Free Public APIs](https://www.freepublicapis.com/new) | data portal | Form, no account. A robot needs one free endpoint that works without a key, then tests daily. The page also sells sponsorship: skip that. |
| Library guides: [State Library of Louisiana](https://slol.libguides.com/c.php?g=602846&p=4175851), [East Baton Rouge Parish Library](https://ebrpl.libguides.com/c.php?g=44596&p=281829), [Iowa State](https://instr.iastate.libguides.com/c.php?g=49471&p=318718) | library guide | Pitch through the "Report a problem" or reference link. These guides list auction houses and price databases. |
| [No Reserve Podcast](https://www.noreservepodcast.com/) | podcast | Pitch through the contact page. Offer a data angle. A software vendor runs the show. |

### Pet cremation

The niche is thin. Round 2 verified little.

| Source | Type | Access rule |
|---|---|---|
| [awesome-pettech](https://github.com/dangohq/awesome-pettech) | awesome list | PR. Only two PRs exist. No aftercare section, so the entry goes under API. |
| [Animal Medical Center pet loss resources](https://www.amcny.org/pet-loss-support-resources/) | hospital, nonprofit | Pitch to the social work team. The page invites resource recommendations. It names no cremation provider. |
| [Ohio State vet center pet loss page](https://vmc.vet.osu.edu/resources/pet-loss-support) | hospital | Pitch. The page lists providers owners suggested. It cannot endorse any. |

### Psilocybin

| Source | Type | Access rule |
|---|---|---|
| [Colorado Natural Medicine Division](https://nmd.colorado.gov/third-party-educational-resources) | gov | Form, no account. "Recommend an organization." Scored on credibility, evidence, transparency and compliance. The Division does not endorse. |
| [Psychedelics Today guest form](https://psychedelicstoday.com/contact/) | podcast | Form. "Very selective." Pitch a topic, not a link. |
| [Lucid News](https://www.lucid.news/contact/) and [Reality Sandwich](https://realitysandwich.com/contribute/) | editorial | Form. Story ideas and original articles. A link drop is refused. |
| [DoubleBlind Magazine](https://doubleblindmag.com/about/) | magazine | Pitch to the ideas inbox on the About page. |
| [SSDP psychedelic resource list](https://ssdp.org/blog/students-for-sensible-drug-policys-psychedelics-committee-presents-a-psychedelic-resource-masterlist/) | nonprofit | Pitch through the contact form. Student-run, so replies are slow. |

### Sober bars

| Source | Type | Access rule |
|---|---|---|
| [Club Soda store list](https://joinclubsoda.com/hub/where-to-buy-drinks-online/) | newsletter, nonprofit | Pitch. The page asks for missing stores. The list is online stores, so ask for a see-also link. |
| [The Sober Curator](https://thesobercurator.com/contact-the-sober-curator/) | editorial | Form. Essays need real writing. Sober Spotlight profiles a person, not a site. |
| PUNCH, Imbibe, Full Pour, VinePair, Eater | magazine | Pitch. Send a reported story with a data angle. Press-release rewrites and link drops are refused. |

### Driving schools

| Source | Type | Access rule |
|---|---|---|
| [ICBC resources for driving instructors](https://partners.icbc.com/driver-training/driver-training-resources/driver-training-online-resources) | gov | Pitch. The page invites resource suggestions by email. B.C. instructors. Links are dofollow. |
| [MODSEA](https://www.modsea.org/) | association | Form, no account. The Missouri driver-ed association has a driving school resources section. |
| [TIRF (Canada)](https://tirf.ca/contact/) | nonprofit | Form. Ask TIRF to link a free Canadian driving school data set. |
| [Ontario Data Catalogue feedback](https://www.ontario.ca/form/provide-feedback-ontario-data-catalogue) | data portal | Form, no account. A backlink is unlikely. It records reuse of the approved driving schools data set. |
| DIPOD and The Instructor podcasts, In the Passenger Seat newsletter | podcast, newsletter | Pitch. Instructor audiences in the UK and Australia. Offer a short item, not an ad. |

### Robotaxis

| Source | Type | Access rule |
|---|---|---|
| [Urbanism Next resource database](https://www.urbanismnext.org/resources) | library guide | Form, no account. Each page ends with a "have a suggestion" form. No fee. |
| [Virginia DOT Research Library](https://library.vdot.virginia.gov/services/suggest) | library guide | Form, no account. The Autonomous Vehicles Hot Topic takes recommendations. |
| [TRB AV and Shared Mobility Forum directory](https://trb.org/AVSMForum) | association | Pitch to TRB staff. The directory invites resources from 2017 or later. |
| [National Transportation Library CAV guide](https://transportation.libguides.com/c.php?g=839351&p=5995913) | library guide | Pitch through "Report a problem". One short note. |
| [Streetsblog USA](https://usa.streetsblog.org/contribute-to-streetsblog) | news | Pitch of 300 words at most. Unpaid commentary up to 800 words. Disclose your interest. No generative AI text. |
| [Open Mobility Foundation](https://www.openmobilityfoundation.org/get-in-touch/) | association | Form with reCAPTCHA v3, so a person sends it. Fit is partial: it works on city mobility data. |

### Reddit and Quora

Do not plan Reddit or Quora posts here. They returned 403 to our fetch tool,
so nobody read the rules, and the rules differ by community and change. A
person reads the current rules in a browser, then decides. Qwoted and similar
platforms were not verified either.

## 12a. Round 4 results and how to repeat them

Round 4 ran on 2026-10-22 with eleven research workers. They read 202 candidate
pages. After a dedupe against the catalog, the ledger and rounds 1 to 3, and a
second `curl` check, 168 targets stayed. 160 went into the catalog. Eight are
pitch routes and stay in the outreach queue. No form was submitted.

| Result | Count |
|---|---|
| Form, no account | 29 |
| Form with email or account sign-in | 93 |
| GitHub PR or issue | 37 |
| Dofollow stated on the page | 40 |

What the run showed:

- **General boards still pay. Niche lists do not.** Launch boards, tool
  directories and awesome lists gave about 140 targets. Two waves of niche
  workers for all 17 sites gave about 25. Trade bodies keep member
  lists behind a fee. Do not spend more workers on petcremation, doulas,
  peptideclinic or soberbars until a new kind of source appears.
- **Dedupe by domain, not only by URL.** A second wave found the same domain
  under a different path. Keep one `known-domains.txt` and check it first.
- **Recheck every URL after the worker reports.** Workers read pages with a
  fetch tool. A plain `curl -L` with a browser user agent dropped seven more
  targets that answered 403 or 405.
- **Pitch is not a catalog row.** Eight library and blog pages had only an
  email or suggestion route. They stay in the JSON and out of the catalog.
- **Split a catalog change by section.** 160 rows are about 1,500 lines. The
  500 line cap needs four pull requests, one per group of catalog sections, so
  the pull requests do not touch the same hunk.
- **Hand browser work over as a queue.** Write a CSV with the columns
  `target,url,submit_url,sites,method,notes`. Put form-anon rows first, then
  dofollow rows, then account and OAuth rows.

## 12b. Round 5 results and how to change the method

Round 5 ran on 2026-10-22 with six research workers, then three retry workers
for the thin niche sites, then five second-read workers. Round 5 searched by
mining. It did not use WebSearch or GitHub search, because both quotas were
empty. 238 candidates came back. After the domain dedupe and a `curl` recheck,
219 stayed. After dropping 36 local-business directories and a second read of
every submit page, 130 targets stayed. 126 went into the catalog. Three are
pitch routes. One was already in the catalog. No form was submitted.

| Result | Count |
|---|---|
| Form, no account | 54 |
| Form with email, account or OAuth sign-in | 71 |
| GitHub PR or API | 2 |
| Dofollow stated on the page | 38 |
| Free route needs a badge | 44 |

What the run showed:

- **One meta-list gave most of the yield.** A public README of 653 startup
  directories and a directory-of-directories JSON file gave most of the 219
  candidates. Fetch the raw file and filter the domains with
  `comm -23` against `known-domains.txt` before you fetch any page.
- **The second read removed 53 targets.** A first-pass worker quoted page
  text that was not a clear free route. A second worker read each submit page
  again and dropped sites that were paid only, AI-only, or for a narrow type
  such as clinics, apps or one state. Keep this step. A first pass alone
  overstates the count.
- **Scope AI-only boards with a `sites` allowlist.** About 40 verified boards
  list AI tools only. Give them `agentsandboxes`, `agentwalletindex` and
  `private-repo-337e`. Do not give them to the other sites.
- **Local-business directories are not a fit.** Yellow Pages, Gelbe Seiten and
  MisterWhat clones need a local business and address. Round 5 dropped 36.
- **The thin niches stay thin.** Eleven niche sites got 18 site-scoped targets
  after two passes, and several are weak fits. Search through
  `curl -sL "https://r.jina.ai/https://html.duckduckgo.com/html/?q=..."`
  works for unquoted queries when direct search engines show captchas. It is
  rate limited, so run it one query at a time.
- **Wayback and Common Crawl indexes were slow or down.** Do not plan a run
  that depends on them.
- **Split the catalog change by section and by site group.** 126 rows are
  about 1,300 lines. Four pull requests keep each one under 500 lines.

## 13. What failed or blocked

Skip these dead ends, or hand them to a person. The dates come from the
fleet's browser and API runs on 2026-10-21 and 2026-10-22. Re-check a row
before you give up on it for good.

| Cause | Directories | What to do |
|---|---|---|
| Captcha | SaaSHub and AlternativeTo (hCaptcha). SideProjectors, PromoteProject and Entireweb (reCAPTCHA). Launching Next (math check). Wiby and Lightning-Strike (image captcha). LawHelpNY (math check). | Never solve a captcha. Mark the row `blocked` and hand it to a person. |
| OAuth-only sign-up | PitchWall, StartupBase. | The only way in is a personal Google or GitHub identity. Use an owner account or skip. |
| Login in another browser | Yandex Webmaster, Naver Search Advisor, Poe. | Needs an account that the agent browser does not hold. A person signs in. |
| Paid or card | Tiny Startups (GBP 69 to go live). Solo Launches ($9 for each date). SaaSCity (dofollow). MCP Market remote route ($69). AI Pure, GPTDemo, AI Center, Linezine, FindMyAITool and Dessign (paid only). Findstack ($99). | Do not enter a card. Mark `skip: paid`. |
| Needs a badge or backlink first | LaunchIgniter, LaunchKoala, ScrollLaunch, LaunchIt, bunny.directory, Startup Fame, TheSaasDir, InventList. Turbo0 also needs a site with DR above 10. | Ship the badge to production first (section 14). |
| Needs a public repo | punkpeye `awesome-mcp-servers` (also a Glama score badge), MobinX `awesome-mcp-list`, `best-of-mcp-servers` (needs a `github_id`), `awesome-healthcare-mcp-servers`, TensorBlock, kyrolabs, awesome-selfhosted. | A site whose source is private cannot use these. Skip them. |
| Needs personal data | Startup Dope (founder phone). DevHunt (bio and social link). Tools.so (X handle). GetLatka (company email). Grok bot directories (an X Premium Grok bot link). | Skip unless the owner supplies the data. |
| Removed or broken | Smithery publish (403, "updating servers has been removed"). MCPCentral CLI ("API integration pending"). Open Launch (the email verification link returns HTTP 500). Alternative.me (no verification email after 15 minutes). Connectively (closed in December 2024). | Retry the broken ones later. Drop the removed ones. |
| Not a fit | AI-tool-only lists (altern.ai, AI Tools Directory, Dofollow.Tools) for a non-AI site. Dataset hosts when the site has no open dataset. Personal profile pages. Show HN. | A listing in the wrong category gets removed. Skip it. |
| Email-only routes | API Tracker, ITS America and every pitch row in section 12. | The pipeline sends no email (section 15). |
| Link farms and leads | Same-template link directories, and sites that sell the link you want to earn. | Skip. |

### Review queues, as of 2026-10-22

| Directory | Queue | Next step |
|---|---|---|
| 10words | Free queue. Estimated feature date about 2034. | Leave it. The listing may appear after review. |
| Uneed | About 13 months. One scheduled launch for each account. | Skip unless you have time. |
| SaaSCity | About 329 days. | Skip. |
| OpenHunts | About 60 weeks. A badge skips the queue. | Skip. |
| MCP Market | 4-6 weeks on the free tier. | Wait. |
| mcpservers.org | Review within 2 weeks. | Re-check on 2026-10-29. |
| TinyLaunch | Weekly slots from 2026-11-23 to 2027-03-15, pending approval. A top-3 finish and its badge earn the backlink. | Re-check on 2026-10-29. |
| Claude Connectors Directory | 7 of 17 sites published, 10 in review. | Re-check on 2026-10-29. |
| Neeed Directory | Three clinic sites held "Under review". Its guidelines exclude clinics and local services. | Do not add a badge to those sites. |
| Findstack, DevResources | About 5 months. | Skip. |

### Rate limits we hit

| Where | Limit |
|---|---|
| Neeed Directory | About 10 submissions an hour. |
| cursor.directory | About 5 plugins an hour. |
| mcp.tc | A daily limit for each IP. The API returns `rate_limited` and a `retry_after` value. |
| Uneed | Rapid clicks on the join endpoint return 429. Space joins minutes apart. |
| Gmail API | `rateLimitExceeded` when several agents read mail. Retry after about 10 seconds. |
| A2A Registry | 10 registrations an hour. See section 14. |


## 14. Listed-on badges and A2A registry registration

### Badges that unlock a followed link

Some directories give a nofollow or a queued listing until your site shows
their badge. The directory then checks your live production page. Staging does
not count: it is noindex and a different host.

| Directory | What the checker wants | Verify | Limit or note |
|---|---|---|---|
| Neeed Directory | Its badge link on the homepage, no `nofollow`. | Open the product page, click the owner's verify control, reload. The outbound link loses `nofollow`. | About 10 actions an hour. Space the clicks out. |
| Startup Fame | A visible link to `startupfa.me`, no `nofollow`, `ugc` or `sponsored`. | Sign in, tick the checklist attestation, click "Verify badge". | Review takes about 7 days. |
| LaunchIt | Any link to `launchit.fast` on the homepage. | None. The check runs at review. | Adding the badge after you submit is allowed. |
| LaunchKoala | A link to LaunchKoala on a page of your domain, no `nofollow`. | Paste the homepage URL in the wizard and click verify. | Errors: `NOT_FOUND`, `NOFOLLOW`, `DOMAIN_MISMATCH`. |
| ScrollLaunch | Its badge image, which uses your product slug. | Create the product first, then use the badge step on the product page. | Free listings stay dofollow while the badge stays. It re-checks weekly. |
| LaunchIgniter | The badge on the homepage. | Run the badge check on the product page. | A manual confirm is allowed if the checker is blocked. |
| bunny.directory | The badge link, followed, while it stays. | Click "Check my badge". Pass text: "Found the badge on your site". | The checker errors on `nofollow`. |
| EarlyHunt, SaaSPA.ge | Its badge for dofollow. Otherwise the link is nofollow. | Follow the submit wizard. | Top-3 finishes also earn dofollow. |
| AIToolzDir, ThatsMy AI | A backlink or partner link kept on your site. | Check the live page after it deploys. | A sitewide link to a low-quality directory can cost more than the listing earns. |

Steps for every badge:

1. Submit the listing first. Read the slug or URL the directory gives you.
2. Add the badge markup from the directory's own page. Never guess a slug. A
   badge that links to a dead listing proves nothing and can fail review.
3. Put the badge in the server-rendered HTML. A script-injected badge is
   invisible to most checkers.
4. Add the badge image origin to the CSP `img-src`, or a security-headers
   test fails on the blocked image.
5. Deploy to production. Then prove the badge is live:
   ```sh
   curl -sL "https://<domain>/" | grep -o '<a [^>]*<directory-host>[^>]*>'
   ```
   Pass when the output holds the directory link and no `nofollow`. A miss
   means the deploy did not finish. Do not click verify yet.
6. Click verify, or wait for the review. Then check the live listing page. The
   link `rel` is the proof. A "verified" message alone is not.

Not worth a badge yet: Turbo0 (needs DR above 10), SaaSCity and OpenHunts
(queues of months). Fazier needs three comments on other products first.

### A2A registry registration

An A2A registry lists agents that answer the A2A protocol. A site with
`/.well-known/agent-card.json` can register. The card must point at a working
A2A endpoint, not at an MCP endpoint. The fleet's first 17 rows were skipped
for that reason.

**A2A Registry** (`a2aregistry.org`) is free and has no account. It sends a
real `message/send` when you register, and every 30 minutes after. It lists a
site only while that call works. Fix and deploy the endpoint to production
first.

```sh
# Dry run. Registers nothing.
curl -s -X POST https://a2aregistry.org/api/agents/preview \
  -H 'Content-Type: application/json' \
  -d '{"wellKnownURI":"https://<domain>/.well-known/agent-card.json"}'

# Register. Replace "preview" with "register".
```

The body has one field: `wellKnownURI`. It must end in
`/.well-known/agent-card.json`. The registry checks that the card has a name,
a description, a URL and a version.

| HTTP | Meaning | Ledger status |
|---|---|---|
| 201 | Registered. The body holds an `id`. | `live` after the check below |
| 202 | Held for review (`under_review`). Not a failure. | `submitted` |
| 400 | Card or smoke test refused. Read `detail`. | `blocked`, with the detail as the reason |
| 409 | Same host, or same name and author. | `live` if the check passes |
| 429 | Over the limit, or the registry is at review capacity. Wait for `Retry-After`. | no change, retry |

Limits for each client IP: 10 registrations an hour and 30 a day. Preview all
your sites first. Then register 10, wait an hour, and register the rest. On
2026-10-22 the registry answered 429 "reached its review capacity" for the
first live calls, so plan for retries.

Verify each site:

```sh
curl -s 'https://a2aregistry.org/api/agents?search=<name>'
curl -s 'https://a2aregistry.org/api/agents/<id>/health'
```

Pass when `conformance` is true and `task_conformance` is `WORKING`. Any other
value means the probe failed. Open an issue in the site's repo. Do not mark the
row `live`.

These limits and result codes come from the registry's public source and our
dry runs. The success path was not yet proved on a live site when this was
written. Check the code or `https://a2aregistry.org/submit` if a call differs.

Other A2A targets, not used:

- **LinkAgora** (`openagora.cc`): API-only registration that returns a key once.
  Check its docs for field names before you call it. Store the key in a
  secrets file, never in the repo.
- **Global A2A Registry**: needs a console account and a DNS TXT record for
  each domain. Defer it.
- **awesome-a2a lists**: they take A2A protocol resources only. A niche
  directory is a site, and many sibling PRs read as promotion. Skip.

## 15. Warm-up and outreach policy

The submission pipeline files forms, PRs, issues and API calls. It never sends
a cold pitch. Every "pitch" row in section 12 goes through a separate outreach
queue instead:

- A person approves each batch.
- Mail leaves from a sending subdomain that has passed warm-up. Use
  `domain-email-warming` for authentication, the volume ramp and placement
  tests.
- Send one plain note for each page. No follow-up sequence and no bulk blast.
  Use `growth-cold-email` for the consent and CASL rules.

Mark pitch rows `skip: human` in the catalog so `run` never picks them up
(section 11).

## 16. The directory registry and the fast run

`directories.csv` in this folder holds one row for every directory that
rounds 1 to 3 looked at. It is a snapshot of the fleet catalog and ledger from
2026-10-22. Read it before you open a browser. It tells you which boards work,
which ones block, and when to look again.

| Column | What it holds |
|---|---|
| `name`, `url`, `submit_url` | The directory and where its form, PR or API lives. |
| `type` | `launch-board`, `startup-directory`, `saas-directory`, `review-site`, `ai-tool-directory`, `awesome-list`, `mcp-registry`, `agent-platform`, `llms-txt-directory`, `search-engine`, `api-directory`, `dataset-catalog`, `library-guide`, `association`, `forum`, `newsletter` and a few more. |
| `method` | How a run files it: `api`, `github-pr`, `github-issue`, `form-anon`, `form-email`, `form-account`, `form-oauth`, `form-captcha`, `pitch`. |
| `free_tier` | `free`, `freemium` or `paid-only`. Never enter a card. |
| `requirements` | Tags, separated by `;`. See the list below. |
| `rate_limit` | The limit we hit or read. Empty means none seen. |
| `link_rel` | `dofollow`, `nofollow`, `dofollow-after-badge` or `unknown`. |
| `review_time` | How long the board takes. |
| `fit`, `sites` | Which kind of site suits it. `all` means every site. Else a list of sites. |
| `outcome` | `live`, `under-review`, `blocked`, `skipped` or `todo` (never tried). It is the best result over all sites. |
| `outcome_sites` | The count for each status, for example `live:14;under-review:3`. |
| `outcome_date`, `recheck_date` | When the last result came in, and when to look again. |
| `outcome_note`, `notes` | Proof URL or the reason, then the rules the board states. |

Tags in `requirements`: `account`, `email-verify` (a confirm link in the
inbox), `email-field`, `email-pitch`, `badge` (your site must show its badge),
`reciprocal-link`, `rate-limit`, `captcha`, `oauth`, `human-only`,
`paid-gate`, `needs-repo` (a public repo), `needs-dataset`,
`personal-data` (phone, photo or X Premium), `ai-restricted` and
`product-domain-email`. A row with no tag is an open form.

Pick the open rows with a short script. This one lists boards never tried that
need no human, captcha, OAuth, badge or payment:

```sh
python3 -I - <<'PY'
import csv
bad = {"human-only", "captcha", "oauth", "badge", "paid-gate", "needs-repo",
       "personal-data", "email-pitch", "ai-restricted"}
for r in csv.DictReader(open("directories.csv")):
    if r["outcome"] == "todo" and not bad & set(r["requirements"].split(";")):
        print(r["name"], r["method"], r["submit_url"])
PY
```

### What rounds 1 to 3 taught us

- **Rate limits count per network.** Unloc Tools stops after about 6
  submissions in 90 minutes. BuildVoyage returns HTTP 429 after about 9 in 70
  minutes. Neeed allows about 10 actions an hour. cursor.directory allows about
  5 plugins an hour. The A2A Registry allows 10 an hour. Uneed returns 429 on
  fast joins. Stop at the first limit and retry the next day. Do not rotate
  networks or accounts. That risks a ban on the one account you keep.
- **Weekly caps count per account.** Clapstorm allows 3 launches a week.
  TinyLaunch allows one launch per date. Uneed allows one scheduled launch for
  each free account. Plan the sites across weeks.
- **Badge-first boards.** EarlyHunt, InventList, LaunchIgniter, LaunchKoala,
  LaunchIt, ScrollLaunch, bunny.directory, Startup Fame, AIToolzDir and
  ThatsMy AI need a badge or partner link on the live site first. Ship the
  badge (section 14), then file. Neeed lists a site at once but keeps the link
  `nofollow` until the badge is verified.
- **OAuth-only boards.** Lifto, SaaSPA.ge, StrictSeal, VoteKicker,
  Indie-Builds, ToolsNoCode, WebCatalog, Resource.fyi, PitchWall and
  StartupBase accept only Google or GitHub sign-in. That signs in the owner's
  personal identity. Mark them `blocked`. Do not click authorize for the owner.
- **Captcha boards.** SaaSHub and AlternativeTo (hCaptcha). SideProjectors,
  PromoteProject, Entireweb, TechDirectory.io and Startup Europe (reCAPTCHA).
  Never solve one. Managed Turnstile (Unloc) passes by itself in the owner's
  own Chrome profile. That is not a solve.
- **Boards that refuse AI submissions.** awesome-selfhosted bans LLM-generated
  PRs. awesome-osint says an LLM or agent cannot open the PR, and it closes the
  PR. Kagi Small Web bars LLM-generated content. VoteKicker asks if the
  text is AI-generated. DEV Community wants AI help disclosed. kyrolabs
  auto-closes PRs from new GitHub accounts. Mark these `skipped` or hand them
  to a person. Answer honestly when a form asks.
- **Needs a public repo.** punkpeye, MobinX, ToolSDK, best-of-mcp-servers,
  kyrolabs and the healthcare MCP lists need a public source repo. A private
  repo means skip.
- **Human only.** Curlie needs a volunteer editor. Lobsters is invite-only.
  Startup Dope wants a founder phone number. IndieHacker.Tools wants a personal
  photo. The Colorado Natural Medicine form records the signed-in Google
  address. Forums, Stack Exchange and Reddit need a person who writes a real
  answer and discloses the tie.
- **Email at the product domain.** BuildVoyage asks for a maker email at the
  product's own domain. Use `hello@<site-domain>`. It lands in the same inbox.
  Confirm each submission with the emailed link.
- **Browser traps.** Take a screenshot to wake the tab before a click. Take a
  `snapshot` before every `fill`, because refs bind only then. Custom radios
  and checkboxes ignore `click`: use `check`. A calendar day may be missing from
  the snapshot: click the enabled day with `eval`. A fill or click on a
  disabled button also prints "Done". Read the result on the destination site.
- **Mail reads.** The Gmail API returns `rateLimitExceeded` when agents read
  together. Wait about 10 seconds and retry.

### The fast run

1. **Check the site first.** The production URL answers 200 with real
   content. The packet (section 0) is complete. Badges are live if you
   want badge boards.
2. **Select rows.** Open `directories.csv`. Keep rows where `outcome` is `todo`
   or `recheck_date` is today or older. Drop rows tagged `human-only`,
   `captcha`, `oauth`, `paid-gate`, `needs-repo` or `ai-restricted`. Drop rows
   whose `sites` or `fit` do not match the site. Drop `email-pitch` rows: they
   go to the outreach queue (section 15).
3. **Order the work.** First `api` and `form-anon` rows (no account). Next
   `github-pr` and `github-issue` rows, done by a worker with `gh` only. Then
   `form-account` boards on the one shared account. Then `email-verify` boards,
   which need the inbox. Badge boards come after the badges deploy.
4. **Batch by board, not by site.** One login serves every site. Run one board
   across all sites in one loop. Read `rate_limit` first and space the calls.
   Stop the loop on the first 429 or "too many". Write `blocked` with a
   `retry_after` date and move to the next board.
5. **Use one browser driver.** Run one driver at a time on one Chrome profile.
   The helpers in `scripts/directory-submit` (itsryanarmani/scripts) read the
   packet JSON for each site, run one driver per board, and write the ledger.
6. **Verify on the destination.** Open the board's own list or status page.
   Read the product page, the search API or the "pending review" email. A
   printed "submitted" proves nothing.
7. **Record.** Write one ledger row for each target and site with a proof URL or
   a reason (section 11). Then update the registry row: `outcome`,
   `outcome_sites`, `outcome_date`, `recheck_date` and `outcome_note`. Add any
   new rate limit or trap to `rate_limit` and `notes`.
8. **Set re-checks.** Under review: look again in 7 days. Rate limited: the
   next day. Weekly cap: the next week. Review queues longer than 60 days: skip.

## Checklist

- [ ] Packet written from real copy (§0), stored in the repo, no placeholders.
- [ ] Production URL verified: 200, real content, canonical correct.
- [ ] Tier-1 web directories submitted (§1), Gartner triple via one onboarding.
- [ ] `server.json` with `remotes[]` published to the official registry (if the site ships `/mcp`).
- [ ] Awesome-list PRs opened + mcp.so issue filed (if the site ships `/mcp`).
- [ ] Agent/bot platforms filed where the account + asset exist: Claude
  connector (paid plan), ChatGPT plugin (verified org), cursor.directory,
  Grok template dirs (needs the `x.ai/bot` link first), Poe bot.
- [ ] AI/GEO directories submitted (if the product has a real AI surface).
- [ ] Long tail batched in DR order.
- [ ] Niche targets found per site (§10) and added to the catalog with a
  `sites` allowlist. Every result recorded in the ledger (§11).
- [ ] Badges shipped to production and checked with `curl` before you click
  verify (§14). A2A endpoint answers `message/send` before you register.
- [ ] No cold pitch sent from the pipeline. Pitch rows go to the outreach
  queue (§15).
- [ ] The registry row in `directories.csv` is updated after each run (§16).
- [ ] `submissions.csv` tracks every directory, date, and status. Use honest
  status words: `listed` (publicly visible), `pending` (filed, awaiting
  review), `draft` (needs one more step — e.g. site verification), `blocked`
  (gate named), `paid` (skipped on free lanes), `dead` (URL unreachable).
- [ ] Human-gated submits (Product Hunt, BetaList, logins) handed off with fields + assets ready.

## See also

- [`../launch-seo/SKILL.md`](../launch-seo/SKILL.md) — search-console submission; run before this.
- [`../domain-email-warming/SKILL.md`](../domain-email-warming/SKILL.md) — warm a sending domain before any pitch (§15).
- [`../growth-cold-email/SKILL.md`](../growth-cold-email/SKILL.md) — consent and CASL rules for outreach (§15).
- [`../geo-aeo/SKILL.md`](../geo-aeo/SKILL.md) — AI quotability; run before this.
- [`../product-hunt-launch/SKILL.md`](../product-hunt-launch/SKILL.md) — the Product Hunt row of §1, expanded into full launch ops.
- [`../mcp-directory-submission/SKILL.md`](../mcp-directory-submission/SKILL.md) — the MCP rows of §4, expanded (manifest schemas, CLI quirks, OAuth path).
- [`../launch-directory-site/SKILL.md`](../launch-directory-site/SKILL.md) — the directory-site launch pipeline; points here for backlinks.
- [`../ship-a-product/SKILL.md`](../ship-a-product/SKILL.md) — orchestrator; this is the distribution stage after `geo-aeo`.
