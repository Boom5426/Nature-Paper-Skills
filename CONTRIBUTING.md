# Contributing

Thanks for contributing. This repository is intentionally narrow: it is a journal-first skill stack for `Nature`-style manuscript work, not a generic prompt dump.

## Good Contributions

- new skills that materially improve drafting, revision, figure planning, citation hygiene, submission preflight, or rebuttal workflows
- focused improvements to existing skills, examples, or installation docs
- helper scripts that are clearly owned by a skill and shipped inside that skill directory
- bilingual documentation improvements that reduce adoption friction for new users

## Out Of Scope

- generic writing prompts with no clear role in the manuscript workflow
- conference-first logic inside the core journal path
- large dependency-heavy tooling that is not required by a specific skill
- orphan scripts, templates, or references that are not linked from a skill

## Repository Structure

- `skills/core/`: default journal workflow skills
- `skills/venue/`: venue-selection or venue-policy skills
- `skills/research/`: literature, analysis, and evidence-generation helpers
- `skills/review/`: reviewer-side evaluation skills
- `skills/optional/`: useful but non-default extensions
- `docs/`: workflow maps, installation notes, and design references
- `examples/`: compact examples that show the expected output shape or handoff style

## Skill Conventions

- Use lowercase kebab-case for skill directory names.
- Every skill directory must include `SKILL.md`.
- Keep a skill self-contained and directly copyable into `~/.codex/skills/` or `~/.claude/skills/`.
- Put skill-local assets under that skill directory, for example `scripts/`, `references/`, `templates/`, or `examples/`.
- Prefer one clear job per skill. If a new skill overlaps heavily with an existing one, narrow the scope or extend the existing skill instead.
- If a skill is adapted or renamed from another source, update [ATTRIBUTION.md](ATTRIBUTION.md).

## Writing And Editing Style

- Stay journal-first and claim-driven.
- Prefer explicit workflow guidance over generic advice.
- Keep Markdown concise and scannable.
- Preserve the repository's existing tone: direct, opinionated, and evidence-bounded.
- When you add user-facing functionality, update both [README.md](README.md) and [README.en.md](README.en.md).

## Adding Or Updating A Skill

1. Choose the right category under `skills/`.
2. Write or update `SKILL.md` with a clear `name` and `description`.
3. Add only the supporting files the skill actually needs.
4. Update [docs/skill-map.md](docs/skill-map.md) if the skill changes the public map of the repo.
5. Update the root READMEs if install guidance, scope, or the default workflow changes.
6. Update [ATTRIBUTION.md](ATTRIBUTION.md) when provenance needs to be recorded.

## Pull Request Expectations

- Explain the problem being solved, not just the files changed.
- Keep the PR focused; unrelated cleanup should go in a separate change.
- Call out any user-facing workflow change, install change, or naming change.
- Include example prompts, before/after snippets, or screenshots only when they make the change easier to evaluate.
- Mention any new dependencies introduced by helper scripts.

## Validation Checklist

This repository is mostly Markdown and skill assets, so verification is lightweight but still required:

- confirm every referenced path exists
- confirm install snippets still point to real skill directories
- confirm new scripts are referenced from the owning `SKILL.md`
- re-read the changed README sections for consistency with the actual repository layout
- check whether the Chinese README needs the same user-facing change

## Licensing

By contributing, you agree that your contributions will be released under the [MIT License](LICENSE).
