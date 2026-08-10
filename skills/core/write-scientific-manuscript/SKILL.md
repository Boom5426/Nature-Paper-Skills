---
name: write-scientific-manuscript
description: >-
  Diagnose and repair the clarity and logic of manuscript prose, journal-agnostic. Use when a
  passage is technically correct but hard to follow: buried topic sentences, missing logical
  bridges, ambiguous referents, abstract noun chains, overloaded sentences, incomplete comparisons
  with no stated dataset or metric or direction, scope qualifiers placed too far from the claim,
  and invented or inflated terminology that should have been an ordinary word. Also covers writing
  for a broad scientific reader without losing precision, section-by-section logic patterns,
  paragraph-level reverse outlines, and keeping observation separate from interpretation. This is
  the layer between structure and punctuation: use manuscript-optimizer when the claim hierarchy
  itself is unstable, and scientific-prose-style for the final sentence-level pass.
---

# Write Scientific Manuscripts

Make the science easy to follow before making the prose elegant. Optimize in this order: scientific logic, reader comprehension, evidential precision, then style.

## Where this sits

This skill owns clarity and logic diagnosis. It carries no house style and no punctuation budget.

- `manuscript-optimizer` when the problem is above the prose: the claim hierarchy, evidence chain,
  or figure logic is unstable. Fix that first. Polishing a paragraph whose scientific role is wrong
  wastes the edit.
- `scientific-writing` when a section needs drafting or rewriting into full paragraphs, or when the
  task names a citation style or a reporting guideline.
- `scientific-prose-style` last, for punctuation and rhythm. This file deliberately carries no
  em-dash rule; that skill owns it, and its cap is at most one em dash per paragraph and none in
  the abstract.
- `results-section-revision` when only Results subsection flow and paragraph openings need repair.
- `review-article-architecture` when the piece is a Review, survey, or Perspective.
- `rebuttal-response` when the prose is a reply to reviewers rather than manuscript text. The
  claim-calibration ladder there is the same one used below.

## Establish the intended meaning

Before rewriting, determine:

1. What single point must the reader understand?
2. What information must the reader already know for that point to make sense?
3. What evidence supports it?
4. What inference is justified, and what remains uncertain?
5. Why does the point matter at this location in the manuscript?

Do not polish a sentence whose scientific role is unclear. If necessary, briefly diagnose the logic before drafting.

For file-based revision, identify the authoritative version and preserve citations, figure references, terminology, numbers, and formatting. Read the file before editing it, and rebuild the document when the edit could disturb layout, floats, or cross-references.

## Write for a broad scientific reader

- Assume intelligence but not local project knowledge.
- Introduce the biological or methodological problem before project-specific machinery.
- Define an uncommon term when first needed, not several paragraphs earlier.
- Make referents explicit. Replace ambiguous `this`, `these`, and `it` when the reader could plausibly choose the wrong antecedent.
- State the logical connection instead of asking the reader to infer it.
- Prefer a concrete subject and verb over abstract noun chains.
- Preserve necessary technical detail, but move secondary detail away from the sentence carrying the main claim.

Broad accessibility does not mean removing precision. Keep exact distinctions when they change the scientific meaning.

## Put logic first

Give each paragraph one main job. Use this default progression when applicable:

1. **Topic sentence:** state the paragraph's point or function.
2. **Necessary setup:** provide only the context needed to understand the evidence.
3. **Evidence or reasoning:** report the relevant result, comparison, or limitation.
4. **Interpretation:** explain what the evidence means at the supported strength.
5. **Connection:** show why the next paragraph or section follows.

Do not force all five elements into every paragraph. Do require the first sentence to orient the reader. Avoid paragraphs that begin with implementation detail and reveal their purpose only at the end.

Build explicit bridges between adjacent claims. A valid sentence can still be misplaced if it does not answer the question raised immediately before it.

Read [section-logic.md](references/section-logic.md) when restructuring a section, an abstract, or a full manuscript.

## Prefer the simplest accurate language

- Use familiar scientific words when they express the same meaning.
- Prefer short, direct constructions, but vary sentence length naturally.
- Keep one principal claim per sentence unless two claims are inseparable.
- Use active voice when it makes the actor or logic clearer; use passive voice when the procedure or result is the natural focus.
- Remove throat-clearing, duplicated meaning, ornamental transitions, and empty intensifiers.
- Avoid compressed strings of nouns and stacked modifiers.
- Do not replace a clear ordinary word merely to sound more sophisticated.
- Do not use a fragmentary series of very short sentences when the causal or contrastive relation is clearer in one well-formed sentence.

