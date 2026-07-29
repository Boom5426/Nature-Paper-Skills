# The Figure Delivery Bundle

How to package a figure so a reviewer can audit it, a co-author can assemble it
by hand, and a later session can change it without archaeology.

Load this when a figure has to survive review rather than merely be produced:
multi-panel display items, figures asserting qualitative judgements, figures that
will be hand-assembled in a drawing program, or any project where more than one
person touches the artwork.

---

## The pipeline: panels first, composite last

**Build every panel as its own independent unit, review it at true printed size,
and only then assemble the composite.** Do not draw a multi-panel figure as one
script that emits one image.

```
1. content        state what each panel asserts, before drawing anything
2. draw           one panel = one source file = one PDF + PNG at true print size
                  (add SVG if a co-author edits panels in a drawing program)
3. review panels  inspect each panel alone, at 1:1
4. assemble       compose the panels into the sheet, stamp the letters
5. review sheet   inspect the composite for balance, colour, whitespace
6. bundle         source data, provenance, canonical version, notes
```

Steps 3 and 5 are both required and neither substitutes for the other; see the
review section below.

Why panel-first, concretely:

- **A panel that regenerates alone can be fixed alone.** In a monolithic script,
  changing panel g means re-running and re-checking all twelve.
- **Panels can be worked in parallel** by different people or different agents,
  because each one owns a file.
- **Review at true size is only possible if the panel exists at true size.**
  A panel cropped out of a rendered composite has already lost its type metrics.
- **Assembly becomes a separate, reviewable step** instead of an emergent property
  of plotting code.

### Directory layout

One directory per figure. Keep it tidy as you go, because the mess is what makes
a figure unmaintainable three rounds later, not the plotting code.

```
figures/
  README.md               the figure index: one row per figure directory, plus
                          the canonical-version block (see below)
  <sharedstyle>.py        HOW anything is drawn, shared by EVERY figure:
                          colour, type scale, mm geometry, export settings
  <sharedloaders>.py      shared data loaders, with expected values documented
  fig02_<name>/
    README.md             this figure's contract, provenance, blockers, and
                          the panel table. The canonical-version declaration
                          lives once, in figures/README.md.
    content.py            WHAT this figure asserts. NO PLOTTING LIBRARY HERE.
    fig02_data.py         loaders specific to this figure, if any
    fig02a_<what>.py      one file per panel
    fig02a_<what>.pdf     vector, page = the panel's true printed size
    fig02a_<what>.png     raster preview at the same size
    fig02b_<what>.py
    ...
    fig02_assemble.tex    WHERE each panel sits; builds the composite
    fig02_composite.pdf   the deliverable
    fig02_sourcedata.csv  every asserted cell, with its owning section
    placement.json        each panel's rectangle on the sheet, in mm
  _superseded/            replaced artwork, prefixed with where it came from
```

Two naming rules that pay for themselves:

- **The panel letter is in the file name**, so `fig02c` sorts next to its
  neighbours and a reviewer's "panel c is broken" maps to one file.
- **Superseded files keep their origin in the name** (`fig03_fig3a_schematic.pdf`),
  because a flat archive of files called `Fig1a.pdf` is not an archive.

### The layers that stay shared

Panel-first does not mean per-panel duplication of style. Keep one shared module
holding colour, type scale, page geometry in millimetres, and export settings, and
have every panel import it.

**Changing one colour across the whole paper then touches one file.** Without
that, it touches every panel and half of them get missed. The same applies to the
single-column and double-column widths, the type-size floor, and the
export-text-as-editable-text setting that lets a co-author relabel a panel.

The hard rule is the one in capitals above: **`content.py` imports no plotting
library.** It is the layer a co-author or a reviewer can actually read to check
what the figure claims. The moment assertions are interleaved with axis calls,
nobody reads them, including you.

---

## Pipeline steps 1 and 6: source data, and the section that owns each cell

A figure that prints a maturity label, a "not established", or "no independent
evaluation" is making an assertion. It needs the same traceability as a sentence
in the manuscript, and it usually gets none, because the assertion is buried in
plotting code.

Emit a source-data CSV alongside every figure, one row per asserted cell:

```
panel, row, column, value, note, owning_section
```

**Enforce the last column at write time:**

```python
missing = [r for r in self.rows if not r["owning_section"]]
assert not missing, (
    f"{len(missing)} source-data rows carry no owning section, "
    f"first is {missing[0]}. Every asserted cell needs one.")
```

The assertion is what makes this real rather than aspirational. A convention that
every cell should name its section decays within a few sessions; a build that
fails does not.

What this buys: a reviewer can open **one CSV** and check every claim the artwork
makes without reading a line of plotting code. That is a materially different
review than squinting at a rendered panel.

Two extensions worth adopting:

- **Quantitative panels emit their plotted values too**, not just the qualitative
  cells. Many journals now ask for source data per figure anyway; generating it
  as a build product rather than assembling it at submission is strictly cheaper.
- **Blocked cells are rows too.** A cell that is a labelled placeholder because
  the data does not exist should appear in the CSV saying so, with the blocker
  named. Absence from the CSV reads as "not asserted", which is a different claim.

