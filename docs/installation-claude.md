# Installation For Claude Code

## Global Install

```bash
mkdir -p ~/.claude/skills
cp -R skills/core/paper-bootstrap ~/.claude/skills/
cp -R skills/core/manuscript-optimizer ~/.claude/skills/
cp -R skills/core/results-section-revision ~/.claude/skills/
cp -R skills/core/submission-audit ~/.claude/skills/
cp -R skills/venue/nature-portfolio-playbook ~/.claude/skills/
```

## Project-Local Install

```bash
mkdir -p .claude/skills
cp -R skills/core/paper-bootstrap .claude/skills/
cp -R skills/core/manuscript-optimizer .claude/skills/
cp -R skills/core/results-section-revision .claude/skills/
cp -R skills/core/submission-audit .claude/skills/
cp -R skills/venue/nature-portfolio-playbook .claude/skills/
```

## Note

If you install the full core stack, copy the entire skill directories rather than only `SKILL.md`, because some skills include local scripts.
