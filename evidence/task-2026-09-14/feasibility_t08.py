"""T08 (docs/PLAN_2026-09-14_CR09.md): evaluate A2/A3 with the EXISTING v3 scorer by supplying
each candidate's path as temporary endpoint-only dictionaries. Prints the frozen targets and the
observed values; exits 1 if any target fails. Development material, not site evidence.

Run from the repository root:  PYTHONPATH=analysis python evidence/task-2026-09-14/feasibility_t08.py
"""
import json, sys, time
from pathlib import Path
import numpy as np
from catanroads import extract_candidates
from catanroads import stress_cases as SC

ROOT = Path(__file__).resolve().parents[2]
V3 = json.loads((ROOT / "results/extractor_stress_cases_baseline_v3_2026-09-14.json").read_text())["cases"]
CURVED, STRAIGHT = ("low_snr", "tight_curve", "demo_reference"), ("wide_corridor", "faint_corridor", "gradient_background")

rows, ok_all, t0, biggest = [], True, time.perf_counter(), 0
for name in CURVED + STRAIGHT:
    d, truth, cl = SC.CASES[name](); cands = extract_candidates(d)
    biggest = max([biggest] + [c["n_pixels"] for c in cands])
    segments = [dict(endpoints_px=[p, q]) for c in cands for p, q in zip(c["path_px"], c["path_px"][1:])]
    s = SC.score_lines(cl, segments, truth=truth); r, p = s["line_recall"], s["line_precision"]
    r3, p3 = V3[name]["line_recall"], V3[name]["line_precision"]
    if name in CURVED:
        target, ok = "A2: recall and precision >= 0.80", r >= 0.80 and p >= 0.80
    elif name == "wide_corridor":
        target, ok = "A3: recall and precision >= 0.98", r >= 0.98 and p >= 0.98
    else:
        target, ok = f"A3: >= own v3 - 0.02 ({r3 - 0.02:.4f} / {p3 - 0.02:.4f})", r >= r3 - 0.02 and p >= p3 - 0.02
    ok_all &= ok
    rows.append(dict(case=name, path_line_recall=r, path_line_precision=p, chord_v3_recall=r3, chord_v3_precision=p3, target=target, result="PASS" if ok else "FAIL"))
print(json.dumps(dict(scorer="v3 score_lines, tol_px=2 (two 4-neighbour dilations), unchanged", runtime_s=round(time.perf_counter() - t0, 2),
                      largest_component_px=biggest, rows=rows, a2_a3=("PASS" if ok_all else "FAIL")), indent=1))
sys.exit(0 if ok_all else 1)
