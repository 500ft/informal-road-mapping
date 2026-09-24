# Phase-2 topology follow-up — prospective design note

Prepared 2026-09-23 (week plan Day 5). **Design note only. Nothing here is implemented, and this
note does not authorize implementation.** No threshold, default, site or gate changes.

## The ceiling this addresses

`extract.py` delivers **one interior-biased path per accepted component**, marked in the code with a
`ponytail:` comment naming the ceiling. Three stress cases pin its consequences: `crossing` returns
zero candidates, `short_segments` returns zero, and `linear_confound_riverbank` returns a false
corridor as the strongest candidate.

The literature review (2026-09-22) located the ceiling more precisely than the code comment did:

- **It begins in the filter, not in the path step.** Hannink 2014 states multiscale Frangi-style
  vesselness cannot cope with crossings or bifurcations, because the image-domain Hessian supports
  only one orientation per location. So relaxing `min_elongation` cannot recover a crossing cleanly,
  which matches the stress case's own note that lowering it to 1.5 recovers *one* component for two
  roads.
- **Braiding is fused before anything downstream sees it.** Law & Chung 2008 shows Hessian detection
  merges closely located adjacent structures. Braided corridors — this project's stated distinctive
  target — are exactly that geometry.
- **The pipeline shape is itself criticised.** Bastani 2018 shows segmentation-then-postprocess
  carries high topological error, and iterative tracing captures 45% more junctions at 5% error.

## The three options, as specified in the owner's handoff

### Option A — split at skeleton junctions after accepted components

Replace the single path with a thinned skeleton, detect junction pixels, and emit one candidate per
skeleton branch.

| | |
|---|---|
| new input | none |
| new dependency | none required — `Zhang & Suen 1984` or `Lee 1994` thinning is implementable on the existing numpy/scipy core; `Bai 2007` is the standard answer to the spurious spurs that follow |
| synthetic cases that would expose improvement | `crossing` (currently 0 candidates) and the `branched` and `ring` fixtures already in `test_path_export.py` |
| metrics that must not change | component layer on all ten cases; `chord_line`; the v1 and v3 archives; every extractor default |
| likely false-positive modes | spurious spurs on noisy masks inflating candidate counts; a braided pair fused by the filter still yields one skeleton, so Option A **cannot** fix braiding — only junctions within an already-correct component |
| implementation cost | moderate: thinning, junction detection, branch extraction, pruning, plus a record schema change to carry multiple paths per component |
| trigger for promotion | a confirmation task demonstrates that a missing junction changes a human decision the current candidate list otherwise supports |

### Option B — retain the path, emit branch candidates from local graph forks

Keep the primary path as the delivered geometry and additionally emit secondary candidates where the
component graph forks away from it.

| | |
|---|---|
| new input | none |
| new dependency | none; the 8-neighbour component graph already exists in `_component_path_px` |
| synthetic cases | `branched` fixture; `crossing` partially |
| metrics that must not change | the primary path's own line recall and precision must be byte-identical, so Option B is strictly additive and A1 is unaffected |
| likely false-positive modes | every noise bump on the component boundary is a fork; without a length or depth threshold this generates many short spurious branches, and any such threshold is a new tunable parameter the project has so far avoided |
| implementation cost | low to moderate, but the thresholding question is the real cost |
| trigger | same as A, plus evidence that secondary branches are wanted as *candidates* rather than as topology |

### Option C — defer topology; use the current path for confirmation triage only

Ship the single path as what it is: a triage geometry that tells a human reviewer where to look at
higher resolution. Junctions and braids are recorded as known limits rather than solved.

| | |
|---|---|
| new input | none |
| new dependency | none |
| synthetic cases | none needed; the existing stress record already documents the limits |
| metrics that must not change | everything |
| likely false-positive modes | unchanged from today |
| implementation cost | zero |
| trigger to leave Option C | a real Phase-1 signal survives the negative control, **or** a reviewer demonstrates that the current geometry prevents a useful confirmation triage |

## Recommendation — Option C, and the reason is not inertia

Option C stands. Three independent arguments:

1. **Topology cannot be repaired downstream of a filter that lost the junction.** Hannink 2014
   places the loss in the Hessian response. Options A and B both operate on the component the filter
   produced, so neither recovers a crossing the filter already merged or dropped. Fixing this
   properly means changing the enhancement step — orientation scores, or Türetken 2013's integer
   program over candidate paths — which is a far larger change than either option describes.
2. **There is nothing to be topologically correct about yet.** No site is verified, no Earth Engine
   export exists, and CR-08 is the only research gate. Improving the geometry of candidates that
   have never been compared to a real corridor optimises an unmeasured quantity.
3. **The dominant error is not topological.** The stress record shows the extractor *fabricates* a
   river-bank-shaped feature as its strongest candidate, and the literature says this is a field-wide
   failure — Liu 2016 finds wadi extraction commission-errors onto roads, Nagel 2024 cannot separate
   road from seismic line at Sentinel-2 resolution, Queiroz 2020 treats roads, pipelines, seismic
   lines and power lines as one detectable class. **Better line geometry does not improve road
   versus non-road discrimination**, and discrimination is what a candidate list needs.

## What to do instead, if effort becomes available before CR-08 clears

Ranked by expected value, none of which is topology:

1. **The per-band median composite.** NDVI and BSI are currently ratios of independently medianed
   bands. Roberts 2017 shows this takes a ratio on a pixel that never existed; the geometric median
   or a medoid is the documented fix. This is a correctness issue in the Phase-1 input, upstream of
   everything else, and its magnitude here is untested.
2. **A sign-stable or sensor-independent channel** for the recovering site: tasseled-cap brightness
   with Shi & Xu 2019's Sentinel-2 coefficients, LandTrendr-style segment fitting which is
   sign-agnostic, or Sentinel-1 coherence, which Ji 2025 tested in Eastern Mongolian rangeland.
3. **An arid-appropriate index** for the Gobi site: MSAVI2 needs no extra data and no tuning
   constant, and Okin 2001 sets the honest floor — below roughly 30% green cover no vegetation index
   refinement helps and the detector must key on soil brightness.
4. **A second evaluation metric** alongside the buffer score: TOPO, APLS or clDice. Citraro 2020
   shows a single tolerance-based score can be blind to whole classes of error.

## Boundaries

No new dependency (no scikit-image, networkx, rasterio or learned model) is added by this note. The
L1 two-pixel scoring contract is unchanged. Pixel-space length is not metres. This note is a
prospective design record: if any option is later adopted, that adoption is a plan revision with its
own acceptance criteria, not an implementation decision taken from here.
