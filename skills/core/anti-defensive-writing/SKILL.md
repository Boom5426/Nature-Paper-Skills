---
name: anti-defensive-writing
description: "Remove defensive writing from a draft: unnecessary caveats, disclaimers, hedges, apology-like framing, self-limiting negations, and over-explanations added to pre-empt an imagined critic, while preserving the scope, accuracy, safety, ethical, legal, and methodological limits that are load-bearing. Runs at the rhetorical-posture layer, after the claim hierarchy and the integrity audits are settled and before the final sentence pass. Load when a draft reads hedged, over-caveated, apologetic, verbose, or timid, when a paragraph opens with a limitation, when the text keeps saying what it does not claim, or on request: make it more direct, more confident, less defensive, cut the hedging, 防御性写作, 太多免责, 写得太怂, 太啰嗦, 删掉多余的限定, 让语气更肯定, 别老说自己不主张什么."
license: MIT
---

# Anti-Defensive Writing

Run this at the rhetorical-posture layer, not first. See **Local integration** at the end of this
file for where it sits in the `paper-workflow` chain and which limitations it must never delete.

## Core Rule

Advance the claim directly.

Say what is true, what the text argues, what the evidence shows, or what the method does. Do not default to explaining what the text does not claim, does not prove, does not imply, does not cover, or does not attempt.

Use a calm, competent authorial posture. Write as an author explaining an argument to the reader, not as an author negotiating with an imagined critic.

## Preserve Necessary Precision

Keep limitations when they are necessary for accuracy, ethics, law, safety, or methodological transparency.

A limitation is necessary when it affects:

- the validity of the claim;
- the interpretation of the evidence;
- the scope of application;
- the research design;
- the reader's ability to use the result correctly.

Write necessary limitations once, clearly and calmly. Place them in the appropriate section, usually methods, discussion, or limitations. Do not scatter them through abstracts, introductions, contribution paragraphs, topic sentences, conclusions, or executive summaries unless the limitation is essential to that exact sentence.

## Detection Checklist

Before finalizing a draft or revision, check for:

- unnecessary disclaimers;
- repeated statements of what the text does not claim;
- excessive hedging;
- caveats in high-impact positions;
- paragraphs that start with limitations;
- negative framing where positive framing would work;
- explanations added only to prevent hypothetical misunderstanding;
- self-undermining contribution statements;
- unnecessary "not X but Y" structures;
- redundant "however", "nevertheless", or "although" transitions.

Revise any item that weakens the text without improving accuracy.

## Rewrite Procedure

1. Identify the function of the defensive sentence.

Classify it as one of:

- unnecessary disclaimer;
- necessary scope condition;
- real methodological limitation;
- useful conceptual contrast;
- evidence-based qualification;
- redundant clarification.

2. Delete unnecessary disclaimers.

Remove any sentence that does not add evidence, scope, logic, conceptual precision, or necessary reader guidance.

3. Convert defensive limitation into positive scope.

Prefer:

> The analysis focuses on urban governance cases from 2015 to 2023.

Avoid:

> We do not claim that these cases are representative of all urban governance contexts.

4. Replace hedging with precision.

Prefer:

> The evidence indicates that X influences Y in these cases.

Avoid:

> This may suggest that X could potentially influence Y.

If uncertainty is real, specify its source:

> The available evidence supports this interpretation, although the design does not estimate population-level effects.

5. Rebuild the paragraph around the main point.

Ensure the paragraph has:

- a clear topic sentence;
- one main job;
- a logical sequence;
- no repeated caveats;
- no apology-like framing;
- a direct connection to the larger argument.

## Writing Principles

Lead with the claim. Start paragraphs with the point, not with a caveat.

Use positive scope. State what the text examines, explains, tests, compares, or contributes.

Strengthen with evidence, not apology. When a claim feels too broad, improve the concepts, evidence, causal logic, scope, or paragraph structure instead of adding protective caveats.

Keep one paragraph, one job. Do not mix argument, caveat, apology, exception, and clarification in the same paragraph.

Use contrast only when the contrast itself is part of the argument. Avoid reflexive "not X but Y", "rather than", "instead of", "to be clear", and "it should be noted that" structures.

## Preferred Patterns

Use patterns like:

