# Claim ledger

Each row is a claim the repository **already makes**, with its source, and the literature that
supports or challenges it. Filled in 2026-09-22 from [bibliography.md](bibliography.md).

Confidence is about *this project's warrant* for the claim, not the papers' own quality.
**high** = multiple grade A/B papers agree and the setting transfers. **moderate** = supported with
a setting or scale mismatch. **low** = only weak or indirect evidence. **challenged** = the
literature found points the other way. **unsupported** = no supporting paper was found.

---

## C1 — "A 2.5–3 m track is sub-pixel at 10 m", therefore target braided corridors
**Source:** design.md:27, 183 · **Confidence: moderate — right conclusion, wrong reason**

The corridor decision is **well supported**, and by better evidence than the design gives.
Keshkamat 2012 measures Mongolian dirt-track corridors at 30–125 m (mean 164 m along national
routes); Amarsanaa 2022 finds 58% of Gobi dirt road is 3–4 parallel tracks averaging **26.5 m**.
The target genuinely is a multi-pixel swath.

The *reasoning* does not survive, though less dramatically than this ledger first claimed
(corrected 2026-09-24). Welch 1982 separates **detection** from **identification** and shows
high-contrast linear objects are detectable below the nominal pixel size; Atkinson 2005 and
Thornton 2006/2007 recover sub-pixel linear features, with linearity itself as exploitable prior
information. Jia 2023 produces a **2.5 m output map** from 10 m inputs by super-resolution mapping
with fine-resolution training labels — that is output grid spacing, **not** a demonstrated 2.5 m
minimum detectable width, and certainly not for a low-contrast Gobi track. Löw & Duveiller 2014 give
a framework, tested in Central Asia, for computing a recoverable width instead of asserting one.

**Restate as:** sub-pixel detection is possible in principle, but single tracks are not separable
*by this project's per-pixel index method*, so corridors remain the operative target. **This
project's minimum detectable width is unmeasured**, and no cited paper supplies it.

## C2 — "Abandoned tracks stay visible for years"
**Source:** design.md:165 · **Confidence: high for the claim, but the timescale is unsettled**

Supported, and the mechanism is documented: Kinugasa & Oda 2014 found track formation eroded soil
by 8.3–9.4 cm, destroying the seed bank, so recovery is not simple regrowth. Li 2006 shows early
recovery is a **compositional** change (pioneer species colonising compacted surfaces), not a
return to background greenness.

The timescale spans two orders of magnitude because the papers measure different variables:

| source | system | variable | time |
|---|---|---|---|
| Kinugasa 2015 | Mongolian steppe | cover and biomass | ~4 years |
| Keshkamat 2012 | Mongolia | full revegetation | 10–15 years |
| Jorgenson 2010 | Arctic tundra | severe-impact trails | 2 decades+ |
| Webb 2002 | Mojave | soil compaction | 80–130 years |

Jorgenson 2010 further shows recovery time is a strong function of initial severity and substrate,
and Burke 2014 that it is substrate-specific. **The project must name which variable it claims
recovery in, and carry a range rather than a point estimate**, for the `dev-02-recovering` site.

## C3 — "Drought/grazing/fire/rain all move NDVI independently"
**Source:** design.md:164 · **Confidence: high — and stronger than stated**

Strongly supported and, for Mongolia specifically, sharpened into a hazard. Purevjav 2025 (Science)
finds **climate rather than overgrazing explains most** Mongolian rangeland productivity change.
Wessels 2007 shows degradation is detectable only after removing the rainfall effect, and that
rain-use efficiency is unreliable. Prince 1998 showed an apparent Sahelian desertification signal
largely vanished after rainfall normalisation.

Evans & Geerken 2004 (RESTREND) is the standard correction; Burrell 2017 (TSS-RESTREND) adds break
detection. But Wessels 2012 sets the ceiling: degraded areas differ by only ~10–20% in vegetation
index, and simulated degradation ≥20% **breaks the very NDVI–rainfall relationship RESTREND needs**.
Hein & de Ridder 2006 with the Prince 2007 reply show the correction itself is contested.

Hamunyela 2016 is the closest published analogue to this project's control-ring z-score and should
be its primary methodological citation.

## C4 — NDVI and bare-soil indices "are related, not independent"
**Source:** design.md:191 · **Confidence: high**

