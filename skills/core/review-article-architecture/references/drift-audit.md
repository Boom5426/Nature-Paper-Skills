# Drift Audit

How to detect that a Review has become a different Review, and what to do about
it once you have.

---

## The checklist

Run before any compression or polish pass, and whenever the draft has been worked
across more than a handful of sessions. Read the plan first, then the draft, in
that order. Reading the draft first primes you to find it correct.

**1. Genre.** Read the plan's prohibitions, not its requirements. Is the draft one
of the things the plan says it must not be? Requirements phrased positively do
not catch a genre shift, because a drifted draft usually satisfies most of them.

**2. Completeness.** List the plan's required sections. Which are missing from the
draft? A missing section is invisible from inside the draft: the remaining
sections read as a complete piece.

**3. Emphasis.** Measure section word counts. Compare to the plan's designated
emphasis. Is the section the plan names as the centrepiece actually the heaviest?
An inverted emphasis needs an explicit explanation, not an assumption that it
worked out that way for a reason.

**4. Thesis.** Put the plan's thesis sentence and the draft's abstract side by
side. Compare word by word. Not "is it weaker or stronger" but "is it the same
claim". A different claim expressed with equal confidence is the hardest drift to
see.

**5. Terminology.** Take the plan's canonical term list. Grep each term in the
draft. Then grep the draft's headings and figure labels for terms that are not on
the list. New terms that nobody added to the plan are drift with a vocabulary.

**6. The commissioned question.** Write it in one line from the plan. Read the
abstract. Does the abstract answer that question, or a neighbouring one? A
neighbouring question is drift regardless of how well it is answered.

---

## The real case

A commissioned Review on a broad sensing topic drifted, over several sessions,
into a metrology argument: that the same trait captured by different sensors is
not comparable, and that the field should be organised around measurement
comparability.

The drifted version was **good**. Six sections, five figures, internally
consistent, defensible on its own terms, well sourced. It read like a paper
somebody meant to write.

It failed checks 1 through 5, the last two together:

1. The plan explicitly prohibited writing a pure device review. That version was
   one.
2. The plan required a market section. It had been dropped entirely.
3. The plan designated one section as the centrepiece carrying the author team's
   accumulated work. It had been flattened to the same weight as everything else.
4. The thesis and the whole terminology system were different from the plan's.

Nobody made a bad decision. Each session improved the sentences in front of it.
The drift was the sum.

**What made it detectable at all** was that the plan existed as a separate,
authoritative file. Against a mutable outline, the drift would have been
indistinguishable from progress, because the outline would have drifted with it.

---

## Recovery

Recovery is not incremental. A drifted draft cannot be edited back, because the
edits that produced it were each locally correct and reversing them one at a time
reverses good work along with bad.

1. **Revert to the plan, not to a commit.** Rebuild the section structure the plan
   specifies. Start from the plan's outline with an empty body.
2. **Migrate material by paragraph, deliberately.** For each paragraph of the
   drifted version, decide: does it belong in the new structure, and under which
   section? Record the destination of every paragraph, including the ones that go
   nowhere.
3. **Keep the migration record in the tree.** In the real case this was a short
   archive section listing where every paragraph went. It is what lets a later
   reader ask "did we lose the eye-safety material?" and get an answer in ten
   seconds.
4. **Archive the drifted version to version control, not to a directory in the
   tree.** See `draft-marker-discipline`: name the commit and the recovery
   commands. Leaving it as `attic/` makes every future reader re-decide whether
   that directory still counts.

---

## What must not be carried forward

This is the part that takes discipline, because the drifted version usually
contains real work and the instinct is to salvage all of it.

In the real case, three of the drifted version's findings were judged unusable and
deliberately **not** migrated:

- an error budget whose derivation was circular, using as an input a quantity it
  purported to bound
- a readiness ladder for a set of modalities where the underlying quantities were
  never calibrated against each other, so the ordering was not meaningful
- a variance criterion stated as an if-and-only-if when only one direction holds

Each was well written. Each would have survived a prose review. The reason they
were dropped is that the drifted version's argument had accepted them, and the
new argument does not need them and cannot support them.

**Write down why each was dropped**, and keep that record in the tree even though
the material itself goes to version control. The dividing line is worth stating
explicitly:

> Material that records **why something cannot be used** stays in the working
> tree. The unusable material itself goes to git history.

Without the record, the next session rediscovers the finding, thinks it is new,
and puts it back.

---

## Prevention

The audit is a backstop. Cheaper habits, in rough order of value:

- **Read the plan at the start of a session that will touch structure.** Not the
  README, not the last section you wrote. The plan.
- **Call the thesis macro instead of retyping it.** Retyping is where thesis drift
  physically happens.
- **Amend the plan before the manuscript, always.** A manuscript edited ahead of
  its plan is drift by definition, even when the edit is right.
- **Keep the raw commissioning materials annotated as superseded** where their
  content conflicts with the plan.
- **Run checks 3 and 4 monthly**, or after any multi-session push. They are the
  two cheapest and they catch the two most expensive failures.