- "This paper examines..."
- "This study shows..."
- "The analysis focuses on..."
- "The evidence indicates..."
- "This design allows..."
- "The results suggest..."
- "The central contribution is..."
- "This section explains..."
- "The argument proceeds in three steps..."
- "In this setting, X shapes Y by..."

## Discouraged Patterns

Avoid these unless they are necessary for accuracy:

- "This paper does not claim..."
- "We do not attempt to..."
- "This is not to say that..."
- "This should not be taken to mean..."
- "The goal is not X but Y..."
- "Rather than arguing X, this paper argues Y..."
- "Although this study has limitations..."
- "Of course, this does not fully capture..."
- "It is worth noting that..."
- "To be clear..."

## Examples

Defensive:

> We do not claim that these cases are representative of all contexts.

Stronger:

> The cases show how the mechanism operates across three institutional settings.

Defensive:

> This paper is not intended to provide a comprehensive theory of platform governance, but rather to examine one specific mechanism.

Stronger:

> This paper identifies a mechanism through which platform governance reshapes participation.

Defensive:

> This does not mean that policy design alone determines implementation outcomes.

Stronger:

> Implementation outcomes depend on how policy design interacts with administrative capacity.

Defensive:

> While the sample is limited and cannot capture every variation, it still offers useful insights.

Stronger:

> The sample captures the variation most relevant to the study's theoretical question.

Defensive:

> We are not arguing that this model is superior in every situation.

Stronger:

> The model is most useful when the task requires interpretable comparisons across cases.

## Final Pass

Before producing the final answer, remove any sentence that exists mainly to protect against a hypothetical objection rather than to advance the text. Deliver text that is concise, direct, confident, logically organized, and free of unnecessary disclaimers.

## Local integration

### Where this runs

`paper-workflow` places this skill at layer 4, the rhetorical-posture layer:

1. structure (`manuscript-optimizer`)
2. prose (`scientific-writing`)
3. passage logic (`write-scientific-manuscript`)
4. **rhetorical posture (this skill)**
5. sentence pass (`scientific-prose-style`), last

Run it after the claim hierarchy is stable. Before that point an unnecessary disclaimer and a real
scope condition are indistinguishable, because the claim they qualify is still moving. Run it before
`scientific-prose-style`, because removing defensive scaffolding rewrites paragraph openers and
sentence boundaries that the punctuation and rhythm pass then has to settle.

### Boundary with the integrity audits

In a scientific manuscript many caveats are mandated rather than defensive. Treat every limitation
placed by `stats-reporting-audit`, `claim-source-verification`, `citation-verifier`,
`data-availability`, or `submission-audit` as load-bearing and leave it in place. The same applies to
any limitation the Methods needs in order to be reproducible: an exact scope, a chance level, a
denominator, an estimator convention, a known non-comparability between two panels.

The edit those cases need is a change of form, not deletion:

- move the limitation out of a high-impact position and into Methods, Discussion, or Limitations;
- state it once instead of restating it at every mention;
- write it as positive scope rather than as a negation of an unmade claim;
- drop the surrounding instruction to the reader and keep the fact.

Worked example, from a Methods section:

Defensive:

> Two consequences follow and should be borne in mind when comparing dsR10 across panels.

Stronger, same information:

> Two properties set the scale of dsR10.

Defensive:

> This component is an operational residual and is not assumed to represent a noise-free biological
> or causal effect. It may contain measurement noise and other unmodelled variation.

Stronger, same information:

> This component is an operational residual under the specified additive decomposition. It aggregates
> context-specific pharmacological variation, residual marginal structure and measurement noise.

### Boundary with `scientific-prose-style`

`scientific-prose-style` owns punctuation, rhythm, the em-dash budget, and hedge calibration at the
sentence level. This skill owns authorial posture at the paragraph level: what a paragraph leads
with, where a caveat sits, and whether a sentence exists to advance the argument or to pre-empt an
objection. They stack, in that order.

### Reporting

Report what was removed and why, and list separately every limitation kept and the reason it is
load-bearing. A defensive-writing pass that silently deletes a mandated caveat is a reporting
failure, not a style improvement.

## Provenance

Adapted from `Kiterlin/anti-defensive-writing` (MIT, https://github.com/Kiterlin/anti-defensive-writing).
The rules, checklist, rewrite procedure, preferred and discouraged patterns, and examples above are
upstream and unmodified. The frontmatter and the **Local integration** section are local additions.
See `LICENSE` and `UPSTREAM.md`.