Supported at the mechanism level. Huete 1985 held vegetation constant, swapped four soils, and
found **no** greenness measure predicted the spectra — a substrate change alone, which is what a
graded track is, moves NDVI. Huete & Jackson 1987 is the arid-rangeland statement of the same
point. Drusch 2012 adds an instrument constraint the design document already half-notices: the
shortwave band a bare-soil index needs is **20 m**, not 10 m.

## C5 — "Mongolian routes curve, split, and braid"
**Source:** design.md:196 · **Confidence: high**

Quantified by Amarsanaa 2022 (58% of Gobi dirt road is 3–4 parallel tracks) and mechanistically
explained by Keshkamat 2012 (washboard and rutting drive drivers onto new parallel trails). Law &
Chung 2008 adds the algorithmic consequence: Hessian detection **merges closely located adjacent
structures**, so braided tracks are fused into one component before anything downstream sees them.

## C6 — A ridge-filter plus skeleton-and-graph pipeline "is the likely method"
**Source:** design.md:197 · **Confidence: moderate — challenged on the pipeline shape**

The filter family is standard (Frangi 1998, Sato 1998, Lindeberg 1998, Steger 1998) and
Wegner 2015 formalises road networks as collections of minimum-cost paths, which is close to what
this project does.

But **Bastani 2018 (RoadTracer) shows segmentation-then-postprocess pipelines carry high
topological error** and that iterative tracing captures 45% more junctions at 5% error. This
project's shape — ridge mask, connected components, shortest path — is exactly the pattern
criticised. Sironi 2014 adds that ideal-cylinder filters lose accuracy when structures are very
irregular, which informal roads are.

## C7 — OSM seeding must stay "a score, not a hard gate"
**Source:** design.md:199 · **Confidence: moderate — the conclusion holds, one premise does not**

The incompleteness premise is well supported: Poley 2022 found global and national road datasets
hold only **11–14%** of the roads in regional or volunteered data; Meijer 2018 found GRIP yields
2–3× the length of prior global datasets; Engert 2024 found roads 3–6.6× longer than leading
datasets. Herfort 2023 shows coverage bias is structural and patterned, not random. Usmani 2023
shows training on OSM transfers its errors, worst outside metropolitan areas. Wu 2019 names a
second defect: centrelines carry no width, so OSM could not label a **corridor** output anyway.

**The challenge:** Barrington-Leigh & Millard-Ball 2017 find completeness has a **U-shaped**
relationship with population density — sparsely populated areas are among the *better* mapped. A
"Mongolia is sparse, therefore OSM is poor there" argument does not follow from the global average.
Girres & Touya 2010 adds that quality is heterogeneous within a single country.

**And the deferral may be stronger than necessary:** Fobi 2020 formalises partial and misaligned
labels as a solvable learning problem; Meng 2023 uses OSM as weak pretraining; Henry & Fraundorfer
2025 uses it as a prompt rather than a gate. Incompleteness can be modelled, not only avoided.

**Action:** extract the Mongolia-specific completeness figure from Barrington-Leigh & Millard-Ball's
supplementary data instead of citing the global number.

## C8 — Corridor-level validation with a centreline tolerance and site-level holdouts
**Source:** design.md:204 · **Confidence: high — and this project reinvented a named standard**

Wiedemann 1998 is the canonical buffer-based framework: **completeness and correctness** measured
by matching within a buffer of a reference centreline. This project's recall and precision of
centreline pixels inside a 2-pixel band is a raster reimplementation of it and should be named as
such. Heipke 1997 states the trade-off the 2-pixel choice must answer to: less tolerant matching
looks less complete but more accurate. Mayer 2006 gives the empirical range published systems
reach. Chemura 2024 gives the closest comparable numbers for informal tracks: **77.5% completeness,
89.2% correctness** — at 50 cm on a different sensor, dataset and landscape, so it is a comparison
point, **not** a mathematical bound on this project in either direction (corrected 2026-09-24).

Site-level holdout is supported by Roberts 2017 and vividly by Ploton 2020, where non-spatial
validation suggested a model explained over half the variance while spatial validation showed
quasi-null skill. Wadoux 2021 is the necessary counterweight: present the held-out site as a
**generalisation test, not an unbiased accuracy estimate**.

## C9 — A static land-cover product is ill-suited; use temporal probabilities instead
**Source:** design.md:188 · **Confidence: low — half wrong, and the replacement is weak here**

