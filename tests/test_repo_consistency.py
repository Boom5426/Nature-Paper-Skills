"""Invariants that keep the repository installable and internally consistent.

These exist because the failures they catch are silent. A stale skill count in a
badge, a skill listed in install.sh that no longer exists, or a routing rule that
sends a user to a skill the default install does not provide all look fine in a
diff and only surface after someone has already installed the repository.

No third-party dependencies: the frontmatter parser here handles the small subset
of YAML the skills actually use, so the suite runs on a bare Python install.
"""

import re
import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / "skills"
INSTALL_SH = REPO_ROOT / "install.sh"


def skill_paths() -> list[Path]:
    return sorted(SKILLS_ROOT.glob("*/*/SKILL.md"))


def frontmatter(path: Path) -> dict[str, str]:
    """Parse the top-level scalar keys of a SKILL.md frontmatter block."""
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if match is None:
        return {}
    fields: dict[str, str] = {}
    key = None
    for line in match.group(1).split("\n"):
        header = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)
        if header:
            key = header.group(1)
            fields[key] = header.group(2).strip()
        elif key and line.startswith(" "):
            fields[key] = (fields[key] + " " + line.strip()).strip()
    return fields


def bash_array(name: str) -> list[str]:
    """Read a simple `NAME=( ... )` array out of install.sh."""
    text = INSTALL_SH.read_text(encoding="utf-8")
    match = re.search(rf"^{name}=\((.*?)^\)", text, re.S | re.M)
    if match is None:
        return []
    return [line.strip() for line in match.group(1).split("\n") if line.strip() and not line.strip().startswith("#")]


class SkillFrontmatterTests(unittest.TestCase):
    def test_every_skill_has_parseable_frontmatter(self) -> None:
        for path in skill_paths():
            with self.subTest(skill=path.parent.name):
                self.assertNotEqual(frontmatter(path), {}, f"{path} has no frontmatter block")

    def test_frontmatter_name_matches_directory(self) -> None:
        for path in skill_paths():
            with self.subTest(skill=path.parent.name):
                self.assertEqual(
                    frontmatter(path).get("name"),
                    path.parent.name,
                    f"{path}: frontmatter name must equal the directory name, "
                    "or the agent will load it under an unexpected name",
                )

    def test_every_skill_has_a_description(self) -> None:
        for path in skill_paths():
            with self.subTest(skill=path.parent.name):
                description = frontmatter(path).get("description", "").lstrip(">-| ").strip()
                self.assertTrue(description, f"{path}: description drives skill selection and must not be empty")

    def test_descriptions_fit_the_1024_character_limit(self) -> None:
        for path in skill_paths():
            with self.subTest(skill=path.parent.name):
                description = frontmatter(path)["description"].lstrip(">-| ").strip()
                if description.startswith('"'):
                    description = json.loads(description)
                self.assertLessEqual(len(description), 1024, f"{path}: description exceeds the skill metadata limit")


class InstallerTests(unittest.TestCase):
    def test_installer_lists_only_skills_that_exist(self) -> None:
        for entry in bash_array("RECOMMENDED_SKILLS") + bash_array("FIGURE_SKILLS"):
            with self.subTest(entry=entry):
                self.assertTrue(
                    (SKILLS_ROOT / entry / "SKILL.md").is_file(),
                    f"install.sh references {entry}, which does not exist",
                )

    def test_installation_docs_match_the_recommended_set(self) -> None:
        expected = {entry.split("/", 1)[1] for entry in bash_array("RECOMMENDED_SKILLS")}
        for doc in ("docs/installation-claude.md", "docs/installation-codex.md"):
            with self.subTest(doc=doc):
                text = (REPO_ROOT / doc).read_text(encoding="utf-8")
                listed = re.search(r"<!-- recommended-skills -->(.*?)<!-- /recommended-skills -->", text, re.S)
                self.assertIsNotNone(listed, f"{doc}: could not locate the skill list")
                names = set(re.findall(r"`([a-z][a-z0-9-]+)`", listed.group(1)))
                self.assertEqual(
                    names,
                    expected,
                    f"{doc} and install.sh disagree about the recommended set",
                )


