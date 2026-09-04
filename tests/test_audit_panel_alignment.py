"""Geometry-core tests for `skills/figure/nature-figure/scripts/audit_panel_alignment.py`.

The alignment gate exists to stop a multi-panel figure claiming a shared row or
column that its rendered geometry does not have. These tests pin the three
states the gate must be able to reach, and in particular the third one: a
layout it cannot measure has to say so, never report a pass.

Standard library only: the CI runner is a bare interpreter with no third-party
packages, so nothing here imports matplotlib. The matplotlib bridge is covered
by the script's own `--self-test` and by the skill's render-time gate.
"""

import importlib.util
import json
import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills" / "figure" / "nature-figure" / "scripts" / "audit_panel_alignment.py"


def load_audit_module():
    """Import the vendored script without leaving a __pycache__ beside it.

    `ATTRIBUTION.md` records `scripts/__pycache__` as removed from the vendored
    tree, and `test_license_shipping` fails if it reappears, so this loader must
    not write bytecode into the skill directory.
    """
    spec = importlib.util.spec_from_file_location("nature_figure_audit_panel_alignment", SCRIPT)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    previously_writing_bytecode = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = previously_writing_bytecode
    return module


AUDIT = load_audit_module()


def grid_panel(panel_id, bbox, row, column):
    """A panel that carries the grid metadata a SubplotSpec would supply."""
    return {
        "id": panel_id,
        "bbox_pt": list(bbox),
        "grid_id": "grid",
        "row_start": row[0],
        "row_stop": row[1],
        "col_start": column[0],
        "col_stop": column[1],
    }


def two_by_two():
    return {
        "schema_version": 1,
        "backend": "test",
        "figure": {"width_pt": 300, "height_pt": 200},
        "panels": [
            grid_panel("a", [20, 110, 130, 180], (0, 1), (0, 1)),
            grid_panel("b", [170, 110, 280, 180], (0, 1), (1, 2)),
            grid_panel("c", [20, 20, 130, 90], (1, 2), (0, 1)),
            grid_panel("d", [170, 20, 280, 90], (1, 2), (1, 2)),
        ],
    }


class PanelLetterDetectionTests(unittest.TestCase):
    """FIX 1: panel letters are matched in both cases."""

    def test_lowercase_and_uppercase_single_letters_are_panel_letters(self):
        for letter in ("a", "d", "z", "A", "D", "Z"):
            with self.subTest(letter=letter):
                self.assertTrue(AUDIT.is_panel_letter(letter))

    def test_non_letters_are_rejected(self):
        for text in ("", "ab", "AB", "1", "a.", " a", "(a)", "α"):
            with self.subTest(text=text):
                self.assertFalse(AUDIT.is_panel_letter(text))

    def test_uppercase_letters_are_not_silently_dropped_by_the_pattern(self):
        # The measured defect: re.fullmatch(r"[a-z]", label) ignored every
        # letter produced by kernel.panel_letter(case="upper").
        self.assertIsNotNone(AUDIT.PANEL_LETTER_PATTERN.fullmatch("A"))

    def test_no_detected_letter_warns_instead_of_passing_quietly(self):
        manifest = two_by_two()
        manifest["panel_label_detection"] = {"attempted": True, "panels": 4, "detected": 0}

        report = AUDIT.audit_layout_manifest(manifest)
        kinds = [finding["kind"] for finding in report["findings"]]

        self.assertIn("panel-label-not-detected", kinds)
        self.assertEqual(report["verdict"], "REVIEW REQUIRED")
        self.assertEqual(report["summary"]["warn"], 1)

    def test_detected_letters_do_not_warn(self):
        manifest = two_by_two()
        manifest["panel_label_detection"] = {"attempted": True, "panels": 4, "detected": 4}

        report = AUDIT.audit_layout_manifest(manifest)

        self.assertEqual(report["verdict"], "PASS")

    def test_a_backend_that_never_looks_for_letters_does_not_warn(self):
        # The R/gtable manifest carries no label anchors at all. Reporting
        # "labels not detected" there would be an alarm about a check the
        # backend never claimed to run.
        report = AUDIT.audit_layout_manifest(two_by_two())

        self.assertEqual(report["verdict"], "PASS")
        self.assertEqual(report["findings"], [])

    def test_a_recorded_panel_label_exemption_silences_the_warning(self):
        manifest = two_by_two()
        manifest["panel_label_detection"] = {"attempted": True, "panels": 4, "detected": 0}
        manifest["exemptions"] = [
            {
                "panels": ["a", "b", "c", "d"],
                "checks": ["panel-label"],
                "reason": "panel letters are set with fig.text, outside the axes",
            }
        ]

        report = AUDIT.audit_layout_manifest(manifest)

        self.assertEqual(report["verdict"], "PASS")
        self.assertEqual(report["summary"]["exemptions"], 1)


