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
