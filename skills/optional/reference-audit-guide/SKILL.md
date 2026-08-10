---
name: reference-audit-guide
description: >-
  Verify that cited references actually exist and that their metadata matches, using the runnable
  scripts this skill ships for CrossRef, Semantic Scholar, arXiv, and PubMed. Use when the
  bibliography must be checked against live sources rather than inspected locally: detecting
  fabricated or hallucinated citations, confirming that DOIs resolve, and matching title, authors,
  venue, and year against the record. Also covers the underlying verification principles and
  reference-audit best practices. For an offline hygiene pass over a .bib or .tex file, run
  citation-verifier first; for whether a real source supports the sentence citing it, run
  claim-source-verification.
---

# Citation Verification Reference Guide

Verification principles plus runnable citation checkers for academic writing.

## Position in the citation pipeline

This repository separates three citation questions that are routinely confused. Run them in order.

1. `citation-verifier`: is the bibliography a well-formed artifact? Duplicate keys, missing fields,
   DOI syntax, cited-but-undefined. Offline, immediate.
2. **This skill**: does the cited work exist, and does its metadata match what the manuscript says?
   Queries live scholarly APIs. This is the only stage that catches a fabricated citation carrying
   a well-formed DOI.
3. `claim-source-verification`: does the real, correctly-cited source actually support the sentence
   citing it?

None of the three substitutes for another. A clean local scan shows the bibliography is
well-formed, not that the papers are real. A verified DOI shows the paper is real, not that it
says what the sentence claims.

**Core Principle**: Proactively verify every citation during the writing process using trusted scholarly sources rather than memory.

## Core Problems

Citation issues in academic papers seriously impact research integrity:

1. **Fake citations** - Citing non-existent papers
2. **Incorrect information** - Mismatched authors, titles, years, etc.
3. **Inconsistent formatting** - Mixed citation formats
4. **Missing citations** - Referenced but uncited work

These issues can lead to:
- Paper rejection or retraction
- Damage to academic reputation
- Reviewers questioning research rigor

## Verification Principles

This skill provides verification principles based on trusted scholarly sources:

### 1. Proactive Verification

**Core idea**: Verify immediately when adding a citation, rather than checking after writing is complete.

- Search for the paper each time a citation is needed
- Confirm the paper exists in a trusted source
- Add to bibliography only after verification passes

### 2. Source Hierarchy

Prefer these sources:
- publisher page or DOI resolver
- PubMed for biomedical papers
- arXiv for preprints
- Crossref or Semantic Scholar for metadata cross-checking
- Google Scholar as a fallback discovery aid

### 3. Information Matching Verification

**Information that must match**:
- Title
- Authors
- Year
- Publication venue

### 4. Claim Verification

**Key principle**: When citing a specific claim, confirm the claim actually appears in the paper.

- Access the paper PDF
- Search for relevant keywords
- Confirm the accuracy of the claim
- Record the section or page where the claim appears

## Best Practices

1. **Never generate citations from memory**
2. **Do not guess when verification fails**
3. **Mark unverifiable references clearly**
4. **Differentiate preprints from published versions**
5. **Verify the claim, not just the metadata**
