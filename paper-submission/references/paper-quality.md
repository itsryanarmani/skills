# Paper quality guide for a benchmark paper

How to make a benchmark or evaluation paper strong, not only acceptable. It extends [`checklists.md`](checklists.md) and [`venues.md`](venues.md) and does not repeat them.

Checked 2026-10-16. A row marked verified means the original page or PDF was opened on that date. `UNVERIFIED` means it could not be opened. "Advice (mine)" marks a judgement, not a source claim.

The worked example is a family of 22 open benchmark packages with deterministic graders and no real-model results. Replace those facts with yours.

## 0. Five findings that change the paper

1. NeurIPS E&D 2026 has a contribution type for tools and infrastructure. Reviewers ask "Is it robust and well-engineered, not just a demo?" Frame the paper as infrastructure plus validity evidence.
2. The agentic checklist ABC asks for an oracle solver (T.9) and trivial-agent baselines (R.13). Your scripted good and bad policies are exactly that. Make them a headline result with intervals.
3. Bean et al. find that only 53.4% of 445 benchmarks justify construct validity. Add one construct paragraph and table row per benchmark.
4. NeurIPS wants a validated Croissant file with Core and RAI fields for every dataset. Non-compliance means desk rejection. That is 22 files.
5. Small item counts break the usual error bars. Use paired differences and exact or Bayesian intervals, not mean plus or minus standard error.

---

## A. What reviewers reward and punish

### A1. NeurIPS Evaluations & Datasets (E&D), 2026 cycle

| Fact (quoted words in quotes) | Source | Verified |
|---|---|---|
| Track name is "NeurIPS 2026 Evaluations & Datasets Track". Full papers were due 2026-05-06. Notices went out 2026-09-24. The next cycle is not on the page. | https://neurips.cc/Conferences/2026/CallForEvaluationsDatasets | 2026-10-16 |
| "evaluation becomes an object of scientific study in its own right". "Submissions need not introduce a new model or outperform prior work." | same | 2026-10-16 |
| "We aim for an equally stringent review as the main conference track". | same | 2026-10-16 |
| Quality: "Is the submission technically sound, and are the claims well-supported by empirical, analytical, or conceptual arguments?" | https://neurips.cc/Conferences/2026/EvaluationsDatasetsReviewerGuidelines | 2026-10-16 |
| Clarity: "Is the submission clearly written, well-organized, and detailed enough to enable reproducibility?" | same | 2026-10-16 |
| Significance: "Are the results impactful for the community?" | same | 2026-10-16 |
| Originality: "Providing novel insights, exposing failure modes, evaluating existing methods, or framing new metrics is equally valuable." | same | 2026-10-16 |
| Benchmark Design: clarity test is "Could another team re-run the benchmark from this paper?" Significance test is "Does it change how we measure progress in this area?" "Beating a baseline is not required." | same | 2026-10-16 |
| Benchmark Design quality: "Evaluate the rigor of task design, item selection, and evaluation setup." Also "Assess whether benchmark saturation or overfitting is adequately addressed." | same (fetch summary; the first line is a close paraphrase) | 2026-10-16 |
| Infrastructure papers: "Is it robust and well-engineered, not just a demo?" "In most cases, code release is mandatory". "No code = reject unless a convincing justification is provided". | same | 2026-10-16 |
| Audit papers: "Claims must be independently verifiable." "Negative results are valuable when rigorously supported." | same | 2026-10-16 |
| Dataset mandatory checks: "Is a valid Croissant file present?" "Is the RAI metadata complete (biases, limits, intended use, sensitive info)". "Is the dataset accessible without PI request". "Check the automated reviewer report". | same | 2026-10-16 |
| "authors should be rewarded rather than punished for being up front about the limitations of their work". "answering 'no' to some questions is typically not grounds for rejection". | same | 2026-10-16 |
| Default review is double-blind. A dataset that cannot be anonymised may choose single-blind. Anonymise hosting accounts. No leak "(including in the Croissant file)". | https://neurips.cc/Conferences/2026/EvaluationsDatasetsFAQ | 2026-10-16 |
| "You should submit a Croissant file for every dataset (and check whether they are all valid)." | same | 2026-10-16 |
| "Training datasets" without a shown "value in improving (downstream) evaluations" are "not in scope". | same | 2026-10-16 |
| The 2025 track blog lists missing metadata in first submissions: licence 11.9%, description 4.9%, URL 3.5%. 84% of accepted papers introduced new datasets. Over 80% used HF, Kaggle, Dataverse or OpenML. | https://blog.neurips.cc/2025/12/05/neurips-datasets-benchmarks-track-from-art-to-science-in-ai-evaluations/ | 2026-10-16 |

### A2. NeurIPS paper checklist (the 16 topics)

Source: https://neurips.cc/public/guides/PaperChecklist. Verified 2026-10-16.
Topics: claims, limitations, theory, reproducibility, open access to data and code, experimental setting, statistical significance, compute, code of ethics, broader impacts, safeguards, licences, assets, crowdsourcing, IRB, LLM usage.
Two quoted rules matter here:
- "It should be clear whether the error bar is the standard deviation or the standard error of the mean."
- "The factors of variability that the error bars are capturing should be clearly stated."
For new assets: "Researchers should communicate the details of the dataset/code/model as part of their submissions via structured templates."

