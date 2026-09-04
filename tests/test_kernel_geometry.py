"""Geometry invariants for the figure-style kernel helpers.

Two defects these tests pin down, both measured in rendered pixels rather than
judged by eye:

1. ``end_of_line_labels`` used to write its labels past the axes' right edge
   without reserving any room, so on a multi-panel sheet they landed on the
   neighbouring panel's letter and tick labels. A label must now stay inside
   the axes that owns it (SKILL.md §3.1 "extend the limit past any annotation",
   §6.9 a label stays anchored to the row it names).
2. ``panel_letter`` used to offset the letter in axes fractions, so its
   absolute height above the panel scaled with panel height and the letters
   misaligned across a mosaic of unequal panels. The offset must now be
   physical, identical for every panel on the sheet.

matplotlib is not installed on the bare CI runner, so the whole module skips
there; it is not a silent pass, the skip reason names the missing package.
"""

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KERNEL = ROOT / "skills" / "figure" / "figure-style" / "kernel.py"

try:  # matplotlib is a hard requirement of these helpers, not of the repo
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    HAVE_MPL = True
    WHY = ""
except ImportError as exc:  # pragma: no cover - depends on the runner
    HAVE_MPL = False
    WHY = f"needs matplotlib and numpy ({exc})"


def load_kernel():
    """Import kernel.py by path; it is a skill payload, not an installed module."""
    spec = importlib.util.spec_from_file_location("figure_style_kernel", KERNEL)
    module = importlib.util.module_from_spec(spec)
    # Executing a module from the skill tree would drop __pycache__ into a
    # shipped directory, and install.sh copies the working tree.
    _previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = _previous
    return module


def overlap_area(a, b):
    """Area of the intersection of two display-space bboxes, in px^2."""
    w = max(0.0, min(a.x1, b.x1) - max(a.x0, b.x0))
    h = max(0.0, min(a.y1, b.y1) - max(a.y0, b.y0))
    return w * h


