---
name: paper-workflow
description: Use when deciding which paper-related skill to use or how to sequence manuscript work under `/data/boom/Papers` from project setup through submission and rebuttal.
---

# Paper Workflow

## Overview

Use this skill as the routing map for paper work. It does not replace the specialized skills. It tells you which one to use next.

Default assumption: unless the user explicitly names a conference venue, the manuscript should follow the journal-oriented, `Nature`-style workflow.

When writing follows experiments or analysis performed across multiple sessions, freeze a compact handoff first: current paper story, supported findings, unresolved decisions, and the figure list that actually carries those findings.

## Routing Map

Use:
- `paper-bootstrap` when a project is new, messy, or missing a source of truth
- `nature-portfolio-playbook` when the target is `Nature`, `Nature Methods`, `Nature Biotechnology`, or the venue fit among those journals is still unclear
- `scientific-writing` when drafting or rewriting sections in prose
- `manuscript-optimizer` when the paper's claim structure, evidence chain, terminology, or prose need revision
- `figure-planner` when the main bottleneck is figure logic, panel roles, or legend sync
- `citation-verifier` when bibliography hygiene or source verification is the bottleneck
- `submission-audit` when the paper is near submission or resubmission and needs a preflight pass
- `rebuttal-response` when reviewer comments exist and a response letter plus aligned manuscript edits are needed
- `ml-paper-writing` only when the user explicitly wants a conference paper for venues such as NeurIPS, ICML, ICLR, ACL, AAAI, or COLM

## Default Sequence

For most papers under `/data/boom/Papers`, prefer this order:

1. `paper-bootstrap`
2. `nature-portfolio-playbook` when venue fit or article type is uncertain
3. Refresh `notes/project_truth.md`, `notes/result_summary.md`, and `notes/paper_handoff.md` after any major experimental or figure update
4. `scientific-writing` or `manuscript-optimizer`
5. `figure-planner`
6. `citation-verifier`
7. `submission-audit`
8. `rebuttal-response` after external review

## Common Mistakes

- using conference-style writing skills by default for journal manuscripts
- polishing sections before the active manuscript source of truth is clear
- rewriting the manuscript from experiment memory instead of a current `result_summary.md` or `paper_handoff.md`
- editing figure legends late without rechecking the Results text
- postponing Nature Portfolio article-type or venue-fit decisions until after the paper is mostly rewritten
- treating citation formatting as the same thing as citation verification
- writing a response letter before deciding the underlying manuscript edits
