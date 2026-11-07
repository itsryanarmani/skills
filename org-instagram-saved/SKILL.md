---
name: org-instagram-saved
description: "Use when the user wants to organize Instagram saved posts and collections — exporting to Notion or Notes reference, restructuring collections, identifying stale saves, and pruning. Triggers: 'clean up Instagram bookmarks', 'organize my IG saves'."
---

# Instagram Saved Organizer

Process Instagram saved posts and collections.

## Requirements

- Instagram account.
- **`instaclaw` CLI** — [itsryanarmani/instaclaw](https://github.com/itsryanarmani/instaclaw) (scaffold; needs implementation). Browser-cookie-based scraper in steipete's `*claw` style. Goal: claw saved posts and collections into structured JSON.
- Logged-in Instagram session in a browser (Meta auth shared with Threads).
- Fallback until `instaclaw` is built: Meta's "Download Your Information" data export, or Playwright on the web app.

## Step 1 — Ask the User First

```
1. Goal — export, restructure collections in-place, or both?
2. Already using Collections? — keep, consolidate, or rebuild?
3. Categorization — by content type (food / travel / fashion / how-to), by source (creator)?
4. After export — unsave, or leave originals?
5. Source — work from "Your Activity → Saved" or from a "Download Your Data" archive?
```

## Steps (TBD)

1. **Inventory** — fetch saved list (URL, post type, creator) via web scrape or downloaded archive.
2. **Classify** — by collection or AI-suggested category.
3. **Plan** — collection restructure + export TSV.
4. **Approve** — batch by collection.
5. **Apply** — Instagram's web app supports moving between collections; bulk operations are tedious — consider per-collection batches.
6. **Verify** — final saves count + collection structure.

## Surface-specific notes

- **No public API** for saved posts. Instagram's "Download Your Data" feature is the most reliable bulk source.
- Anti-scraping is strict; the web app can rate-limit aggressively.
- Reels-vs-Posts have separate saved lists in some accounts.
- High-volume saves (1000+) often indicate "saved-as-bookmark" intent — most users want to convert these into Notion.

## See also

- [`../org-life-organizer/_lib/taxonomy.md`](../org-life-organizer/_lib/taxonomy.md)
- [`../org-life-organizer/_lib/patterns.md`](../org-life-organizer/_lib/patterns.md)
- [`../notion-organizer/SKILL.md`](../notion-organizer/SKILL.md)
