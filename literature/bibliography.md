# Bibliography

Grouped by theme. Each entry: citation, one-line finding, why it matters here, **A**boutness 0–3,
**E**vidence A–D, and **transcription confidence** (see [README](README.md) for the grades and the
verification policy). Entries marked *unverified* on a field were not confirmed against the
publisher record — do not cite those fields externally without checking.

Retrieved 2026-09-22 by eight parallel searches. The session's web-search budget was exhausted
partway through; several clusters finished verification through the Crossref API, which confirms
bibliographic fields precisely but discovers less well than full-text search. See [gaps.md](gaps.md).

---

## 1. The application — informal, unpaved and off-road track detection

- **Keshkamat, S.S.; Tsendbazar, N.-E.; Zuidgeest, M.H.P.; van der Veen, A.; de Leeuw, J.** | 2012 | *The Environmental Impact of not Having Paved Roads in Arid Regions: An Example from Mongolia* | AMBIO 41(2):202–205 | doi:10.1007/s13280-011-0155-3
  - Dirt-track corridors are normally **30–125 m wide** (max ~6200 m); ~3260 km² lost to corridor degradation along ~11,000 km of national routes (mean width 164 m); **full revegetation takes 10–15 years** after a track falls out of use.
  - Supplies two of this project's load-bearing priors at once — the braiding mechanism and a Mongolia-specific recovery timescale. **A3 · EC · high**
- **Amarsanaa, S.; Lkhagva, A.; Chogsom, B.; Bayaraa, B.; Damdin, B.; Tsooj, B.; Nyamjav, J.; Baival, B.; Jamsranjav, C.** | 2022 | *Quantifying the Spatial Extent of Roads and Their Effects on the Vegetation in Mongolia's Gobi Desert* | Land 11(6):820 | doi:10.3390/land11060820
  - Road length nearly doubled 2010–2020; **42% of dirt road is a single track, 58% is 3–4 parallel tracks averaging 26.5 m wide**; vegetation near unpaved roads is measurably stressed.
  - Same sensor, same country, same object class. The 26.5 m mean is 2.6 Sentinel-2 pixels and is the best available width prior for the Gobi site. **A3 · EB · high** (author list truncated at six in one record; nine appear correct)
- **Keshkamat, S.S.; Tsendbazar, N.E.; Zuidgeest, M.H.P.; Shiirev-Adiya, S.; van der Veen, A.; van Maarseveen, M.F.A.M.** | 2013 | *Understanding transportation-caused rangeland damage in Mongolia* | Journal of Environmental Management 114:433–444 | doi:10.1016/j.jenvman.2012.10.043
  - Characterises how vehicle transport generates and widens rangeland damage corridors in Mongolia.
  - Closest existing work to this project's problem statement; the methodological baseline to differentiate from. **A3 · EC · high on citation, medium on finding wording**
- **Dashpurev, B.; Bendix, J.; Lehnert, L.W.** | 2020 | *Monitoring Oil Exploitation Infrastructure and Dirt Roads with Object-Based Image Analysis and Random Forest in the Eastern Mongolian Steppe* | Remote Sensing 12(1):144 | doi:10.3390/rs12010144
  - Object-based random forest over PlanetScope/RapidEye/Landsat back to 2005; grassland disturbed by dirt roads and oil infrastructure **grew 88% since 2005**.
  - A directly comparable methodological alternative — object/texture features rather than one change index, which sidesteps the sign problem entirely. **A3 · EB · high**
- **Chemura, A.; Lu, S.; Skidmore, A.K.; Duporge, I.; Lee, S.J.; Yu, Z.; Ngene, S.; Wang, T.** | 2024 | *Mapping off-road tracks and animal paths in protected areas using high-resolution GeoEye-1 panchromatic satellite imagery* | International Journal of Remote Sensing 45(16):5425–5442 | doi:10.1080/01431161.2024.2377230
  - Curvelet + active-contour + fuzzy pipeline on 50 cm imagery: **77.5% completeness, 89.2% correctness, 79.5% overall**; tracks and animal paths co-occur (r = 0.75).
  - A useful comparison point for a non-learned linear-feature extractor on informal tracks, and it names **animal paths** as a confound stratum this project did not carry. A different sensor (50 cm), dataset and landscape does **not** mathematically bound this project's achievable scores in either direction. Corrected 2026-09-24. **A3 · EB · high**
