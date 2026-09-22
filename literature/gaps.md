# Gaps — what the literature does not settle

Absence of found evidence is not evidence of absence. Everything below is either a search failure
or a real hole in the literature, and the two are distinguished where possible.

## Things this project must establish itself

1. **No paper quantifies the effect of missing years on a bi-temporal or z-score change estimate.**
   The closest hits were gap-filling and time-series-reconstruction work, not an evaluation of how
   dropping a year biases a change magnitude. This project's ">= 2 valid recent years" rule has no
   cited basis. Either run the ablation or state it as a novel contribution.
2. **No paper analyses an L1 dilation band as an evaluation tolerance**, or the sensitivity of
   completeness and correctness to buffer width. The 2-pixel choice rests only on Heipke 1997's
   qualitative trade-off statement. Wiedemann 2003's redundancy caveat applies and is unaddressed.
3. **No OpenStreetMap completeness study exists for Mongolia or Central Asian steppe.** The nearest
   are Iran (Minaei 2020) and China (Zhang 2015). The Mongolia-specific figure should be extracted
   from Barrington-Leigh & Millard-Ball's supplementary data rather than inferred from the global
   average — especially given their U-shaped density finding.
4. **No confusion matrix with "river bank" as a class in a road detector was found.** Liu 2016 and
   Lu 2024 document the confusion qualitatively and in the mirror direction. This may genuinely be
   a hole in the literature and is worth stating as such rather than assumed missed.
5. **No head-to-head benchmark of Hessian ridge filters on satellite roads.** The filter lineage is
   medical imaging; the road-extraction literature rarely evaluates it directly. That comparison may
   simply not exist, which is itself reportable.
6. **Pre-registration in remote sensing appears to be an empty set.** Two targeted searches returned
   nothing. The nearest anchors are geography reproducibility (Nüst & Pebesma 2021) and the ecology
   adaptation (Parker 2016). Do not claim precedent for "pre-registered remote sensing" without a
   deeper search of the OSF registries and EarthArXiv.
7. **Nothing found on what resampling a 20 m shortwave band to 10 m does to a narrow-feature index.**
   A specific, checkable weakness in the bare-soil-index claim that remains unsupported either way.

## Engineering hazards named by the literature and checked here (2026-09-22)

| hazard | source | checked | result |
|---|---|---|---|
| Sentinel-2 Processing Baseline 04.00 radiometric offset (25 Jan 2022) falls **between** the 2018–2021 and 2023–2026 windows and creates a false step change | ESA/Copernicus documentation, not a peer-reviewed paper | `gee/ndvi_change.js` | **passes** — uses `COPERNICUS/S2_SR_HARMONIZED`, which rescales post-2022 reflectance to the earlier convention |
| A **per-band median** composite destroys the inter-band spectral relationship, so a band ratio is taken on a pixel that never existed | Roberts, Mueller & McIntyre 2017 | `julyS2` medians B2/B3/B4/B8/B11, then `julyComposite` computes NDVI and BSI from those medians | **applies** — the geometric median or a medoid is the documented fix; magnitude here is untested |
| BRDF is the largest uncontrolled term in time-series consistency | Qiu 2019 | pipeline | **applies** — no BRDF correction is present |
| The default Sen2Cor scene-classification mask is the weakest of the common options (84% vs MAJA 91%, FMask 90%) | Baetens 2019 | `maskS2` | **worth testing** — Cloud Score+ (Pasquarella 2023) runs natively in Earth Engine and allows weighting rather than hard masking |
| Cloud-mask models report weakness specifically on **road** and urban surfaces | Wright 2024 | — | named hazard for a pipeline whose targets are bare linear tracks |

## Clusters that are thin, and why

The session's shared web-search budget (200 calls) was exhausted partway through. Several searches
finished through the Crossref and OpenAlex APIs, which verify bibliographic fields precisely but
**discover** far less well — they can only confirm papers already named. The following are therefore
"correctly transcribed but not exhaustively discovered":

- Research-integrity and pre-registration (biased toward canonical works recalled by name).
- Google Earth Engine reproducibility (platform and bibliometric reviews only; no pitfalls paper).
- Seismic-line and pipeline detection outside the Alberta and boreal cluster.
- Railway-versus-road confusion: searched, returned noise, nothing usable.

## Not searched at all

- **Non-English literature.** Mongolian, Russian and Chinese-language work on Gobi and Inner
  Mongolian track corridors is almost certainly substantial and entirely absent here.
- **Synthetic aperture radar** beyond two incidental hits (Stewart 2020, Ji 2025). Sentinel-1
  backscatter and coherence are plausibly more sensitive to compaction than optical indices and
  would sidestep the recovery-sign problem. This is the largest unexplored methodological branch.
- **Biological soil crusts**, which strongly affect both NDVI and bare-soil indices in drylands.
- **Grey literature**: World Bank and Asian Development Bank transport assessments, Mongolian
  government road inventories — any of which might already contain the ground-truth corridors this
  project is trying to detect.
- **Neuron tracing** (APP2, Vaa3D, Rivulet, the DIADEM challenge), which solves the same
  one-path-versus-tree problem in a parallel field.
- **Archaeology and open-source-intelligence track mapping**, and desert braided-track
  geomorphology.

## Citations that need checking before external use

| entry | what is unverified |
|---|---|
| Wiedemann 1998 | book title: "Empirical Evaluation **Methods**" versus the widely cited "**Techniques** in Computer Vision" |
| Sato 1998 | co-author order beyond the first author; DOI |
| Mnih & Hinton 2010 | the attribution of "relaxed" precision/recall at ρ-pixel slack to this paper |
| Sloan 2024 | the "up to 81%" figure and its metric definition |
| Law & Chung 2008 | LNCS volume and page numbers |
| Funke 2015 | venue entirely unverified, no DOI found |
| Borgefors 1986, Zhou & Toga 1999, Rikimaru 2002, Nedkov 2017, Mena 2003, Chen 2022, Gruen & Li 1997, Wegner 2015 | DOI and/or page range taken from secondary sources |
| D-LinkNet, Forest Line Mapper (2020 entry), Mongolia GF-2 paper, Sentinel-2/PRISMA desert tracks | full author lists (the GF-2 paper's authors were later resolved as Wang, M.; Wang, J.-L.) |
| Dashpurev 2021 | key finding — no abstract was retrievable; read before claiming novelty against it |

Preprints without a confirmed peer-reviewed venue: Van Etten 2018 and 2019, Wang 2024 (R2-Net),
Nagel 2024, Meng 2023, Fobi 2020, Kamalu & Choi 2020. No entry in this folder was found to be
retracted.

## Method limitations of this review

No protocol was registered in advance, there was no second reviewer, and database coverage is not
guaranteed. Aboutness and evidence grades were assigned from abstracts and search results, not from
reading methods sections — including the grade A assignments. Findings for roughly a third of
entries come from abstracts or index records rather than full text, because publisher sites
returned access errors throughout. This folder can show an idea is distinct within what was
retrieved; it cannot establish that anything here is globally novel.
