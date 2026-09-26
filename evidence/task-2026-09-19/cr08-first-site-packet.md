# CR-08 — first-site inspection packet

Prepared 2026-09-21 (week plan Day 3). **Nothing here inspects imagery, changes a site, or closes
CR-08.** It is the form and the preflight checklist so that one dated judgment, when it exists, can
be applied as a reviewable diff. Authority for site fields stays
[config/sites.geojson](../../config/sites.geojson); procedure stays
[COMPLETION_RECONCILIATION.md](../../docs/COMPLETION_RECONCILIATION.md) and
[SITE_VERIFICATION_WORKSHEET.md](../../docs/SITE_VERIFICATION_WORKSHEET.md).

Evidence categories may not substitute for one another (audit guidance 2026-09-21, section 5): a
proposed setting is not synthetic truth, synthetic truth is not a dated image judgment, and a dated
image judgment is not an Earth Engine export. Each is recorded separately and an unresolved one
stays unresolved.

## Proposed inspection order — a proposal, not a manifest change

1. **`dev-01-braided`** (development; primary positive). Its expected feature is the most
   distinctive of the six — a wide braided corridor with multiple parallel ruts — so it offers the
   best chance of a *confident* judgment, and confident is what matters for the first one. A
   rejection or an uncertain result here is the most informative early signal the project can get,
   because the positive arm rests on it.
2. **`negative-01`** (negative control; falsification gate). Requires inspecting the full registered
   AOI rather than its centre, and records what portion could actually be assessed.

Alternative order, equally defensible: `negative-01` first, on the principle that the falsification
control should be established before any positive. The owner picks; neither order changes a
coordinate, a role or a stratum. **Do not choose a site because its gate output was convenient**,
and do not open the holdout.

## Judgment form — one per site, copy and fill

```
site_id:
role / stratum:
inspector (actual person):
inspection date:
imagery provider:
scene or view identifier / authorized access reference:
image acquisition date(s):            # the scene date, NOT an access or copyright year
inspected extent and scale/resolution:
obscured or unassessable area:
expected feature judgment:            # confirmed / rejected / uncertain
counter-evidence and confounds seen:  # see the confound checklist below
second dated observation (recovery claims only):
source screenshot / image reference (only if redistribution is authorized):
supports verified = true:              # yes / no
supports ref_imagery_date:             # yes / no
supports provenance:                   # yes / no
reviewer notes:
```

Rules that do not bend: an AI-assisted read is labelled as such and is not an independent human
judgment; a basemap of unknown date is not a dated scene; a blank or partially filled form is not
evidence; `verified=true` is never set to unblock software.

## Confound checklist — what to rule out, and why each is on the list

