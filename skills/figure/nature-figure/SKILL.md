---
name: nature-figure
description: >-
  Submission-grade Nature/high-impact journal figure workflow for Python or R, plus optional OpenRouter GPT Image 2 manuscript schematic generation when the user explicitly asks for AI-generated graphical abstracts, concept schematics, mechanism diagrams, or paper schematic illustrations. Use whenever the user asks to create, revise, audit, or polish manuscript figures, multi-panel scientific plots, figures4papers-style matplotlib plots, journal-ready SVG/PDF/TIFF outputs, or OpenRouter/API-generated schematic drafts, especially for Nature-family or other high-impact journals. Before plotting or image generation, define the figure's conclusion, evidence logic, export needs, and review risks. For plotting tasks, honor an explicit Python/R choice, otherwise reuse the saved nature-figure backend preference; if no preference exists, ask once whether the user prefers Python or R and save that answer for future calls. For explicit OpenRouter/GPT Image 2 schematic generation, do not ask Python or R; use the AI-schematic route. Supports matplotlib/seaborn, ggplot2/patchwork/ComplexHeatmap, and OpenRouter Images API drafts. Not for dashboards or Illustrator/Figma-first infographics. Also trigger on general academic-writing figure needs even without the word "Nature", such as making figures/plots for a paper, scientific/academic plotting, data visualization for a manuscript, AI-generated paper schematics, and Chinese phrasings like 论文配图、学术写作配图、科研绘图、科研作图、画图、作图、出图、论文图表、可视化、论文示意图、机制示意图、图形摘要.
license: Apache-2.0
---

# Nature Figure Making — Router

This skill is split into two layers:

- A **static layer** under `static/` that holds versioned, reusable content fragments (the figure contract and default stance, plus a per-backend quick-start for Python and R).
- A **dynamic layer** (this file plus `manifest.yaml`) that detects the plotting backend and loads only the fragment needed for the current job. The large design, API, pattern, and QA material lives in on-demand references.

Do not try to apply the figure logic from memory or from this router. Always load fragments from disk as described below.

## Routing protocol

Follow these steps every time the skill is invoked.

### 0. Check for the OpenRouter AI-schematic route

If the user explicitly asks to generate a manuscript schematic, graphical abstract, mechanism diagram, concept illustration, or paper schematic with OpenRouter, GPT Image 2, an image-generation API, or similar wording, do **not** ask "Python or R?". This is a non-plotting AI-schematic route.

For this route:

1. Read [manifest.yaml](manifest.yaml) and the `always_load` files.
2. Read [references/openrouter-image-generation.md](references/openrouter-image-generation.md).
3. Use [scripts/generate_openrouter_schematic.py](scripts/generate_openrouter_schematic.py) when the user wants a real API call or a reproducible payload.
4. Treat output as a draft schematic / graphical abstract, not as a quantitative data panel. Do not invent experimental values, author logos, institutional marks, or unsupported mechanisms.

Only continue to the Python/R backend gate for plotting, charting, data visualization, or manuscript figure assembly tasks that are not explicit OpenRouter AI image-generation requests.

### 1. Load the manifest and the core layer

Read [manifest.yaml](manifest.yaml). It declares the `backend` axis, the allowed values, and the file paths each value maps to.

Also read every file listed under `always_load` (`static/core/contract.md` and `static/core/stance.md`). These hold the figure contract, the backend gate, the missing-runtime rule, the privacy rule, and the default operating stance that apply to every figure job.

### 2. Resolve the backend — a blocking gate

Backend selection blocks plotting tasks, but it should not annoy the same user forever. Decide the `backend` value in this order:

1. If the current request explicitly chooses Python or R, use that backend and save it with `scripts/nature_figure_backend.py set python` or `scripts/nature_figure_backend.py set r`.
2. If the request provides a clearly language-specific input file/workflow, use that backend and save it.
3. Otherwise run `scripts/nature_figure_backend.py get`. If it returns `python` or `r`, use the saved preference.
4. If no saved preference exists, ask exactly one concise question — **Python or R? I will remember this as your default.** — and stop. After the user answers, save the answer before proceeding.

- `python` — matplotlib / seaborn.
- `r` — ggplot2 / patchwork / ComplexHeatmap.

