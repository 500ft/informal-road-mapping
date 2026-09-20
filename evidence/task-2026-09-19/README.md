# Week of 2026-09-19 — Day 1 intake and stack review (W0)

Plan: [docs/WEEKLY_PLAN_2026-09-19.md](../../docs/WEEKLY_PLAN_2026-09-19.md) (the committed,
critiqued version of the handoff draft). Day 1 is **review only**: no source file, record,
threshold, site or PR was changed by this task. Synthetic evidence throughout; CR-08 unchanged.

## 1.1 — Starting identities (observed 2026-09-19, not copied from PR text)

| item | observed |
|---|---|
| `origin/main` | `515ce3d` (PR #21 merged) |
| PR #22 `task/cr09-t09-t23-20260916` → main | head `37aa405`, MERGEABLE/CLEAN, check `analysis-tests` SUCCESS |
| PR #23 `docs/housekeeping-20260916` → main | head `6c8aa86`, MERGEABLE/CLEAN, check `analysis-tests` SUCCESS |
| PR #24 `figures/stress-gallery-20260916` → **`task/cr09-t09-t23-20260916`** | head `44f2b68`, MERGEABLE/CLEAN, **no checks reported** (see finding F3) |
| environment | Python 3.11.8, NumPy 2.4.6, SciPy 1.17.1, pytest 9.1.1, Node v26.8.2 |

The three head SHAs in the handoff draft match the live PRs; nothing moved over the weekend.

## 1.2 — Verification by execution (clean detached worktree of PR #22 `37aa405`)

The draft asked for a hand-written review matrix. A hand matrix restates test names and rots the
moment a test is renamed, so Day 1 instead **re-ran the claims** from a clean checkout and
**derived** the acceptance map from the tree. Every row below is an observed exit, not a PR quote.

| command | observed |
|---|---|
| `python -m compileall -q analysis/catanroads analysis/tests` | exit 0 |
| `PYTHONPATH=analysis MPLBACKEND=Agg python -m pytest analysis/tests -q` | **116 passed** |
| `PYTHONPATH=analysis python evidence/task-2026-09-14/feasibility_t08.py` | exit 0 (A2/A3 PASS) |
| `node tools/validate_phase1.mjs` / `node tools/test_temporal_qa.mjs` | exit 0 / exit 0 |
| `PYTHONPATH=analysis python -m catanroads.site_worksheet --check` | exit 0, no site verified |
| `python tools/check_presentation.py . "Informal Road Mapping" informal-road-mapping` | exit 0, issues: [] |
| `python tools/test_presentation.py` | exit 0 |
| `git diff --check` | clean |

Record reproduction, run independently of the committed file:

| check | observed |
|---|---|
| live CLI output == committed v4 record (numeric + metadata keys) | True |
| component layer == v3 archive, all ten cases | True |
| `chord_line` == v3 line layer, all ten cases | True |
| candidate ranking key excludes `path_length_px` | True |
| v1 and v3 archive SHA-256 == the hashes in `evidence/task-2026-09-14/README.md` | True |

**Gate A: PASS.** **Gate B: PASS** (one selector; see F1/F2 for the doc-level exception).
**Gate C: PASS with finding F1.**

### Acceptance → test map, derived from the PR #22 tree

| acceptance | tests |
|---|---|
| A1 | `test_a1_component_layer_and_ranking_match_v3` (test_stress_cases.py)<br>`test_a1_legacy_fields_ids_order_and_counts_match_the_pre_cr09_baseline` (test_path_export.py) |
| A2 | `test_a2_curved_corridors_pass_the_component_layer_and_the_delivered_line_layer` (test_stress_cases.py) |
| A3 | `test_a3_straight_corridors_do_not_regress` (test_stress_cases.py) |
| A4 | `test_a4_path_is_finite_adjacent_confined_and_repeatable` (test_path_export.py)<br>`test_a4_length_equals_segment_sum_via_extract` (test_path_export.py)<br>`test_a4_u_turn_stays_on_its_corridor_and_reaches_both_tips` (test_path_export.py)<br>`test_a4_wide_strip_endpoints_are_centred_after_amendment_a` (test_path_export.py)<br>`test_a4_ring_and_branch_give_one_connected_path_not_topology` (test_path_export.py)<br>`test_a4_contract_violations_raise` (test_path_export.py) |
| A5 | `test_a5_geojson_and_scorer_deliver_the_same_pixels` (test_stress_cases.py) |
| A6 | `test_a6_corrupting_the_path_degrades_line_scores_and_leaves_component_scores_fixed` (test_stress_cases.py)<br>`test_a6_corrupting_the_chord_with_a_valid_path_leaves_delivered_geometry_fixed` (test_stress_cases.py) |
| A7 | `test_a7_malformed_present_path_raises_through_every_consumer` (test_stress_cases.py) |
| A8 | `test_a8_archived_records_are_byte_unchanged_and_component_numbers_agree` (test_stress_cases.py)<br>`test_a8_record_has_complete_v4_metadata` (test_stress_cases.py)<br>`test_a8_cli_reproduces_the_committed_numeric_payload_exactly` (test_stress_cases.py) |

Derivation: every `def test_a<N>_*` in the four test modules on `37aa405`. If a test is renamed
or dropped, this table is regenerated from the tree rather than edited, so it cannot silently
disagree with the suite.

## 1.3 — Review conflicts and findings

The draft listed seven conflict classes to hunt. Checked, with the result:

| class hunted | result |
|---|---|
| hidden changes to defaults, selection, IDs, ranking, tolerances, Phase-1 thresholds | none; A1 tests and the v3 comparison hold, sort key unchanged |
| path scored but not exported / not plotted | none; `candidate_coordinates_px` is the single selector for GeoJSON, scorer, demo (A5) |
| malformed path silently falling back to the chord | none; raises `ValueError` through every consumer (A7) |
| v4 metadata missing baseline revision, metric, runtime, generator, superseded records | none; all present (A8) |
| result generation that can truncate the committed JSON | **F1 — open** |
| a target asserted without keeping the old chord control | none; `chord_line` is recorded per case and asserted against v3 (A2) |
| docs implying real-road accuracy | none found; every surface says synthetic |

### F1 — the repository documents an unsafe regeneration command (Gate C, owner decision)

`results/README.md` on #22 says *"Regenerate with `PYTHONPATH=analysis python -m catanroads.stress_cases`"*.
The reviewed plan's own critique row requires the opposite: *"stage output in a temporary file,
validate, then replace"*, because the CLI writes to stdout and a shell redirect truncates the
committed record if the run fails midway. The plan's T17 and its verification block say this; the
user-facing guide does not. The record on #22 was in fact produced the safe way (staged, validated,
copied — recorded in `evidence/task-2026-09-14/README.md`), so this is a documentation defect that
invites an unsafe repeat, not a corrupted artifact.

