---
name: review-article-architecture
description: Use when writing, restructuring, or auditing a Review, survey, or Perspective rather than a research article, especially a commissioned one written across many sessions. Covers the governing plan document, drift detection, single-definition thesis and field judgements, section-owns-figure allocation, display-item budgets, four-state status markers, and authorship-blank discipline. For research articles with Results and Methods, use manuscript-optimizer instead.
---

# Review Article Architecture

## Overview

A Review fails differently from a research article. A research article drifts by
overclaiming past its own data. A Review drifts by **becoming a different Review**:
the argument that felt strongest in session 20 quietly replaces the argument the
piece was commissioned to make, and because each individual edit was an
improvement, nothing looks wrong until someone reads it against the brief.

That is not hypothetical. One commissioned Review in this lineage drifted over
several sessions into a metrology argument about cross-sensor interoperability.
It was internally consistent, well sourced, and would have been a reasonable
paper. It was the wrong paper, it violated four explicit constraints of its own
brief, and it had to be reverted wholesale.

This skill is the machinery that makes that drift detectable and mostly
preventable.

## When To Use

Use this skill when:

- writing or revising a commissioned, invited, or submitted Review, survey, or
  Perspective
- a Review is being written across many sessions, by several people, or by agents
- the piece has an explicit brief, synopsis, or commissioning plan
- structure, section ownership, terminology, or display-item count is unstable
- an outline exists and the question is whether the draft still matches it

Do not use this skill for:

- research articles with Results and Methods. Use `manuscript-optimizer`.
- venue selection among Nature journals. Use `nature-portfolio-playbook`.
- sentence-level prose. Use `scientific-prose-style` after this is stable.
- finding, summarizing, or comparing the literature itself. Use
  `academic-researcher` (optional set, installed with `--set all`); this skill
  governs the article's structure, not source
  discovery.
- deciding what each figure argues. Use `figure-planner`; this skill decides
  which section owns it and how many there may be.

## 1. The Governing Document Is Authoritative, Not Advisory

Designate exactly one file as the brief, and give it authority in writing:

- it fixes the body sections and their order
- it fixes the display items and their count
- it fixes the terminology
- it records the adjudications that resolved earlier disagreements

Then the rule, stated in the manuscript README so nobody has to infer it:

> Do not reorder, merge, or add a section, a figure, or a term without amending
> this file first. **If the plan and a better idea conflict, raise the conflict.
> Do not resolve it by editing the manuscript.**

This is the load-bearing rule of the whole skill. A Review written over months
accumulates dozens of locally-good decisions, and without an authority to check
them against, their sum is a different paper. The plan is not there because it is
smarter than you. It is there because it does not change while you are working.

**Record adjudications, not just requirements.** When the plan settles a question,
write the settlement into the plan. In the Review above, an early outline had a
comparison Table; the final adjudication merged its content into Figure 1 and
fixed the count at six figures and no Table. Without that written down, the Table
regrows: someone reads the old synopsis, notices a Table is missing, and helpfully
adds it back.

**Point the raw materials at the plan.** A commissioning synopsis, a slide deck,
and an early figure draft all contain figure numbering and item plans that the
plan has since superseded. Say so explicitly next to each raw material, or the
next reader will follow the wrong one.

## 2. Drift Audit

Run this whenever a Review has been drafted across multiple sessions, and always
before a compression or polish pass. Polishing a drifted draft makes it harder to
detect, not easier.

Four symptoms identified the real case:

1. **The draft is a genre the plan prohibits.** The plan forbade writing a pure
   device review; the drifted version was one. Read the plan's prohibitions, not
   just its requirements, and check the draft against each.
2. **A required section is missing.** The plan required a market section. The
   drifted version had dropped it entirely, and nobody noticed because the
   remaining sections were good.
3. **The designated centrepiece is flattened.** The plan named one section as the
   heart of the Review, carrying the author team's accumulated work. The drifted
   version had it at the same weight as everything else. Check section word counts
   against the plan's intended emphasis, and require an explanation for any
   inversion.
4. **The thesis and terminology are different.** Not weaker, not stronger:
   different. Compare the current thesis sentence to the plan's, word by word.

A fifth check worth adding: **does the draft still answer the commissioned
question?** Write the question in one line, then read the abstract. If the
abstract answers a neighbouring question, that is drift regardless of quality.

When drift is found, the recovery is not incremental. See
`references/drift-audit.md` for what to carry forward from a reverted version and
what must not be carried forward.

## 3. The Thesis Is A Macro, Not Prose

Define the Review's central claim **once**, as a macro, and never retype it:

```latex
\newcommand{\thesisline}{...}   % the Review's claim, defined here and nowhere else
\newcommand{\claimA}{...}       % field judgement, owned by section 2 and Figure 1
\newcommand{\claimB}{...}
```

Call the macro in exactly the places the thesis belongs: the abstract, and the
close of the Introduction. Each field judgement gets one Key points bullet and at
most one figure caption. **A caption carries one judgement, never the whole
thesis.**

The failure this prevents is specific and this project had it: the abstract, the
Introduction, and the Key points each carried a hand-typed version of the same
claim, and three rounds of independent editing left them saying three different
things. Calling a macro makes that impossible rather than merely discouraged.

