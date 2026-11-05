# Style: anime, heavy cuts

First used for: a protest-button product (a launch film made only from generated footage, 25.7 s, 2026-11-05).

## Use it for
A "one voice against a wall" story with a clear hero, a villain object and a payoff. Strong for products where
many people act together. It carries no real product footage, so keep one real screenshot as the proof beat.

## Look
- Ground: modern 2D anime, cel shading, bold ink lines, hard shadow blocks, speed lines, bloom. Three-color
  palette taken from the product (here orange, cardboard tan, ink black). Frame 0 is a finished key-art frame.
- One original hero with one locked description. Never a real person. Never a real company as the villain.
- Villain is an object (a price tag made of storm cloud), not a brand.
- Type: Barlow Condensed 700, uppercase, white fill, hard ink offset shadow, skewX -6, two lines max.
  One accent word in the palette color (never accent text on an accent ground: contrast fails).
- Tag "SIMULATED" top right for the whole film. End card on paper: mark, name, one-line promise, URL, one note line.

## Pipeline that worked (cost about $6)
1. Hero still first (`seedream-v4`, $0.027). Look at it. Then 16 shots as `seedream-v4/edit` with the hero as the
   reference, so the hero face holds across six shots. Append "zero writing, zero hashtags, zero neon lettering" to
   any shot with signs or buildings: the model prints junk text on them.
2. Contact sheet of all stills. Fix stray text and wrong mood before any video spend.
3. Veo 3.1 Fast on Vertex, image to video, 4 s, 720p, audio off, one clip per hero shot (8 clips, about 1 min each,
   4 in parallel, about $0.15 per second). One camera move and one action per clip. Stills not animated by Veo get
   a punch, push, pull or pan in the edit.
4. Lyria 2 bed (32 s, about $0.06). Its loudness is flat, so build the drop in the edit with a volume lane.
5. ElevenLabs sound effects (about $0.002 each): whoosh, impact, slam, stamp, riser, ring, pop.
6. Beat grid with `hyperframes beats`, then edit in HyperFrames from a spec (`video-film/film_build.py` in the
   scripts repo). All times are in beats.

## Storyboard template (140 BPM, beat 0.429 s, bar 1.714 s, 60 beats)
| Beats | Shot | Purpose |
| --- | --- | --- |
| 0-7 | Hero key art with Veo push-in, hook text | Pain, in plain words |
| 7-11 | Four 1-beat inserts: eyes, thumb on send, paper plane into a void, blank stamp | The cost, fast |
| 11-15 | Split-panel grid of people alone, one text line | Stakes |
| 15-16 | Near black, one orange dot grows, music ducks | Breath before the drop |
| 16-23 | Hero slams the button, white flash, shake. Name, then promise | Value on the drop |
| 23-34 | Burst: 1-2 beat cuts (signs rise, stream, spiral, scroll), then a held scroll with one line | Demo |
| 34-40 | Charge, crowd, strike on the gate (flash, shake), gate turns green with one neutral status line | Action and result |
| 40-48 | Real screenshot in a framed panel, then sunrise payoff line | Proof, payoff |
| 54-60 | End card, 2.5 s | Install or link |

## Rhythm rules
- Burst shots last 1 to 2 beats (0.43 to 0.86 s). Never two equal lengths twice in a row. Text shots hold 4 beats or more.
- Flash: white, 3 frames, decay 0.22 s, on the downbeat of each impact. Shake: six x/y steps of 0.045 s, decaying.
- Radial speed-line overlay (`repeating-conic-gradient` with a radial mask, `mix-blend-mode: screen`) from the first burst
  to the strike, rotating slowly.
- Text slam: scale 1.7 to 1, x -70 to 0, opacity 0 to 1 in 0.2 s, `power4.out`. Second line enters 0.6 beat later.
- Cut on beats. Put every impact on a beat. Put an SFX 0.05 s before each cut.

## Music prompt (Lyria 2, negative: vocals, singing, lyrics, speech)
"Epic anime action soundtrack, 140 BPM, driving taiko drums and breakbeat, aggressive staccato strings, electric guitar
stabs, orchestral hit on every downbeat, a short drop to near silence before a huge impact, then full power again,
shonen battle energy, instrumental." Duck the bed to 0.12 on beat 14.4 and slam it back to 1.0 on beat 16.

## Traps seen
- The model puts text on signs and buildings. Name every surface "blank" and check the contact sheet.
- Orange text on an orange frame failed the contrast check. Use white text with an ink shadow.
- `Impact` in a font stack fails the font check. List only the bundled family.
- A closing line needs 2 s on screen at least. End card stays 2.5 s and the last line enters by +0.46 s.
- Veo clips begin on a burst. That suits a cut on the downbeat. Trim with `data-media-start`, not by speeding up.
- gcloud tokens for Vertex expire. See `launch-video-generation` for the re-login path.
