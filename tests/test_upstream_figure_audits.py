"""Upstream-derived audit tests adopted for the vendored nature-figure scripts.

Provenance
----------
Three test classes were carried over from the upstream project that these
scripts were vendored from:

* ``PanelAlignmentCoreTests`` (14 methods) -- ``audit_panel_alignment.py``
* ``PdfTextAuditTests`` (3) and ``SourceSafetyTests`` (7) -- ``audit_pdf_text.py``
  and ``validate_figure.py``
* ``CollisionGeometryTests`` (5) -- ``audit_figure_collisions.py``

Upstream's workflow-integration classes were deliberately NOT adopted: they
assert against upstream repository paths and upstream documentation files that
this repository does not have. The matplotlib- and PyMuPDF-backed end-to-end
classes were also dropped, because CI here is a bare Python 3.11 with no pip
step; those code paths stay covered by each script's own ``--self-test``.

Why these three classes and not others
--------------------------------------
They encode two anti-silent-degradation invariants that this repository's
standards demand and that nothing else in ``tests/`` pinned when they were
adopted:

1. A checker must be able to report that it could not check. ``NOT AUDITABLE``
   with exit code 2 when a PDF carries no extractable text, and ``NOT
   APPLICABLE`` with exit code 0 for a single-panel figure. Neither state may
   be collapsed into a pass.
2. An alignment exemption must carry a written reason. An exemption with an
   empty reason does not silently waive the check; it puts the whole audit into
   ``NOT AUDITABLE``.

Adapted, not copied
-------------------
The vendored scripts were patched during vendoring, so three upstream
assertions no longer describe them. Each divergence is marked ``ADAPTED FROM
UPSTREAM`` at the point of use, and in every case the test was moved onto the
patched behaviour while the invariant behind it is asserted separately, so a
future regression still fails here:

* ``audit_figure_collisions.exit_code`` returns 4 (``EXIT_NOT_AUDITABLE``) for
  the not-auditable state, not upstream's 2, which the vendored script reserves
  for ``EXIT_ERROR``. The test asserts the named constant and, separately, that
  the code is neither pass nor fail.
* ``audit_pdf_text.audit_pdf`` walks resolved page and form content streams so
  it can report the size actually printed; upstream scanned the raw file. The
  fixture therefore carries a real ``/Type /Page``, and the result keys are
  ``minimum_effective_pt`` / ``minimum_raw_tf_pt`` rather than
  ``minimum_found_pt``.
* ``validate_figure.check_panel_alignment_gate`` reports ``WARN`` for an ungated
  multi-panel source where upstream reported ``FAIL``. The downgrade is
  deliberate and reasoned in the script's own source. The tests assert ``WARN``
  and, separately, that the ungated case is never ``PASS``.

Standard library only. Nothing here imports matplotlib, numpy, or PyMuPDF.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "figure" / "nature-figure" / "scripts"


def load_script(module_name: str, filename: str):
    """Import a vendored script without leaving __pycache__ in the skill tree.

    ``tests/test_license_shipping.py`` audits the shipped tree file by file and
    fails if a ``__pycache__`` directory appears inside it, so bytecode writing
    is suppressed for the duration of the import.
    """
    path = SCRIPTS / filename
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:  # pragma: no cover - import wiring
        raise AssertionError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    previously_writing_bytecode = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = previously_writing_bytecode
    return module


# Module names are prefixed so this file never clobbers the sys.modules entries
# created by the per-script test files that sit beside it.
ALIGN = load_script("upstream_audit_panel_alignment", "audit_panel_alignment.py")
COLLISION = load_script("upstream_audit_figure_collisions", "audit_figure_collisions.py")
PDF_AUDIT = load_script("upstream_audit_pdf_text", "audit_pdf_text.py")
VALIDATOR = load_script("upstream_validate_figure", "validate_figure.py")


# ---------------------------------------------------------------------------
# Section 1 -- panel alignment geometry (upstream PanelAlignmentCoreTests)
# ---------------------------------------------------------------------------


def panel(
    panel_id: str,
    bbox: list[float],
    row: tuple[int, int],
    column: tuple[int, int],
) -> dict[str, object]:
    return {
        "id": panel_id,
        "bbox_pt": bbox,
        "grid_id": "grid",
        "row_start": row[0],
        "row_stop": row[1],
        "col_start": column[0],
        "col_stop": column[1],
    }


def aligned_manifest() -> dict[str, object]:
    return {
        "schema_version": 1,
        "backend": "test",
        "figure": {"width_pt": 300, "height_pt": 200},
        "panels": [
            panel("a", [20, 110, 130, 180], (0, 1), (0, 1)),
            panel("b", [170, 110, 280, 180], (0, 1), (1, 2)),
            panel("c", [20, 20, 130, 90], (1, 2), (0, 1)),
            panel("d", [170, 20, 280, 90], (1, 2), (1, 2)),
        ],
    }


def asymmetric_vertical_manifest(spanning_side: str) -> dict[str, object]:
    if spanning_side == "right":
        panels = [
            panel("a", [20, 110, 130, 180], (0, 1), (0, 1)),
            panel("b", [20, 20, 130, 90], (1, 2), (0, 1)),
            panel("c", [170, 20, 280, 180], (0, 2), (1, 2)),
        ]
    elif spanning_side == "left":
        panels = [
            panel("a", [20, 20, 130, 180], (0, 2), (0, 1)),
            panel("b", [170, 110, 280, 180], (0, 1), (1, 2)),
            panel("c", [170, 20, 280, 90], (1, 2), (1, 2)),
        ]
    else:
        raise ValueError("spanning_side must be left or right")
    return {
        "schema_version": 1,
        "backend": "test",
        "figure": {"width_pt": 300, "height_pt": 200},
        "panels": panels,
    }


def horizontal_manifest(
    widths: list[float],
    *,
    column_spans: list[int] | None = None,
    exemptions: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    spans = [1] * len(widths) if column_spans is None else column_spans
    panels = []
    left = 10.0
    column_start = 0
    for index, (width, span) in enumerate(zip(widths, spans)):
        panels.append(
            panel(
                chr(ord("a") + index),
                [left, 20, left + width, 80],
                (0, 1),
                (column_start, column_start + span),
            )
        )
        left += width + 20
        column_start += span
    return {
        "schema_version": 1,
        "backend": "test",
        "figure": {"width_pt": left + 10, "height_pt": 100},
        "panels": panels,
        "exemptions": [] if exemptions is None else exemptions,
    }


class PanelAlignmentCoreTests(unittest.TestCase):
    """Geometry core of the alignment gate, adopted from upstream unchanged."""

    def test_single_panel_is_not_applicable_and_nonblocking(self) -> None:
        """A one-panel figure has no alignment claim, so the gate must say so."""
        manifest = {
            "schema_version": 1,
            "backend": "test",
            "figure": {"width_pt": 200, "height_pt": 120},
            "panels": [{"id": "a", "bbox_pt": [20, 20, 180, 100]}],
        }
        report = ALIGN.audit_layout_manifest(manifest)
        self.assertEqual(report["verdict"], "NOT APPLICABLE")
        self.assertEqual(ALIGN.exit_code(report), 0)

    def test_aligned_two_by_two_grid_passes(self) -> None:
        report = ALIGN.audit_layout_manifest(aligned_manifest())

        self.assertTrue(report["auditable"])
        self.assertEqual(report["verdict"], "PASS")
        self.assertEqual(report["summary"]["comparisons"], 4)
        self.assertEqual(ALIGN.exit_code(report), 0)

    def test_shifted_panel_blocks_row_and_column_alignment(self) -> None:
        manifest = aligned_manifest()
        manifest["panels"][1]["bbox_pt"] = [175, 104, 285, 174]

        report = ALIGN.audit_layout_manifest(manifest)
        kinds = {finding["kind"] for finding in report["findings"]}

        self.assertEqual(report["verdict"], "FIX BEFORE DELIVERY")
        self.assertIn("row-axes-misalignment", kinds)
        self.assertIn("column-axes-misalignment", kinds)
        self.assertEqual(ALIGN.exit_code(report), 1)

    def test_left_two_right_one_and_left_one_right_two_pass(self) -> None:
        for spanning_side in ("right", "left"):
            with self.subTest(spanning_side=spanning_side):
                report = ALIGN.audit_layout_manifest(
                    asymmetric_vertical_manifest(spanning_side)
                )
                self.assertEqual(report["verdict"], "PASS")
                self.assertEqual(report["summary"]["comparisons"], 3)
                self.assertEqual(
                    {group["edge"] for group in report["layout"]["boundary_groups"]},
                    {"top", "bottom"},
                )

    def test_shifted_spanning_panel_blocks_shared_outer_edges(self) -> None:
        for spanning_side, panel_index in (("right", 2), ("left", 0)):
            with self.subTest(spanning_side=spanning_side):
                manifest = asymmetric_vertical_manifest(spanning_side)
                box = manifest["panels"][panel_index]["bbox_pt"]
                manifest["panels"][panel_index]["bbox_pt"] = [
                    box[0],
                    box[1] + 5,
                    box[2],
                    box[3] - 5,
                ]
                report = ALIGN.audit_layout_manifest(manifest)
                kinds = {finding["kind"] for finding in report["findings"]}
                self.assertEqual(report["verdict"], "FIX BEFORE DELIVERY")
                self.assertIn("shared-top-edge-misalignment", kinds)
                self.assertIn("shared-bottom-edge-misalignment", kinds)
                self.assertEqual(ALIGN.exit_code(report), 1)

    def test_spanning_layout_panel_labels_follow_the_shared_top_edge(self) -> None:
        manifest = asymmetric_vertical_manifest("right")
        anchors = ([15, 185], [15, 95], [165, 180])
        for panel_row, anchor in zip(manifest["panels"], anchors):
            panel_row["panel_label_anchor_pt"] = anchor

        report = ALIGN.audit_layout_manifest(manifest, require_panel_labels=True)
        kinds = {finding["kind"] for finding in report["findings"]}

        self.assertEqual(report["verdict"], "FIX BEFORE DELIVERY")
        self.assertIn("shared-top-panel-label-misalignment", kinds)

    def test_three_and_four_horizontal_equal_width_panels_pass(self) -> None:
        for widths in ([60, 60, 60], [45, 45, 45, 45]):
            with self.subTest(panel_count=len(widths)):
                report = ALIGN.audit_layout_manifest(horizontal_manifest(list(widths)))
                self.assertEqual(report["verdict"], "PASS")
                self.assertEqual(ALIGN.exit_code(report), 0)

    def test_three_and_four_horizontal_unequal_width_panels_block(self) -> None:
        for widths in ([60, 80, 100], [45, 60, 75, 90]):
            with self.subTest(panel_count=len(widths)):
                report = ALIGN.audit_layout_manifest(horizontal_manifest(list(widths)))
                kinds = {finding["kind"] for finding in report["findings"]}
                self.assertEqual(report["verdict"], "FIX BEFORE DELIVERY")
                self.assertIn("horizontal-panel-width-misalignment", kinds)
                self.assertEqual(ALIGN.exit_code(report), 1)

    def test_horizontal_width_check_compares_only_equal_grid_spans(self) -> None:
        report = ALIGN.audit_layout_manifest(
            horizontal_manifest([120, 60, 60], column_spans=[2, 1, 1])
        )
        self.assertEqual(report["verdict"], "PASS")

    def test_intentional_horizontal_width_exception_requires_panel_width_reason(self) -> None:
        manifest = horizontal_manifest(
            [60, 80, 60],
            exemptions=[
                {
                    "panels": ["b"],
                    "checks": ["panel-width"],
                    "reason": "middle hero panel intentionally receives extra width",
                }
            ],
        )
        report = ALIGN.audit_layout_manifest(manifest)
        self.assertEqual(report["verdict"], "PASS")
        self.assertEqual(report["summary"]["exemptions"], 1)

    def test_unequal_gutters_block_delivery(self) -> None:
        manifest = {
            "schema_version": 1,
            "backend": "test",
            "figure": {"width_pt": 220, "height_pt": 100},
            "panels": [
                panel("a", [10, 20, 50, 80], (0, 1), (0, 1)),
                panel("b", [70, 20, 110, 80], (0, 1), (1, 2)),
                panel("c", [150, 20, 190, 80], (0, 1), (2, 3)),
            ],
        }

        report = ALIGN.audit_layout_manifest(manifest)

        self.assertEqual(report["verdict"], "FIX BEFORE DELIVERY")
        self.assertIn(
            "horizontal-gutter-misalignment",
            {finding["kind"] for finding in report["findings"]},
        )

    def test_asymmetric_hero_panel_uses_only_valid_shared_edges(self) -> None:
        manifest = {
            "schema_version": 1,
            "backend": "test",
            "figure": {"width_pt": 300, "height_pt": 200},
            "panels": [
                panel("a", [20, 105, 280, 185], (0, 1), (0, 2)),
                panel("b", [20, 20, 130, 85], (1, 2), (0, 1)),
                panel("c", [170, 20, 280, 85], (1, 2), (1, 2)),
            ],
        }

        report = ALIGN.audit_layout_manifest(manifest)

        self.assertEqual(report["verdict"], "PASS")
        self.assertEqual(report["summary"]["comparisons"], 3)

    def test_exemption_requires_reason_and_can_remove_an_inset(self) -> None:
        """An exemption without a written reason must not silently waive a check."""
        manifest = {
            "schema_version": 1,
            "backend": "test",
            "figure": {"width_pt": 240, "height_pt": 120},
            "panels": [
                panel("a", [10, 20, 60, 90], (0, 1), (0, 1)),
                panel("b", [85, 28, 135, 98], (0, 1), (1, 2)),
                panel("c", [160, 20, 210, 90], (0, 1), (2, 3)),
            ],
            "exemptions": [
                {
                    "panels": ["b"],
                    "checks": ["row", "horizontal-gutter"],
                    "reason": "intentional inset panel",
                }
            ],
        }

        report = ALIGN.audit_layout_manifest(manifest)
        self.assertEqual(report["verdict"], "PASS")
        self.assertEqual(report["summary"]["exemptions"], 1)

        manifest["exemptions"][0]["reason"] = ""
        invalid = ALIGN.audit_layout_manifest(manifest)
        self.assertEqual(invalid["verdict"], "NOT AUDITABLE")
        self.assertEqual(ALIGN.exit_code(invalid), 4)

    def test_diagnostic_svg_and_json_are_written(self) -> None:
        report = ALIGN.audit_layout_manifest(aligned_manifest())
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            json_path = root / "alignment.json"
            svg_path = root / "alignment.svg"
            ALIGN.write_json_report(report, json_path)
            ALIGN.write_overlay_svg(report, svg_path)

            self.assertEqual(json.loads(json_path.read_text())["verdict"], "PASS")
            self.assertIn("<svg", svg_path.read_text())


# ---------------------------------------------------------------------------
# Section 2 -- PDF text audit and source-pattern safety
# (upstream PdfTextAuditTests and SourceSafetyTests)
# ---------------------------------------------------------------------------


def _stream_object(number: int, stream: bytes, compressed: bool) -> bytes:
    payload = zlib.compress(stream) if compressed else stream
    filter_entry = b" /Filter /FlateDecode" if compressed else b""
    return (
        str(number).encode("ascii")
        + b" 0 obj\n<< /Length "
        + str(len(payload)).encode("ascii")
        + filter_entry
        + b" >>\nstream\n"
        + payload
        + b"\nendstream\nendobj\n"
    )


def page_pdf(stream: bytes, compressed: bool = False) -> bytes:
    """A minimal PDF whose content stream hangs off a real ``/Type /Page``.

    ADAPTED FROM UPSTREAM. Upstream's helper emitted a naked stream object with
    no page around it, because upstream's auditor scanned the whole file for
    ``Tf`` operators. The vendored auditor walks resolved page and form content
    streams instead, so it can apply the CTM and text matrix and report the
    *printed* size rather than the raw ``Tf`` operand. A stream that belongs to
    no page therefore has an unknown transform context, and the vendored script
    refuses to audit it (see ``no_page_pdf`` below). That is the patched
    behaviour, not a regression, so the fixture grew a page object.
    """
    page = (
        b"1 0 obj\n<< /Type /Page /MediaBox [0 0 200 120] /Resources << >> "
        b"/Contents 2 0 R >>\nendobj\n"
    )
    return b"%PDF-1.4\n" + page + _stream_object(2, stream, compressed) + b"%%EOF\n"


def no_page_pdf(stream: bytes, compressed: bool = False) -> bytes:
    """Upstream's original fixture shape: a stream object with no page."""
    return b"%PDF-1.4\n" + _stream_object(1, stream, compressed) + b"%%EOF\n"


