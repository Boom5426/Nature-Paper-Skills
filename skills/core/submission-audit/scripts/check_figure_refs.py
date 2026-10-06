#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path


FIGURE_TOKEN = r"\d+(?:[a-z](?:[-–,][a-z])*)?"
REF_PATTERN = re.compile(
    r"(?P<kind>"
    r"Extended\s+Data\s+(?:Figs?\.|Figures?)|"
    r"Supplementary\s+(?:Figs?\.|Figures?)|"
    r"(?:Figs?\.|Figures?)"
    r")\s*"
    rf"(?P<refs>{FIGURE_TOKEN}"
    rf"(?:(?:\s*,\s*(?:and\s+)?|\s+(?:and|&)\s+){FIGURE_TOKEN})*)"
    r"(?=\b|[)\].,;:])",
    re.IGNORECASE,
)
REF_ITEM_PATTERN = re.compile(
    r"(?P<num>\d+)"
    r"(?P<panels>(?:[a-z](?:[-–,][a-z])*)?)"
    r"(?=\b|[)\].,;:]|\s)",
    re.IGNORECASE,
)


def expand_panels(raw: str) -> list[str]:
    if not raw:
        return []
    raw = raw.strip().replace("–", "-")
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
                for item in REF_ITEM_PATTERN.finditer(match.group("refs")):
                    key = f"{kind}:{item.group('num')}"
                    grouped[key]["mentions"] = int(grouped[key]["mentions"]) + 1
                    panels = expand_panels(item.group("panels"))
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
