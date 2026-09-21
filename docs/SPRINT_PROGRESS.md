# Sprint progress — CatanRoads

## 2026-09-12 → 2026-09-16 — stress cases, editing convention, CR-09

- **2026-09-12/13, CR-R03 → R03c** (PRs #12, #13, #14; merged 2026-09-13): the extractor is
  stress-tested beyond its favourable demo on ten fixed constructions; two review repairs moved
  the line layer from the component mask to the exported geometry, then to reference
  centerlines. Finding carried forward: curved corridors passed the component layer and failed
  the exported straight chord. [Evidence](../evidence/task-2026-09-12/README.md).
- **2026-09-14, ponytail** (PRs #15, #16): [AGENTS.md](../AGENTS.md) adopted as the editing
  convention; two refactor passes, −44 lines, records unchanged.
- **2026-09-14/15, CR-09 plan**: #17 (agent draft) superseded by the owner's reviewed #18
  (merged). #19 was built from #17 by mistake and reverted in #20, which also built the reviewed
  contract to its T08 feasibility stop (A3 failed on the wide strip, 0.9688 < 0.98); #21 fixed
  the ledger row.
- **2026-09-16, CR-09 build** (#22, awaiting owner review): amendment A to the endpoint rule
  adopted by the owner; A1–A8 pass; `path_px` delivered through one selector to GeoJSON,
  scoring and the demo; v4 record with chord comparison; 116 tests.
  [Plan](PLAN_2026-09-14_CR09.md) · [Evidence](../evidence/task-2026-09-14/README.md).
- **CR-08** unchanged: all six sites unverified; no imagery inspected; the intake path was
  re-checked on 2026-09-16 (see [REVIEW_READY.md](REVIEW_READY.md)).


## 2026-09-11 — evidence-gap correction

The [current correction](COMPLETION_RECONCILIATION.md) supersedes any interpretation that earlier preparation closed a physical, approval, or source-review gate. Work is on `fix/evidence-gaps-20260911` from current renamed main; historical entries below retain their original dates and PR snapshots. The original day-3 and presentation PRs are now merged, but this correction is a new reviewable change, not an asserted merge or publication.

Each omitted or incomplete recommendation is accounted for separately in the current correction and existing task ledgers. No owner signature, measurement, PI conversation, imagery judgment, disclosure approval or independent review was fabricated. Exact tests, scope and next inputs are linked from the correction record; actual delivery state is established by its PR.

## Day-3 work — 2026-09-09

Delivery update: the preparation was committed as 500ft and pushed; [day-3 PR](https://github.com/500ft/informal-road-mapping/pull/8) is open against main. Initial implementation source: `b3e7797f62ac2a8b1c0cd630b5d2455a9bfb2b52` (later review/documentation commits are visible in the PR). This supersedes the pre-push stopping state below. Original day-1/day-2 PRs are merged; this new PR is not merged. Resume from the named unresolved project gates in [DAY3_PLAN.md](DAY3_PLAN.md), not from the already completed push step.

Both reviewed PR layers merged into main; new work starts from `346b942b6de2ade58d40f2dfe367cbd086370d87` on `task/day-three-20260909`. Five generated-worksheet tests cover holdout omission, unchanged eligibility, future site inclusion, duplicate IDs and committed output consistency. 63 analysis tests and both Node checks pass. All six sites remain unverified; no imagery or Earth Engine evaluation occurred.

The [evidence record](../evidence/task-day3-2026-09-09/README.md) contains checks and limits. Work is locally verified and not yet recorded here as pushed/merged. Current edits belong to this task; original checkouts were preserved. Next: finish verification, commit the bounded change and open the new PR; preserve all stated external gates.

## 2026-09-09 — review amendment to CR-D02

Reproduced three filename-handling failures in the rehearsal; fixed literal
argument substitution and clarified that importability is not package-install
validation. Full suite now 58 passed; both Node checks, compile and whitespace
pass. Enabled CI for the existing manual stack's base; hosted status remains
separate until observed. [Review evidence](../evidence/review-2026-09-09/README.md).
CR-08 and all site/measurement flags remain unchanged. Review branch
`review/day-two-20260909`; delivery will amend PR #7, not merge either layer.

## 2026-09-09 — CR-D02 runbook rehearsal

Executed the Phase-1 runbook's gate command *as written in the document* against synthetic
fixtures, through a subprocess, in [7 tests](../analysis/tests/test_runbook_rehearsal.py): synthetic
→ `DEVELOPMENT_ONLY` (3); the committed unverified manifest → `INCONCLUSIVE` (2) even with good
metrics; missing export → `INCONCLUSIVE`, no traceback; exit table equals the CLI mapping. Renaming a
flag or altering the exit table in the runbook fails the suite. Full suite 55 passed. Software
preparation only; CR-08 unchanged. [Verification](../evidence/task-2026-09-09/README.md).
Branch `task/priority-two-20260909`.

## 2026-09-08 — CR-D01 temporal QA follow-up

Completed one bounded P1 software task after the original 30h sprint; its original
rows and evidence are preserved. Base `b4cee1fcb2d6e0cc62b4c48699fa692e7b774ef9`,
branch `task/priority-one-20260908`, isolated worktree under
`/Users/redhose/Developer/daily-prs/2026-09-08/CatanRoads`.
[Review and reproduction](../evidence/task-2026-09-08/README.md): 48 Python tests,
Node branch/schema and static checks pass. Empty annual collections retain
masked bands; exported scene QA is required at intake. Candidate commit/push
identity is recorded in the PR. CR-08 remains owner-blocked; no imagery run.
Next command: `node tools/test_temporal_qa.mjs`; next external task CR-08.

## 2026-09-06 — Partial handoff

- Sprint start2026-09-05; canonical checkout `/Users/redhose/Developer/research-sprints/2026-09-05/CatanRoads` (historical path; the repository was renamed and the current canonical clone is `~/Developer/repo-professionalization-20260910/informal-road-mapping`).
- Branch `sprint/evidence-integrity-20260905`; HEAD/base `690c2fcf88bbe689bd006cce91863821a39edb2a`.
- Seven Agent tasks done with linked evidence; CR-08 blocked on: Dated imagery/site verification and Earth Engine runtime credentials are not supplied. The existing unverified sites remain unverified. Hosted Actions requires a separately authorized push.
- 35 tests passed (9 existing plus26 intake cases); static GEE validator passed; 6/6 installed-CLI cases matched.
- [Final checks](../evidence/sprint-2026-09-05/final-checks.json), [candidate](../evidence/sprint-2026-09-05/candidate.json), [original expectations](../evidence/sprint-2026-09-05/evaluation-plan.md), [outcomes](../evidence/sprint-2026-09-05/evaluation.json).
- These are developer software checks; no physical/new scientific results. Catan's real-data arm, where applicable, stays blocked despite its software fallback evaluation.
- Handoff was prepared before commit; the PR records the final commit and push. Original user changes remain untouched.
- Next verification command: `python evidence/sprint-2026-09-05/evaluate_candidate.py`.
- Exact next task: CR-08: provide dated site verification and actual GEE exports per docs/PHASE1_RUNBOOK.md.
- Owner action moved to Day1 (2h); Day1 now7h, Day6 now2h, total30h. External turnaround is not accelerated.

## Baseline and interrupted execution

Baseline commands, outputs and identity remain in [evidence](../evidence/sprint-2026-09-05/baseline.json). Plans were saved before behavior changes. Runtime-limit pauses were followed by resuming the existing worktree; no baseline or external reply was invented. Original failing cases and corrected behavior are linked in [REVIEW_READY.md](REVIEW_READY.md).
