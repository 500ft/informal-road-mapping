# Week of 2026-09-19 — build plan (revised from the 2026-09-19 handoff draft)

Status authority stays [SPRINT_TASKS.csv](SPRINT_TASKS.csv); this file schedules work, it does not
record task status. Editing convention: [AGENTS.md](../AGENTS.md). Research design:
[design.md](design.md). Day 1 is executed and recorded in
[evidence/task-2026-09-19/README.md](../evidence/task-2026-09-19/README.md).

Base: `main` @ `515ce3d`. Synthetic evidence only. This plan authorizes no change to the registered
sites, thresholds, holdout policy or Phase-1 gate, and no scientific claim.

## What changed from the draft, and why

The draft handoff was sound on scope discipline, stop rules and the adaptive tiering; those are kept
almost verbatim. Six things are changed because they would have cost time or produced a wrong order.

1. **Owner review moves from Day 7 to Day 2.** The draft reconciled the ledger on Day 6 "after the
   relevant PRs actually merge" but put the owner's approve/reject on Day 7. Nothing could merge
   before the last day, so Day 6's integration work had no merged state to integrate. The stack has
   been green and waiting since 2026-09-16; the review request goes out first.
2. **Verification by execution replaces the hand-written review matrix.** The draft spent Day 1 and
   half of Day 2 (about 4 h) building a table mapping each acceptance item to a test name. That
   table restates the suite and rots on the next rename. Day 1 instead re-ran every claim from a
   clean detached checkout of the PR head and **derived** the acceptance map from the tree. It cost
   well under the allotted time and produced three findings the table would not have surfaced.
3. **Owner-independent CR-08 work is pulled earlier and decoupled.** The draft put the packet on
   Day 4 and the owner's inspection inside the same day, so an owner who is busy on Thursday idles
   the whole afternoon and pushes Day 5. The packet, the export preflight checklist and the CLI
   rehearsal need no owner input at all: they move to Day 3 and run to completion. The owner's dated
   judgment is treated as an **interrupt that may land on any day or not at all**, with the
   manifest-application step defined but unscheduled.
4. **Budget is stated in artifacts, not hours.** Hour estimates calibrated for a person do not
   transfer, and in this repository they invite filling the time. Each day now names what must
   exist when it is done.
5. **Merge sequencing waits for PR #24's first CI run.** #24 targets #22's branch, and the workflow
   only triggers on pull requests to `main`, so #24 has never been checked by hosted CI (Day 1
   finding F3). When #22 merges, GitHub retargets #24 to `main` and the check runs for the first
   time. Treating #24's current clean status as a green build would merge an unexercised branch.
6. **One factual correction.** The draft's read-first list names
   `results/extractor_stress_cases_baseline_2026-09-14.json`; the file is
   `results/extractor_stress_cases_baseline_v3_2026-09-14.json`.

Two things in the draft are deliberately **not** adopted. Day 3's record-integrity checker and
consumer round-trip test are largely already on #22 (`test_a8_*`, `test_a5_*`, `test_a7_*`,
`test_geojson_prefers_path_over_conflicting_chord_and_accepts_legacy_dicts`); rebuilding them would
be duplicate coverage, so Day 3 closes only the measured gaps instead. And the draft's Day 6 "run
the complete repository gate" is folded into the post-merge day rather than run twice.

## Addendum — engineering-audit guidance, 2026-09-21

The owner recorded [ENGINEERING_AUDIT_PLANNING_GUIDANCE_2026-09-21.txt](ENGINEERING_AUDIT_PLANNING_GUIDANCE_2026-09-21.txt)
and linked it from [AGENTS.md](../AGENTS.md). It is a planning reference, not a new result, and it
asks that existing coverage be checked before anything is added. Day 3 checked all six sections and
found three genuine gaps and three principles already satisfied:

| guidance section | state before Day 3 | action |
|---|---|---|
| 1 independently specified expected results | partial — two A4 fixtures carried hand-derived coordinates, the rest asserted properties only, and `baseline_candidates.json` is extractor-generated | closed: hand-derived coordinate lists where the route is uniquely determined, an x/y-versus-row/col assertion, and the baseline's status named in the test module as regression compatibility rather than an oracle |
| 2 coordinate probes | gap — the transform test recomputed its expectation from the same lambda, with equal x and y scale magnitudes | closed: a probe under `(x, y) -> (100 + 2x, 200 - 3y)` with hand-computed expected vertices |
| 3 input changes reach the artifact | already satisfied by the CR-09 `test_a6_*` controls | none; coverage confirmed, nothing added |
| 4 saved export and completed operation | gap — every comparison was in-memory; the atomic-write work was still only planned | closed: a `json.dumps`/`loads` round-trip comparing ids, vertex order, coordinates and path-length semantics, plus the `--out` writer from F2 with validation before replacement |
| 5 evidence provenance | already the repository's discipline | reinforced in the CR-08 packet, which states that the four evidence categories cannot substitute for one another |
| 6 first useful failure signal | already satisfied — the CR-09 evidence discloses the two rejected endpoint rules as development data | none |

The guidance's limits are respected: no CAD or FEA work enters this project, the L1 two-pixel
scoring contract is unchanged, and pixel-space length is not meters.

## Decision gates

