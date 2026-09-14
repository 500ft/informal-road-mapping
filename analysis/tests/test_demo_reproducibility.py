"""Gate the synthetic method demo on numbers rather than on image pixels.

results/method_demo_synthetic.png cannot be diffed usefully across machines: font
rasterisation differs between freetype builds, so the title and footer text bands change
by hundreds of pixels while every data pixel is identical. Comparing PNG bytes therefore
reports drift that does not exist, and would hide real drift in the noise.

So the demo's *numeric* output is pinned instead: the scene fingerprint and the extracted
candidate geometry, recorded in results/method_demo_synthetic.numeric.json. If the
extractor or the synthetic scene ever changes, this fails with the offending number.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pytest

from catanroads import extract_candidates, make_scene

RECORD = Path(__file__).resolve().parents[2] / "results" / "method_demo_synthetic.numeric.json"

# Endpoint coordinates come out of a least-squares fit, so they are compared with a
# tolerance rather than exactly. It is tight enough that any change to the extractor or
# the scene shows up, and loose enough to survive BLAS-level reassociation.
ENDPOINT_ATOL_PX = 1e-6


@pytest.fixture(scope="module")
def record():
    if not RECORD.exists():
        pytest.skip(f"numeric record not committed: {RECORD}")
    return json.loads(RECORD.read_text())


@pytest.fixture(scope="module")
def demo():
    scene, _truth = make_scene(size=256, seed=1)
    return scene, extract_candidates(scene)


def test_scene_fingerprint_matches(record, demo):
    scene, _ = demo
    expected = record["scene"]
    assert list(scene.shape) == expected["shape"]
    got = hashlib.sha256(np.ascontiguousarray(scene, dtype=np.float64)).hexdigest()
    assert got == expected["sha256_float64"], (
        "the synthetic scene changed: make_scene(size=256, seed=1) no longer reproduces the "
        f"committed fingerprint (got {got[:16]}..., expected "
        f"{expected['sha256_float64'][:16]}...). numpy's Generator stream is version-stable, "
        "so this means the scene code or its parameters changed."
    )


def test_candidate_count_matches(record, demo):
    _, cands = demo
    assert len(cands) == record["candidates"]["n"], (
        f"the extractor now returns {len(cands)} candidates, not "
        f"{record['candidates']['n']}"
    )


def test_candidate_geometry_matches(record, demo):
    _, cands = demo
    got = np.asarray([[list(p) for p in c["endpoints_px"]] for c in cands], dtype=float)
    expected = np.asarray(record["candidates"]["endpoints_px"], dtype=float)
    assert got.shape == expected.shape
    worst = float(np.max(np.abs(got - expected)))
    assert worst <= ENDPOINT_ATOL_PX, (
        f"candidate endpoints moved by up to {worst:.3e} px, above the "
        f"{ENDPOINT_ATOL_PX:.0e} px tolerance"
    )


def test_candidate_lengths_match(record, demo):
    _, cands = demo
    got = np.asarray([c["length_px"] for c in cands], dtype=float)
    expected = np.asarray(record["candidates"]["length_px"], dtype=float)
    worst = float(np.max(np.abs(got - expected)))
    assert worst <= ENDPOINT_ATOL_PX, (
        f"candidate lengths moved by up to {worst:.3e} px, above the "
        f"{ENDPOINT_ATOL_PX:.0e} px tolerance"
    )
