"""Gallery of the CR-09 stress cases: what the extractor delivers (path_px) against what it used to
deliver (the endpoints_px chord), on synthetic constructions with known truth.

    MPLBACKEND=Agg PYTHONPATH=analysis python analysis/plot_stress_cases.py   # -> results/figures/*.png

Numbers in the titles are read from results/extractor_stress_cases.json (schema v4). Synthetic
only: nothing here is imagery or a site result.
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from catanroads import candidate_coordinates_px, extract_candidates
from catanroads import stress_cases as SC

ROOT = Path(__file__).resolve().parents[1]
INK, RED, CHORD, TRUTH, MUTED = "#1b2a24", "#b2182b", "#5f6b64", "#2d6a4f", "#6b7671"
FOOT = "Synthetic construction (analysis/catanroads/stress_cases.py); not imagery, not a site result."


def _f(v):
    return "—" if v is None else f"{v:.2f}"


def draw(ax, d, cl, cands, title, vmin=-1, vmax=3, chords=True, ends=False, note=None):
    ax.imshow(d, cmap="Greys", vmin=vmin, vmax=vmax)
    h, w = d.shape
    ys, xs = np.nonzero(cl)
    ax.scatter(xs, ys, s=1, color=TRUTH, label="reference centerline", zorder=2)
    for k, c in enumerate(cands):
        if chords:
            (x0, y0), (x1, y1) = c["endpoints_px"]
            ax.plot([x0, x1], [y0, y1], "--", color=CHORD, lw=1.4, label="legacy chord (endpoints_px)" if k == 0 else None, zorder=3)
        px, py = zip(*candidate_coordinates_px(c))
        ax.plot(px, py, color=RED, lw=1.8, label="delivered path (path_px)" if k == 0 else None, zorder=4)
        if ends:
            ax.plot([px[0], px[-1]], [py[0], py[-1]], "o", color=RED, ms=5, zorder=5)
    ax.set_xlim(-0.5, w - 0.5); ax.set_ylim(h - 0.5, -0.5)
    ax.set_title(title, fontsize=10.5, color=INK)
    if note:
        ax.set_xlabel(note, fontsize=9, color=MUTED)
    ax.set_xticks([]); ax.set_yticks([])


def plot_all(out_dir):
    out_dir = Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    rec = json.loads((ROOT / "results/extractor_stress_cases.json").read_text())["cases"]

    def scores(name):
        c = rec[name]
        return (f"line recall / precision vs centerline (2 px):  path {_f(c['line_recall'])} / {_f(c['line_precision'])}   ·   "
                f"legacy chord {_f(c['chord_line']['line_recall'])} / {_f(c['chord_line']['line_precision'])}")

    def finish(fig, name, suptitle):
        fig.suptitle(suptitle, fontsize=13, fontweight="bold", color=INK)
        fig.text(0.5, 0.015, FOOT, ha="center", fontsize=8.5, color=MUTED)
        handles, labels = fig.axes[-1].get_legend_handles_labels()
        if handles:
            fig.legend(handles, labels, loc="lower center", bbox_to_anchor=(0.5, 0.045), ncol=3, fontsize=8.5, frameon=False)
        fig.subplots_adjust(top=0.84, bottom=0.2, wspace=0.08)
        path = out_dir / f"{name}.png"; fig.savefig(path, dpi=130, facecolor="white"); plt.close(fig); return path

    written = []
    # 1 — the demo scene: chords vs paths
    d, t, cl = SC.case_demo_reference(); cands = extract_candidates(d)
    fig, axes = plt.subplots(1, 2, figsize=(12, 6.2))
    axes[0].imshow(d, cmap="BrBG_r", vmin=-2, vmax=2); axes[0].set_title("Input: synthetic surface disturbance (known truth)", fontsize=10.5, color=INK)
    axes[0].set_xticks([]); axes[0].set_yticks([])
    draw(axes[1], d, cl, cands, f"Delivered geometry, {len(cands)} candidates", note=scores("demo_reference"))
    written.append(finish(fig, "01_demo_paths_vs_chords", "Demo scene — each accepted component delivered as one path instead of a chord (CR-09)"))
    # 2 — hairpin
    d, t, cl = SC.case_tight_curve(); cands = extract_candidates(d)
    fig, ax = plt.subplots(figsize=(9, 4.4))
    draw(ax, d, cl, cands, "Half-ellipse corridor, 128 px wide and ~20 px tall; endpoints marked", ends=True, note=scores("tight_curve"))
    ax.set_xlim(40, 216); ax.set_ylim(170, 110)
    written.append(finish(fig, "02_hairpin_chord_vs_path", "Hairpin — the chord cuts across the bend; the delivered path follows it"))
    # 3 — wide corridor
    d, t, cl = SC.case_wide_corridor(); cands = extract_candidates(d)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4))
    for ax, (x0, x1), side in zip(axes, ((-0.5, 47.5), (207.5, 255.5)), ("left", "right")):
        draw(ax, d, cl, cands, f"{side} end of the 13-px corridor; endpoint marked", ends=True)
        ax.set_xlim(x0, x1); ax.set_ylim(147.5, 108.5)
    fig.text(0.5, 0.165, scores("wide_corridor") + f"   ·   area coverage {_f(rec['wide_corridor']['area_coverage'])} (2-px band on a 13-px road: a diagnostic, not a penalty)",
             ha="center", fontsize=9, color=MUTED)
    written.append(finish(fig, "03_wide_corridor_centred_endpoints", "Wide corridor — amendment A puts the endpoints on the centre row (A3 target ≥ 0.98)"))
    # 4 — low SNR curve
    d, t, cl = SC.case_low_snr(); cands = extract_candidates(d)
    fig, axes = plt.subplots(1, 2, figsize=(12, 6.2))
    axes[0].imshow(d, cmap="Greys", vmin=-2, vmax=4); axes[0].set_title("Input at 3× the demo noise (σ = 0.9)", fontsize=10.5, color=INK)
    axes[0].set_xticks([]); axes[0].set_yticks([])
    draw(axes[1], d, cl, cands, "Delivered geometry", vmin=-2, vmax=4, note=scores("low_snr"))
    c = rec["low_snr"]
    written.append(finish(fig, "04_low_snr_curve", "Low signal-to-noise curve — component recall "
                          f"{_f(c['pixel_recall'])}; line recall {_f(c['chord_line']['line_recall'])} (chord) → {_f(c['line_recall'])} (path)"))
    # 5 — what stays missed or fabricated
    fig, axes = plt.subplots(1, 3, figsize=(15, 5.6))
    for ax, name, label in zip(axes, ("crossing", "short_segments", "linear_confound_riverbank"),
                               ("Crossing: union component fails min_elongation", "Dashed track: each 9-px dash < min_length_px", "River-bank confound: delivered as the strongest candidate")):
        d, t, cl = SC.CASES[name](); cands = extract_candidates(d); c = rec[name]
        note = (f"{c['n_candidates']} candidate(s), {c['n_false_candidates']} false\n"
                f"component recall {_f(c['pixel_recall'])} · line recall {_f(c['line_recall'])}")
        if c["line_precision"] is not None:
            note += f" / precision {_f(c['line_precision'])}"
        draw(ax, d, cl, cands, label, note=note)
    written.append(finish(fig, "05_misses_and_confound", "What stays missed or fabricated by construction — unchanged by CR-09"))
    return written


if __name__ == "__main__":
    for p in plot_all(ROOT / "results" / "figures"):
        print("wrote", p.relative_to(ROOT))
