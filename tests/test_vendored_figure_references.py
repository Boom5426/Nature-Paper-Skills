"""Invariants for the four reference documents vendored into nature-figure.

These files were copied in from an upstream skill that ships a 30 MB asset
bundle this repository deliberately does not distribute, and whose AI-imagery
guidance disagreed with the policy this skill already states. The failures that
introduces are silent: a link into `assets/` renders as ordinary text, and a
second, softer statement of a journal policy reads as guidance rather than as a
contradiction. Both only surface when a user follows the wrong one.

Checked here:

* the four files are present and `template-catalog.md`, which indexes the
  undistributed bundle, is not;
* every relative path they mention resolves to a file that exists in this
  repository, including paths written inside backticks;
* they carry no reference to the undistributed bundle or to upstream-only
  directories;
* `ai-graphical-abstract-workflow.md` defers the AI-imagery policy to
  `figure-delivery-bundle.md` instead of restating a graded-risk version of it;
* they do not re-state the export settings that already live in three other
  files in this skill.

No third-party dependencies: this runs on a bare Python install.
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "figure" / "nature-figure"
REFERENCES = SKILL_ROOT / "references"

VENDORED = (
    "multipanel-evidence-architecture.md",
    "nature-article-requirements.md",
    "asset-adaptation.md",
    "ai-graphical-abstract-workflow.md",
)

# Path-like tokens are only resolved when they start with one of these, so that
# prose such as `path/to/figure.pdf` or `--min-pt` is not mistaken for a claim
# that a file exists.
SKILL_RELATIVE_PREFIXES = ("references/", "scripts/", "static/")

# Strings that can only refer to material this repository does not ship.
UNDISTRIBUTED = (
    "assets/",
    "template-catalog",
    "nature-shared",
    "figures4papers/",
)

# Export settings belong to qa-contract.md, api.md and the backend fragments.
EXPORT_SETTINGS = ("svg.fonttype", "pdf.fonttype", "savefig(", "cairo_pdf(", "agg_tiff(")


def read(name: str) -> str:
    """Return a vendored file's text, or fail loudly rather than skip."""
    path = REFERENCES / name
    if not path.is_file():
        raise AssertionError(
            f"cannot check {name}: {path} does not exist. This test makes no "
            f"claim about a file it cannot read."
        )
    return path.read_text(encoding="utf-8")


def slugify(heading: str) -> str:
    slug = heading.strip().lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    return re.sub(r"[\s_]+", "-", slug).strip("-")


def markdown_link_targets(text: str) -> list[str]:
    return re.findall(r"\]\(([^)]+)\)", text)


def backticked_path_tokens(text: str) -> list[str]:
    tokens: list[str] = []
    for span in re.findall(r"`([^`\n]+)`", text):
        for token in span.split():
            # Strip trailing sentence punctuation only: stripping from the left
            # would eat the leading ".." of a relative path and silently change
            # which file the token is checked against.
            token = token.lstrip("(\"'").rstrip(",;:)\"'")
            token = token[:-1] if token.endswith(".") else token
            if token.startswith(SKILL_RELATIVE_PREFIXES) or "../" in token:
                tokens.append(token)
    return tokens


class VendoredFilesPresentTests(unittest.TestCase):
    def test_repository_layout_is_checkable(self) -> None:
        self.assertTrue(
            REFERENCES.is_dir(),
            f"cannot check anything: {REFERENCES} is missing, so this suite "
            f"verifies nothing rather than passing",
        )

    def test_the_four_vendored_files_exist(self) -> None:
        for name in VENDORED:
            with self.subTest(reference=name):
                self.assertTrue((REFERENCES / name).is_file(), f"{name} is not vendored")

    def test_asset_bundle_index_is_not_vendored(self) -> None:
        catalog = REFERENCES / "template-catalog.md"
        self.assertFalse(
            catalog.exists(),
            "template-catalog.md indexes the 30 MB asset bundle this repository "
            "does not distribute; it must not be vendored",
        )


