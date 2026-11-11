# Organic static ads: phone-photo style for Meta feeds

A reference for image ads that look like a snapshot from a phone, not a campaign. It adds to the
`ad-image-prompt-library` skill. Read `SKILL.md` first for the polished recipes and the HTML mockups.
Read `ad-creative-generation` for endpoints, references and the vision-QA loop. This file adds twelve
organic prompt templates, overlay and call-to-action (CTA) rules, a policy checklist, a test plan and a
dated source catalog. Everything here is generic. Swap each `[PLACEHOLDER]` for your own facts.

## 1. The hypothesis, and how strong the evidence is

**Hypothesis to test:** for a given audience and offer, a static that looks like a candid phone photo gets
a lower cost per result than a polished static with the same hook and offer.

Do not treat this as settled. As of 2026-11-10, the public sources say this:

| Claim you will read | What the source shows | Level |
|---|---|---|
| Phone-shot statics beat polished statics by 25 to 30 percent | One agency post. It says the figure is cross-account and not causal. No data shown. | Assertion |
| Native-looking formats (notes, sticky notes, comment screenshots) work on Meta | Several agency and newsletter posts name the formats. Most show example ads, not results. | Assertion |
| One organic-style static produced cheap purchases | One agency reports a single account: 63 purchases at 24.35 EUR for its top static. No organic versus polished comparison. | Single case |
| Static ads are a large share of DTC creative | A count of 67,852 ads from 106 brands: 55.6 percent static. It measures how common they are, not how well they work. | Prevalence only |
| Polished still wins in some categories | The same agency says finance, premium positioning and product demos. No data. | Assertion |

Read the table as: formats are named often, controlled proof is missing. The Ad Library gives a weak
signal at best. In a small US pull of 118 active ads for neutral home topics (2026-11-10), the four longest image
runs (over 500 days) were all one advertiser's free checklist ads with a Download button. Run length shows an ad is
still active. It does not show that the ad is profitable.

## 2. Test plan: polished versus organic

Change one thing. Keep everything else equal.

1. **Write one hypothesis** with a number and a date. Example: "organic look lowers cost per `[RESULT]` by
   at least `[X]` percent within `[N]` days."
2. **Build two arms from one prompt.** Keep the scene, the person description, the overlay words, the CTA
   line, the offer, the landing page and the file size the same. Swap only the look block (section 3).
3. **Equal budget, same audience, same placement, same start time.** Use the Ads Manager A/B test tool. It
   splits the audience at random, so the two arms do not compete in the same auction. Two plain ad sets
   with the same audience overlap and deliver unevenly, so a gap between them proves little. Use that
   setup only for a rough read, and say so in your log. Switch off any automatic image or text change for
   the test, so both arms show what you made.
4. **Set the stop rule before you launch:** a minimum number of results per arm and a minimum run time.
   Under about 50 results per arm the noise is large. This is a rule of thumb, not a power calculation.
5. **Judge on cost per result and one step further down the funnel.** Click-through rate alone can mislead.
6. **Log the result** with the prompt, the look block and the dates. A loss is data. Keep it.
7. **Then change the next variable.** Order: look, scene template, person present or absent, overlay style,
   CTA line, format (4:5 or 9:16). Never change two at once.

See `ad-experiments` for how to read the result.

## 3. The prompt recipe

Build every prompt from six parts. Keep each part to one or two short sentences.

1. **Who shoots, with what, from where.** A named role and a device: "a friend holding an older phone at
   chest height".
2. **One thing happening, mid-action.** "Halfway through saying something", not "sitting in a kitchen".
3. **A reason for the face.** Say why the person looks that way: "listening to the person behind the
   phone".
4. **One main light and what it leaves.** "Late window light across one cheek, the other side in shade".
5. **Two or three placed objects.** Things someone put down: a mug, a pen, a folded paper.
6. **One or two flaws, each with a cause.** "Slight blur because the hand moved".

Write like a person briefing a friend, not like a spec sheet. Describe what the person does, not how
attractive they are. Say what the picture is not. Do not stack every flaw: more detail makes the image look
retouched again.

### Vocabulary to pick from

- **Device:** older phone camera, a 2014 phone, front camera at arm's length, cheap point-and-shoot.
- **Light:** window light, overhead kitchen lamp, on-camera flash at night, dusk through blinds, mixed warm
  lamp and cool window, light through a car window.
