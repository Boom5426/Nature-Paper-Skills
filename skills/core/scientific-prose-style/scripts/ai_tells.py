#!/usr/bin/env python3
"""Flag candidate AI-writing tells in manuscript prose and compare them with a published corpus.

Every flag is a candidate, not a verdict. Apply the information test in
references/ai-tells.md before changing anything: delete a word or a sentence only when the reader
loses no fact by its removal. Standard library only.

Usage:
    python ai_tells.py draft.tex [more.tex ...]
    python ai_tells.py draft.md --json report.json
"""
import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

# Body text of 28 computational-method Articles (Nature Methods, Nature Biotechnology, Nature
# Communications, 2022-2025), recomputed with `python scripts/section_corpus.py --xml-dir <cache>
# --tells` from the repository root. Values: occurrences per 10,000 words, papers containing one.
CORPUS_WORDS = 328_473
RARE_PER_10K = 0.15  # at or below this corpus rate, every occurrence is flagged


@dataclass(frozen=True)
class Tell:
    key: str
    family: str
    pattern: str
    case_sensitive: bool = False
    corpus_per_10k: Optional[float] = None
    corpus_papers: Optional[int] = None

    def regex(self) -> re.Pattern[str]:
        return re.compile(self.pattern, 0 if self.case_sensitive else re.IGNORECASE)


TELLS: tuple[Tell, ...] = (
    # Words and phrases that published papers almost never use.
    Tell("delve", "rare", r"\bdelv(?:e|es|ed|ing)\b", corpus_per_10k=0.00, corpus_papers=0),
    Tell("tapestry/realm", "rare", r"\b(?:tapestry|tapestries|realms?)\b", corpus_per_10k=0.00, corpus_papers=0),
    Tell("holistic", "rare", r"\bholistic(?:ally)?\b", corpus_per_10k=0.00, corpus_papers=0),
    Tell("in its own right", "rare", r"\bin (?:its|their) own right\b", corpus_per_10k=0.00, corpus_papers=0),
    Tell("not merely / more than just", "rare", r"\b(?:not merely|more than just|not simply)\b", corpus_per_10k=0.03, corpus_papers=1),
    Tell("underscore", "rare", r"\bunderscor(?:e|es|ed|ing)\b", corpus_per_10k=0.03, corpus_papers=1),
    Tell("shed light", "rare", r"\bshed(?:s|ding)? (?:new )?light\b", corpus_per_10k=0.06, corpus_papers=2),
    Tell("unlock", "rare", r"\bunlock(?:s|ed|ing)?\b", corpus_per_10k=0.03, corpus_papers=1),
    Tell("paradigm", "rare", r"\bparadigm(?:s|atic)?\b", corpus_per_10k=0.03, corpus_papers=1),
    Tell("seamless", "rare", r"\bseamless(?:ly)?\b", corpus_per_10k=0.03, corpus_papers=1),
    Tell("pivotal", "rare", r"\bpivotal\b", corpus_per_10k=0.03, corpus_papers=1),
    Tell("harness", "rare", r"\bharness(?:es|ed|ing)?\b", corpus_per_10k=0.06, corpus_papers=2),
    Tell("intricate", "rare", r"\bintricate(?:ly)?\b", corpus_per_10k=0.06, corpus_papers=2),
    Tell("it is worth noting", "rare", r"\b(?:it is worth not(?:ing|e)|it should be noted|it is important to note)\b", corpus_per_10k=0.06, corpus_papers=2),
    Tell("In this way,", "rare", r"\bIn this way,", case_sensitive=True, corpus_per_10k=0.09, corpus_papers=3),
    Tell("crucially/critically", "rare", r"\b(?:crucially|critically)\b", corpus_per_10k=0.12, corpus_papers=3),
    # Common in published papers: flagged only when much denser than the corpus.
    Tell("ultimately", "intensifier", r"\bultimately\b", corpus_per_10k=0.30, corpus_papers=7),
    Tell("fundamental(ly)", "intensifier", r"\bfundamental(?:ly)?\b", corpus_per_10k=0.40, corpus_papers=9),
    Tell("importantly", "intensifier", r"\bimportantly\b", corpus_per_10k=0.79, corpus_papers=14),
    Tell("remarkable/strikingly", "intensifier", r"\b(?:remarkabl[ey]|strikingly)\b", corpus_per_10k=0.27, corpus_papers=7),
    Tell("indeed", "intensifier", r"\bindeed\b", corpus_per_10k=1.34, corpus_papers=19),
    Tell("notably", "intensifier", r"\bnotably\b", corpus_per_10k=1.77, corpus_papers=19),
    Tell("clear(ly)", "intensifier", r"\bclear(?:ly)?\b", corpus_per_10k=2.53, corpus_papers=19),
    Tell("not only ... but", "framing", r"\bnot only\b[^.]{0,120}?\bbut\b", corpus_per_10k=0.40, corpus_papers=11),
    Tell("Together/Taken together/Collectively,", "recap", r"\b(?:Together|Taken together|Collectively),", case_sensitive=True, corpus_per_10k=0.70, corpus_papers=12),
    Tell("this highlights/underscores", "recap", r"\b(?:This|These|which) (?:further )?(?:highlight|underscore)s?\b", corpus_per_10k=0.06, corpus_papers=2),
    Tell("motivates future work / opens avenues", "forward pointer", r"\b(?:motivat\w+ (?:future|further)|open\w* (?:new )?avenues|future work (?:could|should|will)|paves? the way|paved the way)\b", corpus_per_10k=0.30, corpus_papers=5),
    Tell("question mark", "question", r"\?(?=\s|$)", corpus_per_10k=0.06, corpus_papers=1),
    Tell("coined compound modifier", "coined term", r"\b[a-z]{3,}-(?:available|aware|centric|agnostic|native|grounded|ready|oriented|first)\b", corpus_per_10k=1.22, corpus_papers=10),
    Tell("em dash", "typography", "\u2014", case_sensitive=True, corpus_per_10k=2.28, corpus_papers=11),
)

