---
name: paper-workflow
description: >-
  Route general manuscript requests such as improve my paper, revise this draft,
  优化论文, 润色论文 or 投稿前检查. Identify the article type, requested scope, the
  sections in scope and available evidence, then choose the necessary writing or checking steps.
  Also use when one section is named, such as rewrite the Abstract, 改摘要, 写引言 or 讨论怎么写,
  so that the section's contract and its dependencies on other sections apply.
  Go to a specialist directly when the user names one or a narrow job such as a
  citation style. Do not route ordinary
  emails, code documentation or non-manuscript writing through this workflow.
---

# Paper Workflow: Dispatcher

Use this dispatcher when the author has not identified a specific writing task. A request such as `优化一下论文` or `improve my manuscript`
names a goal, not a layer. Manuscript work happens at distinct layers, and editing the wrong layer
first wastes the edit: a paragraph whose scientific role is wrong should never be polished, and a
sentence whose claim is unstable should never be re-punctuated.

Classify the request before editing. Check the relevant layers in scientific-to-stylistic order,
then load and apply only the specialists needed to resolve observed problems. A single specialist
may be sufficient after diagnosis; a general request does not itself require repeated rewriting.

Default assumption: unless a conference venue is named, the manuscript follows the journal-oriented
`Nature`-style path.

## Step 1: Establish the task and classify the input

Identify the active source, article type, requested scope, the positions in scope (Abstract,
Introduction, Results, Methods and so on; see Positions below) and output before choosing a route.
Use supplied context; ask only when an ambiguity would change the work. A request to inspect,
review, diagnose or suggest produces findings, not file edits. A request to revise authorizes
edits within its stated scope. Explicitly frozen decisions and numerical results remain fixed.

Carry forward named protected passages and the requested edit depth. A light-touch request does
not reopen approved Abstract, Introduction or Discussion prose. If a protected passage contains
a material scientific error, report it with a concrete remedy; preserving its text is not a
clean bill of health. Reuse supplied constraints rather than demanding a new state file.

Treat the byline, correspondence and contribution roles as author decisions. Checking initials or
aligning contribution formatting does not authorize adding/removing authors or changing their
roles. Resolve initials against full names and current source; flag an ambiguous mapping rather
than infer an identity or propagate a suspected correction into other metadata.

Work with the material provided. Do not demand project-state files for a paragraph edit.
For whole-paper work, reuse existing results and decision records; create lightweight notes
only when they prevent cross-session drift. If the input is a PDF, determine whether editable
source exists; do not promise Word track changes, PDF layout editing or LaTeX compilation
without a working toolchain. For missing evidence, identify the affected claim and continue
with independent edits. Never fabricate the missing result or citation.

The table gives candidate steps in order, not mandatory rewrite passes.

| Input | Class | Chain |
|---|---|---|
| One sentence or one paragraph | `passage` | `write-scientific-manuscript`, then `anti-defensive-writing` if the passage is hedged, over-caveated or written in an audit, self-critical, developer or commitment voice, then `scientific-prose-style` |
| One section to draft or rewrite in prose, such as the Abstract or the Introduction | `section` | Read that position's entry in `references/section-contracts.md` and check its upstream dependency; `scientific-writing` for needed drafting; passage, posture and sentence specialists only for observed issues |
| A Results section that is scientifically settled but reads figure-by-figure | `results-flow` | `results-section-revision`, `anti-defensive-writing`, then `scientific-prose-style` |
| A whole draft, or no unit named | `manuscript` | `manuscript-optimizer`, with `references/section-contracts.md` as the per-section standard; `scientific-writing` for needed drafting; passage, posture and sentence specialists only for observed issues |
| Reads like an audit report, a rebuttal or a self-critique; hedged, over-caveated or apologetic; a paragraph opens with a limitation; the SI or data statements confess what could not be found; the text names folders, files or build steps, or promises a future release | `posture` | `anti-defensive-writing`, then `scientific-prose-style`. If the claim hierarchy is not yet settled, run `manuscript-optimizer` first: an unnecessary disclaimer and a real scope condition look identical while the claim is still moving |
| A Review, survey, or Perspective | `review-article` | `review-article-architecture` first, then the Review path below |
| A draft carried across many sessions | `long-draft` | Reconcile current source and decisions with `draft-marker-discipline` if markers/state are relevant; research articles use `manuscript-optimizer`, Reviews/surveys/Perspectives use `review-article-architecture`. Length alone never selects the Review route |
| Near submission or resubmission | `preflight` | `submission-audit`, `citation-verifier`, `claim-source-verification`, `stats-reporting-audit`, `data-availability` |
| Reviewer comments exist | `response` | `paper-reviewer` to inventory every ask, `rebuttal-response` to draft and calibrate, then `paper-reviewer` again to grade the draft. `paper-reviewer` and `rebuttal-response` are both in the recommended set |
| A manuscript to referee, or a request to predict what reviewers will attack | `referee` | `paper-reviewer` (recommended set) |
| Figures are the bottleneck | `figure` | `figure-planner`, then `nature-figure` to render, then `figure-style` to check. The last two are the figure stack, installed with `--figure` |
| Equation numbering, float placement, SI table pagination or other LaTeX typesetting | `layout` | `scientific-writing` with `references/latex-layout.md`; use `write-scientific-manuscript` only if paragraph boundaries also need semantic repair. Placement alone does not select the figure-production chain |
| No draft yet, project new or messy | `bootstrap` | `paper-bootstrap` then `nature-portfolio-playbook` |

