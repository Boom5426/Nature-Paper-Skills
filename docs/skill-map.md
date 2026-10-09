# Skill Map

Recommended: all 17 Core skills, the Venue skill and `paper-reviewer` (19 total). Add both Figure skills with `--figure`; install all 27 with `--set all`. Start with [task recipes](task-recipes.md) if you do not need the complete catalog.

## Core

- `paper-workflow`: top-level router; owns the section contracts (what each section must do, its dependencies and typical shape) and the paper sample behind them
- `paper-bootstrap`: initialize a paper project and source of truth
- `scientific-writing`: draft and section-level rewriting
- `write-scientific-manuscript`: clarity and logic diagnosis for a passage that is correct but hard to follow
- `manuscript-optimizer`: structural revision and evidence-chain repair
- `results-section-revision`: late-stage Results narrative repair
- `figure-planner`: figure claim design and legend sync
- `citation-verifier`: bibliography hygiene (duplicate keys, required fields, DOI syntax, cited-vs-defined, BibTeX toolchain hardening)
- `claim-source-verification`: adversarial claim-to-evidence checking; does a cited source actually support the sentence
- `review-article-architecture`: Review, survey, and Perspective structure; governing plan document, drift audit, thesis-as-macro, display-item budget
- `draft-marker-discipline`: in-source draft markers, triage by resolution route, prose word counts, safe archival, assertion-guarded scripted edits
- `data-availability`: data-sharing statements, repository planning, and source-data coverage
- `submission-audit`: pre-submission or pre-resubmission QA
- `rebuttal-response`: author-side reviewer response workflow, claim calibration, and final letter audit
- `stats-reporting-audit`: author-side statistical-reporting audit (independent-unit `n`, replication, multiple comparisons, figure-legend statistics)
- `anti-defensive-writing`: rhetorical posture (audit, defensive, self-critical, developer-facing and commitment writing in the main text, SI, legends, table notes and data statements; caveats in high-impact positions; paragraphs opening with a limitation). Runs after the relevant claim is stable; preserve scientifically necessary scope, numbers, reporting requirements and reproducibility facts. Apply only when the task needs this layer
- `scientific-prose-style`: sentence-level prose linting (em-dash budget, hedging, sentence rhythm, paragraph openers)

## Venue

- `nature-portfolio-playbook`: choose among `Nature`, `Nature Methods`, and `Nature Biotechnology`; run Nature Portfolio preflight

## Figure

- `nature-figure`: submission-grade Python or R figure production workflow, plus an optional OpenRouter AI-schematic route (needs a plotting backend)
- `figure-style`: publication-grade figure correctness and legibility checklist with portable matplotlib helpers

## Research

- `paper-analyzer`: deep analysis of one paper
- `academic-researcher`: broad literature and methodology support
- `results-analysis`: convert experiment outputs into paper-ready findings

## Review

- `paper-reviewer`: both sides of the referee exchange. Writes referee reports on methodology, evidence,
  reproducibility, and reporting; splits a received report into every ask and sub-ask in the reviewer's
  own numbering; and grades a drafted reply for one-to-one coverage and plainness

## Optional

- `reference-audit-guide`: principle-oriented citation reference
- `conference-paper-writing`: only for conference-first workflows
- `academic-presentations`: turn papers into decks or talks
