---
name: org-threads-bookmarks
description: "Use when the user wants to organize Threads saved posts — exporting to Notion or Notes reference, categorizing, and pruning the saved queue. Triggers: 'clean up Threads bookmarks'."
---

# Threads Saved Organizer

Process Threads saved posts.

## Requirements

- Threads account (Meta).
- **`threadsclaw` CLI** — [itsryanarmani/threadsclaw](https://github.com/itsryanarmani/threadsclaw) (scaffold; needs implementation). Browser-cookie-based scraper in steipete's `*claw` style. Goal: claw saved posts into structured JSON.
- Logged-in Threads session in a browser (Meta auth — shares cookies with Instagram).
- Fallback until `threadsclaw` is built: Meta's "Download Your Information" export, or Playwright on the web app.

## Step 1 — Ask the User First

```
1. Goal — export to a destination, or in-place organization (Threads has no folders)?
2. Categorization — topic-based, by author, by content type?
3. After export — unsave, or leave originals?
4. Source — Meta data download or live scrape?
```

## Steps (TBD)

1. **Inventory** — fetch saved list (URL, author, content excerpt, date).
2. **Classify** — topic clustering.
3. **Plan** — migration TSV.
4. **Approve** — batch.
5. **Apply** — write to destination, optionally unsave.
6. **Verify** — final count.

## Surface-specific notes

- Threads is newer than X / Instagram; tooling is thinner. Browser scraping is the practical path.
- Volume tends to be lower than X bookmarks; most users have hundreds, not thousands.

## See also

- [`../org-life-organizer/_lib/taxonomy.md`](../org-life-organizer/_lib/taxonomy.md)
- [`../org-life-organizer/_lib/patterns.md`](../org-life-organizer/_lib/patterns.md)
- [`../notion-organizer/SKILL.md`](../notion-organizer/SKILL.md)
- [`../org-instagram-saved/SKILL.md`](../org-instagram-saved/SKILL.md) — shares Meta auth
