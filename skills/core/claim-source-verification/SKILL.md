---
name: claim-source-verification
description: Use when a manuscript's claims need to be checked against the sources cited for them, when literature search results must be verified before they enter a draft, or when an agent or collaborator has proposed references that have not yet been adversarially reviewed. This is claim-to-evidence verification, not bibliography hygiene; for duplicate keys, DOI syntax, and metadata cleanup use citation-verifier instead.
---

# Claim-Source Verification

## Overview

A citation can be perfectly real, perfectly formatted, and still wrong, because
the paper it points to does not say what the sentence claims it says. That is
the failure this skill exists to catch, and it is the dominant one.

The calibration comes from a real Review manuscript. Seven research agents
proposed **139 sources** to resolve 44 open factual questions. An independent
skeptic then re-checked every one. It rejected **55**.

| Rejection class | Count |
| --- | --- |
| `does_not_support_claim` | 29 |
| `metadata_wrong` | 12 |
| `wrong_site_or_population` | 6 |
| `not_primary_but_required_to_be` | 5 |
| `paywalled_unverifiable` | 3 |

**None was fabricated.** Every rejected source was a real, findable paper with a
real DOI. An existence check would have passed all 139. A metadata check would
have caught 12. The largest class, more than half of all rejections, is invisible
to both: a genuine paper made to carry a conclusion it does not reach.

So the operating rule is: **a source's existence is not evidence that it supports
the claim, and a clean bibliography audit is not evidence of anything at all.**

## When To Use

Use this skill when:

- an agent, a collaborator, or a literature-search tool has proposed references
  and nothing has adversarially checked them yet
- a manuscript makes quantitative claims (limits, thresholds, error rates,
  standard clauses, benchmark numbers) that trace to cited sources
- open factual or sourcing markers are being closed out in batch
- a Review or survey is being sourced, where most claims are about other people's
  measurements rather than the author's own

Do not use this skill for:

- duplicate BibTeX keys, DOI syntax, missing fields, placeholder entries. That is
  `citation-verifier`, and it runs before this, not instead of it.
- discovering literature from scratch. That is `academic-researcher`, installed
  with `--set all`. This skill checks what such a pass produces.
- deciding whether a claim is interesting. That is `manuscript-optimizer`.

The three stack: `citation-verifier` for hygiene, this skill for claim support,
`reference-audit-guide` for the underlying principles.

## The Two-Role Protocol

Verification must be adversarial and it must be **separate**. A researcher who
proposes a source and then checks their own source will confirm it, because they
already believe it. Run two roles:

**Proposer.** Given one claim, find sources that support it. Return, per source:
the identifier, the metadata, and **the sentence from the source that carries the
claim, quoted verbatim**.

**Skeptic.** Given the claim and the proposed source, **try to refute the pairing**.
Run this in a fresh context that has never seen the proposer's reasoning.

Three rules make the skeptic work:

1. **The default verdict is reject.** Uncertainty resolves against the source, not
   in its favour. A skeptic that needs to be convinced to reject will confirm
   almost everything.
2. **No verbatim supporting sentence, no confirmation.** If the skeptic cannot
   quote the line that carries the claim, the pairing is rejected regardless of
   how plausible it looks. This single rule produced most of the 29
   `does_not_support_claim` rejections.
3. **Spend more on verification than on research.** The skeptic reads the actual
   source; the proposer often reads an abstract. Give the verify stage the higher
   reasoning budget, not the lower one.

If the claim can fail in more than one way, give the skeptics different lenses
rather than running three identical ones: does the source say this, is the
population right, is this the primary record. Diversity catches failure modes
that redundancy cannot.

`references/adversarial-protocol.md` carries the prompt shapes and the structured
output schema.

## Four Outcomes, Never Two

Confirmed-or-rejected is not enough, because it forces two different situations
into one bucket and loses the distinction that matters most.

- **CONFIRMED.** The source supports the claim, the metadata is right, and the
  supporting sentence has been quoted. The claim can go into the manuscript with
  this citation.
- **PARTIAL.** The finding holds, but at least one proposed source has to be
  replaced first. **Do not apply. Do not remove the marker.** A PARTIAL that gets
  written up as done is how an unsupported sentence enters a draft while the
  audit trail says it was verified.
- **REJECTED.** The claim is not supported by anything proposed. Either it is
  narrowed to what the surviving sources do support, or the sentence goes.
- **BLOCKED.** The answer exists but is behind a paywall, in proprietary vendor
  data, or requires a decision only the authors can make. This is a real state
  and it needs to be reported as one, not left to look like unfinished work.

In the run above, 44 markers were researched. Eight were discharged outright,
two were narrowed to what the surviving sources support, and **25 came back
PARTIAL**. That was the largest bucket by a wide margin. Plan for it: most of
the work after a verification pass is replacing individual sources, not
rewriting claims.

## Named Traps