An explicit mixed request can use the relevant steps from more than one class. Ask one question
only when competing interpretations would change the authorized work; do not ask merely because
numbering, paragraphs and floats need different specialists.

## Step 2: Announce the scope and execute the necessary steps

State the chosen scope and sequence in one short line. For example:

> I will check the claim/evidence structure, revise the affected Results paragraphs,
> and check the changes against the figures and original numbers.

Check the layers in order, but distinguish checking a layer from rewriting it. If a layer is
already sound, preserve it. Do not reopen settled structure during a sentence edit. Apply a
posture edit only after the relevant claim is stable. When a requested comprehensive preflight
cannot check a category, report that category as unchecked and explain what input is missing.

Finish each edit with a focused check of the changed text and its dependent figure references,
comparisons, terminology and citations. Do not repeatedly rewrite stable prose to satisfy a chain.

## Output contract

- Revision: deliver the revised text/file first, then at most 3–5 material changes and any
  unresolved author decisions. A short passage normally needs only the replacement and a brief reason.
- Diagnosis: give prioritized findings with locations, reasons and concrete remedies; stop before edits.
- Preflight: distinguish blocking issues, useful improvements and unchecked categories. Do not
  turn missing tools or unread sources into a clean bill of health.
- Rebuttal: preserve every reviewer ask and original numbering; link replies to actual manuscript
  changes and completed evidence. A proposed experiment is not a completed experiment.
- Never claim an export, render, citation lookup, experiment or file modification was performed
  unless it was performed. Keep detailed process notes outside the manuscript.

## Step 3: Stop rules

Stop or narrow the affected work and explain why when:

- an upstream layer finds a problem that invalidates downstream work, such as a claim the evidence
  does not support. Fix or surface it before polishing;
- the requested scope is complete. `帮我把这句话改短` ends after the passage edit and its local check;
- a later layer would undo a decision the author explicitly approved.

Run a full `preflight` once the draft is stable; if the author requests it earlier, identify instability and check only categories that can be assessed. Auditing unstable text produces
findings that evaporate on the next revision.

Never run `scientific-prose-style` on a drifted Review before the drift audit. Polishing a drifted
draft makes the drift harder to see, not easier.

Never run `anti-defensive-writing` before the claim hierarchy is stable. Until the claim is settled,
an unnecessary disclaimer and a real scope condition look identical, and the pass strips the wrong
one.

## The layers

Use these layers to diagnose problems and preserve dependency order.

1. **Structure**: is there a defensible claim hierarchy and evidence chain?
   `manuscript-optimizer` for research articles, `review-article-architecture` for Reviews.
2. **Prose**: is the section drafted in full paragraphs that carry the argument?
   `scientific-writing`, with `results-section-revision` for late-stage Results architecture.
3. **Passage logic**: is this paragraph followable? Buried topic sentences, missing bridges,
   ambiguous referents, noun chains, incomplete comparisons, coined terminology.
   `write-scientific-manuscript`.
4. **Rhetorical posture**: does the text advance its claim, or negotiate with an imagined critic?
   Audit voice (project process in the paper), defensive voice (arguing with an imagined reviewer),
   self-critical voice (the paper grading itself), developer voice (the repository in the paper),
   commitment voice (promises of a future release), caveats in high-impact positions, paragraphs that
   open with a limitation, reflexive `not X but Y`. `anti-defensive-writing`, which also covers the SI,
   legends and data statements. It runs after the claim hierarchy is settled,
   because before that an unnecessary disclaimer and a real scope condition are indistinguishable:
   the claim they qualify is still moving.
