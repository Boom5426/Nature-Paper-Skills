"""Tests for skills/figure/nature-figure/scripts/figure_safety.py.

The suite runs on a bare interpreter with no third-party packages. The one
numpy-dependent class is an agreement cross-check and reports itself as
*skipped*, never as passed, when numpy is absent.
"""

import ast
import importlib.util
import random
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "skills/figure/nature-figure/scripts/figure_safety.py"

_spec = importlib.util.spec_from_file_location("figure_safety", MODULE_PATH)
figure_safety = importlib.util.module_from_spec(_spec)
# Load without leaving a __pycache__ directory inside the shipped skill tree;
# tests/test_license_shipping.py audits that tree file by file.
_prev_bytecode = sys.dont_write_bytecode
sys.dont_write_bytecode = True
try:
    _spec.loader.exec_module(figure_safety)
finally:
    sys.dont_write_bytecode = _prev_bytecode

interp_monotone = figure_safety.interp_monotone
label_y_above = figure_safety.label_y_above
ylim_top_for_label = figure_safety.ylim_top_for_label

try:
    import numpy as np
except ImportError:  # reported as a skip below, never as a pass
    np = None

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except ImportError:  # reported as a skip below, never as a pass
    plt = None


class BareInterpreterImportTests(unittest.TestCase):
    """Every import in the module must resolve on a stdlib-only interpreter."""

    def test_module_imports_only_the_standard_library(self) -> None:
        tree = ast.parse(MODULE_PATH.read_text(encoding="utf-8"))
        roots = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                roots.add(node.module.split(".")[0])
        offenders = sorted(r for r in roots if r not in sys.stdlib_module_names)
        self.assertEqual(
            offenders,
            [],
            f"{MODULE_PATH.name} imports non-stdlib modules {offenders}; CI runs a "
            "bare interpreter with no pip step, so these must be deferred into the "
            "function that needs them or removed",
        )


class InterpMonotoneTests(unittest.TestCase):
    def test_increasing_grid_interpolates_linearly(self) -> None:
        self.assertEqual(interp_monotone(2.5, [1, 2, 3, 4], [10, 20, 30, 40]), 25.0)

    def test_decreasing_grid_gives_the_same_answer_as_its_reversal(self) -> None:
        forward = interp_monotone([1.5, 2.5, 3.5], [1, 2, 3, 4], [10, 20, 30, 40])
        reverse = interp_monotone([1.5, 2.5, 3.5], [4, 3, 2, 1], [40, 30, 20, 10])
        self.assertEqual(forward, reverse)
        self.assertEqual(forward, [15.0, 25.0, 35.0])

    def test_out_of_range_targets_clamp_to_the_end_values(self) -> None:
        self.assertEqual(interp_monotone([-99.0, 99.0], [1, 2, 3], [10, 20, 30]), [10.0, 30.0])

    def test_grid_points_return_their_own_values(self) -> None:
        xp = [0.5, 1.25, 7.0]
        fp = [-3.0, 8.0, 2.5]
        self.assertEqual(interp_monotone(xp, xp, fp), fp)

    def test_direction_change_is_refused(self) -> None:
        with self.assertRaisesRegex(ValueError, "strictly monotone"):
            interp_monotone(2.5, [1, 3, 2, 4], [10, 30, 20, 40])

    def test_duplicate_coordinates_are_refused(self) -> None:
        with self.assertRaisesRegex(ValueError, "strictly monotone"):
            interp_monotone(2.0, [1, 2, 2, 3], [10, 20, 25, 30])

    def test_length_mismatch_is_refused(self) -> None:
        with self.assertRaisesRegex(ValueError, "equal length"):
            interp_monotone(1.0, [1, 2, 3], [10, 20])

    def test_single_point_grid_is_refused(self) -> None:
        with self.assertRaisesRegex(ValueError, "at least two"):
            interp_monotone(1.0, [1], [10])

    def test_non_finite_input_is_refused(self) -> None:
        for xp, fp in (([1.0, float("nan")], [1.0, 2.0]), ([1.0, 2.0], [1.0, float("inf")])):
            with self.subTest(xp=xp, fp=fp):
                with self.assertRaisesRegex(ValueError, "finite"):
                    interp_monotone(1.5, xp, fp)

    def test_scalar_in_scalar_out_and_sequence_in_list_out(self) -> None:
        self.assertIsInstance(interp_monotone(1.5, [1, 2], [10, 20]), float)
        self.assertIsInstance(interp_monotone([1.5], [1, 2], [10, 20]), list)