class ReportPermissionTests(unittest.TestCase):
    """FIX 2: QA artifacts follow the umask instead of being forced to 0600."""

    def write_under_umask(self, mask):
        report = AUDIT.audit_layout_manifest(two_by_two())
        previous = os.umask(mask)
        try:
            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                json_path = root / "alignment.json"
                svg_path = root / "alignment.svg"
                AUDIT.write_json_report(report, json_path)
                AUDIT.write_overlay_svg(report, svg_path)
                return (
                    stat.S_IMODE(json_path.stat().st_mode),
                    stat.S_IMODE(svg_path.stat().st_mode),
                    json.loads(json_path.read_text(encoding="utf-8")),
                    svg_path.read_text(encoding="utf-8"),
                )
        finally:
            os.umask(previous)

    def test_report_and_overlay_modes_follow_the_umask(self):
        for mask, expected in ((0o022, 0o644), (0o002, 0o664), (0o077, 0o600)):
            with self.subTest(umask=oct(mask)):
                json_mode, svg_mode, payload, svg = self.write_under_umask(mask)
                self.assertEqual(json_mode, expected)
                self.assertEqual(svg_mode, expected)
                self.assertEqual(payload["verdict"], "PASS")
                self.assertIn("<svg", svg)

    def test_a_permissive_umask_is_not_overridden_to_owner_only(self):
        json_mode, svg_mode, _payload, _svg = self.write_under_umask(0o022)

        self.assertNotEqual(json_mode, 0o600)
        self.assertNotEqual(svg_mode, 0o600)
        self.assertTrue(json_mode & stat.S_IRGRP)
        self.assertTrue(json_mode & stat.S_IROTH)

    def test_the_temporary_file_does_not_survive_a_failed_write(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "alignment.svg"
            with self.assertRaises(ValueError):
                AUDIT.write_overlay_svg({"verdict": "PASS"}, target)
            self.assertEqual(sorted(item.name for item in root.iterdir()), [])


class NotAuditableStateTests(unittest.TestCase):
    """FIX 3: geometry that cannot be measured is reported, never passed."""

    def hand_built_layout(self):
        # What fig.add_axes() produces: rectangles with no grid metadata, so
        # nothing in the layout says which panels are meant to line up.
        return {
            "schema_version": 1,
            "backend": "test",
            "figure": {"width_pt": 300, "height_pt": 200},
            "panels": [
                {"id": "a", "bbox_pt": [20, 110, 130, 180]},
                {"id": "b", "bbox_pt": [170, 104, 280, 174]},
            ],
        }

    def test_hand_built_layout_is_not_auditable_and_blocks(self):
        report = AUDIT.audit_layout_manifest(self.hand_built_layout())

        self.assertEqual(report["verdict"], "NOT AUDITABLE")
        self.assertFalse(report["auditable"])
        self.assertEqual(AUDIT.exit_code(report), 4)
        self.assertNotEqual(report["verdict"], "PASS")

    def test_the_unauditable_message_names_the_remedy(self):
        report = AUDIT.audit_layout_manifest(self.hand_built_layout())
        errors = " ".join(report.get("errors", []))

        self.assertIn("no grid metadata", errors)
        self.assertIn("row_groups", errors)
        self.assertIn("column_groups", errors)
        self.assertIn("NOT a pass", errors)

    def test_explicit_row_groups_make_a_hand_built_layout_auditable_again(self):
        manifest = self.hand_built_layout()
        manifest["row_groups"] = [["a", "b"]]

        report = AUDIT.audit_layout_manifest(manifest)
        kinds = {finding["kind"] for finding in report["findings"]}

        self.assertEqual(report["verdict"], "FIX BEFORE DELIVERY")
        self.assertIn("row-axes-misalignment", kinds)
        self.assertEqual(AUDIT.exit_code(report), 1)

    def test_an_aligned_hand_built_layout_with_groups_passes(self):
        manifest = self.hand_built_layout()
        manifest["panels"][1]["bbox_pt"] = [170, 110, 280, 180]
        manifest["row_groups"] = [["a", "b"]]

        report = AUDIT.audit_layout_manifest(manifest)

        self.assertEqual(report["verdict"], "PASS")
        self.assertEqual(AUDIT.exit_code(report), 0)

    def test_a_panel_outside_every_group_is_never_hidden_behind_a_pass(self):
        # Mixed layout: a gridspec row plus one hand-placed panel. The gridspec
        # row is measurable, the loose panel is not, and the old report called
        # the whole figure PASS.
        manifest = two_by_two()
        manifest["panels"].append({"id": "e", "bbox_pt": [285, 5, 295, 15]})

        report = AUDIT.audit_layout_manifest(manifest)
        loose = [
            finding for finding in report["findings"] if finding["kind"] == "panel-not-auditable"
        ]

        self.assertNotEqual(report["verdict"], "PASS")
        self.assertEqual(report["verdict"], "REVIEW REQUIRED")
        self.assertEqual(len(loose), 1)
        self.assertEqual(loose[0]["panels"], ["e"])
        self.assertEqual(loose[0]["severity"], "WARN")
        self.assertIn("row_groups", loose[0]["message"])
        self.assertEqual(report["layout"]["ungrouped_panels"], ["e"])
        self.assertEqual(AUDIT.exit_code(report, strict=True), 1)

    def test_an_exempted_loose_panel_is_accepted_with_its_recorded_reason(self):
        manifest = two_by_two()
        manifest["panels"].append({"id": "e", "bbox_pt": [285, 5, 295, 15]})
        manifest["exemptions"] = [
            {
                "panels": ["e"],
                "checks": ["all"],
                "reason": "scale-bar inset placed by hand over panel d",
            }
        ]

        report = AUDIT.audit_layout_manifest(manifest)

        self.assertEqual(report["verdict"], "PASS")
        self.assertEqual(report["layout"]["ungrouped_panels"], [])

    def test_an_exemption_without_a_reason_is_not_auditable(self):
        manifest = two_by_two()
        manifest["exemptions"] = [{"panels": ["b"], "checks": ["row"], "reason": ""}]

        report = AUDIT.audit_layout_manifest(manifest)

        self.assertEqual(report["verdict"], "NOT AUDITABLE")
        self.assertEqual(AUDIT.exit_code(report), 4)


class GeometryCoreTests(unittest.TestCase):
    """The measurements the gate exists to make."""

    def test_single_panel_is_not_applicable_and_does_not_block(self):
        manifest = {
            "schema_version": 1,
            "backend": "test",
            "figure": {"width_pt": 200, "height_pt": 120},
            "panels": [{"id": "a", "bbox_pt": [20, 20, 180, 100]}],
        }

        report = AUDIT.audit_layout_manifest(manifest)

        self.assertEqual(report["verdict"], "NOT APPLICABLE")
        self.assertEqual(AUDIT.exit_code(report), 0)

    def test_clean_two_by_two_grid_produces_no_findings(self):
        report = AUDIT.audit_layout_manifest(two_by_two())

        self.assertEqual(report["verdict"], "PASS")
        self.assertEqual(report["findings"], [])
        self.assertEqual(report["summary"]["comparisons"], 4)

    def test_an_injected_shift_is_located_on_the_right_panel_and_edge(self):
        manifest = two_by_two()
        manifest["panels"][1]["bbox_pt"] = [170, 107, 280, 177]  # panel b, 3 pt down

        report = AUDIT.audit_layout_manifest(manifest)
        rows = [
            finding for finding in report["findings"] if finding["kind"] == "row-axes-misalignment"
        ]

        self.assertEqual(report["verdict"], "FIX BEFORE DELIVERY")
        self.assertEqual(len(rows), 1)
        self.assertEqual(sorted(rows[0]["panels"]), ["a", "b"])
        self.assertAlmostEqual(rows[0]["metric_spreads_pt"]["top"], 3.0, places=6)
        self.assertAlmostEqual(rows[0]["metric_spreads_pt"]["bottom"], 3.0, places=6)
        self.assertAlmostEqual(rows[0]["metric_spreads_pt"]["height"], 0.0, places=6)
        self.assertEqual(rows[0]["values_pt"]["top"], {"a": 180.0, "b": 177.0})

    def test_a_shift_inside_the_tolerance_still_passes(self):
        manifest = two_by_two()
        manifest["panels"][1]["bbox_pt"] = [170, 109, 280, 179]  # 1 pt < 1.5 pt

        self.assertEqual(AUDIT.audit_layout_manifest(manifest)["verdict"], "PASS")

    def test_row_spanning_panel_label_offset_is_reported_with_its_size(self):
        # The kernel.panel_letter(dy=1.02) geometry: the letter sits 2% of each
        # panel's own height above its top edge, so a row-spanning panel puts
        # its letter higher in absolute terms than its shorter neighbour.
        short_height, tall_height = 100.8, 221.76
        top = 253.44
        manifest = {
            "schema_version": 1,
            "backend": "test",
            "figure": {"width_pt": 432, "height_pt": 288},
            "panels": [
                dict(
                    grid_panel("A", [54.0, top - short_height, 270.6, top], (0, 1), (0, 2)),
                    panel_label_anchor_pt=[15.0, top + 0.02 * short_height],
                ),
                dict(
                    grid_panel("B", [290.3, top - tall_height, 388.8, top], (0, 2), (2, 3)),
                    panel_label_anchor_pt=[272.6, top + 0.02 * tall_height],
                ),
                dict(
                    grid_panel("C", [54.0, 31.68, 270.6, 132.48], (1, 2), (0, 2)),
                    panel_label_anchor_pt=[15.0, 134.496],
                ),
            ],
        }

        report = AUDIT.audit_layout_manifest(manifest, require_panel_labels=True)
        labels = [
            finding
            for finding in report["findings"]
            if finding["kind"] == "shared-top-panel-label-misalignment"
        ]

        self.assertEqual(report["verdict"], "FIX BEFORE DELIVERY")
        self.assertEqual(len(labels), 1)
        self.assertEqual(sorted(labels[0]["panels"]), ["A", "B"])
        self.assertAlmostEqual(
            labels[0]["metric_spreads_pt"]["label-y"],
            0.02 * (tall_height - short_height),
            places=6,
        )

    def test_a_malformed_manifest_is_not_auditable_rather_than_passing(self):
        for manifest in (
            {"schema_version": 99, "figure": {"width_pt": 1, "height_pt": 1}, "panels": []},
            {"schema_version": 1, "figure": {"width_pt": 0, "height_pt": 0}, "panels": []},
            {
                "schema_version": 1,
                "figure": {"width_pt": 100, "height_pt": 100},
                "panels": [{"id": "a", "bbox_pt": [10, 10, 5, 5]}],
            },
        ):
            with self.subTest(manifest=manifest):
                report = AUDIT.audit_layout_manifest(manifest)
                self.assertEqual(report["verdict"], "NOT AUDITABLE")
                self.assertEqual(AUDIT.exit_code(report), 4)
                self.assertTrue(report["errors"])

    def test_the_public_entry_points_referenced_by_validate_figure_exist(self):
        for name in ("require_matplotlib_panel_alignment", "audit_layout_manifest"):
            self.assertTrue(callable(getattr(AUDIT, name, None)), name)

    def test_the_shipped_self_test_passes(self):
        AUDIT.run_self_tests()


if __name__ == "__main__":
    unittest.main()
