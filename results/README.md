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



## `extractor_stress_cases.json` — where the extractor detects, misses, fabricates, or misrepresents (CR-R03 / CR-R03b, 2026-09-12)

Ten fixed synthetic cases (`analysis/catanroads/stress_cases.py`), each with its own truth mask, scored on **two layers that must not be confused**: the *component* layer (pixel recall/precision of the extractor's internal mask, within 2 px) and the *exported-line* layer (recall/precision of the straight segment the extractor actually delivers as `endpoints_px`). Regenerate with `python -m catanroads.stress_cases`; `tests/test_stress_cases.py` pins the observed behaviour. `extractor_stress_cases_baseline_2026-09-12.json` is the first, component-only record, kept byte-unchanged as the baseline. **Synthetic constructions only — nothing here is imagery or a site result.**

| case | cands | false | component recall | exported-line recall / precision |
|---|---:|---:|---:|---:|
| demo_reference | 6 | 0 | 0.92 | 0.35 / 0.47 |
| faint_corridor | 7 | 0 | 0.93 | 0.92 / 1.00 |
| wide_corridor | 1 | 0 | 1.00 | 0.38 / 1.00 |
| crossing | 0 | 0 | 0.00 | 0.00 / — |
| short_segments | 0 | 0 | 0.00 | 0.00 / — |
| linear_confound_riverbank | 1 | 1 | — | — / 0.00 |
| speckle_only | 0 | 0 | — | — / — |
| low_snr | 1 | 0 | 1.00 | 0.10 / 0.14 |
| gradient_background | 3 | 2 | 1.00 | 1.00 / 0.90 |
| tight_curve | 1 | 0 | 1.00 | 0.27 / 0.40 |

**Two corrections to the first record (review 2026-09-12).** (1) The component score is blind to the exported geometry: replacing every candidate's endpoints with an obviously wrong segment leaves it unchanged. The line layer is not — the same substitution drops wide-corridor line recall from 0.38 to 0.02. (2) The earlier "53 px width under 3× noise" was wrong: `width_px` is the component's minor-axis *extent*, and for the curved corridor it is 54.7 px with **zero** noise (the curve's transverse extent), against a 3 px road. The quantity confuses curve extent with road width.

What the line layer shows that the component layer hid: every **curved** corridor — the demo scene included — passes the component layer and **fails** the exported line (low-SNR curve 0.10, hairpin 0.27, demo 0.35), because a single straight chord cannot represent a curve. Straight corridors pass both. The wide corridor's line recall of 0.38 is a metric artifact (a 13 px thick truth vs a 2 px tolerance around a centre line), stated so it is not read as a miss.

For CR-09 and what to fix next: the **representation** (one straight segment per component) and its evaluation, not the threshold. Misses at crossings and dashes, and the river-bank false candidate, are unchanged from the baseline.
