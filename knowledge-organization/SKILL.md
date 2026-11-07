---
name: knowledge-organization
description: "Use when the user wants to organize their knowledge, files, or notes across multiple platforms (local, iCloud, Google Drive, Notion, GitHub, Notes app). Triggers: 'organize my knowledge', 'second brain', 'unified folder structure', 'sync iCloud and Drive', 'context graph', 'personal knowledge base', 'everything in sync'."
---

# Knowledge Organization

Set up a unified knowledge system across all platforms — local, iCloud, Google Drive, GitHub, Notes — with a single taxonomy and an optional connected-notes layer.

---

## Step 1 — Ask These Questions First

```
1. What platforms do you use? (local/iCloud/Google Drive/GitHub/Notion/Apple Notes/Obsidian)

2. What's your primary pain? 
   a) Can't find things — no consistent structure
   b) Ideas siloed — notes don't connect to files
   c) Platforms out of sync — different folder names everywhere

3. What type of content dominates?
   a) Documents/files (PDFs, decks, contracts)
   b) Ideas/notes/writing (knowledge, research, journaling)
   c) Code and projects (repos, scripts, configs)
   d) Mix of all

4. Do you have a folder structure preference?
   a) PARA (Projects / Areas / Resources / Archive — Tiago Forte)
   b) Flat project folders (one folder per project/brand)
   c) Johnny Decimal (numbered hierarchy: 10-19 Finance, 20-29 Health…)
   d) No preference — recommend one
```

---

## Method Comparison

| Method | Best for | Weakness |
|--------|----------|----------|
| **PARA** | Action-oriented people; lots of active projects | Archive gets messy; bad for pure ideas |
| **Zettelkasten** | Researchers, writers, idea people | No clear home for files/docs |
| **Johnny Decimal** | People who retrieve more than create; strict types | Rigid; numbering friction |
| **Flat project folders** | Developers; one folder per brand/product | Doesn't scale for personal life |
| **LYT (Maps of Content)** | Non-linear thinkers; Obsidian users | Requires Obsidian; upfront setup |
| **BASB / CODE** | Creatives capturing from everywhere | Heavy process; needs discipline |

**Recommended hybrid for most people:**  
→ **PARA-inspired folders** for files/documents + **Zettelkasten-inspired notes** for ideas = best of both worlds.

---

## The Unified Taxonomy

One structure, mirrored across every platform. Files live in ONE place; others link or reference.

```
Root/
├── 0 - Inbox/              ← capture everything first, process weekly
├── 1 - Projects/           ← active work with a specific outcome
│   ├── {project-name}/
│   └── ...
├── 2 - Areas/              ← ongoing responsibilities (no deadline)
│   ├── Finance/
│   ├── Health/
│   ├── Legal/
│   ├── House/
│   ├── Music/
│   └── Personal/
├── 3 - Resources/          ← reference material (no action needed)
│   ├── Learning/
│   ├── Design Assets/
│   └── Research/
└── 4 - Archive/            ← inactive projects, old docs
```

**Projects naming:** use the brand/product name (`Mozilla/`, `Solo/`, `Beehouse/`).

---

## Platform Roles (Canon vs Mirror)

Don't put everything everywhere. Assign each platform a **role**:

| Platform | Canonical for | Syncs to |
|----------|--------------|----------|
| **Local `~/Documents/`** | Code repos, dev tools, active projects | GitHub (code), iCloud (docs) |
| **iCloud** | Personal documents, legal, finance, media | Backup only |
| **Google Drive** | Shared docs, decks, collaboration assets | Drive links in notes |
| **GitHub** | Code, scripts, skills, automation | Local via clone |
| **Obsidian / Notes** | Ideas, atomic notes, journal, MOCs | Obsidian sync or iCloud vault |

**Rule:** a file has ONE home. Other platforms reference it, not copy it.

---

## The Context Graph (Connected Notes Layer)

On top of the folder taxonomy, add a **notes layer** in Obsidian (or Apple Notes) that links everything together.

### Obsidian vault structure

```
Notes/                          ← lives in iCloud/Areas/Personal/Notes/ or iCloud vault
├── _inbox/                     ← quick captures (process weekly)
├── MOC - Projects.md           ← Map of Content: links to all active projects
├── MOC - Areas.md              ← links to area notes and key docs
├── MOC - Resources.md          ← links to learning notes, books, research
├── atoms/                      ← atomic notes: one idea per file, [[wiki-linked]]
│   ├── idea-name.md
│   └── ...
├── journal/                    ← daily notes (YYYY-MM-DD.md)
└── templates/                  ← note templates
```

### Atomic note format (Karpathy-inspired)

```markdown
# Idea Title

One clear statement of the idea.

## Connections
- [[related-idea-1]]
- [[related-idea-2]]
- Source: [[book-or-article-title]]

## Why it matters
...

## Questions it raises
- ...

Tags: #topic #domain
```

### Maps of Content (MOC)

Hub notes that act as entry points to a topic:

```markdown
# MOC - Solo Products

## Active
- [[beehouse-strategy]] | [[example-roadmap]] | [[vibeads-notes]]

## Resources
- [[solopreneur-principles]] | [[pricing-strategies]]

## Archive
- [[artenal-notes]] | [[mobile-saloon-postmortem]]
```

---

## Setup by Platform

### iCloud
Use the `icloud-organizer` skill or script to classify files into the taxonomy.

### Google Drive
Use the `google-drive-organizer` skill to restructure into the same taxonomy.

### Local `~/Documents/`
```
~/Documents/
├── {project}/          ← one dir per project (flat, no nesting)
│   ├── code/           ← git repos
│   ├── docs/           ← strategy, specs
│   ├── content/        ← marketing, social
│   └── assets/         ← logos, design files
└── pooriaarab/         ← personal "project" = you
    ├── finances/
    ├── health/
    ├── legal/
    ├── photos/
    └── notes/          ← Obsidian vault symlink or clone
```

### GitHub
Each code project gets its own repo. Personal scripts/tools → `itsryanarmani/tools`.  
Skills → `itsryanarmani/skills`.

### Apple Notes / Obsidian
Point Obsidian vault at `iCloud/Areas/Personal/Notes/` so notes sync automatically.

---

## Weekly Maintenance Ritual (5 min)

1. **Empty Inbox** — classify everything in `0 - Inbox/` to its PARA folder
2. **Review Projects** — is anything done? Move to Archive.
3. **Process atomic notes** — link new notes to existing MOCs
4. **Sync check** — anything on Desktop or Downloads? Move it.

---

## Cross-Platform Search

Once taxonomy is unified, search works everywhere:
- **Spotlight** — finds local + iCloud files by name/content
- **Obsidian search** — full-text across all notes + backlinks
- **Google Drive search** — Drive files only
- **GitHub search** — code + READMEs

For a unified search layer, consider **Raycast** with Drive + Obsidian + GitHub plugins.

---

## Related Skills

- `mac-organizer` — disk cleanup + local Documents structure
- `icloud-organizer` — AI-powered iCloud → PARA reorganization (Apple Intelligence, 100% local)
- `google-drive-organizer` — restructure Drive into the same taxonomy
- `notion-organizer` — Notion workspace → clean hierarchy
