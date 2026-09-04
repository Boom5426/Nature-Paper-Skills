# Tutorials — Nature Figure Making

End-to-end walkthroughs for the most common publication figure types.
All examples use helpers from [api.md](api.md) and patterns from [common-patterns.md](common-patterns.md).
For real production scripts and output previews from figures4papers, open [demos.md](demos.md).

---

## Tutorial 1: Grouped bar chart (multi-metric comparison)

**Goal**: Several methods compared across multiple metrics, drawn at the size it
will print. When methods belong to related families, use one coherent baseline
family plus one coherent hero family.

**Scale**: print. `S = canvas_in / printed_in = 1`, so 7 pt is 7 pt on the page
and `axes.linewidth = 0.8` is a 0.8 pt rule. The design-scale form of this figure
was `figsize=(28, 6)` with `font.size = 24`, i.e. `S = 28 / 7.20 = 3.9`; every
absolute size below is that number divided by `S`.

**Two integrity rules this figure follows.**

- **Zero baseline.** A bar encodes magnitude by length, so a truncated y-axis
  multiplies a small difference into a large one. The earlier version of this
  tutorial set `ylim` to the data range plus a 15% margin, which turned a
  0.11-wide spread in Metric 1 into a full-height panel. `ax.set_ylim(0, top * 1.12)`
  keeps the encoding honest. The cost is real: with a zero baseline the six
  Metric 1 bars look nearly equal, because they nearly are. When a small
  difference is the point, plot the difference itself (paired Δ with a CI) or a
  dot plot with an effect-size axis. Do not cut the bar axis.
- **Show the replicates.** A bar plus an s.d. cap hides whether five seeds agree
  or one outlier carries the mean. Overlaying the per-seed points costs nothing,
  makes *n* visible, and lets the reader see the spread the cap only summarises.

Dropping the dedicated legend column buys back a third of the width for the data.
The zero baseline needs top headroom anyway, so the shared legend strip sits in
that headroom instead of in a column of its own. (The dedicated-legend-panel
pattern is still the right answer when the panels are square and the legend is
tall; see [common-patterns.md](common-patterns.md).)

```python
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec

MM = 1 / 25.4   # print scale: the canvas IS the printed panel

# --- Style (every size below is the size the reader sees) ---
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
plt.rcParams['svg.fonttype'] = 'none'
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42
plt.rcParams['font.size'] = 7
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['legend.frameon'] = False

# --- Data: synthetic and illustrative, not measured benchmark results ---
# Kept per-seed on purpose: the figure plots the replicates, and the mean and
# s.d. are derived from them rather than invented alongside them.
rng = np.random.default_rng(0)          # seeds are explicit and reproducible
methods = ['ResNet1d18', 'ResNet1d34', 'ECGFounder', 'CSFM-Tiny', 'CSFM-Base', 'CSFM-Large']
colors  = ['#484878', '#7884B4', '#B4C0E4', '#E4E4F0', '#E4CCD8', '#F0C0CC']
metrics = ['Metric 1', 'Metric 2', 'Metric 3']
centre = {
    'Metric 1': np.array([0.81, 0.83, 0.86, 0.89, 0.91, 0.92]),
    'Metric 2': np.array([0.63, 0.67, 0.71, 0.74, 0.77, 0.79]),
    'Metric 3': np.array([0.41, 0.45, 0.49, 0.53, 0.56, 0.58]),
}
N_SEEDS = 5
# Replace this block with your real per-seed runs. mean and s.d. are DERIVED
# from the replicates, never invented alongside them.
# sd chosen so the illustration's ordering stays monotone; it is not a measured
# dispersion, and a real figure must not tune it to make an ordering hold.
reps = {m: c[:, None] + rng.normal(0, 0.012, (len(methods), N_SEEDS))
        for m, c in centre.items()}
mean = {m: r.mean(axis=1) for m, r in reps.items()}
std  = {m: r.std(axis=1, ddof=1) for m, r in reps.items()}

# --- Figure: 183 mm double column ---
fig = plt.figure(figsize=(183 * MM, 50 * MM))
gs = gridspec.GridSpec(1, len(metrics))

handles, labels = None, None
for col, metric in enumerate(metrics):
    ax = fig.add_subplot(gs[col])
    ax.bar(
        range(len(methods)),
        mean[metric],
        yerr=std[metric],
        capsize=1.5,
        color=colors,
        label=methods,
        edgecolor='black',
        linewidth=0.4,
        error_kw={'elinewidth': 0.6, 'capthick': 0.6},
    )
    # Per-seed replicates, jittered so overlapping runs stay countable
    for i in range(len(methods)):
        ax.scatter(
            i + rng.uniform(-0.18, 0.18, N_SEEDS),
            reps[metric][i],
            s=2.5, color='#272727', linewidths=0.2, edgecolors='white', zorder=3,
        )
    if col == 0:
        handles, labels = ax.get_legend_handles_labels()
    ax.set_xticks([])
    # Zero baseline; 12% headroom above the tallest cap or point
    top = max((mean[metric] + std[metric]).max(), reps[metric].max())
    ax.set_ylim(0, top * 1.12)
    ax.set_ylabel(metric, fontsize=7)

# Shared legend strip in the headroom the zero baseline created
fig.legend(handles, labels, ncol=len(methods), loc='upper center',
           bbox_to_anchor=(0.5, 1.0), fontsize=7, frameon=False,
           handlelength=1.2, handletextpad=0.5, columnspacing=1.4)

fig.tight_layout(pad=0.4, rect=[0, 0, 1, 0.87])   # pad in font-size units: 0.4 at 7 pt is ~1 mm
os.makedirs('./figures', exist_ok=True)
fig.savefig('./figures/comparison.svg')   # primary, editable text
fig.savefig('./figures/comparison.pdf')
fig.savefig('./figures/comparison.png', dpi=600)   # QA raster only
plt.close(fig)
```

