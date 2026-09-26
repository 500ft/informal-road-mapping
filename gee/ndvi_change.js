/**
 * Catan Roads — Phase-1 composite surface-disturbance gate
 * --------------------------------------------------------
 * Paste into the Earth Engine Code Editor: https://code.earthengine.google.com/
 *
 * This is NOT an NDVI road classifier. It builds a persistent, locally
 * normalized surface-disturbance signal and reports a fixed-scale quantitative
 * statistic for comparison between pre-registered development sites and the
 * road-free negative control. A site is ineligible for the gate until its entry
 * in config/sites.geojson has been visually verified with dated reference imagery.
 */

// --- 1. Registered site -------------------------------------------------------
// This block mirrors config/sites.geojson. Keep the selected SITE_ID, verification
// flag, date, and provenance synchronized with that canonical manifest.
var SITE_ID = 'dev-01-braided';
var ALLOW_UNVERIFIED_QA = true; // permits inspection, never a gate result

var SITES = {
  'dev-01-braided': {
    id: 'dev-01-braided', stratum: 'development',
    centerLat: 47.30, centerLon: 102.30, halfKm: 8,
    verified: false, refImageryDate: 'TBD',
    provenance: 'starting guess, central-Mongolia steppe'
  },
  'dev-02-recovering': {
    id: 'dev-02-recovering', stratum: 'development',
    centerLat: 46.20, centerLon: 104.60, halfKm: 8,
    verified: false, refImageryDate: 'TBD', provenance: 'starting guess'
  },
  'dev-03-gobi': {
    id: 'dev-03-gobi', stratum: 'development',
    centerLat: 45.40, centerLon: 100.10, halfKm: 8,
    verified: false, refImageryDate: 'TBD', provenance: 'starting guess'
  },
  'holdout-01': {
    id: 'holdout-01', stratum: 'holdout',
    centerLat: 48.10, centerLon: 98.20, halfKm: 8,
    verified: false, refImageryDate: 'TBD', provenance: 'starting guess'
  },
  'confound-01': {
    id: 'confound-01', stratum: 'confound',
    centerLat: 48.60, centerLon: 106.20, halfKm: 8,
    verified: false, refImageryDate: 'TBD', provenance: 'starting guess'
  },
  'negative-01': {
    id: 'negative-01', stratum: 'negative_control',
    centerLat: 46.80, centerLon: 99.50, halfKm: 8,
    verified: false, refImageryDate: 'TBD', provenance: 'starting guess'
  }
};

var SITE = SITES[SITE_ID];
if (!SITE) throw new Error('Unknown SITE_ID: ' + SITE_ID);
if (!SITE.verified && !ALLOW_UNVERIFIED_QA) {
  throw new Error('Site is unverified in config/sites.geojson: ' + SITE_ID);
}
if (!SITE.verified) {
  print('UNVERIFIED QA ONLY — do not report this as a Phase-1 gate result: ' + SITE_ID);
}

var aoi = ee.Geometry.Point([SITE.centerLon, SITE.centerLat])
  .buffer(SITE.halfKm * 1000).bounds();
Map.centerObject(aoi, 13); // inspect at zoom >=13; analysis itself is fixed at 10 m
Map.setOptions('HYBRID'); // visual QA only; never a road reference or tracing source

// --- 2. Pre-registered analysis configuration --------------------------------
var MONTH = 7;
var earlyYears = [2018, 2019, 2020, 2021];
var recentYears = [2023, 2024, 2025, 2026]; // 2022 is a temporal buffer

var ANALYSIS_CRS = 'EPSG:3857';
var ANALYSIS_SCALE_M = 10;
var CONTROL_INNER_M = 200;
var CONTROL_OUTER_M = 800;
var MIN_CONTROL_PIXELS = 500;

// Z_MIN intentionally matches analysis/catanroads/extract.py disturb_thresh.
var Z_MIN = 1.0;
var YEARLY_EFFECT_MIN = 0.02; // per-year effect-size floor; test 0.01/0.02/0.03
var PERSISTENCE_MIN = 2 / 3;
var MIN_VALID_RECENT_YEARS = 2;
var MIN_COMPONENT_PIXELS = 50;
// maxSize argument to connectedPixelCount(): the count is CAPPED at this value, so a component
// larger than this reports exactly this number, not its true size. Harmless for the current
// MIN_COMPONENT_PIXELS = 50 test, because min(trueSize, 256) >= 50 whenever trueSize >= 50.
// HAZARD: if MIN_COMPONENT_PIXELS is ever raised above this cap, the >= test becomes impossible to
// satisfy and the gate silently returns no large components. Keep MAX_CONNECTED_PIXELS strictly
// greater than MIN_COMPONENT_PIXELS; tools/validate_phase1.mjs enforces that.
// The counts are also unusable as component SIZES above the cap; only the threshold test is valid.
var MAX_CONNECTED_PIXELS = 256;

