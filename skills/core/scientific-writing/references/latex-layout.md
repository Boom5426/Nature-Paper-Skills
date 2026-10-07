# LaTeX manuscript layout: equations, figures and SI tables

Reference for **typesetting/layout** requests (排版): equation numbering, figure
placement, stranded headings, oversized floats and SI table pagination. Load it
for these tasks without reopening the paper's claims or regenerating approved figures.

Golden rule: **change → compile → render to image → look → iterate.** Never judge
layout from the `.tex` alone. Measure, don't guess.

Preserve the active template, scientific content and the user's protected passages.
Distinguish a documented venue requirement (journal, article type and submission
stage) from a template default or a project preference. Top-aligned figures,
same-page captions and SI equation prefixes can be project choices; do not present
them as universal Nature rules. If a request conflicts with a known requirement,
report the specific conflict rather than silently change the deliverable.

The snippets below illustrate ordinary `article` layouts. Do not paste private
float internals, geometry settings or package changes into a class that already
controls them without checking compatibility. Keep backups and build outputs
separate from the authoritative source until verification succeeds.

---

## 0. Diagnosis workflow (do this first)

1. Compile and read the log, especially:
   - `Float too large for page by Xpt` — a float (often figure+caption) exceeds the text height.
   - `Overfull \vbox` — content ran past the bottom margin (often `[H]` placement).
   - `Reference ... undefined` / `Citation ... undefined` — a missing target or another pass may be needed; follow actual cross-document dependencies rather than assume SI-first compilation.
   Also inspect overfull horizontal boxes and duplicate equation/PDF destinations.
2. Render pages to PNG and *look*. With pymupdf:
   `fitz.open(pdf)[i].get_pixmap(dpi=90).save(...)`. Build a **contact sheet**
   (all pages as a grid) to spot whitespace, stranded headings, and split floats at a glance.
3. Measure figure aspect ratios from the source PDFs (`pypdf` mediabox, or pymupdf):
   `aspect = width/height`. Then `displayed_height_pt ≈ textwidth_pt / aspect`.
   Use the active class's actual `\linewidth` and `\textheight`; include captions,
   headings, table notes and required spacing in the page budget.

---

## 1. The "loose / 松散" float page — top-align the glue

**Symptom:** a page holding only floats (two tables, or a figure) has a big band of
whitespace in the middle / above, content seemingly centered with gaps.

**Cause:** LaTeX's float-page glue is rubber and spreads floats to fill the page:
`\@fptop = 0pt plus 1fil`, `\@fpsep = 8pt plus 2fil`, `\@fpbot = 0pt plus 1fil`.

**Option:** if top alignment is requested or fits the current layout, top-align
float pages so slack collects at the bottom. This controls dedicated float pages;
it does not decide where a float goes on a page that also contains body text:

```latex
\makeatletter
\setlength{\@fptop}{0pt}            % no stretch at top → floats start at top
\setlength{\@fpsep}{14pt}           % fixed gap between stacked floats
\setlength{\@fpbot}{0pt plus 1fil}  % all slack to the bottom
\makeatother
% Let a page hold more float and less forced text:
\renewcommand{\topfraction}{0.95}
\renewcommand{\bottomfraction}{0.95}
\renewcommand{\textfraction}{0.06}
\renewcommand{\floatpagefraction}{0.80}
\setlength{\textfloatsep}{16pt plus 3pt minus 3pt}
\setlength{\floatsep}{14pt plus 3pt minus 3pt}
```

Apply compatible settings only to the affected document. For body-text pages,
`[!tp]` permits top placement or a dedicated float page; `[p]` permits a float page
only. Measure the graphic plus caption before restricting placement. In embedded
figure layouts, keep the whole graphic and caption together when legible and feasible;
retain separate legend pages when the requested submission format uses them.

---

## 2. Wide-and-short figures: distinguish placement from redesign

**Observation:** a figure (e.g. a 1×N strip of per-dataset bars) sits at full width but
is short (aspect 3:1–4:1). On a dedicated float page it can leave substantial
whitespace. The aspect ratio alone is not a defect; diagnose any stranded heading
separately (see §4).

**Why stretching is not a remedy:** the figure is width-bound at `\textwidth`. A 3.3:1 figure
at 468 pt wide is only ~140 pt tall. You cannot make it taller without making it wider
than the text, and stretching (`height=...` without keeping aspect) distorts it.

