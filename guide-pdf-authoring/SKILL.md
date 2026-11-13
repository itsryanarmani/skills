---
name: guide-pdf-authoring
description: Write and export long-form guides to rich PDFs (cover, TOC, tables). Use with the humanizer skill first.
---

# Guide PDF authoring

1. Draft in markdown with `title`, `description`, `updated` in frontmatter.
2. Run **humanizer** on the body — no AI slop before export.
3. Use `##` sections (they become TOC entries). Add pipe tables where comparisons help.
4. Export with `bun render.ts guide.md --out guide.pdf --seed "#your-brand" --publisher "Optional series name"`.
5. Omit `--publisher` for a neutral cover (only title + description).

Layout tokens: `coverBackground`, `accent`, `panelFill` — pass via `--seed` or edit `GuidePdfTheme` in guide-pdf.ts.
