#!/usr/bin/env python3
"""Numerical and layout safety helpers for publication figures.

Both helpers exist to refuse a figure that would assert more than its data
supports: ``interp_monotone`` refuses a grid on which interpolation is
ambiguous, and ``label_y_above`` refuses to guess an axis scale it was not
given. Neither ever returns a plausible-looking number in place of an error.

Pure standard library. Nothing outside ``bisect``, ``math`` and ``typing`` is
imported, at module level or anywhere else, so the module imports on a bare
interpreter with no site-packages. This matches the convention in
``skills/figure/figure-style/kernel.py``, where every third-party import sits
inside the function that needs it.
"""

from __future__ import annotations

from bisect import bisect_right
from math import isfinite
from typing import Any, Iterable, Sequence


def interp_monotone(target: Any, xp: Any, fp: Any) -> Any:
    """Linear interpolation on a strictly monotone grid, refusing unsafe grids.

    ``numpy.interp`` documents that ``xp`` must be increasing but does not check
    it: given a decreasing grid it returns numbers that look plausible and are
    wrong. This helper accepts a strictly increasing *or* strictly decreasing
    grid, reverses a decreasing one together with ``fp``, and raises on
    duplicate or direction-changing coordinates rather than returning a value.

    On an increasing grid the results match ``numpy.interp`` exactly, including
    its out-of-range behaviour of clamping to ``fp[0]`` and ``fp[-1]``;
    ``tests/test_figure_safety.py`` property-tests that agreement.

    Args:
        target: A scalar, or an iterable of scalars, to evaluate at. Every value
            must be finite; a NaN target is an upstream bug, not a request.
        xp: Grid coordinates, strictly increasing or strictly decreasing.
        fp: Grid values, same length as ``xp``.

    Returns:
        ``float`` for a scalar ``target``, otherwise ``list[float]``. A list, not
        an ndarray: this module has no numpy dependency. Matplotlib, ``min``,
        ``max`` and ``numpy.asarray`` all accept it.

    Raises:
        ValueError: if the grid is shorter than two points, lengths disagree, any
            value is non-finite, or ``xp`` is not strictly monotone.
    """
    grid = _finite_floats(xp, "xp")
    values = _finite_floats(fp, "fp")
    if len(grid) != len(values):
        raise ValueError(
            f"xp and fp must have equal length; got {len(grid)} and {len(values)}"
        )
    if len(grid) < 2:
        raise ValueError("at least two interpolation points are required")

    steps = [b - a for a, b in zip(grid, grid[1:])]
    if all(step > 0.0 for step in steps):
        pass
    elif all(step < 0.0 for step in steps):
        grid = grid[::-1]
        values = values[::-1]
    else:
        raise ValueError(
            "xp must be strictly monotone; duplicate or direction-changing "
            "coordinates make the interpolation ambiguous, and numpy.interp "
            "would return a silently wrong answer for them"
        )

    if _is_scalar(target):
        return _interp_one(_finite_floats([target], "target")[0], grid, values)
    return [_interp_one(t, grid, values) for t in _finite_floats(target, "target")]


