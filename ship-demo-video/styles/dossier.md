# Dossier

A case file: cream paper, ink, a serif that whispers then shouts, red-ink marks. It builds tension, then cuts
to the product on the musical drop.

**Use it for** safety and privacy stories, anything about catching a mistake before it happens.
First shipped: PII Guard, a 22.5 s launch video.

## Look

| Role | Value |
| --- | --- |
| Ground | Paper `#f0eee6` with a dot grid: `radial-gradient(circle, rgba(38,36,30,.09) 1.6px, transparent 1.6px) 0 0 / 34px 34px` |
| Ink | `#262624` (text, rules, card outlines) |
| Muted | `#6f6e66` (labels) |
| Red ink | `#b83a1b`: underlines, tags, the stamp, the italic key word |
| Card | `#fffdf8`, 3 px ink outline, 20 px radius |

Type: **Newsreader** serif, embedded as woff2 (500 roman, 500 italic, 700 for the wordmark). Use giant italic
for the one-word beats (420 px "Wait.") and 150 px roman for sentences. **IBM Plex Mono** for labels, exhibit
tags, placeholders and the URL.

## Copy pattern

| Beat | Formula | First video |
| --- | --- | --- |
| Setup | A realistic message typed into a plain composer, holding the risk | "Hi! I'm Maria Gonzalez, my email is maria.g@example.com. Can you fix my CV?" |
| Mark | The risky parts underlined in red ink, each with a mono tag | NAME, EMAIL |
| Stop | One word, giant italic | "Wait." |
| Stakes | One sentence naming the danger; the danger word in red italic | "You're about to send this / to an *AI.*" |
| Demo label | Evidence framing per clip, plus a running italic line | "Exhibit A · ChatGPT" … "Caught before you send." |
| Payoff | The same message, values swapping to tags, a stamp | "[NAME_1]", "[EMAIL_1]", REDACTED |
| End card | Bold serif wordmark with a red period, an ink rule, two mono lines | "PII Guard." "A free Firefox add-on. Checks run on your device." |

## Storyboard template (22.5 s, beat = 0.504 s, drop on beat 19)

| Scene | Beats | On screen | Purpose |
| --- | --- | --- | --- |
| Setup | 0–8 | The message types in; underlines wipe on beats 4 and 5 | The everyday risk |
| Stop | 8–11 | "Wait." | The jolt |
| Stakes | 11–19 | Two masked rows; they zoom through into the drop | Tension to the drop |
| Exhibits | 19–31 | Three tilted footage cards, hard cuts on beats 25 and 28 | The product catching it, everywhere |
| Payoff | 31–37 | The values swap to tags on beats 33 and 34; stamp on beat 35 | Relief |
| End card | 37–end | Wordmark, rule, lines | Where to get it |

Build tension until the drop, then put footage only after it. The drop is the product arriving.

## Text entrances

- **Frame-stepped typing:** 0.024 s per character.
- **Underline wipe:** `clipPath inset(0 100% 0 0) → inset(0 0% 0 0)`, `power3.out`, 0.35 s, on the beat; the tag
  fades up 0.15 s later.
- **Snap-in:** `opacity 0 → 1`, `scale 1.08 → 1`, `power3.out`, 0.18 s. Fast enough to feel like a cut.
- **Masked rows:** `y 190 → 0`, `expo.out`, 0.55 s, 0.5 s apart.
- **Masked word swap:** the old value goes `yPercent −115` (`power2.in`, 0.22 s); the tag comes up from
  `yPercent 115` (`expo.out`, 0.3 s) 0.08 s later; the slot narrows to the tag's width in the same 0.3 s.
- **Stamp:** `scale 1.6 → 1`, `opacity 0 → 1`, 0.18 s, rotated −6°.

## Seams

- **Recede:** the composer card leaves with `scale 0.82`, `blur 14 px`, fade, `power3.in`, 0.32 s.
- **Zoom-through into the drop:** the rows go `scale 1.55`, `blur 18 px`, fade, `power2.in`, 0.34 s, ending
  exactly on the drop.
- **Exhibit cuts:** hard cuts on the beat, with a 0.25 s settle from `scale 1.06`.

## Footage treatment

Footage is pasted evidence: a `#fffdf8` mat with 18 px padding, a 3 px ink outline and a soft shadow, tilted −1.2°,
+1° and −0.8° for successive exhibits. Start each clip already pushed in on the subject (`scale 1.6`) and drift
to 1.52 over the clip. Speed clips to 1.3×.

## Music

> Dark tense thriller cue, 100 BPM: pulsing low synth bass in eighth notes, ticking clock hi-hats, a nervous
> plucked motif, a rising tension riser that resolves at 10 seconds into a confident, punchy electronic drop
> with big kick and claps, then a clean hard stop on the last bar. Instrumental, cinematic tech trailer, no vocals.

`elevenlabs/music`, `music_length_ms: 26000`. Chosen because its energy curve builds for 8 s and drops at 9.6 s,
exactly where the demo should start. The beat detector read it at double tempo, so it was halved to 0.504 s.

## SFX cue map

| Event | SFX |
| --- | --- |
| Typing (two overlapping bursts) | type (0.3) |
| Each underline | scribble |
| "Wait." and the REDACTED stamp | stamp |
| The build into the drop (2 beats before) | riser |
| The drop and the wordmark | hit |
| Exhibit cuts | whoosh |
| Each tag swap | pop |

## Reference build

`itsryanarmani/scripts` → `demo-video/styles/dossier.py` with `demo-video/examples/dossier.json`.
