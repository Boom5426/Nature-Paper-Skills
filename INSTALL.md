# Agent-assisted installation

This document is for the agent receiving an installation request. Handle source
retrieval, installation and verification yourself. The user should not need to
run commands, build a ZIP, upload files or explicitly mention a creator skill.

Default: the **recommended 19 skills** defined by `RECOMMENDED_SKILLS` in
`install.sh`. Include the two figure skills only when requested; use all 27 only
when requested. Preserve complete skill directories, resources and licenses.

## 1. Identify the installation environment

Distinguish a local Codex/Claude Code client from ChatGPT Work on the web. A shell
inside a web task is not evidence of a persistent local client installation.
Determine the actual client, operating system, skill discovery location and
available tools before writing files.

Retrieve this repository into a fresh working directory, or use the checkout
explicitly supplied by the user. Read `install.sh` and the relevant guide below.
Do not commit, push, publish, delete existing skills or change the user's agent
environment as part of installation.

## 2. Local Codex or Claude Code

Use the repository's installer; it retains licensing, installation records and
recovery information. Run from the retrieved checkout:

```bash
bash install.sh --agent codex --on-conflict keep
bash install.sh --agent codex --doctor
```

For Claude Code, substitute `--agent claude`. A requested project installation
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
- Derive repeated `--skill` arguments from the selected arrays in `install.sh`
  and repeated `--apache` arguments from `APACHE_SKILLS`; do not omit the latter.
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
   explicit output directory, when execution is available. Its default output
   includes one `nature-paper-workflow` entry retaining the 19 specialists under
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
