# Speech-driven cuts: dead air and mistakes

Word-gap silence removal and review-gated mistake cuts, adapted from
herk-edit-kit (MIT + a custom use-permission note; see `sources.md`).
Both scripts take any `{words:[{text,start,end}]}` transcript — local
whisper output works. Verified 2026-11-12 in a local eval run; the
vendor clones and eval outputs were local-only and are not in this repo.

## 1. Make the word JSON from local whisper

```bash
ffmpeg -y -i input.mp4 -vn -ac 1 -ar 16000 work/audio.wav
whisper work/audio.wav --model small --output_format json \
  --word_timestamps True --output_dir work
```

whisper's JSON has keys `text`, `segments`, `language` — **no
`duration` key**. Words nest under `segments[].words[]` with key
`word`. Flatten it to the shape the cut tools want (`text`, `start`,
`end`) and nothing else:

```python
import json
src = json.load(open("work/audio.json"))
words = [{"text": w["word"].strip(), "start": w["start"], "end": w["end"]}
         for s in src["segments"] for w in s.get("words", [])]
json.dump({"words": words}, open("work/words.json", "w"))
```

Do not emit `audio_duration_secs`: `cut-silences.mjs` falls back to
`ffprobe` on `--video` for the source duration, which is the true
container length. An earlier draft of this doc wrote
`src["duration"]` — that raises `KeyError` on real whisper output
(reproduced 2026-11-12: `KeyError: 'duration'`).

Model choice: the first eval used `--model tiny` (fast, rough on names
and fast cuts). This fix-round run used `small` on the meltdown clip
and `tiny` on the sitcom clip; both are cached locally. Use `small` or
better for real ads.

## 2. Cut silences

```bash
node cut-silences.mjs work/words.json \
  --video input.mp4 --out-dir work/out --apply
```

Options (verified against the script): `--gap 0.55` (min pause to
trim), `--head-pad 0.22`, `--tail-pad 0.34`, `--output`, `--out-dir`,
`--apply` (renders via ffmpeg `libx264 crf 18`, `aac 192k`, faststart).
There is no keep-range flag — the tail is controlled only by
`--tail-pad`.

Outputs land in `--out-dir` (default: alongside the transcript):
`<stem>.silence-edl.json` (keep/delete ranges + reasons),
`<stem>.silence-transcript.json` (**words re-timed to the edited
timeline**), `<stem>.silence-decisions.md`, and the cut mp4.

This is word-gap driven, not loudness driven. It keeps deliberate breaths
in TTS narration that a loudness-only tool (auto-editor) would eat.
Copy the script into our tooling; do not depend on the vendor repo.
When copying, keep its MIT notice (`Copyright (c) 2026 Nate Herk`) and
the `licenses/PIPELINE-USE-PERMISSION.txt` notice with the file.

### Measured results (re-run 2026-11-12, fixed converter)

Clip lengths are ffprobe `format=duration` on the encoded files;
whisper `tiny` unless noted.

| Clip | Before (ffprobe) | After (ffprobe) | Change | Deletes |
|---|---|---|---|---|
| sitcom_v2.mp4 | 19.875 s | 13.808 s | -30.5 % | 6 ranges |
| sA_meltdown_v2.mp4 | 10.21 s | 8.70 s | -14.8 % | 1 range (tail) |
| sA_meltdown_v2.mp4, `--model small` | 10.21 s | 8.567 s | -16.1 % | 1 range (tail) |

The earlier draft of this table showed 20.62 s / 9.34 s "before" —
those were the last word end + 1.0 s written by the eval's converter,
not the clip length. The real before-lengths are above.

### The CTA tail trap (found in this re-run)

On `sA_meltdown_v2.mp4` the only delete was the tail trim
8.68–10.21 s. The CTA sound sits at ~10.0 s (`last_sound_s` in the
local videos5 sync QA, a 2026-11-12 artifact not in this repo), inside
that deleted range — the cut dropped the last
~1.5 s and with it the call-to-action audio. `pacing.md` rule 7 says
the CTA must be held ~2 s; a transcript-only tool cannot see a
non-speech sting, so:

- **Rule:** the last keep range must extend to the end of the CTA/last
  sound, not just past the last word. Before `--apply`, measure where
  the last non-speech sound ends (the sync-QA `last_sound_s` check in
  `qa.md`, or `silencedetect` on the stem) and compare it to the EDL's
  last `keep_ranges` end.
- **Check:** after rendering, `last_sound_s` on the output must still
  cover the CTA. If the tail trim removed it, the edit fails.
- **Protection:** raise `--tail-pad` so `last_word_end + tail_pad`
  reaches past the CTA end (there is no explicit keep flag).
  Verified: `--tail-pad 2.0` on the meltdown clip produced 0 delete
  ranges and kept all 10.21 s. Alternatively cut the CTA region by
  hand afterwards, or accept the trim only when the CTA is speech the
  transcript actually saw.

### Synthetic re-run

A 12 s testsrc2+sine clip with a hand-written 9-word JSON containing
three ~2 s gaps went to 4.44 s (-63 %), 4 delete ranges, rendered mp4
verified by ffprobe — **a run made while writing this skill**, not an
independent eval.

## 3. Cut mistakes (review-gated)

```bash
node find-cut-candidates.mjs work/out/<stem>.silence-transcript.json \
  --out-dir work/out
# review each candidate in context; write approved-cuts.json as
# {"cuts":[{"start":<s>,"end":<s>,"reason":"..."}]} on the SAME timeline;
# then:
node apply-cuts.mjs work/out/<stem>.silence-transcript.json \
  --cuts approved-cuts.json \
  --video work/out/<video-stem>.silenced.mp4 \
  --out-dir work/out-mistakes --apply
```

`apply-cuts.mjs` usage is `<transcript.json> --cuts <approved.json>
[--video ...] [--output ...] [--out-dir ...] [--apply]`. The earlier
draft omitted `--cuts`, which fails with "no --cuts file given", and
showed no `--apply`, which renders nothing. Both fixed and exercised
2026-11-12: one hand-approved 0.6 s false-start cut on the silenced
meltdown clip rendered 8.68 s → 8.08 s.

- Feed step 2 the **re-timed** transcript. Never mix original and edited
  timestamps.
- The finder is mechanical: stutters, repeated words, false starts,
  retakes. It emits candidates with context and a reason. On our clean
  TTS-narrated clips it found 0 candidates; **stutter/retake detection
  was read but not exercised on real retakes** — validate it on a
  talking-head take before trusting it.
- A person or review step approves each cut. Intentional repetition is
  not a mistake. `apply-cuts` renders only approved ranges (an empty
  `cuts` array is valid and renders the input unchanged).
- For TTS-narrated ads there are usually no spoken mistakes; the silence
  cut alone is the common case. The mistake scan earns its keep on real
  talking-head takes.

## Traps

- Word JSON key is `text` for these scripts. Other tools differ —
  OpenMontage's subtitle_gen wants `word`. Normalize once at ingest.
- `--apply` renders into `--out-dir` (default: alongside the inputs),
  not next to the video unless `--out-dir` points there.
- Dead-air detection without a transcript exists (ffmpeg
  `silencedetect`, verified in the eval) but found nothing on our
  produced clips — their audio beds are continuous. Speech-gap cutting
  needs the transcript.
