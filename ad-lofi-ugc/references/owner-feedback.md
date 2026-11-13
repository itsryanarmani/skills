# Owner feedback rules

Each rule is a past owner correction. Check every rule before you ship an ad video.
An adversarial reviewer must test each rule and write PASS or FAIL with a measured value.
When the owner gives new feedback, add a rule here in the same PR that fixes it.

| # | Rule | How to check | Origin |
| --- | --- | --- | --- |
| R1 | Wild emotional hook in the first second. | Watch 0 to 1 s with sound off. Record what frame 0.0 s shows. It must be a strong emotion or an odd event. | Round 3 hook was "not intriguing". |
| R2 | Cause comes before effect on screen. Show the action, then the result, then who reacts. | Step through 0 to 3 s. No character appears without a reason. No object is already broken. | Sitcom: door fell, people appeared at 0:02. |
| R3 | Change the camera angle, not only the zoom. | Look at the frames: the scene-cut filter cannot see a zoom. About one new angle or pose every 2.5 s. Cuts differ in side, height or pose. | "Different left and right views, not slow zooms." |
| R4 | The same person must show different poses and angles. | Same face, outfit and hair across all shots. At least 3 poses. | Marble lady needed jump cuts. |
| R5 | Show problem, agitation, then solution. Make the agitation hurt and be funny. | Mark the three beats on the timeline. Agitation has at least 3 quick cuts, one prop each. | "Highlight problem and solution agitation." |
| R6 | No dead gaps. No silent still over 0.3 s. Tail after the last sound under 0.3 s. | `freezedetect=n=-60dB:d=0.3` crossed with `silencedetect=n=-35dB:d=0.25`. A range in both is a dead gap. | Round 4 had dead gaps. |
| R7 | Speed up the picture, not the voice. Normal speech pace. | Words per second from whisper: 2 to 3. Average shot length: 1.2 to 1.5 s for a fast punch edit, 1.5 to 2.2 s for a lo-fi story. No shot over 2.5 s. | "Sound speed too much, pace better." |
| R8 | Voice, face and ethnicity must match. | A person listens to each voice with the face. Log the voice id per character. | "Ethnicity of source does not match." |
| R9 | A story the viewer can follow. It is personal and coherent, in the first person, as a dramatization. It makes no factual claim. | Read the captions alone. They tell one story in the first person. | Meltdown: "random words". |
| R10 | Captions have spaces. At most 3 words. Time them to the audio. | Measure the pixel gap: at least 14 px of clear gap between words at 1080 px. Compare caption start with the whisper word start (under 0.15 s). | Caption spacing and sync. |
| R11 | Mouth movement matches speech. Mouths close in laugh breaks. | Manual spot check until measured: mouth movement starts within 100 to 200 ms of voice onset (see `ad-video-editing` qa.md section 6). Where a lip-landmark tool ran, give its correlation (0.4 or more) and the tool name. List each failing line. | Sitcom v2 and v3. |
| R12 | Never cut to a static image that makes no sense. | Check each cut. Every shot has motion or a reason to hold. | Sitcom v2 feedback. |
| R13 | Back-and-forth dialogue is wanted. Keep it and add more. | Count speaker changes. At least 4 in a sitcom. | "Love the dialogue." |
| R14 | Sound is required. The ad also works muted. | Play with sound off. The story and the offer still read. Ship both files. | Round 3 had no sound. |
| R15 | Hold the object identity. A phone stays a phone. | Compare held objects in frames across the clip. | Phone turned into a notepad. |
| R16 | Lo-fi organic look. No logo. No text except captions and the dramatization tag. | Look at the frames. No logo, no studio polish. | Polished images were rejected. |
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

1. Open this file. For each rule write PASS, FAIL, NOT CHECKED or OWNER CHECK with a measured value.
2. A NOT CHECKED rule blocks the ship.
3. Use OWNER CHECK for what only a person's ear can judge: R8 voice fit and the sound fit in R14. Send those to the owner with the video.
