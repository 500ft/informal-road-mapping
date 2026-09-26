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

---

# Day 3 — 2026-09-21 — audit guidance, F1/F2, and the CR-08 packet (W2 + W3)

Base: `main` at `dcf9df0`. Two things happened before this work started that change the record.

## F4 — the merge order stranded the gallery (found 2026-09-21, fixed here)

The owner merged all three review PRs today: #22 into `main` at 14:13:55, #23 into `main` at
14:14:16, and **#24 into `task/cr09-t09-t23-20260916` at 14:15:31** — that is, into a base branch
that had already been merged into `main` two minutes earlier. The gallery therefore landed on an
orphaned branch and **never reached `main`**: no `results/figures/`, no
`analysis/plot_stress_cases.py`, no `analysis/tests/test_plot_stress_cases.py`. The Day 3 code work,
which had been pushed to the same branch, was stranded with it.

This is Day 1 finding F3 arriving by a different route. F3 said a stacked pull request has no CI
until its base merges and GitHub retargets it; the same stacking also means that **merging the base
first leaves the stacked branch pointing at a commit that is already history**. Merging the stacked
PR afterwards is a no-op with respect to `main`.

Recovered here by merging the orphaned branch into a branch cut from `main`. Verified present after
recovery: five figures, the generator, its smoke test, the `--out` writer, the guidance document and
the `AGENTS.md` link. Nothing was rebuilt or regenerated; the recovery is a merge, so the gallery
commits `44f2b68` and `1b06128` keep their identity.

**Rule added to the plan's definition of done:** when a stacked pull request exists, merge the
stacked one first, or re-target it before merging its base.

## Audit guidance addendum — coverage checked before anything was added

The guidance asks that existing coverage be confirmed before new tests or tools appear. All six
sections were checked against the tree; three were already satisfied and nothing was added for them.

| section | verdict |
|---|---|
| 3 input changes reach the artifact | already covered by `test_a6_corrupting_the_path_*` and `test_a6_corrupting_the_chord_*`; nothing added |
| 5 evidence provenance | already the repository's discipline; restated in the CR-08 packet |
| 6 first useful failure signal | already satisfied; the CR-09 evidence discloses the two rejected endpoint rules as development data |

Three were genuine gaps and are closed:

