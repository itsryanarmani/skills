# Identifiers, cookies and checkout

## Click ids and UTM fields

- Capture the click id of every paid platform you run, plus the five standard UTM fields. A platform matches a conversion to a click only with its own id.
- Keep this list: `gclid`, `gbraid`, `wbraid`, `dclid` (Google), `fbclid` (Meta), `rdt_cid` (Reddit). Add `ttclid`, `msclkid`, `li_fat_id` or `twclid` only when you run that platform. A short list stays correct.
- Add `variant` to the allowlist, next to the UTM fields. See [variants-and-naming.md](variants-and-naming.md).
- Keep click ids and UTM fields in two lists. Build one allowlist from both. Cookie capture and link forwarding must use the same set.
- Forward only the allowlist across domains. Do not forward other keys such as `utm_id`. This stops junk and leaks.
- Add params to a link only when its host equals the target host. Do not put visitor params in a link or request to any other site.
- Keep a third list, capture-only: the platform's dynamic fields, such as keyword, match type, campaign id, ad group id, creative, device, network, placement, position and location. Store them on the lead record on the server, with the same cleaning. Do not put them in the cookie. Do not forward them. Analysis needs them. The destination does not.
- Never store the full query string. It can hold tokens, codes or emails. Store only allowlisted params, plus the capture-only list on the lead record. Keep the raw `utm_*` values for the UTM fields only, so a tag that does not parse still shows in reports.
- Clean every captured value. Strip control characters, collapse spaces, trim, and cap the length at 200. URL values are untrusted.

## Cookies: first touch and latest click

Use two cookies. They have two jobs.

| Cookie | Holds | Flags | Use |
|---|---|---|---|
| First touch | The first value per allowlisted param, UTM fields and `variant` | `HttpOnly`, `Secure`, `SameSite=Lax`, 90 days | Source reporting. Only the server reads it. |
| Latest click | The newest `fbclid` and `rdt_cid`, and any other id you must send fresh | `Secure`, `SameSite=Lax`, 90 days. **Not** `HttpOnly` | Page script reads it at the purchase click. |

- The latest-click cookie must be readable by script, so it cannot be `HttpOnly`. Put nothing else in it: no visitor key, no user id, no email. Keep `HttpOnly` for the first-touch cookie and for every visitor key or session cookie.
- Report source from first touch. Send the platform the latest click id. Meta says to store and send the most recent `fbclid` value, and to rebuild `_fbc` when the URL value differs from the cookie ([Meta: fbp and fbc](https://developers.facebook.com/docs/marketing-api/conversions-api/parameters/fbp-and-fbc)). Apply the same rule to the Reddit id. Check Reddit's current docs before you ship.
- First touch: keep the first value per param. Merge in params that are new on later visits. A visitor who clicked ads on two platforms keeps both first touches.
- Latest click: overwrite the id when the URL carries a different value. Keep the Google id as the Rules below say.
- Write a cookie only when a param is new or changed. A `Set-Cookie` on every response breaks CDN caching. Never add `Set-Cookie` to a cacheable response without a new or changed param.
- Set cookies on every response path, including redirects and rewrites. A redirect drops the query string. The id is lost if that response sets nothing.
- The parent domain is shared by every subdomain by design. Each subdomain, including old or third-party ones, receives the cookie on every request. Use the parent domain only when you run all subdomains under one privacy notice. Otherwise use a host-only cookie. Keep only allowlisted params in it.

### Consent

Write both cookies and the local-storage backup only after consent where the law needs opt-in. Use the same rule as [ad-conversion-hub](../../ad-conversion-hub/SKILL.md): no ad use without `measurement: true`. Before consent, keep params in page memory for that page view and write nothing. On decline, drop them. Where the law does not need opt-in, write them on first touch.

Back up the same params in local storage, with the same lifetime and the same consent rule. Let the current URL win for the page being viewed. Treat the backup as best effort, because private mode can block storage.

## Links on the page

- Put the allowlisted params on the server-rendered CTA link. Apply them again at click time. The helper must be safe to run twice. This works before hydration, without scripts, and for crawlers.
- Params already on a destination link win. Inbound values fill only missing keys. A pre-set UTM tag on a CTA stays correct.
- After a lead form, prefill the captured value on the next URL. Then attach the allowlisted params again. The visitor stays attributed through signup.
- Exempt the public lead API from login checks. Post to it as an anonymous visitor in a test. A login redirect once dropped leads and their attribution with no error.

## Checkout and webhook

1. Read the click ids and the analytics client id in the browser at the moment of the purchase click. The click ids come from the latest-click cookie.
2. Send them to your server. Check each by format and length. The client is not trusted.
3. Store them in the payment session metadata. Respect the provider's limit per metadata value. Stripe, for example, allows 500 characters per value ([Stripe metadata](https://docs.stripe.com/metadata)). Other providers differ.
4. Read them back in the payment webhook. The webhook has no browser.

Do not stamp attribution at signup. Signup-time stamping depends on timing. A long-lived cookie read at purchase does not.

For server events:

- Use the real client id from the `_ga` cookie. Fall back to the user id only when the cookie is truly absent. A user id does not join the visitor's session.
- Keep the Google click id with its capture time. Google's upload guide does not say to send the first click. It says only to capture the id from the ad click URL. It also says a successful response does not prove attribution. Send the click id that you tested against your attribution setting.
- Send the latest Meta and Reddit click id from the latest-click cookie, not the first-touch value. Keep first touch for source reports only.
- Send the raw `_fbc` cookie value as is. Build it from `fbclid` only when the cookie is missing. Send `_fbp` too. The cookie keeps the original click time, and `_fbp` raises match quality.
