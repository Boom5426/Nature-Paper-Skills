# Installation For Codex

Codex reads skills from `~/.codex/skills/`. It has no project-local skill directory, so all installs are global.
Codex installs coexist with Claude Code installs, which read `~/.claude/skills/` or `.claude/skills/`.

## One-Line Install

```bash
curl -fsSL https://raw.githubusercontent.com/Boom5426/Nature-Paper-Skills/main/install.sh | bash -s -- --agent codex
```

With the figure stack:

```bash
curl -fsSL https://raw.githubusercontent.com/Boom5426/Nature-Paper-Skills/main/install.sh | bash -s -- --agent codex --figure
```

From a clone, the installer copies from your working tree instead of downloading:

```bash
git clone https://github.com/Boom5426/Nature-Paper-Skills.git
cd Nature-Paper-Skills
./install.sh --agent codex
```

Useful flags: `--set all` (install all 22 skills), `--dry-run` (preview), `--list` (print the selection), `--dest <dir>` (explicit target), `--ref <branch|tag|sha>` (download and install a specific ref, even when run from a clone), `--help`.

Re-running the installer upgrades in place: each skill directory is removed and re-copied, so files deleted upstream do not linger.

## Ask Codex To Install It

If you would rather not run a script, paste this into Codex from a clone of this repository:

```text
Install the recommended skills from this repository into ~/.codex/skills/: paper-workflow, paper-bootstrap, nature-portfolio-playbook, scientific-writing, manuscript-optimizer, results-section-revision, figure-planner, citation-verifier, data-availability, submission-audit, rebuttal-response, stats-reporting-audit, scientific-prose-style. Copy the full skill directories, not just SKILL.md, and delete any existing copy of a skill before re-copying it. When finished, list the installed directories and use paper-workflow to tell me which skill I should use next for my manuscript.
```

## Install One Skill

```bash
mkdir -p ~/.codex/skills
rm -rf ~/.codex/skills/paper-bootstrap
cp -R skills/core/paper-bootstrap ~/.codex/skills/paper-bootstrap
```

## Manual Install Of The Core Journal Stack

The recommended set is every skill in `skills/core/` plus `skills/venue/nature-portfolio-playbook`.
Copy whole skill directories, not just `SKILL.md`, because some skills include local scripts.

```bash
DEST=~/.codex/skills
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
DEST=~/.codex/skills
mkdir -p "$DEST"
for s in skills/figure/*/; do
  name=$(basename "$s")
  rm -rf "$DEST/$name"
  cp -R "$s" "$DEST/$name"
done
```

## Note

A plain `cp -R` over an existing skill directory merges into it rather than replacing it, so files removed in a newer version of the skill survive the upgrade and two versions end up mixed in one directory. Delete the target directory first, or use `install.sh`, which does this for you.
