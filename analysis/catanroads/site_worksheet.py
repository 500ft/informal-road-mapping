"""Generate inspection forms without opening imagery or modifying site eligibility."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "docs/SITE_VERIFICATION_WORKSHEET.md"
INTRO = """# Site verification worksheet — generated, 2026-09-09

This is a development inspection form, not verified imagery evidence. Generated from
[sites.geojson](../config/sites.geojson); the manifest remains unchanged. The untouched
holdout is deliberately omitted. Do not open its imagery until the candidate and
evaluation procedure have been frozen.

The admission fields are exactly `verified`, `ref_imagery_date`, and `provenance`.
Only actual dated source-image inspection can populate them. A search result, coordinate,
copyright year, access date or low-resolution NDVI map is not feature confirmation.

## Source choice and reason

Use [Google Earth's historical imagery controls](https://support.google.com/earth/answer/15468379)
as the first inspection route (official help inspected 2026-09-09), because the task needs
dated high-resolution comparisons rather than a current basemap of unknown acquisition date.
This confirms a tool capability, not coverage or licensing for these particular sites.
Use an accessible primary imagery provider with explicit scene dates if Earth has no
usable scene; retain provider attribution and an authorized access reference rather than
redistributing imagery without permission. No site image has been inspected in this task.

## Procedure before viewing model output

1. Open the coordinates below and record scene acquisition date(s), provider, view extent,
   scale/resolution, access link or retained screenshot reference, and inspector identity.
2. Check the expected feature and document contradictory land use, riverbeds, shadow,
   agriculture, clouds or mosaic-date boundaries. Also record, as present / absent /
   cannot tell, the three confounds a geometry-based detector cannot separate from a
   road: dry drainage channels, fence lines, and animal or livestock paths. Record them
   even when the expected feature is confirmed, because a site can contain both.
   Uncertain visibility stays unverified.
3. For a recovering corridor, compare at least two dated images; a single green scene
   cannot distinguish abandonment, rain response or absence of a road. The Phase-1
   positive-disturbance gate is not itself a recovery/road classifier.
4. For the negative control inspect the full registered AOI, not just its center.
   Record what portion could actually be assessed. Never choose a replacement because
   the candidate's negative-control output was inconvenient.
5. Record reference judgments before inspecting predictions. Any relocation or stratum
   change is a prospective design amendment with old coordinates retained, not a silent
   edit after seeing results.

These are five inspection forms, not a claim they can all be verified in a fixed hour.
Record an unresolved outcome if imagery is missing or ambiguous. An AI-assisted image
review is not an independent human review. CR-08 remains open.

"""
def render(manifest):
    seen, sections = set(), [INTRO]
    for feature in manifest["features"]:
        p = feature["properties"]
        if p["id"] in seen:
            raise ValueError("duplicate site id")
        seen.add(p["id"])
        if p["stratum"] == "holdout":
            continue
        lon, lat = feature["geometry"]["coordinates"]
        if (p["center_lon"], p["center_lat"]) != (lon, lat):
            raise ValueError("manifest coordinate fields disagree")
        sections.append(f"""## {p['id']}

- Stratum: {p['stratum']}; role: {p['role']}.
- Center (latitude, longitude): {lat}, {lon}; registered half_km: {p['half_km']}.
- Expected feature: {p['expected_feature']}.
- Current manifest eligibility: {str(p['verified']).lower()}.
- verified: **leave false until confirmed**.
- ref_imagery_date: **unfilled** (scene acquisition date, YYYY-MM-DD).
- provenance: **unfilled** (provider, scene/view link, date, extent, inspector and evidence reference).
- Observed feature / counter-evidence: **unfilled**.
- Older reference date and evidence for temporal interpretation, where needed: **unfilled**.
- Decision: confirmed / rejected / uncertain; reason: **unfilled**.

""")
    sections.append("""## After inspection

Apply only evidence-supported findings to the canonical manifest, with a reviewable diff.
Do not fill positive judgments from this template automatically. Then follow
[PHASE1_RUNBOOK.md](PHASE1_RUNBOOK.md), including regenerating the exported reference
metadata after manifest changes. Its tested gate command still needs real Earth Engine
exports; worksheet completion alone is not a Phase-1 pass.

Regenerate this derived document with `PYTHONPATH=analysis python -m catanroads.site_worksheet`.
Check consistency with the same command plus `--check`. Generation never modifies the manifest.
""")
    return "".join(sections)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    text = render(json.loads((ROOT / "config/sites.geojson").read_text()))
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_text() != text:
            parser.exit(1, "Site worksheet missing or stale\n")
    else:
        OUTPUT.write_text(text, encoding="utf-8")
    print("Development worksheet consistent; no sites verified and no imagery inspected")


if __name__ == "__main__":
    main()
