# Design — Catan Roads

## Amendment — 2026-09-24 — the analysis grid's units

**Nothing about the frozen gate changes here. This corrects how two sentences in this document
describe the grid; no threshold, site, window or setting is altered.**

The screen runs on `EPSG:3857` at `ANALYSIS_SCALE_M = 10`. Web Mercator's linear scale factor is
1/cos(latitude), so a nominal-10 pixel spans roughly **6.6–7.0 m of ground** across the registered
site latitudes — not 10 m. This document previously called it "a fixed 10 m grid", which conflates
nominal projected units with ground distance. Two consequences follow, both recorded as claim C19 in
[the literature claim ledger](../literature/claim-ledger.md) and pinned by
`analysis/tests/test_support_and_compositing.py`:

- The `min_component_pixels = 50` threshold corresponds to about **2,300 m²** of ground, not the
  5,000 m² a 10 m assumption implies. Overstatement differs by dimension: about **47% for linear
  distance**, about **117% for area**.
- Because the native sampling of B4 and B8 is 10 m, the analysis grid's **spacing is about 1.47×
  finer than native 10 m sampling**. Reprojection here does not add measurements: an estimated
  2,300 m² is about **23 native-10 m pixel areas**, or **5.75 native-20 m pixel areas** for the
  shortwave band BSI uses. **These are area equivalents, not independent sample counts** — that
  division establishes neither overlapping-pixel counts nor an effective sample size, and
  `min_component_pixels` is a geometric selection rule, not a statistical sample-size requirement.

**Which predictions have been seen: none.** No Earth Engine run has occurred, no site is verified,
and no gate result exists. This amendment therefore cannot be a post-hoc adjustment to an observed
outcome. It is a correction of a measurement description, made before any prediction, and the
pre-registered gate stands exactly as frozen on 2026-08-23.

These are independently calculated estimates under the spherical approximation, **not** measurements
of an exported raster. The exact ellipsoidal geometry, the delivered affine transform, and whether
the metre-specified 200–800 m control ring carries the same distortion as the pixel grid all remain
untested and require Earth Engine access.

## Current implementation boundary — 2026-09-06

The Phase-1 GEE mask selects positive disturbance, not signed recovery. A
recovering track generally has the opposite sign and an unchanged track may be
invisible. The registered dev-02-recovering role therefore does not establish
recovery detection via a positive gate. Do not swap sites, reverse its sign or
retune thresholds after predictions; any recovery endpoint needs a separately
recorded prospective amendment.

The new [intake runbook](PHASE1_RUNBOOK.md) requires verified references and
matching CSV settings before the fixed two-of-three screen can pass. All current
sites remain unverified. Passing large-component fractions would justify the
next investigation, not road classification or network-conditioned performance.
The remainder describes intended research, not accomplished end-to-end behavior.

This document is the **technical design** for the project — the full methodology
that the current early-stage tooling (see the README) is built toward. It is
deliberately explicit about where the hard problems and the unproven assumptions
are, so that results are never claimed beyond what the method supports.

