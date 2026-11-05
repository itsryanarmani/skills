# Style library

Each file here is one proven look for a 20 to 30 second demo video. A style fixes the ground, type,
motion, seams, pacing, music and sound, so two videos made in the same style feel like one series,
and videos in different styles never look alike.

| Style | Feels like | Best for | Tempo | Length |
| --- | --- | --- | --- | --- |
| [Keynote whip](keynote-whip.md) | An Apple keynote: calm, confident, fast | A capability that "just works" (an agent, an automation) | about 120 BPM | 26 s |
| [Dossier](dossier.md) | A case file: tension, then relief | Safety, privacy, "caught in time" stories | about 119 BPM, with a drop | 22.5 s |
| [Pop flats](pop-flats.md) | A satisfying clean-up: loud, playful, quick | Annoyance killers, "never again" products | 120 BPM | 23 s |
| [Brutalist mono](brutalist-mono.md) | A stark spec sheet: hard grid, one acid accent | Scaffolders and one-command CLIs | 126 BPM | 23 s |
| [CRT terminal](crt-terminal.md) | A glowing 80s terminal: commands and logs | Developer tools that survive a crash or a kill | 112 BPM | 24 s |
| [Dark halftone](dark-halftone.md) | A threat briefing: black, teal dots, one red word | Security tools that catch an attack | 100 BPM | 22 s |
| [Paper cutout](paper-cutout.md) | Handmade stop-motion: warm, bouncy | Friendly local-first tools | 108 BPM | 24 s |
| [Neon synthwave](neon-synthwave.md) | An 80s outrun night: neon sign, sunset grid | Gates and switches with a hard yes or no | 118 BPM | 23.5 s |
| [Museum archive labels](museum-archive-labels.md) | A quiet gallery: framed exhibits, wall labels | Inspectors and tools that read what is on screen | 100 BPM | 21.5 s |
| [Risograph duotone](risograph-duotone.md) | A two-ink print: warm, a little off-register | Pairing and approval flows | about 110 BPM | 24 s |
| [Retro desktop OS](retro-desktop-os.md) | A 90s desktop: every line is a dialog box | Account links, tokens and permission prompts | 124 BPM | 22.5 s |
| [Pixel arcade](pixel-arcade.md) | An 8-bit game: stages and a boss fight | Stories with an attacker to beat | 140 BPM | 22.3 s |
| [Whiteboard marker](whiteboard-marker.md) | A hand-drawn explainer: circled words, ticks | A loop or a flow that needs a diagram | 107 BPM | 20.7 s |
| [Blueprint](blueprint.md) | An engineering drawing: grid, dimension lines, a spec sheet | Benchmarks and tools that prove a claim | 124 BPM | 24 s |
| [Editorial magazine](editorial-magazine.md) | A print feature: cover line, drop cap, white stock | Calm, personal tools such as memory or notes | 112 BPM | 23.5 s |
| [Financial ticker](financial-ticker.md) | A trading terminal: tickers, live numbers | Payments, budgets and spend limits | 118 BPM | 25.6 s |
| [Glass on shader](glass-on-shader.md) | Frosted glass panels over moving light | Abstract AI products; sits well under a voice | 100 BPM | 22.8 s |
| [Newsprint zine](newsprint-zine.md) | A photocopied punk zine: cut-out words, stamps | Tamper detection and "caught it" stories | 128 BPM | 21.8 s |
| [Swiss grid](swiss-grid.md) | International Typographic: a visible 12-column grid | Rule engines and policy gates | 120 BPM | 24.5 s |
| [Patch bay](patch-bay.md) | A modular-synth panel: jacks, lamps, patch cables | Connectors and direct links with no server between | 112 BPM | 27 s |
| [Anime, heavy cuts](anime-heavy-cut.md) | A shonen action film: key art, impact flashes, speed lines | Many people against one wall; protest and group-action products | 140 BPM | 25.7 s |

[Presenter](presenter.md) is a module, not a style: a talking-head avatar card that any style can carry.

## Choose a style

1. Name the story's emotion: confidence, relief or satisfaction. Pick the style that carries it.
2. In a set of videos, use each style once, and add new styles for the rest. A set that repeats one look reads as generic.
3. Give the presenter to the video where a person adds the most: usually the flagship or the most abstract product.

## Shared rules (every style)

- **Arc:** hook in outcome language (0 to 2 s) → the stakes or a second hook beat → product name and promise by beat
  two → the demo, landing on the musical drop or build → one measured proof → end card. Each claim traces to a
  measured run.
- **Pace:** about 8 to 10 shots in 20 to 26 s. Hold a sentence about 3.5 s; cut fast only between pure
  graphic frames. See the polish rules in `SKILL.md`.
- **Grid:** every scene starts on a detected beat. Write scene lengths in beats, not seconds.
- **Graphics first:** draw the product's UI as animated SVG in the style. Use at most one real screenshot, in a
  styled card, pushed in on the subject; full browser frames are unreadable on a phone.
- **Sound:** an instrumental bed chosen by its energy curve, and SFX on every cut, tap and slam.
- **Gates:** stills for every scene before the render; a frame audit of the final file before anyone sees it.

## Add a new style

Copy this outline into `styles/<name>.md`, fill every section from a real render, and add a row to the table above.
Do not add a style that has not shipped at least one video.

1. **Use it for** — the story emotion and product type.
2. **Look** — ground, palette with hex values and roles, type pair (bundled fonts or embedded woff2), layout grid.
3. **Copy pattern** — hook formula, scene lines, end card, with the real lines from the first video.
4. **Storyboard template** — a table: scene, length in beats, on screen, purpose.
5. **Text entrances** — each technique with its ease, duration and stagger.
6. **Seams** — how scenes hand over (whip, mask, color cut, zoom-through), with values.
7. **Footage treatment** — card, frame, tilt, zoom values.
8. **Music** — the generation prompt, the model, the tempo and how the variant was chosen.
9. **SFX cue map** — which sound lands on which event.
10. **Reference build** — the example spec and builder in `pooriaarab/scripts` `demo-video/`. Until a
    style has a builder there, name the video it first shipped on.
