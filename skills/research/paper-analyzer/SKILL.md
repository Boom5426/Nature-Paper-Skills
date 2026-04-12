---
name: paper-analyzer
description: Use when deeply analyzing a single paper and producing structured notes on claims, methods, figures, evaluation, strengths, limitations, and related work.
---
# Paper Analyzer

## Overview

Perform deep analysis of a specific paper, generating structured notes that cover claims, methodology, experiment evaluation, strengths and limitations, and links to adjacent work.

# Workflow

## Step 1: Identify Paper
Accept input: arXiv ID (e.g., "2402.12345"), full ID ("arXiv:2402.12345"), paper title, or file path.

## Step 2: Fetch Paper Content
```bash
curl -L "https://arxiv.org/pdf/[PAPER_ID]" -o /tmp/paper_analysis/[PAPER_ID].pdf
curl -L "https://arxiv.org/e-print/[PAPER_ID]" -o /tmp/paper_analysis/[PAPER_ID].tar.gz
curl -s "https://arxiv.org/abs/[PAPER_ID]" > /tmp/paper_analysis/arxiv_page.html
```

## Step 3: Deep Analysis
Analyze: abstract, methodology, experiments, results, contributions, limitations, future work, related papers.

## Step 4: Generate Note
```bash
python scripts/generate_note.py --paper-id "$PAPER_ID" --title "$TITLE" --authors "$AUTHORS" --domain "$DOMAIN"
```

## Step 5: Update Knowledge Graph
```bash
python scripts/update_graph.py --paper-id "$PAPER_ID" --title "$TITLE" --domain "$DOMAIN" --score $SCORE
```

# Scripts
- `scripts/generate_note.py` — Generate structured note template
- `scripts/update_graph.py` — Update paper relationship graph

# Note Structure
The generated note includes: core info, abstract (EN/CN), research background, method overview with architecture figures, experiment results with tables, deep analysis, related paper comparison, tech roadmap positioning, future work, and comprehensive evaluation (0-10 scoring).

# Dependencies
- Python 3.8+, PyYAML, requests
- Network access (arXiv)

---
> Based on [evil-read-arxiv](https://github.com/evil-read-arxiv) — an automated paper reading workflow. MIT License.
