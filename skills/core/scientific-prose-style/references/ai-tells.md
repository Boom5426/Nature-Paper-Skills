# AI tells in scientific prose

Text reads as machine-written when it spends the reader's attention on words that carry nothing:
an intensifier on a plain fact, a frame that inflates a modest point, a sentence that repeats the one
before it, a closing line that announces significance instead of stating a result. Editors and
reviewers notice these quickly, and they cost the paper credibility it has earned elsewhere.

This file is the single list of these tells. `scientific-prose-style` owns words, sentence scaffolds
and typography. `anti-defensive-writing` owns recaps, forward pointers and rhetorical questions as
part of its commentary voice. `write-scientific-manuscript` owns coined terms and weak subjects.
`paper-workflow` routes a request such as "去 AI 味" through them in that order: terms and passage
logic, then posture, then sentences.

## The information test

For each candidate, delete the word or the sentence and reread. If the reader loses no fact, number,
condition or logical link, leave it deleted. If something is lost, keep that content and state it
plainly.

Never fix a tell with a synonym. "This highlights" changed to "This emphasizes" still carries
nothing. Never delete a number, a condition or a null result to make a passage lighter.

## Words do not decide it

Many words that are called AI vocabulary are common in published papers. In the body text of the 28
method Articles behind `paper-workflow`'s section evidence (328,473 words), "robust" appears in 27
papers, "moreover" or "furthermore" in 25, "notably", "indeed", "clear(ly)" and the verb "highlight"
in 19 each, and "Together, ..." or "Taken together, ..." in 12. Removing them by list makes prose
thin and changes nothing about why it read as generated.

A few words almost never appear there, and those are reliable tells.

| Near absent from the corpus (per 10,000 words, papers of 28) | Common in the corpus |
|---|---|
| delve, tapestry, realm, holistic, "in its own right": 0, 0 | robust, moreover, furthermore |
| underscore, unlock, paradigm, seamless, pivotal, "not merely": 0.03, 1 | notably, indeed, clear(ly), highlight |
| shed light, harness, intricate, "it is worth noting": 0.06, 2 | importantly, fundamental(ly), ultimately |
| "In this way,": 0.09, 3. crucially or critically: 0.12, 3 | "Together, these ...", "not only ... but" |

Flag a near-absent word wherever it occurs. Flag a common one only when its sentence fails the
information test, or when a draft uses it at several times the corpus rate. `scripts/ai_tells.py`
reports both.

## Families

Each family names what the reader loses time on, with a before and after. The examples are
synthetic.

### 1. Empty intensifiers

"Ultimately", "fundamentally", "clearly", "crucially", "a clear X", "importantly" on a sentence that
is no more important than its neighbours.

- Before: "The experiments further reveal a clear boundary set by information availability."
- After: "Information availability sets a boundary: with fewer than 20 profiled perturbations, no
  method beats the mean baseline."

### 2. Elevation frames

"Not only X but Y", "in its own right", "not merely", "more than just", which raise a point instead
of stating it.

- Before: "Choosing experiments is not only a modelling challenge but a decision problem in its own
  right."
- After: "The practical question is which experiments to run first when only a few are affordable."

Rewording the frame keeps it. "A decision problem as well as a modelling one", "both a modelling and
a decision problem" and "more than a modelling problem" still say only that the point is bigger than
it looks. Replace the frame with its content: what must be decided, by whom, under what constraint.

### 3. Restatement

A sentence that repeats the previous one in other words, often opening with "In this way",
"This means that" or "In other words". Delete it. If the earlier sentence was unclear, fix that one.

### 4. Recap and inflation closers

A paragraph or section that ends by announcing significance: "Together, these results extend our
understanding of cellular decision making." Delete it, or replace it with the synthesis the
paragraph supports. A closer that adds a conclusion stays: "Together, these analyses show that the
gain comes from the dose module, not from model size." `paper-workflow`'s section contracts say
which positions need an explicit takeaway.

### 5. Forward pointers and meta-commentary

"These controls motivate improving the evidence", "this opens new avenues", "paves the way". A
concrete next step belongs once, in the Discussion's closing scope paragraph, and names what it
would test.

### 6. Rhetorical questions

A paragraph that opens with a question the authors then answer. State what the analysis isolates.

- Before: "What, then, does the model transfer when the target is masked?"
- After: "The masking design isolates what the model transfers when the target is unseen."

### 7. Weak subjects and nominalizations

"The experiments reveal", "this analysis demonstrates the existence of", "the results show a
dependence of X on Y". Make the thing that acts the subject: "X depends on Y."

### 8. Coined compound modifiers

A hyphenated modifier invented for the paper: "deployment-available biological knowledge". Write
"biological knowledge available before profiling". Established field terms stay ("cell-type-aware",
"spatially aware"). The test is whether readers in the field already use the term.

### 9. Typography

- Bold sentences in body text. Emphasis comes from position, the first sentence of a paragraph, not
  from formatting. Bold is for run-in headings where the venue uses them.
- Em dashes, semicolon chains and a colon in every sentence: Rules 1 and 2 of `SKILL.md`.

### 10. Uniform shape

Every paragraph runs claim, elaboration, recap, and every sentence has the same length. Vary the
rhythm (Rule 4) and drop the recap where family 4 applies.

## The venue decides some of these

Readers at different venues expect different things. ML conferences expect signposting ("In this
section, we ...") and a bulleted contribution list in the Introduction, so those are not tells there.
Derive each case from the reader, as `paper-workflow`'s "Where the rules come from" says.

## Detection

```bash
python ~/.agents/skills/scientific-prose-style/scripts/ai_tells.py manuscript.tex
# Claude Code: replace ~/.agents/skills with ~/.claude/skills
```

The script reads `.tex`, `.md` and `.txt`. It drops LaTeX comments, citations, references and inline
math. It reports each tell's count and rate per 10,000 words against the corpus rate, with the line
of every candidate. It reports each distinct coined compound once with its count, plus bold
sentences and paragraphs with more than one semicolon. It changes nothing. Below 1,000 words it does
not judge density.

The corpus rates are stored in the script. From the repository root,
`python scripts/section_corpus.py --xml-dir <cache> --tells` recomputes them from the same papers
and patterns.

## Limits

The corpus covers 2022 to 2025, so some papers may already contain AI-assisted text, and its rates
are an upper bound for unassisted prose. It contains only computational-method papers in three
journals. The families come from one revision history and one reader. A flag is a reason to read the
sentence, not a reason to change it.
