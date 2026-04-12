#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path


REF_PATTERN = re.compile(
    r"(?P<kind>Supplementary\s+Fig\.|Fig\.)\s*"
    r"(?P<num>\d+)"
    r"(?P<panels>(?:[a-z](?:[-,][a-z])*)?)",
    re.IGNORECASE,
)


def expand_panels(raw: str) -> list[str]:
    if not raw:
        return []
    parts: list[str] = []
    for chunk in raw.split(","):
        chunk = chunk.strip()
        if "-" in chunk and len(chunk) == 3:
            start, end = chunk.split("-")
            for code in range(ord(start), ord(end) + 1):
                parts.append(chr(code))
        elif chunk:
            parts.append(chunk)
    return parts


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize figure and supplementary-figure references in manuscript text.")
    parser.add_argument("files", nargs="+", help="Text, markdown, or TeX files to scan")
    args = parser.parse_args()

    grouped: dict[str, dict[str, set[str] | int]] = defaultdict(lambda: {"panels": set(), "whole": 0, "mentions": 0})

    for raw in args.files:
        path = Path(raw)
        text = path.read_text(encoding="utf-8", errors="replace")
        for lineno, line in enumerate(text.splitlines(), start=1):
            for match in REF_PATTERN.finditer(line):
                kind = "supp" if "supplementary" in match.group("kind").lower() else "main"
                key = f"{kind}:{match.group('num')}"
                grouped[key]["mentions"] = int(grouped[key]["mentions"]) + 1
                panels = expand_panels(match.group("panels"))
                if panels:
                    cast = grouped[key]["panels"]
                    assert isinstance(cast, set)
                    cast.update(panels)
                else:
                    grouped[key]["whole"] = int(grouped[key]["whole"]) + 1

    for key in sorted(grouped.keys(), key=lambda x: (x.split(":")[0], int(x.split(":")[1]))):
        kind, num = key.split(":")
        prefix = "Supplementary Fig." if kind == "supp" else "Fig."
        panels = sorted(grouped[key]["panels"])
        whole = int(grouped[key]["whole"])
        mentions = int(grouped[key]["mentions"])
        panel_text = ",".join(panels) if panels else "-"
        print(f"{prefix} {num}: mentions={mentions}, whole_figure_refs={whole}, panels={panel_text}")


if __name__ == "__main__":
    main()
