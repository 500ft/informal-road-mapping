"""Fixed synthetic stress cases for the corridor extractor (CR-R03).

The demonstration scene (synthetic.make_scene) is favourable: strong straight-ish corridors on
Gaussian noise. These cases are constructed to find where extract_candidates detects, misses,
or fabricates corridors. Docstrings describe the construction only; what the extractor DID on
each case is recorded in results/extractor_stress_cases.json and tested in
tests/test_stress_cases.py, so a change in behaviour is a test failure, not a surprise.
Every case is deterministic (fixed seed, fixed geometry) and carries
its own ground-truth mask, so per-case pixel recall, pixel precision and false-candidate
counts are computed, never eyeballed. Nothing here is imagery; the numbers describe the
algorithm's behaviour on constructions, not any site.

Scoring (per case), two layers that must not be confused (review 2026-09-12):
  COMPONENT layer -- what the extractor's internal mask covered:
    pixel_recall     fraction of truth pixels lying within `tol_px` of any candidate's pixels
    pixel_precision  fraction of candidate pixels within `tol_px` of the truth mask
    false_candidates candidates whose pixels have < 20 % overlap (dilated) with the truth mask
  LINE layer -- what the extractor actually EXPORTS (path_px, a polyline; CR-09. Until CR-09 this
  was the straight endpoints_px chord), scored against each case's REFERENCE CENTERLINE (never the
  road-area mask; review 2, 2026-09-12):
    line_recall      fraction of reference-centerline pixels within `tol_px` of the exported polyline
    line_precision   fraction of exported-polyline pixels within `tol_px` of the reference centerline
    area_coverage    fraction of the road-AREA mask the exported band covers -- a separate diagnostic
  detected         pixel_recall >= 0.5 (component layer, deliberately coarse)
  line_ok          line_recall >= 0.5 AND line_precision >= 0.5
The component layer can be excellent while the delivered geometry is wrong (a hairpin exported as
one straight chord, as it was before CR-09); only the line layer sees that. width_px is the component's
minor-axis EXTENT, not road width: for a curved corridor it is the curve's transverse extent and is
~55 px with zero noise.
"""
from __future__ import annotations
import numpy as np
from scipy import ndimage
from .extract import extract_candidates, label_candidates
from .synthetic import make_scene


def _stamp(d, truth, xs, ys, half_width, strength, centerline=None):
    """Stamp a corridor of the given half-width and, if given, record its 1-px reference CENTERLINE."""
    size = d.shape[0]
    for x, y in zip(xs, ys):
        for dy in range(-half_width, half_width + 1):
            yy, xx = int(round(y + dy)), int(round(x))
            if 0 <= yy < size and 0 <= xx < size:
                d[yy, xx] += strength; truth[yy, xx] = True
        if centerline is not None:
            yy, xx = int(round(y)), int(round(x))
            if 0 <= yy < size and 0 <= xx < size: centerline[yy, xx] = True


def _base(size, seed, noise):
    """(disturbance, empty truth mask, empty reference centerline, rng)."""
    rng = np.random.default_rng(seed)
    return rng.normal(0.0, noise, (size, size)), np.zeros((size, size), dtype=bool), np.zeros((size, size), dtype=bool), rng


def case_faint_corridor(size=256, seed=11, noise=0.3, strength=1.15):
    """A single straight corridor with strength near disturb_thresh=1.0 (default 1.15 on noise 0.3)."""
    d, truth, cl, _ = _base(size, seed, noise)
    x = np.arange(size); _stamp(d, truth, x, np.full(size, size * 0.5), 1, strength, centerline=cl)
    return d, truth, cl


def case_wide_corridor(size=256, seed=12, noise=0.3, half_width=6):
    """A 13-px-wide corridor (graded road at coarse resolution); ridge sigmas top out at 3 px."""
    d, truth, cl, _ = _base(size, seed, noise)
    x = np.arange(size); _stamp(d, truth, x, np.full(size, size * 0.5), half_width, 2.4, centerline=cl)
    return d, truth, cl


def case_crossing(size=256, seed=13, noise=0.3):
    """Two full-width corridors crossing at 90 degrees; they form one 8-connected component."""
    d, truth, cl, _ = _base(size, seed, noise)
    x = np.arange(size)
    _stamp(d, truth, x, np.full(size, size * 0.5), 1, 2.4, centerline=cl)
    _stamp(d, truth, np.full(size, size * 0.5), x, 1, 2.4, centerline=cl)
    return d, truth, cl


def case_short_segments(size=256, seed=14, noise=0.3, seg_len=9, gap=7):
    """A corridor visible only as 9-px dashes with 7-px gaps (each dash < min_length_px=12)."""
    d, truth, cl, _ = _base(size, seed, noise)
    x = np.arange(size); keep = (x % (seg_len + gap)) < seg_len
    _stamp(d, truth, x[keep], np.full(int(keep.sum()), size * 0.4), 1, 2.4, centerline=cl)
    return d, truth, cl