class PdfTextAuditTests(unittest.TestCase):
    def test_plain_pdf_passes_when_all_tf_sizes_meet_floor(self):
        result = PDF_AUDIT.audit_pdf(page_pdf(b"BT /F1 7 Tf (Label) Tj ET"))
        self.assertTrue(result["auditable"])
        self.assertEqual(result["verdict"], "PASS")
        # ADAPTED: upstream read `minimum_found_pt`. The vendored script splits
        # that into the raw Tf operand and the size actually printed after the
        # transform; under an identity CTM the two agree.
        self.assertEqual(result["minimum_effective_pt"], 7.0)
        self.assertEqual(result["minimum_raw_tf_pt"], 7.0)
        self.assertEqual(result["below_minimum_count"], 0)

    def test_flate_pdf_catches_mathtext_sized_run(self):
        result = PDF_AUDIT.audit_pdf(
            page_pdf(b"BT /F1 7 Tf (R) Tj /F2 4.9 Tf (2) Tj ET", compressed=True)
        )
        self.assertTrue(result["auditable"])
        self.assertEqual(result["verdict"], "FAIL")
        self.assertEqual(result["minimum_effective_pt"], 4.9)
        self.assertEqual(result["below_minimum_count"], 1)
        self.assertEqual(result["below_minimum"][0]["font"], "F2")

    def test_pdf_without_supported_tf_is_not_auditable(self):
        """Two ways of having nothing to measure, both reported as "cannot check"."""
        drawing_only = PDF_AUDIT.audit_pdf(page_pdf(b"0 0 m 10 10 l S"))
        self.assertFalse(drawing_only["auditable"])
        self.assertEqual(drawing_only["verdict"], "NOT AUDITABLE")
        self.assertTrue(drawing_only["blocked_reasons"])

        # ADDED with the patched parser: Tf operators that sit in no resolvable
        # page or form have an unknown transform, so their printed size is
        # unknown. The audit must block rather than report the raw operand.
        orphan_text = PDF_AUDIT.audit_pdf(no_page_pdf(b"BT /F1 7 Tf (Label) Tj ET"))
        self.assertFalse(orphan_text["auditable"])
        self.assertEqual(orphan_text["verdict"], "NOT AUDITABLE")
        self.assertEqual(orphan_text["content_streams_walked"], 0)