Caption must state *n* and what the error bar is: "Bars, mean of n = 5 seeds;
points, individual seeds; error bars, s.d."
---

## Tutorial 2: Ablation bar chart (alpha-graduated, horizontal)

**Goal**: Same method with components progressively added; alpha encodes completeness.

**Scale**: print, 89 mm single column, 7 pt base, 0.8 pt rules. The design-scale
form was `figsize=(12, 6)` with `font.size = 24` (`S = 12 / 3.50 = 3.4`).

The same zero-baseline rule as Tutorial 1 applies on the x-axis here: these are
bars, so `xlim` starts at 0.

```python
import os
import numpy as np
import matplotlib.pyplot as plt

MM = 1 / 25.4   # print scale: the canvas IS the printed panel

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
plt.rcParams['svg.fonttype'] = 'none'
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42
plt.rcParams['font.size'] = 7
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['legend.frameon'] = False

configs = ['None', '+ Module A', '+ Module B', '+ Module C', 'Full']
values  = np.array([0.72, 0.78, 0.81, 0.84, 0.88])
stds    = np.array([0.02, 0.02, 0.01, 0.01, 0.01])

n = len(configs)
blue_rgb = (0.215686, 0.458824, 0.729412)   # #3775BA
# Floor the ramp at 0.35: composited over white, alpha 0.2 gives 1.30:1 against
# the page, which is invisible at 6 pt. 0.35 gives 1.60:1 and the outline below
# carries identification regardless of fill.
alphas = np.linspace(0.35, 1.0, n)
colors = [(blue_rgb[0], blue_rgb[1], blue_rgb[2], a) for a in alphas]

fig, ax = plt.subplots(figsize=(89 * MM, 45 * MM))   # 89 mm single column
ax.barh(range(n), values, xerr=stds,
        color=colors, edgecolor=blue_rgb, linewidth=0.4,
        ecolor='k', capsize=1.5,
        error_kw={'elinewidth': 0.6, 'capthick': 0.6})
ax.set_yticks(range(n))
ax.set_yticklabels(configs)
ax.set_xlim(0, (values + stds).max() * 1.10)   # zero baseline, 10% headroom
ax.set_xlabel('Score', fontsize=7)

fig.tight_layout(pad=0.4)
os.makedirs('./figures', exist_ok=True)
fig.savefig('./figures/ablation.svg')   # primary, editable text
fig.savefig('./figures/ablation.pdf')
fig.savefig('./figures/ablation.png', dpi=600)   # QA raster only
plt.close(fig)
```

At 89 mm the alpha ramp does most of the work and the axis stays quiet. If the
ablation deltas are too small to read against a zero baseline, that is the honest
signal that the ablation table belongs in the text, not that the axis should move.
---

