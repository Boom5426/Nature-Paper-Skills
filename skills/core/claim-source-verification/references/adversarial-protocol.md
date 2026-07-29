# Adversarial Protocol

How to actually run the two-role verification, including prompt shapes, the
structured output schema, and the reasons behind the parts that look like
overhead.

---

## Why the roles must be separate contexts

A researcher who proposes a source and then checks it will confirm it. Not from
dishonesty: they already read it that way once, and re-reading with the same
frame reproduces the same reading. The rejection rate of self-checked proposals
is near zero, which looks like quality and is actually the absence of a test.

So the skeptic must start from a context that has never seen the proposer's
reasoning. It gets the claim and the source. It does not get the argument for why
the source fits, because that argument is exactly what it is supposed to
construct independently or fail to construct.

If you are running this with subagents, that means two separate agent
invocations, not two turns in one conversation.

---

## Stage 1: the proposer

One claim per invocation. Batching claims into one research pass produces
sources that drift between claims.

```
Resolve this open sourcing question from a manuscript.

CLAIM AS CURRENTLY WRITTEN:
  <the sentence, verbatim, with surrounding context>

WHAT THE MARKER ASKS:
  <the specific factual question>

For every source you propose, return:
  - full metadata as it appears in the publisher record
  - the sentence from the source that carries this claim, QUOTED VERBATIM
  - whether that sentence is printed in the source or derived by you from it
  - the source's own scope: what was measured, on whom, under what conditions
  - whether this is a primary record or a secondary account

If you cannot quote a supporting sentence, say so and propose nothing rather
than proposing the closest paper you found. A near miss costs more downstream
than an empty result.

If the source contradicts the claim, report that. Do not quietly pick a
different source.
```

That last instruction matters. In one run it is how a manuscript error surfaced:
the researcher was asked to source a claim, found the standard, and reported that
the clause says the opposite. A prompt that only asks for support would have
produced a shrug and a weaker source.

---

## Stage 2: the skeptic

```
You are verifying a proposed source-claim pairing. Your default verdict is
REJECT. Confirm only if you can do all of the following.

CLAIM:  <verbatim>
SOURCE: <metadata only, not the proposer's reasoning>

To confirm, you must:
  1. quote the sentence in the source that carries this claim
  2. confirm every metadata field comes from this one artifact
  3. confirm the source's population, site, and conditions match what the
     claim needs
  4. confirm this is a primary record if the claim requires one

Any number in the claim: state whether it is printed in the source or computed
from values in it. If computed, show the arithmetic and say so.

If you cannot open the source, verdict is BLOCKED, not CONFIRMED and not
REJECTED. Check the publisher preview before declaring it blocked; clauses and
abstracts are often outside the paywall.

If uncertain, reject.
```

**Give this stage the higher reasoning budget.** It is the stage that reads the
actual source while the proposer often read an abstract. The common mistake is to
spend effort on search and economise on verification, which inverts the value.

---

## Perspective-diverse skeptics

When a pairing can fail in more than one way, run several skeptics with
*different* lenses rather than several identical ones. Redundancy catches
inconsistency; diversity catches failure modes.

Useful lenses:

- **Does it say this?** The verbatim-sentence check.
- **On whom, and under what conditions?** The scope check.
- **Is this the primary record?** The citation-chain check. Follow it three steps;
  if it never terminates in a measurement, the claim is convention.
- **Where did the number come from?** The arithmetic check, for any quantitative
  claim.

Confirm on majority, and record the dissent. A pairing that two lenses accept and
one rejects is a PARTIAL, not a CONFIRMED with a footnote.

---

## Structured output schema

Force structured output at the tool-call layer so a mismatch is retried rather
than parsed loosely.

```json
{
  "type": "object",
  "required": ["claim_id", "source_id", "verdict"],
  "properties": {
    "claim_id":   {"type": "string"},
    "source_id":  {"type": "string"},
    "verdict":    {"enum": ["CONFIRMED", "PARTIAL", "REJECTED", "BLOCKED"]},
    "rejection_class": {
      "enum": ["does_not_support_claim", "metadata_wrong",
               "wrong_site_or_population", "not_primary_but_required_to_be",
               "paywalled_unverifiable", "fabricated"]
    },
    "supporting_sentence_verbatim": {"type": "string"},
    "sentence_is_printed_not_derived": {"type": "boolean"},
    "derivation_if_computed": {"type": "string"},
    "source_scope": {"type": "string"},
    "is_primary": {"type": "boolean"},
    "replacement_needed": {"type": "string"},
    "contradicts_manuscript": {"type": "boolean"},
    "contradiction_detail": {"type": "string"}
  }
}
```

Two fields do disproportionate work:

`supporting_sentence_verbatim` is the whole test. Requiring it converts a vague
judgement into a retrieval that either succeeds or does not.

`contradicts_manuscript` is the channel through which verification reverses a
claim. Without an explicit field, a contradiction gets reported as a rejection and
the manuscript keeps its error.

---

## Pipeline shape

Verify each claim as soon as its research completes. Do not barrier the whole
research stage before starting verification: the stages are independent per claim,
and a barrier wastes the wall-clock of every fast claim waiting on the slowest.

Barrier only when a later stage genuinely needs all prior results at once, for
example deduplicating proposed sources across claims before paying for retrieval.

---

## After the pass

Three things must survive the pass, or it will be repeated from scratch:

1. **The resolution log.** Claim, verdict, what was established, which source
   carried it.
2. **The PARTIAL list.** Which specific source needs replacing and why. PARTIAL
   markers stay in the manuscript. Removing a marker whose finding is not fully
   sourced is how an unsupported sentence ends up with an audit trail saying it
   was verified.
3. **The rejections, kept as warnings.** Otherwise the next research pass proposes
   the same rejected sources, and the second pass looks like confirmation of the
   first.

Report proposed, rejected, and rejected-by-class. A pass with no rejections did
not verify anything.