### F2 — nothing makes the safe procedure the easy one (Gate C, follow-up)

`stress_cases.__main__` only writes to stdout. The safe procedure is prose a reader must follow.
Proposed bounded fix: an `--out PATH` flag that writes to a temporary file in the destination
directory, parses it back, and then `os.replace`s it into place (stdlib only, no new dependency),
with the guide and the plan's verification block pointing at the flag. Not done on Day 1: Day 1 is
review only.

### F3 — PR #24 has never been exercised by hosted CI

`.github/workflows/ci.yml` triggers on pull requests targeting `main` and `task/priority-one-*`.
PR #24 targets `task/cr09-t09-t23-20260916`, so no check ran; `gh pr checks 24` reports none. Its
gallery test passed locally, but the hosted gate has not seen it. When #22 merges, GitHub retargets
#24 to `main` and CI will run; the merge sequence must therefore **wait for #24's first check**
rather than treating its current clean status as a green build.

## Findings summary

| id | gate | severity | state | proposed owner decision |
|---|---|---|---|---|
| F1 | C | low (docs) | open | fix inside #22 before merge (one commit, the line is introduced by #22), or follow-up after merge |
| F2 | C | low (ergonomics) | open | schedule as the Day-3 bounded fix, or decline as unnecessary |
| F3 | — | medium (process) | open | none needed; the merge sequence in the plan now waits for #24's first CI run |

No finding blocks Gate A or Gate B. CR-09 remains merge-ready on the evidence observed here.

