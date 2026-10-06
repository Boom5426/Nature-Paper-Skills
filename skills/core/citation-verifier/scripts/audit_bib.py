#!/usr/bin/env python3
"""Offline bibliography audit for a hand-maintained BibTeX file.

    audit_bib.py --bib refs.bib --tex main.tex --tex 'sections/*.tex'
    audit_bib.py --bib refs.bib --tex 'src/**/*.tex' --author-share 0.10
    audit_bib.py --bib refs.bib                       # skip cited-vs-defined

Pure stdlib, no network. This script never resolves a DOI and never contacts
CrossRef. It checks internal consistency and surfaces the things that need a
human, which is more honest than a tool that appears to have verified them.

Checks
  1. duplicate citation keys
  2. the same work under different keys (the "[4] and [19] are one paper" case)
  3. required fields missing, by entry type
  3b. standards entries carrying no edition year, reported as advisory
  4. DOI syntax, plus the list of DOIs still needing external verification
  5. keys cited in .tex but absent from .bib, and entries never cited
  6. entries carrying a % VERIFY comment
  7. author concentration

Exit status is 1 if any BLOCKING problem is found, else 0. Items that merely
need human verification are reported but do not fail the build, because they
cannot be resolved offline.

This checks bibliography hygiene only. Whether a source actually supports the
claim made of it is a different and larger problem; see the
claim-source-verification skill.
"""

from __future__ import annotations

import argparse
import glob
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from citation_syntax import iter_citations

# Fields insisted on before a reference is allowed to ship, per entry type.
#
# A field given as a tuple is satisfied by ANY member, which is how edited
# volumes pass with `editor` instead of `author`.
#
# Note what @manual does NOT require: `year`. For a standard, the edition year
# is precisely the thing that has to be looked up in the issuing body's
# catalogue. Making `year` mandatory here would push authors to invent one to
# get a green run, which is the opposite of the point. Missing edition years
# are counted separately below as an advisory.
REQUIRED = {
    "article": ["author", "title", "journal", "year"],
    "inproceedings": ["author", "title", "booktitle", "year"],
    "book": [("author", "editor"), "title", "publisher", "year"],
    "incollection": [("author", "editor"), "title", "booktitle", "publisher", "year"],
    "techreport": ["author", "title", "institution", "year"],
    "phdthesis": ["author", "title", "school", "year"],
    "mastersthesis": ["author", "title", "school", "year"],
    "manual": ["title", ("organization", "author")],
    "misc": ["title"],
}

# Entry types whose edition year is legitimately absent until someone reads it
# off the issuing catalogue.
UNDATED_OK = {"manual"}

DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$")

# Not a journal rule and not a universal constant. A project-level default,
# reported as advisory. Override with --author-share.
DEFAULT_AUTHOR_SHARE = 0.15


def read(path: Path) -> str:
    """Read a source file, naming it if the encoding is not UTF-8."""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        print(f"  warning: {path} is not valid UTF-8; undecodable bytes replaced",
              file=sys.stderr)
        return path.read_text(encoding="utf-8", errors="replace")


def strip_comments(text: str) -> str:
    """Remove whole-line % comments but keep them retrievable elsewhere."""
    return "\n".join(l for l in text.splitlines() if not l.lstrip().startswith("%"))


def braced_end(text: str, start: int, label: str) -> int:
    """Find a complete brace group, respecting escaped braces."""
    depth, i = 1, start + 1
    while i < len(text):
        if text[i] == "\\":
            i += 2
            continue
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if not depth:
                return i + 1
        i += 1
    raise ValueError(f"Unclosed braces in {label}")


def parse_fields(body: str, key: str) -> dict[str, str]:
    """Accept braced/quoted values and numbers; reject unresolved expressions."""
    fields, pos = {}, 0
    while pos < len(body):
        while pos < len(body) and body[pos].isspace():
            pos += 1
        if pos == len(body):
            break
        match = re.match(r"([\w-]+)\s*=\s*", body[pos:])
        if not match:
            raise ValueError(f"Cannot parse field in {key}: {body[pos:pos + 40]!r}")
        name = match.group(1).lower()
        pos += match.end()
        if pos == len(body):
            raise ValueError(f"Missing value for {key}.{name}")
        start = pos
        if body[pos] == "{":
            pos = braced_end(body, pos, f"{key}.{name}")
            value = body[start + 1:pos - 1]
        elif body[pos] == '"':
            pos += 1
            depth = 0
            while pos < len(body):
                char = body[pos]
                if char == "\\":
                    pos += 2
                    continue
                if char == "{":
                    depth += 1
                elif char == "}":
                    depth -= 1
                elif char == '"' and not depth:
                    break
                pos += 1
            if pos >= len(body) or depth:
                raise ValueError(f"Unclosed quoted value in {key}.{name}")
            value = body[start + 1:pos]
            pos += 1
        else:
            number = re.match(r"\d+", body[pos:])
            if not number:
                raise ValueError(f"Unsupported value in {key}.{name}; use braces or quotes (string macros are not expanded)")
            value = number.group()
            pos += number.end()
        if name in fields:
            raise ValueError(f"Duplicate field {key}.{name}")
        fields[name] = " ".join(value.split())
        while pos < len(body) and body[pos].isspace():
            pos += 1
        if pos < len(body):
            if body[pos] != ",":
                raise ValueError(f"Expected a comma after {key}.{name}; concatenated values are not supported")
            pos += 1
    return fields


