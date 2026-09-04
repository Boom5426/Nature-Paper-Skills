"""Guard the Apache-2.0 obligations that `install.sh` and `ATTRIBUTION.md` carry.

`install.sh` distributes a skill directory on its own, without the repository root,
so a skill holding Apache-2.0 material must ship the licence text and the NOTICE
beside it (Apache-2.0 sections 4(a) and 4(d)). The section 4(b) modified-file list
lives in `ATTRIBUTION.md` between machine-readable markers so this test can read it.

Standard library only: the CI runner has no third-party packages.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INSTALL = ROOT / "install.sh"
ATTRIBUTION = ROOT / "ATTRIBUTION.md"
VENDORED = ROOT / "skills" / "figure" / "nature-figure"

BEGIN = "<!-- APACHE-MODIFIED-FILES:BEGIN -->"
END = "<!-- APACHE-MODIFIED-FILES:END -->"


def bash_array(name: str) -> list[str]:
    """Read a simple one-entry-per-line bash array out of install.sh."""
    text = INSTALL.read_text()
    match = re.search(rf"^{name}=\((.*?)^\)", text, re.S | re.M)
    if match is None:
        raise AssertionError(f"{name} not found in install.sh")
    return [line.strip() for line in match.group(1).splitlines() if line.strip()]


def declared_apache_skills() -> list[str]:
    """Skills whose SKILL.md frontmatter declares Apache-2.0."""
    found = []
    for skill in sorted((ROOT / "skills").glob("*/*/SKILL.md")):
        if re.search(r"^license:\s*Apache-2\.0\s*$", skill.read_text(), re.M):
            found.append(f"{skill.parent.parent.name}/{skill.parent.name}")
    return found


class TestLicenseShipping(unittest.TestCase):
    def test_license_files_exist_at_root(self):
        for name in ("LICENSE", "LICENSE-APACHE", "NOTICE", "ATTRIBUTION.md"):
            self.assertTrue((ROOT / name).is_file(), f"{name} missing from the repository root")

    def test_every_declared_apache_skill_ships_the_licence(self):
        shipped = set(bash_array("APACHE_SKILLS"))
        for rel in declared_apache_skills():
            self.assertIn(
                rel,
                shipped,
                f"{rel} declares license: Apache-2.0 but install.sh would not ship "
                "LICENSE-APACHE/NOTICE with it; add it to APACHE_SKILLS",
            )

    def test_apache_skills_entries_exist(self):
        for rel in bash_array("APACHE_SKILLS"):
            self.assertTrue(
                (ROOT / "skills" / rel).is_dir(),
                f"install.sh APACHE_SKILLS names {rel}, which is not a skill directory",
            )

    def test_installer_copies_the_licence_and_prunes_bytecode(self):
        text = INSTALL.read_text()
        self.assertIn('cp "$SOURCE_DIR/LICENSE-APACHE"', text)
        self.assertIn('cp "$SOURCE_DIR/NOTICE"', text)
        self.assertIn("__pycache__", text, "installs would ship gitignored bytecode")

    def test_third_party_notice_present_and_referenced(self):
        notice = VENDORED / "THIRD_PARTY_NOTICES.md"
        self.assertTrue(notice.is_file(), "restored third-party notice is missing")
        self.assertIn("THIRD_PARTY_NOTICES.md", ATTRIBUTION.read_text())

    def test_section_4b_list_matches_the_tree(self):
        text = ATTRIBUTION.read_text()
        self.assertIn(BEGIN, text)
        self.assertIn(END, text)
        block = text.split(BEGIN, 1)[1].split(END, 1)[0]

        # The block holds three labelled lists. Parse them by their headings so
        # adding a fourth cannot silently fold into the one before it.
        sections = {}
        current = None
        for line in block.splitlines():
            heading = re.match(r"^(Modified|Removed|Added)[^(]*\((\d+) (?:files|entries)\)", line)
            if heading:
                current = heading.group(1)
                sections[current] = {"stated": int(heading.group(2)), "entries": []}
                continue
            entry = re.match(r"^- `([^`]+)`$", line)
            if entry and current:
                sections[current]["entries"].append(entry.group(1))

        for label in ("Modified", "Removed", "Added"):
            self.assertIn(label, sections, f"the 4(b) block has no {label} list")
            self.assertEqual(
                sections[label]["stated"],
                len(sections[label]["entries"]),
                f"the {label} list says {sections[label]['stated']} but holds "
                f"{len(sections[label]['entries'])}",
            )

        self.assertGreater(len(sections["Modified"]["entries"]), 20, "Modified list looks truncated")

        for entry in sections["Modified"]["entries"] + sections["Added"]["entries"]:
            self.assertTrue(
                (VENDORED / entry).exists(),
                f"ATTRIBUTION lists {entry} as present but it is not in the skill",
            )
        # The reverse direction matters more than it looks: restoring a dropped
        # upstream file without striking it from the Removed list republishes a
        # false notice, and every other assertion here would still pass.
        for entry in sections["Removed"]["entries"]:
            self.assertFalse(
                (VENDORED / entry).exists(),
                f"ATTRIBUTION lists {entry} as removed but it is present; "
                "move it to the modified list",
            )


if __name__ == "__main__":
    unittest.main()
