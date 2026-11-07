---
name: public-identity-migration
description: Audit and migrate a person's former public name, handles, and website across owned accounts, GitHub, publications, directories, and third-party mentions. Use for legal-name changes, personal rebrands, old-handle cleanup, or correction outreach. Track verified changes and unresolved records without claiming complete internet coverage.
---

# Public identity migration

Create an evidence ledger, correct owned surfaces, and request corrections from verified publishers.
Use an existing authorization. Do not ask again for actions the user already approves.

## Establish the identity contract

Record these values in a private task folder:

- Current display name, former names, aliases, and common misspellings.
- Exact current handles and URLs for each platform.
- Confirmed account ownership, immutable account IDs, and the current website.
- Authorized account edits, repository changes, publication corrections, and external messages.
- Contacts or accounts that need a signed-in session or user verification.

A display name, account handle, npm maintainer, email address, and repository owner are separate fields.
Never infer that one changes because another changes.
Do not publish identity documents, private account bindings, tokens, or the private ledger.

## Discover and classify

Start with existing inventories. Search aliases separately across web search, platform search, and first-party APIs.
Check profiles, pinned content, bios, articles, videos, descriptions, captions, PDFs, events, awards, directories, and research records.
Follow source links into mirrors and aggregators. Group repeated URLs under their publisher or account.

Record each finding with:

| Field | Meaning |
|---|---|
| URL and source | Exact page and discovery source |
| Checked time | Time of the live observation |
| Evidence | Current matching text, a stale search result, or a failed read |
| Identity | Confirmed person, probable match, unrelated person, or unknown |
| Control | Owned account, owned repository, publisher, mirror, or immutable record |
| Proposed change | Exact fields and replacement values |
| State | Found, ready, changed, request sent, verified, blocked, or retained identifier |
| Proof | Commit, PR, API read-back, message ID, ticket, or screenshot path |

Confirm identity through an independent account link, project, affiliation, or immutable ID.
Exclude unrelated people who share the same name.
A blocked page is unknown. A search snippet is not proof of current page content.
Counts describe URLs or records, not necessarily distinct profiles or people.

## Audit GitHub

1. Read the authenticated account ID and login.
2. Enumerate owned public repositories with pagination. Mark private repositories separately.
3. Record each default branch and commit. Scan that exact commit rather than a moving branch.
4. Check current source, README files, repository descriptions, homepage URLs, topics, gists, and the profile README.
5. Query public issues, PRs, comments, discussions, releases, and other owners' repositories separately.
6. Record search totals, result caps, truncated trees, large files, inaccessible records, and archive failures.

Use `scripts/audit_identity.py` for a read-only scan of a local Git checkout:

```sh
python3 scripts/audit_identity.py /path/to/repo \
  --term 'Former Name' --term formerhandle --output /private/audit.json
```

The scanner records the baseline commit, tracked working-tree state, file hashes, and matching line locations.
It does not copy complete source lines.
It does not change files or contact GitHub.
It skips likely credential files, links, binaries, and large files. Review its coverage gaps separately.
A local scan does not cover remote issues, comments, gists, or other branches.

## Correct owned surfaces

Edit the source that controls each public surface. Verify the rendered result afterward.
For social accounts, use the existing [social-profile](../social-profile/SKILL.md) skill where its supported fields fit.
Use platform APIs or an existing signed-in session for other fields.
Record missing access rather than claiming the account changes.

For GitHub:

- Verify that a renamed account has the same immutable ID.
- Check whether its profile README repository still has the former username.
- Update current profile text, links, badges, contribution widgets, repository metadata, and owned author credits.
- Fix CI download URLs before depending on checks that fetch another renamed repository.
- Preserve working package names, npm ownership, email delivery addresses, application IDs, and credential keys.
- Use exact URL or field replacements. Do not replace every matching substring.
- Preserve third-party copyright, coauthors, quotes, historical evidence, and commit IDs.
- Do not rewrite Git history or alter other people's content to remove a former name.
- Keep release artifacts and historical snapshots in a separate review queue.

Follow each repository's issue, branch, local check, proof, and review rules.
Keep one concern per PR. Split large changes before writing them.
Do not publish a release or deploy a site merely because its README changes.

For a website, inspect HTML, JSON-LD, social metadata, canonical URLs, sitemaps, feeds, PDFs, and stored content.
A source-file edit does not update database rows or a deployed bundle.
Back up affected rows. Compare exact expected replacements before and after each write.

## Correct publications

Use the publisher's supported author-name correction process.
Preserve DOI, ORCID, coauthors, license, version identity, scientific claims, and numeric results.
Verify both the displayed name and structured given/family names in the DOI registry.

For file corrections, download the originals and verify their checksums first.
Compare text, page counts, and title-page appearance after rebuilding.
Obtain exclusive access when an edit endpoint can reuse an existing draft.
Stop on an uncertain write result. Read back before deciding whether a retry is safe.
Do not create a new version or DOI unless the publisher requires it for the approved change.
Do not infer account-profile changes from corrected publication metadata.

## Contact third parties

Send requests only when the user authorizes external contact.
Honor that authorization without adding another approval step.

Verify the recipient through the publisher's own contact or correction page.
Use the user's connected personal account. Do not send personal requests from a work account.
Deduplicate by publisher and check prior sent mail before sending.
Include exact affected URLs and requested field changes.
Ask for the current name and links. Preserve the underlying article, dates, and other people's credits.
Do not attach identification documents automatically.

Use this short request, adapted to the verified record:

> Hello,
>
> My public name is now [current name]. Your page still credits me as [former name]:
> [exact URLs]
>
> Please update my name to [current name] and my website to [current website].
> Please keep the other facts, dates, and credits unchanged.
> Let me know if you need an account verification step.
>
> Thank you,
> [current name]

Keep the sent message ID, recipient, source contact page, body hash, affected URLs, and send time in the private ledger.
Do not equate a sent request with a corrected page.
For uncertain send outcomes, check sent mail before retrying.
Record a follow-up date. Follow up once, without sending repeated requests to several staff members.

## Verify and hand back

Read changed profiles and documents through their normal public URLs.
Recheck repository default commits after merges. Confirm deployed pages use the merged content.
Check redirects and dependent tools after any handle or domain change.
Separate these outcomes:

- Changed and publicly verified.
- Request sent; publisher response pending.
- Access or verification required.
- Retained technical or historical identifiers, with a reason.
- Unchecked or inaccessible records, with coverage limits.

Report the concrete counts, linked PRs, sent requests, and remaining work.
Never claim that every internet occurrence is found or removed.
