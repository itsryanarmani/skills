---
name: name-a-product
description: "Find a product name and clear it before you commit — brief, generate candidates, say them aloud, check for competing COMPANIES and trademarks, then check domains (that order matters: a domain sweep hands back variants that funded competitors already occupy). Includes RDAP bulk sweeps, Cloudflare domain-check for price/tier, handle and registry checks, and an appendix of naming lanes that came back empty in one ~100k-check session. Use before cloudflare-domain-launch, or when renaming a product."
---

# name-a-product

Naming fails in a predictable order: people generate, fall in love, check the
domain, buy it, and only then discover the competitor. Run the steps below in
order and the expensive discoveries happen while they're still cheap.

## 0. Brief before candidates

Write down, in one line each, before generating anything:

- **What it is** and who buys it (consumer vs enterprise changes acceptable tone).
- **Register** — plain and modest (Notion, Ramp, Linear, Stripe, Loom) vs
  characterful (Chili Piper, Gusto, Lemonade). Both work. Mixing them reads as
  indecision.
- **Markets and languages** it must work in.
- **Budget** — register price only, or is aftermarket in scope? This single
  answer eliminates most of the search space (see Appendix).
- **Must it be one word?** and **must it be `.com`?** Hold these loosely; they
  are usually the constraints that make the brief unsatisfiable.

If a stakeholder wants a simple, one-word, kid-pronounceable `.com` at register
price, say early that this is very unlikely to exist (Appendix) so the brief can
change in round one rather than round ten.

## 1. Generate candidates

Random string generation does not produce brandable names — it produces
pronounceable mush. Names that work come from a *source*:

- **A real thing with a picture attached** — Bullpen, Legwork, Nightdesk. Concrete
  beats abstract; abstract nouns read as "trying too hard".
- **A metaphor from the product's own domain.** Prefer one that hands you a
  vocabulary: *Popcorn* gives kernel (idle) → pop (activate) → batch (parallel run)
  → kettle (dashboard). That vocabulary is worth more than a marginally nicer sound.
- **Two simple words fused.** Facebook, Dropbox, Snapchat, YouTube. At 6–8
  characters the seam disappears. (Netflix and TikTok are *not* this — Netflix
  respells "flicks", TikTok is reduplication. Both are still fine models.)
- **A suffix, not a second word.** `-ley`, `-mere`, `-wick`, `-ham`, `-ton`,
  `-bury` are English place-name suffixes: `Mossley` reads as one word the way
  `Ashley` does.
- **A lower-search-volume synonym** of the word you want, when SEO matters:
  `provolone` over `pepperoni`, `romesco` over `pesto`.

## 2. Say it aloud, then look at it written

Cheap, and it kills candidates fast:

- **Phone test.** Say it to someone and have them spell it back. `Dabir` comes
  back as `Dabeer`. That is a fatal, permanent tax.
- **Embedded words.** `Dabir` contains "beer". Read every candidate for words
  hiding inside it.
- **Homophones and plurals.** Does the plural or possessive break? Does it collide
  with a common word when spoken?
- **Search-suggest.** Type the name into Google and read the autocomplete. If it
  suggests something unfortunate, that is what your customers will see too.
- **Across markets.** Check meaning and pronunciation in every language in the
  brief, not just English.

**Connotation checklist** — a name can be available, memorable, and still wrong:

| Trap | Examples |
|---|---|
| Villain coding | `Vizier` (Jafar), `Praetorian` (assassinated emperors) |
| Failure coding | `Icarus` (flies too close, falls), `Sisyphus` |
| Dishonesty coding | `Fudge` — "fudge the numbers", fatal near data or money |
| Subordinate coding | `Satrap` reads as puppet ruler |
| Slurs / regional meaning | `Cracker` (US slur). Check every market |
| "Plain/boring" coding | `Vanilla` |
| Regional illegibility | `Bullpen` is invisible outside North America |

## 3. Competing companies — BEFORE domains

**This is the step everyone skips and it is the one that matters.**

Domain availability tells you far less than it appears to. Funded competitors in
your category already hold the `try<name>.ai`, `<name>ai.com` and `get<name>.com`
variants that a domain sweep returns as "available alternatives" — so a clean
sweep can walk you straight into someone else's brand.

