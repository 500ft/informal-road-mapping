# Closeout — 2026-09-25

Owner-independent preparation for this repository, executed against
[docs/CLOSEOUT_PLAN_2026-09-25_CLAUDE_HANDOFF.txt](../../docs/CLOSEOUT_PLAN_2026-09-25_CLAUDE_HANDOFF.txt).
**This closes the preparation work. It does not manufacture research completion.** No site is
verified, no Earth Engine run occurred, no gate, threshold or committed record changed.

## A — PR #37 corrected before merge

The review found a scientific overclaim I had introduced: "23 independent 10 m samples". Dividing
ground area by native pixel area gives an **area equivalent**, and establishes neither the number of
overlapping native pixels nor an effective sample size — footprint shape, grid alignment,
interpolation, sensor spatial response and spatial covariance all bear on that. `min_component_pixels`
is a **geometric selection rule, not a statistical sample-size requirement**.

Also corrected on that branch: "finer than the data supports" became "grid spacing about 1.47x finer
than native 10 m sampling"; the single "~45% overstated" figure was split by dimension (**~47%
linear, ~117% areal** at 47.3 deg N); and "single tracks are not separable by this method" became
"this method has not demonstrated reliable single-track separation", because an unmeasured limit is
not an established impossibility. The test asserting independence was renamed to describe area
equivalents.

## B — missingness sensitivity, exhaustive (package D)

`missingness_sensitivity.py` -> `missingness_sensitivity.json`. **MODEL_CHECKED, not
EARTH_ENGINE_VERIFIED.**

16 histories x 11 retention masks (2, 3 or 4 years retained) = **176 pairs**.

| outcome | pairs |
|---|---:|
| unchanged | 146 |
| fail -> pass | 18 |
| pass -> fail | 12 |

**The finding worth keeping is directional.** Dropping only *quiet* years produced
18 fail->pass flips and
0 pass->fail. Dropping only *disturbed* years
produced 12 pass->fail and
0 fail->pass. So missingness is **not
decision-neutral when it is not random**: losing quiet observations can only help a pixel pass, and
losing disturbed ones can only make it fail.

Flips concentrate where the full history is mixed: all of them occur at full disturbed counts of 2
and 3, and none at 0, 1 or 4. At n=4 nothing can flip by construction.

Boundary semantics pinned from `gee/ndvi_change.js` and asserted against the live source, so a
changed operator invalidates the model rather than leaving it quietly green: disturbance is
**strictly** greater than 0.02 (an effect of exactly 0.02 is **not** disturbed), persistence is
`k/n >= 2/3` evaluated as `3k >= 2n`, eligibility is `n >= 2`. Minimum passing counts are
{'n=2': 2, 'n=3': 2, 'n=4': 3}; n of 0 or 1 is ineligible. A masked year is absent from both k and n
and is **never imputed as a quiet observation**.

**What this does not establish.** It is an arithmetic model of the rule, not an execution of the
Earth Engine calculation. Uniform enumeration is not an empirical probability model for
cloud-related missingness, so any percentage is a fraction of enumerated cases and not an estimated
field failure rate. The 176 pairs share observed histories and are not 176 independent samples.
Early-baseline (2018-2021) support is unmodelled, and all recent comparisons share that baseline.

## C — compositor comparison frozen offline

[docs/specs/compositor-ab/plan.md](../../docs/specs/compositor-ab/plan.md).
**OFFLINE_COMPLETE / REAL_COMPARISON_PENDING.**

Variant A is the current pipeline, unchanged and without B's joint-validity mask imposed on it.
Variant B is now exactly specified: per-acquisition indices from jointly valid bands, both
denominators strictly positive, median over the same eligible set, even counts as the mean of the
two middle values, empty support left masked, everything downstream untouched. The third estimator
(median of a per-acquisition combined index) is explicitly parked.

New hand-derived fixtures: BSI values, a B2/B11-missing case where red and NIR remain valid, a
zero-denominator rejection, an all-invalid year, a single-acquisition year, and an even-count
median. Expected values come from independent arithmetic, not the implementation under test.

Because B changes **both** estimator order **and** common support, the protocol requires
matched-support cases to be tabulated separately. Review triggers are predeclared and are **not**
success criteria for B.

## D — grid runtime probe (package B)

`grid_runtime_probe.js` + `grid_runtime_expectations.json`. **PREPARED_UNEXECUTED** — it needs
authorized Earth Engine access. Syntax-checked with `node --check`. It inspects no registered site
imagery and never touches the holdout.

It measures projection, affine transform, nominal scale, `pixelArea`, one-pixel-east ground
distance, a 50-pixel footprint, and the ring kernel's actual support, at a registered development
latitude **and an equatorial control** that isolates latitude distortion from other error.

