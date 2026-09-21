"""Synthetic-corridor tests for the candidate extractor: python -m pytest analysis/tests"""
import json
import math

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


def test_geojson_coordinate_probe_unequal_scales_hand_computed():
    # Guidance 2026-09-21 section 2: an expectation recomputed from the same lambda only proves the
    # same function ran. These vertices are computed by hand under (x, y) -> (100 + 2x, 200 - 3y),
    # whose x and y scales differ in magnitude and sign, so a swapped or transposed axis fails.
    c = dict(id=1, path_px=[[0.0, 0.0], [3.0, 1.0], [10.0, 4.0]], endpoints_px=[[0.0, 0.0], [10.0, 4.0]])
    gj = to_geojson([c], transform=lambda x, y: (100.0 + 2.0 * x, 200.0 - 3.0 * y))
    assert gj["features"][0]["geometry"]["coordinates"] == [[100.0, 200.0], [106.0, 197.0], [120.0, 188.0]]


def test_geojson_survives_serialization_round_trip():
    # Guidance 2026-09-21 section 4: in-memory equality misses serialization. Write the document
    # out, read it back, and compare ids, vertex order, coordinates and path-length semantics.
    d, _ = make_scene(seed=6)
    cands = extract_candidates(d)
    assert cands
    reloaded = json.loads(json.dumps(to_geojson(cands)))
    assert [f["properties"]["id"] for f in reloaded["features"]] == [c["id"] for c in cands]
    for f, c in zip(reloaded["features"], cands):
        assert f["geometry"]["type"] == "LineString"
        assert f["geometry"]["coordinates"] == c["path_px"]          # order and values, not just a set
        expect = sum(math.dist(a, b) for a, b in zip(c["path_px"], c["path_px"][1:]))
        assert math.isclose(f["properties"]["path_length_px"], expect, rel_tol=0, abs_tol=1e-9)
        assert "path_px" not in f["properties"] and "endpoints_px" not in f["properties"]


def test_geojson_prefers_path_over_conflicting_chord_and_accepts_legacy_dicts():
    # A5: conflicting chord/path -> the path is delivered. Endpoint-only legacy dicts still export.
    c = dict(id=1, endpoints_px=[[0.0, 0.0], [9.0, 9.0]], path_px=[[0.0, 5.0], [4.0, 5.0], [9.0, 5.0]], length_px=9.0)
    assert to_geojson([c])["features"][0]["geometry"]["coordinates"] == c["path_px"]
    legacy = dict(id=2, endpoints_px=[[0.0, 0.0], [9.0, 9.0]])
    assert to_geojson([legacy])["features"][0]["geometry"]["coordinates"] == legacy["endpoints_px"]
    assert to_geojson([]) == {"type": "FeatureCollection", "features": []}

