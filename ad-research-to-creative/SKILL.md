---
name: ad-research-to-creative
description: "Plan paid ads for any site or product from public competitor data: pull live Meta ads, rank by run length, pick angles and a persona, write scripts, build landing pages and short video ads, then hand off to a small test. Use before spending on ads for a new project, or when asked to research existing ads, make a spokesperson persona, or build a VSL or landing page per ad."
---

# ad-research-to-creative

One repeatable path from "we should run ads" to a paused, tracked test. Each step has an output file. Do not skip to creatives.

## 0. Check the economics first
- Compute cold CAC = CPC / click-to-purchase rate. Compare it with gross profit per order, not with revenue: take the price, then remove payment fees, refunds, the cost of making or delivering the product, and any other per-order cost. A digital guide keeps most of its price, but fees and refunds still count.
- Assume a guide under $100 will not pay back on the first order, and check that with your own numbers. Plan the ladder: free checklist, guide, kit, back end.
- Mark every benchmark as an assumption until the first $300 of spend replaces it.
- Check policy risk. A ban on an unverified Meta portfolio stops every site. Start with low-risk niches.

## 1. Research live ads (read-only, about $0.10)
Script: `ad-research OUTDIR US 3 "keyword" ...` from the `scripts` repo (treg, about $0.0019 a page). Run it from a clone of that repo.
- Use 8-10 keywords: the buyer's words, the builder's words, and the education words ("guide", "checklist").
- Keyword search is loose. Filter the result to ads that name the topic. Half the raw hits are noise.
- Meta hides spend on commercial ads. **Run length is a weak signal.** An ad can stay active while it loses money, so use it to rank ads and pick which to study, never as proof that an ad pays.
- Group by advertiser. Count ads per advertiser, formats and CTAs.
- Deep-pull one advertiser's full ad set with Apify `apify~facebook-ads-scraper` (about $0.005 an ad, free plan has a $5 cap). Use `view_all_page_id=<page_id>` in the Ad Library URL.
- Look for the nearest guide or lead-magnet ads. They are the closest model for the offer.
- The advertisers are also the B2B prospect list: a business that pays for lead ads can pay for a Featured listing.

Auth notes:
- Keys come from the environment (`APIFY_TOKEN`, `TREG_TOKEN`) or a local env file kept outside the repo. Never print them.
- The treg MCP key can expire while the `treg` CLI still works. Use `treg call`, `treg balance`.
- A free-plan Apify token still works for small pulls.

Output: `summary.md`, `ads.csv`, `builder-prospects.csv`.

## 2. Pick angles
- Name the patterns that run long: pain hook ("Tired of..."), local callout, one-day or one-step promise, free tool, price anchor.
- Pick 3 to 5 angles. Write one hypothesis each: audience, hook, offer, what result means a win.
- Follow `ad-experiments`: one audience, one geo, one creative per test.

