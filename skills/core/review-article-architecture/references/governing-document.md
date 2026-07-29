# The Governing Document

A skeleton for the plan file that a Review is written against, and the protocol
for amending it.

---

## Why one file, and why authoritative

A Review written over weeks accumulates locally-good decisions. Each one is an
improvement on the sentence in front of you. Their sum can be a different paper.
The only defence that scales is an authority that does not move while you work.

The plan is not authoritative because it is better reasoned than a decision made
in session 30. It is authoritative because it was made once, deliberately, with
the whole piece in view, and because a rule that yields to any sufficiently good
argument is not a rule.

---

## Skeleton

```markdown
# <Title> Review: governing plan

## 0. Scope and prohibitions
What this Review is. What it is explicitly NOT.
State the prohibitions as prohibitions, because the drift audit checks against
them and a requirement phrased positively does not catch a genre shift.

## 1. Commissioned question and thesis
1.1  The question in one sentence.
1.2  The audience.
1.3  The thesis, verbatim. This is the string the \thesisline macro carries.
1.4  Emphasis: which section is the centrepiece, and why.

## 2. Field judgements
The N claims the Review defends, one per Key point bullet.
Each names its owning section and the display item that carries it.

## 3. Body sections
Numbered, ordered, one line each on what the section must do.
Order is fixed. Merging or adding requires amending this section.

## 4. Display items
Fixed count. One row per item: number, title, owning section, what it argues,
and any data register it depends on.
State the venue's limits here: item count, full width in mm, minimum type size.

## 5. Terminology
The canonical term list. Any term used in the abstract, a heading, a figure
label, or a legend appears here or is not used.

## 6. Source materials
Every raw input, what it is good for, and what in it is SUPERSEDED by this plan.

## 7. Deliverable contract
What ships per display item and per section.

## 8. Blockers
What cannot be resolved inside the project, and who or what would resolve it.

## 9. Adjudications
Dated record of questions this plan has settled and the reasoning.
Read this before proposing to change anything above.
```

---

## Section 9 is the one people skip

An adjudication log is what stops a settled question from reopening every few
sessions. Without it the pattern is:

> Session 12 decides six figures and no Table, folding the Table's content into
> Figure 1. Session 31 reads the original commissioning synopsis, notices a Table
> in the item plan, and helpfully adds it back.

Neither session did anything wrong. The information that the question was already
settled simply did not exist anywhere durable.

Write each adjudication as: the question, the decision, the reasoning, the date,
and **what in the older materials it supersedes**. That last clause is what makes
the raw synopsis safe to keep on disk.

---

## Amendment protocol

1. **Raise the conflict as a conflict.** State what the plan says, what the better
   idea is, and what changes downstream if the plan yields. Do not open with the
   edit.
2. **Name the blast radius.** A section change touches the section list, the
   ownership table, the word budget, and both READMEs. A terminology change
   touches the abstract, every heading, every figure label, and every legend.
   A display-item change touches the assignment table, and that is exactly where
   an unassigned item hides.
3. **The authors decide.** Not the drafter, not the agent. This holds even when
   the drafter is obviously right, because the value of the plan comes entirely
   from it not being unilaterally editable.
4. **Amend the plan first, then the manuscript.** In that order. A manuscript
   edited ahead of its plan is indistinguishable from drift.
5. **Log it in section 9**, including what it supersedes.
6. **Reconcile the derived documents in the same pass.** The manuscript README,
   the figures README, and the assignment table all restate parts of the plan.
   Leaving them stale converts one authority into several disagreeing ones.

---

## The exception, and its cost

Sometimes a plan requirement is discovered to be factually impossible: the data
does not exist, the standard says something else, the claim is wrong. Then the
plan is wrong and must change.

Handle it the same way, with one addition: record **what evidence forced the
change**. "We found it awkward" is not that. "Clause 7.7 of the cited standard
states the opposite, quoted here" is.

See `claim-source-verification` for the protocol when a source reverses a
manuscript claim. That case is the legitimate path from evidence to plan
amendment, and it should be the only one.

---

## Superseding raw materials safely

Commissioning synopses, slide decks, and early figure drafts stay useful for
scope and terminology long after their item plans are obsolete. Keep them, keep
them read-only, and annotate each one where it is listed:

> `<synopsis>.docx`: commissioning scope, abstract, key points, base references.
> **Its figure numbering and display-item plan are an early version and are
> superseded by plan section 4.**

Without that annotation, every new reader has to rediscover which document wins,
and some of them will guess wrong.
