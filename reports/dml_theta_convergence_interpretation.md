# DML Theta Stability and Convergence Interpretation

## Purpose

This note reviews whether the DML treatment coefficient estimates are stable across learners, seeds, and cross-fitting folds. The goal is to decide how much weight to place on the DML results in the research narrative.

The DML results should be interpreted as a flexible-control robustness diagnostic, not as stand-alone causal proof.

## Main Interpretation

| Treatment | Stability assessment | Recommended role |
|---|---|---|
| `real_min_wage` | Stable negative direction across main runs, with some uncertainty in confidence intervals. | Robustness check for the level treatment. |
| `log_real_min_wage` | Most coherent DML signal: stable negative direction across main runs and folds, but different sign from TWFE. | Preferred DML treatment for robustness discussion, with caution. |
| `min_wage_growth` | Unstable across folds and statistically weak. | Exploratory only, not a main DML treatment. |

## Evidence by Treatment

### `real_min_wage`

Across the main DML runs, the estimated theta is consistently negative. The average theta is approximately `-0.000010`, and all 9 main estimates are negative. Across fold-level estimates, 44 out of 45 estimates are negative.

This indicates reasonably stable directional evidence. However, 3 out of 9 main confidence intervals include zero, and the magnitude varies by learner. The ridge learner gives a more negative estimate than the tree-based learners. This means the sign is stable, but the exact magnitude should not be overinterpreted.

### `log_real_min_wage`

This is the most coherent DML specification. The average theta is approximately `-33.34`, all 9 main estimates are negative, and 44 out of 45 fold-level estimates are negative. The average p-value is about `0.029`, and 2 out of 9 main confidence intervals include zero.

This supports using `log_real_min_wage` as the main DML treatment in the robustness narrative. However, the DML estimate has the opposite sign from the TWFE baseline. That disagreement is substantively important and should be presented as evidence that the estimated association is sensitive to model specification, not as a clean causal conclusion.

### `min_wage_growth`

The growth treatment is not stable. Although 8 out of 9 main DML estimates are negative, all 9 main confidence intervals include zero. At the fold level, only 30 out of 45 estimates are negative and 15 are positive. The fold-level dispersion is also much larger than for the level and log-level treatments.

This means `min_wage_growth` should not be used as the main DML treatment. It may still be reported as an exploratory robustness check, but the correct interpretation is weak and unstable evidence.

## Methodological Caveats

Several caveats should be stated clearly in the paper or report:

- The current DML implementation is a robustness diagnostic for flexible controls, not a complete causal design.
- The sample is small for machine-learning-based causal estimation: 441 province-year observations.
- The current DML setup does not include full province fixed effects in the nuisance functions.
- Cross-fitting is implemented at the row level, not as grouped folds by province.
- DML estimates should be compared with OLS/FE/TWFE results rather than replacing them.

## Suggested Paper Wording

The DML stability check indicates that the level and log-level minimum wage treatments produce consistently negative theta estimates across learners, random seeds, and most cross-fitting folds. The log real minimum wage specification is the most stable DML result. However, this DML estimate differs in sign from the TWFE baseline, and the sample is small for flexible causal estimation. Therefore, the DML results are best interpreted as robustness evidence that the estimated relationship is sensitive to functional-form and control-function choices, rather than as definitive causal evidence.

## Source Files Used

- `reports/tables/dml_main_results.csv`
- `reports/tables/dml_theta_stability.csv`
- `reports/tables/dml_theta_by_fold.csv`
- `reports/tables/dml_theta_by_seed.csv`
- `reports/tables/dml_theta_by_learner.csv`
- `reports/dml_results_summary.md`
- `reports/decision_note_dml.md`

