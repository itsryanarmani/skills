---
name: voice-clone-from-video
description: "Use to train a saved copy of your own voice from a clean clip of one of your videos, so you can generate a missing word or fill a gap in your own voice. Uses WaveSpeed minimax/voice-clone. Covers the sample to pick, the one-time $1.60 cost, the 7-day expiry of a voice no speech call has used, a check that the clone matches, an optional keep-alive, and the consent and disclosure rules. Use when asked to clone, train or save my voice, fix a mispronounced word, or fill a gap in a recording."
---

# voice-clone-from-video

Train a saved copy of **your own** voice once, then generate speech in it for
cents. Measured November 2026 with the `wavespeed` CLI v0.2.3.

## Rules first

- **Clone only a voice you own, or one whose owner agreed in writing.** Never
  clone a colleague, a recruiter or a public figure.
- **Say so where a viewer would care.** A job application, a testimonial or a
  sales claim spoken by a synthetic voice needs a label. Fixing a mispronounced
  word does not. Filling in a sentence you never said does.
- **A cloned voice does not match lips.** Use it where the speaker is off camera
  or under a cutaway. Never put it over a visible mouth.
- **The sample is uploaded to WaveSpeed's CDN** and gets a link. Use only a clip
  you would be fine sharing.
- **The key stays in the environment.** Set `WAVESPEED_API_KEY` from your secret
  file. Never put it on a command line or in a repository.

## What it costs

| Step | Cost |
| --- | --- |
| Train the voice, `minimax/voice-clone` | $1.60 once (balance fell $7.045 to $5.435, including two speech calls) |
| Speak with it, `minimax/speech-02-hd` | about $0.10 per 1,000 characters; a short line was under $0.01 |
| Optional insurance, `keepalive.sh` | about $0.002 per run |
| Clone from a sample on every call, `omnivoice` or `qwen3-tts` | $0.005 per call, and **nothing is saved** |

Check a price before you pay: `wavespeed price minimax/voice-clone`.

## Steps

1. **Pick a sample: 5 to 20 s of clean speech.** WaveSpeed asks for 5 to 20 s.
   Use a stretch from an edited video of you alone, with no music and no echo.
   More audio is not needed. A 20 s sample matched the speaker well.
2. **Dry run.** It extracts the sample, prints its length, level and the price,
   and spends nothing.
   ```bash
   bash scripts/clone.sh video.mp4 MyVoice2026 --start 0.4 --secs 20 --dry-run
   ```
3. **Train.** The ID needs 8 or more characters, a leading letter, letters and
   digits, and must be new. A duplicate fails.
   ```bash
   bash scripts/clone.sh video.mp4 MyVoice2026 --start 0.4 --secs 20
   ```
   It uploads the sample, clones, uses the voice once, and writes
   `~/.voice-clones/MyVoice2026/voice.json` (mode 600). Move that record to a
   private place. A voice ID is an asset, so do not publish it.
4. **Check it.** Generate a line you also have on tape, then compare:
   ```bash
   python3 scripts/check.py sample.wav generated.mp3 "the exact words spoken"
   ```
   It passes when the median pitch is within 15% of the sample and the words
   match. First real run: 134 Hz sample against 136 Hz clone, same pitch range,
   and the transcript matched word for word. **This is a rough check. Listen.**
5. **Use it once.** WaveSpeed deletes an ID, and its embedding, that **no speech
   call has used within 7 days**. Its page says one call makes the voice reusable
   long-term. `clone.sh` makes that call. If a later call says the voice is not
   found, train again. `bash scripts/keepalive.sh MyVoice2026` is cheap insurance
   (about $0.002), and I did not verify that the clock restarts on each use.

## Speaking with it

`wavespeed run minimax/speech-02-hd -i voice_id=MyVoice2026 -i text="..." --download "out.{ext}"`.
Other models that accept a trained ID: `speech-02-turbo`, `speech-2.6-hd`,
`speech-2.6-turbo`. Keep the text under 10,000 characters. Put `<#0.5#>` between
words to set a pause.

## Filling a gap in a video

**Untested here.** The plan: transcribe the gap with `talking-head-edit`,
generate the missing words, match the level to -16 LUFS, cut it in with a 15 ms
fade on each side, and re-run the `talking-head-edit` checks. Check a sample
with the speaker's real audio on both sides: pitch, pace and room tone must
match, or the join is obvious. Cover the gap with a cutaway (see the lip rule).

## Verify the skill

```bash
set -a; . ~/path/to/wavespeed.env; set +a
bash scripts/e2e.sh verdict.json     # exit 0 and "pass": true, about 12 s, about $0.005
```

It checks that a dry run prints the price and spends nothing (the balance is read
before and after), that a speech call makes audio, and that `check.py` passes on a
matching clip. Two **controls must fail**: a different voice and the wrong text.
It never makes the $1.60 clone call. That call was run once by hand and its result
is above.

## Traps

- **A voice ID that no speech call has used is deleted after 7 days.** Make one call.
- **A duplicate ID fails.** Pick a new one, or keep the old record.
- **Training audio is not "more is better".** The model asks for 5 to 20 s.
- **`--dry-run` still extracts audio** from the video. It never uploads.
- **A password in `ps` output leaks.** Pass the key in the environment only.
