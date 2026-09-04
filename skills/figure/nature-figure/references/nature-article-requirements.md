# Flagship Nature Article figure requirements

Use this reference for figures submitted to the flagship journal **Nature**.
Keep initial-review files separate from accepted-in-principle production files,
and do not apply these formats automatically to Nature Portfolio subjournals.

This file carries only the journal file-format and stage contract: which file
types, dimensions and resolutions the journal accepts at which stage. The
general pre-delivery checklist is in `references/qa-contract.md`, legend wording
is in `references/figure-legend-conventions.md`, and the packaging pipeline is in
`references/figure-delivery-bundle.md`. Verify the official pages in section 9
before relying on any number here; journal specifications change.

## Contents

1. Stage gate
2. Initial-submission figures
3. Legend contract
4. Production dimensions and typography
5. Main-figure production files
6. Extended Data production files
7. Accessibility and image integrity
8. Delivery audit
9. Official sources

## 1. Stage gate

Record one stage before auditing:

- `initial_submission`: figures may be embedded in the Word/PDF manuscript;
  production-quality files are not required
- `revision`: follow both the public guide and the editor's instructions
- `accepted_in_principle`: supply production-quality main figures and Extended
  Data using their different file contracts

Do not fail an initial submission solely because it lacks separate editable
production artwork. Do fail it when the displayed data are unreadable,
misrepresented, incomplete or impossible for referees to assess.

## 2. Initial-submission figures

- Prefer figures embedded with manuscript text in one Word or PDF file.
- Put each figure legend on the same page as its figure.
- Use enough resolution for referees to evaluate the data.
- If embedding is impractical, supply separate files or an accessible
  repository route and confirm every figure is cited.
- Run the statistics, source-data and image-integrity checks even though final
  artwork formatting is deferred.

## 3. Legend contract

Legend structure, tense, self-containment and the statistics that must appear in
the legend are in `references/figure-legend-conventions.md`, and the statistics
fields to capture are in `references/qa-contract.md`. Only the flagship-specific
constraints are recorded here:

- keep the complete legend below 250 words, which is tighter than the
  corpus-derived 300-word guidance in `references/figure-legend-conventions.md`;
  for a flagship Nature submission the 250-word limit wins
- do not use the legend to narrate results or duplicate Methods
- identify adaptations and permissions when third-party material is used
- table legends begin with a short title sentence; explanatory detail may go in
  footnotes

## 4. Production dimensions and typography

For accepted-in-principle main figures:

- use 89 mm for a single-column figure or 183 mm for a double-column figure
- do not exceed 170 mm height, leaving room for the legend
- label multi-panel figures with 8 pt bold upright lowercase `a`, `b`, `c`, etc.
- use Courier or another monospaced font for amino-acid sequences
- embed TrueType 2 or 42 fonts
- arrange panels alphabetically where practical and minimize unused space

Text size, typeface and the editable-text requirement itself are checklist rows
in `references/qa-contract.md`; the font-embedding numbers above are the
journal-specific part.

## 5. Main-figure production files

Main figures require vector artwork with editable layers.

Preferred:

- `.ai`
- `.eps`
- editable `.pdf`

Also accepted by the current research figure guide when properly prepared:

- layered Photoshop artwork
- PowerPoint converted to PDF
- plain `.svg`
- Excel
- `.ps`

Do not submit flattened `.jpeg`, `.tiff` or `.png` as the final main-figure
production file merely because the workflow also creates those formats for QA
or preview. Keep all components embedded rather than externally linked and aim
to keep each file below 50 MB.

## 6. Extended Data production files

Extended Data has a different production contract:

- save in RGB
- use no more than 300 dpi
- keep each file at or below 10 MB
- use `.jpeg` preferably, or `.tiff`/`.eps`
- fit each item on one page with room for its legend or footnotes
- use the journal's required filename pattern based on the corresponding
  author's surname and the ED figure/table number

Do not send a main figure through the Extended Data file route or vice versa.

## 7. Accessibility and image integrity

- include axis lines and tick marks
- label every axis and place units in parentheses
- avoid background gridlines, drop shadows, decorative icons, patterns,
  overlapping labels and coloured text
- use an accessible palette; do not rely on red/green or rainbow scales
- supply artwork in RGB; photographic images need at least 300 dpi, with
  450 dpi preferred for the highest online-proof resolution
- keep scale bars and their labels editable rather than flattened into images
- use scale bars instead of magnification factors

For microscopy, gels, blots or other processed images, record the fields listed
under "Image-integrity minimum" in `references/qa-contract.md`: raw-file
provenance, crop, brightness/contrast/gamma, pseudocolour, stitching and
quantification link. Add lane rearrangement and processing software for gels and
blots, which the journal's image-integrity policy asks for and that checklist
does not name.

## 8. Delivery audit

Return:

| Item | Stage | Required contract | Current file/evidence | Status | Action |
|---|---|---|---|---|---|

Before approval, run the validation sequence in `references/asset-adaptation.md`
("Validate and deliver") and the checklist in `references/qa-contract.md`, then
add the two stage-specific checks this file owns:

- confirm the stage recorded in section 1 matches the files actually being sent
- verify that preview/export bundles are not mislabeled as the journal's final
  accepted upload formats

## 9. Official sources

Access-date recorded upstream as 2026-08-08. That date was carried over with the
text and has not been re-checked in this repository, so treat every number in
this file as needing confirmation against these pages before a real submission:

- Nature initial submission: <https://www.nature.com/nature/for-authors/initial-submission>
- Preparing figures: <https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/>
- Building and exporting figure panels: <https://research-figure-guide.nature.com/figures/building-and-exporting-figure-panels/>
- Image integrity: <https://www.nature.com/nature-portfolio/editorial-policies/image-integrity>
