# Speech-driven cuts: dead air and mistakes

Word-gap silence removal and review-gated mistake cuts, adapted from
herk-edit-kit (MIT + use-permission note; see `sources.md`). Both
scripts take any `{words:[{text,start,end}]}` transcript — local
whisper output works. Verified 2026-11-12 in a local eval run (vendor
clones and eval outputs were local-only, not in this repo).

## 1. Make the word JSON from local whisper

```bash
ffmpeg -y -i input.mp4 -vn -ac 1 -ar 16000 work/audio.wav
whisper work/audio.wav --model small --output_format json \
  --word_timestamps True --output_dir work
```

whisper's JSON has keys `text`, `segments`, `language` — **no
`duration` key**. Words nest under `segments[].words[]` with key
`word`; flatten to `text`/`start`/`end` and nothing else:

```python
import json
src = json.load(open("work/audio.json"))
words = [{"text": w["word"].strip(), "start": w["start"], "end": w["end"]}
         for s in src["segments"] for w in s.get("words", [])]
json.dump({"words": words}, open("work/words.json", "w"))
```

Do not emit `audio_duration_secs`: `cut-silences.mjs` falls back to
`ffprobe` on `--video` for the true container duration; `src["duration"]`
raises `KeyError` on real whisper output (reproduced 2026-11-12).

Model choice: `tiny` is fast but rough on names and fast cuts (first
eval); `small` ran on the meltdown clip in the fix round. Use `small`+ for real ads.

## 2. Cut silences

```bash
node cut-silences.mjs work/words.json \
  --video input.mp4 --out-dir work/out --apply
```

Options (verified): `--gap 0.55` min pause to trim, `--head-pad 0.22`,
`--tail-pad 0.34`, `--output`, `--out-dir`, `--apply` (ffmpeg
`libx264 crf 18`, `aac 192k`, faststart). No keep-range flag — the tail is set only by `--tail-pad`.

Outputs land in `--out-dir` (default: alongside the transcript):
`<stem>.silence-edl.json` (keep/delete ranges + reasons),
`<stem>.silence-transcript.json` (**words re-timed to the edited
timeline**), `<stem>.silence-decisions.md`, and the cut mp4.

This is word-gap driven, not loudness driven — it keeps deliberate
breaths in TTS narration that auto-editor would eat. Copy the script
into our tooling; when copying, keep its MIT notice (`Copyright (c)
2026 Nate Herk`) and the `licenses/PIPELINE-USE-PERMISSION.txt` notice.

### Measured results (re-run 2026-11-12, fixed converter)

Clip lengths are ffprobe `format=duration` on the encoded files;
whisper `tiny` unless noted.

| Clip | Before (ffprobe) | After (ffprobe) | Change | Deletes |
|---|---|---|---|---|
| sitcom_v2.mp4 | 19.875 s | 13.808 s | -30.5 % | 6 ranges |
| sA_meltdown_v2.mp4 | 10.21 s | 8.70 s | -14.8 % | 1 range (tail) |
| sA_meltdown_v2.mp4, `--model small` | 10.21 s | 8.567 s | -16.1 % | 1 range (tail) |

The earlier draft showed 20.62 s / 9.34 s "before" — last word end +
1.0 s from the converter, not the clip length.

### The CTA tail trap (found in this re-run)

On `sA_meltdown_v2.mp4` the only delete was the tail trim 8.68–10.21 s.
The CTA sound sits at ~10.0 s (`last_sound_s` in the local videos5 sync
QA, a 2026-11-12 artifact not in this repo), inside that range — the cut
dropped the last ~1.5 s and the call-to-action audio. `pacing.md`'s
end-tail rule says the CTA must be held ~2 s; a transcript-only tool
cannot see a non-speech sting:

- **Rule:** the last keep range must reach the end of the CTA/last
  sound, not just past the last word. Before `--apply`, find where the
  last non-speech sound ends (`last_sound_s` in `qa.md`, or
  `silencedetect`) and compare it to the EDL's last `keep_ranges` end.
- **Check:** after rendering, `last_sound_s` on the output must still
  cover the CTA; if the trim removed it, the edit fails.
- **Protection:** raise `--tail-pad` so `last_word_end + tail_pad`
  reaches past the CTA end (no keep flag exists). Verified: `--tail-pad
  2.0` kept all 10.21 s with 0 deletes. Or cut the CTA region by hand,
  or accept the trim only when the CTA is speech the transcript saw.

### Synthetic re-run

A 12 s testsrc2+sine clip with a hand-written 9-word JSON containing
three ~2 s gaps went to 4.44 s (-63 %), 4 delete ranges, ffprobe-verified
mp4 — **a run made while writing this skill**, not an independent eval.

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

`apply-cuts.mjs` usage: `<transcript.json> --cuts <approved.json>
[--video ...] [--output ...] [--out-dir ...] [--apply]` — omitting
`--cuts` fails with "no --cuts file given"; without `--apply` nothing
renders. Exercised 2026-11-12: one hand-approved 0.6 s false-start cut
on the silenced clip rendered 8.68 s → 8.08 s.

- Feed step 2 the **re-timed** transcript; never mix original and edited
  timestamps.
- The finder is mechanical: stutters, repeated words, false starts,
  retakes. On clean TTS clips it found 0 candidates; **stutter/retake
  detection was read but not exercised on real retakes** — validate on
  a talking-head take first.
- A person or review step approves each cut; intentional repetition is
  not a mistake. `apply-cuts` renders only approved ranges (empty `cuts`
  renders input unchanged).
- TTS-narrated ads usually have no spoken mistakes — the silence cut
  alone is the common case.

## Traps

- Word JSON key is `text` for these scripts. Other tools differ —
  OpenMontage's subtitle_gen wants `word`. Normalize once at ingest.
- `--apply` renders into `--out-dir` (default: alongside the inputs),
  not next to the video unless `--out-dir` points there.
- Dead-air detection without a transcript exists (ffmpeg
  `silencedetect`, verified in the eval) but found nothing on our clips
  — their audio beds are continuous. Speech-gap cutting needs the transcript.