class DocumentedCountTests(unittest.TestCase):
    def test_claimed_totals_match_the_repository(self) -> None:
        total = len(skill_paths())
        patterns = [
            # The skill count now appears in a text navigation link, not a decorative badge.
            ("README.md", rf"\[🧩 {total} Skills\]\(docs/skill-map\.md\)"),
            ("README.zh-CN.md", rf"\[🧩 {total} Skills\]\(docs/skill-map\.md\)"),
            ("README.zh-CN.md", rf"{total} 个 skill"),
        ]
        for doc, pattern in patterns:
            with self.subTest(doc=doc, pattern=pattern):
                text = (REPO_ROOT / doc).read_text(encoding="utf-8")
                self.assertRegex(text, pattern, f"{doc}: stale skill count, the repository has {total}")

    def test_readme_first_screen_is_consistent(self) -> None:
        """Both READMEs retain the illustrated hero and a unified text navigation."""
        nav_labels = {
            "README.md": (
                "[🌐 Website](", "[🗺️ Workflow](", "[🚀 Quick start](",
                "[🧩 Choose a task](", "[🪄 Examples](", "[🧩 27 Skills](", "[⭐ Stars](",
            ),
            "README.zh-CN.md": (
                "[🌐 项目主页](", "[🗺️ 工作流总览](", "[🚀 快速开始](",
                "[🧩 按任务选择](", "[🪄 Examples](", "[🧩 27 Skills](", "[⭐ Stars](",
            ),
        }
        for doc, labels in nav_labels.items():
            with self.subTest(doc=doc):
                text = (REPO_ROOT / doc).read_text(encoding="utf-8")
                header = text.split("</div>", 1)[0]
                self.assertIn("# 🧬 Nature-Paper-Skills", header)
                self.assertNotIn("![", header, "Metadata links belong in the unified nav, not badges")
                self.assertIn("[⭐ Stars](https://github.com/Boom5426/Nature-Paper-Skills/stargazers)", header)
                self.assertIn("docs/skill-map.md", header)
                lines = [line for line in header.splitlines() if line.startswith(labels[0])]
                self.assertEqual(len(lines), 1, "Exactly one homepage-first navigation row")
                nav = lines[0]
                self.assertEqual(nav.count(" · "), 6, "Navigation should contain seven actions")
                positions = [nav.index(label) for label in labels]
                self.assertEqual(positions, sorted(positions), "Navigation order is fixed")
                self.assertIn("🧠", header, "Restore the five illustrated workflow themes")
                self.assertRegex(header, r"responses\. Built for|工作流。面向 Codex")
                self.assertNotRegex(header, r"responses\.  \nBuilt for|工作流。  \n面向 Codex")
                self.assertRegex(header, r"🌐 (?:\*\*English\*\*|\[English\]\(README\.md\))")

    def test_claimed_recommended_counts_match_the_installer(self) -> None:
        count = len(bash_array("RECOMMENDED_SKILLS"))
        for doc, pattern in [
            ("README.zh-CN.md", rf"推荐的 {count} 个 skill"),
            ("README.md", rf"recommended {count}-skill stack"),
            ("install.sh", rf"recommended \({count} skills\)"),
        ]:
            with self.subTest(doc=doc):
                text = (REPO_ROOT / doc).read_text(encoding="utf-8")
                self.assertRegex(text, pattern, f"{doc}: stale recommended count, install.sh installs {count}")


class SectionContractTests(unittest.TestCase):
    """Section standards live in one file; specialists point to it rather than restating it.

    A renamed or deleted contract would leave every pointer dangling without any diff showing it.
    """

    CONTRACT = SKILLS_ROOT / "core/paper-workflow/references/section-contracts.md"
    EVIDENCE = SKILLS_ROOT / "core/paper-workflow/references/section-evidence.md"
    POINTERS = (
        "core/manuscript-optimizer/SKILL.md",
        "core/write-scientific-manuscript/SKILL.md",
        "core/write-scientific-manuscript/references/section-logic.md",
        "core/scientific-writing/SKILL.md",
        "venue/nature-portfolio-playbook/SKILL.md",
    )

    def test_contract_and_evidence_are_linked_from_the_dispatcher(self) -> None:
        dispatcher = (SKILLS_ROOT / "core/paper-workflow/SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(self.CONTRACT.is_file())
        self.assertIn("references/section-contracts.md", dispatcher)
        self.assertTrue(self.EVIDENCE.is_file())
        self.assertIn("(section-evidence.md)", self.CONTRACT.read_text(encoding="utf-8"))

    def test_specialists_point_to_the_contract_in_a_default_skill(self) -> None:
        self.assertIn("core/paper-workflow", bash_array("RECOMMENDED_SKILLS"))
        for rel in self.POINTERS:
            text = (SKILLS_ROOT / rel).read_text(encoding="utf-8")
            with self.subTest(rel=rel):
                self.assertIn("`paper-workflow`", text)
                self.assertIn("references/section-contracts.md", text)

    def test_evidence_names_its_reproduction_script(self) -> None:
        self.assertIn("scripts/section_corpus.py", self.EVIDENCE.read_text(encoding="utf-8"))
        self.assertTrue((REPO_ROOT / "scripts/section_corpus.py").is_file())


class RoutingReachabilityTests(unittest.TestCase):
    """A default install must not route the user to a skill it did not install.

    Naming an uninstalled skill is allowed, but the same file must say where to
    get it, otherwise the user follows the instruction into a dead end.
    """

    AVAILABILITY_HINTS = (
        "--figure",
        "--set all",
        "figure stack",
        "Figure Stack",
        "optional set",
        "not installed",
        "not in the default recommended set",
        "once installed",
    )

    def test_references_to_non_default_skills_say_how_to_get_them(self) -> None:
        all_skills = {path.parent.name for path in skill_paths()}
        default = {entry.split("/", 1)[1] for entry in bash_array("RECOMMENDED_SKILLS")}
        missing_report: list[str] = []

        for name in sorted(default):
            skill_dir = next(p.parent for p in skill_paths() if p.parent.name == name)
            for doc in sorted(skill_dir.rglob("*.md")):
                text = doc.read_text(encoding="utf-8")
                referenced = {m.group(1) for m in re.finditer(r"`([a-z][a-z0-9]+(?:-[a-z0-9]+)+)`", text)}
                unavailable = (referenced & all_skills) - default
                if unavailable and not any(hint in text for hint in self.AVAILABILITY_HINTS):
                    rel = doc.relative_to(REPO_ROOT)
                    missing_report.append(f"{rel} points at {sorted(unavailable)} with no install hint")

        self.assertEqual(missing_report, [], "\n" + "\n".join(missing_report))


if __name__ == "__main__":
    unittest.main()
