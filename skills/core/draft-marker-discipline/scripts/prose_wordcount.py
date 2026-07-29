#!/usr/bin/env python3
"""Count the prose a reader reads, not the draft apparatus around it.

    prose_wordcount.py --sections paper/sections
    prose_wordcount.py --sections paper/sections --order 01-intro,02-methods
    prose_wordcount.py --sections paper/sections --extra 00-abstract,92-box1
    prose_wordcount.py --file paper/main.tex          # follows \\input/\\include

Why this is not ``wc -w``
-------------------------
On one real manuscript a bare word count over the .tex files returned about
19,900 words. The prose a reader actually reads was about 14,300. The gap is
markup, four draft markers, and six figure legends of roughly 200 words each.

Reporting the larger number makes the manuscript look 40% over length and
invites cutting prose that is not the problem. So this strips, before handing
anything to ``detex``:

  * whole ``figure`` / ``figure*`` / ``table`` / ``table*`` environments,
    legends included. A legend is the display item's word budget, not the
    section's.
  * every ``\\NAME{...}`` for the draft markers named by --markers, matched by
    BRACE COUNTING rather than by regex. Nested braces are ordinary in these
    markers (``\\note{... \\texttt{refs.bib} ...}`` among them) and a lazy
    ``\\TODO\\{.*?\\}`` stops at the first inner close brace. That exact mistake
    has truncated a marker in a real project and produced a fatal LaTeX error,
    so the brace matching here is deliberate and its failure is loud.
  * whole-line comments.

``\\input`` and ``\\include`` are resolved in Python FIRST, and ``detex`` is then
run with ``-n`` so it does not follow them again. Without that, a root file that
is only ``\\input`` lines is stripped (nothing to strip) and then expanded by
detex, so every marker and legend in the included files is counted after all.
That failure is silent and inflates the count by exactly the amount this script
exists to remove.

Requires ``detex`` (texlive-binextra on Debian/Ubuntu).

Quote this script's command next to any word count you write down, so the
number stays reproducible rather than remembered.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import shutil
import subprocess
import sys

# The four draft markers plus a placeholder-float macro. Override with
# --markers when a project names its markers differently.
DEFAULT_MARKERS = ("TODO", "note", "directive", "superseded", "draftfig")

# Float environments whose contents are the display item's budget, not the
# owning section's. Override with --floats.
DEFAULT_FLOATS = ("figure", "table")

INPUT_RE = re.compile(r"(?<!\\)\\(?:input|include)\s*\{([^}]*)\}")


def read(path: pathlib.Path) -> str:
    """Read a source file, naming it if the encoding is not UTF-8."""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        print(f"  warning: {path} is not valid UTF-8; undecodable bytes replaced",
              file=sys.stderr)
        return path.read_text(encoding="utf-8", errors="replace")


def strip_macro(text: str, name: str) -> str:
    """Remove every ``\\name{...}``, honouring nested and escaped braces.

    Escapes are consumed two characters at a time, so a literal ``\\{`` inside a
    marker does not open a group. Without that, legal LaTeX raises a false
    "unbalanced marker" here and a marker containing ``\\}`` silently swallows
    the rest of the file.

    Raises rather than returning a plausible-looking result: an unbalanced
    marker means the source is already damaged, usually by an earlier lazy
    regex strip, and a silent swallow would report a smaller word count and
    hide it.
    """
    out, i, tag = [], 0, "\\" + name + "{"
    while True:
        j = text.find(tag, i)
        if j < 0:
            out.append(text[i:])
            return "".join(out)
        out.append(text[i:j])
        k, depth = j + len(tag), 1
        while k < len(text) and depth:
            c = text[k]
            if c == "\\":
                k += 2          # \{ \} \\ are literals, not group delimiters
                continue
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
            k += 1
        if depth:
            raise SystemExit(f"unbalanced \\{name}{{ at offset {j}; "
                             "a marker is truncated in the source")
        i = k


def resolve_inputs(path: pathlib.Path, seen: set | None = None) -> str:
    """Return the file's text with \\input and \\include expanded, recursively."""
    seen = seen if seen is not None else set()
    real = path.resolve()
    if real in seen:                      # a cyclic \input would not compile
        return ""
    seen.add(real)
    text = read(path)

    def sub(m: re.Match) -> str:
        name = m.group(1).strip()
        if not name:
            return ""
        child = (path.parent / name)
        if child.suffix != ".tex":
            child = child.with_suffix(".tex")
        if not child.is_file():
            print(f"  warning: {path.name} inputs {name!r}, which does not exist",
                  file=sys.stderr)
            return ""
        return "\n" + resolve_inputs(child, seen) + "\n"

    return INPUT_RE.sub(sub, text)


