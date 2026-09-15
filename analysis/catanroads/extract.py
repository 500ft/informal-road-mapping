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
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra


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


def medial_path(component, proj, step=4):
    """Centred polyline through one component (CR-09): the cheapest 8-connected route between the
    component's two ends, with edge cost 1/edt so the route hugs the medial axis. The ends are the
    deepest pixels at the extremes of ``proj`` (the pixels' projection on the major axis, in
    ``np.nonzero`` order). Returns a list of ``[x, y]`` vertices."""
    h, w = component.shape
    ys, xs = np.nonzero(component)
    idx = np.full(component.shape, -1); idx[ys, xs] = np.arange(xs.size)
    edt = ndimage.distance_transform_edt(component)
    src, dst, cost = [], [], []
    for dy, dx in ((0, 1), (1, 0), (1, 1), (1, -1)):        # half the 8-neighbourhood; graph is undirected
        y2, x2 = ys + dy, xs + dx
        ok = (y2 >= 0) & (y2 < h) & (x2 >= 0) & (x2 < w)
        ok[ok] &= idx[y2[ok], x2[ok]] >= 0
        src.append(idx[ys[ok], xs[ok]]); dst.append(idx[y2[ok], x2[ok]])
        cost.append(np.hypot(dy, dx) * (1 / edt[ys[ok], xs[ok]] + 1 / edt[y2[ok], x2[ok]]) / 2)
    g = coo_matrix((np.concatenate(cost), (np.concatenate(src), np.concatenate(dst))), shape=(xs.size,) * 2).tocsr()
    depth = edt[ys, xs]
    a = int(np.argmax(np.where(proj <= proj.min() + 1, depth, -1)))
    b = int(np.argmax(np.where(proj >= proj.max() - 1, depth, -1)))
    _, pred = dijkstra(g, directed=False, indices=a, return_predecessors=True)
    path = [b]
    while path[-1] != a:
        path.append(pred[path[-1]])
    path = np.asarray(path[::-1])
    # ponytail: fixed 4-px subsample; Douglas-Peucker when someone needs fewer vertices
    keep = np.r_[0:len(path) - 1:step, len(path) - 1]
    return np.column_stack([xs[path[keep]], ys[path[keep]]]).astype(float).tolist()


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
    ``endpoints_px`` is the straight major-axis chord (summary geometry); ``path_px`` is the
    centred polyline actually exported (see ``medial_path``).
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
            "path_px": medial_path(lbl == i, proj),
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
    """FeatureCollection of candidate LineStrings along each candidate's ``path_px``.

    ``transform`` is an optional ``(x_px, y_px) -> (lon, lat)`` callable; without it
    coordinates are left in pixel space. No shapely dependency required.
    """
    features = []
    for c in candidates:
        coords = c["path_px"]
        if transform is not None:
            coords = [list(transform(x, y)) for x, y in coords]
        props = {k: v for k, v in c.items() if k not in ("path_px", "endpoints_px")}
        features.append({
            "type": "Feature",
            "geometry": {"type": "LineString", "coordinates": coords},
            "properties": props,
        })
    return {"type": "FeatureCollection", "features": features}
