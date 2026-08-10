# Response Patterns

## Contents

1. Substantive-comment architecture
2. Overview paragraph
3. Action list
4. Evidence sections
5. Claim-strength substitutions
6. Common response types

## 1. Substantive-comment architecture

Use this skeleton selectively. Replace bracketed text with verified facts.

```text
Response: We thank the reviewer for this important comment. We [performed/added/clarified] [action] to address [specific concern]. [Central result.] We have therefore revised the manuscript to [revised interpretation or scope]. Specifically, we:

1. [action or clarification];
2. [analysis and reporting change];
3. [interpretive boundary]; and
4. [documents or sections revised].

1. We first clarified [scope or design]. [What the study does and does not evaluate.]

2. We next tested [question]. [Design, controlled factors, result, and direct implication.]

3. We then examined [mechanism, sensitivity, or robustness]. [Evidence and cautious interpretation.]

4. Taken together, [supported conclusion]. [Boundary: what this should not be interpreted as proving.]

Detailed revisions are provided in [locations].
```

Keep list items parallel and order them exactly as the detailed sections.

## 2. Overview paragraph

The overview should answer four questions without forcing the reviewer to read further:

| Question | Required content |
| --- | --- |
| What did you do? | New experiment, reanalysis, clarification, or textual revision |
| What did you find? | Central result, including direction and scope |
| What does it mean? | Direct answer to the reviewer concern |
| What changed? | Revised claim, method, limitation, or supporting material |

Prefer:

```text
We added a multi-seed analysis to characterize the magnitude of the observed differences relative to run-to-run variation. The results showed [verified result]. We therefore revised the manuscript to distinguish reproducibility across training runs from practical effect magnitude and to avoid interpreting small numerical differences as universal superiority.
```

Avoid:

```text
We performed additional experiments and added more discussion. The results support our conclusions.
```

## 3. Action list

Action items should describe completed, auditable changes. Begin with verbs:

- clarified;
- evaluated;
- quantified;
- compared;
- added;
- reported;
- revised;
- restricted;
- documented.

Do not use vague entries such as `improved the discussion` unless the item states what interpretation was added or changed.

## 4. Evidence sections

Use explicit first sentences:

- `We first clarified the objective and scope of the comparison.`
- `Having defined this scope, we next tested whether the main finding was sensitive to...`
- `We then examined the factors associated with...`
- `Finally, we clarified the interpretation and boundary of these results.`
- `Taken together, these analyses show... within the evaluated protocol.`

Within a section, use this order when possible:

1. question;
2. design and controls;
3. result;
4. interpretation;
5. limitation or boundary;
6. document/figure citation.

## 5. Claim-strength substitutions

| Risky wording | Safer evidence-matched wording |
| --- | --- |
| proved that X causes Y | provides evidence consistent with X contributing to Y |
| isolated the effect of X | varied X while retaining [named factors]; [remaining factors] could not be separated |
| target-specific optimum | best-performing target-specific ratio in the evaluated sweep |
| statistically identical | did not show a practically substantial difference under the evaluated analysis |
| consistently inferior | showed the lowest overall performance on [dataset/setting] |
| robust in general | remained stable across the evaluated [seeds/configurations/datasets] |
| fair comparison | controlled comparison under a standardized protocol |
| intrinsic representation quality | practical downstream utility under the evaluated pipeline |
| model capacity was controlled | maximum input-to-output path depth was held constant; effective capacity may still differ |
| effective cross-modal exchange | shared layers through which cross-modal information could contribute |
| disruption proves use of modality | predictions were sensitive to information carried by the disrupted modality |
| feature-space harmonization | harmonization to the shared [exact output/input] space |
| entered a stable regime | validation performance had stabilized or reached a plateau |

## 6. Common response types

### Standardized benchmark versus individual optimization

Define the benchmark target first. Explain that a common protocol estimates practical downstream utility, not intrinsic quality or each method's performance ceiling. Add sensitivity analyses if available. Limit the conclusion to the evaluated architectures and protocols.

### Frozen versus fine-tuned backbones

Explain why the primary frozen protocol serves the benchmark objective. Describe evaluated adaptation strategies as task-specific fine-tuning approaches. State why a method's released tuning workflow may not transfer to the setting evaluated here. Report the result, then preserve the possibility that more extensive model-specific conditioning could differ.

### Small numerical improvements

Separate:

1. run-to-run stability;
2. absolute effect magnitude;
3. consistency across datasets.

Explain what the seed count actually quantifies and what it does not. Report precise mean ± s.d. for the primary comparison. Avoid a low-power significance test merely to produce a P value.

### Mechanistic interpretation from diagnostics

Name each diagnostic and the exact property it measures. Keep performance, gradient behavior, disruption sensitivity, and mechanistic interpretation in separate sentences. Use `consistent with` unless the design supports causal isolation.

### Out-of-distribution failure

Analyze each OOD setting separately before synthesizing. State which factors can be isolated and which remain confounded. Use exact feature or output-space language. Do not turn correlations into a complete causal decomposition.

### Data pairing and multimodal complementarity

Describe pairing granularity, aggregation, alignment keys, retained metadata, and unmatched nuisance factors. Distinguish co-measurement of two modalities on the same unit from matching them at a coarser entity level. Prefer `predictive complementarity` or `non-redundant predictive information` unless complementarity in the underlying system is directly demonstrated.

### Missing baseline or comparison

Name what the added comparator tests and under what protocol before reporting any number. State whether the comparator was tuned or ran under the shared protocol with its published configuration unreproduced. A comparison added under a protocol that favors the proposed method answers a different question than the one asked.

### Insufficient ablation

State what each removed component is hypothesized to contribute, then report the observed change against run-to-run variation, not against zero. A drop smaller than the seed spread does not establish a contribution. Say which ablations were run and which were not.

### Scalability or efficiency

Separate wall-clock time, peak memory, and asymptotic complexity; they fail independently. Name hardware, batch size, precision, and data size for every timing number. Do not present a complexity bound as a measurement, or a single measurement as a bound.

### Theoretical concern

State the assumptions of any added proposition and whether the empirical setting satisfies them. A result proved under assumptions the experiments violate is not evidence for those experiments; say so rather than letting the statement stand as implicit support.

### Missing related work

State how the cited work differs in problem setting, supervision, or evaluation, not only that it differs. Verify every added citation against the actual paper. Do not add a reference solely to satisfy the comment, and do not assert a difference the cited work does not have.

### Minor comment

Use one compact paragraph: acknowledge, answer directly, quote the corrected wording if useful, and identify the location. Do not inflate a terminology correction into a multi-part response.
