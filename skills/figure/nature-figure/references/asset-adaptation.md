# Plotting Asset Adaptation

Use this reference when reusing an example script, a preview image, or a user-provided plotting script. Treat examples as visual and structural starting points, not as evidence that a script is compatible with new data.

This repository does not vendor the worked-example asset bundle. `references/demos.md` says where those scripts and previews live and how to read them; everything below applies to any candidate you obtain, including a user's own template collection.

## Choose the reuse level

Assign every candidate to one of four levels before editing it:

| Level | Use when | Allowed changes |
|---|---|---|
| Exact reuse | Scientific meaning, data shape, transformations, and backend all match | Input path, labels, and output prefix only |
| Structural adaptation | Scientific meaning and dimensionality match, but field names or group labels differ | Explicit field mapping plus documented transform guards |
| Style-only inheritance | The plot family is useful but the data structure or statistic differs | Palette, typography, spacing, marker, legend, and annotation conventions only |
| Build anew | The candidate answers a different question or would require replacing its statistical logic | Do not force the template; implement the confirmed figure contract directly |

Do not call a script production-ready merely because it renders its bundled example.

## Inspect before mapping

1. Open the companion preview when one exists. If the candidate is an upstream demo, read the script itself rather than assuming the preview matches it.
2. State what the candidate actually displays: dimensionality, mark type, grouping, statistic, uncertainty, transforms, and annotations.
3. State what the requested panel must answer.
4. Reject structural reuse when those meanings differ. A 2D joint-density plot is not a reusable implementation of several 1D marginal densities, and a benchmark bar chart is not automatically a valid small-sample biological comparison.

## Map the data contract

Write an explicit mapping before changing code:

```text
template field -> user field -> role -> units -> allowed values
group field    -> user field -> category order
replicate unit -> source rows/images -> biological or technical
uncertainty    -> source field or calculation -> definition
```

Confirm ambiguous mappings with the user. Never choose convenient columns silently. Keep identifiers separate from measurements and preserve the requested category order unless a scientifically justified ordering is declared.

## Guard transformations

Check every inherited transformation against the new data:

- Log axes and logarithms require strictly positive values unless a declared signed-log or pseudocount method is scientifically justified.
- Ratios and normalized values require finite denominators and a defined zero-denominator policy.
- Square-root transforms require non-negative inputs.
- Min-max scaling requires non-constant finite ranges.
- Binning and density estimation require enough distinct observations; record bin or bandwidth choices.
- Correlation, PCA, clustering, and statistical annotations require explicit missing-value handling and an appropriate replicate unit.

If a guard fails, change the transformation only when the scientific meaning remains valid and record the change. Otherwise use style-only inheritance or build anew.

## Preserve data integrity

- Use all supplied observations and requested variables by default.
- Do not downsample for aesthetics or rendering speed. Use rasterization, hexbin/density marks, transparent points, aggregation with a stated rule, or backend-native large-data rendering.
- If the analysis requires filtering, record the exact predicate and before/after row, column, replicate, or image counts.
- When the user explicitly requests sampling, record the method, sample size, seed, and whether sampling changes any inferential claim.
- Never leave simulated values in a production deliverable. Isolate demos behind an explicit demo flag or a separate example file.

## Adapt without erasing provenance

Copy the candidate into the task workspace before editing. Keep source assets unchanged. Preserve license and attribution notices, but do not expose private local paths or private template identifiers in generated figures, legends, manuscript text, or user-facing reports.

Record the reuse level and source category in internal QA notes. The privacy rules that govern how a private template collection may be described in user-facing output are in `static/core/stance.md` and `references/r-template-index.md`; this file does not restate them.

The adaptation method in this reference incorporates portable ideas from the Apache-2.0 `academic-figure-skill` workflow while replacing its path-bound runners and project-specific assumptions.

## Validate and deliver

1. Run the adapted script with representative real input using the selected backend.
2. Run `python scripts/validate_figure.py path/to/script.py` or the corresponding `.R` file.
3. Run `python scripts/audit_pdf_text.py path/to/panel_a.pdf --min-pt 5` on **each panel PDF**, not on the composite. A composite assembled by placing scaled panel PDFs reports `NOT AUDITABLE` (exit 4) by design: the type size inside a placed form cannot be recovered from the page. Run `python scripts/audit_figure_collisions.py path/to/figure.pdf --json-out path/to/figure.collision-audit.json` on the composite, which is where collisions actually appear.
4. Treat static and geometry validation as preflight only; fix collision FAIL findings and review every WARN, but do not infer statistical correctness or complete visual quality from a pass. A run that could not check something (missing runtime, unparsable file) is not a pass; report it as unchecked.
5. Inspect SVG/PDF text editability, raster resolution, clipping, ambiguous overlays, color accessibility, and readability at final physical size.
6. Include the field mapping, exclusions, transform changes, collision report, and remaining caveats in the QA notes.

The export settings themselves, the pre-submission checklist, and the journal file-format contract are not repeated here: use `references/qa-contract.md` for the checklist and export blocks, and `references/nature-article-requirements.md` when the target is flagship *Nature*.
