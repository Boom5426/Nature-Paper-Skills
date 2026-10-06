"""Verify project initialization preserves existing files and rejects conflicts."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT/'skills/core/paper-bootstrap/scripts/init_paper_layout.py'


class PaperBootstrapTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.root = self.base/'paper'
        self.addCleanup(self.temp.cleanup)

    def run_script(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), str(self.root), *args],
                              capture_output=True, text=True)

    def test_new_layout_is_created_and_existing_notes_preserved(self):
        first = self.run_script()
        self.assertEqual(first.returncode, 0, first.stderr)
        note = self.root/'notes/project_truth.md'
        note.write_text('Custom truth')
        second = self.run_script()
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(note.read_text(), 'Custom truth')
        self.assertTrue((self.root/'output/review').is_dir())

    def test_dangling_link_is_rejected_before_any_creation(self):
        (self.root/'notes').mkdir(parents=True)
        outside = self.base/'external.md'
        link = self.root/'notes/project_truth.md'
        link.symlink_to(outside)
        for flags in ((), ('--dry-run',)):
            with self.subTest(flags=flags):
                result = self.run_script(*flags)
                self.assertEqual(result.returncode, 2)
                self.assertIn('linked project entry', result.stderr)
                self.assertFalse(outside.exists())
                self.assertTrue(link.is_symlink())
                self.assertFalse((self.root/'input').exists())

    def test_live_linked_parent_is_not_followed(self):
        self.root.mkdir()
        outside = self.base/'external-notes'
        outside.mkdir()
        (self.root/'notes').symlink_to(outside, target_is_directory=True)
        result = self.run_script()
        self.assertEqual(result.returncode, 2)
        self.assertEqual(list(outside.iterdir()), [])
        self.assertFalse((self.root/'input').exists())

    def test_wrong_types_fail_before_creating_other_entries(self):
        for rel, directory in [('input', False), ('output', False), ('notes/project_truth.md', True)]:
            with self.subTest(rel=rel):
                target = self.root/rel
                target.parent.mkdir(parents=True, exist_ok=True)
                if directory:
                    target.mkdir()
                else:
                    target.write_text('Keep me')
                result = self.run_script()
                self.assertEqual(result.returncode, 2)
                self.assertIn('Expected a', result.stderr)
                self.assertFalse((self.root/'figures').exists())
                if not directory:
                    self.assertEqual(target.read_text(), 'Keep me')
                if directory:
                    target.rmdir()
                else:
                    target.unlink()

    def test_dry_run_does_not_create_root(self):
        result = self.run_script('--dry-run')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.root.exists())

    def test_root_below_a_file_fails_in_dry_run_too(self):
        blocker = self.base/'blocker'
        blocker.write_text('Keep me')
        self.root = blocker/'paper'
        result = self.run_script('--dry-run')
        self.assertEqual(result.returncode, 2)
        self.assertIn('not a directory', result.stderr)
        self.assertEqual(blocker.read_text(), 'Keep me')

    def test_explicit_linked_root_remains_supported(self):
        actual = self.base/'actual'
        actual.mkdir()
        self.root.symlink_to(actual, target_is_directory=True)
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(self.root.is_symlink())
        self.assertTrue((actual/'notes/project_truth.md').is_file())
