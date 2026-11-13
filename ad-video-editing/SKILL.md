---
name: ad-video-editing
description: "Fast-cut editing for short ad videos (TikTok, Reels, Shorts; about 10-30 s). Covers removing dead air and word-gap silences from word-level transcripts, review-gated mistake cuts, punch-in zooms and whip transitions, sound effects placed on cuts and events, word-by-word caption timing from local whisper, and post-render QA (determinism, flash/freeze/black frames, -14 LUFS loudness, A/V sync). Use when asked for a fast-cut edit, punch-in zoom, remove dead air, tighten the pacing, caption timing, sound effects on cuts, a TikTok edit, or to turn raw clips plus voiceover into a punchy ad."
---

# ad-video-editing

A repeatable post-production workflow for short vertical ads — generated clips,
voiceover lines and SFX into a fast, loud, captioned ad that passes QA. For
footage see `ad-lofi-ugc` or `ad-video-styles`. Verified November 2026.

## Workflow

1. **Transcribe.** Extract 16 kHz mono audio, run local whisper with word
   timestamps, convert to the `{words:[{text,start,end}]}` JSON the cut
   tools take. See `references/speech-cut.md`.
2. **Cut dead air.** Run the word-gap silence cutter. It emits an EDL, a
   re-timed transcript and the cut video. For TTS-narrated ads this is
   usually the only speech cut needed.
3. **Scan for mistakes (review-gated).** Find stutters, retakes and false
   starts. Show each candidate to a person or review step. Apply only the
   approved cuts with `apply-cuts.mjs --cuts`, always on the re-timed
   transcript. Same reference.
4. **Set the pace.** Put the hook in the first second, cut every 0.8-2 s,
   keep voice at normal speed and speed up the picture instead, land one
   whoosh, end with under 0.3 s of tail. See `references/pacing.md`.
5. **Place sound on events.** Search the OpenFilm CC0 library for a whoosh,
   impact or transition — on events and reveals only, never one per cut.
   SFX sit under the voice. See `references/library.md`.
6. **Time the captions.** Word-by-word captions come from the whisper word
   timestamps on the final timeline, not estimates.
7. **Render.** Deterministic timeline, one paused clock. ffmpeg
   `filter_complex` for flat cuts, HyperFrames for composed ads.
8. **Run post-render QA.** Determinism double-draw, flash/freeze/black
   scan, loudness to -14 LUFS, silence and tail checks, caption timing,
   mouth-sync spot check. See `references/qa.md`.

## Non-negotiable rules

- **The timeline comes from measured voice lines, not fixed shot lengths**
  — fixed shots left dead gaps in the first fast-cut attempt.
- **Never mix timestamp domains.** After a silence cut, all downstream steps use the re-timed transcript only.
- **Review before applying.** Mistake cuts are proposals until approved; intentional repetition is not a mistake.
- **Keep the CTA.** Last keep range must reach the end of the CTA sound, not just the last word — a tail trim can drop a non-speech sting.
- **Do not copy code from OpenMontage** — AGPL-3.0, ideas only; write our own. See `references/sources.md`.
- **Keep `packages/openfilm/library/LICENSE.md` with any OpenFilm asset** — library CC0, emoji stickers MIT.
- **Pin the OpenFilm version.** Do not run `npx openfilm@latest`.
- **Listen once before shipping** — the numbers in `qa.md` do not prove an effect fits the picture.

## References

- `references/speech-cut.md` — silence/mistake cuts: commands, results, transcript conversion.
- `references/pacing.md` — measured pacing rules and their evidence.
- `references/library.md` — OpenFilm CC0 library: contents, search, take, license, pinning.
- `references/qa.md` — post-render checks on the encoded file.
- `references/sources.md` — repo audit: stars, licenses, adopt vs not. Verified 2026-11-12.