Two problems. First, Zanaga 2022 shows WorldCover has **two** epochs (2020 v100 and 2021 v200), not
one, though ESA warns they are not directly comparable for change — so the factual basis of the
rejection needs correcting even if the conclusion survives.

Second and more serious: **Venter 2022** measures Dynamic World at 72% overall but only **grass 34%,
shrub/scrub 47%, bare ground 57%** — precisely the classes that dominate the Mongolian steppe. The
built and water classes are fine at 83% and 92%. So a Dynamic World confound gate is far weaker in
this landscape than the "cropland/built/water" framing implies. Brown 2022 remains the correct
product citation.

## C10 — A coarse candidate generator feeding high-resolution confirmation
**Source:** design.md, Developments beyond the review · **Confidence: high**

This is an established operational pattern, not a fallback. Hansen 2016 (GLAD alerts) ships a
per-pixel **screen** that explicitly does not distinguish human-induced from natural disturbance,
and the alert community routinely confirms alerts at higher resolution.

**Correction 2026-09-24.** This ledger previously cited Zhu 2020 (COLD) as giving "the realistic
error floor" at 27% omission and 28% commission. That was wrong. Those are *measured results* for
one algorithm on the authors' Landsat evaluation against their reference data. They are not a lower
bound, not a prediction for Mongolian track candidates, and not an acceptable-error target here.
Quoting them as a floor could excuse a poor detector before it has been measured. **This screen's
error rates and the review burden it implies have not been measured at all.**

## C11 — A positive-disturbance mask is not a recovery detector
**Source:** design.md:1–10 · **Confidence: high — with a concrete remedy available**

The claim itself is correct. The literature offers **candidate remedies, each a hypothesis with its
own unmet input requirements** — not a fix (corrected 2026-09-24).

- Kennedy 2010 (LandTrendr) fits piecewise segments, so recovery could appear as a positive-slope
  segment rather than failing a fixed positive threshold. Naming it does not supply the index, the
  sign convention, sufficient temporal support, or independently dated changes it needs.
- Burrell 2017 (TSS-RESTREND) represents abandonment as a breakpoint plus an opposite-sign residual
  trend, and inherits RESTREND's rainfall-regression requirements.
- Crist & Cicone 1984 offers tasseled-cap **brightness**. But Shi & Xu 2019's Sentinel-2
  coefficients are derived for **at-sensor** reflectance and this repository uses **surface**
  reflectance, so they do not transfer without a compatible source or a tested conversion. Brightness
  is **not** established here as a directionally invariant marker of compaction or recovery across
  substrates.
- Ji 2025 uses Sentinel-1 **interferometric coherence** for grazing-related vegetation breakpoints —
  not road abandonment. Earth Engine's `S1_GRD` is detected backscatter, **not** coherence, which
  needs complex SLC pairs and separate interferometric processing. This is a separate pipeline to
  scope, not a channel to switch on.

## C12 — The multiscale Hessian ridge response is an appropriate corridor enhancer
**Source:** `extract.py::ridge_strength` · **Confidence: moderate — sound family, three documented weaknesses**

Provenance is solid: Frangi 1998 and Sato 1998 for the filter, Lindeberg 1998 for the
scale-normalised max. Sato's noise-equalisation across scales is the fix if the smallest scale
currently dominates.

Three documented weaknesses **motivate inspection** of observed behaviour, but none has been shown
to cause it here (corrected 2026-09-24). Hannink 2014 analyses **Frangi** vesselness at crossings;
`ridge_strength` is Sato-like, `max(0, -λ_min)·σ²`, and implements no eigenvalue-ratio suppression,
so that finding motivates a search for enhancement loss rather than diagnosing one. Law & Chung 2008
shows Hessian detection merges adjacent structures. Jerman 2016 shows Frangi/Sato response is
non-uniform across structure size and contrast. Steger 1998 adds that asymmetric lateral contrast
biases the detected centreline off axis.

**Scale range — the earlier arithmetic here was wrong twice.** It said sigmas 1–3 px on a 10 m grid
enhance "~10–30 m structures", implying an exclusive detectable-width band. Both halves fail:

1. **Filter scale is not a hard width cutoff.** A scale-normalised max over σ responds outside the
   nominal band with reduced, not zero, sensitivity.
