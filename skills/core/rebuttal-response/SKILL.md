---
name: rebuttal-response
description: >-
  Author-side reviewer response workflow. Triage each comment by cause, decide whether to concede,
  clarify, or push back, calibrate every claim to the evidence, and audit the drafted letter before
  it is sent. Use when reviewer comments exist and a point-by-point response plus aligned manuscript
  edits are needed, and whenever a reply must stay inside what the data actually support: seeds
  versus independent samples, a finite sweep versus an optimum, a diagnostic versus a mechanism,
  absence of difference versus equivalence, dataset-specific versus general superiority, or mean
  plus or minus s.d. versus a confidence interval. Also covers overview-first response
  architecture, evidence-ladder wording substitutions, honest handling of negative results, and a
  submission-ready audit of numbers, figures, panels, notes, terminology, and response to
  manuscript to Supplementary synchronization.
---

# Revise Reviewer Responses

Build reviewer replies as an evidence chain, not as defensive prose. Make the reviewer understand, in this order: what was done, what was found, what changed, and what remains outside the evidence.

## Where this sits

This skill owns the whole author-side response job: triage, stance, claim calibration, and the
final audit. It does not restructure the manuscript itself.

- `manuscript-optimizer` when a reviewer comment exposes an unstable claim hierarchy or evidence
  chain. Fix the manuscript there first, then write the reply against the revised text.
- `stats-reporting-audit` when the disputed point is the statistical reporting itself rather than
  its wording.
- `claim-source-verification` when a reviewer disputes whether a cited source supports the sentence
  citing it, and `citation-verifier` when the bibliography artifact is at fault.
- `scientific-prose-style` for a final sentence-level pass on the finished letter.
- `paper-compilation` conventions apply to the revised manuscript build; see the build checks in
  `references/final-audit.md`.

## Start from the authoritative materials

1. Identify the newest response letter, manuscript, Supplementary Information, figures, tables, and result files relevant to the comment.
2. Treat the user's stated version hierarchy as binding. Do not revive text or conclusions from an older response when the user says the manuscript or SI is authoritative.
3. Read the complete reviewer comment and the complete current response before editing either.
4. Build a compact evidence ledger:
   - reviewer request;
   - action taken;
   - result or textual clarification;
   - document location;
   - inferential limit.
5. Never invent a result, statistic, experiment, citation, revision location, or placeholder value. Mark unavailable values explicitly or ask for the missing source.

If the task involves editing the response letter or manuscript on disk, read the file before editing it, keep the marked copy separate from the clean copy, and render the finished file (`paper-compilation` for LaTeX) so the result can be checked visually. Never edit a file you have not read.

## Analyze before drafting

Unless the user explicitly requests only final prose, begin with a short diagnosis:

- What is the reviewer actually asking for?
- Is the concern methodological, evidential, interpretive, presentational, or terminological?
- Does it require a new experiment, a new analysis of existing results, a clarification, or only narrower wording?
- What is the strongest conclusion the available evidence supports?
- What statement in the manuscript, SI, or response must change for the reply to be credible?

Do not assume that adding an experiment is automatically the best response. Prefer the smallest action that genuinely resolves the concern, but do not use wording changes to conceal a real evidential gap.

Read [triage-and-stance.md](references/triage-and-stance.md) to classify the comment by cause and to decide whether the reply should concede, clarify, or push back. Make that decision before drafting; claim calibration applies to the stance you chose, it does not substitute for choosing one.

## Use the default response architecture

For a substantive comment, preserve this structure:

1. **Overview paragraph.** State the measure taken, the central result, and the revised conclusion. It must stand alone for a reviewer who reads only this paragraph.
2. **Action list.** Introduce with `Specifically, we:` and list the concrete revisions or analyses in the same order as the detailed response.
3. **Numbered evidence sections.** Give each section a direct topic sentence such as `We first clarified...`, `We next tested...`, or `Taken together...`. Separate scope, design, result, interpretation, and boundary when that helps navigation.
4. **Revision locations and exact text.** Identify where the changes appear and quote the revised manuscript or SI language when useful.
5. **Closing boundary.** End with the conclusion the evidence supports and, when needed, what it should not be interpreted as proving.

Compress this architecture for a simple minor comment. Do not force a long list or multiple subsections when one direct paragraph fully answers the concern.

Read [response-patterns.md](references/response-patterns.md) when drafting or substantially restructuring a reply.

## Make every paragraph reviewer-navigable

- Put the paragraph's conclusion or function in its first sentence.
- Make the logical link explicit; do not require the reviewer to infer why a result answers the comment.
- Distinguish an experimental result from the interpretation it motivates.
- Keep one main claim per paragraph.
- Use direct, familiar scientific vocabulary. Avoid newly coined labels, abstract phrases, unnecessary `transparent`, and formulaic praise.
- Do not default to `We agree that...`; acknowledge the concern briefly and move to the action.
- Avoid em dashes unless the source style clearly favors them.
- Retain relevant literature, figure, table, and Supplementary Note citations during rewriting.

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

State both what was controlled and what necessarily changed. If architecture, parameter sharing, feature construction, preprocessing, or effective capacity differs, preserve that limitation in the reply.

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

Use [final-audit.md](references/final-audit.md) for a whole-letter or submission-ready review.

## Match the requested output mode

### Diagnose a comment

Lead with the verdict: what is already adequate, what is unsupported, and what must change. Then propose the response logic. Do not draft a full reply unless requested.

### Draft or revise a reply

Give a brief analysis first, followed by complete ready-to-use prose. If only one sentence or paragraph is requested, return only that unit after the short analysis. When the deliverable is purely copy-ready prose, keep the analysis to a few lines and put the prose in a single fenced block so it can be copied without edits.

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

---

*Provenance: distilled from a completed major-revision cycle on a computational-biology benchmark manuscript, then generalized. The triage and stance layer in `references/triage-and-stance.md` is this repository's original `rebuttal-response` body.*