From one session, every one of these looked open on domain variants and is a live
company: `popcorn` (Popcorn AI, AI agents), `dumpling` (DumplingAI, agent
builder), `pop` (teampop.com, custom AI agents), `granola` (AI notetaker),
`bagel` (Bagel Labs), `sumac` (case-management software), `deputy` (HR SaaS).

For each candidate:

```bash
# live site on the bare domain?
curl -sL --max-time 10 -A 'Mozilla/5.0' "https://<name>.com" \
  | grep -oiE '<title>[^<]{0,80}'
```

Then search `"<name>" <your category> startup company`, and check Crunchbase and
app stores. Also check **common-law** use (an unregistered but active brand still
blocks you) and CLI/package-name collisions.

## 4. Trademark — mechanics, not just "ask a lawyer"

Do a knockout search yourself first, then pay for clearance:

- **Classes** — software is Nice class **9** (downloadable) and **42** (SaaS).
  Search both.
- **Search** USPTO (tmsearch.uspto.gov) and EUIPO/WIPO for your markets. Both
  block automated queries; do it by hand in a browser.
- **Similarity + relatedness are weighed together.** Identical services raise the
  bar on how different the marks must be. `POPCORN` wholly contains `POP`, so a
  competitor called "Pop" in the same category is a real citation risk.
- **Mark strength.** Fanciful (Kodak) > arbitrary (Apple for computers) >
  suggestive > descriptive > generic. A descriptive name is cheap to pick and
  nearly impossible to defend. Common surnames and generic historical titles
  (`Vizier`) are weak marks.
- Get an attorney knockout search **before** spending on brand assets or starting
  a rename. A completed 3,000-file rename is expensive to reverse; $109 of
  domains is not.

## 5. Domains — availability and price

**RDAP for bulk pre-filtering** (free, no auth). Surface unexpected codes rather
than swallowing them — 429 and 5xx are not "taken", and RDAP has a small
false-positive rate under load (one confirmed case: `mossley.com`, registered
since 2012, returned 404):

```bash
check() {
  code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 \
    "https://rdap.verisign.com/com/v1/domain/${1}.com")
  case "$code" in
    404) echo "FREE  $1" ;;
    200) ;;                       # taken
    *)   echo "RETRY $1 (http $code)" ;;   # do NOT treat as free
  esac
}
export -f check
xargs -P 8 -I{} bash -c 'check {}' < wordlist.txt
```

Throughput scales with `-P`; at `-P 8` expect roughly an hour for tens of
thousands. Treat RDAP as a pre-filter only.

**Cloudflare `domain-check` for the truth and the price.** Batch limit is small
(20 at the time of writing — the API returns an explicit error if you exceed it,
so let it tell you rather than assuming):

```bash
curl -s -X POST \
 "https://api.cloudflare.com/client/v4/accounts/$ACC/registrar/domain-check" \
 -H "Authorization: Bearer $TOK" -H 'Content-Type: application/json' \
 -d '{"domains":["a.com","b.ai"]}'
```

Returns `registrable`, `pricing.registration_cost`, and `tier` — **`tier` is the
one to read**: a "free" `premium` `.com` can cost thousands. Works for any TLD
Cloudflare sells. Token needs `Account > Domain Registrar > Read`. The
`cloudflare-api` MCP needs OAuth and cannot be authorized in a non-interactive
session; use an API token.

Always re-verify finalists with Cloudflare. Never build on an RDAP-only result.

**ccTLD risk.** `.ai` is Anguilla, `.io` is British Indian Ocean Territory, `.co`
is Colombia. Country TLDs carry policy and renewal-price risk a gTLD does not,
and prices have been changed unilaterally before. Confirm current renewal price,
not just registration price.

## 6. Handles, registries, defensive registrations

Check in the same pass; free things go fast.

```bash
curl -s -o /dev/null -w '%{http_code}\n' https://api.github.com/users/<name>  # user
curl -s -o /dev/null -w '%{http_code}\n' https://api.github.com/orgs/<name>   # org
curl -s -o /dev/null -w '%{http_code}\n' https://registry.npmjs.org/<name>
```

