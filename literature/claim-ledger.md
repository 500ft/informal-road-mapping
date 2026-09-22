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

The *reasoning* does not survive. Welch 1982 separates **detection** from **identification** and
shows high-contrast linear objects are detectable below the nominal pixel size; Atkinson 2005 and
Thornton 2006/2007 recover sub-pixel linear features, with linearity itself as exploitable prior
information. Jia 2023 extracts **2.5 m rural roads from 10 m Sentinel-2** — the exact width at the
exact resolution this project declares out of reach. Löw & Duveiller 2014 give a framework, tested
in Central Asia, for computing the recoverable width instead of asserting it.

**Restate as:** single tracks are not separable *by this project's per-pixel index method* at 10 m,
so corridors are the operative target — not that single tracks are unresolvable in principle.

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
89.2% correctness** — at 50 cm, so it is an upper bound this project cannot approach.

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
and the alert community routinely confirms alerts at higher resolution. Zhu 2020 (COLD) gives the
realistic error floor for an unsupervised screen: **27% omission, 28% commission** — so tens of
percent commission is normal, not a defect to hide.

## C11 — A positive-disturbance mask is not a recovery detector
**Source:** design.md:1–10 · **Confidence: high — with a concrete remedy available**

Correct, and the literature offers the fix. Kennedy 2010 (LandTrendr) fits piecewise segments, so
recovery appears as a positive-slope segment instead of failing a fixed positive threshold —
segment fitting is **sign-agnostic**. Burrell 2017 (TSS-RESTREND) represents abandonment as a
breakpoint followed by an opposite-sign residual trend. Crist & Cicone 1984 offers a different
route: tasseled-cap **brightness** is the axis a compacted track moves along and is sign-stable in a
way NDVI change is not, with Sentinel-2 coefficients in Shi & Xu 2019. Ji 2025 offers a fourth:
Sentinel-1 coherence responds to surface disturbance regardless of greenness sign, tested in Eastern
Mongolian rangeland.

## C12 — The multiscale Hessian ridge response is an appropriate corridor enhancer
**Source:** `extract.py::ridge_strength` · **Confidence: moderate — sound family, three documented weaknesses**

Provenance is solid: Frangi 1998 and Sato 1998 for the filter, Lindeberg 1998 for the
scale-normalised max. Sato's noise-equalisation across scales is the fix if the smallest scale
currently dominates.

Three documented weaknesses bear directly on observed behaviour. Hannink 2014 states the filter
**cannot cope with crossings or bifurcations**, because the image-domain Hessian supports one
orientation per location. Law & Chung 2008 shows it **merges adjacent structures**. Jerman 2016
shows Frangi/Sato response is **non-uniform across structure size and contrast**, so a single global
threshold after the scale-max treats narrow and wide corridors differently — and offers a drop-in
eigenvalue-ratio fix. Steger 1998 adds that asymmetric lateral contrast (bare soil one side,
vegetation the other) biases the detected centreline off axis.

**Scale range, checked:** the filter runs at sigmas 1–3 px on a 10 m grid, so it enhances ~10–30 m
structures. Amarsanaa's 26.5 m Gobi corridors fall inside that; Keshkamat's 30–125 m typical
corridors and 164 m national-route mean fall **outside** it. The range was set without a documented
link to any measured width. **Testable recommendation, not a proven defect.**

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

Correct, and the ceiling begins earlier than the code comment implies: Hannink 2014 places the
junction failure **in the filter**, before components or pathfinding. Türetken 2013 is the direct
answer — an integer program that rejects the tree assumption and recovers networks with cycles.
Dirnberger 2015 (NEFI) is the concrete raster-to-graph recipe; Zhang & Suen 1984 and Lee 1994 the
thinning algorithms; Bai 2007 the standard answer to the spurious spurs that follow.
Douglas & Peucker 1973 is the named simplification in the debt comment.

## C15 — Crossings are lost because the union component fails an elongation filter
**Source:** `results/extractor_stress_cases.json`, case `crossing` · **Confidence: challenged — the attribution is incomplete**

The elongation filter does reject the union component, but Hannink 2014 shows the **filter response
itself** is already degraded at crossings. So removing or relaxing the elongation threshold would
not recover the two roads cleanly. The stress case's own note (lowering `min_elongation` to 1.5
recovers *one* component for two roads) is consistent with the failure being upstream.

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
