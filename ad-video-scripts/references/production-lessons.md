# Production lessons: three 25 s vertical ads from finished scripts (first run, 2026-11-10)

Totals: 77 s of finished video, $1.99 spent (balance drop), about 29 min wall time. That is $0.026 per finished second and about $0.66 per video.

## Where the money went
- Lipsync was about 83% of spend ($1.66 of $1.99, including a $0.25 comparison test). Every clip is paid for at least 5 s of audio.
- Stills (6 edits, 2 text-to-image backgrounds) were $0.16, 8%. Voice (15 lines + 3 auditions) was $0.12, 6%.
- Every drawn card, caption, zoom and final render cost $0 (Pillow, headless Chrome, ffmpeg).

## What worked
- One test still before the batch. It passed on the first try, so the batch of five had no retries.
- Edit-model stills from one reference image kept the face, hair and top across all six poses. Lipsync kept the face in all nine clips.
- Generating each voice line as its own short file ($0.005 each) gave exact slots. Four of fifteen lines ran long and needed 1.06x to 1.30x speed-up. Trimming silence first removed 0.05 to 0.15 s per line.
- Real page captures through the browser debug port gave exact element positions, so highlights landed on the right line. Ask the DOM for rectangles. Do not guess pixels.
- Drawing the safe box on a frame from every shot caught three layout bugs a code check would not: a card edge past the box after zoom, an overlapping subtitle on a boundary frame, an arrow hiding a label.

## What wasted money or time
- The 480p vs 720p comparison cost $0.25 for two clips, and one of them (about $0.10) was thrown away. The frames looked alike at phone size. Skip the comparison next time and use 480p for small faces.
- The price command printed 0.06 (480p) and 0.09 (720p) per unit, but the real charge was about $0.10 and $0.147 for a 5 s clip. Measure one real run from the balance before you plan a budget.
- Padding short lines to the 5 s minimum meant paying for 5 s of video to get 1 to 3 s of talk. Three end-card clips carried 1.1 to 2.8 s of speech. About $0.50 of lipsync bought roughly 7 s of useful mouth movement.
- One TTS model read the style instruction aloud as part of the speech. Check one audition by transcript before you use it.
- The lipsync model dropped a raised pointing arm in one clip and kept it in another with the same still. Do not plan a shot around a hand pose surviving lipsync.
- A balance shown with 2 decimals at the start and 3 at the end leaves about $0.01 of error. About $0.05 of spend stayed unexplained. Log the balance with the same precision at every step.
- A timestamp file written with `>>` after `>` shifted fields in my own log script and corrupted one log row. Write log rows from code, not from shell text splitting.

## Change next run to cut cost at the same quality
1. Lipsync two host shots per video (the hook and one mid shot), six clips for three videos, not nine. Show the other host shots as a slow-zoom still with the voice over.
2. Use 480p lipsync (about $0.10 for a 5 s clip, against about $0.147 at 720p) and skip the quality comparison, which cost $0.25 and was thrown away.
3. Make the voice track first and cut to its real length. Then size every slot to the audio, so no line needs a 1.3x speed-up and no clip pads past 5 s.
4. Keep the single test-still rule. Budget one still retry at $0.02, not five.
Expected: six clips at about $0.10 is $0.60 of lipsync, against $1.66 now. With the same stills and voice, the total is about $1.00, $0.33 per video, $0.013 per finished second. Measure it; do not trust the estimate.

## Build notes
- Keep every on-screen element inside the safe box at the END of the zoom, not at the start. A 5% zoom pushed a card edge past the box. 3% was safe.
- Show caption chunks with an end-exclusive time test. An inclusive test showed two chunks on the same boundary frame.
- Pad the audio track to the video length so a player does not cut the end card short.

## Check list after the render
- Look at one frame per shot with the safe box drawn on it. `safe-frame-check` in the scripts repo does this.
- Transcribe the final audio (about $0.001) and compare it with the script. It catches a wrong voice, a read-aloud style prompt and a spoken price.
- Log every step from code with `prodlog` in the scripts repo, with the balance at the same precision at the start and the end.
