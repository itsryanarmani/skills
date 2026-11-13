# Source repos: what to adopt, what not

Audit of the repos behind this skill's methods. Stars and push dates via
`gh api` on 2026-11-12; licenses read from the cloned trees under
`editing/vendor2/` (read-only, untrusted — never run their install
scripts). Full eval: `editing/eval3/REPORT.md`.

| Repo | Stars | Last push | License | Adopt | Do not adopt |
|---|---|---|---|---|---|
| openfilm/openfilm | 6,005 | 2026-11-13 | MIT code; `library/` dedicated CC0 1.0; emoji stickers MIT (Fluent) | CC0 SFX/transition/motion library, `look`-style QA ideas, loudness normalization | `film.html` as a second composition format, paid service connectors |
| nateherkai/herk-edit-kit | 2,803 | 2026-10-14 | MIT + custom use-permission (NOASSERTION on GitHub) | cut-silences / cut-mistakes scripts, EDITING-PLAYBOOK pacing rules | ElevenLabs-only transcription, Kie.ai asset path, AIS brand assets |
| OpenMontageInc/OpenMontage | 80,081 | 2026-11-09 | AGPL-3.0 | Ideas only: per-tool cost/duration metadata, subtitle cue grouping, clip-factory shape | Any code — AGPL contaminates our MIT repos. No copying, ever |
| kurbaitaev/ghost-editor | 453 | 2026-10-30 | MIT | CC0 meme-SFX pack concept (already covered by OpenFilm library) | — |
| WyattBlue/auto-editor | 5,867 | 2026-11-13 | Unlicense | Loudness-only silence pass as a fallback when no transcript exists | Primary speech editing — word-gap cuts beat loudness cuts for TTS ads |
| heygen-com/hyperframes | 83,542 | 2026-11-13 | Apache-2.0 | The render target for composed ads (see `hyperframes` skill) | — |

## License text (quoted)

**openfilm `library/LICENSE.md`:**

> "Everything in OpenFilm's library can be used in any film, commercial or
> not, changed and shared, with no need to credit anyone. … These are
> dedicated to the public domain under CC0 1.0."

Emoji stickers: "MIT License … Copyright (c) Microsoft Corporation." —
notice must be kept with them.

**herk-edit-kit `LICENSE`:** standard MIT text ("Permission is hereby
granted, free of charge, to any person obtaining a copy … to use, copy,
modify, merge, publish, distribute, sublicense, and/or sell"), plus a note
that AIS brand assets "remain the property of AI Automation Society and
are not licensed for reuse".

**herk-edit-kit `licenses/PIPELINE-USE-PERMISSION.txt`:**

> "Permission is granted to students and other recipients to use, copy,
> modify, and share the original teaching-kit code, templates, and
> documentation, and to use them to produce personal or commercial
> videos. Retain this notice when redistributing the kit or substantial
> portions of its source materials."

**OpenMontage `LICENSE`:** "GNU AFFERO GENERAL PUBLIC LICENSE Version 3,
19 November 2007". AGPL-3.0 means: do not copy code into our MIT repos;
clean-room reimplementation of ideas is fine.

**auto-editor:** Unlicense (public domain). **ghost-editor, hyperframes:**
MIT / Apache-2.0 respectively (GitHub SPDX).

## Caveats

- OpenMontage's 80k stars on a months-old repo look anomalous; treat the
  count with suspicion. Its value here is design patterns, not code.
- Vendor clones live outside this repo. When adopting a script (e.g.
  cut-silences.mjs), copy the file into our tooling and record its
  source + license here — do not link to a path that will not exist for
  the next agent.
- Whisper `tiny` transcripts are rough; use `small`+ for names.