An intentional page tail can be acceptable. First try permitted float placement
or sharing space with related text. A request to move a figure does not authorize
changing its panel arrangement, plot geometry, data or legend. If the source figure
itself needs redesign, surface that need and use the figure workflow within the
authorized scope (`figure-planner`; production skills are in the figure stack,
installed with `--figure`). Do not impose a target aspect ratio to fill a page.

When source resizing is actually in scope:

- **Verify faithful regeneration:** check the original configuration against the
  approved figure's data, panel content, labels and style. Pixel comparison helps
  when renderer/version equality is expected; it is not proof of scientific fidelity.
- **Touch only the requested output branch.** A layout change to an SI version does
  not authorize altering its approved main-text counterpart.
- **Font-size caveat:** the on-page text size is set by the *display width* (figure
  scaled to `\textwidth`). Making a figure *taller* does **not** enlarge tick/label
  fonts — it only adds vertical extent (taller bars, more breathing room). To enlarge
  labels you must *narrow* the figure (more scale-up to `\textwidth`) or bump the
  in-plot font, not add height.
- **Mind the caption budget.** A 5–6 line caption is ~80 pt. Size the figure so
  `heading + intro + 2 panels + subcaptions + caption ≤ usable height`. A long-caption
  figure (e.g. a timeline) often needs to be ~0.5 in shorter than a short-caption one.

---

## 3. Portrait and landscape are deliverable-specific

Check the applicable template or sourced venue requirement before treating an
orientation as mandatory. Prefer upright content where it remains readable. A wide
SI table can use a landscape page when allowed and appropriate; a figure's orientation
rule does not automatically apply to tables. Keep aspect ratios intact and verify
rotated pages in the final PDF. Portrait is not a reason to squeeze text below a
legible size or to redraw an approved figure outside scope.

---

## 4. Float backlog → stranded section headings

**Symptom (very common in figure-heavy SI):** two or more section headings pile at the
top of a page above a huge empty gap; their figures appear pages later.

**Cause:** big floats can't be placed, so they defer; meanwhile body text and the next
`\section` keep flowing and stack up. The headings out-run their figures.

**Choose a local remedy:** allow suitable top/float-page placement, shorten only
unnecessary spacing, or add a targeted barrier where the reading order requires it.
If an SI section is intended to be a dedicated heading/intro/figure unit, and its
full content fits, a fresh page plus `[H]` is one option:

1. Make the figure short enough to *share a page* with its heading + intro
   (`heading + intro + figure ≤ usable height`; see §2 caption budget).
2. Start that dedicated section on a fresh page only when this fits the intended
   document structure. `\clearpage` also flushes earlier pending floats.
3. Pin the figure with `[H]` (needs `\usepackage{float}`) right after the heading/intro
   so it cannot float away:

```latex
\clearpage
\section{Per-dataset context scaling}
Figure~\ref{fig:scaling} shows ...        % short intro
\begin{figure}[H]                         % H = exactly here, no floating
  ...two stacked panels...
  \caption{...}\label{fig:scaling}
\end{figure}
```

This example keeps the heading and figure local; it is not the default for every
Results subsection and does not place the graphic above its heading.

Inspect the preceding page too: flushing its trailing float can strand its intro.
Fix the observed boundary without automatically pinning every preceding figure or
shrinking graphics to fill pages. Display figures are ordinarily indivisible floats;
if content appears split, inspect oversized boxes, separately placed panels/captions
or explicit continuation constructs before applying a generic float fix.

---

## 5. `[H]` and `placeins` — sharp edges

- **`[H]`** (float package) does not float. It can break before a figure or overflow
  when space is insufficient. Use it only for an intended local unit that fits;
  applying it everywhere is not a solution to a page-top placement request.
- **`\usepackage[section]{placeins}`** puts a `\FloatBarrier` at every `\section`, keeping
  a section's floats inside it. Useful against backlog — **but** it flushes the previous
  float and can strand the *current* heading alone on a page if that section's figure is
  too tall to share. Check the complete unit's height and the preceding page before
  adding a barrier; a local barrier may be enough without a document-wide package option.
- **Don't blanket-`\clearpage` every section.** Section-boundary clearpages create
  near-empty pages when a section is short. Use `\clearpage` surgically (figure sections,
  §4), not everywhere.

---

## 6. Multi-panel figures: preserve approved arrangements

- Panel arrangements belong to figure planning, not an automatic typesetting pass.
  If rearrangement is authorized, a vertical stack can improve wide-panel readability;
  other figures may fit a grid better. Do not convert an approved grid solely to fill space.
