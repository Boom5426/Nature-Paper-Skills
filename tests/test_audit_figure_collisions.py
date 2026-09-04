"""Tests for skills/figure/nature-figure/scripts/audit_figure_collisions.py.

Everything here runs on a bare interpreter: the geometry core is pure standard
library, and the PyMuPDF-dependent path is exercised by *blocking* the import,
so the NOT RUN state is tested identically whether or not PyMuPDF happens to be
installed on the machine running the tests.
"""

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "skills/figure/nature-figure/scripts/audit_figure_collisions.py"


def load_module():
    """Import the script by path without leaving a __pycache__ next to it."""
    spec = importlib.util.spec_from_file_location("audit_figure_collisions_under_test", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    # Register before exec: dataclasses resolves annotations through sys.modules.
    sys.modules[spec.name] = module
    previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = previous
    return module


audit = load_module()


def blocked_pymupdf_env() -> tuple[str, dict[str, str]]:
    """Return (directory, env) whose PYTHONPATH makes PyMuPDF unimportable.

    The caller removes the directory; importing a stub leaves a __pycache__ in
    it, so it must be removed as a tree.
    """
    directory = tempfile.mkdtemp(prefix="no-pymupdf-")
    for name in ("pymupdf", "fitz"):
        Path(directory, f"{name}.py").write_text(
            f'raise ImportError("{name} is blocked by the test harness")\n', encoding="utf-8"
        )
    env = dict(os.environ)
    env["PYTHONPATH"] = directory + os.pathsep + env.get("PYTHONPATH", "")
    return directory, env


class GeometryCoreTests(unittest.TestCase):
    """The stdlib geometry core: rectangles, segments, and the audit verdicts."""

    def test_rect_helpers(self) -> None:
        self.assertEqual(audit.normalize_rect((10, 20, 4, 5)), (4, 5, 10, 20))
        self.assertEqual(audit.rect_intersection((0, 0, 10, 10), (5, 5, 20, 20)), (5, 5, 10, 10))
        self.assertIsNone(audit.rect_intersection((0, 0, 10, 10), (10, 10, 20, 20)))
        self.assertAlmostEqual(
            audit.rect_overlap_ratio((0, 0, 10, 10), (5, 0, 15, 10)), 0.5
        )
        self.assertEqual(audit.rect_overlap_ratio((0, 0, 10, 10), (30, 30, 40, 40)), 0.0)
        self.assertTrue(audit.rect_contains((0, 0, 10, 10), (2, 2, 8, 8)))
        self.assertFalse(audit.rect_contains((0, 0, 10, 10), (2, 2, 12, 8)))
        self.assertEqual(audit.union_rects([(0, 1, 2, 3), (5, 0, 6, 9)]), (0, 0, 6, 9))
        self.assertIsNone(audit.union_rects([]))

    def test_rect_inset_is_capped_so_thin_boxes_do_not_invert(self) -> None:
        # A 40x8 text box may only be inset by 20% of its short side (1.6 pt).
        self.assertEqual(audit.rect_inset((0, 0, 40, 8), 5.0), (1.6, 1.6, 38.4, 6.4))

    def test_segment_intersects_rect(self) -> None:
        box = (10, 10, 20, 20)
        self.assertTrue(audit.segment_intersects_rect(((0, 15), (30, 15)), box))
        self.assertTrue(audit.segment_intersects_rect(((15, 15), (16, 16)), box))
        self.assertFalse(audit.segment_intersects_rect(((0, 30), (30, 30)), box))
        self.assertFalse(audit.segment_intersects_rect(((0, 0), (5, 5)), box))

    def test_clean_page_passes(self) -> None:
        page = audit.PageGeometry(
            page=1,
            bbox=(0, 0, 200, 120),
            texts=[audit.TextBox(0, "Clear", (50, 20, 90, 32))],
            traces=[audit.TraceBox(0, "Clear", (50, 20, 90, 32))],
            strokes=[audit.StrokePath(0, (20, 70, 180, 70), 1.0, (((20, 70), (180, 70)),))],
        )
        result = audit.audit_geometries([page])
        self.assertEqual(result["verdict"], "PASS")
        self.assertEqual(result["status"], "RAN")
        self.assertEqual(result["checks_run"], list(audit.CHECK_NAMES))
        self.assertEqual(result["checks_not_run"], [])
        self.assertEqual(audit.exit_code(result), audit.EXIT_PASS)

    def test_overlapping_text_boxes_fail(self) -> None:
        page = audit.PageGeometry(
            page=1,
            bbox=(0, 0, 200, 120),
            texts=[
                audit.TextBox(0, "Baseline-A", (100, 40, 150, 50)),
                audit.TextBox(1, "AUROC", (120, 40, 170, 50)),
            ],
            traces=[audit.TraceBox(0, "Baseline-A", (100, 40, 150, 50))],
        )
        result = audit.audit_geometries([page])
        self.assertEqual(result["verdict"], "FIX BEFORE DELIVERY")
        self.assertEqual(result["findings"][0]["kind"], "text-text")
        self.assertEqual(result["findings"][0]["other_text"], "AUROC")
        self.assertEqual(audit.exit_code(result), audit.EXIT_FAIL)

    def test_text_crossed_by_stroke_fails(self) -> None:
        page = audit.PageGeometry(
            page=1,
            bbox=(0, 0, 200, 120),
            texts=[audit.TextBox(0, "Crossed", (50, 40, 100, 54))],
            traces=[audit.TraceBox(0, "Crossed", (50, 40, 100, 54))],
            strokes=[audit.StrokePath(0, (20, 47, 180, 47), 1.0, (((20, 47), (180, 47)),))],
        )
        result = audit.audit_geometries([page])
        self.assertEqual(result["findings"][0]["kind"], "text-stroke")
        self.assertEqual(audit.exit_code(result), audit.EXIT_FAIL)

    def test_text_fully_inside_a_fill_is_reported_as_intentional(self) -> None:
        page = audit.PageGeometry(
            page=1,
            bbox=(0, 0, 200, 120),
            texts=[audit.TextBox(0, "Inside", (60, 40, 90, 52))],
            traces=[audit.TraceBox(0, "Inside", (60, 40, 90, 52))],
            fills=[audit.FilledRegion(0, (50, 30, 100, 60), "fill")],
        )
        result = audit.audit_geometries([page])
        self.assertEqual(result["verdict"], "PASS")
        self.assertEqual(result["summary"]["contained_fill_overlays"], 1)

    def test_text_on_a_fill_edge_warns_only(self) -> None:
        page = audit.PageGeometry(
            page=1,
            bbox=(0, 0, 200, 120),
            texts=[audit.TextBox(0, "Edge", (90, 40, 130, 52))],
            traces=[audit.TraceBox(0, "Edge", (90, 40, 130, 52))],
            fills=[audit.FilledRegion(0, (50, 30, 100, 60), "fill")],
        )
        result = audit.audit_geometries([page])
        self.assertEqual(result["verdict"], "REVIEW REQUIRED")
        self.assertEqual(result["findings"][0]["severity"], "WARN")
        self.assertEqual(audit.exit_code(result), audit.EXIT_PASS)
        self.assertEqual(audit.exit_code(result, strict=True), audit.EXIT_FAIL)

    def test_text_outside_the_page_fails(self) -> None:
        page = audit.PageGeometry(
            page=1,
            bbox=(0, 0, 200, 120),
            texts=[audit.TextBox(0, "Clipped", (185, 40, 260, 52))],
            traces=[audit.TraceBox(0, "Clipped", (185, 40, 260, 52))],
        )
        result = audit.audit_geometries([page])
        kinds = {finding["kind"] for finding in result["findings"]}
        self.assertIn("text-page-clipping", kinds)
        self.assertEqual(audit.exit_code(result), audit.EXIT_FAIL)

    def test_page_without_text_is_not_auditable(self) -> None:
        result = audit.audit_geometries([audit.PageGeometry(page=1, bbox=(0, 0, 200, 120))])
        self.assertEqual(result["verdict"], "NOT AUDITABLE")
        self.assertEqual(audit.exit_code(result), audit.EXIT_NOT_AUDITABLE)

    def test_self_test_runs_on_this_interpreter(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--self-test"],
            check=False, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("self-test: PASS", result.stdout)


class NotRunStateTests(unittest.TestCase):
    """A check that could not run must never be readable as a check that passed."""

    def test_exit_codes_are_all_distinct(self) -> None:
        codes = [audit.EXIT_PASS, audit.EXIT_FAIL, audit.EXIT_ERROR,
                 audit.EXIT_NOT_RUN, audit.EXIT_NOT_AUDITABLE]
        self.assertEqual(len(set(codes)), len(codes), codes)

    def test_install_hint_is_a_direct_pip_command(self) -> None:
        self.assertEqual(
            audit.PYMUPDF_INSTALL_HINT,
            'python -m pip install "PyMuPDF>=1.24.0,<2.0.0"',
        )
        # The repository has no requirements.txt to point at.
        self.assertNotIn("requirements.txt", SCRIPT.read_text(encoding="utf-8"))

    def test_not_run_result_reports_the_blocker_and_names_the_skipped_checks(self) -> None:
        exc = audit.DependencyMissing("PyMuPDF", "reading rendered PDF geometry",
                                      audit.PYMUPDF_INSTALL_HINT)
        result = audit.not_run_result(Path("figure.pdf"), exc)
        self.assertEqual(result["status"], "NOT RUN")
        self.assertEqual(result["verdict"], "NOT RUN")
        self.assertEqual(result["checks_run"], [])
        self.assertEqual(result["checks_not_run"], list(audit.CHECK_NAMES))
        self.assertEqual(result["blockers"][0]["package"], "PyMuPDF")
        self.assertEqual(result["blockers"][0]["install"], audit.PYMUPDF_INSTALL_HINT)
        self.assertEqual(audit.exit_code(result), audit.EXIT_NOT_RUN)
        self.assertNotIn(audit.exit_code(result), (audit.EXIT_PASS, audit.EXIT_FAIL))

    def test_not_run_counts_are_null_not_zero(self) -> None:
        exc = audit.DependencyMissing("PyMuPDF", "reading rendered PDF geometry",
                                      audit.PYMUPDF_INSTALL_HINT)
        result = audit.not_run_result(Path("figure.pdf"), exc)
        for key in ("fail", "warn", "contained_fill_overlays", "contained_image_overlays"):
            self.assertIsNone(result["summary"][key], key)
        self.assertIsNone(result["page_count"])
        self.assertIsNone(result["auditable"])

    def test_not_run_text_says_it_is_not_a_pass(self) -> None:
        exc = audit.DependencyMissing("PyMuPDF", "reading rendered PDF geometry",
                                      audit.PYMUPDF_INSTALL_HINT)
        rendered = audit.render_text(audit.not_run_result(Path("figure.pdf"), exc))
        self.assertIn("verdict: NOT RUN", rendered)
        self.assertIn("NOT RUN is not PASS", rendered)
        self.assertIn("checks run: none", rendered)
        self.assertIn(audit.PYMUPDF_INSTALL_HINT, rendered)

    def test_cli_reports_not_run_when_pymupdf_cannot_be_imported(self) -> None:
        directory, env = blocked_pymupdf_env()
        self.addCleanup(shutil.rmtree, directory, True)
        with tempfile.TemporaryDirectory() as work:
            pdf = Path(work, "figure.pdf")
            pdf.write_bytes(b"%PDF-1.4\n")
            report = Path(work, "report.json")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(pdf), "--json-out", str(report)],
                check=False, capture_output=True, text=True, env=env,
            )
            self.assertEqual(result.returncode, audit.EXIT_NOT_RUN, result.stdout + result.stderr)
            self.assertIn("verdict: NOT RUN", result.stdout)
            self.assertIn("PyMuPDF", result.stderr)
            self.assertIn(audit.PYMUPDF_INSTALL_HINT, result.stderr)
            payload = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual(payload["status"], "NOT RUN")
            self.assertEqual(payload["checks_run"], [])
            self.assertEqual(payload["findings"], [])
            self.assertIsNone(payload["summary"]["fail"])


