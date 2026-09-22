# Literature

Why this folder exists: as of 2026-09-22 the repository contained **no citations at all**, while
[docs/design.md](../docs/design.md) made a dozen specific, checkable methodological claims — that a
2.5–3 m track is sub-pixel at 10 m, that abandoned tracks stay visible for years, that NDVI and
bare-soil indices are not independent, that a ridge-and-skeleton pipeline is the likely extraction
method, that OSM seeding risks baking in mapping bias. Those claims were reasonable and unsourced.
This folder attaches evidence to them, and says plainly where no evidence was found.

## How to read this folder

| file | what it is |
|---|---|
| [bibliography.md](bibliography.md) | every paper found, grouped by theme, with a one-line finding, why it matters here, and two grades |
| [claim-ledger.md](claim-ledger.md) | each claim this project already makes, mapped to the papers that support or challenge it |
| [gaps.md](gaps.md) | what the literature does **not** settle, and what this project must therefore establish itself |
| [references.bib](references.bib) | BibTeX for entries with a verified DOI |

## The question this review answers

> For a coarse satellite screen that flags persistent surface-disturbance corridors as candidate
> unmapped informal roads in the Mongolian steppe and Gobi, and hands them to higher-resolution
> confirmation: what is already known about (a) detecting unpaved and off-road tracks from
> imagery, (b) the change-detection and index choices the screen depends on, (c) the ridge and
> centreline extraction it uses, (d) how such linear output should be evaluated, and (e) the
> failure modes — linear non-road confounds, arid-site index weakness, and reference-data bias?

## Method, and the two grades

Following the separation that keeps fame from buying relevance: **aboutness** was decided first,
from title and abstract only, and **importance** only afterwards, among papers that passed.

**Aboutness (0–3).** 3 = core, directly about this question. 2 = relevant method family or study
system. 1 = tangential background. 0 = excluded, not listed here.

**Evidence (A–D).** A = replicated, or validated against independent reference data. B = a single
well-controlled study or benchmark validation. C = method, model or simulation without external
validation, or small-n. D = position paper, commentary, preprint, or qualitative argument.

The two grades are never blended into one score. A heavily cited paper that is tangential stays
tangential.

## Verification policy — read this before citing anything here

Every entry was produced by an actual literature search, not from recall. Each carries a
**transcription confidence**. An entry marked *medium* or *low* has some field — usually the venue,
volume or DOI — that was not confirmed against the publisher record.

- **Do not cite a `low` entry in anything that leaves this repository** until it is checked.
- An entry with no DOI is *unverified*, not *unimportant*, and is capped below verified entries.
- Where a search returned nothing for a claim, that is recorded in [gaps.md](gaps.md) as an absence
  of found evidence, which is not the same as evidence of absence.

This folder is a reading list and a claim map. It is **not** a systematic review: there was no
protocol registered in advance, no database-coverage guarantee, and no second reviewer. It cannot
establish that any idea here is globally novel, only that it is distinct within what was retrieved.

## Scope boundary

Nothing in this folder changes a threshold, a site, the holdout policy, or the Phase-1 gate, and
nothing here is a result. CR-08 remains the only research gate: no imagery has been inspected and
no Earth Engine export exists.
