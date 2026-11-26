# Research and the sheet

One private Google Sheet holds everything. Write it with `gog sheets`. Give the
tab name in every range (see [lessons.md](lessons.md)).

## Tabs

| Tab | One row per | Main columns |
| --- | --- | --- |
| `Roles` | role | #, company, role, name in the file name, source video, edited video, edit status, video link, saved LinkedIn post, post author, author profile, saved job, match note |
| `Contacts` | person | company, role, person type (hiring manager, recruiter, post author, product leader), name, title, profile URL, work email, office, source URL, confidence, notes |
| `Companies` | role | company and role, HQ address, mailing address, careers URL, email pattern, gift policy, source URL, confidence, address check, canonical address |
| `Outreach` | send | date, channel, person, what was sent, cost, status, reply |

Keep a column for confidence in every research tab. A name taken from a video file
name is "probable". A title from a search snippet is "unconfirmed".

## Where the facts come from

1. **The saved LinkedIn posts and jobs.** If the person saved the posting, the
   author of the post is the best first contact. Read the owner's own saved items by
   hand in the owner's own session. Do not run bulk scraping: LinkedIn's terms forbid
   it. Match a post to a role by company and title.
2. **The posting.** It names the office, and sometimes the team or a manager.
3. **Company pages.** The contact, legal and privacy pages give the real mailing
   address. SEC filings give the head-office address for a public company. A
   company register gives the registered office for UK and French firms.
4. **A people-lookup tool** (a paid API) for work emails. Treat a returned email
   as unverified until you verify it. Do not guess `first.last@` patterns and send.
5. **Directories** (company-profile sites) only as a last resort. They are
   often old, and one showed a different company with a near name.

## Rules

- Collect work facts only: name, title, public profile, work email, office.
- Mark each row high, medium or low. A "likely hiring leader" is not a hiring
  manager until a source says so.
- Write what you could not find ("not found") instead of leaving a blank.
- Never put a private person's home address or phone in the sheet.
