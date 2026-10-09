# Workflow map

The agent-facing routing rules live in [paper-workflow](../skills/core/paper-workflow/SKILL.md). This page summarizes them for users.

## Choose scope first

Identify the active manuscript, article type, requested unit, editing permission and available evidence. A paragraph does not require whole-project setup. A diagnosis request does not authorize rewriting. Existing project decisions and explicit venue instructions take precedence over defaults.

## Scientific-to-stylistic order

| Layer | Question | Specialist when needed |
|---|---|---|
| Structure | Do the question, claims and evidence support one another? | `manuscript-optimizer` for research; `review-article-architecture` for Reviews |
| Section prose | Does this section need drafting or substantial rewriting? | `scientific-writing`; `results-section-revision` for stable but fragmented Results |
| Passage logic | Are comparisons, references and reasoning followable? | `write-scientific-manuscript` |
| Posture | Is the manuscript reporting findings in reader-facing language? | `anti-defensive-writing` |
| Sentence style | Is the remaining issue rhythm, punctuation or wording? | `scientific-prose-style` |

Check relevant layers in this order, and edit only layers with observed problems. A layer that is sound does not need a rewrite. A posture edit follows stabilization of its claim. Stop after the requested scope and a focused consistency check are complete.

## Positions

The layers decide what to fix first; the position decides what a fixed section must do. Each
position (Title, Abstract, Introduction, Results, Discussion, Methods, legends, SI) has one contract
in [section-contracts.md](../skills/core/paper-workflow/references/section-contracts.md): its job,
what it depends on, its typical shape and what makes it fail. Positions depend on one another in
this order: figures and evidence → Results → Discussion → Introduction → Abstract → Title. A request
to revise the Abstract stays an Abstract edit, but a claim that rests on an unsettled result stays
out of it, and a changed Results claim is rechecked wherever it is restated. Formats such as
abstract length come from the journal's current guide, not from the contracts. The typical ranges
and method-paper patterns come from 28 Nature Methods, Nature Biotechnology and Nature Communications
method papers; see [section-evidence.md](../skills/core/paper-workflow/references/section-evidence.md).

## Integrity checks

Statistics, citation metadata, live source existence, claim support and availability are distinct. Run those needed for the task, and cover all applicable categories in a comprehensive preflight. An unavailable source or tool is an unchecked category. Necessary limitations, independent-unit n, measurement values, negative results and reproducibility facts survive every style pass.

## Special paths

- **Research article across many sessions:** reconcile current results and decisions; use `manuscript-optimizer` where the argument has drifted. Length does not select the Review route.
- **Review/survey/Perspective:** establish the governing plan with `review-article-architecture`, source alongside drafting, then check plan drift before compression/polish.
- **Figures:** `figure-planner` establishes claims and panel roles. `nature-figure` and `figure-style` produce/check figures when installed with `--figure`; a plan alone is not a rendered or audited figure.
- **Rebuttal:** `paper-reviewer` inventories the original asks, `rebuttal-response` drafts against completed evidence and manuscript edits, and `paper-reviewer` checks coverage. Both are in the recommended set.
- **Reference existence:** `reference-audit-guide` ships live API checkers in `--set all`. A local bibliography check is not a substitute.
- **Conference/presentation/research extensions:** install `--set all` and invoke for the specific task.

## What you receive

A revision returns the revised material first, then a few material changes and unresolved author decisions. A diagnosis gives locations and remedies. Detailed working notes stay outside the manuscript. Do not describe a proposed experiment, pending manuscript edit or unperformed check as completed.

[Task recipes](task-recipes.md) · [Input/output compatibility](compatibility.md) · [Figure checks](figure-workflow.md)
