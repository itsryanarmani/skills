---
name: ship-demo-video
description: "Use for any product's launch, demo or announcement video, built from real footage of the product working: capture from its own harness, a plain captioned cut, then a designed 20-26 s HyperFrames cut on a generated instrumental bed with cuts on detected beats. Holds the series brief, polish rules, privacy audit, spend caps and a style library of proven looks with music prompts and SFX cue maps, plus HyperFrames traps from real renders. Draws on launch-video-generation for generated stills and image-to-video."
---

# Demo videos from real product footage

A demo cut from real footage proves the product works. Generated imagery cannot. This skill takes a product
from "it runs in a test harness" to a 20 to 30 second video that is ready to post, and back again
when the product changes.

**Start here for any product video.** Use this skill first for every launch, demo or announcement video,
whatever the product. When a shot needs generated imagery (AI stills, image-to-video, a cinematic scene),
take the technique from `launch-video-generation`. For the post that carries the video, use
`social-launch-post`.

## Series brief

Every video in a set follows these rules. When several agents make a set, copy them into one shared brief
and add only the per-video facts: product, style, install line, avatar look.

- **Length and grid.** 20 to 26 s. Pure graphic shots last 1 to 1.5 s; text shots hold for the reading pace
  (see the polish rules). Cut on beats detected with `npx hyperframes beats`, and skip beats as needed.
