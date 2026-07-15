# Current Issues and Remediation Plan

## Purpose

This note documents the main unresolved issues in the current research repo and proposes concrete remediation steps. The goal is to make the project more transparent, auditable, and suitable for a scientific research paper.

The issues below do not mean the current pipeline is unusable. They mean that some claims must be written cautiously, and some data/method details should be strengthened before final submission.

## Executive Summary

The current repo already has a working province-year panel for Vietnam from 2018 to 2024, baseline OLS/FE/TWFE results, nonlinearity diagnostics, and DML robustness checks. The main remaining concerns are:

1. The exact citation/source metadata for `informal_rate` is not fully documented.
2. The province-level wage-region mapping is an approximation because official minimum wage regions can vary at district level.
3. The current DML implementation is useful as robustness, but it is not a full causal design and does not fully reproduce province fixed effects in the nuisance functions.
4. OLS/FE/TWFE and DML results differ in sign, so the empirical narrative must emphasize specification sensitivity.
5. CRF is not implemented and should remain blank.
6. Some literature metadata still needs final verification before submission.

The strongest immediate fix is to create a transparent data-source and treatment-mapping note, then run robustness checks around the wage-region mapping if time allows.

## Issue 1: `informal_rate` Source and Citation Are Not Fully Documented

### Current Status

The final panel uses:

```text
informal_rate
```

The variable is created from the raw Excel file:

```text
data/raw/17_informal_employment_rate_by_province_2018_2024.xlsx
```

The cleaning script is:

```text
scripts/01_clean_nso_province_panel.py
```

Inside the workbook, the relevant sheet is:

```text
E02.51
```

The title row in the sheet is:

```text
Informal employment rate by province by Cities, provincies and Year
```

The sheet contains yearly values for 2018-2024, including `Prel. 2024`. However, during inspection, no explicit source row was found inside the workbook.

### Why This Matters

For a research paper, saying that the data came from a local Excel file is not enough. A reader needs to know the official source of the data.

The paper should be able to answer:

- Which institution published the data?
- What is the exact table name?
- Is the 2024 value preliminary?
- Was the table downloaded from an official portal, statistical yearbook, or manually compiled?
- What is the access date?
- Is there a URL or publication reference?

Without this information, the variable is technically usable in the code pipeline, but the paper's data section remains incomplete.

### Risk Level

Medium to high for final paper quality.

This is not a computational blocker because the variable exists and validates correctly. It is a documentation and credibility issue.

### How To Fix

#### Minimum Fix

Create a data-source note that records the current known information:

```text
Variable: informal_rate
Raw file: data/raw/17_informal_employment_rate_by_province_2018_2024.xlsx
Sheet: E02.51
Table title: Informal employment rate by province by Cities, provincies and Year
Years: 2018-2024
2024 status: preliminary
Current citation status: source institution/link still needs verification
```

Then write in the paper:

> Informal employment rates are taken from the province-level statistical table "Informal employment rate by province by Cities, provincies and Year" for 2018-2024. The 2024 value is preliminary. The final citation to the official statistical source will be verified before submission.

This is acceptable for an internal draft, but not ideal for final submission.

#### Recommended Fix

Find the official source of the Excel table and record:

- Official institution name, likely GSO/NSO if verified.
- Official table title.
- URL or publication name.
- Download/access date.
- Whether 2024 is preliminary.
- Any definitions/notes attached to informal employment.

Then create or update:

```text
reports/data_sources.md
```

with a structured citation entry.

Suggested entry format:

```text
### Informal employment rate

- Variable in repo: `informal_rate`
- Raw file: `data/raw/17_informal_employment_rate_by_province_2018_2024.xlsx`
- Sheet/table: `E02.51`
- Table title: `Informal employment rate by province by Cities, provincies and Year`
- Publisher: [to verify]
- URL/publication: [to verify]
- Years used: 2018-2024
- Note: 2024 is preliminary in the source table.
- Processing script: `scripts/01_clean_nso_province_panel.py`
```

#### Strong Fix

If the official source has methodological notes, add a short definition note:

- What counts as informal employment?
- Is the denominator total employed persons?
- Does the measure include agriculture, household business, self-employment, or informal wage work?
- Are definitions stable across years?

