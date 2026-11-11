# Funnel-type blueprints

Four types have 4 or more pages. The other 11 types have 3 or fewer pages each (waitlist 3, booking calendar 3, short course sale 3, and singletons): do not build a blueprint from them. One screen = 1500 px of screenshot height. Medians come from `tools/aggregate_teardowns.py`. "Order" is the section types present on at least half of the pages, sorted by median position; exact orders almost never repeat (the most common exact order appears on 1-2 pages), so read it as a tendency.

| Type | n | Screens | First-screen words | Total words | CTAs | Person in hero | Nav | Urgency | Testimonials |
|---|---|---|---|---|---|---|---|---|---|
| Webinar sign-up | 14 | 3.7 | 110 | 838 | 6 | 12/14 | 0/14 | 12/14 | 9/14 |
| Lead-magnet opt-in | 8 | 1.8 | 75 | 410 | 3 | 4/8 | 1/8 | 0/8 | 3/8 |
| Long course sale | 7 | 10.2 | 85 | 1,900 | 6 | 3/7 | 3/7 | 3/7 | 7/7 |
| Event registration | 6 | 4.2 | 75 | 1,062 | 4.5 | 5/6 | 1/6 | 5/6 | 3/6 |

The long-course length is a lower bound: 3 of its 7 captures hit the cap or were cut. Median form fields in the first screen is 0 for all four types: the form sits behind a button or lower down.

## Webinar sign-up (n=14)

```text
[hero: promise, date, one button] > [problem 8/14] > [what you learn 12/14] > [host 12/14] > [proof 9/14] > [final button] > [FAQ 7/14]
```

- **Asks for:** an email, for a free live or replay session. 0 of 14 show a price.
- **Copy:** one button label repeated down the page (median 6 buttons); a date and time in the hero; 3-5 numbered learning points; a host block with one fact a visitor can check.
- **Skip:** a money-back line or a "value" price on a free session (seen on `prajakta-bhujbal-style-masterclass`, `sjak-card-reading-healer-workshop`); countdown clocks (3 of 14; the page `sjak-card-reading-healer-workshop` shows three clocks that disagree).
- **Counter-examples:** `siddharth-rajsekar-ai-coaching-workshop` is 0.5 screens; `jenna-kutcher-pinterest-traffic-strategy` is 9.2 screens. Length varies about 18-fold inside one type.

## Lead-magnet opt-in (n=8)

```text
[hero: item mock-up, one line of promise, one button] > [what is inside 7/8] > [final button 4/8]
```

- **Asks for:** an email for a file, checklist or short guide. 0 of 8 show a price and 0 of 8 use urgency.
- **Copy:** the title names the thing plainly; a mock-up of the item; a button label that names the item or says free; a short list of what is inside.
- **Skip:** an outcome promise you cannot show; navigation (7 of 8 have none).
- **Counter-examples:** `marie-forleo-free-writing-class` is 0.6 screens with about 150 words and one button; `jeff-walker-audience-monetization-blueprint` is 2.2 screens and has no testimonial. Short pages with no testimonial are normal here.

## Long course sale (n=7)

```text
[hero] > [problem 6/7] > [solution 5/7] > [host 6/7] > [proof 7/7] > [curriculum 6/7] > [bonuses 4/7] > [guarantee 4/7] > [FAQ 5/7] > [price 4/7]
```

- **Asks for:** money on or next to the page (price shown on 6 of 7). Anchoring on 6 of 7, a guarantee on 5 of 7, testimonials on 7 of 7.
- **Copy:** the order problem, solution, host, proof, what is inside, guarantee, FAQ; a curriculum list with a count per module; the guarantee in its own block with its conditions stated.
- **Skip:** grids of 16 or more result cards (they push the price far down); a struck-through "usual" price; income calculators; a guarantee that needs a minimum ad spend (`ads-course-ad-system`). Three of 7 pages carry income claims.
- **Counter-examples:** `think-media-youtube-cohort` is 4.3 screens and shows the price early; `ali-abdaal-youtube-creator-course` is 15.7 screens. Read the conditions on each guarantee before you copy one; the notes found them conditional on the pages they checked.

## Event registration (n=6)

```text
[hero: event, date, button] > [proof 3/6] > [what you get 4/6] > [host 3/6] > [FAQ 5/6]
```

- **Asks for:** a sign-up for a dated event; 3 of 6 also show a price. Urgency on 5 of 6 (date and seat limit).
- **Copy:** the date in the hero; the seat limit only if it is real; the FAQ before the last button.
- **Skip:** a second tier that appears only in the FAQ; clocks that do not match the date.
- **Counter-examples:** `iman-gadhzi-faceless-product-launch` is 95 words and one button; `sara-workshops-optin-social` is 11.3 screens.

## Use a blueprint

1. Pick the type by the action you ask for, not by how the page feels.
2. Stay inside the median screens and words at first. Test longer or shorter later (`measurement.md`).
3. Keep one action. Repeat the same button label.
4. Replace every skipped item with the honest substitute in `honest-adaptation.md`.
