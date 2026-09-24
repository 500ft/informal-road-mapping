# Phase-1 evaluation packet — template

Prepared 2026-09-23 (week plan Day 5). **This is a blank template, not a result.** No Earth Engine
run has occurred, no site is verified, and CR-08 remains the only research gate. Filling this in is
what a real Phase-1 evaluation *is*; anything less is a preparation artifact.

Authority: [PHASE1_RUNBOOK.md](PHASE1_RUNBOOK.md) for the procedure,
[SPRINT_TASKS.csv](SPRINT_TASKS.csv) for status, `analysis/catanroads/phase1_gate.py` for the gate
itself. Do not create a second gate or a second set of thresholds.

## 0. What a SCREEN_PASS means, stated before any number is entered

A SCREEN_PASS is the registered **large-component positive-disturbance screen**. It is not road
precision, not road recall, not recovery detection, and not source authentication. Hansen 2016's
alert system is the precedent for shipping a screen that explicitly does not separate human-induced
from natural disturbance.

**Corrected 2026-09-24.** An earlier draft quoted Zhu 2020's COLD results as "the realistic error
floor" for an unsupervised screen. That transfer was unjustified: 27% omission and 28% commission
are measured results for one algorithm on the authors' Landsat evaluation against their reference
data, not a bound and not a prediction for Mongolian track candidates. Quoting them as a floor could
excuse a poor detector before it has been measured. The correct statement is: **other disturbance
screens report substantial errors, and this screen's error rates and the review burden they imply
have not yet been measured.**

## 1. Identity — fill before looking at any output

| field | value |
|---|---|
| source commit of this repository | |
| SHA-256 of `config/sites.geojson` | |
| SHA-256 of `gee/ndvi_change.js` | |
| Earth Engine script revision / asset id | |
| Earth Engine task ids, one per export | |
| terminal task state for each (a launch is **not** a completed export) | |
| operator identity and run date | |
| Sentinel-2 collection used | expected `COPERNICUS/S2_SR_HARMONIZED` |

The collection matters and is not cosmetic: the Processing Baseline 04.00 radiometric offset was
deployed 25 January 2022, which falls **between** the 2018–2021 and 2023–2026 windows. A
non-harmonized collection introduces a false step change across exactly the comparison this gate
makes. Verified present in the script on 2026-09-22.

## 2. Sites — role and verification provenance

One row per registered site. **A row may not be filled from a worksheet, a coordinate, a basemap of
unknown date, or an AI-only answer** (see [COMPLETION_RECONCILIATION.md](COMPLETION_RECONCILIATION.md)).

| site_id | stratum | `verified` | `ref_imagery_date` | provenance | inspector | confounds recorded |
|---|---|---|---|---|---|---|
| dev-01-braided | development | | | | | |
| dev-02-recovering | development | | | | | |
| dev-03-gobi | development | | | | | |
| negative-01 | negative_control | | | | | |

`holdout-01` and `confound-01` do **not** appear. A holdout row in the metrics CSV is a gate failure,
not an oversight.

## 3. Per-site exported metrics

One one-row CSV per site, four in total. Every field is checked by the existing intake; this table
is for the human reader, not a substitute for running the CLI.

| field | dev-01 | dev-02 | dev-03 | negative-01 |
|---|---|---|---|---|
| `large_component_fraction` | | | | |
| `coverage_fraction` (must be ≥ 0.90) | | | | |
| `s2_scene_count_2018` … `_2021` | | | | |
| `s2_scene_count_2023` … `_2026` | | | | |
| years with zero scenes (retained, never back-filled) | | | | |
| `n_valid` recent years (must be ≥ 2) | | | | |

Frozen settings that must match the manifest on every row, none of which may be changed for this
run: early years 2018–2021, recent years 2023–2026, CRS EPSG:3857, nominal scale 10, control ring
200–800 m, minimum 500 control pixels, month 7, `z_min` 1.0, yearly effect floor 0.02, persistence
2/3, minimum 2 valid recent years, minimum component size 50 pixels.

**Record the grid's physical meaning alongside these, do not assume it.** The CRS is Web Mercator, so
a nominal-10 pixel spans roughly **6.6–7.0 m** of ground across the registered latitudes, and the
50-pixel component threshold corresponds to about **2,200–2,500 m²** rather than 5,000 m². `BSI`
additionally draws on B11, whose native sampling is 20 m. Enter the exported affine transform,
`pixelArea` and the nominal scale here rather than converting from an assumed 10 m — see C19 in the
[claim ledger](../literature/claim-ledger.md).

## 4. Primary decision — recorded before any sensitivity run

```sh
PYTHONPATH=analysis python -m catanroads.phase1_gate \
  --sites config/sites.geojson \
  --metrics PATH_TO_DEV_01.csv PATH_TO_DEV_02.csv PATH_TO_DEV_03.csv PATH_TO_NEGATIVE_01.csv \
  --evidence-kind earth-engine-export
```

| field | value |
|---|---|
| exit code | |
| status (0 SCREEN_PASS · 1 SCREEN_FAIL · 2 INCONCLUSIVE · 3 DEVELOPMENT_ONLY) | |
| threshold applied (`max(2 × negative, 0.0001)`) | |
| passing development sites | |
| `input_sha256` block, verbatim | |

**Stop rule.** Record this result whatever it is. A SCREEN_FAIL is a valid outcome and is not a
reason to change a site, a threshold, a window or the negative control. Simmons 2011 and
Gelman & Loken 2014 are the reason: tuning after seeing which corridors light up inflates the error
rate even if only one analysis is finally reported.

## 5. Sensitivity — only after section 4 is written down

Record every run attempted, including the ones that weakened the result. State plainly that these
are development material and not an independent test.

| variation | rationale stated in advance | status | notes |
|---|---|---|---|

## 6. Exclusions and unresolved inputs

| item | why excluded or unresolved |
|---|---|

Missing dates, absent provenance, zero-scene years and uninspected sites stay unresolved here.
They are not zeros.

## 7. What this packet does not establish

- Not road precision or recall. The delivered geometry is scored separately and only on synthetic
  constructions; see [results/README.md](../results/README.md).
- Not recovery. The mask is positive disturbance; a recovering corridor has the opposite sign.
- Not an area estimate. Olofsson 2014 requires a probability sample and an error-adjusted area with
  a confidence interval before any extent figure is quoted; a count of components is not that.
- Not generalisation. Ploton 2020 shows in-site scores can be near-meaningless out-of-site, and
  Wadoux 2021 that a held-out site is a generalisation test rather than an unbiased accuracy
  estimate.
