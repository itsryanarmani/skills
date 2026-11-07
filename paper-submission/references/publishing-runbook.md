# Publishing runbook

An ordered run from a finished PDF to published copies. Follow the steps in order. Each step names the file that holds the facts. This file does not repeat them.

Checked 2026-10-16. `UNVERIFIED` means no official page confirmed the fact. A person opens the page before acting. Re-open each source URL before you act: pages change.

Tool: [`paper-publish`](https://github.com/itsryanarmani/scripts/blob/main/paper-publish) in `itsryanarmani/scripts`. It checks, drafts, archives and writes forms. It never submits, never solves a CAPTCHA and never ticks an agreement. Its failure modes are in `paper-publish.failure-modes.md` in the same repo.

Inputs you need: the PDF, the arXiv tarball with a `.bbl` (see [`arxiv-independent-author.md`](arxiv-independent-author.md) section F2), a `CITATION.cff`, and a `meta.json` with `title`, `abstract`, `authors` (name, affiliation, ORCID), `license`, `keywords`, `subject_class`, `comments`, `code_url`, `data_concept_dois`, and `venues`.

## 1. Pre-flight

```sh
paper-publish check meta.json --pdf paper.pdf --cff CITATION.cff
```

The command exits 1 and lists every problem. Fix them all. Run it on the final abstract, never on a draft. On its first real use it found an abstract of 1954 characters, over the arXiv limit of 1920, before the arXiv form did. It checks:

- The title is the same in `meta.json`, on page 1 of the PDF, and in `CITATION.cff`.
- The abstract has 100 to 1920 characters. arXiv rejects a longer one.
- No `XXXX` and no em dash in the text.
- Every ORCID has the right shape and checksum.
- A license is set.
- Every URL in the abstract returns 200. Use `--offline` to skip this.

Then walk the claim check in [`paper-quality.md`](paper-quality.md) (section G) and the venue checklist in [`checklists.md`](checklists.md). A paper claim must match the evidence. State only what the runs support. If a model run used a paid model without the owner's yes, stop. The experiments follow the free-only rule in [`../../paper-experiments/SKILL.md`](../../paper-experiments/SKILL.md).

## 2. Same-day free actions (no review)

These need no editor. Do them on day one.

### 2.1 Zenodo paper record

Zenodo gives a DOI at once. It does not put the paper in Google Scholar (see [`google-scholar.md`](google-scholar.md)).

1. A person makes a token with the scopes `deposit:write` and `deposit:actions`. Keep it in a 0600 file outside any repo (see [`accounts-and-traps.md`](accounts-and-traps.md)). Export it as `ZENODO_TOKEN`. Never put it in a command line.
2. Dry run on the sandbox:

   ```sh
   ZENODO_BASE=https://sandbox.zenodo.org/api paper-publish zenodo-draft \
     --pdf paper.pdf --tarball arxiv.tar.gz --meta meta.json
   ```

   The sandbox needs its own account and its own token.
3. Make the real draft. Add `--community SLUG` if a community fits. Zenodo owners accept or decline the request.

   ```sh
   paper-publish zenodo-draft --pdf paper.pdf --tarball arxiv.tar.gz --meta meta.json
   ```

   It prints the draft id and the preview URL. The record is a draft. Nothing is public. A live run on 2026-10-17 worked: create, upload, metadata and preview.
   Name the local files with their final names first. Zenodo keeps the local file name, and the first draft said `paper.pdf`.
4. A person opens the preview and reads it. A person clicks Publish in the Zenodo page. Publish through the web page or through the API. The tool never publishes without both `--publish` and `--i-confirm-permanent`. A published record cannot be deleted, so decide the title first. A draft can be deleted: `DELETE /deposit/depositions/<id>` returned 204 in the live run (the API page lists 201). A withdrawal is an exceptional act that leaves a tombstone page and keeps the DOI (https://about.zenodo.org/policies/).
5. Save the concept id. It is the DOI of all versions. Cite it in the README.

The tool adds the code repo (`code_url`) and the data records (`data_concept_dois`) as related identifiers. Do not also list the repo URL in `related_identifiers` when `code_url` is set: Zenodo then shows it twice. Adding the 23 concept DOIs through `data_concept_dois` made the paper record link every package. A new version of an existing record uses `--new-version-of CONCEPT_ID`. Zenodo accepts `publication-preprint` as a `resource_type` in a related identifier: a public record carried it on 2026-10-16. That closes the open item in [`citation-and-discovery.md`](citation-and-discovery.md) section E3 for the read side. A deposit that writes it is UNVERIFIED.

### 2.2 Software Heritage

Free. No login. It archives the source and gives each repo a SWHID.

```sh
paper-publish swh-save https://github.com/itsryanarmani/benchmark-core https://github.com/itsryanarmani/benchmark-family-paper
```

Each line is `URL`, `status`, `SWHID`. The tool waits when the service says 429. A large repo can time out on the first call. Run the command again: it succeeded on the second try. The anonymous API answered `X-Ratelimit-Limit: 120` on 2026-10-16. The period is UNVERIFIED. Add the SWHID to `CITATION.cff` as an `identifiers` entry with `type: swh` (the CFF schema guide lists that type).

### 2.3 Hugging Face dataset repos

A dataset repo and its card are free. Create them now. The paper page needs the arXiv id, so it waits for section 5. The card format is in [`citation-and-discovery.md`](citation-and-discovery.md) section E5.

## 3. Preprint servers, one by one

Pick ONE server for the paper text. That server is arXiv. Every other server adds a copy, not reach. Research Square says that posting the exact same preprint on several servers "is generally discouraged by major repositories and publishing guidelines" (official support page, 2026-10-16). TMLR and some journals ask you to declare each copy.

Write one form file per server:

```sh
paper-publish packet meta.json --out packet/
```

Each file holds the exact fields for that venue, copied from `meta.json`. `CHECKLIST.md` lists the steps a person does.

### 3.1 arXiv (the main copy)

A person does every click. Read [`arxiv-independent-author.md`](arxiv-independent-author.md) first. It has the steps (F2), the licences (F3), the AI-use note (F4), and the order for this owner (G).

Fields on the arXiv form (https://info.arxiv.org/help/prep.html):

| Field | Value |
|---|---|
| Title, Authors, Abstract | Required. ASCII only. Abstract up to 1920 characters. No TeX in the abstract. |
| Comments | Page and figure counts, the site URL, the AI-use note. |
| Category | `cs.AI` primary. `cs.SE` cross-list (advice in F10). |
| Licence | CC BY 4.0 (irrevocable once chosen). |
| Journal-ref, DOI, Report-no | Leave blank. arXiv assigns the DOI `10.48550/arXiv.<id>`. |
| MSC-class, ACM-class | Skip unless you know the class. |

Upload the TeX source as one `.tar.gz`. Do not upload a PDF built from TeX. Read the compile log. Preview the PDF. Then the author clicks Submit Article. The date stamp is set at that click.

### 3.2 SSRN (optional copy)

Free to upload. Papers by individual authors download free. The licence is chosen at submit (see [`venues.md`](venues.md)). A person logs in and uses "Submit a Paper" on https://www.ssrn.com/.

- The form fields are UNVERIFIED. The SSRN help pages did not load on 2026-10-16.
- The Computer Science Research Network page is UNVERIFIED.
- Google Scholar can take 6 to 9 months or longer to index SSRN (https://www.elsevier.support/ssrn/answer/google-scholar).

### 3.3 Research Square (optional copy)

Free. The steps (https://support.researchsquare.com/support/solutions/articles/6000271843-how-do-i-submit-a-preprint-, checked 2026-10-16):

1. Click Submit a Preprint. Enter the title. Accept the terms. Log in.
2. Upload a `.pdf`, `.docx` or `.doc`.
3. Fill the metadata. Enter the institution. Write "Independent Researcher" if you have none (the page does not say this is accepted: UNVERIFIED).
4. Tick the declarations. A conflict-of-interest statement is required.
5. Click Submit. A pop-up says the preprint posts publicly and permanently. The author clicks "Proceed with my preprint".
6. Staff screen it. Posting takes 24 to 48 hours. You get a DOI.

The CS subject list is UNVERIFIED. Skip this server unless a reason beats the duplicate-copy warning above.

### 3.4 Not eligible

Do not spend time on these. The reasons and sources are in [`free-venues.md`](free-venues.md) (section A2) and [`venues.md`](venues.md).

| Server | Why not |
|---|---|
| SciELO Preprints | Its checklist says the manuscript was not posted on another server first. That conflicts with arXiv. |
| engrXiv | It does not accept computer science without a strong engineering link. |
| Open Research Europe | It needs an EU grant or an author in a listed country. |
| HAL | It is open to academic institutions. An independent author is not named. |
| Papers with Code | The service ended. The domain redirects to Hugging Face. Use the Hugging Face paper page. |
| OSF Preprints (generalist) | New submissions are suspended since 2025-08-25. |
| TechRxiv | Submissions are paused during a platform move. |
| Figshare | The free platform takes data, not papers. |

## 4. Choose ONE peer-reviewed venue

Send the paper to one peer-reviewed venue at a time. A preprint server or an archive is not peer review. Two review venues at once is dual submission. `paper-publish packet` refuses a packet for two review venues unless a person passes `--allow-second-review-venue`.

| Order | Venue | Use it when | Review |
|---|---|---|---|
| 1 | DMLR | A benchmark or dataset paper. Best topic fit. Rolling. No fee. | Single blind. Names stay on the PDF. |
| 2 | TMLR | DMLR declines, or the claims are the main point. Rolling. No fee. | Double blind. The PDF must be anonymous. |
| 3 | JOSS | The software core only (`benchmark-core`), public for more than six months. | Public, not anonymous. |
| 3 | JMLR MLOSS | The software core only. Four pages. The fee is UNVERIFIED. | Not anonymous. |
| 4 | JAIR | A fit exists. The reproducibility checklist is required or the paper is desk rejected. | See the journal page. |

Facts and sources for each row are in [`free-venues.md`](free-venues.md) (section B) and [`venues.md`](venues.md). Both review modes were re-read on 2026-10-16: DMLR "employs a single-blind review process with open reviewing" (https://data.mlr.press/submissions.html). TMLR "uses a double blind review process and submissions must be anonymized" (https://jmlr.org/tmlr/author-guide.html).

**The anonymity difference.** For TMLR, remove the authors, the acknowledgements, and every link that names you. A GitHub URL, a Croissant file and a commit email can name you. The TMLR PDF must not link to a named version of the paper. A person may still post the paper on arXiv at any time, with or without a name. For DMLR, keep the names. DMLR makes accepted papers, reviews and discussions public after the decision.

Wait for the first real-model run before you submit. Both journals judge claims against evidence (see the risk note in `free-venues.md` section B). Template and checklist: [`templates.md`](templates.md), [`checklists.md`](checklists.md).

## 5. After the arXiv id appears

P means a person logs in. A means an agent can work. One PR per repo, each under 500 lines.

1. A: In every `CITATION.cff`, add the `preferred-citation` block with `doi: 10.48550/arXiv.<id>`. The example is in [`citation-and-discovery.md`](citation-and-discovery.md) section E2.
2. A: In every README, update the Cite block (BibTeX, section E4). Replace the placeholder id.
3. A: Update the Hugging Face dataset cards. Put the arXiv abstract URL in each card. The Hub then adds the `arxiv:<id>` tag.
4. A or P: In the Zenodo paper record, add the arXiv DOI as a related identifier. The relation `isIdenticalTo` is in the Zenodo vocabulary (https://developers.zenodo.org/). Edit the record or use `paper-publish zenodo-draft --new-version-of CONCEPT_ID`.
5. P: Open `hf.co/papers/<id>`. Index the paper if needed. Click "claim authorship". An admin checks the claim.
6. P: Create the Google Scholar profile with a personal Google account. Add the paper by title. Turn on "New citations to my articles". See [`google-scholar.md`](google-scholar.md).
7. P: Claim the Semantic Scholar author page and the OpenAlex profile. In ORCID, use "+Add works" and import the arXiv entry. See [`citation-and-discovery.md`](citation-and-discovery.md) section D.
8. A: Check once a day for 12 weeks, read only: the arXiv abstract tags, OpenAlex by DOI, Semantic Scholar by arXiv id, the Hugging Face paper page. Report any gap.
9. P: After a real-model run, post v2 on arXiv (one replace per week at most). Then submit to the venue chosen in section 4.

## 6. Gotchas

- **arXiv endorsement.** A new author needs a personal endorser. Institutional email alone no longer endorses (since 2026-01-21). arXiv staff cannot endorse. The endorser must have papers in the same endorsement domain, submitted between three months and five years ago. The public help page says "the number of papers depends on the particular subject area". The count of 3 in [`accounts-and-traps.md`](accounts-and-traps.md) came from the account flow. It is UNVERIFIED on the public page. The six-character endorsement code is emailed to the author when a submission starts. Whether the code expires is UNVERIFIED: the help page does not say. Ask ONE person who knows your work. Do not mass-email, pay, or post a public call. Source: https://info.arxiv.org/help/endorsement.html.
- **Two submissions per month.** arXiv limits each submitter to 2 submissions per calendar month and 3 active submissions (since 2026-10-01). Put the whole benchmark family in ONE paper. Rejected papers count.
- **One account per service.** arXiv, ORCID and Google Scholar ban a second account for one person. Use a contact alias on the manuscript for each paper. Keep one login per service.
- **Do not solve a CAPTCHA.** The account owner types it. An agent must not.
- **The last click belongs to the author.** Submit, Publish, "Proceed with my preprint", and every agreement box are a person's act. Stop and hand over the packet.
- **A posted draft cannot be unsaid.** Zenodo publish, Research Square posting and an arXiv announcement are permanent or nearly so. Old arXiv versions stay public. Check the preview first.
- **Post Zenodo before arXiv, or relate the DOI.** Zenodo says content that already has an external DOI can have its Zenodo DOI invalidated (https://about.zenodo.org/policies/). The arXiv DOI is probably an external DOI. That reading is UNVERIFIED. Post the Zenodo record first for that reason.
- **Zenodo is not in Google Scholar.** Zenodo says so in its FAQ. A Zenodo DOI helps citation. arXiv and a Scholar profile put the paper in Scholar.
- **Research Square is permanent and slow.** The posting is public and permanent. Screening takes 24 to 48 hours.
- **Two copies, one decision.** A second preprint server is a duplicate copy. Do not post to a server whose rules bar an earlier preprint (SciELO).
- **Benchmark terms.** Some providers forbid publishing benchmark scores in their terms. Cerebras, Together AI and Fireworks are on that list in [`../../paper-experiments/references/cheap-compute.md`](../../paper-experiments/references/cheap-compute.md). Never post their numbers without written permission. Read the current terms first.
- **Free-only models.** Run experiments on `:free` or local models behind `free-only-proxy`. A paid run needs the owner's yes and a dollar cap.
- **Claims match evidence.** If no real-model results exist, the abstract says so. See [`paper-quality.md`](paper-quality.md).
- **Do not print a token.** `paper-publish` reads `ZENODO_TOKEN` from the environment only. It never logs it. Do not paste it into a chat or a PR.

## Stop

Do not submit, publish, pay, accept an agreement, solve a CAPTCHA or send an endorsement request. Hand the owner the packet, the PDF and the unanswered login.
