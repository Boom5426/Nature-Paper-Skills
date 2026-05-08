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

    def test_reports_when_no_references_are_found(self) -> None:
        result = self.run_script("This paragraph has no figure citation.\n")

        self.assertEqual(result.returncode, 0)
        self.assertIn("No figure references found.", result.stdout)

    def test_does_not_treat_following_words_as_panel_letters(self) -> None:
        result = self.run_script("Supplementary Fig. 3 is cited for completeness.\n")

        self.assertEqual(result.returncode, 0)
        self.assertIn("Supplementary Fig. 3: mentions=1, whole_figure_refs=1, panels=-", result.stdout)


if __name__ == "__main__":
    unittest.main()