### A3. Other venues

| Venue | What it says that touches benchmarks | Source | Verified |
|---|---|---|---|
| TMLR | Accept if "claims made in the submission supported by accurate and convincing evidence" (most important) and if some of the audience would be interested. It avoids the words "significant", "impactful", "novel". Authors may close a claim-evidence gap by narrowing the claim. | https://jmlr.org/tmlr/acceptance-criteria.html | 2026-10-16 |
| DMLR | "Submissions introducing or incorporating a dataset and/or benchmark are required to include comprehensive documentation." Needs a reviewer URL, a responsibility statement with licence confirmation, and a "Hosting, licensing, and maintenance plan". No page limit. Template violation "may result in desk rejection". | https://data.mlr.press/submissions.html | 2026-10-16 |
| ACL Rolling Review | Reject example the guide calls unfortunate: "the paper is mostly a description of the corpus and its collection and contains little scientific contribution". Evaluation papers: "it should be clear why this sample was selected". Flaws named: baselines "not sufficiently well-tuned", a sample that "does not represent the population". "SOTA results are neither necessary nor sufficient for a scientific contribution." | https://aclrollingreview.org/reviewerguidelines | 2026-10-16 |
| ICLR 2027 | "Not all work needs to compete on an established leaderboard". "a lack of state-of-the-art results does not by itself constitute grounds for rejection." Reviewers ask "Does the paper support the claims?" | https://iclr.cc/Conferences/2027/ReviewerGuidelines | 2026-10-16 |
| ICML 2026 | Soundness: "Are claims well supported". "are the experiments well-designed?" Reject example: "technical flaws, weak evaluation, inadequate reproducibility". The page has no benchmark-specific text. | https://icml.cc/Conferences/2026/ReviewerInstructions | 2026-10-16 |
| COLM 2026 | Scope lists "benchmarks (static and dynamic), simulation environments". The review guide wants "evaluation metrics that are known or shown to measure what they claim to". Weakness "cannot be an immediate reason to reject". 9 page limit. | https://colm.cc/Conferences/2026/ReviewGuidelines and https://colm.cc/Conferences/2026/CallForPapers | 2026-10-16 |

### A4. Dataset documentation expectations

| Item | Fact | Source | Verified |
|---|---|---|---|
| Datasheets for Datasets | Gebru, Morgenstern, Vecchione, Vaughan, Wallach, Daume III, Crawford. arXiv 2018-03-23, v8 2021-12-01. CACM, December 2021. Seven sections: Motivation, Composition, Collection process, Preprocessing/cleaning/labeling, Uses, Distribution, Maintenance. | https://arxiv.org/abs/1803.09010 and the PDF | 2026-10-16 |
| Data Cards | Pushkarna, Zaldivar, Kjartansson. FAccT 2022 submission. DMLR lists it as an accepted framework. AgentDojo ships one as its appendix F. | https://arxiv.org/abs/2204.01075 | 2026-10-16 |
| Croissant | Akhtar et al. (31 authors), NeurIPS 2024 Datasets and Benchmarks. Spec 1.0, 2024-03-01. Core properties: `name`, `description`, `license`, `url`, `distribution`, `creator`, `datePublished`, `conformsTo`. `version` uses MAJOR.MINOR.PATCH. `sha256` on each file is "strongly" recommended. | https://arxiv.org/abs/2403.19546 and https://docs.mlcommons.org/croissant/docs/croissant-spec.html | 2026-10-16 |
| Croissant RAI | Spec 1.0, 2024-03-06. Fields include `rai:dataCollection`, `rai:dataPreprocessingProtocol`, `rai:dataAnnotationProtocol`, `rai:annotationsPerItem`, `rai:dataBiases`, `rai:dataLimitations`, `rai:dataUseCases`, `rai:personalSensitiveInformation`, `rai:dataSocialImpact`, `rai:dataReleaseMaintenancePlan`. The spec text has inconsistent property names, so copy names from the validator, not the prose. | https://docs.mlcommons.org/croissant/docs/croissant-rai-spec.html | 2026-10-16 |
| NeurIPS hosting | "Croissant file with both Core and (minimal) Responsible AI metadata fields". RAI "must be included in the Croissant file". "Datasets should have a clear license". The licence "should be included in the Croissant file". Hosts: Dataverse, Kaggle, Hugging Face, OpenML. The page does not require a DOI. Accepted datasets must be public by camera-ready. | https://neurips.cc/Conferences/2026/EvaluationsDatasetsHosting | 2026-10-16 |
| NeurIPS RAI note | Missing RAI metadata "will be flagged during review". Posted 2026-05-04. | https://blog.neurips.cc/?p=1527 | 2026-10-16 |
| Hugging Face card | README.md is the card. YAML holds `license`, `language`, `pretty_name`, `tags`, `task_categories`. A link to an arXiv abs page adds an `arxiv:<ID>` tag. | https://huggingface.co/docs/hub/datasets-cards | 2026-10-16 |

