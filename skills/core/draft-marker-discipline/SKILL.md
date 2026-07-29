---
name: draft-marker-discipline
description: >-
  Use when a manuscript is being drafted across many sessions and needs auditable open-question tracking: in-source draft markers with distinct jobs, triage of open items by what would actually resolve each one, word counts that exclude draft apparatus, safe archival of superseded material, and assertion-guarded scripted edits. Load before doing a batch pass over TODO markers or before quoting a manuscript's length.
---

# Draft Marker Discipline

## Overview

A manuscript written across many sessions accumulates open questions. Where those
questions live determines whether the draft is auditable or merely long.

Kept in chat, they evaporate at the end of the session. Kept in a separate issue
list, they drift out of sync with the sentence they belong to. Kept in the source
next to the claim, they survive, they travel with the text, and they can be
counted.

This skill covers the marker system, the triage that makes a marker count
meaningful, the measurement that makes a length claim honest, and the two
mechanical traps that have each cost a real build.

## When To Use

Use this skill when:

- a manuscript is drafted across sessions, by several people, or by agents
- you are about to do a batch pass over open markers
- you are about to quote the manuscript's length
- superseded material needs to be removed from the tree
- you are about to make the same edit across many files with a script

Do not use this skill for:

- deciding whether a claim's source supports it. That is
  `claim-source-verification`; this skill is the bookkeeping around it.
- restructuring an unstable argument. That is `manuscript-optimizer`.

## 1. Four Markers, Four Jobs

```latex
\TODO{...}        red     an unresolved FACTUAL or SOURCING question
\note{...}        blue    editorial, addressed to the authors
\directive{...}   boxed   what must change in this passage, and why
\superseded{...}  grey    text a freeze decision replaced, kept not deleted
```

All four vanish under a draft-mode switch, so a clean copy for circulation is one
boolean away.

**The discipline is the restriction on `\TODO`.** It carries factual and sourcing
questions only, never style notes, never "tighten this", never "consider
rephrasing". Style goes in `\note`; a required change goes in `\directive`.

The payoff is that the `\TODO` count becomes a readiness metric rather than a
mixed bag. "Thirty-seven open TODOs" means thirty-seven unresolved factual
questions, which is a statement about the manuscript's evidentiary state. If
style notes are mixed in, the number means nothing and stops being reported.

**`\superseded` earns its place** by making "nothing is deleted silently" cheap.
Replaced text stays visible in draft mode, greyed, so a reader can see what a
freeze decision changed without going to version control.

## 2. Triage By Resolution Route, Not By Topic

"Do the TODOs" is not one task. Sorting them by section tells you where they are;
sorting them by **what would actually resolve each one** tells you which are work
you can do now, which need money, and which need a person.

Five routes:

| Route | Meaning |
| --- | --- |
| **A. Open retrieval** | Answerable from the public literature. An agent or a search can close it. |
| **B. Paid or restricted text** | Needs a purchased standard, a paywalled full text, or a vendor document. |
| **C. Team or author decision** | Not a fact. Someone has to decide. |
| **D. Proprietary data** | Needs data that exists but is not accessible. |
| **E. The evidence does not exist** | The resolution is to say so in the text, with bounds. |

Route E is a real outcome, not a failure. In one Review, a widely-quoted market
share traced to a conference talk and a newspaper report with no survey behind
either. The resolution was to report it as an estimate and name its provenance,
which is a better sentence than the confident one it replaced.

Sort by route and the shape of the remaining work becomes visible: in the run
above, roughly two thirds were route A, about a fifth route B, and a handful
routes C to E. That is a plan. "Thirty-nine TODOs" is not.

**Flag single points of failure.** When one inaccessible document is the only
thing blocking a whole subsection, say so in the triage file by name. It is the
item most worth spending money on and it is invisible in a flat list.

## 3. The Counting Trap

Report the actionable count, not the raw grep count.

The noun form, used to typeset the word inside a sentence that talks about
markers, matches the same pattern as a real marker:

```bash
grep -o '\\TODO{' sections/*.tex | wc -l    # 39
grep -n '\\TODO{}' sections/*.tex           # the 2 noun-form uses, not work
```

Two out of thirty-nine is a 5% overstatement, which sounds harmless until the
number appears in a status report and someone plans against it. Print both, and
say which is which.

The same applies to any count quoted from a grep. Show the command next to the
number so the next person can re-derive it instead of trusting it.

## 4. Word Count Must Exclude The Apparatus

Measured once, on one Review at one point in its drafting: a bare `wc -w` over
the section `.tex` files returned about **19,900** words, and the prose a reader
actually reads was about **14,300**. The gap was markup, the four draft markers,
and six figure legends of roughly 200 words each.

The ratio is not a constant and yours will differ. What generalises is the
direction and the consequence: the inflated number made that Review look far
over length and would have invited cutting prose that was not the problem. This
is not a rounding issue; it is a measurement that points at the wrong fix.

Strip, before counting:

- **whole figure environments, legends included.** A legend is the display item's
  word budget, not the section's. Charging a 200-word legend to the section that
  carries the float makes that section look bloated.
- **all four markers plus any placeholder-float macro**, by brace matching.
- **comment lines.**