def label_y_above(
    values: Any,
    spread: Any = None,
    *,
    ylim: Sequence[float] | None = None,
    label_height_fraction: float = 0.0,
    pad_fraction: float = 0.04,
) -> float:
    """Y coordinate for a value label drawn above data, per figure-style 3.1.

    Axis assumptions, stated explicitly because the previous version guessed
    them and was silently wrong whenever the guess was:

    1. **The pad is a fraction of the visible y-axis span, not of the data.**
       Rule 3.1 of ``figure-style`` asks that limits clear the data and that
       text never touch a spine. That clearance is a visual distance, so the
       only scale that makes it come out right is ``ylim[1] - ylim[0]``. Pass
       ``ylim`` (from ``ax.get_ylim()``) and the result is correct on any linear
       axis: zero-based, offset such as ``(98, 102)``, negative, or
       small-valued such as ``(0.001, 0.002)``.
    2. **With ``ylim=None`` the data span stands in for the axis span.** That is
       correct only when the axis is scaled tightly to exactly this data. If
       anything else is drawn on the axis, or the limits are set by hand, pass
       ``ylim``. A zero-width data span raises rather than falling back to an
       invented unit.
    3. **The y axis is linear and increasing.** On a log axis a constant
       additive offset is not a constant visual distance; compute the position
       in log space instead. An inverted axis (``ylim[1] < ylim[0]``) is
       refused, since "above" then means numerically below.
    4. ``values`` are bar tops or point centres and ``spread`` is the
       non-negative half-length of the error bar, per element or one scalar.
       Labels are placed above the upper end.
    5. **The returned number is the label's anchor, not its ink.** Rule 3.1 is
       about drawn ink, and text drawn with ``va="bottom"`` occupies height
       above its anchor. Pass ``label_height_fraction`` and the check below
       covers the whole glyph box; leave it at 0.0 and the guarantee covers only
       a zero-height annotation such as a marker or a tick, while a text label's
       glyph tops overshoot the top spine by their own height.

       It is a fraction of the **axes height in pixels**, not a height in data
       units, and that is the point: a data-unit height is only valid for the
       ylim it was measured at, so it goes stale the moment you widen the axis
       to make room, and the correction never converges. The pixel fraction does
       not move when ylim does. Measure it once, after any draw::

           h_px = txt.get_window_extent(fig.canvas.get_renderer()).height
           label_height_fraction = h_px / ax.get_window_extent().height

    When ``ylim`` is given the result is checked against rule 3.1 on both sides:
    the anchor must clear ``max(values + spread)`` by one pad, and the top of
    the glyph box must clear ``ylim[1]`` by one pad. If the top limit is too low
    the raised message names the smallest top that fits, which is what
    :func:`ylim_top_for_label` returns.

    Raises:
        ValueError: on non-finite or empty input, a negative ``spread``, a
            ``pad_fraction`` outside ``[0, 0.5)``, a negative
            ``label_height_fraction``, a ``2 * pad_fraction +
            label_height_fraction`` that reserves the whole axis, a degenerate
            or inverted ``ylim``, a zero-width data span when ``ylim`` is None,
            or a label whose ink would touch the top spine.
    """
    upper = _upper_envelope(values, spread)
    centers = _finite_sequence(values, "values")
    label_height_fraction = _non_negative(label_height_fraction, "label_height_fraction")
    _check_fractions(pad_fraction, label_height_fraction)

    data_max = max(upper)
    if ylim is None:
        span = data_max - min(min(centers), min(upper))
        if span <= 0.0:
            raise ValueError(
                "cannot derive a label offset from a zero-width data span; pass "
                "ylim=ax.get_ylim() so the pad is a fraction of the visible axis"
            )
        return data_max + pad_fraction * span

    bottom, top = _ylim_pair(ylim)
    span = top - bottom
    offset = pad_fraction * span
    label_y = data_max + offset
    # 1e-9 of the axis span is far below any distance a reader or a renderer can
    # resolve. The slack exists so the exact fixed point returned by
    # ylim_top_for_label is not rejected by a one-ulp rounding error.
    if label_y + label_height_fraction * span + offset - top > 1e-9 * span:
        needed = ylim_top_for_label(
            values, spread, bottom=bottom,
            label_height_fraction=label_height_fraction, pad_fraction=pad_fraction,
        )
        raise ValueError(
            f"a label occupying {label_height_fraction:.4g} of the axes height, "
            f"anchored at y={label_y:.6g}, would come within one pad of the top spine "
            f"at y={top:.6g}, violating figure-style 3.1; raise the top limit to at "
            f"least {needed:.6g} (ylim_top_for_label) and recompute"
        )
    return label_y


