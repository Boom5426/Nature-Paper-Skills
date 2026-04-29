---
name: paper-reviewer
description: Use when acting as a journal or grant reviewer and writing formal reviewer-side evaluations focused on methodology, statistics, reporting standards, reproducibility, and constructive feedback.
---

# Scientific Critical Evaluation and Peer Review

## Overview

Peer review is a systematic process for evaluating scientific manuscripts. Assess methodology, statistics, design, reproducibility, ethics, and reporting standards. Apply this skill for manuscript and grant review across disciplines with constructive, rigorous evaluation.

## When to Use This Skill

This skill should be used when:
- Conducting peer review of scientific manuscripts for journals
- Evaluating grant proposals and research applications
- Assessing methodology and experimental design rigor
- Reviewing statistical analyses and reporting standards
- Evaluating reproducibility and data availability
- Checking compliance with reporting guidelines (CONSORT, STROBE, PRISMA)
- Providing constructive feedback on scientific writing

## Visual Enhancement with Scientific Figures

**When creating documents with this skill, consider adding diagrams when they clarify a workflow, architecture, or evaluation framework.**

If the document does not already contain suitable figures:
- Use an installed figure-generation skill such as `inno-figure-gen` to generate publication-style diagrams.
- Describe the desired figure in natural language and specify academic style constraints.
- Iterate prompts until the figure is clear, readable, and suitable for review materials.

**Example command:**
```bash
uv run ~/.codex/skills/inno-figure-gen/scripts/generate_image.py \
  --prompt "Publication-style diagram of the review workflow; white background; clean labels; colorblind-friendly palette; high contrast" \
  --filename "figures/review-workflow.png" \
  --resolution 2K
```

If you are in Claude Code, replace `~/.codex/skills` with `~/.claude/skills`. Requires `GEMINI_API_KEY` or an explicit `--api-key`.

**When to add figures:**
- Peer review workflow diagrams
- Evaluation criteria decision trees
- Review process flowcharts
- Methodology assessment frameworks
- Quality assessment visualizations
- Reporting guidelines compliance diagrams
- Any complex concept that benefits from visualization

For detailed guidance on creating figures, refer to the figure-generation skill you have installed.

---

## Peer Review Workflow

Conduct peer review systematically through the following stages, adapting depth and focus based on the manuscript type and discipline.

### Stage 1: Initial Assessment

Begin with a high-level evaluation to determine the manuscript's scope, novelty, and overall quality.

**Key Questions:**
- What is the central research question or hypothesis?
- What are the main findings and conclusions?
- Is the work scientifically sound and significant?
- Is the work appropriate for the intended venue?
- Are there any immediate major flaws that would preclude publication?

**Output:** Brief summary (2-3 sentences) capturing the manuscript's essence and initial impression.

### Stage 2: Detailed Section-by-Section Review

Conduct a thorough evaluation of each manuscript section, documenting specific concerns and strengths.

#### Abstract and Title
- **Accuracy:** Does the abstract accurately reflect the study's content and conclusions?
- **Clarity:** Is the title specific, accurate, and informative?
- **Completeness:** Are key findings and methods summarized appropriately?
- **Accessibility:** Is the abstract comprehensible to a broad scientific audience?

#### Introduction
- **Context:** Is the background information adequate and current?
- **Rationale:** Is the research question clearly motivated and justified?
- **Novelty:** Is the work's originality and significance clearly articulated?
- **Literature:** Are relevant prior studies appropriately cited?
- **Objectives:** Are research aims/hypotheses clearly stated?

#### Methods
- **Reproducibility:** Can another researcher replicate the study from the description provided?
- **Rigor:** Are the methods appropriate for addressing the research questions?
- **Detail:** Are protocols, reagents, equipment, and parameters sufficiently described?
- **Ethics:** Are ethical approvals, consent, and data handling properly documented?
- **Statistics:** Are statistical methods appropriate, clearly described, and justified?
- **Validation:** Are controls, replicates, and validation approaches adequate?

**Critical elements to verify:**
- Sample sizes and power calculations
- Randomization and blinding procedures
- Inclusion/exclusion criteria
- Data collection protocols
- Computational methods and software versions
- Statistical tests and correction for multiple comparisons

#### Results
- **Presentation:** Are results presented logically and clearly?
- **Figures/Tables:** Are visualizations appropriate, clear, and properly labeled?
- **Statistics:** Are statistical results properly reported (effect sizes, confidence intervals, p-values)?
- **Objectivity:** Are results presented without over-interpretation?
- **Completeness:** Are all relevant results included, including negative results?
- **Reproducibility:** Are raw data or summary statistics provided?

**Common issues to identify:**
- Selective reporting of results
- Inappropriate statistical tests
- Missing error bars or measures of variability
- Over-fitting or circular analysis
- Batch effects or confounding variables
- Missing controls or validation experiments

#### Discussion
- **Interpretation:** Are conclusions supported by the data?
- **Limitations:** Are study limitations acknowledged and discussed?
- **Context:** Are findings placed appropriately within existing literature?
- **Speculation:** Is speculation clearly distinguished from data-supported conclusions?
- **Significance:** Are implications and importance clearly articulated?
- **Future directions:** Are next steps or unanswered questions discussed?

**Red flags:**
- Overstated conclusions
- Ignoring contradictory evidence
- Causal claims from correlational data
- Inadequate discussion of limitations
- Mechanistic claims without mechanistic evidence

#### References
- **Completeness:** Are key relevant papers cited?
- **Currency:** Are recent important studies included?
- **Balance:** Are contrary viewpoints appropriately cited?
- **Accuracy:** Are citations accurate and appropriate?
- **Self-citation:** Is there excessive or inappropriate self-citation?
