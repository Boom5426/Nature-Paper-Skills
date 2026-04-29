# Nature-Paper-Skills

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Nature-first](https://img.shields.io/badge/focus-Nature%20series-1f6feb)](docs/venue-routing.md)
[![Workflow](https://img.shields.io/badge/workflow-claim--driven-blue)](docs/workflow-map.md)
[![Codex](https://img.shields.io/badge/agent-Codex-0a7ea4)](docs/installation-codex.md)
[![Claude Code](https://img.shields.io/badge/agent-Claude%20Code-cc785c)](docs/installation-claude.md)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![GitHub stars](https://img.shields.io/github/stars/Boom5426/nature-paper-skills?style=social)](https://github.com/Boom5426/nature-paper-skills/stargazers)

[简体中文](README.md) | English

Agent skills for drafting, revising, auditing, and resubmitting `Nature`-series journal manuscripts.

This repository is opinionated. It is not a generic paper-writing toolbox. It is a journal-first skill stack for claim-driven manuscripts, figure-led storytelling, evidence-aware revision, and Nature-series pre-submission discipline.

## Quick Start

The fastest path is not to read every skill first. Install the recommended stack, then let the agent route your next step.

### Step 1: Clone The Repository

```bash
git clone https://github.com/Boom5426/nature-paper-skills.git
cd nature-paper-skills
```

### Step 2: Choose An Install Mode

#### Option A: Ask Codex To Install It

Paste this into Codex:

```text
Install the recommended skills from this repository into ~/.codex/skills/: paper-workflow, paper-bootstrap, nature-portfolio-playbook, scientific-writing, manuscript-optimizer, results-section-revision, figure-planner, citation-verifier, submission-audit, rebuttal-response. Copy the full skill directories, not just SKILL.md. When finished, list the installed directories and use paper-workflow to tell me which skill I should use next for my manuscript.
```

#### Option B: Ask Claude Code To Install It

Paste this into Claude Code:

```text
Install the recommended skills from this repository into ~/.claude/skills/: paper-workflow, paper-bootstrap, nature-portfolio-playbook, scientific-writing, manuscript-optimizer, results-section-revision, figure-planner, citation-verifier, submission-audit, rebuttal-response. Copy the full skill directories, not just SKILL.md. When finished, list the installed directories and use paper-workflow to tell me which skill I should use next for my manuscript.
```

#### Option C: Install Manually

If you prefer shell commands, clone the repo and copy the full skill directories.

Codex:

```bash
mkdir -p ~/.codex/skills
cp -R \
  skills/core/paper-workflow \
  skills/core/paper-bootstrap \
  skills/core/scientific-writing \
  skills/core/manuscript-optimizer \
  skills/core/results-section-revision \
  skills/core/figure-planner \
  skills/core/citation-verifier \
  skills/core/submission-audit \
  skills/core/rebuttal-response \
  skills/venue/nature-portfolio-playbook \
  ~/.codex/skills/
```

Claude Code:

```bash
mkdir -p ~/.claude/skills
cp -R \
  skills/core/paper-workflow \
  skills/core/paper-bootstrap \
  skills/core/scientific-writing \
  skills/core/manuscript-optimizer \
  skills/core/results-section-revision \
  skills/core/figure-planner \
  skills/core/citation-verifier \
  skills/core/submission-audit \
  skills/core/rebuttal-response \
  skills/venue/nature-portfolio-playbook \
  ~/.claude/skills/
```

### First Prompt After Install

After installation, a good first prompt is:

```text
Use paper-workflow to tell me which skill I should use next for this manuscript.
```

For more installation detail, see [docs/installation-codex.md](docs/installation-codex.md) and [docs/installation-claude.md](docs/installation-claude.md).

## Default Workflow

```text
paper-bootstrap
  -> nature-portfolio-playbook
  -> scientific-writing / manuscript-optimizer
  -> figure-planner
  -> results-section-revision
  -> citation-verifier
  -> submission-audit
  -> rebuttal-response
```

The default assumption is:
- journal-first, not conference-first
- `Nature`-series journals by default unless the user or project says otherwise
- structure and evidence chain before sentence polish

## What Is In This Repo

### Core Skills
- `paper-workflow`: route manuscript work to the right skill in the right order
- `paper-bootstrap`: initialize a paper project, source of truth, and state files
- `scientific-writing`: draft or rewrite manuscript sections in full prose
- `manuscript-optimizer`: repair claim structure, evidence chain, terminology, and prose drift
- `results-section-revision`: repair late-stage narrative flow inside Results subsections
- `figure-planner`: reorganize figures around one main claim each and align legends with Results
- `citation-verifier`: clean local bibliography artifacts before final source verification
- `submission-audit`: run a final manuscript preflight before submission or resubmission
- `rebuttal-response`: turn reviewer comments into aligned manuscript edits and response letters

### Venue Skill
- `nature-portfolio-playbook`: position the manuscript within `Nature`-series journals and run a policy-aware pre-submission check

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
├── .github/
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
├── CONTRIBUTING.md
├── LICENSE
├── README.md
└── README.en.md
```

Scripts needed by individual skills live inside the skill directories so each skill remains installable as a self-contained unit.

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

## Repository Metadata

Suggested GitHub repository description, topics, and About-panel copy live in [.github/repo-metadata.md](.github/repo-metadata.md).

## Scope

This repository is for:
- `Nature`-series life-science and computational-biology manuscripts
- methods, frameworks, benchmarks, resources, and translational analysis papers
- drafting, revision, submission preflight, and rebuttal

This repository is not trying to be:
- a universal academic-writing library
- a conference-template collection
- a full research orchestration platform
- a replacement for journal author guidelines

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution rules, naming conventions, and pull-request expectations.

## Attribution

Some skills in this repository were adapted from previously existing local skills or broader agent-skill libraries. See [ATTRIBUTION.md](ATTRIBUTION.md).
