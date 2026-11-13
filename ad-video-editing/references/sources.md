# Source repos: what to adopt, what not

Audit of the repos behind this skill's methods. Stars and push dates
via `gh api` on 2026-11-12; licenses from shallow clones kept outside
this repo (read-only, untrusted — install scripts never ran). The eval
was a local 2026-11-12 run; its report and outputs are not in this repo.

| Repo | Stars | Last push | License | Adopt | Do not adopt |
|---|---|---|---|---|---|
| openfilm/openfilm | 6,005 | 2026-11-13 | MIT code; `library/` dedicated CC0 1.0; emoji stickers MIT (Fluent) | CC0 SFX/transition/motion library, `look`-style QA ideas, loudness normalization | `film.html` as a second composition format, paid service connectors |
| nateherkai/herk-edit-kit | 2,803 | 2026-10-14 | MIT + custom use-permission (NOASSERTION on GitHub) | cut-silences / cut-mistakes scripts, EDITING-PLAYBOOK pacing rules | ElevenLabs-only transcription, Kie.ai asset path, AIS brand assets |
| OpenMontageInc/OpenMontage | 80,081 | 2026-11-09 | AGPL-3.0 | Ideas only: per-tool cost/duration metadata, subtitle cue grouping, clip-factory shape | Any code — AGPL contaminates our MIT repos. No copying, ever |
| kurbaitaev/ghost-editor | 453 | 2026-10-30 | MIT | CC0 meme-SFX pack concept (already covered by OpenFilm library) | — |
| WyattBlue/auto-editor | 5,867 | 2026-11-13 | Unlicense | Loudness-only silence pass as a fallback when no transcript exists | Primary speech editing — word-gap cuts beat loudness cuts for TTS ads |
| heygen-com/hyperframes | 83,542 | 2026-11-13 | Apache-2.0 | The render target for composed ads (the `hyperframes` skill is installed locally on the machine, not in this repo) | — |

## License text (quoted)

**openfilm `library/LICENSE.md`:** CC0 quote in `library.md`. Emoji stickers:
"MIT License … Copyright (c) Microsoft Corporation." — keep the notice with them.

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

When copying a herk script (`cut-silences.mjs`, `find-cut-candidates.mjs`,
`apply-cuts.mjs`), keep the MIT notice (`Copyright (c) 2026 Nate Herk`)
and this use-permission notice with the file.

**OpenMontage `LICENSE`:** "GNU AFFERO GENERAL PUBLIC LICENSE Version 3,
19 November 2007". AGPL-3.0 means: do not copy code into our MIT repos;
clean-room reimplementation of ideas is fine.

**auto-editor:** Unlicense (public domain). **ghost-editor:** MIT. **hyperframes:** Apache-2.0 (GitHub SPDX).

## Caveats

- OpenMontage's 80k stars on a months-old repo look anomalous; treat the
  count with suspicion. Its value here is design patterns, not code.
- Vendor clones live outside this repo. When adopting a script, copy it
  into our tooling and record its source + license here — do not link a
  path that will not exist for the next agent.
- Whisper `tiny` is rough on names and fast cuts; eval used `tiny`, commands use `small`.