- **Look:** soft focus, visible grain, faded warm 2014 colour, slightly blown highlights, slight motion blur,
  flat colour, a little underexposed.
- **Framing:** imperfect framing, horizon tilted a few degrees, subject off centre, top of head cropped, an
  object in the foreground edge.
- **People:** messy hair, flyaway strands, bare face, natural skin texture, creased clothes. Adults only.

### Look blocks for the A/B test

Paste one block into the `[LOOK]` slot of any template.

```
POLISHED: shot on a full-frame camera, softbox light, clean seamless background, sharp focus, retouched,
  neat styling.
ORGANIC:  shot on an older phone, [window light | on-camera flash], soft focus, visible grain, faded warm
  2014 colour, imperfect framing, messy hair, flyaway strands, natural skin texture.
```

### Base negative list

Paste after every prompt. Add template extras where shown.

```
NEG-BASE: no logos, no brand marks, no readable licence plates, no text in the image, no watermark,
  no stray hands, no extra fingers, no gloss, no studio light, no skin smoothing, no faces or posters in
  the background, no stock-photo pose.
```

## 4. Twelve templates

Each template is a six-part skeleton. Add `[LOOK]` and `NEG-BASE` to every one. Set the aspect ratio in the
API call, not in the prompt: 4:5 for feed, 9:16 for Stories and Reels. Generate several candidates and run
the QA loop in `ad-creative-generation`.

**Any text a template shows is added after generation.** Image models garble words. Make the paper, screen,
note or board blank or out of focus, then add real text in a template (section 5). For an exact notes or
message screen, render the HTML recipes A1 and A2 in `SKILL.md` instead of asking the model.

### T1. Selfie

```
A [ROLE] takes a selfie at arm's length with the front camera, mid-sentence, [REASON FOR EXPRESSION].
[SETTING: ordinary room] behind them, slightly out of focus. Light: [ONE LIGHT SOURCE]. In frame:
[OBJECT 1], [OBJECT 2]. Flaw: [ONE FLAW + CAUSE]. [LOOK]. NEG-BASE.
```

### T2. Candid, mid-sentence

```
A friend takes a photo of [PERSON DESCRIPTION] while they explain [TOPIC, no words shown], one hand
moving, eyes on the friend, not the camera. [SETTING]. Light: [ONE LIGHT SOURCE]. Flaw: slight blur on the
moving hand. [LOOK]. NEG-BASE, plus no direct smile to camera.
```

### T3. Holding a printed checklist

```
[PERSON DESCRIPTION] holds up a printed sheet with the printed side tilted away so no text is readable,
other hand on [OBJECT], looking at the sheet. [SETTING]. Light: [ONE LIGHT SOURCE]. The sheet shows only
pale grey lines. [LOOK]. NEG-BASE, plus no readable words on the sheet.
```
Add the real checklist title in post. Match it to a real file.

### T4. Pointing at a detail

```
Close, slightly crooked shot. [PERSON DESCRIPTION] points one finger at [DETAIL: a crack, a joint, a label
area left blank] on [OBJECT], face half in frame, mouth slightly open as if explaining. [SETTING].
Light: [ONE LIGHT SOURCE]. [LOOK]. NEG-BASE, plus exactly one hand with five fingers.
```

### T5. Tape-measure moment

```
[PERSON DESCRIPTION] stretches a tape measure across [SPACE OR OBJECT], one end pinched in each hand,
checking a number, tongue slightly out in concentration. A pencil behind one ear. [SETTING]. Light: [ONE
LIGHT SOURCE]. The tape shows no readable numbers. [LOOK]. NEG-BASE.
```

### T6. Laughing at a tablet

```
A friend photographs [PERSON DESCRIPTION] on [SEAT], laughing at a tablet held in both hands. The tablet
screen faces away from the camera. [SETTING]. Light: [ONE LIGHT SOURCE], with a faint glow on the chin.
Flaw: soft focus because they are moving. [LOOK]. NEG-BASE.
```

### T7. Notes-app screenshot

Use HTML recipe A2 in `SKILL.md`. Content template, with your own real lines:

```
Title: [SHORT PLAIN TITLE]
- [REAL POINT 1]
- [REAL POINT 2]
- [REAL POINT 3]
(blinking cursor after point 3)
```
If you need a photo of a phone instead: "a hand holds a phone at an angle over [SURFACE], the screen is
bright but out of focus and unreadable. [LOOK]. NEG-BASE." Then place the text in post.

