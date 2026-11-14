# Ranked Meta Ad Formats — Impulse Guides & Directory Lead Gen

**Researched:** 13 November 2026.
**Scope:** Cheap impulse purchases (CA$5–CA$30 guides on Stripe) and niche directory lead gen.
**Economics median:** Meta median ROAS 1.88, CPM $15.06, CTR 2.39% (Triple Whale Aug 2025–Jul 2026). A $19 guide often does not pay back on the first order — plan a ladder (free checklist → guide → kit / featured listing).

---

## 1. The 12 Ranked Formats

| Rank | Format | Best fit | Ship with |
|---:|---|---|---|
| 1 | **Notes app / honest screenshot** | Impulse guide, also lead gen | HTML template (Notes UI) |
| 2 | **iMessage / SMS thread** | Both, especially impulse | HTML template (chat bubbles) |
| 3 | **Lo-fi UGC selfie / phone talking-head** | Both | Seedream 5.5 + ffmpeg degrade |
| 4 | **Blurred lead-magnet / PDF screenshot** | Impulse guide | HTML + CSS blur |
| 5 | **Native organic post (candid still + long primary text)** | Lead gen first, also guides | Seedream 5.5 / Z-Image + degrade |
| 6 | **Whiteboard / post-it / handwritten** | Impulse guide | Photo + handwriting overlay |
| 7 | **Us-vs-them / comparison** | Directory lead gen, also guides | HTML split layout |
| 8 | **Before / after (no fake results)** | Both (truthful only) | Seedream pair or HTML diptych |
| 9 | **Zack D. Films-style explainer (video)** | Impulse guide (mechanism) | Nano Banana 2 Lite stills + Wan/Seedance |
| 10 | **Stickman explainer** | Impulse guide, also lead gen | Recraft Flash (9:16) |
| 11 | **Meme / native joke static** | Cold awareness, then retarget | HTML over generated/original photo |
| 12 | **ChatGPT (or similar) chat-reveal** | Impulse guide | HTML template |

**Honorable mention (not in top 12):** Checklist static — if not already covered by Notes app or screen checklists, worth a later test as a generic "things to send a contractor" format.

---

## 2. ROAS Ranking & Launch-First Rotation

### Condensed ROAS Ranking (from research benchmarks)
- **Notes / iMessage / blurred statics** — highest CTR, lowest CPA among static families (native UI, low cognitive load)
- **Lo-fi UGC selfie** — +59% link CTR vs polished static (DataAlly), about level CPA, +5% ROAS
- **Whiteboard / handwritten** — pattern-break, educational, moderate CTR, good for consideration
- **Us-vs-them / comparison** — strong for directory lead gen (self-qualifies in one glance)
- **Before / after** — instant story, but only when claims are truthful and documented
- **Zack D. / Stickman** — lower hit rates (Motion 2026: animation class 4.57%), test not scale
- **Meme / ChatGPT** — top-of-funnel attention only; single-ad tests, not full ad set

### What to actually launch first (CA$50 directory cap, 50–100 impressions per ad set)

| Wave | Formats | Details |
|---|---|---|
| **1st wave** | Notes, iMessage, blurred guide screenshot (HTML statics, 4:5 and 9:16), **plus one lo-fi UGC selfie** (Seedream 5.5 + degrade) | Cheapest, most on-brief for $5–$30 impulse. Deliver 50–100 impressions quickly. |
| **1st swaps** | One us-vs-them HTML static (each directory) + one whiteboard still with overlaid handwriting (each guide) | Add after first-wave ads deliver. |
| **2nd wave** | Zack D and stickman, **once statics are delivering** | Start with stickman 9:16 (Recraft Flash, under $0.01) using same script as Zack D cut. Promote only the script that holds watch time. |
| **Single-ad tests** | Memes and ChatGPT | Not a full ad set. Test one ad each, then retarget. |
| **Kill gate** | Judge on CTR, CPC, and landing-page views against pre-written kill gate. Do not claim ROAS winner until Stripe purchases or verified leads exist. If CTR is healthy and sales/leads are zero, stop swapping formats and fix the landing page. | (`ad-experiments`, `ad-auto-optimizer`) |

---

## 3. WaveSpeed CLI Usage

**Key only from `WAVESPEED_API_KEY` environment variable.** Never print it, never hardcode it.

The WaveSpeed CLI reads `WAVESPEED_API_KEY` from the environment. Export it, then run:

```bash
# WAVESPEED_API_KEY must already be set in the environment
wavespeed run bytedance/seedream-v5.5 \
  -i prompt="A friendly 30s adult standing in a sunlit kitchen, natural light from window at left" \
  -i aspect_ratio="4:5" \
  -i resolution="1.5k"
```

### Model picks (from research, checked 13 Nov 2026)

