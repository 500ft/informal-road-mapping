# Compositor A/B — frozen offline protocol

Prepared 2026-09-25. **Status: OFFLINE_COMPLETE / REAL_COMPARISON_PENDING.** Nothing in production
changed. This freezes one comparison before any real output is seen; it does not establish that
either estimator is better.

## Why this exists

`julyS2` takes a per-band median, and `julyComposite` then forms NDVI and BSI from those medians.
Forming a ratio from independently medianed bands is a different estimator from summarising
per-acquisition ratios, and the two do not commute. A hand-derived counterexample already on main
proves the difference exists (red `[0.10, 0.40, 0.30]`, NIR `[0.20, 0.50, 0.90]`: ratio-of-medians
`0.25`, median-of-ratios `1/3`). **Which estimator is preferable here is unmeasured.**

## Variant A — the baseline, unchanged

Exactly the current pipeline: per-band median of B2/B3/B4/B8/B11 within July, then NDVI and BSI
from those medians. **Do not impose B's joint-validity mask on A** — with that imposed A is no
longer the baseline, and the comparison would confound two changes.

## Variant B — frozen before any real output

1. **Alignment.** For a given acquisition, B2/B4/B8/B11 are placed on a declared common grid under
   an explicit per-band resampling contract. B11's native sampling is 20 m; the others are 10 m.
   *Offline fixtures are already aligned and therefore cannot validate this step* — it is a
   geospatial concern for the real comparison only.
2. **Eligibility.** An acquisition contributes only if **all four bands are valid and finite** and
   **both index denominators are strictly positive**. A valid zero reflectance is a number;
   missingness is a separate mask and is never encoded as zero.
3. **Indices, per acquisition.**
   `NDVI = (B8 − B4) / (B8 + B4)`,
   `BSI  = ((B11 + B4) − (B8 + B2)) / ((B11 + B4) + (B8 + B2))`.
4. **Within-July summary.** Median NDVI and median BSI over the **same eligible acquisition set**.
   Even counts take the mean of the two middle values. Empty support stays masked and contributes
   no invented annual value.
5. **Everything downstream unchanged:** across-year medians, the change calculation, annual
   comparisons, persistence rules and all thresholds.

**Explicitly parked:** the third estimator, "median of a per-acquisition combined disturbance
index". Naming it here prevents it drifting into scope later.

## What would prompt scientific review

These are **review triggers, not success criteria for B**:

- any eligibility or gate-verdict flip;
- altered component membership;
- a sign reversal in signed disturbance;
- a changed candidate-review outcome.

Record continuous differences even when none of these occur. Because B changes **both** the
estimator order **and** the common support, tabulate matched-support cases separately — otherwise a
difference caused by dropped acquisitions would be misattributed to compositing order.

Improvement cannot be declared from this comparison. It requires independent imagery judgments and
an agreed review burden.

## Offline checks that exist

In `analysis/tests/test_support_and_compositing.py`, with expected values derived by hand rather
than from the implementation under test: the NDVI non-commutation counterexample and the
missing-band case (both already on main), plus hand-derived BSI values, a B2/B11-missing case where
red and NIR remain valid, a zero-denominator case, an all-invalid year, a single-acquisition year,
and an even-count median.

## Resumption contract

Needs: authorized Earth Engine access, fixed AOIs, dates, masking, grids and samples declared
before predictions are read. Discordant locations are reviewed **blind to which variant produced
them**. A larger candidate fraction is not an improvement criterion.
