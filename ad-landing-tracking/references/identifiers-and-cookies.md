# Identifiers, cookies and checkout

## Click ids and UTM fields

- Capture the click id of every paid platform you run, plus the five standard UTM fields. A platform matches a conversion to a click only with its own id.
- Keep this list: `gclid`, `gbraid`, `wbraid`, `dclid` (Google), `fbclid` (Meta), `rdt_cid` (Reddit). Add `ttclid`, `msclkid`, `li_fat_id` or `twclid` only when you run that platform. A short list stays correct.
- Add `variant` to the allowlist, next to the UTM fields. See [variants-and-naming.md](variants-and-naming.md).
- Keep click ids and UTM fields in two lists. Build one allowlist from both. Cookie capture and link forwarding must use the same set.
- Forward only the allowlist across domains. Do not forward other keys such as `utm_id`. This stops junk and leaks.
- Add params to a link only when its host equals the target host. Sibling sites must never receive visitor params.
- Capture the ad platform's dynamic fields with each lead: keyword, match type, campaign id, ad group id, creative, device, network, placement, position, location. Do not forward them. Analysis needs them. The destination does not.
- Never store the full query string. It can hold tokens, codes or emails. Store only allowlisted params. Keep the raw `utm_*` values for the UTM fields only, so a tag that does not parse still shows in reports.
- Clean every captured value. Strip control characters, collapse spaces, trim, and cap the length at 200. URL values are untrusted.

## First-touch cookie

| Rule | Reason |
|---|---|
| Use `HttpOnly`, `Secure`, `SameSite=Lax`, on the parent domain, 90 days | Subdomains share it. Page scripts cannot read it. |
| Keep the first value per param. Merge in params that are new on later visits. | A visitor who clicked ads on two platforms keeps both first touches. |
| Write the cookie only when a new param arrives | A `Set-Cookie` on every response breaks CDN caching. |
| Set the cookie on every response path, including redirects and rewrites | A redirect drops the query string. The id is lost if that response sets nothing. |
| Never add `Set-Cookie` to a cacheable response without a new param | Edge caching keeps working. |

Back up first-touch params in local storage with the same lifetime. Let the current URL win for the page being viewed. Treat the backup as best effort, because private mode can block storage.

## Links on the page

- Put the allowlisted params on the server-rendered CTA link. Apply them again at click time. The helper must be safe to run twice. This works before hydration, without scripts, and for crawlers.
- Params already on a destination link win. Inbound values fill only missing keys. A pre-set UTM tag on a CTA stays correct.
- After a lead form, prefill the captured value on the next URL. Then attach the allowlisted params again. The visitor stays attributed through signup.
- Exempt the public lead API from login checks. Post to it as an anonymous visitor in a test. A login redirect once dropped leads and their attribution with no error.

## Checkout and webhook

1. Read the click ids and the analytics client id in the browser at the moment of the purchase click.
2. Send them to your server. Check each by format and length. The client is not trusted.
3. Store them in the payment session metadata. Respect the provider's limit per metadata value (500 characters).
4. Read them back in the payment webhook. The webhook has no browser.

Do not stamp attribution at signup. Signup-time stamping depends on timing. A long-lived cookie read at purchase does not.

For server events:

- Use the real client id from the `_ga` cookie. Fall back to the user id only when the cookie is truly absent. A user id does not join the visitor's session.
- Keep the Google click id with its capture time. Google's upload guide does not say to send the first click. It says only to capture the id from the ad click URL. It also says a successful response does not prove attribution. Send the click id that you tested against your attribution setting.
- Keep the latest Meta and Reddit click id. Their server APIs should follow the latest click that can lead to a sale.
- Send the raw `_fbc` cookie value as is. Build it from `fbclid` only when the cookie is missing. Send `_fbp` too. The cookie keeps the original click time, and `_fbp` raises match quality.
