"""Pin the extractor's OBSERVED behaviour on the fixed stress cases (CR-R03).

These are not aspirations. Each assertion states what extract_candidates does today on a
deterministic construction, including the misses and the false candidate, so that a change to
the extractor shows up here as a named behaviour change rather than a silent shift in a demo
figure. results/extractor_stress_cases.json is the committed record the CLI regenerates.
"""
import json, math
from pathlib import Path
import numpy as np
import pytest
from catanroads import extract_candidates
from catanroads import stress_cases as SC

ROOT = Path(__file__).resolve().parents[2]
RECORD = json.loads((ROOT / "results/extractor_stress_cases.json").read_text())


@pytest.fixture(scope="module")
def live():
    return SC.run_all()


def test_committed_record_matches_live_run(live):
    for name, s in live.items():
        rec = RECORD["cases"][name]
        assert s["n_candidates"] == rec["n_candidates"], name
        assert s["n_false_candidates"] == rec["n_false_candidates"], name
        for k in ("pixel_recall", "pixel_precision", "line_recall", "line_precision"):
            if rec[k] is None:
                assert s[k] is None, (name, k)
            else:
                assert math.isclose(s[k], rec[k], abs_tol=1e-9), (name, k)


# ── where it detects ────────────────────────────────────────────────────────────────────
def test_detects_wide_low_snr_gradient_and_hairpin_corridors(live):
    for name in ("wide_corridor", "low_snr", "gradient_background", "tight_curve"):
        assert live[name]["detected"] and live[name]["pixel_recall"] >= 0.99, name


def test_faint_corridor_is_detected_but_fragmented(live):
    s = live["faint_corridor"]
    assert s["detected"] and s["pixel_recall"] > 0.9
    assert s["n_candidates"] == 7, "one corridor reported as seven pieces"


def test_speckle_alone_produces_no_candidates():
    for n in (400, 1500, 4000):
        d, _ = SC.case_speckle_only(n_specks=n)
        assert extract_candidates(d) == [], n


# ── where it misses ─────────────────────────────────────────────────────────────────────
def test_crossing_corridors_are_both_lost(live):
    # Two full corridors, zero candidates: the union component's elongation is below min_elongation.
    assert live["crossing"]["n_candidates"] == 0 and live["crossing"]["pixel_recall"] == 0.0
    d, _ = SC.case_crossing()
    assert len(extract_candidates(d, min_elongation=1.5)) == 1, "lowering min_elongation recovers ONE component for two roads"


def test_dashed_corridor_is_lost_entirely(live):
    assert live["short_segments"]["n_candidates"] == 0


def test_detection_cliff_sits_at_disturb_thresh():
    sweep = {r["strength"]: r for r in SC.faint_strength_sweep()}
    assert sweep[1.3]["pixel_recall"] == 1.0
    assert sweep[1.05]["pixel_recall"] < 0.5
    assert sweep[0.9]["n_candidates"] == 0


# ── where it fabricates ─────────────────────────────────────────────────────────────────
def test_linear_non_road_feature_is_a_confident_false_candidate(live):
    s = live["linear_confound_riverbank"]
    assert s["n_candidates"] == 1 and s["n_false_candidates"] == 1 and s["pixel_precision"] == 0.0
    d, _ = SC.case_linear_confound_riverbank()
    c = extract_candidates(d)[0]
    assert c["length_px"] > 250 and c["mean_disturbance"] > 2, "ranked like a strong road"


def test_gradient_background_adds_small_false_candidates(live):
    s = live["gradient_background"]
    assert s["n_false_candidates"] == 2 and s["pixel_precision"] > 0.95


# ── where it misrepresents ──────────────────────────────────────────────────────────────
def test_hairpin_is_summarised_as_one_straight_segment():
    d, _ = SC.case_tight_curve(); c = extract_candidates(d)[0]
    (x0, y0), (x1, y1) = c["endpoints_px"]
    assert abs(y0 - y1) < 1.0, "endpoints lie on one horizontal line; the doubling-back is invisible"
    assert c["width_px"] > 20, "the hairpin's height is reported as candidate WIDTH"


def test_width_px_is_curve_extent_not_road_width_regardless_of_noise():
    # Review 2026-09-12: the first record blamed noise for a 53 px width. It is the curved
    # component's transverse extent: ~55 px at ZERO noise for a 3-px-thick corridor.
    w0 = extract_candidates(SC.case_low_snr(noise=0.0)[0])[0]["width_px"]
    w9 = extract_candidates(SC.case_low_snr(noise=0.9)[0])[0]["width_px"]
    assert 50 < w0 < 62 and abs(w0 - w9) < 5, (w0, w9)
    assert SC.curve_extent_without_noise()["true_road_thickness_px"] == 3


# ── exported-line layer (review 2026-09-12: component scores ignored the delivered geometry) ──
def test_wrong_endpoints_score_worse_on_the_line_layer_negative_control():
    d, t = SC.case_wide_corridor(); c = extract_candidates(d)
    good = SC.score_lines(t, c)
    for cc in c: cc["endpoints_px"] = [[0.0, 0.0], [255.0, 255.0]]
    bad = SC.score_lines(t, c)
    assert good["line_recall"] > 5 * bad["line_recall"], (good, bad)
    assert good["line_precision"] > 0.95 and bad["line_precision"] < 0.1


def test_component_layer_is_blind_to_endpoints_and_the_record_says_so(live):
    d, t = SC.case_low_snr(); c = extract_candidates(d)
    s0 = SC.score(d, t, c)
    for cc in c: cc["endpoints_px"] = [[0.0, 0.0], [255.0, 255.0]]
    s1 = SC.score(d, t, c)
    assert (s0["pixel_recall"], s0["pixel_precision"]) == (s1["pixel_recall"], s1["pixel_precision"])   # blind, by construction
    assert s1["line_recall"] < s0["line_recall"]                                                           # the line layer is not


def test_curved_corridors_pass_the_component_layer_and_fail_the_line_layer(live):
    for name in ("low_snr", "tight_curve", "demo_reference"):
        assert live[name]["detected"] and not live[name]["line_ok"], name
    assert live["low_snr"]["line_recall"] < 0.2 and live["tight_curve"]["line_recall"] < 0.35


def test_straight_corridors_pass_both_layers(live):
    for name in ("faint_corridor", "gradient_background"):
        assert live[name]["line_ok"], name


def test_baseline_record_is_preserved_unchanged():
    base = json.loads((ROOT / "results/extractor_stress_cases_baseline_2026-09-12.json").read_text())
    assert base["schema_version"] == 1
    for name, s in RECORD["cases"].items():
        for k in ("n_candidates", "n_false_candidates", "pixel_recall", "pixel_precision"):
            assert base["cases"][name][k] == s[k], (name, k)



def test_cli_reproduces_the_committed_record_exactly():
    import subprocess, sys
    out = subprocess.run([sys.executable, "-m", "catanroads.stress_cases"], cwd=ROOT / "analysis", capture_output=True, text=True)
    assert out.returncode == 0, out.stderr[-400:]
    live = json.loads(out.stdout)
    for k in ("cases", "faint_strength_sweep", "curve_extent_without_noise"):
        assert live[k] == RECORD[k], k
