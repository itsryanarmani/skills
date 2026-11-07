# Citation and discovery

How to make a repo citable (`CITATION.cff`, Zenodo, BibTeX, dataset cards, JSON-LD) and which services index a paper.

Checked 2026-10-16 against the official pages named in each row. `UNVERIFIED` means
the page did not load (403, bot wall, or empty). Do not act on an `UNVERIFIED` cell until a person
opens the page. Re-open the source URL before you act: pages change.

## D. Other discovery and citation services

| Service | Exact free action | Login | Delay | Source | Verified |
|---|---|---|---|---|---|
| Semantic Scholar | It indexes arXiv and other sources by itself ("PubMed, arXiv, and Springer Nature"). There is no submit form. When the paper appears, find your author page and click "Claim Author Page". Add ORCID, affiliation, field and homepage to the claim form. Then use "Edit Author Page" and "Add Papers". | P | Edits up to 24 hours. | https://www.semanticscholar.org/faq and https://www.semanticscholar.org/faq/author-id and https://www.semanticscholar.org/faq/edit-author-page | 2026-10-16 |
| ORCID | Register a free iD ("free of charge"). Add works with "+Add works", then import from Crossref or DataCite. Turn on auto-update for DataCite. | P | Minutes | https://info.orcid.org/researchers/ and https://info.orcid.org/researcher-faq/ | 2026-10-16 (free: opened; menu labels: search snippet, UNVERIFIED) |
| OpenAlex | It ingests Crossref, DataCite, PubMed, HAL and repositories. A work with an arXiv ID joins one work record by that ID. To claim: sign in, open your author page, click "Claim". Linking an ORCID approves the claim at once. Add works by title, DOI or CV. | P | Changes "typically live within about two days". | https://help.openalex.org/how-to/fixing-authors/ and https://help.openalex.org/data/works/ | 2026-10-16 |
| CORE | An agent cannot submit. CORE harvests repositories. It tells authors to deposit in a repository and does not take full texts by email. | none | Hours to weeks | https://core.ac.uk/faq | 2026-10-16 |
| DBLP | UNVERIFIED. Every dblp page returned a bot wall. A search snippet of the FAQ says there is no direct submit route, and arXiv/CoRR preprints are added automatically. Do not plan on dblp for this paper. | none | UNVERIFIED | https://dblp.org/faq/ | UNVERIFIED |
| Crossref DOIs | Only members register content. Individuals are not covered on the page. Skip. | n/a | n/a | https://www.crossref.org/documentation/register-maintain-records/ | 2026-10-16 |
| DataCite DOIs | Zenodo registers DOIs "with DataCite". arXiv also registers DataCite DOIs (prefix `10.48550`) at no cost. Direct DataCite membership for an individual is UNVERIFIED. | n/a | At publish | https://help.zenodo.org/docs/deposit/about-records/ and https://info.arxiv.org/help/doi.html | 2026-10-16 |
| Hugging Face Papers | A paper page appears when a model, dataset or Space card links an arXiv abstract or PDF URL. The Hub adds an `arxiv:<id>` tag. You can also visit `hf.co/papers/<arxiv-id>` to index it. To claim: click your name on the page, click "claim authorship", confirm in settings, and wait for an admin check. | P | Admin check. Time not stated. | https://huggingface.co/docs/hub/en/paper-pages and https://huggingface.co/docs/hub/en/datasets-cards | 2026-10-16 |
| alphaXiv | Paper pages use `alphaxiv.org/abs/<arxiv-id>`. The arXiv abstract page has an "alphaXiv" toggle. A claim process is UNVERIFIED. | P | UNVERIFIED | https://www.alphaxiv.org/ and https://arxiv.org/abs/2609.32390 | 2026-10-16 |
| Papers with Code | Ended. `paperswithcode.com` redirects (302) to Hugging Face Trending Papers. Do not submit there. | none | n/a | https://paperswithcode.com/ | 2026-10-16 |
| arXiv abstract page tabs | The page of a 2026 paper shows toggles for alphaXiv, CatalyzeX, DagsHub, Huggingface, Links to Code, Litmaps, Replicate, Spaces, and Semantic Scholar. It shows no Papers with Code toggle. | none | at announcement | https://arxiv.org/abs/2609.32390 | 2026-10-16 |
| Connected Papers | Free tier is UNVERIFIED (the pricing page loads blank). It is a viewing tool. No author action exists. | n/a | n/a | https://www.connectedpapers.com/pricing | UNVERIFIED |
| Scilit | UNVERIFIED. The site returns 403. Snippets say MDPI runs it and it harvests arXiv. | n/a | UNVERIFIED | https://www.scilit.com/ | UNVERIFIED |
| Dimensions | Free web app "for personal, non-commercial use". A free account can link publications to your ORCID record. No submit step. | P (optional) | n/a | https://www.dimensions.ai/products/free/ | 2026-10-16 |
| Lens.org | Scholarly sources: "Microsoft Academic, PubMed and Crossref", plus Unpaywall. arXiv is not named. No author action found. | n/a | n/a | https://support.lens.org/knowledge-base/scholarly-works-search/ | 2026-10-16 |
| Altmetric | Free tools: a bookmarklet, free badges for individual researchers, a free API for non-commercial research. Which identifiers it tracks is UNVERIFIED. | none | n/a | https://www.altmetric.com/solutions/free-tools/ | 2026-10-16 |
| Internet Archive Scholar | No upload. Use the inclusion form for a journal URL. Wait three months. | none | 3+ months | https://scholar.archive.org/about | 2026-10-16 |
| Software Heritage | "Save Code Now" archives a repo and gives a SWHID. Steps UNVERIFIED. | none | n/a | https://www.softwareheritage.org/save-and-reference-research-software/ | 2026-10-16 |