### T8. Message-bubble screenshot

Use HTML recipe A1 in `SKILL.md`. Every line must be real. Take the question from a real support
message you have permission to use, with the name, photo and number removed. Write only an answer that
is true. Content template:

```
Incoming: [REAL QUESTION, USED WITH PERMISSION]
Outgoing: [PLAIN ANSWER THAT IS TRUE TODAY]
```
Do not invent a customer reaction. If you have no real, permitted question, skip this format. See the
honesty rules in section 6.
If you want a photo of the phone instead: "a hand holds a phone at a slight angle on [SURFACE], the
screen shows blurred grey and blue bubble shapes with no readable words, thumb at the lower edge.
[LOOK]. NEG-BASE." Then place the real message text in post.

### T9. Handwritten sticker

```
A yellow paper sticky note stuck on [OBJECT: a box, a door, a monitor edge], slightly curled at one corner,
the note is blank, a thumb shadow at the edge. [SETTING]. Light: [ONE LIGHT SOURCE]. [LOOK].
NEG-BASE, plus no handwriting, no marks on the note.
```
Add handwriting in post with a marker font, or write the real note by hand and photograph it.

### T10. Whiteboard

```
A small whiteboard leaning on [SURFACE] in [SETTING], wiped unevenly with faint ghost smears, an uncapped
marker on the ledge. The board is blank. Light: [ONE LIGHT SOURCE], glare on one corner. [LOOK]. NEG-BASE,
plus no writing, no diagrams.
```
Add a three-to-five word line or a short list in post.

### T11. Over the shoulder

```
Over-the-shoulder shot from behind [PERSON DESCRIPTION, no face visible] looking at [OBJECT OR SPACE] on
[SURFACE]. The back of the head and one shoulder fill the left third. [SETTING]. Light: [ONE LIGHT
SOURCE]. Flaw: horizon tilted a few degrees. [LOOK]. NEG-BASE.
```

### T12. Found photo

```
A snapshot that looks pulled from an old camera roll: [PERSON DESCRIPTION] doing [ONE ORDINARY ACTION] in
[SETTING], taken by someone nearby with an older phone, on-camera flash, faded warm 2014 colour, soft
focus, grain, subject off centre, a little underexposed. Light: [ONE LIGHT SOURCE]. NEG-BASE, plus no
date stamp, no frame, no border.
```

## 5. Text overlays and CTA lines

Add text in a design tool or HTML template, never in the image prompt.

**Overlay styles that read as native:**

- **Caption line:** a plain system-style sans font in white, on a soft dark band or on a calm part of the
  photo.
- **Marker note:** a handwriting font for a sticker or whiteboard, in one colour, slightly rotated.
- **Typewriter label:** one short line in a plain mono font on a strip, like a label maker.
- **Quoted line:** a real words-as-said line in sentence case, with no quote marks added unless you have the
  permission and the source.

**Rules:**

1. Write the line first. Keep it near ten words and two lines at most. Write it as someone would say it.
2. Sentence case. No all caps, no emoji strings, no stacked exclamation marks.
3. One idea. If the line needs "and", split it into two tests.
4. Keep text inside the safe frame below. Never put text over a face or a hand that points.
5. Contrast: dark on light or light on dark, readable at thumbnail size. Shrink the file to about 300 pixels
   wide and read it.
6. No logo. Put the brand in the account name, not in the picture.

**CTA line patterns that do not read as a button** (all as plain sentences, no box, no arrow):

- "The full list is at the link."
- "Free to download. Link below."
- "Here is the one I use: `[LINK TEXT]`."
- "Ask me for the `[ASSET]`."
- A question that the link answers: "Not sure where to start? Link has a one-page guide."

Do not draw buttons, play icons or interface controls that do nothing. Use the real CTA button of the ad
unit and match its label to the offer. In a small US pull of home topics, the most common labels were
Learn more, Shop now and Download.

