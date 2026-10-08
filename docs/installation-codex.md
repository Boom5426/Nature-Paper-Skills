# Installation for Codex

Requires Codex, Bash and Python 3.9+ (no pip packages). Remote installs also use curl and tar. See [environment verification and file formats](compatibility.md).

## Install

To let the agent perform installation, copy the instruction in the [README](../README.md#1-install). [INSTALL.md](../INSTALL.md) routes the request to the actual client environment and does not require an explicit creator mention. Terminal commands are below if preferred.

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

## Windows desktop app

The [current Windows app](https://learn.chatgpt.com/docs/windows/windows-app) supports skills and uses a Windows-native agent with PowerShell by default. This repository supplies a Bash installer; pasting the quickstart into PowerShell does not make it a native installer.

### Windows-native agent

Run these commands in **Git Bash**, with Windows Python 3.9+ available. They derive an explicit destination from `USERPROFILE`; confirm that this is the same Windows user as the app:

```bash
NPS_WINDOWS_HOME="$(cygpath -m "${USERPROFILE:?USERPROFILE is not set}")" &&
curl -fsSL https://raw.githubusercontent.com/Boom5426/Nature-Paper-Skills/main/install.sh |
  bash -s -- --agent codex --dest "$NPS_WINDOWS_HOME/.agents/skills"
```

Check the printed destination, then refresh/reopen the app and select `paper-workflow`. This repository does not supply a PowerShell installer, and native Windows installation/discovery remains unverified.

### WSL2 agent

Choose **WSL** as the agent environment in app settings and restart the app. Open the same distribution used by the agent, then run:

```bash
curl -fsSL https://raw.githubusercontent.com/Boom5426/Nature-Paper-Skills/main/install.sh | bash -s -- --agent codex
```

The destination is that Linux user's `~/.agents/skills`, separate from the Windows user's home. For Codex CLI in WSL2, run the installer in the distribution where you launch the CLI.

The app's integrated terminal and agent environment are configured separately. Choosing a WSL terminal alone does not switch the agent. Native Windows and WSL installation/discovery have not been exercised by this repository's Linux/macOS checks.

When using the built-in `skill-installer`, select individual directories such as `skills/core/paper-workflow`, each containing `SKILL.md`. The repository root is a collection of 27 skills and has no `SKILL.md`; passing only its root URL to the installer leaves the skill path unspecified. Preserve each skill's supporting files and applicable license/NOTICE files. See the [skill map](skill-map.md) for the available directories.

## ChatGPT Work on the web

[OpenAI Docs](https://learn.chatgpt.com/docs/build-skills) distinguishes local standalone skills from skills distributed through plugins. [Workspace skill and plugin controls](https://learn.chatgpt.com/docs/enterprise/skills) are separate from filesystem installation.

Use the same copyable agent instruction from the README. [INSTALL.md](../INSTALL.md) asks the agent to check the account's supported registration flow and perform resource handling itself. It does not require selecting `@skill-creator`, running a build command or uploading a ZIP.

Automatic web registration remains unverified. The [web distribution guide](installation-chatgpt-work.md) covers maintainer packaging, plugin publishing and administrator import. Local file installation and a web account installation need separate verification.

## First use

Open the skill selector or explicitly invoke $paper-workflow. Run the [first-revision example](../examples/first-run/README.md), then use your own active source and evidence. If the skill is absent, verify the scope and agent environment, refresh the skill list or reopen the session. Doctor confirms file integrity; it cannot confirm live session loading.

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
