---
name: manuscript-optimizer
description: Use when reviewing or revising an academic manuscript whose central claim, evidence chain, figures, terminology, and prose may have drifted out of sync before submission or resubmission.
---

# Manuscript Optimizer

## Overview

Use this skill to treat a manuscript like a precision instrument: fix the top-level design first, then the evidence chain, then the figures, then the terminology, and only then the sentence-level polish.

This workflow is not tied to a single paper or field. Use it across manuscript projects whenever structure, evidence, figures, and prose need to be brought back into alignment.

Core rule: do not spend effort polishing prose that sits on top of an unstable claim, a broken evidence chain, or inconsistent figures.

## When To Use

Use this skill when:
- A paper is being drafted, revised, resubmitted, or journal-adapted
- The abstract or introduction may be stronger than the downstream evidence
- The storyline feels diffuse, repetitive, or hard to defend
- Figures, legends, and main text may have drifted out of sync
- Core terminology or abbreviations may be unstable
- The writing needs to become clearer, tighter, and more reader-friendly without losing rigor

Do not use this skill as the primary workflow for:
- Pure literature review generation
- Citation-format-only cleanup
- Methods-only statistical review
- Journal peer review reports that focus mainly on acceptance recommendations

## Operating Principle

Always move in this order:
1. Direction first
2. Logic second
3. Visual evidence third
4. Terminology fourth
5. Language last

If a higher-level problem is unresolved, do not present lower-level polish as a solution.

## Two Modes

### Review Mode

Use when the task is to diagnose weaknesses before editing.

Output priorities:
- Findings first
- Highest-level issues first
- Explicitly separate unsupported claims, weak support, and cosmetic issues
- Cite exact sections, figures, or sentences when possible

### Optimization Mode

Use when the task is to actually rewrite or tighten the manuscript.

Execution order:
- Fix macro positioning and claim boundaries
- Repair section logic and evidence chain
- Sync figures, legends, and text
- Canonicalize terminology
- Polish prose, grammar, and format

## The Five-Level Audit

### 1. Top-Level Design And Core Contribution

Check the manuscript's top story before touching paragraph style.

Audit:
- What is the central problem?
- Why does it matter now?
- What is the single-sentence take-home message?
- Is the main contribution a method, framework, benchmark, resource, biological finding, or something else?
- Is the claim ambitious enough to matter but narrow enough to defend?
- After reading the abstract and introduction, can a broad scientific reader understand why this work is not interchangeable with prior work?

Guardrails:
- Do not let the paper sound like it contributes three equally important things unless that structure is deliberate and defensible
- Do not let examples, intuitions, or motivating cases masquerade as experimental evidence
- If the real contribution is a reformulation or evaluation framework, do not accidentally rewrite it as "a new model"

### 2. Logic Architecture And Evidence Chain

This is the main structural check.

Build a claim-to-evidence map:
- Extract every substantive claim from the abstract
- Extract every substantive claim from the introduction and discussion
- For each claim, point to the exact supporting result, figure, table, or supplementary item
- Mark each claim as:
  - fully supported
  - partially supported
  - not supported by current evidence

Then run a reverse outline on the current section structure:
- Write the section thesis in one sentence.
- Write one line for each paragraph:
  - paragraph job
  - key evidence or reasoning inside it
  - the transition relation to the previous paragraph
- Merge, move, or remove any paragraph that cannot be mapped cleanly to the section thesis.

When a claim is not fully supported, only three acceptable actions exist:
- weaken the claim
- add the missing evidence
- reframe the claim as intuition, hypothesis, or motivation

Questions to ask:
- Does each Results subsection answer a clear question?
- Does each module in the method or framework have a corresponding validation experiment?
- If the manuscript claims OOD generalization, cross-domain transfer, causal disentanglement, or clinical relevance, is there direct evidence for that exact statement?
- Are surprising or paradoxical findings explained, not merely reported?

Never leave the abstract or introduction stronger than the Results.

### Adversarial Self-Review

Before calling the structure stable, pressure-test the manuscript like a skeptical reviewer in five dimensions:
- contribution sufficiency
- writing clarity and reproducibility
- empirical strength
- evaluation completeness
- method or framework soundness

Do not answer these with intuition alone. Point to concrete sections, figures, tables, or supplementary items.

### 3. Data Visualization And Figure Expression

Treat figures as independent carriers of the paper's logic.

Audit each figure on its own:
- Can the figure tell its own story without the main text?
- Do panel labels, legends, and body text say the same thing?
- Are metrics, baselines, datasets, and abbreviations defined consistently?
- If a panel was removed or reordered, were the text and legend updated in the same pass?
- Are the key comparisons visually obvious, not buried in clutter?
- Does the figure support the exact claim made about it in the Results?

For high-impact-journal style manuscripts:
- Prefer figures that communicate one main message each
- Reduce decorative complexity
- Make figure titles and legends carry real interpretive value
- Do not let legends overclaim relative to the plotted data