Advice (mine): write one datasheet per dataset, then generate the Croissant RAI fields from the same source text. One source of truth prevents drift between the two.

---

## B. Benchmark quality frameworks (self-score)

Titles, authors and venues below come from arXiv abs pages or proceedings pages opened on 2026-10-16.

| Framework | Real citation | What it asks you to show |
|---|---|---|
| BetterBench | Reuel, Hardy, Smith, Lamparth, Hardy, Kochenderfer. "BetterBench: Assessing AI Benchmarks, Uncovering Issues, and Establishing Best Practices". arXiv 2411.12990 (2024-11-20). NeurIPS 2024 D&B, Spotlight. https://arxiv.org/abs/2411.12990 | Four stages with criteria: design, implementation, documentation, maintenance. Scored 0, 5, 10 or 15. Stage mean of 10 or more is "reasonably good". Count caveat: arXiv v1 says 46 practices and 24 benchmarks. The NeurIPS page says 40 and 25 (https://proceedings.neurips.cc/paper_files/paper/2024/hash/26889e8359e7ef8a7f5d77457364ca55-Abstract.html). Cite one version. |
| Construct validity review | Bean et al. (42 authors). "Measuring what Matters: Construct Validity in Large Language Model Benchmarks". arXiv 2511.04703 (2025-11-03). NeurIPS 2025 D&B. https://arxiv.org/abs/2511.04703 | Eight recommendations. See B2. |
| Agentic Benchmark Checklist (ABC) | Zhu et al. (25 authors, Kang last). arXiv 2507.02825, v5 2025-08-07. NeurIPS 2025 D&B title is "...Best Practices in Building Rigorous Agentic Benchmarks". https://arxiv.org/abs/2507.02825 and https://proceedings.neurips.cc/paper_files/paper/2025/hash/f316275b44ee2de533102913828a8107-Abstract-Datasets_and_Benchmarks_Track.html | Task validity, outcome validity, reporting. See B3. |
| Error bars | Miller. "Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations". arXiv 2411.00640 (2024-11-01). No venue listed. https://arxiv.org/abs/2411.00640 | Five recommendations. See B4. |
| Small-n intervals | Bowyer, Aitchison, Ivanova. "Position: Don't Use the CLT in LLM Evals With Fewer Than a Few Hundred Datapoints". arXiv 2503.01747. ICML 2025 spotlight position paper. https://arxiv.org/abs/2503.01747 | CLT error bars "usually dramatically underestimate uncertainty" on small sets. Use frequentist or Bayesian alternatives. Library: `bayes_evals`. |
| Reproducible evals | Biderman, Schoelkopf, Sutawika, Gao et al. "Lessons from the Trenches on Reproducible Evaluation of Language Models". arXiv 2405.14782, v3 2026-05-31. No venue listed. https://arxiv.org/abs/2405.14782 | Appendix D checklist: share exact prompts, do not copy results from other papers, provide model outputs, do qualitative analysis, test significance. |
| Agent benchmark critique | Kapoor, Stroebl, Siegel, Nadgir, Narayanan. "AI Agents That Matter". arXiv 2407.01502 (2024-07-01). The arXiv page lists no venue. A secondary index says TMLR 2025 (UNVERIFIED). https://arxiv.org/abs/2407.01502 | Report cost with accuracy. Keep "appropriate holdouts" by generality level. Standardise evaluation. Abstract: "many agent benchmarks have inadequate holdout sets, and sometimes none at all." |
| Meta-review | Eriksson et al. "Can We Trust AI Benchmarks? An Interdisciplinary Review of Current Issues in AI Evaluation". arXiv 2502.06559. arXiv comment says "Under review as conference paper". AIES 2025 is UNVERIFIED on arXiv. https://arxiv.org/abs/2502.06559 | About 100 studies. Issues: dataset bias, weak documentation, contamination, signal versus noise, construct validity, gaming. |
| Saturation | Akhtar, Reuel et al. "When AI Benchmarks Plateau: A Systematic Study of Benchmark Saturation". ICML 2026, PMLR 306, pp. 1602-1629. https://proceedings.mlr.press/v306/akhtar26a.html | 60 benchmarks, 14 properties. "nearly half" saturate. "resilience to saturation is impacted by expert-curation, not by public test data". |
| Saturation map | Ott et al. "Mapping global dynamics of benchmark creation and saturation in artificial intelligence". arXiv 2203.04592. Nature Communications 13:6793 (2022). https://arxiv.org/abs/2203.04592 | 3,765 benchmarks. Many saturate fast. Many are little used. |
| Contamination survey | Xu, Guan, Greene, Kechadi. "Benchmark Data Contamination of Large Language Models: A Survey". arXiv 2406.04244 (2024-06-06). No venue listed. https://arxiv.org/abs/2406.04244 | Defines benchmark data contamination and alternatives to static benchmarks. |
| Reporting standards | Kapoor et al. REFORMS. Science Advances 2024, DOI 10.1126/sciadv.adk3452. 32 items, 8 sections. https://reforms.cs.princeton.edu/ | Written for ML-based science. Useful for the "study design" parts of a paper. |
| Reproducibility program | Pineau et al. JMLR 22(164), 2021. https://jmlr.org/papers/v22/20-303.html | Code policy, challenge, checklist. |