5. **Sentence**: em-dash budget, hedging, sentence rhythm, paragraph openers.
   `scientific-prose-style`, last.

Integrity checks run alongside, not in sequence: `citation-verifier`, `claim-source-verification`,
`stats-reporting-audit`, `draft-marker-discipline`.

Layer 4 has a boundary the other layers do not: **a load-bearing statement stays.** Load-bearing is
decided by what a sentence states, not by which skill added it: the unit of replication and n, no P
values, blinding and exclusions, an access route, the count behind a reporting decision, an
estimator's assumptions, a null result, and any scope condition the Methods needs to stay
reproducible. `anti-defensive-writing` may move such a statement out of a high-impact position, state
it once instead of at every mention, or rewrite it as positive scope, but it must not delete it. A
pass that silently removes one is a reporting failure, not a style improvement. Audit-voice wording
added by an integrity check ("as checked", "could not be identified") is not protected.

## Positions

The layers decide what to fix first. The position decides what a fixed section must do. An
Abstract, an Introduction and a Methods section are held to different standards, and some layers
behave differently in them: a Methods section is almost entirely load-bearing, and an Abstract keeps
effect sizes but not test statistics. [section-contracts.md](references/section-contracts.md) states
each position's job, dependencies, acceptance criteria and owning specialists once. Specialists
apply it and do not restate it. Read the entry for every position in scope before diagnosing it,
and check the edit against the same entry afterwards.

Positions depend on one another:

> figures and evidence → Results → Discussion → Introduction → Abstract → Title

Methods records what was actually done and changes only with the procedure. Three rules follow:

- A request for a downstream position stays narrow. Edit it against the current upstream text, keep
  claims that rest on unsettled results out of it or mark them as pending, and name the dependency
  in the reply.
- After a claim changes upstream, recheck the positions that restate it: the Discussion opening,
  the final Introduction paragraph, the Abstract, the Title and the affected legends. This is a
  focused check, not a rewrite.
- No position claims more than its upstream supports.

Format is not part of a contract. Abstract length and structure, citations in the abstract, title
length and Methods placement come from the target journal's current guide, through
`nature-portfolio-playbook` for Nature Portfolio journals. A generic template, such as a structured
clinical abstract, is never the default.

## Default journal path

Use this as a coverage map over the life of a paper; run only the steps applicable to the current request.

1. `paper-bootstrap`
2. `nature-portfolio-playbook` when venue fit or article type is uncertain
3. Refresh `notes/project_truth.md`, `notes/result_summary.md`, `notes/paper_handoff.md` after any
   experimental, statistical, or figure update
4. `manuscript-optimizer` or `scientific-writing` per the class table, then
   `write-scientific-manuscript` for passage-level clarity
5. `figure-planner`, then `nature-figure` to produce and `figure-style` to check (figure stack, `--figure`)
6. `results-section-revision` when Results is stable but reads jumpy
7. `stats-reporting-audit`
8. `citation-verifier`, then `claim-source-verification`
9. `data-availability`
10. `anti-defensive-writing`, after the integrity checks above have added the statements they require
11. `scientific-prose-style`
12. `submission-audit`; anything it adds is held to rule zero of `anti-defensive-writing`, and that
    skill's detection pass is rerun on the changed passages
13. after external review: `paper-reviewer` to inventory the reports, `rebuttal-response` to draft and
    calibrate, then `paper-reviewer` again to grade the draft

## Review, survey, and Perspective path

A Review is not a short research article. Its failure mode is becoming a different Review, not
overclaiming past its data.

1. `review-article-architecture` to establish the governing plan document first
2. `nature-portfolio-playbook` for venue and article-type fit
3. `draft-marker-discipline` to set up the marker system before drafting starts
4. `scientific-writing`, sourcing in step with the prose
5. `citation-verifier`, then `claim-source-verification`
6. `figure-planner`, then `nature-figure` and `figure-style` (figure stack, `--figure`)
7. `review-article-architecture` drift audit, before any compression pass
8. `draft-marker-discipline` to measure length and triage what remains open
9. `anti-defensive-writing`
10. `scientific-prose-style`, last
11. `submission-audit`

Run step 7 before step 10, never after.

## Choosing between adjacent skills

