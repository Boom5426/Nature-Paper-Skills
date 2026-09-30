# Upstream provenance

| Field | Value |
|---|---|
| Source | https://github.com/Kiterlin/anti-defensive-writing |
| Path in repo | `skill/anti-defensive-writing/SKILL.md` |
| Ref | `main` |
| Fetched | 2026-08-22 |
| Upstream SKILL.md size at fetch | 6,458 bytes |
| License | MIT (Copyright (c) 2026 Kiterlin), see `LICENSE` |

## What was changed locally

On install (2026-08-22): the frontmatter was restated for this repository's dispatcher with bilingual
triggers and `license: MIT`, and `## Local integration` (chain position, boundary against the
integrity audits and against `scientific-prose-style`, a worked Methods example, a reporting
requirement) and `## Provenance` were appended. The upstream body was kept verbatim.

On 2026-09-30 the body was rewritten from this repository's manuscript-revision history, and it no
longer carries upstream text verbatim. What remains from upstream is the core rule (advance the claim
directly, keep necessary limitations, prefer positive scope) and the three examples reproduced
unmodified at the end of `references/worked-examples.md`. Local additions: rule zero (do not add
defensive text while editing), the four voices (audit, defensive, self-critical, commentary), What
stays, the placement table, the six-way classification, the edit, proposal and light-touch modes, the
detection pass, and `references/worked-examples.md`.

Later on 2026-09-30, from a further manuscript revision: the developer voice (repository paths, file
names, workbook and build notes, pipeline internals) and the commitment voice (promised releases and
arranged access) were added, verdict columns in tables joined the self-critical voice, the detection
pass now scans `\texttt{...}` and gained developer and commitment lines, the procedure now edits
generated text at its generator and checks prose panel references, and reporting lists gaps that need
the author.

## Files not carried over

`skill.json`, `agents/openai.yaml`, `install.sh`, `README.md`, `README.zh-CN.md`, `assets/cover.png`.
These describe Codex packaging and installation and have no function under the local skills layout.

## Refresh

    curl -sL https://raw.githubusercontent.com/Kiterlin/anti-defensive-writing/main/skill/anti-defensive-writing/SKILL.md

The local body is no longer a patch on upstream. To adopt an upstream change, read the upstream diff
and merge any new idea into the local structure by hand.