"Benchmarks are not..." (your wording): I could not find a paper with that title. UNVERIFIED. Bean et al. is the closest match.
Contamination or saturation papers about deterministic, generated tasks: I found none. Advice (mine): say why contamination is limited here (fresh seeded instances, public task code) and measure it where you can.

### B1. BetterBench self-score (Verified 2026-10-16 from the arXiv v1 HTML text)

- [ ] Design: goals and scope stated. Domain experts involved. Differences from related benchmarks stated.
- [ ] Design: interpretable metrics. Floor, ceiling, random and human levels reported.
- [ ] Design: validated automatic evaluation.
- [ ] Implementation: working eval code. A script that replicates the first results.
- [ ] Implementation: API and local model support. A training-on-test-set check.
- [ ] Documentation: construction, collection, metrics, significance. Limitations and normative assumptions. Licence.
- [ ] Documentation: requirements file, quick start, code structure.
- [ ] Maintenance: feedback channel. Named contact. Retirement statement.

### B2. Construct validity checklist (Bean et al., Section "recommendations", HTML v1)

1. Define the phenomenon. Give scope. Split sub-components.
2. Measure the phenomenon and only the phenomenon. Validate output parsing.
3. Build a representative dataset. Use a sampling strategy. Test known sensitivities.
4. State limits of reusing datasets. Say what you changed and why.
5. Prepare for contamination. Keep a held-out set.
6. Use statistical methods to compare models. Report sample size and uncertainty.
7. Do an error analysis. Check failures against confounders.
8. Justify construct validity against real use and against other benchmarks.

Field rates to quote (445 benchmarks): defined phenomenon 78.2%. Statistical tests or uncertainty 16.0%. Construct validity justified 53.4%. Human baseline 32.4%. Exact-match scoring 81.3%.

### B3. ABC items that fit deterministic graders (HTML v5)

- T.5 isolate the agent from ground truth. T.6 freeze the environment. T.7 and T.8 verify annotations and setup. T.9 "Provide an automatic oracle solver". T.10 inspect pilot outliers.
- O.b.3 prevent success by guessing. O.g.1 to O.g.3 cover all valid end states and make trivial changes fail.
- R.1 and R.2 open data and harness. R.3 and R.4 contamination measures. R.5 and R.6 capability and construct validity.
- R.7 to R.9 document, then show qualitatively and quantitatively how limits affect results.
- R.10 significance. R.11 interpretation guide. R.12 and R.13 baselines, "such as trivial agents".

### B4. Statistics recipe (Miller, HTML v1)

- Rec 1: standard error of the mean. Binary score: sqrt(p(1-p)/n).
- Rec 2: clustered standard errors when items come in groups. Up to about 3 times the naive value.
- Rec 3: resample answers to cut variance.
- Rec 4: compare two systems with "question-level paired differences".
- Rec 5: power analysis for the number of items.
- Advice (mine): per benchmark n may be under a few hundred. Use Bowyer et al. intervals. Report whether each interval is over items or over runs.
- tau-bench defines pass^k, the chance that all k trials succeed. Use it when a policy is stochastic. https://arxiv.org/abs/2406.12045 (2026-10-16).

---

## C. Section-by-section outline of a strong benchmark paper

Exemplars are in C2. Read "Evidence" as what the exemplars show, not as a rule.

| Section | Holds | Figure or table | Evidence |
|---|---|---|---|
| Abstract | Problem, artifact, 3 numbers, one honest limit ("no real-model leaderboard") | none | arXiv policy text in `arxiv-independent-author.md`5 |
| 1 Introduction | Gap, claim, contributions list | Fig 1 teaser: one task through the system to a score | SWE-bench Fig 1, tau-bench Fig 1 |
| 2 Related work | What each prior suite lacks, in a table | Table: feature matrix vs prior suites | BetterBench "differences from related benchmarks" |
| 3 Design and construct | Phenomenon definition per benchmark, scope, exclusions | Table: benchmark, construct, task source, grader type, n | Bean rec 1, 3, 8 |
| 4 System | Engine, four surfaces, determinism | System diagram. Table: same task, same score on all four surfaces | NeurIPS "robust and well-engineered, not just a demo" |
| 5 Tasks | Generation, difficulty, coverage | 3 to 4 task examples. Coverage heatmap | SWE-bench Fig 2, Fig 3 |
| 6 Graders | Decision flow, edge cases, false pass and false fail rules | Grader flow diagram. Table of grader checks | ABC O.* items; tau-bench state comparison |
| 7 Validation | Scripted good and bad policies. Oracle solver. Trivial agents | Score-separation plot with intervals per benchmark | ABC T.9, R.13 |
| 8 Independent review | Who reviewed, how, defects found, fixed, left open | Defect-class bar chart. Table of open items | ABC T.7, T.10; WebArena double annotation |
| 9 Reliability | Repeat-run hashes, seeds, surface parity, runtime and cost | Table: N repeats, identical outputs, wall time | Miller rec 3; Lessons from the Trenches |
| 10 Contamination and saturation | Seeded fresh instances, held-out split, headroom | Table: split, seed, public or private | Bean rec 5; NeurIPS saturation question |
| 11 Error analysis | Failure modes of the bad policies | Breakdown figure with percentages | MMLU-Pro 5.3; tau-bench 5.2 |
| 12 Limitations | What the paper does not show | Short table: claim, evidence, gap | HELM sections 10 and 11; GPQA section 6 |
| 13 Ethics and impact | Misuse, licences, no human subjects statement | none | NeurIPS checklist items 9 to 15 |
| 14 Reproducibility | One command, versions, hashes, hardware, logs | Table of artifacts with DOIs and checksums | NeurIPS Clarity question; Croissant `sha256` |
| Appendix | Datasheets, Croissant link, full tables, prompts, review log | Data cards per dataset | AgentDojo appendix F |

