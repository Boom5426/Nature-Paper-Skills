---
name: paper-reviewer
description: >-
  Referee-side skill for Nature Portfolio manuscripts, in four modes. Write a referee report:
  methodology, statistics, reporting standards, reproducibility, and data and code availability.
  Inventory a report you received: split it into every ask and sub-ask, in the referee's own words,
  own numbering, and own order, so that each one can be answered separately and nothing is missed.
  Grade a drafted reply the way an impatient referee reads it: one reply per ask, the referee's own
  comment verbatim above its answer, the answer in the first sentence, no invented vocabulary, and
  every reply landing somewhere in the manuscript. Use when the ask is review this manuscript, write
  a referee report, what will reviewers attack, turn these reviewer comments into a checklist, answer
  each comment one by one, did I miss a reviewer point, would this reply satisfy the reviewer,
  审稿, 写审稿意见, 模拟审稿, 拆解审稿意见, 逐个回复, 逐条对照, 有没有漏回, 审稿人会不会接受,
  以审稿人视角检查回复, 回复够不够直白. To choose the stance on each ask, calibrate a claim to the
  evidence, and assemble and audit the whole letter, use `rebuttal-response`: this skill decides what
  must be answered and what counts as an answer, that one decides what to say.
---

# Referee Reports and the Replies That Answer Them

Two jobs, one standpoint. Writing a referee report and answering one are the same competence seen from
two sides: you can only prove you answered a question if you can reconstruct the question that was
asked.

Pick the mode before starting.

| Mode | Input | Output |
|---|---|---|
| `report` | a manuscript | a referee report, or a prediction of what referees will attack |
| `inventory` | a referee report | every ask and sub-ask, in the referee's own words and order |
| `reply` | a report plus a manuscript | one reply per ask, plus the coverage audit |
| `grade` | a drafted reply | what an impatient referee would send back |

## The contract

A referee report is a list of questions. A reply is a list of answers. The job is to make the two lists
line up so exactly that a referee can verify it by scrolling their own report alongside your letter.

**Same count. Same identifiers. Same order. Same words. Depth matched to weight.**

The alignment has to be visible on the page, not asserted in a summary. Three consequences, and every
rule in this skill follows from them:

1. **The referee's comment is reproduced verbatim, immediately above its reply.** Not paraphrased, not
   summarised, not trimmed. Nature Methods names rephrasing a referee's comment as a manipulative
   tactic, and Nature Chemistry asks authors to list the referees' individual points.
2. **The reply uses the referee's own words.** If they wrote `data leak`, the reply says `data leak`.
   Never coin a replacement term, a framework name, or a category label that the referee would have to
   learn in order to read your answer. Plain language comes from glossing their term, never from
   inventing a better one.
3. **The referee is impatient.** Nature Neuroscience puts it as `keeping in mind that referees are
   busy`. The first sentence carries the answer. Reply length is the minimum that settles the point.
   Over-answering a light comment is as much a defect as under-answering a heavy one, and Nature
   Chemistry warns specifically that a long-winded essay style makes a revision harder to follow.

## What this skill does not own

- **`rebuttal-response`** decides what to say: the stance on each ask, the strongest claim the evidence
  supports, honest handling of negative results, and keeping letter, manuscript, and Supplementary
  Information consistent. Build the inventory here, draft there, bring the draft back here for the
  impatient-referee pass.
- **`submission-audit`** runs a single referee-style rejection pass over a manuscript nobody has
  reviewed yet. Use it before submitting; use this skill to simulate a referee beforehand and to work
  real reports afterwards.
- **`stats-reporting-audit`** owns statistical substance: the independent unit behind `n`, replication,
  multiple-comparison correction, figure-legend statistics. When an ask is statistical, take the
  substance from there and only the reply shape from here.
- **`nature-portfolio-playbook`** owns venue and article-type choice. This skill assumes the venue is
  fixed.

## Mode `report`

Read [review_checklist.md](references/review_checklist.md) for the stage-by-stage criteria, the referee
fields Nature Portfolio actually asks about, the report shape, and the rules for writing comments that
can be answered one at a time. [common_issues.md](references/common_issues.md) is the catalogue of what
to look for; [reporting_standards.md](references/reporting_standards.md) covers guideline compliance and
the portfolio-wide Reporting Summary.