- **Gomes, O.F.M.; Feitosa, R.Q.; Coutinho, H.L.C.** | 2004 | *Sub-pixel unpaved roads detection in Landsat images* | ISPRS Congress XXXV Comm. III | [PDF](https://isprs.org/proceedings/XXXV/congress/comm3/papers/448.pdf)
  - Finds sub-pixel-width dirt roads as long, narrow, smooth segments spectrally closer to bare soil than their surroundings.
  - The closest classical precedent for this project's core problem at medium resolution. **A3 · EC · high**
- **Tømmervik, H.; Johansen, B.; Høgda, K.A.; Strann, K.B.** | 2012 | *High-resolution satellite imagery for detection of tracks and vegetation damage caused by all-terrain vehicles (ATVs) in Northern Norway* | Land Degradation & Development 23:43–52 | doi:10.1002/ldr.1047
  - Detects ATV tracks and vegetation damage using IKONOS and QuickBird (< 1 m) plus fieldwork.
  - The honest prior this project must argue against: off-road track detection has historically required sub-metre imagery. **A3 · EB · high**
- **Chen, Z.; Jefferies, B.; Adlakha, P.; Salehi, B.; Power, D.** | 2014 | *Monitoring Linear Disturbance Footprint Based on Dense Time Series Landsat Imagery* | Canadian Journal of Remote Sensing 40(5):348–361 | doi:10.1080/07038992.2014.987375
  - Directional template line detection, **line updating by reappearance frequency across dates**, Hough connection, then characterisation, over four Alberta sites.
  - Architecturally the same problem at the same coarse resolution, and its reappearance-frequency step is the direct precedent for this project's multi-year persistence rule. **A3 · EB · high**
- **Sloan, S.; Talkhani, R.R.; Huang, T.; Engert, J.; Laurance, W.F.** | 2024 | *Mapping Remote Roads Using Artificial Intelligence and Satellite Imagery* | Remote Sensing 16(5):839 | doi:10.3390/rs16050839
  - CNN on volunteer-digitised labels to detect remote/unmapped roads; a secondary source reports accuracy "up to 81%".
  - Closest published analogue to this project's task. **A3 · EC · high on citation, low on the 81% figure** (metric definition unverified)
- **Stewart, C.; Lazzarini, M.** *(further co-authors unverified)* | 2020 | *Deep Learning with Open Data for Desert Road Mapping* | Remote Sensing 12(14):2274 | doi:10.3390/rs12142274
  - OSM labels + Copernicus data with a U-Net for desert roads; **Sentinel-1 VV backscatter averages alone were the best model input**.
  - A direct counter-hypothesis: in arid terrain SAR may separate compacted tracks better than the optical signal this project relies on. **A3 · EB · high on citation, medium on author list**
- **Jia, Y.; Zhang, X.; Xiang, R.; Ge, Y.** | 2023 | *Super-Resolution Rural Road Extraction from Sentinel-2 Imagery Using a Spatial Relationship-Informed Network* | Remote Sensing 15(17):4193 | doi:10.3390/rs15174193
  - Produces a **2.5 m output map** from 10 m Sentinel-2 inputs by super-resolution mapping, using learned spatial relationships and fine-resolution training labels; reports better results for elongated rural roads than spectral-only methods.
  - Output grid spacing is **not** a demonstrated minimum detectable road width, and the training regime is not available here. It establishes that sub-pixel mapping is possible in principle; it does not establish reliable detection of a 2.5 m low-contrast Gobi track. This project's minimum detectable width remains **unmeasured**. Corrected 2026-09-24. **A2 · EB · high**
- **Oehmcke, S.; Thrysøe, C.; Borgstad, A.; Vaz Salles, M.A.; Brandt, M.; Gieseke, F.** | 2019 | *Detecting Hardly Visible Roads in Low-Resolution Satellite Time Series Data* | IEEE Big Data 2019:2403–2412 | doi:10.1109/bigdata47090.2019.9006251
  - Frames Sentinel-2 road detection as **ordinal** classification over cloud-affected time series, avoiding curated clear-sky tiles, evaluated against OSM.
  - Two transferable moves: grade corridors faint-to-clear instead of binary, and use the messy stack directly rather than compositing. **A3 · EB · high**
- **Zhou, Q.; Liu, Z.; Huang, Z.** | 2024 | *Mapping Road Surface Type of Kenya Using OpenStreetMap and High-resolution Google Satellite Imagery* | Scientific Data 11 | doi:10.1038/s41597-024-03158-7
  - National paved/unpaved surface map combining incomplete OSM attributes with imagery classification.
  - A template for deciding whether a detected corridor is genuinely "unmapped" given a partial reference. **A3 · EB · high**
- **Anon.** *(authors unverified)* | 2020 | *The Forest Line Mapper: A Semi-Automated Tool for Mapping Linear Disturbances in Forests* | Remote Sensing 12(24):4176 | doi:10.3390/rs12244176
  - Least-cost path over LiDAR canopy models predicting both **centreline and footprint** of roads, pipelines, seismic lines and power lines.
  - Operational precedent for this project's centreline-by-least-cost-path design, including the centreline-versus-footprint distinction it must make explicit. **A2 · EB · high on citation, author list unverified**
- **Anon.** *(authors unverified)* | 2024 | *Dirty road extraction from GF-2 images by semi-supervised deep learning method for arid and semiarid regions of southern Mongolia* | International Journal of Digital Earth 17(1) | doi:10.1080/17538947.2024.2384631
  - New natural-road dataset for Gurvantes Sumu, South Gobi; semi-supervised UniMatch reaches **IoU 73.51% / mIoU 86.37%**.
  - The direct methodological competitor in this project's exact study region. **A3 · EB · high on citation, author list unverified**
- **Anon.** *(authors, year and exact venue unverified)* | 2024 | *Automatic Desert Off-Road Track Mapping Using the Fusion of Sentinel-2 and PRISMA Data* | IEEE Xplore doc. 10537255
  - Fuses Sentinel-2 with PRISMA, then uses edges and **NDWI to separate drainage networks** before classification.
  - The most directly comparable Sentinel-2 off-road method found, and its drainage disambiguation addresses a confusion class this project's ridge filter will certainly hit. **A3 · EC · medium**

## 2. Mongolia — the study system

- **Li, S.-G.; Tsujimura, M.; Sugimoto, A.; Davaa, G.; Sugita, M.** | 2006 | *Natural recovery of steppe vegetation on vehicle tracks in central Mongolia* | Journal of Biosciences 31(1):85–93 | doi:10.1007/BF02705239
  - Pioneer species colonise compacted track surfaces first, soil hardness then declines, richness rises; early recovery is a **compositional change, not a return to background greenness**. **A3 · EC · high**
- **Kinugasa, T.; Suzuyama, Y.; Tsuchihashi, N.; Nachinshonhor, G.U.** | 2015 (online 2013) | *Colonization and expansion of grassland species after abandonment of dirt roads in the Mongolian steppe* | Landscape and Ecological Engineering 11(1):19–27 | doi:10.1007/s11355-013-0230-y
  - Cover and biomass had **almost recovered 4 years** after abandonment, but the low-palatability clonal herb *Artemisia adamsii* increased. **A3 · EC · high on citation, medium on finding**
- **Kinugasa, T.; Oda, S.** | 2014 | *Effects of vehicle track formation on soil seed banks in grasslands with different vegetation in the Mongolian steppe* | Ecological Engineering 67:112–118 | doi:10.1016/j.ecoleng.2014.03.078
  - Track formation eroded soil by **8.3–9.4 cm**, severely damaging the seed bank — a mechanistic reason the signature persists after traffic stops. **A3 · EC · high on citation, medium on finding**
- **Purevjav, A.-O.; Avirmed, T.; Wilcox, S.W.; Barrett, C.B.** | 2025 | *Climate rather than overgrazing explains most rangeland primary productivity change in Mongolia* | Science 389:1229–1233 | doi:10.1126/science.adn0005
  - Climate, not overgrazing, explains most change in Mongolian rangeland productivity.
  - **Critical caution**: interannual NDVI change in Mongolia is climate-dominated, so a disturbance screen must control for it or fire on wet and dry years. **A2 · EB · high on citation, medium on finding; recent and possibly contested**
- **Byambakhuu, I.; Sugita, M.; Matsushima, D.** | 2010 | *Spectral unmixing model to assess land cover fractions in Mongolian steppe regions* | Remote Sensing of Environment 114(10):2361–2372 | doi:10.1016/j.rse.2010.05.013
  - Field spectra at **58 sites across semi-arid and arid Mongolian steppe** fit and test photosynthetic/non-photosynthetic/bare-soil unmixing.
  - The most site-specific paper found: in-country endmembers for exactly the decomposition the Gobi site needs. **A3 · EB · high**
- **Ji, S.; Gonchigsumlaa, G.; Damdindorj, S.; Tseren, T.; Sharavjamts, D.; Otgondemberel, A.** | 2025 | *Can vegetation breakpoints in Eastern Mongolia rangeland be detected using Sentinel-1 coherence time series data?* | GIScience & Remote Sensing 62(1) | doi:10.1080/15481603.2025.2540222
  - Sentinel-1 **interferometric coherence**, with weather predictors and random forest, for grazing-induced vegetation breakpoints in Mongolian rangeland.
  - A Mongolian coherence application, **not** a validation of road-abandonment detection. Note also that Earth Engine's `COPERNICUS/S1_GRD` is detected backscatter, **not** coherence: coherence needs complex SLC pairs and separate interferometric processing, so this is a separate data pipeline to scope, not a drop-in channel. Corrected 2026-09-24. **A2 · EB · high**
- **Dashpurev, B.; Wesche, K.; Jäschke, Y.; Oyundelger, K.; Phan, T.N.; Bendix, J.; Lehnert, L.W.** | 2021 | *A cost-effective method to monitor vegetation changes in steppes ecosystems: A case study on remote sensing of fire and infrastructure effects in eastern Mongolia* | Ecological Indicators 132:108331 | doi:10.1016/j.ecolind.2021.108331
  - Remote-sensing case study of fire and **infrastructure** effects on eastern Mongolian steppe vegetation. **A2 · EB · high on citation, LOW on finding** (no abstract retrieved; read before claiming novelty)
- **Meng, X.; Gao, X.; Li, S.; Li, S.; Lei, J.** | 2021 | *Monitoring desertification in Mongolia based on Landsat images and Google Earth Engine from 1990 to 2020* | Ecological Indicators 129:107908 | doi:10.1016/j.ecolind.2021.107908
  - National desertification mapping, giving regional background against which a local change can be judged anomalous. **A2 · EB · high**
- **Mendgen, P.; Dejid, N.; Olson, K.; Buuveibaatar, B.; Calabrese, J.M.; Chimeddorj, B.; Dalannast, M.; Fagan, W.F.; Leimgruber, P.; Müller, T.** | 2023 | *Nomadic ungulate movements under threat: Declining mobility of Mongolian gazelles in the Eastern Steppe of Mongolia* | Biological Conservation 286:110271 | doi:10.1016/j.biocon.2023.110271
  - Long-distance gazelle movements fell **36% (142 km in 2007 → 92 km in 2021)**, associated with rising vehicle numbers rather than climate.
  - The "so what": dirt-track density, not paved infrastructure, tracks the ecological cost. **A2 · EB · high on citation, medium on finding**
- **Sainnemekh, S.; Barrio, I.C.; Densambuu, B.; Bestelmeyer, B.; Aradóttir, Á.L.** | 2022 | *Rangeland degradation in Mongolia: A systematic review of the evidence* | Journal of Arid Environments 196:104654 | doi:10.1016/j.jaridenv.2021.104654 — **A2 · EB · high on citation, low-medium on findings**
- **Jamsranjav, C.; Reid, R.S.; Fernández-Giménez, M.E.; Tsevlee, A.; Yadamsuren, B.; Heiner, M.** | 2018 | *Applying a dryland degradation framework for rangelands: the case of Mongolia* | Ecological Applications 28(3):622–642 | doi:10.1002/eap.1684 — **A2 · EB · high on citation, low-medium on findings**
- **Jackson, S.L.** | 2015 | *Dusty roads and disconnections: Perceptions of dust from unpaved mining roads in Mongolia's South Gobi province* | Geoforum 66:94–105 | doi:10.1016/j.geoforum.2015.09.010
  - Documents mining-driven unpaved haul roads as a distinct corridor class in the Gobi. **A2 · ED · high on citation, medium on finding**
- **Chen, Z.; Gao, X.; Lei, J.** | 2023 | *Dust emission and potential diffusion process in Mongolia* | Land Degradation & Development 34:2750–2762 | doi:10.1002/ldr.4621 — **A1 · EC · high on citation, low-medium on finding**

## 3. Off-road vehicle impact and recovery timescales (non-Mongolian drylands and tundra)

- **Webb, R.H.** | 2002 | *Recovery of Severely Compacted Soils in the Mojave Desert, California, USA* | Arid Land Research and Management 16(3):291–305 | doi:10.1080/153249802760284829
  - Compacted desert roadbed soils recover on the order of **80–130 years** — soil compaction outlives vegetation recovery by an order of magnitude. **A2 · EB · high on citation, medium on the figure**
- **Bolling, J.D.; Walker, L.R.** | 2000 | *Plant and soil recovery along a series of abandoned desert roads* | Journal of Arid Environments 46(1):1–24 | doi:10.1006/jare.2000.0651
  - The standard chronosequence design for the question this project's disused-track site poses. **A2 · EB · high on citation, medium on finding**
- **Jorgenson, J.C.; Ver Hoef, J.M.; Jorgenson, M.T.** | 2010 | *Long-term recovery patterns of arctic tundra after winter seismic exploration* | Ecological Applications 20(1):205–221 | doi:10.1890/08-1856.1
  - Paired plots 1984–2002: low-disturbance trails recovered well, **severe impacts persisted two decades**, and recovery was impossible where subsidence occurred.
  - Recovery time is a strong function of initial severity and substrate — do not assume one timescale across sites. **A2 · EB · high**
- **Guo, Q.** | 2004 | *Slow recovery in desert perennial vegetation following prolonged human disturbance* | Journal of Vegetation Science 15(6):757–762 | doi:10.1111/j.1654-1103.2004.tb02318.x
  - Desert perennials recover on multi-decadal timescales; over a few Sentinel-2 years the recovery signal may be smaller than rainfall noise. **A3 · EB · high**
- **Assaeed, A.M.; Al-Rowaily, S.L.; El-Bana, M.I.; Abood, A.A.A.; Dar, B.A.M.; Hegazy, A.K.** | 2019 | *Impact of off-road vehicles on soil and vegetation in a desert rangeland in Saudi Arabia* | Saudi Journal of Biological Sciences 26(6):1187–1193 | doi:10.1016/j.sjbs.2018.05.001
  - Bare ground highest in tracks (60.7%), bulk density up 38%; the **track / inter-track / verge / undisturbed** stratification is directly reusable as a validation sampling design. **A2 · EB · high** (use the Crossref author order; some sources list Abood first)
- **Burke, A.** | 2014 | *Natural recovery of dwarf shrubs following topsoil and vegetation clearing on gravel and sand plains in the southern Namib Desert* | Journal of Arid Environments 100–101:18–22 | doi:10.1016/j.jaridenv.2013.10.002
  - Substrate-specific recovery after exactly the disturbance a graded track produces. **A2 · EB · high**
- **Raynolds, M.K.; Jorgenson, J.C.; Jorgenson, M.T.; Kanevskiy, M.; Liljedahl, A.K.; Nolan, M.; Sturm, M.; Walker, D.A.** | 2020 | *Landscape impacts of 3D-seismic surveys in the Arctic National Wildlife Refuge, Alaska* | Ecological Applications 30(7) | doi:10.1002/eap.2143 — **A2 · EB · high on citation, low-medium on finding**
- **Dewidar, K.; Thomas, J.; Bayoumi, S.** | 2016 | *Detecting the environmental impact of off-road vehicles on Rawdat Al Shams in central Saudi Arabia by remote sensing* | Environmental Monitoring and Assessment 188 | doi:10.1007/s10661-016-5400-6 — **A2 · EC · high on citation, low on finding detail**
- **Bar (Kutiel), P.; Doron, E.; Dorman, M.** | 2025 | *Restoration of Off-Road Vehicle (ORV) Trails in a Hyper-Arid Area for Nature and Landscape Conservation* | Applied Sciences 15:6718 | doi:10.3390/app15126718
  - ORV trails **accumulate unintentionally** in hyper-arid terrain — the same generative process assumed for the Gobi corridor. **A2 · EB · high on citation and design, low on outcome**

## 4. Road extraction methods — classical and learned

- **Mena, J.B.** | 2003 | *State of the art on automatic road extraction for GIS update: a novel classification* | Pattern Recognition Letters 24(16):3037–3058 | DOI unverified
  - Surveys ~250 references and proposes a taxonomy of extraction approaches. Gives this repository the prior-art vocabulary for justifying a non-learned ridge-and-graph pipeline. **A3 · ED · high**
- **Chen, Z.; Deng, L.; Luo, Y.; Li, D.; Marcato Junior, J.; Gonçalves, W.N.; Nurunnabi, A.A.M.; Li, J.; Wang, C.; Li, D.** | 2022 | *Road extraction in remote sensing data: A survey* | Int. J. Applied Earth Observation and Geoinformation 112:102833 | DOI unverified — **A3 · ED · high**
- **Lu, X.; Weng, Q.** | 2025 | *Deep learning-based road extraction from remote sensing imagery: Progress, problems, and perspectives* | ISPRS J. Photogrammetry and Remote Sensing 228:122–140 | doi:10.1016/j.isprsjprs.2025.07.013
  - Names unlabeled-region generalisation and topology preservation as open problems — the current justification for a label-free classical pipeline where no regional labels exist. **A3 · ED · high**
- **Gruen, A.; Li, H.** | 1997 | *Semi-automatic linear feature extraction by dynamic programming and LSB-snakes* | Photogrammetric Engineering & Remote Sensing 63(8):985–995 | DOI unverified
  - Optimises a cost functional along a path between seed points. The canonical ancestor of this project's distance-weighted shortest-path export. **A3 · EC · medium**
- **Wegner, J.D.; Montoya-Zegarra, J.A.; Schindler, K.** | 2013 | *A Higher-Order CRF Model for Road Network Extraction* | CVPR 2013:1698–1705
  - Encodes a road prior as higher-order cliques along line segments so the model favours long thin connected networks over blobs. The principled alternative to connected-component filtering. **A3 · EB · high**
- **Wegner, J.D.; Montoya-Zegarra, J.A.; Schindler, K.** | 2015 | *Road networks as collections of minimum cost paths* | ISPRS J. Photogrammetry and Remote Sensing 108:128–137 | DOI unverified
  - Formulates extraction as selecting minimum-cost paths over an image-derived cost surface — the closest published formalisation of this project's Phase-2 stage. **A3 · EB · medium**
- **Mnih, V.; Hinton, G.E.** | 2010 | *Learning to Detect Roads in High-Resolution Aerial Images* | ECCV 2010:210–223 | doi:10.1007/978-3-642-15567-3_16
  - First large-scale neural road detector. Often credited with "relaxed" precision/recall at ρ-pixel slack — **that attribution was not verified**. **A2 · EB · high on citation, low on the relaxed-metric attribution**
- **Bastani, F.; He, S.; Abbar, S.; Alizadeh, M.; Balakrishnan, H.; Chawla, S.; Madden, S.; DeWitt, D.** | 2018 | *RoadTracer: Automatic Extraction of Road Networks from Aerial Images* | CVPR 2018:4720–4728 | doi:10.1109/CVPR.2018.00496
  - Segmentation-then-postprocess pipelines have **high topological error**; iterative CNN-guided tracing captures 45% more junctions at 5% error across fifteen cities.
  - Direct warning: ridge mask → connected components → shortest path is exactly the pattern shown to be topologically fragile. **A3 · EA · high**
- **He, S.; Bastani, F.; Jagwani, S.; Alizadeh, M.; Balakrishnan, H.; Chawla, S.; Elshrif, M.M.; Madden, S.; Sadeghi, M.A.** | 2020 | *Sat2Graph: Road Graph Extraction Through Graph-Tensor Encoding* | ECCV 2020 | doi:10.1007/978-3-030-58586-0_4
  - Predicts graph structure directly, beating prior work on **TOPO and APLS** — the two graph metrics this project should report instead of pixel overlap. **A3 · EB · high**
- **Zhou, L.** *(co-authors unverified)* | 2018 | *D-LinkNet: LinkNet with Pretrained Encoder and Dilated Convolution for High Resolution Satellite Imagery Road Extraction* | CVPR 2018 Workshops (DeepGlobe) | DOI unverified
  - Won DeepGlobe 2018 at **IoU 0.6466 val / 0.6342 test**. The honest supervised ceiling: even supervised deep learning sits near 0.63, not 0.9. **A3 · EB · medium**
- **Demir, I.; Koperski, K.; Lindenbaum, D.; Pang, G.; Huang, J.; Basu, S.; Hughes, F.; Tuia, D.; Raskar, R.** | 2018 | *DeepGlobe 2018: A Challenge to Parse the Earth through Satellite Images* | CVPR 2018 Workshops | arXiv:1805.06561
  - The de facto road benchmark at 50 cm — usable as a sanity check, but the 10 m / 50 cm gap must be stated. **A3 · EB · high**
- **Mosinska, A.; Márquez-Neila, P.; Koziński, M.; Fua, P.** | 2018 | *Beyond the Pixel-Wise Loss for Topology-Aware Delineation* | CVPR 2018:3136–3145 | arXiv:1712.02190
  - Pixel-wise losses cannot express topological error; a topology-aware term nearly doubles accuracy on some aerial datasets. **A2 · EB · high**
- **Wang, N.; Wang, X.; Pan, Y.; Yao, W.; Zhong, Y.** | 2024 | *Reverse Refinement Network for Narrow Rural Road Detection in High-Resolution Satellite Imagery* | arXiv:2410.10389
  - Targets keeping **narrow rural roads connected**; names WHU-RuR+ as a global rural-road dataset. **A3 · EB · high on transcription; preprint, peer review unverified**
- **Workman, R.; Wong, P.; Wright, A.; Wang, Z.** | 2023 | *Prediction of Unpaved Road Conditions Using High-Resolution Optical Satellite Imagery and Machine Learning* | Remote Sensing 15(16):3985 | doi:10.3390/rs15163985 — **A2 · EB · high**

## 5. Ridge and line filters — the algorithm this project implements

- **Frangi, A.F.; Niessen, W.J.; Vincken, K.L.; Viergever, M.A.** | 1998 | *Multiscale Vessel Enhancement Filtering* | MICCAI 1998, LNCS 1496:130–137 | doi:10.1007/BFb0056195
  - Defines vesselness from multiscale Hessian eigenvalues, taking the maximum response over scales. **The primary citation for `ridge_strength`.** **A3 · EB · high**
- **Sato, Y.; Nakajima, S.; Shiraga, N.; Atsumi, H.; Yoshida, S.; Koller, T.; Gerig, G.; Kikinis, R.** | 1998 | *Three-dimensional multi-scale line filter for segmentation and visualization of curvilinear structures in medical images* | Medical Image Analysis 2(2):143–168 | PMID 10646760, DOI unverified
  - A line filter from Hessian eigenvalues, integrating multi-scale responses by **equalising noise level across scales**.
  - Closer to this project's single-eigenvalue form than Frangi's three-eigenvalue measure; the noise-equalisation point is the fix if the smallest scale currently dominates. **A3 · EB · high** (verify co-author order)
- **Steger, C.** | 1998 | *An Unbiased Detector of Curvilinear Structures* | IEEE TPAMI 20(2):113–125 | doi:10.1109/34.659930
  - Models the line with its surroundings so extracted position is unbiased under **asymmetric lateral contrast**, returning sub-pixel position and width.
  - Diagnoses a specific failure here: a track with bare soil on one side and vegetation on the other shifts the detected centreline off axis. **A3 · EB · high**
- **Lindeberg, T.** | 1998 | *Edge Detection and Ridge Detection with Automatic Scale Selection* | IJCV 30(2):117–154 | doi:10.1023/A:1008097225773
  - Scale-space ridges from normalised derivatives maximal **over scale** — the theoretical justification for the scale-max step and for what the sigma range must cover. **A3 · EC · high**
- **Lindeberg, T.** | 1998 | *Feature Detection with Automatic Scale Selection* | IJCV 30(2):77–116 | doi:10.1023/A:1008045108935
  - The general normalised-derivative principle; a wrong exponent systematically biases which corridor widths win the max. **A2 · EC · high** (page range commonly cited as 79–116; verify)
- **Hannink, J.; Duits, R.; Bekkers, E.** | 2014 | *Crossing-Preserving Multi-scale Vesselness* | MICCAI 2014, LNCS 8674:603–610 | doi:10.1007/978-3-319-10470-6_75
  - States that multiscale **Frangi** vesselness cannot cope with crossings or bifurcations, because the image-domain Hessian supports one orientation per location, and fixes it by lifting to orientation scores.
  - **Motivates** looking for enhancement loss at crossings, but does **not** diagnose this implementation: `ridge_strength` is Sato-like, `max(0, -λ_min)·σ²`, and does not implement Frangi's eigenvalue-ratio suppression. `extract_candidates` separately rejects low-elongation components, so the observed crossing failure has at least three candidate stages and has not been attributed to any of them. Corrected 2026-09-24. **A2 · EB · high**
- **Law, M.W.K.; Chung, A.C.S.** | 2008 | *Three Dimensional Curvilinear Structure Detection Using Optimally Oriented Flux* | ECCV 2008 | DOI unverified
  - Hessian detection **merges closely located adjacent structures** because second-derivative responses are corrupted by neighbours.
  - The second failure mode that matters here: parallel and braided corridors fused into one component, which is what makes one-path-per-component wrong. **A3 · EB · high on venue/year, volume and pages unverified**
- **Jerman, T.; Pernuš, F.; Likar, B.; Špiclin, Ž.** | 2016 | *Enhancement of Vascular Structures in 3D and 2D Angiographic Images* | IEEE TMI 35(9):2107–2118 | doi:10.1109/TMI.2016.2550102
  - An eigenvalue-**ratio** enhancement giving near-uniform response across structure size and contrast, correcting Frangi/Sato's non-uniform scale response.
  - Explains why one global threshold after the scale-max treats narrow and wide corridors differently, and offers a drop-in fix. **A3 · EB · high**
- **Sironi, A.; Lepetit, V.; Fua, P.** | 2014 | *Multiscale Centerline Detection by Learning a Scale-Space Distance Transform* | CVPR 2014:2697–2704
  - Motivated explicitly by ideal-cylinder filters losing accuracy when linear structures become **very irregular** — which informal roads are. **A3 · EB · high**
- **Majer, P.** | 2004 | *On the Influence of Scale Selection on Feature Detection for the Case of Linelike Structures* | IJCV 60:191–202 | doi:10.1023/B:VISI.0000036834.42685.b6
  - Selected scale systematically shifts detected position and strength for line-like structures — relevant to corridors wider than the largest sigma. **A2 · EC · medium**
- **Kovesi, P.** | 1999 | *Image Features from Phase Congruency* | Videre 1(3) | no DOI
  - Contrast- and illumination-invariant feature measure; an alternative that needs no per-scene amplitude threshold. **A2 · EC · high**
- **Longo, A.** *(co-authors unverified)* | 2020 | *Assessment of Hessian-based Frangi vesselness filter in optoacoustic imaging* | Photoacoustics | PMID 32714832, DOI unverified
  - Scale choice, contrast variation and limited view make the Frangi filter **generate artifactual structures** readable as real vessels.
  - The closest thing to a false-positive audit of this filter family. **A2 · EB · medium**

## 6. Centrelines, skeletons, minimal paths and topology

- **Cohen, L.D.; Kimmel, R.** | 1997 | *Global Minimum for Active Contour Models: A Minimal Path Approach* | IJCV 24(1):57–78 | doi:10.1023/A:1007922224810
  - The globally minimal path between two endpoints under a potential-weighted metric.
  - **The formulation this project already implements**: the 1/EDT-weighted shortest path is a discrete instance. Cite as provenance. **A3 · EB · high**
- **Deschamps, T.; Cohen, L.D.** | 2001 | *Fast extraction of minimal paths in 3D images and applications to virtual endoscopy* | Medical Image Analysis 5(4):281–299 | PMID 11731307
  - Introduces a **centred** path inside a tubular structure plus **propagation-based endpoint finding**.
  - The nearest published match to this project's whole path step, including the centring trick and the endpoint selection that its two farthest-point sweeps approximate. **A3 · EB · high**
- **Benmansour, F.; Cohen, L.D.** | 2011 | *Tubular Structure Segmentation Based on Minimal Path Method and Anisotropic Enhancement* | IJCV 92(2):192–210 | doi:10.1007/s11263-010-0331-0
  - Couples tubular enhancement with fast-marching minimal paths, tracking radius as an extra dimension.
  - Shows how to fuse the ridge and path steps into one metric — the ridge response becomes the path cost — and yields corridor width for free. **A3 · EB · high**
- **Sethian, J.A.** | 1996 | *A fast marching level set method for monotonically advancing fronts* | PNAS 93(4):1591–1595 | doi:10.1073/pnas.93.4.1591
  - The continuous analogue of Dijkstra; removes the 8-connectivity metrication bias that makes pixel-graph paths jagged. **A2 · EC · high**
- **Türetken, E.; Benmansour, F.; Andres, B.; Pfister, H.; Fua, P.** | 2013 | *Reconstructing Loopy Curvilinear Structures Using Integer Programming* | CVPR 2013
  - Rejects the tree assumption and recovers networks **with cycles**, penalising spurious junctions and early terminations.
  - **The direct answer to this project's one-path-per-component ceiling.** **A3 · EB · high**
- **Dirnberger, M.; Kehl, T.; Neumann, A.** | 2015 | *NEFI: Network Extraction From Images* | Scientific Reports 5:15669 | doi:10.1038/srep15669
  - Segment, thin to a skeleton, read off graph vertices and edges to yield a weighted undirected planar graph.
  - The concrete raster-to-graph recipe this project lacks, and the path that preserves junctions. **A3 · EB · high**
- **Zhang, T.Y.; Suen, C.Y.** | 1984 | *A fast parallel algorithm for thinning digital patterns* | Communications of the ACM 27(3):236–239 | doi:10.1145/357994.358023
  - Connectivity-preserving unit-width skeleton — the standard alternative that retains junctions and loops by construction. **A3 · EC · high**
- **Lee, T.-C.; Kashyap, R.L.; Chu, C.-N.** | 1994 | *Building Skeleton Models via 3-D Medial Surface/Axis Thinning Algorithms* | CVGIP: Graphical Models and Image Processing 56(6):462–478 | doi:10.1006/cgip.1994.1042
  - The algorithm behind `skimage.morphology.skeletonize(method='lee')`. **A2 · EC · high**
- **Bai, X.; Latecki, L.J.; Liu, W.-Y.** | 2007 | *Skeleton Pruning by Contour Partitioning with Discrete Curve Evolution* | IEEE TPAMI 29(3):449–462 | doi:10.1109/TPAMI.2007.59
  - The standard answer to spurious skeleton spurs on noisy masks. **A2 · EB · high**
- **Zhou, Y.; Toga, A.W.** | 1999 | *Efficient Skeletonization of Volumetric Objects* | IEEE TVCG 5(3):196–209 | DOI unverified
  - Voxel-coding skeletonisation extracting centrelines as paths between coded clusters using distance fields — the classic distance-field-plus-shortest-path pipeline, already including the multi-branch connection step this project lacks. **A3 · EC · medium-high**
- **Blum, H.** | 1967 | *A Transformation for Extracting New Descriptors of Shape* | in *Models for the Perception of Speech and Visual Form*, MIT Press:362–380 | no DOI
  - The medial axis definition — needed to state precisely what this project's polyline approximates and where it diverges. **A2 · ED · high**
- **Borgefors, G.** | 1986 | *Distance transformations in digital images* | CVGIP 34(3):344–371 | DOI unverified
  - Chamfer approximations to Euclidean distance with ~2% error — the reason to prefer an exact transform when 1/EDT is a path cost. **A2 · EB · medium**
- **Douglas, D.H.; Peucker, T.K.** | 1973 | *Algorithms for the Reduction of the Number of Points Required to Represent a Digitized Line or its Caricature* | Cartographica 10(2):112–122 | doi:10.3138/FM57-6770-U75U-7727
  - The citable simplification with an explicit geometric error bound — the named upgrade path in this project's `ponytail:` debt comment. **A2 · EC · high**

## 7. Change detection and time series — what the Phase-1 screen is a version of

- **Zhu, Z.; Woodcock, C.E.** | 2014 | *Continuous change detection and classification of land cover using all available Landsat data* | Remote Sensing of Environment 144:152–171 | doi:10.1016/j.rse.2014.01.011
  - CCDC flags change when observed minus predicted exceeds a threshold on **three consecutive** observations.
  - The canonical ancestor of this project's ">= 2/3 recent years" persistence rule. **A3 · EB · high**
- **Verbesselt, J.; Zeileis, A.; Herold, M.** | 2012 | *Near real-time disturbance detection using satellite image time series* | Remote Sensing of Environment 123:98–108 | doi:10.1016/j.rse.2012.02.022
  - BFAST-Monitor models a stable history period and flags structural deviation in a monitoring period.
  - Formalises exactly the history-versus-monitoring split this project implements as 2018–2021 against 2023–2026, with a statistical test in place of a fixed z ≥ 1.0 cutoff. **A3 · EC · high**
- **Verbesselt, J.; Hyndman, R.; Newnham, G.; Culvenor, D.** | 2010 | *Detecting trend and seasonal changes in satellite image time series* | Remote Sensing of Environment 114(1):106–115 | doi:10.1016/j.rse.2009.08.014
  - Separates trend, seasonal and remainder; trend breaks indicate disturbance, seasonal breaks phenology; reliable above ~0.1 NDVI magnitude.
  - July-only compositing is this project's implicit substitute for a seasonal model, and the 0.1 figure is a usable detection-floor sanity check. **A3 · EB · high**
- **Kennedy, R.E.; Yang, Z.; Cohen, W.B.** | 2010 | *Detecting trends in forest disturbance and recovery using yearly Landsat time series: 1. LandTrendr* | Remote Sensing of Environment 114(12):2897–2910 | doi:10.1016/j.rse.2010.07.008
  - Piecewise-linear segmentation separating abrupt disturbance from slow recovery.
  - **Segment fitting is sign-agnostic**: it records a recovering corridor as a positive-slope segment instead of failing a fixed positive-disturbance threshold. This project's two-window difference is the crudest version of it. **A3 · EB · high**
- **Kennedy, R.E.; Yang, Z.; Gorelick, N.; Braaten, J.; Cavalcante, L.; Cohen, W.B.; Healey, S.** | 2018 | *Implementation of the LandTrendr Algorithm on Google Earth Engine* | Remote Sensing 10(5):691 | doi:10.3390/rs10050691
  - Removes "the platform cannot do it" as a justification for the simpler design, making the two-window choice an explicit scope decision. **A3 · EC · high**
- **Hamunyela, E.; Verbesselt, J.; Herold, M.** | 2016 | *Using spatial context to improve early detection of deforestation from Landsat time series* | Remote Sensing of Environment 172:126–138 | doi:10.1016/j.rse.2015.11.006
  - Normalises each pixel against neighbours above the 90th percentile, cutting median detection delay from 15 observations to 2.
  - **The closest published analogue to this project's control-ring z-score** and the primary methodological citation for that step. **A3 · EB · high**
- **Meroni, M.; Fasbender, D.; Rembold, F.; Atzberger, C.; Klisch, A.** | 2019 | *Near real-time vegetation anomaly detection with MODIS NDVI: Timeliness vs. accuracy and effect of anomaly computation options* | Remote Sensing of Environment 221:508–521 | doi:10.1016/j.rse.2018.11.041
  - Compares z-scores, non-exceedance probability and VCI; the best formulation depends on whether anomalies are averaged or thresholded, and early-window estimates carry large errors.
  - Interrogates this project's two core choices directly, and shows a z ≥ 1.0 cut from few years is the least stable part of the pipeline. **A3 · EB · high**
- **Zhu, Z.; Zhang, J.; Yang, Z.; Aljaddani, A.H.; Cohen, W.B.; Qiu, S.; Zhou, C.** | 2020 | *Continuous monitoring of land disturbance based on Landsat time series* | Remote Sensing of Environment 238:111116 | doi:10.1016/j.rse.2019.03.009
  - COLD detects disturbance without training data, **measured at 27% omission and 28% commission on the authors' Landsat evaluation against their reference data**.
  - An example of what one unsupervised screen achieved on one dataset. It is **not** a lower bound, a prediction for Mongolian track candidates, or an acceptable-error target for this project — those numbers do not transfer. Corrected 2026-09-24. **A2 · EB · high**
- **Reiche, J.; Hamunyela, E.; Verbesselt, J.; Hoekman, D.; Herold, M.** | 2018 | *Improving near-real time deforestation monitoring in tropical dry forests by combining dense Sentinel-1 time series with Landsat and ALOS-2 PALSAR-2* | Remote Sensing of Environment 204:147–161 | doi:10.1016/j.rse.2017.10.034
  - Quantifies the confirmation-versus-latency trade-off that a persistence rule silently makes. **A3 · EB · high**
- **Hansen, M.C.; Krylov, A.; Tyukavina, A.; Potapov, P.V.; Turubanova, S.; Zutta, B.; Ifo, S.; Margono, B.** | 2016 | *Humid tropical forest disturbance alerts using Landsat data* | Environmental Research Letters 11:034008 | doi:10.1088/1748-9326/11/3/034008
  - The GLAD alert system: flags loss and **explicitly does not distinguish human-induced from natural disturbance**.
  - The precedent for shipping a *screen* rather than a classifier, and for saying plainly that "surface disturbance" is not "informal road". **A2 · EB · high** (citation read directly from the GLAD dataset page)
- **Zhu, Z.** | 2017 | *Change detection using Landsat time series: A review* | ISPRS J. Photogrammetry and Remote Sensing 130:370–384 | doi:10.1016/j.isprsjprs.2017.06.013 — **A2 · ED · high**
- **Cohen, W.B.; Yang, Z.; Kennedy, R.** | 2010 | *…2. TimeSync — Tools for calibration and validation* | Remote Sensing of Environment 114:2911–2924 | doi:10.1016/j.rse.2010.07.010
  - The concrete protocol for building the interpreted reference trajectories this project currently lacks. **A2 · EB · high**

## 8. Sentinel-2 preprocessing, cloud masking and compositing

- **Roberts, D.; Mueller, N.; McIntyre, A.** | 2017 | *High-Dimensional Pixel Composites From Earth Observation Time Series* | IEEE TGRS 55(11):6254–6264 | doi:10.1109/TGRS.2017.2723896
  - The **geometric median** preserves the inter-band spectral relationship that a per-band median destroys.
  - **Applies here**: this project computes NDVI and BSI from a per-band median composite, so band ratios are formed from independently medianed bands. The operations do not commute. The **magnitude and downstream effect of that difference in this pipeline are unmeasured**. Note also that a geometric median is itself an estimate rather than an observed spectrum; a medoid selects an actual observation. "Never observed" alone is not the test of whether an estimator is useful. Corrected 2026-09-24. **A3 · EC · high**
- **Qiu, S.; Zhu, Z.; Olofsson, P.; Woodcock, C.E.; Jin, S.** | 2023 | *Evaluation of Landsat image compositing algorithms* | Remote Sensing of Environment 285:113375 | doi:10.1016/j.rse.2022.113375
  - Benchmarks compositing algorithms and reports that **performance depends on the compositing interval and the application, with no universally best compositor**.
  - The earlier summary here ("weighted scoring wins", "median ~70× cheaper") could **not be located in the official abstract** and is withdrawn pending an exact source and page. What survives is the weaker and safer claim: median compositing is a defensible choice whose ranking is task-dependent. Corrected 2026-09-24. **A3 · EB · high on citation, attribution of the specific figures UNRESOLVED**
- **Baetens, L.; Desjardins, C.; Hagolle, O.** | 2019 | *Validation of Copernicus Sentinel-2 Cloud Masks Obtained from MAJA, Sen2Cor, and FMask Processors…* | Remote Sensing 11(4):433 | doi:10.3390/rs11040433
  - On reference masks over 10 sites: **MAJA 91%, FMask 90%, Sen2Cor 84%**.
  - Concrete evidence that the default Sen2Cor scene-classification mask is the weakest of the three. **A3 · EB · high**
- **Skakun, S.; Wevers, J.; Brockmann, C.; Doxani, G.; et al.** | 2022 | *Cloud Mask Intercomparison eXercise (CMIX)* | Remote Sensing of Environment 274:112990 | doi:10.1016/j.rse.2022.112990
  - Algorithms agree on thick cloud but diverge sharply on thin and semi-transparent cloud.
  - Thin-cirrus leakage survives median compositing as a systematic NDVI depression — the unresolved risk for this screen. **A3 · EA · high**
- **Qiu, S.; Zhu, Z.; He, B.** | 2019 | *Fmask 4.0* | Remote Sensing of Environment 231:111205 | doi:10.1016/j.rse.2019.05.024 — **A3 · EA · high**
- **Zhu, Z.; Woodcock, C.E.** | 2012 | *Object-based cloud and cloud shadow detection in Landsat imagery* | Remote Sensing of Environment 118:83–94 | doi:10.1016/j.rse.2011.10.028
  - Cloud **shadow**, not cloud, is the failure mode that mimics NDVI loss in a bright steppe scene. **A2 · EB · high**
- **Pasquarella, V.J.; Brown, C.F.; Czerwinski, W.; Rucklidge, W.J.** | 2023 | *Comprehensive quality assessment of optical satellite imagery using weakly supervised video learning* | CVPR Workshops 2023:2125–2135 | doi:10.1109/CVPRW59228.2023.00206
  - The method behind Cloud Score+: continuous per-pixel usability rather than a binary mask, available natively in Earth Engine.
  - Lets observations be **weighted** instead of hard-masked — the cheapest available fix for the "fewer than two valid recent years" attrition problem. **A3 · EB · high**
- **Wright, N.; Duncan, J.M.A.; Callow, J.N.; Thompson, S.E.; George, R.J.** | 2024 | *CloudS2Mask* | Remote Sensing of Environment 306:114122 | doi:10.1016/j.rse.2024.114122
  - Outperforms s2cloudless on most surfaces **with reported exceptions including "Road" and "Urban"** — a named hazard for a pipeline whose targets are bare linear tracks. **A3 · EB · high**
- **Tarrio, K.; Tang, X.; Masek, J.G.; Claverie, M.; Ju, J.; Qiu, S.; Zhu, Z.; Woodcock, C.E.** | 2020 | *Comparison of cloud detection algorithms for Sentinel-2 imagery* | Science of Remote Sensing 2:100010 | doi:10.1016/j.srs.2020.100010 — **A3 · EB · high**
- **Qiu, S.; Lin, Y.; Shang, R.; Zhang, J.; Ma, L.; Zhu, Z.** | 2019 | *Making Landsat Time Series Consistent* | Remote Sensing 11(1):51 | doi:10.3390/rs11010051
  - **BRDF correction contributes most** to time-series inconsistency, cloud/shadow detection moderately, resampling least. BRDF is absent from this pipeline. **A3 · EB · high**
- **White, J.C.; Wulder, M.A.; Hobart, G.W.; et al.** | 2014 | *Pixel-Based Image Compositing for Large-Area Dense Time Series Applications and Science* | Canadian J. Remote Sensing 40(3):192–212 | doi:10.1080/07038992.2014.945827
  - Best-available-pixel scoring — the alternative to simply dropping a year, which is what the current valid-year rule does. **A3 · EC · high**
- **Main-Knorn, M.; Pflug, B.; Louis, J.; Debaecker, V.; Müller-Wilm, U.; Gascon, F.** | 2017 | *Sen2Cor for Sentinel-2* | Proc. SPIE 10427:1042704 | doi:10.1117/12.2278218 — the provenance citation for the L2A product and its scene-classification layer. **A3 · ED · high**
- **Hagolle, O.; Huc, M.; Villa Pascual, D.; Dedieu, G.** | 2015 | *A Multi-Temporal and Multi-Spectral Method to Estimate Aerosol Optical Thickness over Land…* | Remote Sensing 7(3):2668–2691 | doi:10.3390/rs70302668 — **A2 · EC · high**
- **Claverie, M.; Ju, J.; Masek, J.G.; Dungan, J.L.; Vermote, E.F.; Roger, J.-C.; Skakun, S.V.; Justice, C.** | 2018 | *The Harmonized Landsat and Sentinel-2 surface reflectance data set* | Remote Sensing of Environment 219:145–161 | doi:10.1016/j.rse.2018.09.002
  - The documented route to add Landsat observations if a recent year fails the valid-year test — but at 30 m, which makes the sub-pixel problem worse. **A3 · EB · high**

## 9. Dryland indices, bare soil, and the recovery-sign problem

- **Huete, A.R.** | 1988 | *A soil-adjusted vegetation index (SAVI)* | Remote Sensing of Environment 25(3):295–309 | doi:10.1016/0034-4257(88)90106-X
  - Shifting the origin of NIR–red space by a soil factor nearly eliminates soil-induced variation.
  - The canonical fix for the Gobi failure mode: at low cover a bare-track pixel and a low-cover pixel are not separable by NDVI alone. **A3 · EB · high**
- **Qi, J.; Chehbouni, A.; Huete, A.R.; Kerr, Y.H.; Sorooshian, S.** | 1994 | *A modified soil adjusted vegetation index* | Remote Sensing of Environment 48(2):119–126 | doi:10.1016/0034-4257(94)90134-1
  - MSAVI2 is computable from B04/B08 with no extra data and no tuning constant — the lowest-friction replacement for the Gobi site's NDVI screen. **A3 · EB · high**
- **Huete, A.R.; Jackson, R.D.** | 1987 | *Suitability of spectral indices for evaluating vegetation characteristics on arid rangelands* | Remote Sensing of Environment 23(2):213–232 | doi:10.1016/0034-4257(87)90038-1
  - The closest published analogue to this project's own note that NDVI is weak in the Gobi — citable evidence that the index choice, not the site, is the problem. **A3 · EB · high**
- **Huete, A.R.; Jackson, R.D.; Post, D.F.** | 1985 | *Spectral response of a plant canopy with different soil backgrounds* | Remote Sensing of Environment 17(1):37–53 | doi:10.1016/0034-4257(85)90111-7
  - With vegetation held constant and soils swapped, **no** greenness measure predicted the spectra. A change in substrate alone — which is what a graded track is — moves NDVI without any vegetation change. **A3 · EB · high**
- **Okin, G.S.; Roberts, D.A.; Murray, B.; Okin, W.J.** | 2001 | *Practical limits on hyperspectral vegetation discrimination in arid and semiarid environments* | Remote Sensing of Environment 77(2):212–225 | doi:10.1016/S0034-4257(01)00207-3
  - Simulated hyperspectral unmixing shows unreliable **vegetation-type** retrieval at low green cover, while cover *fraction* itself can sometimes still be estimated.
  - It does **not** establish that every vegetation index fails below 30% cover, nor that this detector must switch to soil brightness. Treat soil-adjusted indices as candidates for a controlled comparison, not as a forced substitution. Corrected 2026-09-24. **A2 · EC · high**
- **Rondeaux, G.; Steven, M.; Baret, F.** | 1996 | *Optimization of soil-adjusted vegetation indices* | Remote Sensing of Environment 55(2):95–107 | doi:10.1016/0034-4257(95)00186-7 — OSAVI, a defensible fixed constant. **A3 · EC · high**
- **Baret, F.; Jacquemoud, S.; Hanocq, J.F.** | 1993 | *The soil line concept in remote sensing* | Remote Sensing Reviews 7(1):65–82 | doi:10.1080/02757259309532166
  - Soil-line slope and intercept vary with soil type and moisture — an assumption inherited by any SAVI-family index and worth checking for Gobi substrates. **A2 · EC · high**
- **Evans, J.; Geerken, R.** | 2004 | *Discrimination between climate and human-induced dryland degradation* | Journal of Arid Environments 57(4):535–554 | doi:10.1016/S0140-1963(03)00121-6
  - Originates **RESTREND**: regress NDVI on rainfall and treat the residual trend as the human signal.
  - The direct answer to this project's sign problem: a raw NDVI-change mask conflates a wet year with real disturbance. **A3 · EB · high**
- **Wessels, K.J.; Prince, S.D.; Malherbe, J.; Small, J.; Frost, P.E.; VanZyl, D.** | 2007 | *Can human-induced land degradation be distinguished from the effects of rainfall variability?* | Journal of Arid Environments 68(2):271–297 | doi:10.1016/j.jaridenv.2006.05.015
  - Degradation is detectable only after removing the rainfall effect; RESTREND outperformed rain-use efficiency, which was unreliable. **A3 · EA · high**
- **Wessels, K.J.; van den Bergh, F.; Scholes, R.J.** | 2012 | *Limits to detectability of land degradation by trend analysis of vegetation index data* | Remote Sensing of Environment 125:10–22 | doi:10.1016/j.rse.2012.06.022
  - Degraded areas differ by only **~10–20%** in vegetation index, and simulated degradation ≥20% breaks the NDVI–rainfall relationship RESTREND depends on.
  - The honest ceiling on the whole approach: the correction fails exactly where disturbance is strongest. **A3 · EC · high**
- **Burrell, A.L.; Evans, J.P.; Liu, Y.** | 2017 | *Detecting dryland degradation using Time Series Segmentation and Residual Trend analysis (TSS-RESTREND)* | Remote Sensing of Environment 197:43–57 | doi:10.1016/j.rse.2017.05.018
  - Combines climate control with structural break detection — the method that can represent the recovering-corridor case as a breakpoint followed by an opposite-sign residual trend. **A3 · EB · high**
- **Prince, S.D.; Brown de Colstoun, E.; Kravitz, L.L.** | 1998 | *Evidence from rain-use efficiencies does not indicate extensive Sahelian desertification* | Global Change Biology 4(4):359–374 | doi:10.1046/j.1365-2486.1998.00158.x
  - After rainfall normalisation the claimed desertification signal largely disappeared — the failure mode a positive-disturbance mask is exposed to. **A2 · EB · high**
- **Herrmann, S.M.; Anyamba, A.; Tucker, C.J.** | 2005 | *Recent trends in vegetation dynamics in the African Sahel and their relationship to climate* | Global Environmental Change 15(4):394–404 | doi:10.1016/j.gloenvcha.2005.08.004 — **A2 · EB · high**
- **Hein, L.; de Ridder, N.** | 2006 | *Desertification in the Sahel: a reinterpretation* | Global Change Biology 12(5):751–758 | doi:10.1111/j.1365-2486.2006.01135.x — with the reply **Prince, Wessels, Tucker & Nicholson** | 2007 | doi:10.1111/j.1365-2486.2007.01356.x
  - A published dispute over whether rainfall normalisation reveals or hides degradation: the correction step is itself contested. **A2 · ED · high**
- **Crist, E.P.; Cicone, R.C.** | 1984 | *A physically-based transformation of Thematic Mapper data — the TM Tasseled Cap* | IEEE TGRS GE-22(3):256–263 | doi:10.1109/TGRS.1984.350619
  - Brightness is the axis a compacted track actually moves along, and a brightness-change screen is **sign-stable** in a way an NDVI-change screen is not. **A3 · EB · high**
- **Shi, T.; Xu, H.** | 2019 | *Derivation of tasseled cap transformation coefficients for Sentinel-2 MSI **at-sensor** reflectance data* | IEEE JSTARS 12(10):4038–4048 | doi:10.1109/JSTARS.2019.2938388
  - Coefficients are derived for **at-sensor** reflectance. This repository uses **surface** reflectance (`S2_SR_HARMONIZED`), so the coefficients do not transfer without a compatible source or a tested conversion. Brightness is **not** established here as a directionally invariant marker of compaction or recovery across substrates. Corrected 2026-09-24. **A2 · ungraded on transfer · high on citation**
- **Rasul, A.; Balzter, H.; Ibrahim, G.R.F.; Hameed, H.M.; Wheeler, J.; Adamu, B.; et al.** | 2018 | *Applying built-up and bare-soil indices from Landsat 8 to cities in dry climates* | Land 7(3):81 | doi:10.3390/land7030081
  - Introduces DBI and DBSI **because indices developed for humid climates misclassify in arid terrain**; 93% and 92% accuracy in Erbil. **A3 · EB · high**
- **Zha, Y.; Gao, J.; Ni, S.** | 2003 | *Use of normalized difference built-up index in automatically mapping urban areas from TM imagery* | IJRS 24(3):583–594 | doi:10.1080/01431160304987 — validated on a humid city, not a desert. **A2 · EB · high**
- **Rikimaru, A.; Roy, P.S.; Miyatake, S.** | 2002 | *Tropical forest cover density mapping* | Tropical Ecology 43(1):39–47 | DOI unverified — commonly cited as the origin of the BSI formulation; the original context is tropical forest, not desert. **A2 · EC · medium**
- **Asner, G.P.; Heidebrecht, K.B.** | 2002 | *Spectral unmixing of vegetation, soil and dry carbon cover in arid regions* | IJRS 23(19):3939–3958 | doi:10.1080/01431160110115960
  - How much photosynthetic / non-photosynthetic / soil separation survives with broad bands rather than hyperspectral. **A3 · EB · high**
- **Okin, G.S.** | 2007 | *Relative spectral mixture analysis — a multitemporal index of total vegetation cover* | Remote Sensing of Environment 106(4):467–479 | doi:10.1016/j.rse.2006.09.018
  - Removes the biggest practical blocker to unmixing here: no validated Mongolian soil endmember library is required. **A3 · EC · high**
- **Guerschman, J.P.; Scarth, P.F.; McVicar, T.R.; et al.** | 2015 | *Assessing the effects of site heterogeneity and soil properties when unmixing…* | Remote Sensing of Environment 161:12–26 | doi:10.1016/j.rse.2015.01.021
  - Validated against 1171 field observations: bare-soil fraction estimates are themselves soil-type biased — expect a Gobi-specific bias, not a universal threshold. **A2 · EA · high**
- **Guerschman, J.P.; Hill, M.J.; Renzullo, L.J.; et al.** | 2009 | *Estimating fractional cover of PV, NPV and bare soil…* | Remote Sensing of Environment 113(5):928–945 | doi:10.1016/j.rse.2009.01.006
  - The index pairing (greenness plus a SWIR dry-matter term) needed because NDVI alone cannot see non-photosynthetic material. **A2 · EB · high**
- **Roberts, D.A.; Gardner, M.; Church, R.; Ustin, S.; Scheer, G.; Green, R.O.** | 1998 | *Mapping chaparral in the Santa Monica Mountains using multiple endmember spectral mixture models* | Remote Sensing of Environment 65(3):267–279 | doi:10.1016/S0034-4257(98)00037-6 — **A1 · EB · high**
- **Keshava, N.; Mustard, J.F.** | 2002 | *Spectral unmixing* | IEEE Signal Processing Magazine 19(1):44–57 | doi:10.1109/79.974727 — **A2 · ED · high**
- **McGwire, K.** *(co-authors unverified)* | 2000 | *Hyperspectral mixture modeling for quantifying sparse vegetation cover in arid environments* | Remote Sensing of Environment 72(3):360–374 | doi:10.1016/S0034-4257(99)00112-1 — **A2 · EC · medium**
- **Zhao, H.; Chen, X.** | 2005 | *Use of normalized difference bareness index…* | IGARSS 2005:1666–1668 | doi:10.1109/IGARSS.2005.1526319 — thermal-dependent, so not transferable to Sentinel-2. **A1 · EC · high**
- **Nedkov, R.** | 2017 | *Orthogonal transformation of segmented images from the satellite Sentinel-2* | C. R. Acad. Bulg. Sci. 70(5):687–692 | DOI unverified — temperate calibration; cross-check only. **A1 · EC · medium**

## 10. Data products and resolution limits

- **Drusch, M.; Del Bello, U.; Carlier, S.; Colin, O.; Fernandez, V.; Gascon, F.; Hoersch, B.; Isola, C.; Laberinti, P.; Martimort, P.; Meygret, A.; Spoto, F.; Sy, O.; Marchese, F.; Bargellini, P.** | 2012 | *Sentinel-2: ESA's Optical High-Resolution Mission for GMES Operational Services* | Remote Sensing of Environment 120:25–36 | doi:10.1016/j.rse.2011.11.026
  - Defines the 13 bands and the **10 m / 20 m / 60 m** native sampling. The 10 m visible-NIR against 20 m shortwave-infrared split is exactly why a bare-soil index using shortwave is coarser than the nominal 10 m. **A3 · EC · high**
- **Brown, C.F.; Brumby, S.P.; Guzder-Williams, B.; Birch, T.; Hyde, S.B.; Mazzariello, J.; et al.** | 2022 | *Dynamic World, Near real-time global 10 m land use land cover mapping* | Scientific Data 9:251 | doi:10.1038/s41597-022-01307-4
  - Per-scene class **probabilities** over user-specified date ranges rather than annual hard labels. The canonical citation for this project's confound layer. **A3 · EB · high**
- **Venter, Z.S.; Barton, D.N.; Chakraborty, T.; Simensen, T.; Singh, G.** | 2022 | *Global 10 m Land Use Land Cover Datasets: A Comparison of Dynamic World, World Cover and Esri Land Cover* | Remote Sensing 14(16):4101 | doi:10.3390/rs14164101
  - Overall accuracy Esri 75% > Dynamic World 72% > WorldCover 65%, but the worst classes were **grass 34%, shrub/scrub 47%, bare ground 57%**.
  - **The strongest challenge in this review**: this project uses Dynamic World to gate confounds in a steppe whose dominant classes are exactly those three. Built 83% and water 92% are fine; grass and bare are not. **A3 · EA · high**
- **Zanaga, D.; Van De Kerchove, R.; Daems, D.; et al.** | 2022 | *ESA WorldCover 10 m 2021 v200* | Zenodo | doi:10.5281/zenodo.7254221
  - The product the design document rejects. The rejection is **half right**: a 2020 v100 release also exists (doi:10.5281/zenodo.5571936), so WorldCover is two epochs, though ESA warns the versions are not directly comparable for change. **A3 · EB · high**
- **Welch, R.** | 1982 | *Spatial resolution requirements for urban studies* | IJRS 3(2):139–146 | doi:10.1080/01431168208948387
  - High-contrast **linear** objects are detectable below the nominal pixel size while areal objects are not.
  - Supports restating this project's hedge: "sub-pixel" bears on *identification*, not *detection* — a distinction the design document currently collapses. **A2 · EC · high**
- **Löw, F.; Duveiller, G.** | 2014 | *Defining the Spatial Resolution Requirements for Crop Identification Using Optical Remote Sensing* | Remote Sensing 6(9):9034–9063 | doi:10.3390/rs6099034
  - A quantitative framework trading pixel size against pixel purity for a target object size, demonstrated over **Central Asia**.
  - Lets this project compute its own recoverable-width threshold rather than assert one. **A2 · EC · high**
- **Atkinson, P.M.** | 2005 | *Sub-pixel Target Mapping from Soft-classified, Remotely Sensed Imagery* | PE&RS 71(7):839–846 | doi:10.14358/pers.71.7.839
  - Sub-pixel is not a synonym for invisible: arrangement within a mixed pixel is partly recoverable. **A2 · EC · high**
- **Thornton, M.W.; Atkinson, P.M.; Holland, D.A.** | 2007 | *A linearised pixel-swapping method for mapping rural linear land cover features…* | Computers & Geosciences 33(10):1261–1272 | doi:10.1016/j.cageo.2007.05.010
  - **Narrowness plus linearity is itself exploitable prior information** — the same structural argument this project makes for corridors, applied successfully to single narrow features. **A3 · EC · high**
- **Thornton, M.W.; Atkinson, P.M.; Holland, D.A.** | 2006 | *Sub-pixel mapping of rural land cover objects…* | IJRS 27(3):473–491 | doi:10.1080/01431160500207088 — **A1 · EC · high**
- **Meijer, J.R.; Huijbregts, M.A.J.; Schotten, K.C.G.J.; Schipper, A.M.** | 2018 | *Global patterns of current and future road infrastructure* | Environmental Research Letters 13(6):064006 | doi:10.1088/1748-9326/aabd42
  - GRIP from ~60 datasets across 222 countries yields >21 million km — **two to three times** the length in the previously best global datasets, which are typically outdated or spatially biased.
  - The natural baseline layer to difference against when claiming a detected corridor is "informal". **A3 · EA · high**

## 11. Evaluation metrics for extracted linear features

- **Wiedemann, C.; Heipke, C.; Mayer, H.; Jamet, O.** | 1998 | *Empirical Evaluation of Automatically Extracted Road Axes* | in *Empirical Evaluation Methods in Computer Vision*, IEEE CS Press:172–187 | DOI unverified
  - Establishes **completeness** (reference inside a buffer around the extraction), **correctness** (extraction inside a buffer around the reference), plus quality, redundancy, RMS difference and gap statistics.
  - THE canonical buffer-based evaluation: this project's recall and precision of centreline pixels inside a 2-pixel band is a raster reimplementation of completeness and correctness, and should be named as such. **A3 · EB · high on authors/year/pages; MEDIUM on the book title** ("Methods" versus the widely cited "Techniques" — resolve before citing)
- **Heipke, C.; Mayer, H.; Wiedemann, C.; Jamet, O.** | 1997 | *Evaluation of Automatic Road Extraction* | IAPRS XXXII(3-4W2):47–56 | [PDF](https://www.unibw.de/visual-computing/publikationen-vortraege/publikationen-1/pdf-dateien-publikationen/isprs-1997-xxxii-part3-4w2.pdf)
  - States explicitly that **the less tolerant the matching, the less complete but more accurate the result appears** — the sentence the 2-pixel choice must be defended against. **A3 · EC · high**
- **Wiedemann, C.** | 2003 | *External Evaluation of Road Networks* | ISPRS Archives XXXIV(3/W8) | [PDF](https://www.isprs.org/proceedings/XXXIV/3-W8/papers/pia03_s4p2.pdf)
  - Formalises completeness, correctness and **redundancy**, noting summary measures are only valid assuming no redundancy.
  - Supplies the caveat a dilation-band pixel score silently violates: one extracted pixel can be matched by several reference pixels inside the band. **A3 · EC · high**
- **Mayer, H.; Hinz, S.; Bacher, U.; Baltsavias, E.** | 2006 | *A Test of Automatic Road Extraction Approaches* | IAPRS 36(3):209–214 | [PDF](https://www.isprs.org/proceedings/xxxvi/part3/singlepapers/O_15.pdf)
  - The EuroSDR benchmark giving the empirical range published systems actually achieve, so this project's numbers can be positioned rather than reported in a vacuum. **A3 · EB · high**
- **Citraro, L.; Koziński, M.; Fua, P.** | 2020 | *Towards Reliable Evaluation of Algorithms for Road Network Reconstruction from Aerial Images* | ECCV 2020:703–719 | doi:10.1007/978-3-030-58604-1_42
  - Existing connectivity metrics **rank the same algorithms inconsistently** because design flaws make them blind to whole classes of error.
  - The strongest available warning that a lone tolerance-based score can miss entire error classes. **A3 · EB · high**
- **Biagioni, J.; Eriksson, J.** | 2012 | *Inferring Road Maps from Global Positioning System Traces: Survey and Comparative Evaluation* | Transportation Research Record 2291:61–71 | doi:10.3141/2291-08
  - Introduces **TOPO**: sample seed vertices, match into the proposal graph, compare reachable sub-graphs.
  - The standard topology-aware alternative that would penalise disconnections a pixel-band score cannot see. **A3 · EB · high**
- **Shit, S.; Paetzold, J.C.; Sekuboyina, A.; Ezhov, I.; Unger, A.; Zhylka, A.; Pluim, J.; et al.** | 2021 | *clDice — A Novel Topology-Preserving Loss Function for Tubular Structure Segmentation* | CVPR 2021:16555–16564 | doi:10.1109/CVPR46437.2021.01629
  - Computed on the intersection of masks with their skeleta, with a topology-preservation guarantee; usable as a **metric**, not only a loss. **A3 · EB · high**
- **Van Etten, A.; Lindenbaum, D.; Bacastow, T.M.** | 2018 | *SpaceNet: A Remote Sensing Dataset and Challenge Series* | arXiv:1807.01232
  - The citable anchor for **APLS**; note the metric's original write-up is an informal blog post, which is a weak citation on its own. **A2 · ED · high, preprint**
- **Van Etten, A.** | 2019 | *City-scale Road Extraction from Satellite Imagery (CRESI)* | arXiv:1904.09901
  - Reports **APLS 0.73 and TOPO 0.58** together — direct precedent for reporting a graph metric alongside a mask metric, the same two-layer split this project already makes. **A3 · EC · high**

## 12. Validation design, reference-data quality and research integrity

- **Olofsson, P.; Foody, G.M.; Herold, M.; Stehman, S.V.; Woodcock, C.E.; Wulder, M.A.** | 2014 | *Good practices for estimating area and assessing accuracy of land change* | Remote Sensing of Environment 148:42–57 | doi:10.1016/j.rse.2014.02.015
  - Sampling design, response design, and unbiased area estimation with confidence intervals, warning explicitly that map-counted change area is biased.
  - **Non-negotiable here**: a count of large connected components reported without a probability sample and an error-adjusted area is not a defensible number. **A3 · EA · high**
- **Stehman, S.V.; Czaplewski, R.L.** | 1998 | *Design and Analysis for Thematic Map Accuracy Assessment: Fundamental Principles* | Remote Sensing of Environment 64:331–344 | doi:10.1016/S0034-4257(98)00010-8
  - A scoring script is not an accuracy assessment until its sampling and response designs are declared. **A3 · EA · high**
- **Stehman, S.V.; Foody, G.M.** | 2019 | *Key issues in rigorous accuracy assessment of land cover products* | Remote Sensing of Environment 231:111199 | doi:10.1016/j.rse.2019.05.018
  - Corridors are a **rare class** over the steppe: simple random sampling will find almost no positives, so stratification must be pre-specified. **A3 · EA · high**
- **Stehman, S.V.** | 2009 | *Sampling designs for accuracy assessment of land cover* | IJRS 30(20):5243–5272 | doi:10.1080/01431160903131000 — **A2 · EA · high**
- **Olofsson, P.; Foody, G.M.; Stehman, S.V.; Woodcock, C.E.** | 2013 | *Making better use of accuracy data in land change studies* | Remote Sensing of Environment 129:122–131 | doi:10.1016/j.rse.2012.10.031 — **A2 · EB · high**
- **Foody, G.M.** | 2010 | *Assessing the accuracy of land cover change with imperfect ground reference data* | Remote Sensing of Environment 114(10):2271–2285 | doi:10.1016/j.rse.2010.05.003
  - 10% reference error produced an **18.5% under-estimate** of producer's accuracy with independent errors but a **12.3% over-estimate** when errors were correlated.
  - A digitised reference centreline carries positional and completeness error, and this quantifies how far that can move reported recall and precision in either direction. **A3 · EC · high**
- **Foody, G.M.** | 2002 | *Status of land cover classification accuracy assessment* | Remote Sensing of Environment 80(1):185–201 | doi:10.1016/S0034-4257(01)00295-4
  - Names the untenable **perfect co-registration** assumption — precisely what a 2-pixel tolerance silently absorbs. **A2 · EA · high**
- **Roberts, D.R.; Bahn, V.; Ciuti, S.; Boyce, M.S.; Elith, J.; Guillera-Arroita, G.; Hauenstein, S.; et al.** | 2017 | *Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure* | Ecography 40(8):913–929 | doi:10.1111/ecog.02881
  - Ignoring structure seriously underestimates predictive error; block cross-validation is nearly universally more appropriate for prediction to new data.
  - The standard citation for why holding out a **whole site** is the only honest generalisation test here. **A3 · EC · high**
- **Ploton, P.; Mortier, F.; Réjou-Méchain, M.; Barbier, N.; Picard, N.; Rossi, V.; Dormann, C.F.; et al.** | 2020 | *Spatial validation reveals poor predictive performance of large-scale ecological mapping models* | Nature Communications 11:4540 | doi:10.1038/s41467-020-18321-y
  - Non-spatial validation suggested the model explained more than half the variation; spatial validation revealed **quasi-null** predictive power.
  - The most vivid demonstration that in-site scores can be near-meaningless out-of-site — the exact risk the held-out site exists to expose. **A3 · EB · high**
- **Wadoux, A.M.J.-C.; Heuvelink, G.B.M.; de Bruin, S.; Brus, D.J.** | 2021 | *Spatial cross-validation is not the right way to evaluate map accuracy* | Ecological Modelling 457:109692 | doi:10.1016/j.ecolmodel.2021.109692
  - The necessary counterweight: present the held-out site as a **generalisation test**, not an unbiased accuracy estimate. **A3 · EC · high**
- **de Bruin, S.; Brus, D.J.; Heuvelink, G.B.M.; van Ebbenhorst Tengbergen, T.; Wadoux, A.M.J.-C.** | 2022 | *Dealing with clustered samples for assessing map accuracy by cross-validation* | Ecological Informatics 69:101665 | doi:10.1016/j.ecoinf.2022.101665 — **A2 · EC · high**
- **Meyer, H.; Pebesma, E.** | 2021 | *Predicting into unknown space? Estimating the area of applicability of spatial prediction models* | Methods in Ecology and Evolution 12(9):1620–1633 | doi:10.1111/2041-210X.13650
  - A defensible way to state the envelope in which reported scores mean anything, rather than implying global validity. **A2 · EC · high**
- **Lipsitch, M.; Tchetgen Tchetgen, E.; Cohen, T.** | 2010 | *Negative Controls: A Tool for Detecting Confounding and Bias in Observational Studies* | Epidemiology 21(3):383–388 | doi:10.1097/EDE.0b013e3181d61eeb
  - The methodological origin of the term, and the **conditions under which a negative control is actually informative** — it only detects bias it shares a confounding pathway with.
  - The citation for this project's road-free falsification gate, and the standard that gate must meet. **A2 · ED · high**
- **Simmons, J.P.; Nelson, L.D.; Simonsohn, U.** | 2011 | *False-Positive Psychology* | Psychological Science 22(11):1359–1366 | doi:10.1177/0956797611417632
  - Undisclosed flexibility pushes real false-positive rates far above nominal. Every threshold here is a researcher degree of freedom. **A3 · EB · high**
- **Gelman, A.; Loken, E.** | 2014 | *The Statistical Crisis in Science* | American Scientist 102(6):460 | doi:10.1511/2014.111.460
  - **Potential** comparisons suffice to inflate error rates: tuning a threshold after seeing which corridors light up is a forking path even if one analysis is reported. (The working-paper title is "The garden of forking paths".) **A3 · ED · high**
- **Nosek, B.A.; Ebersole, C.R.; DeHaven, A.C.; Mellor, D.T.** | 2018 | *The preregistration revolution* | PNAS 115(11):2600–2606 | doi:10.1073/pnas.1708274114
  - Gives this project's "pre-registered gate" its meaning **and its standard**: a timestamped, uneditable record, not a threshold written in a design document. **A3 · ED · high**
- **Chambers, C.D.; Tzavella, L.** | 2021 | *The past, present and future of Registered Reports* | Nature Human Behaviour 6:29–42 | doi:10.1038/s41562-021-01193-7 — **A2 · EB · high**
- **Parker, T.H.; Forstmeier, W.; Koricheva, J.; Fidler, F.; et al.** | 2016 | *Transparency in Ecology and Evolution: Real Problems, Real Solutions* | Trends in Ecology & Evolution 31(9):711–719 | doi:10.1016/j.tree.2016.07.002
  - Closer to this project's situation than the psychology literature: how to pre-register when analysing an existing archive. **A2 · ED · high**
- **Munafò, M.R.; Nosek, B.A.; Bishop, D.V.M.; et al.** | 2017 | *A manifesto for reproducible science* | Nature Human Behaviour 1:0021 | doi:10.1038/s41562-016-0021 — **A2 · ED · high**
- **Nüst, D.; Pebesma, E.** | 2021 | *Practical Reproducibility in Geography and Geosciences* | Annals of the AAG 111(5):1300–1310 | doi:10.1080/24694452.2020.1806028
  - The operational counterpart to pre-registration: an Earth-observation claim is checkable only if code and product versions are pinned and archived. **A2 · ED · high**
- **Sui, D.; Kedron, P.** | 2021 | *Reproducibility and Replicability in the Context of the Contested Identities of Geography* | Annals of the AAG 111(5):1275–1283 | doi:10.1080/24694452.2020.1806024 — **A1 · ED · high**
- **Gorelick, N.; Hancher, M.; Dixon, M.; Ilyushchenko, S.; Thau, D.; Moore, R.** | 2017 | *Google Earth Engine: Planetary-scale geospatial analysis for everyone* | Remote Sensing of Environment 202:18–27 | doi:10.1016/j.rse.2017.06.031
  - The mandatory platform citation, and the source for the lazy-evaluation semantics that make results sensitive to scale and projection defaults this project should pin explicitly. **A3 · ED · high**
- **Tamiminia, H.; Salehi, B.; Mahdianpari, M.; Quackenbush, L.; Adeli, S.; Brisco, B.** | 2020 | *Google Earth Engine for geo-big data applications: A meta-analysis and systematic review* | ISPRS J. Photogrammetry and Remote Sensing 164:152–170 | doi:10.1016/j.isprsjprs.2020.04.001 — **A2 · ED · high**

## 13. Reference data — OpenStreetMap completeness, ghost roads, and weak labels

- **Barrington-Leigh, C.P.; Millard-Ball, A.** | 2017 | *The world's user-generated road map is more than 80% complete* | PLoS ONE 12(8):e0180698 | doi:10.1371/journal.pone.0180698 (correction 2019, doi:10.1371/journal.pone.0224742)
  - Two independent methods put OSM at ~83% complete globally; more than 40% of countries fully mapped; and completeness has a **U-shaped relationship with population density** — both sparsely populated areas and dense cities are best mapped.
  - **Cuts both ways for this project.** It quantifies incompleteness, but the U-shape weakens a naive "Mongolia is sparse therefore OSM is poor there" argument. Extract the Mongolia-specific value from the supplementary data rather than citing the global average. **A3 · EA · high**
- **Poley, L.G.; Schuster, R.; Smith, W.; Ray, J.C.** | 2022 | *Identifying differences in roadless areas in Canada based on global, national, and regional road datasets* | Conservation Science and Practice | doi:10.1111/csp2.12656
  - Global and national road datasets contained on average only **11–14%** of the roads in regional or volunteered data, worst in less-developed areas.
  - The most concrete number for "any reference layer you condition on is a small subset of reality" — and it inverts the usual framing, since volunteered data often has **more** roads than authoritative global layers. **A3 · EB · high**
- **Engert, J.E.; Campbell, M.J.; Cinner, J.E.; Ishida, Y.; Sloan, S.; Supriatna, J.; Alamgir, M.; Cislowski, J.; Laurance, W.F.** | 2024 | *Ghost roads and the destruction of Asia-Pacific tropical forests* | Nature 629(8011):370–375 | doi:10.1038/s41586-024-07303-5 (correction doi:10.1038/s41586-024-07535-5)
  - ~7,000 hours of mapping over 1.42 million plots found roads **3–6.6× longer** than in leading datasets, and ghost-road density was the strongest correlate of forest loss, almost always preceding it.
  - The headline quantified-extent citation and the strongest justification for building a screening tool at all — but it is tropical forest, not drylands. **A2–3 · EB · high**
- **Herfort, B.; Lautenbach, S.; Porto de Albuquerque, J.; Anderson, J.; Zipf, A.** | 2023 | *A spatio-temporal analysis investigating completeness and inequalities of global urban building data in OpenStreetMap* | Nature Communications | doi:10.1038/s41467-023-39698-6
  - Coverage bias is **structural and patterned**, not random noise, and analyses ignoring it will mislead. Caveat: measures buildings, not roads. **A3 · EA · high**
- **Senaratne, H.; Mobasheri, A.; Ali, A.L.; Capineri, C.; Haklay, M.** | 2017 | *A review of volunteered geographic information quality assessment methods* | IJGIS 31(1):139–167 | doi:10.1080/13658816.2016.1189556
  - Splits quality assessment into **extrinsic** (compare against an external reference) and **intrinsic** (indicators from the data itself, where no reference exists).
  - The vocabulary for arguing that in Mongolia no trustworthy extrinsic reference exists, so intrinsic assessment is the only honest option. **A3 · EA · high**
- **Usmani, M.; Bovolo, F.; Napolitano, M.** | 2023 | *Remote Sensing and Deep Learning to Understand Noisy OpenStreetMap* | Remote Sensing 15(18):4639 | doi:10.3390/rs15184639
  - Models trained on crowdsourced annotations misclassify because of label noise, and quality is inconsistent **outside metropolitan areas**. **A3 · EB · high**
- **Wu, S.; Du, C.; Chen, H.; Xu, Y.; Guo, N.; Jing, N.** | 2019 | *Road Extraction from Very High Resolution Images Using Weakly labeled OpenStreetMap Centerline* | IJGI 8(11):478 | doi:10.3390/ijgi8110478
  - Names a second OSM defect beyond incompleteness — **geometric under-specification**: centrelines carry no width, so OSM could not supply matching labels for a corridor output even where complete. **A3 · EB · high**
- **Fobi, S.; Conlon, T.; Taneja, J.; Modi, V.** | 2020 | *Learning to segment from misaligned and partial labels* | ACM COMPASS 2020 | arXiv:2005.13180
  - Formalises "OSM labels are partial and misaligned" as a learning problem with a published remedy — **the most citable counter-argument to a blanket OSM deferral**, since incompleteness can be modelled rather than only avoided. **A3 · EB · high**
- **Henry, C.; Fraundorfer, F.** | 2025 | *Worldwide High-Fidelity Road Extraction from Aerial and Satellite Imagery Enabled by Low-Fidelity OpenStreetMap Labels* | LNCS | doi:10.1007/978-3-031-85187-2_19
  - The "use OSM as a prompt, not a gate" pattern — the middle path between full deferral and naive conditioning. **A3 · EC · high on citation, medium on finding**
- **Meng, S.; Di, Z.; Yang, S.; Wang, Y.** | 2023 | *Large-scale Weakly Supervised Learning for Road Extraction from Satellite Imagery* | arXiv:2309.07823 — OSM as weak pretraining signal, plus a cross-region generalisation warning. **A3 · EC · high on citation, unreplicated**
- **Ibisch, P.L.; Hoffmann, M.T.; Kreft, S.; Pe'er, G.; Kati, V.; Biber-Freudenberger, L.; DellaSala, D.A.; Vale, M.M.; Hobson, P.R.; Selva, N.** | 2016 | *A global map of roadless areas and their conservation status* | Science 354(6318):1423–1427 | doi:10.1126/science.aaf7166
  - ~80% of land is roadless but fragmented into ~600,000 patches. **Built on OSM**, so this project's premise is an argument that the map overstates roadlessness. **A2 · EC · high**
- **Hughes, A.C.** | 2017 | *Global roadless areas: Hidden roads* | Science 355(6332):1381 | doi:10.1126/science.aam6995 — with the reply **Ibisch & Selva** | 2017 | Science 355(6332):1382 | doi:10.1126/science.aam9830
  - The explicit published statement of this project's premise, and the reason to cite Ibisch with a caveat. **A2 · ED · high**
- **Laurance, W.F.; Clements, G.R.; Sloan, S.; et al.** | 2014 | *A global strategy for road building* | Nature 513:229–232 | doi:10.1038/nature13717 (corrigendum doi:10.1038/nature13876) — **A2 · EC · high**
- **Randhawa, S.; Aygün, E.; Randhawa, G.; Herfort, B.; Lautenbach, S.; Zipf, A.** | 2025 | *Paved or unpaved? A deep learning derived road surface global dataset from Mapillary street-view imagery* | ISPRS J. Photogrammetry and Remote Sensing 223:362–374 | doi:10.1016/j.isprsjprs.2025.02.020
  - A potential independent paved/unpaved label source, though street-view coverage in rural Mongolia is likely near zero — check before relying on it. **A2 · EB · high**
- **Minaei, M.** | 2020 | *Evolution, density and completeness of OpenStreetMap road networks in developing countries: The case of Iran* | Applied Geography 119:102246 | doi:10.1016/j.apgeog.2020.102246 — the closest template for what an OSM completeness assessment in Mongolia would look like. **A2 · EB · high on citation, medium on finding**
- **Moradi, M.; Roche, S.; Mostafavi, M.A.** | 2021 | *Exploring five indicators for the quality of OpenStreetMap road networks: Québec* | Geomatica 75(4):1–31 | doi:10.1139/geomat-2021-0012 — the recipe for bounding OSM quality with no authoritative reference. **A2 · EB · high**
- **Girres, J.-F.; Touya, G.** | 2010 | *Quality Assessment of the French OpenStreetMap Dataset* | Transactions in GIS | doi:10.1111/j.1467-9671.2010.01203.x
  - OSM quality is **heterogeneous within a single country**, so a national completeness figure cannot license region-level decisions. **A2 · EB · high**
- **Neis, P.; Zielstra, D.; Zipf, A.** | 2011 | *The Street Network Evolution of Crowdsourced Maps: OpenStreetMap in Germany 2007–2011* | Future Internet 4(1):1–21 | doi:10.3390/fi4010001
  - The saturation framing: a layer can look stable and complete while whole unseeded classes remain unmapped. Recency of edits is not evidence of completeness. **A2 · EB · high**
- **Zhang, Y.; Li, X.; Wang, A.; Bao, T.; Tian, S.** | 2015 | *Density and diversity of OpenStreetMap road networks in China* | J. Urban Management 4(2):135–146 | doi:10.1016/j.jum.2015.10.001 — **A2 · EB · high**
- **Funke, S.; Schirrmeister, R.T.; Storandt, S.** | 2015 | *Automatic extrapolation of missing road network data in OpenStreetMap* | venue **unverified**, no DOI found
  - The "condition on OSM topology to guess unseeded roads" family this project is deferring — cite as the approach being rejected, because it assumes the existing network is representative. **A2 · ED · medium — verify before citing**
- **Sehra, S.S.; Singh, J.; Rai, H.S.** | 2013 | *Assessment of OpenStreetMap Data — A Review* | IJCA 76(16):17–20 | arXiv:1309.6608 — low-tier venue; entry point only. **A1 · ED · high on citation, non-authoritative**
- **Kamalu, J.; Choi, B.** | 2020 | *Road Mapping in Low Data Environments with OpenStreetMap* | arXiv:2006.07993 — framing only, weak as evidence. **A2 · ED · low authority**

## 14. Linear non-road confounds — the fabrication failure class

- **Queiroz, G.L.; McDermid, G.J.; Rahman, M.M.; Linke, J.** | 2020 | *The Forest Line Mapper: A Semi-Automated Tool for Mapping Linear Disturbances in Forests* | Remote Sensing 12(24):4176 | doi:10.3390/rs12244176
  - Predicts centreline and footprint for "roads, pipelines, seismic lines, and power lines" as **one detectable class**.
  - From the authors' own framing: this project's confound set is not a corner case, it is what geometry-driven linear extractors actually detect. **A3 · EB · high**
- **Nagel, A.M.; Webster, A.; Henry, C.J.; Storie, C.D.; Lopez Sanchez, I.A.; Tsui, O.; Duffe, J.A.; Dean, A.** | 2024 | *Automated Linear Disturbance Mapping via Semantic Segmentation of Sentinel-2 Imagery* | arXiv:2409.12817
  - Deep segmentation of **Sentinel-2** for boreal linear disturbances treats roads, seismic lines and pipelines together, and reports thin disturbances as the hard case at this resolution.
  - The direct published precedent for this project's fabrication failure, at the same resolution: at 10 m the model cannot separate road from seismic line. **A3 · EC · high, preprint**
- **Liu, Y.; Chen, X.; Yang, Y.; Sun, C.; Zhang, S.** | 2016 | *Automated Extraction and Mapping for Desert Wadis from Landsat Imagery in Arid West Asia* | Remote Sensing 8(3):246 | doi:10.3390/rs8030246
  - Wadi extraction reaches ~95% accuracy, but commission errors occur mainly in non-wadi features falsely enhanced by water indices — **specifically roads** — and wadis have inconspicuous spectral contrast, causing frequent false alarms.
  - **The mirror image of this project's river-bank fabrication, in an arid landscape.** Dry drainage channels and unpaved tracks are interchangeable at moderate resolution, so a road detector over the steppe will return dry channels. **A3 · EB · high**
- **Buzzard, S.A.; Jakes, A.F.; Pearson, A.J.; Broberg, L.** | 2022 | *Advancing fence datasets: Comparing approaches to map fence locations and specifications in southwest Montana* | Frontiers in Conservation Science | doi:10.3389/fcosc.2022.958729
  - ~34,700 km of fence at mean density **0.93 km/km²** (max 14.9), validated on 330 road transects — and the fence model was built partly **from road layers**.
  - At about a kilometre of fence per square kilometre in comparable grazing country, fence lines are a pervasive background signal, not a rare confound, and they are spatially coupled to roads. **A3 · EB · high**
- **Løvschal, M.; Nørmark, M.J.; Svenning, J.-C.; Wall, J.** | 2022 | *New land tenure fences are still cropping up in the Greater Mara* | Scientific Reports 12 | doi:10.1038/s41598-022-15132-7
  - Rapid, satellite-visible fencing proliferation in open pastoral rangeland structurally similar to Mongolian steppe. **A2 · EB · high on citation, medium on finding**
- **Matikainen, L.; Lehtomäki, M.; Ahokas, E.; Hyyppä, J.; Karjalainen, M.; Jaakkola, A.; Kukko, A.; Heinonen, T.** | 2016 | *Remote sensing methods for power line corridor surveys* | ISPRS J. Photogrammetry and Remote Sensing | doi:10.1016/j.isprsjprs.2016.04.011
  - Power-line corridors are an independently studied detectable class — evidence that this confound is real and mappable, not hypothetical. **A2 · EA · high**
- **Lu, W.; Shi, X.; Lu, Z.** | 2024 | *A new two-step road extraction method in high resolution remote sensing images* | PLoS ONE 19(7):e0305933 | doi:10.1371/journal.pone.0305933
  - Motivated explicitly by many ground objects presenting road-like linear features (**rivers, city walls**) causing misclassification — a recent statement inside the road-extraction literature that this project's fabrication result is a field-wide failure, not an implementation bug. **A2 · EC · high on citation, medium on the specific sentence**
