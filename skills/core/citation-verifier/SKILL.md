---
name: citation-verifier
description: Use when checking manuscript citations, bibliography hygiene, DOI or PMID completeness, placeholder references, or BibTeX consistency before submission or revision.
---

# Citation Verifier

## Overview

Use this skill when citation integrity is the bottleneck. It is narrower and more operational than general writing skills: the goal is to catch unverifiable references, missing identifiers, duplicated BibTeX keys, placeholder citations, and mismatches between local citation artifacts before they become submission problems.

Use this skill together with `scientific-writing` or `submission-audit`, not instead of them.

## When To Use

Use this skill when:
- a manuscript is close to submission or resubmission
- the bibliography may contain placeholders, guessed entries, or stale metadata
- a `.bib` file needs a hygiene pass
- the draft mixes DOI, arXiv, PMID, or plain-text references inconsistently
- you need to verify that local citation artifacts are ready before manual or online source verification

Do not use this skill for:
- generic literature discovery from scratch
- full manuscript restructuring
- venue formatting that does not depend on citation integrity

## Local First Pass

Start with a local citation scan before any online verification.

The helper script:

```bash
python ~/.codex/skills/citation-verifier/scripts/scan_citations.py path/to/file_or_dir [...]
# Claude Code (global install): replace ~/.codex/skills with ~/.claude/skills
# Claude Code (project-local install): replace ~/.codex/skills with .claude/skills
```

Use it to find:
- `[CITATION NEEDED]` or similar placeholders
- `PLACEHOLDER_...` citation keys
- `TODO: verify` markers
- DOI, arXiv, and PMID tokens
- LaTeX `\cite{...}` keys
- duplicate BibTeX keys inside `.bib` files

Treat imported BibTeX and Google Scholar-style exports as draft metadata, not as verified truth.

## Verification Order

1. Scan the local draft and bibliography artifacts.
2. Remove or flag all placeholder citations.
3. Check BibTeX-key uniqueness and obvious identifier gaps.
4. Normalize metadata fields that are commonly wrong in copied BibTeX:
   - author list and spelling
   - year
   - venue or journal name
   - volume, issue, pages, or article number
   - DOI versus preprint identifier
5. For every citation that matters to a scientific claim, verify the paper exists in trusted sources.
6. If a claim depends on a specific result, confirm the cited paper actually supports that claim.
7. Only then finalize formatting for the venue.

## Severity Grading

When you report field-level mismatches, grade each one so authors fix the dangerous ones first:

- **Critical (must fix)**: wrong or fabricated first author, reversed author order, a DOI that resolves to a different paper, a title whose core terms do not match, or a page range off by five or more.
- **Warning (verify)**: volume-year inconsistent with the DOI-registration year, a missing or extra issue number, a missing middle initial, a page range off by one to four, or an ambiguous publisher-name variant.
- **Info (note only)**: title case versus sentence case, abbreviated versus full journal name, and punctuation or conjunction differences (`and` versus `&`).

Two checks are easy to miss and worth running explicitly:
- **Volume-year versus DOI-year**: a citation whose stated volume-year differs from the year encoded in the DOI or the online-publication date is a common sign of a miscopied entry.
- **Author-order reversal**: verify the first author specifically, not just that all names are present; a reversed or shifted author list still passes a set-membership check.

Roll each reference up to one confidence verdict: `verified`, `check_suggested` (has a Warning), `needs_fix` (has a Critical), or `unverifiable` (no source could confirm it).

## Trusted Verification Sources

Prefer this order when moving beyond local scans:
- publisher page or DOI resolver
- PubMed for biomedical papers
- arXiv for preprints
- Crossref or Semantic Scholar for metadata cross-checking
- Google Scholar only as a fallback discovery aid, not as the sole source of truth

## Common Failure Modes

- writing BibTeX from memory
- leaving placeholder citation keys in the draft
- assuming an arXiv preprint and published version are interchangeable
- citing a paper correctly but using it to support a claim it does not make
- letting duplicate BibTeX keys silently overwrite entries
- blindly trusting copied Scholar or BibTeX metadata for venue names, pages, years, or DOI fields

## Output Standard

When using this skill, report:
- placeholder or unverifiable items
- duplicate or suspicious BibTeX keys
- missing or inconsistent DOI/arXiv/PMID information
- suspicious metadata fields that need manual correction
- claims that still need source verification
- the minimum safe next step before submission