class RelativeLinkTests(unittest.TestCase):
    def test_markdown_links_resolve(self) -> None:
        for name in VENDORED:
            text = read(name)
            for target in markdown_link_targets(text):
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                with self.subTest(reference=name, link=target):
                    resolved = (REFERENCES / target.split("#", 1)[0]).resolve()
                    self.assertTrue(
                        resolved.exists(),
                        f"{name} links to {target}, which does not exist here",
                    )

    def test_backticked_paths_resolve(self) -> None:
        for name in VENDORED:
            text = read(name)
            for token in backticked_path_tokens(text):
                with self.subTest(reference=name, path=token):
                    if "../" in token:
                        resolved = (REFERENCES / token).resolve()
                    else:
                        resolved = (SKILL_ROOT / token).resolve()
                    self.assertTrue(
                        resolved.exists(),
                        f"{name} names {token}, which does not exist in this skill",
                    )

    def test_in_page_anchors_match_a_heading(self) -> None:
        for name in VENDORED:
            text = read(name)
            slugs = {slugify(h) for h in re.findall(r"^#{2,6}\s+(.*)$", text, re.M)}
            for target in markdown_link_targets(text):
                if not target.startswith("#"):
                    continue
                with self.subTest(reference=name, anchor=target):
                    self.assertIn(
                        target[1:],
                        slugs,
                        f"{name} has a table-of-contents entry {target} with no matching heading",
                    )


class UndistributedMaterialTests(unittest.TestCase):
    def test_no_reference_to_material_this_repository_does_not_ship(self) -> None:
        for name in VENDORED:
            text = read(name)
            for needle in UNDISTRIBUTED:
                with self.subTest(reference=name, needle=needle):
                    self.assertNotIn(
                        needle,
                        text,
                        f"{name} still points at {needle}, which is not distributed here",
                    )


class AiImageryPolicyTests(unittest.TestCase):
    """The vendored workflow must not restate the AI-imagery policy itself."""

    NAME = "ai-graphical-abstract-workflow.md"

    # Wording from the upstream graded-risk framework, which contradicts
    # figure-delivery-bundle.md.
    CONTRADICTING = (
        "risk-assessment framework",
        "assistive use",
        "generative use requires",
        "interpretive or",
    )

    def test_defers_to_the_delivery_bundle(self) -> None:
        text = read(self.NAME)
        self.assertIn(
            "figure-delivery-bundle.md",
            text,
            f"{self.NAME} must name figure-delivery-bundle.md as the source of truth",
        )

    def test_does_not_restate_a_graded_risk_policy(self) -> None:
        text = read(self.NAME).lower()
        for phrase in self.CONTRADICTING:
            with self.subTest(phrase=phrase):
                self.assertNotIn(
                    phrase,
                    text,
                    f"{self.NAME} restates the upstream graded-risk policy, which "
                    f"contradicts figure-delivery-bundle.md",
                )

    def test_keeps_the_uncontested_requirements(self) -> None:
        text = read(self.NAME).lower()
        for phrase in ("access date", "internal design draft", "submission eligibility unverified"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text, f"{self.NAME} dropped a requirement that was genuinely its own")


class NoDuplicatedExportRulesTests(unittest.TestCase):
    def test_vendored_files_do_not_restate_export_settings(self) -> None:
        for name in VENDORED:
            text = read(name)
            for setting in EXPORT_SETTINGS:
                with self.subTest(reference=name, setting=setting):
                    self.assertNotIn(
                        setting,
                        text,
                        f"{name} repeats an export setting that already lives in "
                        f"qa-contract.md, api.md and the backend fragments",
                    )

    def test_each_vendored_file_points_at_something_this_skill_already_ships(self) -> None:
        siblings = {p.name for p in REFERENCES.glob("*.md")} - set(VENDORED)
        for name in VENDORED:
            text = read(name)
            with self.subTest(reference=name):
                self.assertTrue(
                    any(sibling in text for sibling in siblings),
                    f"{name} cites none of this skill's existing references, so a "
                    f"reader has no route back to the material it defers to",
                )


if __name__ == "__main__":
    unittest.main()