**Section 1 — independent expected results.** `evidence/task-2026-09-14/baseline_candidates.json`
was produced by the pre-CR-09 extractor itself, so `test_a1_*` proves the legacy fields did not move
and nothing more. That status is now written into the test module so no reader mistakes it for a
correctness oracle. Two fixtures already carried hand-derived coordinates (the wide strip's centre
row, the U-turn's two tips); two more now do, where the route is uniquely determined: a 3×40 strip
must be row 1 left to right, and a 20×20 identity has exactly one 8-connected chain. Both
expectations were written before running the router and both passed unchanged, which is the first
falsifiable confirmation of the routing itself rather than of its own baseline. The non-square
fixture now asserts that coordinates are `(x, y)` and not `(row, col)` — a 25×7 mask makes a
transposition visible, and a square one cannot.

**Section 2 — coordinate probes.** The existing transform test computed its expectation from the
same lambda it passed in, so it proved that one function ran over every vertex, not that the right
argument reached the right axis; its x and y scales were equal in magnitude, so a transposition
survived. Added a probe under the guidance's own suggested transform, `(x, y) -> (100 + 2x, 200 - 3y)`,
with vertices computed by hand. Pixel-space length remains pixels; nothing here validates a real
affine transform or CRS, and the guidance says so.

**Section 4 — saved artifacts.** Every geometry comparison was in-memory. Added a
`json.dumps`/`json.loads` round-trip comparing candidate ids, vertex order, coordinate values and
`path_length_px` semantics, and asserting neither coordinate array leaks into `properties`.

## F1 and F2 — closed

`results/README.md` documented regeneration as a plain CLI run, which a shell redirect turns into a
truncation risk; the reviewed CR-09 plan required temp-file staging and the guide contradicted it.
`stress_cases.main` now takes `--out PATH`: it writes a temporary file beside the destination,
validates it by parsing it back and checking schema, geometry field, required metadata, every case
and the strength sweep, then `os.replace`s it. stdout remains the default and is byte-identical, so
`test_a8_cli_reproduces_the_committed_numeric_payload_exactly` is unaffected. Two tests: `--out`
matches stdout and leaves no temporary file; a regeneration that fails validation leaves an accepted
record byte-identical and removes its temporary file.

## Phase-1 CLI rehearsal (no Earth Engine run, controlled synthetic and missing inputs)

| input | exit | status | traceback |
|---|---:|---|---|
| synthetic, well-formed | 3 | DEVELOPMENT_ONLY | no |
| export-labelled, well-formed | 0 | SCREEN_PASS | no |
| export-labelled, all development sites below the floor | 1 | SCREEN_FAIL | no |
| the committed unverified manifest, well-formed metrics | 2 | INCONCLUSIVE | no |
| missing export file | 2 | INCONCLUSIVE | no |

All four documented exit codes reproduce through the real CLI and a missing export fails closed
without a traceback that could be mistaken for a result.

## CR-08 packet

[cr08-first-site-packet.md](cr08-first-site-packet.md): a proposed inspection order with its
reasoning and a named alternative, the blank judgment form, the rule that no evidence category
substitutes for another, what happens to each of the three outcomes, and the machine-checkable
export preflight checklist bound to the existing gate. No site, coordinate, role or flag was
touched; no imagery was inspected. CR-08 remains blocked.

## Checks observed
`compileall` exit 0 · `pytest analysis/tests -q` **124 passed** · `feasibility_t08.py` exit 0 ·
both Node checks exit 0 · `site_worksheet --check` exit 0 · both presentation checks exit 0 ·
`git diff --check` clean · committed stress record byte-unchanged.

---

# 2026-09-22 — dependency bumps merged, and the CR-08 intake path completed from the literature

## Merges
PR #29 (literature review) merged as `1194d94`. Three Dependabot pull requests then merged:
`actions/checkout` 5 → 7 (#31), `actions/setup-node` 4 → 7 (#33), `actions/setup-python` 6 → 7
(#32, which conflicted once the other two landed and was rebased by Dependabot rather than bypassed).
All four carried passing `analysis-tests`, CodeQL and dependency-review checks. `main` is `e44f314`
and its post-merge CI and CodeQL runs both completed successfully on all three bumped actions.

## CR-08 intake path — two additions the literature made necessary

The packet delivered on Day 3 was complete against the repository's own knowledge. The literature
review merged the same week showed it was incomplete in two specific ways, both now closed.

**1. Three missing confound strata.** The inspection form asked an inspector to rule out
agriculture, riverbeds, shadow and settlement. The literature identifies three more that a
geometry-driven detector provably cannot separate from a road, none of which this project carried:

| stratum | evidence |
|---|---|
| dry drainage channel / wadi | Liu 2016 extracts desert wadis and reports commission errors occurring mainly in features falsely enhanced by water indices — **specifically roads**. The same confusion, documented in the mirror direction, in arid terrain, at moderate resolution. |
| fence line | Buzzard 2022 measures ~0.93 km of fence per km² (max 14.9) in comparable grazing country and built its fence model partly *from* road layers. A pervasive background signal, not a rare confound. |
| animal path / livestock trail | Chemura 2024 mapped off-road tracks and animal paths together in open rangeland and found them co-occurring at **r = 0.75**, requiring a separate classification stage even at 50 cm. |

Queiroz 2020 states that roads, pipelines, seismic lines and power lines are **one detectable class**
for geometry-driven extractors, and Nagel 2024 finds a deep model cannot separate road from seismic
line at Sentinel-2 resolution. Geometry alone cannot decide roadness, which is the reason this
inspection exists. The three strata were added **to the worksheet generator**
(`analysis/catanroads/site_worksheet.py`), not hand-edited into its output, and the committed
worksheet was regenerated from it; `test_committed_sheet_matches` still passes.

**2. The recovering site needs a named variable and a range.** The packet now carries the four-study
spread — ~4 years for cover and biomass, 10–15 for full revegetation, two decades for severe tundra
impacts, 80–130 for soil compaction — and requires the inspector to state *which variable* was
judged. Li 2006 shows early steppe recovery is a compositional change rather than a return to
background greenness, and Kinugasa & Oda 2014 found track formation removed 8.3–9.4 cm of soil and
the seed bank with it, so recovery is not simple regrowth.

## Checks observed
`pytest analysis/tests -q` **124 passed** · `site_worksheet --check` consistent · both Node checks
exit 0 · both presentation checks exit 0 · `git diff --check` clean · all six `verified` flags still
`false`.

## Not done
No site, coordinate, role or flag was changed. No imagery was inspected. CR-08 remains blocked on
one dated source-image judgment, and the first-site order (`dev-01-braided` proposed,
`negative-01` the named alternative) is still an open owner decision.

---

# Day 5 — 2026-09-23 — evaluation protocol and the next-experiment design (W4)

Base: `main` at `2dd6992`. Two design documents, no implementation, no code change.

## Artifacts
- [docs/PHASE1_EVALUATION_PACKET.md](../../docs/PHASE1_EVALUATION_PACKET.md) — the blank template a
  real Phase-1 run fills in: identity and hashes, Earth Engine task ids with their **terminal state**
  (a launch is not a completed export), per-site metrics against the frozen settings read from
  `phase1_gate.py`, the primary decision recorded **before** any sensitivity run, exclusions, and an
  explicit list of what a SCREEN_PASS does not establish. It restates the collection check found on
  2026-09-22: the Processing Baseline 04.00 offset falls between the two analysis windows, so a
  non-harmonized collection would inject a false step change into exactly this comparison.
- [docs/specs/phase-2-topology-followup/plan.md](../../docs/specs/phase-2-topology-followup/plan.md) —
  Options A, B and C for the one-path-per-component ceiling, each with its required input,
  dependency, exposing synthetic cases, invariant metrics, false-positive modes, cost and promotion
  trigger.

## Recommendation and why it is not inertia
**Option C (defer topology) stands**, on three grounds the literature review supplied:

1. Hannink 2014 places the junction loss **in the Hessian filter**, so Options A and B both operate
   on a component the filter already merged or dropped. Neither can recover a crossing downstream.
2. No site is verified and no export exists, so improving candidate geometry optimises a quantity
   that has never been compared to a real corridor.
3. The dominant error is **not topological**. The extractor fabricates a river-bank-shaped feature
   as its strongest candidate, and Liu 2016, Nagel 2024 and Queiroz 2020 show that is a field-wide
   failure. Better line geometry does not improve road versus non-road discrimination.

The note therefore ranks four non-topology alternatives instead, led by the per-band median
composite issue (Roberts 2017), which is a correctness question upstream of everything else.

## CAD scope, asked and answered
No part of Day 5 requires CAD or FEA. The owner's own recorded guidance
([ENGINEERING_AUDIT_PLANNING_GUIDANCE_2026-09-21.txt](../../docs/ENGINEERING_AUDIT_PLANNING_GUIDANCE_2026-09-21.txt))
states that reusable CAD/FEA machinery belongs in `500ft/engineering-audit` and that **no CAD/FEA
work is added to this satellite-mapping project** by that reference. Nothing was added.

## Checks observed
`tools/check_presentation.py` issues: [] with 78 local links · `tools/test_presentation.py` OK ·
`git diff --check` clean. No code, test, record, threshold, site or gate touched; all six `verified`
flags remain `false`; CR-08 unchanged.

---

# 2026-09-24 — literature corrections from the owner's critique

The owner audited the merged literature review against the primary sources and found several claims
overstated. **Every correction was checked here and every one was correct.** The failure mode was
consistent: a measured result from one study, one sensor and one outcome carried across as if it
constrained this project. Where I had written a bound, the source supported only an example.

## Verified before accepting

| check | result |
|---|---|
| Web Mercator ground span at the six registered latitudes | 6.61–7.02 m for a nominal-10 pixel; 50 px = 2,187–2,465 m² against the 5,000 m² assumed |
| the NDVI commutation counterexample (red [0.10, 0.40, 0.30], NIR [0.20, 0.50, 0.90]) | ratio-of-medians 0.25, median-of-ratios 1/3 — reproduced exactly |
| is `ridge_strength` Frangi? | **no** — `max(0, -λ_min)·σ²`, Sato-like, no eigenvalue-ratio suppression; its own docstring says so |
| does BSI use a 20 m band? | yes, B11 alongside B4, B8, B2 at 10 m |

## Corrections applied

Nine bibliography entries, seven claim-ledger claims, the evaluation packet's section 0 and frozen
settings, the topology note, and the categorical language throughout `gaps.md`
("no paper exists" → "not located in this review"). One claim added:

**C19 — the analysis grid's nominal metres are not ground metres.** Independently calculated, not
measured on an export. `path_length_px` must never be converted to metres using an assumed 10.

Two consequences I had missed and which the critique surfaced:

- **Option A cannot recover the case it was proposed for.** It skeletonises *accepted* components,
  but the `crossing` case produces **zero** accepted components. Recorded as a placement conflict.
- **A grade must record its access level.** Some entries were graded from a Crossref record alone,
  which cannot support an independent-validation grade. Noted in `gaps.md`.

## New tests
`analysis/tests/test_support_and_compositing.py` pins both arithmetic facts — the ground-scale
shortfall at every registered site, and the non-commutation of ratio-of-medians against
median-of-ratios, including the case where a missing band changes which acquisitions are jointly
valid. Neither test asserts which estimator is better; that is unmeasured.

## Checks observed
`pytest analysis/tests -q` **129 passed** (124 + 5 new) · both Node checks · worksheet check · both
presentation checks · `git diff --check` clean. No threshold, default, site, gate or committed
record changed; all six `verified` flags remain `false`; CR-08 unchanged.

## Not done from the critique's work package
Sections 2 to 6 propose diagnostics needing Earth Engine access or owner time: the runtime grid
probe, the compositor A/B on real imagery, the missing-year sensitivity on real QA pixels, and the
triage response design. The two arithmetic oracles are delivered above; the rest remain specified
and unexecuted.

---

# 2026-09-24 (second pass) — propagating C19 into the documents it invalidated

The literature corrections left three inconsistencies and surfaced one new consequence. All four are
closed here. **No threshold, site, window, setting or committed record changed.**

## What was inconsistent

1. **`docs/design.md` described the screen as running on "a fixed 10 m grid".** After C19 that is
   incorrect — it conflates nominal Web Mercator units with ground distance. The same document also
   still carried the sub-pixel claim in the form the corrected ledger says to restate, so the two
   documents disagreed about the same decision.
2. **`docs/PHASE1_RUNBOOK.md` listed `min_component_pixels=50` with no ground-area caveat.** It is
   the document an operator follows during a real run, so it was the worst remaining place for the
   10 m assumption to survive unqualified.
3. **The oversampling consequence was unrecorded.** C19 established the ground span but not what it
   implies about independent support.

## The new finding

The native sampling of B4 and B8 is 10 m. A ~6.8 m analysis grid is therefore about **1.47x finer
than the data supports**, and the bilinear reprojection creates no new information.

| quantity | value |
|---|---|
| 50 analysis pixels | ~2,300 m² of ground |
| native-10 m pixel **areas** in that footprint | ~23 |
| native-20 m pixel **areas** (B11, used by BSI) | ~5.75 |
| grid spacing versus native 10 m sampling | ~1.47x finer |

**Corrected 2026-09-25: these are area equivalents, not independent sample counts.** An earlier
draft of this entry said the threshold "counts roughly twice as many pixels as there are independent
samples beneath it". Dividing ground area by native pixel area establishes neither the number of
overlapping native pixels nor an effective sample size — footprint shape, grid alignment,
interpolation, sensor spatial response and spatial covariance all bear on that and none is
determined here. `min_component_pixels` is a **geometric selection rule, not a statistical
sample-size requirement**. The oversampling caution stands; the statistical inference does not.

Overstatement from a 10 m assumption also differs by dimension: about **47% for a linear distance**
at 47.3° N, about **117% for an area**. One percentage does not apply to every metre figure.

## How the design change was made

As a **dated amendment at the top of `design.md`**, not a silent edit, per the critique's own rule
that a necessary correction needs a dated amendment and a statement of which predictions have
already been seen. That statement is: **none.** No Earth Engine run has occurred, no site is
verified, and no gate result exists, so this cannot be a post-hoc adjustment to an observed outcome.
The pre-registered gate stands exactly as frozen on 2026-08-23; only the description of the grid's
units changed.

## Deliberately not changed
The critique handoff remains a raw `.txt`. The earlier weekly handoff was converted to a committed
plan because it was a *plan* being superseded; this one is a dated audit record, which is the same
kind of artifact as an evidence file, so it keeps its original form.

## Checks observed
`pytest analysis/tests -q` **131 passed** (129 + 2 new) · both Node checks · worksheet check ·
presentation checks with 78 links and no issues · new in-document anchor resolves ·
`git diff --check` clean · all six `verified` flags remain `false`; CR-08 unchanged.
