<div align="center">

# 🧬 Nature-Paper-Skills

**Turn scientific drafts into clear, evidence-grounded journal manuscripts.**

Skills for Codex and Claude Code: structure, revision, figures, references, submission and rebuttal.
Built for Nature-series life-science, computational-biology and methods papers.

[![Skills](https://img.shields.io/badge/skills-27-8a63d2)](docs/skill-map.md)
[![CI](https://github.com/Boom5426/Nature-Paper-Skills/actions/workflows/ci.yml/badge.svg)](https://github.com/Boom5426/Nature-Paper-Skills/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT%20%2B%20Apache--2.0-green)](#license)
[![Stars](https://img.shields.io/github/stars/Boom5426/Nature-Paper-Skills?style=social)](https://github.com/Boom5426/Nature-Paper-Skills/stargazers)

**English** · [简体中文](README.zh-CN.md) · [Quick start](#quick-start) · [Choose a task](#choose-a-task) · [All skills](docs/skill-map.md)

</div>

## See what changes

The writing layer removes project-log language and defensive scaffolding while retaining the facts that make a result interpretable.

| Before | After | What stays |
|---|---|---|
| “We carefully verified that survival changed by 1 percentage point (95% CI −3 to 5), which should not be overinterpreted.” | “Survival changed by 1 percentage point (95% CI −3 to 5), with no clear evidence of improvement.” | The measured effect, interval and uncertainty |
| “These orderings should not be read as a universal ranking across all settings.” | “These orderings hold for the tested settings.” | The scope of the comparison |
| “The analysis reads the final output from `results/final_scores.csv`.” | “The analysis uses the measured response scores.” | The scientific object; file access details belong in the appropriate methods/data documentation |

These are illustrative edits, not claims about a real study. A scientific limitation or reproducibility detail must remain wherever it is needed. See [worked examples](skills/core/anti-defensive-writing/references/worked-examples.md) and the [complete first-run example](examples/first-run/README.md).

## Quick start

**Requirements:** Codex or Claude Code, Bash, and Python 3.9+ (standard library only). Remote installation also uses `curl` and `tar`. On Windows, use an agent environment in WSL or Git Bash; this Bash command is not a PowerShell command. Check [environments and file formats](docs/compatibility.md) for verification status.

Install the recommended 19-skill stack, including reviewer responses:

```bash
curl -fsSL https://raw.githubusercontent.com/Boom5426/Nature-Paper-Skills/main/install.sh | bash
```

To choose explicitly, append `-s -- --agent codex` or `-s -- --agent claude` after `bash`.
Read [install.sh](install.sh) first if you prefer, or [install from a clone](docs/installation-codex.md). Existing copies are backed up before replacement; [update and restore](docs/installation-management.md).

**Try one complete task.** Put your current manuscript and its supporting results in the agent's working folder, then ask:

```text
Use paper-workflow. Revise the Results paragraph in draft.md using evidence.md.
Preserve measured values and figure references. Save a revised copy and briefly
explain the material changes.
```

For a ready-made input and a reference output, use [First successful revision](examples/first-run/README.md). In Codex CLI/IDE you can explicitly mention `$paper-workflow`; in Claude Code invoke `/paper-workflow`. If the skill is not visible, refresh the skill list or reopen the session; see [troubleshooting](docs/installation-management.md#troubleshooting).

You can then use ordinary requests such as “improve this manuscript” or name a specialist. The dispatcher diagnoses the task, states the scope, and applies the steps needed. You do not need to memorize skill names.

## Choose a task

| Your task | Provide | Expected result | Entry |
|---|---|---|---|
| Improve a whole manuscript | Current draft, relevant results/figures, target venue if decided | Revised draft, key changes, unresolved evidence gaps | `paper-workflow` |
| Fix a paragraph | Passage, surrounding context, requested scope | Replacement passage with a brief explanation where useful | `write-scientific-manuscript` |
| Remove audit/defensive writing | Main text, SI, legend or availability statement | Direct scientific prose retaining numbers and necessary conditions | `anti-defensive-writing` |
| Plan or make figures | Scientific question, result table or existing figure | Panel plan; rendered files when data and tools are available | `figure-planner`; add `--figure` for production |
| Check before submission | Final draft, SI, bibliography and venue | Prioritized findings with locations; unchecked categories identified | `submission-audit` |
| Reply to reviewers | Original comments, manuscript, completed new evidence | Numbered response draft and matching manuscript changes | `paper-workflow` |

A request to **review or suggest** produces findings. A request to **revise** produces edits within the requested scope. Missing evidence is surfaced; it is never written into existence.

## What makes the workflow useful

- **Scientific reasoning before polish.** Check the question, contribution and evidence chain before changing sentences. Preserve settled text when it needs no repair.
- **Figures carry claims.** Plan the role of each panel and keep legends and Results aligned. The optional figure stack includes executable checks for text size, collisions, alignment and source data.
- **Write for the reader.** Remove audit, defensive, self-critical, commentary, developer-facing and future-commitment language from the manuscript. Preserve negative results, required reporting and reproducibility facts.
- **Separate citation checks.** Bibliography consistency, live reference existence and claim-to-source support are different checks. A local bibliography scan does not prove a paper exists or supports a claim.
- **Keep work proportional.** Diagnose relevant layers, edit those with problems, and check affected dependencies. Research articles and Reviews have different routes; a long research draft remains a research article.

[Workflow](docs/workflow-map.md) · [Writing principles](docs/design-principles.md) · [Figure workflow and exit codes](docs/figure-workflow.md) · [Task examples](docs/task-recipes.md)

## Installation options

```bash
# From a clone; no source download unless --ref is supplied
git clone https://github.com/Boom5426/Nature-Paper-Skills.git
cd Nature-Paper-Skills
bash install.sh --agent codex --local     # this project's .agents/skills
bash install.sh --agent claude --local    # this project's .claude/skills
bash install.sh --agent both             # both user-level locations
bash install.sh --agent codex --figure   # add figure production/checking
bash install.sh --agent codex --set all  # all 27 skills
bash install.sh --agent codex --dry-run  # preview
bash install.sh --agent codex --doctor   # file/version/dependency checks
```

**Default:** 19 writing, review and venue skills. **Figure add-on:** `nature-figure` and `figure-style`; needs Python plotting packages or an R plotting setup. **All:** 27 skills, adding literature/research tools and optional conference/presentation/reference-verification workflows. The core writing and data-plotting routes do not require an OpenRouter key; only the optional AI schematic draft route does. Follow the target journal's image policy.

Agent-specific instructions: [Codex](docs/installation-codex.md) · [Claude Code](docs/installation-claude.md). Version history: [CHANGELOG](CHANGELOG.md). Pin an immutable commit with `--ref <full-commit-sha>`; the installer records the source and file hashes.

## Scope and limits

This is a focused journal-writing workflow for life sciences, computational biology, methods, benchmarks and resources. Explicit venue and project instructions take precedence over its Nature-style defaults. It is independent of Nature Portfolio and does not predict acceptance.

Skills provide instructions and some helper scripts. They do not themselves supply a Word editor, PDF renderer, LaTeX installation, browsing access or experimental evidence. [Compatibility](docs/compatibility.md) separates readable inputs from editable/exportable outputs.

Repository tests cover scripts, installation and consistency. [Behavior cases](evals/README.md) check task scope, evidence preservation and honest reporting of missing capabilities; their limitations and recorded runs are documented separately.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Changes to user-facing behavior should include a task case or an example, and both READMEs should stay aligned. Component provenance is in [ATTRIBUTION.md](ATTRIBUTION.md).

## Acknowledgements

Parts of this repository were inspired by [OpenLAIR/dr-claw](https://github.com/OpenLAIR/dr-claw), [Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills), and the Claude Science skill pack.

The figure layer also draws on design observations from [ChenLiu-1996/figures4papers](https://github.com/ChenLiu-1996/figures4papers). None of that repository's code or prose is distributed here; see [THIRD_PARTY_NOTICES](skills/figure/nature-figure/THIRD_PARTY_NOTICES.md).

## License

Original content is [MIT](LICENSE). Components carrying Apache-2.0 material retain [LICENSE-APACHE](LICENSE-APACHE) and [NOTICE](NOTICE), including in installer-managed copies. See [ATTRIBUTION](ATTRIBUTION.md) for coverage.

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Boom5426/Nature-Paper-Skills&type=Date)](https://star-history.com/#Boom5426/Nature-Paper-Skills&Date)
