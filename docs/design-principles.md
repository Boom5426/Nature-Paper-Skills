# Design Principles

Every principle below serves a reader of the paper at its target venue: the editor who decides
whether it goes to review, the reviewer who checks the evidence, or the reader who uses the result.
They are written for the default case, a research article in a Nature Portfolio journal. When the
venue, the article type or the reader differs, derive the rule again from that reader's need
instead of applying its wording. Principle 12 states this directly.

## 1. Claim Before Polish

Do not smooth prose that sits on top of an unstable claim or weak evidence chain.

## 2. Figure-Led Results

Prefer one main claim per figure. If a figure needs subdivision, keep it minimal and deliberate.

## 3. Legends Are Second-Layer Narration

Main text should stay compressed. Legends should preserve the panel roles, the essential quantitative anchors, and the exact scope of interpretation.

## 4. Reverse Outline Before Rewriting

When revising an existing section:
- identify the section thesis
- identify the job of each paragraph
- identify the evidence or reasoning each paragraph carries

Then rewrite.

## 5. Evidence-Bounded Language

Never let the abstract, introduction, or discussion overstate what the results directly show.

## 6. Venue Fit Is A Structural Decision

Choose venue family and article type early. Do not optimize a manuscript for the wrong target and try to fix it late with stylistic edits.

## 7. A Source Must Support The Claim, Not Merely Exist

Existence and correct metadata are the cheapest properties a citation has, and checking them proves almost nothing. In one measured verification run over 139 proposed sources, 55 were rejected and none was fabricated; the largest class by far was a real paper made to carry a conclusion it does not reach.

So a source is confirmed only when the sentence carrying the claim can be quoted verbatim from it. Uncertainty resolves against the source. Report the rejection count, not just the confirmation count: a pass that confirms everything did not verify anything.

## 8. Governing Document Over Good Ideas

A manuscript written across many sessions accumulates locally-good decisions whose sum is a different manuscript. Designate one file as authoritative over sections, display items, and terminology, and amend it before the manuscript, never after.

The plan is not authoritative because it is better reasoned than a decision made later. It is authoritative because it does not change while you work, and because a rule that yields to any sufficiently good argument is not a rule. When the plan and a better idea conflict, raise the conflict.

## 9. A Paper, Not An Audit Log

A manuscript states what the work found. It does not narrate how the project was run and checked
(locked, frozen, verified, post hoc), argue with a reviewer who is not in the room (does not
establish, should not be read as, for completeness), or grade itself (could not be identified, not
directly comparable, unused datasets listed). The Supplementary Information, legends and data
statements follow the same rule.

What stays is what a reader needs: numbers, definitions, reproducibility facts, the statistical
statements a journal requires, the scope condition behind a reporting decision, and null results
stated plainly. Most audit and defensive text is added while editing, so the rule binds editors
first: a change adds no qualifier unless the sentence would otherwise be false. See
`anti-defensive-writing`.

Whether a sentence is defence or a required statement depends on whether the target venue's
reviewers look for it. An ML conference needs the no-leakage sentence and the release statement
that a journal edit would cut.

## 10. Each Section Has One Job

The layer decides what to fix first; the position decides what a fixed section must do. An
Abstract, an Introduction and a Methods section are held to different standards, written once in
`paper-workflow`'s section contracts and nowhere else. Sections restate claims settled upstream
(Results → Discussion → Introduction → Abstract → Title), so a changed claim is rechecked downstream
and no section claims more than its upstream supports. Typical shapes are measured from published
papers and used as checks; formats come from the journal.

## 11. Write The Framing For The Broad Peer

Breadth is a matter of framing, not vocabulary. Front matter puts the reader in front of a problem
they recognise as theirs by the second sentence, introduces the method by what it lets its users
do, measures success against what the reader relies on and states findings in the reader's terms,
numbers included. Technical terms stay, placed after the function they
serve, and technical detail lives in Results and Methods. Clarity rules make a passage followable;
they do not make a specialist framing broad.

## 12. Derive Each Rule From Its Reader

A rule is a conclusion about what some reader needs, not a premise. Before applying one, name the
reader it serves and what it protects. When the venue, the article type or the reader differs,
derive it again and say so. Text that meets a rule's wording while defeating its purpose fails the
rule. Two corrections came from this: "open with biology" became "the reader meets their problem by
the second sentence", because weak openings in the corpus are truisms about biology as often as
about technology, and "at most one number in the abstract" became "keep the numbers the reader can
use", because most `Nature` abstracts in the sample carry them.
