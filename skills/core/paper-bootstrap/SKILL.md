---
name: paper-bootstrap
description: Use when starting a new manuscript project or cleaning up an existing paper directory and you need a standard structure, active source files, project memory, and venue defaults before deeper writing begins.
---

# Paper Bootstrap

## Overview

Use this skill to make a paper project writable before trying to make it good. The goal is not to generate boilerplate. The goal is to identify the real manuscript source of truth, create only the folders that help the workflow, and lock the project onto the correct venue and contribution framing early.

Default assumption: broad-impact journal work should start from the global `Nature`-style preference unless the user explicitly overrides the venue.

When the manuscript depends on experiments, figures, or results produced across multiple rounds, initialize lightweight project-state documents early so writing does not depend on memory alone: `project_truth.md`, `decision_log.md`, `result_summary.md`, and `paper_handoff.md`.

Use the helper script when you need a clean baseline layout quickly:

```bash
python ~/.codex/skills/paper-bootstrap/scripts/init_paper_layout.py path/to/paper
# Claude Code (global install): replace ~/.codex/skills with ~/.claude/skills
# Claude Code (project-local install): replace ~/.codex/skills with .claude/skills
```

## When To Use

Use this skill when:
- A new paper directory is being created
- An existing paper directory has drafts, figures, notes, and outputs scattered across multiple places
- It is unclear which file is the active manuscript source of truth
- The project has no paper-specific memory yet
- The writing workflow needs a clean starting structure before revision begins

Do not use this skill for:
- Late-stage section polishing
- Figure-by-figure logic repair inside an already stable manuscript
- Conference-template conversion after the paper structure is already settled

## Bootstrap Order

1. Inspect the current paper directory before creating anything.
2. Identify the active manuscript source of truth.
3. Classify the paper's contribution type:
   - method
   - framework
   - benchmark
   - resource
   - biological finding
   - mixed, with one clearly dominant contribution
4. Lock the working venue style:
   - default to `Nature`-style unless the user says otherwise
   - record venue-specific overrides only if they materially affect structure
5. Create only the directories that the project actually needs.
6. Create or reuse lightweight state files when they will reduce drift:
   - `notes/project_truth.md`
   - `notes/decision_log.md`
   - `notes/result_summary.md`
   - `notes/paper_handoff.md`
7. Save or update project memory with the stable local constraints.
8. End with a short startup summary:
   - active manuscript file
   - dominant contribution type
   - venue style
   - missing assets or unresolved ambiguity
   - recommended next revision step

## Preferred Project Layout

Do not force this layout mechanically. Use it as the default skeleton when the repository is messy or empty.

- `input/` for external source material, reviewer comments, and imported files
- `notes/` for working notes, claim maps, figure plans, meeting summaries, and lightweight state files
- `figures/` for source figures and editable figure assets
- `output/doc/` for active manuscript drafts and exported versions
- `output/review/` for audits, revision memos, and pre-submission checks

Default state files inside `notes/` when the project does not already have equivalents:
- `project_truth.md` for the current paper story, active manuscript, central claim, and stable constraints
- `decision_log.md` for durable framing or scope decisions that future revisions must respect
- `result_summary.md` for experiment-to-manuscript translation of supported findings, weak findings, and figure anchors
- `paper_handoff.md` for the current writing-ready package: what is ready to draft, what still lacks evidence, and which figures or tables carry each point

If the project already has an established structure, preserve it and map the workflow onto that structure instead of rebuilding everything.

## Memory Rules

Write project memory only for stable local facts such as:
- the manuscript's dominant contribution type
- persistent figure-role constraints
- project-specific terminology
- local preferences that do not generalize beyond the paper

Do not write project memory for:
- transient to-do lists
- single-round wording preferences
- one-off tactical decisions that are unlikely to matter next week

## Common Mistakes

- Creating a directory tree before checking what already exists
- Treating every paper like a methods paper when the real contribution is a framework or benchmark
- Leaving multiple draft files active with no declared source of truth
- Carrying conference-style structure into a broad-impact journal manuscript by default
- Writing directly from remembered experiment outcomes instead of refreshing `result_summary.md` and `paper_handoff.md`
- Saving local clutter into memory instead of only the stable constraints

## Output Standard

When you finish bootstrapping, report:
- active source file
- chosen venue style
- contribution type
- directories created or reused
- state files created or reused
- project-memory items saved
- next concrete writing step
