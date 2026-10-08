# Agent-assisted installation

This document is for the agent receiving an installation request. Handle source
retrieval, installation and verification yourself. The user should not need to
run commands, build a ZIP, upload files or explicitly mention a creator skill.

Follow the profile explicitly requested by the user. The README offers all 27
first for the full research workflow and 19 for manuscript writing and review.
Preserve complete skill directories, resources and licenses.

| User request | Profile flags for installer and builder | Selection |
|---|---|---|
| All skills, full workflow, or 27 skills | `--set all` | Every `skills/*/*/SKILL.md` directory (27) |
| Recommended, writing/review, or 19 skills | `--set recommended` | `RECOMMENDED_SKILLS` in `install.sh` (19) |
| Recommended plus figures, or 21 skills | `--set recommended --figure` | `RECOMMENDED_SKILLS` plus `FIGURE_SKILLS` (21) |
| No profile specified | `--set recommended` | Existing installer default (19) |

Pass the selected flags to installation, doctor and packaging. A request for 27
must use `--set all`; do not silently substitute the 19-skill default. Installing
skill files does not install the optional runtimes or dependencies used by their
scripts; check those when the corresponding task is requested.

## 1. Identify the installation environment

Distinguish a local Codex/Claude Code client from ChatGPT Work on the web. A shell
inside a web task is not evidence of a persistent local client installation.
Determine the actual client, operating system, skill discovery location and
available tools before writing files.

Retrieve the original files from the `main` branch of
[the GitHub repository](https://github.com/Boom5426/Nature-Paper-Skills), or use
an exact source ref or checkout explicitly supplied by the user. The installation
entry is [this GitHub file page](https://github.com/Boom5426/Nature-Paper-Skills/blob/main/INSTALL.md);
access to `raw.githubusercontent.com` is optional.

If webpage reading fails, use an available GitHub tool to retrieve complete file
contents or clone the repository over GitHub HTTPS into a new, explicit directory:

```bash
git clone --depth 1 --single-branch --branch main https://github.com/Boom5426/Nature-Paper-Skills.git "<new-checkout-directory>"
```

Choose an unused destination. Read the retrieved `INSTALL.md` and `install.sh`,
then the relevant guide below; obtain the complete selected skill directories
before installation. Record the actual source commit when it can be resolved.
Do not use search snippets, a cached README or memory as a substitute for the
original installation files. If every supported retrieval path is blocked,
report the inaccessible source and stop; do not attempt to bypass network policy.
Do not commit, push, publish, delete existing skills or change the user's agent
environment as part of installation.

## 2. Local Codex or Claude Code

Use the repository's installer; it retains licensing, installation records and
recovery information. For a full 27-skill request, run from the retrieved checkout:

```bash
bash install.sh --agent codex --set all --on-conflict keep
bash install.sh --agent codex --set all --doctor
```

For 19 skills, replace `--set all` with `--set recommended` in both commands;
for 21, also add `--figure`. For Claude Code, substitute `--agent claude`. A requested project installation
uses `--local`, run from the intended project with an explicit path to the script.
An explicit destination uses `--dest` for both installation and doctor.

Preserve existing local modifications and linked skills. Report any preserved
entries that prevent the selected profile from being fully installed.

For Windows, determine whether the client uses a native Windows agent or WSL.
Follow [Codex Windows setup](docs/installation-codex.md#windows-desktop-app);
the integrated terminal alone does not identify the agent's environment.

If native Windows has Python 3.9+ but no Bash, the same standard-library manager
is available as `scripts/manage_install.py`. Read its CLI before invoking it:

- Use `--source` with the retrieved checkout and `--dest` with the Windows
  client's actual skill directory.
- Derive repeated `--skill` arguments from the selected profile: enumerate all
  `skills/*/*/SKILL.md` directories for 27, use `RECOMMENDED_SKILLS` for 19,
  or add `FIGURE_SKILLS` for 21. Pass each skill's category/name relative path.
- Derive repeated `--apache` arguments from `APACHE_SKILLS` in `install.sh`;
  do not omit these license-shipping arguments.
- Pass `--repo`, `--source-ref`, and the known source `--commit` for provenance,
  plus `--on-conflict keep`. Do not claim an unknown commit is known.
- Run the same manager with `--source`, `--dest` and `--doctor` afterward.

This Python entry point has been exercised on Linux. Native Windows client
discovery remains unverified. Do not install a runtime or switch to WSL silently
if the current environment lacks the necessary tools.

Report the installed location and count, preserved entries, doctor result, and
how to select `paper-workflow` in a new session. A file integrity check does not
verify live client discovery; report that check separately.

## 3. ChatGPT Work on the web

First inspect the actual capabilities available in this account. Proceed only
through a supported workspace skill/plugin installation or creation flow that
can save and register reusable content. A local directory in a task sandbox does
not register a skill in the ChatGPT account.

No particular creator is mandatory. If a suitable creator is available and can
be used by the agent, it may be used internally. Do not ask the user to select
`@skill-creator`, run Python or upload a ZIP as a prerequisite.

If the account provides a supported registration flow:

1. Prefer an actual published Nature Paper Skills plugin listing or an already
   imported workspace listing when available. Do not invent a listing URL or ID.
2. If the supported flow can create from repository resources, retrieve the
   complete source. Use `scripts/build_chatgpt_plugin.py` yourself, with a new,
   explicit output directory and the selected profile flags, when execution is
   available. Use `--set all` for a 27-skill request. Its output includes one
   `nature-paper-workflow` entry retaining every selected specialist under
   `resources/`, as well as a skills-only plugin and marketplace tree.
3. Preserve the entry's `SKILL.md`, every specialist resource, scripts,
   references, templates, assets and licenses. Follow the actual tool's schema;
   a generated source ZIP is not a documented automatic workspace importer.
4. Complete supported saving/registration. Report the returned skill/plugin ID
   or listing, its visibility, and how to select it in a new chat. State whether
   new-chat invocation was actually tested.

If no supported persistent registration flow is exposed, stop and report the
missing capability. Do not report installation success after downloading,
building, attaching files or writing to `~/.agents/skills` in a sandbox. Do not
substitute a manual ZIP workflow for the user's automatic installation request.

The documented web distribution routes are a published plugin or an
administrator-imported GitHub marketplace. These require maintainer/workspace
setup; this instruction does not publish or import on the user's behalf. See
[web distribution and verification](docs/installation-chatgpt-work.md).

## Verification boundary

Local installer and bundle checks can verify files. ChatGPT Work account
registration and reuse require a live account check and are currently
unverified for this repository.

[Official skill support](https://learn.chatgpt.com/docs/build-skills) ·
[Workspace skill controls](https://learn.chatgpt.com/docs/enterprise/skills) ·
[GitHub marketplace import](https://learn.chatgpt.com/docs/enterprise/plugin-management)
