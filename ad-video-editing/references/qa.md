# Post-render QA for fast-cut ads

Run these on the encoded mp4, not on the project file. The numbers catch
the failures a timeline lint cannot see. Verified 2026-11-12; the
determinism, flash/freeze/black and loudness checks are ported from
OpenFilm's `look` command (verified in the eval on our own clip).

For the speech/pacing timing gate (silence-vs-motion, shot length,
first-sound/tail), reuse the "Sync and pacing gate" section of
[`ad-lofi-ugc/references/qa.md`](../../ad-lofi-ugc/references/qa.md) —
do not copy it here.

## 1. Determinism double-draw

A render that draws frame `t` differently by seek order is not shippable.
OpenFilm's `look` drew 12 frames twice in two shuffled orders and reported
"same t, same picture" on our clip.

```bash
ffmpeg -ss <t1> -i out.mp4 -frames:v 1 a.png
ffmpeg -ss <t0> -i out.mp4 -frames:v 1 -ss <delta> b.png   # different path, same t
cmp a.png b.png
```

For composition renders, seek `frame(t)` twice through different orders
and pixel-compare. Any difference = nondeterminism (wall clock, random
seed, unseeded noise).

## 2. Flash, freeze and black scan

```bash
ffmpeg -i out.mp4 -vf "freezedetect=n=-60dB:d=2,blackdetect=d=0.1:pix_th=0.10" -an -f null -
ffmpeg -i out.mp4 -vf "select='gt(scene,0.4)',metadata=print" -an -f null - 2>&1 | grep pts_time
```

- **Black frames:** any `blackdetect` hit inside the ad fails.
- **Frozen frames:** a still ≥ ~1 s inside a fast-cut ad is suspicious
  (end cards excepted); ≥ 6 s always fails.
- **White flashes / strobe:** extract at 10 fps; flag frames whose mean
  luma jumps > ~150 between neighbors without a scene cut, plus near-white
  frames. A transition flash is intentional; a strobe is not.
- The scene-cut list doubles as the cut list for the pacing gate.

## 3. Loudness

Target for TikTok/Reels: **-14 LUFS integrated, true peak ≤ -1 dBTP**.

```bash
ffmpeg -i out.mp4 -af ebur128=peak=true -f null -
```

Read `I:` (integrated) and `Peak:` from the summary. OpenFilm's
`render --loudness=-14` delivered -14.1 LUFS on our test render.
Normalize with `loudnorm` two-pass or a final `alimiter`+gain stage;
keep SFX under voice (see `library.md`).

## 4. Silence and tail

```bash
ffmpeg -i out.mp4 -af silencedetect=n=-35dB:d=0.25 -vn -f null -
```

- A silent range where the picture is also static > 0.3 s fails — that
  is a dead gap (see `pacing.md`).
- First sound within 0.3 s of frame one; last sound to last frame < 0.3 s.
- Also check A/V stream durations match within ~0.1 s and the moov atom
  is up front (`+faststart`).

## 5. Caption timing from whisper

Captions must come from whisper word timestamps on the **final** audio,
not from the script or the pre-cut transcript:

1. Extract audio from the rendered mp4, re-run whisper with
   `--word_timestamps True`.
2. For each caption cue, confirm `start`/`end` bracket the spoken word
   within ~0.15 s. Whisper `tiny`/`small` drift on fast cuts; check the
   first and last cue of each shot manually.
3. Karaoke highlight follows the same word times — if the highlight
   leads or lags the voice, the timing is wrong even if the text is right.

## 6. Mouth-sync spot check

For talking-head shots: correlate the audio envelope (50 ms windows)
with mouth-region frame diff over each shot. Onsets should align within
~100-200 ms. **Not re-run** — no lip-sync footage was tested; treat as a
manual spot check until measured on a real take.
