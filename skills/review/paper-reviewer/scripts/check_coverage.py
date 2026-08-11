#!/usr/bin/env python3
"""Check that a point-by-point response letter mirrors its referee report.

    check_coverage.py --letter response.md --reviewer referee.txt
    check_coverage.py --letter response.md --reviewer referee.txt --strict
    check_coverage.py --letter response.md --reviewer referee.txt \\
        --ledger ledger.md --manuscript revised.md --json

The contract enforced here is structural: every referee ask gets its own reply,
the comment is reproduced verbatim above the reply, replies run in the referee's
order, every reply ends with a manuscript location, and reply length matches the
weight of the question. A reply block is an optional HTML machine tag, a
blockquote holding the referee's words, then the reply body:

    <!-- R1/2.Fig2c.1 severity=minor kind=question -->
    > c) The used dataset is not mentioned in the figure legend.

    Yes, it is BBBC022. The legend now names it. (Fig. 2 legend)

Tags are optional; a letter with none is parsed by matching its blockquotes
against the referee source. Comparisons fold whitespace, curly quotes, dash
variants, leading list markers, and case, so retyped punctuation does not read
as drift while genuine word changes still do.

Pure stdlib, no network, writes nothing. Exit status is 1 if any BLOCKING
finding is raised, else 0; under --strict the advisory findings fail too.

This checker verifies structure only. It cannot tell you whether a reply is
responsive, whether the science is correct, or whether a manuscript change is
adequate. A clean run is not a good letter.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path

FOOTER = (
    "This checker verifies structure only. It cannot tell you whether a reply is responsive,\n"
    "whether the science is correct, or whether a manuscript change is adequate. A clean run\n"
    "is not a good letter."
)

BLOCKING_CODES = frozenset({
    "QUOTE_NOT_VERBATIM", "ORDER_MISMATCH", "MISSING_REPLY", "ORPHAN_REPLY",
    "KEY_DUPLICATE", "NO_LOCATION", "BLANKET_REPLY", "SUBITEM_UNSPLIT",
    "PANEL_MISSING", "POINTER_UNRESOLVED", "PROMISED_NOT_LANDED",
    "NO_REPLY_BLOCKS",
})

# Blanket wording: one reply standing in for several asks. Matched as patterns rather
# than fixed substrings because real letters write "all THE minor comments", with a
# determiner and adverbs the author chose freely.
BLANKET_RE = re.compile(
    r"\ball\b[^.]{0,30}?\b(?:minor|other|remaining|further)\b[^.]{0,20}?"
    r"\b(?:comments?|points?|concerns?|suggestions?|issues?)\b"
    r"|\beach of the (?:remaining|minor|other)\s+(?:comments?|points?|concerns?)\b"
    r"|\bthe rest of the (?:comments?|points?|concerns?)\b"
    r"|\ball of the above\b|\bthese have all been\b"
    r"|\bwe have addressed all\b|\bas suggested throughout\b", re.IGNORECASE)
BLANKET_WHOLE = ("revised accordingly",)     # blanket only when it is the whole reply
ASK_CUES = ("should", "must", "please", "i suggest", "i recommend", "it would be valuable",
            "the authors are encouraged", "clarify", "provide")
# Words too generic to locate a passage by searching the manuscript for them.
STOPWORDS = frozenset(
    "manuscript revised revision reviewer referee comment comments however because therefore "
    "additional following included provided suggested addressed performed described although "
    "further between accordingly corresponding supplementary extended section sections methods "
    "results discussion figures analysis analyses".split())
ABBREVIATIONS = ("fig", "figs", "figure", "eq", "eqs", "ref", "refs", "e.g", "i.e", "cf",
                 "vs", "al", "no", "suppl", "approx", "sec", "dr", "prof", "et")

HEADING_RE = re.compile(r"^\s{0,3}(#{1,6})\s+(.*)$")
QUOTE_RE = re.compile(r"^\s{0,3}>\s?(.*)$")
TAG_RE = re.compile(r"<!--\s*(?P<body>.*?)\s*-->")
ENUM_RE = re.compile(r"(?:(?<=\s)|^)\(?(?:\d{1,2}|[ivxIVX]{1,4}|[a-hA-H])[.)]\s")
DASH_LIST_RE = re.compile(r"(?m)^\s*-\s+\S")
PANEL_RE = re.compile(r"Fig(?:ure)?\.?\s*(\d+)\s*([a-h])\b")
BARE_PANEL_RE = re.compile(r"(?:^|\s)\(?([a-h])\)")
FIG_CONTEXT_RE = re.compile(r"\bfig(?:ure)?\b|\bpanel\b|\blegend\b", re.IGNORECASE)
NO_CHANGE_RE = re.compile(r"no\s+(?:manuscript\s+)?change", re.IGNORECASE)
LOCATION_RE = re.compile(
    r"\(page\s+\d+|\bpages?\s+\d+|\blines?\s+\d+"
    r"|\bFig(?:ure)?s?\.?\s*\d|\bTables?\s+[\dSIVX]"
    r"|\bSupplementary\s+\w+|\bExtended\s+Data\b|\bSections?\s+\S+",
    re.IGNORECASE)
# Bare section names count only when capitalised, so "the methods we used"
# does not pass as a pointer into the Methods section.
SECTION_RE = re.compile(r"\b(?:Methods|Results|Discussion)\b")


def normalise(text: str) -> str:
    """Fold typography, list markers, case, and whitespace for comparison.

    Dash variants and the soft hyphen are spelled as escapes on purpose: this
    repository forbids the literal long dash in source files.
    """
    for src, dst in ((chr(0x2018), "'"), (chr(0x2019), "'"), (chr(0x201C), '"'),
                     (chr(0x201D), '"'), (chr(0x201A), "'"), (chr(0x201E), '"'),
                     (chr(0x2032), "'"), (chr(0x2033), '"'), (chr(0x2013), "-"),
                     (chr(0x2014), "-"), (chr(0x2212), "-"), (chr(0x00AD), "")):
        text = text.replace(src, dst)
    text = re.sub(r"^\s*(?:[-*•]|\(?\d{1,2}[.)]|\(?[a-zA-Z][.)])\s+", "", text)
    text = " ".join(text.split())
    # Rejoin words broken across a line by a hyphen, as pdftotext leaves them.
    return re.sub(r"(\w)-\s+(\w)", r"\1-\2", text).lower()


def sentences(text: str) -> list[str]:
    """Split into sentences, keeping common scientific abbreviations intact."""
    guarded = text
    for abbrev in ABBREVIATIONS:
        # Keep the source casing: a case-sensitive location test runs on the result.
        guarded = re.sub(r"(?<![A-Za-z])" + re.escape(abbrev) + r"\.",
                         lambda m: m.group(0)[:-1] + "\x00", guarded, flags=re.IGNORECASE)
    guarded = re.sub(r"\b([A-Z])\.", "\\1\x00", guarded)
    parts = re.split(r"(?<=[.!?])[\s\)]+", guarded)
    return [p.replace("\x00", ".").strip() for p in parts if p.strip()]


def words(text: str) -> int:
    """Word count of prose, punctuation excluded."""
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'’-]*", text))


class Block:
    """One reply block: optional machine tag, referee quote, reply body."""

    def __init__(self, key: str | None, attrs: dict[str, str], heading: str,
                 comment: str, reply: str, line: int) -> None:
        self.key, self.attrs, self.heading = key, attrs, heading
        self.comment, self.reply, self.line = comment, reply, line
        self.offset = -1        # character offset of the quote in the referee source

    def label(self) -> str:
        """Machine tag key when present, else a quoted prefix of the comment."""
        if self.key:
            return self.key
        head = " ".join(self.comment.split())[:34]
        return f'"{head}..."' if head else f"line {self.line}"


def read(path: Path) -> str:
    """Read a source file, naming it if the encoding is not UTF-8."""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        print(f"  warning: {path} is not valid UTF-8; bytes replaced", file=sys.stderr)
        return path.read_text(encoding="utf-8", errors="replace")


def parse_tag(line: str) -> tuple[str | None, dict[str, str]] | None:
    """Parse `<!-- KEY name=value ... -->` into its key and attributes."""
    match = TAG_RE.search(line)
    if not match or not line.lstrip().startswith("<!--"):
        return None
    tokens = match.group("body").split()
    key = tokens[0] if tokens and "=" not in tokens[0] else None
    attrs = {k.lower(): v.lower() for k, v in
             (t.split("=", 1) for t in tokens if "=" in t)}
    return key, attrs


def parse_letter(text: str) -> tuple[list[Block], list[Block]]:
    """Return (reply blocks, loose prose chunks carrying no blockquote)."""
    lines = text.splitlines()
    blocks: list[Block] = []
    loose: list[Block] = []
    heading, pending_line, i = "", 0, 0
    pending: tuple[str | None, dict[str, str]] | None = None

    def take_body(j: int) -> tuple[str, int]:
        """Reply text from line j up to the next heading, quote, or tag."""
        out: list[str] = []
        while j < len(lines) and not (HEADING_RE.match(lines[j])
                                      or QUOTE_RE.match(lines[j]) or parse_tag(lines[j])):
            out.append(lines[j])
            j += 1
        return "\n".join(out).strip(), j

    while i < len(lines):
        line = lines[i]
        head = HEADING_RE.match(line)
        if head:
            heading, pending, i = head.group(2).strip(), None, i + 1
            continue
        tag = parse_tag(line)
        if tag:
            pending, pending_line, i = tag, i + 1, i + 1
            continue
        if QUOTE_RE.match(line):
            quote: list[str] = []
            start = i
            while i < len(lines):
                inner = QUOTE_RE.match(lines[i])
                blank_gap = (not lines[i].strip() and i + 1 < len(lines)
                             and QUOTE_RE.match(lines[i + 1]))
                if not inner and not blank_gap:
                    break
                quote.append(inner.group(1) if inner else "")
                i += 1
            body, i = take_body(i)
            key, attrs = pending if pending else (None, {})
            blocks.append(Block(key, attrs, heading, "\n".join(quote).strip(),
                                body, pending_line if pending else start + 1))
            pending = None
            continue
        if line.strip():
            body, end = take_body(i)
            key, attrs = pending if pending else (None, {})
            loose.append(Block(key, attrs, heading, "", body,
                               pending_line if pending else i + 1))
            pending, i = None, end
            continue
        i += 1
    return blocks, loose


def parse_ledger(text: str) -> dict[str, dict[str, str]]:
    """Parse a markdown pipe table keyed by its Key/Severity/Landed columns."""
    rows: dict[str, dict[str, str]] = {}
    index: dict[str, int] = {}
    for line in text.splitlines():
        if line.count("|") < 2:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        lowered = [c.lower() for c in cells]
        if not index:
            if all(name in lowered for name in ("key", "severity", "landed")):
                index = {name: lowered.index(name)
                         for name in ("key", "severity", "landed")}
            continue
        if set("".join(cells)) <= set("-: ") or max(index.values()) >= len(cells):
            continue
        key = cells[index["key"]].strip("`* ")
        if key:
            rows[key] = {"severity": cells[index["severity"]].lower(),
                         "landed": cells[index["landed"]].strip()}
    return rows


def enumerators(text: str) -> int:
    """Count inner list items, ignoring any number the text itself opens with.

    Shared by SUBITEM_UNSPLIT, which asks whether the referee sub-listed, and by
    BLANKET_REPLY, which asks whether the author answered item by item.
    """
    inner = re.sub(r"^\s*\(?(?:\d{1,2}|[ivxIVX]{1,4}|[a-hA-H])[.)]\s+", "", text)
    dashes = len(DASH_LIST_RE.findall(inner))
    return len(ENUM_RE.findall(inner)) + (dashes if dashes > 1 else 0)


def distinctive(text: str) -> list[str]:
    """The three longest non-generic alphabetic tokens over six characters."""
    found = {w.lower() for w in re.findall(r"[A-Za-z][A-Za-z-]{6,}", text)}
    ranked = sorted(found, key=lambda w: (-len(w), w))
    return [w for w in ranked if w.strip("-") not in STOPWORDS][:3]


def names_panel(reply: str, num: str | None, letter: str) -> bool:
    """True when the reply refers to the same figure panel as the comment."""
    span = r"[a-h,\s\u2013\u2014-]*"
    if num and re.search(rf"Fig(?:ure)?\.?\s*{num}\s*{span}{letter}\b", reply, re.IGNORECASE):
        return True
    if num is None and re.search(rf"Fig(?:ure)?\.?\s*\d+\s*{span}{letter}\b", reply, re.IGNORECASE):
        return True
    if re.search(rf"\bpanel\s+\(?{letter}\)?\b", reply, re.IGNORECASE):
        return True
    return bool(re.search(rf"(?:^|\s)\(?{letter}\)", reply))


def add(findings: list[dict], code: str, label: str, message: str, position: int) -> None:
    """Record one finding, marking it blocking or advisory by its code."""
    findings.append({"key": label, "code": code, "blocking": code in BLOCKING_CODES,
                     "message": message, "position": position})


def check_quotes(blocks: list[Block], source: str, findings: list[dict]) -> None:
    """Verbatim fidelity of each blockquote, then referee order across them."""
    source_norm = normalise(source)
    source_sents = sentences(source_norm)
    for block in blocks:
        comment = normalise(block.comment)
        if not comment:
            continue
        block.offset = source_norm.find(comment)
        if block.offset < 0:
            near = difflib.get_close_matches(comment[:200], source_sents, n=1, cutoff=0.35)
            hint = f'nearest referee text: "{near[0][:90]}"' if near else \
                "no similar referee sentence found"
            add(findings, "QUOTE_NOT_VERBATIM", block.label(),
                f"quote absent from the referee source; {hint}", block.line)

    placed = [b for b in blocks if b.offset >= 0]
    for prev, curr in zip(placed, placed[1:]):
        if curr.offset < prev.offset:
            add(findings, "ORDER_MISMATCH", curr.label(), f"answered after {prev.label()} "
                f"but stands earlier in the referee report ({curr.offset} < {prev.offset})",
                curr.line)
            return


def check_structure(blocks: list[Block], loose: list[Block], findings: list[dict]) -> None:
    """Missing replies, orphan replies, and duplicated machine tag keys."""
    seen: dict[str, int] = {}
    for block in blocks + loose:
        if not block.key:
            continue
        if block.key in seen:
            add(findings, "KEY_DUPLICATE", block.key,
                f"key already used at letter line {seen[block.key]}", block.line)
        seen.setdefault(block.key, block.line)
    for block in blocks:
        if not block.reply.strip():
            add(findings, "MISSING_REPLY", block.label(), "quoted with no reply under it",
                block.line)
    # Prose with no quote above it. Section preamble ("We thank the reviewer")
    # is exempt on purpose; a tagged chunk or a comment-shaped heading is not,
    # because both promise a reply block and deliver an unquoted one.
    comment_heading = re.compile(r"comment|point|^r\d|^\s*\d+[.)]", re.IGNORECASE)
    quoted_headings = {b.heading for b in blocks}
    for chunk in loose:
        if chunk.key or chunk.attrs:
            add(findings, "ORPHAN_REPLY", chunk.label(),
                "tagged as a reply block but quotes no referee comment", chunk.line)
        elif (chunk.heading and comment_heading.search(chunk.heading)
              and chunk.heading not in quoted_headings):
            add(findings, "ORPHAN_REPLY", f'"{chunk.heading[:34]}"',
                "section reads as one comment but quotes none", chunk.line)


def check_subitems(blocks: list[Block], findings: list[dict]) -> None:
    """Referee sub-lists that the letter answered with a single block."""
    norms = [(b, normalise(b.comment)) for b in blocks]
    for block, comment in norms:
        listed = enumerators(block.comment)
        if listed < 2 or not comment:
            continue
        covered = any(other is not block and len(text) >= 20 and
                      (text in comment or comment in text) for other, text in norms)
        if not covered:
            add(findings, "SUBITEM_UNSPLIT", block.label(), f"referee sub-listed {listed} "
                "asks here; the letter answers them in one block", block.line)


def check_body(block: Block, ledger: dict[str, dict[str, str]], findings: list[dict]) -> None:
    """Per-block checks over the reply text: location, blanket wording, size."""
    reply = block.reply.strip()
    if not reply:
        return
    label, sents = block.label(), sentences(reply)
    tail = " ".join(sents[-2:])
    if not (LOCATION_RE.search(tail) or SECTION_RE.search(tail) or NO_CHANGE_RE.search(reply)):
        add(findings, "NO_LOCATION", label, "reply does not close on a manuscript "
            "location and states no explicit no-change", block.line)

    flat = " ".join(reply.split())
    match = BLANKET_RE.search(flat)
    phrase = match.group(0) if match else next(
        (p for p in BLANKET_WHOLE if flat.strip(" .").lower() == p), None)
    # A reply that points at a numbered location or walks the items one by one has not
    # stood in for several asks, so "All twelve minor comments, below" stays legitimate.
    if phrase and not (LOCATION_RE.search(reply) or enumerators(reply) >= 2):
        add(findings, "BLANKET_REPLY", label, f'blanket wording "{phrase}"; each ask '
            "needs its own reply", block.line)

    panels = {(m.group(1), m.group(2).lower()) for m in PANEL_RE.finditer(block.comment)}
    if FIG_CONTEXT_RE.search(block.comment):
        panels |= {(None, m.group(1).lower()) for m in BARE_PANEL_RE.finditer(block.comment)}
    for num, letter in sorted(panels, key=lambda p: (p[0] or "", p[1])):
        if not names_panel(reply, num, letter):
            named = f"Fig. {num}{letter}" if num else f"panel {letter}"
            add(findings, "PANEL_MISSING", label,
                f"comment names {named}; the reply never names that panel", block.line)

    first = sents[0] if sents else ""
    if words(first) > 25:
        add(findings, "FIRSTLINE_LONG", label, f"first sentence is {words(first)} words; "
            "the answer should land inside 25", block.line)
    if "?" in block.comment and not (re.match(r"\s*(Yes|No|We\s|This\s)", first)
                                     or re.search(r"\d", first)):
        add(findings, "NO_DIRECT_ANSWER", label, "referee asked a question; the reply does "
            "not open with a direct answer", block.line)

    # Severity comes from the ledger row when there is one, else from the block's tag.
    severity = ledger.get(block.key or "", {}).get("severity") or block.attrs.get("severity", "")
    minor_section = bool(re.search(r"minor", block.heading, re.IGNORECASE))
    cap = 40 if minor_section else (300 if severity in ("major", "blocking") else 120)
    band = "minor section" if minor_section else \
        (f"severity {severity}" if severity in ("major", "blocking") else "default band")
    n_reply, n_comment = words(reply), words(block.comment)
    if n_reply > cap:
        add(findings, "REPLY_BLOAT", label,
            f"{n_reply} words against a {cap}-word ceiling ({band})", block.line)
    elif 0 < n_comment < 25 and n_reply > 8 * n_comment:
        add(findings, "REPLY_BLOAT", label,
            f"{n_reply} words answering a {n_comment}-word comment", block.line)
    if severity in ("major", "blocking") and n_reply < 40 and not re.search(r"\d", reply) \
            and not LOCATION_RE.search(reply):
        add(findings, "REPLY_THIN", label, f"severity {severity} answered in {n_reply} "
            "words with no number and no location", block.line)


def check_pointers(blocks: list[Block], manuscripts: list[tuple[str, str]],
                   findings: list[dict]) -> None:
    """Reply content words that appear in no supplied manuscript file."""
    names = ", ".join(name for name, _ in manuscripts)
    for block in blocks:
        tokens = distinctive(block.reply)
        if not tokens:
            continue
        absent = [t for t in tokens if not any(t in body for _, body in manuscripts)]
        if len(absent) * 2 < len(tokens):
            continue
        where = LOCATION_RE.search(block.reply) or SECTION_RE.search(block.reply)
        stated = f"; stated location: {where.group(0).strip()}" if where else ""
        add(findings, "POINTER_UNRESOLVED", block.label(),
            f'"{absent[0]}" not found in {names}{stated}', block.line)


def check_ledger(ledger: dict[str, dict[str, str]], findings: list[dict]) -> None:
    """Ledger rows whose change was promised but never recorded as landed."""
    for key, row in ledger.items():
        landed = row["landed"]
        if not landed or re.fullmatch(r"promised only\.?", landed, re.IGNORECASE):
            add(findings, "PROMISED_NOT_LANDED", key,
                f"ledger Landed cell is {'empty' if not landed else landed!r}", 0)


def check_ask_count(source: str, n_blocks: int, findings: list[dict]) -> None:
    """Heuristic gap between referee ask cues and the number of reply blocks."""
    lowered = source.lower()
    cues = lowered.count("?") + sum(lowered.count(cue) for cue in ASK_CUES)
    if not n_blocks:
        # A checker that silently found nothing to check has reproduced the very
        # failure it exists to catch, so an unquoted letter blocks rather than passes.
        add(findings, "NO_REPLY_BLOCKS", "letter", "the letter quotes no referee comment, "
            f"so nothing was mirrored against the {cues} ask cues in the report", 0)
    elif cues > n_blocks * 1.2:
        add(findings, "ASK_COUNT_GAP", "letter", f"{cues} ask cues in the referee report "
            f"against {n_blocks} reply blocks; advisory and imprecise, cues are counted by "
            "keyword and over-count ordinary prose", 0)


def report(findings: list[dict], skipped: list[str], n_blocks: int) -> None:
    """Print one greppable line per finding, then the summary and footer."""
    if findings:
        key_w = min(max(len(f["key"]) for f in findings), 40)
        code_w = max(len(f["code"]) for f in findings)
        for f in findings:
            print(f"{f['key']:<{key_w}}   {f['code']:<{code_w}}   {f['message']}")
    else:
        print("No structural finding.")
    blocking = sum(1 for f in findings if f["blocking"])
    print("\n" + "=" * 60)
    print(f"reply blocks      : {n_blocks}")
    print(f"BLOCKING findings : {blocking}")
    print(f"advisory findings : {len(findings) - blocking}")
    print(f"skipped checks    : {'; '.join(skipped) if skipped else 'none'}")
    print("\n" + FOOTER)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        epilog=FOOTER,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--letter", required=True, type=Path,
                    help="the point-by-point response letter, markdown")
    ap.add_argument("--reviewer", required=True, type=Path,
                    help="the referee report as received, text or markdown")
    ap.add_argument("--ledger", type=Path,
                    help="markdown pipe table with Key, Severity, Landed columns; "
                         "enables PROMISED_NOT_LANDED and the severity bands")
    ap.add_argument("--manuscript", action="append", default=[], type=Path,
                    help="revised manuscript text; repeatable. Enables "
                         "POINTER_UNRESOLVED.")
    ap.add_argument("--strict", action="store_true",
                    help="let advisory findings fail the run too")
    ap.add_argument("--json", action="store_true",
                    help="emit findings and summary as JSON instead of lines")
    a = ap.parse_args(argv)

    for path in [a.letter, a.reviewer] + ([a.ledger] if a.ledger else []) + a.manuscript:
        if not path.is_file():
            print(f"FATAL: {path} not found", file=sys.stderr)
            return 2

    blocks, loose = parse_letter(read(a.letter))
    source = read(a.reviewer)
    ledger = parse_ledger(read(a.ledger)) if a.ledger else {}
    manuscripts = [(p.name, normalise(read(p))) for p in a.manuscript]
    skipped = ([] if a.ledger else ["PROMISED_NOT_LANDED and the ledger severity bands "
                                    "(no --ledger)"])
    if not manuscripts:
        skipped.append("POINTER_UNRESOLVED (no --manuscript)")

    findings: list[dict] = []
    check_quotes(blocks, source, findings)
    check_structure(blocks, loose, findings)
    check_subitems(blocks, findings)
    for block in blocks:
        check_body(block, ledger, findings)
    if manuscripts:
        check_pointers(blocks, manuscripts, findings)
    if ledger:
        check_ledger(ledger, findings)
    check_ask_count(source, len(blocks), findings)

    findings.sort(key=lambda f: (not f["blocking"], f["position"], f["code"]))

    if a.json:
        blocking = sum(1 for f in findings if f["blocking"])
        print(json.dumps({"findings": findings,
                          "summary": {"reply_blocks": len(blocks),
                                      "blocking": blocking,
                                      "advisory": len(findings) - blocking,
                                      "skipped": skipped,
                                      "limitation": FOOTER}}, indent=2))
    else:
        report(findings, skipped, len(blocks))

    if any(f["blocking"] for f in findings):
        return 1
    return 1 if a.strict and findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
