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

Next level: posts and a contact method. Posts are public, so the owner approves
each one first. Never invent reviews, followers or testimonials.

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
