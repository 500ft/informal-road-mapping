"""Pin the extractor's OBSERVED behaviour on the fixed stress cases (CR-R03).

These are not aspirations. Each assertion states what extract_candidates does today on a
deterministic construction, including the misses and the false candidate, so that a change to
the extractor shows up here as a named behaviour change rather than a silent shift in a demo
figure. results/extractor_stress_cases.json is the committed record the CLI regenerates.
"""
import hashlib, json, math, subprocess, sys
from pathlib import Path
import numpy as np
import pytest
from catanroads import extract_candidates, to_geojson
from catanroads import stress_cases as SC

ROOT = Path(__file__).resolve().parents[2]
RECORD = json.loads((ROOT / "results/extractor_stress_cases.json").read_text())
V3 = json.loads((ROOT / SC.V3_ARCHIVE).read_text())
V3_SHA256 = "f906d96b371039db2bea59fe0e971e41bd7e41520e5a61d69b7ac8230d51285f"
V1_SHA256 = "5baa8ff3e69fd829988b85800e60faee9bcdecc836a34d05019b7e8765bb300c"


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
        d, _, _ = SC.case_speckle_only(n_specks=n)
        assert extract_candidates(d) == [], n


# ── where it misses ─────────────────────────────────────────────────────────────────────
def test_crossing_corridors_are_both_lost(live):
    # Two full corridors, zero candidates: the union component's elongation is below min_elongation.
    assert live["crossing"]["n_candidates"] == 0 and live["crossing"]["pixel_recall"] == 0.0
    d, _, _ = SC.case_crossing()
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
    d, _, _ = SC.case_linear_confound_riverbank()
    c = extract_candidates(d)[0]
    assert c["length_px"] > 250 and c["mean_disturbance"] > 2, "ranked like a strong road"


def test_gradient_background_adds_small_false_candidates(live):
    s = live["gradient_background"]
    assert s["n_false_candidates"] == 2 and s["pixel_precision"] > 0.95


# ── where it misrepresents ──────────────────────────────────────────────────────────────
def test_hairpin_chord_is_flat_and_width_is_extent_but_the_delivered_path_follows_the_bend():
    d, _, _ = SC.case_tight_curve(); c = extract_candidates(d)[0]
    (x0, y0), (x1, y1) = c["endpoints_px"]
    assert abs(y0 - y1) < 1.0, "the legacy chord is still one horizontal line; the doubling-back is invisible to it"
    assert c["width_px"] > 20, "the hairpin's height is still reported as candidate WIDTH (minor-axis extent)"
    ys = [y for _, y in c["path_px"]]
    assert max(ys) - min(ys) > 15 and c["path_length_px"] > c["length_px"], "path_px follows the arc: taller than 15 px and longer than the chord"


def test_width_px_is_curve_extent_not_road_width_regardless_of_noise():
    # Review 2026-09-12: the first record blamed noise for a 53 px width. It is the curved
    # component's transverse extent: ~55 px at ZERO noise for a 3-px-thick corridor.
    w0 = extract_candidates(SC.case_low_snr(noise=0.0)[0])[0]["width_px"]
    w9 = extract_candidates(SC.case_low_snr(noise=0.9)[0])[0]["width_px"]
    assert 50 < w0 < 62 and abs(w0 - w9) < 5, (w0, w9)
    assert SC.curve_extent_without_noise()["true_road_thickness_px"] == 3


# ── exported-line layer (review 2026-09-12: component scores ignored the delivered geometry) ──
def test_a6_corrupting_the_path_degrades_line_scores_and_leaves_component_scores_fixed():
    d, t, cl = SC.case_wide_corridor(); c = extract_candidates(d)
    good = SC.score(d, t, c, centerline=cl)
    for cc in c: cc["path_px"] = [[0.0, 0.0], [255.0, 255.0]]
    bad = SC.score(d, t, c, centerline=cl)
    assert good["line_recall"] > 5 * bad["line_recall"] and good["line_precision"] > 0.95 and bad["line_precision"] < 0.1
    assert (good["pixel_recall"], good["pixel_precision"]) == (bad["pixel_recall"], bad["pixel_precision"])


def test_a6_corrupting_the_chord_with_a_valid_path_leaves_delivered_geometry_fixed():
    d, t, cl = SC.case_wide_corridor(); c = extract_candidates(d)
    before = SC.score_lines(cl, c, truth=t); gj = to_geojson(c)
    for cc in c: cc["endpoints_px"] = [[0.0, 0.0], [255.0, 255.0]]
    assert SC.score_lines(cl, c, truth=t) == before and to_geojson(c) == gj


