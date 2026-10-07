---
name: submission-audit
description: Use when a manuscript is close to submission or resubmission and you need a preflight audit for claim support, figure-panel coverage, legend sync, methods references, terminology stability, and venue-facing risks.
---

# Submission Audit

## Overview

Use this skill for late-stage manuscript QA. It is narrower than `manuscript-optimizer`: do not use it to redesign a paper from scratch. Use it when the structure mostly exists and the main task is to catch the failures that survive normal revision cycles.

The core rule is simple: never treat a clean-looking manuscript as submission-ready until the front half, figures, legends, methods, supplement, and venue expectations have been checked against each other.

Use the helper script when you want a fast local pass over figure citations:

```bash
python ~/.agents/skills/submission-audit/scripts/check_figure_refs.py path/to/manuscript.md
# Claude Code (global install): replace ~/.agents/skills with ~/.claude/skills
# Claude Code (project-local install): replace ~/.agents/skills with .claude/skills
```

## When To Use

Use this skill when:
- The draft is near submission, resubmission, or internal circulation
- Figures and legends are mostly finalized
- The paper needs a last pass for overclaim, missing references, or cross-section drift
- A revision round compressed the prose and may have dropped supporting detail
- The supplement exists and may no longer match the main text

Do not use this skill for:
- Early brainstorming
- Initial section drafting
- Citation discovery from scratch
- Heavy structural rewrites that belong in `manuscript-optimizer`

## Audit Order

1. Front-half alignment
   - check title, abstract, introduction, and discussion against the actual Results
   - flag any claim stronger than the downstream evidence
2. Figure and legend coverage
   - verify that every main-figure panel and supplementary panel cited in the paper actually exists
   - verify that panel letters, metrics, datasets, and numbers agree across figure, legend, and main text
3. Methods and supplement anchoring
   - check that methods are cited where needed from Results
   - check that supplementary figures, tables, and notes are referenced precisely enough to be usable
4. Terminology and metrics
   - enforce one canonical name per concept
   - check abbreviations, metric naming, domain-shift labels, cohort names, and model names
5. Risk pass
   - overclaim
   - evidence gaps
   - unsupported mechanism language
   - venue-specific style drift
   - Statistical analysis declares only statistics the paper reports (see `stats-reporting-audit`)
   - voice: audit, defensive or self-critical writing in the main text, SI, legends and data
     statements (run the `anti-defensive-writing` detection pass)
6. Nature Portfolio preflight when relevant
   - reporting-summary readiness
   - data and code availability statements
   - accession IDs, repositories, and disclosure of sharing restrictions
   - image-integrity and raw-data readiness
   - end matter: competing interests; author contributions whose initials match the byline; a
     generative-AI statement in the Methods scoped to actual use, with no AI-generated images; code
     availability consistent with the released repository
   - preprint, related-manuscript, and conference-proceedings disclosure

   Initials are checked against full names, not treated as unique identifiers. A missing or ambiguous
   contribution mapping is a finding for the authors; it is not authorization to remove a byline
   entry, change correspondence or assign a contribution role.
7. Reviewer-side rejection pass
   - contribution sufficiency
   - writing clarity and reproducibility
   - empirical strength
   - evaluation completeness
   - design or framework soundness

   A finding from this pass is fixed with evidence, a precise definition or a narrower claim, never
   with an added caveat. Anything this audit adds to the manuscript is held to rule zero of
   `anti-defensive-writing`, because this audit runs after the posture pass.

## Required Checks

- Does every substantive abstract claim map to a figure, table, or supplement item?
- Does every Results subsection cite the correct panel range?
- Does every figure legend still reflect the current plot content?
- Are `Methods` cross-references present where interpretation depends on setup or metric definition?
- Is the supplement indexed precisely enough, including panel letters when needed?
- Are strong causal or mechanism words used only where direct evidence exists?
- Are title, abstract, and discussion consistent about the paper's actual contribution type?
- If the target is `Nature Portfolio`, are the reporting-summary inputs, data/code statements, image-integrity materials, and disclosure items actually ready rather than merely planned?
- If a submission form or portal draft already exists, do the title, abstract, keywords, availability statements, and related metadata still match the manuscript exactly?
- Has the paper been pressure-tested against the main rejection dimensions: insufficient contribution, weak clarity, weak empirical effect, incomplete evaluation, and questionable design?

For a supplied LaTeX manuscript with typesetting in scope, use `scientific-writing`'s
`references/latex-layout.md` to check the numbered formulas, figure/caption placement, table parts
and paragraph continuity in the rendered PDF. A navigation-only paragraph is assessed by function;
a short scientific finding may be valid. Check the chosen numbering convention and existing labels,
not a blanket requirement to number every display. Apply template, venue and project-specific
placement rules to the relevant deliverable; separate figure legends or a genuinely long table
can be intentional. If compilation or visual inspection is unavailable, identify it as unchecked.

## Finding Format

Report findings in this order:
- High: submission-blocking or claim-distorting issues
- Medium: credibility or reader-friction issues
- Low: consistency and polish issues

Each finding should include:
- exact file reference
- what is wrong
- why it matters
- the minimum safe fix

If no major problems exist, say that explicitly and then list only the residual risks or final checks still worth doing.

## Common Failure Modes

- Abstract promise stronger than Results support
- Figure panel mentioned in text but not actually indexed or explained
- Legend still describing an old version of the plot
- Supplementary figure cited at whole-figure level when the argument depends on one panel
- Metric names drifting between sections
- Discussion slipping into mechanism-level language not earned by the evidence
- Nature Portfolio submission blocked late by missing accession IDs, undeclared sharing restrictions, undisclosed AI use, or missing raw image support
- Submission-form title or abstract drifting away from the latest manuscript
- The manuscript reading cleanly on the surface while still failing a reviewer-style contribution or evaluation check

## Output Standard

End the audit with:
- a one-sentence readiness assessment
- the top remaining risk
- the next highest-leverage fix before submission
