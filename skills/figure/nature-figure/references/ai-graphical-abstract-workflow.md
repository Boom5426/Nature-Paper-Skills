# AI-Assisted Graphical Abstract Workflow

Use this reference whenever a task involves planning, generating, revising, or
auditing a graphical abstract with AI assistance. Apply it before any
provider-specific image-generation instructions.

## Contents

- [Authority boundary and policy gate](#authority-boundary-and-policy-gate)
- [1. Define the communication target](#1-define-the-communication-target)
- [2. Build a visual brief](#2-build-a-visual-brief)
- [3. Assign AI a bounded role](#3-assign-ai-a-bounded-role)
- [4. Write the prompt as a figure contract](#4-write-the-prompt-as-a-figure-contract)
- [5. Run human scientific and publication QA](#5-run-human-scientific-and-publication-qa)
- [Sources and status](#sources-and-status)

## Authority boundary and policy gate

- **`references/figure-delivery-bundle.md` is this skill's single source of
  truth on whether AI-generated imagery may ship.** Read its "AI-generated
  imagery" section before generating anything intended for a manuscript, and do
  not derive a different answer from this file. In particular, this file takes
  no position of its own on Nature Portfolio artwork: the delivery bundle states
  it, and where the two could be read differently, the delivery bundle wins.
- Treat Ananya Thakur's 22 July 2026 *Nature* Careers column as practitioner
  guidance, not as a submission policy or a blanket permission to publish
  AI-generated artwork.
- Before generating a submission candidate, verify the target journal's current
  graphical-abstract, artificial-intelligence, image-integrity, copyright, and
  disclosure rules on official pages. Record the journal, URL, and access date.
  A journal may be stricter than the venue you assumed.
- If journal clearance is unknown, label the output **internal design draft,
  submission eligibility unverified**. Do not call it submission-ready, and do
  not let an unlabelled draft reach the delivery bundle.
- Keep two decisions strictly separate: whether a draft is useful internally,
  and whether the final asset is eligible for submission. The first never
  implies the second.

## 1. Define the communication target

Before choosing a tool or visual style, write down:

1. the single sentence the reader should remember
2. the figure type: mechanism, process, experimental setup, workflow,
   comparison, timeline, cycle, or branching decision
3. the intended audience and its expected vocabulary
4. the evidence boundary: what the study demonstrates, what is contextual, and
   what must not be implied
5. the details to omit because they do not support the central message

Do not ask an image model to summarize an entire manuscript into a final image
without this brief.

## 2. Build a visual brief

- Inspect graphical abstracts from comparable papers for information density,
  reading order, and composition. Learn the visual grammar; do not copy
  protected artwork, icons, or distinctive layouts.
- Choose an explicit reading path: left-to-right, top-to-bottom, cycle, split
  comparison, or fork. Use arrows and grouping only when they clarify that path.
- Use a limited, consistent, high-contrast, color-accessible palette. Assign
  color by scientific meaning, not decoration, and do not rely on color alone.
- Reserve the strongest accent for the central causal step or principal result.
  Keep labels short and plan their placement before generating artwork.
- Prefer one representative pathway over an exhaustive interaction network when
  the fuller network would obscure the central claim. Preserve necessary caveats
  in the legend or manuscript.

## 3. Assign AI a bounded role

Use AI to assist with tasks such as:

- distilling author-provided claims into candidate one-sentence messages
- comparing audience-specific levels of terminology and detail
- proposing several compositions or label placements
- checking palette contrast and color accessibility
- turning an author-owned sketch into a draft layout or vectorization plan
- brainstorming pictorial metaphors that will be scientifically reviewed

The prohibitions on invented measurements, mechanisms, effects, citations and
labels, and on sending confidential material to an image service, are stated in
`references/openrouter-image-generation.md` under "Safety and scientific
integrity". They apply to every provider, not only that route.

## 4. Write the prompt as a figure contract

`references/openrouter-image-generation.md` carries the prompt-field list for the
provider route (claim, entities, mechanism, layout, aspect ratio, required
labels, exclusions). Add these three fields, which that list does not have and
which come from the brief above:

- **Evidence boundary and forbidden implications**: what the study demonstrates,
  what is only context, and what the image must not imply
- **Audience**: the vocabulary level the labels are pitched at
- **Output role**: state `concept draft` explicitly whenever generative AI made
  any part of the image

Generate layout alternatives before polishing a single composition. Correct
scientific structure first, then typography, color, and visual finish. Redraw
critical text, arrows, chemical structures, and quantitative marks with
deterministic or editable tools whenever possible.

## 5. Run human scientific and publication QA

Before delivery, check every visual element against the manuscript and source
data:

- scientific entities, directions, causal links, scale, anatomy, and chronology
- all labels, abbreviations, spelling, units, and symbol definitions
- absence of invented data, unsupported effects, misleading realism, or
  decorative evidence
- readable hierarchy at final size and a color-blindness-safe reading path
- originality, licenses, permissions, attribution, and resemblance to source art
- target-journal eligibility, disclosure wording, and figure-legend treatment

Keep the prompt and generation metadata under version control and the generated
image files out of it, as `references/figure-delivery-bundle.md` requires. Beyond
what that file lists, retain the reference-image rights, the generated
candidates, the selected output, and a log of manual corrections. Human authors
remain accountable for the final asset.

## Sources and status

- Practitioner workflow: Ananya Thakur, “How to use AI to make a graphical
  abstract in minutes,” *Nature* Careers, 22 July 2026,
  <https://doi.org/10.1038/d41586-026-02072-9>.
- Governing policy for whether AI-generated artwork may ship:
  `references/figure-delivery-bundle.md`. Do not restate a policy position here.
- Publisher page to recheck at submission time, with the journal's own author
  guide: Nature Portfolio, “Artificial Intelligence (AI),”
  <https://www.nature.com/nature-portfolio/editorial-policies/ai>. The upstream
  access date was 15 August 2026 and has not been re-checked in this repository;
  the policy is reviewed periodically, so read it again and record the date.