def test_a5_geojson_and_scorer_deliver_the_same_pixels():
    d, t, cl = SC.case_tight_curve(); c = extract_candidates(d)
    gj = to_geojson(c)                                                            # identity transform
    from_geojson = [dict(path_px=f["geometry"]["coordinates"]) for f in gj["features"]]
    assert (SC.rasterise_segments(from_geojson, t.shape) == SC.rasterise_segments(c, t.shape)).all()


@pytest.mark.parametrize("bad", [None, [], [[0.0, 0.0]], [[0.0, 0.0], [float("nan"), 1.0]], [[0.0, 0.0], [float("inf"), 1.0]],
                                 [[0.0, 0.0], [0.0, 0.0], [1.0, 1.0]], [[0.0], [1.0]], [[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]], "0,0 1,1"])
def test_a7_malformed_present_path_raises_through_every_consumer(bad):
    c = [dict(id=1, endpoints_px=[[0.0, 0.0], [9.0, 9.0]], path_px=bad)]
    with pytest.raises(ValueError):
        to_geojson(c)
    with pytest.raises(ValueError):
        SC.rasterise_segments(c, (16, 16))
    assert to_geojson([]) == {"type": "FeatureCollection", "features": []}
    assert SC.score_lines(np.zeros((16, 16), bool), [])["line_recall"] is None


# ── review 2 (2026-09-12): the line layer penalised road width ──
def test_perfect_centerline_passes_regardless_of_road_width():
    d, t, cl = SC.case_wide_corridor()
    perfect = [dict(id=1, endpoints_px=[[0.0, 128.0], [255.0, 128.0]])]
    s = SC.score_lines(cl, perfect, truth=t)
    assert s["line_recall"] == 1.0 and s["line_precision"] == 1.0 and s["line_ok"]
    assert 0.3 < s["area_coverage"] < 0.45, "area coverage of a 13-px road by a 2-px band is a separate diagnostic, not a penalty"


def test_offset_centerline_is_penalised_by_the_centerline_metric():
    d, t, cl = SC.case_wide_corridor()
    off = [dict(id=1, endpoints_px=[[0.0, 133.0], [255.0, 133.0]])]     # 5 px off-centre, still inside the 13-px road
    s = SC.score_lines(cl, off, truth=t)
    assert s["line_recall"] == 0.0 and not s["line_ok"], s


def test_every_case_carries_a_reference_centerline_inside_its_truth():
    for name, fn in SC.CASES.items():
        d, t, cl = fn()
        assert cl.shape == t.shape and not (cl & ~t).any(), name
        if t.any(): assert cl.any(), name


def test_demo_centerline_reconstruction_matches_the_generator():
    d, t, cl = SC.case_demo_reference()
    assert not (cl & ~t).any() and 800 < cl.sum() < 1000


def test_component_layer_is_blind_to_endpoints_and_the_record_says_so(live):
    d, t, cl = SC.case_low_snr(); c = extract_candidates(d)
    s0 = SC.score(d, t, c, centerline=cl)
    for cc in c: cc["path_px"] = [[0.0, 0.0], [255.0, 255.0]]
    s1 = SC.score(d, t, c, centerline=cl)
    assert (s0["pixel_recall"], s0["pixel_precision"]) == (s1["pixel_recall"], s1["pixel_precision"])   # blind, by construction
    assert s1["line_recall"] < s0["line_recall"]                                                           # the line layer is not


def test_a2_curved_corridors_pass_the_component_layer_and_the_delivered_line_layer(live):
    # Frozen target (plan A2): recall AND precision >= 0.80 on each curved case. The chord they used
    # to deliver is kept as chord_line and still fails, so the old failure stays demonstrable.
    for name in ("low_snr", "tight_curve", "demo_reference"):
        s = live[name]
        assert s["detected"] and s["line_ok"] and s["line_recall"] >= 0.80 and s["line_precision"] >= 0.80, (name, s["line_recall"], s["line_precision"])
        assert not s["chord_line"]["line_ok"] and math.isclose(s["chord_line"]["line_recall"], V3["cases"][name]["line_recall"], abs_tol=1e-9), name


