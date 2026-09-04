# API Reference — Nature Figure Making

Conventions, constants, and reusable code blocks. Implement in your script or adapt as needed.

---

## Constants

### PALETTE

```python
PALETTE = {
    "blue_main":      "#0F4D92",
    "blue_secondary": "#3775BA",
    "green_1": "#DDF3DE",
    "green_2": "#AADCA9",
    "green_3": "#8BCF8B",
    "red_1":   "#F6CFCB",
    "red_2":   "#E9A6A1",
    "red_strong": "#B64342",
    "neutral_light": "#CFCECE",
    "neutral_mid":   "#767676",
    "neutral_dark":  "#4D4D4D",
    "neutral_black": "#272727",
    "gold":   "#FFD700",
    "teal":   "#42949E",
    "violet": "#9A4D8E",
    "magenta":"#EA84DD",
}

DEFAULT_COLORS = [
    PALETTE["blue_main"],
    PALETTE["green_3"],
    PALETTE["red_strong"],
    PALETTE["teal"],
    PALETTE["violet"],
    PALETTE["neutral_light"],
]

PALETTE_NMI_PASTEL = {
    "baseline_dark": "#484878",
    "baseline_mid":  "#7884B4",
    "baseline_soft": "#B4C0E4",
    "ours_tiny":  "#E4E4F0",
    "ours_base":  "#E4CCD8",
    "ours_large": "#F0C0CC",
    "bg_lilac": "#E0E0F0",
    "bg_aqua":  "#E0F0F0",
    "bg_peach": "#F0E0D0",
    "neutral_light": "#D8D8D8",
    "neutral_mid":   "#A8A8A8",
    "neutral_dark":  "#606060",
    "delta_up":   "#2E9E44",
    "delta_down": "#E53935",
}

DEFAULT_COLORS_NMI_PASTEL = [
    PALETTE_NMI_PASTEL["baseline_dark"],
    PALETTE_NMI_PASTEL["baseline_mid"],
    PALETTE_NMI_PASTEL["baseline_soft"],
    PALETTE_NMI_PASTEL["ours_tiny"],
    PALETTE_NMI_PASTEL["ours_base"],
    PALETTE_NMI_PASTEL["ours_large"],
]

PALETTE_NATURE_IMAGING = {
    "bg": "#000000",
    "context": "#B8B8B8",
    "cyan": "#22D7E6",
    "magenta": "#FF2AD4",
    "white": "#FFFFFF",
}

PALETTE_NATURE_MATERIAL = {
    "aqua": "#77D7D1",
    "teal": "#33B5A5",
    "lilac": "#B9A7E8",
    "violet": "#7C6CCF",
    "callout_red": "#E53935",
    "neutral": "#D9D9D9",
}

PALETTE_NATURE_CLINICAL = {
    "baseline": "#272727",
    "week6": "#E28E2C",
    "week13": "#D24B40",
    "week26": "#5B8FD6",
    "year1": "#7BAA5B",
    "year2": "#C45AD6",
    "group_band": "#F2E6D9",
}

PALETTE_NATURE_GENOMICS = {
    "neutral_light": "#D8D8D8",
    "neutral_mid": "#8F8F8F",
    "wave1": "#D9544D",
    "wave2": "#5B7FCA",
    "wave3": "#B89BD9",
    "outline": "#4D4D4D",
}
```

Use `DEFAULT_COLORS` when color itself carries explicit semantic meaning (`hero`, `baseline`, `positive variant`).
Use `DEFAULT_COLORS_NMI_PASTEL` when several compared methods belong to one or two related families and the page
should feel visually unified.

---

## MANDATORY font + SVG rules (always first, no exceptions)

These lines are **non-negotiable** and must appear at the top of every script,
before any figure is created. They guarantee editable text in both SVG and PDF
output. Type-3 fonts, matplotlib's PDF default, are flagged or rejected by
several publishers' preflight, which is what `pdf.fonttype = 42` avoids:

```python
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
plt.rcParams['svg.fonttype'] = 'none'   # keeps text as <text> nodes, not paths
plt.rcParams['pdf.fonttype'] = 42       # TrueType, not Type-3, in PDF
plt.rcParams['ps.fonttype'] = 42
```

