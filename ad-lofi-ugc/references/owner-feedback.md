# Owner feedback rules

Each rule is a past owner correction. Check every rule before you ship an ad video.
An adversarial reviewer must test each rule and write PASS or FAIL with a measured value.
When the owner gives new feedback, add a rule here in the same PR that fixes it.

| # | Rule | How to check | Origin |
| --- | --- | --- | --- |
| R1 | Wild emotional hook in the first second. | Watch 0 to 1 s with sound off. Record what frame 0.0 s shows. It must be a strong emotion or an odd event. In a format with a person, R20 applies. | Round 3 hook was "not intriguing". |
| R2 | Cause comes before effect on screen. Show the action, then the result, then who reacts. In a format with a person, the reaction face of R20 comes first. Then the order is action, result, reaction, all by 3 s. | Step through 0 to 3 s. No character appears without a reason. No object is already broken. | Sitcom: door fell, people appeared at 0:02. |
| R3 | Change the camera angle, not only the zoom. | Look at the frames: the scene-cut filter cannot see a zoom. About one new angle or pose every 2.5 s. Cuts differ in height, pose or distance. A side change stays on one side of the 180-degree line (R21). | "Different left and right views, not slow zooms." |
| R4 | The same person must show different poses and angles. | Same face, outfit and hair across all shots. At least 3 poses. | Marble lady needed jump cuts. |
| R5 | Show problem, agitation, then solution. Make the agitation hurt and be funny. | Mark the three beats on the timeline. Agitation has at least 3 quick cuts, one prop each. | "Highlight problem and solution agitation." |
| R6 | No dead gaps. No silent still over 0.3 s. Tail after the last sound under 0.3 s. | `ad-audio-qa` R6_dead_audio is a coarse guard: FAIL on any stretch >= 1.5 s below -60 LUFS (see `ad-video-editing/references/audio-qa.md`). `freezedetect=n=-60dB:d=0.3` crossed with `silencedetect=n=-35dB:d=0.25` for the picture side is the gate. | Round 4 had dead gaps. |
| R7 | Speed up the picture, not the voice. Normal speech pace. | `ad-audio-qa` R7_speech_pace: true WPS <= 3.4 from the whisper transcript is the tool alarm; the hand target stays 2 to 3 words per second (see `ad-video-editing/references/audio-qa.md`). Average shot length: 1.5 to 2.2 s for a lo-fi story (the gate in `qa.md`), 1.2 to 1.5 s only for a fast punch edit. No shot over 2.5 s. | "Sound speed too much, pace better." |
| R8 | Voice, face and ethnicity must match. | OWNER CHECK: a person listens to each voice with the face. `ad-audio-qa` automates only consistency — R8_voice_consistency FAILs when one character's per-line F0 medians spread >1.6x (see `ad-video-editing/references/audio-qa.md`). Log the voice id per character. | "Ethnicity of source does not match." |
| R9 | A story the viewer can follow. It is personal and coherent, in the first person, as a dramatization. It makes no factual claim. | Read the captions alone. They tell one story in the first person. | Meltdown: "random words". |
| R10 | Captions have spaces. At most 3 words. Time them to the audio. | Measure the pixel gap: at least 14 px of clear gap between words at 1080 px. `ad-audio-qa` R10_caption_sync: median offset <= 300 ms and >= 70% within 300 ms of speech onsets is the tool alarm; the hand target stays 0.15 s (see `ad-video-editing/references/audio-qa.md`). | Caption spacing and sync. |
| R11 | Mouth movement matches speech. Mouths close in laugh breaks. | Manual spot check until measured: mouth movement starts within 100 to 200 ms of voice onset (see `ad-video-editing` qa.md section 6). Where a lip-landmark tool ran, give its correlation (0.4 or more) and the tool name. List each failing line. | Sitcom v2 and v3. |
| R12 | Never cut to a static image that makes no sense. | Check each cut. Every shot has motion or a reason to hold. | Sitcom v2 feedback. |
| R13 | Back-and-forth dialogue is wanted. Keep it and add more. | Count speaker changes. At least 4 in a sitcom. | "Love the dialogue." |
| R14 | Sound is required. The ad also works muted. | `ad-audio-qa` R14_sound_and_cuts and sfx_onset_80ms need `--sfx-stem` (a wav of the sfx and laugh track alone): FAIL "Sound is required" when the stem has no onsets, else FAIL when under 80% of picture cuts have an sfx onset within 80 ms (see `ad-video-editing/references/audio-qa.md`). A voice onset does not count as a sound event. sfx_vs_voice needs `--voice-stem` too. pacing.md: sfx only on events, never one per cut. Play with sound off. The story and the offer still read. Ship both files. | Round 3 had no sound. |
| R15 | Hold the object identity. A phone stays a phone. | Compare held objects in frames across the clip. | Phone turned into a notepad. |
| R16 | Lo-fi organic look. No logo. No text except captions, the dramatization tag and one end card with the offer. | Look at the frames. No logo, no studio polish. | Polished images were rejected. |
| R17 | Housing safety. "dramatization" label. No invented numbers. No real people. No children. | Run the policy lint on all text and captions. | Housing special ad category. |
| R18 | Cost goes down each time. Report cost per video by stage. | Compare with the last video of the same format. Explain any rise. | Goal: cut cost 50 to 75 percent. |
| R19 | Do not show an event the video model cannot render. Show damage another way. | Render one clip first. Look at 3 frames of the event. No duplicate objects (two doors), no melting. If it fails, change the beat (cracking wall, falling plaster). | "No crash, two doors, AI artifact." |
| R20 | In a format with a person, the first frame is that person's reaction face. The cause follows in the next shot or two (see R2). This replaces the 0.0 s check in R1 for those formats. | Frame 0.0 s: a face, eyes and mouth readable, emotion matches the hook. The cause is on screen by 3 s. | "Shocked face in the first frame." |
| R21 | Keep screen direction. Each person stays on the same side of the frame in every shot. Change the angle on one side of the 180-degree line. Do not cross it. | List left/right per shot for each person. No swap, including cutaways. | Street interview: host moved from right to left. |
| R22 | A conversation looks like one: eyelines, head turns, small hand gestures, a slow push-in on the punchline. Do the push-in in the edit as a crop. Ask the model for small gestures only. | Per talking shot: where does the person look? Count eyeline-matched reverse shots (at least 1). Note the crop push-in. OWNER CHECK for how natural it looks. | "Talk as if to someone, more hand movement, zoom in on the guy." |
| R23 | Captions never look jumbled. | Compile `swiftc -O ocr.swift` (macOS Vision, `VNRecognizeTextRequest`, accurate, language correction off). Run it on one frame per caption from the final render. Retry once on an `e5rt` crash. Character error rate (edit distance divided by expected length, upper case, spaces collapsed) 0.10 or less. Do not run `swift ocr.swift` (it hangs). | "Some letters get jumbled." |
| R24 | Show the tool of the format. A street interview shows the microphone in the host's hand. Name the mic in the motion prompt and include it in the R15 frame comparison. | Frame check: mic visible in every host shot, same shape in each. | Interview had no visible mic. |
| R25 | A horror-comic variant needs a scare beat: something moves behind a door, a sting, a reaction. Then it resolves as a joke. | Mark the beat on the timeline. A sting starts within 0.2 s of the beat, then a reaction shot. OWNER CHECK for how scary it feels. | "Feel a little bit scared." |
| R26 | A personal story has a clear hook: the loss, the place, the trust that broke, the surprise. The offer is on the end card. The narrator never says the product worked. See R9 and R17. | Caption read: one sentence per beat, in that order. No line claims a result. | "I spent all my savings on this house ... a slick agent gave me a lien ... someone lives there." |

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
3. Use OWNER CHECK for what only a person's ear or eye can judge: R8 voice fit, the sound fit in R14, and how natural R22 and how scary R25 feel. Send those to the owner with the video.