2. **The pixel is not 10 m on the ground.** The grid is EPSG:3857 at nominal scale 10. Under the
   spherical Web Mercator approximation a 10-unit pixel spans about **6.6–7.0 m** of ground distance
   across the registered site latitudes, so every metre figure previously derived from a 10 m
   assumption was overstated by roughly 45%. See [C19](#c19--the-analysis-grids-nominal-metres-are-not-ground-metres).

The honest residue: the σ range was chosen without a documented link to any measured corridor width,
and measured Mongolian corridors span roughly 26–164 m. That is a **question to measure**, not a
proven mismatch.

## C13 — A distance-weighted shortest path yields a usable centreline
**Source:** `extract.py::_component_path_px` · **Confidence: high — and it has a published name**

This is a discrete instance of Cohen & Kimmel 1997's minimal-path model. Deschamps & Cohen 2001 is
the nearest published match to the whole step, including the centring trick and the
propagation-based endpoint finding that the two farthest-point sweeps approximate — cite both as
provenance rather than presenting it as bespoke. Gruen & Li 1997 is the remote-sensing ancestor.
Sethian 1996 (fast marching) would remove the 8-connectivity metrication bias. Benmansour 2011 shows
how to fuse the ridge and path steps into one metric and get corridor width for free.

## C14 — One path per component cannot represent junctions, loops or braids
**Source:** `extract.py` `ponytail:` comment · **Confidence: high — and the marked upgrade path exists**

Correct as stated. Where the ceiling *begins* is **not established** (corrected 2026-09-24):
Hannink 2014 concerns Frangi and motivates suspecting enhancement loss, but this implementation's
crossing failure has at least three candidate stages — enhancement, the quantile mask, and the
elongation rejection — and has not been attributed to any of them.

One consequence is already clear and was missed: **skeletonising only accepted components cannot
recover a crossing that was rejected before acceptance.** Any Option-A-style proposal has to
resolve that placement conflict first. Türetken 2013 remains the published answer for loopy
networks, but adopting it is a larger change than the topology note implied.
Dirnberger 2015 (NEFI) is the concrete raster-to-graph recipe; Zhang & Suen 1984 and Lee 1994 the
thinning algorithms; Bai 2007 the standard answer to the spurious spurs that follow.
Douglas & Peucker 1973 is the named simplification in the debt comment.

## C15 — Crossings are lost because the union component fails an elongation filter
**Source:** `results/extractor_stress_cases.json`, case `crossing` · **Confidence: challenged — the attribution is incomplete**

The elongation filter does reject the union component. Whether the **filter response** is already
degraded at the crossing is *suspected, not shown*: Hannink 2014 analyses Frangi, not this Sato-like
response. The stress case's own note (lowering `min_elongation` to 1.5 recovers *one* component for
two roads) is **consistent with** an upstream loss but does not establish it.

**This diagnosis is provisional** until the stage-by-stage trace is run: raw disturbance → per-scale
ridge response → quantile mask → component membership → length/elongation rejection → exported path,
recording junction and arm retention at each step. Corrected 2026-09-24.

## C16 — A river-bank-shaped feature is returned as the strongest candidate
**Source:** case `linear_confound_riverbank` · **Confidence: high — a field-wide failure, not a local bug**

Well documented, including in the mirror direction. Liu 2016 extracts desert wadis and reports
commission errors occurring mainly in features falsely enhanced by water indices — **specifically
roads**. Nagel 2024 finds that at Sentinel-2 resolution a deep model cannot separate road from
seismic line. Queiroz 2020 states from the authors' own framing that roads, pipelines, seismic lines
and power lines are **one detectable class** for geometry-driven extractors. Lu 2024 names rivers
and walls as recognised road false positives.

Two confound classes this project does not yet carry: **fence lines**, at ~0.93 km/km² mean density
in comparable grazing country (Buzzard 2022, with fencing proliferating in similar rangeland per
Løvschal 2022); and **animal paths**, which Chemura 2024 found co-occur with vehicle tracks at
r = 0.75.

## C17 — Scoring exported geometry against a reference centreline within a 2-pixel band
**Source:** `stress_cases.py::score_lines` · **Confidence: moderate — right family, two unaddressed critiques**

The family is canonical (Wiedemann 1998). Two specific critiques apply. Wiedemann 2003 formalises
**redundancy** and notes summary measures are valid only assuming none — but an L1 dilation band
lets one extracted pixel be matched by several reference pixels, which is exactly the double
counting warned about. Citraro 2020 shows connectivity metrics **rank the same algorithms
inconsistently** because design flaws blind them to whole error classes, so a single tolerance score
should not stand alone.