This would make the outcome variable much more defensible in the paper.

## Issue 2: Province-Level Wage Region Mapping Is an Approximation

### Current Status

The current treatment mapping is created from:

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

The mapping note is:

```text
reports/province_wage_region_mapping_notes.md
```

The current script explicitly states that the mapping is a province-level approximation. It assigns one wage region to each province-year because the research panel is at province-year level.

However, Vietnam's minimum wage regions are officially defined at more detailed administrative levels in many cases. A province can contain districts, urban districts, towns, or provincial cities assigned to different wage regions.

The raw mapping currently includes:

```text
province-level approximation based on provincial capital; mixed district regions
```

for many rows.

Current inspection shows:

- 441 province-year rows in the mapping.
- 385 rows flagged as mixed district regions.
- 56 rows marked as mostly one wage region.

### Why This Matters

The outcome is measured at province-year level:

```text
province x year
```

But the official treatment assignment can vary within province:

```text
district or urban district x year
```

This creates treatment measurement error. For example, if a province contains both Region I and Region II districts, assigning the whole province to one region based on the provincial capital may overstate or understate actual exposure for workers in other districts.

This matters especially because the treatment variables are central:

```text
real_min_wage
log_real_min_wage
min_wage_growth
```

If treatment is measured with error, estimated coefficients can be biased or unstable. It also weakens causal interpretation.

### Risk Level

High for causal interpretation.

Medium for descriptive/diagnostic analysis.

The current mapping is still usable as an approximation, but the paper must state it clearly.

### How To Fix

#### Minimum Fix

Keep the current mapping, but explicitly label it:

```text
province-level wage-region approximation
```

In the data section, write:

> Because the outcome is observed at province-year level, the minimum wage region is assigned at province-year level. For provinces containing districts in multiple wage regions, the assignment uses a province-level approximation based on the provincial capital. This may introduce treatment measurement error and is treated as a limitation.

This is enough for a transparent internal draft.

#### Recommended Fix

Add a binary flag:

```text
mixed_district_region
```

where:

```text
1 = province-year contains mixed district wage regions
0 = province-year is mostly one wage region
```

Then use this flag in robustness checks:

1. Main sample: all province-years.
2. Restricted sample: province-years not flagged as mixed district regions.
3. Sensitivity table: compare TWFE and DML direction across both samples.

Potential output files:

```text
reports/tables/wage_region_mapping_sensitivity.csv
reports/wage_region_mapping_sensitivity.md
```

Suggested interpretation:

- If results are similar, mapping approximation is less concerning.
- If results change sharply, treatment measurement is an important limitation.

#### Strong Fix

Build district-year treatment exposure.

Required inputs:

- District-year wage region assignments from each minimum wage decree.
- District population, labor force, employment, or working-age population weights.
- District-to-province crosswalk for 2018-2024.

Then construct a province-year weighted treatment:

```text
province_real_min_wage = weighted average of district-level real minimum wage
```

Possible weights:

- district employed persons
- district labor force
- district working-age population
- district population

If no weights are available, use unweighted district average as a second-best option.

This would make the treatment much stronger, but it requires substantial additional data work.

## Issue 3: `min_wage_growth` Is Weak as a Main Treatment

### Current Status

The project currently includes:

```text
min_wage_growth
```

This variable is computed from `real_min_wage` by wage region over time in:

```text
scripts/07_merge_final_analysis_panel.py
```

The 2018 value is filled as 0 because it is the first year in the panel.

DML and baseline results show that this treatment is weak:

- TWFE estimate is statistically insignificant.
- DML average p-value is high.
- DML confidence intervals contain zero in all main runs.
- Fold-level DML signs are unstable.

### Why This Matters

Growth treatment may be conceptually appealing because it measures policy change, not policy level. However, in this panel it appears noisy and unstable.

Also, filling the first year with 0 is a practical choice, but it can create an artificial value for 2018. This does not necessarily break the model, but it should be documented.

### Risk Level

Medium.

This is not a pipeline error, but it is risky to present `min_wage_growth` as a main treatment.

### How To Fix

#### Minimum Fix

Do not use `min_wage_growth` as a main treatment.

Label it as:

```text
exploratory treatment
```