## Tutorial 3: Multi-panel trend with shared legend

**Goal**: Two trend panels (e.g., train/val curves) and a legend-only third panel.

**Scale**: print, 183 mm double column, 7 pt base, 0.8 pt rules. The design-scale
form was `figsize=(18, 5)` with `font.size = 15` (`S = 18 / 7.20 = 2.5`), so the
line width drops from 2.5 to 1.0 and markers from 6 to 2.5. Line art is exactly
the case where print scale is mandatory: a downscaled raster of these curves
throws away the vector the journal wants.

Trend panels are not bars, so a non-zero y-axis is legitimate here. The rule that
was violated in Tutorial 1 is about *length encodings*, not about all axes.

```python
import os
import numpy as np
import matplotlib.pyplot as plt

MM = 1 / 25.4   # print scale: the canvas IS the printed panel

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
plt.rcParams['svg.fonttype'] = 'none'
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42
plt.rcParams['font.size'] = 7
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['legend.frameon'] = False

rng = np.random.default_rng(0)   # explicit seed: the same figure every run
methods = ['Baseline', 'CSFM-Tiny', 'CSFM-Base', 'CSFM-Large']
colors  = ['#7884B4', '#E4E4F0', '#E4CCD8', '#F0C0CC']
offsets = {'Baseline': -0.03, 'CSFM-Tiny': 0.00, 'CSFM-Base': 0.02, 'CSFM-Large': 0.03}
x = np.arange(0, 100, 5)

fig, axes = plt.subplots(1, 3, figsize=(183 * MM, 51 * MM))   # 183 mm double column

for panel_idx, (ax, panel_name) in enumerate(zip(axes[:2], ['Training', 'Validation'])):
    for method, color in zip(methods, colors):
        y = (0.52 + 0.40 * (1 - np.exp(-x / 30))
             + rng.normal(0, 0.01, len(x)) + offsets[method])
        ax.plot(x, y, color=color, lw=1.0, marker='o', markersize=2.5,
                markeredgecolor='none', label=method)
    # 0.5 is a real null on this scale, so it is drawn rather than implied.
    ax.axhline(0.5, color='#767676', lw=0.6, ls=(0, (2, 2)), zorder=0)
    if panel_idx == 0:
        ax.annotate('chance', xy=(x[-1], 0.5), xytext=(-2, 2),
                    textcoords='offset points', ha='right', va='bottom',
                    fontsize=6, color='#767676')
    ax.set_title(panel_name, fontsize=7)
    ax.set_xlabel('Epoch', fontsize=7)
    ax.set_ylabel('AUROC', fontsize=7)
    if panel_idx == 0:
        handles, labels = ax.get_legend_handles_labels()

# Legend-only panel
axes[2].legend(handles, labels, fontsize=7, loc='center', frameon=False,
               handlelength=1.5, handletextpad=0.5)
axes[2].set_axis_off()

fig.tight_layout(pad=0.4)
os.makedirs('./figures', exist_ok=True)
fig.savefig('./figures/trends.svg')   # primary, editable text
fig.savefig('./figures/trends.pdf')
fig.savefig('./figures/trends.png', dpi=600)   # QA raster only
plt.close(fig)
```

Two cautions at this size. `markeredgecolor='none'` matters: the default marker
edge is 1.0 pt, which at `markersize=2.5` would be most of the marker. And
`#E4E4F0` is at the contrast floor for a 1 pt stroke on white; it was chosen as a
*fill* in Tutorial 1, where area carries it. If these curves must survive
printing on uncoated stock, move CSFM-Tiny to `#B4C0E4` and shift the rest of the
hero family one step darker.
---

## Tutorial 4: Mixed-direction benchmark heatmap (zero-anchored columns)

**Goal**: one table-shaped panel comparing methods across metrics that do not point the
same way and do not share a unit. Colour states how good a value is in absolute terms;
the printed number carries the comparison.

**What this replaces.** The earlier version built the negative-direction column as
`Normalize(vmin=col_max, vmax=0)`. That inverts the interval, so the annotation loop's
first `cmap(norm(val))` raised `ValueError: minvalue must be less than or equal to
maxvalue`. It also rebuilt the norm a second time inside that loop, which let the fill
colour and the colour used to choose the text ink drift apart. Both defects come from
one habit: deciding a cell's colour more than once. Here the colour is resolved once,
into an RGBA array, and everything downstream reads that array.

