# Audio QA for finished ads

Measured audio checks for a rendered ad, run by the `ad-audio-qa` tool in
[itsryanarmani/scripts](https://github.com/itsryanarmani/scripts/pull/860).
It calls [earshot](https://github.com/Leonxlnx/earshot) (MIT, CPU-only, local)
as an external dependency — no earshot code or models live in this repo.
Every rule prints PASS, FAIL, NOT CHECKED or OWNER CHECK with a measured
value. Run it after `SKILL.md` step 8, before you ship.

## Setup (one time)

```bash
git clone --depth 1 https://github.com/Leonxlnx/earshot earshot/repo
python3.12 -m venv earshot/venv
earshot/venv/bin/pip install ./earshot/repo
earshot/venv/bin/earshot doctor --fetch   # ~1.1 GB models, Hugging Face
export AD_AUDIO_QA_EARSHOT=/path/to/earshot   # checkout, venv, or python
```

Never run `earshot llm`: it uploads audio. `ad-audio-qa` has no code path to
it, and earshot never uploads audio on its own — the first run only downloads
models from Hugging Face. Missing earshot exits 2 with a one-line error.

## Run

```bash
ad-audio-qa FINAL.mp4 --out qa-audio.json \
  --sfx-stem sfx.wav --voice-stem voice.wav \
  --lines "audio/l_*.wav" --voice-map maps/voicemap.json \
  --transcript work/transcript.json
```

`--sfx-stem` is a wav of the sfx and laugh track alone; `--voice-stem` a wav
of the voice alone. A mixed track cannot separate them, so R14, the sfx onset
check and `sfx_vs_voice` print NOT CHECKED without the stems. `--lines` +
`--voice-map` enable the R8 consistency check. `--transcript` (word timings
from local whisper) enables true WPS (R7) and caption sync (R10); a `groups`
list gives caption segments directly, word timings are chunked to 3 words.

## Rules and thresholds

| Rule | Pass condition |
| --- | --- |
| R6 dead audio | Coarse guard: FAIL on any stretch >= 1.5 s below -60 LUFS momentary; not digital silence. The ffmpeg `silencedetect` (-35 dB, 0.25 s) crossed with `freezedetect` (0.3 s) in `owner-feedback.md` is the gate. |
| loudness | Integrated -16 to -12 LUFS (target -14); true peak <= -1 dBTP. |
| R14 sound and cuts | Needs `--sfx-stem`. FAIL "Sound is required" when the stem has no onsets; else FAIL when < 80% of the sfx onsets land within 80 ms of a picture cut (ffmpeg scene > 0.3). A cut with no sfx is fine (`pacing.md`: sfx only on events); an sfx that floats between cuts is a miss. A voice onset never counts. |
| sfx onset 80 ms | Same stem and cut list as R14; reports the share of onsets within 80 ms of a cut. |
| sfx vs voice | Needs both stems. Sfx median active-frame level >= 6 dB under the voice stem level (dialogue formats). `pacing.md`'s -1.4 to -3.6 dB range is for loud punch edits without dialogue. Those pacing.md figures came from the old mixed-track measurement, so treat them as unverified. |
| R7 speech pace | True WPS <= 3.4 with `--transcript`; NOT CHECKED without it. Hand target stays 2 to 3 words per second. |
| R8 voice consistency | Per-character F0 spread: <= 1.25 PASS, above 1.25 OWNER CHECK ("weak proxy, listen"). Never FAIL: a calibration found neither pitch spread nor a speaker embedding separated the one voice the owner rejected from eleven the owner accepted. NOT CHECKED when no character has 2 or more usable lines. |
| R10 caption sync | Tool alarm: median offset <= 300 ms and >= 70% within 300 ms of speech onsets. Hand target stays 0.15 s. |
| R8 voice-face fit, R11 mouth-voice, owner judgment | OWNER CHECK — always a person. |

## Final master step

Normalize the final mix to -14 LUFS with two-pass `loudnorm`, then remux into
the mp4 and measure THAT file — AAC encoding moves the true peak. Keep the
bitrate at 192k: 128k AAC raised the true peak from -1.5 to -0.6 dBTP in the
run below, 192k kept -1.4.

```bash
# pass 1: measure
ffmpeg -i mix.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json" \
  -f null - 2> p1.log
sed -n '/^{/,/^}/p' p1.log > p1.json

# pass 2: parse the pass-1 values into the filter, then limit
AF=$(python3 -c 'import json; m=json.load(open("p1.json")); \
print("loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=%s:measured_TP=%s:" \
"measured_LRA=%s:measured_thresh=%s:offset=%s:linear=true" % \
(m["input_i"],m["input_tp"],m["input_lra"],m["input_thresh"], \
m["target_offset"]))')
ffmpeg -i mix.wav -af "$AF,alimiter=limit=0.841:attack=5:release=50:\
level=false" -ar 48000 master.wav

# remux: video stream copied, audio re-encoded
ffmpeg -i FINAL.mp4 -i master.wav -map 0:v -map 1:a -c:v copy \
  -c:a aac -b:a 192k FINAL-master.mp4
ffmpeg -i FINAL-master.mp4 -af ebur128=peak=true -f null -
```

`alimiter` is a sample-peak limiter, not a true-peak limiter — it cannot see
inter-sample peaks, so the ebur128 check on the final mp4 is the gate.

### Proof on synthetic defect audio

Generator — a 10 s stereo clip: a quiet harmonic bed plus 5 ms bursts at
11025 Hz, amplitude 1.27, every 2 s:

```bash
#!/bin/bash   # zsh reads "$B:s=..." as a history modifier and runs forever: use bash
B="0.063*sin(2*PI*110*t)+0.038*sin(2*PI*220*t)+0.025*sin(2*PI*330*t)+0.019*sin(2*PI*440*t)"
ffmpeg -f lavfi -i "aevalsrc=${B}|${B}:s=48000:d=10" \
  -f lavfi -i "aevalsrc=1.27*sin(2*PI*11025*t)|1.27*sin(2*PI*11025*t):s=48000:d=0.005" \
  -filter_complex "[1:a]asplit=5[b0][b1][b2][b3][b4];\
[b0]adelay=0|0[x0];[b1]adelay=2000|2000[x1];[b2]adelay=4000|4000[x2];\
[b3]adelay=6000|6000[x3];[b4]adelay=8000|8000[x4];\
[x0][x1][x2][x3][x4]amix=inputs=5:normalize=0,apad=whole_dur=10[s];\
[0:a][s]amix=inputs=2:normalize=0[m]" -map "[m]" -c:a pcm_f32le defect.wav
cp defect.wav mix.wav   # the master steps above read mix.wav
```

Measured before: I = -19.1 LUFS, true peak +2.9 dBTP (the two real defects:
a quiet mix and clipped peaks).

Pass 1 JSON (`input_i`, `input_tp`, `input_lra`, `input_thresh`,
`target_offset` — the pass-2 command above parses exactly these):

```json
{ "input_i": "-19.27", "input_tp": "2.86", "input_lra": "1.90",
  "input_thresh": "-29.27", "target_offset": "3.79",
  "normalization_type": "dynamic" }
```

After pass 2 + remux at 192k, measured on the final mp4: I = -14.4 LUFS,
true peak -1.4 dBTP, zero samples at or above 0 dBFS, and the video stream
md5 is identical before and after (`-map 0:v -c:v copy` touches only
container timing).

Honest limit: `loudnorm` can switch to dynamic mode — pass 1 prints
`normalization_type`, and on this clip it predicted -17.8 LUFS, not -14.
Dynamic gain rides the gated loudness and can overshoot on steady material
with LRA 0 (reported: -13.1 in, -18.4 out on a pure-tone bed). Always
re-measure the master; never trust pass-1 `output_i`.

## What earshot found that our QA missed

On four finals from our research workspace (the three `videos6` finals and the sitcom final; the workspace is local and not committed, so run the tool on your own finals to reproduce), earshot and ffmpeg caught what the old checks passed:

| Final | Integrated | True peak | Clipped samples |
| --- | --- | --- | --- |
| `sA_meltdown_v3` | -12.1 LUFS | +2.7 dBTP | 160 |
| `sB_door_v3` | -12.3 LUFS | +0.3 dBTP | 8 |
| `sC_window_v3` | -12.4 LUFS | +0.1 dBTP | 4 |
| `sitcom_v3` | -19.8 LUFS | -0.9 dBTP | 0 |


- True-peak violations and clipping on all three videos6 finals (up to
  +2.7 dBTP, 160 clipped samples). The true-peak check existed in `qa.md`
  but was not run.
- One sitcom final 5.8 LU quiet (-19.8 vs -14 target).

Two earlier claims are withdrawn: the sfx-vs-voice margins and the sitcom
sound-to-cut sync numbers came from earshot's mixed-track events, which
count voice syllables as sound events and report the mix peak — they are
not valid measurements. Both rules now require separated stems.

## What it cannot judge

- Voice-to-face, body, character, ethnicity, age or accent fit — audio only.
- Acting quality, joke quality, whether the mix "feels" right.
- Speech content — it tags Speech but cannot transcribe or judge words.
- Provenance — `realness` is a probabilistic acoustic classifier.
- Content above ~14 kHz; `match` on voice/instrument/mood is unvalidated.

## Owner-check rule

R8 voice stays an OWNER CHECK, both fit and consistency. The F0 spread
measures neither reliably: it flagged voices the owner accepted, and a
speaker embedding rated the rejected voice as the most consistent. Keep
`R8_voice_consistency` as a prompt to listen; send fit, consistency,
acting, music taste and mix feel to the owner with the video. Same for R11
mouth-voice — wire the FaceLandmarker artifacts before trusting any
automated verdict.