## Mode `inventory`

Read [comment_splitting.md](references/comment_splitting.md). The rule in one line:

> Split wherever a different action would be needed to satisfy the referee.

Two clauses are one ask only if the same action settles both. The test: could the referee write in
round 2, about this span alone, `the authors did not do this`?

Split on any enumerator the referee supplied, any request verb, any question, any sentence asserting a
defect as fact, any separate target object, and any change of deliverable. Subtract a lead sentence that
the sub-items enumerate, a request restated in different words, and the sentences that merely justify a
request. An ask naming a set expands to one entry per element in the ledger, which is what stops a
half-done set from slipping through. In the letter those entries may share one reply, provided it names
every element and says what happened to each, including the ones needing no change. A range reply that
names none of them reads the same whether you fixed four panels or two.

**Numbering is the referee's.** Never renumber, never reorder, never regroup by theme. Preserve gaps: if
they commented on panels `a)` and `c)` and skipped `b)`, so does the reply. Preserve their typos inside
the quote. If the referee numbered nothing, do not invent a scheme that looks like theirs; split at
their paragraph breaks, use visibly author-added labels such as `R1-P1`, and say once that you added
them.

Record the result in `notes/review-ledger.md`. It is a working artifact and it never enters the letter:
a referee should not have to consult a table to find the reply to their own point, and should never be
handed a table in which the authors have graded their comments.

## Mode `reply`

Read [reply_blocks.md](references/reply_blocks.md). The block is fixed:

```
[the referee's comment, verbatim, complete]

[answer sentence]

[evidence, if the band allows it]

[location]
```

What that looks like on the page. The referee's own labels, their own order, one reply each, and the
answer first in every one:

````markdown
## Reviewer #2

Reviewer #2 raised 5 numbered comments, 6 points under "Figures:", and 12 points under
"Minor comments:". Each is quoted below in your original order with its own reply.

### Fig. 2a
> a) y-axis legend (FoE) is missing.

Added. The y axis of Fig. 2a now reads "FoE (fraction of enriched features, higher is better)".
(Fig. 2a)

### Fig. 2c
> c) The used dataset is not mentioned in the figure legend. Is it BBBC022?

Yes, it is BBBC022. The legend now names it. (Fig. 2 legend)

### Fig. 2d
> d) Classification loss decrease makes MAP and FoE worse?

Yes, beyond epoch 40. Lower classification loss past that point reflects fitting plate-level batch
signal, which MAP and FoE penalise. (page 7; Supplementary Fig. 7b)
````

Two panels the referee did not raise get no block, and the gap is left open. A referee scrolling their
own report sees their `a)`, `c)`, `d)` against your `a)`, `c)`, `d)`.

### Two dials

Severity, meaning your judgment of scientific risk, sets how much **work** happens. The referee's own
framing sets how many **words** the reply gets.

| The referee's framing | Ceiling |
|---|---|
| under a `minor` heading, or one sentence requesting one edit | 40 words |
| a numbered substantive comment | 120 words |
| an objection to validity, controls, statistics, or the central claim | 300 words |

**When the two disagree, do the work and keep the reply short.** A serious problem filed as a one-line
minor comment still gets the full experiment and the manuscript rewrite. The reply is still two
sentences, because the fix lives in the manuscript and the reply points at it.

### Plain language

The rules that matter most. The full set of fourteen, each with a failing example and its rewrite, is in
[reply_blocks.md](references/reply_blocks.md).

1. The first sentence is the answer, and reads correctly for someone who has not re-read the comment.
2. First sentence under 25 words, one main clause.
3. First sentence uses the referee's own nouns.
4. Never rename what the referee named. If their term is loose, keep it as the head word and attach the
   correction in the same sentence.
5. Any term they did not use gets a plain gloss, six words or fewer, on first use in that block.
6. Thanks is at most a clause, never a sentence of its own.
7. Every number carries value, unit or metric, direction of goodness, and comparator.
8. One idea per sentence, 30 words maximum, one hedge, and no pronoun subject reaching back across a
   sentence boundary. No em dashes.
