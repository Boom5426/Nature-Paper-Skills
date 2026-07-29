# Rejection Taxonomy

Five classes, with the decision boundary between them and a worked example each.
The counts are from one real verification run over 139 proposed sources for a
Review manuscript: 55 rejections, none fabricated.

Classify every rejection. An unclassified rejection teaches the next pass
nothing, and the class is what tells the author whether to find a different
source, fix a field, narrow the claim, or give up and mark it blocked.

---

## 1. `does_not_support_claim` (29 of 55)

**Definition.** The source is real, correctly identified, and topically adjacent,
but no sentence in it carries the claim the manuscript makes of it.

**Boundary.** This is not "the source is weak" and not "the source disagrees".
It is that the claim is simply absent. If the source contains a contradicting
statement, that is still this class, but say so, because it may be a
manuscript-level correction rather than a sourcing problem.

**Test.** Can you quote the supporting sentence? If not, this class. No exceptions
for "it clearly implies", "any reader would conclude", or "it follows from
Figure 3".

**Worked example.** A general overview of depth-sensing technologies was carrying
a specific proportionality between depth noise and an optical quantity. The paper
contains no noise model at all. It surveys the field; it does not derive the
relation. The fix was not a better reading of that paper, it was the primary
source that actually derives the relation from the lock-in measurement.

**Why it dominates.** A researcher looking for support for claim X finds a paper
about X, reads the abstract, and stops. Everything about the pairing looks right
except the one thing nobody checked.

**What to do.** Replace the source. If no source supports the claim, narrow the
claim to what the surviving sources do support, or cut it.

---

## 2. `metadata_wrong` (12 of 55)

**Definition.** The work exists and does support the claim, but the reference is
wrong: author list, year, venue, volume, pages, edition, or entry type.

**Boundary.** Distinguish from class 1 by asking whether fixing the fields would
make the pairing valid. If yes, this class.

**Two sub-traps worth naming separately:**

*One key, several works.* An entry built from a 1984 monograph but given the
volume and page numbers of a 1990 journal update. Every field is real; no single
artifact has all of them. Check that all fields come from one physical thing.

*The correction that is worse.* A proposed author-list fix that dropped the third
and fifth authors of a twenty-plus-author paper. The original incomplete entry
was closer to correct. Corrections arrive with borrowed authority; verify them
with the same suspicion as originals.

**What to do.** Fix the fields against the publisher record, not against memory
and not against a search-result snippet. Then re-check that the claim still
holds, because a metadata fix sometimes reveals you had a different paper in mind.

---

## 3. `wrong_site_or_population` (6 of 55)

**Definition.** The source measures the right quantity, but on a different
population, body site, cohort, capture condition, or operating regime than the
claim needs.

**Boundary.** The claim and the source are both true. The pairing is not.

**Test.** Read the source's own scope sentence: who or what was measured, under
what conditions, at what scale. Then read the manuscript sentence. If the
manuscript generalises past the source's scope, this class.

**Related trap.** *One team's choice attributed to the field.* A preprocessing
decision that one group describes as "we do X" written into the manuscript as
standard practice. Check the scope word in the source: "we" is not "commonly".

**What to do.** Either narrow the manuscript claim to the source's scope and say
so explicitly, or find a source at the scope the claim needs. Do not leave the
generalisation implicit.

---

## 4. `not_primary_but_required_to_be` (5 of 55)

**Definition.** The claim requires a primary record (a measurement, a standard's
clause, an evaluation report) and the proposal supplies a secondary one (a
review, a textbook, a press summary, another paper's citation of the primary).

**Boundary.** Secondary sources are fine for framing, orientation, and
attribution of ideas. They are not fine for a number, a limit, a threshold, or a
clause. Reserve this class for claims that need the primary.

**Worked example, the folklore case.** A pair of frequency ranges quoted for
decades in every secondary source, with no primary study reporting those bounds
anywhere. Every citation traced to another citation. The resolution was to
replace the folklore pair with two actual measurements, each carrying its own
population and task, and to say in the text which population each came from.

**Test for folklore.** Follow the citation chain three steps. If it never
terminates in a measurement, the claim is convention. Report it as convention and
name it as such, or drop it.

**What to do.** Retrieve the primary. If the primary does not exist, that itself
is the finding, and it is often more interesting than the claim would have been.

---

## 5. `paywalled_unverifiable` (3 of 55)

**Definition.** The source may well support the claim, but it could not be opened,
so nobody knows.

**Boundary.** This is not a rejection of the source. It is a refusal to certify
it. Keep it distinct from class 1: "does not support" is a finding, "could not
check" is an open item.

**Worked example.** A proposed replacement text cited a specific count from a
paper whose full text is paywalled and was never retrieved. The proposal was
itself unverifiable, and it was written as though it had been read.

**What to do.** Mark the claim BLOCKED and record exactly what would unblock it:
which document, which clause or figure, and what access is needed. Do not
downgrade to a secondary source that quotes the primary unless the manuscript
explicitly says the number is quoted at second hand.

**Note on publisher previews.** Sometimes the clause you need is in the free
preview. In the run above, one standard's clause 7.7 was extractable verbatim
from a publisher preview, and that single retrieval reversed a manuscript claim.
Check the preview before declaring a source blocked.

---

## Sixth category: not a rejection

**`fabricated`.** The source does not exist, or its identifier resolves to nothing
or to a different work.

Zero of 55 in the run above. Include the class anyway, because when it does occur
it is categorically more serious than the other five and must never be silently
folded into `metadata_wrong`. A fabricated source means the research pass itself
cannot be trusted and should be re-run rather than patched.

---

## Using the counts

The distribution is a prior, not a law, but it is a useful one:

- Expect the largest class by far to be sources that do not support their claim.
  Budget verification effort there.
- Expect roughly a fifth of rejections to be fixable metadata rather than a bad
  pairing. Do not throw those sources away.
- Expect a small but real tail of blocked items. Report them as a state, not as
  incomplete work.
- If your run reports a rejection rate near zero, the skeptic is not adversarial
  enough. About 40% of proposals were rejected in the run above, and the
  manuscript was already careful.
