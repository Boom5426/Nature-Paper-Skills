# Environments and input/output support

## Installation environments

| Environment | Route | Verification status |
|---|---|---|
| Linux with Bash and Python 3.9+ | `bash install.sh` | Local integration suite executed; Ubuntu CI checks the suite |
| macOS with Bash and Python 3.9+ | Same script, portable standard-library file handling | macOS added to CI; inspect the current run before treating it as passed |
| Windows desktop app, native agent | Default agent uses PowerShell; the supplied installer requires Bash. See [Windows setup](installation-codex.md#windows-desktop-app) | Skill directories pass static validation; no native app install/discovery test recorded |
| Windows with WSL2 | Run the installer and agent inside the same WSL distribution; changing the terminal alone does not switch the agent | No Windows/WSL runtime test recorded in this release |
| Windows with Git Bash | Bash + Windows Python; ensure Python and the app resolve the same Windows user/target path | No native Windows runtime test recorded |
| Windows PowerShell / CMD alone | Bash script cannot execute directly | Native installer is not supplied |
| ChatGPT Work on the web | [Agent instruction](../INSTALL.md) checks available registration; published plugins or administrator-imported marketplaces provide distribution | Package structure and retained resources are tested locally; automatic registration, live import and new-chat invocation remain unverified. See [web distribution](installation-chatgpt-work.md) |
| Hosted/cloud agent | Depends on its writable skill locations and persistence rules | Copying files to a local CLI directory does not install them in a hosted session |

The installation manager uses only the Python standard library. Core prose tasks do not require a plotting library or an image-generation API key. A file installation check and a live agent invocation are separate checks. Codex and Claude Code may change discovery behavior; agent-specific guides link the official documentation.

## Manuscript materials

| Input | Reading and diagnosis | Editing/output boundary |
|---|---|---|
| Pasted text / Markdown / plain text | Directly usable | Revised text or a new text file; preserve requested scope |
| LaTeX + bibliography | Read source, preserve commands, labels and citation keys | Edit source; compilation requires a separate TeX toolchain and must actually run before claiming success |
| DOCX | Requires an available DOCX reader/editor | Formatting preservation and tracked changes require appropriate document tools; these skills alone do not provide them |
| PDF | Requires text extraction and, for visual checks, rendering | Diagnose the extracted content; request editable source for reliable manuscript revision. PDF layout is not editable merely because its text can be read |
| Figure image / PDF | Requires image viewing/rendering for visual diagnosis | Replot from source data/code when available; reading an image does not recover raw observations |
| CSV / numerical table | Inspect supplied values and labels | Plot with installed Python/R dependencies; summary data cannot supply individual distributions or missing covariance |
| References / DOI list | Local checks find formatting and consistency issues | Existence and claim support require accessible authoritative sources; unavailable sources remain unchecked |

Never claim a render, export, compilation, source lookup or tracked-change edit that was not performed. When a capability is absent, deliver the useful supported portion and identify the remaining input/tool requirement.
