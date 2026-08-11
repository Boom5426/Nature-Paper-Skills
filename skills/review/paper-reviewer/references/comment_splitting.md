# Splitting a Referee Report Into Asks

Everything in the reply depends on getting this right. A reply set can only be complete if the ask set
is complete first, and no amount of good writing later recovers a question nobody noticed.

## Contents

- [The rule](#the-rule)
- [Split triggers](#split-triggers)
- [Subtraction rules](#subtraction-rules)
- [Set expansion](#set-expansion)
- [Numbering: use theirs](#numbering-use-theirs)
- [When the referee did not number anything](#when-the-referee-did-not-number-anything)
- [Worked example 1: a nested numbered point](#worked-example-1-a-nested-numbered-point)
- [Worked example 2: an unnumbered paragraph](#worked-example-2-an-unnumbered-paragraph)
- [Worked example 3: a minor block](#worked-example-3-a-minor-block)
- [The ledger](#the-ledger)
- [Carrying the ledger across rounds](#carrying-the-ledger-across-rounds)

## The rule

**Split wherever a different action would be needed to satisfy the referee.**

Two clauses are one ask only if one and the same action settles both. If they could be satisfied
separately, refused separately, or half-done, they are two asks.

The test to apply to any candidate span: could the referee write in round 2, about this span alone,
`the authors did not do this`? If yes, it is an ask and it needs its own reply.

Over-splitting is a real failure too. A referee who spends four sentences justifying one request made
one request. The subtraction rules below exist to stop the count inflating.

## Split triggers

Mark every one of these in the referee's text, then apply the independence test to each mark.

- **An enumerator the referee supplied.** `1.`, `(2)`, `a)`, `i)`, a bullet, a dash, or
  `First, ... Second, ...`.
- **A request verb aimed at the authors.** `should`, `must`, `need to`, `please`, `I suggest`,
  `I recommend`, `it would be valuable`, `I would encourage`, `the authors are advised to`.
- **A question mark**, and the unmarked question forms: `it is unclear whether`, `I wonder`, `why`,
  `how did`.
- **A sentence asserting a defect as fact.** A factual claim is an ask. It has to be confirmed or
  refuted, and leaving it alone means the referee keeps a wrong model of the paper.
- **A separate target object.** A different figure, panel, table, equation, dataset, metric, cohort,
  section, or line number is a different ask. `Fig. 2c` and `Fig. 2d` are two asks.
- **A change of deliverable.** New data, new computation on existing data, text, a display item, a
  citation, or a factual confirmation. These six are internal working categories. They exist to make
  `different deliverable, therefore different ask` mechanical, and to catch a reply that quietly
  answers an experiment request with a paragraph of discussion. Never print them in the letter.
- **`and` or `as well as` joining two deliverables or two target objects.**

## Subtraction rules

- **Header rule.** A lead sentence that the sub-items go on to enumerate is not a separate ask. It is
  answered by one summary line before the sub-replies, or by nothing at all. A lead claim the sub-items
  do **not** cover is a separate ask.
- **Restatement rule.** A referee who says the same thing twice in different words made one ask. Answer
  it once, under the first occurrence. Do not silently drop the second sentence from the verbatim quote.
- **Rationale rule.** Do not split a request from the sentences that justify it. `The evaluation is not
  convincing because the only baseline is outdated, so the authors should add recent baselines` is one
  ask with two sentences of reasoning attached.
- **Courtesy rule.** Praise, the opening paraphrase of the paper, and referee self-disclosure such as
  `I am not an expert in imaging` are not asks. Two exceptions. A factual error inside the paraphrase
  is an ask, because letting it stand leaves the referee with a wrong model of the paper. And
  self-disclosure is a signal: every ask in that area needs to be written more plainly than usual.

## Set expansion

An ask that names a set expands to one entry per element **in the ledger**, before any drafting.

`Please add units to Fig. 2c to 2f` is four entries. `Both datasets need the split described` is two.
`All instances of the term should be corrected` is one entry per instance, which means counting them
first.

This is not pedantry. Partial execution of a set is one of the most commonly caught failures in real
review, and it is caught because the referee still has their own list. A referee who named four panels
will diff your four against theirs.

**In the letter, a set may share one reply, provided the reply names every element and says what
happened to each, including the elements that needed no change.** Four ledger entries can become:

```
Units added to Fig. 2c, 2d and 2f. Fig. 2e already carried units on both axes and is unchanged.
```

That satisfies the referee's diff without fragmenting one edit into four blocks. What is forbidden is
the range reply that names none of them: `Units have been added to Fig. 2c to 2f` leaves the referee
no way to check, and reads identically whether you did four panels or two.

Split the set into separate replies when its elements genuinely need different answers. If `2c` was
fixed, `2d` was already correct, and `2e` cannot be fixed for a reason that needs explaining, that is
three answers and it should look like three answers.

The same logic covers a set that shares one action, such as a request to define notation across
equations (3) to (5) and (8) to (10). One reply, six equations named.

## Numbering: use theirs

- **Use the referee's own number.** Never renumber, never reorder, never regroup by theme.
- **Nested items take the referee's own markers.** A point `6.` with sub-items `1)` to `5)` becomes
  `6.1)` to `6.5)`.
- **Preserve gaps.** If the referee commented on Fig. 2 panels `a)` and `c)` and skipped `b)`, the reply
  has `a)` and `c)` and no `b)`. Closing the gap is renumbering, and it makes the referee's own list
  stop matching yours.
- **Preserve their typos and their formatting inside the quote.** `Fig 2a` stays `Fig 2a`. If a typo
  makes the ask genuinely ambiguous, answer both readings in one sentence rather than picking one and
  hoping.
- **Odd labels stay odd.** `2b`, `Minor 3`, `Point 4 continued`. Tidying them is renumbering.

## When the referee did not number anything

Nature Portfolio does not require referees to number their points, and many do not. This case needs its
own rule, because inventing a numbering scheme that looks like the referee's is the worst option
available: the referee sees identifiers they never wrote and cannot map them back.

- Split at the referee's own paragraph breaks and keep the paragraphs in source order.
- Label them in a form that is **visibly the author's**, such as `R1-P1`, `R1-P2`.
- Say once, at the head of that referee's section, that the report was unnumbered and the labels were
  added by the authors for reference.
- Never merge two referee paragraphs into one block.
- If one paragraph holds two separable asks, reproduce the full paragraph once and answer the sub-asks
  under it as `R1-P3(a)`, `R1-P3(b)`, each opening with a short quotation of the referee's own phrase
  for that ask. The quotation, not the label, is what makes the pairing visible.

## Worked example 1: a nested numbered point

Referee text as received:

```
6. The evaluation is not convincing. 1) The authors should report performance on an independent
dataset. 2) The comparison in Table 2 uses different preprocessing for the baselines, which makes
it hard to interpret. 3) Fig. 2: - a) y-axis legend (FoE) is missing. - c) The used dataset is not
mentioned in the figure legend. 4) It would be valuable to discuss why the method fails on the
small-molecule subset. 5) Please state the runtime.
```

Six asks from one numbered point:

| Key | Verb | Object | Deliverable |
|---|---|---|---|
| 6 (header) | none | `not convincing` | covered by 6.1 to 6.5; one summary line at most |
| 6.1 | report | performance on an independent dataset | new data |
| 6.2 | make interpretable | baseline preprocessing in Table 2 | new computation, or text justifying it |
| 6.3a | add | y-axis legend of Fig. 2a | display item |
| 6.3c | name | dataset in the Fig. 2c legend | display item |
| 6.4 | discuss | failure on the small-molecule subset | text |
| 6.5 | state | runtime | text, one number |

What a fast reader gets wrong: item `3)` looks like one bullet and is two asks, because Fig. 2a and
Fig. 2c fail independently and can be half-fixed. And item `5)` is easy to lose entirely, because
short asks hide in the tail of long points.

## Worked example 2: an unnumbered paragraph

Referee text as received:

```
The claim that the method generalizes is not supported. All experiments use a single cell line, and
the authors do not report what happens when the reference dataset is swapped. I would also note that
the Discussion does not mention the concurrent work of Smith et al.
```

Three asks, no referee numbering, so the labels are visibly the authors':

| Key | Quoted anchor | The ask | Deliverable |
|---|---|---|---|
| R1-P4(a) | `All experiments use a single cell line` | evaluate on a second cell line, or narrow the claim | new data or text |
| R1-P4(b) | `do not report what happens when the reference dataset is swapped` | run the swap and report it | new computation |
| R1-P4(c) | `the Discussion does not mention the concurrent work of Smith et al.` | cite and discuss it | citation |

The lead sentence, `The claim that the method generalizes is not supported`, is a header under the
header rule: the three following sentences enumerate it. It gets one summary line, not its own reply.

## Worked example 3: a minor block

A minor block that quotes manuscript phrases is one ask per quoted phrase. Twelve quoted phrases are
twelve asks and twelve replies. Not one blanket line, and not twelve paragraphs either: see the 40-word
band in `reply_blocks.md`.

```
Minor comments:
- "the model achieves state-of-the-art": no comparison is given.
- "traditional methods such as ResNet50 and ViT": neither is a traditional method.
- "six times the compression without significant quality loss": PNG is lossless, so where does the
  quality loss come from?
```

Three asks. The third contains a question mark and needs a direct answer, not just an edit, so its
reply must open with the answer and not only with what was changed.

## The ledger

Build it before drafting anything. It lives at `notes/review-ledger.md`, following the `notes/`
state-file convention that `paper-bootstrap` establishes. It is an author-side working artifact and it
**never goes into the letter**. A referee should not have to consult a table to find the reply to their
own point, and should never be handed a table in which the authors have graded their comments.

```markdown
# Review ledger

Key format: R<round>/<referee>.<the referee's own label>[.<sub-label>]
Everything after the slash is copied from the referee. Author-added labels are marked.

| Round | Decision | Referees | Notes |
|---|---|---|---|
| 1 | Major revision | #1, #2, editor | |
| 2 | Minor revision | #2 only; #1 did not re-review | |

## Round 1

| Key | Referee's words (verbatim) | The ask, one line | Deliverable | Severity | Landed | Status | Link |
|---|---|---|---|---|---|---|---|
| R1/2.6.1 | "The authors should report performance on an independent dataset." | Does the gain hold on another lab's data? | new data | major | p.9, Supp. Fig. 4 | answered | new |
| R1/2.6.3a | "a) y-axis legend (FoE) is missing." | Add the y-axis label to Fig. 2a. | display item | minor | Fig. 2a | answered | new |
| R1/2.6.5 | "Please state the runtime." | What is the runtime? | text | minor | p.19 | answered | new |
| R1/2.Minor.7 | "leave-perturbations-out split" | Define the split in Methods. | text | minor | promised only | answered | new |
```

**The frozen-restatement rule.** Fill `The ask, one line` before drafting, and never edit it afterwards.
If you find yourself softening or broadening that line so it matches the reply you wrote, you have just
documented a case of answering the wrong question. Change the reply, not the question.

`Severity` is `minor`, `major`, `blocking`, or `unclear`, the same vocabulary
`rebuttal-response/references/triage-and-stance.md` uses. It is internal. It sets how much work happens,
not how many words the reply gets. See the two dials in `SKILL.md`.

`Landed: promised only` is the state that produces a round-2 complaint. No row may still read
`promised only` when the letter goes out.

In the working copy of the letter, carry the key in an HTML comment above each reply. It is invisible
when rendered, dropped by Pandoc on conversion, and greppable by `scripts/check_coverage.py`:

```markdown
<!-- R1/2.6.3a severity=minor kind=display -->
```

The LaTeX equivalent is a `%` comment. If the letter is drafted in Word, tags are impossible and the
checker falls back to matching the quoted comments against the referee source.

## Carrying the ledger across rounds

The ledger is append-only. Round-1 rows change only in `Landed`, `Status`, and `Link`.

`Status` is `open`, `answered`, `reopened`, or `closed`. **Only a referee or an editor produces
`closed`.** The authors set `answered` and stop there.

`Link` is `new`, `reopens <key>`, `duplicate-of <key>`, or `split-from <key>`.

- A round-2 comment that refers back to `my previous concern about the split` carries `reopens <key>`.
  Find the key by matching the referee's own words against the round-1 verbatim column. If nothing
  matches, that is itself a finding: the round-1 ledger was incomplete. Go back to the original report,
  add the missing row retroactively, and mark it `reopened`. Never invent a link.
- One round-2 sentence can reopen several round-1 keys. `Fig 2a and 2b were updated, but 2c, 2d, 2e,
  and 2f are not` is four entries, each linked to its own round-1 key, plus a new one for any panel the
  referee had not raised before.
- A reopened key never returns to `answered` on round-1 evidence alone. The round-2 reply restates what
  was committed, says what actually landed, and gives the current location.
- `The authors have addressed all my concerns` closes every key for that referee already at `answered`,
  and the closing sentence is recorded with its round. Keys still at `open` are **not** closed by a
  blanket statement. Flag them, because a blanket closure over an unanswered ask means the referee did
  not notice, and the editor or a later reader may.
- Journals sometimes add or replace referees between rounds. Use the journal's number and record
  `identity: new in round 2` in the round header. Do not assume `R1/3` and `R2/3` are the same person.
- Before drafting round N, list every prior key not yet `closed`. Each must appear in the round-N
  working set. A key that vanishes between rounds is a defect, not a resolution.