- Tune inter-panel space with `\vspace` between `subfigure`s (e.g. `0.3em–0.8em`).
- If you see `Float too large for page by X pt` and X is small (<5 pt), shave the
  smallest thing first: reduce inter-panel `\vspace`, or panel width by ~2%, before
  touching the figure itself.

Within an approved subfigure arrangement (using the template's compatible subfigure package):

```latex
\begin{figure}[p]\centering
  \begin{subfigure}{0.66\textwidth}\includegraphics[width=\textwidth]{a}\caption{}\end{subfigure}
  \vspace{0.3em}
  \begin{subfigure}{0.66\textwidth}\includegraphics[width=\textwidth]{b}\caption{}\end{subfigure}
  ...
  \caption{...}\label{...}
\end{figure}
```

---

## 7. Readability and continuity before page count or fullness

Neither a smaller page count nor a full canvas proves good layout. Respect actual
page limits, legible type and coherent reading order. Avoid stranded headings,
isolated paragraph lines and clipped material; accept intentional whitespace.
Widow/club penalties or a local keep-with-next adjustment may help, but inspect their
effect on surrounding pages rather than impose one global setting on every class.

---

## 8. Displayed formulas: continuity and numbering

Decide which formulas should be numbered from the request and active convention.
Do not automatically number every `\[...\]`: a parameter-value list or an intermediate
derivation can intentionally remain unnumbered. Preserve existing labels, references
and explicit tags; do not introduce a second numbering system over them.

For a requested numbered definition, use the class-compatible equation environment
and a semantic label. Keep its introduction and immediate explanation in the same
paragraph when they form one reasoning unit:

```latex
The response score is
\begin{equation}\label{eq:response-score}
S(q,d)=-D(q,d),
\end{equation}
where $D$ denotes the response distance.
```

Ordinary source wrapping is not a paragraph break; blank lines and `\par` are.
A new scientific topic after the formula can legitimately start a new paragraph.
Use `write-scientific-manuscript` for semantic decisions; a scan is only a shortlist.

Main-text Arabic numbers and an SI prefix such as `S1` are one possible convention.
For an independently compiled SI, `\renewcommand{\theequation}{S\arabic{equation}}`
can implement that prefix when the class permits it; do not reset a counter partway
through a document or replace the template's existing scheme without intent.
Use `aligned`/`split` within an equation for one numbered multiline relation, or
`align` when independent relations need separate numbers. Preserve mathematical
content and punctuation, including the sign and order of every term.

Check visible tags and resolved labels after compilation. Formulas in captions or
longtable headers may be measured/replayed; ensure their counters and labels are
not incremented repeatedly and that PDF destinations are unique. If that cannot
be guaranteed, place the equation in adjacent text or use the template's supported
mechanism while preserving the table description. Check long formulas for tag collisions.

## 9. SI tables: readable parts and legitimate continuations

Keep every value, unit, uncertainty, exclusion and necessary note. Do not delete
rows, remove conditions or reduce type to make a table fit. First inspect column
widths, wrapping, alignment, padding and unnecessary spacing. A wide table may fit
a permitted landscape page; portrait and landscape have different available widths.

Keep a compact table with its title and required notes on one page where feasible.
When a large table has independent logical parts, split at those boundaries and
label each part/continuation clearly. Avoid a lone row or a title/footnote detached
from its associated content. A genuinely long table can span pages with repeated
column headings and a clear continuation label; do not promise one page for every table.
`longtable` is not a float, so figure float-placement options do not control it.

Avoid blanket `\clearpage` changes outside the affected table blocks. Render each
changed part and adjoining pages to check rules, wrapping, margins and notes.

## 10. Verification proportional to the change

- [ ] Diff changes only the authorized prose boundaries, numbering or layout settings;
      scientific content, author metadata and protected assets remain intact.
- [ ] Numbered formulas use the chosen convention; existing labels and references resolve,
      with no duplicate tags/destinations or collisions.
- [ ] Complete graphics and captions follow the requested embedded/separate-legend format;
      placement fixes have not silently changed plots or panel content.
- [ ] Tables retain data and necessary notes, with legible parts/continuations.
- [ ] Compile has no oversized floats, overflow or unresolved references; review remaining
      warnings and do not describe an unavailable build as successful.
- [ ] Render affected pages and their neighbors. A contact sheet helps navigation;
      inspect dense equations, table text and captions at readable resolution.

Preserve scientific identifiers and original content in a focused diff or snapshot.
Checksums can establish unchanged assets; visual comparison checks layout. Neither
substitutes for checking edited formulas, data and references. If compilation or
rendering is unavailable, provide the source changes and mark that verification
unperformed; do not claim the result is visually validated.
