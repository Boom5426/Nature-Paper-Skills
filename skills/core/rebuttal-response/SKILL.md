---
name: rebuttal-response
description: Analyze, draft, revise, or audit scientific peer-review response letters and point-by-point rebuttals. Use for reviewer comments, response letters, rebuttals, revision summaries, quoted manuscript changes, replies that must align with a manuscript or Supplementary Information, and submission-ready checks of direct question-answer alignment, evidence, figures, tables, notes, panels, terminology, numbers, and internal citations. Especially useful when replies must reuse the reviewer's terms, map every sub-question to an explicit answer, report new analyses or experiments, identify exact revision locations, or distinguish mandatory fixes from optional polishing.
---

# Revise Reviewer Responses

Build reviewer replies for a busy reader. Begin every formal response with a brief expression of thanks to the reviewer. Then make every answer immediately traceable to the reviewer's exact concern: lead with what was done and found, state what it means, and identify where the manuscript changed. Do not make the reviewer infer the mapping, search across paragraphs, or read defensive prose after the answer is already clear.

## Start from the authoritative materials

1. Identify the newest response letter, manuscript, Supplementary Information, figures, tables, and result files relevant to the comment.
2. Treat the user's stated version hierarchy as binding. Do not revive text or conclusions from an older response when the user says the manuscript or SI is authoritative.
3. Read the complete reviewer comment and the complete current response before editing either.
4. Split the comment into independently answerable requests. Preserve the reviewer's own nouns and distinctions, including datasets, methods, comparison units, requested analyses, and claimed outcomes.
5. Build a private alignment matrix with one row per request:
   - reviewer's exact concern or phrase;
   - direct answer;
   - action or evidence;
   - result;
   - supported conclusion;
   - revision location;
   - essential evidence boundary, if one is genuinely required.
6. Use the matrix as an acceptance test. Every row must appear explicitly in the response; no paragraph may substitute an adjacent analysis for the requested object.
7. Never invent a result, statistic, experiment, citation, revision location, or placeholder value. Mark unavailable values explicitly or ask for the missing source.

If the task involves direct document editing, also use the relevant document skill and render the finished file for visual verification.

## Analyze before drafting

Unless the user explicitly requests only final prose, begin with a short diagnosis:

- What is the reviewer actually asking for?
- Is the concern methodological, evidential, interpretive, presentational, or terminological?
- Does it require a new experiment, a new analysis of existing results, a clarification, or only narrower wording?
- What is the strongest conclusion the available evidence supports?
- What statement in the manuscript, SI, or response must change for the reply to be credible?

Do not assume that adding an experiment is automatically the best response. Prefer the smallest action that genuinely resolves the concern, but do not use wording changes to conceal a real evidential gap.

Read [triage-and-stance.md](references/triage-and-stance.md) to classify the comment by cause and to decide whether the reply should concede, clarify, or push back. Make that decision before drafting; claim calibration applies to the stance you chose, it does not substitute for choosing one.

## Choose the response architecture by complexity

Do not impose one template on every comment.

- **Simple comment:** direct answer or action, corrected text if useful, and revision location in one compact paragraph.
- **Moderate substantive comment:** one stand-alone overview followed by two or three sections named after the reviewer's actual sub-questions, then a precise revision-location paragraph.
- **Complex multi-part major comment:** one stand-alone overview, an optional `Specifically, we:` action list, matching evidence sections in exactly the same order, and a precise revision-location paragraph.

Use an action list only when it materially helps navigation. If used, make it a true table of contents: its item count, order, concepts, and labels must match the detailed sections. Do not place a top-level action beside a lower-level result such as gene and drug analyses if both belong under one experiment.

The overview must stand alone for a reviewer who reads only the first paragraph. Its first sentence must briefly thank the reviewer. Vary the wording naturally according to the comment, for example `We thank the reviewer for this important comment`, `We appreciate the reviewer's helpful suggestion`, or `We thank the reviewer for raising this point`. Do not use the same phrase mechanically throughout the letter, add excessive praise, agree with a premise that is not accepted, or paraphrase the full comment in the thank-you sentence.

Immediately after the thank-you sentence, open the substantive response with the action, result, or direct answer that resolves the concern, not a sentence merely announcing that the concern was addressed. Follow this order whenever the evidence permits:

1. brief thanks;
2. action or experiment;
3. central result;
4. direct answer to the reviewer;
5. manuscript change.

Name detailed sections with the reviewer's question objects rather than the author's internal reasoning categories. Reuse the reviewer's exact technical terms when accurate. If the reviewer separately asks about two representations, datasets, baselines, settings, or outcomes, answer them separately.

Read [response-patterns.md](references/response-patterns.md) when drafting or substantially restructuring a reply.

## Make every paragraph reviewer-navigable