| Purpose | Model | Price | Notes |
|---|---|---|---|
| Photoreal stills (default) | `bytedance/seedream-v5.5` | $0.02/image | Skill-verified. `aspect_ratio` `4:5` or `9:16`, `resolution` `1.5k`. |
| Cheap photoreal batches | `wavespeed-ai/z-image/turbo` | $0.005 | `size` e.g. `1024*1280` (4:5, below 1536 cap). |
| Faces / persona stills | `wavespeed-ai/jib-mix-qwen-image/text-to-image` | $0.02 | From `ad-research-to-creative`. No name tag, no text, no hands. |
| Illustration, stickman, flat graphic | `recraft-ai/recraft-v4.1-flash/text-to-image` | $0.008 | `aspect_ratio` only: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`. Use `9:16`. |
| Short on-image words (last resort) | `ideogram-ai/ideogram-v3-turbo` or `bytedance/seedream-v4.5` | $0.03 / $0.04 | Seedream 4.5 is typography-optimized. Still QA every letter. Prefer HTML. |
| 3D / Zack D stills | `google/nano-banana-2-lite/text-to-image` | $0.04 | Good prompt-following, flexible ratios including `4:5` and `9:16`. |
| Image-to-video | `wavespeed-ai/wan-2.2/i2v-480p-ultra-fast` | $0.01/s | Keep motion small (`ad-lofi-ugc`). |
| Cleaner video, if needed | `bytedance/seedance-v1-pro-fast/image-to-video` | ~$0.012+ | Used in `ad-video-styles`. |

**Common generate pattern** (same env rule):

```bash
# WAVESPEED_API_KEY must already be set in the environment
wavespeed run bytedance/seedream-v5.5 \
  -i prompt="PROMPT" \
  -i aspect_ratio="4:5" \
  -i resolution="1.5k"
```

After any photoreal still, run the ffmpeg degrade in `ad-lofi-ugc/references/prompts-images.md` so it reads as a camera-roll photo, not an AI render.

---

## 4. Creative Rules (restated once, linked elsewhere)

- **Blurry lo-fi 2000s phone-photo people** — the look is the product. Grain, crooked horizon, faded warm 2014 colour, on-camera flash, imperfect framing.
- **No header/footer/logo** — never put a brand logo or app header in the image model; render UI in HTML/CSS instead.
- **Never text-only** — always pair a visual with copy; image models garble exact text/logos/UI.
- **Plain STE-100 copy** — simple, factual body copy; no invented testimonials, stats, or "worth $X" stacks.
- **No invented testimonials, reviews, ratings, or stats** — real data only (see `ad-creative-templates` §6, `ad-research-to-creative` §6).
- **No fake interface** — no fake buttons, fake notification badges, or fake platform marks.
- **No deceptive pricing** — price must match landing page; no "was" price you never charged.
- **Check Meta's current rules on labelling AI-generated images** before launch.

**Cross-links:** HTML-mockup formats (iMessage, Notes, ChatGPT, lock-screen) belong in `ad-creative-templates` and `ad-image-prompt-library` Part A. Lo-fi UGC pipeline belongs in `ad-lofi-ugc`. Truthfulness rules across all skills: `ad-creative-templates` §6, `ad-research-to-creative` §6, `ad-experiments` truthfulness gate.

---

## 5. How the Existing Skills Link In

Each of the seven skills below now has a brief section pointing to this shared reference, so an agent loading any skill finds the formats without duplicating the table.

| Skill | Link / Patch |
|---|---|
| `ad-creative-templates` | See `impulse-formats.md` §1–§4 for ranked formats, rotation rule, WaveSpeed model picks, and creative rules. Existing template catalog (iMessage, Notes, ChatGPT) remains the canonical pipeline for HTML-mockup formats. |
| `ad-image-prompt-library` | Part A (HTML-mockup) recipes remain. Part B (AI-image-gen) prompts now cross-reference `impulse-formats.md` §3 for model picks and `ad-lofi-ugc` for camera-and-era-first degrade. |
| `ad-lofi-ugc` | Camera-and-era-first prompt rule extended and cross-linked (no overwrite of verified model notes). ffmpeg degrade recipe referenced. Model picks from `impulse-formats.md` §3. |
| `ad-research-to-creative` | Economics ladder (free checklist → guide → kit) cross-references the ROAS ranking. WaveSpeed model picks from `impulse-formats.md` §3. Creative rules from `impulse-formats.md` §4 restated. |
| `ad-creative-generation` | Image-model mechanics cross-reference `impulse-formats.md` §3 for model picks and creative rules §4. The template-vs-gen division is reinforced: text/UI/logo-heavy formats → HTML templates; photoreal scenes → this skill. |
| `ad-experiments` | Kill gate from rotation/launch-first rule cross-references `impulse-formats.md` §2. Budget sizing ($50 reads CPC/CTR, not ROAS) from `impulse-formats.md` §2. |
| `ads-meta` | Tracking setup cross-references the honesty rules in `impulse-formats.md` §4. No fabricated testimonials/spin. |

---

**Dedup note:** The 12 ranks, ROAS table, WaveSpeed model picks, and creative rules live in `impulse-formats.md` only. The seven skills each contain a short cross-link so an agent can find the formats from any entry point, without pasting the same table seven times.