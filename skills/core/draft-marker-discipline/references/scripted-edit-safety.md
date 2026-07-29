# Scripted Edit Safety

Rules for changing a manuscript with a script instead of by hand. Every rule here
was written after the corresponding failure, not before it.

---

## Rule 1: every substitution asserts its hit count

```python
def replace_exactly(text: str, old: str, new: str, expected: int, where: str) -> str:
    n = text.count(old)
    if n != expected:
        raise SystemExit(
            f"{where}: expected {expected} occurrence(s) of {old!r}, found {n}. "
            "Nothing was changed.")
    return text.replace(old, new)
```

Shell equivalent, when a script is genuinely the right tool:

```bash
n=$(grep -c 'OLD' "$f") || n=0
[ "$n" -eq "$EXPECTED" ] || { echo "FAIL $f: expected $EXPECTED, found $n"; exit 1; }
sed -i 's/OLD/NEW/g' "$f"
```

### Why, from two real incidents in one project

**A silent no-op.** A `sed` intended to fix a layout problem matched nothing. It
exited 0. The pipeline reported success. The layout stayed broken and the failure
surfaced much later, in a rendered page, with no obvious connection to the script
that had reported success weeks earlier.

**An assertion that paid.** A later script repointed references to an archived
directory. It expected two occurrences in one file and found one. The second
reference was a bare directory-tree shorthand that the pattern did not cover. A
plain `sed` would have rewritten one, skipped the other, exited 0, and left two
documents disagreeing about where the archive lives.

Note what the assertion caught: not a bug in the pattern's syntax, but an
incomplete model of the file. That is the class of error assertions are for, and
it is invisible to testing the regex in isolation.

**Zero hits is an error, not a no-op.** If you genuinely expect a pattern to be
absent sometimes, pass `expected=0` explicitly. Making it explicit is the point.

---

## Rule 2: brace matching, never lazy regex, on braced macros

```python
re.sub(r"\\TODO\{.*?\}", "", text)      # WRONG
```

The lazy quantifier stops at the first closing brace, which is an inner one
whenever the macro argument contains any other braced macro. Nested braces are
ordinary in draft markers:

```latex
\note{the count is reproduced by \texttt{prose\_wordcount.py} against \texttt{refs.bib}}
```

Stripped lazily, this leaves `against \texttt{refs.bib}}` behind: an extra closing
brace, an unbalanced group, and in the incident that produced this rule, a fatal
LaTeX error and no PDF.

A greedy `.*` is worse, not better: it swallows everything to the last brace in
the file.

Use the brace-matched stripper shipped in this skill's
`scripts/prose_wordcount.py`, and keep its failure behaviour:

```python
if depth:
    raise SystemExit(f"unbalanced \\{name}{{ at offset {j}; "
                     "a marker is truncated in the source")
```

An unbalanced marker means the source is already damaged, probably by an earlier
lazy strip. A stripper that swallows the remainder of the file instead of raising
will report a smaller, plausible word count and hide the damage.

---

## Rule 3: LaTeX comments are not line comments

When scanning `.tex` for citation keys, macro uses, or anything else, an
unescaped `%` swallows the rest of the line **and the leading whitespace of the
next line**. Long wrapped argument lists rely on exactly this:

```latex
\citep{smith2020,jones2021,%
       liu2022,chen2023}
```

Strip comments naively, line by line, and `liu2022` becomes part of whatever
precedes it, or the continuation marker becomes part of a key. Apply LaTeX's own
rule:

```python
body = re.sub(r"(?<!\\)%.*?\n[ \t]*", "", body)
```

The `(?<!\\)` matters: `\%` is a literal percent sign in the text, not a comment.

---

## Rule 4: check what a `.bst` file will typeset before writing into a field

Some bibliography styles typeset the `note` field into the rendered
bibliography. That makes `note` an input to the typesetter rather than a comment,
so raw TeX specials in it break the build.

One project wrote `alpha^-1` into a `note`. The style typeset it, `^` opened math
mode outside math, and the build died with `Missing $ inserted` and produced no
PDF. It was rewritten as `1/alpha` and every note thereafter was scanned:

```bash
grep -nE 'note = \{[^}]*[\^_&#$%]' refs.bib
```

More generally: before writing free text into any bibliography or metadata field,
find out whether that field is rendered. If it is, it is prose and needs escaping;
if it is not, it is a comment and does not. Do not assume.

---

## Rule 5: verify against the artifact, not the exit code

A zero exit code means the tool ran. It does not mean the change is correct.

- After a scripted edit to a manuscript, **rebuild and read the log**, not just
  the return code. Check undefined references, overfull boxes, and the page count.
- After a scripted edit to a figure pipeline, **rebuild and look at the figure**.
  Layout regressions do not raise exceptions.
- After a scripted edit to a bibliography, **re-run the bibliography audit** and
  compare the entry and cited-key counts to what you expected before the edit.

The general form: state the number you expect the artifact to have after the
change, then measure it. An edit whose success cannot be checked against a
measurable property of the output should be made by hand.
