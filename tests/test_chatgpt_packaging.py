"""Exercise web bundles as archives, including resources and existing-output safety."""
import importlib.util
import json
from pathlib import Path
import re
import stat
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("build_chatgpt_plugin", ROOT / "scripts/build_chatgpt_plugin.py")
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


class TestChatGPTPackaging(unittest.TestCase):
    def build(self, folder, **kwargs):
        return builder.build(ROOT, Path(folder), **kwargs)

    def test_recommended_plugin_archive_and_marketplace(self):
        with tempfile.TemporaryDirectory() as temp:
            result = self.build(Path(temp) / "new")
            self.assertEqual(result["skill_count"], 19)
            catalog = json.loads((Path(result["marketplace_root"]) / ".agents/plugins/marketplace.json").read_text())
            plugin = Path(result["marketplace_root"]) / catalog["plugins"][0]["source"]["path"]
            self.assertEqual(plugin, Path(result["plugin"]))
            with zipfile.ZipFile(result["zip"]) as archive:
                names = archive.namelist()
                self.assertIsNone(archive.testzip())
                self.assertIn("plugin.json", names)
                self.assertIn(".codex-plugin/plugin.json", names)
                skills = [n for n in names if re.fullmatch(r"skills/[^/]+/SKILL.md", n)]
                self.assertEqual(len(skills), 19)
                self.assertIn("skills/rebuttal-response/SKILL.md", skills)
                self.assertIn("skills/paper-reviewer/SKILL.md", skills)
                self.assertNotIn(".agents/plugins/marketplace.json", names)
                for name in names:
                    self.assertNotIn("..", Path(name).parts)
                    self.assertFalse(name.startswith("/"))
                    self.assertTrue(stat.S_ISREG(archive.getinfo(name).external_attr >> 16))
                portable = json.loads(archive.read("plugin.json"))
                compatibility = json.loads(archive.read(".codex-plugin/plugin.json"))
                self.assertEqual(portable["name"], compatibility["name"])
                self.assertEqual(portable["version"], compatibility["version"])
                self.assertEqual(compatibility["skills"], "./skills/")
                self.assertEqual(portable["extensions"]["com.openai"]["interface"], compatibility["interface"])
                self.assertNotIn("mcpServers", compatibility)
                self.assertNotIn("apps", compatibility)
                self.assertNotIn(".mcp.json", names)

    def test_one_entry_web_skill_keeps_specialist_resources(self):
        with tempfile.TemporaryDirectory() as temp:
            result = self.build(Path(temp) / "new")
            with zipfile.ZipFile(result["web_skill_zip"]) as archive:
                names = archive.namelist()
                entry = archive.read("SKILL.md").decode()
                self.assertIn("name: nature-paper-workflow", entry)
                self.assertIn("resources/paper-workflow/SKILL.md", entry)
                self.assertNotIn("plugin.json", names)
                self.assertEqual(archive.read("resources/paper-workflow/SKILL.md"),
                                 (ROOT / "skills/core/paper-workflow/SKILL.md").read_bytes())
                self.assertEqual(archive.read("resources/rebuttal-response/references/final-audit.md"),
                                 (ROOT / "skills/core/rebuttal-response/references/final-audit.md").read_bytes())
                index = archive.read("references/bundled-skills.md").decode()
                links = re.findall(r"\]\(\.\./([^)]*)\)", index)
                self.assertEqual(len(links), 19)
                for link in links:
                    self.assertIn(link, names)
                for filename in ("LICENSE", "LICENSE-APACHE", "NOTICE", "ATTRIBUTION.md"):
                    self.assertIn(filename, names)
                import hashlib
                info = json.loads(archive.read("build-info.json"))
                self.assertEqual(info["entry_skill"], "nature-paper-workflow")
                for name, digest in info["files"].items():
                    self.assertEqual(hashlib.sha256(archive.read(name)).hexdigest(), digest)
                    self.assertEqual((Path(result["web_skill"]) / name).read_bytes(), archive.read(name))

    def test_all_profile_keeps_data_scripts_templates_and_licenses(self):
        with tempfile.TemporaryDirectory() as temp:
            result = self.build(Path(temp) / "new", profile="all")
            self.assertEqual(result["skill_count"], 27)
            expected = {
                "results-analysis/scripts/example_statistics.py": "research/results-analysis/scripts/example_statistics.py",
                "results-analysis/examples/usage-runs.csv": "research/results-analysis/examples/usage-runs.csv",
                "conference-paper-writing/templates/icml2026/icml2026.sty": "optional/conference-paper-writing/templates/icml2026/icml2026.sty",
                "nature-figure/THIRD_PARTY_NOTICES.md": "figure/nature-figure/THIRD_PARTY_NOTICES.md",
            }
            with zipfile.ZipFile(result["zip"]) as plugin, zipfile.ZipFile(result["web_skill_zip"]) as skill:
                for dest, source in expected.items():
                    data = (ROOT / "skills" / source).read_bytes()
                    self.assertEqual(plugin.read("skills/" + dest), data)
                    self.assertEqual(skill.read("resources/" + dest), data)
                for source in builder.installer_array(ROOT, "APACHE_SKILLS"):
                    name = Path(source).name
                    for license_name in ("LICENSE-APACHE", "NOTICE"):
                        data = (ROOT / license_name).read_bytes()
                        self.assertEqual(plugin.read(f"skills/{name}/{license_name}"), data)
                        self.assertEqual(skill.read(f"resources/{name}/{license_name}"), data)
                self.assertLess(Path(result["zip"]).stat().st_size, 100_000_000)

    def test_figure_addon_reuses_installer_selection(self):
        with tempfile.TemporaryDirectory() as temp:
            result = self.build(Path(temp) / "new", figure=True)
            self.assertEqual(result["skill_count"], 21)
            with zipfile.ZipFile(result["web_skill_zip"]) as archive:
                self.assertIn("resources/nature-figure/SKILL.md", archive.namelist())
                self.assertIn("resources/figure-style/SKILL.md", archive.namelist())
            self.assertTrue(result["web_skill_zip"].endswith("-recommended-figure.zip"))

    def test_existing_directory_file_and_broken_link_are_preserved(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            directory = root / "existing"
            directory.mkdir()
            sentinel = directory / "keep.txt"
            sentinel.write_text("keep this result")
            file = root / "file"
            file.write_text("keep this file")
            paths = [directory, file]
            link = root / "link"
            try:
                link.symlink_to(root / "missing", target_is_directory=True)
            except OSError:
                pass
            else:
                paths.append(link)
            for path in paths:
                with self.subTest(path=path.name):
                    with self.assertRaisesRegex(ValueError, "Output already exists"):
                        self.build(path)
            self.assertEqual(sentinel.read_text(), "keep this result")
            self.assertEqual(file.read_text(), "keep this file")
            if link in paths:
                self.assertTrue(link.is_symlink())

    def test_invalid_version_leaves_no_output(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "new"
            with self.assertRaisesRegex(ValueError, "semantic version"):
                self.build(output, version="../bad")
            self.assertFalse(output.exists())

    def test_resources_exclude_bytecode_and_reject_links(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "SKILL.md").write_text("real resource")
            (root / "__pycache__").mkdir()
            (root / "__pycache__/cache.pyc").write_bytes(b"bytecode")
            (root / "cache.pyo").write_bytes(b"bytecode")
            self.assertEqual([rel for _, rel in builder.resource_files(root)], ["SKILL.md"])
            try:
                (root / "link.md").symlink_to(root / "SKILL.md")
            except OSError:
                return
            with self.assertRaisesRegex(ValueError, "symlinks"):
                list(builder.resource_files(root))

    def test_archive_is_reproducible_and_records_resource_hashes(self):
        import hashlib
        manifest, payload, selected = builder.package_plan(ROOT)
        self.assertEqual(builder.archive_bytes(payload), builder.archive_bytes(payload))
        info = json.loads(payload["build-info.json"][0])
        self.assertEqual(len(selected), len(info["skills"]))
        for rel, digest in info["files"].items():
            self.assertEqual(hashlib.sha256(payload[rel][0]).hexdigest(), digest)
        self.assertEqual(info["repository"], manifest["repository"])

    def test_plugin_metadata_and_icons_meet_documented_basics(self):
        manifest, payload, _ = builder.package_plan(ROOT)
        interface = manifest["extensions"]["com.openai"]["interface"]
        self.assertLessEqual(len(interface["shortDescription"]), 30)
        self.assertLessEqual(len(interface["longDescription"]), 4000)
        for prompt in interface["defaultPrompt"]:
            self.assertLessEqual(len(prompt), 128)
        for field in ("composerIcon", "logo"):
            icon = ET.fromstring(payload[interface[field][2:]][0])
            self.assertEqual(icon.tag, "{http://www.w3.org/2000/svg}svg")
            self.assertEqual(icon.attrib["width"], icon.attrib["height"])
            self.assertGreaterEqual(int(icon.attrib["width"]), 48)


if __name__ == "__main__":
    unittest.main()
