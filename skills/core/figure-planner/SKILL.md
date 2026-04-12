---
name: figure-planner
description: Use when designing, restructuring, or auditing manuscript figures and you need to define one main claim per figure, assign panel roles, align legends with the text, or decide what belongs in main figures versus supplement.
---

# Figure Planner

## Overview

Use this skill when the bottleneck is no longer sentence writing but figure logic. The goal is to make each figure carry a defensible scientific job, keep the panel set coherent, and ensure that the legend and Results text tell the same story.

This skill is narrower than `manuscript-optimizer`. Use `manuscript-optimizer` when the whole paper structure is unstable. Use `figure-planner` when the central issue is what each figure should prove and how each panel should function.

## When To Use

Use this skill when:
- a figure feels overloaded, fragmented, or hard to summarize
- the paper has too many Results subsections driven by panel count
- it is unclear what belongs in the main figure versus the supplement
- legends, panel letters, and Results text may have drifted apart
- you need to redesign figure titles or panel grouping around claims rather than around plotting convenience

Do not use this skill for:
- low-level visual styling only
- final proofreading without figure changes
- manuscript-wide claim restructuring that exceeds the figures themselves

## Core Rule

Each main figure should earn its place by carrying one dominant claim.

If a figure cannot be summarized by one clean sentence, either:
- split it,
- demote part of it to the supplement,
- or rewrite the figure around a clearer claim.

## Panel Roles

Assign each panel one primary role before writing the legend or Results paragraph:

- claim-supporting evidence
- methodological bridge or definition
- validation under a new regime
- ranking or benchmark comparison
- translational or practical consequence
- case illustration
- failure mode or limitation

Do not let one panel pretend to do three jobs at once.

## Planning Order

1. Write the single-sentence claim of the figure.
2. List the minimum panels needed to support that claim.
3. Assign each panel one role.
4. Decide which panel is the anchor panel:
   - the panel the Results paragraph should revolve around
5. Move secondary detail to:
   - another figure
   - the supplement
   - the legend
6. Rewrite the figure title and legend to match the actual claim.
7. Check that the Results subsection matches the same panel logic.

## Main Figure Versus Supplement

Keep in the main figure:
- the panels required to establish the core claim
- the key comparison readers must see immediately
- the panel that defines a new metric, decomposition, or evaluation regime when that definition is part of the argument

Move to the supplement:
- robustness variants
- denser method-by-method comparisons
- extended cases
- secondary ablations
- additional examples that support but do not define the main claim

## Legend Rules

Legends should do more than decode axes.

Each legend should:
- define the role of each panel
- preserve the key quantitative anchors omitted from the compressed main text
- stay consistent with panel letters, metrics, datasets, and baselines
- avoid interpretation that is stronger than the plotted evidence

## Visual Hygiene Pass

After the figure logic is stable, run one visual-hygiene pass:

- keep figure-internal fonts consistent and close to the manuscript's reading scale
- prefer vector graphics for plots, diagrams, and schematic panels when possible
- use a restrained palette; keep the same category in the same color family
- avoid accidental salience from one panel or module being much darker or brighter unless that emphasis is deliberate
- trim dead margins and unnecessary whitespace around panels
- reduce text load inside the figure; let shapes, alignment, and grouping do more of the explanatory work
- keep arrow direction and symbol conventions consistent when the figure is showing flow or process
- borrow proven table or panel arrangements as layout references when useful, but do not inherit conference-template clutter by default

## Common Failure Modes

- one figure trying to carry multiple unrelated claims
- panel order following plotting chronology instead of argument logic
- methodological bridge panels described as generic motivation
- Results text claiming something the legend or panel does not support
- supplementary figures cited too vaguely when one panel is doing the real work
- keeping weak auxiliary metrics at headline level instead of demoting them
- inconsistent figure typography, whitespace, or color logic making the scientific comparison harder to read

## Output Standard

When using this skill, produce:
- the figure's one-sentence claim
- the proposed panel list with roles
- what stays in the main figure versus what moves to supplement
- the legend logic
- the visual-hygiene notes that still need attention
- the matching Results subsection title or topic sentence
