"""CR-09 routing contract (docs/PLAN_2026-09-14_CR09.md, A1 and A4): hand-built masks whose
geometry is known before the router runs, plus the legacy-field invariant against the pre-CR-09
baseline snapshot. Nothing here scores road accuracy.

Two kinds of check live here and must not be confused (guidance 2026-09-21, section 1):
  * INDEPENDENT CORRECTNESS -- the fixtures below are hand-constructed and, where the route through
    them is uniquely determined, the expected coordinate list is written out by hand before the
    router runs. These can falsify the implementation.
  * REGRESSION COMPATIBILITY -- `test_a1_*` compares against
    evidence/task-2026-09-14/baseline_candidates.json, which was produced by the PRE-CR-09
    EXTRACTOR ITSELF. It proves the legacy fields did not move; it is NOT an independent oracle and
    cannot show that those fields were ever right.
"""
import json, math
from pathlib import Path
import numpy as np
import pytest
from catanroads import extract_candidates
from catanroads import stress_cases as SC
from catanroads.extract import _component_path_px

ROOT = Path(__file__).resolve().parents[2]
BASELINE = json.loads((ROOT / "evidence/task-2026-09-14/baseline_candidates.json").read_text())
LEGACY = ("id", "centroid_px", "endpoints_px", "length_px", "width_px", "orientation_deg", "elongation", "mean_disturbance", "n_pixels")


def straight(h=3, w=40):
    return np.ones((h, w), bool)

def wide_strip():
    return np.ones((13, 60), bool)

def diagonal_only(n=20):
    return np.eye(n, dtype=bool)

def u_turn():
    """Both tips on the same (left) side: two horizontal 1-px arms joined by a vertical 1-px bar."""
    m = np.zeros((9, 30), bool); m[1, :26] = True; m[7, :26] = True; m[1:8, 25] = True
    return m

def border_touching():
    m = np.zeros((6, 30), bool); m[0, :] = True; return m

def non_square():
    m = np.zeros((25, 7), bool); m[:, 3] = True; m[12, :] = True; return m

def ring():
    m = np.zeros((9, 9), bool); m[1, 1:8] = m[7, 1:8] = True; m[1:8, 1] = m[1:8, 7] = True; return m

def branched():
    m = np.zeros((9, 21), bool); m[4, :] = True; m[:, 10] = True; return m

FIXTURES = dict(straight=straight, wide_strip=wide_strip, diagonal_only=diagonal_only, u_turn=u_turn,
                border_touching=border_touching, non_square=non_square, ring=ring, branched=branched)


def _steps(path):
    p = np.asarray(path); return np.abs(np.diff(p, axis=0)).max(axis=1)


@pytest.mark.parametrize("name", list(FIXTURES))
def test_a4_path_is_finite_adjacent_confined_and_repeatable(name):
    m = FIXTURES[name](); path = _component_path_px(m)
    p = np.asarray(path)
    assert p.ndim == 2 and p.shape[1] == 2 and len(p) >= 2 and np.isfinite(p).all(), name
    assert (_steps(path) == 1).all(), (name, "every step is one 8-neighbour move, no repeats")
    assert m[p[:, 1].astype(int), p[:, 0].astype(int)].all(), (name, "path leaves the component")
    assert _component_path_px(m) == path, (name, "not deterministic")


@pytest.mark.parametrize("name,expected", [
    # Independently specified: on a 3x40 strip the medial row is row 1, so the route is that row,
    # left to right. On a 20x20 identity the only 8-connected chain is the main diagonal.
    ("straight", [[float(x), 1.0] for x in range(40)]),
    ("diagonal_only", [[float(i), float(i)] for i in range(20)]),
])
def test_a4_hand_derived_expected_coordinates(name, expected):
    assert _component_path_px(FIXTURES[name]()) == expected


def test_a4_coordinates_are_x_y_not_row_col():
    # The non-square fixture is 25 rows x 7 columns: a transposed return would put a value >= 7 in
    # the x slot. A square fixture cannot catch this.
    m = non_square(); p = np.asarray(_component_path_px(m))
    assert p[:, 0].max() < m.shape[1] and p[:, 1].max() < m.shape[0], p.max(axis=0).tolist()
    assert m[p[:, 1].astype(int), p[:, 0].astype(int)].all()


def test_a4_length_equals_segment_sum_via_extract():
    d, _, _ = SC.case_wide_corridor(); c = extract_candidates(d)[0]
    p = np.asarray(c["path_px"])
    assert math.isclose(c["path_length_px"], float(np.hypot(*np.diff(p, axis=0).T).sum()))


def test_a4_u_turn_stays_on_its_corridor_and_reaches_both_tips():
    m = u_turn(); path = _component_path_px(m); p = np.asarray(path)
    tips = {(0.0, 1.0), (0.0, 7.0)}
    assert {tuple(p[0]), tuple(p[-1])} == tips, "both tips are on the same side; the route must reach both"
    assert m[p[:, 1].astype(int), p[:, 0].astype(int)].all()


def test_a4_wide_strip_endpoints_are_centred_after_amendment_a():
    # Before amendment A the geometric two-sweep picked the corners (0,0)-(59,12) and A3 failed on
    # wide_corridor (0.9688). The amended rule takes, within one half-width of each end, the pixel
    # closest to the major axis: the route now starts and ends on the centre row.
    m = wide_strip(); p = np.asarray(_component_path_px(m))
    assert p[0].tolist() == [0.0, 6.0] and p[-1].tolist() == [59.0, 6.0], p[[0, -1]].tolist()
    assert (p[:, 1] == 6.0).all(), "the whole route is on the medial row"


def test_a4_ring_and_branch_give_one_connected_path_not_topology():
    for name in ("ring", "branched"):
        p = np.asarray(_component_path_px(FIXTURES[name]()))
        assert (_steps(p) == 1).all() and len(p) >= 2, name


@pytest.mark.parametrize("bad", ["empty", "disconnected"])
def test_a4_contract_violations_raise(bad):
    m = np.zeros((5, 5), bool)
    if bad == "disconnected":
        m[0, 0] = m[4, 4] = True
    with pytest.raises(ValueError):
        _component_path_px(m)


def _legacy_equal(live, base, name):
    assert len(live) == len(base), name
    for lv, bs in zip(live, base):
        for k in LEGACY:
            if isinstance(bs[k], (int, str)):
                assert lv[k] == bs[k], (name, k)
            else:
                assert np.allclose(np.asarray(lv[k], float), np.asarray(bs[k], float), rtol=0, atol=1e-6), (name, k)


def test_a1_legacy_fields_ids_order_and_counts_match_the_pre_cr09_baseline():
    for name, fn in SC.CASES.items():
        d, _, _ = fn(); _legacy_equal(extract_candidates(d), BASELINE["cases"][name], name)
    for st, base in BASELINE["faint_strength_sweep"].items():
        d, _, _ = SC.case_faint_corridor(strength=float(st)); _legacy_equal(extract_candidates(d), base, ("sweep", st))
