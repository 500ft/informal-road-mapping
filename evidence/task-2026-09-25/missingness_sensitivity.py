"""Exhaustive enumeration of how missing recent years change the persistence decision.

MODEL_CHECKED, not EARTH_ENGINE_VERIFIED. The real per-pixel persistence calculation lives in
gee/ndvi_change.js and runs on Earth Engine; this is a small arithmetic model of the same decision
rule, plus static assertions binding it to the operators and constants in that source. If the
source changes, the binding assertions fail rather than leaving a stale model quietly green.

Rule, as read from gee/ndvi_change.js:
  disturbed(year)  <- yearlyComp.gt(YEARLY_EFFECT_MIN)        strictly greater than 0.02
  persistence pass <- persist.gte(PERSISTENCE_MIN)            k/n >= 2/3, i.e. 3k >= 2n
  eligibility      <- validCount.gte(MIN_VALID_RECENT_YEARS)  n >= 2
A masked year is absent from both k and n. It is never imputed as a quiet observation.

Run:  PYTHONPATH=analysis python evidence/task-2026-09-25/missingness_sensitivity.py
"""
import itertools
import json
import re
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GEE = ROOT / "gee" / "ndvi_change.js"
YEARS = (2023, 2024, 2025, 2026)


def decide(history, mask):
    """Exact integer decision for one history under one retention mask."""
    retained = [d for d, keep in zip(history, mask) if keep]
    n, k = len(retained), sum(retained)
    if n < 2:
        return {"n": n, "k": k, "eligible": False, "persist": False, "pass": False}
    # 3k >= 2n avoids float comparison entirely; Fraction cross-checks it.
    persist = 3 * k >= 2 * n
    assert persist == (Fraction(k, n) >= Fraction(2, 3)), (history, mask)
    return {"n": n, "k": k, "eligible": True, "persist": persist, "pass": persist}


def source_binding():
    """Fail loudly if the source no longer matches the modelled rule."""
    src = GEE.read_text()
    checks = {
        "yearly_effect_is_strict_gt": bool(re.search(r"\.gt\(YEARLY_EFFECT_MIN\)", src)),
        "persistence_is_gte": bool(re.search(r"\.gte\(PERSISTENCE_MIN\)", src)),
        "valid_count_is_gte": bool(re.search(r"\.gte\(MIN_VALID_RECENT_YEARS\)", src)),
        "yearly_effect_min_is_0_02": bool(re.search(r"YEARLY_EFFECT_MIN = 0\.02\b", src)),
        "persistence_min_is_two_thirds": bool(re.search(r"PERSISTENCE_MIN = 2 / 3", src)),
        "min_valid_recent_years_is_2": bool(re.search(r"MIN_VALID_RECENT_YEARS = 2", src)),
    }
    return checks


def enumerate_all():
    histories = list(itertools.product((0, 1), repeat=4))                  # 16
    masks = [m for m in itertools.product((0, 1), repeat=4) if sum(m) >= 2]  # C(4,2)+C(4,3)+C(4,4)=11
    assert len(histories) == 16 and len(masks) == 11
    rows = []
    for h in histories:
        full = decide(h, (1, 1, 1, 1))
        for m in masks:
            r = decide(h, m)
            if full["pass"] and not r["pass"]:
                flip = "pass_to_fail"
            elif r["pass"] and not full["pass"]:
                flip = "fail_to_pass"
            else:
                flip = "unchanged"
            dropped = [y for y, keep in zip(YEARS, m) if not keep]
            dropped_disturbed = sum(d for d, keep in zip(h, m) if not keep)
            rows.append({
                "history": list(h), "mask": list(m), "retained_n": r["n"], "retained_k": r["k"],
                "full_disturbed": sum(h), "full_pass": full["pass"], "retained_pass": r["pass"],
                "flip": flip, "dropped_years": dropped,
                "dropped_disturbed": dropped_disturbed,
                "dropped_quiet": len(dropped) - dropped_disturbed,
            })
    return rows


