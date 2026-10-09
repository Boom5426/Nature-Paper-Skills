#!/usr/bin/env python3
"""Reproduce the mechanical counts behind skills/core/paper-workflow/references/section-evidence.md.

The sample is fixed below by PMCID, so a rerun measures the same papers even after citation counts
change. Full-text JATS XML is fetched from Europe PMC (falling back to NCBI efetch for accepted
manuscripts) into --xml-dir and reused on later runs. The judgement-based codings in the evidence
file (what each paragraph does) are not computed here.

Usage:
    python3 scripts/section_corpus.py --xml-dir /path/to/cache            # download if missing
    python3 scripts/section_corpus.py --xml-dir /path/to/cache --offline  # use cached XML only
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import statistics as st
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

# Selection on 2026-10-09: Europe PMC, OPEN_ACCESS:y, HAS_FT:y, PUB_YEAR 2022-2025, title matching
# single-cell, spatial transcriptomics, spatially or perturbation, sorted by citations; per journal,
# the first ten papers that introduce a named computational method.
SAMPLE: dict[str, dict[str, str]] = {
    "Nat Methods": {
        "SCENIC+": "PMC10482700", "CellRank": "PMC8828480", "COMMOT": "PMC9911355",
        "CellRank 2": "PMC11239496", "CellOT": "PMC10630137", "scPoli": "PMC10630133",
        "alevin-fry": "PMC8933848", "CytoTRACE 2": "PMC12615260", "Nicheformer": "PMC12695652",
        "SATURN": "PMC11310084",
    },
    "Nat Biotechnol": {
        "Milo": "PMC7617075", "scArches": "PMC8763644", "CARD": "PMC9464662", "GLUE": "PMC9546775",
        "Scissor": "PMC9010342", "DestVI": "PMC9756396", "SEACells": "PMC10713451",
        "CytoSPACE": "PMC10635828", "Higashi": "PMC8843812", "MaxFuse": "PMC11638971",
    },
    "Nat Commun": {
        "ScType": "PMC8913782", "STAGATE": "PMC8976049", "GraphST": "PMC9977836",
        "ALRA": "PMC8752663", "SpatialPCA": "PMC9684472", "STdeconvolve": "PMC9055051",
        "dsb": "PMC9018908", "SpaTalk": "PMC9338929", "scDEAL": "PMC9618578", "nnSVG": "PMC10333391",
    },
}
# Brief Communications: no Results or Discussion headings, so excluded from Article counts.
BRIEF = {"CytoTRACE 2", "CytoSPACE"}
# Accepted manuscripts rather than the typeset version: excluded from abstract and figure counts.
ACCEPTED_MANUSCRIPT = {"alevin-fry", "Milo", "CARD", "Scissor", "DestVI"}

EUROPE_PMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
NCBI_EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id={num}"


def fetch(pmcid: str, dest: Path) -> None:
    """Download one article's JATS XML, trying Europe PMC first and NCBI second."""
    errors = []
    for url in (EUROPE_PMC.format(pmcid=pmcid), NCBI_EFETCH.format(num=pmcid.removeprefix("PMC"))):
        try:
            with urllib.request.urlopen(url, timeout=90) as response:
                data = response.read()
        except OSError as exc:  # URLError and HTTPError are OSError subclasses
            errors.append(f"{url}: {exc}")
            continue
        if b"<body" in data:
            dest.write_bytes(data)
            return
        errors.append(f"{url}: no <body> in response")
    raise RuntimeError(f"could not fetch {pmcid}: " + "; ".join(errors))


def txt(el: ET.Element) -> str:
    return re.sub(r"\s+", " ", "".join(el.itertext())).strip()


def title(sec: ET.Element) -> str:
    t = sec.find("title")
    return txt(t) if t is not None else ""


def tag(el: ET.Element) -> str:
    return el.tag.split("}")[-1]


ABBREV = re.compile(r"\b(e\.g|i\.e|et al|Fig|Figs|Supplementary|vs|ref|refs|approx|Ext|no)\.")


def sents(s: str) -> list[str]:
    """Approximate sentence split; protects common abbreviations."""
    s = ABBREV.sub(lambda m: m.group(0).replace(".", "§"), s)
    parts = [p for p in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9(])", s) if p.strip()]
    return [p.replace("§", ".") for p in parts]


def paras(el: ET.Element) -> list[str]:
    """Paragraphs that are direct children of a section or of its nested sections."""
    out = []
    for ch in el:
        if tag(ch) == "p" and len(txt(ch)) > 40:
            out.append(txt(ch))
        elif tag(ch) == "sec":
            out.extend(paras(ch))
    return out


