<div align="center">

# 🧬 Nature-Paper-Skills

**From first draft to submission and rebuttal, build a clear, evidence-grounded manuscript.**

🧠 **Structure** · 📊 **Figures** · ✍️ **Writing** · 📚 **Citations** · 📨 **Rebuttals**

[![Skills](https://img.shields.io/badge/skills-27-8a63d2)](docs/skill-map.md)
[![CI](https://github.com/Boom5426/Nature-Paper-Skills/actions/workflows/ci.yml/badge.svg)](https://github.com/Boom5426/Nature-Paper-Skills/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT%20%2B%20Apache--2.0-green)](#license)
[![Stars](https://img.shields.io/github/stars/Boom5426/Nature-Paper-Skills?style=social)](https://github.com/Boom5426/Nature-Paper-Skills/stargazers)

🌐 **English** · [简体中文](README.zh-CN.md)

[🗺️ Workflow](#workflow-at-a-glance) · [🚀 Quick start](#quick-start) · [🧩 Choose a task](#choose-a-task) · [📚 All skills](docs/skill-map.md)

</div>

---

<a name="what-makes-the-workflow-useful"></a>

27 skills for Codex and Claude Code, connecting structure, scientific writing, figures, citations and reviewer responses.
Built for Nature-series life-science, computational-biology and methods papers.

## ✨ What makes the workflow useful

- 🎯 **Build the argument before polishing sentences.** Connect the scientific question, contribution and evidence chain before refining the prose.
- 📊 **Give every figure a job.** Define its main claim, organize panels and keep legends aligned with Results. The optional figure stack checks text size, collisions, alignment and source data.
- ✍️ **Write for the journal reader.** Turn project-log language and defensive scaffolding into direct scientific prose while preserving measured values, necessary conditions and negative results.
- 📚 **Check what a citation actually supports.** Treat bibliography consistency, reference existence and claim-to-source support as separate checks.
- 📨 **Connect reviewer replies to manuscript changes.** Preserve the referee's numbering, answer each ask and tie the reply to completed evidence and the revised text.
- 📐 **Hold each section to its own job.** The Abstract, Introduction, Results, Discussion and Methods each have one contract: what the section must do, what it depends on and its typical shape, drawn from 28 Nature Methods, Nature Biotechnology and Nature Communications method papers. A changed Results claim is rechecked wherever the Abstract, Introduction or Discussion restates it.
- 🧩 **Use the workflow at the scale you need.** Revise a whole paper, repair a Results section or work on one paragraph. The dispatcher selects the relevant layers and preserves settled material.

<a name="workflow-at-a-glance"></a>

## 🗺️ Workflow at a glance

**One connected workflow, from the research question to the reviewer response.**

```mermaid
flowchart LR
    A("🎯 Frame the paper<br/>Question · venue")
    B("🧠 Build the argument<br/>Claims · evidence")
    C("📊 Figures & Results<br/>Panels · legends")
    D("✍️ Revise the prose<br/>Logic · style")
    E("📨 Submit & respond<br/>Preflight · rebuttal")
    I(["🔎 Check throughout<br/>Statistics · citations · data"])
    A --> B --> C --> D --> E
    I -.-> B
    I -.-> C
    I -.-> E
    classDef frame fill:#eef2ff,stroke:#818cf8,color:#312e81;
    classDef argument fill:#f5f0ff,stroke:#a78bfa,color:#4c1d95;
    classDef figures fill:#ecfdf5,stroke:#34d399,color:#064e3b;
    classDef prose fill:#fff7ed,stroke:#fb923c,color:#7c2d12;
    classDef response fill:#eff6ff,stroke:#60a5fa,color:#1e3a8a;
    classDef integrity fill:#f8fafc,stroke:#94a3b8,color:#334155,stroke-dasharray:4 3;
    class A frame;
    class B argument;
    class C figures;
    class D prose;
    class E response;
    class I integrity;
```

Structure and evidence come before sentence polish. Statistics, citation support and data availability are checked at the relevant stages. Enter at the stage your task needs; a paragraph edit does not require the entire chain. Reviews, surveys and Perspectives have their own architecture route.

The diagram includes figure production, available with `--figure`; the default installation already covers figure planning, manuscript revision and reviewer responses.

[🗺️ Full workflow](docs/workflow-map.md) · [📐 Section contracts](skills/core/paper-workflow/references/section-contracts.md) · [📚 All skills](docs/skill-map.md) · [✍️ Writing principles](docs/design-principles.md) · [📊 Figure workflow](docs/figure-workflow.md)

<a name="see-what-changes"></a>

## 🪄 See what changes

The workflow connects manuscript revision, figure work and reviewer responses. These examples zoom in on the writing layer: direct scientific prose with the facts that make a result interpretable.

| 📝 Before | ✨ After | 🔒 What stays |
|---|---|---|
| “We carefully verified that survival changed by 1 percentage point (95% CI −3 to 5), which should not be overinterpreted.” | “Survival changed by 1 percentage point (95% CI −3 to 5), with no clear evidence of improvement.” | The measured effect, interval and uncertainty |
| “These orderings should not be read as a universal ranking across all settings.” | “These orderings hold for the tested settings.” | The scope of the comparison |
| “The analysis reads the final output from `results/final_scores.csv`.” | “The analysis uses the measured response scores.” | The scientific object; file access details belong in the appropriate methods/data documentation |

These are illustrative edits, not claims about a real study. A scientific limitation or reproducibility detail must remain wherever it is needed. See [worked examples](skills/core/anti-defensive-writing/references/worked-examples.md) and the [complete first-run example](examples/first-run/README.md).

<a name="quick-start"></a>

## 🚀 Quick start

<a name="1-install"></a>

### 📥 1. Install

Choose all 27 skills for the full research workflow, or 19 for manuscript writing and review. The complete set adds figure production, literature research, results analysis, reference auditing, conference writing and presentations. Local installation needs Bash and Python 3.9+; remote installation also needs curl and tar.

**Let the agent handle installation:** use the code block's top-right copy button, then paste the instruction into your agent chat:

**Full research workflow: all 27 skills**

```text
Read and follow https://github.com/Boom5426/Nature-Paper-Skills/blob/main/INSTALL.md to install all 27 Nature Paper Skills for this environment, using the all profile, and verify the result.
If the page cannot be read, use an available GitHub tool or git clone to retrieve the main branch and read INSTALL.md from the repository root; do not substitute search snippets for the file.
```

**Manuscript writing and review: recommended 19-skill stack**

```text
Read and follow https://github.com/Boom5426/Nature-Paper-Skills/blob/main/INSTALL.md to install the recommended 19 Nature Paper Skills for this environment, and verify the result.
If the page cannot be read, use an available GitHub tool or git clone to retrieve the main branch and read INSTALL.md from the repository root; do not substitute search snippets for the file.
```

No explicit creator selection is required. [INSTALL.md](INSTALL.md) chooses the supported route and asks the agent to handle retrieval and verification. Persistent ChatGPT Work web installation remains unverified; account registration must be available before the agent reports success.

| Your app | Start here |
|---|---|
| Codex: app, CLI or IDE | [Install for Codex](#install-codex-bash); Windows instructions are in the detailed guide |
| Claude Code | [Install for Claude Code](#install-claude-code) |
| ChatGPT Work on the web | [Web installation and availability](#install-chatgpt-work-web); automatic installation is unverified |

<a name="install-codex-bash"></a>

<details>
<summary><b>Codex</b></summary>

On Linux/macOS, run:

```bash
curl -fsSL https://raw.githubusercontent.com/Boom5426/Nature-Paper-Skills/main/install.sh | bash -s -- --agent codex --set all
```

This command installs all 27. Use `--set recommended` for the 19-skill stack.

On Windows, follow the [Windows instructions](docs/installation-codex.md#windows-desktop-app), choosing the native agent or WSL2 route used by your app.

The default destination is `~/.agents/skills`. Refresh the skill list or start a new chat, then select `paper-workflow`; in CLI/IDE, explicitly invoke `$paper-workflow`. See [Codex setup](docs/installation-codex.md) for requirements and verification status.

If using the built-in `skill-installer`, specify a directory containing `SKILL.md`, such as [`skills/core/paper-workflow`](https://github.com/Boom5426/Nature-Paper-Skills/tree/main/skills/core/paper-workflow). The repository root is a collection, not a single skill; see the [skill map](docs/skill-map.md) for the directories in a complete workflow.

</details>

<a name="install-claude-code"></a>

<details>
<summary><b>Claude Code</b></summary>

Run in the same machine and user environment as Claude Code:

```bash
curl -fsSL https://raw.githubusercontent.com/Boom5426/Nature-Paper-Skills/main/install.sh | bash -s -- --agent claude --set all
```

This command installs all 27. Use `--set recommended` for the 19-skill stack.

The default destination is `~/.claude/skills`. Refresh/reopen Claude Code and invoke `/paper-workflow`. See [Claude Code setup](docs/installation-claude.md) for requirements and verification status.

</details>

<a name="install-chatgpt-work-web"></a>

<details>
<summary><b>ChatGPT Work on the web</b></summary>

Use **either copyable instruction above**. The agent handles retrieval and any supported installation flow; you do not need to select `@skill-creator`, run Python or upload a ZIP.

**Automatic web installation is unverified.** It requires this account to expose a supported save/register flow. A download or a skill directory inside a web task does not confirm availability in a new chat. The agent should report the missing capability if registration is unavailable.

For reliable distribution, the maintainer publishes a plugin or a workspace administrator imports its GitHub marketplace. See [web distribution and verification](docs/installation-chatgpt-work.md); packaging commands are maintainer instructions.

</details>

Existing copies are backed up by the repository installer. Add `--figure` for the figure stack or `--set all` for all 27 skills; scope, preview, update and restore commands are in [Installation options](#installation-options).

<a name="2-complete-your-first-revision"></a>

### ✍️ 2. Complete your first revision

Once the local skill is visible, put your current manuscript and its supporting results in the agent's working folder, then ask:

```text
Use paper-workflow. Revise the Results paragraph in draft.md using evidence.md.
Preserve measured values and figure references. Save a revised copy and briefly
explain the material changes.
```

For ready-made inputs and a reference output, use [First successful revision](examples/first-run/README.md). In Codex CLI/IDE you can explicitly mention `$paper-workflow`; in Claude Code invoke `/paper-workflow`.

You can then use ordinary requests such as “improve this manuscript” or name a specialist. The dispatcher diagnoses the task, states the scope and applies the steps needed. You do not need to memorize skill names.

<a name="choose-a-task"></a>

## 🧩 Choose a task

| Your task | Provide | Expected result | Entry |
|---|---|---|---|
| 🧬 Improve a whole manuscript | Current draft, relevant results/figures, target venue if decided | Revised draft, key changes, unresolved evidence gaps | `paper-workflow` |
| 📐 Write or revise one section | The section, current Results and figures, target journal | Revised section held to its contract; claims resting on unsettled results named | `paper-workflow` |
| ✍️ Fix a paragraph | Passage, surrounding context, requested scope | Replacement passage with a brief explanation where useful | `write-scientific-manuscript` |
| 🪄 Remove audit/defensive writing | Main text, SI, legend or availability statement | Direct scientific prose retaining numbers and necessary conditions | `anti-defensive-writing` |
| 📊 Plan or make figures | Scientific question, result table or existing figure | Panel plan; rendered files when data and tools are available | `figure-planner`; add `--figure` for production |
| 🔎 Check before submission | Final draft, SI, bibliography and venue | Prioritized findings with locations; unchecked categories identified | `submission-audit` |
| 📨 Reply to reviewers | Original comments, manuscript, completed new evidence | Numbered response draft and matching manuscript changes | `paper-workflow` |

A request to **review or suggest** produces findings. A request to **revise** produces edits within the requested scope. Missing evidence is surfaced; it is never written into existence.

For complete prompts and task setups, see [task examples](docs/task-recipes.md). The optional `--set all` selection includes a [recomputable statistics walkthrough](skills/research/results-analysis/USAGE.md); its example helper needs SciPy.

<a name="installation-options"></a>

## 📦 Installation options

<details>
<summary><b>⚙️ Choose an agent, installation scope or skill set</b></summary>

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

</details>

<details>
<summary><b>🛠️ Environment requirements and skill loading</b></summary>

**Local installer requirements:** Codex or Claude Code, Bash, and Python 3.9+ (standard library only; no extra pip packages for installation). Remote installation also uses `curl` and `tar`. For Windows, see [Codex Windows setup](docs/installation-codex.md#windows-desktop-app). [ChatGPT Work on the web](#install-chatgpt-work-web) uses a separate distribution flow. See [environments and file formats](docs/compatibility.md) for verification status.

If a skill is not visible, refresh the skill list or reopen the session, then check [troubleshooting](docs/installation-management.md#troubleshooting). Agent-specific instructions: [Codex](docs/installation-codex.md) · [Claude Code](docs/installation-claude.md).

</details>

<details>
<summary><b>🔄 Inspect the installer, update, restore or pin a version</b></summary>

Read [install.sh](install.sh) before running it if you prefer, or use the clone-based commands above. Existing copies are backed up before replacement; see [update and restore](docs/installation-management.md).

To share one installed copy across agents, follow the [manual linked layout](docs/installation-management.md#manual-layout-one-canonical-copy-linked-into-the-agent-directory). Run updates, checks and restores against the canonical directory; existing agent entries are preserved.

Pin an immutable commit with `--ref <full-commit-sha>`; the installer records the source and file hashes. Version history: [CHANGELOG](CHANGELOG.md).

</details>

<a name="scope-and-limits"></a>

## 🧭 Scope and limits

This is a focused journal-writing workflow for life sciences, computational biology, methods, benchmarks and resources. Explicit venue and project instructions take precedence over its Nature-style defaults. It is independent of Nature Portfolio and does not predict acceptance.

The typical section shapes come from 28 open-access computational-method papers in three Nature Portfolio journals ([evidence and limits](skills/core/paper-workflow/references/section-evidence.md)). They are checks on a draft, not format rules; the target journal's current guide sets the format.

Skills provide instructions and some helper scripts. They do not themselves supply a Word editor, PDF renderer, LaTeX installation, browsing access or experimental evidence. [Compatibility](docs/compatibility.md) separates readable inputs from editable/exportable outputs.

Repository tests cover scripts, installation and consistency. [Behavior cases](evals/README.md) check task scope, evidence preservation and honest reporting of missing capabilities; their limitations and recorded runs are documented separately.

<a name="contributing"></a>

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Changes to user-facing behavior should include a task case or an example, and both READMEs should stay aligned. Component provenance is in [ATTRIBUTION.md](ATTRIBUTION.md).

<a name="acknowledgements"></a>

## 💙 Acknowledgements

Parts of this repository were inspired by [OpenLAIR/dr-claw](https://github.com/OpenLAIR/dr-claw), [Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills), and the Claude Science skill pack.

The figure layer also draws on design observations from [ChenLiu-1996/figures4papers](https://github.com/ChenLiu-1996/figures4papers). None of that repository's code or prose is distributed here; see [THIRD_PARTY_NOTICES](skills/figure/nature-figure/THIRD_PARTY_NOTICES.md).

<a name="license"></a>

## ⚖️ License

Original content is [MIT](LICENSE). Components carrying Apache-2.0 material retain [LICENSE-APACHE](LICENSE-APACHE) and [NOTICE](NOTICE), including in installer-managed copies. See [ATTRIBUTION](ATTRIBUTION.md) for coverage.

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Boom5426/Nature-Paper-Skills&type=Date)](https://star-history.com/#Boom5426/Nature-Paper-Skills&Date)
