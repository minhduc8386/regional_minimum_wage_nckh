# Current Issues and Remediation Plan

## Purpose

This note documents the current unresolved issues in the research repo after merging the latest updates from `main`. The latest merge added enhanced nonlinearity diagnostics, DML K-fold sweeps, a DML variant with province dummies, Causal Forest DML outputs, and a method-comparison table.

The project is now stronger than before, but the interpretation must also become more careful. The central message is no longer simply that there is nonlinearity. The central message is that the results are **specification-sensitive and variation-source-sensitive**.

## Executive Summary

The current repo has:

- a validated balanced province-year panel for 2018-2024;
- baseline OLS/FE/TWFE results;
- raw and residualized LOWESS diagnostics;
- PDP and feature-importance diagnostics;
- formal nonlinearity tests;
- DML stability checks across learners, seeds, folds, and K choices;
- a DML variant with province dummies;
- Causal Forest DML outputs;
- a method-comparison summary.

The main remaining issues are:

1. The official citation/source metadata for `informal_rate` is not fully documented.
2. Province-level wage-region mapping remains an approximation because official wage regions can vary at district level.
3. Most treatment variation appears to be between provinces; within-province DML evidence becomes weak when province dummies are added.
4. OLS/FE/TWFE, DML, and CRF do not give one unified sign.
5. CRF is now implemented, but it is exploratory and statistically uncertain.
6. `min_wage_growth` remains weak as a main treatment.
7. Literature metadata still needs final verification.
8. Some older notes have encoding issues.

The two most important fixes before final submission are:

1. verify and document the official source for `informal_rate`;
2. strengthen or clearly disclose the province-level wage-region approximation.

## Issue 1: `informal_rate` Source And Citation Are Not Fully Documented

### Current Status

The final panel uses:

```text
informal_rate
```

The variable is created from:

```text
data/raw/17_informal_employment_rate_by_province_2018_2024.xlsx
```

The cleaning script is:

```text
scripts/01_clean_nso_province_panel.py
```

Inside the workbook:

```text
Sheet: E02.51
Title: Informal employment rate by province by Cities, provincies and Year
Years: 2018-2024
2024 column: Prel. 2024
```

The workbook inspection did not find a source row inside the sheet. Therefore, the repo currently knows the raw file and table title, but not the final official citation.

### Why This Matters

For a scientific paper, the data section must identify the official data source. A reader should be able to verify:

- the institution or publisher;
- the official table name;
- the definition of informal employment;
- the denominator used for the informal employment rate;
- whether 2024 is preliminary;
- the access date;
- the URL or publication source.

Without this information, the variable is computationally valid but not fully documented for publication.

### Risk Level

High for final paper quality.

Not a code blocker, but a documentation blocker for final submission.

### Minimum Fix

Add a data-source note:

```text
Variable: informal_rate
Raw file: data/raw/17_informal_employment_rate_by_province_2018_2024.xlsx
Sheet: E02.51
Table title: Informal employment rate by province by Cities, provincies and Year
Years: 2018-2024
2024 status: preliminary
Official citation: to verify
```

### Recommended Fix

Create:

```text
reports/data_sources.md
```

and document:

- official publisher;
- official URL or publication;
- access date;
- table title;
- definition notes;
- processing script.

### Strong Fix

Find the official metadata or methodological note defining informal employment. The paper should clarify whether informal employment includes informal wage workers, self-employment, household business workers, agriculture, or other categories.

## Issue 2: Province-Level Wage-Region Mapping Is An Approximation

### Current Status

The mapping source is:

```text
data/raw/policy/province_wage_region_map_raw_2018_2024.csv
```

The mapping script is:

```text
scripts/05_build_province_wage_region_map.py
```

The processed output is:

```text
data/processed/policy/province_wage_region_map.csv
```

The current mapping assigns one wage region to each province-year because the outcome is measured at province-year level. The mapping note states that this is a province-level approximation.

The key issue is that Vietnam's official minimum wage regions can vary at district or urban district level. A single province can contain districts in multiple wage regions.

Current raw mapping inspection showed:

- 441 province-year rows;
- 385 rows flagged as mixed district regions;
- 56 rows marked as mostly one wage region.

### Why This Matters

