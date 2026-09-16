# CR-09 — reviewed plan build, stopped at the T08 feasibility checkpoint — 2026-09-15

Plan: [docs/PLAN_2026-09-14_CR09.md](../../docs/PLAN_2026-09-14_CR09.md) (reviewed version, PR #18,
merged as e87079a). Build branch `task/cr09-reconcile-20260915`. Synthetic only; no imagery, no
site, no Mongolia result; CR-08 unchanged.

## Correction of sequence (read first)
PR #19 (bff0397) implemented and merged a path export from the **superseded** #17 plan on
2026-09-15, before the reviewed plan (#18) was seen. That was an agent error. This branch
**reverts #19** (fa9b9fd) so `main` again matches the premise the reviewed plan was written
against: chord-only export, v3 record, 86 → 85 tests. Everything below is built on that base.

## T00 — baseline
- Merged base: `e87079a` (main = #18 merged on bff0397); build base after revert: `fa9b9fd`.
- Working tree clean at T00 apart from the T01 artifacts below.
- Python 3.11.8, NumPy 2.4.6, SciPy 1.17.1 (fresh venv, `pip install -e "analysis[dev]"`).
- Baseline commands and exits at `fa9b9fd`: `pytest analysis/tests -q` 85 passed;
  `node tools/validate_phase1.mjs` pass; `node tools/test_temporal_qa.mjs` PASS;
  `tools/check_presentation.py` issues []; `tools/test_presentation.py` OK;
  `site_worksheet --check` consistent. Pre-existing failure, unchanged and historical:
  `evidence/sprint-2026-09-05/evaluate_candidate.py` (candidate hashes frozen 2026-09-06).

## T01 — archive and baseline snapshot (captured from the pre-CR-09 extractor at 9fa31ff)
| file | SHA-256 |
|---|---|
| `results/extractor_stress_cases_baseline_v3_2026-09-14.json` (= v3 record at 9fa31ff, byte-identical to the live record after the revert) | `f906d96b371039db2bea59fe0e971e41bd7e41520e5a61d69b7ac8230d51285f` |
| `results/extractor_stress_cases_baseline_2026-09-12.json` (v1) | `5baa8ff3e69fd829988b85800e60faee9bcdecc836a34d05019b7e8765bb300c` |
| `results/method_demo_synthetic.numeric.json` (legacy chord/scene record) | `620481b3b76e0759bdb05d80a55cbd2f42a1e6919b2c96fd793372a9c2fd2bf8` |
| `evidence/task-2026-09-14/baseline_candidates.json` (complete ordered candidate dicts, 10 cases + 5 sweep strengths, old extractor) | `43253aeb0bac8c8eed734f1489c7161ebabab29392a42ed2fd9530adbd52edee` |

## T02–T07 — helper, fixtures, attachment
`analysis/catanroads/extract.py::_component_path_px(mask)` implements contract steps 1–6 exactly:
padded-crop EDT, row-major nodes, symmetric 8-neighbour CSR edges, geometric two-sweep endpoints
from node 0 with lowest-ID ties (rtol=atol=1e-12), symmetric cost `ell*(1/edt(u)+1/edt(v))/2`,
single-source `dijkstra(indices=...)`, canonical lowest-ID reconstruction from distance labels,
lower endpoint ID first, every vertex kept, `ValueError` on empty/disconnected/unreachable/invalid
chain. `extract_candidates` attaches `path_px` (global coordinates) and `path_length_px` after
acceptance; selection, IDs, order and ranking untouched.
`analysis/tests/test_path_export.py`: straight, wide strip, diagonal-only, U-turn with both tips
on one side, border-touching, non-square, one-pixel ring, branched mask (A4) and the A1 legacy-field
invariant against the baseline snapshot (exact ints/lists, 1e-6 floats). 100 tests pass.
Observed on the wide strip fixture, as the plan's critique anticipated: the two-sweep heuristic
picks the corners (0,0) and (59,12) as endpoints; the middle of the route is on the medial row.

## T08 — A2/A3 with the unchanged v3 scorer (`feasibility_t08.py`, run 2026-09-15)
Each candidate's `path_px` supplied as temporary endpoint-only segment dictionaries to the
existing `score_lines` (tol_px=2, two 4-neighbour dilations). Runtime 1.02 s for six cases;
largest component 3328 px.

| case | path recall / precision | chord (v3) | frozen target | result |
|---|---:|---:|---|---|
| low_snr | 1.0000 / 1.0000 | 0.1055 / 0.1107 | A2 ≥ 0.80 | PASS |
| tight_curve | 1.0000 / 1.0000 | 0.2452 / 0.2636 | A2 ≥ 0.80 | PASS |
| demo_reference | 0.9347 / 1.0000 | 0.4448 / 0.4518 | A2 ≥ 0.80 | PASS |
| **wide_corridor** | **0.9688 / 0.9688** | 1.0000 / 1.0000 | A3 ≥ 0.98 | **FAIL** |
| faint_corridor | 0.9180 / 1.0000 | 0.9375 / 1.0000 | A3 ≥ 0.9175 / 0.9800 | PASS |
| gradient_background | 1.0000 / 0.8982 | 1.0000 / 0.9014 | A3 ≥ 0.9800 / 0.8814 | PASS |

**Feasibility stop applied.** A3 fails on the wide strip: the corner endpoints put the first and
last ~4 route pixels outside the 2-px band at each end (8 of 256 centerline pixels missed, 8 of
256 route pixels off). No threshold, tolerance, cost, connectivity, default or fixture was
changed. T09–T23 (selector, GeoJSON, scorer, v4 record, demo, docs, sensitivity seeds) were
**not started**. CR-09 stays incomplete; ledger status `blocked`.

## Development data disclosed
Before this build, one alternative endpoint rule was run once under the same contract (padded
EDT, all vertices): "deepest pixel at each major-axis projection extreme, ties lowest ID". It
also fails A3 (wide 0.9688 / 0.9764; faint 0.9102 < 0.9175) because the padded end column ties at
depth 1 and the tie again lands on a corner. It is not adopted and not in the code.

## Proposed prospective amendment (not adopted; owner decision)
Amend contract step 3 so endpoints are chosen among the pixels at each geometric extreme by
**minimal distance to the major axis** (the chord line already computed for `endpoints_px`),
ties lowest ID. Hypothesis: centred endpoints on straight strips, unchanged tips on curves.
Unmeasured; if accepted, re-run T08 and continue at T09 only if A2/A3 then pass.

## Remaining failures (mandatory taxonomy, unchanged)
Crossings rejected by component elongation; short dashes rejected by minimum length;
river-bank / field-edge confounds still accepted as the strongest candidate; faint routes still
fragmented into seven pieces; one route per accepted component does not resolve junctions,
loops or braided topology. Better line geometry does not improve road / non-road discrimination.

## Checks observed (repository root, venv above)
| command | observed |
|---|---|
| `python -m compileall -q analysis/catanroads analysis/tests` | exit 0 |
| `PYTHONPATH=analysis MPLBACKEND=Agg python -m pytest analysis/tests -q` | 100 passed (85 + 15 new) |
| `PYTHONPATH=analysis python evidence/task-2026-09-14/feasibility_t08.py` | exit 1 (A3 wide FAIL, table above) |
| `node tools/validate_phase1.mjs` / `node tools/test_temporal_qa.mjs` | pass / PASS |
| `tools/check_presentation.py` / `tools/test_presentation.py` | issues: [] / OK |
| `PYTHONPATH=analysis python -m catanroads.site_worksheet --check` | consistent |
| `git diff --check` | clean (ledger lines are CRLF by convention) |