### The four rules this figure follows

**1. Anchor every column at zero, carry direction in the ramp.**
A single expression covers both cases and cannot invert:

```text
lo = min(0.0, col.min())      # non-negative column -> Normalize(0, col_max)
hi = max(0.0, col.max())      # non-positive column -> Normalize(col_min, 0)
```

Direction is then applied to the *ramp*, not to the norm: a forward ramp for a
higher-is-better column, a reversed ramp (`Oranges_r`) for a lower-is-better one. The
result is one reading rule for the whole panel, saturation means better, whether the
column is an AUROC, an RMSE, a negative batch silhouette, or a runtime in minutes.

State the cost plainly, because it is real. Zero anchoring compresses within-column
contrast: AUROC spans 0.742 to 0.871 on a 0 to 0.871 ramp, so it occupies the top 15%
of the ramp and the six cells look almost alike; RMSE stays pale throughout because no
method is near a perfect 0. That is the point. A ramp stretched to `col.min()` would
magnify a 0.045 AUROC gap into a full light-to-dark sweep and invite the reader to see
a difference the numbers do not support. Colour here is a coarse absolute prior; the
annotations do the quantitative work.

When a metric has a fixed reference that this run's data does not know about, use it
instead of `col_max`: 0.5 for an AUROC no-skill floor, 1.0 for a bounded ceiling. The
anchor is a claim about the measurement scale, not a summary of the sample.

**2. Annotate every cell and ship no colourbar.**
Six columns carry six different normalisations across three unit systems. A single bar
would assert a shared scale that does not exist, and six bars would cost more space than
the numbers they replace. So the numbers are the quantitative channel, not decoration,
and the code asserts that no colourbar axes was created. Hue marks direction (blue for
↑, orange for ↓), redundant with the arrow already in each column label; neither hue is
the red-versus-green pair, so no cell reads as "bad" from colour alone.

**3. Choose the in-mark ink by linearised relative luminance at 0.179.**
BT.601 luma compared against 128 is a rule for gamma-encoded video, not for judging
legibility on a printed page. Linearise each channel first, weight by 0.2126 / 0.7152 /
0.0722, and cut at 0.179, the luminance where black text and white text are exactly
equally legible. On this figure the two rules disagree on 5 of 36 cells, and the luma
rule leaves the worst of them at **3.53:1**, below the 4.5:1 WCAG AA floor for body
text. With the luminance rule the measured worst case over all 42 text marks is
**4.73:1** (white on the mid-blue "Baseline B / Pearson r" cell). The 0.179 crossover
bounds any cell at about 4.58:1 whatever the fill turns out to be.

**4. Mark the derived row by more than one signal, and print its losses.**
`pct = 100 * direction * (ours - best) / abs(best)`. The `direction` factor turns a drop
in a lower-is-better metric into a gain, and `abs()` keeps the denominator meaningful
when the best baseline is itself negative, as it is for batch silhouette. The row is
separated from measured data by four signals: a physical gap, unfilled cells, italic
type, and the word "derived" in its own label. Two of the six entries are losses and
both are printed, at -1.6% on Pearson r and -112.5% on runtime. A derived row that only
ever shows gains is a row the reader should not trust.

### Code