Unchanged from the draft: **A** CR-09 stack integrity, **B** consumer consistency, **C** evidence
integrity, **D** CR-08 intake (a real dated judgment, never a worksheet or an AI answer),
**E** Phase-1 screen (real exports through the existing fail-closed CLI; a SCREEN_PASS is a
disturbance screen, not road accuracy). Day 1 recorded A, B and C as **pass**, with findings F1–F3.

## Days

### Day 1 — 2026-09-19 — intake and stack review — **done**
Artifacts: `evidence/task-2026-09-19/README.md` with observed identities, the full gate re-run from
a clean PR #22 checkout (116 passed; record, archives and ranking all reproduce), the derived
acceptance map, and findings F1–F3. No source change.

### Day 2 — 2026-09-20 — owner review request and gallery read
Artifacts: a short review request naming the three PRs, the proposed order and the **one** decision
each needs, not an invitation to read the repository; a written gallery review note for #24 (scores
read from the record not typed, synthetic labelling, component vs exported-line recall kept
distinct, no clipped labels, manifest and guide entries present) with either a clean note or a
named correction list. The gallery is not redesigned this week.

Proposed merge order, unchanged in dependency from the draft: **#22**, then **#24 once its first CI
run on the retargeted base passes**, then **#23**, resolving any changed-line conflicts. #17 and
#18 stay open or closed as historical plan records; history is not rewritten.

### Day 3 — 2026-09-21 — measured gaps, the audit addendum, and the CR-08 packet — **done**
Artifacts: the F1/F2 fix if the owner approves it (an `--out PATH` flag that stages through a
temporary file in the destination directory, validates by parsing it back, then `os.replace`s, plus
the guide and plan verification block pointing at it; stdlib only, one test that a failed run leaves
the committed record untouched); `evidence/task-2026-09-19/cr08-first-site-packet.md` with the
proposed first site, the blank copyable judgment form and the machine-checkable export preflight
checklist from the draft's Task 4.4, both unchanged in content; and the CLI rehearsal against
controlled synthetic and missing-file inputs confirming exit codes 0/1/2/3 and that a missing export
is INCONCLUSIVE rather than a traceback.

### Day 4 — 2026-09-22 — post-merge integration, or the blocker
If the owner approved: merge in the stated order, then run the complete repository gate on merged
`main`, confirm the changed-file boundary is limited to path export, consumers, records, tests,
evidence and the gallery, and reconcile only the authoritative ledger rows and dated progress
entries. If the owner did not approve, or asked for a correction: implement the one named bounded
correction with its acceptance test, and leave the stack open. Either way CR-08 is untouched.

### Day 5 — 2026-09-23 — evaluation protocol and the next-experiment design — **done**
Artifacts: the real evaluation packet template from the draft's Task 5.2 (source commit and manifest
hash, site role and verification provenance, Earth Engine script revision, four per-site CSVs, eight
scene counts, coverage and `n_valid`, primary gate decision, sensitivity only after the primary
decision, exclusions, and the explicit statement that this is a disturbance screen); and
`docs/specs/phase-2-topology-followup/plan.md` comparing Options A/B/C for the one-path-per-component
ceiling exactly as the draft specifies, with Option C (defer topology) the standing recommendation.
Design note only; nothing is implemented.

### Day 6 — 2026-09-24 — review packet and next-week decision
Artifacts: a concise packet linking the merged commits, the v4 record and the v1/v3 archives, the
CR-09 evidence, the five figures, the CR-08 outcome, every command and exit, and **the one** next
decision. The week's focus for the following week is selected: real-data gate, bounded topology
experiment, or a documented pivot.

### Owner input, unscheduled
One dated source-image judgment for one registered development or control site, with provider,
acquisition date, extent, inspector, evidence reference and a confirmed / rejected / uncertain
decision. If it arrives: apply only evidence-supported manifest changes as a minimal reviewable
diff, retaining any superseded coordinate in evidence, regenerate the worksheet, mirror the approved
fields in `gee/ndvi_change.js`, and re-run the static validator and worksheet check. If it does not
arrive, or is rejected, uncertain or inaccessible: the manifest is not touched and CR-08 stays
blocked. `verified=true` is never set to unblock software.

## Adaptive scope

Must-have, nice-to-have, trigger-gated and out-of-scope are adopted from the draft **unchanged**:
land the CR-09 stack safely; preserve and verify v1/v3/legacy records; keep one shared geometry
contract; run the first CR-08 inspection if imagery exists; leave a complete failure taxonomy.
Triggered items stay parked with their stated triggers — skeleton/junction extraction, gap bridging,
OSM conditioning, high-resolution confirmation, activity/recovery classification. Out of scope:
learned classifiers, country-wide search, site replacement, holdout inspection, any new threshold,
tolerance or metric adopted to pass a target, real-road precision claims from synthetic tests, new
heavy geospatial dependencies, and any publication or claimed Earth Engine execution.

## Operating rules and stop rules

Adopted from the draft unchanged. Read the source and its tests first; identify the smallest failing
check; preserve and hash the current record before regeneration; make one narrow change; run the
narrow check then the full gate; record command, exit, version and artifact path. On failure, do not
loosen a threshold first — classify the failure, preserve the output in evidence, and stop dependent
work. On a missing real input, stay INCONCLUSIVE or blocked and invent nothing.

## Definition of done

The draft's definition is adopted unchanged, with one addition from finding F3: **no branch is
merged on the strength of a CI status that never ran.** The strongest available outcome remains a
repository that shows exactly what the synthetic extractor delivers, exactly where it still fails,
and exactly what real input the next scientific claim requires.
