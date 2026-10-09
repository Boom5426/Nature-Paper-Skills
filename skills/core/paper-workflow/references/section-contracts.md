# Section contracts

The layers in `SKILL.md` decide what to fix first. The position decides what a fixed section must
do. An abstract, an Introduction and a Methods section are held to different standards, and some
layers behave differently in them. This file states each position's job once. Specialist skills
apply these contracts at their own layer and do not restate them.

Use an entry twice: to diagnose the section before editing, and to accept the edit afterwards.

## Logic here, format at the journal

A contract says what a position must do. It does not set the format. Abstract length, a single
paragraph versus a structured abstract, whether the abstract carries citations, title length,
heading rules, Methods placement and display-item limits come from the target journal's current
guide. For Nature Portfolio journals, `nature-portfolio-playbook` lists what to check.

Never import a format from a generic template. A structured abstract with Background, Methods,
Results and Conclusions labels is a requirement of some journals and reporting guidelines, not a
default. On the default journal path, with no stated format, write the abstract as one unstructured
paragraph and report the format as unchecked.

## Dependency order

Positions restate claims that are settled elsewhere:

> figures and evidence → Results → Discussion → Introduction → Abstract → Title

The Introduction's opening rests on the central question; its final paragraph rests on the Results.
Methods records what was actually done and changes only when a procedure or analysis changes.
Legends depend on their figure and on the Results sentence that cites it.

Three rules follow.

1. **A downstream request stays narrow.** When the requested position depends on an unsettled
   upstream result, make the requested edit against the current upstream text. Keep claims that
   rest on the unsettled result out of it, or mark them as pending, and name the dependency in the
   reply. Do not widen the edit to the upstream section.
2. **An upstream change ripples forward.** After a Results claim changes, recheck the positions that
   restate it: the Discussion opening, the final Introduction paragraph, the Abstract, the Title and
   the affected legends. This is a focused consistency check, not a rewrite.
3. **No position claims more than its upstream supports.** The Title is no stronger than the
   Abstract, and the Abstract is no stronger than the Results.

## Typical shape

Count moves, not paragraphs. The ranges below are checks: a section far outside them usually has a
move missing, split or duplicated. They are not targets to pad or trim toward. They come from 28
computational-method Articles in Nature Methods, Nature Biotechnology and Nature Communications
([section-evidence.md](section-evidence.md)), except where marked as a house choice.

| Position | Moves, in order | Typical range |
|---|---|---|
| Abstract | problem, gap, approach, findings, implication | one paragraph of 5–8 sentences |
| Introduction | field problem, what prior work cannot answer, why it is hard, this study and its main findings | 3–5 paragraphs |
| Results | one subsection per claim | 5–8 subsections of 3–6 paragraphs |
| Discussion | findings and their significance, why they hold and what they mean, scope and field-level implication | 3–5 paragraphs (house choice; the sample median is 5) |

## Title

- **Job:** name the central finding or question at the highest level the evidence supports.
- **Depends on:** the main claim, as compressed in the Abstract.
- **Meets the contract when:** the focus follows concept or finding > framework name >
  implementation; a broad reader knows what the paper is about after one pass; it uses the terms
  the intended readers search for.
