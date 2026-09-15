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



## `extractor_stress_cases.json` — where the extractor detects, misses, fabricates, or misrepresents (CR-R03 → R03c → CR-09, 2026-09-15)

Ten fixed synthetic cases (`analysis/catanroads/stress_cases.py`), each with a road-area truth mask **and a 1-px reference centerline**, scored on two layers that must not be confused: the *component* layer (the extractor's internal mask vs the road-area truth, within 2 px) and the *exported-line* layer (the polyline the extractor delivers as `path_px` **vs the reference centerline**, within 2 px). `area_coverage` — how much of the road-area mask the exported band covers — is reported as a separate diagnostic and never enters `line_ok`. Regenerate with `python -m catanroads.stress_cases`; `tests/test_stress_cases.py` pins the observed behaviour. `extractor_stress_cases_baseline_2026-09-12.json` is the v1 component-only record, kept byte-unchanged. **Synthetic constructions only — nothing here is imagery or a site result.**

| case | cands | false | component recall | exported-line recall / precision (vs centerline) | area coverage |
|---|---:|---:|---:|---:|---:|
| demo_reference | 6 | 0 | 0.92 | 0.94 / 1.00 | 0.89 |
| faint_corridor | 7 | 0 | 0.93 | 0.91 / 1.00 | 0.90 |
| wide_corridor | 1 | 0 | 1.00 | 1.00 / 1.00 | 0.38 |
| crossing | 0 | 0 | 0.00 | 0.00 / — | 0.00 |
| short_segments | 0 | 0 | 0.00 | 0.00 / — | 0.00 |
| linear_confound_riverbank | 1 | 1 | — | — / 0.00 | — |
| speckle_only | 0 | 0 | — | — / — | — |
| low_snr | 1 | 0 | 1.00 | 1.00 / 1.00 | 1.00 |
| gradient_background | 3 | 2 | 1.00 | 1.00 / 0.90 | 1.00 |
| tight_curve | 1 | 0 | 1.00 | 0.97 / 1.00 | 0.99 |

**Four records.** (v1) component layer only. (v2) the component score is blind to the exported geometry, so a line layer was added; `width_px` is the component's minor-axis *extent*, 54.7 px for the curved corridor at zero noise. (v3) the line layer is scored against the reference centerline, not the road-area mask, so a perfect centerline scores 1.0 regardless of road width. (v4, CR-09) the exported geometry is `path_px`, a centred polyline along the component's medial axis, instead of the straight `endpoints_px` chord; the chord stays as a summary field. Before v4 every **curved** corridor passed the component layer and failed the exported line (0.11 / 0.25 / 0.44); with `path_px` all three pass. Component-layer numbers are identical across all four records.

What still fails, by construction: crossings and dashes are missed (elongation and minimum-length filters); the river-bank confound is fabricated. Those are the extractor's remaining limits, recorded in [the CR-09 evidence](../evidence/task-2026-09-15/README.md).