// Primary gate, frozen before registered-site output is inspected:
// >=2 of 3 development sites must have large_component_fraction >=
// max(2 * negative-01, 0.0001), and every compared site needs >=90% coverage.
var GATE_RATIO_MIN = 2.0;
var GATE_ABSOLUTE_FLOOR = 0.0001;
var GATE_MIN_DEVELOPMENT_SITES = 2;
var GATE_MIN_COVERAGE = 0.90;
// Full-resolution gate metrics are authoritative in the table export. Leave the
// interactive print off unless doing a quick diagnostic on a smaller workload;
// the Code Editor stops synchronous computations after roughly five minutes.
var PRINT_GATE_METRICS = false;

function yearSpan(years) {
  return years[0] + '-' + years[years.length - 1];
}

function atAnalysisScale(img) {
  return img.resample('bilinear').reproject({
    crs: ANALYSIS_CRS, scale: ANALYSIS_SCALE_M
  });
}

// --- 3. Same-season Sentinel-2 evidence cube ---------------------------------
function maskS2(img) {
  var scl = img.select('SCL');
  var clear = scl.neq(3).and(scl.neq(8)).and(scl.neq(9))
    .and(scl.neq(10)).and(scl.neq(11));
  return img.updateMask(clear);
}

// Missing years remain masked observations with the expected band schema, never
// fabricated zero reflectance. Scene presence does not imply usable pixels.
function medianOrMasked(collection, bands) {
  var empty = ee.Image.constant(bands.map(function () { return 0; }))
    .rename(bands).toFloat().updateMask(0);
  return ee.Image(ee.Algorithms.If(collection.size().gt(0),
    collection.median(), empty)).select(bands);
}

function julyS2(year) {
  var start = ee.Date.fromYMD(year, MONTH, 1);
  var collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
    .filterBounds(aoi)
    .filterDate(start, start.advance(1, 'month'))
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 40))
    .map(maskS2);
  return medianOrMasked(collection, ['B2', 'B3', 'B4', 'B8', 'B11'])
    .clip(aoi)
    .set('year', year);
}

function julyComposite(year) {
  var c = julyS2(year);
  var ndvi = c.normalizedDifference(['B8', 'B4']).rename('NDVI');
  // BSI = ((SWIR+Red) - (NIR+Blue)) / ((SWIR+Red) + (NIR+Blue))
  var sr = c.select('B11').add(c.select('B4'));
  var nb = c.select('B8').add(c.select('B2'));
  var bsi = sr.subtract(nb).divide(sr.add(nb)).rename('BSI');
  return c.select(['B4', 'B3', 'B2']).addBands(ndvi).addBands(bsi)
    .set('year', year);
}

function collFor(years) {
  return ee.ImageCollection(years.map(julyComposite));
}

var earlyCollection = collFor(earlyYears);
var recentCollection = collFor(recentYears);
var earlyRGB = atAnalysisScale(earlyCollection.select(['B4', 'B3', 'B2']).median());
var recentRGB = atAnalysisScale(recentCollection.select(['B4', 'B3', 'B2']).median());
var earlyNDVI = atAnalysisScale(earlyCollection.select('NDVI').median());
var earlyBSI = atAnalysisScale(earlyCollection.select('BSI').median());
var recentNDVI = atAnalysisScale(recentCollection.select('NDVI').median());
var recentBSI = atAnalysisScale(recentCollection.select('BSI').median());

// Higher composite values mean vegetation loss plus exposed-surface gain.
var dNDVI = recentNDVI.subtract(earlyNDVI);
var dBSI = recentBSI.subtract(earlyBSI);
var comp = dBSI.subtract(dNDVI).multiply(0.5).rename('v');

