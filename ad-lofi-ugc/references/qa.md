# QA gates for lo-fi UGC ads

Four gates run before anything ships: object continuity, the mute test,
orientation, and the policy lint. Plus the spend meter that runs during
generation. Each gate exists because a real failure slipped past a weaker
check.

Before you ship, also test every rule in `owner-feedback.md` (R1 to R26).

## 1. Object-continuity check (video)

Generative video invents and swaps objects. The real failure: a character
held a phone in the hook shot and it became a yellow notepad three seconds
later. Nobody noticed until the owner watched the render.

Method:

1. Extract one frame every 0.5 s from the finished clip
   (`ffmpeg -i clip.mp4 -vf fps=2 frames/f%03d.png`).
2. List every held object, clothing item and prop visible in the first
   frame. Write the list down.
3. View the extracted frames in order and confirm each listed object keeps
   its identity and persists to the last frame. Watch for: a phone becoming
   paper/notepad, hands changing finger count, a garment changing color,
   a prop appearing or vanishing.
4. Reject and regenerate any clip that fails, within budget. Regenerate from
   the predecessor's last frame when the shot is chained.

This is a vision task — a human or a vision model must look at the frames.
Mechanical checks (duration, size, no black frames) do not catch morphs.

## 2. Mute test (video)

Take 6 frames from the `_muted.mp4` version with captions cropped or blurred
out. Look at them as a stranger would — no audio, no text. Write down, in
plain words, what story you understood and what offer was made. Pass only if
the offer is understandable. Fail means: move more of the story into the
picture, or strengthen the caption.

## 3. Orientation check (stills and video)

The real failure: a generated photo came back rotated 90 degrees — a
landscape composed sideways inside a portrait frame. It passed every other
check because the content was fine; only the rotation was wrong.

- Check EXIF orientation on every downloaded still.
- View every still at full size once. Look for horizons, doors, faces and
  text baselines that run the wrong way. A sideways door or a face rotated
  90° is an instant fail.
- Same check on extracted video frames: doorframes and horizons must be
  upright.
- One shipped ad was "almost sideways" because the tilt was baked into the
  generation, not added by the degrade crop. Do not assume the degrade
  caused it — look at the raw candidate.

## 4. Policy lint (copy and claims)

Run before upload, on every variant:

- No invented numbers: no prices, percentages, "below market", savings
  claims. Every figure must be real, dated and sourced.
- No eligibility claims: nothing about who may buy ("you could be
  eligible", "first-time buyers only"). Housing/special-ad-category rules
  restrict this.
- No fake testimonials: no "my friend saved $X", no named endorsements,
  no first-person claims of fact presented as real. A dramatized skit needs
  a visible "dramatization" tag.
- No guaranteed outcomes: no "guaranteed profit", "zero risk".
- Disclose what must be disclosed: virtual staging labeled as such, AI
  synthetic people labeled every time, ad nature clear in
  UGC formats.
- Check claims against the product's fact list. A caption that says
  "inspection window" contradicts a fact list that says homes often cannot
  be inspected before sale — flag contradictions, do not ship them.

## 5. The spend meter

Every billed call logs to one JSON file before the call is made (a
reservation), then updated with the result. Rules learned the hard way:

- **One writer per spend file.** Two generator processes racing one
  `spend.json` clobbered each other's entries — eight call records were lost
  and had to be reconstructed. Use a file lock around every
  read-modify-write (`flock`/`fcntl`), write to a temp file, then rename.
- **Never trust the account balance** when other workers share the key.
  The spend file is the meter.
- **Price-check before every call** against the provider's live model
  catalog; record the price you used and when you checked it.
- **Hard cap per batch** (the run used $1.50 for images, $1.50 for video,
  $3.00 for a video+sound round). Refuse calls that would exceed the cap.
- **Log enough to reconstruct**: provider, model, slug/concept, candidate,
  resolution, estimated cost, status, output filename, prediction id if the
  provider returns one.

Shape that worked:

```json
{
  "provider": "wavespeed.ai",
  "cap_usd": 1.5,
  "price_checked": [{"when": "...", "model": "...", "cost_used_usd": 0.02}],
  "calls": [{"concept": "s3_yard_sign", "candidate": "a", "model": "...",
             "estimated_cost_usd": 0.02, "status": "completed",
             "output": "s3_yard_sign_a.png"}],
  "total_estimated_cost_usd": 0.52
}
```

- **Never print or commit the API key.** Read it from the environment or a
  secrets file; scripts exit if it is missing.

## Sync and pacing gate (run before any video ships)

Frame checks and loudness are not enough. Measure timing too, and save the numbers.

- Silence: `ffmpeg -i v.mp4 -af silencedetect=n=-35dB:d=0.25 -vn -f null -`. A silent range where the picture is also static for over 0.3 s fails.
- Tail: the last audible sound and the last frame are less than 0.3 s apart. The first sound starts within 0.3 s of the first frame.
- Shot length: the average is 1.5-2.2 s for a fast edit. Count cuts with `select='gt(scene,0.3)'`. Zoom cuts inside one shot do not register, so also read the edit list.
- Loudness: sound effects sit under or beside the voice. A laugh track sits about 6 dB under the voice.
- Listen once. These numbers do not prove that an effect fits the picture. A person must judge the sound.
- Run the same script on the old version first. Report before and after.

