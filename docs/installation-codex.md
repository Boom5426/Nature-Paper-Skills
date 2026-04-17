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
cp -R skills/core/submission-audit ~/.codex/skills/
cp -R skills/core/rebuttal-response ~/.codex/skills/
cp -R skills/venue/nature-portfolio-playbook ~/.codex/skills/
```

## Note

Some skills include helper scripts inside their own directories. Copy the whole skill directory, not just `SKILL.md`.
