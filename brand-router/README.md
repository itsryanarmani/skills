# Brand Skills

A suite for running a whole brand — voice, website, and every social surface —
from one chosen visual direction. Twenty-one directions, each a complete world, each
answering the same twelve surfaces so they stay comparable and swappable.

**Where to start:** run [`brand-router`](SKILL.md). It surveys what
you actually publish, applies three filters, and recommends a kit.

**Architecture:** see [`DESIGN.md`](DESIGN.md).

## The core idea

A brand that only exists on a website is a stylesheet, not a brand. The website
is one of twelve places the work appears, and rarely the first one anybody sees.
So every direction here specifies its voice, its landing page, its avatar, its
LinkedIn banner, its Instagram carousel, its YouTube thumbnail **and edit
style**, its podcast cover, and its decks — with numbers, not adjectives.

The second idea matters as much: **you pick a kit of three, not a single style.**
A core for ~80% of output, an authority register for money and results, and a
launch register used perhaps one post in twenty. The router explains why, and
what breaks when you ignore it.

## Sub-skills

| Skill | Family | Use when | Cost |
|---|---|---|---|
| [`brand-router`](SKILL.md) | meta | "pick a brand direction", "what style should my brand be" | — |
| [`broadsheet`](../brand-broadsheet/SKILL.md) | editorial | It has a byline and a date. Essays, reporting. | cheap |
| [`swiss`](../brand-swiss/SKILL.md) | editorial | Strong content that needs organising, not selling. | cheap |
| [`manuscript`](../brand-manuscript/SKILL.md) | editorial | Long essays, a letter, a thesis. | cheap |
| [`plaque`](../brand-plaque/SKILL.md) | editorial | A portfolio or archive. The work is the thing. | cheap |
| [`annual`](../brand-annual/SKILL.md) | editorial | Investor updates, results, a track record. | moderate |
| [`terminal`](../brand-terminal/SKILL.md) | technical | Technical reader, verifiable claim. Changelogs, benchmarks. | cheap |
| [`blueprint`](../brand-blueprint/SKILL.md) | technical | Showing how something is built. Teardowns, roadmaps. | moderate |
| [`spec`](../brand-spec/SKILL.md) | technical | Pricing, comparisons, reference writing. | cheap |
| [`oscilloscope`](../brand-oscilloscope/SKILL.md) | technical | One metric is the story. | moderate |
| [`punchcard`](../brand-punchcard/SKILL.md) | technical | Work that should feel filed and permanent. Archives. | moderate |
| [`signage`](../brand-signage/SKILL.md) | technical | The reader is moving and deciding. Navigation, onboarding paths, docs maps. | cheap |
| [`buildspace`](../brand-buildspace/SKILL.md) | expressive | Founders talked to, not sold to. Community, newsletter. | cheap |
| [`risograph`](../brand-risograph/SKILL.md) | expressive | A zine, a drop, small-batch work. | expensive |
| [`stadium`](../brand-stadium/SKILL.md) | expressive | A launch, a result, a date. | moderate |
| [`arcade`](../brand-arcade/SKILL.md) | expressive | Playful work, a launch that wants a crowd. | expensive |
| [`flyer`](../brand-flyer/SKILL.md) | expressive | Manifestos, open calls, picking a fight. | expensive |
| [`dispatch`](../brand-dispatch/SKILL.md) | expressive | Real news that cannot wait. | moderate |
| [`dusk`](../brand-dusk/SKILL.md) | atmospheric | Reflection written after the fact. Letters, post-mortems. | moderate |
| [`vellum`](../brand-vellum/SKILL.md) | atmospheric | Work with versions that should stay visible. | moderate |
| [`aurora`](../brand-aurora/SKILL.md) | atmospheric | One serious claim needs the whole page. | expensive |
| [`porcelain`](../brand-porcelain/SKILL.md) | atmospheric | One claim taken seriously with no help from design. | cheap |

## How this differs from `saas-brand-system`

Both design brands. They do not do the same job, and picking the wrong one
wastes real effort.

| | [`saas-brand-system`](../saas-brand-system/SKILL.md) | this suite |
|---|---|---|
| Subject | A product or company | A person, across everything they publish |
| Shape | A **process**: fan out N prototypes, judge, pick, expand | A **reference**: twenty finished directions, already specified |
| Directions | 14 emotion-tagged briefs, generated fresh each run | 20 fixed worlds with committed tokens and audited contrast |
| Output | HTML prototypes, then a logo suite, favicon, OG set | Executable rules for twelve surfaces, per direction |
| Surfaces | Mostly web plus brand assets | Voice, web, avatar, OG, LinkedIn, Instagram carousels, YouTube thumbnails and edits, podcast, decks |
| Best when | The brand does not exist yet and needs exploring | You need to apply a direction consistently, week after week |

**Use `saas-brand-system` to discover a direction for a product. Use this suite
to run a direction across a person's whole output.** They chain: explore there,
and if the winner resembles one of these twenty, adopt that skill for the
day-to-day surfaces.

## Conventions

- **Direction names are lowercase**, always. House style, and it is also the URL
  segment and the skill name.
- **Every direction answers the same twelve surfaces**, in the same order, with
  identical headings. See [`_lib/surfaces.md`](_lib/surfaces.md). That is what
  makes two directions diffable surface by surface.
- **Every direction obeys the shared craft floor**:
  [`_lib/craft-floor.md`](_lib/craft-floor.md). Contrast at least 4.5:1 computed
  rather than eyeballed, a -0.04em tracking floor, no gradient text, one
  authored moment of motion, and that motion animates from an already-visible
  resting state.
- **Every direction declares its cost to run.** A direction needing a designer
  per asset is not viable for one person publishing weekly, and the skill says
  so rather than letting you find out in week four.
- **Every direction names its failure mode.** Usually the most useful paragraph
  in the file.
- **Light and dark are both argued.** The non-native mode is a reasoned port
  (the printed session, the diazo whiteprint, the archive photograph), never a
  mechanical inversion.

## Install

```bash
# The whole suite
npx skills add itsryanarmani/brand

# Just the router, then add directions as you pick them
npx skills add itsryanarmani/brand/brand-router
npx skills add itsryanarmani/brand/buildspace
npx skills add itsryanarmani/brand/annual
```

## Provenance

Twenty of the directions exist as running code — verified palettes, real texture
CSS, working motion — in the `private-repo-4a88` repo under
`apps/website/src/brand/`, rendered at `/brand` with a live preview per
direction, and paired there with twenty structural site archetypes at `/lab`.
The hex values, font stacks, and contrast ratios quoted in those skills are
copied from that source, not invented.

`signage` is the exception and is marked as such deliberately. It has no
implementation in that repo yet, so its palette was authored here and every
contrast ratio in it was **computed** from the committed hex values rather than
read off a running page. That is a weaker provenance than the other twenty have,
and it is worth knowing which kind you are reading: the numbers are correct, but
nothing has yet proved the direction survives contact with a real page.
