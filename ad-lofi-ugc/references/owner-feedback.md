# Owner feedback rules

Each rule is a past owner correction. Check every rule before you ship an ad video.
An adversarial reviewer must test each rule and write PASS or FAIL with a measured value.
When the owner gives new feedback, add a rule here in the same PR that fixes it.

| # | Rule | How to check | Origin |
| --- | --- | --- | --- |
| R1 | Wild emotional hook in the first second. | Watch 0 to 1 s with sound off. A person shows strong emotion or an odd event. | Round 3 hook was "not intriguing". |
| R2 | Cause comes before effect on screen. Show the action, then the result, then who reacts. | Step through 0 to 3 s. No character appears without a reason. No object is already broken. | Sitcom: door fell, people appeared at 0:02. |
| R3 | Change the camera angle, not only the zoom. | Count distinct angles and poses. At least 6 in 14 s. Cuts differ in side, height or pose. | "Different left and right views, not slow zooms." |
| R4 | The same person must show different poses and angles. | Same face, outfit and hair across all shots. At least 3 poses. | Marble lady needed jump cuts. |
| R5 | Show problem, agitation, then solution. Make the agitation hurt and be funny. | Mark the three beats on the timeline. Agitation has at least 3 quick cuts, one prop each. | "Highlight problem and solution agitation." |
| R6 | No dead gaps. No silent still over 0.3 s. Tail after the last sound under 0.3 s. | `silencedetect` and `freezedetect` (see `ad-video-editing`). | Round 4 had dead gaps. |
| R7 | Speed up the picture, not the voice. Normal speech pace. | Words per second from whisper: 2 to 3. Cuts every 0.8 to 2 s. | "Sound speed too much, pace better." |
| R8 | Voice, face and ethnicity must match. | A person listens to each voice with the face. Log the voice id per character. | "Ethnicity of source does not match." |
| R9 | A story the viewer can follow. It is personal and coherent. | Read the captions alone. They tell one story in the first person. | Meltdown: "random words". |
| R10 | Captions have spaces. At most 3 words. Time them to the audio. | Measure the pixel gap. Compare caption start with the whisper word start (under 0.15 s). | Caption spacing and sync. |
| R11 | Mouth movement matches speech. Mouths close in laugh breaks. | Mouth-open against voice level, at least 0.4 per talk. List each failing line. | Sitcom v2 and v3. |
| R12 | Never cut to a static image that makes no sense. | Check each cut. Every shot has motion or a reason to hold. | Sitcom v2 feedback. |
| R13 | Back-and-forth dialogue is wanted. Keep it and add more. | Count speaker changes. At least 4 in a sitcom. | "Love the dialogue." |
| R14 | Sound is required. The ad also works muted. | Play with sound off. The story and the offer still read. Ship both files. | Round 3 had no sound. |
| R15 | Hold the object identity. A phone stays a phone. | Compare held objects in frames across the clip. | Phone turned into a notepad. |
| R16 | Lo-fi organic look. No logo. Almost no text. | Look at the frames. No logo, no studio polish. | Polished images were rejected. |
| R17 | Housing safety. "dramatization" label. No invented numbers. No real people. No children. | Run the policy lint on all text and captions. | Housing special ad category. |
| R18 | Cost goes down each time. Report cost per video by stage. | Compare with the last video of the same format. Explain any rise. | Goal: cut cost 50 to 75 percent. |

## Cost ratchet (R18)

- Set a hard cap before you spend. One writer per spend log.
- Reuse faces, sets, stills, clips and voice ids from earlier videos first.
- Pick one lip-sync model for a format and keep it. Do not repeat a bake-off.
- Do not make the same still twice. Do not pay for an unused line.
- Write `COST_NOTES.md`. Show cost per stage and against the last video of the format.
- A video that costs more than the last one of its format needs a one-line reason.

## Reviewer checklist

1. Open this file. For each rule write PASS, FAIL or NOT CHECKED with a measured value.
2. A NOT CHECKED rule blocks the ship.
3. Say what you cannot judge. Voice fit and sound fit need the owner's ear.
