# Installation For Claude Code

Claude Code supports both global installs in `~/.claude/skills/` and project-local installs in `.claude/skills/`.
Use the project-local option when you want repo-specific behavior without affecting other projects.
Neither option conflicts with Codex, which reads from `~/.codex/skills/`.

## Global Install

```bash
mkdir -p ~/.claude/skills
cp -R skills/core/paper-workflow ~/.claude/skills/
cp -R skills/core/paper-bootstrap ~/.claude/skills/
cp -R skills/core/scientific-writing ~/.claude/skills/
cp -R skills/core/manuscript-optimizer ~/.claude/skills/
cp -R skills/core/results-section-revision ~/.claude/skills/
cp -R skills/core/figure-planner ~/.claude/skills/
cp -R skills/core/citation-verifier ~/.claude/skills/
cp -R skills/core/data-availability ~/.claude/skills/
cp -R skills/core/submission-audit ~/.claude/skills/
cp -R skills/core/rebuttal-response ~/.claude/skills/
cp -R skills/core/stats-reporting-audit ~/.claude/skills/
cp -R skills/core/scientific-prose-style ~/.claude/skills/
cp -R skills/venue/nature-portfolio-playbook ~/.claude/skills/
```

## Project-Local Install

```bash
mkdir -p .claude/skills
cp -R skills/core/paper-workflow .claude/skills/
cp -R skills/core/paper-bootstrap .claude/skills/
cp -R skills/core/scientific-writing .claude/skills/
cp -R skills/core/manuscript-optimizer .claude/skills/
cp -R skills/core/results-section-revision .claude/skills/
cp -R skills/core/figure-planner .claude/skills/
cp -R skills/core/citation-verifier .claude/skills/
cp -R skills/core/data-availability .claude/skills/
cp -R skills/core/submission-audit .claude/skills/
cp -R skills/core/rebuttal-response .claude/skills/
cp -R skills/core/stats-reporting-audit .claude/skills/
cp -R skills/core/scientific-prose-style .claude/skills/
cp -R skills/venue/nature-portfolio-playbook .claude/skills/
```

## Figure Stack (Optional)

These produce and check publication figures. They need a plotting backend (Python matplotlib/seaborn or R ggplot2/patchwork/ComplexHeatmap). `nature-figure`'s optional AI-schematic route additionally needs an `OPENROUTER_API_KEY`; the Python/R plotting core works without it. Use `~/.claude/skills/` for a global install or `.claude/skills/` for a project-local one.

```bash
mkdir -p ~/.claude/skills
cp -R skills/figure/nature-figure ~/.claude/skills/
cp -R skills/figure/figure-style ~/.claude/skills/
```

## Note

If you install the full core stack, copy the entire skill directories rather than only `SKILL.md`, because some skills include local scripts.
When helper commands inside a skill mention `~/.claude/skills`, use `.claude/skills` instead if you chose the project-local install.
