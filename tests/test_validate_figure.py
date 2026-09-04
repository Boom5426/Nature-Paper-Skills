"""Tests for skills/figure/nature-figure/scripts/validate_figure.py.

Two jobs:

1. Run the validator's own ``run_self_tests()`` under unittest, so the assertions
   that live beside the checks are executed by ``python3 -m unittest discover``.
2. Pin the behaviours that were repaired when the script was vendored, so a
   revert is a test failure rather than a silent loss:
   - the subscript rcParams form (``plt.rcParams['pdf.fonttype'] = 42``), which
     references/api.md mandates and which the upstream regexes could not see;
   - the multi-panel gate warning, which must name a remedy that exists;
   - the export contract of references/figure-delivery-bundle.md (PDF + PNG);
   - export paths built at run time, the references/tutorials.md idiom.

Standard library only. The validator must import on a bare interpreter with no
third-party packages, so this file must not need any either.
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path
from types import ModuleType


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills/figure/nature-figure/scripts/validate_figure.py"


def load_validator() -> ModuleType:
    """Import the validator from its path.

    Registered in ``sys.modules`` before execution because ``dataclasses`` looks
    the defining module up by name while it processes the ``Finding`` class.
    """
    spec = importlib.util.spec_from_file_location("nature_figure_validate_figure", SCRIPT)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load a module spec from {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    # Executing a module from the skill tree would drop __pycache__ into a
    # shipped directory, and install.sh copies the working tree.
    _previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = _previous
    return module


# ---------------------------------------------------------------------------
# Fixtures. Each is a minimal source that isolates one behaviour.
# ---------------------------------------------------------------------------

# references/api.md, "MANDATORY font + SVG rules": the subscript form.
SUBSCRIPT_RCPARAMS = """
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
plt.rcParams['svg.fonttype'] = 'none'
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42
plt.rcParams['font.size'] = 7
plt.rcParams['savefig.dpi'] = 600

fig, ax = plt.subplots(figsize=(7.2, 2.4))
fig.savefig("figure.pdf")
fig.savefig("figure.png")
"""

# The dict form, which already worked and must keep working.
DICT_RCPARAMS = """
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica"],
    "font.size": 7,
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "savefig.dpi": 600,
})