- `scientific-writing` when a section mostly needs drafting or rewriting in prose, or when a
  citation style or reporting guideline is named. `manuscript-optimizer` when the story, evidence
  chain, figure logic, or terminology may be unstable. `write-scientific-manuscript` when the
  science is settled but the passage is hard to follow.
- `results-section-revision` when the remaining problem is local Results architecture rather than
  claim selection.
- `anti-defensive-writing` when the text is accurate but reads like an audit report, a rebuttal or a
  self-critique: it reports project process instead of findings, keeps saying what it does not
  claim, opens paragraphs with caveats, confesses what could not be found, explains itself to a
  critic who is not in the room, documents the repository, or promises what does not exist yet. It covers the SI, legends and data statements as well as the main
  text. `scientific-prose-style` when the remaining problem is
  punctuation, rhythm, em-dash budget, or hedge calibration inside a single sentence. They stack, in
  that order, because removing defensive scaffolding rewrites the paragraph openers and sentence
  boundaries the punctuation pass then settles. Neither one may overrule an integrity audit; see the
  layer-4 boundary above. A Methods section is mostly load-bearing reproducibility detail, and the
  edit is usually to convert a negation into positive scope and to state it once instead of at every
  mention.
- `citation-verifier` when the bibliography as an artifact is the problem: duplicate keys, missing
  fields, DOI syntax, cited-but-undefined. `claim-source-verification` when the question is whether
  a source supports the sentence citing it. They stack, in that order. A clean bibliography audit
  says nothing about claim support: in one measured run, 55 of 139 proposed sources were rejected,
  none of them fabricated.
- `reference-audit-guide` when references must be checked against live scholarly APIs rather than
  inspected locally. Optional set, installed with `--set all`. It ships runnable verification scripts and is the only stage that catches a
  fabricated citation carrying a well-formed DOI.
- `review-article-architecture` for a Review, survey, or Perspective, or whenever a piece written
  across many sessions may no longer match its brief. `manuscript-optimizer` for research articles.
- `draft-marker-discipline` before a batch pass over open markers, before quoting a manuscript's
  length, before removing superseded material, and before scripting the same edit across many files.
- `figure-planner` to decide what each figure argues, then `nature-figure` to render it, then
  `figure-style` to check correctness and legibility before export. The last two are the figure
  stack; if they are not installed, `figure-planner` still produces the panel plan and the author
  renders it themselves.
- `conference-paper-writing` only when a conference venue is explicitly named. Optional set,
  installed with `--set all`.
- `paper-reviewer` when the question is what the reviewer asked or whether the reviewer would accept
  the answer. `rebuttal-response` when the question is what the authors may claim and how the letter,
  manuscript, and Supplementary Information stay consistent. They stack, in that order, and
  `paper-reviewer` runs a second time at the end to grade the draft. `rebuttal-response` is in the
  recommended set; `paper-reviewer` is in the recommended set. A manuscript
  change made in reply to a reviewer follows rule zero of `anti-defensive-writing`: a result, a
  precise definition or a narrowed claim, not an added caveat.

## Working principle

Do not polish sections written from stale memory. After experimental, statistical, or figure
updates, refresh `notes/project_truth.md`, `notes/result_summary.md`, and `notes/paper_handoff.md`
before attempting heavy revision.

## Common mistakes

- editing a general manuscript request without first identifying the actual problem layer
- treating the coverage map as a requirement to rewrite every section on every request
- polishing sentences before the claim hierarchy is stable
- writing the Abstract or Title from a Results claim that is still moving, or failing to recheck them
  after it moves
- importing an abstract format, such as a structured clinical abstract, that the target journal does
  not ask for
- holding every section to one generic standard instead of its own contract
- running a defensive-writing pass before the claim hierarchy is stable, which strips real scope
  conditions along with the disclaimers
- letting a posture edit delete scientifically necessary limitations, numerical results or reproducibility facts
- running a submission audit on a draft still being restructured
- polishing a Review before its drift audit
- using conference-style writing skills by default for journal manuscripts
- rewriting the manuscript from experiment memory instead of a current `result_summary.md`
- editing figure legends late without rechecking the Results text
- leaving repository choice, accession IDs, or source-data coverage until the portal is open
- treating citation formatting as the same thing as citation verification
- treating a clean bibliography as evidence that the sources support the claims
- writing a response letter before deciding the underlying manuscript edits
- answering a reviewer report without first listing every ask and sub-ask in the reviewer's own words
- renumbering, reordering, or grouping reviewer comments by theme, which makes coverage impossible to
  check at a glance
- rewriting whole paragraphs when the author flagged two sentences