or:

```text
appendix robustness only
```

#### Recommended Fix

When reporting `min_wage_growth`, explicitly say:

> The growth treatment is exploratory because its estimates are statistically weak and unstable across DML folds. The first year is filled with zero because no lagged real minimum wage is observed within the 2018-2024 panel.

#### Strong Fix

Extend the wage panel backward before 2018 if possible, so that the 2018 growth rate can be computed from a real 2017 value rather than filled as 0.

## Issue 4: DML Is Robustness, Not Stand-Alone Causal Identification

### Current Status

The DML script is:

```text
scripts/13_run_dml_theta_stability.py
```

The key outputs are:

```text
reports/tables/dml_main_results.csv
reports/tables/dml_theta_stability.csv
reports/tables/dml_theta_by_fold.csv
reports/tables/dml_theta_by_seed.csv
reports/tables/dml_theta_by_learner.csv
reports/dml_results_summary.md
reports/dml_theta_convergence_interpretation.md
```

The preferred DML treatment is:

```text
log_real_min_wage
```

The DML theta for `log_real_min_wage` is stable and negative across most checks. However, the current DML setup:

- uses a small sample of 441 observations;
- includes year dummies but not full province fixed effects in the nuisance functions;
- uses row-level cross-fitting rather than province-grouped cross-fitting;
- does not create exogenous treatment variation.

### Why This Matters

DML can help control flexibly for observed confounders, but it does not solve identification by itself.

In this project, DML should answer:

> Does the estimated treatment parameter remain stable after flexible nuisance adjustment?

It should not be used to claim:

> DML proves the causal effect of minimum wages on informal employment.

### Risk Level

High if overinterpreted.

Low if clearly framed as robustness.

### How To Fix

#### Minimum Fix

Keep the current DML outputs, but always label them as:

```text
flexible-control robustness
```

Never call DML the main causal estimator.

#### Recommended Fix

Add province-grouped cross-fitting:

- Keep all observations from the same province in the same fold.
- This avoids training on some years of a province and testing on other years of the same province.
- It better respects panel dependence.

Suggested output:

```text
reports/tables/dml_theta_grouped_folds.csv
reports/dml_grouped_fold_robustness.md
```

#### Strong Fix

Develop a clear identification strategy before using DML for causal claims. Possible directions:

- district-level data with stronger wage-region exposure;
- event-style policy timing if a credible shock exists;
- microdata with worker-level controls and policy exposure;
- replication/backtest of a stronger DiD design from the literature.

## Issue 5: TWFE and DML Differ in Sign

### Current Status

For the main treatment:

```text
log_real_min_wage
```

the current evidence is:

- pooled OLS with controls: negative;
- year FE with controls: negative;
- province FE with controls: positive;
- TWFE with controls: positive;
- DML: negative.

This means the main linear panel benchmark and DML robustness check do not agree.

### Why This Matters

This is not just a small technical detail. It is one of the central empirical facts of the project.

The sign difference suggests that results are sensitive to:

- cross-province differences;
- within-province changes;
- common year shocks;
- nonlinear controls;
- functional form;
- treatment measurement.

### Risk Level

High if hidden.

Low if presented transparently.

### How To Fix

#### Minimum Fix

State directly:

> The estimates are specification-sensitive. TWFE and DML differ in sign, so the evidence should not be interpreted as a definitive causal effect.

#### Recommended Fix

Make the sign difference a core results paragraph, not a footnote.

Suggested wording:

> The main empirical result is not a single stable causal coefficient, but rather the sensitivity of the estimated relationship to modeling choices. Province fixed effects reverse the pooled association, and DML produces an opposite-signed estimate relative to TWFE. This pattern indicates that province heterogeneity and functional form are central to interpretation.

#### Strong Fix

Run additional sensitivity checks:

- alternative control sets;
- lagged treatment if theoretically justified;
- excluding COVID years;
- excluding mixed district-region provinces;
- grouped-fold DML;
- province-specific trends if degrees of freedom allow.

## Issue 6: CRF Is Not Implemented

### Current Status

Causal Random Forest is not currently implemented in the repo.

No CRF script, validation table, or estimate exists.

### Why This Matters