class ReportFileModeTests(unittest.TestCase):
    """Report artifacts follow the umask; they are not private 0600 files."""

    def write_under_umask(self, mask: int) -> int:
        previous = os.umask(mask)
        try:
            with tempfile.TemporaryDirectory() as work:
                destination = Path(work, "report.json")
                audit.write_report_json(destination, {"status": "RAN"})
                return destination.stat().st_mode & 0o777
        finally:
            os.umask(previous)

    def test_shared_umask_yields_group_and_other_readable_report(self) -> None:
        self.assertEqual(oct(self.write_under_umask(0o022)), oct(0o644))

    def test_group_writable_umask_is_respected(self) -> None:
        self.assertEqual(oct(self.write_under_umask(0o002)), oct(0o664))

    def test_private_umask_is_respected(self) -> None:
        self.assertEqual(oct(self.write_under_umask(0o077)), oct(0o600))

    def test_shared_file_mode_matches_the_process_umask(self) -> None:
        previous = os.umask(0o027)
        try:
            self.assertEqual(audit.current_umask(), 0o027)
            self.assertEqual(audit.shared_file_mode(), 0o640)
        finally:
            os.umask(previous)

    def test_atomic_write_leaves_no_temporary_file_behind(self) -> None:
        with tempfile.TemporaryDirectory() as work:
            destination = Path(work, "out.txt")
            audit.atomic_write(destination, lambda path: path.write_text("done", encoding="utf-8"))
            self.assertEqual(destination.read_text(encoding="utf-8"), "done")
            self.assertEqual([p.name for p in Path(work).iterdir()], ["out.txt"])

    def test_atomic_write_does_not_replace_the_target_when_the_writer_fails(self) -> None:
        with tempfile.TemporaryDirectory() as work:
            destination = Path(work, "out.txt")
            destination.write_text("original", encoding="utf-8")

            def failing(path: Path) -> None:
                raise RuntimeError("writer failed")

            with self.assertRaises(RuntimeError):
                audit.atomic_write(destination, failing)
            self.assertEqual(destination.read_text(encoding="utf-8"), "original")
            self.assertEqual([p.name for p in Path(work).iterdir()], ["out.txt"])


if __name__ == "__main__":
    unittest.main()