DENSE_RATIO = 3.0  # common tell flagged when its rate is at least this multiple of the corpus rate
DENSE_MIN_COUNT = 2
DENSE_MIN_WORDS = 1000  # below this, a rate says nothing about density
BOLD_MIN_WORDS = 6

_LATEX_COMMENT = re.compile(r"(?<!\\)%.*$")
_LATEX_DROP = re.compile(r"\\(?:cite\w*|ref|eqref|autoref|cref|Cref|label|url|href)\*?(?:\[[^\]]*\])*\{[^}]*\}")
_INLINE_MATH = re.compile(r"\$[^$]*\$")
_WORD = re.compile(r"[A-Za-z][A-Za-z'-]*")
_BOLD = re.compile(r"\\textbf\{([^{}]*)\}|\*\*([^*]+)\*\*")


def prose_lines(path: Path) -> list[tuple[int, str]]:
    """Return (line number, text) with LaTeX comments, citations, references and inline math removed."""
    text = path.read_text(encoding="utf-8")
    latex = path.suffix.lower() in {".tex", ".ltx"}
    out = []
    for number, line in enumerate(text.splitlines(), 1):
        if latex:
            line = _LATEX_COMMENT.sub("", line)
            line = _LATEX_DROP.sub("", line)
            line = _INLINE_MATH.sub(" ", line)
            line = line.replace("---", "\u2014")
        out.append((number, line))
    return out


def paragraphs(lines: list[tuple[int, str]]) -> list[tuple[int, str]]:
    """Group lines into blank-line separated paragraphs, keeping the first line number."""
    out, start, buf = [], None, []
    for number, line in lines + [(0, "")]:
        if line.strip():
            start = start or number
            buf.append(line.strip())
        elif buf:
            out.append((start, " ".join(buf)))
            start, buf = None, []
    return out


