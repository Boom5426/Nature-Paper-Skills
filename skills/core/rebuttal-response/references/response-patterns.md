# Response Patterns

## Contents

1. Reviewer-alignment matrix
2. Architecture selection
3. Overview paragraph
4. Action lists and evidence sections
5. Revision-location close
6. Claim-strength substitutions
7. Common response types

## 1. Reviewer-alignment matrix

Before drafting, create one private row for every independently answerable request:

| Reviewer term or request | Direct answer | Action/evidence | Result | Revision location |
| --- | --- | --- | --- | --- |
| [exact object] | [yes/no/what changed] | [analysis or edit] | [verified finding] | [figure, note, section] |

Treat this as an acceptance test, not text to paste into the letter. Preserve distinctions in the comment. For example, do not merge gene and drug representations, external datasets and cell lines, or component ablation and hyperparameter sensitivity if the reviewer names them separately.

## 2. Architecture selection

### Simple comment

```text
Response: We thank the reviewer for [raising this point/this helpful suggestion]. We [corrected/clarified/added] [direct answer or change]. The revised text now reads: "[verified text]." This change appears in [exact location].
```

### Moderate substantive comment

```text
Response: We thank the reviewer for [this important comment/raising this point]. To determine whether [reviewer's concern], we [action]. [Central result.] These results show [direct answer]. We added the analysis to [location] and revised [section] to [specific change].

1. [Reviewer's first question object]
[Direct answer -> design -> result -> implication.]

2. [Reviewer's second question object]
[Direct answer -> design -> result -> implication.]

The complete analysis has been added to [figure/note]. We revised the Results to [change], the Methods to [change], and the Discussion to [change].
```

### Complex multi-part major comment

Use the moderate structure plus `Specifically, we:` only when the reviewer benefits from a short roadmap. Make every list item correspond one-to-one with a detailed section. Delete the list if it merely repeats the overview.

## 3. Overview paragraph

Begin every formal response with one brief sentence thanking the reviewer. Vary the wording naturally across comments, but do not turn the sentence into formulaic praise, a full paraphrase of the comment, or an automatic statement of agreement. The first substantive sentence immediately after it should answer the concern.

The overview should then answer four questions without forcing the reviewer to read further:

| Question | Required content |
| --- | --- |
| What did you do? | New experiment, reanalysis, clarification, or textual revision |
| What did you find? | Central result, including direction and scope |
| What does it mean? | Direct answer to the reviewer concern |
| What changed? | Revised claim, method, interpretation, or supporting material |

Prefer a brief-thanks-then-action opening:

```text
We thank the reviewer for this important comment. To determine whether [reviewer's named factor] affected [named outcome], we evaluated [design]. Although [specific values or local results] changed, [overall result] remained stable. These results show [direct answer]. We added the complete analysis to [location] and revised [section] to [specific change].
```

Avoid:

```text
We sincerely thank the reviewer for the extremely insightful and valuable comment regarding [full paraphrase of the comment]. We directly addressed this concern and added more discussion.
```

## 4. Action lists and evidence sections

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

Keep the hierarchy consistent. If an experiment contains separate gene and drug results, use one top-level action for the experiment and place gene and drug as matched subsections beneath it. Do not mix them as peer items in the action list.

### Evidence sections

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
5. document or figure citation;
6. essential boundary only if needed for accuracy.

Use the reviewer's vocabulary in section titles when accurate. Prefer `Ranking stability of gene representations` over an author-centered label such as `Further analysis 1`.

## 5. Revision-location close

Close the response by specifying both location and function:

```text
The complete analysis has been added to Supplementary Note [X], "[title]," and Supplementary Fig. [Y]. We revised the Results to report [finding], the Methods to describe [design], and the Discussion to clarify [interpretation].
```

Do not end with a generic `The manuscript has been revised accordingly.` Do not append an automatic defensive limitation after this close.

## 6. Claim-strength substitutions

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

## 7. Common response types

### Standardized benchmark versus individual optimization

Directly test whether the named downstream choice changes the requested outcome, such as overall rankings. Report absolute-value changes, local rank exchanges, and overall ranking stability separately. Then clarify what the standardized benchmark measures. Do not let a scope explanation replace the requested sensitivity evidence.

### Frozen versus fine-tuned backbones

Explain why the primary frozen protocol serves the benchmark objective. Describe evaluated adaptation strategies as task-specific fine-tuning approaches. State why released tuning workflows may not transfer to the present perturbation setting. Report the result directly. Mention untested model-specific conditioning only when needed to answer the reviewer accurately.

### Small numerical improvements

Separate:

1. run-to-run stability;
2. absolute effect magnitude;
3. consistency across datasets.

Explain what five seeds do and do not quantify. Report precise mean ± s.d. for the primary comparison. Avoid a low-power significance test merely to produce a P value.

### Mechanistic interpretation from diagnostics

Name each diagnostic and the exact property it measures. Keep performance, gradient behavior, disruption sensitivity, and mechanistic interpretation in separate sentences. Use `consistent with` unless the design supports causal isolation.

### Out-of-distribution failure

Analyze each OOD setting separately before synthesizing. State which factors can be isolated and which remain confounded. Use exact feature or output-space language. Do not turn correlations into a complete causal decomposition.

### Data pairing and multimodal complementarity

Describe pairing granularity, aggregation, alignment keys, retained metadata, and unmatched nuisance factors. Distinguish co-measurement from compound-level matching. Prefer `predictive complementarity` or `non-redundant predictive information` unless biological complementarity is directly demonstrated.

### Minor comment

Use one compact paragraph: acknowledge, answer directly, quote the corrected wording if useful, and identify the location. Do not inflate a terminology correction into a multi-part response.