def ylim_top_for_label(
    values: Any,
    spread: Any = None,
    *,
    bottom: float,
    label_height_fraction: float = 0.0,
    pad_fraction: float = 0.04,
) -> float:
    """Smallest top y-limit at which :func:`label_y_above` satisfies rule 3.1.

    Raising the top limit widens the span, which widens both the pad and the
    label's data-unit height, so the answer is a fixed point rather than
    ``data_max + 2 * pad``. With ``p = pad_fraction`` and
    ``f = label_height_fraction``, solving
    ``data_max + (2 * p + f) * (top - bottom) <= top`` gives the closed form
    used here: exact, and without iteration. This is why the label height is
    taken as a fraction of the axes height rather than in data units; see
    :func:`label_y_above`.

    Typical use, in this order::

        f = txt.get_window_extent(r).height / ax.get_window_extent().height
        bottom = ax.get_ylim()[0]
        ax.set_ylim(bottom, ylim_top_for_label(vals, err, bottom=bottom,
                                               label_height_fraction=f))
        y = label_y_above(vals, err, ylim=ax.get_ylim(), label_height_fraction=f)
    """
    label_height_fraction = _non_negative(label_height_fraction, "label_height_fraction")
    _check_fractions(pad_fraction, label_height_fraction)
    bottom = _finite_floats([bottom], "bottom")[0]
    data_max = max(_upper_envelope(values, spread))
    if data_max <= bottom:
        raise ValueError(
            f"data max {data_max:.6g} is at or below the bottom limit {bottom:.6g}; "
            "no top limit puts the label above the data inside the axis"
        )
    reserved = 2.0 * pad_fraction + label_height_fraction
    return (data_max - reserved * bottom) / (1.0 - reserved)


def _interp_one(x: float, grid: list[float], values: list[float]) -> float:
    """One clamped linear interpolation on a strictly increasing ``grid``."""
    if x <= grid[0]:
        return values[0]
    if x >= grid[-1]:
        return values[-1]
    j = bisect_right(grid, x) - 1
    slope = (values[j + 1] - values[j]) / (grid[j + 1] - grid[j])
    return slope * (x - grid[j]) + values[j]


def _upper_envelope(values: Any, spread: Any) -> list[float]:
    """Per-element ``value + spread``, with ``spread`` scalar, per-element, or None."""
    centers = _finite_sequence(values, "values")
    if spread is None:
        return list(centers)
    spreads = _finite_sequence(spread, "spread")
    if len(spreads) == 1:
        spreads = spreads * len(centers)
    if len(spreads) != len(centers):
        raise ValueError(
            f"spread must be a scalar or match len(values)={len(centers)}; "
            f"got {len(spreads)} values"
        )
    for s in spreads:
        if s < 0.0:
            raise ValueError(
                f"spread is the non-negative half-length of an error bar; got {s!r}"
            )
    return [c + s for c, s in zip(centers, spreads)]


def _check_fractions(pad_fraction: float, label_height_fraction: float) -> None:
    """Both pads plus the label must leave the axis some room for the data."""
    if not 0.0 <= pad_fraction < 0.5:
        raise ValueError(f"pad_fraction must be in [0, 0.5); got {pad_fraction!r}")
    reserved = 2.0 * pad_fraction + label_height_fraction
    if reserved >= 1.0:
        raise ValueError(
            f"2 * pad_fraction + label_height_fraction = {reserved:.6g} would reserve "
            "the whole axis or more; no top limit satisfies figure-style 3.1"
        )


def _non_negative(value: Any, name: str) -> float:
    number = _finite_floats([value], name)[0]
    if number < 0.0:
        raise ValueError(f"{name} must be non-negative; got {number!r}")
    return number


def _ylim_pair(ylim: Any) -> tuple[float, float]:
    """Validate ``ylim`` as an increasing, non-degenerate pair of finite floats."""
    pair = _finite_floats(ylim, "ylim")
    if len(pair) != 2:
        raise ValueError(f"ylim must be a (bottom, top) pair; got {len(pair)} values")
    bottom, top = pair
    if top <= bottom:
        raise ValueError(
            f"ylim must be increasing and non-degenerate; got bottom={bottom!r}, "
            f"top={top!r}. label_y_above assumes an upward y axis"
        )
    return bottom, top