### C1. What is fixed in the field, and what you can honestly claim

Fixed (sources: ABC R.12, BetterBench design stage, Bean rec 7, ARR R1):
- Readers expect baselines, a floor and a ceiling, and an error analysis.
- Readers expect real-model results to show a benchmark separates systems.

Not required (NeurIPS reviewer guide, 2026-10-16): "Beating a baseline is not required." "Submissions need not introduce a new model or outperform prior work."

What a no-model-results paper can claim honestly (Advice (mine), grounded in the sources above):
- The graders are correct on known cases. Show oracle and trivial policies with intervals.
- The engine is deterministic and portable. Show repeat-run hashes and four-surface parity.
- Independent review found and fixed N defects in M classes. Show the log.
- The artifacts are open, versioned and documented.
Do not claim:
- That the suite measures model capability.
- That the suite is hard, saturated, or discriminating among real models.
- That scripted policies stand in for models.
Say: "Results on real models are future work. We publish the protocol and invite replication."
Option (mine): a small pilot on 2 to 3 real models for one benchmark would remove the most likely reviewer objection. Label it a pilot.

### C2. Eight exemplars (PDFs opened and read on 2026-10-16)

| Paper | Venue and source | What makes it work |
|---|---|---|
| SWE-bench | ICLR 2024. https://arxiv.org/abs/2310.06770 | Fig 1 shows the whole pipeline. Execution tests: at least one fail-to-pass test and a median of 51 other tests per task. Table 7 splits tasks before and after 2023. Short limits, ethics and reproducibility statements. |
| tau-bench | arXiv 2406.12045; page lists no venue. https://arxiv.org/abs/2406.12045 | Replaces human judges with a database state comparison. Adds pass^k for consistency. Error analysis: 115 trajectories, 40 failed, 4 traced to instruction typos. Admits curation bias from tuning on gpt-4-turbo. |
| WebArena | arXiv 2307.13854; page lists no venue. https://arxiv.org/abs/2307.13854 | Human baseline 78.24% against 14.41% for the best agent. Unachievable tasks test false claims. Double annotation with a third tie-breaker. |
| AgentDojo | arXiv 2406.13352; page lists no venue. https://arxiv.org/abs/2406.13352 | Separate utility and security metrics. Ground-truth call sequences are run to check they pass. Ablation on attacker knowledge. Pareto plot. Data card in appendix. v3 comment lists a fixed bug. |
| GPQA | arXiv 2311.12022; page lists no venue. https://arxiv.org/abs/2311.12022 | Four-stage expert and non-expert validation. Bonuses reward objective and hard items. Limits name small size (448) and low statistical power. |
| MMLU-Pro | NeurIPS 2024 D&B Spotlight. https://arxiv.org/abs/2406.01574 | Two review rounds. 24 prompt styles show lower sensitivity. Error analysis of 120 GPT-4o failures with percentages. Direct comparison with MMLU. |
| HELM | TMLR 2023. https://arxiv.org/abs/2211.09110 | A taxonomy, then a section "What is missing" and a three-part limitations section. Coverage of core scenarios rises from 18% to 96%. |
| BFCL | ICML 2025, PMLR 267, pp. 48371-48392. https://proceedings.mlr.press/v267/patil25a.html | Scalable AST-based grader and abstention tests. I read only the abstract page. Dataset size and human validation are not on that page. |

Infrastructure notes:
- Inspect (UK AISI and Meridian Labs) has no paper. Its site gives a BibTeX entry for a software release and the attribution "AI Security Institute, UK. 2024." Task = dataset + solver + scorer. https://inspect.aisi.org.uk/ (2026-10-16).
- BIG-bench: TMLR, 450 authors, 204 tasks, human expert raters as baseline. https://arxiv.org/abs/2206.04615 (2026-10-16). The text of the paper was not opened. Not used as a structure exemplar.
- lm-eval: see "Lessons from the Trenches" in section B. The 2023 lm-eval harness paper itself: UNVERIFIED.

---

## D. Writing quality for science

