# Landing pages for ads

Rules for pages that receive paid clicks. Each has a reason and a check.

| Rule | Why | How to check |
|---|---|---|
| Make a lasting, catalog-built page indexable, with a canonical to the product page. Throwaway variant pages stay `noindex`. | The product page keeps the ranking. The ad page does not compete with it. | Read the `canonical` link. It points to the product page URL. |
| Leave out the site header and footer. | Each extra link is an exit before the form. | Load the page. The only actions are the form and the offer. |
| Load the pixel on every page, the thank-you page too, after the consent check. | A missing page breaks the funnel and the audiences. | Capture pixel requests on each page. See [verify-events-live.md](verify-events-live.md). |
| Carry UTM fields, click ids and `variant` through the form and checkout. | A lost id means a sale the platform never sees. | Submit with test params. Read them on the lead row and in the payment metadata. |
| Build pages from the store catalog, not hand copy. | Any site on the template can then run ads. Hand copy drifts from the product. | Change a product price in the catalog. The ad page shows the new price. |
| Never print paid content on a public page. | The page gives away what the buyer pays for. | Search the page source for text from the paid product. Expect no match. |

Note: `ad-test-launch` and [variants-and-naming.md](variants-and-naming.md)
keep throwaway persona and variant pages out of the index. Use the canonical
rule here only for lasting pages built from the catalog.
