---
name: ad-lofi-ugc
description: "Make cheap lo-fi UGC-style ad creatives and short video ads that read as real phone photos, not ads. Covers the camera-and-era-first image prompt rule, the exact ffmpeg degrade recipes that turn clean AI stills into 2000s camera-roll photos and video, one consistent synthetic character across clips (character bible + last-frame chaining), muted-first sound design (voiceover, ambient bed, ffmpeg SFX), and the QA gates that catch the real failures (objects that change identity, rotated images, garbled text, policy violations, runaway spend). Use when asked for UGC ads, lo-fi ads, fake-phone-photo creatives, TikTok/Reels-style video ads, cheap ad batches on a small budget, or 'make it look like a real person filmed it'. Pair with ad-creative-generation for clean photoreal stills, ad-image-prompt-library for text-exact HTML formats, and ad-video-styles for polished generated-footage styles."
---

# ad-lofi-ugc

A repeatable workflow for lo-fi UGC ad creative: stills and short vertical video
that look like a real person shot them on an old phone. Built and measured on a
real campaign run in November 2026. Total creative spend for a 12-image + 5-clip
batch was under $1.00.

The look is the product. A clean, glossy AI image reads as an ad and gets
scrolled past. A grainy 2004 point-and-shoot photo with a crooked horizon reads
as a camera roll and earns the second look. Everything here serves that.

Pairs with:

- `ad-creative-generation` — clean photoreal stills, reference-image rules,
  vision QA on un-degraded output.
- `ad-creative-templates` / `ad-image-prompt-library` — text, captions, UI and
  end cards. Never let the image or video model paint text (see
  `references/prompts-images.md`).
- `ad-video-styles` — a different family: polished generated footage with
  static overlay type. Use this skill when the goal is "looks amateur on
  purpose".
- `ad-video-editing` — the fast-cut post stage: dead-air removal, pacing,
  SFX on cuts, captions and render QA for the finished video.
- `ad-experiments` — how to size budget and read results once ads ship.

## The pipeline, in order

1. **Find the format.** Mine a free viral-format library for structures that
   already work. A person can browse `darkugc.com` by hand; see the
   format research section below for the rules.
2. **Write the character bible** if a person recurs. One paragraph, pasted
   verbatim into every prompt. See `references/characters.md`.
3. **Generate stills** with the camera-and-era-first prompt rule. See
   `references/prompts-images.md`.
4. **QA the stills**: orientation, hands, objects, no text. See
   `references/qa.md`.
5. **Degrade** each still with the ffmpeg recipe. This is what makes it lo-fi.
   Same file.
6. **Animate** with image-to-video motion prompts kept deliberately small. See
   `references/prompts-motion.md`.
7. **Chain shots** by feeding each clip's last frame into the next shot. See
   `references/characters.md`.
8. **Add sound last, and design muted-first.** The video must work with sound
   off. See `references/sound.md`.
9. **Run the QA gates**: object continuity, mute test, policy lint, spend
   meter. See `references/qa.md`.
10. **Log every prompt and every billed call.** The prompt file is how the
    next run repeats this one.

## Non-negotiable rules

- **Camera and era first, then subject and moment, then flaws, then
  negatives.** That order is what made the prompts work. Full rule and the
  exact prompts in `references/prompts-images.md`.
- **The model never paints text.** Captions, headlines, lower-thirds and end
  cards are HTML renders or ffmpeg overlays added after generation. Blank
  signs, taped notices and "no readable text" prompts still produced garbage
  letters twice; the fix is to keep text out of the frame entirely.
- **Keep motion small.** Tiny shake, slow push-in, one continuous shot. Every
  time we asked for more (walking, cuts, zooms) the model invented people,
  phones and morphs.
- **Muted-first.** Captions carry the story; sound is a bonus layer. Export a
  `_muted.mp4` of every video as proof.
- **One writer per spend log.** Two workers racing one `spend.json` clobbered
  each other's entries. Lock the file, price-check before every call, hard-cap
  the batch. Details in `references/qa.md` and `references/failures.md`.
- **Strip PII before anything ships.** No real names, account ids, keys,
  wallet balances or private domains in prompts, logs or this repo.

## Format research: viral-format libraries

`darkugc.com` is a free public library of viral short-form ad videos with view
counts. Its terms ban scraping, bulk download and any automated access to the
site or its API, including bots, scripts, headless browsers and "AI agents".
Follow them.

- Human use: a person opens `https://darkugc.com/`, sorts by Views, and filters
  by category and format family. Brand pages exist per advertiser. The person
  notes the story structure by hand.
- Agent use: only through the route the site names for agents, its MCP server
  at `https://darkugc.com/mcp`, with a free account the owner signs in to.
  `https://darkugc.com/llms.txt` states the AI policy. Read it first.
- Never send a fake `User-Agent` or `Referer` to get past a block. A block is
  a no. Do not call `/api/` paths directly, and do not save bulk copies of
  its data. The site's `robots.txt` disallows `/api/`.
- When the MCP route is not set up, use other sources: the open-source prompt
  and hook repos in `references/providers.md`, and the ad libraries run by the
  platforms (for example the Meta Ad Library API).

Copy the structure, never the footage, the face, the words or the music. A
library is inspiration, not source material.

## Cost shape (measured, 2026-11-12/13)

| Step | Model | Price | Verified |
|---|---|---|---|
| Stills | `bytedance/seedream-v5.5` @1.5k on WaveSpeed | $0.02/image | yes |
| Image-to-video | `wavespeed-ai/wan-2.2/i2v-480p-ultra-fast` | $0.01/s ($0.05 per 5 s clip) | yes |
| TTS voiceover | cheapest decent WaveSpeed TTS | per-call, check first | partially |

Full provider table with alternates and unverified marks:
`references/providers.md`. Every price must be re-checked on the day; prices
and model ids change.

## References

- `references/prompts-images.md` — prompt structure rule, exact working
  prompts, ffmpeg degrade recipes for stills and video.
- `references/prompts-motion.md` — image-to-video motion prompts that worked,
  and what to keep small.
- `references/characters.md` — character bible method, anchor contact sheet,
  last-frame chaining.
- `references/sound.md` — voiceover, ambient bed, ffmpeg SFX, muted-first
  design.
- `references/owner-feedback.md` — 18 numbered owner rules (R1 to R18) and the cost ratchet. The reviewer checks each one.
- `references/qa.md` — continuity check, mute test, orientation check, policy
  lint, spend meter.
- `references/providers.md` — cheapest working models and prices, dated and
  marked verified or unverified.
- `references/failures.md` — every failure hit and the fix.
