# Helper inputs, failures and interpretation

These helpers inspect local files. A successful run is not evidence that a
paper is scientifically correct, that references support claims, or that an
agent has loaded a skill. Preserve stderr and the exit status with any report.

## File writes

- Installation records are written through an exclusively created temporary
  sibling and then atomically replaced. Existing `installed.json.tmp` or
  `before.json.tmp` entries are not opened or followed. Ordinary write/replace
  failures clean up the new temporary file.
- `paper-bootstrap/scripts/init_paper_layout.py` checks the complete default
  layout before creating entries, including in `--dry-run`. A file where a
  directory is required, a directory where a note is required, or a symlink
  inside the layout stops initialization with exit 2. Inspect the conflict
  manually. Existing ordinary files are reused without overwriting them.
- An explicitly supplied symlink for the entire project root is resolved.
  Child links are refused, including live links and dangling links. New note
  files use exclusive creation. These checks are not a concurrency guarantee;
  avoid changing project entries while initialization runs.

## Citation inventory and bibliography audit

`citation-verifier/scripts/scan_citations.py` recognizes literal `\cite...`
commands, including starred forms, optional arguments and wrapped key lists.
TeX comments are excluded from citation extraction and original line positions
are retained. `audit_bib.py` uses the same citation extractor.

Missing requested inputs, including one missing input among several existing
ones, make the scan incomplete. The inventory returns exit 2 and does not print
a complete summary. An empty directory with no supported files is also
incomplete. A completed inventory exits 0 even when it finds placeholders; it
is a discovery tool, not a pass/fail citation-quality gate.

The bibliography audit accepts brace-delimited entries with braced or quoted
field values and bare numeric values. It checks that entry and field groups
close. Unsupported expressions, such as string macros or concatenation, are
blocking instead of silently ignored. It is not a full BibTeX implementation.
`@comment` and `@preamble` groups are skipped. Omit `--tex` to deliberately skip
cited-vs-defined comparison; any explicitly requested file/glob that matches
nothing is blocking, even if other inputs exist. Blocking problems exit 1.

These scanners do not expand custom TeX macros. They do not resolve DOIs or
verify whether the cited work supports a manuscript claim.

## Figure references

`submission-audit/scripts/check_figure_refs.py` scans reference phrases across
line wraps and normalizes whitespace in category names. Examples include:

```text
Extended  Data Figure 2a
Figs. 1–3 and 5
Fig. 1a, b and c
Figs. 6a and
7b
```

Explicit figure numbers create mentions; panel continuations belong to the
same mention. Panel letters are normalized to lowercase. Descending ranges,
mixed figure/panel ranges and unsupported range tails are reported as
incomplete with exit 1 rather than producing a successful truncated summary.
Ranges spanning more than 1,001 figure numbers are refused. This is a static
text summary, not a check that figures or panels actually exist.

An article such as `a control experiment` after a reference is treated as
prose. For an ambiguous panel list ending in `a` immediately before prose,
repeat the figure number (for example `Fig. 1b and 1a agree`) to make it explicit.

## Prose word counts

`draft-marker-discipline/scripts/prose_wordcount.py` requires `detex`. Under
`--file`, literal `\input`/`\include` paths are resolved relative to the root
manuscript's directory, as when compiling from that directory. Custom input
macros and `TEXINPUTS` search paths are not expanded. Missing inputs and cyclic
inclusion fail instead of returning an incomplete total.

Repeated inclusion is counted each time. Comments are removed before following
inputs or stripping floats/markers; escaped percent signs remain. Under
`--sections`, `--extra` files are reported only outside the body total, both
with the default file selection and an explicit `--order`.

```bash
python prose_wordcount.py --sections paper/sections --extra 00-abstract
python prose_wordcount.py --file paper/main.tex
```
