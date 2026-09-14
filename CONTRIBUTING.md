# Contributing

Changes should make the method easier to reproduce while preserving the
distinction between synthetic tests, source imagery and real-site evaluation.

## Set up and check

Follow the [README](README.md#getting-started) for the Python environment,
editable `analysis[dev]` install and Node.js prerequisite. From the root:

```sh
PYTHONPATH=analysis python -m pytest analysis/tests -q
node tools/validate_phase1.mjs
node tools/test_temporal_qa.mjs
PYTHONPATH=analysis python -m catanroads.site_worksheet --check
```

These are local software checks, not Earth Engine or physical validation.

## Evidence rules

- Add a minimal regression case before fixing a behavioral defect.
- Preserve source dates, provenance and denominators; missing data is not zero.
- Do not change registered sites, thresholds or primary settings after seeing outputs.
- Leave the holdout uninspected until the candidate and evaluation procedure are frozen.
- Mark conceptual diagrams, synthetic examples and measured/source-image evidence explicitly.
- Regenerate figures from their documented source; do not retouch result pixels.
- Do not commit credentials, restricted imagery or unapproved personal information.

The [runbook](docs/PHASE1_RUNBOOK.md), [design](docs/design.md) and
[figure guide](docs/data-and-figures.md) define the detailed contracts.

## Editing convention

Code changes follow the [ponytail ruleset](AGENTS.md): reuse what exists, prefer the
standard library, ship the shortest working diff, and never cut validation, error
handling or the one check that proves the logic.

## Submit a change

Use a focused branch and explain the problem, exact commands, input provenance,
observed result and remaining uncertainty in the pull request. An automated
check does not substitute for source-image verification or independent review.

Repository code uses [MIT](LICENSE); third-party data retains its original terms.