Do not guess or choose a backend by aesthetics alone. Only recommend a backend when the user explicitly asks you to choose; then use `references/backend-selection.md`, state the reason, save the selected backend, and proceed. Once selected, the backend is **exclusive** for all drawing, previewing, exporting, and visual QA (see `static/core/contract.md`). This gate does not apply to the explicit OpenRouter AI-schematic route above.

### 3. Load the matching backend fragment

After the backend is resolved, Read the mapped fragment (`static/fragments/backend/python.md` or `static/fragments/backend/r.md`). It carries the backend-only execution rule and the publication quick-start (rcParams/theme and export helper). Do **not** load the other backend's fragment.

### 4. Build the figure using the loaded material

Apply the loaded material in this order:

1. Figure contract (`static/core/contract.md`) — write the core conclusion, map the evidence chain, classify the archetype, set the journal/export contract, before any code.
2. Default stance (`static/core/stance.md`) — archetype-first composition, hero panel, restrained palette, statistics/integrity as part of the figure.
3. Backend fragment — the exclusive Python or R quick-start and execution rule.

The chart serves the scientific logic; aesthetic polish is subordinate to making the core conclusion clear, defensible, and reviewable.

### 5. Reach for references only when needed

The files under `references/` are deep references, not defaults. Open them on demand per the `references.on_demand` table in the manifest — for example `references/figure-contract.md` to build the contract, `references/api.md` for the Python palette and helpers, `references/r-workflow.md` for R, `references/design-theory.md` for color/typography/export rationale, `references/common-patterns.md` and `references/chart-types.md` for layout/chart recipes, `references/nature-2026-observations.md` for real Nature page archetypes, `references/qa-contract.md` before final delivery, `references/figure-delivery-bundle.md` for the panel-first build pipeline (draw each panel as its own unit, review at 1:1, then assemble the composite) and for handing a figure over as an auditable bundle (directory layout, canonical version, source-data traceability), `references/tutorials.md` / `references/demos.md` for worked examples, `references/multipanel-evidence-architecture.md` when the figure is an evidence chain rather than a single claim, `references/nature-article-requirements.md` when the target is the flagship journal Nature, `references/asset-adaptation.md` before reusing someone else's plotting script, and `references/ai-graphical-abstract-workflow.md` for AI-assisted graphical abstracts.

### 6. Run the audit tools before delivery

`scripts/` holds dependency-free preflight and audit tools that make the prose rules in `references/qa-contract.md` executable: `validate_figure.py` on the source before rendering, then `audit_pdf_text.py`, `audit_figure_collisions.py` and `audit_panel_alignment.py` on the export. They share one exit-code contract: 0 pass, 1 fail, 2 usage or I/O error, 3 not run because a dependency is absent, 4 not auditable. **2, 3 and 4 are not passes.** A tool that could not check says so; treating that as success ships an unchecked figure. `figure_source_data.py` loads the table behind a quantitative panel and records which rows were used and which were excluded; `figure_safety.py` refuses an interpolation or a label position it cannot compute honestly. See the `qa_tooling` section of [manifest.yaml](manifest.yaml) for when each applies.

## Why this split

- The static layer is versioned and reviewable. The backend gate is now explicit in the manifest rather than buried in prose.
- The dynamic layer keeps each invocation cheap: only the selected backend's quick-start enters context, and the 2,600+ lines of reference depth load only when a step needs them.
- The router itself is short on purpose. Update fragments and references, not this file, when adding scope.
- For figure *planning* (one claim per figure, panel roles, main-vs-supplement) use the repo's `figure-planner` skill; for one standalone plot's correctness and legibility rules use the sibling `figure-style` skill. This skill covers figure *production*.

---

*Provenance: adapted from github.com/Yuan1z0825/nature-skills (skill `nature-figure`, Apache-2.0). The ~30 MB demo/gallery/chart-atlas asset bundle was removed to keep this repo lean; it lives upstream. Beyond asset references and sibling-skill cross-references, this skill's reference layer carries local corrections to the scale regime and the export settings, and its audit scripts carry fixes for defects measured against this repository's own figures. `ATTRIBUTION.md` in the repository root holds the current file-by-file list, which is checked by `tests/test_license_shipping.py`.*