// --- 4. Annular local-control normalization ----------------------------------
// Excluding the inner 200 m prevents a broad/braided target from dominating its
// own reference population. Fixed reprojection makes map and export thresholds
// refer to the same 10 m analysis grid.
function ringStats(img, rIn, rOut) {
  var kInner = ee.Kernel.circle({
    radius: rIn, units: 'meters', normalize: false
  });
  var kOuter = ee.Kernel.circle({
    radius: rOut, units: 'meters', normalize: false
  });
  var one = ee.Image(1).updateMask(img.mask());

  function ringSum(im) {
    var outer = im.reduceNeighborhood(ee.Reducer.sum(), kOuter).rename('v');
    var inner = im.reduceNeighborhood(ee.Reducer.sum(), kInner).rename('v');
    return outer.subtract(inner);
  }

  var n = ringSum(one).rename('ring_n');
  var sum = ringSum(img);
  var sumSquares = ringSum(img.pow(2));
  var mean = sum.divide(n).rename('local_mean');
  var variance = sumSquares.divide(n).subtract(mean.pow(2)).max(0);
  return {mean: mean, std: variance.sqrt().rename('local_std'), n: n};
}

var local = ringStats(comp, CONTROL_INNER_M, CONTROL_OUTER_M);
var zscore = comp.subtract(local.mean)
  .divide(local.std.max(1e-4))
  .rename('disturbance_z')
  .updateMask(local.n.gte(MIN_CONTROL_PIXELS));

// --- 5. Persistence with an explicit valid-year denominator ------------------
var perYear = ee.ImageCollection(recentYears.map(function (year) {
  var im = julyComposite(year);
  var yearlyComp = im.select('BSI').subtract(earlyBSI)
    .subtract(im.select('NDVI').subtract(earlyNDVI))
    .multiply(0.5);
  yearlyComp = atAnalysisScale(yearlyComp).rename('yearly_disturbance');
  return yearlyComp.gt(YEARLY_EFFECT_MIN).rename('disturbed')
    .set('year', year);
}));

var validCount = perYear.count().rename('n_valid');
var disturbedCount = perYear.sum().rename('n_disturbed');
var persistence = disturbedCount.divide(validCount)
  .rename('persistence')
  .updateMask(validCount.gt(0));

// --- 6. Water-safe candidate mask --------------------------------------------
var water = ee.Image('JRC/GSW1_4/GlobalSurfaceWater')
  .select('occurrence').gt(50).unmask(0).rename('permanent_water');
var landMask = water.not();
var zMasked = zscore.updateMask(landMask);
var persistMasked = persistence.updateMask(landMask);
var validCountMasked = validCount.updateMask(landMask);

// Do not add an absolute composite gate here: YEARLY_EFFECT_MIN is already the
// named effect-size floor inside persistence, while z supplies local normalization.
var candidateMask = zMasked.gte(Z_MIN)
  .and(persistMasked.gte(PERSISTENCE_MIN))
  .and(validCountMasked.gte(MIN_VALID_RECENT_YEARS))
  .rename('candidate_mask');

var connectedCount = candidateMask.selfMask()
  .reproject({crs: ANALYSIS_CRS, scale: ANALYSIS_SCALE_M})
  .connectedPixelCount(MAX_CONNECTED_PIXELS, true);
var largeComponentMask = connectedCount.gte(MIN_COMPONENT_PIXELS)
  .selfMask().rename('large_component_mask');

// --- 7. Temporal land-cover confound channel ---------------------------------
// Dynamic World replaces static WorldCover: only temporal probability changes
// in built, crop, and water classes are retained as an interpretation aid.
var DW_BANDS = ['built', 'crops', 'water'];
function julyDynamicWorld(year) {
  var start = ee.Date.fromYMD(year, MONTH, 1);
  var collection = ee.ImageCollection('GOOGLE/DYNAMICWORLD/V1')
    .filterBounds(aoi)
    .filterDate(start, start.advance(1, 'month'))
    .select(DW_BANDS);
  return medianOrMasked(collection, DW_BANDS)
    .clip(aoi)
    .set('year', year);
}

function dwFor(years) {
  return atAnalysisScale(ee.ImageCollection(years.map(julyDynamicWorld)).median());
}

var earlyDW = dwFor(earlyYears);
var recentDW = dwFor(recentYears);
var dwBuiltChange = recentDW.select('built').subtract(earlyDW.select('built'))
  .rename('dw_built_change');
var dwCropsChange = recentDW.select('crops').subtract(earlyDW.select('crops'))
  .rename('dw_crops_change');
var dwWaterChange = recentDW.select('water').subtract(earlyDW.select('water'))
  .rename('dw_water_change');
