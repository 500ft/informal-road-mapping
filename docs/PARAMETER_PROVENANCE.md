# Parameter provenance, audit and traceability index

Prepared 2026-09-25. **This is a documentation audit. It changes no value, threshold, site or gate,
and it does not validate the detector.** Its purpose is that a reader can tell, for every
consequential number, whether it was imposed, measured, derived, chosen, or merely inherited.

The framework is adapted from a mechanical-design provenance prompt. The mechanical sections there
(grip force, flexures, fasteners, servo torque) have no counterpart here and are not transplanted.
What carries over is the part that matters: **an existing choice is not a justified choice**, and
prediction is never validation.

## The headline audit finding

Most of this project's consequential numbers are **selected design values, frozen by
pre-registration on 2026-08-23, whose selection rationale was never recorded.**

That is not the same as being arbitrary, and pre-registration is a real methodological strength: the
values were fixed before any result was seen, which is what stops them being tuned afterwards. But
freezing a number records *when* it was chosen, not *why*. Searching the repository for a derivation
of `Z_MIN`, `PERSISTENCE_MIN`, `MIN_COMPONENT_PIXELS`, `YEARLY_EFFECT_MIN`, `CONTROL_INNER_M`,
`MIN_CONTROL_PIXELS` or `GATE_RATIO_MIN` returns **no rationale-bearing text for any of them**.
`docs/design.md` states the values and lists sensitivity alternatives; it does not say why the
primary was preferred.

Three exceptions, and one important caveat about them:

| quantity | what exists | kind |
|---|---|---|
| `GATE_ABSOLUTE_FLOOR` | design.md explains it prevents a zero negative-control response producing an infinite ratio | **original rationale** |
| `MIN_COMPONENT_PIXELS` | C19's ground-area analysis (~2,300 m², not 5,000) | **retrospective assessment** |
| `PERSISTENCE_MIN` with `MIN_VALID_RECENT_YEARS` | the 176-pair enumeration of decision behaviour | **retrospective assessment** |
| `tol_px` | identified as a Wiedemann-family buffer metric by the literature review | **retrospective assessment** |

**A retrospective assessment cannot establish the original designer's reasoning.** It can say whether
a value is defensible now. Nothing in this document should be read as recovering intent.

## Provenance categories used here

| category | meaning |
|---|---|
| **requirement** | imposed target or external constraint |
| **measured input** | a quantity someone measured |
| **sourced assumption** | taken from a cited external source, with its applicability limits |
| **calculated result** | derived from other quantities by a stated model |
| **selected design value** | chosen by the designer; may or may not have a recorded basis |
| **measured result** | an outcome observed from a real run |
| **provisional estimate** | placeholder, explicitly awaiting evidence |

**Evidence status is tracked separately from provenance**, because a selected value can be
unverified, analytically assessed, or physically tested, and those are three different things.

| status | meaning |
|---|---|
| `FROZEN_UNDERIVED` | pre-registered, no recorded derivation |
| `RETRO_ASSESSED` | assessed after the fact by analysis; original intent not recovered |
| `MODEL_CHECKED` | behaviour characterised by an arithmetic model, not by execution |
| `SYNTHETIC_ONLY` | exercised only on constructions with known truth |
| `UNVERIFIED` | no analysis and no measurement |
| `REAL_MEASURED` | observed from real data — **nothing in this repository holds this status** |

## Canonical register

One definition per quantity. Values are asserted against source by
`analysis/tests/test_parameter_register.py`, so a drift between this table and the code fails a test
rather than rotting silently. Units are stated because several are not what their name implies.

### Phase-1 screen — `gee/ndvi_change.js`, mirrored in `phase1_gate.py::CONFIG`

