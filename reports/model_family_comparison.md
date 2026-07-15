# OLS, FE, TWFE, and DML Comparison

## Purpose

This note compares the current model families by research role. It should not be read as a horse race where the model with the preferred sign or lower prediction error is automatically the correct causal model.

The comparison uses `log_real_min_wage` as the main treatment because it is the preferred DML treatment and the most interpretable treatment for reporting.

## Current Comparison

| Model family | Current result for `log_real_min_wage` | Main role | Interpretation |
|---|---:|---|---|
| Pooled OLS with controls | `-44.84`, p = `0.0035` | Descriptive baseline | Negative association, but mixes cross-province and within-province variation. |
| Province FE with controls | `13.91`, p = `0.0034` | Within-province baseline | Positive within-province association after absorbing time-invariant province differences. |
| Year FE with controls | `-48.18`, p = `0.0039` | Common-shock-adjusted baseline | Negative association after absorbing common year shocks, but without province FE. |
| TWFE with controls | `13.33`, p = `0.0375` | Main linear panel benchmark | Positive within-province association net of common year shocks. Still not definitive causal proof. |
| DML partialling-out | mean theta `-33.34`, average p = `0.0293` | Flexible-control robustness | Stable negative DML theta, but opposite sign from TWFE. Indicates model sensitivity. |
| Causal Random Forest | Not implemented in current repo | Left blank | No CRF result is reported because CRF has not been implemented. |

## Main Takeaway

The baseline linear panel models and DML do not tell one fully consistent story.

The TWFE estimate for `log_real_min_wage` is positive and statistically significant at conventional levels. The DML theta is negative and relatively stable across learners, seeds, and folds. This disagreement is the main methodological result from the comparison.

The safest interpretation is:

- Pooled OLS and year-FE estimates are negative, but they are strongly affected by cross-sectional structure.
- Province-FE and TWFE estimates are positive, suggesting that within-province changes tell a different story from pooled cross-sectional comparisons.
- DML estimates are negative after flexible nuisance adjustment, but the current DML setup is not a stronger identification design than TWFE.
- Therefore, the evidence is specification-sensitive and should be reported cautiously.

## How To Position Each Model

### OLS

Pooled OLS is useful for a first descriptive association. It should not be used as the main causal estimate because provinces differ structurally in productivity, employment scale, industrial composition, and informality.

### Province FE

Province fixed effects are important because they remove time-invariant differences across provinces. In the current output, adding province FE changes the sign of the `log_real_min_wage` coefficient from negative to positive. This sign change is substantively important and should be discussed.

### TWFE

TWFE is the main linear panel benchmark because it includes both province and year fixed effects. However, TWFE still imposes a linear additive specification and does not solve all identification concerns. It should be reported as the strongest current baseline association, not as final causal proof.

### DML

DML is useful because the diagnostics show nonlinear relationships between `informal_rate`, treatment variables, and controls. In the current repo, DML is best interpreted as a flexible-control robustness exercise. It should not replace the TWFE baseline because the sample is small, province fixed effects are not fully included in the nuisance functions, and cross-fitting is row-level rather than grouped by province.

### CRF

This section is intentionally left blank because Causal Random Forest has not been implemented in the current repo. No CRF estimates should be reported or interpreted.

## Recommendation for the Next Narrative

The empirical narrative should be:

1. Report OLS/FE/TWFE as transparent baseline associations.
2. Emphasize the sign flip between pooled/year-FE and province/TWFE specifications.
3. Use DML as a robustness diagnostic showing that flexible nuisance adjustment produces a stable but opposite-signed estimate.
4. State that the current evidence is specification-sensitive.
5. Leave CRF blank unless it is implemented and validated in a later step.

## Source Files Used

- `reports/tables/baseline_ols_fe_results.csv`
- `reports/baseline_ols_fe_summary.md`
- `reports/tables/dml_theta_stability.csv`
- `reports/tables/dml_main_results.csv`
- `reports/dml_results_summary.md`
- `reports/dml_theta_convergence_interpretation.md`
- `reports/why_linear_ols_may_be_limited.md`
