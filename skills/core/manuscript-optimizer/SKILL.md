---
name: manuscript-optimizer
description: Use when auditing, restructuring, or revising a research manuscript whose scientific question, claim hierarchy, evidence chain, section logic, figures, terminology, or prose may be unclear or out of sync. Apply before sentence-level polishing, especially for whole drafts, major revisions, resubmissions, overclaiming, experiment-by-experiment Results, inaccessible narratives, or manuscripts that need a claim-driven architecture.
---

# Manuscript Optimizer

Treat scientific writing as reasoning, not decoration. Do not make existing results sound more
impressive. Organize the scientific question, evidence, interpretation, and conclusion into a chain
that a broad scientific reader can follow and evaluate.

Use this priority order without exception:

> scientific correctness > logic > information structure > clarity > concision > style

Prefer the simplest sentence that preserves the full scientific meaning. Never polish prose built
on an unstable claim, a missing evidence link, or a false scientific premise.

## Scope and handoff

Use this skill above the sentence level. Own the paper's scientific direction, claim architecture,
evidence boundaries, section and paragraph functions, figure-text logic, and terminology.

- Use `scientific-writing` after the architecture is stable to draft or rewrite full prose.
- Use `write-scientific-manuscript` to repair paragraph-level clarity and local reasoning.
- Use `scientific-prose-style` last for punctuation and rhythm.
- Use `results-section-revision` only when the claims are stable and Results needs local flow repair.
- Use `review-article-architecture` instead for a Review, survey, or Perspective.

For review-only requests, diagnose and stop. For revision requests, diagnose first and then edit in
the macro-to-micro order below.

## Hard constraints

Preserve the scientific record. Never:

- invent an experiment, result, citation, mechanism, or conclusion;
- alter a number, metric, comparison, data split, configuration, seed, or significance status;
- turn correlation, prediction, sensitivity, or consistency into causation or mechanism;
- turn a trend into a statistically significant result;
- generalize a dataset-, task-, model-, or condition-specific result into a universal conclusion;
- delete an important counterexample, negative result, or metric disagreement to improve the story;
- silently change the meaning of a term or the direction of a comparison.

When the evidence is missing, state the gap. Do not fill it with language. If a design or
implementation flaw invalidates a result, stop interpreting that result and report the flaw.

## Reader model

Assume a reader who understands the broad life-science or AI domain but does not know this
benchmark, dataset, metric, model, or local terminology.

Do not assume that the reader knows:

- why an analysis is necessary;
- what a metric measures scientifically;
- why a comparison is valid;
- why a model or baseline is included;
- why a result matters;
- whether two nearby terms denote the same concept.

Supply only the information required to understand the next logical step. Minimize reader inference
without turning the manuscript into an experimental log or a tutorial.

## Mandatory workflow

### 1. Establish the source of truth

Before rewriting, identify the authoritative manuscript, figures, legends, tables, result summary,
and project decisions. Preserve citations, figure references, numbers, symbols, and formatting.

Separate the input into three classes:

- **Confirmed:** directly supported by provided results or authoritative project records.
- **Assumed:** plausible but not verified from the supplied material.
- **Unresolved:** missing, contradictory, or scientifically ambiguous.

Do not present an assumption as a confirmed fact. Ask for missing information only when it would
materially change the scientific conclusion or revision direction; otherwise flag it and continue.

### 2. Define the North Star

Write one sentence for each item:

1. the broad problem;
2. the central scientific question;
3. the main claim supported by the study;
4. the contribution type, such as finding, method, benchmark, framework, resource, or reformulation;
5. the boundary conditions.

Look beneath model comparison when appropriate. Ask whether measurement, identifiability, data
resolution, task formulation, or evaluation design is the actual limiting issue.

If the main claim cannot be stated accurately in one sentence, do not begin prose revision.

### 3. Build the Claim Architecture

Create this artifact before restructuring a whole manuscript:

```text
North Star
└── Central scientific question
    └── Main claim
        ├── Claim 1
        │   └── Evidence: result / figure / table / analysis
        ├── Claim 2
        │   └── Evidence: result / figure / table / analysis
        ├── Claim 3
        │   └── Evidence: result / figure / table / analysis
        └── Boundary conditions and unresolved points
```

Use the architecture across the paper:

- Introduction raises the question.
- Results establishes the claims.
- Discussion interprets and connects the claims.
- Abstract compresses the chain.
- Title expresses the highest supported claim or question.

Do not force three claims when the paper supports two, and do not present several contributions as
equally central unless the evidence and design require that structure.