def parse_entries(raw: str):
    """Read brace-delimited entries; malformed/unsupported syntax fails loudly."""
    entries, pos = [], 0
    pattern = re.compile(r"@(\w+)\s*([({])")
    while match := pattern.search(raw, pos):
        etype = match.group(1).lower()
        if match.group(2) != "{":
            raise ValueError(f"Unsupported @{etype}(...) entry; use brace-delimited entries")
        opening = match.end() - 1
        pos = braced_end(raw, opening, f"@{etype} entry at offset {match.start()}")
        block = raw[opening + 1:pos - 1]
        if etype in {"comment", "preamble"}:
            continue
        if etype == "string":
            raise ValueError("@string macros are not expanded; use explicit field values")
        key, comma, body = block.partition(",")
        key = key.strip()
        if not comma or not key or re.search(r"[\s{}]", key):
            raise ValueError(f"Missing or invalid citation key in @{etype} entry")
        entries.append((key, etype, parse_fields(body, key), block))
    if not entries and raw.strip() and not re.search(r"@(?:comment|preamble)\s*\{", raw, re.I):
        raise ValueError("No parseable bibliography entries; check the input format")
    return entries


def norm_title(t: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", t.lower())


def all_surnames(author: str):
    out = []
    for a in author.split(" and "):
        a = a.strip()
        if not a or a == "others":
            continue
        if "," in a:
            out.append(a.split(",")[0].strip().lower())
        elif a.split():
            out.append(a.split()[-1].strip().lower())
    return out


def expand(patterns) -> list[Path]:
    """Expand shell-style globs, keeping literal paths that exist."""
    out: list[Path] = []
    for pat in patterns or []:
        hits = [Path(h) for h in sorted(glob.glob(pat, recursive=True))
                if Path(h).is_file()]
        if hits:
            out.extend(hits)
        elif Path(pat).is_file():
            out.append(Path(pat))
        else:
            raise ValueError(f"No file matches requested --tex input {pat!r}; scan incomplete")
    return list(dict.fromkeys(out))


def collect_cited(paths: list[Path]) -> set[str]:
    cited: set[str] = set()
    for p in paths:
        cited.update(key for _, key in iter_citations(read(p)))
    return cited


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--bib", required=True, type=Path, help="the .bib file")
    ap.add_argument("--tex", action="append", default=[],
                    help="a .tex file or glob to scan for \\cite keys; "
                         "repeatable. Omit to skip check 5.")
    ap.add_argument("--author-share", type=float, default=DEFAULT_AUTHOR_SHARE,
                    help=f"advisory ceiling on any one author's share of "
                         f"entries (default {DEFAULT_AUTHOR_SHARE:.2f}). "
                         "A project rule, not a journal rule.")
    a = ap.parse_args(argv)

    if not 0 < a.author_share <= 1:
        ap.error("--author-share must be in (0, 1]")

    if not a.bib.is_file():
        print(f"FATAL: {a.bib} not found")
        return 1

    raw_full = read(a.bib)
    raw = strip_comments(raw_full)
    try:
        entries = parse_entries(raw)
    except ValueError as exc:
        print(f"BLOCKING: {a.bib}: {exc}")
        return 1

    blocking = 0
    advisory = 0

    print(f"{a.bib}: {len(entries)} entries\n")

    # ---- 1. duplicate keys -------------------------------------------------
    keys = [e[0] for e in entries]
    dup_keys = [k for k, n in Counter(keys).items() if n > 1]
    print("--- 1. duplicate citation keys ---")
    if dup_keys:
        for k in dup_keys:
            print(f"  BLOCKING  {k} defined {keys.count(k)} times")
        blocking += len(dup_keys)
    else:
        print("  none")

    # ---- 2. near-duplicate content ----------------------------------------
    print("\n--- 2. same work under different keys ---")
    by_sig = defaultdict(list)
    for key, _et, f, _b in entries:
        sig = (norm_title(f.get("title", "")), f.get("year", ""))
        if sig[0]:
            by_sig[sig].append(key)
    dups = {s: ks for s, ks in by_sig.items() if len(ks) > 1}
    if dups:
        for (t, y), ks in dups.items():
            print(f"  BLOCKING  {', '.join(ks)}  (same title+year: {t[:44]}... {y})")
        blocking += len(dups)
    else:
        print("  none")

    # ---- 3. required fields ------------------------------------------------
    print("\n--- 3. missing required fields ---")
    missing_any = False
    for key, et, f, _b in entries:
        req = REQUIRED.get(et)
        if req is None:
            print(f"  advisory  {key}: unknown entry type @{et}, no field rule applied")
            advisory += 1
            continue
        gone = []
        for r in req:
            alts = r if isinstance(r, tuple) else (r,)
            if not any(f.get(A) for A in alts):
                gone.append(" or ".join(alts))
        if gone:
            print(f"  BLOCKING  {key} (@{et}) missing: {', '.join(gone)}")
            blocking += 1
            missing_any = True
    if not missing_any:
        print("  none")

    # ---- 3b. standards without an edition year ------------------------------
    print("\n--- 3b. standards carrying no edition year ---")
    noyear = [k for k, et, f, _ in entries if et in UNDATED_OK and not f.get("year")]
    if noyear:
        print(f"  {len(noyear)} entries of type {'/'.join(sorted(UNDATED_OK))} have no year.")
        print("  This is ALLOWED and is usually correct: an unverified edition")
        print("  year must not be guessed. Each still needs a human to read it")
        print("  off the issuing body's catalogue.")
        advisory += len(noyear)
    else:
        print("  none")

    # ---- 4. DOIs -----------------------------------------------------------
    print("\n--- 4. DOI status ---")
    have, bad, empty = [], [], []
    for key, _et, f, _b in entries:
        d = f.get("doi", "").strip()
        if not d:
            empty.append(key)
        elif DOI_RE.match(d):
            have.append((key, d))
        else:
            bad.append((key, d))
    for key, d in bad:
        print(f"  BLOCKING  {key}: malformed DOI {d!r} (expected 10.xxxx/suffix)")
        blocking += 1
    print(f"  {len(empty)} entries with no DOI yet")
    if have:
        print(f"  {len(have)} entries carry a DOI. EVERY ONE still needs external")
        print("  verification against CrossRef; this script does not resolve them:")
        for key, d in have:
            print(f"      {key:<34} {d}")
    else:
        print("  0 entries carry a DOI")

    # ---- 5. cited vs defined ----------------------------------------------
    print("\n--- 5. cited vs defined ---")
    try:
        tex_paths = expand(a.tex)
    except ValueError as exc:
        print(f"  BLOCKING  {exc}")
        blocking += 1
        tex_paths = None
    if tex_paths is None:
        print("  cited-vs-defined check incomplete; no completeness claim made")
    elif not a.tex:
        print("  skipped: no --tex given")
    elif not tex_paths:
        # Silently skipping this check is exactly the failure it exists to
        # catch, so a --tex that matches nothing is blocking, not advisory.
        print(f"  BLOCKING  --tex was given but matched no file: {a.tex}")
        print("            (globs are relative to the current directory; quote "
              "them so the shell does not expand them first)")
        blocking += 1
    else:
        cited = collect_cited(tex_paths)
        defined = set(keys)
        undefined = sorted(cited - defined)
        uncited = sorted(defined - cited)
        print(f"  scanned {len(tex_paths)} file(s), {len(cited)} distinct keys cited")
        if undefined:
            for k in undefined:
                print(f"  BLOCKING  \\cite{{{k}}} has no entry in {a.bib.name}")
            blocking += len(undefined)
        else:
            print("  every cited key is defined")
        print(f"  {len(uncited)} defined but never cited"
              + (": " + ", ".join(uncited) if uncited and len(uncited) <= 12 else ""))

    # ---- 6. VERIFY flags ---------------------------------------------------
    print("\n--- 6. entries flagged for human verification ---")
    verify = [l.strip() for l in raw_full.splitlines()
              if "VERIFY" in l and l.lstrip().startswith("%")]
    if verify:
        for v in verify:
            print(f"  {v[:112]}")
        advisory += len(verify)
    else:
        print("  none")

    # ---- 7. author concentration -------------------------------------------
    print("\n--- 7. author concentration ---")
    n = len(entries)
    counts: Counter = Counter()
    for _k, _et, f, _b in entries:
        for s in set(all_surnames(f.get("author", ""))):
            counts[s] += 1
    if n and counts:
        print(f"  project rule, not a journal rule: no single author above "
              f"{a.author_share:.0%} of {n} entries")
        for surname, c in counts.most_common(6):
            share = c / n
            flag = "  OVER" if share > a.author_share else ""
            print(f"      {surname:<20} {c:>3}/{n}  {share:>5.1%}{flag}")
            if share > a.author_share:
                advisory += 1
        print("  note: the fix is to enlarge the denominator, not to delete")
        print("  self-citations. The stricter structural form of the rule is that")
        print("  no subsection may rest on a single group's work alone.")
    else:
        print("  no author data")

    # ---- summary -----------------------------------------------------------
    print("\n" + "=" * 60)
    print(f"BLOCKING problems : {blocking}")
    print(f"needs human check : {advisory}")
    if blocking:
        print(f"\n{a.bib.name} is NOT ready. Fix the blocking items above.")
    else:
        print("\nNo blocking problem. Items under 4, 6 and 7 still need a human,")
        print("and nothing here checks whether a source supports its claim.")
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