---

## E. Citation mechanics for the repos

### E1. Present state (measured with the GitHub API, 2026-10-16)

| Item | Result |
|---|---|
| Public `benchmark-*` repos | 24: 22 task-set packages, `benchmark-core`, and `benchmark-family-paper`. The template repository is private. |
| `CITATION.cff` | Missing in all 24. |
| `.zenodo.json` | Missing in all 24. |
| `package.json` fields | `repository`, `homepage`, `bugs`, `keywords`, `license`, `author` are set (checked on `benchmark-sycophancy`). `funding` is empty. |
| `benchmark-family-paper` has no `package.json` | That is fine. |
| Site `private-repo-337e.com` | JSON-LD exists for `Organization` and `WebPage`. No `ScholarlyArticle` or `Dataset` found on the home page. No `citation_*` tags on the home page. |

### E2. CITATION.cff

| Fact | Value | Source | Verified |
|---|---|---|---|
| Spec version | `cff-version: 1.2.0` | https://raw.githubusercontent.com/citation-file-format/citation-file-format/main/schema-guide.md | 2026-10-16 |
| Required top-level keys | `authors`, `cff-version`, `message`, `title` | same | 2026-10-16 |
| `type` values | `software` (default) or `dataset` | same | 2026-10-16 |
| `preferred-citation` | Optional. "A reference to another work that should be cited instead of the software or dataset itself." | same | 2026-10-16 |
| GitHub behaviour | A `CITATION.cff` in the root on the default branch adds a "Cite this repository" link. GitHub supports APA and BibTeX output. | https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files | 2026-10-16 |
| Zenodo subset | Zenodo reads a subset of the schema. | https://help.zenodo.org/docs/github/describe-software/citation-file/ | 2026-10-16 |

Validated example (I checked it against the official 1.2.0 JSON schema with `jsonschema`: no errors). The arXiv ID `2610.00000` is a placeholder. Replace it after announcement.

```yaml
cff-version: 1.2.0
message: "If you use this benchmark, please cite the paper in preferred-citation."
type: software
title: "benchmark-sycophancy"
abstract: "A deterministic benchmark that measures whether an agent keeps a correct answer under user pushback."
authors:
  - family-names: Arab
    given-names: Pooria
    # orcid: "https://orcid.org/0000-0000-0000-0000"
version: 0.2.0
date-released: "2026-10-16"
license: MIT
repository-code: "https://github.com/itsryanarmani/benchmark-sycophancy"
url: "https://private-repo-337e.com/benchmarks/benchmark-sycophancy"
keywords:
  - ai-benchmark
  - llm-evaluation
  - sycophancy
preferred-citation:
  type: article
  authors:
    - family-names: Arab
      given-names: Pooria
  title: "benchmark-core and the AI Benchmark Index: deterministic, reproducible agent benchmarks with four surfaces"
  journal: "arXiv"
  year: 2026
  doi: "10.48550/arXiv.2610.00000"
  url: "https://arxiv.org/abs/2610.00000"
```