```python
import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.patches import Rectangle

MM = 1 / 25.4  # matplotlib speaks inches; manuscripts are specified in millimetres

# --- MANDATORY style block (api.md), print scale ---
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
plt.rcParams['svg.fonttype'] = 'none'   # text stays <text>, never outlined paths
plt.rcParams['pdf.fonttype'] = 42       # TrueType, not Type-3
plt.rcParams['ps.fonttype'] = 42
plt.rcParams['font.size'] = 7
plt.rcParams['axes.linewidth'] = 0.8

# --- Data: synthetic and illustrative, not measured benchmark results ---
methods = ['Baseline A', 'Baseline B', 'Baseline C', 'Baseline D', 'Baseline E', 'Ours']
metrics = ['AUROC ↑', 'AUPRC ↑', 'Pearson r ↑', 'RMSE ↓', 'Batch ASW ↓', 'Runtime ↓ (min)']
direction = np.array([+1, +1, +1, -1, -1, -1])     # +1 higher is better, -1 lower is better
cell_fmt = ['{:.3f}', '{:.3f}', '{:.3f}', '{:.3f}', '{:.3f}', '{:.1f}']
matrix = np.array([
    [0.742, 0.401, 0.318, 0.884, -0.052,  3.2],
    [0.771, 0.438, 0.352, 0.851, -0.088,  5.4],
    [0.803, 0.472, 0.397, 0.804, -0.113,  8.1],
    [0.815, 0.489, 0.410, 0.796, -0.071, 12.7],
    [0.826, 0.503, 0.428, 0.781, -0.126, 21.5],
    [0.871, 0.556, 0.421, 0.712, -0.207,  6.8],
])
n_rows, n_cols = matrix.shape
assert len(methods) == n_rows and len(metrics) == n_cols == len(direction) == len(cell_fmt)


def zero_anchored_norm(col):
    """Normalize spanning zero to the column's far extreme.

    Non-negative column -> Normalize(0, col_max)
    Non-positive column -> Normalize(col_min, 0)
    vmin <= vmax holds by construction, so this can never raise
    'minvalue must be less than or equal to maxvalue'.
    """
    lo = min(0.0, float(np.min(col)))
    hi = max(0.0, float(np.max(col)))
    if lo == hi:
        raise ValueError('column is identically zero; it carries no colour signal')
    return mpl.colors.Normalize(vmin=lo, vmax=hi)


def truncate_cmap(name, lo=0.15, hi=0.85, n=256):
    """Trim the ramp's endpoints. The value-to-position map stays linear."""
    base = plt.get_cmap(name)
    return mpl.colors.ListedColormap(base(np.linspace(lo, hi, n)), name=f'{name}_trunc')


CMAP_UP = truncate_cmap('Blues')        # forward ramp: saturated = far from 0 = good
CMAP_DOWN = truncate_cmap('Oranges_r')  # reversed ramp: saturated = near 0 = good


def srgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(rgb):
    """WCAG relative luminance: linearise each channel, then weight."""
    r, g, b = (srgb_to_linear(float(v)) for v in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(lum_a, lum_b):
    lo, hi = sorted((lum_a, lum_b))
    return (hi + 0.05) / (lo + 0.05)


def ink_for(rgb, threshold=0.179):
    """Pick black or white ink. 0.179 is the luminance where the two are
    equally legible, so the worse choice is never below 4.58:1."""
    return ('#FFFFFF', 1.0) if relative_luminance(rgb) < threshold else ('#000000', 0.0)


# --- Resolve each cell's colour ONCE, then reuse it for fill and for ink ---
rgba = np.zeros(matrix.shape + (4,))
norms = []
for j in range(n_cols):
    norm = zero_anchored_norm(matrix[:, j])
    cmap = CMAP_UP if direction[j] > 0 else CMAP_DOWN
    rgba[:, j] = cmap(norm(matrix[:, j]))
    norms.append(norm)

# --- Derived row: sign-aware improvement over the best baseline ---
baselines, ours = matrix[:-1], matrix[-1]
best_row = np.array([int(np.argmax(direction[j] * baselines[:, j])) for j in range(n_cols)])
best = baselines[best_row, np.arange(n_cols)]
delta = ours - best
if np.any(best == 0):
    raise ValueError('a best baseline is exactly zero; per-cent change is undefined there')
pct = 100.0 * direction * delta / np.abs(best)

# --- Figure: 183 mm double column, margins fixed in mm, no tight_layout guessing ---
W_MM, H_MM = 183.0, 52.0
M = dict(left=27.0, right=1.0, top=4.0, bottom=2.0, gap=4.0)   # millimetres
unit = (H_MM - M['top'] - M['bottom'] - M['gap']) / (n_rows + 1)  # one row's height

fig = plt.figure(figsize=(W_MM * MM, H_MM * MM))
gs = gridspec.GridSpec(
    2, 1, figure=fig,
    height_ratios=[n_rows, 1], hspace=M['gap'] / (0.5 * (n_rows + 1) * unit),
    left=M['left'] / W_MM, right=1 - M['right'] / W_MM,
    top=1 - M['top'] / H_MM, bottom=M['bottom'] / H_MM,
)
ax = fig.add_subplot(gs[0])
ax_d = fig.add_subplot(gs[1])          # deliberately NOT sharex: it would share ticks too

# Rectangles, not imshow: imshow would embed a raster inside the vector PDF.
audit = []
for (i, j), val in np.ndenumerate(matrix):
    ax.add_patch(Rectangle((j - 0.5, i - 0.5), 1, 1, facecolor=rgba[i, j],
                           edgecolor='white', linewidth=0.7))
    ink, ink_lum = ink_for(rgba[i, j])
    audit.append((methods[i], metrics[j],
                  contrast_ratio(ink_lum, relative_luminance(rgba[i, j]))))
    ax.text(j, i, cell_fmt[j].format(val), ha='center', va='center', fontsize=7,
            color=ink, fontweight='bold' if methods[i] == 'Ours' else 'normal')

ax.set_xlim(-0.5, n_cols - 0.5)
ax.set_ylim(n_rows - 0.5, -0.5)          # row 0 at the top
ax.set_xticks(np.arange(n_cols))
ax.set_xticklabels(metrics, fontsize=7)
ax.xaxis.set_ticks_position('top')
ax.set_yticks(np.arange(n_rows))
ax.set_yticklabels(methods, fontsize=7)
for lbl, name in zip(ax.get_yticklabels(), methods):
    lbl.set_fontweight('bold' if name == 'Ours' else 'normal')
ax.tick_params(which='both', length=0, pad=2)
ax.set_frame_on(False)

# --- Derived row, marked by four signals: a gap, no fill, italics, an explicit label ---
# The hue pair is redundant, never load-bearing: the printed sign (+/-) already
# carries gain versus loss, so the row survives greyscale print and CVD. Colour
# alone as the gain/loss channel is a correctness failure, see figure-style 4.5.
GAIN, LOSS = '#1B7837', '#B2182B'
ax_d.set_xlim(-0.5, n_cols - 0.5)
ax_d.set_ylim(-0.5, 0.5)
ax_d.set_yticks([0])
ax_d.set_yticklabels(['Δ vs. best (derived)'], fontsize=7, style='italic')
ax_d.set_xticks([])
ax_d.tick_params(which='both', length=0, pad=2)
ax_d.set_frame_on(False)
ax_d.axhline(0.5, color='#767676', linewidth=0.6, linestyle=(0, (2, 2)))
white_lum = relative_luminance((1.0, 1.0, 1.0))
for j in range(n_cols):
    ink = GAIN if pct[j] >= 0 else LOSS
    audit.append(('derived row', metrics[j],
                  contrast_ratio(relative_luminance(mpl.colors.to_rgb(ink)), white_lum)))
    ax_d.text(j, 0, f'{pct[j]:+.1f}%', ha='center', va='center',
              fontsize=7, color=ink, style='italic')

assert len(fig.axes) == 2, 'a colourbar axes appeared; the columns do not share a scale'
assert sum(len(a.texts) for a in fig.axes) == matrix.size + n_cols, 'a cell went unannotated'

os.makedirs('./figures', exist_ok=True)
saved = []
for ext in ('svg', 'pdf', 'png'):      # svg/pdf ship; png is the QA review raster
    path = f'./figures/tutorial4_benchmark_heatmap.{ext}'
    fig.savefig(path, dpi=600)
    saved.append(path)
plt.close(fig)

# --- Report what the figure actually did ---
print('per-column zero-anchored normalisation')
for j, nrm in enumerate(norms):
    form = f'Normalize(0, {nrm.vmax:.3f})' if nrm.vmin == 0 else f'Normalize({nrm.vmin:.3f}, 0)'
    print(f'  {metrics[j]:<16s} dir={direction[j]:+d}  {form:<22s} '
          f'ramp={"Blues" if direction[j] > 0 else "Oranges_r"}')
print('\nderived row: pct = 100 * direction * (ours - best) / abs(best)')
for j in range(n_cols):
    print(f'  {metrics[j]:<16s} best={best[j]:>7.3f}  ours={ours[j]:>7.3f}  '
          f'delta={delta[j]:>+7.3f}  {pct[j]:>+8.1f}%  '
          f'{"gain" if pct[j] >= 0 else "LOSS"}')
worst = min(audit, key=lambda t: t[2])
print(f'\ncells annotated: {matrix.size} measured + {n_cols} derived; colourbars: 0')
print(f'worst-case text contrast: {worst[2]:.2f}:1 ({worst[0]}, {worst[1]}), '
      f'min over {len(audit)} text marks; WCAG AA body text is 4.5:1')
print('\nsaved')
for p in saved:
    print(f'  {os.path.abspath(p)}  {os.path.getsize(p):,} bytes')
```