**Keep the retired thesis sentences.** When a thesis is replaced, leave the
previous ones in the preamble as comments with the reason each was retired. Three
were tried and dropped in the Review above; keeping them stops a later session
from reintroducing one as a fresh idea.

## 4. Each Section Owns Its Display Items

Write an explicit ownership table and keep it in the manuscript README:

| Figure | Owning section | Field judgement it carries |
| --- | --- | --- |
| Fig 1 | landscape | judgement A |
| Fig 4 | the centrepiece section | judgement B |

Two consequences follow:

- **The float lives in the owning section**, not massed at the end of the file.
  A Review's figures are read alongside their argument, and a figure whose owning
  section is unclear is usually a figure whose claim is unclear.
- **Every asserted cell in the artwork traces to the owning section.** If a figure
  states a maturity level, a "not established", or an absence of evaluation, that
  is an assertion and it needs the same traceability as a sentence. See
  `nature-figure`'s figure-delivery-bundle reference for the mechanism
  (figure stack, installed with `--figure`).

**Watch for ownership gaps when the plan changes.** In the real case, the team's
division of labour was written against five figures and a Table. The plan later
adjudicated six figures and no Table. That left Figure 6 with no owner and the
Table assignment pointing at nothing. Neither gap was visible until the two
documents were read side by side. When the plan changes a display item, re-read
the assignment table in the same pass.

## 5. Display-Item Budget

Venue limits are hard constraints and they are structural, not cosmetic. Fix the
count in the plan early, because item count drives section structure: a section
that owns no display item usually turns out to be a section with no independent
claim.

Check the venue's actual limits (item count, full-width dimension, minimum type
size) before designing, not after drawing. Retrofitting a seven-item Review into a
six-item budget means deciding which argument loses its evidence, and that
decision is much worse when made under deadline.

## 6. Status Markers Are Four-State, Never Two

This one is easy to get wrong and it changes conclusions. When a Review tabulates
what exists, resist the binary:

- **established**: exists and is independently evaluated
- **partial**: exists with a stated limitation
- **not established**: the thing exists but has not been settled, standardised,
  or independently evaluated
- **absent**: it does not exist as checked

**"Not established" is itself a finding** and it is often the most interesting
cell in the table. Collapsing it into "absent" throws away the distinction between
a field that has not done the work and a field where the work is impossible.
Collapsing it into "established" is straightforward overclaiming.

Use the same four states in the prose and in the artwork, with the same words.

## 7. Negative Claims Name What Was Checked

A Review makes many claims of absence, and absence is unfalsifiable as usually
written. Bound every one:

Not: "no standard covers this."
But: "absent from the public record as checked, namely <the standards catalogue,
the evaluation programmes, the corpora> examined."

Name the documents and programmes. This costs a clause and converts an
unfalsifiable claim into a checkable one, which is the difference between a
reviewer trusting the sentence and a reviewer having to take your word.

## 8. Word Budget Measured By Section

Measure, do not remember, and measure the prose a reader reads rather than the
markup. See `draft-marker-discipline` for the mechanism. In one measured Review
a bare word count read 19,900 against 14,300 words of actual prose, about 40%
over. The size of that gap depends entirely on your legend count and marker
density, so measure yours rather than assuming that figure.

Then, for every section that looks disproportionate, state which it is:

- **long by design**, because the plan designates it as the centrepiece
- **long by drift**, and due for compression
- **short because finished**
- **short because blocked**, naming what blocks it

A Review whose market section is 350 words is not a Review with a thin market
section. It is a Review whose market data does not exist yet. Those need
different responses and the word count alone cannot tell them apart.

## 9. Authorship Blank While It Is Being Discussed

If the author list and order are not settled, keep **every** contributor name out
of the manuscript tree: not in the title block, not in a figure caption, not in a
comment, not in a planning document inside the tree.

The reason is social rather than technical. A name written next to a deliverable
reads as a claim on authorship, and it accumulates weight simply by sitting there
across sessions.

Enforce it with a scan rather than a convention:

```make
check:
	@grep -rnE '<name1>|<name2>' main.tex sections/ figures/ *.md || echo "  none"
```

Keep the coordination record (who is drawing which figure) **outside** the
manuscript directory, and say in that file that it is coordination, not
attribution. When authorship is agreed, fill it in once, in one file.

## Default Workflow

1. Identify or create the governing document. If the brief is a synopsis or a
   slide deck, convert it into a plan file and mark the raw materials superseded.
   `references/governing-document.md` carries the skeleton and the amendment
   protocol.
2. Fix sections, display-item count, and terminology in that file. Record
   adjudications.
3. Run the drift audit against the current draft, if one exists.
4. Define the thesis and field judgements as macros. Replace every inline copy.
5. Write the section-owns-figure table; check it against the plan after any
   display-item change.
6. Draft, sourcing as you go rather than retrofitting citations
   (`claim-source-verification`).
7. Measure word counts by section; label each disproportion by cause.
8. Only then compress and polish (`scientific-prose-style`).

## Standing Rules

1. **The plan is authoritative. Conflicts get raised, not resolved by editing.**
2. **The thesis is defined once and called, never retyped.**
3. **Nothing is deleted silently.** Superseded material is archived with a record
   of where it went. See `draft-marker-discipline`.
4. **A negative claim names what was checked.**
5. **Four status states, not two.** "Not established" is a finding.
6. **No contributor name in the tree while authorship is open.**