The outcome is province-year, but treatment may vary within province. Assigning one wage region to an entire province can create treatment measurement error.

This can affect:

- `real_min_wage`;
- `log_real_min_wage`;
- `min_wage_growth`;
- baseline OLS/FE/TWFE estimates;
- DML and CRF estimates.

This issue is especially important because many current estimates are sensitive to model specification.

### Risk Level

High for causal interpretation.

Medium for descriptive/diagnostic analysis.

### Minimum Fix

Keep the current mapping, but explicitly label it:

```text
province-level wage-region approximation
```

Suggested paper wording:

> Because the outcome is observed at province-year level, the minimum wage region is assigned at province-year level. For provinces containing districts in multiple wage regions, the assignment uses a province-level approximation based on the provincial capital. This may introduce treatment measurement error and is treated as a limitation.

### Recommended Fix

Add a flag:

```text
mixed_district_region
```

Then run robustness checks:

1. all province-years;
2. only province-years without mixed district-region flags;
3. possibly province-level groups based on severity of mapping ambiguity.

Suggested outputs:

```text
reports/tables/wage_region_mapping_sensitivity.csv
reports/wage_region_mapping_sensitivity.md
```

### Strong Fix

Build district-year treatment exposure:

1. collect district-year wage-region classifications from each decree;
2. create a district-to-province crosswalk;
3. merge district population, labor force, or employment weights;
4. construct weighted province-year minimum wage exposure.

This would greatly improve treatment measurement, but it requires substantial additional data work.

## Issue 3: Most Treatment Variation Is Between Provinces

### Current Status

The enhanced DML outputs show a critical pattern.

Main DML with controls and year dummies:

- `log_real_min_wage` theta is stable and negative;
- signs are stable across learners, seeds, folds, and K choices;
- average p-value is approximately `0.0293`.

DML with province dummies:

- `log_real_min_wage` theta becomes approximately `-1.87`;
- p-value rises to approximately `0.3096`;
- signs become mixed across learners;
- confidence intervals often contain zero.

The method-comparison table notes that little within-province variation remains after province dummies; roughly 95 percent of D variation is between provinces.

### Why This Matters

This changes the interpretation of DML.

The main DML result is stable, but it is not TWFE-equivalent. It uses a variation source closer to year-FE/between-province comparisons. When the model is pushed toward a within-province comparison, the DML signal weakens.

### Risk Level

High for interpretation.

### Minimum Fix

Always distinguish:

```text
DML with W + year dummies
```

from:

```text
DML with W + year dummies + province dummies
```

Do not compare main DML directly with TWFE as if they use the same variation.

### Recommended Fix

In the results narrative, write:

> The stable negative DML estimate relies mainly on between-province variation. When province dummies are added, the estimate becomes weak and sign-unstable, suggesting limited within-province identifying variation for flexible DML.

### Strong Fix

If the research goal is causal inference, find stronger within-province or quasi-experimental variation:

- longer panel;
- district-level exposure;
- policy shock;
- microdata with richer controls;
- valid instrument or design-based approach.

## Issue 4: OLS/FE/TWFE, DML, And CRF Do Not Give One Unified Sign

### Current Status

For `log_real_min_wage`:

- Pooled OLS + W: negative.
- Year FE + W: negative.
- Province FE + W: positive.
- TWFE + W: positive.
- Main DML: negative.
- DML + province dummies: weak/mixed.
- CRF: broadly negative, but uncertain.

### Why This Matters

This is the central empirical result. The project should not hide the disagreement. The disagreement shows that estimates depend on:

- cross-province differences;
- within-province changes;
- common year shocks;
- nonlinear controls;
- treatment measurement;
- flexible nuisance adjustment.

### Risk Level

High if overclaimed.

Low if framed transparently.

### Minimum Fix

Use the phrase:

```text
specification-sensitive and variation-source-sensitive evidence
```

throughout the results section.

### Recommended Fix

Make the disagreement the main results narrative:

> The evidence does not support one clean causal conclusion. Instead, it shows that the estimated association between regional minimum wages and informal employment depends strongly on model specification and source of variation.

## Issue 5: CRF Is Implemented But Exploratory

### Current Status

CRF is now implemented through:

