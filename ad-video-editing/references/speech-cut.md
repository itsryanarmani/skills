# Speech-driven cuts: dead air and mistakes

Word-gap silence removal and review-gated mistake cuts, adapted from
herk-edit-kit (MIT-equivalent; see `sources.md`). Both scripts take any
`{words:[{text,start,end}]}` transcript — local whisper output works.
Verified 2026-11-12.

## 1. Make the word JSON from local whisper

```bash
ffmpeg -y -i input.mp4 -vn -ac 1 -ar 16000 work/audio.wav
whisper work/audio.wav --model small --output_format json \
  --word_timestamps True --output_dir work
```

whisper's JSON nests words under `segments[].words[]` with key `word`.
Flatten it to the shape the cut tools want (`text`, `start`, `end`):

```python
import json
src = json.load(open("work/audio.json"))
words = [{"text": w["word"].strip(), "start": w["start"], "end": w["end"]}
         for s in src["segments"] for w in s.get("words", [])]
json.dump({"words": words,
           "audio_duration_secs": src["duration"]},
          open("work/words.json", "w"))
```

Use `small` or better for real ads; `tiny` is rough on names. The whisper
command matches the eval (`tests/NOTES.md`); the converter matches its
`tests/work/` output. The cut step was re-run on synthetic input
(section 2); the whisper step was verified in the eval.

## 2. Cut silences

```bash
node cut-silences.mjs work/words.json \
  --video input.mp4 --out-dir work/out --apply
```

Options: `--gap 0.55` (min pause to trim), `--head-pad 0.22`,
`--tail-pad 0.34`, `--output`, `--apply` (renders via ffmpeg
`libx264 crf 18`, `aac 192k`, faststart).

Outputs: `<stem>.silence-edl.json` (keep/delete ranges + reasons),
`<stem>.silence-transcript.json` (**words re-timed to the edited
timeline**), `<stem>.silence-decisions.md`, and the cut mp4.

This is word-gap driven, not loudness driven. It keeps deliberate breaths
in TTS narration that a loudness-only tool (auto-editor) would eat.
Copy the script into our tooling; do not depend on the vendor repo.

Measured results (eval, 2026-11-12, real ad clips 1080x1920):

| Clip | Before | After | Change |
|---|---|---|---|
| sitcom_v2.mp4 | 20.62 s | 13.84 s | -32.9 %, 7 delete ranges |
| sA_meltdown_v2.mp4 | 9.34 s | 8.68 s | -7.1 %, 1 delete range |

Re-run on synthetic input 2026-11-12: a 12 s testsrc2+sine clip with a
hand-written 9-word JSON containing three ~2 s gaps went to 4.44 s
(-63 %), 4 delete ranges, rendered mp4 verified by ffprobe. The script
path in the eval was
`vendor2/herk-edit-kit/src/.claude/skills/cut-silences/scripts/cut-silences.mjs`;
copy the script into our own tooling rather than depending on the repo.

## 3. Cut mistakes (review-gated)

```bash
node find-cut-candidates.mjs work/out/words.silence-transcript.json \
  --out-dir work/out
# review each candidate in context; record decisions; then:
node apply-cuts.mjs <candidates-with-decisions> --video <silenced.mp4>
```

- Feed step 2 the **re-timed** transcript. Never mix original and edited
  timestamps.
- The finder is mechanical: stutters, repeated words, false starts,
  retakes. It emits candidates with context and a reason.
- A person or review step approves each cut. Intentional repetition is
  not a mistake. `apply-cuts` renders only approved ranges.
- For TTS-narrated ads there are usually no spoken mistakes; the silence
  cut alone is the common case. The mistake scan earns its keep on real
  talking-head takes.

## Traps

- Word JSON key is `text` for these scripts. Other tools differ —
  OpenMontage's subtitle_gen wants `word`. Normalize once at ingest.
- `--apply` renders next to the inputs unless `--output` is set.
- Dead-air detection without a transcript exists (ffmpeg
  `silencedetect`, verified in the eval) but found nothing on our
  produced clips — their audio beds are continuous. Speech-gap cutting
  needs the transcript.
