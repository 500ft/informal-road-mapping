# Site verification worksheet — generated, 2026-09-09

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

## dev-01-braided

- Stratum: development; role: primary positive: braided corridor.
- Center (latitude, longitude): 47.3, 102.3; registered half_km: 8.
- Expected feature: wide braided off-road corridor with multiple parallel ruts.
- Current manifest eligibility: false.
- verified: **leave false until confirmed**.
- ref_imagery_date: **unfilled** (scene acquisition date, YYYY-MM-DD).
- provenance: **unfilled** (provider, scene/view link, date, extent, inspector and evidence reference).
- Observed feature / counter-evidence: **unfilled**.
- Older reference date and evidence for temporal interpretation, where needed: **unfilled**.
- Decision: confirmed / rejected / uncertain; reason: **unfilled**.

## dev-02-recovering

- Stratum: development; role: positive: likely recovering / disused corridor.
- Center (latitude, longitude): 46.2, 104.6; registered half_km: 8.
- Expected feature: track showing progressive vegetation recovery vs older imagery.
- Current manifest eligibility: false.
- verified: **leave false until confirmed**.
- ref_imagery_date: **unfilled** (scene acquisition date, YYYY-MM-DD).
- provenance: **unfilled** (provider, scene/view link, date, extent, inspector and evidence reference).
- Observed feature / counter-evidence: **unfilled**.
- Older reference date and evidence for temporal interpretation, where needed: **unfilled**.
- Decision: confirmed / rejected / uncertain; reason: **unfilled**.

## dev-03-gobi

- Stratum: development; role: positive: arid / low-vegetation corridor.
- Center (latitude, longitude): 45.4, 100.1; registered half_km: 8.
- Expected feature: corridor over sparse gobi where NDVI is weak and bare-soil carries the signal.
- Current manifest eligibility: false.
- verified: **leave false until confirmed**.
- ref_imagery_date: **unfilled** (scene acquisition date, YYYY-MM-DD).
- provenance: **unfilled** (provider, scene/view link, date, extent, inspector and evidence reference).
- Observed feature / counter-evidence: **unfilled**.
- Older reference date and evidence for temporal interpretation, where needed: **unfilled**.
- Decision: confirmed / rejected / uncertain; reason: **unfilled**.

## confound-01

- Stratum: confound; role: environmental confound stratum.
- Center (latitude, longitude): 48.6, 106.2; registered half_km: 8.
- Expected feature: agriculture / riverbed / settlement expansion producing non-road land-use change.
- Current manifest eligibility: false.
- verified: **leave false until confirmed**.
- ref_imagery_date: **unfilled** (scene acquisition date, YYYY-MM-DD).
- provenance: **unfilled** (provider, scene/view link, date, extent, inspector and evidence reference).
- Observed feature / counter-evidence: **unfilled**.
- Older reference date and evidence for temporal interpretation, where needed: **unfilled**.
- Decision: confirmed / rejected / uncertain; reason: **unfilled**.

## negative-01

- Stratum: negative_control; role: road-free negative control (falsification gate).
- Center (latitude, longitude): 46.8, 99.5; registered half_km: 8.
- Expected feature: open terrain with no informal roads.
- Current manifest eligibility: false.
- verified: **leave false until confirmed**.
- ref_imagery_date: **unfilled** (scene acquisition date, YYYY-MM-DD).
- provenance: **unfilled** (provider, scene/view link, date, extent, inspector and evidence reference).
- Observed feature / counter-evidence: **unfilled**.
- Older reference date and evidence for temporal interpretation, where needed: **unfilled**.
- Decision: confirmed / rejected / uncertain; reason: **unfilled**.

## After inspection

Apply only evidence-supported findings to the canonical manifest, with a reviewable diff.
Do not fill positive judgments from this template automatically. Then follow
[PHASE1_RUNBOOK.md](PHASE1_RUNBOOK.md), including regenerating the exported reference
metadata after manifest changes. Its tested gate command still needs real Earth Engine
exports; worksheet completion alone is not a Phase-1 pass.

Regenerate this derived document with `PYTHONPATH=analysis python -m catanroads.site_worksheet`.
Check consistency with the same command plus `--check`. Generation never modifies the manifest.
