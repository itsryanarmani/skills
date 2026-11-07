---
name: org-slack-dm
description: "Use when the user wants to organize Slack DMs and saved items — archiving stale DM threads, processing the Saved Items queue, identifying conversations to convert into reference notes, and reducing notification clutter. Triggers: 'clean up Slack', 'process my Slack saved items'."
---

# Slack DM Organizer

Triage Slack DMs and the Saved Items queue.

## Requirements

- Slack workspace with admin or user-level token (`xoxp-...`) — see Slack API docs.
- **`slackclaw` CLI** — [itsryanarmani/slackclaw](https://github.com/itsryanarmani/slackclaw) (scaffold; needs implementation). Goal: parallel to steipete's `discrawl` (Discord) but for Slack — local SQLite archive of DMs and saved items, claw-able for agents.
- Per-workspace scope (Slack tokens are per-workspace, not global).
- Until `slackclaw` is built: use the Slack Web API directly (`conversations.list`, `conversations.history`, etc.) with a user-token from https://api.slack.com/apps.

## Step 1 — Ask the User First

```
1. Workspaces in scope — pick which to touch (likely one at a time).
2. Saved Items strategy — convert to Notes / Notion reference, archive, or just review and clear?
3. Stale DM threads — archive after N days of inactivity?
4. Notification preferences — also re-tune notification settings per channel?
5. Bot DMs — separate treatment for bot-driven DMs (deploys, alerts, integrations)?
```

## Steps (TBD)

1. **Inventory** — list DMs (1:1 + multi-person), list saved items, list active channels with notification noise.
2. **Classify** — DMs by recency, saved items by category (reference / actionable / stale).
3. **Plan** — proposed archive list + saved-items export plan.
4. **Approve** — batch.
5. **Apply** — `conversations.archive`, save-items processing, notification tuning.
6. **Verify** — final state + saved items count.

## Surface-specific notes

- Slack DMs aren't "deletable" by users — only archivable from view (still searchable).
- Saved Items is a personal queue; processing it = converting to Notes/Notion or unsaving.
- Per-workspace token: get from https://api.slack.com/apps. Required scopes: `users.profile:read`, `conversations.read`, `conversations.history`, `conversations.write`, `bookmarks.read`.
- Free workspaces have message-history retention limits — plan around that.

## See also

- [`../org-life-organizer/_lib/taxonomy.md`](../org-life-organizer/_lib/taxonomy.md)
- [`../org-life-organizer/_lib/patterns.md`](../org-life-organizer/_lib/patterns.md)
- [`../notion-organizer/SKILL.md`](../notion-organizer/SKILL.md) — destination for saved items worth keeping
