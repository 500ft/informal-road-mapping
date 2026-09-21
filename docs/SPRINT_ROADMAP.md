# CatanRoads — Six-day evidence-integrity sprint

Prepared: 2026-09-05. Budget: 30 focused hours; optional Day 7 adds at most 4 hours for owner review only. Days are effort groupings, not unattended calendar commitments. Status lives only in [SPRINT_TASKS.csv](SPRINT_TASKS.csv).

## A. Outcome and baseline identity

A reproducible, fail-closed Phase-1 evidence intake and locally verified CI configuration that distinguishes QA runs from eligible Mongolia disturbance-screening results; real-site claims remain blocked until reference verification.

Publication-state update (2026-09-06): the owner authorized local commits, branch
pushes, and pull requests for this sprint. This does not authorize deployment,
research publication, outreach, spending, or any blocked physical/data action.

Audience: engineering/research reviewer and graduate-application portfolio reader.
Canonical sprint checkout: `/Users/redhose/Developer/research-sprints/2026-09-05/CatanRoads` (historical path; the repository was renamed and the current canonical clone is `~/Developer/repo-professionalization-20260910/informal-road-mapping`).
Remote: https://github.com/500ft/informal-road-mapping (then named CatanRoads). Base: `690c2fcf88bbe689bd006cce91863821a39edb2a`.
Branch: `sprint/evidence-integrity-20260905`. Prepared from freshly fetched origin/main, not from original dirty drafts.
Original checkout: `/Users/redhose/.graphify/repos/500ft/CatanRoads`; preserved. New sprint checkout was clean before evidence capture. No commit, push, publication, purchase, deployment or outreach is claimed or planned as an automatic action.

## B. Verified baseline and priority gaps

Verified: config/sites.geojson has six unverified starting guesses; GEE candidateMask is positive disturbance, including a recovering site whose expected sign is opposite. Current gate counts large components, not roads. No installed .github/workflows exists; proposed patch is not active CI.

Sources inspected: [config/sites.geojson](../config/sites.geojson), [gee/ndvi_change.js](../gee/ndvi_change.js), [tools/validate_phase1.mjs](../tools/validate_phase1.mjs), [docs/design.md](../docs/design.md), [README.md](../README.md), [analysis/pyproject.toml](../analysis/pyproject.toml), [ci-proposed/README.md](../ci-proposed/README.md).
[Actual baseline command outputs](../evidence/sprint-2026-09-05/baseline.json) record working directories, runtime versions, outputs and exit statuses. Alleged defects become reproduced failures only when the red tests record them. Test counts are not research performance.

Verified existing commands (repository root; local Python may need the recorded readline workaround):

```sh
PYTHONPATH=analysis python -c 'import sys, types; sys.modules["readline"] = types.ModuleType("readline"); import pytest; raise SystemExit(pytest.main(["-q"]))'
node tools/validate_phase1.mjs
```

No separately configured typechecker/linter was found in this scoped configuration. Use compileall for changed Python, relevant tests, existing CI commands and `git diff --check`; do not call syntax compilation a typecheck. Proposed test/CLI paths below do not exist until implemented.

## C. Scope, ownership and critical path

Must-haves: repaired claim/validation boundary; regression evidence including original failures; consistent operative scope; reproducible local delivery/check commands; review index identifying unresolved external work.
Exclusions: No network graph/OSM tracing implementation, active/abandoned classifier, coordinate guesses relabeled verified, retuned preregistered thresholds, or claimed Mongolia results.
Owner/External dependencies: Dated imagery/site verification and Earth Engine runtime credentials are not supplied. The existing unverified sites remain unverified. Hosted Actions requires a separately authorized push.
Critical path: baseline → regression failure → minimal correction → full affected checks → candidate identity/selection freeze → bounded evaluation → review packet. Prepare owner requests on Day1; replies do not block independent code fixes. External feedback is not presumed.

## D. Daily budget

