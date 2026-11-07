---
name: figma-plugin-submission
description: "Use when publishing a Figma plugin to Community from the desktop publish dialog: minting a plugin ID, fixing figma.clientStorage that throws without one, thumbnails, and the Data security step."
---

# Submitting a Figma plugin through Community

The build path (sandbox, iframe, manifest, fetch) is the `figma-plugin` skill. This skill is
the part that happens in the Figma desktop app once the plugin exists: minting a plugin ID,
listing assets, the Data security form, and first publish. Everything below was verified by
hand on 2026-08-28; none of it is in Figma's docs or in the `figma-plugin` skill.

Companion playbook: `itsryanarmani/scripts` `scripts/figma-plugin/README.md` — the
command-level steps. This skill is the traps.

Worked example: Content Rabbit, submitted 2026-08-28 —
<https://www.figma.com/community/plugin/1675058575243742396>. Source is
`integrations/figma-plugin/` in `itsryanarmani/private-repo-c4e6`, and the filled-in
listing copy and data-security answers are in that repo's
`.claude/docs/figma/submission.md`.

## When to use

- **Triggers:** 'submit Figma plugin', 'publish to Figma Community', 'Cannot access client storage without a plugin ID', 'Figma plugin thumbnail', 'Figma Data security', 'Figma plugin ID', 'figma.clientStorage throws', 'Figma plugin review rejected'.
- figma.clientStorage throws until manifest.json has an id; minting via New plugin creates a second dev plugin you must not publish from.
- The thumbnail is 1920x1080 (not 1920x960); thumbnail and 128x128 icon must be flattened with no alpha. Data security has five questions; the first demands a public vulnerability process. No video needed; the playground file is optional.
- Sibling: figma-plugin (the build path).

## 1. `figma.clientStorage` throws without a plugin ID

The exact error is `Cannot access client storage without a plugin ID`.
`manifest.json` has no `id` until you put one there, so every locally imported
build fails to save an API key.

Two fixes. Do both.

**(a) Mint an ID early.** In the Figma desktop app: **Plugins → Development →
New plugin… → Figma design → Empty**. Copy the `id` out of the manifest Figma
scaffolds. Paste it into yours. The ID is permanent. It is also the published
listing's ID.

**(b) Make the plugin degrade.** Hold the key in sandbox memory for the session.
Tell the user it will not persist. Do not report a hard failure.

## 2. Minting an ID creates a second dev plugin

The scaffold and your imported plugin are separate entries in **Manage plugins**.
Remove both. Re-import your manifest (which now carries the ID). Publish from
that one. Publishing from the scaffold ships an empty plugin.

## 3. The thumbnail slot is 1920×1080, not 1920×960

The publish dialog says "Set a thumbnail — recommended 1920 x 1080px". The icon
is 128×128. Flatten both onto the brand field so neither carries alpha.

## 4. The Data security step is five questions with free-text follow-ups

Answer shape for a plugin that exports canvas content to your own API:

1. Backend service — "yes, and data read/derived from Figma's plugin API is sent
   to this backend". This then demands a public vulnerability-disclosure process
   and any security accreditations.
2. Network requests to services you do not host — tick "not captured by the
   above" and name your CDN/upload hosts.
3. Authentication — "via a site that I host".
4. Storage — "locally (figma.clientStorage)".
5. How updates are managed.

Question 1 asks for a **publicly documented** vulnerability process. If the
product has no SECURITY.md or /security page, that answer cannot honestly be
yes. Write one before submitting. Do not bluff.

## 5. Figma needs no walkthrough video

Unlike Canva and monday, Figma does not require a walkthrough video. Review
happens once on first publish. Later updates ship without re-review.

## 6. "Include a playground file" is optional

Skip it for a plugin that acts on the user's own canvas.

## Sequence that avoids the traps

1. Mint a plugin ID via **New plugin… → Figma design → Empty**. Copy `id` into
   your `manifest.json`.
2. Remove the scaffold and your imported plugin from Manage plugins.
3. Re-import your manifest (now with the ID).
4. Degrade `figma.clientStorage` failures to in-memory storage plus a persist
   warning, so a missing ID is not a hard failure.
5. Write a public SECURITY.md or /security page before you open Data security.
6. Prepare a **1920×1080** thumbnail and a **128×128** icon. Flatten both. No
   alpha.
7. Skip the playground file if the plugin acts on the user's canvas. Skip the
   walkthrough video.
8. Fill the five Data security questions.
9. Publish from the re-imported plugin, not the scaffold.

## Related skills
- `figma-plugin` — the build path: sandbox vs iframe, `networkAccess`,
  `exportAsync`, the self-contained UI.
- `canva-app` — sibling marketplace playbook; Canva does require a walkthrough
  video.
- `monday-app-submission` — sibling marketplace playbook; monday does require a
  demo video.
