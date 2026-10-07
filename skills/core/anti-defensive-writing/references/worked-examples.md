# Worked examples

Before-and-after pairs from past manuscript revisions, lightly anonymized. Each pair keeps the
information and changes the posture. Read the last two sections too: some sentences that look
defensive are load-bearing, and some fixes are to a whole element, not a sentence.

## Audit voice

> The configuration was frozen, hashed in advance, and the locked split was scored once.

> The evaluation split was held out from model selection.

---

> The final matrices were rebuilt from raw counts on those genes using all-gene size factors, so that
> normalization is applied once.

> The final matrices were rebuilt from raw counts on the selected genes, using size factors computed
> across all genes.

---

> All three splits are leakage-safe.

> Hidden material was excluded from the candidate library in all three splits.

---

> The additive decoder was included precisely because it cannot express interaction. It is a
> structural control rather than a competitor: the decomposition should assign it an interaction
> amplitude of zero, and this was verified rather than assumed.

> The additive decoder is a structural control: it cannot express interaction, so the decomposition
> should assign it an interaction amplitude of zero. [The measured amplitude follows.]

---

> |corr| is the absolute correlation between the two components and is the numerical check that the
> decomposition is orthogonal wherever it is applied.

> |corr| is the absolute correlation between the two components.

---

> ... with no additive cost resolvable.

> ... with no detectable change in additive recovery.

---

