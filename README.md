# Nature-Paper-Skills

Agent skills for drafting, revising, auditing, and resubmitting `Nature`-style journal manuscripts, with first-class support for `Nature`, `Nature Methods`, and `Nature Biotechnology`.

This repository is opinionated. It is not a generic paper-writing toolbox. It is a journal-first skill stack for claim-driven manuscripts, figure-led storytelling, evidence-aware revision, and Nature Portfolio pre-submission discipline.

## Default Workflow

```text
paper-bootstrap
  -> nature-portfolio-playbook
  -> scientific-writing / manuscript-optimizer
  -> figure-planner
  -> citation-verifier
  -> submission-audit
  -> rebuttal-response
```

The default assumption is:
- journal-first, not conference-first
- `Nature` family by default unless the user or project says otherwise
- structure and evidence chain before sentence polish

## What Is In This Repo

### Core Skills
- `paper-workflow`: route manuscript work to the right skill in the right order
- `paper-bootstrap`: initialize a paper project, source of truth, and state files
- `scientific-writing`: draft or rewrite manuscript sections in full prose
- `manuscript-optimizer`: repair claim structure, evidence chain, terminology, and prose drift
- `figure-planner`: reorganize figures around one main claim each and align legends with Results
- `citation-verifier`: clean local bibliography artifacts before final source verification
- `submission-audit`: run a final manuscript preflight before submission or resubmission
- `rebuttal-response`: turn reviewer comments into aligned manuscript edits and response letters

### Venue Skill
- `nature-portfolio-playbook`: choose among `Nature`, `Nature Methods`, and `Nature Biotechnology`, and run a policy-aware pre-submission check

### Research And Review Skills
- `paper-analyzer`
- `academic-researcher`
- `results-analysis`
- `paper-reviewer`

### Optional Skills
- `reference-audit-guide`
- `conference-paper-writing`
- `academic-presentations`

## Repository Layout

```text
nature-paper-skills/
├── docs/
├── examples/
├── skills/
│   ├── core/
│   ├── venue/
│   ├── research/
│   ├── review/
│   └── optional/
├── .gitignore
├── ATTRIBUTION.md
├── LICENSE
└── README.md
```

Scripts needed by individual skills live inside the skill directories so each skill remains installable as a self-contained unit.

## Quick Start

### Codex

Copy one or more skill directories into `~/.codex/skills/`.

Example:

```bash
mkdir -p ~/.codex/skills
cp -R skills/core/paper-bootstrap ~/.codex/skills/
cp -R skills/core/manuscript-optimizer ~/.codex/skills/
cp -R skills/core/submission-audit ~/.codex/skills/
cp -R skills/venue/nature-portfolio-playbook ~/.codex/skills/
```

Then ask for the skill explicitly or trigger it with a matching task.

### Claude Code

Copy one or more skill directories into either:
- `~/.claude/skills/` for global use
- `.claude/skills/` for project-local use

See [installation-codex.md](docs/installation-codex.md) and [installation-claude.md](docs/installation-claude.md).

## Recommended First Install

If you only install the minimum useful path for journal work, start with:
- `paper-workflow`
- `paper-bootstrap`
- `nature-portfolio-playbook`
- `scientific-writing`
- `manuscript-optimizer`
- `figure-planner`
- `citation-verifier`
- `submission-audit`
- `rebuttal-response`

## Design Principles

- claim-driven, not panel-driven
- one main claim per figure unless a stronger split is clearly necessary
- figure legends are the second layer of result narration
- keep only the numbers needed to support the local claim in the main text
- reverse-outline before polishing stale prose
- never let the front half promise more than the downstream evidence supports
- decide venue fit and article type before optimizing the whole manuscript around the wrong target

See:
- [workflow-map.md](docs/workflow-map.md)
- [skill-map.md](docs/skill-map.md)
- [venue-routing.md](docs/venue-routing.md)
- [design-principles.md](docs/design-principles.md)

## Scope

This repository is for:
- `Nature`-style life-science and computational-biology manuscripts
- methods, frameworks, benchmarks, resources, and translational analysis papers
- drafting, revision, submission preflight, and rebuttal

This repository is not trying to be:
- a universal academic-writing library
- a conference-template collection
- a full research orchestration platform
- a replacement for journal author guidelines

## Attribution

Some skills in this repository were adapted from previously existing local skills or broader agent-skill libraries. See [ATTRIBUTION.md](ATTRIBUTION.md).
