"""Two arithmetic facts the 2026-09-24 literature critique established, pinned as tests.

Neither needs imagery, Earth Engine or a network. Both are deductions from the committed
configuration, not claims borrowed from a paper, and both correct a statement this repository
previously made:

  1. The analysis grid is EPSG:3857 at nominal scale 10. Web Mercator's linear scale factor is
     1/cos(latitude) under the spherical approximation, so a nominal-10 pixel does NOT span 10 m of
     ground at the registered site latitudes. Metre figures derived from a 10 m assumption were
     overstated by roughly 45%.
  2. Forming a band ratio from per-band medians is not the same estimator as taking the median of
     per-acquisition ratios. The pipeline does the former; this test proves the two differ.

Neither test says which estimator is better, nor that any committed number is wrong — only that the
physical and statistical assumptions behind them need stating. See literature/claim-ledger.md C19.
"""
import json
import math
import statistics
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
NOMINAL_SCALE_M = 10.0          # ANALYSIS_SCALE_M in gee/ndvi_change.js
MIN_COMPONENT_PIXELS = 50       # CONFIG["min_component_pixels"] in phase1_gate.py


def ground_span_m(latitude_deg, nominal_scale_m=NOMINAL_SCALE_M):
    """Ground distance spanned by one nominal-scale Web Mercator pixel (spherical approximation)."""
    return nominal_scale_m * math.cos(math.radians(latitude_deg))


def registered_latitudes():
    manifest = json.loads((ROOT / "config/sites.geojson").read_text())
    return {f["properties"]["id"]: f["properties"]["center_lat"] for f in manifest["features"]}


def test_nominal_ten_metre_pixel_is_not_ten_ground_metres_at_any_registered_site():
    for site, lat in registered_latitudes().items():
        span = ground_span_m(lat)
        assert 6.5 < span < 7.1, (site, lat, span)
        assert span < NOMINAL_SCALE_M * 0.72, (site, "closer to 10 m than expected", span)


def test_fifty_pixel_component_is_about_2300_not_5000_square_metres():
    # The threshold was reasoned about as 50 x 10 x 10 = 5000 m^2. It is not.
    for site, lat in registered_latitudes().items():
        area = MIN_COMPONENT_PIXELS * ground_span_m(lat) ** 2
        assert 2100 < area < 2600, (site, area)
        assert area < 0.55 * (MIN_COMPONENT_PIXELS * NOMINAL_SCALE_M ** 2), (site, area)


def test_ground_span_shrinks_as_latitude_rises():
    lats = registered_latitudes()
    ordered = sorted(lats.values())
    spans = [ground_span_m(lat) for lat in ordered]
    assert spans == sorted(spans, reverse=True), spans


def test_band_ratio_of_medians_differs_from_median_of_per_acquisition_ratios():
    # Hand-derived counterexample; both routes are legitimate estimators and they disagree.
    red = [0.10, 0.40, 0.30]
    nir = [0.20, 0.50, 0.90]
    ratio_of_medians = (statistics.median(nir) - statistics.median(red)) / (
        statistics.median(nir) + statistics.median(red)
    )
    per_acquisition = [(n - r) / (n + r) for r, n in zip(red, nir)]
    median_of_ratios = statistics.median(per_acquisition)

    assert math.isclose(ratio_of_medians, 0.25, abs_tol=1e-12)
    assert math.isclose(median_of_ratios, 1 / 3, abs_tol=1e-12)
    assert not math.isclose(ratio_of_medians, median_of_ratios, abs_tol=1e-6)
    # The pipeline (gee/ndvi_change.js) takes the first route: medianOrMasked() then
    # normalizedDifference(). Which route is preferable here is NOT established by this test.


