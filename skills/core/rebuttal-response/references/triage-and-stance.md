# Triage and Stance

Use this file before drafting, to decide what a comment actually is and what stance the reply
should take. Claim calibration comes after this decision, not before it.

This is the triage and stance layer of `rebuttal-response`. Read it before drafting; claim
calibration in `SKILL.md` applies to the stance chosen here, it does not substitute for choosing one.

## Contents

1. Ordering rule
2. Triage by cause
3. Severity and readiness
4. Comment taxonomy
5. Outcome commitment
6. When to concede
7. When to clarify without new work
8. When to push back
9. Editor-efficiency rule
10. Writing rules
11. Tone rules
12. Failure modes
13. Output standard

## 1. Ordering rule

Revise the manuscript first when the reply depends on a real change. Then write the reply against
the updated manuscript, never against the old draft. A letter drafted before the edits exist will
describe changes that were never made and will quote text that does not appear.

## 2. Triage by cause

Classify each comment by why the reviewer raised it. This is a different axis from the domain
taxonomy (editorial, statistical, ethics, and so on) and it determines the stance:

- **misunderstanding.** The paper already answers the point, but the answer was not findable.
- **clarity problem.** The claim is defensible, but wording or organization caused confusion.
- **evidence gap.** The requested support is genuinely missing or too weak.
- **scope mismatch.** The request is reasonable in general but outside the paper's contribution
  or the revision budget.
- **incorrect premise.** The comment rests on a factual or interpretive error.
- **high-risk criticism.** The comment attacks novelty, validity, leakage, controls, statistics,
  or an overclaim. Treat these first and never draft around them.

Triage every comment before deciding any action. Do not let the easiest action drive the diagnosis.

## 3. Severity and readiness

Assign each comment a severity:

- `minor`: presentation, clarity, formatting, citation, or small method-detail issue.
- `major`: evidence, validation, method, statistics, interpretation, or scope issue that may affect
  editorial confidence.
- `blocking`: ethics, compliance, data integrity, or an unsupported central claim. Do not draft
  around these.
- `unclear`: insufficient information to judge severity safely.

Label the package honestly at the end, and never label it `ready_to_submit` while any item is not:

- `ready_to_submit`
- `draft_with_placeholders`
- `needs_author_input`
- `blocked`

## 4. Comment taxonomy

Triage by cause answers why the reviewer raised the point. This second axis answers what domain it
belongs to, and it selects the response action:

- editorial or presentation
- evidence or interpretation
- methodological
- statistical
- data, code, or materials
- citation or positioning
- scope or feasibility
- ethics or compliance

Editorial issues usually need text or figure clarification. Evidence and statistics issues often
need new support, a softened claim, or explicit limitation language. Ethics and compliance issues
are usually `blocking` until the missing facts exist.

## 5. Outcome commitment

Every comment must end in exactly one of these:

- clarified in the response only;
- revised in the manuscript;
- revised in both manuscript and response;
- respectfully declined with a stated boundary.

Do not leave a comment in the middle ground where the reply sounds cooperative but the action
taken is unclear. If a claim was softened, say that it was softened.

## 6. When to concede

Concede when the reviewer correctly identifies an evidence gap, a claim stronger than the data,
wording that invited a reasonable misreading, or a missing control, comparison, or limitation.

Best move: narrow the claim to what the data support, add the missing evidence when feasible, and
state the limitation explicitly. Conceding a claim boundary is cheaper than defending an
indefensible one through two more review rounds.

## 7. When to clarify without new work

Clarify when the result already exists but was buried, when the reviewer missed a definition,
setup, or metric, or when reorganization and cross-references resolve the point.

Best move: revise the manuscript for discoverability, then point to the revised location. Do not
imply that a scientific flaw was fixed when the issue was presentation. That misrepresentation is
easy for a reviewer to check and expensive to lose.

## 8. When to push back

Push back only when the request rests on a false premise, falls outside the paper's stated scope,
would require a different study rather than a fair revision, or is already answered by evidence in
the manuscript.

Best move: acknowledge the concern as reasonable, state the disagreement narrowly, give the
study-design or scope reason, and point to the existing evidence. Do not lead with time, funding,
or convenience. Do not write that the reviewer misunderstood; treat a misunderstanding as a
presentation signal and fix the text.

Pushing back and calibrating claims are different moves. If the evidence does not reach the claim,
narrow the claim; do not argue the reviewer out of a correct objection.

## 9. Editor-efficiency rule

Assume the editor scans for three things: whether you agree, what concrete revision was made, and
where to find it. State all three in the first two sentences of each reply.

## 10. Writing rules

- Quote or paraphrase each reviewer point fairly before responding.
- State the action taken in the first one or two sentences of the reply.
- State explicitly whether you agree, partially agree, or disagree when the action alone does not
  make that obvious.
- Distinguish what was changed, what was clarified, and what was not changed and why.
- If new text, analysis, or figures were added, say exactly where.
- Give page and line numbers whenever the manuscript format allows it.
- If figure, table, or supplement numbering changed, cite the updated identifiers.
- If a claim was softened, say so explicitly rather than letting the reviewer discover it.
- If a request cannot be fully satisfied, state the scope boundary and give the strongest honest
  response available.
- If the journal expects marked revisions, make sure changed text is visibly highlighted.

## 11. Tone rules

Prefer respectful, direct, specific, non-defensive, evidence-led prose.

Avoid over-thanking, vague promises, evasive wording, answering criticism with hype, and claiming a
concern is addressed when only the wording changed.

## 12. Failure modes

- Writing the letter before deciding the manuscript edits.
- Thanking the reviewer and never stating the action.
- `Revised accordingly` without saying what changed.
- Claiming a concern is addressed without citing the revised location.
- Agreeing with two contradictory reviewer requests without resolving the conflict.
- Declining a request without defining the scope boundary.
- Using soft language to hide that the paper needed a claim downgrade.

## 13. Output standard

When this skill runs, produce:

- a triaged comment map with severity per item;
- the action chosen for each comment;
- the revised response text;
- the linked manuscript change locations;
- any unresolved issue that still needs author judgement;
- a final readiness label from section 3.