class SourceSafetyTests(unittest.TestCase):
    def findings(self, source: str):
        return {row.check_id: row for row in VALIDATOR.validate_source(source, "python")}

    def test_risky_patterns_are_reported(self):
        source = '''
import numpy as np
seed_scores = np.median(scores, axis=0)
n_equiv = np.interp(target, decreasing_error, n_samples)
ax.plot(x, seed_scores, label="+ semantic guidance")
ax.text(0.5, 0.5, "$R^2$", fontsize=7, rotation=45,
        bbox=dict(facecolor="white", edgecolor="none"))
LABEL_Y = 96.4
'''
        rows = self.findings(source)
        for check_id in (
            "FONT-GLYPH-FLOOR",
            "LEGEND-LABEL-CASE",
            "INTERP-MONOTONIC",
            "UNCERTAINTY-ENCODING",
            "ROTATION-ANCHOR",
            "ANNOTATION-WORKAROUND",
        ):
            self.assertEqual(rows[check_id].level, "WARN", check_id)

    def test_guarded_patterns_pass_targeted_checks(self):
        source = '''
import numpy as np
def interp_monotone(target, xp, fp):
    order = np.argsort(xp)
    xp = xp[order]
    fp = fp[order]
    assert np.all(np.diff(xp) > 0)
    return np.interp(target, xp, fp)

seed_scores = np.median(scores, axis=0)
ax.plot(x, seed_scores, label="+ Semantic guidance")
ax.fill_between(x, seed_scores - seed_std, seed_scores + seed_std)
ax.text(0.5, 0.5, "R²", fontsize=7, rotation=45, rotation_mode="anchor")
'''
        rows = self.findings(source)
        for check_id in (
            "FONT-GLYPH-FLOOR",
            "LEGEND-LABEL-CASE",
            "INTERP-MONOTONIC",
            "UNCERTAINTY-ENCODING",
            "ROTATION-ANCHOR",
            "ANNOTATION-WORKAROUND",
        ):
            self.assertEqual(rows[check_id].level, "PASS", check_id)

    def test_string_split_is_not_mistaken_for_random_split(self):
        source = '''
columns = [value.strip() for value in args.columns.split(",")]
ax.set_ylabel("Mean fold change")
'''
        rows = self.findings(source)
        self.assertEqual(rows["UNCERTAINTY-ENCODING"].level, "PASS")

    def test_every_rotated_call_must_be_anchored(self):
        source = '''
ax.text(0.2, 0.3, "A", rotation=45, rotation_mode="anchor")
ax.text(0.5, 0.6, "B", rotation=90)
'''
        rows = self.findings(source)
        self.assertEqual(rows["ROTATION-ANCHOR"].level, "WARN")
        self.assertEqual(rows["ROTATION-ANCHOR"].evidence, ["line 3: rotation=..."])

    def test_python_multipanel_source_requires_alignment_gate(self):
        """An ungated multi-panel source must be flagged, never reported clean.

        ADAPTED FROM UPSTREAM. Upstream asserted ``FAIL`` for every ungated
        case. The vendored ``check_panel_alignment_gate`` deliberately downgrades
        the ungated verdict to ``WARN``, with the reason written in the source:
        a static source check cannot observe a render-time gate, so a hard FAIL
        blocks compliant multi-panel examples the skill itself ships, and a gate
        that blocks compliant work gets switched off. The invariant this test
        actually protects is unaffected and is asserted separately below: the
        ungated case is never ``PASS``.
        """
        ungated_sources = {
            "subplots": "fig, axes = plt.subplots(2, 2)",
            "import_only": (
                "from audit_panel_alignment import require_matplotlib_panel_alignment\n"
                "fig, axes = plt.subplots(2, 2)"
            ),
            "manual_axes": (
                "fig = plt.figure()\n"
                "ax_a = fig.add_axes([0.1, 0.1, 0.3, 0.8])\n"
                "ax_b = fig.add_axes([0.6, 0.1, 0.3, 0.8])"
            ),
            "mosaic": "fig, axes = plt.subplot_mosaic([['a', 'b']])",
        }
        for name, source in ungated_sources.items():
            with self.subTest(source=name):
                level = self.findings(source)["PANEL-ALIGNMENT-GATE"].level
                self.assertNotEqual(level, "PASS")
                self.assertEqual(level, "WARN")

        wired = self.findings(
            '''
fig, axes = plt.subplots(2, 2)
require_matplotlib_panel_alignment(fig, strict=True)
'''
        )
        self.assertEqual(wired["PANEL-ALIGNMENT-GATE"].level, "PASS")

    def test_r_patchwork_source_requires_alignment_gate(self):
        missing = {
            row.check_id: row
            for row in VALIDATOR.validate_source(
                "fig <- (p_a | p_b) + plot_layout(guides = 'collect')",
                "r",
            )
        }
        # ADAPTED: WARN, not upstream's FAIL. See the Python case above.
        self.assertNotEqual(missing["PANEL-ALIGNMENT-GATE"].level, "PASS")
        self.assertEqual(missing["PANEL-ALIGNMENT-GATE"].level, "WARN")

        manifest_only = {
            row.check_id: row
            for row in VALIDATOR.validate_source(
                "fig <- p_a | p_b\nwrite_patchwork_panel_layout(fig, manifest_path='a.json')",
                "r",
            )
        }
        # Writing the manifest is not running the audit, so this stays flagged.
        self.assertNotEqual(manifest_only["PANEL-ALIGNMENT-GATE"].level, "PASS")
        self.assertEqual(manifest_only["PANEL-ALIGNMENT-GATE"].level, "WARN")

        wired = {
            row.check_id: row
            for row in VALIDATOR.validate_source(
                "fig <- p_a | p_b\nrequire_patchwork_panel_alignment(fig, manifest_path='a.json')",
                "r",
            )
        }
        self.assertEqual(wired["PANEL-ALIGNMENT-GATE"].level, "PASS")

    def test_r_delimiter_check_ignores_comments(self):
        finding = VALIDATOR.check_syntax(
            "# patchwork's final panel cells { are measured\nfig <- (p_a | p_b)",
            "r",
        )
        self.assertEqual(finding.level, "WARN")
        self.assertIn("delimiter check passed", finding.message)


