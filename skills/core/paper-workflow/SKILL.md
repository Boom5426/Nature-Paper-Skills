---
name: paper-workflow
description: >-
  Entry point for any manuscript request that does not name a specific skill. Load this FIRST
  whenever the ask is general, then run the chain it prescribes. Covers optimize my paper, improve
  the manuscript, polish this draft, make this better, clean it up, help with my paper, review my
  writing, get this ready to submit, work on the paper, and the Chinese equivalents 优化论文,
  改论文, 润色论文, 帮我看看论文, 论文写作, 学术写作, 把论文弄好, 论文修改, 投稿前检查.
  Also decides which skill applies and how to sequence manuscript work from project setup through
  submission and rebuttal, including the separate path for a Review, survey, or Perspective.
  A general manuscript request is never served well by one skill alone; this file decides which
  chain to run.
---

# Paper Workflow: Dispatcher

This is the entry point, not a menu. A request such as `优化一下论文` or `improve my manuscript`
names a goal, not a layer. Manuscript work happens at distinct layers, and editing the wrong layer
first wastes the edit: a paragraph whose scientific role is wrong should never be polished, and a
sentence whose claim is unstable should never be re-punctuated.

**Do not answer a general manuscript request by loading a single specialist skill.** Classify the
request, then run the whole chain for that class.

Default assumption: unless a conference venue is named, the manuscript follows the journal-oriented
`Nature`-style path.

## Step 1: Classify by what was actually handed over

| Input | Class | Chain |
|---|---|---|
| One sentence or one paragraph | `passage` | `write-scientific-manuscript` then `scientific-prose-style` |
| One section to draft or rewrite in prose | `section` | `scientific-writing`, `write-scientific-manuscript`, then `scientific-prose-style` |
| A Results section that is scientifically settled but reads figure-by-figure | `results-flow` | `results-section-revision` then `scientific-prose-style` |
| A whole draft, or no unit named | `manuscript` | `manuscript-optimizer`, `scientific-writing`, `write-scientific-manuscript`, then `scientific-prose-style` |
| A Review, survey, or Perspective | `review-article` | `review-article-architecture` first, then the Review path below |
| A long draft carried across many sessions | `long-draft` | `draft-marker-discipline` then `review-article-architecture` drift audit |
| Near submission or resubmission | `preflight` | `submission-audit`, `citation-verifier`, `claim-source-verification`, `stats-reporting-audit`, `data-availability` |
| Reviewer comments exist | `response` | `paper-reviewer` to inventory every ask, `rebuttal-response` to draft and calibrate, then `paper-reviewer` again to grade the draft. `paper-reviewer` is not in the default recommended set; install it with `--set all` |
| A manuscript to referee, or a request to predict what reviewers will attack | `referee` | `paper-reviewer`, installed with `--set all` |
| Figures are the bottleneck | `figure` | `figure-planner`, then `nature-figure` to render, then `figure-style` to check. The last two are the figure stack, installed with `--figure` |
| No draft yet, project new or messy | `bootstrap` | `paper-bootstrap` then `nature-portfolio-playbook` |

When two classes with different chains both fit, ask one question. That is the one case worth a
clarifying question; guessing wastes more time than asking.

## Step 2: Announce the chain, then run it in order

State the chain in one line before starting, so the author can redirect early:

> Running the `manuscript` chain: structure (`manuscript-optimizer`), prose (`scientific-writing`),
> passage logic (`write-scientific-manuscript`), then sentence pass (`scientific-prose-style`).

Load each skill in sequence and apply it. Do not skip a link because the previous one already
improved the text. Each layer catches a different defect class, and a later layer cannot see the
defect an earlier one owns.

## Step 3: Stop rules

Stop the chain and report why when:

- an upstream layer finds a problem that invalidates downstream work, such as a claim the evidence
  does not support. Fix or surface it before polishing;
- the request was narrow. `帮我把这句话改短` is a `passage` job, not a licence to restructure the
  paper;
- a later layer would undo a decision the author explicitly approved.

Never run `preflight` on a draft still in `manuscript` class. Auditing unstable text produces
findings that evaporate on the next revision.

Never run `scientific-prose-style` on a drifted Review before the drift audit. Polishing a drifted
draft makes the drift harder to see, not easier.

## The layers

Every skill sits at one layer. This is why the chains are ordered.

1. **Structure**: is there a defensible claim hierarchy and evidence chain?
   `manuscript-optimizer` for research articles, `review-article-architecture` for Reviews.
2. **Prose**: is the section drafted in full paragraphs that carry the argument?
   `scientific-writing`, with `results-section-revision` for late-stage Results architecture.
3. **Passage logic**: is this paragraph followable? Buried topic sentences, missing bridges,
   ambiguous referents, noun chains, incomplete comparisons, coined terminology.
   `write-scientific-manuscript`.
4. **Sentence**: em-dash budget, hedging, sentence rhythm, paragraph openers.
   `scientific-prose-style`, last.

Integrity checks run alongside, not in sequence: `citation-verifier`, `claim-source-verification`,
`stats-reporting-audit`, `draft-marker-discipline`.

## Default journal path

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
10. `scientific-prose-style`
11. `submission-audit`
12. after external review: `paper-reviewer` to inventory the reports, `rebuttal-response` to draft and
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
9. `scientific-prose-style`, last
10. `submission-audit`

Run step 7 before step 9, never after.

## Choosing between adjacent skills

- `scientific-writing` when a section mostly needs drafting or rewriting in prose, or when a
  citation style or reporting guideline is named. `manuscript-optimizer` when the story, evidence
  chain, figure logic, or terminology may be unstable. `write-scientific-manuscript` when the
  science is settled but the passage is hard to follow.
- `results-section-revision` when the remaining problem is local Results architecture rather than
  claim selection.
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
  `paper-reviewer` runs a second time at the end to grade the draft. Optional set, installed with
  `--set all`.

## Working principle

Do not polish sections written from stale memory. After experimental, statistical, or figure
updates, refresh `notes/project_truth.md`, `notes/result_summary.md`, and `notes/paper_handoff.md`
before attempting heavy revision.

## Common mistakes

- answering a general manuscript request with whichever single skill matched the wording best
- polishing sentences before the claim hierarchy is stable
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
