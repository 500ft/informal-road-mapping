/**
 * Grid / support runtime probe — Earth Engine Code Editor script.
 *
 * STATUS WHEN COMMITTED: PREPARED_UNEXECUTED. Nothing here has been run.
 * It inspects NO registered site imagery and NEVER touches holdout-01.
 *
 * Purpose: measure what this project's analysis grid physically is, rather than assuming it.
 * Expected values are in grid_runtime_expectations.json, computed independently (inverse
 * projection + geodesic), NOT read back from the same Earth Engine operation.
 *
 * Run: paste into https://code.earthengine.google.com with an authorized project, press Run,
 * copy the console output into the observed-results table in README.md, and export the tasks.
 */

var ANALYSIS_CRS = 'EPSG:3857';      // mirrors gee/ndvi_change.js
var ANALYSIS_SCALE_M = 10;

// A registered development latitude, and an equatorial control where Web Mercator is ~1:1.
var PROBE_POINTS = {
  'dev-01-braided-lat': ee.Geometry.Point([102.3, 47.3]),
  'equator-control':    ee.Geometry.Point([102.3, 0.0])
};

// ---------------------------------------------------------------- 1. projection and transform
function reportProjection(label, img) {
  var p = img.projection();
  print(label + ' :: crs', p.crs());
  print(label + ' :: nominalScale (m)', p.nominalScale());
  print(label + ' :: transform', p.getInfo().transform);
}

// ---------------------------------------------------------------- 2. pixel area and spacing
function reportPixelGeometry(label, pt) {
  var area = ee.Image.pixelArea()
    .reproject({crs: ANALYSIS_CRS, scale: ANALYSIS_SCALE_M})
    .reduceRegion({reducer: ee.Reducer.first(), geometry: pt, scale: ANALYSIS_SCALE_M});
  print(label + ' :: pixelArea at point (m2)', area);

  // Neighbour-centre distance: offset one pixel east in PROJECTED units, measure on the ground.
  var c = pt.coordinates();
  var proj = ee.Projection(ANALYSIS_CRS).atScale(ANALYSIS_SCALE_M);
  var here = pt.transform(proj, 0.001);
  var east = ee.Geometry.Point(
    ee.List([ee.Number(here.coordinates().get(0)).add(ANALYSIS_SCALE_M),
             here.coordinates().get(1)]), proj);
  print(label + ' :: one-pixel-east ground distance (m)',
        here.transform('EPSG:4326', 0.001).distance(east.transform('EPSG:4326', 0.001), 0.001));
  print(label + ' :: lon/lat', c);
}

// ---------------------------------------------------------------- 3. 50-pixel footprint
function reportComponentFootprint(label, pt) {
  // A known shape: a 5x10 block of analysis pixels = the min_component_pixels = 50 threshold.
  var proj = ee.Projection(ANALYSIS_CRS).atScale(ANALYSIS_SCALE_M);
  var box = pt.transform(proj, 0.001).buffer(ANALYSIS_SCALE_M * 5, 0.001, proj).bounds(0.001, proj);
  print(label + ' :: 50-px-equivalent box area on the ground (m2)', box.area(0.001));
}

// ---------------------------------------------------------------- 4. the ring kernel's support
function reportRingKernel(label) {
  // CONTROL_INNER_M = 200, CONTROL_OUTER_M = 800 in gee/ndvi_change.js.
  // Competing interpretations: metres on the ground, versus projected units on this grid.
  // Record which one the measured support matches, and its boundary convention.
  var outer = ee.Kernel.circle({radius: 800, units: 'meters'});
  var inner = ee.Kernel.circle({radius: 200, units: 'meters'});
  print(label + ' :: outer kernel weights (rows)', ee.List(outer.weights()).length());
  print(label + ' :: inner kernel weights (rows)', ee.List(inner.weights()).length());
}

// ---------------------------------------------------------------- 5. resample-on-composites
// gee/ndvi_change.js::atAnalysisScale calls .resample('bilinear') on DERIVED images, including
// collection medians. Earth Engine documents that resample needs a meaningful default projection
// and warns against applying it to composites, which have none.
// https://developers.google.com/earth-engine/apidocs/ee-image-resample
// This reproduces BOTH orders and prints the projections at each step so the difference is
// observed rather than argued. An error here is an OBSERVED FAILURE to record, not a licence to
// change the live helper during closeout.
function reportResampleOrder(pt) {
  var coll = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
    .filterBounds(pt).filterDate('2023-07-01', '2023-08-01')
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 40))
    .select(['B4', 'B8']);

  print('resample :: source image projection', ee.Image(coll.first()).projection().crs());
  print('resample :: source nominalScale', ee.Image(coll.first()).projection().nominalScale());

  // Order 1 — what the repository does today: composite, THEN resample.
  var compositeFirst = coll.median();
  print('resample :: composite projection BEFORE resample (expect a default/WGS84-like projection)',
        compositeFirst.projection().crs());
  var afterComposite = compositeFirst.resample('bilinear')
    .reproject({crs: ANALYSIS_CRS, scale: ANALYSIS_SCALE_M});
  print('resample :: order-1 (composite -> resample) result projection', afterComposite.projection().crs());

  // Order 2 — resample each source image first, then composite.
  var beforeComposite = coll.map(function (img) { return img.resample('bilinear'); }).median()
    .reproject({crs: ANALYSIS_CRS, scale: ANALYSIS_SCALE_M});
  print('resample :: order-2 (resample -> composite) result projection', beforeComposite.projection().crs());

  // Numeric difference at the probe point, if both evaluate.
  var diff = afterComposite.subtract(beforeComposite)
    .reduceRegion({reducer: ee.Reducer.first(), geometry: pt, scale: ANALYSIS_SCALE_M});
  print('resample :: order-1 minus order-2 at probe point (B4, B8)', diff);
}

// ---------------------------------------------------------------- 6. band alignment
function reportBandAlignment(pt) {
  var img = ee.Image(ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
    .filterBounds(pt).filterDate('2023-07-01', '2023-08-01').first());
  ['B2', 'B4', 'B8', 'B11'].forEach(function (b) {
    print('alignment :: ' + b + ' nominalScale (m)', img.select(b).projection().nominalScale());
  });
}

// ---------------------------------------------------------------- run
Object.keys(PROBE_POINTS).forEach(function (label) {
  var pt = PROBE_POINTS[label];
  reportProjection(label, ee.Image.pixelArea().reproject({crs: ANALYSIS_CRS, scale: ANALYSIS_SCALE_M}));
  reportPixelGeometry(label, pt);
  reportComponentFootprint(label, pt);
});
reportRingKernel('kernel');
reportResampleOrder(PROBE_POINTS['dev-01-braided-lat']);
reportBandAlignment(PROBE_POINTS['dev-01-braided-lat']);