**Why `svg.fonttype = 'none'`**: matplotlib's default (`'path'`) converts every
glyph to a bezier path, making text unselectable, unsearchable, and impossible to
re-align in Illustrator / Inkscape. With `'none'`, text stays as SVG `<text>` elements
and font substitution happens at render time.

**Output format**: always save as `.svg` (primary), with `.pdf` alongside it for
submission. Never deliver `.png` alone when the figure contains text that may need
adjustment. PNG remains the right format for the review raster that the
`figure-style` QA loop inspects; that is a working copy, not a delivery format.

---

## apply_publication_style()

```python
def apply_publication_style(font_size=7, axes_linewidth=0.8, use_tex=False):
    """Apply Nature-style rcParams. Call once before creating any figures."""
    # ── MANDATORY: editable SVG text ──────────────────────────────────────────
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
    plt.rcParams['svg.fonttype'] = 'none'
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42
    # ── Layout & style ────────────────────────────────────────────────────────
    plt.rcParams['font.size'] = font_size
    plt.rcParams['axes.spines.right'] = False
    plt.rcParams['axes.spines.top'] = False
    plt.rcParams['axes.linewidth'] = axes_linewidth
    plt.rcParams['legend.frameon'] = False
    if use_tex:
        plt.rcParams['text.usetex'] = True
```

**Presets (print scale, the default regime).** The canvas is the printed panel, so
every number is the size the reader sees:

- Single or double column: `apply_publication_style()` gives 7 pt text, 0.8 pt rules
- Dense journal-width multi-panels: `apply_publication_style(font_size=6, axes_linewidth=0.6)`
- LaTeX labels: `apply_publication_style(use_tex=True)`

**Presets (design scale).** Use only when deliberately authoring on an `S`-times
oversized canvas and downscaling a raster into the column. Divide by `S` to check
the value that actually prints:

- `S` about 2, compact: `apply_publication_style(font_size=15, axes_linewidth=2)` prints at 7.5 pt / 1.0 pt
- `S` about 4, large bar panels: `apply_publication_style(font_size=24, axes_linewidth=3)` prints at 6.1 pt / 0.76 pt

Every other absolute size in this file is print scale. Do not mix the two regimes
in one script, and do not use design scale for line art: a downscaled PNG of a bar
chart is a raster of something that should have stayed a vector.

---

## ink_on(rgb) — in-mark label colour

```python
def relative_luminance(rgb):
    """WCAG relative luminance from an (r, g, b) triple in 0-1."""
    def lin(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(c) for c in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ink_on(rgb, threshold=0.179):
    """Return 'white' or 'black', whichever has more contrast against `rgb`.

    0.179 is the luminance where white and black tie at about 4.58:1, so the
    worse of the two choices still clears the WCAG AA 4.5:1 floor. The older
    BT.601 rule (0.299r + 0.587g + 0.114b < 128 on 0-255) picks the wrong ink
    on mid-tone fills and bottoms out near 3.5:1, which is not enough for a
    5-7 pt label sitting inside a mark.
    """
    return 'white' if relative_luminance(rgb) < threshold else 'black'


def hex_to_rgb(hex_color):
    c = hex_color.lstrip('#')
    return tuple(int(c[i:i + 2], 16) / 255 for i in (0, 2, 4))
```

---

## add_panel_label(ax, label, ...)

```python
def add_panel_label(ax, label, x=-0.06, y=1.02, fontsize=8,
                    color='black', fontweight='bold'):
    """Place a Nature-style panel label near the top-left edge."""
    ax.text(
        x, y, label,
        transform=ax.transAxes,
        fontsize=fontsize,
        fontweight=fontweight,
        color=color,
        ha='left',
        va='bottom',
    )
```

For dark image plates, move the label inside the panel and switch to white:
`add_panel_label(ax, 'a', x=0.01, y=0.98, color='white')`

---

## style_dark_image_ax(ax, ...)

```python
def style_dark_image_ax(ax, facecolor='black'):
    """Prepare an axes for microscopy / rendering plates."""
    ax.set_facecolor(facecolor)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    return ax
```

---

## make_grouped_bar(ax, categories, series, labels, ...)