class LabelPaddingScaleTests(unittest.TestCase):
    """figure-style 3.1: the pad is a fraction of the visible axis, not of the data.

    These are the cases the removed ``max(range, abs(data_max), 1.0)`` scale got
    wrong: it padded by ``abs(data_max)`` on an axis that does not start at zero,
    and by a hard-coded 1.0 unit whenever the data were small.
    """

    CASES = (
        ("offset axis", [99.0, 100.0, 101.0], (98.0, 102.0)),
        ("small values", [0.0010, 0.0015, 0.0020], (0.0, 0.0025)),
        ("negative only", [-5.0, -4.0, -3.0], (-6.0, -2.0)),
        ("zero based", [1.0, 5.0, 10.0], (0.0, 12.0)),
        ("straddling zero", [-2.0, 0.0, 3.0], (-4.0, 5.0)),
    )

    def test_offset_is_exactly_pad_fraction_of_the_axis_span(self) -> None:
        for name, values, ylim in self.CASES:
            with self.subTest(case=name):
                span = ylim[1] - ylim[0]
                offset = label_y_above(values, ylim=ylim) - max(values)
                self.assertAlmostEqual(offset / span, 0.04, places=12)

    def test_offset_does_not_depend_on_the_distance_from_zero(self) -> None:
        base = label_y_above([1.0, 2.0], ylim=(0.0, 3.0)) - 2.0
        shifted = label_y_above([1e6 + 1.0, 1e6 + 2.0], ylim=(1e6, 1e6 + 3.0)) - (1e6 + 2.0)
        self.assertAlmostEqual(base, shifted, places=9)

    def test_small_valued_axis_keeps_the_label_inside_the_axis(self) -> None:
        values = [1e-6, 2e-6]
        ylim = (0.0, 3e-6)
        self.assertLess(label_y_above(values, ylim=ylim), ylim[1])

    def test_zero_width_data_span_without_ylim_is_refused(self) -> None:
        with self.assertRaisesRegex(ValueError, "zero-width data span"):
            label_y_above([7.0, 7.0])

    def test_data_span_fallback_is_used_when_no_ylim_is_given(self) -> None:
        self.assertAlmostEqual(label_y_above([0.0, 10.0]), 10.4, places=12)


