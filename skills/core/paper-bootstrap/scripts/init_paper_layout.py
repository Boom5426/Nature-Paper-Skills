#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


DEFAULT_DIRS = [
    "input",
    "notes",
    "figures",
    "output/doc",
    "output/review",
]

DEFAULT_FILES = {
    "notes/project_truth.md": """# Project Truth

## Core Story
- Central claim:
- Venue target:
- Article type:
- Dominant contribution:
- Active manuscript:

## Stable Constraints
- 

## Active Evidence Anchors
- 

## Open Risks
- 
""",
    "notes/decision_log.md": """# Decision Log

## Entry Template
- Date:
- Decision:
- Reason:
- Impact on manuscript or experiments:
""",
    "notes/result_summary.md": """# Result Summary

## Locked Findings
- Claim:
  - Evidence:
  - Figure or table:
  - Status:

## Directional Or Weak Findings
- 

## Open Evidence Gaps
- 
""",
    "notes/paper_handoff.md": """# Paper Handoff

## Ready To Draft
- Section or figure:
  - Input artifact:
  - Main takeaway:

## Still Blocked
- 

## Next Writing Step
- 
""",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize a minimal paper-project directory layout.")
    parser.add_argument("root", help="Paper project root")
    parser.add_argument("--dry-run", action="store_true", help="Report planned changes without creating directories")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    print(f"root: {root}")
    created = []
    reused = []

    for rel in DEFAULT_DIRS:
        target = root / rel
        if target.exists():
            reused.append(str(target))
            continue
        created.append(str(target))
        if not args.dry_run:
            target.mkdir(parents=True, exist_ok=True)

    for rel, content in DEFAULT_FILES.items():
        target = root / rel
        if target.exists():
            reused.append(str(target))
            continue
        created.append(str(target))
        if not args.dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)

    print("created:")
    for path in created:
        print(f"  {path}")
    print("reused:")
    for path in reused:
        print(f"  {path}")


if __name__ == "__main__":
    main()
