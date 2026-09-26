"""The canonical register in docs/PARAMETER_PROVENANCE.md must not drift from the source.

A register that silently disagrees with the code is worse than no register: it invites a reader to
trust a number that is no longer true. These tests read the values out of the source files and
assert the document states them. They check nothing about whether a value is *correct* — that is
the audit's open-questions section, not something a test can settle.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = (ROOT / "docs/PARAMETER_PROVENANCE.md").read_text()
GEE = (ROOT / "gee/ndvi_change.js").read_text()
EXTRACT = (ROOT / "analysis/catanroads/extract.py").read_text()


def gee_constants():
    return {k: v.strip() for k, v in re.findall(r"^var ([A-Z_]+) = ([0-9./ ]+);", GEE, re.M)}


# Quantities are also named in the headline-findings table above; only the canonical register
# carries authoritative values, so searching the whole document would match the wrong row.
REGISTER = DOC.split("## Canonical register", 1)[1].split("## Audit table", 1)[0]


def _row(name):
    """The value column of the canonical-register row for a backticked quantity, or None."""
    m = re.search(rf"^\| `{re.escape(name)}` \| ([^|]+) \|", REGISTER, re.M)
    return m.group(1).strip() if m else None


def test_every_numeric_gee_constant_appears_in_the_register():
    missing = [k for k in gee_constants() if f"`{k}`" not in DOC]
    assert not missing, f"constants absent from the register: {missing}"


def test_register_values_match_the_earth_engine_source():
    expected = {
        "MONTH": "7", "ANALYSIS_SCALE_M": "10", "CONTROL_INNER_M": "200", "CONTROL_OUTER_M": "800",
        "MIN_CONTROL_PIXELS": "500", "Z_MIN": "1.0", "YEARLY_EFFECT_MIN": "0.02",
        "MIN_VALID_RECENT_YEARS": "2", "MIN_COMPONENT_PIXELS": "50", "MAX_CONNECTED_PIXELS": "256",
        "GATE_RATIO_MIN": "2.0", "GATE_ABSOLUTE_FLOOR": "0.0001",
        "GATE_MIN_DEVELOPMENT_SITES": "2", "GATE_MIN_COVERAGE": "0.90",
    }
    src = gee_constants()
    for name, value in expected.items():
        assert src[name] == value, f"{name}: source says {src[name]}, register expects {value}"
        assert _row(name) == value, f"{name}: register row says {_row(name)}, source says {value}"
    # PERSISTENCE_MIN is written as an expression in source and as a fraction in the register.
    assert src["PERSISTENCE_MIN"] == "2 / 3"
    assert _row("PERSISTENCE_MIN") == "2/3"


def test_register_values_match_the_extractor_defaults():
    for name, value in (("disturb_thresh", "1.0"), ("ridge_quantile", "0.85"),
                        ("min_length_px", "12"), ("min_elongation", "3.0")):
        src = re.search(rf"{name}: float = ([0-9.]+)", EXTRACT).group(1)
        assert src.rstrip("0").rstrip(".") == value.rstrip("0").rstrip("."), (name, src, value)
        assert _row(name) == value, f"{name}: register says {_row(name)}, source says {src}"
    assert re.search(r"ridge_sigmas=\(1\.0, 2\.0, 3\.0\)", EXTRACT)
    assert _row("ridge_sigmas") == "(1, 2, 3)"


def test_site_half_km_matches_the_manifest():
    manifest = json.loads((ROOT / "config/sites.geojson").read_text())
    half_km = {f["properties"]["half_km"] for f in manifest["features"]}
    assert half_km == {8}, half_km
    assert "| `half_km` (all six sites) | 8 |" in DOC


def test_no_quantity_is_claimed_as_really_measured():
    # The register's own rule: nothing here has been observed from a real run.
    assert re.search(r"REAL_MEASURED`\s+status\*\*, because no real run has occurred", DOC)
    rows = re.findall(r"^\| `[^`]+` \|[^\n]*REAL_MEASURED[^\n]*$", REGISTER, re.M)
    assert rows == [], f"a quantity claims REAL_MEASURED status: {rows}"


def test_every_site_is_still_unverified():
    manifest = json.loads((ROOT / "config/sites.geojson").read_text())
    assert all(f["properties"]["verified"] is False for f in manifest["features"])