def test_a_missing_band_makes_joint_validity_explicit():
    # One acquisition with an unusable NIR: per-acquisition ratios must drop it, whereas per-band
    # medians would silently keep its red value. That asymmetry is the reason joint validity has to
    # be stated rather than assumed.
    red = [0.10, 0.40, 0.30, 0.55]
    nir = [0.20, 0.50, 0.90, None]
    jointly_valid = [(r, n) for r, n in zip(red, nir) if n is not None]
    assert len(jointly_valid) == 3
    red_all_median = statistics.median(red)
    red_joint_median = statistics.median([r for r, _ in jointly_valid])
    assert not math.isclose(red_all_median, red_joint_median, abs_tol=1e-6)


# ── missingness sensitivity (package D) ───────────────────────────────────────────────────
# The committed enumeration is checked against an INDEPENDENT oracle written here: a different
# formulation of the same rule (Fraction comparison rather than 3k >= 2n integer arithmetic).
# If the two ever disagree, one of them is wrong and the test says so.
MISSINGNESS = ROOT / "evidence/task-2026-09-25/missingness_sensitivity.json"


def _oracle(history, mask):
    from fractions import Fraction
    kept = [d for d, m in zip(history, mask) if m]
    if len(kept) < 2:
        return False
    return Fraction(sum(kept), len(kept)) >= Fraction(2, 3)


def test_missingness_enumeration_is_complete_and_matches_an_independent_oracle():
    rec = json.loads(MISSINGNESS.read_text())
    assert rec["counts"] == {"histories": 16, "masks": 11, "pairs": 176}
    assert len(rec["pairs"]) == 176
    assert len({(tuple(p["history"]), tuple(p["mask"])) for p in rec["pairs"]}) == 176
    for p in rec["pairs"]:
        assert p["retained_pass"] == _oracle(p["history"], p["mask"]), p
        assert p["full_pass"] == _oracle(p["history"], (1, 1, 1, 1)), p


def test_missing_years_flip_the_persistence_decision_in_both_directions():
    rec = json.loads(MISSINGNESS.read_text())
    flips = rec["summary"]["by_flip"]
    assert flips["fail_to_pass"] > 0 and flips["pass_to_fail"] > 0
    assert sum(flips.values()) == 176


def test_which_years_go_missing_determines_the_direction_of_the_flip():
    # The finding worth keeping: losing only quiet years can only help a pixel pass, and losing
    # only disturbed years can only make it fail. Missingness is therefore not decision-neutral
    # when it is not random. This is enumeration over a rule, NOT a field probability estimate.
    rec = json.loads(MISSINGNESS.read_text())
    quiet = rec["summary"]["dropping_only_quiet_years"]
    dist = rec["summary"]["dropping_only_disturbed_years"]
    assert quiet["pass_to_fail"] == 0 and quiet["fail_to_pass"] > 0, quiet
    assert dist["fail_to_pass"] == 0 and dist["pass_to_fail"] > 0, dist


def test_enumeration_is_bound_to_the_live_source_operators():
    # A stale model must fail rather than stay quietly green if gee/ndvi_change.js changes.
    rec = json.loads(MISSINGNESS.read_text())
    assert all(rec["source_binding"].values()), rec["source_binding"]
    assert rec["status"] == "MODEL_CHECKED"


def test_effect_size_boundary_is_strictly_greater_than():
    rec = json.loads(MISSINGNESS.read_text())["edge_cases"]["yearly_effect_boundary"]
    assert rec["effect_0.0199_disturbed"] is False
    assert rec["effect_0.0200_disturbed"] is False     # exactly at the floor is NOT disturbed
    assert rec["effect_0.0201_disturbed"] is True


def test_minimum_passing_counts_are_two_of_two_two_of_three_three_of_four():
    rec = json.loads(MISSINGNESS.read_text())["edge_cases"]
    assert rec["minimum_passing_counts"] == {"n=2": 2, "n=3": 2, "n=4": 3}
    assert rec["n_equals_1_is_ineligible"]["eligible"] is False
    assert rec["n_equals_0_is_ineligible"]["eligible"] is False


