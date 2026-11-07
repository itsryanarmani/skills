# Pop flats

Loud, playful and quick. Flat color grounds that change on the beat, giant condensed type, and pop-art cards with
hard shadows. It feels like clearing clutter.

**Use it for** annoyance killers and "never again" products: blockers, cleaners, auto-refusers.
First shipped: Consent Shield, a 23 s launch video.

## Look

| Role | Value |
| --- | --- |
| Grounds | Flat, one per scene, cut on the beat: red `#ff4050`, ink `#121212`, yellow `#ffd23f`, violet `#6d3cf5`, green `#19c37d` |
| Text | White on red, violet and ink; ink `#121212` on yellow and green |
| Cards | 12 px white border, 16 px radius, hard shadow `18px 18px 0 #121212` |

Type: **League Gothic** for everything big (330 to 820 px, uppercase, crops off the frame on purpose). **Space Mono**
for small labels and the promise line.

## Copy pattern

| Beat | Formula | First video |
| --- | --- | --- |
| Hook | The annoyance as one word with a question mark | "COOKIES?" |
| Flood | Real screenshots of the annoyance piling up, with a mono caption | "real banners, real sites, one morning" |
| Scale | Three words, one per beat | "EVERY. SINGLE. SITE." |
| Name | The product name, wide-to-tight, then the promise | "CONSENT SHIELD" / "Says no for you. Never presses Accept." |
| Demo labels | Each setting it changes, with an inverted OFF chip, one per beat, then a verdict | "FUNCTIONAL OFF", "TARGETING OFF", "PERFORMANCE OFF", "SAVED." |
| Attitude | A giant word behind the next card, swapping on the bar | "NOPE." then "NO." |
| Second annoyance | The refusal itself as the headline | "NO THANKS." |
| Proof | Two numbers | "10/10" refuse paths matched; "0" Accept-all clicks |
| End card | Name, promise, URL | "A free Firefox add-on. Never presses Accept." |

## Storyboard template (23.2 s, beat = 0.5 s, 120 BPM)

| Scene | Beats | Ground | On screen |
| --- | --- | --- | --- |
| Hook | 0–2 | red | "COOKIES?" slam |
| Flood | 2–6 | ink | 7 screenshots arriving at 0, 0.42, 0.33, 0.25, 0.17, 0.12, 0.07 s gaps |
| Scale | 6–9 | yellow | Three hard-cut words |
| Name | 9–14 | violet | Wide-to-tight name, promise rises |
| Demo 1 | 14–24 | green | Card on the left, OFF rows on the right on beats 20 to 22, "SAVED." on 23 |
| Demo 2 | 24–32 | yellow | Card on the right, giant word behind it, swapping on beat 28 |
| Demo 3 | 32–36 | red | Headline top-left, card lower right |
| Proof | 36–40 | yellow | Two numbers slam, one per bar |
| End card | 40–end | violet | Name, promise, URL |

## Text entrances

- **Slam:** `scale 1.25 → 1`, `opacity 0.15 → 1`, `blur 20 → 0`, `expo.out`, 0.4 s. Used for almost everything.
- **Hard-cut word swap:** `tl.set` opacity on each beat. No tween; the cut is the beat.
- **Wide-to-tight tracking:** each glyph starts at `x = (i − middle) × 34 px` and settles to 0, `power2.out`, 0.45 s.
- **Montage pop:** each screenshot `scale 0.86 → 1`, `expo.out`, 0.16 s, with its own offset and a rotation of −3.5° to +3°.

## Seams

Seams are color cuts: the ground's `backgroundColor` is set on the beat (`tl.set`), and the scene's content
slams in on the same frame. Cards enter with `scale 1.08 → 1` and `rotation −2° → 0` in 0.3 s.

## Footage treatment

Pop-art cards (1250 × 800, or 1100 × 704 when a giant word shares the frame). Start each clip pushed in on the
subject (for example, a banner in the bottom-left: `scale 1.5`, `xPercent 25`, `yPercent −25`), and hold it.
Speed: 1.2 to 1.6×. A giant word may sit behind a card (lower z-index) so only part of it shows.

## Music

> Playful, bouncy, satisfying funk-pop instrumental, 120 BPM: slap bass, tight claps on 2 and 4, bright pizzicato
> strings and marimba plucks, little rhythmic stabs, feels like tidying up and popping bubble wrap. Starts on beat
> one immediately, groovy throughout, ends with a cheeky final stab. No vocals.

`elevenlabs/music`, `music_length_ms: 26000`. Chosen because it is at full energy from the first second with no
intro, and ends cleanly at about 23 s.

## SFX cue map

| Event | SFX |
| --- | --- |
| Hook | glitch |
| Each screenshot in the flood | pop (0.4) |
| Each scale word, each proof number | stamp |
| Name | whoosh |
| A click in the footage | click |
| Each OFF row | pop |
| "SAVED." and each giant word | hit |
| End card | chime |

Give every SFX its own audio track. The montage pops overlap.

## Reference build

`itsryanarmani/scripts` → `demo-video/styles/pop_flats.py` with `demo-video/examples/pop-flats.json`.