September6 reconciliation: owner resource/reference actions start on Day1 rather
than after the evaluation packet. This moves two estimated hours forward; total
remains30. External turnaround is not compressed by this workload allocation.

| Day | Hours | Primary deliverable |
|---|---:|---|
| 1 | 7 | Baseline/scope (5 Agent hours), early resource/provenance action (2 Owner hours) |
| 2 | 5 | Make eligibility a tested executable gate |
| 3 | 6 | Install local CI workflow and reconcile sign/scope |
| 4 | 4 | Freeze intake candidate and real-data run instructions |
| 5 | 6 | Evaluate selected real sites if eligible; otherwise fail-closed delivery evaluation |
| 6 | 2 | Review packet; external feedback remains conditional |
| Total | 30 | Local evidence-ready candidate or explicitly partial handoff |

## E. Ordered tasks and done conditions

### CR-01 — Day 1: Capture baseline and reproduce audit hypotheses

Priority: P0 · Owner: Agent · Focused hours: 3 · Depends on: none.
Files: config/sites.geojson; gee/ndvi_change.js; tools/validate_phase1.mjs; docs/design.md; README.md; analysis/pyproject.toml; ci-proposed/README.md.
Deliverable / Done when: Record base identity, clean sprint start, versions, exact CI commands and observed outputs; preserve original worktree changes.
Verification: PYTHONPATH=analysis python -c 'import sys, types; sys.modules["readline"] = types.ModuleType("readline"); import pytest; raise SystemExit(pytest.main(["-q"]))'
node tools/validate_phase1.mjs
Evidence to retain: evidence/sprint-2026-09-05/baseline.json.

### CR-02 — Day 1: Freeze scope and evidence-first execution design

Priority: P0 · Owner: Agent · Focused hours: 2 · Depends on: CR-01.
Files: NEW docs/SPRINT_ROADMAP.md; NEW docs/SPRINT_TASKS.csv; NEW docs/SPRINT_PROGRESS.md; NEW docs/REVIEW_READY.md.
Deliverable / Done when: Six-day30h plan saved, requirements testable, user-provided plan-and-execute authorization recorded, external authority excluded.
Verification: Review this roadmap and parse task CSV; hours sum to30.
Evidence to retain: docs/SPRINT_ROADMAP.md.

### CR-03 — Day 2: Make eligibility a tested executable gate

Priority: P0 · Owner: Agent · Focused hours: 5 · Depends on: CR-02.
Files: NEW analysis/catanroads/phase1_gate.py; NEW analysis/tests/test_phase1_gate.py; config/sites.geojson; README.md.
Deliverable / Done when: Unverified sites, missing dates, duplicate site metrics, nonfinite/out-of-range fractions, low coverage and missing rows cannot PASS; all primary thresholds retained; no real result invented.
Verification: PYTHONPATH=analysis python -m pytest analysis/tests/test_phase1_gate.py -q; proposed CLI python -m catanroads.phase1_gate --help
Evidence to retain: command, inputs, outputs and exit status under evidence/sprint-2026-09-05/; link from task ledger.

### CR-04 — Day 3: Install local CI workflow and reconcile sign/scope

Priority: P0 · Owner: Agent · Focused hours: 6 · Depends on: CR-03.
Files: NEW .github/workflows/ci.yml; ci-proposed/README.md; README.md; docs/design.md; config/sites.geojson.
Deliverable / Done when: Workflow invokes real Python tests and static JS check; local success not called hosted CI; recovery/stable corridors are not claimed detected by positive change; frozen sites not silently swapped to pass.
Verification: PYTHONPATH=analysis python -m pytest analysis/tests -q; node tools/validate_phase1.mjs; manually compare workflow commands with local log.
Evidence to retain: command, inputs, outputs and exit status under evidence/sprint-2026-09-05/; link from task ledger.

### CR-05 — Day 4: Freeze intake candidate and real-data run instructions