| Rule | Source | Verified |
|---|---|---|
| One unit of text, one point. "Each unit of discourse, no matter what the size, is expected to serve a single function, to make a single point." | Gopen and Swan, American Scientist 78(6), 1990, pp. 550-558. Excerpts at https://wstomv.win.tue.nl/quotes/science-of-scientific-writing.html. The original page returned 503, so the original is UNVERIFIED. | 2026-10-16 |
| Put old information first, new information last. "readers naturally emphasize the material that arrives at the end of a sentence." | same | 2026-10-16 |
| Keep subject and verb close. "Readers expect a grammatical subject to be followed immediately by the verb." | same | 2026-10-16 |
| Tell one story, name your contributions, put readers first. The page says there are "seven simple, concrete suggestions". It does not list them. The list is UNVERIFIED. | https://www.microsoft.com/en-us/research/academic-program/write-great-research-paper/ (Peyton Jones) | 2026-10-16 |
| Use active voice. "make clear who's performing the action." | https://developers.google.com/style/highlights | 2026-10-16 |
| "Use present tense for statements that describe general behavior that's not associated with a particular time." | https://developers.google.com/style/tense | 2026-10-16 |
| Numerals for 10 and up. Always numerals for technical quantities. A zero before decimals below one. "%" with no space. | https://developers.google.com/style/numbers | 2026-10-16 |

Rules for this paper (Advice (mine)):
- Claim first. Every paragraph opens with its result. Evidence follows.
- Every number has a unit, an n, and an interval. Say what the interval covers (items or runs).
- Define each term once, at first use. Keep a glossary table in the appendix. Do not rename a term.
- Use past tense for what you did. Use present tense for what the artifact does.
- Do not write "novel", "robust", "comprehensive" or "state-of-the-art" without a number beside it.
- Hedge with a scope, not with "may" or "could". Write "on 22 benchmarks, 1 scripted policy" instead.
- Keep sentences under 25 words. Break long noun strings.
- Google's guide says to use "you" instead of "we". That rule is for documentation. A paper uses "we" or an impersonal subject. Keep one choice.
- Google's guide says to use a hyphen for ranges. In LaTeX, write "10 to 20" and skip the question.

### D1. The humanizer pass

- Run the `humanizer` skill on the abstract, introduction, captions, limitations and README text. The skill is referenced in itsryanarmani/skills (`geo-aeo`, `marketing-site`, `repo-standards`) but is not stored there (git tree checked 2026-10-16).
- After the pass, diff the text. Every number, interval, citation key and defined term must survive.
- Reject edits that remove a hedge which carries scope. Reject edits that add rhythm tricks, lists of three, or praise words.
- Do not run it on code, BibTeX, tables of results or commit messages.

### D2. Why not ASD-STE100 for the paper

- What it is: "designed to enhance the readability and consistency of technical documentation" in aerospace, defence and manufacturing. Issue 9 came out 2025-01-15. Sources: https://www.asd-europe.org/news-media/news-events/news/simplified-technical-english-asd-ste100-issue-9 and https://www.tcworld.info/e-magazine/column/asd-ste100-issue-9-setting-a-standard-for-technical-documentation (2026-10-16).
- tcworld: "originally developed for the aerospace and defense industry". The official site https://asd-ste100.org/ returned 403 on 2026-10-16, so the formal scope clause and any "maintenance" wording are UNVERIFIED.
- Advice (mine): STE is a controlled language with an approved dictionary, built for procedures. A paper needs terms such as "construct validity" and "Wilson interval". It also needs scoped hedges and numbers with intervals. A fixed dictionary does not fit those.
- Use instead: short sentences, plain words, and a definition for every term you keep. Keep your ASD-STE100 habit for the README, the CLI help and the reproduction steps. Those are procedures.

---

## E. Figures and charts

| Figure | Takeaway the caption states | Data source | Notes |
|---|---|---|---|
| E1 System diagram (TikZ) | One engine, four surfaces, one score path | hand-drawn, labels from package names | Keep to 8 boxes. Number the arrows. |
| E2 Score separation, scripted good vs bad, per benchmark | "Good policies score above X, bad below Y on all 22" | CSV written by the repo's run script | Wilson or Bayesian interval per bar. Same y-axis range everywhere. Mark any overlap. |
| E3 Defect-class bar chart | "N defects in M classes, K fixed before release" | review log in the repo | Count by class and by severity. Show open items. |
| E4 Coverage or difficulty heatmap | Which task attributes each benchmark covers | task metadata | Sequential, colour-blind-safe map. Print the cell value. |
| E5 Grader decision flow | How a run becomes pass or fail | the grader code | One flow for the shared engine. Mark where the oracle and trivial cases enter. |
| E6 Cost and time table | Runtime per surface | run logs | A table is enough. |