### What it prints

Real output of the fence above, run on matplotlib 3.11.1 / numpy 2.5.1:

```text
per-column zero-anchored normalisation
  AUROC ↑          dir=+1  Normalize(0, 0.871)    ramp=Blues
  AUPRC ↑          dir=+1  Normalize(0, 0.556)    ramp=Blues
  Pearson r ↑      dir=+1  Normalize(0, 0.428)    ramp=Blues
  RMSE ↓           dir=-1  Normalize(0, 0.884)    ramp=Oranges_r
  Batch ASW ↓      dir=-1  Normalize(-0.207, 0)   ramp=Oranges_r
  Runtime ↓ (min)  dir=-1  Normalize(0, 21.500)   ramp=Oranges_r

derived row: pct = 100 * direction * (ours - best) / abs(best)
  AUROC ↑          best=  0.826  ours=  0.871  delta= +0.045      +5.4%  gain
  AUPRC ↑          best=  0.503  ours=  0.556  delta= +0.053     +10.5%  gain
  Pearson r ↑      best=  0.428  ours=  0.421  delta= -0.007      -1.6%  LOSS
  RMSE ↓           best=  0.781  ours=  0.712  delta= -0.069      +8.8%  gain
  Batch ASW ↓      best= -0.126  ours= -0.207  delta= -0.081     +64.3%  gain
  Runtime ↓ (min)  best=  3.200  ours=  6.800  delta= +3.600    -112.5%  LOSS

cells annotated: 36 measured + 6 derived; colourbars: 0
worst-case text contrast: 4.73:1 (Baseline B, Pearson r ↑), min over 42 text marks; WCAG AA body text is 4.5:1

saved
  /.../figures/tutorial4_benchmark_heatmap.svg  25,392 bytes
  /.../figures/tutorial4_benchmark_heatmap.pdf  44,916 bytes
  /.../figures/tutorial4_benchmark_heatmap.png  287,936 bytes
```