## Not done on Day 1
No code, record, threshold, site, manifest, ledger row or PR state was changed. No imagery was
inspected. CR-08 is unchanged and still blocked on a dated source-image judgment.

---

# Day 2 — 2026-09-20 — gallery review and owner review request (W1)

PR #25 merged as `c5886a4`; `main` is at that commit. Day 2 produces two artifacts: a written
review of the five-figure gallery on PR #24, and the owner review request below. Still no change to
any record, threshold, site or the Phase-1 gate.

## Gallery review — PR #24, base head `44f2b68`

Reviewed against the six criteria in the plan. The gallery is my own work from 2026-09-16, so it is
reviewed here as a reviewer would, not defended.

| criterion | result |
|---|---|
| scores read from the committed record, not typed | **fail → fixed (G1)** |
| scene labelled synthetic / development evidence | pass — every figure carries the same footer naming the generator and denying imagery |
| component recall kept distinct from exported-line recall | **fail → fixed (G2)** |
| no implication of real imagery or road classification | pass — no figure names a site, a region or an accuracy |
| no clipped labels, overlapping annotations or misleading legend | pass after the Day 2 wrap; the three-panel notes collided once the labels grew and were wrapped to two lines |
| listed in the figure manifest and the figure guide | pass — one manifest entry with all five outputs, its generator, its three inputs and its command, and one row in `docs/data-and-figures.md` |

### G1 — figure 4 carried hand-typed observed numbers

`04_low_snr_curve.png` had the suptitle *"component recall 1.00; chord 0.11 → path 0.99"* written as
a literal string, while every other number in the gallery is read from
`results/extractor_stress_cases.json`. Three observed values in the most quotable position on the
figure would have gone stale silently the first time the record changed. Now derived from the record
like the rest; the rendered title is unchanged today because the values are the same, which is the
point.

Not a defect: figure 3's *"A3 target ≥ 0.98"* is a frozen plan constant, not an observed score, and
is correctly a literal.

### G2 — figure 5 said "recall" without naming the layer

`05_misses_and_confound.png` annotated the crossing and dashed-track panels *"recall 0.00"*. Both
layers are in fact 0.00 there, so no number was wrong, but the whole subject of the gallery is that
component recall and exported-line recall differ, and this is the one figure that blurred them. Both
are now named per panel (`component recall … · line recall …`), and the longer labels are wrapped to
two lines because they collided with the neighbouring panel at the first attempt.

Both corrections are on #24 as a second commit, `1b06128`. No figure was redesigned, no layout
reworked, no new figure added. 117 tests pass; presentation checks clean.

## Owner review request

Three pull requests are ready. Each needs **one** decision; none needs a repository-wide read.

| PR | what it is | the one decision |
|---|---|---|
| **#22** CR-09 T09–T23 | The path export: one interior-biased route per accepted component, delivered through a single selector to GeoJSON, scoring and the demo. Curved corridors go from 0.11 / 0.25 / 0.44 line recall to 0.99 / 1.00 / 0.93; the legacy chord is retained per case as `chord_line`; the component layer is byte-identical to v3. Re-verified Day 1 from a clean checkout. | Approve the representation, or name one bounded correction. |
| **#24** gallery | Five figures showing what the extractor now delivers and what it still gets wrong, with the two Day 2 corrections applied. Stacked on #22's branch. | Approve, or name a figure to change. |
| **#23** docs housekeeping | Progress and review-index entries for the R03 stack, ponytail and CR-09; the stale CatanRoads links retargeted; the CR-08 intake re-check recorded. | Approve. |

Proposed order, unchanged from the plan: **#22**, then **#24 once its first hosted CI run passes**
(finding F3: it has never been checked, because the workflow only triggers on pull requests to
`main`; merging #22 retargets it and the check runs for the first time), then **#23**.

Still open from Day 1, and not decided by me: **F1/F2**, whether the unsafe documented regeneration
command and the missing atomic writer are fixed inside #22 before merge or as a follow-up. My
recommendation remains fixing it inside #22, because the offending line is introduced by #22 and is
not yet on `main`.

## Not done on Day 2
No record, threshold, site, manifest or ledger row changed. No imagery inspected. CR-08 unchanged.
