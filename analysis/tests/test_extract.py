"""Synthetic-corridor tests for the candidate extractor: python -m pytest analysis/tests"""
import numpy as np
from catanroads import extract_candidates, make_scene, to_geojson


def _hits_truth(cand, truth, tol=3):
    """True if the candidate's centerline passes over truth pixels."""
    (x0, y0), (x1, y1) = cand["endpoints_px"]
    for t in np.linspace(0, 1, 60):
        x, y = int(round(x0 + t * (x1 - x0))), int(round(y0 + t * (y1 - y0)))
        y0l, y1l = max(0, y - tol), min(truth.shape[0], y + tol + 1)
        x0l, x1l = max(0, x - tol), min(truth.shape[1], x + tol + 1)
        if truth[y0l:y1l, x0l:x1l].any():
            return True
    return False


def test_finds_corridors():
    d, truth = make_scene(seed=1)
    cands = extract_candidates(d)
    assert len(cands) >= 1, "expected at least one candidate corridor"
    assert any(_hits_truth(c, truth) for c in cands), "no candidate overlaps a true corridor"


def test_rejects_pure_noise():
    # No corridors, no blob: a road-free control. Long linear candidates must be rare.
    d, _ = make_scene(seed=2, with_corridors=False, with_blob=False)
    cands = extract_candidates(d)
    assert len(cands) == 0, f"noise-only scene produced {len(cands)} false corridors"


def test_rejects_round_blob():
    # Only a strong ROUND blob: high disturbance but not elongated -> must be rejected.
    d, _ = make_scene(seed=3, with_corridors=False, with_blob=True)
    cands = extract_candidates(d)
    assert len(cands) == 0, "round blob was wrongly accepted as a corridor"


def test_geojson_shape():
    d, _ = make_scene(seed=4)
    cands = extract_candidates(d)
    gj = to_geojson(cands)
    assert gj["type"] == "FeatureCollection" and len(gj["features"]) == len(cands)
    for f, c in zip(gj["features"], cands):
        assert f["geometry"]["type"] == "LineString"
        assert f["geometry"]["coordinates"] == c["path_px"] and len(c["path_px"]) >= 2
        assert "length_px" in f["properties"] and "elongation" in f["properties"] and "path_length_px" in f["properties"]
        assert "path_px" not in f["properties"] and "endpoints_px" not in f["properties"]


def test_transform_applied_to_every_vertex():
    d, _ = make_scene(seed=5)
    cands = extract_candidates(d)
    assert cands
    gj = to_geojson(cands, transform=lambda x, y: (100.0 + x * 1e-4, 47.0 - y * 1e-4))
    for f, c in zip(gj["features"], cands):
        expect = [[100.0 + x * 1e-4, 47.0 - y * 1e-4] for x, y in c["path_px"]]
        assert np.allclose(f["geometry"]["coordinates"], expect)


def test_geojson_prefers_path_over_conflicting_chord_and_accepts_legacy_dicts():
    # A5: conflicting chord/path -> the path is delivered. Endpoint-only legacy dicts still export.
    c = dict(id=1, endpoints_px=[[0.0, 0.0], [9.0, 9.0]], path_px=[[0.0, 5.0], [4.0, 5.0], [9.0, 5.0]], length_px=9.0)
    assert to_geojson([c])["features"][0]["geometry"]["coordinates"] == c["path_px"]
    legacy = dict(id=2, endpoints_px=[[0.0, 0.0], [9.0, 9.0]])
    assert to_geojson([legacy])["features"][0]["geometry"]["coordinates"] == legacy["endpoints_px"]
    assert to_geojson([]) == {"type": "FeatureCollection", "features": []}

