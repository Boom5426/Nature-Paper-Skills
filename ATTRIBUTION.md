# Attribution

This repository assembles and curates an applied manuscript-skill stack from a working local environment.

## Directly Adapted Or Renamed From Existing Local Skills

- `results-analysis` was adapted from `inno-experiment-analysis`
- `paper-reviewer` was adapted from `inno-paper-reviewer`
- `reference-audit-guide` was adapted from `inno-reference-audit`
- `conference-paper-writing` was adapted from `ml-paper-writing`
- `academic-presentations` was adapted from `making-academic-presentations`

## Integrated From `Yuan1z0825/nature-skills` (Apache-2.0)

Source: https://github.com/Yuan1z0825/nature-skills

- `skills/figure/nature-figure` was vendored from the upstream `nature-figure` skill. The roughly 30 MB demo, gallery, and chart-atlas asset bundle was removed to keep this repository lean; it lives upstream. Only asset references and sibling-skill cross-references were changed; the figure-making logic is unmodified.
- `skills/core/stats-reporting-audit` corresponds to the upstream `nature-statistics` skill, normalized to this repository's naming and cross-references.
- The following upstream material was merged into existing skills rather than added as standalone skills:
  - the FAIR/DataCite metadata checklist and Chinese-author alignment notes from `nature-data`, merged into `skills/core/data-availability/references/`;
  - the citation severity matrix and the volume-year versus DOI-year check from `nature-ref-verifier`, merged into `skills/core/citation-verifier`;
  - the LaTeX float and layout reference from `nature-polishing`, merged into `skills/core/scientific-writing/references/latex-layout.md`.

## Integrated From The Claude Science Skill Pack (Apache-2.0)

- `skills/core/scientific-prose-style` was vendored from the Claude Science `scientific-prose-style` skill; figure cross-references were repointed to this repository's `figure-planner`.
- `skills/figure/figure-style` was vendored from the Claude Science `figure-style` skill; the render-then-verify loop and helper loading were de-coupled from the Operon host runtime so the skill runs in a plain install. The correctness checklist is unchanged.
- The Nature-style color palette merged into `skills/core/figure-planner` derives from the Claude Science `nature-palette` skill (original source: github.com/Boom5426/Awesome-Virtual-Cell 配色.ipynb).

## Additional Notes

- `academic-researcher` preserves the role and broad intent of an earlier imported skill and was normalized for this repository.
- Several workflow refinements in the core manuscript skills were shaped by iterative manuscript work on `Nature`-style papers and by public paper-writing guidance that informed the local skill stack over time.

This file is intentionally conservative. If you later want per-skill provenance, add a short `ORIGIN.md` inside each adapted skill directory.
