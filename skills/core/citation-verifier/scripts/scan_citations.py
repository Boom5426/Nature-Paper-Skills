#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path


PLACEHOLDER_PATTERNS = [
    re.compile(r"\[CITATION NEEDED\]", re.IGNORECASE),
    re.compile(r"PLACEHOLDER_[A-Za-z0-9_:-]+"),
    re.compile(r"TODO[: ]+verify", re.IGNORECASE),
    re.compile(r"FIXME[: ]+citation", re.IGNORECASE),
]

DOI_PATTERN = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b", re.IGNORECASE)
ARXIV_PATTERN = re.compile(r"\barXiv:\s*\d{4}\.\d{4,5}(?:v\d+)?\b|https?://arxiv\.org/(?:abs|pdf)/\d{4}\.\d{4,5}(?:v\d+)?", re.IGNORECASE)
PMID_PATTERN = re.compile(r"\bPMID:\s*\d+\b|\bpmid\s+\d+\b", re.IGNORECASE)
CITE_PATTERN = re.compile(r"\\cite[t|p]?\{([^}]+)\}")
BIB_ENTRY_PATTERN = re.compile(r"@\w+\s*\{\s*([^,\s]+)", re.IGNORECASE)


def iter_paths(paths: list[str]) -> list[Path]:
    collected: list[Path] = []
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            for ext in (".md", ".txt", ".tex", ".bib"):
                collected.extend(sorted(path.rglob(f"*{ext}")))
        elif path.exists():
            collected.append(path)
        else:
            print(f"[warn] missing path: {path}", file=sys.stderr)
    return collected


def scan_text_file(path: Path) -> dict[str, list[tuple[int, str]]]:
    findings: dict[str, list[tuple[int, str]]] = defaultdict(list)
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8", errors="replace")

    for lineno, line in enumerate(text.splitlines(), start=1):
        for pat in PLACEHOLDER_PATTERNS:
            for m in pat.finditer(line):
                findings["placeholders"].append((lineno, m.group(0)))
        for m in DOI_PATTERN.finditer(line):
            findings["dois"].append((lineno, m.group(0)))
        for m in ARXIV_PATTERN.finditer(line):
            findings["arxiv"].append((lineno, m.group(0)))
        for m in PMID_PATTERN.finditer(line):
            findings["pmid"].append((lineno, m.group(0)))
        for m in CITE_PATTERN.finditer(line):
            for key in [part.strip() for part in m.group(1).split(",") if part.strip()]:
                findings["cite_keys"].append((lineno, key))
    return findings


def scan_bib_keys(path: Path) -> tuple[list[tuple[int, str]], list[str]]:
    keys: list[tuple[int, str]] = []
    duplicates: list[str] = []
    seen: dict[str, int] = {}
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8", errors="replace")
    for lineno, line in enumerate(text.splitlines(), start=1):
        match = BIB_ENTRY_PATTERN.search(line)
        if not match:
            continue
        key = match.group(1).strip()
        keys.append((lineno, key))
        if key in seen and key not in duplicates:
            duplicates.append(key)
        seen[key] = seen.get(key, 0) + 1
    return keys, duplicates


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan local manuscript files for citation hygiene issues.")
    parser.add_argument("paths", nargs="+", help="Files or directories to scan")
    args = parser.parse_args()

    paths = iter_paths(args.paths)
    if not paths:
        print("No files found.")
        return

    total_placeholders = 0
    total_dois = 0
    total_arxiv = 0
    total_pmid = 0
    total_cite_keys = 0
    total_bib_keys = 0
    duplicate_keys: dict[str, list[str]] = {}

    for path in paths:
        findings = scan_text_file(path)
        bib_keys: list[tuple[int, str]] = []
        bib_dups: list[str] = []
        if path.suffix.lower() == ".bib":
            bib_keys, bib_dups = scan_bib_keys(path)

        if not any(findings.values()) and not bib_keys and not bib_dups:
            continue

        print(path)
        if findings["placeholders"]:
            total_placeholders += len(findings["placeholders"])
            print("  placeholders:")
            for lineno, token in findings["placeholders"]:
                print(f"    L{lineno}: {token}")
        if findings["cite_keys"]:
            total_cite_keys += len(findings["cite_keys"])
            unique_keys = sorted({key for _, key in findings["cite_keys"]})
            print(f"  cite_keys: {len(unique_keys)} unique / {len(findings['cite_keys'])} total")
        if findings["dois"]:
            total_dois += len(findings["dois"])
            print(f"  dois: {len(findings['dois'])}")
        if findings["arxiv"]:
            total_arxiv += len(findings["arxiv"])
            print(f"  arxiv: {len(findings['arxiv'])}")
        if findings["pmid"]:
            total_pmid += len(findings["pmid"])
            print(f"  pmid: {len(findings['pmid'])}")
        if bib_keys:
            total_bib_keys += len(bib_keys)
            print(f"  bib_keys: {len(bib_keys)}")
        if bib_dups:
            duplicate_keys[str(path)] = bib_dups
            print("  duplicate_bib_keys:")
            for key in bib_dups:
                print(f"    {key}")

    print("\nSummary")
    print(f"  placeholders: {total_placeholders}")
    print(f"  cite_keys: {total_cite_keys}")
    print(f"  dois: {total_dois}")
    print(f"  arxiv: {total_arxiv}")
    print(f"  pmid: {total_pmid}")
    print(f"  bib_keys: {total_bib_keys}")
    print(f"  files_with_duplicate_bib_keys: {len(duplicate_keys)}")


if __name__ == "__main__":
    main()