def scan(paths: list[Path]) -> dict:
    lines = [(f"{p.name}:{n}", t) for p in paths for n, t in prose_lines(p)]
    words = sum(len(_WORD.findall(t)) for _, t in lines)
    report = {"words": words, "tells": [], "locations": []}
    for tell in TELLS:
        rx = tell.regex()
        hits = [(where, m.group(0), t) for where, t in lines for m in rx.finditer(t)]
        rate = 1e4 * len(hits) / words if words else 0.0
        base = tell.corpus_per_10k
        if not hits:
            flag = ""
        elif tell.family in ("rare", "question", "coined term", "typography") or (base is not None and base <= RARE_PER_10K):
            flag = "check every occurrence"
        elif base and words >= DENSE_MIN_WORDS and rate >= DENSE_RATIO * base and len(hits) >= DENSE_MIN_COUNT:
            flag = f"dense: {rate / base:.1f}x corpus"
        else:
            flag = "check sentences that carry no new fact"
        report["tells"].append({"key": tell.key, "family": tell.family, "count": len(hits),
                                "per_10k": round(rate, 2), "corpus_per_10k": base,
                                "corpus_papers": tell.corpus_papers, "flag": flag})
        if tell.family == "coined term":
            seen: dict[str, list] = {}
            for where, match, text in hits:
                seen.setdefault(match.lower(), [where, text, 0])[2] += 1
            for match, (where, text, n) in seen.items():
                report["locations"].append({"where": where, "tell": f"{tell.key} (x{n}; keep if established in the field)",
                                            "match": match, "context": _context(text.lower(), match)})
            continue
        for where, match, text in hits:
            report["locations"].append({"where": where, "tell": tell.key, "match": match,
                                        "context": _context(text, match)})
    for path in paths:
        plines = prose_lines(path)
        for start, para in paragraphs(plines):
            n = para.count(";")
            if n > 1:
                report["locations"].append({"where": f"{path.name}:{start}", "tell": "semicolons in one paragraph",
                                            "match": str(n), "context": para[:120]})
        for number, line in plines:
            for m in _BOLD.finditer(line):
                inner = m.group(1) or m.group(2)
                if len(_WORD.findall(inner)) >= BOLD_MIN_WORDS:
                    report["locations"].append({"where": f"{path.name}:{number}", "tell": "bold sentence in body text",
                                                "match": inner[:60], "context": inner[:120]})
    return report


def _context(text: str, match: str, width: int = 60) -> str:
    i = text.find(match)
    return text[max(0, i - width): i + len(match) + width].strip()


def format_report(report: dict) -> str:
    out = [f"Prose words scanned: {report['words']} (comments, citations, references and inline math removed)",
           f"Corpus: {CORPUS_WORDS} words from 28 published method Articles. Candidates only: apply the information test.",
           "", f"{'tell':40} {'family':16} {'count':>5} {'per 10k':>8} {'corpus':>7}  flag"]
    for t in report["tells"]:
        if t["count"]:
            base = "-" if t["corpus_per_10k"] is None else f"{t['corpus_per_10k']:.2f}"
            out.append(f"{t['key']:40} {t['family']:16} {t['count']:>5} {t['per_10k']:>8.2f} {base:>7}  {t['flag']}")
    if not any(t["count"] for t in report["tells"]):
        out.append("(no listed tell found)")
    if report["locations"]:
        out += ["", "Locations:"]
        out += [f"  {loc['where']}: {loc['tell']}: ...{loc['context']}..." for loc in report["locations"]]
    return "\n".join(out)


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+", type=Path, help="manuscript files (.tex, .md or .txt)")
    ap.add_argument("--json", type=Path, help="also write the report to this new JSON file")
    args = ap.parse_args(argv)
    missing = [str(p) for p in args.files if not p.is_file()]
    if missing:
        ap.error(f"not a file: {', '.join(missing)}")
    if args.json is not None and args.json.exists():
        ap.error(f"refusing to overwrite {args.json}")
    report = scan(args.files)
    print(format_report(report))
    if args.json is not None:
        args.json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
