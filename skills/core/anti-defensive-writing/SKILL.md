---
name: anti-defensive-writing
description: "Remove audit, defensive and self-critical writing from a manuscript, its Supplementary Information, figure legends, data and code statements and figure content, while keeping every number, definition, reproducibility fact, mandated statistical statement, null result and scope condition that sets a reported value. Audit voice is project process leaking into the paper (locked, frozen, hashed, verified, post hoc, leakage-safe, gate verdicts, implementation checks). Defensive voice argues with an imagined reviewer (does not establish, should not be read as, we do not claim, for completeness). Self-critical voice has the paper judge or apologize for itself (could not be identified, not directly comparable, only a small fraction, unused datasets listed). Also carries the rule for not adding any of these while editing. Runs at the rhetorical-posture layer, after the claim hierarchy is settled and before the sentence pass. Load when a draft or SI reads like an audit report, a rebuttal letter or a self-critique, when a paragraph opens with a limitation, or on request: de-audit, less defensive, more direct, cut the hedging, 去审计, 审计味, 防御性写作, 自我批评, 自我限制, 评判式写作, 去包装, 太多免责, 写得太怂, 太啰嗦, 让语气更肯定, 别老说自己不主张什么, 读者和编辑不关心的内容."
license: MIT
---

# Anti-Defensive Writing

A research paper argues from evidence. It does not keep an audit log of its own project, argue with
an imagined reviewer, or criticize itself. This skill removes those voices from every part of the
paper, Supplementary Information included, and keeps everything a reader needs to understand, trust
and reproduce the work.

The paper should feel controlled because the design is clear, not because the authors keep saying
that it is controlled.

Read **What stays** before deleting anything, and **Local integration** for where this skill sits in
the `paper-workflow` chain.

## Rule zero: do not add it

Most audit and defensive text is added during editing, not during drafting: an edit fixes an
ambiguity, answers a co-author or reviewer comment, or adds provenance "to be safe". While editing any
text:

- Add no qualifier, disclaimer or provenance note unless the sentence would otherwise be literally
  false.
- Fix an ambiguity with a precise definition, not with a caveat. "Labels A to D denote four dataset
  regimes" beats a sentence explaining what the labels should not be taken to mean.
- A request for a small change gets a small change: one sentence, not a protective paragraph around it.
- Do not weaken a claim in advance because a control or baseline is not yet in the draft. Whether a
  claim needs qualifying is decided when that evidence arrives.

## The four voices

Each voice has recognition cues and one fix. A cue is a candidate, not a verdict; classify it with the
procedure below before changing it.

### 1. Audit voice: the project's process leaking into the paper

The text reports how the work was run and checked instead of what it found. Typical cues:

- process status: locked, frozen, hashed, scored once, fixed in advance, deterministic assignment,
  identical comparison arms restated, configuration hashes;
- verification talk: verified rather than assumed, the numerical check that, to verify, sanity check,
  leakage-safe, implementation verification, the pipeline was confirmed to;
- provenance qualifiers in Results: post hoc, added after the original evaluation, historical locked
  recomputation, primary arm of the original design;
- internal vocabulary: phase and gate names, PASS or FAIL verdicts, retired metric names, file or
  variable names outside `\texttt`;
- checker language presented as a finding: "no additive cost is resolvable".