@unittest.skipUnless(HAVE_MPL, WHY)
class KernelGeometryTest(unittest.TestCase):
    def setUp(self):
        self.kernel = load_kernel()
        self.kernel.apply_figure_style()
        self.addCleanup(plt.close, "all")

    def renderer(self, fig):
        fig.canvas.draw()
        return fig.canvas.get_renderer()

    def letter_offsets(self, mosaic, figsize):
        """Pixel gap between each panel letter's bottom and its axes' top edge."""
        fig, axd = plt.subplot_mosaic(mosaic, figsize=figsize)
        for key, ax in axd.items():
            ax.plot([0, 1], [0, 1])
            self.kernel.panel_letter(ax, key)
        r = self.renderer(fig)
        offsets = {}
        for key, ax in axd.items():
            text = next(t for t in ax.texts if t.get_text().strip().lower() == key.lower())
            offsets[key] = text.get_window_extent(renderer=r).y0 - ax.bbox.y1
        heights = {key: ax.bbox.height for key, ax in axd.items()}
        return offsets, heights, fig

    # ---- defect 2: panel-letter offset must not scale with panel height ----

    def test_panel_letter_offset_is_equal_across_unequal_panels(self):
        offsets, heights, _ = self.letter_offsets("AAB\nCCB", (7.0, 4.0))
        self.assertGreater(
            max(heights.values()) / min(heights.values()), 1.5,
            "the mosaic must actually contain panels of different heights",
        )
        spread = max(offsets.values()) - min(offsets.values())
        self.assertLess(
            spread, 0.05,
            f"panel letters misaligned by {spread:.3f}px across panel heights "
            f"{heights}; offsets were {offsets}",
        )

    def test_panel_letter_offset_equals_pad_pt(self):
        fig, ax = plt.subplots(figsize=(3.0, 2.0))
        text = self.kernel.panel_letter(ax, "a", pad_pt=6.0)
        r = self.renderer(fig)
        gap_pt = (text.get_window_extent(renderer=r).y0 - ax.bbox.y1) / fig.dpi * 72.0
        self.assertAlmostEqual(gap_pt, 6.0, places=3)

    def test_panel_letter_offset_survives_a_figure_resize(self):
        """A physical offset is invariant to the panel growing; a fractional one is not."""
        fig, ax = plt.subplots(figsize=(3.0, 2.0))
        text = self.kernel.panel_letter(ax, "a")
        r = self.renderer(fig)
        before = (text.get_window_extent(renderer=r).y0 - ax.bbox.y1) / fig.dpi
        fig.set_size_inches(3.0, 6.0)
        r = self.renderer(fig)
        after = (text.get_window_extent(renderer=r).y0 - ax.bbox.y1) / fig.dpi
        self.assertAlmostEqual(before, after, places=5)

    def test_panel_letter_legacy_dy_warns_instead_of_silently_shifting(self):
        fig, ax = plt.subplots(figsize=(3.0, 2.0))
        with self.assertWarns(DeprecationWarning):
            self.kernel.panel_letter(ax, "a", dy=1.02)

    def test_panel_letter_still_detected_by_panel_crops(self):
        fig, axd = plt.subplot_mosaic("AB", figsize=(6.0, 2.0))
        for key, ax in axd.items():
            ax.plot([0, 1], [0, 1])
            self.kernel.panel_letter(ax, key)
        self.assertEqual(sorted(self.kernel.panel_crops(fig)), ["a", "b"])

    # ---- defect 1: end-of-line labels must not overrun the axes ----

    def two_panel_sheet(self, labels):
        fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.4))
        x = np.linspace(0, 10, 50)
        ys = [np.sin(x) * 0.5 + i for i in range(len(labels))]
        for y in ys:
            axes[0].plot(x, y)
        axes[1].plot(x, np.tanh(x - 5))
        axes[1].set_ylabel("effect size")
        self.kernel.panel_letter(axes[1], "b")
        texts = self.kernel.end_of_line_labels(axes[0], [x] * len(ys), ys, labels)
        return fig, axes, texts

    def test_labels_never_cross_the_owning_axes_right_edge(self):
        fig, axes, texts = self.two_panel_sheet(
            ["Perturb-seq (held-out)", "scGPT fine-tuned"])
        r = self.renderer(fig)
        for text in texts:
            box = text.get_window_extent(renderer=r)
            self.assertLessEqual(
                box.x1, axes[0].bbox.x1,
                f"label {text.get_text()!r} overruns its axes by "
                f"{box.x1 - axes[0].bbox.x1:.1f}px",
            )

    def test_labels_do_not_overlap_the_neighbouring_panel(self):
        fig, axes, texts = self.two_panel_sheet(
            ["Perturb-seq (held-out)", "scGPT fine-tuned"])
        r = self.renderer(fig)
        neighbour = axes[1].get_tightbbox(r)
        total = sum(overlap_area(t.get_window_extent(renderer=r), neighbour)
                    for t in texts)
        self.assertEqual(
            total, 0.0,
            f"labels cover {total:.1f}px^2 of the neighbouring panel",
        )

    def test_short_labels_reserve_room_by_extending_the_axis(self):
        fig, axes, texts = self.two_panel_sheet(["sin", "cos"])
        r = self.renderer(fig)
        self.assertGreater(
            axes[0].get_xlim()[1], 10.0,
            "the x limit should have been extended to hold the labels",
        )
        for text in texts:
            self.assertEqual(text.get_ha(), "left")
            self.assertLessEqual(text.get_window_extent(renderer=r).x1, axes[0].bbox.x1)

    def test_labels_too_wide_to_sit_outside_fall_back_inside_the_axes(self):
        import warnings

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            fig, axes, texts = self.two_panel_sheet(["Perturb-seq (held-out)"])
        r = self.renderer(fig)
        self.assertEqual([t.get_ha() for t in texts], ["right"])
        self.assertEqual(axes[0].get_xlim(), (-0.5, 10.5),
                         "the inside fallback must leave the x limits alone")
        box = texts[0].get_window_extent(renderer=r)
        self.assertLessEqual(box.x1, axes[0].bbox.x1)
        self.assertGreaterEqual(box.x0, axes[0].bbox.x0)
        self.assertEqual([str(w.message) for w in caught], [],
                         "a label that does fit inside must not warn")

    def test_label_wider_than_the_panel_warns_rather_than_claiming_a_fit(self):
        fig, axes = plt.subplots(1, 2, figsize=(3.0, 2.0))
        x = np.linspace(0, 10, 20)
        axes[0].plot(x, np.sin(x))
        with self.assertWarns(RuntimeWarning):
            self.kernel.end_of_line_labels(
                axes[0], [x], [np.sin(x)],
                ["a label far wider than this tiny panel could ever hold"])

    def test_labels_are_returned_and_anchored_to_their_own_series(self):
        fig, axes, texts = self.two_panel_sheet(["sin", "cos"])
        self.assertEqual([t.get_text() for t in texts], ["sin", "cos"])
        for text, y in zip(texts, [0.0, 1.0]):
            self.assertAlmostEqual(
                text.get_position()[1], np.sin(10.0) * 0.5 + y, places=6)

    def test_empty_series_places_nothing(self):
        fig, ax = plt.subplots(figsize=(3.0, 2.0))
        self.assertEqual(self.kernel.end_of_line_labels(ax, [[]], [[]], ["none"]), [])


if __name__ == "__main__":
    unittest.main()
