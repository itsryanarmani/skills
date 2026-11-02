---
name: journal-reviewer-applications
description: "Become a peer reviewer for journals, conference program committees, and artifact evaluation committees — the profiles to set up first (ORCID, Web of Science reviewer profile, OpenReview, Google Scholar), free reviewer training, how to pick venues by topic and entry requirements, how to apply per venue type (open form, account plus reviewer profile, volunteer form, email to the editor, invitation only), a short honest cover email template, how to avoid predatory venues, an application tracker, and a CSV of venues. Use when someone asks how to start reviewing, how to join a program committee or artifact evaluation committee, or which journals accept reviewer sign-ups."
---

# journal-reviewer-applications

Editors invite people they can find and trust. This skill gets a researcher or
practitioner findable, picks venues that accept new reviewers, applies once per
venue with accurate credentials, and stops before paying anything or claiming
expertise the profile does not show.

## Prerequisites

Set these up once. Most reviewer forms ask for a link to at least one.

1. **ORCID.** Create the iD, then fill employment, education, and works. Use
   Search & link (DataCite, Crossref) to import works instead of typing them.
   Set visibility to public for the sections an editor needs to see.
2. **Web of Science researcher profile.** It carries reviewer recognition
   (formerly Publons). Record reviews here once a journal supports it.
3. **OpenReview profile.** Required for many ML conference committees. Without
   an institutional email, moderation can take up to two weeks, so sign up
   before a call for reviewers opens. Docs:
   <https://docs.openreview.net/getting-started/creating-an-openreview-profile/signing-up-for-openreview>
4. **Google Scholar profile.** Gives editors a quick view of topics and output.
5. **Free training**, useful as evidence when publications are thin:
   - Elsevier Researcher Academy, Certified Peer Reviewer Course:
     <https://researcheracademy.elsevier.com>
   - Nature Masterclasses, Focus on Peer Review:
     <https://masterclasses.nature.com/focus-on-peer-review-online-course/16605550>
6. **Publisher accounts** (ScholarOne, Editorial Manager) are per journal. Create
   one only when a venue asks for it.

## Pick venues

Filter [`reviewer-venues.csv`](reviewer-venues.csv) in this folder, then check
each hit against these questions:

- **Topic match.** Can you name two subtopics you could review without reading
  a textbook first? If not, skip the venue.
- **Open sign-up or invitation.** Open forms and self-nomination come first.
  Invitation-only venues are a later step (see below).
- **Entry requirements.** Check `phd_required`, `publications_required`, and
  `other_criteria` before spending time on an application.
- **Practitioner-friendly venue types.** Start here without a PhD:
  - Open-source and reproducibility journals: JOSS
    (<https://reviewers.joss.theoj.org/>), ReScience C.
  - Artifact evaluation committees, which often accept students and engineers
    through self-nomination.
  - Practitioner magazines.
  - Preprint review, such as PREreview.
  - Journals with a reviewer registration, such as JMIR.
- **Region coverage.** Regional platforms such as AJOL (Africa), SciELO (Latin
  America, Iberia, South Africa), and J-STAGE (Japan) list journals that
  actively need reviewers.

### The data file

`reviewer-venues.csv` has one row per venue. Columns:

| Column | Meaning |
|---|---|
| `name`, `publisher` | Venue and who runs it |
| `region`, `country` | Where the venue or publisher is based |
| `field`, `field_group` | Specific topic and coarse group |
| `venue_type` | journal, conference PC, artifact evaluation, practitioner magazine, reviewer database, and so on |
| `signup_url` | Where to start |
| `phd_required`, `publications_required`, `orcid_required` | Entry gates as stated on the venue page (`yes`, `no`, `preferred`, or `unknown` when not stated) |
| `other_criteria` | Anything else the page says |
| `application_type` | How to apply: `open form`, `account + reviewer profile`, `volunteer form`, `email editor`, or `invitation only`, matching the next section |
| `form_asks` | What the form or editor usually requests |
| `deadline_cadence` | Rolling, annual, or per cycle |
| `fee` | Fee to review (should be `none`) |
| `predatory_check` | Notes from the legitimacy check |
| `url_check` | Whether the sign-up URL loaded when checked |

Coverage skews to AI/ML, computer science, HCI, ethics and policy, and practitioner venues. Treat a row as a lead. Re-read the venue page before applying: criteria and
URLs change, and some sites block scripted checks but load in a browser.

## Apply by type

| Type | What to do | What it usually asks |
|---|---|---|
| Open form | Fill the venue's reviewer sign-up form | Name, affiliation, keywords, ORCID |
| Account plus reviewer profile | Register in the submission system, then complete the reviewer profile and expertise keywords | Email, affiliation, ORCID, 3-10 keywords, sometimes a CV link |
| Volunteer form | Conferences and artifact evaluation committees: answer the call for reviewers or self-nomination form | Name, affiliation, topics, relevant publications or artifacts, availability, conflicts |
| Email the editor | Send the template below to the managing editor or the address on the journal's reviewer page | Short bio, expertise, a link to evidence |
| Invitation only | Do not cold-apply. Get noticed: publish and share work on the venue's topic, join the community's open reviewing, cite the journal's papers, and offer artifact reviews. Then use the email route if the page allows it | n/a |

Rules that apply to every type:

- Declare real credentials. Do not state a degree, title, or review history you
  do not have.
- Declare conflicts of interest when asked.
- Apply to a few venues at a time. Accepting more reviews than you can finish
  on time hurts the editors you want to impress.

## Cover email

Keep it under 150 words. Replace every placeholder before sending.

```text
Subject: Reviewer volunteer for {{journal}}: {{expertise_1}}, {{expertise_2}}

Dear {{editor_name}},

I would like to volunteer as a reviewer for {{journal}}. I am {{role_and_org}}
and work on {{expertise_1}} and {{expertise_2}}.

Evidence of my work: {{evidence_link}}
ORCID: {{orcid_url}}

I do not hold a prior reviewer role at this journal. I can commit to returning
reports on time, declaring conflicts of interest, and keeping manuscripts
confidential. If the journal has a reviewer form, I am happy to use it instead.

Thank you for considering this,
{{your_name}}
{{contact_email}}
```

If you have no publications, point `{{evidence_link}}` at relevant code,
artifacts, or a training certificate and say so plainly.

## Avoid predatory venues

Check every venue before applying:

- **DOAJ:** is the journal listed at <https://doaj.org>?
- **COPE:** is the publisher a member of the Committee on Publication Ethics (<https://publicationethics.org/members>)?
- **Think.Check.Submit:** run the checklist at <https://thinkchecksubmit.org>.
- **Warning signs:** a fee to review or to be listed as a reviewer, spam
  invitations outside your field, fake or invented impact factors, promised
  fast review, an unclear or unverifiable editorial board, a vague scope that
  covers everything.

Never pay to review. A legitimate venue does not charge reviewers. Drop any
venue that asks.

## Track applications

Keep one row per application. Update it when a reply arrives and set a
follow-up date two to four weeks out.

| Venue | Type | Applied on | Method | Contact | Status | Follow-up | Notes |
|---|---|---|---|---|---|---|---|
| Example Journal | account plus profile | 2026-01-15 | Reviewer profile | Editorial office | pending | 2026-02-05 | Keywords: x, y |

Statuses: `todo`, `applied`, `pending`, `invited`, `declined`, `dropped`.

## Related data

The same venue dataset and its tooling are public: see the `reviewer-venues`
folder in `pooriaarab/scripts` at <https://github.com/pooriaarab/scripts>.