> **Operative framing (2026 review).** This is *not* an NDVI road classifier. It
> is a **network-conditioned method for finding persistent surface-disturbance
> corridors that may represent unmapped informal roads**, whose deliverable is a
> **prioritized candidate list for higher-resolution confirmation**. That framing
> matches Sentinel-2's limits (a 2.5–3 m track is below the 10 m native sampling of B4/B8; see the
> [2026-09-24 amendment](#amendment--2026-09-24--the-analysis-grids-units) for why that is not the
> same as the analysis grid's spacing) and keeps the
> project scientifically defensible. The sections below record the original vision;
> the **[Developed execution plan](#developed-execution-plan-phase-04)** at the end
> supersedes the earlier "experiment structure" and is what the code is built to.

## Refined problem definition

> Detect active informal roads and abandoned tracks in Mongolia by analyzing
> multi-year satellite imagery around known mapped road intersections, then
> tracing previously unmapped branches using changes in vegetation cover,
> apparent road width, surface disturbance, continuity, terrain feasibility, and
> surrounding road-network structure.

The system is not searching the country blindly. It uses mapped intersections as
seed nodes, searches outward within a radius, detects candidate unmapped
branches, follows them, and flags a **candidate** activity state over time. (Per
the reframe above, "active/abandoned" is a post-validation goal, not a claim the
current method makes — public wording stays "candidate disturbance/recovery.")

## System logic

### 1. Seed-node generation

Start from a mapped road graph `G_m = (V_m, E_m)` where `V_m` are intersections
and endpoints and `E_m` are segments. Not every point where two polylines touch
is a useful seed — distinguish true intersections, endpoints, forks,
grade-separated crossings, and mapping artifacts, and **prioritize rural forks,
endpoints, and low-degree nodes**.

For each node `v_i`, search a region `Ω_i = { p : |p − v_i| ≤ r_i }`. The radius
should not be a single fixed value; it depends on imagery resolution, node type,
road density, terrain, and expected branch length. Prototype by testing
`r ∈ {250, 500, 1000, 2000} m` and reporting sensitivity.

### 2. Detect unrecorded branches

Within a search region, score a candidate branch by evidence, not appearance
alone:

```
S_branch = w1·C_origin + w2·C_continuity + w3·C_surface
         + w4·C_width  + w5·C_terrain    − w6·C_overlap
```

- `C_origin` — begins at the node
- `C_continuity` — uninterrupted trail strength
- `C_surface` — disturbed soil / reduced vegetation
- `C_width` — consistent with an off-road vehicle track
- `C_terrain` — physically traversable
- `C_overlap` — similarity to already-mapped roads or non-road features (penalty)

### 3. Trail following

Once detected, follow a branch outside the node radius — this is graph growth,
not whole-image segmentation. At each step choose the continuation direction:

```
d* = argmax_d [ w1·I_d + w2·K_d + w3·W_d + w4·T_d − w5·Δθ_d ]
```

(image evidence, continuity, width, terrain feasibility, minus an
abrupt-turn penalty). Terminate when confidence drops, the branch joins a mapped
road, it reaches a destination, disappears, or the terrain becomes implausible.
**Allow branching** — informal tracks split.

## Multi-year activity classification

The temporal comparison is the point. For a segment `e` and year `t`, estimate
`F_{e,t} = [W, V, D, C, B]` (width, vegetation encroachment, surface
disturbance, continuity, neighboring-branch strength) and an activity index:

```
A_{e,t} = αW − βV + γD + δC + εB      ΔA_e = A_{e,late} − A_{e,early}
```

| Classification | Expected pattern |
| --- | --- |
| Active, increasing | wider track, more exposed soil, less vegetation, more branches |
| Active, stable | similar width and disturbance across years |
| Active, decreasing | narrower, more vegetation, weaker continuity |
| Abandoned | progressive vegetation recovery, loss of continuity, no recent disturbance |
| Uncertain | conflicting imagery, poor resolution, seasonal obstruction |

Treat this probabilistically. The defensible output is *evidence of increasing /
stable / decreasing / absent recent use* — **not** vehicle counts.

## The distinctive problem: braided tracks

In open terrain drivers spread into several parallel ruts around potholes, mud,
sand, snow, and steep sections. Several physical tracks `{e_1, …, e_n}` are
functionally **one route corridor** `R_j`. Treating each visible rut as a
separate road makes the graph wrong. Model a corridor with: total width, number
of parallel tracks, average separation, dominant centerline, active-track
fraction, and lateral migration over time. This is the most novel and
Mongolia-specific contribution.

## Reference vehicle

"Any off-road vehicle" is not an engineering requirement. Use a class:

- **Light 4×4 (SUV / utility pickup):** ~1.8–2.1 m wide, needs ~2.5–3.0 m usable
  track, moderate rough-terrain capability, no heavy-truck assumption.

Classify passability as *likely traversable by light 4×4 / uncertain /
unlikely* rather than predicting exact accessibility.

## Research questions

1. Can multi-year imagery + graph-based tracing from mapped rural intersections
   identify previously unmapped active and abandoned corridors in Mongolia?
2. Can vegetation encroachment, corridor width, surface disturbance, and branch
   connectivity distinguish active informal roads from abandoned tracks?
3. Does node-seeded tracing outperform full-area segmentation in precision,
   processing cost, and network connectivity?

## Experiment structure

Compare, and show each subsystem earns its place:

- **A** — full-area segmentation (search all pixels)
- **B** — node-seeded search + branch tracing
- **C** — B + multi-year temporal analysis
- **D** — C + terrain constraints + corridor grouping + graph topology

## Ground truth

Classification cannot be evaluated without independent labels
`Y ∈ {active, abandoned, non-road, uncertain}`. Sources: GPS traces from local
drivers, field visits, recent drone imagery, expert manual interpretation,
repeated very-high-resolution imagery, or transportation records. Without this,
the project produces plausible maps, not defensible results.

## Known confounds and honest limits (fix these before believing any output)

- **Season/sensor mismatch** — compare same-month, comparable-condition imagery;
  otherwise you measure grass, not roads.
- **Vegetation ≠ abandonment** — normalize against local control regions and
  climate; drought/grazing/fire/rain all move NDVI independently.
- **Persistent scars** — abandoned tracks stay visible for years; require
  temporal *recovery* evidence, not just current visibility.
- **Width from pixels is noisy** — report width as an interval with a minimum
  pixel count across the road.
- **Mapping bias** — more mapped branches may just mean better imagery; keep
  observed topology separate from inferred topology.
- **Data source** — use OSM or an authorized GIS layer as the seed graph, not a
  scraped commercial provider.
- **Short archive** — three years (2024–2026) may be noise. The Phase-1 primary
  run uses four years per baseline (2018–2021 vs 2023–2026) and exposes the valid
  recent-year count; use a longer consistent archive when the temporal buffer and
  sensor record permit it.
- **Sentinel-1 acquisition mismatch** — the early and recent periods have different
  platform/revisit histories. Verify coverage and normalize sampling before treating
  radar change as evidence; Sentinel-1 is deferred until after the Phase-1 gate.

## Design decisions (2026 review)

1. **Target corridors, not single tracks.** A 2.5–3 m track is below the 10 m native sampling of
   B4/B8, and BSI additionally pulls in a 20 m SWIR band. Detect braided corridors, parallel-track
   clusters, and network-scale disturbance; prioritize candidates for high-res inspection. This
   makes the *braided-corridor* idea the distinctive contribution.

   **Restated 2026-09-24, sharpened 2026-09-25.** Being below the native sampling does not by itself
   make a feature undetectable — Welch 1982 separates detection from identification, and sub-pixel
   mapping literature recovers narrow linear features in principle. The defensible claim is narrower
   still: **this method has not demonstrated reliable single-track separation; corridors are its
   present target.** An unmeasured limit is not an established impossibility. **Minimum detectable
   width is unmeasured**, and no cited paper supplies it. See C1 in
   [the claim ledger](../literature/claim-ledger.md).
2. **Do not hard-mask cropland/built land.** That would erase real branches near
   settlements, and WorldCover is a static 2021 product ill-suited to a multi-year
   comparison. Hard-exclude only permanent water/snow; use temporal Dynamic World
   probability changes to flag cropland/built/water transitions as confounds.
3. **NDVI and bare-soil are related, not independent.** They share bands, so their
   agreement is one **composite disturbance score** (ΔNDVI, ΔBSI, local-control
   normalization, persistence; optional Sentinel-1 roughness later) — not two
   independent confirmations.
4. **Hough is a baseline, not the method.** Mongolian routes curve, split, and
   braid. Compare thresholded connected components, probabilistic Hough, multiscale
   ridge filtering, and skeletonization + graph tracing; the ridge/skeleton pipeline
   is the likely method.
5. **OSM seeds are a score, not a hard gate.** Keep both all-area and
   network-conditioned candidate sets; the seeded-vs-unseeded ablation is itself a
   headline result.
6. **Validate corridors, not pixels.** Fully label evaluation *tiles* (not
   cherry-picked tracks), use positive/negative/uncertain corridor labels,
   site-level holdouts, object-level precision/recall with a centerline-distance
   tolerance, length-weighted completeness, and per-site bootstrap CIs.

### Developments beyond the review

- **Two-stage by design, not as a fallback.** The deliverable is a coarse, free,
  scalable **candidate generator feeding targeted high-resolution confirmation** —
  adopted as the primary architecture from Phase 0, because it is the honest and
  strongest framing of what a 10 m sensor can do.
- **Resolution honesty is a reported result.** Characterize the minimum corridor
  width / braiding Sentinel-2 can resolve; this is publishable regardless of outcome.
- **Negative-control gate is quantitative and pre-registered.** Development-site
  disturbance must exceed the road-free control by a stated margin *before* any line
  extraction — the single most important gate (see below).
- **Local-control normalization implemented in code**, so the README's "compared
  against controls" is true, not aspirational (`gee/ndvi_change.js`, fixed-scale
  200–800 m annular z-score).
- **Provenance manifest on every artifact** (inputs, dates, scene counts, code
  version), emitted by the Earth Engine run and required for each exported raster.

### Pre-registered Phase-1 gate (frozen 2026-08-23)

The primary metric is **`large_component_fraction`**: the fraction of
non-permanent-water pixels on the fixed analysis grid (`EPSG:3857` at nominal scale 10 — see the
[2026-09-24 amendment](#amendment--2026-09-24--the-analysis-grids-units); this is **not** 10 m of
ground) that meet all of the following:

1. annulus-normalized composite disturbance `z >= 1.0`;
2. annual disturbance persistence `>= 2/3`;
3. at least two valid recent-year observations; and
4. membership in an 8-connected component of at least 50 pixels.

Phase 1 passes only when all compared sites have `coverage_fraction >= 0.90`
and at least two of the three verified development sites satisfy:

```
development large_component_fraction
    >= max(2.0 * negative-01 large_component_fraction, 0.0001)
```

The absolute floor prevents a near-zero negative control from turning a trivial
development response into an infinite ratio. `candidate_fraction` and the 90th
and 99th disturbance-z percentiles are reported as diagnostics but do not enter
the pass/fail decision. Site coordinates, reference-imagery date, provenance,
and `verified=true` must be frozen in `config/sites.geojson` before a run is gate
eligible. Unverified runs are explicitly labelled QA-only.

The primary configuration is also frozen before gate inspection: July composites
for 2018–2021 and 2023–2026 (2022 buffer), a 200–800 m control annulus, per-year
effect-size floor `0.02`, and the thresholds above. After the primary decision,
report sensitivity for z thresholds `{0.75, 1.0, 1.25}`, annual effect floors
`{0.01, 0.02, 0.03}`, annuli `{100–600, 200–800, 300–1000} m`, and component
sizes `{25, 50, 100}` pixels. Sensitivity runs cannot replace the registered
primary result.

## Developed execution plan (Phase 0–4)

Supersedes the earlier "Experiment structure". Sites are declared in
`config/sites.geojson` (development, holdout, confound, negative control).

**Phase 0 — Honest benchmark foundation.** Finalize `config/sites.geojson` with
≥3 development AOIs, 1 untouched holdout, ≥1 braided corridor, ≥1 recovering
corridor, ≥1 environmental confound, and ≥1 road-free negative control — each with
coordinates, rationale, reference-imagery date, and provenance. Change all public
wording from "active/abandoned" to "candidate disturbance/recovery".

**Phase 1 — Temporal evidence cube.** Replace two-date comparison with annual,
same-season composites (early 2018–2021, recent 2023–2026, with 2022 held out as a
temporal buffer), retaining every annual composite. Compute disturbance magnitude,
annulus-normalized change, valid-year count, and persistence. Replace static
WorldCover with temporal Dynamic World probability-change channels for confound
interpretation. Export float GeoTIFFs containing the evidence channels,
`candidate_mask`, `n_valid`, and `large_component_mask`, plus the run manifest.
**Deliverable:** verified-site metrics and one real Mongolia figure with early and
recent RGB as the first visual falsification check. **Gate:** use the exact rule in
the pre-registration above; rendered layers never determine pass/fail.

**Phase 2 — Raster→vector candidate extraction.** A proper Python package
(`pyproject.toml`, `rasterio`, `geopandas`, `scikit-image`, `shapely`, `networkx`)
with unit tests on synthetic curved/broken/braided corridors. Output GeoJSON with
geometry, length, orientation, width estimate, persistence, and uncertainty per
candidate. Compare connected-components / Hough / ridge / skeleton extractors.
*Status: a numpy/scipy ridge + connected-component baseline is implemented and
synthetic-tested in [`../analysis/`](../analysis/) (9/9 tests, incl. a road-free
noise control); skeleton + graph tracing and shapely/rasterio I/O are the `full`
optional extra. The extractor is applied to real imagery only after the Phase-1 gate.*

**Phase 3 — Network conditioning and corridor grouping.** Load a versioned
OSM/Geofabrik extract, rasterize large QA overlays with `ee.Image.paint`, and test
mapped-road buffers beginning at 60, 80, and 100 m to cover rural digitizing offset
and braided-corridor width. Score proximity to endpoints/rural intersections,
compare seeded vs unseeded detection, group parallel segments into corridors, and
keep observed geometry separate from inferred connections. During Phase 1, overlay
the exported GeoTIFF on the dated Geofabrik extract in QGIS; do not ingest an Earth
Engine road asset until interactive Phase-3 triage needs it. Google HYBRID tiles are
visual QA only and must never become reference geometry or a tracing source.

**Phase 4 — Evaluation.** Freeze the annotation protocol *before* threshold tuning.
Report candidate precision/recall, corridor completeness, false positives by land
cover, seeded-vs-unseeded ablation, Hough-vs-ridge/skeleton, development-vs-holdout
results, and candidate activity classification only if temporal labels are credible.

### Go / no-go

Cap Phase 0–1 at one weekend. **The gate:** apply the pre-registered 2×
large-component-fraction rule before any line extraction is attempted. If
Sentinel-2 cannot expose corridor-scale structure after temporal normalization, do
**not** spend weeks tuning line detectors. Pivot to: (1) detect only braided/wide
corridors; (2) use Sentinel-2 as a coarse candidate generator with high-resolution
confirmation — the strongest portfolio framing; or (3) reframe as a reproducible
study of *when* medium-resolution imagery fails to resolve informal-track networks.

## Attribution

Design shaped by an external project-scoping review. Imagery: Copernicus
Sentinel-2. Road graph: OpenStreetMap contributors.
