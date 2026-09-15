# CR-09 — export the corridor's path, not one chord — 2026-09-15

Branch `task/cr09-path-export-20260914` off `main` 0028c5f (merged plan
[docs/PLAN_2026-09-14_CR09.md](../../docs/PLAN_2026-09-14_CR09.md), PR #17). Built
2026-09-15; the plan named the evidence folder `task-2026-09-14`, this folder is dated
by when the work was actually done. Owner decisions in the plan were not edited before
merge, so the proposed defaults apply: `path_px` as a new field beside the unchanged
chord; 4-px subsample; Task 2 in the same PR.

## What changed
`extract.medial_path` builds the 8-neighbour graph of one component's pixels with edge cost
`1/edt` (scipy `distance_transform_edt`, `sparse.csgraph.dijkstra`; no new dependency),
picks the deepest pixel at each extreme of the major-axis projection as the two ends, and
exports the cheapest route between them, subsampled every 4 px, as `path_px`.
`endpoints_px`, `length_px`, `width_px`, `orientation_deg`, `elongation` and the component
layer are untouched. `to_geojson` and the demo figure draw `path_px`;
`stress_cases.score_lines` scores it.

## Before / after (exported-line layer vs reference centerline, tol 2 px)
| case | component recall | v3 line recall / precision (chord) | v4 line recall / precision (`path_px`) | line_ok v3 → v4 |
|---|---:|---:|---:|---|
| demo_reference | 0.92 | 0.44 / 0.45 | 0.94 / 1.00 | no → **yes** |
| low_snr (curve) | 1.00 | 0.11 / 0.11 | 1.00 / 1.00 | no → **yes** |
| tight_curve (hairpin) | 1.00 | 0.25 / 0.26 | 0.97 / 1.00 | no → **yes** |
| wide_corridor | 1.00 | 1.00 / 1.00 | 1.00 / 1.00 | yes → yes |
| faint_corridor | 0.93 | 0.94 / 1.00 | 0.91 / 1.00 | yes → yes |
| gradient_background | 1.00 | 1.00 / 0.90 | 1.00 / 0.90 | yes → yes |
| crossing / short_segments | 0.00 | 0.00 / — | 0.00 / — | miss → miss |
| linear_confound_riverbank | — | — / 0.00 | — / 0.00 | fabricated → fabricated |

Component-layer numbers (`n_candidates`, `n_false_candidates`, `pixel_recall`,
`pixel_precision`) are identical to v3 and to the v1 baseline for every case
(asserted by `test_committed_record_matches_live_run` against the new record and
`test_baseline_record_is_preserved_unchanged`). The faint corridor's line recall moved
0.94 → 0.91: its seven fragments' paths end at the deepest pixel of each fragment
rather than the chord's extrapolated tip. No default, `tol_px` or 0.5 threshold changed.

## Record
`results/extractor_stress_cases.json` is now schema v4 (`supersedes` names v3 and
states the line layer scores `path_px`); `results/extractor_stress_cases_baseline_2026-09-12.json`
is byte-unchanged. `results/method_demo_synthetic.png` was regenerated from
`analysis/demo_synthetic.py`; `results/method_demo_synthetic.numeric.json` and its four
tests are untouched because the chord fields did not change.

## Tests
- `test_hairpin_chord_is_flat_but_its_exported_path_doubles_back` (was `..._is_summarised_as_one_straight_segment`): chord still flat; `path_px` y-extent > 15 px.
- `test_curved_corridors_pass_the_component_layer_and_now_the_line_layer` (was `..._and_fail_the_line_layer`): the three curved cases reach `line_ok`; the two `< 0.2 / < 0.35` bounds became `>= 0.5`.
- New: `test_straight_component_path_stays_within_2px_of_its_chord`.
- The four negative controls that overwrote `endpoints_px` now overwrite `path_px`; `test_geojson_shape` accepts ≥ 2 coordinates.

## Checks observed (repository root, fresh venv, `pip install -e "analysis[dev]"`)
| command | observed |
|---|---|
| `python -m compileall -q analysis/catanroads analysis/tests` | exit 0 |
| `PYTHONPATH=analysis MPLBACKEND=Agg python -m pytest analysis/tests -q` | **86 passed** (85 + 1 new) |
| `python -m catanroads.stress_cases` vs committed v4 record | equal (tested by `test_cli_reproduces_the_committed_record_exactly`) |
| `node tools/validate_phase1.mjs` | passed (6 sites; Z_MIN=1.0; four QA layers) |
| `node tools/test_temporal_qa.mjs` | PASS |
| `python tools/check_presentation.py . "Informal Road Mapping" informal-road-mapping` | issues: [] |
| `python tools/test_presentation.py` | OK |
| `PYTHONPATH=analysis python -m catanroads.site_worksheet --check` | consistent |
| `MPLBACKEND=Agg python analysis/demo_synthetic.py` | wrote figure, 6 candidates |

## Task 2 — what stays missed, by construction (CR-09 taxonomy)
Unchanged and still pinned by tests; no parameter was touched:
- **Junctions** (`crossing`): two full corridors form one 8-connected component whose elongation is below `min_elongation=3`; zero candidates. A junction-aware extractor is a separate task with its own stress cases.
- **Gaps** (`short_segments`): 9-px dashes each under `min_length_px=12`; zero candidates. Gap bridging is likewise a separate task.
- **Linear non-road features** (`linear_confound_riverbank`): a river-bank-shaped ridge is returned as the single strongest candidate, precision 0. Nothing in geometry can separate it from a road; this is the class field verification exists for.

## Not done
No imagery, no site, no Mongolia result; CR-08 unchanged. `path_px` follows the
component's medial axis; it says nothing about whether the component is a road.
