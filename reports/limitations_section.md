# Limitations

## Purpose

This note provides a limitations section for the paper draft. It is written to keep the interpretation scientifically cautious and transparent.

## Suggested Limitation Section

This study has several limitations.

First, the analysis uses an aggregate province-year panel rather than worker-level or firm-level microdata. The panel structure is useful for documenting recent regional patterns, but it cannot observe individual transitions between formal employment, informal employment, unemployment, self-employment, and inactivity. This limits the ability to distinguish labor reallocation mechanisms.

Second, the current data do not provide a clean untreated control group. Vietnam's regional minimum wage policy applies nationwide, with provinces exposed through regional wage classifications and intensity differences. This makes a classic binary Difference-in-Differences or event-study design difficult to justify. The estimates should therefore be interpreted as baseline associations and robustness diagnostics rather than as a clean quasi-experimental causal effect.

Third, minimum wage exposure is mapped at the province-year level. In practice, Vietnam's minimum wage regions can vary at more detailed administrative levels, including districts. A province-level mapping may therefore introduce measurement error in treatment assignment, especially for provinces with heterogeneous districts or changes in administrative classification.

Fourth, the sample is small for flexible causal machine learning. The panel contains 441 province-year observations, which is limited for DML. Although the DML theta for `log_real_min_wage` is stable across learners, seeds, and most folds, the method should still be treated as a robustness exercise.

Fifth, the current DML implementation does not fully reproduce a province fixed-effects design in the nuisance functions. It includes observed controls and year dummies, but province fixed effects are not fully included because of sample-size and overfitting concerns. Cross-fitting is also implemented at the row level rather than as province-grouped folds. These choices should be improved before making stronger causal claims.

Sixth, the main estimates are specification-sensitive. Pooled OLS and year-FE models estimate a negative association between `log_real_min_wage` and `informal_rate`, while province-FE and TWFE models estimate a positive association. DML returns a stable negative theta. This disagreement indicates that the estimated relationship depends on how province heterogeneity, year shocks, and nonlinear controls are handled.

Seventh, Causal Random Forest is not implemented in the current repo. The CRF section should therefore remain blank and should not be presented as a result.

Finally, external validity is limited. The panel covers Vietnam from 2018 to 2024, a period that includes COVID and post-COVID labor-market disruptions. Results from this period may not generalize to earlier periods, worker-level settings, or other countries.

## Missing Information To Resolve

The following items would strengthen the final paper:

- A clearer data-source citation for the `informal_rate` measure.
- A more detailed explanation of how provincial wage-region mapping handles district-level variation.
- Verification of all literature citation details and publication status.
- If possible, grouped cross-fitting by province for DML robustness.
- If possible, an expanded dataset or microdata source to support stronger identification.

## Source Files Used

- `reports/did_eventstudy_feasibility.md`
- `reports/dml_theta_convergence_interpretation.md`
- `reports/model_family_comparison.md`
- `reports/literature_comparison_current_results.md`
- `reports/specification_y_d_w.md`