```text
scripts/20_run_crf_main.py
scripts/21_crf_cate_distribution_heterogeneity.py
scripts/22_crf_stability_by_seed.py
```

Key outputs:

```text
reports/crf_implementation_note.md
reports/tables/crf_ate_results.csv
reports/tables/crf_cate_summary.csv
reports/tables/crf_heterogeneity.csv
reports/tables/crf_stability_by_seed.csv
reports/figures/crf/
```

For `log_real_min_wage`, CRF estimates are broadly negative across seeds, but:

- confidence intervals usually contain zero;
- magnitudes are seed-sensitive;
- CATEs are noisy with only 441 observations.

### Why This Matters

CRF can help explore heterogeneity, but it should not be presented as the main causal estimator.

### Risk Level

Medium if properly framed.

High if treated as causal proof.

### Minimum Fix

Label CRF as:

```text
exploratory heterogeneity analysis
```

### Recommended Fix

Use CRF only after reporting OLS/FE/TWFE and DML. State that it explores whether estimated effects appear heterogeneous across productivity, unemployment, training, and employment scale, but individual CATEs are noisy.

### Strong Fix

Only expand CRF if the paper explicitly includes a heterogeneity research question and can defend the small sample size.

## Issue 6: `min_wage_growth` Remains Weak As A Main Treatment

### Current Status

`min_wage_growth` is unstable:

- TWFE is statistically insignificant;
- DML signs are unstable;
- K-sweep DML shows only 56 percent negative signs;
- confidence intervals often contain zero;
- CRF CATEs are highly dispersed.

### Recommendation

Keep `min_wage_growth` as exploratory only.

Do not use it as the main treatment.

## Issue 7: Enhanced Nonlinearity Diagnostics Strengthen But Do Not Prove Causality

### Current Status

The main branch added:

- residualized LOWESS;
- PDP;
- formal nonlinearity tests;
- feature importance.

These improve the evidence that linear specifications may be restrictive.

### Key Interpretation

The nonlinear structure appears stronger in pooled/year-FE settings than after province effects. This suggests that province-level structure and controls drive much of the nonlinearity.

### Recommendation

Use these diagnostics to justify DML and CRF as robustness tools, not as causal evidence.

## Issue 8: Literature Metadata Needs Final Verification

The repo has useful literature notes, but final publication status and ranking still need checking:

- Nguyen Cuong Viet 2025 publication details;
- whether Del Carpio et al. has a peer-reviewed version or only MPRA/RePEc;
- final ranking/category for Perez Perez (2020) according to the advisor's required database;
- final citation style.

## Issue 9: Some Older Notes Have Encoding Problems

Some older markdown files show corrupted Vietnamese accents and author names. This does not affect the modeling pipeline, but it should be cleaned before final presentation.

## Prioritized Action Plan

## Priority 1: Must Fix Before Final Paper

1. Verify and document the official citation for `informal_rate`.
2. Clearly disclose province-level wage-region approximation.
3. Present the result as specification-sensitive and variation-source-sensitive.
4. Distinguish main DML from DML with province dummies.
5. Label CRF as exploratory heterogeneity analysis.
6. Keep `min_wage_growth` exploratory only.

## Priority 2: Strongly Recommended

1. Create `reports/data_sources.md`.
2. Add a `mixed_district_region` flag.
3. Run wage-region mapping sensitivity checks.
4. Add a short appendix explaining variable construction from raw files.
5. Clean encoding issues in final-facing literature notes.

## Priority 3: Nice To Have

1. Build district-year wage-region treatment exposure.
2. Weight district exposure by employment, labor force, or population.
3. Extend the wage panel backward before 2018 to improve `min_wage_growth`.
4. Replicate or backtest a benchmark paper if replication data are available.

## Updated Bottom Line

The project is stronger after the main merge. It now has richer diagnostics and exploratory CRF outputs. But the stronger evidence also makes the cautious conclusion clearer:

> The current data support a transparent, specification-sensitive empirical study. They do not yet support a definitive causal claim about the effect of regional minimum wages on informal employment.

The most defensible final paper should emphasize:

- TWFE as the main linear panel benchmark;
- DML as flexible-control robustness;
- DML with province dummies as a key sensitivity check;
- CRF as exploratory heterogeneity;
- treatment mapping and data-source documentation as major limitations.

