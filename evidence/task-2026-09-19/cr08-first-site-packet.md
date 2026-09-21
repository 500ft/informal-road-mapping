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
counter-evidence and confounds seen:  # agriculture, riverbed, shadow, cloud, mosaic seam
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

## What happens to each outcome

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
