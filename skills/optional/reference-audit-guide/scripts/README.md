# Citation audit scripts

These runnable helpers supplement the `citation-verifier` local workflow for batch metadata and bibliography checks. They do not read papers to verify cited claims; claim verification remains a separate source-reading step.

## Dependencies

```bash
python3 -m pip install 'bibtexparser>=1.4.4,<3' requests
```

Both bibtexparser 1.x and 2.x are supported and tested. `semanticscholar` and `arxiv` are optional for their respective API searches. Offline format checks need only bibtexparser; `--help` does not require it.

## Offline checks

```bash
python3 format-checker.py references.bib --strict --output new-format-report.md
python3 verify-citations.py references.bib --format-only --output new-verification-report.md
python3 format-checker.py paper.tex --check-latex
python3 verify-citations.py paper.tex --check-latex --format-only
```

Literal `\bibliography{refs}` and `\addbibresource{refs.bib}` paths resolve relative to the input `.tex` file. Repeat `--bib` to supply explicit bibliography files when paths use custom macros. For a `.bib` input, `--check-latex` uses the sibling `.tex` unless `--tex` specifies another file. Requested missing files, empty bibliographies and unparsed entries fail; they are never treated as successful empty scans. Common citation commands such as `\cite`, `\citet`, `\citep` and `\autocite` are recognized, with comments excluded. This is a literal scanner, without custom macro expansion or recursive input handling.

`format-checker.py` exits **0** for no errors, **1** for errors (or warnings under `--strict`), and **2** for input/dependency/output problems. `verify-citations.py` exits **1** for format errors, undefined/duplicate citation keys, low matches or failed verification, and **2** for input/dependency/output problems. A format-only success does not establish that the paper exists. Unused citations are warnings.

## Metadata verification

```bash
python3 verify-citations.py references.bib --verbose --output new-api-report.md
```

Crossref DOI lookup is available with requests. Optional arXiv/Semantic Scholar searches provide fallback metadata. An unavailable service or failed search does not establish that a paper is nonexistent. Inspect partial matches and confirm claims against the source paper. `api-clients.py` provides additional client classes with rate limiting and retries.

## Safe output and narrow automatic fixes

Reports refuse to overwrite existing paths. Choose a new output path for each run. Automatic fixes require a separate destination and preserve the original bibliography:

```bash
python3 format-checker.py references.bib --fix-common --fixed-output new-fixed.bib
```

Only single-line braced/quoted DOI URL prefixes and numeric page-range separators are corrected. Author names, titles, years and scientific content are unchanged. Review the copy before adopting it; existing fixed-output files are refused.
