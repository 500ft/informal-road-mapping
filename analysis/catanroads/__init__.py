"""Catan Roads — candidate corridor extraction (Phase 2 baseline)."""
from .extract import candidate_coordinates_px, extract_candidates, ridge_strength, to_geojson
from .synthetic import make_scene

__all__ = ["candidate_coordinates_px", "extract_candidates", "ridge_strength", "to_geojson", "make_scene"]
