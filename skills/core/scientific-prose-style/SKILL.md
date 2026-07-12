---
name: scientific-prose-style
description: "Prose-quality rules for writing scientific manuscript text — abstract, introduction, results, discussion. The headline rule is a strict em-dash budget: the long dash (—) is overused and reads as a stylistic tic, so cap it and rewrite with commas, colons, parentheses, or a period. Also covers hedging, sentence rhythm, and paragraph openers. Load whenever drafting or revising manuscript prose (not figures; that is figure-planner)."
license: Apache-2.0
---

# scientific-prose-style

Rules for the *prose* of a scientific paper — the sentences of the abstract,
introduction, results, and discussion. Load this whenever you draft or revise
manuscript text. (Figure planning lives in `figure-planner`; this skill
is about words on the page.)

## Rule 1 — Em-dash budget (the headline rule)

The long em-dash (`—`) is the single most overused mark in generated scientific
prose. It feels punchy in isolation but a reader hits three or four per paragraph
and it reads as a stylistic tic, not as writing. **Cap it.**

- **At most one em-dash per paragraph, and none in the abstract.** If a sentence
  already has one, the next clause that wants a dash gets a different mark.
- **Never use a *pair* of em-dashes to bracket an aside** if a comma pair or
  parentheses would do — the double dash is the worst offender.
- Prefer, in rough order: **comma** (mild pause), **colon** (a list or an
  expansion of what precedes), **parentheses** (a true aside the sentence reads
  fine without), or **split into two sentences** (the strongest fix for a long
  dash-spliced line).

### Substitution table

| Em-dash use | Replace with | Example fix |
|---|---|---|
| Pause before a summary/payoff | colon | `...never been tested — this is our entry point.` → `...never been tested. This is our entry point.` |
| Bracketed aside (pair of dashes) | commas or parentheses | `no model — including ESM — beats chance` → `no model, including ESM, beats chance` |
| Appositive / renaming | comma | `allele-resolution prediction — telling apart variants` → `allele-resolution prediction, i.e. telling variants apart,` |
| Abrupt contrast | period + connective, or "but" | `real but sub-threshold — the effect vanishes` → `real but sub-threshold: the effect vanishes` |
| Range or span (this is fine) | keep an **en-dash** `–`, not em | `370–1000 cells` stays `370–1000` |

### Before → after (from a real over-dashed abstract)

**Before (5 em-dashes, tic-heavy):**
> Starting from the hardest instance of the problem — allele-resolution
> prediction, distinguishing many coding variants of the same gene — we assemble
> a benchmark, and find this is a measurement limit, not a model limit — a
> split-half floor shows the distance is no larger than sampling noise.

**After (0 em-dashes, same content):**
> We start from the hardest instance of the problem: allele-resolution
> prediction, which distinguishes many coding variants of the same gene. On the
> benchmark we assemble, the ceiling turns out to be a measurement limit rather
> than a model limit. A split-half floor analysis shows the perturbation-versus-
> control distance is no larger than the sampling noise between two halves of a
> variant's own cells.

Note what the rewrite does: promotes one clause to its own sentence, turns the
bracketed aside into a relative clause, and swaps the contrast dash for "rather
than." The prose is calmer and each sentence carries one idea.

## Rule 2 — Don't trade the dash for a colon tic

Colons are the natural replacement, but the same overuse applies: at most one
colon per sentence, and if every sentence in a paragraph ends `...: <expansion>`
you've just moved the tic. Vary the repair — some become periods, some commas.

## Rule 3 — Hedge once, not thrice

Scientific prose stacks hedges (`may possibly suggest that ... could in principle
...`). State the claim with one qualifier and the confidence level, then stop.
`These results suggest X` — not `These results may tentatively be taken to
suggest that X could hold`.

## Rule 4 — Vary sentence length; one idea per sentence

A paragraph of uniformly long, clause-heavy sentences is as fatiguing as the
dash tic. Follow a long sentence with a short one. If a sentence has three
clauses joined by dashes, semicolons, and "and," it is three sentences.

## Rule 5 — Openers and connectives

- Don't open consecutive paragraphs with the same word (`We ... We ... We ...`).
- Prefer plain connectives (`but`, `so`, `because`, `here`) over heavy ones
  (`moreover`, `furthermore`, `additionally`) unless enumerating.

## Self-check before you hand prose back

Run this on any abstract/intro/section you write:

1. **Count em-dashes.** More than one per paragraph, or any in the abstract →
   rewrite the excess with the substitution table.
2. **Count paragraph-opening words.** Repeated opener → vary it.
3. **Read the longest sentence aloud.** If you run out of breath, split it.
4. En-dashes in numeric ranges (`5–10`) and hyphens in compounds
   (`single-cell`) are fine and are not counted against the budget.

---

*Provenance: adapted from the Claude Science `scientific-prose-style` skill (Apache-2.0). Cross-references to figure skills were repointed to this repo's `figure-planner`.*
