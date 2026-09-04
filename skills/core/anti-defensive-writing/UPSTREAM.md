# Upstream provenance

| Field | Value |
|---|---|
| Source | https://github.com/Kiterlin/anti-defensive-writing |
| Path in repo | `skill/anti-defensive-writing/SKILL.md` |
| Ref | `main` |
| Fetched | 2026-08-22 |
| Upstream SKILL.md size at fetch | 6,458 bytes |
| License | MIT (Copyright (c) 2026 Kiterlin), see `LICENSE` |

## What was changed on install

1. **Frontmatter replaced.** Upstream ships a Codex-style `name` + `description`. The local
   frontmatter keeps the same skill name, restates the description in the form the local dispatcher
   matches on, adds bilingual trigger phrases, and declares `license: MIT`.
2. **One pointer sentence added** under the H1, directing the reader to the Local integration
   section before applying the rules.
3. **`## Local integration` appended**: chain position inside `paper-workflow`, the boundary against
   the integrity audits (`stats-reporting-audit`, `claim-source-verification`, `citation-verifier`,
   `data-availability`, `submission-audit`), the boundary against `scientific-prose-style`, a
   worked Methods example, and a reporting requirement.
4. **`## Provenance` appended.**

Everything between `## Core Rule` and `## Final Pass` is upstream text, unmodified.

## Files not carried over

`skill.json`, `agents/openai.yaml`, `install.sh`, `README.md`, `README.zh-CN.md`, `assets/cover.png`.
These describe Codex packaging and installation and have no function under the local skills layout.

## Refresh

    curl -sL https://raw.githubusercontent.com/Kiterlin/anti-defensive-writing/main/skill/anti-defensive-writing/SKILL.md

Diff the body against the section range above before re-adopting; keep the local frontmatter and the
two appended sections.