def without_xrefs(el: ET.Element) -> ET.Element:
    """Copy of an element with citation and figure cross-references removed."""
    el = copy.deepcopy(el)
    for parent in el.iter():
        for ch in list(parent):
            if tag(ch) == "xref":
                parent.remove(ch)
                parent.text = (parent.text or "") + " " + (ch.tail or "")
    return el


NUMBER = re.compile(r"(?<![A-Za-z])\d+(?:[.,]\d+)?\s*(?:%|-fold|×)?")
STUDY_SENTENCE = re.compile(r"\b[Ww]e\b.{0,120}\b(present|develop|developed|introduce|propose|describe|report)\b")
PERFORMANCE_NUMBER = re.compile(r"\d[\d,.~–-]*\s*(%|-fold|×)")
TAKEAWAY = re.compile(r"^(Together|Collectively|Taken together|Overall|In summary|In sum|These (results|findings|analyses|data)|Thus|Therefore|Hence|This (shows|demonstrates|indicates|suggests)|Altogether|In conclusion)\b")
INTERPRETIVE = re.compile(r"\b(suggest\w*|indicat\w*|demonstrat\w*|show\w*|reveal\w*|confirm\w*|highlight\w*|support\w*|underscor\w*|enabl\w*|consistent with)\b", re.I)
COMPARISON = re.compile(r"\b(unlike|in contrast to|compared (?:to|with)|existing methods|previous methods|other methods|competing methods|current methods|prior methods)\b", re.I)
LABELS = ["novel", "first", "unprecedented", "state-of-the-art", "outperform\\w*", "superior", "powerful"]


def opener(sentence: str) -> str:
    if re.match(r"^(To|In order to)\b", sentence):
        return "purpose ('To ...')"
    if re.match(r"^(We (next|then|further|also|first)|Next|Then|Finally|Further|Additionally|Moreover)\b", sentence):
        return "sequence ('Next', 'We next')"
    if re.match(r"^We\b", sentence):
        return "action ('We ...')"
    return "question, context or claim"


def analyse(path: Path) -> dict:
    root = ET.parse(path).getroot()
    art = root if tag(root) == "article" else root.find(".//article")
    abstract = next((a for a in art.findall(".//front//abstract") if a.get("abstract-type") in (None, "")), None)
    ab = re.sub(r"^Abstract\s*", "", txt(abstract)) if abstract is not None else ""
    ab = re.sub(r"Subject terms:.*$", "", ab).strip()
    ab_sents = sents(ab)
    body = art.find(".//body")
    secs = [c for c in body if tag(c) == "sec"]
    titles = [title(s) for s in secs]
    intro = next((paras(s) for s in secs if re.match(r"(introduction|main|background)$", title(s).strip(". ").lower())), None)
    if intro is None:
        intro = [txt(c) for c in body if tag(c) == "p" and len(txt(c)) > 40]
    results = next((s for s in secs if title(s).lower().startswith("results")), None)
    if results is not None:
        subsections = [c for c in results if tag(c) == "sec"]
    else:  # headings placed at top level between Main and Discussion
        subsections = secs[1:titles.index("Discussion")] if "Discussion" in titles else []
    sub_records = []
    for s in subsections:
        ps = [p for p in s.iter() if tag(p) == "p" and len(txt(p)) > 40]
        texts = [txt(p) for p in ps]
        sub_records.append({
            "title": title(s),
            "paragraphs": len(texts),
            "opener": opener(sents(texts[0])[0]) if texts else None,
            "closes_with_takeaway_marker": bool(texts) and bool(TAKEAWAY.match(sents(texts[-1])[-1])),
            "closes_with_interpretive_verb": bool(texts) and bool(INTERPRETIVE.search(sents(texts[-1])[-1])),
            "numbers_per_paragraph": [len(NUMBER.findall(txt(without_xrefs(p)))) for p in ps],
        })
    discussion = next((s for s in secs if title(s).lower().startswith("discussion")), None)
    figure_labels = set()
    for fig in art.iter():
        if tag(fig) == "fig" and fig.find("label") is not None:
            m = re.match(r"^(?:Fig\.?|Figure)\s*(\d+)\b", txt(fig.find("label")))
            if m and not re.search(r"Extended|Supplement", txt(fig.find("label"))):
                figure_labels.add(m.group(1))
    lowered = (txt(art.find(".//front//title-group/article-title")) + " " + ab).lower()
    return {
        "abstract_words": len(ab.split()),
        "abstract_sentences": len(ab_sents),
        "study_sentence_index": next((i for i, s in enumerate(ab_sents, 1) if STUDY_SENTENCE.search(s)), None),
        "abstract_performance_numbers": len(PERFORMANCE_NUMBER.findall(ab)),
        "intro_paragraphs": len(intro),
        "results_subsections": sub_records,
        "discussion_paragraphs": len(paras(discussion)) if discussion is not None else None,
        "discussion_compares_methods": discussion is not None and any(COMPARISON.search(p) for p in paras(discussion)),
        "main_figures": len(figure_labels),
        "labels": {w: bool(re.search(r"\b" + w + r"\b", lowered)) for w in LABELS},
    }