def test_a3_straight_corridors_do_not_regress(live):
    # Frozen target (plan A3): wide >= 0.98 both; faint and gradient >= own v3 value - 0.02, per case.
    s = live["wide_corridor"]; assert s["line_recall"] >= 0.98 and s["line_precision"] >= 0.98, s
    for name in ("faint_corridor", "gradient_background"):
        s, v3 = live[name], V3["cases"][name]
        assert s["line_recall"] >= v3["line_recall"] - 0.02 and s["line_precision"] >= v3["line_precision"] - 0.02, (name, s["line_recall"], s["line_precision"])


def test_a1_component_layer_and_ranking_match_v3(live):
    for name, s in live.items():
        for k in ("n_candidates", "n_false_candidates", "false_candidate_ids", "pixel_recall", "pixel_precision", "top_candidates"):
            assert s[k] == V3["cases"][name][k], (name, k)


def test_straight_wide_corridor_now_passes_the_line_layer(live):
    assert live["wide_corridor"]["line_ok"] and live["wide_corridor"]["line_recall"] == 1.0


def test_straight_corridors_pass_both_layers(live):
    for name in ("faint_corridor", "gradient_background", "wide_corridor"):
        assert live[name]["line_ok"], name


def test_a8_archived_records_are_byte_unchanged_and_component_numbers_agree():
    assert hashlib.sha256((ROOT / SC.V1_ARCHIVE).read_bytes()).hexdigest() == V1_SHA256
    assert hashlib.sha256((ROOT / SC.V3_ARCHIVE).read_bytes()).hexdigest() == V3_SHA256
    base = json.loads((ROOT / SC.V1_ARCHIVE).read_text()); assert base["schema_version"] == 1 and V3["schema_version"] == 3
    for name, s in RECORD["cases"].items():
        for k in ("n_candidates", "n_false_candidates", "pixel_recall", "pixel_precision"):
            assert base["cases"][name][k] == s[k] == V3["cases"][name][k], (name, k)


def test_a8_record_has_complete_v4_metadata():
    assert RECORD["schema_version"] == 4 and RECORD["geometry_field"] == "path_px"
    assert RECORD["supersedes"]["v3"] == SC.V3_ARCHIVE and RECORD["supersedes"]["v1"] == SC.V1_ARCHIVE
    assert RECORD["baseline_revision"] == SC.BASELINE_REVISION and RECORD["tolerance"]["tol_px"] == 2
    assert set(RECORD["environment"]) >= {"python", "numpy", "scipy"} and "produced_by" in RECORD
    assert RECORD["extractor_defaults"] == {"disturb_thresh": 1.0, "ridge_sigmas": [1.0, 2.0, 3.0], "ridge_quantile": 0.85, "min_length_px": 12.0, "min_elongation": 3.0}
    paths = RECORD["cases"]["demo_reference"]["exported_paths_px"]
    assert len(paths) == RECORD["cases"]["demo_reference"]["n_candidates"] and all(len(p["path_px"]) >= 2 for p in paths)


def test_atomic_out_writes_the_same_payload_as_stdout(tmp_path):
    target = tmp_path / "record.json"
    SC.main(["--out", str(target)])
    assert json.loads(target.read_text())["cases"] == RECORD["cases"]
    assert not list(tmp_path.glob("*.tmp"))


def test_a_failed_regeneration_leaves_an_accepted_record_untouched(tmp_path, monkeypatch):
    # F1/F2: the CLI used to be documented as a shell redirect, which truncates the destination when
    # the run fails. --out stages beside the target, validates by parsing back, then os.replace.
    target = tmp_path / "record.json"
    target.write_text('{"accepted": true}')
    monkeypatch.setattr(SC, "record", lambda: {"schema_version": 4, "geometry_field": "path_px"})   # missing metadata
    with pytest.raises(ValueError):
        SC.main(["--out", str(target)])
    assert json.loads(target.read_text()) == {"accepted": True}, "the accepted record was modified"
    assert not list(tmp_path.glob("*.tmp")), "a temporary file was left behind"


def test_a8_cli_reproduces_the_committed_numeric_payload_exactly():
    out = subprocess.run([sys.executable, "-m", "catanroads.stress_cases"], cwd=ROOT / "analysis", capture_output=True, text=True)
    assert out.returncode == 0, out.stderr[-400:]
    live = json.loads(out.stdout)
    for k in ("cases", "faint_strength_sweep", "sensitivity_seeds", "curve_extent_without_noise", "extractor_defaults", "tolerance", "geometry_field", "schema_version", "supersedes", "baseline_revision"):
        assert live[k] == RECORD[k], k
    assert set(live["environment"]) == set(RECORD["environment"])      # reported, not compared