Priority: P1 · Owner: Agent · Focused hours: 4 · Depends on: CR-04.
Files: NEW evidence/sprint-2026-09-05/candidate.json; NEW docs/PHASE1_RUNBOOK.md; docs/REVIEW_READY.md.
Deliverable / Done when: Exact external inputs, expected CSV schema, fixed thresholds, selection rules and missing-year QA listed; installed Python package/CLI exercised without GEE results.
Verification: python -m pip install -e ./analysis --no-deps; python -m catanroads.phase1_gate --help; git diff --check
Evidence to retain: command, inputs, outputs and exit status under evidence/sprint-2026-09-05/; link from task ledger.

### CR-06 — Day 5: Evaluate selected real sites if eligible; otherwise fail-closed delivery evaluation

Priority: P1 · Owner: Agent · Focused hours: 6 · Depends on: CR-05.
Files: config/sites.geojson; NEW evidence/sprint-2026-09-05/evaluation-plan.md; NEW evidence/sprint-2026-09-05/evaluation.json.
Deliverable / Done when: Freeze independently verified development/control sites before GEE predictions; retain CSV/scene provenance. If absent, mark real evaluation blocked and evaluate only intake counterexamples, not road precision.
Verification: Follow docs/PHASE1_RUNBOOK.md; evaluate exported metrics with recorded CLI; preserve all outcomes and exclusions.
Evidence to retain: command, inputs, outputs and exit status under evidence/sprint-2026-09-05/; link from task ledger.

### CR-07 — Day 6: Assemble partial or real-data review packet

Priority: P1 · Owner: Agent · Focused hours: 2 · Depends on: CR-06.
Files: docs/REVIEW_READY.md; docs/SPRINT_PROGRESS.md; docs/SPRINT_TASKS.csv.
Deliverable / Done when: Packet distinguishes implemented intake, local workflow validation and actual external run state; no invented unseen-road performance.
Verification: Run all baseline commands; git diff --check; verify relative links and evidence states.
Evidence to retain: command, inputs, outputs and exit status under evidence/sprint-2026-09-05/; link from task ledger.

### CR-08 — Day 1: Owner verifies reference sites and Earth Engine access

Priority: P0 · Owner: Owner · Focused hours: 2 · Depends on: CR-02.
Files: config/sites.geojson; docs/PHASE1_RUNBOOK.md.
Deliverable / Done when: Dated high-resolution provenance and site selection approved before gate results; runtime access supplied or real-data task explicitly blocked.
Verification: Manually verify dev/control sites in dated imagery; execute Code Editor export tasks only with appropriate access.
Evidence to retain: command, inputs, outputs and exit status under evidence/sprint-2026-09-05/; link from task ledger.


## F. Evaluation and overrun policy

Existing audit counterexamples and all tests inspected while fixing are development evidence, not held-out evaluation. Before Day5, freeze a candidate source/diff identity and selection procedure; save expected judgments before predictions where meaningful. Any observed case used to fix the candidate becomes development material; record that and select new cases for a revised candidate. Hashes identify bytes, not independence. No AI peer is called an independent human reviewer.

If the implementation consumes extra time, cut optional model breadth, cosmetic changes and additional fixtures; never relax numerical thresholds, remove rejection checks or relabel missing measurements. Day7 may add up to4 owner-review hours (34 maximum) only by explicit rebaseline. Do not convert lab lead time into nominal coding hours. Stop affected work at missing authority; proceed with independent authorized tasks. Unavailable external evidence produces a partial handoff, not a completed empirical claim.

Follow-up review checks: reproduce original failures and repaired counterexamples, repeat real commands, inspect runtime and evidence provenance, distinguish local tests from hosted/deployed/physical outcomes, and assess scientific wording independently.

## G. Execution record and first action

[Ledger](SPRINT_TASKS.csv) · [Progress](SPRINT_PROGRESS.md) · [Review index](REVIEW_READY.md).
First behavior-changing action: CR-03; write its regression input, observe failure on baseline, then make the minimal correction. User has authorized plan-and-execute now. No additional start confirmation is required for this bounded scope.