class Rule31ClearanceTests(unittest.TestCase):
    """figure-style 3.1: text never touches a spine, on either side."""

    def test_label_clears_both_the_data_and_the_top_spine_by_one_pad(self) -> None:
        for name, values, ylim in LabelPaddingScaleTests.CASES:
            with self.subTest(case=name):
                pad = 0.04 * (ylim[1] - ylim[0])
                y = label_y_above(values, ylim=ylim)
                self.assertGreaterEqual(y - max(values), pad - 1e-12)
                self.assertGreaterEqual(ylim[1] - y, pad - 1e-12)

    def test_a_top_limit_too_low_for_the_label_is_refused(self) -> None:
        with self.assertRaisesRegex(ValueError, "top spine"):
            label_y_above([10.0], ylim=(0.0, 10.2))

    def test_ylim_top_for_label_is_the_exact_fixed_point(self) -> None:
        # Matplotlib's own default margins produce exactly this too-tight case.
        values = [2.0, 6.0, 10.0]
        bottom = -0.5
        top = ylim_top_for_label(values, bottom=bottom)
        with self.assertRaises(ValueError):
            label_y_above(values, ylim=(bottom, 10.5))
        y = label_y_above(values, ylim=(bottom, top))
        pad = 0.04 * (top - bottom)
        self.assertAlmostEqual(y - max(values), pad, places=12)
        self.assertAlmostEqual(top - y, pad, places=12)

    def test_label_height_fraction_is_reserved_above_the_label(self) -> None:
        values = [10.0]
        bottom = 0.0
        f = 0.10
        top = ylim_top_for_label(values, bottom=bottom, label_height_fraction=f)
        y = label_y_above(values, ylim=(bottom, top), label_height_fraction=f)
        span = top - bottom
        self.assertAlmostEqual(y - max(values), 0.04 * span, places=12)
        self.assertAlmostEqual(top - (y + f * span), 0.04 * span, places=12)

    def test_a_taller_label_needs_a_higher_top(self) -> None:
        short = ylim_top_for_label([10.0], bottom=0.0, label_height_fraction=0.0)
        tall = ylim_top_for_label([10.0], bottom=0.0, label_height_fraction=0.20)
        self.assertGreater(tall, short)

    def test_ignoring_the_label_height_is_caught_as_a_3_1_violation(self) -> None:
        top = ylim_top_for_label([10.0], bottom=0.0)  # room for the anchor only
        label_y_above([10.0], ylim=(0.0, top))  # fine for a zero-height mark
        with self.assertRaisesRegex(ValueError, "top spine"):
            label_y_above([10.0], ylim=(0.0, top), label_height_fraction=0.10)

    def test_reserving_the_whole_axis_is_refused(self) -> None:
        with self.assertRaisesRegex(ValueError, "whole axis"):
            label_y_above([1.0], ylim=(0.0, 4.0), label_height_fraction=0.95)

    def test_negative_label_height_fraction_is_refused(self) -> None:
        with self.assertRaisesRegex(ValueError, "label_height_fraction must be non-negative"):
            label_y_above([1.0], ylim=(0.0, 4.0), label_height_fraction=-0.1)

    def test_ylim_top_for_label_accounts_for_the_spread(self) -> None:
        plain = ylim_top_for_label([10.0], bottom=0.0)
        with_error = ylim_top_for_label([10.0], [2.0], bottom=0.0)
        self.assertGreater(with_error, plain)
        y = label_y_above([10.0], [2.0], ylim=(0.0, with_error))
        self.assertGreaterEqual(y, 12.0)


class LabelInputValidationTests(unittest.TestCase):
    def test_scalar_spread_is_broadcast(self) -> None:
        self.assertEqual(
            label_y_above([1.0, 2.0], 0.5, ylim=(0.0, 4.0)),
            label_y_above([1.0, 2.0], [0.5, 0.5], ylim=(0.0, 4.0)),
        )

    def test_spread_length_mismatch_is_refused(self) -> None:
        with self.assertRaisesRegex(ValueError, "match len"):
            label_y_above([1.0, 2.0], [0.1, 0.2, 0.3], ylim=(0.0, 4.0))

    def test_negative_spread_is_refused(self) -> None:
        with self.assertRaisesRegex(ValueError, "non-negative half-length"):
            label_y_above([1.0], [-0.5], ylim=(0.0, 4.0))

    def test_inverted_axis_is_refused(self) -> None:
        with self.assertRaisesRegex(ValueError, "increasing"):
            label_y_above([1.0], ylim=(4.0, 0.0))

    def test_degenerate_axis_is_refused(self) -> None:
        with self.assertRaisesRegex(ValueError, "non-degenerate"):
            label_y_above([1.0], ylim=(2.0, 2.0))

    def test_pad_fraction_out_of_range_is_refused(self) -> None:
        for bad in (-0.01, 0.5, 1.0):
            with self.subTest(pad_fraction=bad):
                with self.assertRaisesRegex(ValueError, "pad_fraction"):
                    label_y_above([1.0], ylim=(0.0, 4.0), pad_fraction=bad)

    def test_non_finite_values_are_refused(self) -> None:
        with self.assertRaisesRegex(ValueError, "finite"):
            label_y_above([1.0, float("nan")], ylim=(0.0, 4.0))