Caveats: `404` on `/users/` does not mean the **org** name is free — check
`/orgs/` too, and GitHub reserves some names. A `404` on npm does not guarantee
you can publish: npm blocks names too similar to existing packages
(see `agentic-cli-npm-package` §5). Rate limits return `403`, not `404`.

Also check, as applicable: PyPI, crates.io, Docker Hub, Hugging Face, VS Code
Marketplace, Chrome Web Store, Slack App Directory. And the social handles —
note Instagram/TikTok/LinkedIn have their own length and character rules. X
blocks automated checks; verify by hand.

**Defensive registrations**: the obvious typos, keyboard neighbours, the plural,
and the `.net`/`.org`. Cheap now, expensive later. Watch for IDN/homograph
lookalikes if the brand is valuable.

## 7. Buy

See **`cloudflare-domain-launch`** for the full buy + deploy path. Two warnings:

- `POST /accounts/{acc}/registrar/registrations {"domain_name":"x.com"}`
  **executes immediately**. There is no dry-run and no confirmation step — a
  minimal body with only `domain_name` completes the purchase and charges the
  account. Do not send it as a schema probe.
- It is a **real financial transaction**. Surface the exact domain and price, get
  explicit human confirmation, call it once, then poll registration status until
  `state` is `succeeded` before wiring anything against the domain.

Turn **auto-renew on**. An expired-and-unrenewed domain sitting in redemption is
how good names come back on the market.

Then: `saas-brand-system` to build the brand system, `verify-branding` to audit it.

---

## Appendix — lanes that came back empty

One session, ~100,000 checks, `.com` at register price. This is a large sample,
not a proof; treat it as strong prior evidence rather than a law. Re-check before
relying on any single row.

| Lane | Result in that sample |
|---|---|
| Real English words, 4–11 letters | no availability found at any length tried |
| Root + real suffix (`-ery`, `-ry`) | good ones taken (`stewardry`, `makery`, `roostery`) |
| Random melodic coinage (10k sample) | 69% free — all unpronounceable |
| Latin/Greek plurals | `vivaria`, `scriptoria`, `armaria`, `tabularia` taken |
| Phonetic respellings (Lyft/Flickr style) | 0 of 50 (`hyve`, `krew`, `kamp`, `teem`) |
| Dahl-style nonsense | good ones taken; survivors unreadable |
| `get`/`use`/`try` + a good word | 24 of 1,085, all unusable (`getmallet`, `trychum`) |
| `agent<word>` | none found free |
| Kid compounds (`treehouse`, `beehive`) | taken |
| `-ify` / `-ly` (Spotify/Bitly) | `nestify`, `rootify`, `nestly`, `rootly` taken |
| Words containing `ai` | heavily mined; 4-letter `ai*` names 70/70 taken |
| Simple words in JP/FA/FI/EL | 0 of 111 |
| Famous ancient names | `kairos`, `argo`, `hestia`, `agora`, `simurgh`, `asha` taken |
| Simple words on `.ai` (392 sampled) | 2 free — `.ai` was no easier than `.com` here |

**Practical read:** a simple, one-word, kid-pronounceable `.com` at register price
is very hard to find, and the words stakeholders actually want are usually
five-figure-plus aftermarket. Get that on the table in round one.

## Related

**Skills**

- `cloudflare-domain-launch` — buy the domain, deploy the site, DNS/cert gotchas
- `saas-brand-system` — build the brand system once the name lands
- `verify-branding` — audit that the name and brand are applied consistently
- `ship-a-product` — the wider launch sequence (this is stage 0)
- `new-product-workspace` — overlaps on "name it"; run the company check here first
- `agentic-cli-npm-package` — npm naming rules and publish blocks
- `launch-seo` — exact-match vs brandable domain strategy follows from this choice
- `product-hunt-launch`, `saas-legal-docs` — both assume a settled name

**Not a skill**

- `vibebrand` (`github.com/itsryanarmani/vibebrand`) — npm package productizing
  `saas-brand-system`: 14 emotion-tagged directions, oklch tokens (light + dark),
  font pairings, generative logos, parametric mascot, CLI + SDK.
