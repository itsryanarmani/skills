---
name: talking-head-edit
description: "Use to clean up a single-camera talking-head video (application, intro, pitch, explainer; 1-10 min): cut dead air and filler sounds, set loudness, and check the cuts are smooth. One command, local tools, no model tokens for the edit. A model only reads the transcript to judge rambling. Use when asked to edit, tighten, cut the dead parts, fix the sound level, or process a folder of talking videos."
---

# talking-head-edit

One command edits a talking-head video: it cuts dead air, sets loudness, then
measures its own output. No model runs during the edit. Measured November 2026
on two 1080p ProRes files (97 s and 108 s), Apple-silicon laptop.

For short vertical ads use `ad-video-editing`; for product demos,
`ship-demo-video`. This skill adds no graphics.

## Run it

```bash
PROMPT="Name, Product, Company" bash scripts/tidy.sh "in.mov"    # -> in-edited.mp4
```

It writes `in-edited.mp4`, `.report.json` and `.transcript.txt` next to the
source and never changes the source. It prints a JSON verdict. Exit 0 means
every check passed. For a folder: `for f in *.mov; do bash scripts/tidy.sh "$f"; done`.

| Stage | Wall time, 108 s video |
| --- | --- |
| Transcribe, local whisper `small.en` (default) | 47 s |
| Cut, loudness, encode | 23 s |
| Re-transcribe the output, verify | 40 s |
| **Total** | **about 110 s, no model tokens** (`WHISPER_MODEL=base.en`: about 60 s) |

## What the agent does

1. Run `tidy.sh`. Read the verdict (about 20 lines).
2. Read `*.transcript.txt` once (about 1k tokens per 100 s). Judge it as in
   "What to trim". This is the only step that needs a model.
3. For a cut, pass `--cut START-END` (transcript seconds) after the file names,
   run again, and report what changed and what the speaker must decide.

Do not send frames or audio to a model to find cuts. Audio energy holds them.

## How the cuts stay smooth

Three bugs made earlier cuts abrupt. Each is fixed and tested.

- **Cut times come from audio energy, not from whisper.** Whisper word ends
  are off by 0.1 to 0.5 s, so cuts placed from them clip a word. The script
  cuts inside true silence (room floor + 10 dB) and keeps 0.15 s of pause on
  each side. In a test, voice was still sounding at the edge of 9 of 12
  whisper-placed cuts.
- **Add the audio start offset.** In real camera files the audio starts 0.12
  to 0.17 s after the video. Cuts measured on the audio clock but trimmed on
  the container clock land early, inside the previous word. The script adds
  the offset, minus any container start. Worst join: 27 dB above the room floor
  before, 6.5 dB after.
- **Fade every join by 15 ms,** so no join clicks.

**Never cut from word times, even for a sound whisper skipped.** A rule that
cut "voiced gaps with no word" turned "subscriptions" into "systems": whisper
had ended the word early, so real speech looked untranscribed. Such sounds are
only flagged (`sound_without_word_to_review`, 0.8 s or more of voice with no
word). The flag needs `small.en`: `base.en` filled a known 1.1 s gap and missed
it. Listen, then cut it with `--cut`. A manual cut snaps to the quietest 10 ms
within 80 ms and warns if the edge is on voice.

## What the verdict checks

It measures the real output, not the plan:

| Check | Pass |
| --- | --- |
| Length equals plan | within 0.15 s |
| Loudness | within 1 LU of -16 LUFS |
| True peak | at or below -1 dBTP |
| Every join | at most 10 dB above the room floor |
| Warnings | none |

`repeated_words_to_review` lists a word said twice in a row in the edited
transcript. Ask the speaker. Do not auto-cut it. It was empty on both test
videos after the fixes. Doubled words seen earlier came from the misaligned
cuts, not from real stutters.

**Check word loss with `small.en`.** Transcribe source and output and diff the
lower-cased word lists. A diff caught the "systems" bug that every other check
missed. Final results: 217 words to 217 (two whisper corrections), and 206 to
208 (the output has two words the source transcript missed). Before the fixes a
208-word file had 8 differences. `base.en` hears the same audio differently each
run and gives false alarms.

## What to trim

Pauses are automatic. Words are a judgment. Flag, in this order:

1. A sentence the speaker restarts. Keep the better take.
2. A claim with no number or proof ("papers out there"). Ask for a count.
3. Jargon a stranger cannot parse.
4. A claim that may hurt the goal (risky tactics in a job application).
   **Flag it and ask. Do not cut it alone.**

Do not cut meaning without the speaker's approval. Pauses and sounds are safe.

`base.en` spells names wrong (a studio name as "Feelout", the speaker as
"Brian"). `PROMPT` helps. Still never copy a name from the transcript into
text a viewer reads. Ask the speaker.

## Cost

| Item | Cost |
| --- | --- |
| Tools: ffmpeg, whisper, numpy | $0, about 2 min of laptop time per video |
| Model, per video | one run, one verdict, one transcript read: a few thousand tokens (an estimate, not a bill) |

A Haiku-class model could list restarts from the transcript. This is
**untested**. Plant one known restart in a test video first: a model that
finds nothing looks the same as a clean video. Brief a sub-agent with the
transcript, the goal and the output shape (`START-END reason`).

## Verify the skill

```bash
bash scripts/e2e.sh verdict.json    # exit 0 and "pass": true, about 35 s
```

It builds a clip with the audio delayed 0.3 s, runs the real flow, and checks
length, loudness, joins and word loss. A **control run with the offset fix off
must fail**, or the test cannot see the bug. The first version passed with the
fix off, because a join check at planned positions cannot see audio that is
short. The length check caught it. Needs `say` or `espeak`, and `numpy`.

## Traps

- **`silencedetect` at -35 dB found nothing** on a real voice with room noise.
  Use the energy floor of the file itself.
- **A synthetic video shorter than its audio shortens the output.** Match the
  lengths, or the length check fails for the wrong reason.
- **Do not rebuild a plan from a second whisper run.** A name hint changes the
  words and so the cuts. Read `keep` and `joins_db` from the report.
