# Phase-2 topology follow-up — prospective design note

Prepared 2026-09-23 (week plan Day 5). **Design note only. Nothing here is implemented, and this
note does not authorize implementation.** No threshold, default, site or gate changes.

## The ceiling this addresses

`extract.py` delivers **one interior-biased path per accepted component**, marked in the code with a
`ponytail:` comment naming the ceiling. Three stress cases pin its consequences: `crossing` returns
zero candidates, `short_segments` returns zero, and `linear_confound_riverbank` returns a false
corridor as the strongest candidate.

**Correction 2026-09-24.** An earlier version of this note asserted that the ceiling "begins in the
filter, not in the path step", citing Hannink 2014. That was an over-attribution. Hannink analyses
**Frangi** vesselness; `ridge_strength` is Sato-like, `max(0, -λ_min)·σ²`, with no eigenvalue-ratio
suppression, and `extract_candidates` separately rejects low-elongation components. The literature
**motivates suspecting** enhancement loss; it does not establish that enhancement caused the
observed crossing failure.

What the literature does support:

- **Enhancement loss at crossings is a real phenomenon worth looking for.** Hannink 2014 shows the
  image-domain Hessian supports one orientation per location, which is a property of any
  Hessian-based response, this one included.
- **Braiding can be fused before anything downstream sees it.** Law & Chung 2008 shows Hessian
  detection merges closely located adjacent structures. Braided corridors are exactly that geometry.
- **The pipeline shape is criticised in general.** Bastani 2018 shows segmentation-then-postprocess
  carries high topological error and that iterative tracing captured 45% more junctions at 5% error
  on their urban benchmark.

**The crossing failure has at least three candidate stages** — per-scale ridge response, the
quantile mask, and the length/elongation rejection — and has been attributed to none of them. The
diagnostic that would settle it is specified below.

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
| **placement conflict (added 2026-09-24)** | Option A skeletonises **accepted** components. The `crossing` case produces **zero** accepted components, because the union fails `min_elongation` before acceptance. **Option A therefore cannot recover the very case it is proposed for** unless it is moved upstream of the acceptance test — which is a different and larger change than this option describes. |
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

1. **Neither option can act on a case that produces no accepted component.** The `crossing` case
   yields zero candidates, so Option A has nothing to skeletonise and Option B has no path to fork
   from. Whether the structure was lost in the ridge response or only at the elongation test is
   **unresolved** — Hannink 2014 concerns Frangi and motivates the question rather than answering it
   — but either way both options sit downstream of the loss. Establishing where it happens is a
   prerequisite, not a detail.
2. **There is nothing to be topologically correct about yet.** No site is verified, no Earth Engine
   export exists, and CR-08 is the only research gate. Improving the geometry of candidates that
   have never been compared to a real corridor optimises an unmeasured quantity.
3. **The dominant error is not topological.** The stress record shows the extractor *fabricates* a
   river-bank-shaped feature as its strongest candidate, and the literature says this is a field-wide
   failure — Liu 2016 finds wadi extraction commission-errors onto roads, Nagel 2024 cannot separate
   road from seismic line at Sentinel-2 resolution, Queiroz 2020 treats roads, pipelines, seismic
   lines and power lines as one detectable class. **Better line geometry does not improve road
   versus non-road discrimination**, and discrimination is what a candidate list needs.

## Prerequisite diagnostic — run this before any option is reconsidered

Added 2026-09-24. Log the existing `crossing` case through every stage and record junction and arm
retention at each: raw synthetic disturbance → per-scale ridge response → quantile mask → component
membership → length and elongation rejection → exported path. Compare the defaults against **one**
named relaxation, leaving the committed baseline record untouched. This separates three
possibilities that are currently conflated — enhancement loss, rejection, and one-path
representation loss — and it is cheap, synthetic, and needs no imagery.

Only propose a new filter if enhancement demonstrably loses the structure. Only propose branch
extraction if accepted components retain it **and** a confirmation task needs it. A single
representative corridor path may be sufficient when the purpose is directing a human to a braided
swath; recovering each individual rut is a different target that nothing has yet asked for.

## What to do instead, if effort becomes available before CR-08 clears

Ranked by expected value, none of which is topology:

1. **The per-band median composite.** NDVI and BSI are currently ratios of independently medianed
   bands. Roberts 2017 shows this takes a ratio on a pixel that never existed; the geometric median
   or a medoid is the documented fix. This is a correctness issue in the Phase-1 input, upstream of
   everything else, and its magnitude here is untested.
2. **Candidate channels for the recovering site, each an experiment with unmet inputs** (corrected
   2026-09-24). Tasseled-cap brightness is attractive, but Shi & Xu 2019's coefficients are for
   **at-sensor** reflectance while this repository uses **surface** reflectance, so a compatible
   source or a tested conversion is required first, and brightness is not established as a
   direction-invariant marker of compaction across substrates. LandTrendr-style segment fitting is
   sign-agnostic, but naming it does not supply an index, a sign convention, sufficient temporal
   support, or independently dated changes. Sentinel-1 **coherence** is not available from Earth
   Engine's `S1_GRD` backscatter — it needs complex SLC pairs and separate interferometric
   processing — and Ji 2025 studied grazing-related vegetation breakpoints, not road abandonment.
3. **A controlled comparison of arid-appropriate indices** for the Gobi site — MSAVI2 needs no extra
   data and no tuning constant. The earlier claim here, that Okin 2001 sets a 30% green-cover floor
   below which no index refinement helps, is **withdrawn**: Okin concerns vegetation-*type* retrieval
   from simulated hyperspectral unmixing, cover fraction can sometimes still be estimated, and no
   universal index cutoff follows. Soil-adjusted indices are candidates to test, not a forced switch.
4. **A second evaluation metric** alongside the buffer score. Do **not** adopt APLS or TOPO merely
   because the literature names them: network metrics require a defined, independently labelled
   graph output, which does not exist here. Until it does, record duplicate candidates and tolerance
   sensitivity beside the current line scores, without claiming those establish topology.
   Citraro 2020 remains the reason a single tolerance-based score should not stand alone.

**Above all of these**, and added 2026-09-24: establish the analysis grid's physical meaning (C19 in
the [claim ledger](../../../literature/claim-ledger.md)). A nominal-10 Web Mercator pixel spans about
6.6–7.0 m on the ground at these latitudes, so the 50-pixel component threshold is nearer 2,300 m²
than 5,000 m². Every metre-denominated statement in this repository inherits that error.

## Boundaries

No new dependency (no scikit-image, networkx, rasterio or learned model) is added by this note. The
L1 two-pixel scoring contract is unchanged. Pixel-space length is not metres. This note is a
prospective design record: if any option is later adopted, that adoption is a plan revision with its
own acceptance criteria, not an implementation decision taken from here.
