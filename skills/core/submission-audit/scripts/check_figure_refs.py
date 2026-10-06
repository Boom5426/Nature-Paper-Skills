#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path


REF_PATTERN = re.compile(
    r"(?<!\w)(?P<kind>"
    r"Extended\s+Data\s+(?:Figs?\.|Figures?)|"
    r"Supplementary\s+(?:Figs?\.|Figures?)|"
    r"(?:Figs?\.|Figures?)"
    r")\s*(?=\d)",
    re.IGNORECASE,
)
# A bare "a" followed by prose is an article, not a range endpoint.
PANEL_END = r"(?:[b-z]|a(?!\s+(?!and\b)[\w\\]))"
REF_ITEM_PATTERN = re.compile(
    r"(?P<num>\d+)"
    rf"(?P<panels>[a-z](?:\s*[-–]\s*{PANEL_END})?)?"
    r"(?:\s*[-–]\s*(?P<end>\d+))?"
    r"(?=\b|[)\].,;:]|$)",
    re.IGNORECASE,
)
PANEL_PATTERN = re.compile(rf"[a-z](?:\s*[-–]\s*{PANEL_END})?(?=\b|[)\].,;:]|$)", re.I)
SEPARATOR = re.compile(r"(?:\s*,\s*(?:(?:and|&)\s+)?|\s+(?:and|&)\s+)", re.I)


def expand_panels(raw: str) -> list[str]:
    if not raw:
        return []
    raw = re.sub(r"\s+", "", raw.lower()).replace("–", "-")
    parts: list[str] = []
    for chunk in raw.split(","):
        chunk = chunk.strip()
        if "-" in chunk and len(chunk) == 3:
            start, end = chunk.split("-")
            if start > end:
                raise ValueError(f"Descending panel range: {chunk}")
            for code in range(ord(start), ord(end) + 1):
                parts.append(chr(code))
        elif chunk:
            parts.append(chunk)
    return parts


def panel_continuation(text: str, pos: int):
    panel = PANEL_PATTERN.match(text, pos)
    if panel and panel.group().lower() == "a" and re.match(r"\s+(?!and\b)[\w\\]", text[panel.end():], re.I):
        return None
    return panel


def parse_refs(text: str, start: int):
    """Read explicit figures/ranges and panel continuations in one phrase."""
    refs, pos = [], start
    while True:
        item = REF_ITEM_PATTERN.match(text, pos)
        if item:
            num = int(item.group("num"))
            panels = expand_panels(item.group("panels") or "")
            last = int(item.group("end") or num)
            if item.group("end") and panels:
                raise ValueError("Mixed figure/panel range is not supported")
            if last < num or last - num > 1000:
                raise ValueError("Descending or excessively large figure range")
            refs.extend((str(n), list(panels)) for n in range(num, last + 1))
            pos = item.end()
        else:
            panel = panel_continuation(text, pos)
            if not panel or not refs or not refs[-1][1]:
                raise ValueError(f"Cannot parse reference near {text[pos:pos + 24]!r}")
            refs[-1][1].extend(expand_panels(panel.group()))
            pos = panel.end()
        tail = re.match(r"\s*[-–]\s*", text[pos:])
        if tail:
            endpoint = pos + tail.end()
            if endpoint == len(text) or text[endpoint].isdigit() or panel_continuation(text, endpoint):
                raise ValueError(f"Unsupported range near {text[pos:pos + 24]!r}")
        sep = SEPARATOR.match(text, pos)
        if not sep:
            return refs
        following = sep.end()
        if following == len(text):
            return refs
        # A quantity after the reference is prose, not another figure number.
        if re.match(r"\d+(?:\.\d+)?\s*(?:\\?%|(?:percent|mm|cm|nm|mg|kg|ml|hours?|minutes?|seconds?)\b)",
                    text[following:], re.I):
            return refs
        if not text[following].isdigit():
            if not refs[-1][1] or not panel_continuation(text, following):
                return refs  # ordinary prose after the reference
        pos = following


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize figure and supplementary-figure references in manuscript text.")
    parser.add_argument("files", nargs="+", help="Text, markdown, or TeX files to scan")
    args = parser.parse_args()

    grouped: dict[str, dict[str, set[str] | int]] = defaultdict(lambda: {"panels": set(), "whole": 0, "mentions": 0})
    incomplete = False

    for raw in args.files:
        path = Path(raw)
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in REF_PATTERN.finditer(text):
            raw_kind = " ".join(match.group("kind").lower().split())
            kind = "extended" if raw_kind.startswith("extended data") else "supp" if raw_kind.startswith("supplementary") else "main"
            try:
                refs = parse_refs(text, match.end())
            except ValueError as exc:
                lineno = text.count("\n", 0, match.start()) + 1
                print(f"warning: {path}:{lineno}: {exc}; figure scan incomplete", file=sys.stderr)
                incomplete = True
                continue
            for num, panels in refs:
                key = f"{kind}:{num}"
                grouped[key]["mentions"] = int(grouped[key]["mentions"]) + 1
                if panels:
                    cast = grouped[key]["panels"]
                    assert isinstance(cast, set)
                    cast.update(panels)
                else:
                    grouped[key]["whole"] = int(grouped[key]["whole"]) + 1

    if not grouped:
        print("No complete figure references found." if incomplete else "No figure references found.")
        return 1 if incomplete else 0

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
    return 1 if incomplete else 0


if __name__ == "__main__":
    sys.exit(main())