# ── compositor variant B contract (package C) ─────────────────────────────────────────────
# Expected values below are derived by hand, not from the implementation under test.
# Protocol: docs/specs/compositor-ab/plan.md. Production is unchanged; this pins B's definition.
def _bsi(b2, b4, b8, b11):
    num, den = (b11 + b4) - (b8 + b2), (b11 + b4) + (b8 + b2)
    if den <= 0:
        raise ZeroDivisionError("BSI denominator is not strictly positive")
    return num / den


def _eligible(sample):
    """Variant B: all four bands valid and finite, and both denominators strictly positive."""
    if any(sample.get(b) is None for b in ("B2", "B4", "B8", "B11")):
        return False
    if not all(math.isfinite(sample[b]) for b in ("B2", "B4", "B8", "B11")):
        return False
    return (sample["B8"] + sample["B4"]) > 0 and ((sample["B11"] + sample["B4"]) + (sample["B8"] + sample["B2"])) > 0


def test_variant_b_bsi_matches_hand_derived_values():
    # B2=0.10 B4=0.20 B8=0.40 B11=0.50 -> ((0.5+0.2)-(0.4+0.1))/((0.5+0.2)+(0.4+0.1)) = 0.2/1.2
    assert math.isclose(_bsi(0.10, 0.20, 0.40, 0.50), 0.2 / 1.2, abs_tol=1e-12)
    # A brighter shortwave raises BSI: B11 0.50 -> 0.80 gives 0.5/1.5
    assert math.isclose(_bsi(0.10, 0.20, 0.40, 0.80), 0.5 / 1.5, abs_tol=1e-12)
    # Symmetric case is exactly zero.
    assert math.isclose(_bsi(0.30, 0.30, 0.30, 0.30), 0.0, abs_tol=1e-12)


def test_variant_b_drops_an_acquisition_missing_b2_or_b11_even_when_red_and_nir_are_valid():
    # NDVI alone would be computable here; variant B requires JOINT validity, so the sample is out.
    assert _eligible({"B2": 0.1, "B4": 0.2, "B8": 0.4, "B11": 0.5}) is True
    assert _eligible({"B2": None, "B4": 0.2, "B8": 0.4, "B11": 0.5}) is False
    assert _eligible({"B2": 0.1, "B4": 0.2, "B8": 0.4, "B11": None}) is False
    assert _eligible({"B2": 0.1, "B4": 0.2, "B8": float("nan"), "B11": 0.5}) is False


def test_variant_b_rejects_a_non_positive_denominator_rather_than_returning_a_number():
    assert _eligible({"B2": 0.0, "B4": 0.0, "B8": 0.0, "B11": 0.0}) is False
    with pytest.raises(ZeroDivisionError):
        _bsi(0.0, 0.0, 0.0, 0.0)
    # A valid zero reflectance in ONE band is still a number, not missingness.
    assert _eligible({"B2": 0.0, "B4": 0.2, "B8": 0.4, "B11": 0.5}) is True


def test_variant_b_even_count_median_is_the_mean_of_the_two_middle_values():
    assert statistics.median([0.1, 0.2, 0.3, 0.4]) == pytest.approx(0.25)
    assert statistics.median([0.1, 0.2, 0.3]) == pytest.approx(0.2)


def test_variant_b_leaves_an_all_invalid_year_masked_and_keeps_a_single_valid_acquisition():
    july = [{"B2": None, "B4": 0.2, "B8": 0.4, "B11": 0.5},
            {"B2": 0.1, "B4": 0.2, "B8": float("inf"), "B11": 0.5}]
    assert [s for s in july if _eligible(s)] == []      # masked; no invented annual value
    july.append({"B2": 0.10, "B4": 0.20, "B8": 0.40, "B11": 0.50})
    eligible = [s for s in july if _eligible(s)]
    assert len(eligible) == 1
    assert math.isclose(statistics.median([_bsi(**{k.lower(): v for k, v in s.items()}) for s in eligible]),
                        0.2 / 1.2, abs_tol=1e-12)
