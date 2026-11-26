# Finding and verifying mailing addresses

An address is either verified or marked unverified. See `agentic-address` for the
rule. This page is the working method.

## Find

1. Start with the company's own contact, legal or privacy page. It often says
   "mail to" with an attention line.
2. For a public company, use the head-office address in its annual filing.
3. For a UK company, read the registered office on Companies House. For a French
   company, read the registry entry. These registers are official.
4. For a role in one office, use that office. If the posting lists several cities
   or says remote, use the head office and say so in the cell.
5. Write the source and a confidence. Keep the raw text and the canonical form
   in two columns.

## Verify

```sh
gog sheets get "$SHEET" "Companies!C1:C30" --json > addr.json
address-verify --sheet-json addr.json --header --dry-run      # the script is on your PATH
address-verify --sheet-json addr.json --header --yes --out result.json
```

| Result | Meaning | Do |
| --- | --- | --- |
| `verified` | matched as written | mail |
| `corrected` | matched after a format fix | mail the canonical form |
| `failed`, "suite identifier" | street is real, a suite or floor is needed | search the company's own pages for the suite and verify again. If none exists, ask the owner: a named person on the first line may be enough, but the owner decides. |
| `failed`, "no match" | not found | check the company's own contact page. A new building can be missing from the postal data. Ask the owner before you mail. |
| not checked | outside the US and Canada | check the official register. A registered office can be an agent's address, not the office, so ask the owner before you mail. |

Write the result and the canonical form back to the sheet, in their own columns,
with the tab name in the range.

## Suites

A company that rents a whole building has no suite. A multi-tenant building has
one on the company's own contact page, in a lease filing, or in a government
register. Do not invent a suite. If none is published, put "Attn: <name>, <team>"
on the first line and get the owner's approval to mail it.

## Per person or per office

Mail to a named person in an office. A card with no name is often thrown away.
Many staff work remotely: a person's profile city may differ from the office
address. Say which one the card goes to.
