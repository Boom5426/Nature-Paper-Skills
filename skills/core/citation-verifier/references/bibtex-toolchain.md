# BibTeX Toolchain Hardening

Operational lessons from running a large hand-maintained bibliography through a
LaTeX build. Each item here corresponds to a build that broke or a number that
was wrong.

---

## Probe the toolchain before choosing the citation stack

```bash
for t in pdflatex xelatex lualatex latexmk bibtex biber; do
  printf '%-10s %s\n' "$t" "$(command -v $t || echo MISSING)"
done
```

Do this first. The available binaries decide the stack, not preference:

- **`biber` missing** rules out `biblatex`. Use `natbib` with a `.bst` file.
- **`latexmk` missing** means the compile passes are driven by hand, usually from
  a Makefile.
- **`xelatex` missing** constrains font and Unicode handling.

Writing a `biblatex` preamble against a machine with no `biber` produces a
confusing failure at the citation-resolution stage rather than an obvious missing
tool error, and the usual reaction is to start editing the bibliography.

**Record the install command, not just the probe result.** "Verified on this
machine" tells the next person nothing about their machine. Write down the
packages the document needs and the command that installs them:

```
Required: mathpazo, natbib, titlesec, enumitem, lineno, float, hyperref
On TinyTeX: tlmgr install mathpazo palatino psnfss fpl titlesec enumitem lineno natbib
```

A minimal TeX distribution is the common case on servers and in containers, and
a missing style package produces an error that reads like a syntax error in your
own preamble.

The manual pass sequence, when `latexmk` is unavailable:

```make
main.pdf: $(TEXSRC) refs.bib
	-pdflatex -interaction=nonstopmode -file-line-error main.tex
	bibtex main || true
	pdflatex -interaction=nonstopmode -halt-on-error -file-line-error main.tex
	pdflatex -interaction=nonstopmode -halt-on-error -file-line-error main.tex
```

---

## The first pass must not halt on error

Note the leading `-` and the absence of `-halt-on-error` on the first
`pdflatex` line above. Both are deliberate.

When `refs.bib` has changed, the `.bbl` left over from the previous run can be
broken. With `-halt-on-error` on the first pass, the build stops there, and
`bibtex` never gets to regenerate the file that would have fixed it. The build
becomes unrecoverable without a manual `rm main.bbl`, and the error message
points at the bibliography rather than at the stale artifact.

Halt on error from the second pass onward, where a genuine error should stop the
build.

---

## `unsrtnat` fails on a bibliography of undated standards

Symptom: the build dies inside the author-year suffix generator, or emits
nonsense suffixes past `z`.

Cause: `natbib`'s author-year styles disambiguate same-author-same-year entries
with `\natexlab{a}`, `\natexlab{b}`, and so on. A bibliography with dozens of
standards entries that share one issuing organisation and **deliberately carry no
year** presents that generator with dozens of collisions in a single bucket. It
runs past the alphabet.

The fix is a numeric style, `unsrt`, ordered by first citation.

**The fix is not to invent edition years.** An unverified edition year is a
fabricated identifier, and the pressure to add one in order to get a green build
is exactly the pressure this note exists to resist. A standards entry with no
year is a correct entry that still needs a human to read the year off the issuing
body's catalogue.

If a bibliography audit flags year-less entries, it should flag them as advisory,
never as blocking, for the same reason.

---

## Some styles typeset the `note` field

`unsrt.bst` renders `note` into the printed bibliography. That makes `note` an
input to the typesetter, not a comment.

One project wrote `alpha^-1` into a note. The style typeset it, the `^` opened
math mode outside math, and the build died with:

```
./main.bbl:343: Missing $ inserted
```

No PDF. The `.bbl` is generated, so the error points at a file nobody edited,
which costs time.

Rewritten as `1/alpha`, and every note thereafter scanned:

A single-line `grep` will miss most of them: `.bib` files align their fields and
wrap long notes across lines, so `note = {` and the offending character are
rarely on the same line. Scan the whole field:

```bash
python3 - <<'EOF'
import re, sys
raw = open("refs.bib").read()
for m in re.finditer(r"note\s*=\s*\{", raw):          # brace-match the value
    i, d = m.end(), 1
    while i < len(raw) and d:
        d += (raw[i] == "{") - (raw[i] == "}")
        i += 1
    val = raw[m.end():i-1]
    # ~ is left out: a non-breaking space is legitimate in a rendered note.
    bad = re.findall(r"(?<!\\)[\^_&#$%]|\\[a-zA-Z]+", val)
    if bad:
        print(raw[:m.start()].count("\n") + 1, sorted(set(bad)), val[:70])
EOF
```

The general rule: **before writing free text into any bibliography field, find out
whether that field is rendered.** If it is, it is prose and needs escaping. Do not
assume a field named `note` is a comment.

---

## `.bbl` is a build artifact until submission, then it is a deliverable

During drafting, `.bbl` belongs in `.gitignore` with the other artifacts.

At submission, most publishers want the `.bbl` in the source package, because
they do not run `bibtex`. It must be force-added past the ignore rule:

```bash
git add -f paper/main.bbl
```

Put that command in the ignore file as a comment next to the `.bbl` line. It is
the kind of step that is obvious while you are writing the ignore rule and
invisible three months later at submission.

---

## State the DOI policy explicitly, whichever one you hold

Two defensible policies, and the failure is holding neither of them on purpose.

**All DOIs present and externally verified.** Workable for a modern bibliography
of moderate size: a 19-entry reference list of recent papers can be fully
DOI-verified, and saying so in the README is a real quality signal.

**DOIs deliberately absent until resolved.** The right policy for a large
bibliography carrying standards, technical reports, and older works, where many
entries have no DOI at all and the rest would have to be looked up one at a time.

What is not defensible is a bibliography where some entries have DOIs, some do
not, and nobody can say which state is intentional. Write the policy into the
README next to the entry count.

## Empty `doi = {}` is a policy, not an oversight

A bibliography where most entries carry `doi = {}` looks incomplete to an audit
script. It can be the opposite: a deliberate refusal to write an identifier that
has not been resolved.

**A DOI written from memory is a fabricated identifier**, and it is worse than a
missing one, because a missing DOI is visibly missing while a wrong one resolves
to a different paper and looks authoritative doing it.

So an audit should:

- report the count of entries without a DOI as a **status**, not a failure
- treat a malformed DOI as **blocking**, since it is either a typo or a guess
- treat every DOI that is present as **still needing external verification**, and
  list them, because the script cannot resolve them offline

The bundled `scripts/audit_bib.py` does all three. It never contacts the network,
by design: an offline script that reports what a human must check is more honest
than an online one that appears to have checked.

---

## Bibliography checks worth running that are not about formatting

The bundled script implements these; the reasoning is here because the reasoning
is the transferable part.

**Same work under two keys.** Not duplicate keys, which any tool catches, but the
same title and year entered twice under different keys. It happens when a
reference is added late and nobody greps first, and it produces a manuscript that
cites the same paper as `[4]` and `[19]`. Normalise the title, bucket by
(title, year), flag any bucket with more than one key.

**Cited but not defined, and defined but not cited.** The first is a build error
already. The second is the useful one: entries defined but never cited are usually
survivors of a deleted sentence, and each one should be checked, because sometimes
the sentence is the thing that should come back.

**Author concentration.** Count distinct entries per surname. This is not a
journal rule and there is no universal threshold; set it per project and say in
the output that it is a project rule. The important part is the framing: **the fix
is to enlarge the denominator, not to delete self-citations.** The stricter and
more useful form of the rule is structural rather than numeric: no subsection may
rest on a single group's work alone.

**Comment-based verification flags.** A `% VERIFY` comment next to an entry is a
cheap way to carry "this one still needs a human" through many sessions. Have the
audit list them so they cannot quietly become permanent.

---

## Scanning `.tex` for citation keys

An unescaped `%` in LaTeX swallows the rest of the line **and the leading
whitespace of the next line**. Long citation lists are wrapped using exactly that:

```latex
\citep{smith2020,jones2021,%
       liu2022,chen2023}
```

A naive line-by-line comment strip turns the continuation marker into part of a
key and drops the keys on the following line. Apply LaTeX's own rule:

```python
body = re.sub(r"(?<!\\)%.*?\n[ \t]*", "", body)
```

The lookbehind matters: `\%` is a literal percent sign in the prose, not a
comment. Getting this wrong produces a cited-key list that is quietly incomplete,
and a "0 undefined references" result that means nothing.
