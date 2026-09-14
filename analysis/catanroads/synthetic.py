"""Synthetic surface-disturbance scenes for validating candidate extraction.

The whole point of a synthetic generator is that ground truth is known, so the
extractor can be measured (recall on corridors, rejection of blobs and noise)
without any real imagery — which keeps tooling development independent of the
Phase-1 data gate.
"""
from __future__ import annotations

import numpy as np


def _stamp_line(d, truth, xs, ys, half_width, strength):
    size = d.shape[0]
    for x, y in zip(xs, ys):
        for dy in range(-half_width, half_width + 1):
            yy, xx = int(y + dy), int(x)
            if 0 <= yy < size and 0 <= xx < size:
                d[yy, xx] += strength
                truth[yy, xx] = True


def make_scene(size: int = 256, seed: int = 0, noise: float = 0.3,
               with_corridors: bool = True, with_blob: bool = True) -> tuple[np.ndarray, np.ndarray]:
    """Return (disturbance, truth_mask).

    Contents (when enabled): a curved corridor, a braided pair of parallel tracks,
    a broken/dashed corridor, plus a round high-disturbance blob (a confound the
    extractor must reject) and background noise.
    """
    rng = np.random.default_rng(seed)
    d = rng.normal(0.0, noise, (size, size))
    truth = np.zeros((size, size), dtype=bool)

    if with_corridors:
        x = np.arange(size)
        # curved corridor
        y = (size * 0.35 + 0.12 * size * np.sin(x / (size / 6.0)))
        _stamp_line(d, truth, x, y, half_width=1, strength=2.6)
        # braided pair (two near-parallel tracks)
        yb = (size * 0.62 + 0.05 * size * np.sin(x / (size / 5.0)))
        _stamp_line(d, truth, x, yb - 2, half_width=0, strength=2.2)
        _stamp_line(d, truth, x, yb + 2, half_width=0, strength=2.2)
        # broken/dashed corridor (diagonal, with gaps)
        xd = np.arange(int(size * 0.15), int(size * 0.85))
        yd = (size * 0.85 - 0.6 * (xd - xd[0]))
        keep = (xd // 8) % 3 != 0            # periodic gaps
        _stamp_line(d, truth, xd[keep], yd[keep], half_width=1, strength=2.4)

    if with_blob:
        cy, cx, r = int(size * 0.5), int(size * 0.8), int(size * 0.06)
        yy, xx = np.ogrid[:size, :size]
        blob = (yy - cy) ** 2 + (xx - cx) ** 2 <= r ** 2
        d[blob] += 2.6                        # strong but ROUND -> must be rejected

    return d, truth
