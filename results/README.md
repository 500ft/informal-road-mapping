# Results

Exported figures and analysis outputs.

The main [`README`](../README.md) displays the synthetic method demonstration.
**`ndvi_change.png`** remains a legacy full-field-rendering placeholder in this
directory. Do not replace it with a claimed result until
the sites are verified and the pre-registered Phase-1 gate outcome is recorded.

## Workflow

1. **Verify** — freeze dated reference-imagery provenance for all three development
   sites and `negative-01` in [`../config/sites.geojson`](../config/sites.geojson).
2. **Gate** — run [`../gee/ndvi_change.js`](../gee/ndvi_change.js) at those four
   registered sites. Preserve each one-row gate-metrics CSV and apply the exact
   2× large-component-fraction rule in [`../docs/design.md`](../docs/design.md).
3. **Generate** — only after preserving the primary metrics, click the candidate
   thumbnail URL or use the raster Drive export for the figure input.
4. **Compose** — turn the raw export into a self-contained figure with a title,
   legend, scale bar, and the required attribution:

   ```bash
   python tools/compose_figure.py \
     --input path/to/gee_export.png \
     --title "Persistent candidate disturbance around <place>" \
     --years "2018-2021 -> 2023-2026" \
     --region "<region>, Mongolia" \
     --scale 10 \
     --year-attr "2018-2021, 2023-2026" \
     --output results/ndvi_change.png
   ```
5. **Report** the gate result next to the figure, including the negative-control
   metric, development-site metrics, coverage, and whether the registered rule
   passed. A failed gate is a valid result; do not replace it with a sensitivity run.

## Caption template

> **Candidate surface disturbance, `<region>`, `<early-window>` vs `<recent-window>` (July).**
> Brown marks pixels meeting the registered water-safe candidate mask (`z >= 1.0`,
> persistence `>= 2/3`, at least two valid recent years). The registered Phase-1
> gate `<passed/failed>`: `large_component_fraction=<values>` with
> `coverage_fraction=<values>`. No active/abandoned claim is made. Contains modified
> Copernicus Sentinel-2 data, processed in Google Earth Engine.

## Attribution & licensing

Sentinel-2 imagery is free and openly licensed (Copernicus). When you publish a
figure, include: *"Contains modified Copernicus Sentinel-2 data (`<years>`),
processed in Google Earth Engine."* `compose_figure.py` bakes this line in.

Do **not** commit raw imagery exports here — GeoTIFFs and archives are ignored by
`.gitignore` to keep the repo light. Keep only finished figures.



## `extractor_stress_cases.json` — where the extractor detects, misses, fabricates, or misrepresents (CR-R03 → R03c, 2026-09-13)

Ten fixed synthetic cases (`analysis/catanroads/stress_cases.py`), each with a road-area truth mask **and a 1-px reference centerline**, scored on two layers that must not be confused: the *component* layer (the extractor's internal mask vs the road-area truth, within 2 px) and the *exported-line* layer (the straight segment the extractor delivers as `endpoints_px` **vs the reference centerline**, within 2 px). `area_coverage` — how much of the road-area mask the exported band covers — is reported as a separate diagnostic and never enters `line_ok`. Regenerate with `python -m catanroads.stress_cases`; `tests/test_stress_cases.py` pins the observed behaviour. `extractor_stress_cases_baseline_2026-09-12.json` is the v1 component-only record, kept byte-unchanged. **Synthetic constructions only — nothing here is imagery or a site result.**

| case | cands | false | component recall | exported-line recall / precision (vs centerline) | area coverage |
|---|---:|---:|---:|---:|---:|
| demo_reference | 6 | 0 | 0.92 | 0.44 / 0.45 | 0.35 |
| faint_corridor | 7 | 0 | 0.93 | 0.94 / 1.00 | 0.92 |
| wide_corridor | 1 | 0 | 1.00 | 1.00 / 1.00 | 0.38 |
| crossing | 0 | 0 | 0.00 | 0.00 / — | 0.00 |
| short_segments | 0 | 0 | 0.00 | 0.00 / — | 0.00 |
| linear_confound_riverbank | 1 | 1 | — | — / 0.00 | — |
| speckle_only | 0 | 0 | — | — / — | — |
| low_snr | 1 | 0 | 1.00 | 0.11 / 0.11 | 0.10 |
| gradient_background | 3 | 2 | 1.00 | 1.00 / 0.90 | 1.00 |
| tight_curve | 1 | 0 | 1.00 | 0.25 / 0.26 | 0.27 |

**Three corrections across two reviews.** (v2) The component score is blind to the exported geometry — replacing endpoints with a wrong segment leaves it unchanged; the line layer catches it. (v2) `width_px` is the component's minor-axis *extent*: 54.7 px for the curved corridor at **zero** noise, against a 3 px road. (v3) The v2 line layer was scored against the road-**area** mask, so a perfect centerline through the 13-px straight road scored recall 0.385 — a 2-px band covers 5/13 of the area. It is now scored against the reference centerline: a perfect centerline scores 1.0 regardless of road width, a 5-px off-centre line inside the road scores 0, and the width effect is visible only as `area_coverage`.

What survives all three: every **curved** corridor — the demo included — passes the component layer and fails the exported line (0.11 / 0.25 / 0.44), because one straight chord cannot represent a curve. Straight corridors pass both. Crossings and dashes are missed; the river-bank confound is fabricated. For CR-09: the **representation** (one straight segment per component), not the threshold, is what to fix next.