Expectations are computed independently — inverse projection plus geodesic formulae, not read back
from the operation under test — and distinguish the spherical approximation from the ellipsoidal
value (dev-01: 6.7816 m spherical against 6.7939 m ellipsoidal, 0.18% apart). Tolerances are
predeclared: 1% spherical-versus-ground, 0.1% between two matched ellipsoidal calculations, 1e-6 for
serialised affine coefficients. **A failed bound is recorded, never silently widened.**

**New requirement covered.** `atAnalysisScale` calls `resample('bilinear')` on derived images
including collection medians, and Earth Engine documents that `resample` needs a meaningful default
projection and warns against applying it to composites. The probe reproduces **both** orders —
composite-then-resample as the code does today, and resample-then-composite — printing the
projection at each step and the numeric difference. An error there is an observed failure to record,
not a licence to edit the live helper during closeout. This is a concern identified from source and
documentation; **no runtime failure has been observed here.**

## E — response design complete

Addendum in [cr08-first-site-packet.md](cr08-first-site-packet.md). **RESPONSE_DESIGN_COMPLETE.**
Provisional preparation order `dev-01-braided` then `negative-01`, documented without another ask:
it changes no site, stratum, coordinate or threshold, and the owner can override it when supplying
evidence. Adds an explicit `unknown` class distinct from `uncertain`, the paired-dated-evidence
requirement for any recovery claim, and a fixed-budget candidate-review pilot reported as **triage
yield, not precision or recall**, with separately inspected prediction-free areas required for any
eventual recall estimate.

## CR-08's actual input state

**Unchanged and blocked.** All six `verified` flags are `false`. No imagery inspected, no Earth
Engine access, no gate result. One dated image would advance intake; it would **not** close the row,
which requires development and control verification *and* runtime access. A new ledger row `CR-P01`
scopes today's preparation separately so CR-08's own acceptance criteria stay intact.

## CAD

External to this repository's completion criteria. The reported host failure was observed in another
session and is not independently reproduced here; absence of suppression instructions in a briefing
does not establish that no API or session-specific solution exists, and absence of a monitor does not
establish whether a GUI session or remote display exists. These stay **unverified conditions with an
external owner**, routed to `engineering-audit`'s backlog, not imported as mapping blockers.

## Checks observed

Run on the combined implementation at this branch's head, in a fresh venv.

| check | command | result |
|---|---|---|
| compile | `python -m compileall -q analysis/catanroads analysis/tests` | exit 0 |
| tests | `PYTHONPATH=analysis MPLBACKEND=Agg python -m pytest analysis/tests -q` | **140 passed** |
| probe syntax | `node --check evidence/task-2026-09-25/grid_runtime_probe.js` | exit 0 |
| GEE static validation | `node tools/validate_phase1.mjs` | exit 0 |
| temporal QA branches | `node tools/test_temporal_qa.mjs` | exit 0 |
| worksheet consistency | `PYTHONPATH=analysis python -m catanroads.site_worksheet --check` | exit 0, no site verified |
| presentation | `tools/check_presentation.py` · `tools/test_presentation.py` | 0 issues, 78 links · OK |
| enumeration reproducibility | `python evidence/task-2026-09-25/missingness_sensitivity.py` | regenerates identically |
| ledger | `csv.DictReader` | parses, 15 rows |
| sites | `config/sites.geojson` | all six `verified` still `false` |

**Inherited results are not reclaimed as today's.** The CR-09 v4 record, the v1/v3 archives and the
five gallery figures were produced on their original commits and are linked, not re-run. The
131-test figure belongs to PR #37's branch; main's earlier evidence reports 129; this branch reports
140 because it adds the package C and D fixtures. **No test count is an acceptance target.**

## State, stated precisely

`READY_FOR_REVIEW` — not `MERGED`, not `COMPLETED_ON_MAIN`. Two pull requests are involved: the
corrected #37, and this closeout. Their merge SHAs are recorded once they land.

## Resumption contract

| input | who | what exactly | resumes |
|---|---|---|---|
| dated scene reference + judgment for `dev-01-braided`, or the name of an available registered control instead | owner | the form in [cr08-first-site-packet.md](cr08-first-site-packet.md); never a credential in this repository | CR-08 intake |
| authorized Earth Engine project/operator, **or** completed export artifacts from the prepared probe | owner | `grid_runtime_probe.js` + the expectations file | package B execution, then compositor A/B on real imagery |
| review of corrected #37 and of this closeout | owner | — | merge |

These may arrive at any time and none of them paused this work.
