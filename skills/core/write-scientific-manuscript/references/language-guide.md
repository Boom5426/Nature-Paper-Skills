# Clear Scientific Language Guide

## Prefer direct constructions

| Less direct | Prefer when accurate |
|---|---|
| `is capable of predicting` | `predicts` or `can predict` |
| `provides an explanation for` | `explains` |
| `conducted an evaluation of` | `evaluated` |
| `with the aim of determining` | `to determine` |
| `owing to the fact that` | `because` |
| `in the context of` | name the actual setting |
| `a large number of` | `many` or the exact number |
| `demonstrated superior performance` | `performed better` plus the metric and comparator |
| `exhibited a reduction` | `decreased` |
| `serves as an indication of` | `indicates` or a calibrated alternative |

Do not apply substitutions mechanically. Preserve phrasing that carries a necessary technical distinction.

## Avoid decorative scientific vocabulary

Words such as `landscape`, `paradigm`, `framework`, `axis`, `signature`, `program`, `fine-grained`, `holistic`, `comprehensive`, `robust`, `novel`, `unprecedented`, `elucidate`, and `unlock` are not forbidden. Use them only when they name something specific. If deleting the word does not change the meaning, delete it or replace it with the concrete object.

Do not use `mechanism` for a predictive correlate, `generalization` for performance on a nearby random split, `validation` for any favorable result, or `representation quality` when only downstream performance was measured.

## Repair abstract noun chains

Find the actor and action.

- `The integration of the characterization of...` usually hides two verbs.
- `outcome prediction performance evaluation` should be unpacked into a relation, such as `evaluation of outcome prediction`.
- More than two consecutive noun modifiers deserve inspection.

Prefer:

> We evaluated whether the additional modality improves prediction across the held-out groups.

over:

> We performed a cross-group additional-modality prediction improvement evaluation.

## Make comparisons complete

State:

- what is compared;
- on which dataset or condition;
- by which metric;
- in which direction;
- by how much, when magnitude matters.

Avoid bare `better`, `higher`, `stable`, `consistent`, or `significant` without a clear reference. Reserve `significant` for statistical significance when that is what is meant.

## Keep scope visible

Attach the scope near the claim:

- `in the evaluated datasets`;
- `under this training protocol`;
- `for the primary prediction task`;
- `among the tested ratios`.

Do not bury a decisive qualifier several sentences later. At the same time, avoid repeating the same scope phrase in every sentence; establish it once per coherent passage when unambiguous.

## Use cautious language precisely

| Evidence | Typical wording |
|---|---|
| Directly measured result | `showed`, `increased`, `was associated with` |
| Repeated empirical pattern | `was observed across the evaluated...` |
| Interpretation consistent with data | `suggests`, `is consistent with`, `may reflect` |
| Plausible but weak explanation | `could arise from`, `one possible explanation is` |
| Isolated causal effect | causal verbs only when the design supports them |

Avoid reflexively adding `may` to every sentence. Unnecessary hedging makes direct observations harder to identify.

## Control sentence load

Revise a sentence when it contains several of the following at once:

- multiple contrasts;
- more than one parenthetical aside;
- a long subject before the main verb;
- several independent results;
- method, result, interpretation, and limitation together;
- pronouns with multiple possible antecedents.

Split at a conceptual boundary, not merely at a word count. Join short adjacent sentences when one supplies the cause, contrast, or consequence of the other.

## Preserve terminology

- Choose one name for each dataset, model component, task, split, metric, and biological concept.
- Do not alternate synonyms merely for stylistic variety when they could imply different meanings.
- Expand an abbreviation at first use and avoid abbreviations used only a few times.
- Match established capitalization, hyphenation, gene/protein notation, and field usage.
- Do not introduce a term in the Abstract that is defined only much later unless its meaning is obvious.

## Final first-read test

For every paragraph, ask:

1. Can a reader state its point after one reading?
2. Is every pronoun unambiguous?
3. Does each sentence explain why the next one belongs?
4. Are observation and interpretation distinguishable?
5. Is there a simpler conventional term for any coined or abstract phrase?
6. Can any phrase be removed without losing meaning?
7. Did simplification alter the scientific claim or its scope?