```python
def make_grouped_bar(ax, categories, series, labels,
                     ylabel='Value', colors=None,
                     annotate=False, bar_width=0.8,
                     error_kw=None):
    """
    Grouped bar chart.

    Parameters
    ----------
    ax         : matplotlib Axes
    categories : list[str]  — x-axis category names (length K)
    series     : list[array] — one array per group (each length K)
    labels     : list[str]  — legend label per group
    ylabel     : str
    colors     : list[str] | None  — defaults to DEFAULT_COLORS; override with
                                     DEFAULT_COLORS_NMI_PASTEL for unified-family figures
    annotate   : bool  — print value above each bar
    bar_width  : float — total width for all bars in one category
    error_kw   : dict  — passed to ax.bar as error_kw

    Returns
    -------
    list[BarContainer]
    """
    import numpy as np
    if colors is None:
        colors = DEFAULT_COLORS
    if error_kw is None:
        error_kw = {'elinewidth': 0.8, 'capthick': 0.8, 'capsize': 2}
    n_groups = len(series)
    n_cats = len(categories)
    w = bar_width / n_groups
    x = np.arange(n_cats)
    containers = []
    for i, (vals, label, color) in enumerate(zip(series, labels, colors)):
        offset = (i - (n_groups - 1) / 2) * w
        bars = ax.bar(x + offset, vals, width=w, label=label,
                      color=color, edgecolor='black', linewidth=0.5,
                      error_kw=error_kw)
        containers.append(bars)
        if annotate:
            for bar, val in zip(bars, vals):
                ax.text(bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + 0.01,
                        f'{val:.2f}', ha='center', va='bottom', fontsize=6)
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_ylabel(ylabel)
    ax.legend()
    return containers
```

---

## make_trend(ax, x, y_series, labels, ...)

```python
def make_trend(ax, x, y_series, labels,
               colors=None, ylabel=None, xlabel=None,
               show_shadow=False, shadow_alpha=0.15,
               lw=1.0, marker='o', markersize=3):
    """
    Multi-line trend plot.

    Parameters
    ----------
    x        : array-like   — shared x values
    y_series : list[array]  — one 1D array per line
    labels   : list[str]
    show_shadow : bool  — fill_between ± std if y_series contains 2D arrays (rows=runs)
    """
    import numpy as np
    if colors is None:
        colors = DEFAULT_COLORS
    for y, label, color in zip(y_series, labels, colors):
        y = np.asarray(y)
        if y.ndim == 2:
            mean, std = y.mean(0), y.std(0)
        else:
            mean, std = y, None
        ax.plot(x, mean, color=color, lw=lw, marker=marker,
                markersize=markersize, label=label)
        if show_shadow and std is not None:
            ax.fill_between(x, mean - std, mean + std,
                            color=color, alpha=shadow_alpha)
    if ylabel:
        ax.set_ylabel(ylabel)
    if xlabel:
        ax.set_xlabel(xlabel)
    ax.legend()
```

---

## make_forest_plot(ax, labels, estimates, ci_low, ci_high, ...)

```python
def make_forest_plot(ax, labels, estimates, ci_low, ci_high,
                     colors=None, ref=0.0, xlabel=None, xlim=None,
                     marker='o', markersize=2.5, lw=0.8):
    """
    Minimal forest plot helper for Nature-style clinical/statistical panels.
    """
    import numpy as np
    y = np.arange(len(labels))[::-1]
    if colors is None:
        colors = ['#B64342'] * len(labels)
    for yi, est, lo, hi, color in zip(y, estimates, ci_low, ci_high, colors):
        ax.plot([lo, hi], [yi, yi], color=color, lw=lw)
        ax.plot(est, yi, marker=marker, ms=markersize, color=color)
    ax.axvline(ref, color='#767676', linestyle='--', linewidth=0.6, alpha=0.8)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    if xlabel:
        ax.set_xlabel(xlabel)
    if xlim is not None:
        ax.set_xlim(xlim)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
```

Use pale `ax.axhspan(...)` bands behind contiguous label groups when you need the
clinical-triptych look from `Nature`.

---

## make_heatmap(ax, matrix, ...)