Rules:
- Vector PDF only. Fonts embedded. No screenshots of charts. arXiv accepts PDF, PNG, JPG for PDF-mode LaTeX (https://info.arxiv.org/help/submit_tex.html, 2026-10-16).
- Colour-blind-safe palette. Okabe and Ito, "Color Universal Design (CUD)" (https://jfly.uni-koeln.de/color/, 2026-10-16). Wong, Nature Methods 8(6):441, 2011, doi:10.1038/nmeth.1618 popularised it. I could not open that column (redirect to a login page). UNVERIFIED.
- Hex codes (secondary source only, UNVERIFIED at the original): #E69F00, #56B4E9, #009E73, #F0E442, #0072B2, #D55E00, #CC79A7, #000000. Also encode with pattern or marker, not colour alone.
- Readable at column width. Use 8 pt minimum text after scaling. Test by printing the PDF at 100%.
- The caption states the takeaway, then the n, then what the bars mean. Rougier, Droettboom and Bourne, "Ten Simple Rules for Better Figures", PLOS Comput Biol 2014: rule 4 is "Captions Are Not Optional". Rule 7 is "Do Not Mislead the Reader". https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003833 (2026-10-16).
- Data comes from the repo. A script writes `results/*.csv`. The figure reads the CSV. No typed numbers. Commit the script and the CSV hash.
- Build in LaTeX with TikZ and pgfplots so a plain `tectonic main.tex` works.
- Dataviz skill: not in itsryanarmani/skills (git tree checked 2026-10-16). The Claude Code host lists a `dataviz` skill. Use it for design choices, then re-implement in pgfplots. Advice (mine).

Tested on this Mac, 2026-10-16: Tectonic 0.17.0 built a grouped bar chart with CSV input, asymmetric error bars, Okabe-Ito colours and a hatch pattern. Output: 7.4 KiB vector PDF, fonts embedded, no raster images. One trap: `pattern=` needs `\usetikzlibrary{patterns}` or the build halts.

```latex
\usepackage{pgfplots}\pgfplotsset{compat=1.17}\usetikzlibrary{patterns}
\definecolor{okblue}{HTML}{0072B2}
\addplot[fill=okblue, error bars/.cd, y dir=both, y explicit]
  table[x=bench, y=good, y error plus=good_ep, y error minus=good_em, col sep=comma] {scores.csv};
```

---

## F. Credibility moves for an independent author

| Move | Why it counts | Source | Verified |
|---|---|---|---|
| Public artifacts with versions and checksums | Croissant carries `version` (MAJOR.MINOR.PATCH) and `sha256`. DOI mechanics: see `citation-and-discovery.md`. | https://docs.mlcommons.org/croissant/docs/croissant-spec.html | 2026-10-16 |
| One-command reproduction | "Could another team re-run the benchmark from this paper?" ABC R.1, R.2 ask for open data and harness. | NeurIPS reviewer guide; https://arxiv.org/abs/2507.02825 | 2026-10-16 |
| Share raw outputs and logs | "Always provide model outputs." Others can recompute scores and test significance. | https://arxiv.org/abs/2405.14782 (Appendix D) | 2026-10-16 |
| Independent review, described exactly | Say who or what reviewed, the prompts or method, the defects, and the fixes. If agents reviewed, say so. arXiv asks authors to report significant AI tool use (see `arxiv-independent-author.md`4). Advice (mine): publish the review log. | https://info.arxiv.org/help/moderation/index.html (see `arxiv-independent-author.md`) | 2026-10-16 |
| Pre-registered claims | State hypotheses and the real-model protocol before you run it. Preregistration questions exist for resource papers. | van Miltenburg, van der Lee, Krahmer. "Preregistering NLP Research". NAACL 2021. https://arxiv.org/abs/2103.06944 | 2026-10-16 |
| Honest limitations | "rewarded rather than punished". COLM: "weakness in some aspects cannot be an immediate reason to reject a paper". | NeurIPS and COLM pages in A | 2026-10-16 |
| Public issue tracker, named contact, feedback channel | BetterBench maintenance criteria: feedback channel, named contact, retirement statement. | https://arxiv.org/html/2411.12990v1 | 2026-10-16 |
| Errata policy and versioned fixes | AgentDojo's arXiv v3 comment reads "Updated version after fixing a bug in the Llama implementation and updating the travel suite". Copy that habit. Keep a CHANGELOG and tag each fix. | https://arxiv.org/abs/2406.13352 | 2026-10-16 |
| Invite third-party replication | NeurIPS has a contribution type for reproduction and stress-testing of evaluations. Ask for it by name in the README and paper. | NeurIPS reviewer guide | 2026-10-16 |
| Living assessment | BetterBench keeps a "living repository of benchmark assessments". Score your own suite with it and publish the table. | https://arxiv.org/abs/2411.12990 | 2026-10-16 |

Do not do: cite your own repos to inflate counts. Do not post fake reviews or stars. Do not claim a review is independent when the reviewer is a tool you configured. Do not claim a leaderboard you do not have.

---

## G. Pre-submission self-review

### G1. Twenty-six yes/no items

Claims
1. Does every sentence in the abstract match a table or figure?
2. Does the abstract say there are no real-model results?
3. Is each contribution testable by a reader?
Construct and design
4. Does each benchmark have a one-line construct definition?
5. Is scope and what is excluded stated for each?
6. Is the task source stated, with sampling or generation method?
7. Is a floor and a ceiling reported for each?
Graders and validation
8. Is there an oracle solver per benchmark that scores at the ceiling?
9. Are trivial or scripted-bad policies reported with intervals?
10. Does the grader flow handle guess, empty output and negation cases?
11. Was the grader checked by someone other than the author, with the log public?
Statistics
12. Does each interval name what it covers (items, runs, seeds)?
13. Are comparisons paired where the same items are used?
14. Are small-n intervals exact or Bayesian, not mean plus or minus SE?
Reliability and contamination
15. Are repeat-run outputs identical, with hashes shown?
16. Do the four surfaces give the same score for the same task?
17. Is the contamination stance stated (seeds, held-out split, public tasks)?
Artifacts
18. Does a Croissant file with Core and RAI fields exist and validate for each dataset?
19. Is the licence in the Croissant file and on the HF card?
20. Does one command rebuild the paper and the figures?
Writing and ethics
21. Does every figure caption state a takeaway?
22. Is every term defined once, and used the same way after?
23. Did the humanizer pass keep all numbers and hedges?
24. Is there a limitations section with a claim, evidence, gap table?
25. Is AI assistance disclosed where the venue or arXiv asks?
26. Does the anonymous PDF and its links hide the author, including the Croissant file?

### G2. Mock-reviewer prompt (author's own draft, run in your own session)

NeurIPS asks real reviewers not to paste submissions into hosted LLMs (https://neurips.cc/Conferences/2026/EvaluationsDatasetsReviewerGuidelines, 2026-10-16). This is for your own draft only.

```text
You are a reviewer for NeurIPS Evaluations & Datasets. Contribution types:
Benchmark Design; Evaluation Tools, Frameworks and Infrastructure; Dataset Documentation.
Score Quality, Clarity, Significance, Originality from 1 to 4. Cite a quote for each score.
Quality: technically sound, claims supported? Rigor of task design, item selection, setup.
Clarity: could another team re-run the benchmark from this paper?
Significance: does it change how we measure progress?
Originality: new insight, failure modes, metrics, or tools count equally.
Mandatory checks: valid Croissant with RAI, access without request, code runnable,
anonymised. For infrastructure: "robust and well-engineered, not just a demo".
Also apply: BetterBench stages, Bean's 8 construct-validity items, ABC T/O/R items.
Output: Strengths; Weaknesses; 5 likeliest reasons to reject, each with a fix;
questions for authors; list of claims the evidence does not support; Accept/Reject.
Do not reward length. Do not penalise lack of real-model baselines unless a claim needs them.
```

### G3. Ten common rejection reasons for benchmark papers

| # | Reason | Source | Verified |
|---|---|---|---|
| 1 | No runnable code and no convincing justification | "No code = reject unless a convincing justification is provided" (NeurIPS E&D reviewer guide) | 2026-10-16 |
| 2 | Missing or invalid Croissant or RAI metadata | "Non-compliance justifies the desk rejection" (NeurIPS E&D CFP) | 2026-10-16 |
| 3 | Data gated behind a personal request | "accessible without PI request" is a mandatory check (reviewer guide) | 2026-10-16 |
| 4 | Construct validity not justified | Only 53.4% of 445 benchmarks justify it (Bean et al.) | 2026-10-16 |
| 5 | No uncertainty or significance | Only 16.0% use statistical tests (Bean et al.). BetterBench and ARR R5 ask for it | 2026-10-16 |
| 6 | Grader flaws inflate or deflate scores | Up to 100% relative error. SWE-bench Verified "insufficient test cases", tau-bench "counts empty responses as successful" (ABC abstract) | 2026-10-16 |
| 7 | Saturation, overfitting or contamination ignored | "Assess whether benchmark saturation or overfitting is adequately addressed" (reviewer guide). Nearly half of 60 benchmarks saturate (Akhtar et al.) | 2026-10-16 |
| 8 | Mostly a description of the data | "mostly a description of the corpus ... little scientific contribution" (ARR guide) | 2026-10-16 |
| 9 | Weak baselines or an unrepresentative sample | ARR R1 and R2; ABC R.12 and R.13 | 2026-10-16 |
| 10 | Claims exceed evidence, or format and anonymity breaks | TMLR criterion 1. NeurIPS: violations "subject to desk rejection". DMLR: template failure "may result in desk rejection" | 2026-10-16 |

Sources for 10: https://jmlr.org/tmlr/acceptance-criteria.html, https://neurips.cc/Conferences/2026/EvaluationsDatasetsFAQ, https://data.mlr.press/submissions.html.
Note: NeurIPS does not publish a ranked list of rejection reasons. The list above is my synthesis of official criteria and survey rates. The track blog says rejection reasons were "not discussed" (https://blog.neurips.cc/2025/12/05/neurips-datasets-benchmarks-track-from-art-to-science-in-ai-evaluations/, 2026-10-16).

---

## H. Open items and caveats

- UNVERIFIED: ASD-STE100 formal scope clause (site returned 403). Gopen and Swan original (503). Wong 2011 column (login redirect). Peyton Jones seven suggestions (page lists none). Okabe-Ito hex codes at the primary source. AI Agents That Matter venue. Eriksson et al. venue. The BFCL dataset size. BIG-bench and lm-eval 2023 paper text. COLM 2026 review form fields.
- The SWE-bench Verified blog returned 403. I rely on the ABC abstract for the "insufficient test cases" claim.
- BetterBench counts differ by version (46 and 24 against 40 and 25). Check before you quote.
- Venue dates change. Re-open the CFP before you plan. `references/venues.md` holds deadlines.
