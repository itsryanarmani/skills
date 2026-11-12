# Facebook Page trust before ads

People tap the Page name on an ad before they click the link. An empty Page
looks abandoned and costs trust. Fix the Page before any spend. The public
`fb-page-polish` tool in `itsryanarmani/scripts` builds the assets and applies
them. Run it with no arguments to read its usage.

## 1. Minimum before any spend

Rule: the Page has a profile photo, a cover photo, a bio, a website link and a
category before the first ad runs.

- Why: with no photo, no cover, no bio, no link and 0 posts, the Page looks
  dead. A visitor who taps the name from the ad leaves.
- Check: open the Page as a visitor. All five fields show in the header and
  the intro.

Then, still before the first ad: hide the two auto-posts and add three starter
posts (sections 6 and 7). Add a contact method when the owner has one.

- Why: a Page with 0 posts looks abandoned even with a good header.
- Never invent reviews, followers or testimonials.

## 2. Build the assets from the site's brand

Rule: make every asset from the site's own logo, colours and words. Never use
stock images.

- Profile photo: the logo on the brand colour, square, with a margin.
  Facebook crops it to a circle, so keep the logo inside the circle.
- Cover: 1640 x 720. The logo, the name and the site's own one-line
  description.
- Bio: max 101 characters. Copy it from the site's tagline. Do not write new
  claims.
- Why: the Page must look like the site the ad sends people to. A stock image
  or a new claim breaks that link.
- Check: put the profile photo, the cover and the site's header side by side.
  They use the same logo, colour and words.

Example: "Example Sheds", a green logo on white, bio "Custom garden sheds,
built and delivered." from the site's tagline, link `https://example.test`.

## 3. Drive the Page editor with a logged-in browser

These notes are for the browse sandbox and a logged-in personal profile. See
`agent-browser-consoles` for general console rules.

- The sandbox reads files only from `/tmp`. Copy the images there before an
  upload.
- The sandbox cannot set cookies for other hosts. Use the logged-in session.
- A "Welcome to your new Page" dialog blocks every click. Close it first.
- Synthetic pointer clicks on menu items are blocked. An in-page
  `element.click()` on the same item works.
- Navigate with `domcontentloaded` and a 60 s timeout. Full page load times out.
- Switch back to the personal profile at the start and the end of every Page.
  Why: a failed run leaves the session acting as a Page. The next Page then
  shows a visitor view with no edit controls.
- Selectors follow Facebook's page text. They break when Facebook changes the
  words. Read the page again when a step finds nothing.
- Skip a field that is already filled. Do not overwrite the owner's work.
- Verify the photos with a contact sheet of header screenshots, one per Page.
  Why: Meta's public picture endpoint can report a silhouette for a real photo.
  Do not trust it as proof.

## 4. Page creation is rate limited

Rule: create only a few Pages per day. Stop on the first "too many attempts".

- Why: the limit is on new Pages, not on edits. The error arrives inside an
  HTTP 200 GraphQL reply, and the screen shows nothing.
- Check: after one attempt, open the Pages list. If no Page was made, stop and
  try on a later day. Do not loop. Do not use another account.

## 5. The Page is the ad identity

Rule: match the Page name and photo to the offer when you can.

- Any Page you control can run ads for any site. But the Page name and photo
  show on the ad, so a mismatch confuses the viewer.
- Do not tie the owner's personal profile to brand Pages in public. Use
  generic brand names, such as "Example Sheds", not a person's name.
- Check: preview one ad. The name and photo match the landing page brand.

## 6. Starter posts

Rule: post three short posts per brand Page. Post 1 says what the Page is, from
the site's own tagline. Posts 2 and 3 each give one useful fact from the site.

- Author: the Page. Switch into the Page before you post. Never post as the
  owner's profile. Why: a post from the profile ties the owner to the brand in
  public.
- Source: draft only from the site's own public text. Each post carries a
  source quote. The quote is a verbatim substring of the cited file.
- Digits: the post may contain no digit that its quote lacks. Why: a model
  rounds, converts or invents numbers. A wrong price or date is a false claim.
- Sensitive topics: hold health, money, legal, immigration and sobriety posts
  for the owner to read first.
- Review: a person reads every post before it goes up. The script is a
  filter, not a review. The owner reads every sensitive post.
- Pace: space the posts out or post them in one batch. Why: the order and the
  timing matter less than the text. Never trade review for speed.
- Never invent followers, reviews, results or testimonials.
- Check: a script runs both tests on every draft before any post. It fails the
  batch when a quote is not in the file or a post has a new digit. The script
  cannot catch a new claim in words, so the human read must.

Example draft record:

```json
{"page": "Example Sheds", "file": "site/about.md",
 "quote": "Custom garden sheds, built and delivered.",
 "post": "Example Sheds: custom garden sheds, built and delivered."}
```

## 7. Auto-posts and admin-only labels

Facebook makes two posts by itself: "updated their profile picture" and
"updated their cover photo". The only option is "Hide from Page".

- Rule: hide both after the polish. Why: they push the starter posts down and
  look like filler.
- Admins see "Published by <owner name>" and "Comment as <owner name>" on Page
  posts. The public never sees these labels.
- Rule: do not read an admin-only label as public exposure.
- Check: before you conclude the owner is exposed, open the Page as a visitor.
  Scan the About, Page transparency and Photos tabs for the owner's name.

## 8. Browser posting traps

- The final "Post" button is not ready right after "Next". Wait, then retry
  the click until the dialog closes.
- A failed click publishes nothing and shows no error.
- Check: after the run, count each post on the Page. Match the full first
  line, not a short prefix. Why: a short prefix matched the Page name and
  counted a post that did not exist.
- The "What's on your mind" box renders late. Wait for it with
  `waitForFunction`, not a fixed sleep.
- Do not use the Graph `picture` endpoint as a check. It flags real photos as
  silhouettes. Use header screenshots (section 3).

## 9. Daily posting (plan, not yet built)

The browser route is a fallback only. It needs the owner's machine on and
Chrome logged in. It breaks when Facebook changes its page text.

The reliable route is the Graph API with a Page access token:

1. Grant the system user "create content" on each Page.
2. Generate a system user token with `pages_show_list`, `pages_manage_posts`
   and `pages_read_engagement`. Read each Page's own access token from it.
   These permissions can need Advanced Access or app review.
3. Queue ready posts per Page. Each post passed the section 6 checks.
4. Post one per day per Page, as the Page.
5. Dry run by default. Post only with an explicit apply flag.
6. Call an approval hook before each post.
7. Give each post a key. Skip a key that is already posted. Why: a retry must
   not post twice.

Engine: the public npm package `agentic-publish`. It routes brand queues
through approval hooks. A Facebook Page route is part of this plan.

Exists now: `fb-page-polish` in the public scripts repo has `post`,
`hide-autoposts` and `verify` subcommands for the browser route.

## 10. News and daily content (plan, not built)

A per-site `/news` section is one tagged blog post per item.

- Sources: an allow-list of feeds only. Use a recency window. Dedupe items.
- Shape: a two-sentence TL;DR first, then a "why it matters" line, the source
  link and a link to the site's own guide.
- Numbers: every number and date in the output must appear in the source
  text. Check it with the same script test as section 6.
- Summarize. Never copy the source text.
- Sensitive niches need a human read before publish.
- Why: mass-produced thin pages risk a search penalty. Each item must add
  context that the source does not give.
- Discovery: the public npm package `agentic-scout`. A new news pipeline
  package is planned.