Named second metrics: TOPO (Biagioni 2012), APLS (Van Etten 2018), clDice (Shit 2021). Van Etten
2019 reports APLS and TOPO together, the same two-layer split this project already makes.
No paper was found analysing an L1 dilation band as a tolerance, or the sensitivity of
completeness/correctness to buffer width — see [gaps.md](gaps.md).

## C18 — A pre-registered negative-control gate is the strongest available check
**Source:** `phase1_gate.py`, design.md:215 · **Confidence: moderate — the design is right, the label is not yet earned**

Lipsitch 2010 is the methodological origin and supplies the condition: a negative control detects
only bias it shares a confounding pathway with. Simmons 2011 and Gelman & Loken 2014 justify
pre-committing every threshold, since **potential** comparisons alone inflate error rates.

But Nosek 2018 sets the standard the word "pre-registered" carries: a timestamped, uneditable
record, **not a threshold written in a version-controlled design document that the same team can
edit**. Parker 2016 is closer to this project's situation — pre-registration when analysing an
existing archive. Olofsson 2014 adds the separate requirement that any reported area or count needs
a probability sample and an error-adjusted estimate, which a deterministic full-raster score does
not provide.

**Action:** either deposit a timestamped registration externally, or soften the wording to
"pre-specified" throughout.


## C19 — The analysis grid's nominal metres are not ground metres
**Source:** `gee/ndvi_change.js` (`ANALYSIS_CRS = 'EPSG:3857'`, `ANALYSIS_SCALE_M = 10`) · **Confidence: high — independently calculated, not yet measured on an export**

Added 2026-09-24. The screen works on a Web Mercator grid at nominal scale 10. Web Mercator's linear
scale factor grows as 1/cos(latitude), so a 10-unit pixel does **not** span 10 m of ground away from
the equator. Under the spherical approximation:

| site | latitude | ground span of a 10-unit pixel | 50-pixel component area |
|---|---:|---:|---:|
| dev-01-braided | 47.30 | 6.78 m | 2,300 m² |
| dev-02-recovering | 46.20 | 6.92 m | 2,395 m² |
| dev-03-gobi | 45.40 | 7.02 m | 2,465 m² |
| holdout-01 | 48.10 | 6.68 m | 2,230 m² |
| confound-01 | 48.60 | 6.61 m | 2,187 m² |
| negative-01 | 46.80 | 6.85 m | 2,343 m² |

The `min_component_pixels = 50` threshold was therefore reasoned about as roughly 5,000 m² and is
closer to **2,200–2,500 m²**. Figures derived from a 10 m assumption were overstated, but **by
different amounts depending on dimension** (corrected 2026-09-25): at 47.3° N, using 10 m instead of
6.78 m overstates a **linear** distance by about **47%**, while using 5,000 m² instead of 2,300 m²
overstates an **area** by about **117%**. Do not apply one percentage to every metre figure.

**The grid is finer than the native sampling** (added 2026-09-24, corrected 2026-09-25). The native
sampling of B4 and B8 is 10 m, so a ~6.8 m analysis grid has **grid spacing about 1.47x finer than
native 10 m sampling**; the bilinear reprojection does not add measurements. An estimated 2,300 m²
is about **23 native-10 m pixel areas** or **5.75 native-20 m pixel areas** (B11, used by BSI).

**These are area equivalents, not independent sample counts.** An earlier version of this entry
called them "independent samples", which was wrong: dividing area by native pixel area establishes
neither the number of overlapping native pixels nor an effective sample size. Footprint shape, grid
alignment, interpolation, sensor spatial response and spatial covariance all bear on that, and none
is determined here. `min_component_pixels` is a **geometric selection rule, not a statistical
sample-size requirement**. The oversampling caution stands; the statistical inference does not.

Two further support questions, unresolved:

- **BSI mixes native samplings.** It uses B11, whose native sampling is 20 m, with B4, B8 and B2 at
  10 m. Resampling changes the grid; it does not create independent 10 m shortwave measurements.
- **The control ring is specified in metres** (200–800 m). Whether the metre-based kernel carries the
  same distortion as the pixel grid has not been tested.

**These are independently calculated estimates, not measurements of an exported raster.** Exact
ellipsoidal geometry, the delivered affine transform and neighbourhood-kernel behaviour all need a
runtime probe, which requires Earth Engine access this project does not have. `path_length_px` must
never be converted to metres using an assumed 10.