| quantity | value | units | provenance | status | note |
|---|---|---|---|---|---|
| `MONTH` | 7 | month index | selected design value | FROZEN_UNDERIVED | same-season comparison; why July specifically is unrecorded |
| `ANALYSIS_SCALE_M` | 10 | **nominal projected**, not ground | selected design value | RETRO_ASSESSED | ~6.6–7.0 m ground at site latitudes — see [C19](../literature/claim-ledger.md) |
| `CONTROL_INNER_M` | 200 | m (kernel-specified) | selected design value | FROZEN_UNDERIVED | whether the kernel carries the grid's distortion is **untested** |
| `CONTROL_OUTER_M` | 800 | m (kernel-specified) | selected design value | FROZEN_UNDERIVED | alternatives 100–600 and 300–1000 listed as sensitivity, not as derivation |
| `MIN_CONTROL_PIXELS` | 500 | pixels | selected design value | UNVERIFIED | no recorded basis |
| `Z_MIN` | 1.0 | standard deviations | selected design value | FROZEN_UNDERIVED | one sigma; no recorded false-positive reasoning |
| `YEARLY_EFFECT_MIN` | 0.02 | index units | selected design value | FROZEN_UNDERIVED | **strict `>`**; source comment lists 0.01/0.03 as sensitivity |
| `PERSISTENCE_MIN` | 2/3 | fraction | selected design value | MODEL_CHECKED | decision behaviour enumerated over 176 cases |
| `MIN_VALID_RECENT_YEARS` | 2 | years | selected design value | MODEL_CHECKED | minimum passing counts are 2/2, 2/3, 3/4 |
| `MIN_COMPONENT_PIXELS` | 50 | pixels | selected design value | RETRO_ASSESSED | ≈2,300 m² ground, not the 5,000 implied by a 10 m assumption |
| `MAX_CONNECTED_PIXELS` | 256 | pixels | selected design value | RETRO_ASSESSED | `connectedPixelCount` **caps** the count here; harmless at `MIN_COMPONENT_PIXELS = 50`, but a threshold at or above this cap silently yields no components. Coupling now enforced by `tools/validate_phase1.mjs` |
| `GATE_RATIO_MIN` | 2.0 | ratio | selected design value | FROZEN_UNDERIVED | the "2× rule"; why 2 and not 1.5 or 3 is unrecorded |
| `GATE_ABSOLUTE_FLOOR` | 0.0001 | fraction | calculated result | **recorded rationale** | prevents a zero negative response giving an infinite ratio |
| `GATE_MIN_DEVELOPMENT_SITES` | 2 | sites | requirement | FROZEN_UNDERIVED | two of three |
| `GATE_MIN_COVERAGE` | 0.90 | fraction | requirement | FROZEN_UNDERIVED | admission threshold |
| early / recent windows | 2018–2021 / 2023–2026 | years | selected design value | FROZEN_UNDERIVED | 2022 buffer; buffer width unrecorded |

### Phase-2 extractor — `analysis/catanroads/extract.py`

| quantity | value | units | provenance | status | note |
|---|---|---|---|---|---|
| `disturb_thresh` | 1.0 | z units | selected design value | SYNTHETIC_ONLY | mirrors `Z_MIN`; static validator enforces the match |
| `ridge_sigmas` | (1, 2, 3) | **pixels** | selected design value | UNVERIFIED | ~6.8–20 m ground; measured Mongolian corridors span ~26–164 m. **No documented link to any measured width** |
| `ridge_quantile` | 0.85 | quantile | selected design value | UNVERIFIED | no recorded basis |
| `min_length_px` | 12 | pixels | selected design value | SYNTHETIC_ONLY | a dashed track of 9-px segments is lost by construction |
| `min_elongation` | 3.0 | ratio | selected design value | SYNTHETIC_ONLY | rejects the crossing case's union component |
| `tol_px` | 2 | pixels, **L1 band** | selected design value | RETRO_ASSESSED | two 4-neighbour dilations, not a Euclidean disk; Wiedemann-family buffer |
| `line_ok` cut | 0.5 | recall and precision | selected design value | SYNTHETIC_ONLY | deliberately coarse |
| A2 / A3 targets | 0.80 / 0.98 | recall and precision | requirement | SYNTHETIC_ONLY | frozen before CR-09 ran; software acceptance, not scientific preregistration |

### Site manifest — `config/sites.geojson`

| quantity | value | provenance | status |
|---|---|---|---|
| `half_km` (all six sites) | 8 | selected design value | FROZEN_UNDERIVED |
| site coordinates | six positions | **provisional estimate** | UNVERIFIED — every `verified` flag is `false` |
| `ref_imagery_date`, `provenance` | unset | provisional estimate | UNVERIFIED |

## Audit table — what is weakly supported, and what to do

Ordered by consequence, not by how easy it is to fix.

| # | decision | evidence today | what is missing | consequence if wrong | action |
|---|---|---|---|---|---|
| 1 | **All six site coordinates** | starting guesses | any dated image judgment | the entire screen runs on unverified locations; a SCREEN_PASS would mean nothing | CR-08; packet and response design are ready |
| 2 | **`ridge_sigmas` = (1,2,3) px** | none | a link to measured corridor widths; the published range is ~26–164 m against a ~7–20 m filter band | corridors may be enhanced weakly or not at all, and the failure would look like absence of roads | measure a detectability envelope over width before trusting any negative result |
| 3 | **`Z_MIN` = 1.0** | none | a false-positive rate at this threshold on any real scene | one sigma over a local ring is permissive; commission may dominate | record commission on the negative control before interpreting any development site |
| 4 | **`CONTROL_INNER_M` / `OUTER_M`** | none; kernel distortion untested | whether the metre-specified kernel matches the pixel grid's distortion | the normalisation ring may not be the size it claims | covered by the prepared grid probe |
| 5 | **`MIN_CONTROL_PIXELS` = 500** | none | a basis for the number | too few samples makes the z-score unstable; too many rejects valid sites | derive from the ring area at the real ground scale |
| 6 | **`MAX_CONNECTED_PIXELS` = 256** | ~~none~~ **resolved 2026-09-26** | the value's *origin* is still unrecorded | a component threshold at or above the cap would silently yield nothing | **done**: it is `connectedPixelCount`'s `maxSize`; documented at its definition and the coupling to `MIN_COMPONENT_PIXELS` is now enforced by the static validator |
| 7 | **`GATE_RATIO_MIN` = 2.0** | the floor companion is explained; the ratio is not | why 2 | the primary gate's strictness is unjustified | state the reasoning, or record it as a convention |
| 8 | **`min_length_px`, `min_elongation`** | synthetic cases pin their effects | real-corridor equivalents | dashes and crossings are lost by construction | already recorded as known limits |
| 9 | **`tol_px` = 2 as an L1 band** | Wiedemann family identified | any analysis of buffer width sensitivity, or of the redundancy the band permits | scores may be optimistic in a way the metric cannot see | literature found none; treat as open |
| 10 | **July-only compositing** | none | why July, and what phenology it assumes | a seasonal choice acts as an uncontrolled variable | record the reasoning |