def prose(path: pathlib.Path, markers, floats, keep_floats: bool,
          follow_inputs: bool) -> int:
    """Words a reader reads in one .tex file."""
    text = resolve_inputs(path) if follow_inputs else read(path)
    if not keep_floats:
        for env in floats:
            e = re.escape(env)
            text = re.sub(r"\\begin\{" + e + r"\*?\}.*?\\end\{" + e + r"\*?\}",
                          "", text, flags=re.S)
    text = re.sub(r"(?m)^\s*%.*$", "", text)
    for name in markers:
        text = strip_macro(text, name)
    # -n: do not follow \input/\include. They are already resolved above, and
    # letting detex expand them a second time would reintroduce unstripped text.
    done = subprocess.run(["detex", "-n"], input=text,
                          capture_output=True, text=True)
    if done.returncode != 0:
        sys.stderr.write(done.stderr)
        raise SystemExit(f"detex failed on {path} with status {done.returncode}")
    return len(done.stdout.split())


def resolve(sections: pathlib.Path, order: str | None):
    """The .tex files to count, in the order they should be reported."""
    if order:
        stems = [s.strip() for s in order.split(",") if s.strip()]
        if not stems:
            raise SystemExit("--order named no section")
        paths = []
        for stem in stems:
            p = sections / (stem if stem.endswith(".tex") else stem + ".tex")
            if not p.is_file():
                raise SystemExit(f"{p} does not exist")
            paths.append(p)
        return paths
    return sorted(sections.glob("*.tex"))


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--sections", type=pathlib.Path,
                     help="directory of section .tex files, counted one per row")
    src.add_argument("--file", type=pathlib.Path, action="append",
                     help="count one file, following its \\input/\\include; "
                          "repeatable. Use for a root file such as main.tex.")
    ap.add_argument("--order",
                    help="--sections only: comma-separated stems fixing which "
                         "sections count toward the body total, and in what "
                         "order. Default: every .tex in the directory, sorted.")
    ap.add_argument("--extra",
                    help="--sections only: comma-separated stems to report "
                         "separately, OUTSIDE the body total (abstract, key "
                         "points, boxes)")
    ap.add_argument("--markers", default=",".join(DEFAULT_MARKERS),
                    help=f"comma-separated macro names to strip "
                         f"(default: {','.join(DEFAULT_MARKERS)})")
    ap.add_argument("--floats", default=",".join(DEFAULT_FLOATS),
                    help=f"comma-separated float environments to strip whole; "
                         f"starred variants are covered automatically "
                         f"(default: {','.join(DEFAULT_FLOATS)})")
    ap.add_argument("--keep-floats", action="store_true",
                    help="count legends too; off by default because a legend "
                         "is the display item's budget, not the section's")
    a = ap.parse_args(argv)

    if a.file and (a.order or a.extra):
        ap.error("--order and --extra apply to --sections only")

    if not shutil.which("detex"):
        print("detex not found; install texlive-binextra", file=sys.stderr)
        return 2

    markers = tuple(m.strip() for m in a.markers.split(",") if m.strip())
    floats = tuple(f.strip() for f in a.floats.split(",") if f.strip())
    extra_stems = [s.strip() for s in (a.extra or "").split(",") if s.strip()]

    if a.file:
        for p in a.file:
            if not p.is_file():
                raise SystemExit(f"{p} is not a file")
        paths = a.file
        labels = [p.name for p in paths]
    else:
        if not a.sections.is_dir():
            raise SystemExit(f"{a.sections} is not a directory")
        paths = resolve(a.sections, a.order)
        if not paths:
            raise SystemExit(f"no .tex files under {a.sections}")
        labels = [p.stem for p in paths]

    width = max(len(x) for x in labels + extra_stems + ["body total"])

    total = 0
    for p, label in zip(paths, labels):
        n = prose(p, markers, floats, a.keep_floats, follow_inputs=bool(a.file))
        total += n
        print(f"  {label:<{width}}  {n:6d}")
    print(f"  {'body total':<{width}}  {total:6d}")

    if extra_stems:
        print()
        for stem in extra_stems:
            p = a.sections / (stem if stem.endswith(".tex") else stem + ".tex")
            if not p.is_file():
                raise SystemExit(f"{p} does not exist")
            n = prose(p, markers, floats, a.keep_floats, follow_inputs=False)
            print(f"  {p.stem:<{width}}  {n:6d}   (outside the body total)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
