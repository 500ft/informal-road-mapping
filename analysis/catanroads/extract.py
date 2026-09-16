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

_TIE = dict(rtol=1e-12, atol=1e-12)


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


def _component_path_px(mask):
    """One interior-biased representative path through one accepted component (CR-09 plan,
    docs/PLAN_2026-09-14_CR09.md, algorithm contract steps 1-6).

    ``mask`` is the tight boolean crop of a single 8-connected component. Returns crop-local
    ``[x, y]`` pixel centres, every vertex kept, oriented with the lower endpoint node ID first.
    EDT is computed on a one-pixel padded crop, so the image border counts as background.
    Endpoints: two geometric farthest-point sweeps from node 0 (a heuristic, not an exact
    diameter). Route: symmetric cost ``ell * (1/edt(u) + 1/edt(v)) / 2`` and canonical
    reconstruction from the distance labels (lowest-ID neighbour, strictly decreasing).
    Raises ``ValueError`` for an empty or disconnected mask or an invalid label chain.
    """
    # ponytail: one route per component; branches, loops and braided topology are out of scope,
    # use separately scoped topology extraction when that is needed.
    mask = np.asarray(mask, dtype=bool)
    ys, xs = np.nonzero(mask)                      # row-major node IDs
    n = xs.size
    if n == 0:
        raise ValueError("empty component mask")
    idx = np.full(mask.shape, -1); idx[ys, xs] = np.arange(n)
    edt = ndimage.distance_transform_edt(np.pad(mask, 1))[1:-1, 1:-1]
    src, dst, ell = [], [], []
    for dy, dx in ((0, 1), (1, 0), (1, 1), (1, -1)):
        y2, x2 = ys + dy, xs + dx
        ok = (y2 >= 0) & (y2 < mask.shape[0]) & (x2 >= 0) & (x2 < mask.shape[1])
        ok[ok] &= idx[y2[ok], x2[ok]] >= 0
        u, v = idx[ys[ok], xs[ok]], idx[y2[ok], x2[ok]]
        src += [u, v]; dst += [v, u]; ell += [np.full(u.size, np.hypot(dy, dx))] * 2
    src, dst, ell = map(np.concatenate, (src, dst, ell))
    geometric = coo_matrix((ell, (src, dst)), shape=(n, n)).tocsr()

    def farthest(dist):
        dist = np.where(np.isfinite(dist), dist, -np.inf)
        return int(np.flatnonzero(np.isclose(dist, dist.max(), **_TIE))[0])   # ties -> lowest ID

    d0 = dijkstra(geometric, directed=True, indices=0)
    if not np.isfinite(d0).all():
        raise ValueError("component mask is not 8-connected")
    a = farthest(d0); b = farthest(dijkstra(geometric, directed=True, indices=a))
    a, b = min(a, b), max(a, b)
    depth = edt[ys, xs]
    weighted = coo_matrix((ell * (1 / depth[src] + 1 / depth[dst]) / 2, (src, dst)), shape=(n, n)).tocsr()
    d = dijkstra(weighted, directed=True, indices=a)
    if not np.isfinite(d[b]):
        raise ValueError("endpoint unreachable")
    path = [b]
    while path[-1] != a:
        cur = path[-1]
        nb = weighted.indices[weighted.indptr[cur]:weighted.indptr[cur + 1]]
        w = weighted.data[weighted.indptr[cur]:weighted.indptr[cur + 1]]
        ok = nb[np.isclose(d[cur], w + d[nb], **_TIE) & (d[nb] < d[cur])]
        if ok.size == 0:
            raise ValueError("invalid distance-label chain")
        path.append(int(ok.min()))
    path = np.asarray(path[::-1])
    return np.column_stack([xs[path], ys[path]]).astype(float).tolist()


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
    crops = ndimage.find_objects(lbl)
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
        sl = crops[i - 1]                                  # CR-09 T07: attach after acceptance, never rank by it
        path = (np.asarray(_component_path_px(lbl[sl] == i)) + [sl[1].start, sl[0].start])
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
            "path_px": path.tolist(),
            "path_length_px": float(np.hypot(*np.diff(path, axis=0).T).sum()),
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
