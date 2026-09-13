# CR-R03 — extractor stress test beyond the favourable demonstration — 2026-09-12

Branch `audit/extractor-stress-cases-20260912` off `main` a006adb. Sprint order task 7.

## Method
Ten deterministic synthetic constructions in `analysis/catanroads/stress_cases.py`, each with its own truth mask, scored by pixel recall and precision within 2 px and by the number of candidates with < 20 % overlap with truth. Case docstrings describe the construction only; what the extractor did is in `results/extractor_stress_cases.json` and pinned by `analysis/tests/test_stress_cases.py`, so a future change in behaviour is a named test failure.

## Observed (extractor defaults)
| case | candidates | false | pixel recall |
|---|---:|---:|---:|
| demo_reference | 6 | 0 | 0.92 |
| faint_corridor | 7 | 0 | 0.93 |
| wide_corridor | 1 | 0 | 1.00 |
| crossing | 0 | 0 | 0.00 |
| short_segments | 0 | 0 | 0.00 |
| linear_confound_riverbank | 1 | 1 | — |
| speckle_only | 0 | 0 | — |
| low_snr | 1 | 0 | 1.00 |
| gradient_background | 3 | 2 | 1.00 |
| tight_curve | 1 | 0 | 1.00 |

Detection cliff on the same corridor at 1.3 / 1.15 / 1.05 / 1.0 / 0.9 × `disturb_thresh`: recall 1.00 / 0.93 / 0.48 / 0.27 / 0.00.

**Detects:** wide, low-SNR, gradient-background and hairpin corridors; faint corridor detected but split into seven pieces.
**Misses:** two crossing roads (zero candidates — the union component fails `min_elongation=3`; lowering it to 1.5 recovers *one* component for two roads); a dashed track of 9-px segments (each below `min_length_px=12`).
**Fabricates:** a river-bank-shaped linear feature is returned as the single, strongest candidate (precision 0); the gradient ramp adds two small false candidates.
**Misrepresents:** the hairpin is summarised as one straight 128 × 22 px segment; under 3× noise a 3-px corridor is reported 53 px wide.
**Robust:** isolated speckle up to 4000 specks yields no candidates.

## Corrections to my own expectations
The case docstrings were first written with predictions (faint → miss, wide → hollow/double detection, hairpin → rejection). Three of those were wrong when run. The predictions were removed; only constructions and observed results are recorded.

## Checks observed
| command | observed |
|---|---|
| `python -m pip install -e ./analysis --no-deps` then `python -m pytest -q analysis/tests` | 74 passed (11 new) |
| `python -m catanroads.stress_cases` vs committed record | identical |

## Not done
No imagery, no site, no Mongolia result; CR-08 unchanged. The failure classes feed CR-09's taxonomy; they do not replace field verification.

## Review repair (CR-R03b, same day)
Two defects the 2026-09-12 review found, both reproduced before fixing:
1. **The score ignored the exported geometry.** Replacing every candidate's `endpoints_px` with an obviously wrong segment left pixel recall/precision unchanged — the metric measured the internal component mask, not what the extractor delivers. Added an exported-line layer (`score_lines`: rasterise each `endpoints_px` segment, recall/precision within 2 px). Negative control: the same substitution drops wide-corridor line recall 0.38 → 0.02.
2. **The width claim was wrong.** "53 px width under 3× noise" — `width_px` is the component's minor-axis extent; for the curved corridor it is **54.7 px at zero noise** (the curve's transverse extent) against a 3 px road. Noise was not the cause. Corrected in the record, README and tests.

What the line layer exposes: every curved corridor — including the favourable demo — passes the component layer and fails the exported line (low-SNR curve 0.10, hairpin 0.27, demo 0.35). Straight corridors pass both. The v1 record is preserved byte-unchanged as `results/extractor_stress_cases_baseline_2026-09-12.json`; a test asserts the v2 component-layer numbers equal it. 80 tests pass; the CLI-equals-record check is now itself a test.

## Review repair 2 (CR-R03c, 2026-09-13)
Reproduced: a manually specified perfect centerline through the 13-px straight road scored line recall 0.385 (precision 1.00, `line_ok` false) because the v2 line layer was scored against the road-**area** mask; a 2-px band covers 5/13 of it. Every case now returns a 1-px **reference centerline** (the demo scene's from its generator's own parametric curves, pinned to the truth mask by a test; no new dependency), and `score_lines` compares exported segments to that centerline. `area_coverage` is reported separately and never enters `line_ok`. Tests: perfect centerline → 1.0/1.0 regardless of width; a 5-px off-centre line inside the road → recall 0; wrong diagonal still 0.02; every case's centerline lies inside its truth. Record v3; v1 baseline unchanged; 85 tests; CLI-equals-record tested.
