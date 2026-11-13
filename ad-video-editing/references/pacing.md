# Pacing rules for fast-cut ads

Measured rules for 10-30 s vertical ads, from our own edit runs
(videos4 → videos5 re-edit, Nov 2026 — a local run, evidence not in
this repo) and the herk-edit-kit editing playbook. Verified 2026-11-12.

## The rules

1. **Hook in the first second.** The first frame must already show the
   peak of the action or the claim. No establishing shot, no logo.
2. **Cut every 0.8-2 s.** Shot length depends on the format: 1.2-1.5 s
   for a fast punch edit, 1.5-2.2 s for a lo-fi UGC story (the lo-fi
   gate lives in `ad-lofi-ugc/references/qa.md`). Our passing videos5
   cuts averaged 1.17-1.30 s.
3. **Voice at normal pace.** Do not speed up speech — `atempo` stays at or under ~1.15; beyond that it sounds rushed.
4. **Speed up the picture, not the speech.** `setpts` 1.4-1.5x on the
   video track compresses dead motion while the voice keeps its timing — a 5 s clip covers a 3 s line.
5. **SFX only on events — one whoosh that lands beats five that blur.**
   Impacts and stings land on the payoff beat, the twist, the CTA;
   nothing plays over silence, and never one per cut. Alternate whoosh
   direction so cuts do not sound identical. Level: our videos5 mix
   measured SFX -1.4 to -3.6 dB under the voice (`sfx_vs_vo_db` in the
   sync QA); `ad-lofi-ugc/references/sound.md` starts bed and SFX ~16 dB
   under voice. Treat -1.4 to -3.6 dB as the floor for a loud fast-cut
   ad, ~16 dB as the safer lo-fi default; trust your ears. The -1.4 to
   -3.6 dB figures came from a mixed-track measurement that
   `audio-qa.md` withdraws: measure sfx level from separate stems.
6. **End tail under 0.3 s.** Last sound to last frame < 0.3 s; first
   sound within 0.3 s of frame one. Hold the final claim or CTA ~2 s so
   it reads — and make sure the edit keeps it: a transcript-only cut can
   tail-trim past the last word and drop a non-speech CTA sting. See the
   CTA tail trap in `speech-cut.md`.
7. **Build the timeline from measured voice lines.** Generate or trim
   each VO line, measure its real duration, then set each shot length to
   that line plus a ~0.14 s tail. Never pick shot lengths first and fit
   audio into them.

## The evidence

Our first fast-cut pass (videos4 finals) failed the pacing gate. The
videos5 re-edit rewrote the script as 6-8 short lines, generated TTS
per line, measured every line with ffprobe, and built `segments.json`
audio-first (shot duration = voice duration + 0.14 s tail):

| File | Duration | Cuts | Avg cut | Dead A/V | First sound | Tail | Result |
|---|---|---|---|---|---|---|---|
| sA_meltdown.mp4 | 16.0 s | 2 | 5.33 s | 0 | 0.10 | 0.00 | FAIL |
| sB_door.mp4 | 16.0 s | 3 | 4.00 s | 0 | 0.10 | 0.10 | FAIL |
| sC_window.mp4 | 16.0 s | 4 | 3.20 s | 0 | 0.00 | 0.00 | FAIL |
| sA_meltdown_v2.mp4 | 10.21 s | 7 | 1.28 s | 0 | 0.00 | 0.21 | PASS |
| sB_door_v2.mp4 | 10.38 s | 7 | 1.30 s | 0 | 0.00 | 0.18 | PASS |
| sC_window_v2.mp4 | 10.49 s | 8 | 1.17 s | 0 | 0.00 | 0.19 | PASS |

Same footage, same voices — the only change was timeline construction;
dead gaps came from fixed-length shots, not footage. Rule 7 is the fix.

## Captions carry the pace

Word-by-word captions carry a 1.2 s-per-shot cut with the sound off; the
muted copy must still tell the story — mute test in `ad-lofi-ugc/references/qa.md`.