@unittest.skipUnless(plt is not None, "matplotlib is not installed: rendered 3.1 check not run")
class RenderedRule31Tests(unittest.TestCase):
    """figure-style 3.1 measured on drawn ink, not on coordinates.

    3.1 says markers and text never touch a spine. Only a render can show that,
    because a text label occupies height its anchor coordinate does not.
    """

    CASES = (
        ("offset axis", [99.0, 100.0, 101.0], 98.0),
        ("small values", [0.0010, 0.0015, 0.0020], 0.0),
        ("negative only", [-5.0, -4.0, -3.0], -6.0),
        ("zero based", [1.0, 5.0, 10.0], 0.0),
        ("straddling zero", [-2.0, 0.0, 3.0], -4.0),
    )

    def test_drawn_label_clears_the_bar_and_the_top_spine_by_one_pad(self) -> None:
        for name, values, bottom in self.CASES:
            with self.subTest(case=name):
                fig, ax = plt.subplots(figsize=(2.4, 1.8), dpi=300)
                self.addCleanup(plt.close, fig)
                ax.bar(range(len(values)), values, bottom=bottom)
                ax.set_ylim(bottom, ylim_top_for_label(values, bottom=bottom))
                text = ax.text(
                    len(values) - 1, max(values), f"{max(values):g}",
                    ha="center", va="bottom", fontsize=6,
                )
                fig.canvas.draw()
                renderer = fig.canvas.get_renderer()
                fraction = (
                    text.get_window_extent(renderer).height / ax.get_window_extent().height
                )
                top = ylim_top_for_label(
                    values, bottom=bottom, label_height_fraction=fraction
                )
                ax.set_ylim(bottom, top)
                text.set_y(
                    label_y_above(values, ylim=(bottom, top), label_height_fraction=fraction)
                )
                fig.canvas.draw()
                box = text.get_window_extent(fig.canvas.get_renderer())
                to_px = ax.transData.transform
                base_px = to_px((0, bottom))[1]
                pad_px = to_px((0, bottom + 0.04 * (top - bottom)))[1] - base_px
                below = box.y0 - to_px((0, max(values)))[1]
                above = to_px((0, top))[1] - box.y1
                self.assertGreaterEqual(below, pad_px - 0.01, f"{name}: label sits on the data")
                self.assertGreaterEqual(above, pad_px - 0.01, f"{name}: label touches the spine")


@unittest.skipUnless(np is not None, "numpy is not installed: agreement cross-check not run")
class NumpyAgreementTests(unittest.TestCase):
    """Property tests against numpy.interp, the function this helper guards."""

    TRIALS = 2000

    def _random_case(self, rng):
        grid = sorted({rng.uniform(-1e3, 1e3) for _ in range(rng.randint(2, 12))})
        while len(grid) < 2:
            grid = sorted({rng.uniform(-1e3, 1e3) for _ in range(4)})
        values = [rng.uniform(-1e6, 1e6) for _ in grid]
        width = grid[-1] - grid[0]
        targets = [rng.uniform(grid[0] - width, grid[-1] + width) for _ in range(5)]
        return grid, values, targets + list(grid)

    def test_agrees_with_numpy_interp_on_increasing_grids(self) -> None:
        rng = random.Random(20260904)
        for trial in range(self.TRIALS):
            grid, values, targets = self._random_case(rng)
            ours = interp_monotone(targets, grid, values)
            theirs = np.interp(targets, grid, values)
            for t, a, b in zip(targets, ours, theirs):
                if a != float(b):
                    self.fail(
                        f"trial {trial}: interp_monotone({t!r}) = {a!r} but "
                        f"np.interp gave {float(b)!r} on grid {grid!r}"
                    )

    def test_numpy_is_silently_wrong_on_decreasing_grids_and_we_are_not(self) -> None:
        grid = [4.0, 3.0, 2.0, 1.0]
        values = [40.0, 30.0, 20.0, 10.0]
        numpy_answer = float(np.interp(2.5, grid, values))
        self.assertEqual(numpy_answer, 10.0)  # plausible, and wrong
        self.assertEqual(interp_monotone(2.5, grid, values), 25.0)

    def test_numpy_is_silently_wrong_on_non_monotone_grids_and_we_refuse(self) -> None:
        grid = [1.0, 3.0, 2.0, 4.0]
        values = [10.0, 30.0, 20.0, 40.0]
        self.assertTrue(np.isfinite(np.interp(2.5, grid, values)))  # no error raised
        with self.assertRaisesRegex(ValueError, "strictly monotone"):
            interp_monotone(2.5, grid, values)

    def test_accepts_numpy_arrays_as_input(self) -> None:
        out = interp_monotone(np.array([1.5, 2.5]), np.array([1.0, 2.0, 3.0]), np.array([10.0, 20.0, 30.0]))
        self.assertEqual(out, [15.0, 25.0])


if __name__ == "__main__":
    unittest.main()
