---
name: paper-submission
description: "Choose a venue for a benchmark, dataset, or evaluation paper and take it from the official template through camera-ready. Covers the preprint, conference, journal, and workshop decision, deadlines and archival status, anonymity and AI-use rules, checklists, data and code hosting, and the traps. Use when someone asks where to submit a benchmark paper, how to format it, or what to do before arXiv or a conference deadline."
---

# paper-submission

A benchmark paper has one archival home. Pick it from the venue table, format
with that venue's own template, and stop before the owner's login, payment, or
signature. Listing the benchmark after acceptance is
[`benchmark-publishing`](../benchmark-publishing/SKILL.md).

Read [`references/venues.md`](references/venues.md) before naming a deadline.
Dates there were checked on 2026-10-16. A cell that says `closed` is past.
`next cycle not announced` means the venue has not posted the next date. Do
not fill either from a deadline aggregator.

## Decide

1. **Need a timestamp this week.** Submit TeX source to arXiv in `cs.AI`,
   `cs.CL`, or `cs.LG` (confirm the names on the
   [taxonomy](https://arxiv.org/category_taxonomy)). A new account or a new
   category may need endorsement. arXiv is not a conference proceeding.
2. **The contribution is a dataset, benchmark, or evaluation.** Use a track
   that says so: NeurIPS Evaluations & Datasets when that cycle is open,
   otherwise KDD Datasets & Benchmarks on its cycle, otherwise the rolling
   journals DMLR or TMLR. Do not also send that manuscript to a method track.
3. **The contribution is a model or method.** Use the main track (ICLR, ICML,
   NeurIPS main, AAAI, or ACL via ARR). A dataset track is the wrong desk.
4. **The artifact is software and the paper is not a research claim.** JOSS
   (short Markdown paper in the repo) or JMLR's open-source track (MLOSS).
5. **The subject is fairness, accountability, or impact.** FAccT. Choose
   archival or non-archival on the form. You cannot switch later.
6. **The subject is language.** Submit to ACL Rolling Review, then commit to
   ACL, EMNLP, NAACL, EACL, or COLING only while that commitment window is
   open and the reviews exist.
7. **A workshop.** Only after that workshop has posted its own CFP. A
   conference date, or a date the organizers suggested to each other, is not
   a paper deadline.

If two rows fit, prefer the one whose deadline cell is still open. If none
are open, use a rolling journal or arXiv and wait. Do not invent a date.

8. **The goal is to be found and cited.** Read
   [`references/google-scholar.md`](references/google-scholar.md) and
   [`references/citation-and-discovery.md`](references/citation-and-discovery.md).
   Scholar has no submit form. It indexes public pages. For an independent
   author, arXiv plus a Scholar profile does the work. Zenodo does not put a
   paper in Scholar.
9. **You are an independent author.** Read
   [`references/arxiv-independent-author.md`](references/arxiv-independent-author.md)
   before you start the arXiv account. A new author needs one personal
   endorser, and arXiv limits each author to 2 submissions a month. Put a
   whole family of benchmarks in ONE paper. The same file gives the order of
   operations and says which steps need a person's login.

10. **You want the paper to be good, not only accepted.** Read
    [`references/paper-quality.md`](references/paper-quality.md): what
    reviewers reward, the benchmark-quality frameworks to self-score, the
    section outline, figures, writing rules and a pre-submission checklist.
    ASD-STE100 is not for a research paper; the guide says what to use.

11. **You want more places to send it.** The three `venues-extended-*`
    files list 125 more venues with cost, fit, traps and sources. Send a paper
    to one peer-reviewed venue at a time. A preprint server or an archive may
    hold the same paper in parallel. Never submit one manuscript to two
    peer-reviewed venues at once: that is dual submission.

12. **The PDF is done and you want it published.** Follow
    [`references/publishing-runbook.md`](references/publishing-runbook.md). It
    orders the free same-day actions, the preprint servers, the one
    peer-reviewed venue, and the steps after the arXiv id appears. The
    `paper-publish` tool in `itsryanarmani/scripts` checks the paper, drafts the
    Zenodo record and writes one form file per venue.

## Steps

1. **Pick the row.** Copy its deadline, archival flag, page limit, and review
   mode into the working note. Re-open the source URL. Pages change.
2. **One archival copy.** If the row is archival, withdraw or wait before
   sending the same paper to another archival venue. Preprints and
   non-archival workshops are different. The row says which.
3. **Official template only.** Links and the page-count check are in
   [`references/templates.md`](references/templates.md). Do not download a
   style file from a course site or a random repo.
4. **Anonymity and AI use.** Follow the row. A double-blind PDF has no
   authors, no acknowledgements, and no link that names you or logs the
   reviewer. Cite your own arXiv in the third person. Disclose model
   assistance where that venue requires it. Spell-check is not authorship.
   An LLM is not an author.
5. **Checklists.** Walk
   [`references/checklists.md`](references/checklists.md). Use the checklist
   file shipped in the template. Do not retype the questions from memory.
6. **Data and code.** Host them the way the row says. NeurIPS new datasets
   need a Croissant file with Responsible AI fields, due with the paper, not
   as an afterthought. Anonymous review needs an anonymous host. Put the
   licence on the data.
7. **Submit on the official system.** Stop if the next click needs the
   owner's account, an endorsement, a fee, or a publishing agreement. Leave
   the packet ready: PDF, source, checklist, links.
8. **Camera-ready.** Re-read the page limit. It often grows by one page.
   Put acknowledgements back. Recheck the compiled PDF against the template,
   not against the draft.
9. **After acceptance.** List the benchmark with `benchmark-publishing`.
   A paper page is not a dataset card.

## Traps

- **Two archival submissions.** Withdraw the first before the second full
  paper goes in. A preprint does not make this safe.
- **Figures count.** At NeurIPS the nine pages include figures and tables.
  Shrinking the margins is a desk reject.
- **Anonymous links that are not.** A GitHub URL, a Dropbox link, a Croissant
  file, or a commit email can name the authors. So can analytics on the page.
- **arXiv wants source.** Do not upload a PDF that was built from TeX. Include
  `.bib` or `.bbl`. Check the PDF arXiv builds before you finish.
- **Closed dates stay in the table.** They stop the next agent from treating
  last cycle as open. Do not delete them.
- **OSF's generalist server is not taking new papers.** New submissions were
  suspended on 2025-08-25. Community servers on OSF still run. None of the
  listed ones is a CS server.
- **TechRxiv is paused.** The homepage says submissions are temporarily
  closed during a platform move. Old DOIs still resolve.
- **Aggregators invent dates.** ConferenceDeadlines and similar sites are not
  a source. If the official page has no date, write `next cycle not announced`.

## Stop

Do not submit, pay, register the owner as a reviewer, or accept a publishing
agreement. Do not post a non-anonymous preprint when the venue's form locked
an anonymity option. Hand the owner the venue row, the PDF, and the unanswered
login.

## See also

- [`references/venues.md`](references/venues.md)
- [`references/venues-extended-preprint.md`](references/venues-extended-preprint.md)
- [`references/venues-extended-journals.md`](references/venues-extended-journals.md)
- [`references/venues-extended-conferences.md`](references/venues-extended-conferences.md)
- [`references/free-venues.md`](references/free-venues.md)
- [`references/google-scholar.md`](references/google-scholar.md)
- [`references/citation-and-discovery.md`](references/citation-and-discovery.md)
- [`references/arxiv-independent-author.md`](references/arxiv-independent-author.md)
- [`references/templates.md`](references/templates.md)
- [`references/accounts-and-traps.md`](references/accounts-and-traps.md)
- [`references/publishing-runbook.md`](references/publishing-runbook.md)
- [`references/paper-quality.md`](references/paper-quality.md)
- [`references/checklists.md`](references/checklists.md)
- [`assets/arxiv-skeleton/`](assets/arxiv-skeleton/)
- [`../benchmark-publishing/SKILL.md`](../benchmark-publishing/SKILL.md)
