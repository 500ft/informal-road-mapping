#!/usr/bin/env node

import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';

const repo = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const geePath = path.join(repo, 'gee', 'ndvi_change.js');
const sitesPath = path.join(repo, 'config', 'sites.geojson');
const extractPath = path.join(repo, 'analysis', 'catanroads', 'extract.py');

const gee = fs.readFileSync(geePath, 'utf8');
const manifest = JSON.parse(fs.readFileSync(sitesPath, 'utf8'));
const extract = fs.readFileSync(extractPath, 'utf8');

function numberConstant(source, name) {
  const match = source.match(new RegExp(`var ${name} = ([0-9.]+);`));
  assert(match, `Missing numeric constant ${name}`);
  return Number(match[1]);
}

const sitesMatch = gee.match(/var SITES = (\{[\s\S]*?\n\});/);
assert(sitesMatch, 'Could not read the mirrored SITES block');
const mirroredSites = vm.runInNewContext(`(${sitesMatch[1]})`);

const canonicalSites = Object.fromEntries(manifest.features.map((feature) => {
  const p = feature.properties;
  return [p.id, {
    id: p.id,
    stratum: p.stratum,
    centerLat: p.center_lat,
    centerLon: p.center_lon,
    halfKm: p.half_km,
    verified: p.verified,
    refImageryDate: p.ref_imagery_date,
    provenance: p.provenance
  }];
}));

assert.deepEqual(
  JSON.parse(JSON.stringify(mirroredSites)),
  canonicalSites,
  'gee/ndvi_change.js SITES block has drifted from config/sites.geojson'
);

const pythonThreshold = extract.match(/disturb_thresh:\s*float\s*=\s*([0-9.]+)/);
assert(pythonThreshold, 'Could not read extract_candidates disturb_thresh');
assert.equal(
  numberConstant(gee, 'Z_MIN'), Number(pythonThreshold[1]),
  'Earth Engine Z_MIN must match extract_candidates disturb_thresh'
);

assert.match(
  gee,
  /var candidateMask = zMasked\.gte\(Z_MIN\)[\s\S]*persistMasked\.gte\(PERSISTENCE_MIN\)[\s\S]*validCountMasked\.gte\(MIN_VALID_RECENT_YEARS\)/,
  'Candidate mask must retain water masks and the valid-year requirement'
);
assert.doesNotMatch(gee, /ESA\/WorldCover/, 'Static WorldCover dataset must not return');
assert.equal(
  (gee.match(/Map\.addLayer\(/g) || []).length, 4,
  'Keep exactly four Earth Engine QA layers loaded'
);
assert.match(gee, /\.addBands\(validCountMasked\.unmask\(0\)\)/,
  'Export must include n_valid');
assert.match(gee, /\.addBands\(candidateMask\.unmask\(0\)\)/,
  'Export must include candidate_mask');
assert.match(gee, /\.addBands\(largeComponentMask\.unmask\(0\)\)/,
  'Export must include large_component_mask');
assert.match(gee, /Export\.table\.toDrive\(/,
  'Gate metrics must be exportable as a machine-readable table');
assert.match(
  gee,
  /candidateForStats\s*\.addBands\(largeForStats\)\s*\.addBands\(analysisCoverage\)\s*\.reduceRegion\(\{/,
  'Gate fractions must share one fixed-scale regional reduction'
);
assert.match(
  gee, /var PRINT_GATE_METRICS = false;/,
  'Interactive gate metrics must default off; the batch CSV is authoritative'
);
assert.match(
  gee, /aoi\.area\(\{\s*maxError:\s*[1-9][0-9]*(?:\.[0-9]+)?\s*\}\)\.divide\(1e6\)/,
  'AOI area must specify a non-zero Earth Engine error margin'
);

// connectedPixelCount() caps its count at MAX_CONNECTED_PIXELS, so a component-size threshold at
// or above the cap can never be met. This coupling is invisible in either constant alone.
assert(
  numberConstant(gee, 'MAX_CONNECTED_PIXELS') > numberConstant(gee, 'MIN_COMPONENT_PIXELS'),
  'MAX_CONNECTED_PIXELS must exceed MIN_COMPONENT_PIXELS: connectedPixelCount caps the count, so a '
  + 'threshold at or above the cap silently yields no large components'
);

assert.equal(numberConstant(gee, 'GATE_RATIO_MIN'), 2.0);
assert.equal(numberConstant(gee, 'GATE_ABSOLUTE_FLOOR'), 0.0001);
assert.equal(numberConstant(gee, 'GATE_MIN_COVERAGE'), 0.90);
assert.equal(manifest._phase1_gate.preregistered_on, '2026-08-23');

console.log(
  `Phase-1 static validation passed (${Object.keys(canonicalSites).length} sites; ` +
  `Z_MIN=${pythonThreshold[1]}; four QA layers).`
);
