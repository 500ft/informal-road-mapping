"""The gallery script runs and writes its five figures (smoke check; pixels are not compared)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from plot_stress_cases import plot_all


def test_gallery_writes_five_figures(tmp_path):
    written = plot_all(tmp_path)
    assert len(written) == 5 and all(p.exists() and p.stat().st_size > 10_000 for p in written)
