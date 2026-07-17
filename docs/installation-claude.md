# Installation For Claude Code

Claude Code reads skills from `~/.claude/skills/` (global) and `.claude/skills/` (project-local).
Use the project-local option when you want repo-specific behavior without affecting other projects.
Neither conflicts with Codex, which reads `~/.codex/skills/`.

## One-Line Install

```bash
curl -fsSL https://raw.githubusercontent.com/Boom5426/Nature-Paper-Skills/main/install.sh | bash -s -- --agent claude
```

Project-local instead of global:

```bash
curl -fsSL https://raw.githubusercontent.com/Boom5426/Nature-Paper-Skills/main/install.sh | bash -s -- --agent claude --local
```

With the figure stack:

```bash
curl -fsSL https://raw.githubusercontent.com/Boom5426/Nature-Paper-Skills/main/install.sh | bash -s -- --agent claude --figure
```

From a clone, the installer copies from your working tree instead of downloading:

```bash
git clone https://github.com/Boom5426/Nature-Paper-Skills.git
cd Nature-Paper-Skills
./install.sh --agent claude
```

Useful flags: `--set all` (install all 22 skills), `--dry-run` (preview), `--list` (print the selection), `--dest <dir>` (explicit target), `--ref <branch|tag|sha>` (download and install a specific ref, even when run from a clone), `--help`.

Re-running the installer upgrades in place: each skill directory is removed and re-copied, so files deleted upstream do not linger.

## Ask Claude Code To Install It

If you would rather not run a script, paste this into Claude Code from a clone of this repository:

```text
Install the recommended skills from this repository into ~/.claude/skills/: paper-workflow, paper-bootstrap, nature-portfolio-playbook, scientific-writing, manuscript-optimizer, results-section-revision, figure-planner, citation-verifier, data-availability, submission-audit, rebuttal-response, stats-reporting-audit, scientific-prose-style. Copy the full skill directories, not just SKILL.md, and delete any existing copy of a skill before re-copying it. When finished, list the installed directories and use paper-workflow to tell me which skill I should use next for my manuscript.
```

For a project-local install, change the target directory to `.claude/skills/`.

## Manual Install

The recommended set is every skill in `skills/core/` plus `skills/venue/nature-portfolio-playbook`.
Copy whole skill directories, not just `SKILL.md`, because some skills include local scripts.

```bash
DEST=~/.claude/skills          # project-local: DEST=.claude/skills
mkdir -p "$DEST"
for s in skills/core/*/ skills/venue/nature-portfolio-playbook/; do
  name=$(basename "$s")
  rm -rf "$DEST/$name"         # replace rather than merge; see the note below
  cp -R "$s" "$DEST/$name"
done
```

## Figure Stack (Optional)

These produce and check publication figures. They need a plotting backend (Python matplotlib/seaborn or R ggplot2/patchwork/ComplexHeatmap). `nature-figure`'s optional AI-schematic route additionally needs an `OPENROUTER_API_KEY`; the Python/R plotting core works without it.

```bash
DEST=~/.claude/skills
mkdir -p "$DEST"
for s in skills/figure/*/; do
  name=$(basename "$s")
  rm -rf "$DEST/$name"
  cp -R "$s" "$DEST/$name"
done
```

## Notes

- A plain `cp -R` over an existing skill directory merges into it rather than replacing it, so files removed in a newer version of the skill survive the upgrade and two versions end up mixed in one directory. Delete the target directory first, or use `install.sh`, which does this for you.
- When helper commands inside a skill mention `~/.claude/skills`, use `.claude/skills` instead if you chose the project-local install.
