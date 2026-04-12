---
name: rebuttal-response
description: Use when responding to journal or conference reviewer comments and you need a structured author response, aligned manuscript edits, and clear decisions about when to clarify, add evidence, concede, or respectfully disagree.
---

# Rebuttal Response

## Overview

Use this skill when reviewer comments already exist and the task is no longer generic manuscript revision. The goal is to produce a response package that is credible, efficient, and easy for editors or reviewers to verify.

This skill is not for redesigning the whole paper. Use `manuscript-optimizer` first if the manuscript itself is structurally unstable. Use this skill when the paper is in revision mode and each comment must be turned into an explicit response and, where needed, a concrete manuscript change.

## When To Use

Use this skill when:
- Reviewer comments, decision letters, or revision requests are available
- The user needs a point-by-point response letter
- The manuscript and response document need to stay synchronized
- Some comments should lead to new analyses or text changes, while others should be answered by clarification
- The revision requires deciding where to concede and where to push back

Do not use this skill for:
- Initial manuscript drafting
- Submission-preflight QA before any reviewer feedback exists
- Generic peer review written from the reviewer side

## Response Principle

Every reviewer comment should end in exactly one of these outcomes:
- clarified in response only
- revised in the manuscript
- revised in both manuscript and response
- respectfully declined with justification

Do not leave a comment in the vague middle ground where the reply sounds polite but the action taken is unclear.

## Triage Categories

Classify each comment before writing:

- misunderstanding
  The paper may already contain the answer, but it was not easy enough to find.
- clarity problem
  The intended claim is defensible, but the wording or organization caused confusion.
- evidence gap
  The reviewer is asking for support that is genuinely missing or too weak.
- scope mismatch
  The request is reasonable in general but outside the paper's actual contribution or revision budget.
- incorrect premise
  The reviewer comment is based on a factual or interpretive error.
- high-risk criticism
  The comment challenges novelty, validity, leakage, controls, statistics, or overclaim.

Triage first. Only then decide what to change.

## Response Order

1. Parse all reviewer comments into atomic items.
2. Mark each item by triage category.
3. Decide the action:
   - clarify
   - edit text
   - add analysis
   - add experiment
   - narrow claim
   - decline with justification
4. Update the manuscript first when the response depends on a real change.
5. Write the response letter against the updated manuscript, not against the old draft.
6. Cite exact revised locations whenever possible:
   - section
   - figure
   - table
   - line or paragraph location if available
7. End with a short revision summary for the editor if the venue expects one.

## Decision Rules

### When To Concede

Concede when:
- the reviewer correctly identifies an evidence gap
- a claim is stronger than the data
- wording created a reasonable misunderstanding
- a control, comparison, or limitation statement is missing

Best move:
- narrow the claim
- add the missing evidence if feasible
- explicitly thank the reviewer for improving precision

### When To Clarify Without Major New Work

Use clarification when:
- the result already exists but was buried
- the reviewer missed a definition, setup, or metric explanation
- the requested point can be handled by reorganizing text or adding cross-references

Best move:
- revise the manuscript for discoverability
- do not imply that a major scientific flaw was fixed if the issue was presentation

### When To Push Back

Push back only when:
- the request depends on a false premise
- the requested experiment is outside the paper's stated scope
- the request would require a different paper rather than a fair revision
- the current evidence already answers the concern

Best move:
- acknowledge the concern as reasonable
- explain the boundary precisely
- point to the evidence already in the manuscript
- avoid defensive tone or rhetorical overreach

## Writing Rules

- Quote or paraphrase each reviewer point fairly before responding.
- Start with appreciation, then move quickly to substance.
- State the action taken in the first 1-2 sentences of the reply.
- Distinguish clearly between:
  - what was changed
  - what was clarified
  - what was not changed and why
- If new text, analysis, or figures were added, say exactly where.
- If a claim was softened, say so explicitly.
- If a request cannot be fully satisfied, explain the scope boundary and give the strongest honest response available.

## Tone Rules

Prefer:
- respectful
- direct
- specific
- non-defensive
- evidence-led

Avoid:
- over-thanking
- vague promises
- evasive wording
- replying to criticism with hype
- claiming to have addressed a concern when only wording changed

## Common Failure Modes

- Writing the response letter before deciding the manuscript edits
- Thanking the reviewer but never stating the action taken
- Claiming a concern is addressed without citing the revised location
- Agreeing with contradictory reviewer requests without resolving the conflict
- Refusing a request without clearly defining the scope boundary
- Using soft language to hide that the paper actually needed a claim downgrade

## Output Standard

When using this skill, produce:
- a triaged reviewer-comment map
- the action chosen for each comment
- the revised response text
- the linked manuscript change locations
- any remaining unresolved issues that still need user judgment
