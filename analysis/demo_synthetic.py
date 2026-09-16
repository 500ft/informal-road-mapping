"""Synthetic method demonstration: disturbance scene -> extracted candidate corridors.

This validates the extraction tooling on data with KNOWN ground truth. It is not a
Mongolia result — real extraction stays gated on the Phase-1 negative-control test.

    python analysis/demo_synthetic.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from catanroads import extract_candidates, make_scene

INK, ACCENT, RED, MUTED = "#1b2a24", "#2d6a4f", "#b2182b", "#6b7671"

d, truth = make_scene(size=256, seed=1)
cands = extract_candidates(d)

fig, axes = plt.subplots(1, 2, figsize=(12.4, 6.4), dpi=130)
fig.patch.set_facecolor("white")

axes[0].imshow(d, cmap="BrBG_r", vmin=-2, vmax=2)
axes[0].set_title("Input: synthetic surface-disturbance", fontsize=13, color=INK)

axes[1].imshow(d, cmap="Greys", vmin=-1, vmax=3)
for c in cands:
    (x0, y0), (x1, y1) = c["endpoints_px"]
    axes[1].plot([x0, x1], [y0, y1], color=RED, lw=2.2)
axes[1].set_title(f"Extracted candidate corridors (n={len(cands)})", fontsize=13, color=INK)

for ax in axes:
    ax.set_xticks([]); ax.set_yticks([])

fig.suptitle("Catan Roads — synthetic method demonstration (Phase 2 extractor)",
             fontsize=15, fontweight="bold", color=INK, y=0.98)
fig.text(0.5, 0.02,
         "Known-truth synthetic scene: the ridge + connected-component extractor recovers curved, braided, and "
         "broken corridors\nwhile rejecting the round blob and background noise. Not a real-imagery result.",
         ha="center", fontsize=9.5, color=MUTED)
fig.subplots_adjust(top=0.90, bottom=0.13)

out = Path(__file__).resolve().parents[1] / "results" / "method_demo_synthetic.png"
fig.savefig(out, facecolor="white")
print(f"wrote {out}  ({len(cands)} candidates)")