def case_linear_confound_riverbank(size=256, seed=15, noise=0.3):
    """A long, thin, high-disturbance feature that is NOT a road (river bank / fence line / field
    edge). Truth mask is empty by construction."""
    d, truth, cl, _ = _base(size, seed, noise)
    x = np.arange(size); y = size * 0.3 + 0.2 * size * np.sin(x / (size / 2.5))
    _stamp(d, truth.copy(), x, y, 1, 2.4)                # truth stays empty: nothing here is a road
    return d, truth, cl


def case_speckle_only(size=256, seed=16, noise=0.3, n_specks=400):
    """Isolated speckle (cloud shadow, bare-rock pixels) with no corridor; truth mask empty."""
    d, truth, cl, rng = _base(size, seed, noise)
    ys, xs = rng.integers(0, size, n_specks), rng.integers(0, size, n_specks)
    d[ys, xs] += rng.uniform(1.5, 3.0, n_specks)
    return d, truth, cl


def case_low_snr(size=256, seed=17, noise=0.9):
    """The demo's curved corridor under 3x the demo noise (sigma 0.9)."""
    d, truth, cl, _ = _base(size, seed, noise)
    x = np.arange(size); y = size * 0.35 + 0.12 * size * np.sin(x / (size / 6.0))
    _stamp(d, truth, x, y, 1, 2.6, centerline=cl)
    return d, truth, cl


def case_gradient_background(size=256, seed=18, noise=0.3, ramp=2.5):
    """A smooth disturbance ramp 0..2.5 across the scene (regional bare-soil gradient) under a
    straight corridor; more than half the background exceeds disturb_thresh."""
    d, truth, cl, _ = _base(size, seed, noise)
    d += np.linspace(0, ramp, size)[None, :]
    x = np.arange(size); _stamp(d, truth, x, np.full(size, size * 0.6), 1, 2.4, centerline=cl)
    return d, truth, cl


def case_tight_curve(size=256, seed=19, noise=0.3):
    """A hairpin: a half-ellipse corridor 128 px wide and ~20 px tall."""
    d, truth, cl, _ = _base(size, seed, noise)
    t = np.linspace(0, np.pi, 300)
    xs = size * 0.5 + size * 0.25 * np.cos(t); ys = size * 0.5 + size * 0.08 * np.sin(t)
    _stamp(d, truth, xs, ys, 1, 2.4, centerline=cl)
    return d, truth, cl


