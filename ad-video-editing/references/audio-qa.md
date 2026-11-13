# Audio QA for finished ads

Measured audio checks for a rendered ad, run by the `ad-audio-qa` tool. It
calls [earshot](https://github.com/Leonxlnx/earshot) (MIT, CPU-only, local)
as an external dependency — no earshot code or models live in this repo.
Every rule prints PASS, FAIL, NOT CHECKED or OWNER CHECK with a measured
value. Run it after `references/qa.md` step 8, before you ship.

## Setup (one time)

```bash
git clone --depth 1 https://github.com/Leonxlnx/earshot earshot/repo
python3.12 -m venv earshot/venv
earshot/venv/bin/pip install ./earshot/repo
earshot/venv/bin/earshot doctor --fetch   # ~1.1 GB models, Hugging Face
export AD_AUDIO_QA_EARSHOT=/path/to/earshot   # checkout, venv, or python
```

Never run `earshot llm`: it uploads audio. `ad-audio-qa` has no code path to
it. Missing earshot exits 2 with a one-line error.

## Run

```bash
ad-audio-qa FINAL.mp4 --out qa-audio.json \
  --lines "audio/l_*.wav" --voice-map maps/voicemap.json \
  --transcript work/transcript.json
```

`--lines` + `--voice-map` enable the R8 consistency check. `--transcript`
(word timings from local whisper) enables true WPS (R7) and caption sync
(R10); a `groups` list gives caption segments directly.

## Rules and thresholds

| Rule | Pass condition |
| --- | --- |
| R6 dead audio | No stretch >= 1.5 s below -60 LUFS momentary; not digital silence. |
| loudness | Integrated -16 to -12 LUFS (target -14); true peak <= -1 dBTP. |
| R14 sound and cuts | >= 80% of picture cuts answered by a sound event within 100 ms. |
| sfx onset 80 ms | >= 80% of answered cuts have sound onset within 80 ms. |
| sfx vs voice | Loudest SFX peak >= 6 dB under median voice peak. |
| R7 speech pace | True WPS <= 3.4 with `--transcript`; else a labelled onset proxy. |
| R8 voice consistency | Per-character F0 spread <= 1.6x across line wavs. Proxy only. |
| R10 caption sync | Median offset <= 300 ms and >= 70% within 300 ms of speech onsets. |
| R8 voice-face fit, R11 mouth-voice, owner judgment | OWNER CHECK — always a person. |

## Final master step

Normalize the final mix to -14 LUFS with two-pass `loudnorm`, then limit the
true peak. Run pass 1 to measure, pass 2 with the measured values:

```bash
ffmpeg -i mix.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json" \
  -f null -
# copy input_i, input_tp, input_lra, input_thresh, target_offset

ffmpeg -i mix.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11:\
measured_I=-19.88:measured_TP=2.72:measured_LRA=0.00:\
measured_thresh=-33.90:offset=12.95:linear=true,\
alimiter=limit=0.841:attack=5:release=50:level=false" \
  -ar 48000 master.wav
```

`alimiter=limit=0.841` is the -1.5 dBTP ceiling. Verify with
`ffmpeg -i master.wav -af ebur128=peak=true -f null -`.

### Proof on synthetic defect audio

Source: 10 s, 5 ms tone bursts at +2.7 dBTP over a quiet bed —
I = -19.9 LUFS, true peak +2.7 dBTP (the two real defects: clipped finals
and a quiet mix). Measured with `ebur128=peak=true`:

| | Before | After loudnorm + limiter |
| --- | --- | --- |
| Integrated | -19.9 LUFS | -19.2 LUFS |
| True peak | +2.7 dBTP | -1.5 dBTP |
| LRA | 0.0 LU | 2.3 LU |

Honest limit: on extreme-crest material (true peak 22 dB over integrated)
the TP ceiling binds first — loudnorm cannot reach -14 LUFS without
exceeding -1.5 dBTP, so the result stays quiet. That is the correct
failure direction: never trade a clipped master for a loud one. For
program material with normal crest the same commands land at -14 LUFS.

## What earshot found that our QA missed

On four real finals, earshot caught what the old checks passed:

- True-peak violations and clipping on all three videos6 finals (up to
  +2.7 dBTP, 160 clipped samples). Our QA never measured true peak.
- One sitcom final 5.8 LU quiet (-19.8 vs -14 target).
- SFX-to-voice margins far under 6 dB on every final (-0.5 to -6.2 dB).
- Sitcom sound-to-cut sync broken: only 5/15 onsets within 80 ms of a cut.
- No continuous music bed in any of the four.

## What it cannot judge

- Voice-to-face, body, character, ethnicity, age or accent fit — audio only.
- Acting quality, joke quality, whether the mix "feels" right.
- Speech content — it tags Speech but cannot transcribe or judge words.
- Provenance — `realness` is a probabilistic acoustic classifier.
- Content above ~14 kHz; `match` on voice/instrument/mood is unvalidated.

## Owner-check rule

R8 voice-to-face fit stays an OWNER CHECK. The F0 spread measures
*consistency*, not correctness: one voice can be consistent and still wrong
for the face. Automate consistency (`R8_voice_consistency`); send fit,
acting, music taste and mix feel to the owner with the video. Same for R11
mouth-voice — wire the FaceLandmarker artifacts before trusting any
automated verdict.
