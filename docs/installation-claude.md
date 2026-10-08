# Installation for Claude Code

Requires Claude Code, Bash and Python 3.9+ (no pip packages). Remote installs also use curl and tar. See [environment verification and file formats](compatibility.md).

## Install

```bash
curl -fsSL https://raw.githubusercontent.com/Boom5426/Nature-Paper-Skills/main/install.sh | bash -s -- --agent claude
```

Default destination: `~/.claude/skills`. For the current project, run from that project and append `--local`; destination: `.claude/skills`.

```bash
git clone https://github.com/Boom5426/Nature-Paper-Skills.git
cd Nature-Paper-Skills
bash install.sh --agent claude
bash install.sh --agent claude --figure
bash install.sh --agent claude --doctor
```

From a clone, installation uses local files. To install into a different project, invoke this script by its absolute path while your terminal is in the intended project. `--local` follows the current working directory.

[Official Claude Code skills documentation](https://code.claude.com/docs/en/skills).

## First use

Open the skill selector or explicitly invoke /paper-workflow. Run the [first-revision example](../examples/first-run/README.md), then use your own active source and evidence. If the skill is absent, verify the scope and agent environment, refresh the skill list or reopen the session. Doctor confirms file integrity; it cannot confirm live session loading.

## Update, preserve and recover

Re-run the installer with the same selection. Existing copies are backed up. `--on-conflict keep` preserves local modifications; `--on-conflict error` stops before changes. `--doctor` lists version records and backup IDs. `--restore <backup-id>` restores replaced copies and backs up the current copies first. `--ref <full-commit-sha>` pins a source version; `--dry-run` previews writes.

See [installation management](installation-management.md) for recovery details and [CHANGELOG](../CHANGELOG.md) for behavior changes. Manual copying bypasses version records and recovery, so the installer is recommended. If copying manually, copy whole directories and the applicable root LICENSE-APACHE and NOTICE files.

To share one installed copy across agents, use the [manual linked layout](installation-management.md#manual-layout-one-canonical-copy-linked-into-the-agent-directory). Update, check and restore its canonical directory; the linking loop preserves existing agent entries.

## Recommended profile

19 skills; figure production/checking uses `--figure`, and all 27 skills use `--set all`.

<!-- recommended-skills -->
- `paper-workflow`
- `paper-bootstrap`
- `scientific-writing`
- `write-scientific-manuscript`
- `manuscript-optimizer`
- `results-section-revision`
- `figure-planner`
- `citation-verifier`
- `claim-source-verification`
- `review-article-architecture`
- `draft-marker-discipline`
- `data-availability`
- `submission-audit`
- `rebuttal-response`
- `stats-reporting-audit`
- `anti-defensive-writing`
- `scientific-prose-style`
- `nature-portfolio-playbook`
- `paper-reviewer`
<!-- /recommended-skills -->