If CRF is mentioned as if it were part of the empirical results, the paper would overstate the current analysis.

### Risk Level

Low, if left blank.

Medium, if discussed as a result.

### How To Fix

Keep CRF sections blank unless CRF is actually implemented and validated.

Recommended wording:

> Causal Random Forest is not implemented in the current analysis; no CRF estimates are reported.

Do not include CRF in the results narrative unless a later task explicitly builds and validates it.

## Issue 7: Literature Metadata Needs Final Verification

### Current Status

The repo includes a literature matrix and several literature notes. These identify:

- Perez Perez (2020) as the main academic/method benchmark.
- Nguyen Cuong Viet as a Vietnam data/method benchmark.
- Del Carpio et al. as a Vietnam context benchmark.
- Chernozhukov et al. (2018) as the DML method reference.

However, some publication status and ranking details still need final verification.

### Why This Matters

If the advisor requires journal quartile ranking or formal publication status, the paper should not overstate working papers as Q-ranked publications.

### Risk Level

Medium.

### How To Fix

Before final submission, verify:

- exact publication version of Nguyen Cuong Viet 2025;
- whether Del Carpio et al. has a peer-reviewed version or only the MPRA/RePEc working paper version;
- World Development ranking/category according to the advisor's required database;
- final citation style.

Then update:

```text
reports/literature_review/literature_matrix_minimum_wage.csv
reports/literature_review/literature_matrix_summary.md
paper/initial_draft.md
```

## Issue 8: Some Existing Literature Notes Have Encoding Problems

### Current Status

Some older markdown files show corrupted Vietnamese accents or author names, for example in references to Perez Perez.

This appears in some literature notes, not in the final new draft files.

### Why This Matters

Encoding problems make the repo look less professional and can create citation errors.

### Risk Level

Low for analysis.

Medium for presentation and final submission.

### How To Fix

#### Minimum Fix

Do not use corrupted text directly in the final paper.

#### Recommended Fix

Clean the key literature files manually:

- replace corrupted author names;
- normalize accents;
- ensure UTF-8 encoding;
- avoid mixing Vietnamese and English if the final paper is in English.

## Prioritized Action Plan

## Priority 1: Must Fix Before Final Paper

1. Verify and document the official citation for `informal_rate`.
2. Clearly label wage-region mapping as province-level approximation.
3. Keep CRF blank because it is not implemented.
4. Write the results as specification-sensitive evidence, not a causal conclusion.
5. Verify literature publication status and citation details.

## Priority 2: Strongly Recommended

1. Add a formal `reports/data_sources.md`.
2. Add `mixed_district_region` flag to the processed wage-region mapping.
3. Run a mapping robustness check excluding mixed district-region rows or provinces.
4. Add province-grouped cross-fitting for DML.
5. Add a short appendix explaining how each raw file maps to each final variable.

## Priority 3: Nice To Have

1. Build district-year wage-region exposure.
2. Weight district exposure by labor force, employment, or population.
3. Extend the wage panel backward to compute pre-2018 wage growth.
4. Clean encoding issues in all old literature notes.
5. Backtest or replicate a benchmark paper if replication data can be accessed.

## Suggested Paper Positioning After These Fixes

The paper should be positioned as:

> a transparent province-year empirical study of the association between regional minimum wage exposure and informal employment rates in Vietnam, with careful panel baselines, nonlinearity diagnostics, and DML robustness checks.

It should not be positioned as:

> definitive causal evidence that minimum wages increase or decrease informal employment.

The strongest contribution is the disciplined research pipeline:

1. build and validate the province-year panel;
2. define Y-D-W clearly;
3. document treatment variation and mapping limitations;
4. run transparent baseline panel models;
5. diagnose nonlinearity;
6. use DML only as robustness;
7. report specification sensitivity honestly.

## Current Bottom Line

The project is in a usable draft stage, but not yet in final-paper stage.

The most important unresolved issue is not code execution. The pipeline runs and produces interpretable outputs. The main remaining work is documentation, treatment-measurement robustness, and cautious interpretation.

The two most important fixes are:

1. verify the official citation for `informal_rate`;
2. strengthen or at least clearly disclose the province-level wage-region approximation.

Once those are addressed, the paper narrative becomes much more defensible.

