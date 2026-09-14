# catanroads — Phase 2 candidate extraction

Turns a surface-disturbance raster into **candidate corridor line-segments**. This
is the Phase-2 baseline from [`../docs/design.md`](../docs/design.md): a multiscale
Hessian **ridge filter** enhances elongated features, then **connected components**
are kept only if long and elongated enough to be corridor-scale — rejecting round
blobs and isolated noise. Each survivor becomes a LineString with length,
orientation, width, elongation, and mean disturbance.

Core runs on **numpy + scipy only**. The fuller pipeline (skeleton + graph tracing,
richer geometry, raster/vector I/O via scikit-image / shapely / rasterio / geopandas)
is the `full` optional extra.

> **Gate.** Per the project's go/no-go rule, this extractor is **not** applied to
> real imagery until the Phase-1 disturbance signal survives its negative control.
> It is developed and validated on synthetic corridors, where ground truth is known.

## Run

```bash
# tests
python -m pytest tests

# synthetic method demonstration -> ../results/method_demo_synthetic.png
python demo_synthetic.py
```

## Use

```python
from catanroads import make_scene, extract_candidates, to_geojson

disturbance, _ = make_scene()          # or your own 2-D array
candidates = extract_candidates(disturbance)
geojson = to_geojson(candidates, transform=None)   # pass a (x,y)->(lon,lat) fn for geo output
```

## Tests

`tests/test_extract.py` checks, on synthetic scenes with known truth, that the
extractor recovers corridors, **rejects a road-free noise scene (0 false corridors)**,
rejects a round blob, and emits valid GeoJSON — the tooling analogue of the
negative-control gate.