## Resolved finding — `MAX_CONNECTED_PIXELS`, 2026-09-26

Audit item 6 asked what this constant was for, because it appeared nowhere in the documentation.
Reading the code path answers it: it is the `maxSize` argument to Earth Engine's
`connectedPixelCount(maxSize, eightConnected)`, which **caps** the returned count. A component
larger than 256 pixels reports exactly 256, not its true size.

**Current effect: none.** The test is `connectedCount >= MIN_COMPONENT_PIXELS` with the threshold at
50, and `min(trueSize, 256) >= 50` whenever `trueSize >= 50`. The planned sensitivity values are
`{25, 50, 100}` pixels, all below the cap, so this would not have bitten on the registered plan
either. **This is a latent hazard that was guarded before it could fire, not a bug that was about to.**

**Why it still matters.** The coupling is invisible in either constant alone. Raise the component
threshold to or above 256 — during a future sensitivity study, or by someone reasoning in ground
area after C19 showed 50 pixels is only ~2,300 m² — and the gate silently returns *no* large
components rather than erroring. A silent empty result on a screen whose whole purpose is detecting
absence-versus-presence is the worst failure shape available.

Two things are now true that were not: the constant explains itself where it is defined, and
`tools/validate_phase1.mjs` asserts `MAX_CONNECTED_PIXELS > MIN_COMPONENT_PIXELS`. Verified by
temporarily raising the threshold to 300 and confirming the validator fails.

The counts are also unusable as component **sizes** above the cap. Only the threshold test is valid,
which matters if anyone later reports component size as a result.

**Still unrecorded:** why 256 specifically. That remains `FROZEN_UNDERIVED` like its neighbours.

## Traceability index

Decision → where its rationale lives → what would validate it → status. **Equations are not
duplicated here**; this is navigation only.

| decision | rationale location | validation route | status |
|---|---|---|---|
| Screen on positive disturbance, not recovery | [design.md](design.md) boundary section | paired dated imagery | open; sign mismatch recorded |
| Target corridors, not single tracks | [design.md](design.md) decision 1 + [C1](../literature/claim-ledger.md) | detectability envelope over width | **minimum detectable width unmeasured** |
| Analysis grid and its physical meaning | [design.md 2026-09-24 amendment](design.md) + [C19](../literature/claim-ledger.md) | [prepared grid probe](../evidence/task-2026-09-25/grid_runtime_probe.js) | PREPARED_UNEXECUTED |
| Persistence rule and minimum valid years | [enumeration](../evidence/task-2026-09-25/missingness_sensitivity.json) | real per-pixel clear-observation counts | MODEL_CHECKED |
| Compositing order for NDVI and BSI | [compositor protocol](specs/compositor-ab/plan.md) | A/B on real imagery | OFFLINE_COMPLETE |
| Ridge filter family and its scale range | [C12](../literature/claim-ledger.md) | stage-by-stage crossing trace | **suspected, unattributed** |
| One path per component | [topology note](specs/phase-2-topology-followup/plan.md) | confirmation task that needs junctions | deferred, Option C |
| Line-layer scoring and its tolerance | [C17](../literature/claim-ledger.md) · [results guide](../results/README.md) | second metric on a labelled graph | SYNTHETIC_ONLY |
| Negative control as falsification gate | [design.md](design.md) + [C18](../literature/claim-ledger.md) | the gate run on real exports | blocked on CR-08 |
| Site selection and verification | [CR-08 packet](../evidence/task-2026-09-19/cr08-first-site-packet.md) | one dated image judgment | RESPONSE_DESIGN_COMPLETE, inputs pending |

## What this audit does not claim

It does not validate the detector, recover any original design intent, or convert a frozen value
into a justified one. No number changed. **Nothing in this repository holds `REAL_MEASURED`
status**, because no real run has occurred.