**Safe-frame numbers** (third-party figures, so check Meta's Ads Guide before you freeze a template):

| Format | Size | Keep text and key detail inside |
|---|---|---|
| 9:16 Stories and Reels | 1080 x 1920 | Top 14 percent (269 px) free. Bottom 35 percent (672 px) free. Sides 6 percent (65 px). Working area about 950 x 979 px. Older guides use about 250 px top and 340 to 400 px bottom. |
| 4:5 feed | 1080 x 1350 | No strict zone in most guides. Working rule: keep key content in the centre 1080 x 1080, so a 1:1 crop loses nothing. That leaves 135 px free at top and bottom. Keep 6 percent at the sides. |

Make a 4:5 version and a 9:16 version of each winner. Do not stretch one into the other.

## 6. Policy checklist and honesty rules

Meta's rules change. Read the linked page before launch. Sources named below were read on 2026-11-10.

| Check | What to do | Source |
|---|---|---|
| Personal attributes | Do not state or hint that the viewer has a trait: health, age, money status, religion, race, orientation and similar. "Do you have X?" fails. "You" with no trait is allowed. | Meta, personal attributes policy |
| Deceptive commercial practices | No misleading price, no endorsement without permission, no promise of assured gains. | Meta, prohibited commercial practices policy |
| Sensational images | No shocking or graphic image. | Meta, Advertising Standards overview |
| Adult content | No nudity or sexual suggestion. | Meta, Advertising Standards overview |
| Relevance | The ad must show the advertiser and the offer, and the product shown must match the landing page. | Meta, Advertising Standards overview |
| Before and after images | High risk. Meta restricts them in health and wellness. Third-party guides disagree on the details. Read the Health and Wellness policy first, and do not make a template of it. | Meta, health and wellness policy (named, not read in full); third-party guides |
| Fake interface | Not confirmed on a Meta page I read. Treat it as a honesty rule: no fake buttons, fake notification badges or fake platform marks. | This guide |
| Looks "too native" | One third-party summary says an ad that does not look like an ad may be flagged. Not confirmed. Keep the sponsored label and the account name visible. | Third-party summary |

**Honesty rules:**

- Do not invent testimonials, quotes, names, star ratings or review counts. Use real, permitted ones.
- Do not invent numbers: prices, savings, time to result, customers served.
- A generated or stock person is not a customer. Do not caption one as a real customer or a real expert.
- Do not use fake scarcity: no countdown timer or "only 3 left" unless it is true and current.
- Do not use deceptive pricing: no "was" price you never charged, and the price must match the landing page.
- Do not copy a competitor's claim, mark or face. Borrow a layout idea only.
- Check Meta's current rules on labelling AI-generated images. This guide did not verify them.

## 7. Check before you ship

- [ ] View at thumbnail size. Does one idea read in a second?
- [ ] Zoom in: hands, fingers, teeth, background text, background faces. Reject nonsense glyphs.
- [ ] No logo, no readable plate, no brand mark, no watermark.
- [ ] Text sits inside the safe frame, not over a face.
- [ ] Every claim and number matches the landing page and is true today.
- [ ] A polished arm exists, with the same hook, if you are testing the look.
- [ ] Prompt, look block, seed or settings, and date are saved with the file.

## 8. Source catalog

Checked 2026-11-10. "Read" means I read the pages named in the last column. "Listed" means I saw only the
title and description in a search result. I took patterns, not text. I copied no wording.

### Repositories

| Name | URL | Licence seen | Status | What I used |
|---|---|---|---|---|
| wuzihuang/candid-photo-prompt | https://github.com/wuzihuang/candid-photo-prompt | MIT | Read | Six-part scene recipe, stock-photo failure list. See THIRD-PARTY-NOTICES.md. |
| forrestneo/iphone-candid-photo-cn | https://github.com/forrestneo/iphone-candid-photo-cn | MIT | Read | One-lens rule, 2 to 4 flaws only, no gloss. See THIRD-PARTY-NOTICES.md. |
| bchenner/nanobanana-prompter | https://github.com/bchenner/nanobanana-prompter | MIT | Read | Brief like a person, action over looks, say what it is not. See THIRD-PARTY-NOTICES.md. |
| Global-AI-Group-Inc/content-generation-skills | https://github.com/Global-AI-Group-Inc/content-generation-skills | MIT | Read | UGC doctrine, no invented on-screen text. See THIRD-PARTY-NOTICES.md. |
| cheercheung/dtc-static-ad-prompts | https://github.com/cheercheung/dtc-static-ad-prompts | No public licence granted | Read (README, usage guide) | Format families only. No text used. |
| igm61799-cloud/ad-prompt-agent | https://github.com/igm61799-cloud/ad-prompt-agent | None seen | Read (README) | Per-model prompt style, a negative line on every prompt. |
| adkit/ads-skills | https://github.com/adkit/ads-skills | None asserted | Read (README) | Strategy skill layout. |
| paidbyfacu/ugly-ads | https://github.com/paidbyfacu/ugly-ads | MIT | Read (README) | Keep text off the action and off the app interface. Video. |
| 52pojie01/ugly-ads-generator | https://github.com/52pojie01/ugly-ads-generator | None seen | Read (README) | A hard-sell "ugly" style. Not the organic style here. |
| KenKaiii/king | https://github.com/KenKaiii/king | AGPL-3.0 | Listed | |
| ai-agents-for-agencies-coaches/image-studio | https://github.com/ai-agents-for-agencies-coaches/image-studio | MIT | Listed | |
| ugcadai-byte/ugc-ad-prompts | https://github.com/ugcadai-byte/ugc-ad-prompts | None seen | Listed | |
| gntrs/swipefile | https://github.com/gntrs/swipefile | MIT | Listed | |
| real-simple-labs/1000-winning-ads | https://github.com/real-simple-labs/1000-winning-ads | None seen | Listed | |

### Ad directories and swipe tools

| Name | URL | Cost seen | Status | Note |
|---|---|---|---|---|
| Meta Ad Library | https://www.facebook.com/ads/library | Free | Read via a research tool | Shows active ads, start date, format, CTA. Run length is a weak signal. |
| Foreplay | https://www.foreplay.co/pricing | From $59 a month ($49 annual), 7-day trial, card needed | Read | Swipe file, discovery library, briefs. |
| Swipekit | https://swipekit.app/pricing | From $26 a month, 14-day trial, no card | Read | Swipe file, brand tracker, browser extension. |
| Atria | https://www.tryatria.com/pricing | Core $129 a month annual promo, free plan listed | Read | Ad library, tracking, AI credits. |
| Motion | https://kive.ai/learn/facebook-ad-library-alternatives | About $750 a month (third-party figure) | Listed | Analyses your own results. Prices differ by source. The URL is a third-party comparison, not the vendor page. |
| MagicBrief | https://ad-radar.dev/alternatives/magicbrief | Not sold | Listed | Third-party posts say it closed on 2026-07-31. The URL is a third-party page. Not checked on the vendor site. |

### Articles and policy

| Name | URL | Date | Evidence |
|---|---|---|---|
| Meta Advertising Standards | https://transparency.meta.com/policies/ad-standards/ | Read 2026-11-10 | Primary policy |
| Meta, personal attributes | https://transparency.meta.com/policies/ad-standards/objectionable-content/privacy-violations-personal-attributes/ | Read 2026-11-10 | Primary policy |
| Meta, prohibited commercial practices | https://transparency.meta.com/policies/ad-standards/deceptive-content/prohibited-commercial-practices/ | Read 2026-11-10 | Primary policy |
| Applica, why ugly ads win on Meta | https://applica.agency/blog/why-ugly-ads-win-on-meta-and-why-polished-brand-creative-keeps-losing-in-feed | 2026, undated | Assertion, agency |
| Ecom Circle, static ads are working again on Meta | https://ecommercecircle.substack.com/p/static-ads-are-working-again-on-meta | 2026-08-26 | Observation |
| 225media, static ad examples | https://www.225media.com/resources/static-ad-examples | 2026-10-08 | One account with numbers |
| Curtis Howland, the DTC static ad system | https://newsletter.curtishowland.com/p/the-dtc-static-ad-system-what-67852 | 2026-06-12 | Prevalence count |
| Vibemyad, UGC static ads | https://www.vibemyad.com/blog/5-ugc-static-ads-worth-stealing-from-in-2026 | 2026-04-14 | Assertion |
| Superscale, Meta ad sizes | https://superscale.ai/learn/meta-ad-sizes | 2026 | Third-party spec; search summary only |
| AdsUploader, Meta ads safe zones | https://adsuploader.com/blog/meta-ads-safe-zones | 2026 | Third-party spec; search summary only |

### Not verified

- No source compares organic and polished statics in a controlled test.
- Meta's own size and safe-zone pages were not read. The numbers in section 5 come from third-party guides.
- Ad images in the Ad Library were not viewed.
- The "too native" flag and the AI-label rules were not confirmed on a Meta page.