### Results Compression And Figure-Legend Balance

When a Results section feels overloaded, compress it by claim rather than by panel count.

Rules:
- Prefer one main claim per figure.
- If a figure needs internal subdivision, keep it to at most two Results subsections unless there is a strong reason otherwise.
- Keep only `1-2` hard numbers in the main-text paragraph that directly support the local claim.
- Move panel-level values, method-by-method comparisons, and denser quantitative detail into figure legends or supplementary display items.
- Treat figure legends as the second layer of result narration: they should define panel roles, preserve key quantitative anchors, and stay synchronized with the compressed main text.

Before rewriting figure-linked prose, identify each panel's real role:
- claim-supporting evidence
- methodological bridge or definition
- validation under a new regime
- translational or practical consequence
- case illustration

Do not flatten a methodological bridge panel into generic motivation. If a panel explains where a metric or evaluation space comes from, say so explicitly in the main text.

When multiple metrics are shown:
- keep the strongest metric as the primary evidence in the Results paragraph
- demote weaker or more auxiliary metrics to complementary readouts
- do not oversell a metric that is mainly included for completeness or secondary utility

### 4. Terminology And Domain Language

Scientific credibility depends on stable naming.

Create a canonical term list early:
- core concepts
- formal decomposition terms
- benchmark names
- task settings
- baseline names
- abbreviations

Then enforce it everywhere:
- abstract
- introduction
- results
- discussion
- figure labels
- legends
- supplementary text

Audit:
- Are old and new names mixed?
- Are informal descriptions replacing formal terms in key places?
- Are multiple near-synonyms being used for one concept?
- Are any terms likely to create domain confusion because they already mean something else in the field?

If a term is formal, keep it stable.
If a looser explanatory phrase is needed, make sure it does not compete with the formal term.

### 5. Micro-Level Polish

Only do this after the first four levels are stable.

Targets:
- grammar
- singular/plural consistency
- tense consistency
- punctuation
- article usage
- redundant phrases
- repeated transitions
- overlong sentences
- vague intensifiers
- empty summary lines

Preferred prose style:
- professional but readable
- specific rather than ornamental
- short-to-medium sentences by default
- one paragraph, one job
- observations and interpretations clearly separated

Avoid:
- bloated topic sentences
- unnecessary jargon
- unstable voice
- repeated transition formulas
- em dashes unless explicitly wanted
- generic AI-sounding escalation words

## Default Workflow

When asked to improve a manuscript, follow this sequence:

1. Identify venue, article type, and the paper's intended central contribution.
2. Read abstract, introduction, results headings, and figure legends first.
3. Write a short claim-to-evidence map.
4. Reverse-outline the current section or subsection structure before rewriting.
5. Flag any mismatch between front-half claims and downstream support.
6. Check whether figures and legends independently support the stated claim.
7. Run a compact skeptical-review pass across contribution, clarity, empirical support, evaluation completeness, and design soundness.
8. Lock canonical terminology.
9. Only after the above, rewrite for clarity and concision.

If the user asks for review only, stop after diagnosis.
If the user asks for revision, edit in the same macro-to-micro order.

## Common Failure Modes

### Front Half Stronger Than Back Half

Symptom:
- Abstract or introduction promises more than the Results show

Fix:
- downgrade the claim or add evidence
- do not hide the gap with stronger prose

### Framework Turns Into Model

Symptom:
- A benchmark, reformulation framework, or evaluation protocol gets described as if it were the predictive architecture itself

Fix:
- restate the contribution type explicitly
- distinguish the framework from the instantiated pipeline or baseline comparisons

### Metric Drop Framed As Mechanism

Symptom:
- A harsher metric is described as causal proof of a deeper mechanism

Fix:
- separate what the metric directly shows from the interpretation it suggests
- use "suggests", "is consistent with", or "implicates" when direct mechanism evidence is absent

### Figure Drift

Symptom:
- Panel letters, metrics, datasets, baselines, or numbers changed in the figure but not in the text

Fix:
- re-read the actual figure
- update text, legend, and claims together

### Terminology Drift

Symptom:
- Several labels compete for the same concept

Fix:
- choose one canonical term
- allow looser explanatory phrases only when they do not function as competing formal labels

### Premature Sentence Polishing

Symptom:
- The prose becomes smoother but the argument remains unstable

Fix:
- return to macro and structural levels first

## Output Standard

When reporting findings, prefer this order:
- macro contribution problem
- evidence-chain problem
- figure or legend inconsistency
- terminology inconsistency
- prose and formatting issues

When no major structural problems exist, say that explicitly and then move to lower-level optimization.

## Minimal Review Template

Use this compact structure when reviewing a manuscript:

- Central claim:
- Claim | Evidence | Status:
- Strongest supporting result:
- Weakest or unsupported claim:
- Reverse-outline break point:
- Figure-text mismatch:
- Terminology drift:
- Recommended next revision step:
