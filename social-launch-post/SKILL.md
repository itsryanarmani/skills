---
name: social-launch-post
description: "Draft and cross-post a product launch announcement (with video/media) across X, LinkedIn, Threads, Bluesky, and Mastodon via the Typefully API -- the real request schemas, the presigned-upload gotcha, per-platform post-shape differences, and the honest limits of what's actually automatable (X blocks automated publishing of link-containing posts)."
---

# social-launch-post

Empirical, from actually posting a real launch announcement with an attached video across 5 platforms via Typefully's v2 API.

## 1. Core flow

```
POST /v2/social-sets/{social_set_id}/drafts   -> creates a draft (omit publish_at to keep it a draft)
PATCH /v2/social-sets/{social_set_id}/drafts/{draft_id}  -> update platforms/content on an existing draft
```

`GET /v2/social-sets` (no id needed) lists the accounts your API key can post as — grab the right `id` from there before doing anything else if there's more than one connected account/brand.

Auth: `Authorization: Bearer $TYPEFULLY_API_KEY` on every call.

## 2. Media upload is a 3-step dance, and the PUT step is a real trap

1. `POST /v2/social-sets/{id}/media/upload` with `{"file_name": "..."}` → returns `{"media_id": "...", "upload_url": "<presigned S3 URL>"}`.
2. `PUT <upload_url>` with the raw file bytes.
3. `GET /v2/social-sets/{id}/media/{media_id}` → poll until `"status": "ready"`.

**Step 2 fails with `SignatureDoesNotMatch` (403) if you send ANY extra headers** — no `Content-Type`, no re-declaring the `x-amz-meta-*` values as headers (they're already baked into the presigned URL's signed query string; sending them again as headers doesn't match what the server actually signed). The working call is exactly:

```bash
curl -X PUT -H "Content-Type:" --data-binary "@file.mp4" "<upload_url>"
```

The empty `-H "Content-Type:"` is deliberate — it tells curl to omit the header entirely, since curl otherwise attaches a default that doesn't match the presigned signature. Three earlier attempts (default content-type, matching content-type explicitly, re-sending the meta headers) all failed identically; the fix was sending *nothing extra at all*.

## 3. Attaching media and building the platform payload

Attach a ready `media_id` to a post via the `media_ids` array field on that post object:

```json
{
  "platforms": {
    "x": {
      "enabled": true,
      "posts": [
        {"text": "hook line here", "media_ids": ["<media_id>"]},
        {"text": "follow-up / link, as a reply in the thread"}
      ]
    }
  }
}
```

**Per-platform post-shape differences are real, not just theoretical:**
- **LinkedIn only supports a single post, not a thread** — sending a 2-element `posts` array to `linkedin` fails validation (`"LinkedIn only supports single posts"`). Combine hook + link into one post's text for LinkedIn specifically; keep the thread structure for X/Threads/Bluesky/Mastodon.
- Enable multiple platforms in the same PATCH by adding each as its own key under `platforms` — reuse the same thread-shaped `posts` array for the platforms that support threads, and a separate single-post array for LinkedIn.

## 4. Publishing is not fully automatable on X

Setting `{"publish_at": "now"}` via the API can return `{"error": {"code": "FORBIDDEN", "message": "This is not allowed by X policy. Direct publishing of X drafts containing URLs is blocked."}}`. This is a real anti-spam/anti-automation policy enforced server-side by Typefully on X's behalf — it applies identically regardless of which client hits the API (REST or an MCP wrapper share the same backend check), so there's no legitimate way around it via API. **Don't try to route around it** (splitting/obfuscating the URL, posting the link in a follow-up edit, etc.) — that's evading an anti-spam control, not solving a technical problem. The correct move: leave the draft ready via the API, and have the human publish it manually through Typefully's own UI, which is designed to satisfy whatever additional human-in-the-loop step X's policy requires.

## 5. A launch series where each X post quotes the last one

A series reads as one story when each launch quote-posts the previous launch, and the newest one is pinned.
Set the quote with `quote_post_url` on the first X post. It applies to X only; the other platforms post the
text and media.

- **A post has no URL until it publishes, so the chain fills one link at a time.** Schedule only the first
  post. Keep every later post an unscheduled draft. When post N goes live, read its `x_published_url`, set it
  as the next draft's `quote_post_url`, and schedule that draft (for example 2 days after N). A draft that is
  scheduled before its quote is set goes out unquoted.
- **Run that step from a job, not from a session.** A chat session closes; a series of 20 posts takes 6
  weeks. `typefully-quote-chain` in `itsryanarmani/scripts` is a launchd job that does this every 15 minutes
  and stops when the chain is done. The job waits on a post that never publishes, so check that each one
  went live.
- **Each platform keeps its own text.** An owner who edits a draft in the Typefully editor often changes only
  the X text; LinkedIn, Threads and Bluesky keep the old copy. After any owner edit, compare every enabled
  platform's text with X's and sync the ones that differ. On one series, 15 of 19 drafts had drifted.
- **A PATCH re-sends every enabled platform.** Build the `platforms` object from the draft you just read,
  change only what you mean to change, and check the response: same text, same `media_ids`, same platforms.
- **Open question: does a scheduled X post with a URL publish?** Section 4's block was seen on
  `publish_at: "now"`. Scheduling a URL post for later returned `status: scheduled`, but whether X lets it
  publish was not yet observed. Watch the first one at its time. If it fails, publish it in Typefully's UI;
  the chain continues once the post has a URL.
- Pinning has no API. Pin each new launch by hand on X.

## 6. Video aspect ratio for cross-posting

A launch video built at 1:1 (square) — the natural choice if the storyboard/generation pipeline (`launch-video-generation`) was built that way — will get pillarboxed (black bars) in vertical-feed players expecting 9:16. Two fixes, and the plainer one is usually the better call:

- **Crop/pad to 9:16 with a blurred background fill** (`ffmpeg` `gblur` on an upscaled+cropped copy of the same footage as background, original square centered on top): technically fills the frame edge-to-edge, but the blurred top/bottom bands read as visually noisy and can look worse than the plain original, not better.
- **Just keep it square.** A 1:1 video posts natively without modification on X/Threads/Bluesky/LinkedIn feeds; pillarboxing on vertical-only surfaces (e.g. a Stories/Reels-style placement) is a smaller cost than an unwanted blur treatment. Prefer this unless the target surface is *specifically* vertical-only.

## See also

- [`../launch-seo/SKILL.md`](../launch-seo/SKILL.md) — run this before posting: without Open Graph/Twitter Card meta on the linked site, the posts this skill drafts will unfurl bare (no title, description, or image) across every platform.
- [`../ship-a-product/SKILL.md`](../ship-a-product/SKILL.md) — orchestrator this stage belongs to.
