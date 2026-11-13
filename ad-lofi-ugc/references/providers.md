# Providers: cheapest working models

Prices checked 2026-11-12/13 unless noted. Re-check on the day — prices and
model ids change, and a gateway can silently swap a model. "Verified" means
confirmed on the provider's own page or live catalog that day; "unverified"
means seen only via a third-party catalog or not confirmed.

## What we actually used (verified)

| Job | Provider / model | Price | Notes |
|---|---|---|---|
| Stills | WaveSpeed `bytedance/seedream-v5.5` @1.5k | $0.02/image | Produced the whole 12-ad lo-fi batch. Price read from live model page + catalog `base_price`. |
| Image-to-video | WaveSpeed `wavespeed-ai/wan-2.2/i2v-480p-ultra-fast` | $0.01/s ($0.05 per 5 s clip) | Cheapest 9:16-capable i2v in the catalog that day. Accepts first frame + last frame for chaining. |
| Uploads | WaveSpeed `/api/v3/media/upload/binary` | free | Use `curl -F file=@...`; urllib multipart was flaky. Returns a `download_url` for the job. |

Measured batch cost: 26 image calls = $0.52; 6 video calls = $0.30. Well
under the caps.

## Alternates (verified prices, unproven for this workflow)

From the same-day pricing research. Prices are list prices; per-call routes
like `treg.to` or Apify can be cheaper still.

| Job | Option | Price | Verified |
|---|---|---|---|
| Images (budget) | fal.ai FLUX.1 schnell | ~$0.003/MP | yes |
| Images (budget) | WaveSpeed Z-Image Turbo | $0.005/image | yes |
| Images (sweet spot) | fal.ai Nano Banana | $0.0398/image | yes |
| Images (alt) | WaveSpeed Nano Banana 2 | $0.045/image | yes |
| Images (premium) | fal.ai Nano Banana Pro | $0.15/image | yes |
| Video (volume drafts) | fal.ai PixVerse V6 | $0.005/s | yes |
| Video (balanced) | WaveSpeed Wan 3.0 or Veo 3.1 Lite | ~$0.05/s | yes |
| Video (hero) | WaveSpeed Seedance 2.5 | $0.18/s | yes |
| Video (mid) | fal.ai Kling v2.5 turbo / v2.6 | $0.07/s | yes |
| Scraping (ad libraries) | treg.to / Apify pay-per-call | ~$1–3/mo at ~500 ads | yes |
| Scraping (free) | Meta Ad Library API, TikTok Creative Center, Google Ads Transparency | $0 | yes |

## Explicitly unverified on 2026-11-12

Do not treat as firm:

- ScrapeCreators' own per-call USD price (only a third-party catalog quote).
- Monid per-endpoint prices for ad-library tools.
- Google-direct Veo 3.1 Lite/Fast prices (third-party quotes only).
- Replicate video prices beyond two entries on its pricing page.
- WaveSpeed TTS per-call price for voiceover — check the catalog before the
  batch; it was not confirmed.

## Rules for any provider

- Read the balance before a batch, but meter spend in your own locked log —
  other workers may share the key.
- Confirm the model id in the job result; gateways retire and swap models.
- Inspect the endpoint's input schema and price before the first paid call.
- Keep the API key in the environment or a secrets file; never in prompts,
  logs, commits or this repo.

## Editing tools and sound sources (verified 2026-11-12 with `gh api`; stars and dates change)

| Tool | License | Use |
| --- | --- | --- |
| `heygen-com/hyperframes` | Apache-2.0 | Write HTML, render MP4. Timeline, zoom keyframes, captions. Skills exist for agents. |
| `kurbaitaev/ghost-editor` | MIT | A Claude skill that turns raw takes into fast-cut reels. Ships recipes and a sound library. |
| `WyattBlue/auto-editor` | Unlicense | Cuts silence and dead air by loudness and motion. |
| `KyaniteLabs/kinocut` | Apache-2.0 | Guarded video-editing MCP server. |
| `ggerganov/whisper.cpp`, `SYSTRAN/faster-whisper` | MIT | Word-level timestamps for pop captions. |

Sound effects: the ghost-editor library lists a source and a license for every file in `library/sfx/manifest.json`. 27 files are CC0 from Freesound (deep boom, record scratch, whip crack, riser, glass break). 51 are Mixkit files that are free for ads but must not be redistributed, so keep them out of repos. The manifest is the claim, so check a file's Freesound page before you rely on it in a paid ad. Never use a recording of a real show as a laugh track.

