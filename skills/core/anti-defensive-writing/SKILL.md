---
name: anti-defensive-writing
description: "Remove audit, defensive, self-critical, developer-facing and commitment writing from manuscripts, Supplementary Information, legends, table notes, data/code statements and figure content. Preserve numbers, definitions, reproducibility facts, mandated statistics, null results and conditions that determine reported values. What is load-bearing depends on the target venue: an ML conference needs the no-leakage sentence a journal pass might cut. Applies the 发布会原则: the strongest advantage leads, no attempts are narrated, numbers grade results, and every comparison the field expects stays reported. Use after claim hierarchy is settled and before sentence polishing, when a draft reads like an audit report, rebuttal, self-critique or repository README, or on requests to de-audit, cut hedging, remove developer notes or promises, 去审计、审计味、防御性写作、自我批评、自我限制、自我削弱、论文是发布会、评判式写作、去包装、太多免责、写得太怂、太啰嗦、让语气更肯定、面向开发人员、代码路径、文件名、事前承诺. Also prevents these voices from being added during editing."
license: MIT
---

# Anti-Defensive Writing

A research paper argues from evidence. It does not keep an audit log of its own project, argue with
an imagined reviewer, criticize itself, document its repository, or make promises. This skill removes
those voices from every part of the paper, Supplementary Information included, and keeps everything a
reader needs to understand, trust and reproduce the work.

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

## The six voices

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
- internal vocabulary: phase and gate names, PASS or FAIL verdicts, retired metric names (files,
  folders and code names are the developer voice, below);
- checker language presented as a finding: "no additive cost is resolvable";
- attempt narration, what was tried before the final design and what did not work: "we first
  tried", "an earlier version", "we also experimented with", "did not help".