---

## Pipeline step 3: review every panel alone, at true printed size

Each panel emits **PDF** (vector, editable text) and **PNG**, with the page size
set to the panel's real printed size. Not scaled to fit, not a crop of the
composite. Add SVG when a co-author will edit panels in a drawing program;
otherwise it is one more file to keep in sync.

Reviewing the assembled figure hides the defects that live inside a panel. On a
180 mm sheet carrying twelve panels, one panel is 40 to 60 mm wide. A label
overlapping its marker by a millimetre is invisible at any zoom that shows the
whole page. At true size, 5.2 pt type is 5.2 pt.

**Panel review and composite review find different things and neither replaces
the other.** Panel review catches collisions, clipped labels, and type below the
journal floor. Composite review catches a band that reads unbalanced, a colour
used inconsistently across panels, whitespace pulling the eye to the wrong place.
Both are in the pipeline for that reason.

If your preview renders a panel on a canvas other than the real one, draw it with
the **same** panel function the figure calls, on a canvas the full sheet width,
with the axes at the fractional rectangle the panel really occupies. Anything
converting millimetres to axis fractions depends on the axes' real size, so
previewing on a differently-sized canvas silently changes the geometry you were
trying to inspect.

---

## Pipeline steps 4 and 5: assemble, then review the sheet

Two ways to turn per-panel PDFs into a composite, with a real tradeoff.

**Assemble in LaTeX** (default). A small `figN_assemble.tex` per figure places the
per-panel PDFs and stamps the panel letters. The composite is then reproducible
from tracked source, panel text stays vector, and a regenerated panel propagates
by rebuilding. Cost: fine positioning is more awkward than dragging.

**Assemble in a drawing program.** Better for irregular compositions and
schematic-led pages. Cost: the composite becomes a hand artifact that can silently
diverge from its panels.

Either way, emit `placement.json` giving each panel's rectangle on the sheet in
millimetres. Place each panel at its `(x_mm, y_mm)` from the sheet's lower left
and the built figure comes back exactly. **Once the coordinates reproduce the
build, every departure from them is a deliberate composition decision rather than
an accident of scale.** If you assemble by hand they are what bounds the
divergence; if you assemble in LaTeX they are what lets someone check the
assembly file.

**Use a uniform bleed on all four sides**, not a fitted crop. A panel head often
sits just above its axes, so a tight crop cuts each panel differently and the mm
coordinates stop lining up. Uniform padding keeps one offset for every panel;
subtract it when placing by the file edge.

## Pipeline step 6: declare the canonical version

A figure directory accumulates variants across review rounds: with and without
confidence intervals, before and after a leakage fix, a rendered schematic
alongside a data-driven version of the same panel. Nothing in the file names says
which one the manuscript actually uses, and `fig4_composite.pdf` is a name that
survives three different figures.

**Write a canonical-versions block in the figures README**, one line per figure:

```markdown
## Canonical versions
All composites here are the final review-round-2 versions:
- Fig 2, 3: CI versions (95% bootstrap whiskers)
- Fig 4: external-parameter (de-leaked) version
- Fig 1: rendered art is the manuscript final; data version kept for reference
```

Two consequences worth stating:

- **A leakage fix supersedes a figure, and that must be visible.** When a
  de-leaked rerun changes a panel, the old panel is not an alternative rendering,
  it is wrong. Say so in the canonical block and move the old file to the
  superseded area, or someone will reuse it in a talk.
- **When two versions of one panel both stay, say why.** "Kept for reference" is
  a legitimate reason and takes four words. Silence is not.

## Every figure number regenerates from a tracked file

No figure may depend on data that lives only on one machine, only on a shared
drive, or only behind an interactive query. When a panel's inputs are pulled from
a working directory, commit the summarised table the figure actually reads, so
that every number in every main figure regenerates from something under version
control.

**Record, in the loader, the numbers each source is expected to reproduce.**

```python
"""Shared loaders for the Fig 2/3/4/5 panels.

  - per-method forests: the multi-seed bootstrap-CI summaries
    (reproduces the Table 1 values, headline metric 0.49 to 0.52)
  - per-gene / per-split breakdowns: the committed grid
    (reproduces the gap 0.31 / 0.19 / 0.13 and the 15 of 17 count)
"""
```

That docstring is a regression test written in prose. If someone repoints a
loader at a different table, the figure still builds and the numbers quietly
change; the expected values are what makes that visible. It is also the fastest
way for a co-author to check that the figure and the Results text describe the
same run.

---

## Directory hygiene, continuously

Tidy the figure directory as part of each pass, not as a cleanup at the end. The
mess is what makes a figure unmaintainable three review rounds later.

**Outputs are generated, never hand-edited.** Change the code and rebuild. The
failure this prevents is specific to hand assembly: someone nudges a label in the
exported SVG, the assembled master now differs from what the build produces, and
the next rebuild silently reverts a fix nobody recorded. Put the rule in the
figures README and keep the outputs reproducible from one command.

