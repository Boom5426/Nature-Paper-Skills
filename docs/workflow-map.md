# Workflow Map

The default manuscript path in this repository is:

```text
1. paper-bootstrap
2. nature-portfolio-playbook
3. refresh project_truth / result_summary / paper_handoff
4. scientific-writing or manuscript-optimizer
5. figure-planner, then nature-figure to produce the figure and figure-style to check it
6. results-section-revision when Results is scientifically stable but still reads as jumpy or figure-by-figure
7. stats-reporting-audit for statistical-reporting integrity
8. citation-verifier for bibliography hygiene, then claim-source-verification for claim-to-evidence support
9. data-availability
10. scientific-prose-style for a final sentence-level prose pass
11. submission-audit
12. rebuttal-response
```

## Review, Survey, And Perspective Path

A Review is not a short research article and does not follow the path above.
Its failure mode is becoming a different Review, not overclaiming past its data.

```text
1. review-article-architecture   establish the governing plan document first
2. nature-portfolio-playbook     venue and article-type fit
3. draft-marker-discipline       set up the marker system before drafting starts
4. scientific-writing            draft, sourcing in step with the prose
5. citation-verifier             bibliography hygiene, then
   claim-source-verification     adversarially verify that each source supports its claim
6. figure-planner, then nature-figure and figure-style
7. review-article-architecture   drift audit, before any compression pass
8. draft-marker-discipline       measure length; triage what remains open
9. scientific-prose-style        sentence-level pass, last
10. submission-audit
```

Run step 7 before step 9, never after. Polishing a drifted draft makes the drift
harder to see, not easier.

## Routing Rule

- Use `scientific-writing` when the section mostly needs to be drafted or rewritten in prose.
- Use `manuscript-optimizer` when the paper's story, evidence chain, figure logic, or terminology may be unstable.
- Use `results-section-revision` when the remaining problem is local Results architecture rather than claim selection.
- Use `data-availability` when repository plans, accession identifiers, source-data coverage, or restricted-data wording are the bottleneck.
- Use `figure-planner` to decide what each figure argues, then `nature-figure` to render it and `figure-style` to check correctness and legibility before export.
- Use `stats-reporting-audit` when the bottleneck is statistical-reporting integrity: independent-unit `n`, pseudoreplication, multiple-comparison correction, or figure-legend statistics.
- Use `scientific-prose-style` for a final sentence-level pass on already-stable prose (em-dash budget, hedging, sentence rhythm), not as a substitute for fixing an unstable claim first.
- Use `citation-verifier` when the problem is the bibliography as an artifact: duplicate keys, missing fields, DOI syntax, cited-but-undefined, toolchain and style failures. Use `claim-source-verification` when the problem is whether a source supports the sentence citing it. They stack, in that order; a clean bibliography audit says nothing about claim support, and in one measured run 55 of 139 proposed sources were rejected with none of them fabricated.
- Use `review-article-architecture` when the manuscript is a Review, survey, or Perspective rather than a research article, or whenever a piece written across many sessions may no longer match its brief. Use `manuscript-optimizer` for research articles.
- Use `draft-marker-discipline` before a batch pass over open markers, before quoting a manuscript's length, before removing superseded material from the tree, and before making the same edit across many files with a script.

## Working Principle

Do not polish sections written from stale memory.

After experimental, statistical, or figure updates, refresh:
- `notes/project_truth.md`
- `notes/result_summary.md`
- `notes/paper_handoff.md`

before attempting heavy manuscript revision.
