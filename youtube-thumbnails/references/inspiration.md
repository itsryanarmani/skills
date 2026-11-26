# Where the rules come from and where to look

We read these sources in November 2026 (one was only read by its description, as marked). Rules marked "we did not test" in `tactics.md` come from them. Costs, timings and the model comparison are our own measurements.
Repositories change. A verified run of ours outranks anything below.

## Sources

| Source | What we took |
| --- | --- |
| https://github.com/inference-sh/skills (`guides/design/youtube-thumbnail-design`) | The 120 px test, safe zones, three-colour limit, six-word ceiling, expression table, A/B variables, the checklist. |
| https://github.com/ChrisTitusTech/titstack (`.agents/skills/youtube-thumbnail`) | One idea, one focal point, one to four words. Do not alter a real person: crop, scale and a soft shadow only. Check at small size. Do not repeat the title. |
| https://github.com/meibraransari/YouTube-Thumbnail-Generator-Prompt | A category list of prompt styles (tech, business, education, mystery) and a prompt shape: subject, lighting, contrast, "viral YouTube style". We did not use its AI-face prompts. |
| https://x.com/designbykashyap/status/2125271065823936795 | The 20 formats in `formats.md`. |
| https://github.com/bdebon/youtube-thumbnail-tester-chrome-extension | Not run by us. Its description says it shows a thumbnail and title in the real home feed, which is the right test for "does it stand out". |
| https://github.com/sediman-agent/OpenSkynet (`skills/kostja94_marketing-skills/youtube`) | Title, description and thumbnail repeat one message, each aimed at a different part of the algorithm. |

Where a source says "preserve the person exactly" (titstack) and our skill makes
poses with a model, the difference is deliberate: the poses are generated from the
person's own photos, with consent, and the real cutout remains an option. Pick
the cutout when the thumbnail must show a real moment.

## How to find examples in your niche

1. Search the topic on YouTube. Open the first 20 results.
2. Screenshot the thumbnails in one grid. Mark the 3 that stand out and say why.
3. Note which layout from `formats.md` each uses, and the colours.
4. Choose a layout and colour that the grid does not already use. Standing out
   beats copying the winner.
5. Check the thumbnail beside the real feed with the tester extension.

## What good examples share

- One face, large, with a clear emotion.
- Three or four words, or none.
- One flat or simple background colour that contrasts with the person.
- A clear gap on one side for the words.
- No small text.

## Keep this file honest

When a layout or rule is proven wrong by a run, change the rule here and say what
was measured. Do not add a source we did not read.
