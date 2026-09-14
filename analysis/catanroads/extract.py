"""Candidate corridor extraction from a surface-disturbance raster.

Phase-2 baseline (numpy + scipy only): a multiscale Hessian ridge filter enhances
elongated bright features, then connected components are kept only if they are long
and elongated enough to be corridor-scale — rejecting round blobs and isolated
noise. Each survivor becomes a candidate LineString with geometry and attributes.

This is the *thresholded-connected-components + ridge* baseline named in the design.
Skeletonization + graph tracing and shapely/rasterio I/O are the scikit-image /
shapely extensions, added when those optional dependencies are installed.

Nothing here is applied to real imagery yet: per the project's go/no-go gate, real
extraction is blocked until the Phase-1 disturbance signal survives its negative
control. These functions are validated on synthetic corridors (see tests/).
"""
from __future__ import annotations

import numpy as np
from scipy import ndimage


def ridge_strength(img: np.ndarray, sigmas=(1.0, 2.0, 3.0)) -> np.ndarray:
    """Multiscale bright-ridge response via Hessian eigenvalues (Sato-like).

    For a bright line on a darker background the smaller Hessian eigenvalue is
    strongly negative; its magnitude (scale-normalized) is the ridge response.
    """
    img = np.asarray(img, dtype=float)
    out = np.zeros_like(img)
    for s in sigmas:
        dyy = ndimage.gaussian_filter(img, s, order=(2, 0))
        dxx = ndimage.gaussian_filter(img, s, order=(0, 2))
        dxy = ndimage.gaussian_filter(img, s, order=(1, 1))
        tmp = np.sqrt((dxx - dyy) ** 2 + 4.0 * dxy ** 2)
        lam_small = 0.5 * (dxx + dyy - tmp)          # more-negative eigenvalue
        resp = np.maximum(0.0, -lam_small) * (s ** 2)  # scale-normalized
        out = np.maximum(out, resp)
    return out


def label_candidates(disturbance, disturb_thresh: float = 1.0, ridge_sigmas=(1.0, 2.0, 3.0),
                     ridge_quantile: float = 0.85):
    """8-connected labels of the candidate mask: disturbance >= ``disturb_thresh`` AND ridge
    response in the top ``1 - ridge_quantile``. Returns ``(labels, n)`` like ``ndimage.label``."""
    d = np.asarray(disturbance, dtype=float)
    ridge = ridge_strength(d, ridge_sigmas)
    pos = ridge[ridge > 0]
    rt = np.quantile(pos, ridge_quantile) if pos.size else np.inf
    return ndimage.label((d >= disturb_thresh) & (ridge >= rt), structure=np.ones((3, 3)))


def extract_candidates(
    disturbance: np.ndarray,
    disturb_thresh: float = 1.0,
    ridge_sigmas=(1.0, 2.0, 3.0),
    ridge_quantile: float = 0.85,
    min_length_px: float = 12.0,
    min_elongation: float = 3.0,
) -> list[dict]:
    """Return candidate corridor segments, most prominent first.

    Components of ``label_candidates`` are kept only if long (``min_length_px``) and
    elongated (``min_elongation``), which rejects round blobs and short noise specks.
    """
    d = np.asarray(disturbance, dtype=float)
    lbl, n = label_candidates(d, disturb_thresh, ridge_sigmas, ridge_quantile)
    candidates: list[dict] = []
    for i in range(1, n + 1):
        ys, xs = np.where(lbl == i)
        if xs.size < 3:
            continue
        pts = np.column_stack([xs, ys]).astype(float)   # (x, y)
        c = pts.mean(axis=0)
        evals, evecs = np.linalg.eigh(np.cov((pts - c).T))   # ascending
        lam_min, lam_max = float(evals[0]), float(evals[1])
        if lam_max <= 1e-9:
            continue
        elong = float(np.sqrt(lam_max / max(lam_min, 1e-9)))
        major = evecs[:, 1]
        minor = evecs[:, 0]
        proj = (pts - c) @ major
        projm = (pts - c) @ minor
        length = float(proj.max() - proj.min())
        width = float(projm.max() - projm.min())
        if length < min_length_px or elong < min_elongation:
            continue
        p0 = c + major * proj.min()
        p1 = c + major * proj.max()
        orient = float(np.degrees(np.arctan2(major[1], major[0])) % 180.0)
        candidates.append({
            "id": int(i),
            "centroid_px": [float(c[0]), float(c[1])],
            "endpoints_px": [[float(p0[0]), float(p0[1])], [float(p1[0]), float(p1[1])]],
            "length_px": length,
            "width_px": width,
            "orientation_deg": orient,
            "elongation": elong,
            "mean_disturbance": float(d[ys, xs].mean()),
            "n_pixels": int(xs.size),
        })
    candidates.sort(key=lambda k: k["length_px"] * k["mean_disturbance"], reverse=True)
    return candidates


def to_geojson(candidates: list[dict], transform=None) -> dict:
    """FeatureCollection of candidate LineStrings.

    ``transform`` is an optional ``(x_px, y_px) -> (lon, lat)`` callable; without it
    coordinates are left in pixel space. No shapely dependency required.
    """
    features = []
    for c in candidates:
        coords = c["endpoints_px"]
        if transform is not None:
            coords = [list(transform(x, y)) for x, y in coords]
        props = {k: v for k, v in c.items() if k != "endpoints_px"}
        features.append({
            "type": "Feature",
            "geometry": {"type": "LineString", "coordinates": coords},
            "properties": props,
        })
    return {"type": "FeatureCollection", "features": features}
