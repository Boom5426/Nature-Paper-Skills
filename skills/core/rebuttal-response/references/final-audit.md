# Final Response-Letter Audit

## Contents

1. Source control
2. Comment coverage
3. Evidence and claim boundaries
4. Cross-document consistency
5. Figures, tables, notes, and citations
6. Editorial and layout integrity
7. Build and revision-marking integrity
8. Final reporting

## 1. Source control

- Confirm the exact latest response letter, manuscript, SI, figures, tables, and result files.
- Exclude superseded drafts from substantive judgment.
- Verify that every new analysis in the reply exists in an authoritative source.
- Search for unresolved placeholders, tracked alternatives, comments, and temporary labels.

## 2. Comment coverage

For every reviewer comment, verify that the reply:

- answers the actual request rather than a nearby issue;
- states the action taken;
- reports the central result or clarification;
- explains how the result changes or supports the manuscript;
- identifies the revision location;
- states the inferential boundary when needed.

Check that the opening summary and the detailed response tell the same story.

## 3. Evidence and claim boundaries

Search for high-risk words and inspect each occurrence:

```text
prove, demonstrate, cause, isolate, solely, fair, intrinsic, optimal,
optimum, universally, consistently, robust, default, meaningful,
significant, identical, equivalent, capacity, mechanism
```

Then verify:

- causal language is supported by design;
- finite searches are not called global optima;
- dataset scope is explicit;
- run-level variability is not population uncertainty;
- lack of evidence is not stated as equivalence;
- nominal weights are not called equal optimization pressure;
- architecture controls do not overstate what was held constant;
- diagnostic measures are defined and normalized when required;
- practical significance is not inferred from reproducibility alone.

## 4. Cross-document consistency

Check every promised revision against the manuscript and SI:

- exact wording or faithful equivalent appears;
- Results, Methods, Discussion, Abstract, captions, and SI do not retain an older broader claim;
- terminology and abbreviations are uniform;
- dataset names and modality suffixes are exact;
- sample, unit, and entity counts agree at every level the paper reports;
- metric names, values, signs, ranges, units, and precision agree;
- seed count, split, checkpoint selection, and training budget agree;
- the response does not contain more methodological detail than the SI can support;
- the response does not cite a Note or figure for a result it does not contain.

## 5. Figures, tables, notes, and citations

Create an object-to-reference matrix for all embedded or cited objects.

For each object, verify:

- it exists;
- the number and panel are correct;
- the cited panel contains the claimed result;
- top/bottom and left/right references match the rendered figure;
- it is introduced in text before an embedded image appears;
- the caption stays with the object;
- every new figure or note has at least one meaningful entry point;
- no nonexistent panel is invented for an unpanelled figure;
- figure captions and response text use the same dataset and metric names;
- literature references are retained and bibliographically correct.

Do not count a caption as the only substantive callout for its own figure.

## 6. Editorial and layout integrity

Search mechanically for:

- duplicated adjacent sentences or phrases;
- repeated words from partial rewrites;
- inconsistent numbering and heading styles;
- missing conjunctions or punctuation in action lists;
- stale cross-references;
- smart-quote or symbol corruption;
- `approximately` where exact values are available;
- unexplained abbreviations;
- contradictory statements between summary and detail.

Render the complete document and inspect every page for:

- clipped text or figures;
- overlap;
- orphaned headings;
- split captions;
- images appearing before their callout;
- excessive blank space caused by object movement;
- inconsistent highlighting or revision colors;
- page-break artifacts.

## 7. Build and revision-marking integrity

Run these when the revised manuscript is a compiled document. Merged from the former
`paper-revision` skill.

- The revised manuscript compiles without new errors, and no new undefined reference or citation
  warning appeared relative to the previous version.
- Every citation added during the revision has a matching bibliography entry, and that entry was
  verified against the actual source rather than generated.
- The revised manuscript still satisfies the venue page or word limit, including any limit that
  counts references and figures.
- Every claimed revision is visibly marked in the marked copy, and a clean copy exists separately.
- The marking convention matches the venue: Nature-family revisions are conventionally red, many
  conference and society venues expect blue. Use one convention throughout, since a document with
  two revision colors reads as two revision rounds.
- No revision marking survives in the clean copy, and no unmarked revision survives in the marked
  copy.
- Figure, table, equation, and section numbers were re-resolved after the edits. A renumbered
  object invalidates every response sentence that cites its old number.

A passing compile is not evidence that the revision is correct. It only means the document builds.

## 8. Final reporting

Lead with one of these verdicts:

- `Submission-ready after the mandatory changes below.`
- `No submission-blocking issue remains.`
- `The response is not yet submission-ready because...`

Report exact locations, current text, and replacement text for every mandatory issue. Separate strong recommendations and optional edits only when the user requested a full audit. Do not bury a factual or citation error among stylistic suggestions.
