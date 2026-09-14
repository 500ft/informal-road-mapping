"""Synthetic scene-count admission checks, not satellite or road evidence."""
from copy import deepcopy
import csv
import json
import os
from pathlib import Path
import subprocess
import sys
import pytest
from test_phase1_gate import fixture as counts_fixture, evaluate   # fixture() already carries 3 scenes per year

YEARS = (2018, 2019, 2020, 2021, 2023, 2024, 2025, 2026)


@pytest.mark.parametrize("value", [-1, 0.5, True, "nan", "inf", ""])
def test_invalid_scene_count_cannot_pass(value):
    manifest, rows = counts_fixture()
    rows[0]["s2_scene_count_2018"] = value
    assert evaluate(manifest, rows)["status"] == "INCONCLUSIVE"


def test_missing_qa_cannot_pass():
    manifest, rows = counts_fixture()
    del rows[0]["s2_scene_count_2026"]
    assert evaluate(manifest, rows)["status"] == "INCONCLUSIVE"


def test_no_early_scenes_cannot_support_baseline():
    manifest, rows = counts_fixture()
    for year in YEARS[:4]:
        rows[0][f"s2_scene_count_{year}"] = 0
    assert evaluate(manifest, rows)["status"] == "INCONCLUSIVE"


def test_one_recent_year_cannot_meet_two_year_requirement():
    manifest, rows = counts_fixture()
    for year in (2023, 2024, 2025):
        rows[0][f"s2_scene_count_{year}"] = 0
    assert evaluate(manifest, rows)["status"] == "INCONCLUSIVE"


def test_missing_2018_is_retained_not_silently_replaced():
    manifest, rows = counts_fixture()
    original = deepcopy(rows)
    rows[0]["s2_scene_count_2018"] = 0
    rows[0]["s2_scene_count_2023"] = 0
    rows[0]["s2_scene_count_2024"] = 0
    result = evaluate(manifest, rows)
    assert result["status"] == "SCREEN_PASS"
    assert result["temporal_qa"][rows[0]["site_id"]]["missing_scene_years"] == [2018, 2023, 2024]
    assert result["temporal_qa"][rows[0]["site_id"]]["scene_counts"]["2026"] == 3
    assert rows[1:] == original[1:]


def test_scene_presence_does_not_override_pixel_coverage():
    manifest, rows = counts_fixture()
    rows[0]["coverage_fraction"] = 0.89
    assert evaluate(manifest, rows)["status"] == "INCONCLUSIVE"


@pytest.mark.parametrize("missing,expected", [(False, 3), (True, 2)])
def test_cli_scene_qa_delivery(tmp_path, missing, expected):
    manifest, rows = counts_fixture()
    if missing:
        for row in rows:
            del row["s2_scene_count_2018"]
    sites, metrics = tmp_path / "sites.json", tmp_path / "metrics.csv"
    sites.write_text(json.dumps(manifest))
    with metrics.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    env = dict(os.environ, PYTHONPATH=str(Path(__file__).resolve().parents[1]))
    run = subprocess.run([sys.executable, "-m", "catanroads.phase1_gate",
        "--sites", str(sites), "--metrics", str(metrics), "--evidence-kind", "synthetic"],
        cwd=tmp_path, env=env, capture_output=True, text=True)
    assert run.returncode == expected, run.stderr
    output = json.loads(run.stdout)
    assert len(output["input_sha256"]) == 2
    if not missing:
        assert len(output["temporal_qa"]) == 4
