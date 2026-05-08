#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path


REF_PATTERN = re.compile(
    r"(?P<kind>Extended\s+Data\s+Fig\.|Supplementary\s+Fig\.|Fig\.)\s*"
    r"(?P<num>\d+)"
    r"(?P<panels>(?:[a-z](?:[-,][a-z])*)?)"
    r"(?=\b|[)\].,;:])",
    re.IGNORECASE,
)


def expand_panels(raw: str) -> list[str]:
    if not raw:
        return []
    raw = raw.strip()
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
        for line in text.splitlines():
            for match in REF_PATTERN.finditer(line):
                raw_kind = match.group("kind").lower()
                if "extended data" in raw_kind:
                    kind = "extended"
                elif "supplementary" in raw_kind:
                    kind = "supp"
                else:
                    kind = "main"
                key = f"{kind}:{match.group('num')}"
                grouped[key]["mentions"] = int(grouped[key]["mentions"]) + 1
                panels = expand_panels(match.group("panels"))
                if panels:
                    cast = grouped[key]["panels"]
                    assert isinstance(cast, set)
                    cast.update(panels)
                else:
                    grouped[key]["whole"] = int(grouped[key]["whole"]) + 1

    if not grouped:
        print("No figure references found.")
        return

    order = {"main": 0, "extended": 1, "supp": 2}
    labels = {
        "main": "Fig.",
        "extended": "Extended Data Fig.",
        "supp": "Supplementary Fig.",
    }

    for key in sorted(grouped.keys(), key=lambda x: (order[x.split(":")[0]], int(x.split(":")[1]))):
        kind, num = key.split(":")
        prefix = labels[kind]
        panels = sorted(grouped[key]["panels"])
        whole = int(grouped[key]["whole"])
        mentions = int(grouped[key]["mentions"])
        panel_text = ",".join(panels) if panels else "-"
        print(f"{prefix} {num}: mentions={mentions}, whole_figure_refs={whole}, panels={panel_text}")


if __name__ == "__main__":
    main()
