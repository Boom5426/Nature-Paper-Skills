# Installation For Codex

## Install One Skill

Copy a skill directory into `~/.codex/skills/`.

Example:

```bash
mkdir -p ~/.codex/skills
cp -R skills/core/paper-bootstrap ~/.codex/skills/
```

## Install The Core Journal Stack

```bash
mkdir -p ~/.codex/skills
cp -R skills/core/paper-workflow ~/.codex/skills/
cp -R skills/core/paper-bootstrap ~/.codex/skills/
cp -R skills/core/scientific-writing ~/.codex/skills/
cp -R skills/core/manuscript-optimizer ~/.codex/skills/
cp -R skills/core/results-section-revision ~/.codex/skills/
cp -R skills/core/figure-planner ~/.codex/skills/
cp -R skills/core/citation-verifier ~/.codex/skills/
cp -R skills/core/data-availability ~/.codex/skills/
cp -R skills/core/submission-audit ~/.codex/skills/
cp -R skills/core/rebuttal-response ~/.codex/skills/
cp -R skills/core/stats-reporting-audit ~/.codex/skills/
cp -R skills/core/scientific-prose-style ~/.codex/skills/
cp -R skills/venue/nature-portfolio-playbook ~/.codex/skills/
```

## Install The Figure Stack (Optional)

These produce and check publication figures. They need a plotting backend (Python matplotlib/seaborn or R ggplot2/patchwork/ComplexHeatmap). `nature-figure`'s optional AI-schematic route additionally needs an `OPENROUTER_API_KEY`; the Python/R plotting core works without it.

```bash
mkdir -p ~/.codex/skills
cp -R skills/figure/nature-figure ~/.codex/skills/
cp -R skills/figure/figure-style ~/.codex/skills/
```

## Note

Some skills include helper scripts inside their own directories. Copy the whole skill directory, not just `SKILL.md`.
Codex installs can coexist with Claude Code installs because Codex reads `~/.codex/skills/` while Claude Code reads `~/.claude/skills/` or `.claude/skills/`.