Note both `Normalize` forms in that first block. `Batch ASW` is the non-positive column
and takes `Normalize(-0.207, 0)`; every other column is non-negative and takes
`Normalize(0, col_max)`. Neither can invert, which is the bug this tutorial no longer
has.

### Export checks worth running once

The PDF's `/MediaBox` is `[0 0 518.74 147.40]` points, which is exactly 183.0 by 52.0 mm,
so the panel drops into a double-column slot at 100% with no rescaling. Two greps are
enough to confirm the export contract held:

```bash
python3 -c "import re;d=open('figures/tutorial4_benchmark_heatmap.pdf','rb').read();\
print(sorted(set(x.decode() for x in re.findall(rb'/Subtype\s*/(\w+)',d))))"
# -> ['CIDFontType2', 'Type0']   no /Type3, and no /Image
grep -c '<text' figures/tutorial4_benchmark_heatmap.svg   # -> 55, one per text mark
```

`/Image` would appear if the colour field were drawn with `imshow`, which embeds a
raster inside the vector file. Drawing the cells as `Rectangle` patches keeps the PDF
fully vector and leaves each cell selectable in Illustrator. `Type3` would appear
without `pdf.fonttype = 42` and is flagged by several publishers' preflight.

### When not to use this

Zero anchoring is honest, and it often reveals that the colour is carrying almost
nothing. If, after anchoring, a column's cells are visually indistinguishable and the
reader is reading only the numbers, the figure has become a table with a decorative
wash. Ship the table. A heatmap earns its place when the pattern across rows and columns
is the claim, not when it is a lookup surface for twelve values. If the claim is instead
"our method wins by this margin", a ranked bar panel with the margin on the axis states
it better than any cell shading.
---

## Related files

- [SKILL.md](../SKILL.md) — When to use this skill
- [api.md](api.md) — Reusable helper implementations
- [common-patterns.md](common-patterns.md) — Layout and encoding patterns used above
- [design-theory.md](design-theory.md) — Why these choices exist
- [chart-types.md](chart-types.md) — Radar, 3D sphere, scatter, fill_between
