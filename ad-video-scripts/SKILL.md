---
name: ad-video-scripts
description: "Write short vertical video ads (20-30 s) for a paid test: pick a hook formula for the goal, write a five-beat script that fits its word budget, tie every claim to a source line, render a storyboard page to review, then hand off to production. Use after ad research and a chosen persona, before any voice or video spend, or when a script reads flat or runs long."
---

# ad-video-scripts

Scripts and storyboard for short ads. Nothing here spends money. Production starts only after the owner approves the storyboard.

Start at `ad-research-to-creative` (research, angles, persona; it is a separate skill, merge it first). Use `launch-video-screenwriting` for craft and `ship-demo-video` for the HyperFrames build. This skill is the glue for paid ads: it picks the hook by goal, fits the words to the time, and checks every claim.

## Flow

1. **Set the offer and the goal.** One video, one offer, one primary event to win. A free guide's primary event is `Lead`. A paid kit's is `Purchase`, and `InitiateCheckout` is the signal on the way. See `ad-conversion-hub` for the event names.
2. **Pick a hook formula** from [hook-formulas](references/hook-formulas.md). Match the formula to the goal. Write one line on why.
3. **Write five beats.** Hook 0-3 s, Cost 3-7 s, Turn 7-13 s, Proof 13-20 s, Afterthought 20-25 s. One job per beat.
4. **Fit the words to the time.** The voice runs about 2.4 words a second. Count the words per shot and compare with the shot length. A 25 s video holds about 58 words. A draft of 71 words needed 30 s and had to be cut.
5. **Fill the claim-check column.** Each shot names the source line it relies on: a line of the guide, a price in the store file, or "opinion, no claim". A shot with no source gets cut or labeled EXAMPLE on screen.
6. **Render the storyboard** with [the tool](tools/build_storyboard.py) and review it in a browser. See [the example](examples/example-scripts.json) for the file shape (a made-up business).
7. **Get approval, then produce.** Voice, then lipsync, then cut-aways, then render. See "Production notes".

## Script rules

- Spoken line and on-screen text differ. Many viewers start with the sound off, so the text carries the promise alone.
- Name the pain flatly in beat 1. No greeting, no logo, no "hey guys".
- Open a loop in the hook and close it in the proof. Never close it in the hook.
- Put the punch word last in a line, so the cut lands on it.
- One number per hook at most, and it must be true. Never invent a number.
- The end card names the offer and the address. No price and no dollar amount, no plea, no tagline. Hold it 3 s. For a free offer, the word "free" names the offer and is fine.
- Frame 0 and the last frame mirror each other, so a rewatch starts the loop.
- One ask only. Do not stack calls to action.
- Do not write "watch what happens" or "you will not believe".

## Rules for an AI host

- The host is a guide, never a customer. Write no first-person experience ("I built this myself").
- Do not write a testimonial, a result or a stat that no source backs.
- An invented example is labeled EXAMPLE on screen, and it shows no real quote, brand or person.
- Keep outfits polished. An ad that reads as sexually suggestive is rejected, and one rejection can hurt the whole ad account.

## Safe frame (9:16, 1080 x 1920)

Meta covers the edges of a vertical ad with its own interface: the profile and label at the top, the caption, audio strip and button at the bottom, and the like, comment and share icons on the right. Design to the tightest placement, Reels.

| Edge | Keep free | Pixels |
|---|---|---|
| Top | 14% | 0 to 269 |
| Bottom | 35% | 1248 to 1920 |
| Left and right | 6% each | 65 each |
| Bottom-right corner | extra clear | the icon column |

- All captions, cards and end-card text sit inside the middle box: x 65 to 1015, y 269 to 1248.
- Keep the host's face inside that box too, with the eyes above y 900.
- A background may run to the edge. Nothing a viewer must read may.
- Render a check image with the box drawn on one frame of each shot, and look at it before the final render.
- Source for the numbers: 2026 ad-spec guides that agree on 14% top, 35% bottom and 6% sides for Reels, for example blog.adnabu.com/meta-ads/meta-safe-zones, adnova.ai/blogs/meta-ad-safe-zones-guide and yosefk.me/blog/meta-ads-safe-zones-complete-guide-2026. These are third-party guides, not a Meta page. Check again if Meta changes its layout.

## Production notes

- **Voice.** Pick one voice per persona and keep it. Make the whole voice track in one pass, then cut the picture to it.
- **Lipsync.** `wavespeed-ai/ltx-2.3/lipsync` takes an image and audio. Audio must be 5-20 s, so split a longer take. Make clips only for the shots where the host is on screen. Quote the price with `wavespeed price` before a run. A still portrait moves little. If it looks stiff, use a HeyGen photo avatar.
- **Identity.** The host's face comes from the chosen image, not from a prompt. Make new poses with the image-edit model (see `ad-research-to-creative`, persona section).
- **Cut-aways.** Use real screen captures of the live guide pages and HTML cards. Never generate on-screen text.
- **Formats.** 9:16 first. A 4:5 feed cut needs its own layout, not a crop.
- **Cost and time, first run.** Three 25 s ads cost $1.99 and about 29 minutes of work: lipsync 83%, stills 8%, voice 6%, everything drawn or rendered locally $0. The steps are in [production-lessons](references/production-lessons.md), with the changes that should cut the next run to about $1.00.
- **Log it.** Record each step's seconds and dollars with `prodlog`, and render the safe-frame check with `safe-frame-check` (both in the scripts repo). Measure one real paid run from the balance before you plan a budget: a quoted price can differ from the charge.
- **Where the video goes.** Meta ads (one ad set per hook), the matching landing page, retargeting of viewers who watch half or more, organic Reels and Shorts, and the first email after a Lead. Meta ads need a Facebook Page (or an Instagram account linked to the ad account). Organic posts need an account on each channel. Check that the site has them before you plan.

## Check before showing the owner

- [ ] Each shot has a source line, or is marked EXAMPLE or opinion.
- [ ] Words fit the time at 2.4 words a second.
- [ ] Spoken and on-screen text differ.
- [ ] The end card holds 3 s and has one ask.
- [ ] No first-person claim, no invented stat.
- [ ] The Page and the currency are listed as open decisions.
- [ ] Every caption and the host's face sit inside the safe frame (see below).

## Lessons log

One dated line per project. Add a line after each run, and fix the rules above when a lesson changes them.

- 2026-11-10, first directory site: three scripts. A 71-word script overran a 25 s video, so the word budget became step 4. The storyboard tool found a clipped URL on the end card. The site had no Facebook Page, so the Page check moved into the production notes. The owner then asked for a safe frame, no price on the end card, and more of the product's world in shot, so those became rules.
- Keep project names, products, hooks and faces out of this public repo. Keep them in a private notes file.
- 2026-11-10, first production run: three 25 s ads for $1.99. Lipsync is the cost. Pay for it only on the hook shot and one mid shot, show the other host shots as a slow-zoom still under the voice, and make the voice track first so no line needs a speed-up. Render the safe-frame check for every shot, because it caught three layout bugs a code check would not.