var dwConfoundChange = dwBuiltChange.abs().max(dwCropsChange.abs())
  .max(dwWaterChange.abs()).rename('dw_confound_change');

// --- 8. Four-layer QA display -------------------------------------------------
var rgbVis = {min: 200, max: 3000, gamma: 1.2};
var candidateVis = {
  min: Z_MIN, max: 3,
  palette: ['f6e8c3', 'd8b365', '8c510a']
};
Map.addLayer(earlyRGB, rgbVis, '1 Early RGB ' + yearSpan(earlyYears), false);
Map.addLayer(recentRGB, rgbVis, '2 Recent RGB ' + yearSpan(recentYears), true);
Map.addLayer(
  dwConfoundChange.updateMask(dwConfoundChange.gte(0.25)),
  {min: 0.25, max: 0.75, palette: ['fff7bc', 'fec44f', 'd95f0e']},
  '3 QA Dynamic World confound change', false, 0.65
);
Map.addLayer(
  zMasked.updateMask(candidateMask), candidateVis,
  '4 Persistent candidate (fixed 10 m)', true, 0.65
);

var legend = ui.Panel({style: {position: 'bottom-left', padding: '8px 10px'}});
legend.add(ui.Label(
  SITE.id + ': candidate disturbance ' + yearSpan(earlyYears) +
    ' vs ' + yearSpan(recentYears),
  {fontWeight: 'bold', fontSize: '12px', margin: '0 0 4px 0'}
));
legend.add(ui.Label(
  '■ brown — z ≥ ' + Z_MIN + ', persistence ≥ 2/3, valid years ≥ ' +
    MIN_VALID_RECENT_YEARS,
  {color: '8c510a', fontSize: '11px', margin: '1px 0'}
));
legend.add(ui.Label(
  SITE.verified ? 'REGISTERED SITE' : 'UNVERIFIED QA ONLY',
  {fontSize: '10px', color: SITE.verified ? '2d6a4f' : 'b2182b', margin: '3px 0 0 0'}
));
Map.add(legend);

// --- 9. Fixed-scale Phase-1 gate statistics ----------------------------------
// Fractions use non-permanent-water area as the denominator. Invalid analysis
// pixels count as zero candidates and are separately exposed by coverage_fraction.
var candidateForStats = candidateMask.unmask(0).updateMask(landMask)
  .rename('candidate_fraction');
var largeForStats = largeComponentMask.unmask(0).updateMask(landMask)
  .rename('large_component_fraction');
var analysisCoverage = validCount.gte(MIN_VALID_RECENT_YEARS)
  .and(zMasked.mask())
  .unmask(0).updateMask(landMask)
  .rename('coverage_fraction');
var fractionMetrics = candidateForStats
  .addBands(largeForStats)
  .addBands(analysisCoverage)
  .reduceRegion({
    reducer: ee.Reducer.mean(), geometry: aoi,
    crs: ANALYSIS_CRS, scale: ANALYSIS_SCALE_M, maxPixels: 1e9
  });
var zPercentiles = zMasked.reduceRegion({
  reducer: ee.Reducer.percentile([90, 99]), geometry: aoi,
  crs: ANALYSIS_CRS, scale: ANALYSIS_SCALE_M, maxPixels: 1e9
});

var gateMetrics = ee.Dictionary({
  site_id: SITE.id,
  stratum: SITE.stratum,
  gate_eligible: SITE.verified
}).combine(fractionMetrics, true).combine(zPercentiles, true);

var exportPrefix = SITE.verified ? 'gate_' : 'qa_unverified_';
var exportName = exportPrefix + SITE.id + '_' + yearSpan(recentYears);

print(ee.Dictionary({
  message_type: 'REGISTERED GATE',
  primary_metric: 'large_component_fraction',
  required_development_sites: GATE_MIN_DEVELOPMENT_SITES,
  development_to_negative_ratio_min: GATE_RATIO_MIN,
  development_absolute_floor: GATE_ABSOLUTE_FLOOR,
  coverage_fraction_min: GATE_MIN_COVERAGE,
  decision_rule: 'Pass when >=2/3 verified development sites have metric >= ' +
    'max(2 * negative-01, 0.0001), with coverage >=0.90 at every compared site.'
}));
if (PRINT_GATE_METRICS) {
  print(gateMetrics.set('message_type', 'GATE SITE METRICS'));
} else {
  print(ee.Dictionary({
    message_type: 'GATE METRICS DELIVERY',
    action: 'Run the Tasks-tab table export: ' + exportName + '_gate_metrics',
    reason: 'Batch export is authoritative; interactive full-resolution reductions can time out.'
  }));
}