**Superseded artwork moves to `_superseded/` in the same commit that replaces it**,
with the origin kept in the file name. Not next week. A replaced panel left beside
its replacement gets reused in a talk.

**Every directory on disk appears in the figures README, and every row of the
README exists on disk.** This drifts almost immediately: a figure gets added in
one session and the table is updated in another that never happens. Check both
directions:

```bash
comm -3 <(ls -d fig*/ | sed 's:/::' | sort) \
        <(grep -oE 'fig[0-9]+[A-Za-z_-]*' README.md | sort -u)
```

Left column is on disk but undocumented; right column is documented but missing.
Adjust the pattern to your own naming: the point is that the check runs in both
directions, not the exact regex.

The same applies to the per-figure manifest: if the README promises every figure
carries a `figure.md`, then every figure carries one, or the README says
`README.md` because that is what they actually carry.

**Large submission-only rasters** (TIFF at print resolution) can be git-ignored,
provided the ignore rule names the command that regenerates them. An ignored
artifact with no regeneration path is a lost artifact.

---

## Four-state status markers

When artwork tabulates what exists, use four states and use the same words the
prose uses:

- **established**: exists and is independently evaluated
- **partial**: exists with a stated limitation
- **not established**: exists but is not settled, standardised, or independently
  evaluated
- **absent**: does not exist as checked

**"Not established" is a finding**, often the most informative cell in the table.
Collapsing it into "absent" throws away the difference between a field that has
not done the work and one where the work is impossible. Collapsing it into
"established" is overclaiming.

Two-state markers are the default in most plotting code because a boolean is
easier to draw. Resist that; the marker vocabulary should be decided by the claim,
not by the shape library.

---

## The open editorial question: may artwork settle what the prose does not?

If the manuscript still flags a claim as unresolved, may the figure state it as
settled?

The argument against: **a figure travels without its manuscript.** It gets pasted
into slides, quoted in reviews, and reproduced in secondary coverage, always
stripped of the marker that qualified it. Whatever the artwork asserts is what the
claim becomes.

The argument for: an unresolved marker is often about the source rather than the
fact, and a figure full of hedges is unreadable.

This skill does not decide it, because it is the authors' call. What it does
require is that **the question be asked explicitly and the answer recorded**, per
figure, in that figure's notes. The failure mode is not choosing wrongly; it is
never noticing that artwork and prose disagree about what is settled. Grep the
manuscript for open markers, check them against the cells of every figure, and
write down the decision.

---

## AI-generated imagery: decide by venue, and record the decision

Policies differ and this is not a judgement call to make silently.

**Nature Portfolio does not accept generative-AI-created or AI-altered images in
manuscript figures.** For a Nature-family submission, treat that as absolute for
the delivered artwork: redraw as vector, typeset every label as vector text, do
not trace.

Other venues permit rendered schematics, usually with disclosure. Some
manuscripts legitimately ship a rendered Figure 1 concept panel. If that is your
venue, **check the current policy at submission time rather than at drawing time**,
and write the decision and its date into the figure's notes, because the
policy is what changes, not the file.

Whichever way it goes, keep the prompt tracked:

```
fig1a_prompt.md      tracked: the prompt and the generation metadata
fig1a_render.png     untracked, or clearly marked as the delivered artifact
```

AI images are useful for **internal composition study** even where they cannot
ship: blocking out a schematic's arrangement before drawing it properly. If you
use them that way:

- keep the **prompt and the generation metadata under version control**, so the
  provenance of a composition decision is recoverable
- keep the **image files out of version control**, so they cannot drift into the
  delivery bundle
- redraw the delivered version as vector, with **every label typeset as vector
  text**, not traced

The distinction to hold onto is between a tool used to think and a tool used to
produce. Only the second is what the policy prohibits, and only the first is what
it is worth using AI for here.

---

## Bundle checklist

Before calling a figure delivered:

**Pipeline**
- [ ] every panel is its own source file, emitting PDF and PNG at true printed size
- [ ] every panel was inspected alone, at 1:1, not only inside the composite
- [ ] the composite was inspected as a whole, for balance and colour consistency
- [ ] the composite is assembled from the panel files, not drawn as one script
- [ ] `placement.json` in millimetres, uniform bleed rather than a fitted crop

**Content and provenance**
- [ ] the assertions layer reads as a list of claims and imports no plotting library
- [ ] source-data file exists; every row names its owning manuscript section
- [ ] blocked or placeholder cells appear in the source data with the blocker named
- [ ] every number regenerates from a tracked file; loaders document their
      expected values
- [ ] status markers are four-state and use the prose's words
- [ ] open manuscript markers checked against every asserted cell, decision recorded

**Directory**
- [ ] canonical version declared, per figure, in the figures README
- [ ] superseded artwork in `_superseded/`, origin kept in the file name
- [ ] every directory on disk is in the README, and every README row is on disk
- [ ] outputs reproducible from one command; nothing hand-edited
- [ ] AI-image policy checked against the target venue, and the decision recorded
      with its date; prompts tracked
- [ ] the figure's notes carry its contract, data provenance, and blockers