def _finite_sequence(data: Any, name: str) -> list[float]:
    """Coerce a scalar or iterable to a non-empty list of finite floats."""
    items = _finite_floats([data] if _is_scalar(data) else data, name)
    if not items:
        raise ValueError(f"{name} must contain at least one value")
    return items


def _finite_floats(data: Iterable[Any], name: str) -> list[float]:
    try:
        items = [float(v) for v in data]
    except (TypeError, ValueError) as exc:
        raise TypeError(f"{name} must be an iterable of real numbers") from exc
    for v in items:
        if not isfinite(v):
            raise ValueError(f"{name} must contain only finite values; found {v!r}")
    return items


def _is_scalar(value: Any) -> bool:
    """True for anything without a length, including floats and 0-d arrays."""
    try:
        len(value)
    except TypeError:
        return True
    return False


__all__ = ["interp_monotone", "label_y_above", "ylim_top_for_label"]


def run_self_tests() -> None:
    """Exercise every guard. Raises AssertionError on the first failure."""
    # Increasing grid: agrees with ordinary linear interpolation.
    got = interp_monotone(1.5, [0.0, 1.0, 2.0], [0.0, 10.0, 20.0])
    assert abs(got - 15.0) < 1e-12, got

    # Strictly DECREASING is still monotone and must be handled correctly. This
    # is the case that motivates the helper: np.interp(0.5, [2,1,0], [20,10,0])
    # silently returns 0.0 where the answer is 5.0.
    got = interp_monotone(0.5, [2.0, 1.0, 0.0], [20.0, 10.0, 0.0])
    assert abs(got - 5.0) < 1e-12, got

    # Non-monotone grids (a duplicate, or a change of direction) are refused.
    for bad_grid in ([0.0, 1.0, 1.0], [0.0, 2.0, 1.0], [1.0, 0.0, 2.0]):
        try:
            interp_monotone(0.5, bad_grid, [0.0, 10.0, 20.0])
        except ValueError:
            pass
        else:
            raise AssertionError(f"non-monotone grid {bad_grid} was not refused")

    # ylim=None is a documented fallback (the data span stands in for the axis
    # span), not a guess, and it must still clear the data.
    y_nolim = label_y_above([1.0, 2.0])
    assert y_nolim > 2.0, y_nolim

    # A zero-width data span has no unit to scale the pad by, so it raises
    # rather than inventing one.
    try:
        label_y_above([2.0, 2.0])
    except ValueError:
        pass
    else:
        raise AssertionError("a zero-width data span did not raise")

    # An inverted axis is refused: "above" would mean numerically below.
    try:
        label_y_above([1.0, 2.0], ylim=(3.0, 0.0))
    except ValueError:
        pass
    else:
        raise AssertionError("an inverted y axis was not refused")

    # The label clears the data by the pad, inside the given limits.
    y = label_y_above([1.0, 2.0], ylim=(0.0, 3.0), pad_fraction=0.04)
    assert 2.0 < y <= 3.0, y

    # ylim_top_for_label returns a top at which the label actually fits.
    top = ylim_top_for_label([1.0, 2.0], bottom=0.0, label_height_fraction=0.05)
    placed = label_y_above([1.0, 2.0], ylim=(0.0, top), label_height_fraction=0.05)
    assert placed <= top + 1e-9, (placed, top)

    print("figure_safety.py self-test: PASS")


if __name__ == "__main__":
    import sys

    if "--self-test" in sys.argv[1:]:
        run_self_tests()
        raise SystemExit(0)
    print(
        "figure_safety is a library, not a CLI. Import interp_monotone, "
        "label_y_above or ylim_top_for_label, or run --self-test.",
        file=sys.stderr,
    )
    raise SystemExit(2)