Aim for the mature, restrained vocabulary common in strong general-science journals. Treat `Nature style` as clarity, economy, reader guidance, and calibrated claims, not as a list of fashionable words.

Read [language-guide.md](references/language-guide.md) when performing sentence-level revision or terminology cleanup.

## Do not invent terminology casually

Use a new label only when all of the following are true:

- the concept is genuinely distinct from established terms;
- the distinction is important more than once;
- existing terminology would be misleading or unwieldy;
- the label can be defined in one direct sentence;
- the same label will be used consistently afterward.

Otherwise, describe the phenomenon directly. Do not capitalize, hyphenate, abbreviate, or name an ordinary analytical step to manufacture novelty. Search the manuscript and, when needed, the relevant literature before asserting that a term is standard or introducing a replacement.

Preserve established field terminology even when it is less elegant than a newly invented alternative. If the source uses an unclear coined term, explain the issue and propose a conventional replacement rather than silently creating another term.

## Calibrate claims to evidence

- Report observations before interpretations.
- Use `show` for a result directly established by the analysis; use `suggest`, `is consistent with`, or `may reflect` for supported interpretations.
- Do not turn association, sensitivity, prediction, or diagnostic evidence into mechanism or causation.
- Scope conclusions to the evaluated datasets, tasks, conditions, models, or search space when needed.
- Avoid `universal`, `optimal`, `robust`, `general`, `fundamental`, `comprehensive`, and `state-of-the-art` unless the design supports the full claim.
- Distinguish an absence of evidence from evidence of absence.
- Retain negative or mixed results and explain what they narrow.

Never improve flow by deleting a scientifically important limitation or qualifier. Instead, place the qualifier where it constrains the claim without obscuring the main message.

## Revise in passes

Use this order for substantial revision:

1. **Scientific function:** identify the role of each section and paragraph.
2. **Argument structure:** reorder, merge, or split material so each claim follows from the preceding question or evidence.
3. **Reader prerequisites:** supply missing definitions and remove premature detail.
4. **Claim boundaries:** align verbs and qualifiers with the evidence.
5. **Terminology:** use conventional terms consistently and remove unnecessary labels or abbreviations.
6. **Sentence clarity:** simplify syntax, repair referents, and remove redundancy.
7. **Continuity:** check transitions, repeated claims, citation placement, and figure callouts.
8. **Read-aloud pass:** revise sentences that remain difficult to parse on first reading.

Do not begin by swapping individual words if the paragraph's logic or order is wrong.

## Adapt to the manuscript section

- **Title:** state the central contribution or finding without claiming more breadth than the study supports. Avoid unexplained acronyms and fashionable umbrella terms that obscure the actual task.
- **Abstract:** follow problem → unresolved gap → approach → central evidence → bounded implication. Make it understandable without the main text.
- **Introduction:** move from broad problem to specific unresolved question, explain why existing approaches do not resolve it, then state what this study does. Do not write a catalogue of prior methods.
- **Results:** lead with the question or purpose, report the result, then give a proportionate interpretation. Keep Methods detail only when needed to understand the comparison.
- **Discussion:** begin with the main advance, interpret rather than repeat the Results, compare with prior work, state limitations, and end with a concrete implication rather than generic optimism.
- **Methods:** favor exact, reproducible description over rhetorical flow. Define data, preprocessing, splits, models, objectives, metrics, statistics, and selection procedures unambiguously.
- **Figure legends:** make the figure interpretable without the Results text; define panels, groups, units, statistics, sample sizes, and visual encodings without adding unsupported interpretation.

## Match the requested output

Unless the user requests prose only, provide:

1. a short diagnosis of the main logical or language problems;
2. complete ready-to-use revised text;
3. brief notes only for choices that materially affect scientific meaning.

When revising a whole section, preserve LaTeX, citation keys, italicization, symbols, and figure references unless asked to change them. Do not fabricate citations or silently drop citation placeholders.

When auditing, separate:

- **Must change:** incorrect logic, unsupported claims, ambiguous scientific meaning, inconsistent terminology, broken references, or language that materially misstates the evidence.
- **Recommended:** substantial improvements to reader comprehension or narrative continuity.
- **Optional:** preference-level polishing.

If the user asks only for mandatory changes, report only those and explicitly state when none remain.

---

*Provenance: distilled from a completed revision cycle on a computational-biology manuscript, then generalized. Cross-references adapted to this repository's skills.*
