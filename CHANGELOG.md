# Changelog

## Unreleased

### Rules derived from the reader

- State where the rules come from: each serves the editor, the reviewer or the broad peer at the target venue, and is derived again when the venue, article type or reader differs (`paper-workflow`, design principle 12). Text that meets a rule's wording while defeating its purpose fails it.
- Replace "the first sentence states the biological stake" with "the reader meets a specific problem they recognise as theirs by the second sentence", in the reader's terms. Coded from both samples: the problem appears by the second sentence in 18 of 28 method Articles and 8 of 12 `Nature` papers, and weak openings are truisms about biology as often as about technology.
- Rewrite the contracts' Reader section as Readers: the editor, the reviewer and the broad peer, with the positions each one reads. `manuscript-optimizer`'s reader model follows.
- At double-blind ML venues, keep an anonymized code link or a release statement and write Limitations in its own section (`anti-defensive-writing`, `conference-paper-writing`).
- Update both READMEs, the design principles, the task recipes and the website's Abstract card.

### Venue, numbers and punctuation

- Decide what a paper must say from the target venue's side: `paper-workflow` now names the venue and asks what its editors and reviewers check before any keep-or-cut decision. `anti-defensive-writing` gains a section on what the venue makes load-bearing. At ML conferences a no-leakage sentence stays, a configuration chosen on evaluation data is reported beside the default instead of labelled "prespecified", verdict sentences give way to estimates and intervals, and a single training run is reported to the author as a gap.
- Add "What Reviewers Check, and What Stays Out" to `conference-paper-writing`, a venue preflight for ML conferences and a source-hygiene step (LaTeX comments are public on arXiv, so strip them with `arxiv_latex_cleaner`) to `submission-audit`.
- Replace the "usually at most one number" abstract rule: numbers that show the scale of the problem, of the data or validation, and the size of a gain with its comparison are kept. The Introduction preview, the Discussion opening and Results claims follow the same rule. Most `Nature` abstracts in the reader sample carry such numbers.
- Cap semicolons in `scientific-prose-style` (none in the abstract, at most one per paragraph), measured against the corpus: 3 of 23 typeset method-paper abstracts and 1 of 12 `Nature` abstracts use one. The section contracts no longer use them.
- Add the `iclr-appendix` behavior case and record the venue and number comparisons.

### Broad-peer framing

- Define the reader for front matter as the broad peer (大同行) rather than an adjacent specialist, in the section contracts' new Reader section, `manuscript-optimizer`'s reader model and `write-scientific-manuscript`. Broad positions (Title, Abstract, opening and close of each section) open with the biological stake, introduce the method by what it does, measure success against experiment, expert work or known biology where the Results allow, and state findings in biological terms.
- Add an `audience` route to `paper-workflow` for drafts that read as too technical.
- Compare abstracts of the 28 method Articles with 12 computational-method papers in `Nature`: framing differs sharply, while the rate of model-internal terms does not (median one per abstract in both). Recorded in `section-evidence.md` and reproducible with `scripts/section_corpus.py`.
- Add the `broad-reader-abstract` behavior case.
- Carry the reader checks into `submission-audit` (front matter written for specialists is a reader-friction finding), `results-section-revision` (first and last sentences of each subsection), the editor-first abstract rules, the Introduction paragraph pattern, the task recipes, the ChatGPT Work entry and the website's Abstract card.

### Section contracts

- Add a position axis to `paper-workflow`: each section (Title, Abstract, Introduction, Results, Discussion, Methods, legends, SI, availability) has one contract stating its job, dependencies, typical shape and failure modes, in `references/section-contracts.md`. `manuscript-optimizer`, `write-scientific-manuscript` and `scientific-writing` now point to it instead of restating their own versions.
- Add dependency rules between positions: an Abstract or Title request stays narrow but keeps claims resting on unsettled results out, and a changed Results claim is rechecked wherever it is restated.
- Separate logic from format: abstract length and structure, citations in the abstract and Methods placement come from the journal's current guide, listed as a format check in `nature-portfolio-playbook`. The IMRaD primer's structured clinical abstract is no longer presented as the default.
- Derive typical ranges and method-paper patterns from 28 Nature Methods, Nature Biotechnology and Nature Communications method Articles (`references/section-evidence.md`), reproducible with `scripts/section_corpus.py`. Discussion length (3–5 paragraphs) and the Introduction's findings preview are recorded as house choices that depart from the sample.
- Add the `abstract-section` behavior case.
- Document the section axis in both READMEs, the workflow map, design principles, skill map and CONTRIBUTING. `paper-workflow` and the ChatGPT Work entry now also trigger on single-section requests such as rewriting the Abstract.

### Usage fixes

- Build on the fixes in PR #11 and PR #13 with complete synthetic run data, consistent t/P/effect sizes and three-comparison Bonferroni reporting. Recompute cross-dataset averages within runs and add numerical regression checks.
- Correct related SD/SE, test/P and one-/two-sided examples, clarify assumption diagnostics, and document the all-skills installation required for results-analysis.