Then run `detex`, not a regex, because stripping markup by hand is its own source
of error.

`scripts/prose_wordcount.py` ships with this skill and does exactly that. It
needs `detex` (Debian/Ubuntu: `texlive-binextra`) and nothing else.

```bash
# Claude Code, global install; for Codex use ~/.codex/skills
python3 ~/.claude/skills/draft-marker-discipline/scripts/prose_wordcount.py \
    --sections paper/sections --order 01-intro,02-methods,03-results
python3 ~/.claude/skills/draft-marker-discipline/scripts/prose_wordcount.py \
    --file paper/main.tex          # follows \input/\include
```

It resolves `\input` and `\include` itself and then runs `detex -n`. Letting
detex expand them instead would reintroduce every marker and legend from the
included files after the stripping had already run, which is silent and inflates
the count by exactly the amount the script exists to remove.

Quote its output, and keep the command next to the number wherever the number is
written down, so it stays reproducible rather than remembered.

## 5. Brace Matching, Not Lazy Regex

**This has already caused a fatal build failure.** Stripping markers with

```python
re.sub(r"\\TODO\{.*?\}", "", text)      # WRONG
```

stops at the first inner closing brace. Nested braces are ordinary inside these
markers: `\note{... see \texttt{refs.bib} ...}` gets truncated after
`\texttt{refs.bib}`, leaving an unbalanced brace and, in the case that produced
this rule, no PDF.

Match braces:

```python
def strip_macro(text: str, name: str) -> str:
    """Remove every \\name{...}, honouring nested braces."""
    out, i, tag = [], 0, "\\" + name + "{"
    while True:
        j = text.find(tag, i)
        if j < 0:
            out.append(text[i:])
            return "".join(out)
        out.append(text[i:j])
        k, depth = j + len(tag), 1
        while k < len(text) and depth:
            if text[k] == "{":
                depth += 1
            elif text[k] == "}":
                depth -= 1
            k += 1
        if depth:
            raise SystemExit(f"unbalanced \\{name}{{ at offset {j}; "
                             "a marker is truncated in the source")
        i = k
```

The `raise` matters as much as the matching. An unbalanced marker means the
source is already damaged, and a counting script that silently swallows the rest
of the file will report a plausible smaller number instead of an error.

## 6. Scripted Edits Assert Their Hit Count

Any scripted substitution across a manuscript must state how many hits it expects
and fail loudly when it does not get them.

```python
n = text.count(old)
assert n == expected, f"expected {expected} occurrences of {old!r}, found {n}"
text = text.replace(old, new)
```

Two incidents in one project, in both directions:

- A `sed` that matched nothing ran, exited 0, and reported success. The layout it
  was supposed to fix stayed broken, and the failure surfaced much later in a
  rendered page.
- An assertion expecting two occurrences found one. The second reference was a
  shorthand form the pattern did not cover. A plain `sed` would have skipped it
  silently and left the tree self-contradictory.

**Zero hits is an error, not a no-op.** That is the whole rule. See
`references/scripted-edit-safety.md`.

## 7. Nothing Deleted Silently, And What That Means Under Version Control

"Nothing is deleted silently" is right, but its correct implementation depends on
whether the archived thing could be mistaken for current work.

**An in-tree archive is fine for small, obviously-dead artifacts.** A
`_superseded/` directory of replaced figure panels, each file named for where it
came from, costs nothing and is faster to consult than git. Nobody mistakes
`_superseded/fig3_fig3a_schematic.pdf` for the live figure.

**Version control is the right home for anything a reader could take as current.**
A whole parallel manuscript directory is the clear case. Left in the tree, it
makes every new reader re-decide whether it still counts, and some of them decide
wrong. Then:

1. **Delete it from the working tree.**
2. **Write an archive note that stays.** It records what was removed, from where,
   how large, why, **the commit that holds it**, and the literal commands to get
   it back:

```bash
git show <commit>:paper/attic/old-version/sections/02-physiological.tex
git checkout <commit> -- paper/attic          # whole directory back
git show <commit> --stat -- paper/attic       # see what is in there first
```

3. **Record where the salvageable parts went.** A per-paragraph migration table
   answers "did we lose the eye-safety material?" in ten seconds instead of an
   afternoon.

**The dividing line, worth writing down verbatim:**

> Material that records **why something cannot be used** stays in the working
> tree. The unusable material itself goes to git history.

So the archive note stays; the archived draft does not. A short archive section
explaining why three findings were judged unusable stays; those findings do not.
Without the note, the next session rediscovers a rejected finding, believes it is
new, and puts it back.

## Standing Rules

1. **`\TODO` is factual and sourcing only.** Style goes elsewhere, or the count
   stops meaning anything.
2. **Triage by resolution route, not by topic.**
3. **Report actionable counts, and show the command that produced them.**
4. **Never quote a bare `wc -w` as a manuscript's length.**
5. **Brace matching, never lazy regex, on any macro with a braced argument.**
6. **Every scripted edit asserts its hit count. Zero hits is an error.**
7. **Archive by what a reader could mistake for current.** Small, obviously-dead
   artifacts can stay in an in-tree `_superseded/`; anything a reader could take
   as live gets deleted from the tree, with a record of why and the commit that
   holds it.
