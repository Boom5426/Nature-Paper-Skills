# Writing the Reply Block

One ask, one block. Write for a referee who is busy, who is reading several manuscripts this month, and
who will read the first line of your reply and skip the rest unless that line gives them a reason to
stay.

## Contents

- [The block](#the-block)
- [Three bands](#three-bands)
- [The five answers](#the-five-answers)
- [Disagreeing](#disagreeing)
- [Sub-lines inside a heavy reply](#sub-lines-inside-a-heavy-reply)
- [Plain language, before and after](#plain-language-before-and-after)
- [Cross-references and embedded figures](#cross-references-and-embedded-figures)
- [Checks before you send](#checks-before-you-send)

## The block

Fixed order, no exceptions:

```
[the referee's comment, verbatim, complete]

[answer sentence]

[evidence, if the band allows it]

[location]
```

Nothing precedes the answer sentence except, at most, one clause of thanks attached to that same
sentence.

**Verbatim means verbatim.** No ellipsis, no trimming a long comment, no fixing their grammar, no
paraphrase. Nature Methods names rephrasing a referee's comment as a manipulative tactic, and it is also
the standard way an ask silently disappears: the paraphrase drops the half you would rather not answer,
and nobody notices, including you. If the comment runs fifteen lines, it runs fifteen lines and the
reply goes underneath it.

**Every block stands alone.** A referee reads their own point, then your answer, and decides. They
should never have to scroll to another block to find out what you did.

## Three bands

Two separate dials control a reply. Severity, which is your judgment of scientific risk, sets how much
**work** happens. The referee's own framing sets how many **words** the reply gets. Conflating them is
what produces four-hundred-word replies to typographical corrections.

| The referee's framing | Shape | Ceiling |
|---|---|---|
| under a heading containing `minor`, or one sentence requesting one edit | answer, change, location, in one or two sentences | 40 words |
| a numbered substantive comment | one short paragraph, first sentence answers | 120 words |
| an objection to validity, controls, statistics, leakage, or the central claim | answer sentence, short evidence run, location, one boundary sentence | 300 words |

**When severity and framing disagree, do the work and keep the reply short.** A serious validity problem
filed by the referee as a one-line minor comment still gets the full experiment, the new supplementary
note, and the manuscript rewrite. The reply is still two sentences, because the fix lives in the
manuscript and the reply points at it. The letter is not where the work goes.

### Band 1, worked

```
> a) y-axis legend (FoE) is missing.

Added. The y axis of Fig. 2a now reads "FoE (fraction of enriched features, higher is better)".
(Fig. 2a)
```

```
> Please state the runtime.

4.2 minutes per 384-well plate on one A100 GPU. (Methods, page 19)
```

No thanks. No sub-lines. No evidence paragraph. No restatement of the ask, which is printed directly
above and costs the referee a line to re-read.

### Band 2, worked

```
> The authors did not pair the ST and scRNA-seq data from the same tissue and same dataset. It would
> be helpful to evaluate how the algorithm performs when different reference datasets are paired with
> a given target dataset.

Performance is stable across reference datasets. We paired each of three target datasets with three
different references and measured SSIM and JS; both varied by less than 6% across all nine
combinations, and the ranking against competing methods did not change. (page 9; Supplementary Fig. 7b)
```

### Band 3

Same opening discipline, then an evidence run, then the location. See the disagreement example below,
which is the hardest band 3 case.

### Anti-padding

- A reply longer than the comment it answers has to earn it.
- Anything the referee does not need in order to accept the point goes into the manuscript or the
  supplementary information.
- Never restate the referee's request back to them as your opening move.
- Do not list what you did not have to do.

## The five answers

These five names are plain descriptions for your own use. They never appear in the letter as labels.

| The answer | The first sentence looks like | The rule that keeps it plain |
|---|---|---|
| We did it | `We evaluated on the independent dataset; SSIM was 0.81 against 0.74 for the next best method, higher is better.` | Past-tense action plus the outcome. No promise verbs. |
| We did a smaller version | `We ran this on the two datasets that carry labels, and not on the third, because no labels exist for it.` | What you did and what you did not do, in that order, in the first two sentences. Never let the shortfall surface in the location line. |
| It is already in the paper | `This is in Table 3, and we have moved it into the Results text so it is easier to find. (page 9)` | Location first. Then change the manuscript anyway. |
| We disagree | `There is no data leak in these experiments.` | See below. |
| We cannot do it | `We cannot run the patient-cohort validation, because the cohort is under a data-use agreement that does not permit model training.` | Reason in the same sentence. Then the nearest thing you did instead. Then the limitation sentence you added to the manuscript. |

Two of these deserve expansion.

**It is already in the paper.** The temptation is to point at the page and stop. Do not. A careful
referee missed it, so the next reader will miss it too, which makes this a findability problem in the
manuscript and not a misreading by the referee. Move it, cross-reference it, give it a subheading, or
pull it into the abstract. A pointer with no edit is an incomplete reply, and it reads as a rebuke.
Never write `as stated in the manuscript` in a tone that implies they should have seen it.

**We cannot do it.** The reason must be real: the material or cohort does not exist and cannot be
obtained; the requested experiment answers a different question; it needs a different study design
rather than a revision; a regulatory, ethical, or data-sharing restriction applies; or the work exceeds
the revision window and no claim in the paper depends on it. Cost and effort alone are never the reason.
A `cannot` with no substitute and no limitation sentence added to the manuscript will not survive.

Choosing which of the five is correct is a triage decision, and `rebuttal-response` owns it. This file
only says how each one is written once chosen.

## Disagreeing

This is where replies go wrong, so it gets its own rules.

1. **Sentence one states the disagreement flatly, in the referee's own words.** `There is no data leak
   in these experiments.` Not `We respectfully disagree`, not `We would like to clarify that we do not
   believe`. Hedged disagreement reads as evasion and costs a round.
2. **Attack the premise, never the reader.** Never write that the referee misunderstood, misread,
   overlooked, or is incorrect. Do not make the referee the subject of a verb about reasoning. State
   what is true and let the comparison do the work.
3. **Say the concern back once, in their terms**, so the disagreement reads as engagement rather than
   deflection.
4. **Order the evidence: reframe, falsify, design, corroborate.** A fact that reframes the premise; then
   a result that would have come out the other way if the referee were right, which is the strongest
   move you have and belongs second, not last; then the design-level reason the problem cannot arise;
   then independent corroboration with numbers. Literature comes last if at all. A citation is the
   weakest thing you can offer against a specific concern about your own paper.
5. **Concede the true fraction, in its own sentence.** There is almost always something: the text was
   ambiguous, the figure invited the reading, the check was never reported. A disagreement with zero
   concession reads as defensive no matter how good the evidence is.
6. **Stay inside the scope raised.** Do not defend adjacent claims nobody questioned. Widening the
   disagreement invites a wider objection.
7. **State it once.** Answer sentence, evidence, location. Do not re-assert the denial in a closing
   paragraph; repetition reads as anxiety.
8. **End with a manuscript change anyway.** The concern arose because the text permitted it. If nothing
   in the paper changes, the next reader asks the same question, and the editor can see that.

Worked, band 3:

```
> It seems that there is a likely data leak in the machine learning process. The regression loss uses
> as ground truth the profiles extracted by an existing tool from these same datasets, and the results
> are then compared against that same tool. I see this as problematic and it likely partly explains
> the strong held-out performance.

There is no data leak, and we can show it three ways. The concern is that the supervision signal came
from a tool that had already seen these images, so the comparison would be circular.

The supervision profiles do not have to come from that tool. We re-ran the whole pipeline with
profiles generated from scratch by a separate model trained only on the training partition, and
performance held: SSIM 0.79 against 0.81 in the original setup, higher is better. If the concern were
correct, this run would have collapsed.

Training and test data are separated at the plate level in every experiment, and the supervision
profiles are always derived from the training partition alone, so test information cannot enter
training by this route.

On ten held-out plates from a different laboratory, never used for training or model selection, the
method still leads the next best by 27.3% in MAP, higher is better.

We agree the original text did not make the provenance of the supervision signal explicit, which is
what invited the reading. Methods now states it directly. (page 4; page 7; Supplementary Note 4;
Supplementary Fig. 4)
```

Note what the first sentence does and does not do. It answers, in the referee's own word `data leak`.
It does not thank, does not restate the objection at length, and does not announce that an argument is
coming.

## Sub-lines inside a heavy reply

Only band 3, and only when the comment genuinely holds three or more parts the referee did not number.

A sub-line is a **declarative claim sentence you could argue with**, not a topic label, and every noun
in it already appears in the referee's comment or in the manuscript.

| Banned | Allowed |
|---|---|
| `Data separation` | `Training and test data are separated at the plate level in every experiment.` |
| `OOD evaluation` | `On plates from a different laboratory, the method still leads by 27.3% in MAP.` |
| `Leakage-firewall architecture` | `The supervision profiles are derived from the training partition alone.` |

If you cannot build the sub-line out of words already on the page, the comment did not need sub-lines.
Coining a name forces the referee to learn vocabulary in order to read your answer, which is the
opposite of the job.

## Plain language, before and after

Fourteen rules. Each is checkable, which is the point.

1. **The first sentence is the answer.** Cover everything below it. A reader who has just read the
   comment must be able to tell whether you did it, did part of it, had already done it, disagree, or
   cannot. If not, rewrite the sentence.
2. **First sentence under 25 words**, one main clause, no parenthesis, no citation.
3. **First sentence uses the referee's own nouns.**
4. **Never rename what the referee named.** No coined replacement term, no framework name, no acronym
   they did not use. If their term is loose, keep it as the head word and attach the correction inside
   the same sentence: `the test split the referee refers to, called the validation split in Methods,
   ...`. Never swap silently.
5. **Any term the referee did not use gets a plain gloss on first use**, six words or fewer, in the same
   sentence. Every block is self-contained, so glossing twice beats a cross-reference.
6. **Thanks is at most a clause, never a sentence of its own**, and never in the first sentence alone.
7. **Every number carries four things:** the value, the unit or metric name, the direction of goodness,
   and what it is compared against.
8. **One idea per sentence, 30 words maximum.**
9. **No pronoun subject reaching back across a sentence boundary.** No sentence opening `This shows` or
   `It confirms`. Name the thing.
10. **One hedge per sentence.**
11. **Say the unwelcome thing first.** If a request was not met, `We did not` comes before the reason.
12. **No filler opener.** Delete `As the referee correctly points out`, `This is an excellent point`,
    `We fully agree with the referee that`, `We have carefully considered`.
13. **No reply ends without a location**, or the explicit sentence that no manuscript change was needed
    and why. Never close on `We hope this addresses the referee's concern`.
14. **No em dashes.** Use a comma, a semicolon, a colon, or a period.

Rules 4 and 5 work together and are easy to get backwards: **gloss the referee's word plainly, do not
replace it. Plain language comes from explaining their term, never from inventing a better one.**

Gallery:

| Before | After | Rule |
|---|---|---|
| `We thank the reviewer for this insightful comment. We have now added the requested analysis.` | `We added the requested analysis; accuracy rose from 74.1% to 78.4%, higher is better. (page 9)` | 1, 6, 7 |
| `Thanks for the comment. We have revised "contents" to "content" in the abstract and throughout the manuscript to ensure grammatical accuracy. We appreciate your valuable feedback, which has helped improve the clarity and quality of our manuscript.` | `Revised "contents" to "content" in the Abstract and throughout. (pages 1 and 3)` | 6, 12, band 1 |
| `We thank the reviewer for the insightful suggestion to analyze which genes are most important for model completion and transfer learning.` | `The most important genes do map onto known biology: content-related genes are enriched in tumour-intrinsic pathways, style-related genes in immune pathways. (Supplementary Fig. 5b, c)` | 1, 12 |
| `Performance improved substantially.` | `MAE fell from 0.42 to 0.31 against the strongest baseline, lower is better.` | 7 |
| `This demonstrates the robustness of our approach.` | `Stability across the nine reference pairings demonstrates that the result does not depend on the reference dataset.` | 9 |
| `The results may possibly suggest a potential improvement.` | `The results suggest an improvement.` | 10 |
| `We have carefully addressed all the minor comments and improved the manuscript.` | one reply per minor comment, each with its own location | band 1, blanket coverage |
| `We introduce a leakage-firewall design that structurally precludes contamination.` | `Training and test data are separated at the plate level in every experiment.` | 4 |
| `We agree and have revised accordingly.` | `Revised. The sentence now reads "matches the best published result on this benchmark". (page 3)` | 13 |
| `While we acknowledge the reviewer's concern, we respectfully believe that there may be a misunderstanding regarding our validation procedure.` | `There is no data leak in these experiments.` | 1, 2, disagreement rule 1 |

## Cross-references and embedded figures

**Cross-references are additive, never substitutive.** `As in our reply to Comment 1` may support a
block. It may never be the block. Give your own answer in your own words first, then point. A reply
whose first sentence is a pointer has been merged with another reply and no longer stands alone.
`As discussed above` is banned outright, because it names no target.

Two referees can ask the same thing. Write both replies. The second may be four lines and may point at
the first, but only after it has answered in its own words.

**A reply may embed a figure.** Introduce it in the sentence above it, give it a full standalone
caption, and number it so it cannot be confused with a manuscript figure, for example `Figure R1`. The
figure comes after the answer sentence, never before it. If a new figure has to be drawn, use
`nature-figure`, which is part of the figure stack and installs with `--figure`.

References cited only inside one reply are listed after the location line and numbered locally to that
reply.

## Checks before you send

**The two-line test**, per reply. Put the referee's ask on one line and your first sentence below it.
Read only those two lines.

- **Verb match.** The ask's main verb has a matching verb in your first sentence, or an explicit refusal
  of it. `Report the runtime` is answered by a runtime number, not by `the method is efficient`.
- **Object match.** The noun the referee attached to that verb appears in your first sentence. They said
  `Fig. 2c`, you say `Fig. 2c`.
- **Before-and-after.** If your first sentence was already true of the paper before the revision, you
  have not answered anything.
- If someone who has not read the paper cannot say whether line 2 answers line 1, the reply fails, no
  matter how good the paragraph underneath it is.

**The count check.** Asks equal reply blocks. Every referee identifier appears exactly once, in their
order, gaps preserved. Every figure, panel, table, equation, and line number they named appears by name
with a statement of what happened to it, including `no change needed` and why. No block's entire answer
is a cross-reference. Every block ends with a location.

**The highlighter check.** Print the referee's comments. Strike through each clause once you have found
the sentence in the reply that settles it. Any unstruck clause is a missing reply. This is the check
that survives a re-review, because it is the check the referee runs on you.

`scripts/check_coverage.py` covers the mechanical half; `SKILL.md` gives the invocation. It cannot tell
you whether a reply is responsive. The two-line test and the highlighter check are yours.