## 3. Persona
- One spokesperson per site. A guide host, never a fake customer.
- Image: WaveSpeed `wavespeed-ai/jib-mix-qwen-image/text-to-image` ($0.02). Prompt: no name tag, no text, alone in frame, no hands. Naming the persona in the prompt makes a name tag appear.
- Make two options. Review before any video spend.
- **Identity comes from the image, not the prompt.** A prompt rebuilt from a chosen image gives the same style but a different face. Once the owner picks a face, keep that image as the reference, in a private place. Make new poses, outfits and backgrounds with the edit model ($0.02, `images` must be an array). The recipe is in `personas/persona-recipe.json`.
- Keep outfits polished and fitted. Meta rejects ads that read as sexually suggestive, and repeated rejections can restrict the ad account. A warm smile and eye contact carry the appeal.
- No data says that one hair or eye color sells more. Test two faces against each other.
- Faces look alike across sites unless the prompt changes age, hair and style. Vary them.
- Video: HeyGen (check the vendor's current API version first) or WaveSpeed lipsync (about $0.10 for a 5 s clip at 480p and about $0.15 at 720p; the model accepts 5 to 20 s of audio per clip and its billing floor can differ from that, so price a clip with `wavespeed price` and measure one real run from the balance). A personal brand should use the real person, not a character.

## 4. Scripts and creatives
- Script shape, 20 to 35 seconds: hook (2 s), pain, one fix, proof from the guide itself, free next step.
- Use only claims the product contains. No invented testimonials, stats or "worth $X" stacks.
- Do not clone a competitor's people, marks or exact copy. Copy the pattern, not the words.
- Use `ad-creative-generation` for still images and `ad-creative-templates` for layouts.

## 5. Landing page per angle
Build the page the ad sends people to, before you build the ad. A bare product page loses the visitor the ad just won. Capture the current page at phone width (430 px) first, and compare.

Two destination types:
- **Free guide (Lead):** headline that repeats the ad hook, the video, one email field, the full list of what is inside, a quiet link to the paid offer.
- **Paid offer (Purchase):** the sales page below.

Order on a phone: kicker, headline, one sentence, **video**, button. The headline must be on the first screen, so do not put the video first.

Sales page order: hero (headline, video, button, three ticks) -> trust strip (counts and sources that are true) -> the cost of the problem (four short pains) -> before and after -> what is inside (one card per document, with what it does) -> a real excerpt from the product, as text -> the guide host in two sentences -> options side by side (free, mid, full), with the full one marked -> questions (objections only) -> final button. A sticky button bar on phones.

Rules:
- Only true proof: real counts, real excerpts, named public sources. No invented testimonials, no fake scarcity or countdowns.
- The price goes on the page, never in the video.
- Do not promise results. Promise the order of work and the documents.
- Match the ad hook in the first line.
- Flag owner decisions, such as currency.
- Preview locally at 430 px and at desktop width before anything goes live. Check that the buy form, the free form and every link work in the real build.

## 6. Tracking, then launch
- Verify pixel and Conversions API events: ViewContent, Lead, InitiateCheckout, Purchase. The event names, ids and tweaks are in `ad-conversion-hub` (section "Event ladder for a small ad test"). Key names and credentials are in `ad-platform-credentials`.
- Read the pixel with `GET /{pixel_id}/stats?aggregation=event&start_time=<unix>&end_time=<unix>` (give a time range). Fire a test event first.
- Check business verification before spend. The status is in Business settings, Security centre.
- Build the campaign paused. Show the owner the exact settings. The owner approves the budget.
- Start with a small test, about $300 to $600 for a guide priced under $100. Set the stop line before launch from the economics: the rules differ by goal. A **Lead test** stops when spend reaches about 3 times the target cost per Lead with zero Leads. A **purchase test** stops when spend reaches about 3 to 5 times the profit left on one order after all per-order costs with zero purchases, even if some Leads came in, and it also stops if Leads come in but none buy after the same spend. The owner's cap wins when it is lower.

## Worked example
A directory site, 2026-11-10: about 800 live ads read for one topic, 33 contractor advertisers found, one free-guide ad in the whole set, and no guide ads aimed at the premium segment. Keep project names, products and hooks in a private notes file, not here.

## Ranked Meta ad formats — cross-reference
For the 12 ranked formats, ROAS ranking table, WaveSpeed model picks, and creative rules, see [`ad-creative-templates/impulse-formats.md`](../ad-creative-templates/impulse-formats.md). That shared reference contains the ranked table, launch-first rotation rule, WaveSpeed CLI usage (key from `WAVESPEED_API_KEY` only), and the creative rules (blurry lo-fi 2000s phone-photo people; no header/footer/logo; never text-only; plain STE-100 copy; no invented testimonials). Economics ladder (free checklist → guide → kit) cross-references the ROAS ranking. WaveSpeed model picks from `impulse-formats.md` §3. Creative rules from `impulse-formats.md` §4 restated.
