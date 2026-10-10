# Behavior evaluations

These small synthetic cases test a few concrete failure modes. They are not a writing-quality benchmark, acceptance predictor, client-compatibility certification or evidence of improvement over a baseline.

## Run

Start a fresh agent session for each file in `cases/`. Give it only the entry skill, access to other repository skills, and the case input. A suitable instruction is:

> Use paper-workflow at skills/core/paper-workflow/SKILL.md to complete the user's task in evals/cases/passage.md. Return the requested result. Do not read other cases, rubrics or expected outputs.

The runner must not show the model `manifest.json`, the tutorial's expected output, previous outputs or the evaluation report. Preserve final responses and any tool/file actions. Grade only after the response is complete against the rubric in `manifest.json`; allow semantically equivalent scientific phrasing.

Run asset validation with:

```bash
python3 scripts/check_behavior_assets.py
```

This checks that the case definitions and files are complete. It does **not** call a model or certify that the behavioral rubric passed. CI runs this asset check and deterministic repository/installation tests. Live agent checks are separate and require a runtime/account.

## Review the output

A case passes only if every criterion is satisfied. Any numerical drift, invented evidence, unsolicited file edit, unsupported mechanism claim or false completion claim is a failure. Record partial/unavailable outcomes rather than silently excluding a case. Keep exact outputs under `evals/runs/` locally when rerunning; that generated directory is ignored by Git. Published observations can live in `results/`.

## Recorded run

[2026-10-02 observations and response excerpts](results/2026-10-02.md): four fresh sessions, one trial per case. The subagents received no earlier conversation or grading rubric. The available agent runtime was used; there was no comparative model study, repeated-sampling study, Codex CLI session or Claude Code session. The result supports only these four observed executions.

[2026-10-09 and 2026-10-10 observations](results/2026-10-10.md): before and after runs for the section contracts and the broad-peer framing, two runs per arm for the latter. Two of the three comparisons did not separate the versions; the record says why.