Each of these is a real rejection from the run described above. They repeat
across projects, so check for them by name.

**Derived value laundered into a measurement.** A proposal reported an equivalent
input noise of 31 dB(A) as a datasheet value. The datasheet gives only a 63 dB(A)
signal-to-noise ratio; 31 is 94 minus 63, an arithmetic step the proposer did and
then presented as a reading. Ask of every number: is this printed in the source,
or computed from it? A computed number needs the computation shown.

**One key carrying several works.** A single BibTeX entry was made to carry three
different works: a 1984 monograph mixed with the volume and page numbers of a
1990 journal update. Each work is real. The reference is not. Check that every
field of an entry comes from the same artifact.

**The correction that is worse than the error.** A proposed author-list "fix"
silently dropped the third and fifth authors of a twenty-plus-author paper. The
existing incomplete entry was less wrong than its replacement. Verify corrections
with the same suspicion as originals; a correction arrives wearing the authority
of having been checked.

**Textbook tradition with no primary behind it.** A pair of frequency ranges had
been quoted for decades and appeared in every secondary source. No primary study
reports those bounds. When every citation traces to another citation, the claim
is folklore. Either find the measurement or report the range as convention and
say so.

**A replacement that cites what nobody opened.** One proposed replacement text
cited a specific figure from a paper whose full text is paywalled and was never
retrieved. The proposal was itself unverifiable. A source you could not open
cannot be a source you confirmed; classify it BLOCKED, not CONFIRMED.

**One team's choice attributed to the field.** A preprocessing decision made by a
single group was written as standard practice. Check the scope word: does the
source say "we", or does it say "commonly"?

**Wrong site, wrong population.** Six rejections were sources that measured the
right quantity on the wrong body site, the wrong cohort, or under a different
capture condition. Metadata is right, claim is right in general, pairing is
wrong. Always check what was measured on whom.

`references/rejection-taxonomy.md` gives the decision boundaries between classes.

## When Verification Reverses The Manuscript

This is the case that justifies the whole exercise, and it needs its own protocol
because it is not a sourcing outcome, it is a scientific one.

In the run above, one marker asked whether a standard gives a signal channel a
physical dimension. The draft, written before anyone had read the standard, said
the channel was an uncalibrated integer count on a fixed scale with the reference
quantity left to the manufacturer. Clause 7.7 of the standard says the opposite:
the unit is the newton, and recorded integers are restored by dividing by a
scaling value carried in the record. Both the researcher and the skeptic pulled
that sentence verbatim from the publisher preview.

The protocol when this happens:

1. **Do not silently apply it.** A conclusion changed without a record is
   indistinguishable from drift.
2. **Do not silently drop it either.** Queueing an inconvenient finding out of
   caution is the same failure with better manners.
3. **Write all four parts down**: what the draft said, what the source says, the
   clause quoted verbatim, and whether the surrounding argument survives.
4. **Say whether the argument got stronger or weaker.** In this case it got
   sharper: the unit exists in the interchange format, but no capture device or
   corpus delivers it, so the section could make a more precise point than
   before. Specifying a unit in a record is not the same thing as normalising a
   transduction.
5. **Flag it under its own heading for the author.** Conclusion-level edits are
   the author's call.
6. **The one exception to waiting**: apply it immediately when not applying it
   means knowingly leaving a sentence that contradicts the source it cites. Then
   flag it anyway. Say explicitly that it was applied rather than queued, and why.

Also drop what has no source. The same marker carried a scale figure that was
never attributable to anything. It went, and nothing was put in its place.

## Reporting

Write the result as a durable log, not a chat message. The next pass needs to
read it.

**Resolution log**, one row per claim checked: the marker or location, the
outcome, and one sentence saying what was established. Name the source that
carried it.

**PARTIAL section**, listing what still blocks each one. Be specific about which
source needs replacing and why.

**Rejections carried forward as warnings.** This is the part everyone skips and
it is the part that pays. Record the sources that were rejected and the reason,
so the next research pass does not propose them again. Four of the rejections
above were written up in the manuscript's triage file precisely because they
would otherwise return.

**Counts.** Proposed, rejected, and rejected by class. Those numbers are the only
honest summary of how much the verification pass actually did.

## Standing Rules

1. **Never write a citation from memory.** Not the key, not the year, not the
   volume. A remembered identifier is a fabricated one.
2. **If a value cannot be sourced, the sentence carries a marker or the sentence
   goes.** There is no third option where it stays unmarked.
3. **A negative claim names what was checked.** "No such evaluation exists"
   becomes "absent from the public record as checked", naming the programmes and
   documents examined.
4. **An unverified edition year is left out, not guessed.** A standard with no
   year is a normal, correct entry. Guessing one to make an audit pass is
   fabrication with a green checkmark on it.
5. **Report the rejection count, not just the confirmation count.** A pass that
   confirms everything did not verify anything.