Rules:

- Add `orcid` only after the person creates an iD. Do not invent one.
- Use `type: dataset` in a CFF for the Hugging Face dataset card source, if you keep one.
- Use the same `preferred-citation` block in all 24 repos.

### E3. Zenodo GitHub integration

| Step or fact | Detail | Source | Verified |
|---|---|---|---|
| Link GitHub | Link the GitHub account under Zenodo profile settings. A person does this once. | https://help.zenodo.org/docs/github/enable-repository/ | 2026-10-16 |
| Enable a repo | Profile menu, GitHub, sync, switch the repo toggle on, refresh. | same | 2026-10-16 |
| What triggers a DOI | "new releases from the repository will be automatically ingested and archived." Create a GitHub release. Wait. Open the record DOI. | https://help.zenodo.org/docs/github/archive-software/github-upload/ | 2026-10-16 |
| Debug a failure | Open the repo, pick the failed release, open "Errors". Fix the metadata and release again. | same | 2026-10-16 |
| Metadata precedence | If both files exist, Zenodo uses only `.zenodo.json` and ignores `CITATION.cff` completely. | https://help.zenodo.org/docs/github/describe-software/citation-file/ | 2026-10-16 |
| Why `.zenodo.json` | It supports grants, communities, `related_identifiers`, access right, and contributor roles. | https://help.zenodo.org/docs/github/describe-software/zenodo-json/ | 2026-10-16 |
| Version DOI | "a DOI representing the specific version of your record". Each release gets one. | https://support.zenodo.org/help/en-gb/1-upload-deposit/97-what-is-doi-versioning | 2026-10-16 |
| Concept DOI | "The last DOI represents all the versions" of the package. Cite this one in the README. | same | 2026-10-16 |
| DOI registrar | DataCite. | https://help.zenodo.org/docs/deposit/about-records/ | 2026-10-16 |
| Scholar | Zenodo says Scholar does not index it (see C6). | see C6 | 2026-10-16 |

Advice: use `CITATION.cff` only. Skip `.zenodo.json`, so one file serves GitHub and Zenodo. Use `.zenodo.json` only if you need a Zenodo community or a grant. If you add it, copy every field from the CFF, because the CFF is then ignored.

Valid `.zenodo.json` example (JSON parse check passed; Zenodo field names copied from the Zenodo example page):

```json
{
  "creators": [{"name": "Arab, Pooria"}],
  "title": "benchmark-sycophancy",
  "upload_type": "software",
  "license": "mit",
  "access_right": "open",
  "keywords": ["ai-benchmark", "llm-evaluation", "sycophancy"],
  "related_identifiers": [
    {"identifier": "10.48550/arXiv.2610.00000", "relation": "isSupplementTo", "resource_type": "publication-preprint"}
  ]
}
```

I did not check the `resource_type` value `publication-preprint` against a Zenodo list. It is UNVERIFIED.

### E4. BibTeX for the README and dataset cards

Brace balance checked by eye. Not compiled: this host has no TeX. Replace the placeholder ID after announcement.

```bibtex
@misc{arab2026benchmarkcore,
  author        = {Arab, Pooria},
  title         = {benchmark-core and the {AI} Benchmark Index: deterministic,
                   reproducible agent benchmarks with four surfaces},
  year          = {2026},
  eprint        = {2610.00000},
  archivePrefix = {arXiv},
  primaryClass  = {cs.AI},
  doi           = {10.48550/arXiv.2610.00000},
  url           = {https://arxiv.org/abs/2610.00000}
}
```

### E5. Hugging Face dataset card

| Item | Fact | Source | Verified |
|---|---|---|---|
| Card file | The dataset `README.md` is the card. YAML metadata sits at the top between `---` lines. | https://huggingface.co/docs/hub/en/datasets-cards | 2026-10-16 |
| Paper link | A link to an HF paper page or an arXiv abstract or PDF in the card adds the tag `arxiv:<id>`. | same | 2026-10-16 |
| Citation field | There is no YAML `citation` key in the doc excerpt I opened. The official template has a "Citation" section with `citation_bibtex` and `citation_apa` placeholders. Put the BibTeX in that section. | https://raw.githubusercontent.com/huggingface/huggingface_hub/main/src/huggingface_hub/templates/datasetcard_template.md | 2026-10-16 |
| Agent action | The `hf/publish.py` script in `benchmark-family-paper` can add the section and the arXiv link. I did not read that script. | repo `itsryanarmani/benchmark-family-paper` | not read |