fig, ax = plt.subplots(figsize=(7.2, 2.4))
fig.savefig("figure.pdf")
fig.savefig("figure.png")
"""

MULTIPANEL_NO_GATE = SUBSCRIPT_RCPARAMS.replace(
    "fig, ax = plt.subplots(figsize=(7.2, 2.4))",
    "fig, axes = plt.subplots(2, 2, figsize=(7.2, 4.8))",
)

# references/figure-delivery-bundle.md: "one PDF + PNG at true print size
# (add SVG if a co-author edits panels)".
PDF_AND_PNG_ONLY = SUBSCRIPT_RCPARAMS

NO_VECTOR_AT_ALL = SUBSCRIPT_RCPARAMS.replace('fig.savefig("figure.pdf")\n', "")

# references/tutorials.md: the extension is a loop variable, so no literal
# ".svg" ever appears in the source.
RUNTIME_BUILT_EXPORT_PATHS = SUBSCRIPT_RCPARAMS.replace(
    'fig.savefig("figure.pdf")\nfig.savefig("figure.png")',
    "for ext in ('svg', 'pdf', 'png'):\n    fig.savefig(f'./figures/panel.{ext}', dpi=600)",
)


class ValidatorSelfTests(unittest.TestCase):
    """The validator's own assertions, run under unittest."""

    def test_run_self_tests_passes(self) -> None:
        load_validator().run_self_tests()

    def test_self_test_cli_exits_zero(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--self-test"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("self-test: PASS", result.stdout)


class ValidatorRegressionTests(unittest.TestCase):
    """Behaviours repaired at vendoring time. A revert must fail here."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()

    def levels(self, source: str, backend: str = "python") -> dict[str, str]:
        return {row.check_id: row.level for row in self.validator.validate_source(source, backend)}

    def finding(self, source: str, check_id: str, backend: str = "python"):
        for row in self.validator.validate_source(source, backend):
            if row.check_id == check_id:
                return row
        raise AssertionError(f"{check_id} is not among the validator's checks")

    # -- subscript-form rcParams blindness ---------------------------------

    def test_subscript_rcparams_editable_text_passes(self) -> None:
        """plt.rcParams['pdf.fonttype'] = 42 configures editable text."""
        row = self.finding(SUBSCRIPT_RCPARAMS, "EDITABLE-TEXT")
        self.assertEqual(row.level, "PASS", row)

    def test_subscript_rcparams_font_size_passes(self) -> None:
        """plt.rcParams['font.size'] = 7 is an explicit, auditable 7 pt."""
        row = self.finding(SUBSCRIPT_RCPARAMS, "FONT-SIZE")
        self.assertEqual(row.level, "PASS", row)
        self.assertEqual(self.validator.explicit_font_sizes(SUBSCRIPT_RCPARAMS), [7.0])

    def test_subscript_rcparams_dpi_passes(self) -> None:
        """plt.rcParams['savefig.dpi'] = 600 is an explicit raster resolution."""
        row = self.finding(SUBSCRIPT_RCPARAMS, "RASTER-DPI")
        self.assertEqual(row.level, "PASS", row)

    def test_dict_form_rcparams_does_not_regress(self) -> None:
        """Widening the patterns must not cost the mpl.rcParams.update({...}) form."""
        levels = self.levels(DICT_RCPARAMS)
        for check_id in ("EDITABLE-TEXT", "FONT-SIZE", "RASTER-DPI"):
            self.assertEqual(levels[check_id], "PASS", (check_id, levels))

    def test_missing_editable_text_still_fails(self) -> None:
        """The widened pattern must not turn the check into a rubber stamp."""
        source = SUBSCRIPT_RCPARAMS.replace("plt.rcParams['pdf.fonttype'] = 42\n", "")
        row = self.finding(source, "EDITABLE-TEXT")
        self.assertEqual(row.level, "FAIL", row)
        self.assertIn("pdf.fonttype=42", row.evidence)

    def test_font_size_below_floor_still_fails(self) -> None:
        source = SUBSCRIPT_RCPARAMS.replace("plt.rcParams['font.size'] = 7", "plt.rcParams['font.size'] = 4")
        row = self.finding(source, "FONT-SIZE")
        self.assertEqual(row.level, "FAIL", row)

    # -- multi-panel gate ---------------------------------------------------

    def test_multipanel_without_gate_warns_and_names_the_remedy(self) -> None:
        """A gate that blocks compliant work gets switched off; warn instead."""
        row = self.finding(MULTIPANEL_NO_GATE, "PANEL-ALIGNMENT-GATE")
        self.assertEqual(row.level, "WARN", row)
        self.assertIn("audit_panel_alignment.py", row.message)

    def test_named_remedy_script_exists(self) -> None:
        """The message must point at a script that is actually shipped."""
        remedy = SCRIPT.parent / "audit_panel_alignment.py"
        self.assertTrue(remedy.is_file(), f"the gate's remedy is missing: {remedy}")

    def test_multipanel_with_gate_passes(self) -> None:
        source = MULTIPANEL_NO_GATE + "\nrequire_matplotlib_panel_alignment(fig)\n"
        row = self.finding(source, "PANEL-ALIGNMENT-GATE")
        self.assertEqual(row.level, "PASS", row)

    # -- export contract ----------------------------------------------------

    def test_pdf_without_svg_passes_vector(self) -> None:
        """figure-delivery-bundle.md: PDF + PNG is the bundle; SVG is optional."""
        row = self.finding(PDF_AND_PNG_ONLY, "EXPORT-VECTOR")
        self.assertEqual(row.level, "PASS", row)
        self.assertIn("SVG", row.message)

    def test_png_without_tiff_passes_raster(self) -> None:
        row = self.finding(PDF_AND_PNG_ONLY, "EXPORT-RASTER")
        self.assertEqual(row.level, "PASS", row)

    def test_no_vector_export_still_fails(self) -> None:
        row = self.finding(NO_VECTOR_AT_ALL, "EXPORT-VECTOR")
        self.assertEqual(row.level, "FAIL", row)

    def test_no_raster_export_still_fails(self) -> None:
        source = SUBSCRIPT_RCPARAMS.replace('fig.savefig("figure.png")\n', "")
        row = self.finding(source, "EXPORT-RASTER")
        self.assertEqual(row.level, "FAIL", row)

    def test_runtime_built_export_paths_are_detected(self) -> None:
        """for ext in ('svg', 'pdf', 'png'): fig.savefig(f'fig.{ext}')."""
        levels = self.levels(RUNTIME_BUILT_EXPORT_PATHS)
        for check_id in ("EXPORT-VECTOR", "EXPORT-RASTER"):
            self.assertEqual(levels[check_id], "PASS", (check_id, levels))

    def test_extension_tokens_need_a_save_call(self) -> None:
        """A bare 'svg' string with nothing writing a file is not an export."""
        self.assertEqual(self.validator.saved_extension_tokens("formats = ('svg', 'pdf')\n"), set())

    def test_rcparams_key_is_not_read_as_an_export(self) -> None:
        """'svg.fonttype' is a key, not an extension."""
        tokens = self.validator.saved_extension_tokens(
            'mpl.rcParams["svg.fonttype"] = "none"\nfig.savefig("figure.pdf")\n'
        )
        self.assertNotIn("svg", tokens)


class ShippedExampleTests(unittest.TestCase):
    """Every complete plotting script the skill ships must clear the validator.

    The reference files also carry illustrative fragments (a palette dict, a
    function body). Those are not plotting sources and are out of scope here,
    so the fences are selected by the presence of a save call.
    """

    REFERENCES = ("tutorials.md", "api.md", "common-patterns.md")

    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()
        cls.refs_dir = SCRIPT.parent.parent / "references"

    @staticmethod
    def python_fences(text: str) -> list[str]:
        fences: list[str] = []
        lines = text.splitlines()
        index = 0
        while index < len(lines):
            if lines[index].strip().startswith("```python"):
                indent = len(lines[index]) - len(lines[index].lstrip())
                index += 1
                body: list[str] = []
                while index < len(lines) and lines[index].strip() != "```":
                    line = lines[index]
                    body.append(line[indent:] if not line[:indent].strip() else line)
                    index += 1
                fences.append("\n".join(body) + "\n")
            index += 1
        return fences

    def test_reference_files_are_present(self) -> None:
        for name in self.REFERENCES:
            self.assertTrue((self.refs_dir / name).is_file(), f"missing reference file: {name}")

    def test_complete_shipped_scripts_have_no_failures(self) -> None:
        checked = 0
        for name in self.REFERENCES:
            text = (self.refs_dir / name).read_text(encoding="utf-8")
            for number, fence in enumerate(self.python_fences(text), start=1):
                # A complete plotting source both configures rcParams and saves.
                # api.md's save_figure() helper does neither for a real figure.
                if "savefig(" not in fence or "rcParams" not in fence:
                    continue
                checked += 1
                failures = [
                    row for row in self.validator.validate_source(fence, "python") if row.level == "FAIL"
                ]
                self.assertEqual(failures, [], f"{name} python fence {number} was rejected: {failures}")
        self.assertGreaterEqual(checked, 4, "no complete shipped plotting script was found to check")


if __name__ == "__main__":
    unittest.main()
