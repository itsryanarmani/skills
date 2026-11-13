# Sound for lo-fi UGC ads

Sound is the last layer, not the foundation. The ad must work muted. Round
two of a real campaign shipped five silent videos and the owner flagged it;
the fix was a sound pass plus muted exports as proof. Design muted-first.

## Muted-first design

The visual story and the burned captions carry the ad. A viewer with sound
off must still get: the hook, the problem, the offer. Sound adds texture and
emphasis; it never carries information that exists nowhere else.

Every video ships in two files:

- `<name>.mp4` — with the full audio mix.
- `<name>_muted.mp4` — same video, no audio. Proof the ad works silent.

## The mix, in order

1. **Voiceover** — the caption lines read aloud, or a shorter script. Pick
   the cheapest decent TTS on your provider and check the price before the
   batch. Casual, fast, dry delivery — not a newsreader. One voice id for the
   whole campaign. Short sentences, ~2.5 words per second.
2. **Ambient bed** — quiet room tone or a lo-fi loop. It should sit under
   the voice, not compete. Generate it, or synthesize noise with ffmpeg
   (`anoisesrc`) and filter it low.
3. **SFX** — a few ffmpeg-synthesized cues: a whoosh on hard cuts, a thud on
   an impact beat, a riser before the twist or payoff. Synthesize them with
   `aevalsrc`/`anoisesrc` or a tiny generated tone; there is no ffmpeg SFX
   library, so keep cues simple (filtered noise bursts work for whoosh and
   thud).
4. **Mix levels** — voice loudest, bed and SFX well under it. The weights
   `1 0.15 0.15` below put bed and SFX about 16 dB under the voice. Treat
   them as a starting point and trust your ears.
   No copyrighted music. AI-disclosed voices follow the same rules as faces:
   never clone a real person's voice without consent.
5. **Encode** — AAC audio in the final MP4:

   ```bash
   # Inputs: 0 = video, 1 = voice, 2 = bed, 3 = SFX stem.
   ffmpeg -i video.mp4 -i voice.wav -i bed.wav -i sfx.wav -filter_complex \
     "[1:a][2:a][3:a]amix=inputs=3:weights='1 0.15 0.15':normalize=0,alimiter[a]" \
     -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 128k -shortest out.mp4
   ```

   (Tested on ffmpeg 9.0.2 with synthetic stems. `normalize=0` needs ffmpeg 4.4 or newer. Adjust inputs to your actual stems; the point is VO + quiet bed + sparse
   SFX, limited, encoded AAC.)

## What goes wrong

- **Sound carrying the hook.** If the first 2 seconds only make sense with
  audio, the ad fails muted. Move the reveal into the picture or the caption.
- **Music fighting the VO.** Duck or drop the bed under speech; sidechain or
  just keep the bed quiet.
- **SFX on every cut.** One whoosh per video lands; five become noise.
- **Splicing voice takes.** Re-voice the whole shot, not one line.
- **Robotic TTS.** If the cheapest voice sounds like a phone menu, spend one
  tier up — voice quality is the difference between UGC and an IVR ad.