Results sentence carrying provenance qualifiers ("in a post hoc analysis added after the original
evaluation, the primary arm of the original design ..."): state the result. If the order in which
analyses were specified matters for interpretation, say so once in Methods.

---

> Support and reference assignments were determined using compound and acquisition identifiers
> without inspecting response values.

> Support and reference assignments were made from compound and acquisition identifiers alone.

---

> ... one pseudo-compound per candidate; gamma was fixed by n and not tuned.

> ... one pseudo-compound per candidate, so gamma is set by n.

## Defensive voice

> These ratios describe score separation on the reported runs. They neither test pairwise differences
> nor establish ranking stability, because they do not estimate the paired covariance of scores
> across seeds.

> These ratios describe score separation on the reported runs.

(The statistical nature of the ratio is stated once, in Statistical analysis, as "a descriptive ratio
of two spreads".)

---

> These displayed orderings are therefore conditional on the tested representation set, decoder and
> seed; they are not a general ranking-stability test.

> These orderings therefore hold for the tested representation set, decoder and seed.

---

> The interaction component is the deviation from the best additive fit to those pairs, so measuring
> different compounds, samples or pairs changes it; it should not be read as an intrinsic biological
> interaction.

> The interaction component is the deviation from the best additive fit to those pairs, so it is
> defined relative to the measured compounds, samples and pairs.

---

> Success under one holdout strategy does not establish the same capability under another.

> Each holdout strategy tests a distinct capability.

---

> It is a genetic-perturbation test of the same retrieval formulation rather than a drug-retrieval
> benchmark.

> Dataset F provides an independent genetic-perturbation retrieval setting.

---

> For the exact recovery calculation, the scored target is required to equal the single arm-A
> measurement, not an average of the two arms. Had that target been an average of n measurements,
> the reference would need rescaling by the Spearman-Brown relation before any recovery ratio was
> formed. This statement is specific to the exact recovery support; it does not relabel the ordinary
> benchmark target.

> On the exact recovery support the scored target equals the single arm-A measurement, so the
> reference applies without the Spearman-Brown rescaling that an average of n measurements would
> require.

---

> The organoid rows are the prespecified primary pooled set, not a set selected by the compatibility
> diagnostic.

> The organoid rows are the prespecified primary pooled set.

---

> The supplementary table lists the per-seed values in both regimes so that the instability is visible
> rather than asserted.

> The supplementary table lists the per-seed values in both regimes.

---

A Methods paragraph beginning "This limiting argument does not imply that every score is
equivalent ...", after Results had already stated the relation: deleted. Methods defines the scores;
Results interprets them once.

---

An Introduction sentence carrying a claim, three regimes, a control, two exceptions and a reference
value in one clause: split into two claims, then a closing sentence that states the consequence.

---

> Agreement across repeats should therefore not be interpreted as recovery of an
> acquisition-independent biological truth.

> Agreement across repeats therefore measures reproducibility within an acquisition design, which
> can include shared technical effects.

---

> The implementation uses this covariance shrinkage rule without claiming that a fully specified
> generative distribution or calibrated posterior intervals were established.

> The rule is used as a point estimator; no posterior intervals are computed.

---

> Bold marks the better mean within each setting, not statistical significance.

> Bold marks the better mean within each setting.

(Significance is carried by the intervals printed in the same cells.)

## Self-critical voice

> All data were read from the processed collection. No primary publication could be identified for
> cohorts A, B, C or D.

> All data were obtained from the processed collection.

---

> The two that do not cover the full panel are scored on the subset they cover and are not directly
> comparable with the rest.

> The two that do not cover the full panel are scored on the subset they cover.

(The fact that sets comparability, a different panel, stays; the verdict goes.)

---

> The held-out-compound rows are listed for completeness and are not interpreted in the main text:
> only a few held-out compounds contribute to them, and Supplementary Note 3 gives the per-seed
> instability that follows.

> The held-out-compound rows rest on a few held-out compounds (Supplementary Note 3).

---

Section headings in an SI note, rewritten from what the quantity is not to what it is:

> It is not technical replication. / It is a summary, not an attainable limit. / Its support is not
> the evaluation support.

> It measures reproducibility across assay generations. / It summarizes a magnitude-dependent
> reproducibility. / It is defined where measurements repeat.

---

> We keep the map linear because deep models do not yet outperform linear baselines for
> perturbation-response prediction.

> We use a linear map as the reference estimator, so that the contribution of candidate-side
> supervision can be separated from model capacity. A later section tests whether higher-capacity
> alternatives recover additional signal.

---

> The method closes only about k% of the gap to the oracle.

> The method closes about k% of the gap to the oracle. The next two sections ask what information the
> remaining gap requires: richer predictors do not recover it, whereas measured responses and more
> perturbation measurements do.

(The number is unchanged. What was framed as a shortfall becomes the entry to a finding, because the
later experiments support that finding.)

---

A Discussion with six itemized limitations, each restating a Results caveat: one closing paragraph
that states the scope of the research at a high level.

## Commentary voice

> In this benchmark, headline performance is dominated by the additive component, rather than the
> sample-level variation the task is usually framed around.

> In this benchmark, aggregate performance is dominated by the additive component.

---

> The aggregate correlation reports none of this.

> The aggregate correlation obscures this redistribution and, under unseen compounds, moves in the
> opposite direction to the interaction gain.

(The rewrite is also more accurate: the aggregate score does report something.)

---

> This is not an edge case: it is the exact situation of every predictor that carries no interaction
> information at all.

> This is the situation of every predictor that carries no interaction information.

---

An Introduction built on hypothetical scores and three rhetorical questions ("Is 0.8 near ...? Is
0.4 poor ...?"): replaced by one sentence naming the three distinct questions the method answers.

## Developer voice

> Source data are provided in Supplementary Data 1 and 2, with larger row-level files in
> `source_data/`.

> Source data are provided in Supplementary Data 1 and 2.

---

> This file contains three supplementary figures, six supplementary tables and detailed methods. The
> supplementary tables are editable LaTeX tables; numerical source data are supplied separately.

> This file contains three supplementary figures, six supplementary tables and detailed methods.

---

> An index sheet in each workbook names the source file for every sheet. Row-level files with more
> than 20,000 rows are provided as CSV files in `source_data/`.

Deleted. The reader needs to know which Supplementary Data file holds the source data for which
figure, not how the workbooks are organized.

---

> The fixed `Reactome_2022.gmt` collection contained 1,818 terms.

> The Reactome 2022 gene-set collection contained 1,818 terms.

---

> For each compound, a fixed manifest selected exactly k distinct physical plates.

> For each compound, exactly k distinct physical plates were selected.

---

> The training launcher fixed the official compound split, seeds 3407, 42 and 2025 and 40 epochs.

> Training used the official compound split, seeds 3407, 42 and 2025 and 40 epochs.

---

> Inputs comprised molecular fingerprints and the control profile. Neither treated profiles nor plate
> identity entered the predictors, and the strict loader excluded all-repeat aggregates and derived
> treatment-profile fields.

> Inputs comprised only molecular fingerprints and the control profile.

---

> A generative artificial intelligence assistant was used for English-language drafting, manuscript
> organization and preparation of the LaTeX source.

> A generative artificial intelligence assistant was used for English-language drafting, manuscript
> organization and typesetting.

## Commitment voice

> The analysis code is deposited in a private GitHub repository at [URL]. Access for editorial
> assessment and peer review can be arranged through the corresponding author, and a licensed,
> versioned public release is planned before acceptance.

> The analysis code is deposited in a GitHub repository at [URL].

(The second sentence is deleted, not reworded. The author is told separately that a private
repository with no present access route does not meet the journal's code policy, which is fixed by
opening the repository or providing a reviewer link, not by a promise.)

---

> The benchmark will be extended to additional cell lines in future work.

Deleted from the paper. If the extension matters to the reader, the closing scope paragraph states
what remains to be tested, not what the authors will do.

## Looked defensive, kept

These carry information a reader needs. They were moved or tightened, not deleted.

- "Queries within a setting are not independent replicates." States the statistical unit. Kept once,
  in Statistical analysis, instead of in each task description.
- "These constructions deliberately enrich for cross-context divergence and are stress tests rather
  than representative panels." Determines how the result may be read. Kept once.
- "No P values are reported and no multiplicity adjustment was applied." A reporting requirement.
- "The prespecified primary success rule was not met." A null result, stated as a finding.
- The number of held-out compounds behind a quantity that is therefore not reported for that shift.
  It sets a reporting decision; kept once, where the decision is made.
- The measurement-model assumptions behind a reproducibility reference, restated as one positive
  sentence ("the two assay generations need not have exchangeable or independent errors, so the
  square root serves as an empirical comparison reference").
- "Mechanism-of-action recovery never became positive in any stratum" was false (one stratum had a
  small positive mean with an interval spanning zero). The fix, "no stratum showed a reliable gain",
  adds precision; it is not a defensive qualifier.

- "Validation across sites, platforms, batches and independently generated experiments will be
  important for determining how well these targets transfer." A statement about what the field
  should test, not a promise by the authors. Kept in the closing scope paragraph.
- "These preprocessing quantities were computed once on the full table, before compound splitting;
  the model standardizers were fitted on training data only." Discloses a preprocessing step that
  saw every compound. Rewritten from "were not refitted separately within each subsequent compound
  split" into a positive fact, and kept.
- "The benchmark used the original test partition, which had also been evaluated during method
  development; models, settings and endpoints were fixed before the reported scores were
  computed." Tells the reader how adaptive the test evaluation was. Kept once, in Statistical
  analysis.

## Whole-element fixes

- **An audit panel in a main figure.** A matrix of which frameworks accept which inputs explains why
  some bars are missing; it answers an interface question, not a scientific one. It moved to an SI
  table plus one Methods sentence, and the panel was replaced by one that answers a scientific
  question with an existing result (does the input representation already separate the variants?).
- **A Supplementary Data file written as an audit.** One row for every project in the source
  collection, including four the study never used, a constant column repeated in every row, and
  notes on what could not be identified. It became one row per resource or cohort actually used,
  with its use, source tables, rows used and primary publication. The SI description shrank to three
  sentences and the main-text pointer to one.
- **An end-matter statement.** A generative-AI disclosure written as a paragraph of assurances
  became two sentences: the tools and their use, and the authors' responsibility.

- **A verdict column in a supplementary table.** A "Qualification" column graded every row: "positive
  interval", "interval crosses zero", "point estimate within tolerance", "exploratory; small subset".
  The intervals already carried each verdict, and the tolerance was a prespecified criterion that
  belongs, once, in Supplementary Methods. The column became a plain "Note" column kept only for
  facts needed to read a row ("pooled over three runs", "n counts conditions").
- **A table note written by a generator.** The note "bold marks the better mean, not statistical
  significance" and the table title came from the script that builds the table, and the manuscript
  held a pasted copy. Editing only the pasted copy would have been reverted by the next rebuild; the
  edit went into the generator, and the table was regenerated and pasted again.

## Paragraph continuity after a posture edit

The posture pass can leave a navigation sentence as an isolated paragraph. This is
a paragraph-function problem, not a reason to delete the scientific reference.

Before:

> Candidate centres span minority-specialist, balanced and majority-specialist responses.
>
> Full generator details are provided in Supplementary Note 2.

After:

> Candidate centres span minority-specialist, balanced and majority-specialist responses
> (Supplementary Note 2).

The destination is retained at the end of the relevant description. If the pointer
also defines an essential condition, keep that condition in the text. Use
`write-scientific-manuscript` for paragraph/equation continuity rather than treating
all short paragraphs as defensive writing.

---

> The prespecified primary success rule was not met.

Keep. This is an independent null finding, even if it is a one-sentence paragraph.
Its brevity alone does not justify merging it with an unrelated positive result.

---

Before:

> We carefully verified that survival changed by 1 percentage point across 12 independent
> cultures (95% CI −3 to 5 percentage points). This should not be overinterpreted.

After:

> Survival changed by 1 percentage point across 12 independent cultures (95% CI −3 to 5
> percentage points).

The effect, interval, unit and replication count remain. No survival benefit is
invented, and the null-compatible interval is not removed to make the text positive.

## Upstream examples

From `Kiterlin/anti-defensive-writing` (MIT), unmodified:

> We do not claim that these cases are representative of all contexts.

> The cases show how the mechanism operates across three institutional settings.

---

> This paper is not intended to provide a comprehensive theory of platform governance, but rather to
> examine one specific mechanism.

> This paper identifies a mechanism through which platform governance reshapes participation.

---

> This does not mean that policy design alone determines implementation outcomes.

> Implementation outcomes depend on how policy design interacts with administrative capacity.
