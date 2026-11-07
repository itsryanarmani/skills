# Keynote whip

Calm, confident and fast, like an Apple keynote. Light stage, white cards, big type, and whip cuts with motion
blur. Pair it with the [presenter](presenter.md) card: a founder speaking in the corner over real footage.

**Use it for** a capability that "just works": an agent, an automation, a tool that does a task for you.
First shipped: foxpilot, a 26 s launch video.

## Look

| Role | Value |
| --- | --- |
| Ground | Flat `#f2f4f7` (cool light gray). No gradients, no texture. |
| Ink | `#0f1115` |
| Muted | `#5b6170` (labels, captions) |
| Accent | One brand color darkened until it passes AA on the ground. Firefox orange `#ff7139` became `#d9480f`. Use it only on the key word, the result line and the period of the wordmark. |
| Cards | White, 28 px radius, shadow `0 30px 80px rgba(15,17,21,.18), 0 2px 6px rgba(15,17,21,.08)` |

Type: **Montserrat 800** for display (tracking −0.045 to −0.06 em, sizes 120 to 330 px). **JetBrains Mono** for
labels, goals and URLs. Left-anchored at x = 150 px; the end card's wordmark is centered.

Layout during demos: the footage card on the left (1180 × 920 at 120, 110), a side column on the right
(x 1370, 470 wide) for the typed goal, and the presenter card bottom-right.

## Copy pattern

| Beat | Formula | First video |
| --- | --- | --- |
| Hook | An imperative of 2 to 3 words | "Type a goal." |
| Promise | The product doing the work, with the work verb in the accent | "Firefox does the **clicking**." |
| Demo label | The user's goal, typed in a card, in their words | "One-way, New York to San Francisco, Oct 9" |
| Result | A checkmark and the outcome | "✓ Top result found" |
| Proof | One measured number, huge | "15.6 s" with "goal to answer · real run, Google Flights" |
| Values | Three short rows, the last in the accent | "Runs on your laptop." "No cloud model." "Free and open source." |
| Finale | Wordmark with an accent period, then a tagline | "foxpilot." "Firefox, on autopilot." |
| End card | Wordmark, a mono line of attributes, the URL | "Free · open source · on-device AI" |

## Storyboard template (26 s at about 121 BPM, beat = 0.4955 s)

| Scene | Beats | On screen | Purpose |
| --- | --- | --- | --- |
| Hook | 3 | The imperative, masked per-word rise | Outcome in under 2 s |
| Promise | 3 | Waterfall line, accent verb, click ripple | Say what it does |
| Demo 1 | 12 | Footage card: setup clip, whip cut, result clip; goal types in the side card; result line | Show it work |
| Proof | 4 | The number slams in, mono caption | Make it credible |
| Demo 2 | 11 | Second task, the same grammar, the card enters from the right | Show range |
| Values | 5 | Three rows, one per beat | Remove objections |
| Finale | 8 | Wordmark slam on the music's build, tagline rises | Land the name |
| End card | rest | Wordmark, attributes, URL | Where to get it |

## Text entrances

- **Masked per-word rise:** each word in an `overflow: hidden` span; `yPercent 115 → 0`, `power4.out`, 0.55 s,
  stagger 0.12 s.
- **Velocity-matched waterfall:** words enter from the right with shrinking travel (`x: gap + 230 → 0` with gaps
  360, 180, 120, 60 px), `power4.out`, 0.32 s, stagger 0.07 s. The first word carries the momentum.
- **Blur-to-sharp slam:** `scale 1.25 → 1`, `opacity 0.15 → 1`, `blur 20 px → 0`, `expo.out`, 0.5 s.
- **Frame-stepped typing:** one `tl.set(char, {opacity: 1})` per character, 0.033 s apart.
- **Row mask slide:** each row `overflow: hidden`, inner `y 140 → 0`, `expo.out`, 0.5 s, one row per beat.

## Seams

- **Whip out:** the outgoing scene moves `x: −1745` (or `y: −900` to `−1300`) with `blur 8 px`, `expo.in`, 0.3 s,
  ending exactly on the next scene's first beat.
- **Card arrival:** `scale 1.3 → 1`, `blur 12 → 0`, `expo.out`, 0.6 s; or a whip-in from the right
  (`x 1745 → 0`, `blur 8 → 0`, 0.45 s).
- **Clip-to-clip cut inside a card:** a hard cut plus `x 300 → 0` with blur, 0.35 s.

## Footage treatment

Push in on the element that matters within 0.35 s of each clip's start: `scale 1.4 to 1.45`, `expo.out`, 0.8 s,
on the inner wrapper. Center a point at fraction `p` with `xPercent = −(p − 0.5) × s × 100`, capped at
`±(s − 1) / 2 × 100`. Speed setup clips to 1.2 to 1.3×, and keep result clips at 0.8 to 1.0× so they read.

## Music

Two variants were generated. The ElevenLabs one went silent at 17 s; the MiniMax one fit. Its prompt
(`minimax/music-2.6`, `is_instrumental: true`):

> Premium minimal tech keynote music, 118 BPM, airy synth chords, tight claps, deep sub kick, light arpeggio,
> spacious and optimistic, leaves room for a voiceover, clean ending.

Chosen because its energy curve stays soft for 16 s (under the voice) and builds right where the finale
lands. The track ran 131 s; the first 27 s were kept with a 1.5 s fade. Duck to 0.26 under the presenter;
bring it back to 1.0 over 0.6 s as the voice ends.

## SFX cue map

| Event | SFX | Volume |
| --- | --- | --- |
| Every whip | whoosh | 0.35 |
| The promise's click | click | 0.5 |
| Goal typing | type | 0.35 |
| Result line | chime | 0.5 |
| Proof slam, wordmark slam | hit | 0.5 |
| Each value row | pop | 0.5 |
| End card | chime | 0.5 |

## Reference build

`itsryanarmani/scripts` → `demo-video/styles/keynote_whip.py` with `demo-video/examples/keynote-whip.json`.

## v2 polish (foxmate, second round)

- **Drawn props over footage:** a cursor that moves and clicks, a prompt that slides up, a lock that slams,
  chain lines that draw on, and a ring with a ticking counter, all as white cards on the grey stage.
- **Seams:** the expo-in whips alternate direction: left, up, right, down.
- **Labels:** a small-caps mono kicker at the top left. A shot shows a label or a sentence, never both.
- **Presenter mix:** SFX stay at 0.3 or less, and at 0.22 or less under the voice. The first cut had them
  too loud.