### E6. npm `package.json`

| Field | Use | Source | Verified |
|---|---|---|---|
| `repository` | Where the code lives. Already set. | https://docs.npmjs.com/cli/v10/configuring-npm/package-json | 2026-10-16 |
| `homepage` | Project URL. Already set to the index page. | same | 2026-10-16 |
| `bugs` | Issue tracker. Already set. | same | 2026-10-16 |
| `keywords` | Array of strings for `npm search`. Already set. | same | 2026-10-16 |
| `license` | SPDX id. Already `MIT`. | same | 2026-10-16 |
| `funding` | A URL or object that shows in `npm fund`. Add one only if a real funding page exists. | same | 2026-10-16 |

npm has no field for a DOI or a paper. Put the paper URL in the README. Add `"homepage"` only once per package. Do not invent a `citation` key.

### E7. JSON-LD on private-repo-337e.com and Google Dataset Search

| Item | Rule from Google | Source | Verified |
|---|---|---|---|
| Required `Dataset` properties | `name` and `description`. The description is 50 to 5000 characters. | https://developers.google.com/search/docs/appearance/structured-data/dataset | 2026-10-16 |
| Download | `distribution.contentUrl` is required inside `DataDownload`. | same | 2026-10-16 |
| Recommended | `creator`, `license` (use a versioned URL), `identifier`, `sameAs`, `keywords`, `version`, `includedInDataCatalog`, `distribution.encodingFormat`. | same | 2026-10-16 |
| Crawl time | "several days" to find a page. | same | 2026-10-16 |
| Check | Use the Rich Results Test and the Search Console report. Both need a person's Google login for Search Console. | same | 2026-10-16 |

Validated example (JSON parse passed; dataset description is 198 characters). Place it in a `<script type="application/ld+json">` tag. Use one `Dataset` per benchmark page and one `ScholarlyArticle` on `/paper`.

```json
[
  {
    "@context": "https://schema.org",
    "@type": "ScholarlyArticle",
    "@id": "https://private-repo-337e.com/paper#article",
    "name": "benchmark-core and the AI Benchmark Index: deterministic, reproducible agent benchmarks with four surfaces",
    "author": {"@type": "Person", "name": "Pooria Arab"},
    "datePublished": "2026-10-16",
    "identifier": "https://doi.org/10.48550/arXiv.2610.00000",
    "sameAs": "https://arxiv.org/abs/2610.00000",
    "url": "https://private-repo-337e.com/paper",
    "license": "https://creativecommons.org/licenses/by/4.0/",
    "isAccessibleForFree": true
  },
  {
    "@context": "https://schema.org",
    "@type": "Dataset",
    "name": "benchmark-sycophancy task set",
    "description": "Task set, deterministic grader and provenance record for the benchmark-sycophancy package. Each task pushes back on a correct agent answer and the grader checks whether the agent holds its position.",
    "creator": {"@type": "Person", "name": "Pooria Arab"},
    "license": "https://opensource.org/licenses/MIT",
    "url": "https://private-repo-337e.com/benchmarks/benchmark-sycophancy",
    "sameAs": "https://huggingface.co/datasets/pooria/benchmark-sycophancy",
    "keywords": ["ai-benchmark", "llm-evaluation", "sycophancy"],
    "version": "0.2.0",
    "isBasedOn": "https://github.com/itsryanarmani/benchmark-sycophancy",
    "distribution": {
      "@type": "DataDownload",
      "encodingFormat": "application/json",
      "contentUrl": "https://huggingface.co/datasets/pooria/benchmark-sycophancy/resolve/main/data.json"
    }
  }
]
```

The `contentUrl` and the HF dataset name above are examples. An agent must read the real file names from the dataset repo before it ships this. Google's page does not say that Scholar reads JSON-LD. Scholar reads `citation_*` meta tags (section C3). Add both on `/paper`.

---
