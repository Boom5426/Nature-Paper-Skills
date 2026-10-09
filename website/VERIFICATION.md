# Website delivery verification

Verified on 2026-10-09. This records website behavior, not scientific writing quality.

## Executed checks

- Source build tested at commit `490529b88f1cb87fed0c24daf6da74d06ca49abd`.
- [Actual CI run](https://github.com/Boom5426/Nature-Paper-Skills/actions/runs/37907080134): Astro check, static build, link validation, dependency audit, unit tests and Chromium tests passed.
- 14 bilingual routes, 706 local/source links checked.
- 222 deterministic content and installation tests passed.
- 70 real-browser tests passed; 0 failed, 0 skipped, 0 flaky. This includes 40 responsive screenshot cases across five widths (375, 768, 1024, 1440, 1920 px), eight axe accessibility scans, route navigation and interaction tests.
- npm audit reported zero known vulnerabilities at the time of this run. Dependencies are exactly versioned in package-lock.json.
- Original repository Python suite: 385 tests executed locally, OK with 6 optional-dependency skips. Original skills, installer and repository CI were not edited.

## Boundaries

Chromium behavior was tested on GitHub-hosted Ubuntu. Safari, Firefox and physical devices were not separately tested. Accessibility checks cover the automated rules exercised, not a complete manual accessibility certification. Installation command generation was tested; this does not certify live Codex, Claude Code, native Windows or ChatGPT Work registration. The manuscript example is synthetic and its reference revision is illustrative, not a recorded model output. GitHub Pages availability must be confirmed from the separate deployment job.

## Repeat

Use Node.js 24 LTS, run `npm ci`, `npm run check`, `npm run build`, `npm run test:unit`, `npx playwright install --with-deps chromium`, and `npm run test:e2e` in website/. The Website workflow repeats these checks and publishes reports as artifacts.