def case_demo_reference(size=256, seed=1, noise=0.3):
    """The favourable demonstration scene itself, for scale. Its reference centerlines are the
    scene generator's own parametric curves (synthetic.make_scene): the curved corridor, the two
    braided tracks, and the dashed diagonal. No new dependency; a test pins this reconstruction
    to the generator's truth mask."""
    d, truth = make_scene(size=size, seed=seed, noise=noise)
    cl = np.zeros((size, size), dtype=bool)
    x = np.arange(size)
    curves = [(x, size * 0.35 + 0.12 * size * np.sin(x / (size / 6.0)))]
    yb = size * 0.62 + 0.05 * size * np.sin(x / (size / 5.0)); curves += [(x, yb - 2), (x, yb + 2)]
    xd = np.arange(int(size * 0.15), int(size * 0.85)); yd = size * 0.85 - 0.6 * (xd - xd[0]); keep = (xd // 8) % 3 != 0
    curves.append((xd[keep], yd[keep]))
    for xs, ys in curves:                         # same int() truncation as synthetic._stamp_line
        for xx, yy in zip(xs, ys):
            yy, xx = int(yy), int(xx)
            if 0 <= yy < size and 0 <= xx < size: cl[yy, xx] = True
    return d, truth, cl


CASES = {
    "demo_reference": case_demo_reference,
    "faint_corridor": case_faint_corridor,
    "wide_corridor": case_wide_corridor,
    "crossing": case_crossing,
    "short_segments": case_short_segments,
    "linear_confound_riverbank": case_linear_confound_riverbank,
    "speckle_only": case_speckle_only,
    "low_snr": case_low_snr,
    "gradient_background": case_gradient_background,
    "tight_curve": case_tight_curve,
}


def candidate_pixel_mask(disturbance, candidates, **kw):
    """Re-derive the labelled mask the extractor used, restricted to the returned candidate ids."""
    lbl, _ = label_candidates(disturbance, **{k: v for k, v in kw.items() if k in ("disturb_thresh", "ridge_sigmas", "ridge_quantile")})
    per = {c["id"]: (lbl == c["id"]) for c in candidates}
    return np.isin(lbl, list(per)), per


def _dilate(mask, tol_px):
    return ndimage.binary_dilation(mask, ndimage.generate_binary_structure(2, 1), iterations=tol_px) if mask.any() else mask


def _fraction_within(of, band):
    """Fraction of `of` pixels lying inside `band` (a dilated mask); None if `of` is empty."""
    return float((of & band).sum() / of.sum()) if of.any() else None


def rasterise_segments(candidates, shape):
    """Pixels of the polylines the extractor exports (path_px, consecutive vertex pairs), 8-connected."""
    m = np.zeros(shape, dtype=bool)
    for c in candidates:
        for (x0, y0), (x1, y1) in zip(c["path_px"], c["path_px"][1:]):
            n = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
            xs = np.rint(np.linspace(x0, x1, n)).astype(int); ys = np.rint(np.linspace(y0, y1, n)).astype(int)
            ok = (xs >= 0) & (xs < shape[1]) & (ys >= 0) & (ys < shape[0])
            m[ys[ok], xs[ok]] = True
    return m


def score_lines(centerline, candidates, tol_px=2, truth=None):
    """Exported polylines (path_px) against the REFERENCE CENTERLINE (review 2, 2026-09-12): a
    perfect centerline scores 1.0 regardless of road width. `line_recall`/`line_precision` are
    centerline-to-centerline within tol_px. If the road-area `truth` mask is also given, the
    fraction of it the tolerance band covers is reported separately as `area_coverage` -- a
    diagnostic, never part of line_ok."""
    ref = np.asarray(centerline, dtype=bool)
    line = rasterise_segments(candidates, ref.shape)
    line_d = _dilate(line, tol_px)
    recall, precision = _fraction_within(ref, line_d), _fraction_within(line, _dilate(ref, tol_px))
    out = dict(line_recall=recall, line_precision=precision, line_pixels=int(line.sum()), reference_centerline_pixels=int(ref.sum()),
               line_ok=(recall is not None and precision is not None and recall >= 0.5 and precision >= 0.5))
    if truth is not None:
        out["area_coverage"] = _fraction_within(np.asarray(truth, dtype=bool), line_d)
    return out


def score(disturbance, truth, candidates, tol_px=2, centerline=None, **kw):
    truth = np.asarray(truth, dtype=bool)
    cand_mask, per = candidate_pixel_mask(disturbance, candidates, **kw)
    truth_d = _dilate(truth, tol_px)
    recall, precision = _fraction_within(truth, _dilate(cand_mask, tol_px)), _fraction_within(cand_mask, truth_d)
    false_ids = [cid for cid, m in per.items() if (m & truth_d).sum() < 0.2 * m.sum()]
    out = dict(n_candidates=len(candidates), n_false_candidates=len(false_ids), false_candidate_ids=false_ids,
               pixel_recall=recall, pixel_precision=precision,
               detected=(recall is not None and recall >= 0.5), truth_pixels=int(truth.sum()), candidate_pixels=int(cand_mask.sum()))
    if centerline is None:
        raise ValueError("score() needs the case's reference centerline; every CASES entry returns (d, truth, centerline)")
    out.update(score_lines(centerline, candidates, tol_px, truth=truth))
    return out


def run_all(**kw):
    out = {}
    for name, fn in CASES.items():
        d, truth, cl = fn()
        cands = extract_candidates(d, **kw)
        s = score(d, truth, cands, centerline=cl, **kw)
        s["doc"] = " ".join((fn.__doc__ or "").split())
        s["top_candidates"] = [{k: round(c[k], 3) for k in ("length_px", "width_px", "elongation", "mean_disturbance", "n_pixels")} for c in cands[:3]]
        s["note_width_px"] = "minor-axis extent of the component, not road width"
        out[name] = s
    return out


def faint_strength_sweep(strengths=(1.3, 1.15, 1.05, 1.0, 0.9), **kw):
    """Detection cliff: the same straight corridor at decreasing strength relative to disturb_thresh."""
    out = []
    for st in strengths:
        d, truth, cl = case_faint_corridor(strength=st)
        cands = extract_candidates(d, **kw); sc = score(d, truth, cands, centerline=cl, **kw)
        out.append(dict(strength=st, n_candidates=sc["n_candidates"], pixel_recall=sc["pixel_recall"]))
    return out



def curve_extent_without_noise():
    """The curved corridor's width_px at zero noise, to show width_px measures curve extent, not road width."""
    d, _, _ = case_low_snr(noise=0.0)
    c = extract_candidates(d)
    return {"width_px_noise_0": c[0]["width_px"] if c else None, "true_road_thickness_px": 3, "curve_peak_to_peak_px": 2 * 0.12 * 256}


if __name__ == "__main__":
    import json, sys
    out = {"cases": run_all(), "faint_strength_sweep": faint_strength_sweep(), "curve_extent_without_noise": curve_extent_without_noise()}
    json.dump(out, sys.stdout, indent=1); print()
