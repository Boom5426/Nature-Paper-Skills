import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills/core/submission-audit/scripts/check_figure_refs.py"


class CheckFigureRefsCliTests(unittest.TestCase):
    def run_script(self, text: str) -> subprocess.CompletedProcess[str]:
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as handle:
            handle.write(text)
            temp_path = Path(handle.name)

        self.addCleanup(temp_path.unlink)
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(temp_path)],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_reports_extended_data_panels(self) -> None:
        result = self.run_script("Extended Data Fig. 2a-c supports the control analysis.\n")

        self.assertEqual(result.returncode, 0)
        self.assertIn("Extended Data Fig. 2: mentions=1, whole_figure_refs=0, panels=a,b,c", result.stdout)

    def test_reports_spelled_out_figure_references(self) -> None:
        result = self.run_script(
            "Figure 5a shows the main effect. Extended Data Figure 3b supports it.\n"
        )

        self.assertEqual(result.returncode, 0)
        self.assertIn("Fig. 5: mentions=1, whole_figure_refs=0, panels=a", result.stdout)
        self.assertIn("Extended Data Fig. 3: mentions=1, whole_figure_refs=0, panels=b", result.stdout)

    def test_reports_each_figure_in_plural_references(self) -> None:
        result = self.run_script("Figs. 6a and 7b agree.\n")

        self.assertEqual(result.returncode, 0)
        self.assertIn("Fig. 6: mentions=1, whole_figure_refs=0, panels=a", result.stdout)
        self.assertIn("Fig. 7: mentions=1, whole_figure_refs=0, panels=b", result.stdout)

    def test_expands_en_dash_panel_ranges(self) -> None:
        result = self.run_script("Fig. 8a–c covers the ablation.\n")

        self.assertEqual(result.returncode, 0)
        self.assertIn("Fig. 8: mentions=1, whole_figure_refs=0, panels=a,b,c", result.stdout)

    def test_reports_when_no_references_are_found(self) -> None:
        result = self.run_script("This paragraph has no figure citation.\n")

        self.assertEqual(result.returncode, 0)
        self.assertIn("No figure references found.", result.stdout)

    def test_does_not_treat_following_words_as_panel_letters(self) -> None:
        result = self.run_script("Supplementary Fig. 3 is cited for completeness.\n")

        self.assertEqual(result.returncode, 0)
        self.assertIn("Supplementary Fig. 3: mentions=1, whole_figure_refs=1, panels=-", result.stdout)

    def test_whitespace_does_not_change_figure_category(self):
        for prefix in ('Extended  Data', 'Extended\tData', 'Extended\nData'):
            with self.subTest(prefix=prefix):
                result = self.run_script(prefix + ' Figure 2a.')
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn('Extended Data Fig. 2:', result.stdout)
                self.assertFalse(result.stdout.startswith('Fig. 2:'))

    def test_wrapped_list_keeps_all_figures(self):
        result = self.run_script('Figs. 6a and\n7b.')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Fig. 6:', result.stdout)
        self.assertIn('Fig. 7:', result.stdout)

    def test_numeric_ranges_and_lists_expand(self):
        result = self.run_script('Figs. 1–3 and 5; Supplementary Figures 7-8.')
        self.assertEqual(result.returncode, 0, result.stderr)
        for num in (1, 2, 3, 5):
            self.assertIn(f'Fig. {num}: mentions=1, whole_figure_refs=1', result.stdout)
        for num in (7, 8):
            self.assertIn(f'Supplementary Fig. {num}:', result.stdout)

    def test_panel_continuations_keep_one_mention(self):
        for phrase in ('Fig. 1a,b,c', 'Fig. 1a, b and c', 'Fig. 1A, B–D'):
            with self.subTest(phrase=phrase):
                result = self.run_script(phrase + '.')
                self.assertEqual(result.returncode, 0, result.stderr)
                panels = 'a,b,c,d' if 'D' in phrase else 'a,b,c'
                self.assertIn(f'Fig. 1: mentions=1, whole_figure_refs=0, panels={panels}', result.stdout)

    def test_invalid_ranges_cannot_report_complete_scan(self):
        for phrase in ('Fig. 1c-a', 'Figs. 3-1', 'Fig. 1a-2c', 'Fig. 1a-c-e'):
            with self.subTest(phrase=phrase):
                result = self.run_script(phrase)
                self.assertEqual(result.returncode, 1)
                self.assertIn('incomplete', result.stderr)

    def test_prose_after_comma_or_and_is_not_a_panel(self):
        result = self.run_script('Fig. 1a, because the effect persists. Fig. 2 and controls agree.')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Fig. 1: mentions=1, whole_figure_refs=0, panels=a', result.stdout)
        self.assertIn('Fig. 2: mentions=1, whole_figure_refs=1, panels=-', result.stdout)


if __name__ == "__main__":
    unittest.main()
