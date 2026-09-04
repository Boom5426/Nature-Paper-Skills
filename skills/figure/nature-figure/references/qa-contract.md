# QA Contract

Use this before final delivery, before a revision package, and whenever the figure
contains microscopy, blots, gels, clinical subgroup analysis, or statistical claims.
Journal rules change, so verify the latest target journal author guide for final
submission. The values below are conservative defaults for Nature-family style work.

## Current official references to verify

- Nature research figure guide: `https://research-figure-guide.nature.com/`
- Nature building/exporting panels: `https://research-figure-guide.nature.com/figures/building-and-exporting-figure-panels/`
- Nature preparing figures/specifications: `https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/`
- Nature initial submission and statistics guidance: `https://www.nature.com/nature/for-authors/initial-submission`
- Nature formatting guide: `https://www.nature.com/nature/for-authors/formatting-guide`
- Journal of Cell Biology figure/video guidelines for microscopy-oriented image QA: `https://rupress.org/jcb/pages/fig-vid-guidelines`
- Elsevier/Cell-family image-manipulation baseline: `https://www.sciencedirect.com/journal/the-cell-surface/publish/guide-for-authors`

## Run the checks, do not only read them

Most rows in the checklist below have an executable counterpart in `scripts/`.
Run them; a checklist ticked by eye is how a 4.2 pt tick label reaches a reviewer.

```bash
# 1. Before rendering: source preflight (sizes, fonts, exports, axis integrity)
python3 scripts/validate_figure.py my_figure.py

# 2. After export, per panel: is any printed text below the journal minimum?
python3 scripts/audit_pdf_text.py fig02a_scatter.pdf --min-pt 5

# 3. After assembly: text collisions, strokes through text, text clipped by the page
python3 scripts/audit_figure_collisions.py fig02.pdf --json-out fig02.collision-audit.json

# 4. Multi-panel: do the panels a reader perceives as aligned actually align?
python3 scripts/audit_panel_alignment.py fig02.layout.json
```

**Point each tool at the artifact it can read.** `audit_pdf_text.py` recovers the
printed type size from the page's own transforms, so it must see the per-panel PDFs
exported at true print size. A composite assembled by placing scaled panel PDFs
reports `NOT AUDITABLE` rather than guessing. `audit_figure_collisions.py` is the
opposite: collisions only exist once the panels are on one page, so it wants the
composite.

**The exit-code contract, shared by every tool here:**

| Code | Meaning | Is it a pass? |
|---|---|---|
| 0 | PASS, the check ran and the figure is acceptable | yes |
| 1 | FAIL, the check ran and found a blocking problem | no |
| 2 | ERROR, usage or I/O problem; nothing was audited | no |
| 3 | NOT RUN, a required dependency is absent | no |
| 4 | NOT AUDITABLE, the input cannot answer this question | no |

Codes 2, 3 and 4 mean the figure is **unchecked**, not clean. A wrapper that
branches on `returncode != 1` will ship an unaudited figure, and an audit that
cannot say "I could not check this" is worse than no audit. Record the state you
actually got in the QA notes, including NOT RUN and NOT AUDITABLE.

Two supporting modules carry rules that are otherwise only prose here:
`scripts/figure_source_data.py` loads the table behind a quantitative panel and
writes a `<figure>.qa.json` recording rows used, rows excluded and why, and a hash
of the source file, which is what makes the source-data row below checkable rather
than asserted. `scripts/figure_safety.py` refuses an interpolation on a grid where
interpolation is ambiguous, and refuses to place a value label on an axis scale it
was not given, instead of returning a plausible number.

---

## Pre-submission checklist

| Check | Pass condition |
|---|---|
| Core conclusion | One-sentence claim exists and every panel maps to it |
| Archetype | Figure has a declared archetype and panel hierarchy |
| Backend exclusivity | The selected backend produced all plotting, previews, exports, and visual QA renders |
| Final size | Single-column about 89 mm or double-column about 183 mm, height not above target journal limit |
| Text size | Body/tick/legend text is readable at final size, usually 5-7 pt for dense journal figures |
| Panel labels | Lowercase, bold, near top-left, typically 8 pt at final size |
| Editable text | SVG/PDF text remains editable; no outlined text unless unavoidable for special symbols |
| Font | Arial/Helvetica/sans-serif fallback is used consistently |
| Color | No rainbow color maps; red/green is not the only encoding; grayscale print remains interpretable |
| Legend strategy | Shared or direct labels where possible; no repeated redundant legends |
| Statistics | `n`, biological/technical repeat definition, center, spread, test, correction, and exact comparison are documented |
| Source data | Quantitative panels can be traced to a clean CSV/TSV/XLSX or script output |
| Raster resolution | Photos/microscopy are high-resolution enough for final size; line art uses vector where possible |
| Microscopy scale | Scale bar is present, calibrated, and not only a magnification factor |
| Image integrity | Crop, contrast, pseudo-color, stitching, reuse, and raw-file provenance are recorded |
| Export bundle | Script, source data, SVG, PDF, TIFF/PNG preview, and QA notes are delivered together when requested |

## Statistics legend minimum

For each quantitative panel, capture:

```text
n definition:
biological replicates:
technical replicates:
center statistic:
spread/interval:
test:
multiple-comparison correction:
p-value display:
source-data file:
```

For machine-learning/model figures, also capture:

```text
train/validation/test split:
number of seeds or folds:
metric definition:
confidence interval or variability definition:
baseline definition:
```

## Image-integrity minimum

For each image panel, capture:

```text
raw file:
processed file:
crop:
brightness/contrast/gamma:
pseudo-color:
scale calibration:
stitching:
reuse in other figures:
quantification link:
```

Global adjustments are generally safer than local selective edits. If an adjustment
changes the visibility of relevant background or bands, flag it instead of silently
normalizing it away.

## Export checks

Run only the export block for the selected backend. If that backend is unavailable,
stop and report the missing runtime/package instead of producing a substitute export
with the other language.

### Python

```python
import matplotlib as mpl
mpl.rcParams["svg.fonttype"] = "none"
mpl.rcParams["pdf.fonttype"] = 42
fig.tight_layout(pad=0.4)          # budget margins here, not at save time
fig.savefig("figure.svg")          # no bbox_inches="tight": it re-crops the
fig.savefig("figure.pdf")          # canvas and the printed size stops matching
fig.savefig("figure.tiff", dpi=600)
```

### R

```r
svglite::svglite("figure.svg", width = width_mm / 25.4, height = height_mm / 25.4)
print(plot)
dev.off()

grDevices::cairo_pdf("figure.pdf", width = width_mm / 25.4, height = height_mm / 25.4, family = "Arial")
print(plot)
dev.off()

ragg::agg_tiff("figure.tiff", width = width_mm / 25.4, height = height_mm / 25.4, units = "in", res = 600)
print(plot)
dev.off()
```

Open the SVG/PDF after export and verify that text can be selected, labels do not
overlap, and the figure still reads at final printed size.
