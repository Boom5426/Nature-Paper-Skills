#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
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


def check_layout(root: Path) -> None:
    """Check all entries before creating anything, including implicit parents."""
    if root.exists() and not root.is_dir():
        raise ValueError(f"Project root is not a directory: {root}")
    for parent in root.parents:
        if parent.exists() and not parent.is_dir():
            raise ValueError(f"Project root parent is not a directory: {parent}")
    for rel in [*DEFAULT_DIRS, *DEFAULT_FILES]:
        target = root / rel
        for path in [target, *target.parents]:
            if path == root:
                break
            if path.is_symlink():
                raise ValueError(f"Refusing linked project entry: {path}; inspect or repair it first")
            if path.exists():
                directory = path != target or rel in DEFAULT_DIRS
                if not (path.is_dir() if directory else path.is_file()):
                    expected = "directory" if directory else "file"
                    raise ValueError(f"Expected a {expected}: {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a minimal paper-project directory layout.")
    parser.add_argument("root", help="Paper project root")
    parser.add_argument("--dry-run", action="store_true", help="Report planned changes without creating directories")
    args = parser.parse_args()

    try:
        root = Path(args.root).expanduser().resolve()
        check_layout(root)
    except (ValueError, OSError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
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
            # Exclusive creation also protects files/links appearing after preflight.
            with target.open("x", encoding="utf-8") as handle:
                handle.write(content)

    print("created:")
    for path in created:
        print(f"  {path}")
    print("reused:")
    for path in reused:
        print(f"  {path}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(2)