- Put the paragraph's conclusion or function in its first sentence.
- Make the first substantive sentence after the mandatory thank-you convey new information. Delete empty transitional openings such as `We directly addressed the concern that...` or a paraphrase of the comment with no action or answer.
- Make the logical link explicit; do not require the reviewer to infer why a result answers the comment.
- Match the experimental or statistical unit the reviewer is questioning. Reusing the reviewer's words is insufficient if the response tests a neighboring but different object.
- Distinguish an experimental result from the interpretation it motivates.
- Keep one main claim per paragraph.
- Use direct, familiar scientific vocabulary. Avoid newly coined labels, abstract phrases, unnecessary `transparent`, and formulaic praise.
- Always thank the reviewer in the first sentence, but do not default to `We agree that...`; gratitude does not require agreeing with every premise of the comment.
- Avoid em dashes unless the source style clearly favors them.
- Retain relevant literature, figure, table, and Supplementary Note citations during rewriting.
- Introduce each embedded figure or table with a sentence stating what question it answers before inserting it.

## Control repetition and defensive prose

- State the overall answer in the overview, the object-specific result in its corresponding section, and the manuscript changes at the end. Do not repeat the same synthesis in an action list, every subsection, a separate conclusion section, and the closing paragraph.
- Delete a standalone synthesis section when it only restates the overview and the preceding results.
- Do not append habitual concessions such as `However, this does not prove...` after a supported conclusion.
- Include a boundary only when the reviewer explicitly asks for it, omission would make the claim inaccurate, or the design creates a material risk of overinterpretation.
- Place a necessary boundary beside the exact claim it qualifies. Do not turn it into a defensive closing paragraph.
- End on the supported answer and concrete revisions, not on speculation about analyses that were not performed.

## Calibrate claims to evidence

Apply this evidence ladder:

1. **Direct observation:** `showed`, `was higher`, `remained impaired`.
2. **Run-level reproducibility:** `was reproduced across the evaluated runs`.
3. **Association:** `was associated with`, `is consistent with`.
4. **Diagnostic or intervention:** `provides evidence consistent with`, `supports a possible explanation`.
5. **Causal attribution:** use only when the design isolates the factor and credible alternatives are controlled.

Follow these recurring boundary rules:

- A diagnostic analysis can support a mechanism; it rarely proves that mechanism.
- Multiple random seeds characterize training variability. They are not automatically independent biological samples or a basis for population-level inference.
- Failure to detect a meaningful advantage does not establish statistical identity or equivalence.
- A finite hyperparameter sweep identifies the `best-performing evaluated ratio`, not a global `optimum`.
- Holding maximum path depth constant does not hold parameter sharing or effective capacity constant.
- Dataset-specific findings must name the dataset. Avoid `consistently`, `universally`, `default choice`, or broad superiority claims unless the evidence truly spans the claimed scope.
- `Mean ± s.d.` describes run-to-run variation; do not call it a confidence interval.
- Distinguish practical effect magnitude, stochastic stability, statistical uncertainty, and cross-dataset consistency.
- When sources of domain shift remain confounded, report setting-specific correlates or plausible explanations, not a complete variance or causal decomposition.
- Equal nominal loss weights do not imply equal gradient pressure.
- A disruption test shows sensitivity or dependence under that intervention; do not automatically call it effective information exchange.

State both what was controlled and what necessarily changed when that distinction is material to the claim. Preserve necessary limitations without automatically foregrounding every conceivable alternative explanation.

## Keep the response, manuscript, and SI synchronized

For each substantive claim, verify:

- the number, unit, metric name, seed count, dataset, split, comparator, and aggregation are exact;
- the manuscript contains the promised revision;
- the SI contains enough methodological detail to support any analysis described at length in the response;
- figure, table, note, and panel numbers exist and match their actual content;
- quoted revised text matches the document verbatim;
- terminology is stable across the overview, detailed reply, manuscript, SI, and captions;
- the response does not generalize beyond the revised manuscript;
- every embedded figure is introduced in text before it appears and has a meaningful callout;
- no figure, table, or note is orphaned, and no citation points to a nonexistent or wrong panel.
- each revision-location statement says what changed there, for example: Results report the finding, Methods describe the analysis, Discussion revises the interpretation;
- the overview, optional action list, section headings, detailed evidence, and closing revision paragraph preserve the same one-to-one mapping.

Use [final-audit.md](references/final-audit.md) for a whole-letter or submission-ready review.

## Match the requested output mode

### Diagnose a comment

Lead with the verdict: what is already adequate, what is unsupported, and what must change. Then propose the response logic. Do not draft a full reply unless requested.

### Draft or revise a reply

Give a brief analysis first, followed by complete ready-to-use prose. If only one sentence or paragraph is requested, return only that unit after the short analysis. Use a writing block when the task is purely copy-ready prose and that capability is available.

### Audit a response letter

Separate findings into:

1. **Must change:** factual errors, unsupported claims, contradictions, missing promised revisions, wrong citations or panels, placeholders, duplicated text, and submission-breaking layout issues.
2. **Strongly recommended:** material clarity or boundary improvements that reduce reviewer risk.
3. **Optional:** stylistic polishing only.

If the user asks only for mandatory changes, report only category 1 and explicitly say when none remain.

## Preserve useful negative results

Do not hide or overcorrect an unfavorable analysis. Reframe it precisely:

- explain what uncertainty or hypothesis the analysis addresses;
- report the observed result without inflation;
- state what conclusion is weakened or narrowed;
- identify the remaining practical implication;
- avoid claiming failure proves irrelevance.

The goal is a credible revision record, not a uniformly positive story.