def summary(values: list[float]) -> str:
    q = st.quantiles(values, n=4) if len(values) > 1 else [values[0]] * 3
    return f"n={len(values)} median={st.median(values)} IQR={q[0]}-{q[2]} range={min(values)}-{max(values)}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--xml-dir", required=True, type=Path, help="cache directory for full-text XML")
    ap.add_argument("--offline", action="store_true", help="do not download; fail if XML is missing")
    ap.add_argument("--json", type=Path, help="also write per-paper records to this new file")
    args = ap.parse_args()
    args.xml_dir.mkdir(parents=True, exist_ok=True)
    if args.json is not None and args.json.exists():
        ap.error(f"refusing to overwrite {args.json}")

    records = {}
    for journal, papers in SAMPLE.items():
        for name, pmcid in papers.items():
            path = args.xml_dir / f"{pmcid}.xml"
            if not path.exists():
                if args.offline:
                    print(f"missing {path} (--offline)", file=sys.stderr)
                    return 1
                fetch(pmcid, path)
                time.sleep(0.5)
            if name in BRIEF:
                continue
            rec = analyse(path)
            rec.update(journal=journal, pmcid=pmcid, accepted_manuscript=name in ACCEPTED_MANUSCRIPT)
            records[name] = rec

    typeset = {n: r for n, r in records.items() if not r["accepted_manuscript"]}
    print(f"Articles: {len(records)} ({len(typeset)} typeset, {len(records) - len(typeset)} accepted manuscripts)")
    for journal in SAMPLE:
        rs = [r for r in typeset.values() if r["journal"] == journal]
        print(f"Abstract words, {journal}: {summary([r['abstract_words'] for r in rs])}")
    print(f"Abstract sentences: {summary([r['abstract_sentences'] for r in typeset.values()])}")
    print("Study sentence position:", dict(Counter(r["study_sentence_index"] for r in records.values())))
    print("Abstracts with a performance number (pattern only):",
          sum(r["abstract_performance_numbers"] > 0 for r in records.values()))
    intro = [r["intro_paragraphs"] for r in records.values()]
    print(f"Introduction paragraphs: {summary(intro)}; 3-5: {sum(3 <= x <= 5 for x in intro)}")
    nsub = [len(r["results_subsections"]) for r in records.values()]
    print(f"Results subsections: {summary(nsub)}; 5-8: {sum(5 <= x <= 8 for x in nsub)}")
    subs = [s for r in records.values() for s in r["results_subsections"]]
    print(f"Paragraphs per subsection: {summary([s['paragraphs'] for s in subs])}")
    later = [s for r in records.values() for s in r["results_subsections"][1:]]
    print("Openers of subsections after the first:", dict(Counter(s["opener"] for s in later)))
    nums = [x for s in subs for x in s["numbers_per_paragraph"]]
    print(f"Numbers per Results paragraph: {summary(nums)}; zero: {sum(x == 0 for x in nums)}; five or more: {sum(x >= 5 for x in nums)}")
    print("Subsections closing with a takeaway marker:", sum(s["closes_with_takeaway_marker"] for s in subs),
          "| with an interpretive verb:", sum(s["closes_with_interpretive_verb"] for s in subs),
          "| either:", sum(s["closes_with_takeaway_marker"] or s["closes_with_interpretive_verb"] for s in subs))
    disc = [r["discussion_paragraphs"] for r in records.values() if r["discussion_paragraphs"]]
    print(f"Discussion paragraphs: {summary(disc)}; 3-5: {sum(3 <= x <= 5 for x in disc)}; 4-8: {sum(4 <= x <= 8 for x in disc)}")
    print("Discussions with a comparison to other methods:",
          sum(r["discussion_compares_methods"] for r in records.values() if r["discussion_paragraphs"]))
    print(f"Main figures (typeset): {summary([r['main_figures'] for r in typeset.values()])}")
    print("Title or abstract uses:", {w: sum(r["labels"][w] for r in records.values()) for w in LABELS})
    print("First Results heading starts with 'Overview' or 'Method overview':",
          sum(bool(r["results_subsections"]) and bool(re.match(r"^(method )?overview\b", r["results_subsections"][0]["title"], re.I))
              for r in records.values()))
    if args.json is not None:
        args.json.write_text(json.dumps(records, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