9. Say the unwelcome thing first, and never open on filler such as `As the referee correctly points out`.
10. No reply ends without a location, or an explicit statement that nothing changed and why.

### The five answers

Plain descriptions for your own use; they never appear as labels in the letter. `We did it`, past-tense
action plus the outcome. `We did a smaller version`, what you did and what you did not, in that order.
`It is already in the paper`, the location first, then a change that makes it findable anyway. `We
disagree`. `We cannot do it`, the refusal and the concrete reason in one sentence.

Disagreement is the one that goes wrong. State the fact, not the stance: `There is no data leak in these
experiments`, never `We respectfully disagree`. Attack the premise, never the reader. Lead the evidence
with a result that would have come out the other way if the referee were right. Concede the true
fraction in its own sentence. Change the manuscript anyway, because the concern arose from text that
permitted it.

## Mode `grade`

- **The two-line test.** Referee's ask on one line, your first sentence below it, read only those two.
  Does the main verb match, or is it explicitly refused? Does the object they named appear? Was your
  first sentence already true before the revision? If a reader who does not know the paper cannot say
  whether line 2 answers line 1, the reply fails.
- **The count check.** Asks equal reply blocks. Every identifier appears once, in order, gaps preserved.
  Every figure, panel, table, and line number they named appears by name, including the ones needing no
  change. No block's whole answer is a cross-reference. Every block ends with a location.
- **The highlighter check.** Strike through each clause of the report once you find the sentence that
  settles it. Anything unstruck is a missing reply.
- **Landing.** The change a reply promises must exist in the manuscript. A reply that lives only in the
  letter is the most commonly caught failure in re-review.

Run the checker for the mechanical half: verbatim quoting, order, one reply per ask, locations, blanket
phrases, bloat.

```bash
python3 ~/.codex/skills/paper-reviewer/scripts/check_coverage.py \
  --reviewer reviews/round1.txt --letter response/round1.md \
  [--ledger notes/review-ledger.md] [--manuscript manuscript.md] [--strict] [--json]
# Claude Code (global install): replace ~/.codex/skills with ~/.claude/skills
# Claude Code (project-local install): replace ~/.codex/skills with .claude/skills
```

It cannot judge whether a reply is responsive. A clean run is not a good letter.

## Nature Portfolio notes

Sources for everything in this section are listed at the end of
[review_checklist.md](references/review_checklist.md). Policy changes, so check the journal page.

- **Assume the reply will be published** unless you have checked the specific journal page and confirmed
  otherwise. Nature has published referee reports and author responses for all new research submissions
  since June 2025; Nature Communications since November 2022; other titles vary, some by opt-in. Every
  referee sees every other referee's report and your rebuttal in any case.
- **The overview belongs in the cover letter to the editor, not at the head of each referee reply.**
  The cover letter is not published and is the place for anything the referees should not see.
- **The editor adjudicates.** Decisions are not a vote. When referees conflict, answer each in their own
  block, state the conflict once as fact, and let the editor resolve it. Do not use one referee against
  another.
- **Editorial requirements are not referee comments.** A decision letter can impose things no referee
  asked for. They get their own blocks.
- **Referee report fields differ across the portfolio**, and reports need not follow the listed order,
  so never assume a received report is numbered. Some journals expose a separate code-assessment
  section, so a code comment may arrive outside the main remarks block and still needs its own reply.

## Related files

| File | Open when |
|---|---|
| [review_checklist.md](references/review_checklist.md) | writing a referee report, or predicting what referees will attack |
| [comment_splitting.md](references/comment_splitting.md) | turning a received report into an inventory, or carrying it across rounds |
| [reply_blocks.md](references/reply_blocks.md) | drafting or grading any individual reply |
| [common_issues.md](references/common_issues.md) | naming a methodological or statistical problem, or classifying a received comment |
| [reporting_standards.md](references/reporting_standards.md) | a guideline, checklist, or Reporting Summary is at issue |
| `scripts/check_coverage.py` | before sending, for the mechanical coverage audit |

---

*Provenance: the referee-report half is adapted from `inno-paper-reviewer`. The reply-alignment layer is
original to this repository, distilled from published Nature Portfolio guidance on responding to
referees and from transparent peer review files.*
