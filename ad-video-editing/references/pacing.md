# Pacing rules for fast-cut ads

Measured rules for 10-30 s vertical ads, from our own edit runs
(videos4 → videos5 re-edit, Nov 2026) and the herk-edit-kit editing
playbook. Verified 2026-11-12.

## The rules

1. **Hook in the first second.** The first frame must already show the
   peak of the action or the claim. No establishing shot, no logo.
2. **Cut every 0.8-2 s.** Average shot length 1.2-1.5 s for the fast
   look. Our passing videos5 cuts averaged 1.17-1.30 s.
3. **Voice at normal pace.** Do not speed up speech. `atempo` stays at
   or under ~1.15; beyond that it sounds rushed.
4. **Speed up the picture, not the speech.** `setpts` 1.4-1.5x on the
   video track compresses dead motion while the voice keeps its timing.
   This is how a 5 s generated clip covers a 3 s line.
5. **SFX only on events.** A whoosh on every cut is the ceiling, not the
   floor. Impacts and stings land on the payoff beat, the twist, the CTA.
   Nothing plays over silence.
6. **One whoosh that lands beats five that blur.** Alternate whoosh
   direction (up/down) so cuts do not sound identical; keep each under
   the voice (about -3 to -6 dB under, measured -1.4 to -3.6 dB in our
   mix check).
7. **End tail under 0.3 s.** The last sound and the last frame sit less
   than 0.3 s apart; the first sound starts within 0.3 s of frame one.
   Hold the final claim or CTA at least ~2 s so it reads.
8. **Build the timeline from measured voice lines.** Generate or trim
   each VO line, measure its real duration, then set each shot length to
   that line plus a ~0.14 s tail. Never pick shot lengths first and fit
   audio into them.

## The evidence

Our first fast-cut pass (videos4 finals) failed the pacing gate:

| File | Duration | Cuts | Avg cut | Dead A/V | First sound | Tail | Result |
|---|---|---|---|---|---|---|---|
| sA_meltdown.mp4 | 16.0 s | 2 | 5.33 s | 0 | 0.10 | 0.00 | FAIL |
| sB_door.mp4 | 16.0 s | 3 | 4.00 s | 0 | 0.10 | 0.10 | FAIL |
| sC_window.mp4 | 16.0 s | 4 | 3.20 s | 0 | 0.00 | 0.00 | FAIL |

The re-edit (videos5) rewrote the script as 6-8 short lines, generated
TTS per line, measured every line with ffprobe, and built `segments.json`
audio-first (shot duration = voice duration + 0.14 s tail). Result:

| File | Duration | Cuts | Avg cut | Dead A/V | First sound | Tail | Result |
|---|---|---|---|---|---|---|---|
| sA_meltdown_v2.mp4 | 10.21 s | 7 | 1.28 s | 0 | 0.00 | 0.21 | PASS |
| sB_door_v2.mp4 | 10.38 s | 7 | 1.30 s | 0 | 0.00 | 0.18 | PASS |
| sC_window_v2.mp4 | 10.49 s | 8 | 1.17 s | 0 | 0.00 | 0.19 | PASS |

Same footage, same voices — the only change was timeline construction.
The lesson: dead gaps in v2-style edits came from fixed-length shots,
not from the footage. Rule 8 is the fix.

## Captions carry the pace

Word-by-word captions let the viewer follow a 1.2 s-per-shot cut without
audio. The muted copy of every video must still tell the story — the
mute test in `ad-lofi-ugc/references/qa.md`.