```python
def make_heatmap(ax, matrix, x_labels=None, y_labels=None,
                 cmap='magma', cbar_label=None, annotate=False,
                 fmt='{:.2f}', fontsize=6, norm=None):
    """2D heatmap with optional colorbar and cell annotations.

    `norm` is a caller-supplied Normalize. Pass one whenever the colour has to
    mean something fixed: anchor it at zero (`Normalize(0, col_max)`, or
    `Normalize(col_min, 0)` with a reversed ramp for a lower-is-better column)
    so saturation always reads as the same direction. The default,
    `Normalize(matrix.min(), matrix.max())`, stretches whatever range it is
    handed, so the palest cell means "smallest here" and nothing more.

    Columns that do not share a scale must not share one colorbar: leave
    `cbar_label` unset and annotate every cell instead.

    `imshow` embeds a raster image inside the exported PDF (`/Subtype /Image`).
    For a fully vector cell field, draw `Rectangle` patches instead; the worked
    version is Tutorial 4 in `tutorials.md`.
    """
    import numpy as np
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    if norm is None:
        norm = mpl.colors.Normalize(vmin=matrix.min(), vmax=matrix.max())
    im = ax.imshow(matrix, cmap=cmap, norm=norm, aspect='auto')
    if cbar_label:
        cbar = ax.figure.colorbar(im, ax=ax)
        cbar.set_label(cbar_label)
    if x_labels:
        ax.set_xticks(range(len(x_labels)))
        ax.set_xticklabels(x_labels, rotation=30, ha='right')
    if y_labels:
        ax.set_yticks(range(len(y_labels)))
        ax.set_yticklabels(y_labels)
    if annotate:
        cm_obj = plt.get_cmap(cmap)
        for (i, j), val in np.ndenumerate(matrix):
            # One RGBA lookup per cell, reused for the fill and for the ink, so
            # the label can never be coloured against a different value.
            rgba = cm_obj(norm(val))
            ax.text(j, i, fmt.format(val), ha='center', va='center',
                    fontsize=fontsize, color=ink_on(rgba))
    ax.set_frame_on(False)
```

---

## finalize_figure(fig, out_path, ...)

```python
def finalize_figure(fig, out_path, formats=None, dpi=600,
                    pad=0.4, bbox_inches=None, close=True):
    """
    Apply tight_layout and save figure.

    Parameters
    ----------
    out_path : str   — path without extension, or with extension
    formats  : list  — e.g. ['png', 'pdf']. If None, uses extension of out_path.
    dpi      : int   — raster only; 600 for line + halftone, 300 is the floor.
                       Ignored by vector formats, which is why svg/pdf come first.
    pad      : float — tight_layout pad, in font-size units. 0.4 at 7 pt is about
                       1 mm. Do not carry a design-scale pad (2) into print scale:
                       at 7 pt that is a 5 mm border, 11% of an 89 mm panel.
    """
    import os
    from pathlib import Path
    import matplotlib.pyplot as plt
    fig.tight_layout(pad=pad)
    base = Path(out_path)
    os.makedirs(base.parent, exist_ok=True)
    if formats is None:
        formats = [base.suffix.lstrip('.') or 'png']
        base = base.with_suffix('')
    saved = []
    for fmt in formats:
        p = str(base) + f'.{fmt}'
        kw = {}
        if bbox_inches is not None:
            kw['bbox_inches'] = bbox_inches
        fig.savefig(p, dpi=dpi, **kw)
        saved.append(p)
    if close:
        plt.close(fig)
    return saved
```

---

## Validation Rules

- `make_grouped_bar`: `len(categories)` must equal length of each array in `series`.
- `make_trend`: each array in `y_series` must have same length as `x`.
- `make_heatmap`: `matrix` must be 2D; `x_labels` length = `matrix.shape[1]`; `y_labels` length = `matrix.shape[0]`.
- `finalize_figure`: supported formats — `png`, `pdf`, `svg`, `eps`, `jpg`, `tif`.

---

## Conventions

- Save outputs under `./figures/` (or path given by user); `finalize_figure` creates parent dirs.
- In headless / batch runs, set non-interactive backend before importing pyplot:
  ```python
  import matplotlib
  matplotlib.use('Agg')
  import matplotlib.pyplot as plt
  ```
- Always `plt.close(fig)` after saving to free memory.
- For multi-panel figures, prefer one baseline family plus one hero family; reserve green/red for delta cues.
- When color roles, resolution, or layout are underspecified and would change the figure, confirm with user before finalizing.