- Refuse overwriting paper notes and generated images/metadata; add explicit alternative note paths and unique default schematic names. Reject empty image responses and payloads.
- Preserve PDF text graphics state across page content streams and `q`/`Q`; block incomplete page content instead of reporting PASS.
- Reject malformed CSV quotes, preserve fixed figure export dimensions, show singleton observations and refuse undefined singleton SD/CI intervals.
- Extract R Markdown/Quarto R chunks before source checks; exclude percentages and measurement units from figure-reference continuations.
- Complete the optional citation checker CLI, support bibtexparser 1.x/2.x, normalize Crossref metadata, resolve literal LaTeX bibliographies and return failure for format/consistency errors. Reports and fixed bibliography copies refuse overwriting.
- Escape paper-note YAML, deduplicate new graph edges and avoid manuscript-pointer errors for explicit no-change replies. Keyword misses are advisory.
- Keep all skill descriptions within 1,024 characters; add usage regressions and CI jobs for optional helper dependencies with both bibtexparser versions.

### Installation safety

- Document the manual canonical-directory and symlink layout from PR #5, with entry points in both READMEs and agent guides; updates, checks and restores target the canonical directory.
- Group README installation guidance into Codex, Claude Code, and ChatGPT Work on the web. Keep Windows-native and WSL2 instructions in the Codex guide, including an explicit Windows-user destination; document individual skill paths for the built-in installer and separate web packaging requirements, with verification limits.
- Add a standard-library web bundle builder: a single-entry `nature-paper-workflow` skill with bundled specialists, a skills-only plugin ZIP and a GitHub marketplace. Retain resources, licenses and file hashes, reuse the installer profiles, and refuse existing output paths.
- Add a copyable agent installation instruction and `INSTALL.md`, without mandatory creator selection or user-run build/upload steps. Separate maintainer packaging and publication from web account registration; keep the latter explicitly unverified.
- Offer the full 27-skill workflow first and the 19-skill writing/review stack as a separate copyable instruction. Carry explicit profile requests through local installation, native Python selection and web packaging; retain the installer's existing default.
- Use the GitHub file page for copyable installation instructions, with GitHub-tool and HTTPS-clone fallbacks. Make raw-domain access optional and require original files rather than search snippets when web retrieval fails.
- Refuse to replace per-skill symlinks under the default `backup` policy or `error`, before changing any selected destination.
- Preserve live, broken and looping skill links under `--on-conflict keep` without adopting them into the installation record.
- Identify linked entries in `--doctor` and direct checks to the canonical installation; linked targets are not automatically verified.
- Retain support for symlinked destination roots and the existing backup/restore workflow for real skill directories.
- Apply link protection to restore preflight, including linked backup entries and all selected destinations.

## 0.2.0 — 2026-10-02

### User workflow

- Reorganize English/Chinese homepages around a complete first revision, task inputs and deliverables.
- Add a synthetic tutorial, task recipes, environment/file-format boundaries and behavioral evaluation cases.
- Diagnose relevant writing layers before editing; preserve stable sections, honor review-only and local-edit scope, and stop after focused consistency checks.
- Route long research articles by article type, not by length. Keep Reviews on their own path.
- Include `paper-reviewer` in the recommended profile (19 skills; total remains 27).

### Installation

- Add Codex project-local `.agents/skills` and user-level `~/.agents/skills` targets; retain explicit custom/legacy destinations.
- Require Python 3.9+ standard library for managed installation; no extra packages for installation or core prose work.
- Record version, source and file hashes; detect local edits; stage copies, back up replacements and roll back ordinary installation errors.
- Add `--doctor`, `--on-conflict backup|keep|error`, and `--restore` with preservation of the current copy.
- Pin source by commit when resolvable; retain a visible unresolved-ref state when GitHub lookup is unavailable.
- Add installation/restore integration coverage and Linux/macOS CI jobs. Inspect Actions for actual platform results; native Windows remains unverified.

Version labels are stored in VERSION. Use an immutable commit SHA for reproducible installation; this file does not imply that a matching Git tag or GitHub Release exists.

## Pending helper fixes

- Protect metadata temporary-file writes and preflight project layout conflicts.
- Correct wrapped figure/citation parsing, numeric figure ranges and panel continuations.
- Block malformed bibliography structures and incomplete requested citation scans.
- Correct repeated/nested/commented inputs and exclude extras from body word totals.
- Add regression coverage and [document helper inputs and failure boundaries](docs/helper-script-boundaries.md). These changes are unreleased; optional real-detex tests run when the dependency is available.

## Earlier history

See [commits](https://github.com/Boom5426/Nature-Paper-Skills/commits/main) for the writing-posture, figure-audit, provenance and bilingual documentation changes preceding this version.
