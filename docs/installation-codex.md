# Installation for Codex

Requires Codex, Bash and Python 3.9+ (no pip packages). Remote installs also use curl and tar. See [environment verification and file formats](compatibility.md).

## Install

```bash
curl -fsSL https://raw.githubusercontent.com/Boom5426/Nature-Paper-Skills/main/install.sh | bash -s -- --agent codex
```

Default destination: `~/.agents/skills`. For the current project, run from that project and append `--local`; destination: `.agents/skills`.

```bash
git clone https://github.com/Boom5426/Nature-Paper-Skills.git
cd Nature-Paper-Skills
bash install.sh --agent codex
bash install.sh --agent codex --figure
bash install.sh --agent codex --doctor
```

From a clone, installation uses local files. To install into a different project, invoke this script by its absolute path while your terminal is in the intended project. `--local` follows the current working directory.

Older clients may use `~/.codex/skills`. Verify the client, then set `--dest ~/.codex/skills` if required. The installer does not delete or migrate that legacy path. Avoid conflicting copies.

[Official Codex skill locations](https://developers.openai.com/codex/build-skills).

## First use

Open the skill selector or explicitly invoke $paper-workflow. Run the [first-revision example](../examples/first-run/README.md), then use your own active source and evidence. If the skill is absent, verify the scope and agent environment, refresh the skill list or reopen the session. Doctor confirms file integrity; it cannot confirm live session loading.

## Update, preserve and recover

Re-run the installer with the same selection. Existing copies are backed up. `--on-conflict keep` preserves local modifications; `--on-conflict error` stops before changes. `--doctor` lists version records and backup IDs. `--restore <backup-id>` restores replaced copies and backs up the current copies first. `--ref <full-commit-sha>` pins a source version; `--dry-run` previews writes.

See [installation management](installation-management.md) for recovery details and [CHANGELOG](../CHANGELOG.md) for behavior changes. Manual copying bypasses version records and recovery, so the installer is recommended. If copying manually, copy whole directories and the applicable root LICENSE-APACHE and NOTICE files.

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
