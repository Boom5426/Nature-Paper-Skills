# Changelog

## Unreleased

### Usage fixes

- Refuse overwriting paper notes and generated images/metadata; add explicit alternative note paths and unique default schematic names. Reject empty image responses and payloads.
- Preserve PDF text graphics state across page content streams and `q`/`Q`; block incomplete page content instead of reporting PASS.
- Reject malformed CSV quotes, preserve fixed figure export dimensions, show singleton observations and refuse undefined singleton SD/CI intervals.
- Extract R Markdown/Quarto R chunks before source checks; exclude percentages and measurement units from figure-reference continuations.
- Complete the optional citation checker CLI, support bibtexparser 1.x/2.x, normalize Crossref metadata, resolve literal LaTeX bibliographies and return failure for format/consistency errors. Reports and fixed bibliography copies refuse overwriting.
- Escape paper-note YAML, deduplicate new graph edges and avoid manuscript-pointer errors for explicit no-change replies. Keyword misses are advisory.
- Keep all skill descriptions within 1,024 characters; add usage regressions and CI jobs for optional helper dependencies with both bibtexparser versions.

### Installation safety

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
