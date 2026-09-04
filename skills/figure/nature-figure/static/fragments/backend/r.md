# Backend: R (ggplot2 / patchwork / ComplexHeatmap)

**R-only execution rule.** When the user has selected R, do all figure drawing, previewing, exporting, and visual QA in R. Do not call matplotlib/seaborn or any Python graphics device to create a temporary preview, fallback export, or layout approximation. If `Rscript`/R or required R packages are missing, stop before rendering and report the exact blocker. You may still write the R script, provide install commands (for example `install.packages(...)`), or ask permission to install dependencies, but do not cross-render the figure in Python.

## R quick-start

```r
library(ggplot2)
library(patchwork)

theme_set(
  theme_classic(base_size = 6.5, base_family = "Arial") +
    theme(
      # ggplot2 measures linewidth in mm: 0.35 mm is about 1.0 pt, which sits in
      # the same 0.75-1 pt band as the Python fragment's axes.linewidth = 0.8.
      # The two numbers differ because the units differ; do not harmonise them.
      axis.line = element_line(linewidth = 0.35, colour = "black"),
      axis.ticks = element_line(linewidth = 0.35, colour = "black"),
      legend.title = element_text(size = 6.2),
      legend.text = element_text(size = 5.8),
      strip.text = element_text(size = 6.2, face = "bold"),
      plot.title = element_text(size = 7, face = "bold"),
      panel.grid = element_blank()
    )
)

save_pub_r <- function(plot, filename, width_mm = 183, height_mm = 120, dpi = 600) {
  w <- width_mm / 25.4
  h <- height_mm / 25.4
  svglite::svglite(paste0(filename, ".svg"), width = w, height = h)
  print(plot)
  dev.off()
  grDevices::cairo_pdf(paste0(filename, ".pdf"), width = w, height = h, family = "Arial")
  print(plot)
  dev.off()
  ragg::agg_tiff(paste0(filename, ".tiff"), width = w, height = h, units = "in", res = dpi)
  print(plot)
  dev.off()
}
```

## Going deeper

- `references/r-workflow.md` — the R plotting workflow when the user provides R scripts, templates, or data.
- `references/r-template-index.md` — adapt a user-provided or private R template collection without exposing source paths.
- `references/design-theory.md` — typography, color theory, layout rationale, export policy (backend-agnostic).
- `references/nature-2026-observations.md` — real Nature page archetypes to match before choosing layout.
- `references/multipanel-evidence-architecture.md` — panel roles as inferential jobs, evidence chains across figures.
- `references/nature-article-requirements.md` — flagship *Nature* file-format contract.
- `references/asset-adaptation.md` — before reusing an example or a user-supplied plotting script.

## Audit tools to run before delivery

Dependency-free unless noted. One exit-code contract across all of them: `0` pass,
`1` fail, `2` usage or I/O error, `3` not run because a dependency is absent,
`4` not auditable. **2, 3 and 4 are not passes.**

```bash
python3 scripts/validate_figure.py my_figure.py          # source preflight, before rendering
python3 scripts/audit_pdf_text.py panel_a.pdf --min-pt 5 # per-panel PDF, not the composite
python3 scripts/audit_figure_collisions.py figure.pdf    # needs PyMuPDF, else exit 3
python3 scripts/audit_panel_alignment.py layout.json     # multi-panel geometry
```

**The R alignment gate is not shipped.** `scripts/audit_panel_alignment.py` reads a
backend-neutral layout manifest, and upstream exported that manifest from patchwork
via `panel_alignment.R`, which this repository did not vendor (it cannot run here:
there is no R in the test environment, and Python is the only guaranteed runtime).
Until it is, write the manifest yourself from the patchwork layout, or check panel
alignment by measuring the exported PDF. Do not report the gate as passed.