Fix. State the design fact once, as a fact ("The evaluation split was held out from model
selection"), in the section where the reader needs it. Move reproducibility detail to Methods or SI.
Delete governance language outright.

### 2. Defensive voice: writing to an imagined reviewer

The text negotiates with a critic who is not in the room. Typical cues:

- negations of unmade claims: does not establish, does not imply, is not a, should not be read as,
  we do not claim, this is not to say, not intended to;
- reflexive contrast: rather than, instead of, not X but Y, where the contrast is not the argument;
- reassurance repeated at every mention: no leakage, prespecified, independent of the answer, why an
  artifact cannot explain the result;
- instructions to the reader: for completeness, to be clear, it should be noted, so that the
  instability is visible rather than asserted, so a reader can see where the line falls;
- counterfactual paragraphs: "Had the target been X, the reference would need Y. This statement is
  specific to Z; it does not relabel W";
- compound sentences that pack a claim together with every exception and control a reviewer might
  raise.

Fix. Say what the object is and what the result shows: positive scope. If a limit changes a reported
number or a reporting decision, keep it once, where it acts, in positive form. Split a
reviewer-defence compound sentence into its claims.

### 3. Self-critical voice: the paper judging or apologizing for itself

The text evaluates its own shortcomings instead of reporting facts. Typical cues:

- confessions of absence: could not be identified, not exposed, not identifiable, not available, no
  record exists;
- self-grading: not directly comparable, unstable, only a small fraction, remains at null, failed to,
  unfortunately, we acknowledge;
- listing what the study did not use: datasets, runs, methods or resources that played no part;
- retreat framed as justification: "we keep it linear because deep models do not yet outperform
  linear baselines";
- limitations placed in Results, legends or SI notes, or itemized at length in the Discussion.

Fix. Report the fact neutrally, or drop it if no reader needs it ("All data were obtained from the X
collection"). Describe what was used, not what was not. Recast a defended choice as the design
decision it was ("A linear map is the reference estimator, so that supervision can be separated from
capacity"). Where the evidence supports it, turn a defended weakness into a finding: a gap that richer
models fail to close is evidence about what limits the task. Gather genuine limitations into one
closing Discussion paragraph, stated as the scope of the research.

### 4. Commentary voice: judging the field, the reader or the rhetoric

- commentary on how others frame the problem: "rather than the variation the task is usually framed
  around";
- rhetorical overstatement: "the aggregate score reports none of this";
- lecture-note devices: chains of rhetorical questions, "This is not an edge case", "the informative
  null is the other one";
- labels such as headline performance or the real task.

Fix. Replace the rhetoric with the factual statement it stood for, and check that it is literally true.

## What stays

A sentence is load-bearing, and is reshaped rather than deleted, when it does one of these:

- **Defines or reproduces the work.** Split construction, held-out design, leakage prevention stated
  once as a fact, control matching, cluster bootstrap, matching rules, seeds, software versions.
  Methods may read procedural; that is its job.
- **Meets a reporting requirement.** Unit of replication and n, no P values or multiplicity
  adjustment, blinding, exclusions, prespecification. State each once, in Statistical analysis.
- **Sets a reported value or a reporting decision.** For example, a ratio is not reported under one
  distribution shift because only a few held-out compounds support it; keep that count once, where
  the decision is made.
- **Gives an estimator's assumptions** that the reader needs to interpret it.
- **Reports a null, negative or contradictory result.** State it plainly as a finding ("The
  prespecified primary success rule was not met"). Never delete a result to improve tone.
- **Frames a construction that determines interpretation**, once: "These constructions enrich for
  cross-context divergence and are stress tests, not representative panels."

Whether a sentence is load-bearing depends on what it states, not on which skill or reviewer put it
there. An integrity audit can place a load-bearing statement ("n is five seeds") and an audit-voice one
("absent from the public record as checked") in the same pass.

Two more constraints. A positive rewrite must be literally true: "never became positive in any
stratum" was false when one stratum reached a small positive mean with an interval spanning zero; the
fix is a precise statement ("no stratum showed a reliable gain"), which is precision, not defence. And
tone never outranks evidence: no number, interval, n, control or null result is traded for
directness, and a posture pass cuts repetition, not content.

## Where each kind of content belongs

| Part | Keeps | Removes or moves |
|---|---|---|
| Abstract | headline findings, effect sizes | test statistics, provenance, caveats unless the claim is false without them |
| Introduction | problem, gap, approach, findings | design controls ("no regime-specific tuning"), field commentary, rhetorical questions |
| Results | question, setup in one sentence, result, interpretation, next question | setup, safeguard, caveat, control, exception chains; provenance qualifiers; implementation checks |
| Figure legends | what is plotted, n, error bars, statistic | interpretation defences, "not selected by", "listed for completeness" |
| Main figures | panels that answer a scientific question | compatibility, interface or eligibility matrices: SI table or one Methods sentence |
| Discussion | what the results mean; one closing scope paragraph | itemized self-criticism, limitations repeated from Results |
| Methods | definitions and every reproducibility fact | interpretation paragraphs, repeated artifact defences, sensitivity results and implementation checks (to SI) |
| Supplementary Information | the experimental record, in the same positive voice | self-criticism, audit commentary, unused items, reader instructions |
| Data, code, Supplementary Data | what is available, where, and what was used | "not exposed", "could not be identified", unused datasets, columns identical in every row |

## Procedure

1. **Settle the claim first.** Run after `manuscript-optimizer`. While the claim is moving, an
   unnecessary disclaimer and a real scope condition look alike.
2. **Detect.** Read paragraph by paragraph, and run the detection pass below on the source. Cover the
   SI, legends, captions, table notes and data statements, not only the main text.
3. **Classify each hit.**
   - A. Necessary to understand the experiment: state once, naturally, where it acts.
   - B. Needed for reproducibility: move to Methods or SI, one plain sentence.
   - C. Reassurance against a possible criticism: delete.
   - D. Internal project or governance language: delete.
   - E. Self-criticism: neutral fact, design decision, finding, or delete.
   - F. Null or contradictory result: keep as a finding, in neutral words.
4. **Rewrite in positive form**, and check that each rewritten sentence is literally true.
5. **Rebuild the paragraph** around its point: lead with the claim, one job per paragraph.
6. **Rebuild the document** and rerun its gates (cross-references, terminology, figures); re-read the
   changed passages in the output.

`references/worked-examples.md` holds before-and-after pairs from past revisions, grouped by voice,
with a section of sentences that looked defensive and were kept. Read it before a whole-document pass.

## Modes

- **Edit** (default): apply the procedure and report.
- **Proposal** ("先不动，只给方案", "just give me a plan"): make no edits. For each hit give the location,
  the quoted text, the voice, the action (delete, move, rewrite) and the proposed wording.
- **Light touch** ("微调", "one sentence"): change only the named sentence, and add nothing around it.

## Detection pass

Candidates only; classify before acting. On a LaTeX source, ignore comments and `\texttt{...}`.

```bash
F=manuscript.tex   # repeat for the SI
grep -n -i -E "locked|frozen|hash|scored once|fixed in advance|verif|sanity|leak|post[- ]hoc|original (design|evaluation)|recomputation|\bgate\b|\bPASS\b|\bFAIL\b|numerical check" "$F"
grep -n -i -E "does not (establish|imply|mean|test|estimate|prove|relabel)|do not (claim|imply)|should not be (read|interpreted|taken)|is not an? |are not an? |not intended|rather than|instead of|for completeness|to be clear|should be noted|worth noting|visible rather than|so (that )?a reader|had .* been|specific to .*; it does not" "$F"
grep -n -i -E "could not be (identified|determined|recovered)|not (exposed|identifiable|directly comparable)|unstable|\bonly (about |around )?[0-9]|remains? at null|failed to|unfortunately|we acknowledge|limitation|shortcoming|caveat" "$F"
grep -n -i -E "headline|usually framed|none of this|edge case|the real task|\?\s*$" "$F"
```

## Reporting

Report three lists: what was deleted or moved and why (by voice and class); every limitation kept and
the reason it is load-bearing; every null or contradictory result, confirming that it is still
stated. Then report the build and gate status. A pass that silently deletes a mandated statement or a
result is a reporting failure, not a style improvement.

## Local integration

### Where this runs

`paper-workflow` places this skill at layer 4, the rhetorical-posture layer:

1. structure (`manuscript-optimizer`)
2. prose (`scientific-writing`)
3. passage logic (`write-scientific-manuscript`)
4. **rhetorical posture (this skill)**
5. sentence pass (`scientific-prose-style`), last

Run it after the claim hierarchy is stable and before `scientific-prose-style`, because removing
defensive scaffolding rewrites paragraph openers and sentence boundaries that the punctuation and
rhythm pass then has to settle. Moving an audit panel out of a main figure is a structural change:
hand it to `figure-planner` rather than editing the figure here.

### Boundary with the integrity audits

`stats-reporting-audit`, `claim-source-verification`, `citation-verifier`, `data-availability` and
`submission-audit` add statements a paper needs: the unit of replication and n, no P values, access
routes, the count behind a reporting decision. Those are load-bearing by type (What stays), and the
edit they may need is a change of form, not deletion: move the statement out of a high-impact
position, state it once instead of at every mention, write it as positive scope, and drop the
instruction to the reader while keeping the fact. The same audits can also add audit voice ("as
checked", "not exposed", "could not be identified"); that wording is treated like any other.

`submission-audit` runs after this skill. Anything it adds is held to rule zero, and the detection
pass is rerun on the changed passages.

Worked example, from a Methods section:

Defensive:

> This component is an operational residual and is not assumed to represent a noise-free biological
> or causal effect. It may contain measurement noise and other unmodelled variation.

Same information, stated as scope:

> This component is an operational residual under the specified additive decomposition. It aggregates
> context-specific pharmacological variation, residual marginal structure and measurement noise.

### Boundary with `scientific-prose-style`

`scientific-prose-style` owns punctuation, rhythm, the em-dash budget and hedge calibration inside a
sentence. This skill owns authorial posture at the paragraph and document level: what a paragraph
leads with, where a caveat sits, whether a sentence advances the argument or pre-empts an objection,
and whether a passage belongs in the paper at all. They stack, in that order.

## Provenance

Adapted from `Kiterlin/anti-defensive-writing` (MIT, https://github.com/Kiterlin/anti-defensive-writing).
The core rule (advance the claim directly, keep necessary limitations, prefer positive scope) and the
three examples marked as upstream in `references/worked-examples.md` come from upstream. On 2026-09-30
the body was rewritten from this repository's manuscript-revision history: rule zero, the four
voices, What stays, the placement table, the six-way classification, the modes, the detection pass and
the remaining worked examples are local. See `LICENSE` and `UPSTREAM.md`.
