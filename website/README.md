# Nature Paper Skills website

A bilingual, static product site. It presents the repository's workflow, task
recipes, source-linked synthetic example, skill catalog and installation choices.
It does not upload manuscripts, run an AI model or install anything in a visitor's
environment. No analytics, external fonts or runtime GitHub API are required.

## Develop

From the repository root:

```bash
cd website
npm ci
npm run dev
```

Node 22.19+ is required. The development and production base path is
`/Nature-Paper-Skills/`; use the full path shown by Astro.

```bash
npm run check       # Astro / TypeScript diagnostics and content generation
npm run build       # static output, internal/source link validation
npm run test:unit   # source invariants and installation matrix
npx playwright install chromium
npm run test:e2e    # routes, interaction, accessibility and viewport screenshots
npm run social     # regenerate original 1200×630 social preview images
```

`PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH` optionally selects an existing Chromium for
browser tests. `PLAYWRIGHT_CHROMIUM_EXECUTABLE` does the same for social-card
rendering. Neither is needed in CI. Tests use a local Astro preview server.

## Source of truth

`scripts/generate-content.mjs` reads `../skills/*/*/SKILL.md`, the installer profile
arrays in `../install.sh`, `../VERSION`, section contracts and the exact three
files in `../examples/first-run/`. It validates paths, frontmatter and profile
membership, then creates the ignored `src/data/repository.json`. Counts are never
maintained in the UI. A hash records the source inputs used for the build.

User-facing bilingual summaries live in `src/data/content.ts`; skill summaries
are keyed by actual skill IDs. Adding or removing a skill requires a corresponding
summary, and a mismatch fails the build. Source links resolve to canonical repo
files. The example preserves the source paragraphs and numbers. It is explicitly
labelled as synthetic and its expected output is not a recorded model run.

`src/lib/installation.mjs` is shared by the rendered initial state, client-side
builder and tests. It enforces profile flags and avoids a Unix shell command for
native Windows or web-only environments. File installation, live client discovery
and web account registration remain separate checks.

## Routes and progressive enhancement

Seven routes are generated in English and Chinese: Home, Workflow, Tasks,
Examples/first-revision, Skills, Install and Docs. Language switching preserves the
route and anchor. The English root is canonical. All meaningful content, source
links and the default agent installation instruction remain available without
JavaScript. JavaScript progressively adds tabs, menu, search, copy and installation
choices. Clipboard denial selects the actual text and asks for manual copying.

The Docs page links to maintained repository documents rather than duplicating
an entire documentation tree. No runtime search service is needed for 27 skills.

## Deployment

`.github/workflows/website.yml` validates the website and publishes `website/dist`
to GitHub Pages on `main`. Pull requests run checks without publishing. The
original repository CI is independent and unchanged. When enabling Pages for a
repository for the first time, **Settings → Pages → Source → GitHub Actions** may
require a maintainer action; a committed workflow is not proof of a successful
live deployment. Inspect the workflow's deployment result.

After enabling the deployment, the intended address is:
`https://boom5426.github.io/Nature-Paper-Skills/`.

## Verification scope

Before the initial main submission, local validation completed 222 deterministic
website tests, a clean Astro check, source/internal link validation and 40
in-memory rendering checks at widths 375, 768, 1024, 1440 and 1920. Eight in-memory
axe scans reported no WCAG A/AA violations in the selected categories. Source
repository regression tests ran 385 cases with six optional-dependency skips.
These local checks do not stand in for browser navigation or clipboard tests;
those run in the separate website CI, which archives its actual report and
screenshots. CI checks software behavior, not writing quality or journal acceptance.

## Maintenance boundaries

Do not copy test results, generated data, `node_modules`, reports or `dist` into
source control. The original social PNGs are versioned; their renderer is included.
Keep the installer, core skills and existing repository tests separate from visual
website work. Preserve upstream provenance and licenses, including the links in
the footer to `ATTRIBUTION.md`, `LICENSE`, `LICENSE-APACHE` and `NOTICE`.
