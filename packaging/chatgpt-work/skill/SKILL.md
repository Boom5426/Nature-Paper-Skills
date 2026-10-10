---
name: nature-paper-workflow
description: >-
  Revise scientific manuscripts or a single section such as the Abstract,
  Introduction or Discussion, make a technical draft readable for scientists
  outside the field, improve Results and Review article structure,
  audit submission evidence, or prepare responses to reviewers. Use for
  优化论文、润色论文、改摘要、写引言、面向大同行、去 AI 味、投稿前检查 and 审稿回复. Apply the bundled Nature Paper
  Skills workflows to the draft and evidence supplied by the user.
---

# Nature Paper Workflow

This is a self-contained entry for the bundled Nature Paper Skills resources.
Explicit user instructions, the requested edit scope and the target venue take
precedence over the bundled defaults.

For a general manuscript request, read
[paper-workflow](resources/paper-workflow/SKILL.md) and use its diagnosis, routing
and output contract. For a named specialist task, load that specialist directly
from the [bundled skill index](references/bundled-skills.md).

When the dispatcher or a specialist calls for another skill, read
`resources/<skill-name>/SKILL.md` from this package and apply its instructions.
These are bundled resources; they do not need separate entries in the @ menu.
Resolve each specialist's relative references, scripts, templates and assets
from that specialist's own directory. When a specialist points to another skill's
reference file, such as `paper-workflow`'s `references/section-contracts.md`, read it
from `resources/<skill-name>/`. Read only the resources needed for the task.

The index records the specialists included in this build. Local installer flags
mentioned by a specialist describe the standalone distribution. If a needed
specialist is absent from this bundle, use the available instructions and identify
the additional resource needed for the affected step.

Use the tools available in the current Work session. Run a packaged helper only
when its interpreter and dependencies are available. Preserve measurements,
citations and protected text; report missing evidence or unavailable operations
without presenting them as completed. Deliver the requested revision or findings
using the original workflow's output contract.