def summarise(rows):
    by_flip, by_n, by_full = {}, {}, {}
    for r in rows:
        by_flip[r["flip"]] = by_flip.get(r["flip"], 0) + 1
        key = f"n={r['retained_n']}"
        by_n.setdefault(key, {}).setdefault(r["flip"], 0)
        by_n[key][r["flip"]] += 1
        key = f"full_disturbed={r['full_disturbed']}"
        by_full.setdefault(key, {}).setdefault(r["flip"], 0)
        by_full[key][r["flip"]] += 1
    # Does dropping only quiet years, or only disturbed years, behave differently?
    only_quiet = [r for r in rows if r["dropped_quiet"] and not r["dropped_disturbed"]]
    only_dist = [r for r in rows if r["dropped_disturbed"] and not r["dropped_quiet"]]
    return {
        "by_flip": by_flip, "by_retained_n": by_n, "by_full_disturbed": by_full,
        "dropping_only_quiet_years": {
            "cases": len(only_quiet),
            "fail_to_pass": sum(1 for r in only_quiet if r["flip"] == "fail_to_pass"),
            "pass_to_fail": sum(1 for r in only_quiet if r["flip"] == "pass_to_fail"),
        },
        "dropping_only_disturbed_years": {
            "cases": len(only_dist),
            "fail_to_pass": sum(1 for r in only_dist if r["flip"] == "fail_to_pass"),
            "pass_to_fail": sum(1 for r in only_dist if r["flip"] == "pass_to_fail"),
        },
    }


def edge_cases():
    """n<2 rejections, and the effect-size boundary, kept separate from the 176 pairs."""
    return {
        "n_equals_1_is_ineligible": decide((1, 0, 0, 0), (1, 0, 0, 0)),
        "n_equals_0_is_ineligible": decide((1, 1, 1, 1), (0, 0, 0, 0)),
        "yearly_effect_boundary": {
            "note": "disturbed uses strict >, so an effect of exactly YEARLY_EFFECT_MIN is NOT disturbed",
            "effect_0.0199_disturbed": 0.0199 > 0.02,
            "effect_0.0200_disturbed": 0.02 > 0.02,
            "effect_0.0201_disturbed": 0.0201 > 0.02,
        },
        "minimum_passing_counts": {f"n={n}": min((k for k in range(n + 1) if 3 * k >= 2 * n), default=None)
                                   for n in (2, 3, 4)},
    }


def build():
    rows = enumerate_all()
    binding = source_binding()
    return {
        "status": "MODEL_CHECKED",
        "not_established": [
            "This is an arithmetic model of the decision rule, not an execution of the Earth Engine "
            "calculation. No pixel persistence was computed.",
            "Uniform enumeration is NOT an empirical probability model for cloud-related missingness. "
            "Any percentage here is a fraction of enumerated cases, not an estimated field failure rate.",
            "176 pairs are enumerated scenarios; several share an observed retained history, so they "
            "are not 176 independent samples.",
            "Early-baseline (2018-2021) support is not modelled. All recent comparisons share that "
            "baseline and are not independent replications.",
            "Actual per-pixel clear-observation counts are a real-data follow-up; AOI scene counts "
            "do not prove per-pixel usable data.",
        ],
        "rule": {
            "source": "gee/ndvi_change.js",
            "disturbed": "yearlyComp > YEARLY_EFFECT_MIN (strict)",
            "persistence": "k/n >= PERSISTENCE_MIN (2/3), evaluated as 3k >= 2n",
            "eligibility": "n >= MIN_VALID_RECENT_YEARS (2)",
            "masked_years": "absent from both k and n; never imputed as quiet",
        },
        "source_binding": binding,
        "counts": {"histories": 16, "masks": 11, "pairs": len(rows)},
        "summary": summarise(rows),
        "worked_examples": {
            "fail_to_pass": {
                "history": [1, 1, 0, 0], "mask": [1, 1, 0, 0],
                "full": decide((1, 1, 0, 0), (1, 1, 1, 1)), "retained": decide((1, 1, 0, 0), (1, 1, 0, 0)),
            },
            "pass_to_fail": {
                "history": [1, 1, 1, 0], "mask": [1, 0, 0, 1],
                "full": decide((1, 1, 1, 0), (1, 1, 1, 1)), "retained": decide((1, 1, 1, 0), (1, 0, 0, 1)),
            },
        },
        "edge_cases": edge_cases(),
        "pairs": rows,
    }


if __name__ == "__main__":
    out = build()
    assert all(out["source_binding"].values()), f"source no longer matches the model: {out['source_binding']}"
    path = Path(__file__).with_name("missingness_sensitivity.json")
    path.write_text(json.dumps(out, indent=1) + "\n")
    s = out["summary"]["by_flip"]
    print(f"{out['counts']['pairs']} pairs | " + " ".join(f"{k}={v}" for k, v in sorted(s.items())))
    print("only-quiet dropped :", out["summary"]["dropping_only_quiet_years"])
    print("only-disturbed drop:", out["summary"]["dropping_only_disturbed_years"])