### 4. Map claims to evidence and calibrate their level

Extract substantive claims from the title, abstract, introduction, Results headings, figure
legends, and discussion. For each claim, record its exact support and mark it:

- fully supported;
- partially supported;
- unsupported by current evidence;
- hypothesis or interpretation rather than direct finding.

Use the claim ladder:

```text
observation → empirical pattern → interpretation → mechanism → general principle
```

Write only at the highest level directly licensed by the evidence. Distinguish, for example,
`performed best under the evaluated settings` from `is the best representation`.

For a claim that exceeds its evidence, take one of three actions:

1. narrow the claim;
2. add or request the missing evidence;
3. label it as a hypothesis, possible explanation, or motivation.

Calibrate the claim itself instead of making an inflated statement and retracting it through a
defensive caveat. Use `This pattern is consistent with...` or `One possible explanation is...`
when a mechanistic interpretation lacks a direct mechanism experiment.

### 5. Reverse-outline before rewriting

For each section, state its one-sentence function. For each paragraph, record:

- its one main message;
- the evidence or reasoning it contains;
- its relationship to the previous paragraph;
- its contribution to the section claim.

Move, merge, split, or remove material that cannot be mapped cleanly. Organize Results by questions
and answers, not by the chronological order of experiments or panels.

Choose the edit depth only after this audit:

- **Micro-edit:** logic and order are sound; wording is the bottleneck.
- **Local rewrite:** the paragraph claim is valid, but order, reasoning, or emphasis is weak.
- **Structural rewrite:** the section question, claim hierarchy, or evidence sequence is wrong.
- **Scientific blocker:** the evidence is missing, contradictory, or invalid; do not rewrite past it.

Do not default to preserving the original sentence or paragraph structure.

### 6. Align figures, text, and terminology

Assign every figure and panel one primary role: claim-supporting evidence, definition or
methodological bridge, validation in a new setting, practical consequence, or case illustration.

Check that:

- each main figure carries one primary claim unless the paper's logic requires a composite figure;
- every major claim points to the correct figure, table, or supplementary item;
- the Results states the question and main inference rather than merely saying a figure is similar;
- the figure carries evidence density while the text carries the inference;
- panel labels, metrics, baselines, datasets, abbreviations, and numbers agree across all locations;
- negative results and metric disagreements remain visible;
- legends define the evidence without making a stronger claim than the plot supports.

Create a canonical term list for core concepts, tasks, settings, datasets, models, baselines, and
abbreviations. Use one primary term per concept. Change terms only when the scientific level truly
changes; do not rotate synonyms merely to avoid repetition.

### 7. Rewrite from macro to micro

After the architecture is stable, revise in this order:

1. section purpose and order;
2. subsection question and claim;
3. paragraph function and evidence sequence;
4. explicit reasoning and transitions;
5. claim verbs and scope qualifiers;
6. terminology;
7. sentence clarity and concision;
8. punctuation and rhythm.

Run a final skeptical review across contribution sufficiency, scientific clarity, empirical
strength, evaluation completeness, and method or framework soundness. Point to evidence rather than
answering from intuition.

## Section contracts

### Title

Express the central scientific finding or question at the highest supported level. Prefer:

> concept or finding > framework name > implementation

Use a benchmark or method name as the title focus only when that artifact is itself the main
contribution. Avoid unexplained acronyms, inflated umbrella terms, and unsupported breadth.

### Abstract

Build one complete chain:

> problem → unresolved gap → approach → two or three main findings → conceptual implication

Do not compress Results mechanically. Omit dataset lists, every baseline, every metric, pipeline
details, and secondary analyses unless one is essential to the main claim. Ensure that a broad
reader can state the paper's main finding after one read.

### Introduction

Use this default progression:

1. the field-level problem;
2. the missing capability or unresolved question;
3. why the problem remains difficult or conceptually unresolved;
4. what this study does and what it makes possible to learn.

Move from `field → gap → precise question → solution`. Use literature to establish the gap, not to
display coverage. Avoid method-by-method catalogues. Define the real scientific problem before
introducing the proposed model, benchmark, or framework.

### Results

Treat Results as an argument. Organize each subsection as:

> question → why the analysis is needed → design → core observation → interpretation

Lead paragraphs with the scientific message when the evidence already supports it, not with a
generic action such as `We next investigated...`. Make the link from analysis to conclusion
explicit; do not make the reader derive the decisive inference from a list of observations.

For every reported metric, state its scientific or evaluative meaning when needed for the next
inference. When metrics disagree, explain what each metric captures and treat the disagreement as a
result. For example, distinguish pattern agreement, magnitude error, and direction accuracy rather
than treating one higher correlation as globally better performance.