# ---------------------------------------------------------------------------
# Section 3 -- collision geometry (upstream CollisionGeometryTests)
# ---------------------------------------------------------------------------


class CollisionGeometryTests(unittest.TestCase):
    def test_clean_text_and_distant_line_pass(self) -> None:
        page = COLLISION.PageGeometry(
            page=1,
            bbox=(0, 0, 200, 120),
            texts=[COLLISION.TextBox(0, "Clear", (50, 20, 90, 32))],
            traces=[COLLISION.TraceBox(0, "Clear", (50, 20, 90, 32))],
            strokes=[
                COLLISION.StrokePath(
                    0,
                    (20, 70, 180, 70),
                    1.0,
                    (((20, 70), (180, 70)),),
                )
            ],
        )

        result = COLLISION.audit_geometries([page])

        self.assertEqual(result["verdict"], "PASS")
        self.assertEqual(result["summary"]["fail"], 0)

    def test_text_stroke_and_text_text_collisions_block_delivery(self) -> None:
        page = COLLISION.PageGeometry(
            page=1,
            bbox=(0, 0, 200, 120),
            texts=[
                COLLISION.TextBox(0, "First", (50, 40, 100, 54)),
                COLLISION.TextBox(1, "Second", (80, 43, 125, 57)),
            ],
            traces=[
                COLLISION.TraceBox(0, "First", (50, 40, 100, 54)),
                COLLISION.TraceBox(1, "Second", (80, 43, 125, 57)),
            ],
            strokes=[
                COLLISION.StrokePath(
                    0,
                    (20, 47, 180, 47),
                    1.0,
                    (((20, 47), (180, 47)),),
                )
            ],
        )

        result = COLLISION.audit_geometries([page])
        kinds = {finding["kind"] for finding in result["findings"]}

        self.assertEqual(result["verdict"], "FIX BEFORE DELIVERY")
        self.assertIn("text-text", kinds)
        self.assertIn("text-stroke", kinds)
        self.assertEqual(COLLISION.exit_code(result), 1)

    def test_contained_fill_is_informational_but_partial_fill_warns(self) -> None:
        page = COLLISION.PageGeometry(
            page=1,
            bbox=(0, 0, 200, 120),
            texts=[
                COLLISION.TextBox(0, "Inside", (60, 40, 90, 52)),
                COLLISION.TextBox(1, "Edge", (120, 40, 155, 52)),
            ],
            traces=[
                COLLISION.TraceBox(0, "Inside", (60, 40, 90, 52)),
                COLLISION.TraceBox(1, "Edge", (120, 40, 155, 52)),
            ],
            fills=[
                COLLISION.FilledRegion(0, (50, 30, 100, 60), "fill"),
                COLLISION.FilledRegion(1, (105, 30, 135, 60), "fill"),
            ],
        )

        result = COLLISION.audit_geometries([page])

        self.assertEqual(result["verdict"], "REVIEW REQUIRED")
        self.assertEqual(result["summary"]["contained_fill_overlays"], 1)
        self.assertEqual(result["summary"]["warn"], 1)
        self.assertEqual(result["findings"][0]["kind"], "text-fill-edge")
        self.assertEqual(COLLISION.exit_code(result), 0)
        self.assertEqual(COLLISION.exit_code(result, strict=True), 1)

    def test_page_clipping_blocks_delivery(self) -> None:
        page = COLLISION.PageGeometry(
            page=1,
            bbox=(0, 0, 200, 120),
            traces=[COLLISION.TraceBox(0, "Clipped", (50, -8, 90, 4))],
        )

        result = COLLISION.audit_geometries([page])

        self.assertEqual(result["summary"]["fail"], 1)
        self.assertEqual(result["findings"][0]["kind"], "text-page-clipping")

    def test_pdf_without_editable_text_is_not_claimed_as_checked(self) -> None:
        """No editable text means the collision audit reports it could not check."""
        result = COLLISION.audit_geometries(
            [COLLISION.PageGeometry(page=1, bbox=(0, 0, 200, 120))]
        )

        self.assertFalse(result["auditable"])
        self.assertEqual(result["verdict"], "NOT AUDITABLE")
        # ADAPTED FROM UPSTREAM. Upstream returned a literal 2 here. The vendored
        # script reserves 2 for EXIT_ERROR (bad arguments, unreadable file) and
        # gives the two "could not check" states codes of their own: 3 NOT RUN
        # for a missing dependency, 4 NOT AUDITABLE for a PDF with no editable
        # text. The invariant is that this state is distinct from both pass and
        # fail, which is asserted directly rather than by pinning the integer.
        self.assertEqual(COLLISION.exit_code(result), COLLISION.EXIT_NOT_AUDITABLE)
        self.assertNotIn(
            COLLISION.exit_code(result),
            (COLLISION.EXIT_PASS, COLLISION.EXIT_FAIL),
        )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
