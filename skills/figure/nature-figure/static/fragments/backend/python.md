# Backend: Python (matplotlib / seaborn)

**Python-only execution rule.** When the user has selected Python, do all figure drawing, previewing, exporting, and visual QA in Python. Do not call R/ggplot2, ComplexHeatmap, patchwork, or any R graphics device to create a temporary preview, fallback export, or layout approximation. If Python or required Python plotting packages are missing, stop before rendering and report the missing dependency. You may still write the Python script, provide `pip`/environment install commands, or ask permission to install dependencies, but do not cross-render the figure in R.

## Python quick-start

```python
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
    "svg.fonttype": "none",     # editable text in SVG
    "pdf.fonttype": 42,         # editable TrueType text in PDF
    "font.size": 7,             # use 15-24 only for large slide-sized panels
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.8,
    "legend.frameon": False,
})

def save_pub_py(fig, filename, dpi=600):
    # No bbox_inches="tight": it re-crops the canvas to the ink, so the exported
    # page stops being the size you set. A figure built at 183 mm comes out at
    # 185.7 mm and the journal rescales it, which silently changes every point
    # size. Budget the margins with fig.tight_layout(pad=0.4) or subplots_adjust
    # before saving, then export the canvas as-is.
    fig.savefig(f"{filename}.svg")
    fig.savefig(f"{filename}.pdf")
    fig.savefig(f"{filename}.tiff", dpi=dpi)
```

Use `text.usetex = True` only when LaTeX is installed and math-rich labels are required.

## Going deeper

- `references/api.md` — Python PALETTE, helper function signatures, validation rules.
- `references/common-patterns.md` — hero panels, legend-only axes, dark image plates, asymmetric layouts.
- `references/chart-types.md` — radar, 3D sphere, fill_between, scatter patterns.
- `references/tutorials.md` — end-to-end walkthroughs for bars, trends, heatmaps.
- `references/demos.md` — worked examples indexed by claim shape.
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

`require_matplotlib_panel_alignment(fig, ...)` from `scripts/audit_panel_alignment.py`
can be called directly after the final layout draw instead of exporting a manifest.