Report only the one or two quantitative anchors needed to support the local claim, not every plotted
number. Keep denser panel-level values in the figure or legend. Do not package all findings as
positive. Context dependence, no universal winner, negative results, and metric disagreement may be
the central result.

### Discussion

Answer these questions instead of replaying the Results:

1. What do the findings jointly establish?
2. What could explain the pattern?
3. How does it change the understanding of the problem?
4. Which implications extend beyond this dataset or analysis, and why?
5. Where are the boundaries?

Use `main answer → scientific interpretation → broader implication → limitations → future
implication`. Clearly label mechanism evidence versus mechanistic hypothesis. State limitations
once, where they constrain the claim, rather than appending defensive caveats to every result.

### Figures and legends

Make the main text state the question, important pattern, and inference. Make the figure carry dense
evidence and the legend define panels, groups, units, statistics, sample sizes, and visual encodings.
Never write only `Supplementary Fig. X shows similar results`; state what question it answers and
what pattern matters.

## Paragraph and sentence rules

Use the paragraph as the basic logical unit. Give it one main job and, when appropriate, this form:

> topic sentence → evidence → interpretation → transition or implication

Make the first sentence explain why the paragraph exists. Prefer the scientific message to the
experimental action. Do not force every paragraph into the template when another order is clearer.

State important inference explicitly. If observations A, B, and C support a modality-dependent
effect, write that conclusion instead of asking the reader to assemble it.

Use common, precise words and concrete scientific nouns. Prefer verbs to nominalizations. Avoid
noun stacks such as `representation architecture robustness evaluation analysis`. Keep one main
logical relationship per sentence. Split a sentence that simultaneously introduces background,
describes a method, reports numbers, interprets the result, and qualifies the claim.

Do not replace readable prose with a sequence of fragments. Align syntactic units with logical
units, and retain technical distinctions that change the scientific meaning.

## Prohibited patterns

Reject or rewrite these patterns unless the evidence and context specifically justify them:

- experiment logs: `We evaluated... We found... We also found... In addition...`;
- disconnected proof: `We did A and B. We observed C and D. Therefore, X` without the missing link;
- procedural paragraph openers that hide the message: `To further investigate...`;
- ornamental or vague abstractions such as `stable performance regimes`, `intrinsic quality`, or
  `comprehensive superiority` when ordinary words are more exact;
- empty intensifiers such as `remarkably`, `notably`, `encouragingly`, and `promisingly`;
- repeated defensive caveats after already bounded claims;
- synonym rotation for one scientific concept;
- causal or mechanistic verbs for observational evidence;
- universal labels such as `optimal`, `general`, `robust`, `fundamental`, `transparent`, or
  `state-of-the-art` without evidence covering that scope;
- subsection titles that name only the procedure when the supported finding can orient the reader;
- figure references with no stated question, pattern, or inference.

Do not ban a word mechanically. Reject it when it obscures meaning, inflates the claim, or adds no
scientific information.

## Six-question gate

Before accepting any revised paragraph, answer:

1. Why is this paragraph here?
2. What is its one message?
3. What evidence supports that message?
4. Does the claim exceed the evidence?
5. Can a broad scientific reader follow the reasoning without supplying a key inference?
6. Can anything be removed without losing scientific meaning?

If question 1, 2, or 3 has no clear answer, restructure the paragraph. If question 4 is yes, narrow
the claim or obtain evidence. If question 5 is no, add the missing bridge. If question 6 is yes,
delete the excess.

## Output standard

For a manuscript audit, report in this order:

1. **Verdict:** whether the scientific narrative is stable enough to rewrite.
2. **Confirmed / assumed / unresolved:** the truth boundary used for the audit.
3. **Claim Architecture:** North Star, central question, main claim, supporting claims, evidence,
   and boundaries.
4. **Major findings:** unsupported claims, missing reasoning, structural breaks, figure-text
   mismatch, metric misinterpretation, and terminology drift, in severity order.
5. **Edit depth:** micro-edit, local rewrite, structural rewrite, or scientific blocker.
6. **Next action:** the smallest safe revision step.

For an authorized revision, add:

- complete ready-to-use revised prose or file edits;
- a concise account of material scientific choices;
- unresolved evidence gaps that language cannot repair;
- verification performed.

Do not claim that a manuscript or section is improved merely because the prose is smoother. Claim
completion only after the evidence chain, information structure, terminology, and revised text have
been checked together.