Extended 2026-09-22 from the [literature review](../../literature/claim-ledger.md#c16--a-river-bank-shaped-feature-is-returned-as-the-strongest-candidate).
The first four were already in the worksheet. The last three are **new**: the extractor's own stress
tests and the literature both say they are the classes a geometry-driven detector cannot separate
from a road, and none of them was in this project's confound stratum.

Tick each as *present / absent / cannot tell* inside the inspected extent. "Cannot tell" is a valid
and useful answer; a blank is not.

| # | confound | why it is on the list |
|---|---|---|
| 1 | agriculture or field boundaries | original worksheet stratum |
| 2 | riverbed or seasonal watercourse | original worksheet stratum |
| 3 | shadow, cloud, or a mosaic seam | original worksheet stratum |
| 4 | settlement expansion | original worksheet stratum |
| 5 | **dry drainage channel / wadi** | Liu 2016 extracts desert wadis and finds commission errors occur mainly in features falsely enhanced by water indices — **specifically roads**. The confusion is documented in the mirror direction, in arid terrain, at moderate resolution. |
| 6 | **fence line** | Buzzard 2022 measures ~0.93 km of fence per km² (max 14.9) in comparable grazing country, and built its fence model partly *from* road layers. At that density a fence is a pervasive background linear signal, not a rare confound. Løvschal 2022 shows fencing proliferating in similar pastoral rangeland. |
| 7 | **animal path / livestock trail** | Chemura 2024 mapped off-road tracks and animal paths together in open rangeland and found they **co-occur at r = 0.75**, needing a separate explicit classification stage even at 50 cm. |

Queiroz 2020 states plainly that roads, pipelines, seismic lines and power lines are one detectable
class for geometry-driven linear extractors, and Nagel 2024 finds that at Sentinel-2 resolution a
deep model cannot separate road from seismic line. **Geometry alone cannot decide roadness.** That
is the whole reason this inspection exists, and why items 5 to 7 must be recorded even when the
expected feature is confirmed — a site can contain both.

## What happens to each outcome

## If the site is `dev-02-recovering`: name the variable and carry a range

The registered recovering-corridor role asks whether a track is recovering. The literature does not
support a single answer, because the available studies measure **different variables**:

| source | system | variable measured | time to recovery |
|---|---|---|---|
| Kinugasa 2015 | Mongolian steppe | cover and biomass | ~4 years |
| Keshkamat 2012 | Mongolia | full revegetation of the swath | 10–15 years |
| Jorgenson 2010 | Arctic tundra | severe-impact trails | 2 decades and beyond |
| Webb 2002 | Mojave Desert | soil compaction | 80–130 years |

Two consequences for the judgment form. First, **state which variable you judged** — greenness,
species composition, visible rutting, or surface brightness — because "recovered" means a different
thing for each, and Li 2006 shows early steppe recovery is a *compositional* change (pioneer species
colonising the compacted surface) rather than a return to background greenness. Second, **carry the
range, never a point estimate**; Jorgenson 2010 shows recovery time depends strongly on initial
severity and substrate, and Kinugasa & Oda 2014 found track formation removed 8.3–9.4 cm of soil and
the seed bank with it, so recovery is not simple regrowth.

Independent of any judgment here: the Phase-1 screen computes **positive** disturbance and is not a
recovery detector. That mismatch is recorded in `docs/design.md` and is not resolved by this
inspection.

| outcome | action |
|---|---|
| confirmed | minimal reviewable diff to `config/sites.geojson`; regenerate the worksheet; mirror the approved fields into `gee/ndvi_change.js`; re-run `node tools/validate_phase1.mjs` and `python -m catanroads.site_worksheet --check`. Any superseded coordinate is retained in evidence, never silently replaced. |
| rejected | manifest unchanged; the rejection and its counter-evidence are recorded; CR-08 stays blocked. |
| uncertain / inaccessible | manifest unchanged; the exact access limitation is recorded so the next attempt starts from it; CR-08 stays blocked. |

## Export preflight checklist — for the eventual four CSVs

Run against the existing gate in `analysis/catanroads/phase1_gate.py` and the contract in
[PHASE1_RUNBOOK.md](../../docs/PHASE1_RUNBOOK.md). **No second gate and no different thresholds.**

- [ ] exactly four rows: `dev-01-braided`, `dev-02-recovering`, `dev-03-gobi`, `negative-01`
- [ ] no holdout row present
- [ ] `reference_imagery_date` and `site_provenance` equal the manifest for each site
- [ ] `center_lat`, `center_lon`, `half_km` equal the manifest for each site
- [ ] `large_component_fraction` and `coverage_fraction` finite and within [0, 1]
- [ ] `coverage_fraction` >= 0.90 for every compared site
- [ ] component fraction does not exceed analyzable coverage
- [ ] every frozen setting matches: early/recent years, CRS, scale, control radii, min control
      pixels, month, `z_min`, yearly effect floor, persistence, min valid recent years,
      min component pixels
- [ ] all eight `s2_scene_count_<year>` columns present, non-negative integers
- [ ] at least one early year has scenes; at least two recent years have scenes
- [ ] zero-scene years retained as zero, never dropped or back-filled
- [ ] CSV headers non-empty and non-duplicated; no row narrower or wider than the header
- [ ] each export file hashed, with its Earth Engine task id, terminal task state and access
      reference recorded — a successful launch is not a completed export (guidance section 4)

Verified behaviour of the existing CLI, rehearsed 2026-09-21 against controlled synthetic and
missing inputs (no Earth Engine run):

| input | exit | status | traceback |
|---|---:|---|---|
| synthetic, well-formed | 3 | DEVELOPMENT_ONLY | no |
| export-labelled, well-formed | 0 | SCREEN_PASS | no |
| export-labelled, all development sites below the floor | 1 | SCREEN_FAIL | no |
| the committed unverified manifest, well-formed metrics | 2 | INCONCLUSIVE | no |
| missing export file | 2 | INCONCLUSIVE | no |

A SCREEN_PASS is the registered large-component positive-disturbance screen. It is not road
precision or recall, not recovery detection, and not source authentication.

---

# Response design addendum — 2026-09-25

**Status: RESPONSE_DESIGN_COMPLETE. Real judgments remain PENDING until actually received.**
This completes the design. It verifies nothing, and no owner decision was required to draft it.

## Preparation order (provisional, not an owner-approved scientific decision)

**`dev-01-braided` first, then `negative-01`.** The first tests whether the primary corridor example
is interpretable at all; the second needs adequate coverage of the *full* AOI, because a positive
chip cannot verify a whole negative-control area. Both are interpreted **before** screen
predictions. `holdout-01` stays uninspected.

Changing this order changes no site, stratum, coordinate or gate threshold, so it is not held up
waiting for confirmation. The owner can override it when supplying evidence.

## What each judgment must carry

| field | rule |
|---|---|
| dated source and scene identifier | the acquisition date, never an access or copyright year |
| authorization / access reference | a reference, never a credential in this repository |
| inspected extent, scale/resolution | plus the portion that could **not** be assessed |
| obscuration | cloud, shadow, seasonal cover, mosaic seam |
| actual inspector | a person; an AI-assisted read is labelled as such and is not independent |
| judgment | confirmed / rejected / uncertain, **plus an explicit `unknown` class** |
| confounds | the seven-item checklist above, each present / absent / cannot tell |

`unknown` is distinct from `uncertain`: *uncertain* means the imagery was seen and did not settle
the question; *unknown* means the question was not reached. Both are recorded outcomes. Neither is
ever rewritten as `verified` to meet a deadline.

## If recovery is claimed

Name the **variable** judged — greenness, species composition, visible rutting or surface
brightness — and supply **paired dated evidence**. A single contemporary image cannot establish
historical change or abandonment. Carry the range from the four-study spread above rather than a
point estimate.

## Later candidate-review pilot (specified now, executed when eligible)

- A **fixed inspection budget** and a **deterministic candidate selection rule**, both frozen before
  any prediction is read.
- Report **confirmed corridors / reviewed candidates**, with uncertain judgments counted separately,
  duplicate reviews recorded, and reviewer minutes per confirmation.
- This is **triage yield, not precision or recall**.
- For any eventual recall estimate, separately inspect **fully covered areas containing no
  predictions**. Reviewing candidates alone cannot estimate recall.
- Retain a small **blind repeat / adjudication subset**.

## What one image does and does not do

A single accepted judgment updates **only its own evidence-supported fields** through the established
review path. It does not imply the other sites are verified, and it does not make the four-site
screen runnable. CR-08's ledger row asks for development and control verification **and** Earth
Engine runtime access; those remain separately visible and separately unmet.