- **Method papers:** the title names the task, the data or setting and the key idea ("Mapping
  single-cell data to reference atlases by transfer learning"). The method name is optional and,
  when present, often follows "with". A claim sentence fits a title when the contribution is a
  finding.
- **Fails when:** a method or benchmark name is the focus although it is not the main contribution;
  it uses an unexplained acronym, an inflated umbrella term or a label such as "novel"; it is
  broader than the evidence.
- **Owners:** `scientific-writing` (`references/editor-first-impression.md`) to draft;
  `manuscript-optimizer` to check it against the claim architecture.

## Abstract

- **Job:** compress the paper's chain so that a reader outside the subfield can state the main
  finding after one read.
- **Depends on:** settled Results claims, the Discussion's main answer and the Introduction's gap.
- **Meets the contract when:** one chain runs problem → unresolved gap → approach → the findings
  that carry the main claim (usually one to three) → bounded implication, and every sentence
  advances it. The sentence that introduces the study ("Here we present ...") follows the problem
  and gap, usually as the second to fourth sentence. Comparative results are stated in words, with
  what was compared and on what ("more accurate than X on Y"). A number appears only when the number
  is the claim, usually at most one, and it carries its direction, magnitude and comparison. A
  closing sentence of field-level implication is acceptable when it names what becomes possible.
  When the supplied material does not provide a move, most often the gap, take it from the
  Introduction or leave it marked for the author; do not compose a new claim about the literature.
- **Fails when:** generic background takes most of the space; it lists datasets, baselines or every
  metric; it says a result was significant without saying what changed, or offers a P value as the
  finding; it claims more than the Results, such as outperforming all methods when the Results show
  a narrower win; it cites a result whose Results subsection is not settled; it uses labels such as
  "novel" or "powerful" in place of a result; it ends on a generic promise ("will be a powerful
  tool").
- **Layer notes:** the Abstract is a compression of the argument, not a summary of the Results in
  order. At the posture layer it keeps headline findings and effect sizes; test statistics,
  provenance and caveats leave unless the claim is false without them (`anti-defensive-writing`).
- **Owners:** `scientific-writing` (`references/editor-first-impression.md`) to draft;
  `write-scientific-manuscript` for the sentence chain; format from the journal.

## Introduction

- **Job:** make the study's question necessary.
- **Depends on:** the central question; the final paragraph also depends on the Results.
- **Meets the contract when:** it moves from the field-level problem to the missing capability or
  unresolved question, then to why that question remains hard, then to what this study does and
  what it makes possible to learn. Prior work is organized by what it can and cannot answer. The
  final paragraph states the question, approach and primary contribution, then previews the main
  findings as an enlarged version of the Abstract's findings sentences: what was shown, against
  what, and what it enables, in a few sentences.
- **Fails when:** it is a method-by-method catalogue or a chronology; the proposed method appears
  before the problem is defined; the final paragraph walks through the applications or figures one
  by one, gives detailed numbers, or promises what the Results later walk back; it carries design
  controls, field commentary or rhetorical questions.
- **Owners:** `scientific-writing` to draft; `write-scientific-manuscript`
  (`references/section-logic.md`) for the paragraph sequence; `claim-source-verification` for the
  sentences that establish the gap.

## Results

- **Job:** establish the claims as an argument, one subsection per question.
- **Depends on:** the figures, tables and analyses, and the claim architecture.
- **Meets the contract when:** each subsection heading states the supported finding. A subsection
  opens with the question or context that makes the analysis necessary; later paragraphs lead with
  their message when the evidence supports it. Each local claim runs question → minimum design →
  core observation with direction and magnitude → interpretation, stated explicitly whenever the
  inference is not obvious from the observation. One or two quantitative anchors carry each local
  claim, each against a named comparison; denser values stay in figures and legends. Where a
  metric's meaning matters for the next inference, the text states what it measures. When metrics
  disagree, the text says what each captures (for example pattern agreement, magnitude error and
  direction accuracy) instead of letting one metric stand for overall performance. Observation,
  interpretation and implication stay distinct.
- **Keeps visible:** metric disagreement, null and negative results, context dependence and the
  absence of a universal winner. Any of these may be the result.
- **Method papers:** the first subsection presents the method and its principle, anchored on
  Fig. 1. Its heading is "Overview of X" or one sentence stating the principle ("X combines A with B
  to model C"). Open with a result instead only when the first contribution is itself a finding.
  The usual order is overview → comparison with baselines, early (often the second subsection) →
  properties such as robustness, ablation and scalability → biological applications, ending on the
  strongest biological result.
- **Fails when:** it follows experiment chronology or panel order; procedural openers ("We next
  investigated", "To test this") are the default pattern or run in consecutive subsections;
  implementation checks are reported as findings; a chain of setup, safeguard and caveat precedes
  the result; a figure is cited without its question or inference; an interpretation is presented
  as a measurement.
- **Owners:** `manuscript-optimizer` while the claims are moving; `results-section-revision` once
  they are settled; `stats-reporting-audit` for reported statistics.

## Discussion

- **Job:** state what the findings jointly establish and what changes because of them.
- **Depends on:** settled Results.
- **Meets the contract when:** it makes three moves, in this order, each in one or more paragraphs.
  1. **Findings and their significance:** open with the main advance and its evidence, and say what
     it adds to or changes in existing methods or understanding. The comparison with related
     methods belongs here or in move 2.
  2. **Why they hold and what they mean:** the methodological logic behind the result (which design
     choice does the work) and the biological value of the findings. Interpret rather than replay,
     and label mechanism evidence apart from mechanistic hypothesis.
  3. **Scope and field-level implication:** the conditions under which the conclusions hold, then
     the implication for the field, including which implications extend beyond the data analysed,
     and why. The final sentence states that implication and names what becomes possible.
- **Limitations:** state genuine limitations once, as scope, in move 3, or where a limit sets a
  reported value. A useful limitation changes how a result is read.
- **Fails when:** it reopens with field background; it repeats Results numbers; it itemizes
  self-criticism or repeats limitations already stated in the Results; it ends on a caveat, a plan
  or a software availability statement; it closes on "paves the way" without naming what becomes
  possible.
- **Owners:** `scientific-writing` to draft; `write-scientific-manuscript` for passage logic;
  `anti-defensive-writing` for posture.

## Methods

- **Job:** let another expert reproduce what was done and judge whether it was valid.
- **Depends on:** the procedures and analyses actually run, not the narrative.
- **Meets the contract when:** data, preprocessing, splits and their unit, models, objectives,
  metrics, statistics, selection procedures and software versions are defined unambiguously; the
  unit of replication and n are stated; every term used in the Results is defined; the items of an
  applicable reporting guideline are present.
- **Method papers:** the comparison setup has its own description: which baselines, which versions
  and settings, how each was tuned and on what data, and how each metric is computed. A comparison
  the reader cannot reproduce cannot carry a claim.
- **Fails when:** a method appears first in the Results; it carries interpretation paragraphs or
  repeated defences of a choice; sensitivity results and implementation checks sit here instead of
  in the SI.
- **Layer notes:** nearly every statement is load-bearing. Posture edits change form (negation to
  positive scope, stated once) and never delete a reproducibility fact. Passage edits fix ambiguity,
  not rhythm; procedural prose is acceptable here.
- **Owners:** `scientific-writing` (`references/reporting_guidelines.md`); `stats-reporting-audit`
  for the statistical analysis subsection.

## Figure legends and table notes

- **Job:** make each display item readable without the Results text.
- **Depends on:** the figure itself and the Results sentence that cites it.
- **Meets the contract when:** it defines each panel's role; states what is plotted, the groups,
  units, n with its unit, error bars and the statistic; keeps the quantitative anchors the main text
  omits; and agrees with panel letters, metrics, datasets and baselines.
- **Method papers:** Fig. 1 usually presents the method (workflow, model and inputs) and anchors the
  first Results subsection.
- **Fails when:** its interpretation is stronger than the plot; it carries interpretation defences
  or verdict columns; it was edited after the Results without rechecking them.
- **Owners:** `figure-planner` (legend rules); `stats-reporting-audit`
  (`references/figure-statistics.md`).

## Supplementary Information

- **Job:** hold the experimental record behind the main claims, in the same voice as the main text.
- **Meets the contract when:** each item states the question it answers, and the main text cites it
  by that question and the pattern that matters, never only "shows similar results".
- **Fails when:** it carries audit commentary, unused items, reader instructions or build notes.
- **Owners:** `anti-defensive-writing`; `scientific-writing` (`references/latex-layout.md`) for SI
  table layout.

## Data and code availability

- **Job:** state what exists now, where it is and what it contains.
- **Owners:** `data-availability`. Repository names, accession numbers and access conditions are
  author facts; never invent or promise them.