// --- 10. Export + run manifest ------------------------------------------------
var stack = zMasked
  .addBands(comp.rename('disturbance'))
  .addBands(persistMasked)
  .addBands(validCountMasked.unmask(0))
  .addBands(candidateMask.unmask(0))
  .addBands(largeComponentMask.unmask(0))
  .addBands(water)
  .addBands(dwBuiltChange)
  .addBands(dwCropsChange)
  .addBands(dwWaterChange)
  .addBands(dwConfoundChange)
  .toFloat();

Export.image.toDrive({
  image: stack,
  description: exportName,
  region: aoi,
  crs: ANALYSIS_CRS,
  scale: ANALYSIS_SCALE_M,
  maxPixels: 1e9
});

var gateRecord = ee.Feature(null, gateMetrics).set({
  // Intake provenance; these do not change any mask or registered threshold.
  center_lat: SITE.centerLat,
  center_lon: SITE.centerLon,
  half_km: SITE.halfKm,
  month: MONTH,
  min_control_pixels: MIN_CONTROL_PIXELS,
  reference_imagery_date: SITE.refImageryDate,
  site_provenance: SITE.provenance,
  early_years: yearSpan(earlyYears),
  recent_years: yearSpan(recentYears),
  analysis_crs: ANALYSIS_CRS,
  analysis_scale_m: ANALYSIS_SCALE_M,
  control_inner_m: CONTROL_INNER_M,
  control_outer_m: CONTROL_OUTER_M,
  z_min: Z_MIN,
  yearly_effect_min: YEARLY_EFFECT_MIN,
  persistence_min: PERSISTENCE_MIN,
  min_valid_recent_years: MIN_VALID_RECENT_YEARS,
  min_component_pixels: MIN_COMPONENT_PIXELS
});
// Retain machine-readable scene QA in each downloaded CSV, not only console text.
earlyYears.concat(recentYears).forEach(function (year) {
  gateRecord = gateRecord.set('s2_scene_count_' + year, countJuly(year));
});
Export.table.toDrive({
  collection: ee.FeatureCollection([gateRecord]),
  description: exportName + '_gate_metrics',
  fileFormat: 'CSV'
});

print(ee.Dictionary({
  message_type: 'Candidate thumbnail (click)',
  url: zMasked.updateMask(candidateMask).visualize(candidateVis).getThumbURL({
    dimensions: 1400, region: aoi, crs: ANALYSIS_CRS, format: 'png'
  })
}));

function countJuly(year) {
  var start = ee.Date.fromYMD(year, MONTH, 1);
  return ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
    .filterBounds(aoi)
    .filterDate(start, start.advance(1, 'month'))
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 40))
    .size();
}

print(ee.Dictionary({
  message_type: 'RUN MANIFEST',
  site_id: SITE.id,
  site_stratum: SITE.stratum,
  site_verified: SITE.verified,
  reference_imagery_date: SITE.refImageryDate,
  site_provenance: SITE.provenance,
  aoi_km2: aoi.area({maxError: 1}).divide(1e6),
  month: MONTH,
  early_years: earlyYears,
  recent_years: recentYears,
  scenes_per_recent_year: ee.Dictionary.fromLists(
    recentYears.map(function (year) { return String(year); }),
    recentYears.map(countJuly)
  ),
  scenes_per_early_year: ee.Dictionary.fromLists(
    earlyYears.map(function (year) { return String(year); }),
    earlyYears.map(countJuly)
  ),
  analysis_crs: ANALYSIS_CRS,
  analysis_scale_m: ANALYSIS_SCALE_M,
  control_annulus_m: [CONTROL_INNER_M, CONTROL_OUTER_M],
  z_min: Z_MIN,
  yearly_effect_min: YEARLY_EFFECT_MIN,
  persistence_min: PERSISTENCE_MIN,
  min_valid_recent_years: MIN_VALID_RECENT_YEARS,
  min_component_pixels: MIN_COMPONENT_PIXELS,
  export_name: exportName
}));

print('NEXT: run this frozen configuration at each VERIFIED development site and ' +
  'negative-01; run each *_gate_metrics table export and compare the CSV ' +
  'large_component_fraction values exactly as ' +
  'specified by REGISTERED GATE. Do not infer the gate from the rendered map.');