Fix. State the design fact once, as a fact ("The evaluation split was held out from model
selection"), in the section where the reader needs it. Move reproducibility detail to Methods or SI.
Delete governance language outright. An attempted variant either becomes a result with a job, an
ablation stated with its numbers as what the component contributes, or leaves the paper. A variant
the source reports without numbers does not gain a size in the rewrite.

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
  unfortunately, we acknowledge, and adjectives that grade a number: modest, limited, marginal, still
  lags, falls short;
- listing what the study did not use: datasets, runs, methods or resources that played no part;
- retreat framed as justification: "we keep it linear because deep models do not yet outperform
  linear baselines";
- limitations placed in Results, legends or SI notes, or itemized at length in the Discussion;
- verdict columns in tables: a "Qualification" or "Status" column that grades each row ("positive
  interval", "interval crosses zero", "within tolerance", "exploratory; small subset").

Fix. Report the fact neutrally, or drop it if no reader needs it ("All data were obtained from the X
collection"). Let the number grade the result: give the value and its comparison, and drop the
grading word in either direction, "modest" as much as "remarkable". Describe what was used, not what
was not. Recast a defended choice as the design
decision it was ("A linear map is the reference estimator, so that supervision can be separated from
capacity"). Where the evidence supports it, turn a defended weakness into a finding: a gap that richer
models fail to close is evidence about what limits the task. Gather genuine limitations into one
closing Discussion paragraph, stated as the scope of the research. A verdict column goes; the interval
already shows what the verdict said. Keep a plain "Note" column only for facts needed to read a row
("pooled over three runs", "n counts conditions").

### 4. Commentary voice: judging the field, the reader or the rhetoric

- commentary on how others frame the problem: "rather than the variation the task is usually framed
  around";
- rhetorical overstatement: "the aggregate score reports none of this";
- lecture-note devices: chains of rhetorical questions, "This is not an edge case", "the informative
  null is the other one";
- labels such as headline performance or the real task;
- recap closers that announce significance instead of stating a result: "Together, these results
  extend our understanding of ...". A closer that adds a conclusion stays ("Together, these
  analyses show that the gain comes from the dose module, not from model size");
- forward pointers and meta-commentary: "These controls motivate improving the evidence", "this
  opens new avenues", "paves the way";
- a rhetorical question that opens a paragraph and is answered by the next sentence.

Fix. Replace the rhetoric with the factual statement it stood for, and check that it is literally true.
Turn a rhetorical question into a statement of what the analysis isolates. Delete a recap or forward
pointer, or keep its content once where it acts: a concrete next step goes in the closing scope
paragraph of the Discussion. These are among the tells listed in `scientific-prose-style`'s
`references/ai-tells.md`.

### 5. Developer voice: the repository leaking into the paper

The text addresses someone who runs the code or opens the files, not someone who reads the paper. It
survives review because it is accurate, but no reader of the paper can act on it. Typical cues:

- folder paths and repository layout: `source_data/`, `results/`, `scripts/`, "in the repository
  root", "with larger row-level files in `source_data/`";
- file names and formats as objects: `Reactome_2022.gmt`, `scores.csv`, "provided as CSV files", "an
  index sheet in each workbook names the source file for every sheet";
- build and format notes: "the supplementary tables are editable LaTeX tables", "generated by script
  X", "regenerate and paste", "preparation of the LaTeX source";
- pipeline internals: manifest, launcher, loader ("the strict loader excluded ..."), run
  configuration ("the run configuration recorded 60 epochs"), artifact, contract, cache, and outputs
  described as "saved", "existing" or "newer";
- internal names for methods, arms, variables or runs that differ from the paper's terms: code names
  of estimators, M0/M1 arm labels, column names, command-line flags.

Fix. Name the scientific object in reader terms, or delete. "The Reactome 2022 gene-set collection
contained 1,818 terms", not the file name; "exactly k plates were selected per compound", not "a fixed
manifest selected"; "training used seeds 3407, 42 and 2025", not "the launcher fixed". Reader-facing
identifiers stay: accession numbers, public URLs, the repository named in the Code availability
statement, software names and versions, seeds, and the names of Supplementary Data files. `\texttt` is
formatting, not a licence: a path set in `\texttt` is still a path.

### 6. Commitment voice: promising what does not exist yet

The text commits the authors to a future action, or describes an arrangement, instead of stating what
exists. Typical cues: will be released, will be made available, will be deposited, a public release is
planned before acceptance, upon publication, upon acceptance, access can be arranged through the
corresponding author, we intend to, a future version will, will be addressed in future work.

Fix. State what exists now: the repository, accession or access route as it stands today, and delete
the promise. At a double-blind venue, an anonymized link or a release statement is the convention
(The venue decides what is load-bearing). If what exists does not meet the journal's policy (a private repository, no route for
editors or reviewers), the author has to fix that before submission; report it, and do not cover it
with a promise. A sentence about what future research should test is not a commitment ("Validation
across sites will be important for ...") and may stay in the closing scope paragraph. A sentence about
what the authors will do is a commitment.

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
- **Reports a comparison the field expects**, such as the standard metric or the strongest
  baseline, even where the method does not win it (Launch principles, below).
- **Declares a prespecified rule.** Keep it once, in the target field's terms (see The venue decides
  what is load-bearing), and check that each outcome it governs is reported somewhere in the paper. If one is not (a prespecified comparator whose contrast appears nowhere),
  flag it to the author; do not delete the criterion to hide the gap.
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

## Launch principles (发布会原则)

A paper is a launch, not a work report. The author's nine principles for manuscript writing map onto
this skill and its neighbours as follows.

| # | Principle | Applied by | Limit |
|---|---|---|---|
| 1 | Organize the narrative around the strongest advantage | `manuscript-optimizer`, Claim Architecture | the strongest advantage the evidence supports |
| 2 | Do not narrate what was done, tried or failed | audit voice (attempt narration) and section contracts, Results | an ablation stays, stated as what the component contributes |
| 3 | No self-weakening wording, and no list of weaknesses for the reviewer | self-critical voice | genuine scope stays once, in the Discussion or in the Limitations section a venue asks for |
| 4 | Do not stage a contest on a metric the method cannot win | Emphasis is chosen, the record is not | the comparison the field expects is still reported |
| 5 | A result that does not win is not written as a loss | Emphasis is chosen, the record is not | parity needs a narrow interval, and a trade-off needs both sides measured |
| 6 | State advantages explicitly | section contracts, Readers checks 3 and 4 and Results | an advantage is a number with its comparison, not an adjective |
| 7 | Every experiment has an argumentative job, or it goes | `manuscript-optimizer`, figure and analysis roles | a control or a prespecified analysis has a job whatever its outcome |
| 8 | Abstract and Introduction open like a launch: problem, gap, idea, hardest result | section contracts, Abstract and Introduction | the problem comes first, then the result |
| 9 | The conclusion reinforces the take-home point and never undercuts itself | section contracts, Discussion | scope comes before the closing sentence, and a scope that contradicts the headline means the headline is too broad |

Principles 6 and 8 add emphasis, not content. A claim about prior work (the gap), a protocol detail
or an explanation that the supplied text does not give is taken from the Introduction or Methods,
or left marked for the author. An explanation the data do not test is written as one ("consistent with"), not as "shows
why". The reply lists every statement the rewrite adds that the source does not contain, derived
numbers included, so that the author can confirm or cut it. The request that usually comes with the
principles, "逐处指出并给出改法", is proposal mode
(Modes).

### Emphasis is chosen, the record is not

The launch analogy holds for attention and fails for evidence. A launch audience cannot check the
numbers. A reviewer has the tables, the SI and often the code, and an omission found there reads as
selective reporting. What leads is a writing choice. What is reported is not.

Principles 1 to 3 and 6 to 9 govern emphasis and apply in full. Principles 4 and 5 touch the record
and apply only in this form:

- **The frame comes from what the method is for.** Lead with the dimension the method was built to
  improve, as the Introduction states it: unseen compounds, data efficiency, cost, a capability the
  baselines lack. Test: would the same frame have been chosen if the numbers had come out the other
  way? If not, the frame follows the result, and that is outcome switching.
- **The comparison the field expects stays.** The standard metric, the strongest baseline and any
  prespecified outcome are reported once, with their numbers and in neutral words, even where the
  method does not win. They belong where the comparison is made, usually the Results body and its
  table, not necessarily a broad position. The Abstract scopes its claim to the dimension it leads
  with, so that no reader infers a win the Results do not show.
- **No loss words, no disguised parity.** Write the values and the comparison: "0.71 against 0.74
  for X". "Comparable", "matches", "on par" and "reached parity" need an interval that is narrow
  against the differences that matter. Otherwise write "no detectable difference" and give the
  interval.
- **A trade-off needs both sides.** Explain a result that does not win by a difference in goal or by
  a trade-off only when both sides are measured and reported together: "removing curated target
  labels lowered benchmark AUROC from 0.83 to 0.80 and raised AUROC on new targets from 0.61 to
  0.70". An untested reason is labelled as a hypothesis.
- **No metric, split, candidate pool or statistic changes after the results are seen.** Wording
  cannot repair a frame chosen that way. Report it to the author as an evidence gap.

Reviewers check these because of what the reporting literature calls spin: emphasising secondary
results when the primary comparison is null, or presenting a non-significant difference as
equivalence (Boutron et al., JAMA 2010). In a randomized trial with 300 clinicians, abstracts with
spin raised the rated benefit of the treatment and lowered the rated rigor of the trial (Boutron et
al., J Clin Oncol 2014). Reporting a secondary win is not spin when the primary result is stated
plainly and is not overshadowed. At ML venues the standard
benchmarks and the strongest baselines belong in the main results table whether or not the method
wins them (`conference-paper-writing`, What Reviewers Check).

## The venue decides what is load-bearing

A sentence is reassurance only if no reader at the target venue needs it. Editors and reviewers at
different venues check different things, so the same sentence can be noise in a journal and required
at a conference. Before classifying, name the target venue and what its editors and reviewers check.
For Nature Portfolio journals, `nature-portfolio-playbook` lists the required statements. For ML
conferences, `conference-paper-writing` does (optional set, installed with `--set all`). The rules
below apply whether or not it is installed. The six voices above are calibrated for journal articles.

At ML conferences such as ICLR, NeurIPS and ICML, reviewers check three things: whether test data
influenced model selection, whether the results can be reproduced (splits, hyperparameters, seeds,
code), and how stable the conclusions are (how many runs, how wide the intervals). Four rules follow.

- **Keep one no-leakage sentence.** Reviewers look for a plain statement that test data played no
  part in selecting the model, its hyperparameters or its configuration. It is class A, not class
  C. State it once, where the evaluation protocol is described.
- **A label does not fix a selection problem.** If a configuration was chosen on data that is later
  used for evaluation, calling it "prespecified" or "fixed in advance" does not answer the reviewer.
  Report the default configuration's result beside the selected one, and report the selection to
  the author as an evidence gap. Wording cannot close it.
- **Use the field's phrasing, not trial vocabulary.** Preregistered, locked, frozen, gates and
  verdict sentences ("supported if the interval excludes zero", "criterion not met") come from
  clinical trials. An unverifiable "preregistered" invites suspicion. Write "the configuration was
  selected on the development split and applied unchanged to the evaluation split", and report
  means, medians and intervals so the reader can judge.
- **Report robustness as runs and spread.** Seed values belong in the hyperparameter table. The text
  states how many runs each number pools and how much they vary. A model trained only once is an
  evidence gap for the author, not a wording problem.

Two more journal rules turn around at ML conferences:

- **A release statement is not a commitment there.** Authors cannot link their own repository
  during review, so an anonymized code link or "code will be released upon publication" is the
  venue's convention. Keep it, worded as that venue's guide asks. The commitment voice applies to
  arrangements the venue does not ask for.
- **Limitations get their own section.** Several ML venues require a Limitations section or a
  checklist answer. Write it there, as scope, instead of folding it into a closing Discussion
  paragraph.

Process detail that a venue asks for, such as a reproducibility statement or a declaration of LLM
use, goes in that statement and follows the venue's current guide. Internal governance, ledgers and
file paths stay out of the paper at every venue.

## Where each kind of content belongs

| Part | Keeps | Removes or moves |
|---|---|---|
| Abstract | headline findings, effect sizes, the scale of the data or validation | test statistics, provenance, caveats unless the claim is false without them |
| Introduction | problem, gap, approach, findings | design controls ("no regime-specific tuning"), field commentary, rhetorical questions |
| Results | question, setup in one sentence, result, interpretation, next question; the comparison the field expects; a control, after the result it supports | chains of setup, safeguards, caveats, controls and exceptions before the result; provenance qualifiers; implementation checks; attempt narration |
| Figure legends | what is plotted, n, error bars, statistic | interpretation defences, "not selected by", "listed for completeness" |
| Table notes and columns | what each column, symbol and bold means; n; the statistic | verdict columns, "not significance" disclaimers, tolerance and gate language |
| Main figures | panels that answer a scientific question | compatibility, interface or eligibility matrices: SI table or one Methods sentence |
| Discussion | what the results mean; one closing scope paragraph | itemized self-criticism, limitations repeated from Results |
| Methods | definitions and every reproducibility fact | interpretation paragraphs, repeated artifact defences, sensitivity results and implementation checks (to SI) |
| Supplementary Information | the experimental record, in the same positive voice | self-criticism, audit commentary, unused items, reader instructions, build and format notes |
| Data, code, Supplementary Data | what exists now: repository or accession, what it contains, what was used | "not exposed", "could not be identified", unused datasets, columns identical in every row, folder paths, file and workbook mechanics, promised releases and arranged access |

## Procedure

1. **Settle the claim and name the venue first.** Run after `manuscript-optimizer`. While the claim
   is moving, an unnecessary disclaimer and a real scope condition look alike. Name the target venue
   and what its reviewers check (The venue decides what is load-bearing).
2. **Detect.** Read paragraph by paragraph, and run the detection pass below on the source. Cover the
   SI, legends, captions, table notes, table columns, end matter and data statements, not only the
   main text.
3. **Classify each hit.**
   - A. Necessary to understand the experiment: state once, naturally, where it acts.
   - B. Needed for reproducibility: move to Methods or SI, one plain sentence.
   - C. Reassurance against a possible criticism that the target venue's reviewers do not check:
     delete.
   - D. Internal project, governance or repository language: restate in reader terms, or delete.
   - E. Self-criticism: neutral fact, design decision, finding, or delete.
   - F. Null or contradictory result: keep as a finding, in neutral words.
   - G. Commitment: state what exists now, or delete and report the gap to the author.
4. **Rewrite in positive form**, and check that each rewritten sentence is literally true.
5. **Rebuild the paragraph** around its point: lead with the claim, one job per paragraph.
6. **Edit at the source.** A caption, table or table note produced by a script and pasted into the
   manuscript is edited in the generator and regenerated; an edit to the pasted copy is reverted at
   the next rebuild. When the edits are scripted, keep the file's encoding and line endings, and check
   that the diff touches only the intended lines.
7. **Rebuild the document** and rerun its gates (cross-references, terminology, figures); re-read the
   changed passages in the output. Check prose references to panel positions ("left", "lower
   section of Fig. 3a") against the current figures: the build cannot catch a figure redrawn under an
   unchanged label.

`references/worked-examples.md` holds before-and-after pairs from past revisions, grouped by voice,
with a section of sentences that looked defensive and were kept. Read it before a whole-document pass.

## Modes

- **Edit** (default): apply the procedure and report.
- **Proposal** ("先不动，只给方案", "逐处指出并给出改法", "just give me a plan"): make no edits. For each hit give the location,
  the quoted text, the voice, the action (delete, move, rewrite) and the proposed wording.
- **Light touch** ("微调", "one sentence"): change only the named sentence, and add nothing around it.

## Detection pass

Candidates only; classify before acting. On a LaTeX source, ignore comments, but scan `\texttt{...}`:
accession numbers belong there, and so do the folder paths and file names the developer-voice line
looks for.

```bash
F=manuscript.tex   # repeat for the SI and for any generator that writes captions or table notes
# audit
grep -n -i -E "locked|frozen|hash|scored once|fixed in advance|verif|sanity|leak|post[- ]hoc|original (design|evaluation)|recomputation|\bgate\b|\bPASS\b|\bFAIL\b|numerical check|predeclared|preregist|criterion (was )?(not )?met|supported if|historical|legacy" "$F"
# attempt narration
grep -n -i -E "we (first|initially) (tried|attempted|explored|used)|an earlier version|(also )?experimented with|did not (help|improve)|we then tried" "$F"
# defensive
grep -n -i -E "does not (establish|imply|mean|test|estimate|prove|relabel)|do not (claim|imply)|should not be (read|interpreted|taken)|is not an? |are not an? |not intended|rather than|instead of|for completeness|to be clear|should be noted|worth noting|visible rather than|so (that )?a reader|had .* been|specific to .*; it does not|without claiming|not (statistical )?significance" "$F"
# self-critical, including verdict columns in tables
grep -n -i -E "could not be (identified|determined|recovered)|not (exposed|identifiable|directly comparable)|unstable|\bonly (about |around )?[0-9]|remains? at null|failed to|unfortunately|we acknowledge|limitation|shortcoming|caveat|exploratory|qualification|within tolerance|interval crosses zero|positive interval|\bmodest|marginal|\blimited (gain|improvement|effect|benefit)|still (lags|behind|below|trails)|falls? short|slightly (worse|lower|behind)" "$F"
# record: parity words, each checked against its interval (Launch principles)
grep -n -i -E "about as well as|comparabl|on par|parity|indistinguishabl|equivalen|no worse than|\bmatches\b" "$F"
# commentary
grep -n -i -E "headline|usually framed|none of this|edge case|the real task|\?\s*$|(together|taken together|collectively), these|motivat\w+ (future|further)|open\w* (new )?avenues|paves? the way" "$F"
# developer: paths, files, workbooks, build and pipeline internals
grep -n -i -E '\\texttt\{|[A-Za-z0-9_\\]+/[ }.,;)]|\.(csv|tsv|xlsx?|json|ya?ml|py|ipynb|gmt|h5ad|parquet|npz|pkl)\b|manifest|launcher|loader|run configuration|artifact|workbook|index sheet|editable latex|latex source|regenerat|\bscript\b|pipeline' "$F"
# commitment
grep -n -i -E "will be (made |publicly )?(available|released|deposited|provided|shared)|(is|are) planned|planned (before|for|to)|can be arranged|upon (acceptance|publication)|after acceptance|we (plan|intend) to|future (release|version)|forthcoming" "$F"
```

## Reporting

Report five lists: every statement the rewrite adds that the source does not contain, such as a
derived number, a protocol detail, a claim about prior work or an explanation, for the author to
confirm; what was deleted or moved and why (by voice and class); every limitation kept and the
reason it is load-bearing; every null, contradictory or non-winning result, confirming that it is
still stated; and every gap that needs the author rather than an edit (an access route that does
not exist yet, a prespecified outcome reported nowhere, a stale panel reference). Then report the
build and gate status. A pass that silently deletes a mandated statement or a result is a reporting
failure, not a style improvement.

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
the body was rewritten from this repository's manuscript-revision history, and later that day the
developer and commitment voices were added: rule zero, the six voices, What stays, the placement
table, the seven-way classification, the modes, the detection pass and the remaining worked examples
are local. On 2026-11-03 the launch principles were added from the author's standing instruction,
with the limits on principles 4 and 5 taken from the reporting literature on spin. See `LICENSE` and
`UPSTREAM.md`.