- **Arc.** Hook in outcome language → value (name and promise) by beat two → the demo on the musical drop →
  proof from measured numbers only (the product's own tests or artifacts; never invent a number) → end card
  with the exact install command and the repository URL.
- **Frame 0 is a hook.** The first frame is a finished graphic with the hook line, never a logo, a title or a
  fade-in. A viewer decides in that frame.
- **One idea per screen.** One hero (text or a graphic), one visual action.
- **Detailed art, not flat shapes.** Draw high-quality, detailed SVG art. Flat circles and rectangles read as
  childish. For isometric objects and figures, use the `anatomy` skill (wheresryan22/anatomy).
- **Reuse a proven style.** Pick a style from the [library](styles/README.md) and reuse its music prompt and
  SFX pack. Inside one set, give each video a different style. Invent a new style only when the library runs
  out, and write its spec after it ships.
- **Names.** Do not use a host platform's trademark as the product name; "for Firefox" or "runs in Chrome" is
  fine. No "demo" in an on-screen product name. Read the package name from `package.json`; it can differ from
  the repository name.
- **Plain language.** Write for a viewer who knows nothing about the field: short sentences, active voice,
  common words. Run the `humanizer` skill on the copy.
- **Music.** Two instrumental variants per video, chosen by the per-second loudness curve (stage 4). SFX on
  cuts, clicks and slams.
- **Spend cap.** Set a hard cap per video before the first call, for example $0.30 for music and SFX and
  $0.15 for images. Check the provider balance before each call, log each charge to `spend.jsonl`, and stop
  and report when the shared balance drops under $0.50.
- **Keys.** Source each API key from its secrets file inside the command. Never print a key.
- **Avatar.** Only on the videos that get one (see the presenter section). Duck the music to about 0.26 under
  the voice. Build everything else first and add the avatar last.
- **Privacy is a stop-ship.** Run the safe-end guard and the frame audit (stage 1 and stage 7) on every
  render.
- **Scope.** Work in a media folder outside the product repository. Do not commit media, push, open PRs or
  post anything as part of making the video.
- **Report per video.** Path, style, length, music model and cost, avatar look, audit result, blockers.

## Stages and gates

Each stage ends at a gate. Do not start the next stage before the gate passes.

| Stage | Output | Gate |
| --- | --- | --- |
| 1. Capture | Raw footage per scenario, with the time of each moment that matters | Every frame shows only the product window |
| 2. Plain cut | One captioned MP4 under 60 s | Ready to share as is; the fallback if stage 5 slips |
| 3. Storyboard | Hook, beats, a frame table with "why" per frame | Each claim traces to footage or a measured run |
| 4. Music | Instrumental bed and a bar grid | No vocals; strong first downbeat; clean last bar |
| 5. Build | HyperFrames project per video | `hyperframes check` passes with no findings |
| 6. Stills | One still per scene, on a contact sheet | Director notes resolved (see the checklist) |
| 7. Render | Final MP4, verified | Duration, streams, loudness and frames checked |
| 8. Save | Corrections written back into this skill | The next run starts from the corrected skill |

In collaborative mode the human approves stages 3, 6 and 7. In autonomous mode, post the storyboard
and contact sheet as heads-ups, and still do the stage 6 review yourself before you render.

## 1. Capture real footage

Drive the product from the same end-to-end harness that tests it, with a visible (headed) browser.
Record the screen while the harness runs. This gives footage of the real product on real sites, and the
run doubles as a test.

### Record the window region, not the screen

- On macOS, `screencapture -v` writes **no file** when a parent process stops it with a signal. A wrapper
  that sends SIGINT gets nothing back. Use ffmpeg's `avfoundation` screen input instead, and finish it by
  writing `q` to its stdin. That closes the file correctly.
- Park the browser window at a fixed position and size before recording (for example with `peekaboo window
  move/resize`), then crop the capture to that region. On a Retina display the crop is in pixels, not
  points: multiply the window rectangle by 2.
- Check a frame from the first test capture before the real run. The crop must show the window and nothing else.

### Privacy

A full-screen capture leaks the menu bar, OS notifications and other apps' windows.

- Crop to the product window. If something still covers it (a persistent notification over a side panel),
  compose the video from two crops instead of touching the user's desktop.
- **Cut every segment before the browser closes.** Harness logs are often buffered. The time a "done" line
  prints can be later than the moment the window closed, and the frames between show the desktop. Sample
  frames around the end of each run and cut before the last product frame.
- Review the tail of every segment frame by frame before you share anything.
- Cut harness segments that show a user name or account, not only the frames after the last product frame. A
  harness log line such as `"user":"<name>"` on screen is a leak too.
- Record the last product frame of each source file (for example 38.45 s), and make the build refuse any
  clip whose `data-media-start + data-duration × rate` reads past it. A cut made 0.3 s too late put a private
  notes window into a finished social video. The guard turns that mistake into a build error:

  ```python
  SAFE = {"flights": 38.45, "maps": 38.65}  # last product frame of each source, in seconds
  for cid, src, start, dur, media_start, rate in clips:
      end = media_start + dur * rate
      assert end <= SAFE[src], f"{cid} reads {src} to {end:.2f}s, past the safe end {SAFE[src]}s"
  ```
- Scrub the final frames for any personal window, notification, email address, file path with a user name,
  or token. One leak stops the release.

### Third-party sites

- Use logged-out sessions. Do not record personal accounts.
- Do not send content to a third party on the user's behalf just to film it. End the scene with Cancel and
  show the full send flow on a local test page.
- Probe first. Load each candidate site, check that the element under test exists (a composer, a consent
  banner) and that no bot wall appears, then choose the sites to film.
- Real sites find real bugs. On one run, filming a consent add-on on a real site showed it following a policy
  link out of the dialog, and saving consent with every optional switch still on. Fix the product first,
  then re-record. Do not film around a bug.

## 2. Make a plain cut first

Cut the raw footage into one MP4 under 60 seconds: trim each scenario to its active window, add one caption
per scene, scale to 1600 px wide. This is shareable on the same day, and it is the fallback when the designed
cut slips.

- Homebrew ffmpeg builds often lack the `drawtext` filter. Render each caption as a transparent PNG (any
  image library) and `overlay` it.
- Keep scenes at real speed in the plain cut. It is the honest version.

## 3. Storyboard the designed cut

Write the plan before any HTML. A frame change here costs a minute; after a render it costs a cycle.
For the script itself (beats, hooks, second-by-second turns, the call to action), use
`launch-video-screenwriting` first, then lay out the frames below.

- **Hook in outcome language.** The first beat says what the viewer gains or avoids, not what the product is.
  "You're one Enter away from pasting your email into an AI" beats "PII Guard detects PII".
- **Value by beat two.** The product name and its one-line promise land in the second scene.
- **Evidence after value.** Footage scenes show the promise working. Each scene gets a short topline that
  says what the viewer is seeing, and changes when the footage changes.
- **Proof from measured runs only.** Use the numbers your harness measured (a timing, a pass count, "0
  network requests"). Do not invent a statistic for impact.
- **End card.** Name, one-line description, where to get it. Do not claim a store listing that is still
  under review. Copy the install line exactly from the README (`npm create <name>@latest`,
  `npm i -g <name>`, `npm i <name>-agent`). A generic `npm i <name>` is wrong for most packages.
- Present it as a proposal: one line saying "this video tells [audience] that [message]", then a table of
  frame, beat, on screen and why. Cut any frame whose "why" does not trace back to the message.

**Start from the [style library](styles/README.md).** It holds every proven look, with a
table to choose from, and the [presenter](styles/presenter.md) module, each specified down to the copy, eases, music prompt and SFX cues.

**Give each video its own style.** A first pass where three videos shared one look (dark radial gradient,
every line fading up, 13 s scenes) came back as "too generic". What fixed it:

- One style per video, each with its own ground, type pair, ease family and tempo band. For example: a
  light gray stage with white cards and exponential whips; cream paper with a dot grid and giant serif beats;
  flat color grounds that cut on the beat, with condensed display type.
- Shorter: 20 to 26 seconds, cut on beats. Fast cuts suit pure graphic frames; any frame with text holds
  long enough to read (see the polish rules below).
- A clear arc: hook, stakes, value, demo on the musical drop, payoff, end card.
- Varied text entrances: masked per-word rise, velocity-matched waterfall (the first word travels furthest),
  blur-to-sharp scale slam, frame-stepped typing, hard-cut word swaps on beats, wide-to-tight tracking.
- Designed seams: whip off with blur, zoom-through, mask open, color cut. Not crossfades.

Mine a real library for these patterns before writing any. HeyGen's `hyperframes-launches` repository has
the source of its launch films. Clone it without large media (`--filter=blob:limit=300k`; the media is in
Git LFS) and have a subagent extract a lookbook with file and line citations: grounds, text techniques,
seams, pacing, sound cues and story arcs.

**Reference beats description.** Name one or two reference videos whose pacing and type you want to match
(launch-video galleries such as whatships.com). Without a reference, an agent falls back to the same default
look: centered text, gradient background, everything fading in. For a big launch, ask for three storyboard
variants and pick one.

### Polish rules

A second round on a 19-video set fixed what the owner still disliked: too much text, too many screenshots,
and cuts too fast to read. Apply these from the first storyboard.

- **Reading pace.** Hold a frame with a sentence until a slow reader finishes: about 3.5 s, plus 0.3 s
  for each word over six. A text frame has at most about 8 words. When in doubt, cut words, not time. That gives about 8 to 10 shots in 20 to 26 s. Cut on beats, but
  skip beats.
- **One idea per frame.** Text or a graphic is the hero, not both. One visual action per shot: never stack
  a screenshot, a scan, a callout and a label in one frame.
- **Graphics are the story.** Draw the UI as animated SVG in the video's style: a cursor clicks, a toggle
  flips, a form fills itself, a stamp lands, a shield blocks an arrow. Use at most one real screenshot per
  video, as a quick "this is real" beat, cropped tight. No terminal, code, JSON or log shots unless the
  viewer needs that exact command.
- **Less text.** At most about 40% of shots carry a text line. The rest carry a 1 to 3 word label at most.
  No two shots in a row use the same entrance.
- **A copy frame per video.** Pick PAS (problem, agitate, solve), BAB (before, after, bridge) or AIDA, and
  vary it across the set. Open on an everyday situation or the worst case, in plain words for a viewer who
  knows nothing about the field. "Do you remember what you ordered yesterday? Neither does your AI."
- **Proof that lands.** Do not put "N/N checks pass" in every video. Prefer one concrete outcome ("0
  requests left your laptop"), and keep numbers only where they carry the story.
- **Frame 0 is the poster.** The first frame is a finished graphic with the hook line, never blank, black
  or a fade-in. Export it as `<name>-poster.png` next to the MP4; it is the social thumbnail.
- **Truth.** Never present a scripted or test agent as a real one; label it "scripted" or "test agent".
  Show no invented URL or domain, only the real repository and package names. Do not invent incidents,
  and name a company as breached only when it is public record.

### The why behind the polish rules

A third round of owner notes came with a reason for each. Apply the reason, not only the rule.

- **One solid ground per video.** A busy or shifting background competes with the graphic, so the eye
  cannot find the one idea. Let the graphic carry the contrast. Use no background you would not pick on
  purpose; if in doubt, use a solid or a subtle gradient in the palette.
- **Graphics explain, they do not decorate.** A graphic that does not show the mechanism is noise. Each
  one shows cause and effect at a glance: what goes in, what is blocked, what comes out.
- **Show, don't tell.** People remember a story and a metaphor, not a claim. Find the product's metaphor
  and build the video on it: a needle in a haystack, a web page seen as a painting, footprints that leave
  damage.
- **Art direction can follow the music.** Under an artistic score, a literal UI demo feels flat. Lean into
  the art reference: a website painted as a famous modern painting, a magnifier that sweeps a haystack of
  UI and zooms in on the one target.
- **Hidden versus visible must be obvious.** A prompt-injection video fails if the viewer cannot see what
  a person sees and what the agent reads. Show the visible page, then reveal the hidden layer with patterns
  real sites use: a hidden div, an `aria-label` or `alt` text, white-on-white or 1 px text, off-screen
  text, an HTML comment, zero-width characters. Never name a real site as compromised.
- **Real logos for real services.** A known logo makes a viewer relate in a fraction of a second; text
  cannot. Use the official SVG (Simple Icons, CC0, or the brand's press kit), unmodified and at a normal
  size, only to name a service the product works with or compares against. Never imply an endorsement.
- **Draw AI the way people see it now.** A cartoon robot reads as dated. Use the current assistant
  language: a soft orb, pulsing dots, a sparkle, a minimal face. Draw your own; do not copy a company's mark.
- **The poster is a thumbnail.** Header and footer text make it unreadable at small size. Use one hook
  line and one strong graphic or logo.
- **Exact alignment.** An overlay that sits a few pixels off (a replacement word not directly over the
  word it replaces) reads as fake and breaks the trust the video builds. Check every overlay in the stills
  review.

## 4. Music bed

- Generate an instrumental per video at the exact length you need. On WaveSpeed, `elevenlabs/music` takes
  `music_length_ms` and `force_instrumental`. It bills $0.01 per second, so a 25 s track costs $0.25. State a tempo, "starts on a strong
  downbeat, no long intro" and "clean ending on the final bar" in the prompt.
- Check every file. Equal byte sizes are normal for constant-bitrate output; compare checksums to confirm the
  tracks differ.
- Detect beats (HyperFrames: `npx hyperframes beats` in the project). A detector can report double the
  tempo you asked for, because it counts eighth notes. Take the median gap and derive the bar: the bar at
  112 BPM is 2.143 s.
- Match the genre to the story, and make the genres differ across a set of videos: a thriller cue with a
  drop for a "caught in time" story, funk-pop for a "clearing clutter" story, a sparse keynote bed under a voice.
- Generate two variants per video from two models, then choose by energy curve, not by name. Under a
  $0.30 cap per video, make the second variant with `minimax/music-02` (about $0.03), not
  `minimax/music-2.6`. `music-02` has no instrumental flag: put "instrumental only, no vocals" in the
  prompt and run speech-to-text on the result to check for lyrics. Print the
  loudness per second (`ebur128`) and look for the shape the story needs: a strong first second, a drop
  where the demo starts, a clean end. Trim a long track to its best section instead of regenerating.
- Add SFX on the story's actions: a whoosh on each whip, a click and pop on taps, a stamp or hit on the
  slams, typing under typed text, a chime on success. `elevenlabs/sound-effects-v2` on WaveSpeed costs
  about $0.002 per effect. Give each SFX `<audio>` its own track and a slot equal to the file length.
- Put every scene boundary on a bar. Hard cuts inside a scene go on beats.
- Under a voice, duck the bed to about 0.26 while the voice plays and bring it up as the voice ends. Keep
  SFX at 0.3 or less under the voice and 0.6 or less elsewhere. The voice must sit clearly on top.
- Run a final `loudnorm` pass on the rendered file (about −16 to −14 LUFS integrated, peak below −1 dB).
  The renderer can ignore the mix volumes, so measure the output, not the composition.
- Fade the bed in over the first 0.4 s and out over the last 1.5 s, using a volume automation lane, not a
  timeline tween. Target about −16 dB mean and a peak below −1 dB.

## 5. Build with HyperFrames

HyperFrames renders video from HTML: `data-*` attributes set the timing, one paused GSAP timeline per
composition drives the animation, and the CLI checks, snapshots and renders.

- Install its skills (`npx hyperframes skills update`, then the workflow skill), and start every build at
  the `/hyperframes` router. A remix of existing footage routes to `general-video`.
- Write `BRIEF.md` (message, destination, aspect, length, assets with source timestamps) and a `STORYBOARD.md`
  with one block per scene, even when no human reviews it. On resume, these files are the only record of the decisions.
- When any scene uses generated stills or clips, keep the record in one `board.json` that follows
  `video.schema.json` (the `storyboard-video` tool in pooriaarab/scripts) instead of the two Markdown files. See
  "Keep the record in board.json" in `launch-video-generation`. Footage-only cuts keep `BRIEF.md` and
  `STORYBOARD.md` until the schema has a footage shot type.
- Use one project per video, with the same scene set: hook, value, footage with a topline, proof, end card.
  Generate the scene files from one spec per video so all videos share one structure.

### Structure rules from real lint and render failures

| Trap | Rule |
| --- | --- |
| A timed `<video>` inside a timed wrapper shows wrong frames, then vanishes | Time the video. Keep its card wrapper untimed. |
| The untimed card wrapper shows as an empty frame during the hook | Hide it in CSS (`opacity: 0`), then reveal it on the timeline. Not `tl.set` at 0. |
| A `fromTo` on a hard-cut card renders its "from" state at build time and shows the card early | Hard cuts use `tl.set` at the cut time. Zoom tweens take `immediateRender: false`. |
| Nested markup in a timed scene gets the warning "nested structure needs sub-composition" | Every text scene is a sub-composition with its own timeline in scene-local time. |
| Footage zooms set from a sub-composition do nothing | Animate the footage on the main timeline, at global time. |
| Repeated kicker elements with no tween overlap their neighbours | One element per distinct label. |
| Decorative ghost text fails the contrast audit | Use non-text decoration (glow, grid), or none. |
| Negative `z-index` highlight disappears | Order it in the DOM: the highlight first, the word in a positioned span after it. |
| Unbundled fonts warn and can fail in cloud renders | Use a bundled pair, for example Montserrat for display and JetBrains Mono for labels. |

### A presenter in the corner

For creator-style edits around a presenter (kinetic hook, gravity drop, text behind the speaker, screen push,
crash zooms, prompt bar, icon strike, giant captions, title cards), use [edit-effects](references/edit-effects.md).
For a handheld selfie presenter instead of a studio look, see the selfie section of [presenter](styles/presenter.md).

A talking presenter in a corner card makes a demo personal. The script does not need to narrate the
footage; a short founder intro over it works.

- HeyGen's current API is `POST /v3/videos` (`type: avatar`, `avatar_id`, `voice_id`, `script`,
  `aspect_ratio: "1:1"`, `resolution`, optional `voice_settings.speed`), then poll `GET /v3/videos/{id}`.
  List looks with `GET /v3/avatars/looks` (`limit` at most 50). The v2 endpoints return a sunset warning.
- Prefer the user's own digital twin and cloned voice. Check every claim in the script against the
  product, the same as on-screen copy. Keep the script to about 40 to 50 words.
- The default Avatar IV engine gave the twin fake, veneer-like teeth. Render with
  `engine: {type: "avatar_v", reference_look_id: <the filmed twin's look>}` instead.
- For a new outfit or angle, edit real photos of the person, not a text-to-image portrait: an image-edit
  model (WaveSpeed `google/nano-banana-2/edit`) with four original photos as references, then a HeyGen
  photo look in the twin's group (about $1.32 each). Use a different outfit in every avatar video of a set.
- Talking-photo models on WaveSpeed were weaker. InfiniteTalk came closest and cheapest (about $0.07 per
  second) but still lost to Avatar V; Kling, LongCat and Pruna were rejected.
- For voice only, HeyGen `POST /v3/voices/speech` with engine `orca` costs about $0.004 per second and
  matched the speaker at 0.954 similarity.
- Keep the avatar's own background and put it in a rounded card. A solid card needs no alpha channel;
  transparent WebM needs a matting-enabled avatar.
- Keep the avatar's sound on its `<video>` (`data-has-audio="true"`), and duck the music under it.
- Measure the avatar clip with `ffprobe` before you time the scenes. A clip can come back shorter than the
  plan, and a fixed timeline then holds a silent end card for 5 s. Fit the end card to the clip.
- Vary the look across a set: other outfits and camera angles of the same twin (`GET /v3/avatars/looks`)
  keep several avatar videos from reading as one recording. Never repeat an outfit in a set.
- Avatar clips cost about $0.05 to $0.09 per second, with a minimum per clip. Render one clip per video at
  full script length (about 15 to 20 s); a short test clip still pays the minimum.

### Asset paths in sub-compositions

- A sub-composition may not reference `../`. Lint rejects it. Put fonts and images next to the
  sub-composition files (`compositions/fonts/`, `compositions/banners/`) and reference them relatively.
- Lint checks each sub-composition alone, so each one that uses a custom font needs its own `@font-face`.
- Verify font files before use: a clone without LFS gives 130-byte pointer files, not fonts. Download open
  fonts (for example from Google Fonts) as woff2 instead.

### Footage handling

- Trim with `data-media-start` plus `data-duration`. Speed up dull stretches with `data-playback-rate`
  (1.15 to 1.65 reads as real; faster looks fake).
- Footage is muted. The only sound is the music `<audio>`, which needs an `id`, or it is silent.
- **Push in on the subject.** Full browser footage is unreadable on a phone. Zoom the inner wrapper to the
  element that matters (the composer, the prompt, the result, the route), and pull back before the cut.
- Zoom math, with `transform-origin` at the center: to center a point at fraction `p` of the width at scale
  `s`, set `xPercent = -(p - 0.5) × s × 100` (the same for y). Keep `|xPercent| ≤ (s − 1) / 2 × 100`, or
  the footage edge shows as a dark strip.

### Motion doctrine

Smooth long-tail settles (`power3.out`), never bounce. Reveal each element when its beat arrives, not all
at once. No breathing loops, no slow drift on content in the back half of a scene. One slow, finite drift
on a background glow is enough life. All motion lives in the paused timeline; no CSS animations.

## 6. Review the stills

Run `npx hyperframes snapshot --at <times>` with one time per scene, at the moment that carries the
scene. Read the contact sheet as a director. Check each item:

- No empty cards, stray frames or bleed from a scene that is not on screen.
- Text inside the footage is legible at phone size. If not, push in.
- No cropped words in toplines or in the footage after a zoom.
- No exposed footage edge after a pan.
- Each scene stays long enough to read its topline twice.
- No desktop, notification or private content in any frame.

Give notes in camera words: "push in on the prompt at 15.4 s", "hard cut on the bar at 19.32", "pull back
before the cut". "Make it better" gets random changes. Re-snapshot after each round of fixes.

## 7. Render and verify

- `npx hyperframes render --quality high --output renders/<name>.mp4`. A 40-second 1080p render takes about a
  minute on a laptop.
- Verify the file, not the log: `ffprobe` duration and streams (video and audio present), a frame grid
  across the whole video, and `volumedetect` for loudness.
- Make the frame grid with this audit script, and read every tile before anyone sees the video
  (`python3 audit.py <video.mp4> <grid.png> [...]`):

  ```python
  # Frame audit: one frame every STEP seconds of each video, tiled into a grid PNG.
  import subprocess, sys
  from io import BytesIO
  from PIL import Image

  STEP, W, COLS = 1.5, 320, 6
  for path, out in zip(sys.argv[1::2], sys.argv[2::2]):
      d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                "-of", "csv=p=0", path], capture_output=True, text=True).stdout)
      imgs, t = [], 0.7
      while t < d:
          png = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", path,
                                "-frames:v", "1", "-vf", f"scale={W}:-1", "-f", "image2pipe",
                                "-vcodec", "png", "-"], capture_output=True).stdout
          imgs.append(Image.open(BytesIO(png))); t += STEP
      h, rows = imgs[0].height, (len(imgs) + COLS - 1) // COLS
      sheet = Image.new("RGB", (COLS * W, rows * h), "black")
      for i, im in enumerate(imgs):
          sheet.paste(im, ((i % COLS) * W, (i // COLS) * h))
      sheet.save(out)
      print(out, len(imgs), "frames")
  ```
- Deliver into the product's media folder, outside the repository. Never commit media to a repo whose
  checks reject committed proof files. Open the folder for the human.

## 8. Save the corrections

After the human watches the result, write each correction back into this skill: a new trap, a note the human
repeated, a gate that was missing. The next agent reads the skill, not this chat.

## Formats

- 16:9 at 1920×1080 suits X, LinkedIn and YouTube. Make this cut first.
- 9:16 needs a new layout (footage card on top, topline below), not a crop of the 16:9 cut.
- Keep each cut at 20 to 30 seconds for a feed. Put the hook in the first 2 seconds.

## Related skills

- `launch-video-generation`: generation techniques this skill draws on: image-to-video, AI stills, music
  and voice models.
- `launch-video-screenwriting`: script craft for the storyboard: beats, hooks, value turns per shot.
- `anatomy`: detailed isometric SVG figures for graphic shots.
- `social-launch-post`: the post that carries the video.
- `app-screenshots`: store screenshots from the same product runs.
