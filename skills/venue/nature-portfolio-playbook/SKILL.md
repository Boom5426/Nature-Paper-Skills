---
name: nature-portfolio-playbook
description: Use when choosing among Nature, Nature Methods, or Nature Biotechnology, or when preparing a Nature Portfolio life-science manuscript for venue fit, article-type framing, and policy-aware pre-submission checks.
---

# Nature Portfolio Playbook

## Overview

Use this skill when the venue decision itself is still live, or when a manuscript already targets `Nature`, `Nature Methods`, or `Nature Biotechnology` and needs venue-specific framing before a heavy revision pass.

This skill is about fit and policy. It does not replace `scientific-writing`, `manuscript-optimizer`, or `submission-audit`.

## When To Use

Use this skill when:
- the user asks whether a story fits `Nature`, `Nature Methods`, or `Nature Biotechnology`
- the paper has a `Nature`-style tone but the actual venue is undecided
- the contribution could be framed as an `Article`, `Resource`, `Analysis`, or short-format methods report
- a manuscript is close to submission and needs a Nature Portfolio-specific preflight

Do not use this skill when:
- the task is generic sentence-level editing
- the venue is a conference or a non-Nature journal
- the manuscript structure itself is still unstable and needs `manuscript-optimizer` first

## Venue Routing

### Flagship `Nature`

Default to `Nature` only when the paper makes a broad conceptual advance that matters outside the immediate specialty and can be explained to non-specialists without heavy field-specific scaffolding.

Use these framing defaults:
- prioritize broad readership over specialist density
- keep title and abstract low-jargon
- preserve the non-specialist-friendly summary paragraph expectation
- if fit is uncertain, explicitly test whether the broad-readership case is real before optimizing prose too far

### `Nature Methods`

Prefer `Nature Methods` when the central contribution is a method, assay, platform, computational approach, or resource whose main claim is enabling power.

Before calling a story `Nature Methods`-fit, check that the manuscript can support all of these:
- a clear technical advance over available approaches
- validation and benchmarking against credible baselines or alternatives
- enough detail or protocol access for reproducibility
- demonstrated general utility, not just one narrow showcase
- a compelling biological or biomedical application that shows why the method matters

### `Nature Biotechnology`

Prefer `Nature Biotechnology` when the paper's value is not just technical novelty but biotechnology significance: enabling capability, translational relevance, engineering depth, platform utility, or community-scale resource value.

Before calling a story `Nature Biotechnology`-fit, check that the manuscript can make legible:
- why the advance matters for biotechnology or medicine, not just for one specialist benchmark
- why the story is substantial enough for a full article rather than a narrower methods report
- whether the paper is truly an `Article` or would be better framed as a `Resource`

## Article-Type Check

Do this early. Do not treat article type as formatting cleanup.

- `Article`: full research story with multiple linked claims and a substantial evidence chain
- `Resource`: community-useful dataset, platform, atlas, database, or screening asset whose lasting value is broad reuse
- `Analysis`: integrative or comparative analytical study when the core contribution is the analytical insight rather than a new experimental method
- short-format method/report categories: use only when the story is tighter, more self-contained, and the journal explicitly supports that format

If the manuscript keeps oscillating between `method paper` and `resource paper`, resolve that before rewriting the abstract or Results.

## Format Check

The section contracts in `paper-workflow` (`references/section-contracts.md`) define what each
section must do. This skill supplies the format the venue imposes on them. Before drafting or
revising front matter, read the target journal's current formatting guide and note its version or
access date in the project notes. Check:

- abstract or summary paragraph: length, single paragraph or structured, whether citations are
  allowed, and any prescribed sequence (the `Nature` summary paragraph is written for readers in
  other disciplines and has its own order)
- title: length and character limits, and whether abbreviations are allowed
- main text: word limit, heading rules, and whether Results and Discussion may be combined
- Methods: placement, length, and which details move to Supplementary Information
- display items: number of main figures and tables, and Extended Data rules

Do not carry limits over from memory, from another journal or from a secondary summary; published
summaries of these limits disagree with one another. If the current guide cannot be read, report
the format as unchecked.

## Nature Portfolio Preflight

Run this before calling a draft submission-ready:

1. Reporting standards
   - confirm whether a reporting summary will be required
   - make sure the manuscript and supplement already contain the information that summary will demand
2. Data and code availability
   - check that repository names, accession IDs, download links, and access restrictions are ready to disclose
   - do not wait until after acceptance to figure out the data/code statement
3. Protocol and reproducibility readiness
   - for methods papers, ensure the usable protocol path is clear: supplement, protocol repository, or public method record
4. Image integrity and raw data
   - ensure unprocessed source images and raw blot/gel material can be produced if requested
   - remove any figure-preparation habit that could look like selective enhancement
5. AI and attribution
   - Nature Portfolio asks for a Methods statement when generative AI helped write the manuscript;
     AI-assisted copy editing alone need not be declared
   - keep it to two sentences scoped to actual use, neither wider nor narrower: the tools and what
     they were used for, then the authors' review and responsibility
   - images made with generative AI are not accepted; an AI-drafted schematic is redrawn by hand or
     in code before submission
6. Related-manuscript and preprint disclosures
   - disclose preprints, overlapping submissions, related manuscripts, and conference-proceedings history when relevant

## Working Rule

Use this decision order:

1. choose audience and venue family
2. choose article type
3. check whether the evidence package matches the venue promise
4. only then optimize framing and prose

## Official Source Pointers

Keep these Nature Portfolio pages as the primary references:
- `Nature` formatting guide
- `Nature` editorial criteria and processes
- `Nature Methods` aims, content, and editorial-policies pages
- `Nature Biotechnology` aims, content, and editorial-policies pages
- Nature Portfolio policies on reporting standards, image integrity, AI, and preprints/conference proceedings
