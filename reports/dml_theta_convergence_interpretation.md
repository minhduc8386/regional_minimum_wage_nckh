# DML Theta Stability After Enhanced Checks

## Purpose

This note updates the DML interpretation after the main branch added K-fold sweeps and a DML variant with province dummies. The goal is to decide how much weight to place on DML in the research narrative.

DML remains a flexible-control robustness exercise, not a stand-alone causal design.

## Main Update

The earlier DML result showed a relatively stable negative theta for `log_real_min_wage`. The enhanced results confirm that this negative sign is relatively stable across learners, seeds, folds, and K choices when the nuisance functions include W controls and year dummies. This should not be described as convergence proof.

However, the new DML variant with province dummies changes the interpretation. When province dummies are added, the theta becomes much smaller, statistically weak, and sign-unstable across learners. This means the original DML result is closer to a year-FE / between-province-flexible-control design than to a TWFE-comparable within-province design.

## Treatment-by-Treatment Interpretation

### `log_real_min_wage`

Main DML with W + year dummies:

- 100 percent of the 9 main runs are negative.
- 98 percent of the 45 fold-level estimates are negative.
- K=2, K=5, and K=10 sweeps all show 100 percent negative signs.
- Average p-value is approximately `0.0293`.
- The theta range across the main 9 runs is approximately `[-51.14, -21.41]`.

This is a relatively stable negative DML signal, not convergence proof.

But DML with province dummies:

- Average theta is approximately `-1.87`.
- Average p-value is approximately `0.3096`.
- Signs are mixed across learners.
- Confidence intervals contain zero in about 78 percent of runs.
- The method-comparison note reports that about 95 percent of treatment variation is between-province, leaving little within-province variation.

Interpretation:

`log_real_min_wage` remains the preferred DML treatment, but the result must be described as flexible-control robustness using mainly between-province variation. It conflicts with TWFE and weakens when made more TWFE-comparable.

### `real_min_wage`

Main DML with W + year dummies:

- 100 percent of the 9 main runs are negative.
- 98 percent of the 45 fold-level estimates are negative.
- K=2, K=5, and K=10 sweeps all show 100 percent negative signs.
- Average p-value is approximately `0.0325`.

DML with province dummies:

- Average theta is approximately `-5.97e-07`.
- Average p-value is approximately `0.3386`.
- Signs are mixed.
- Confidence intervals contain zero in about 89 percent of runs.

Interpretation:

The level treatment confirms the same pattern as the log treatment: relatively stable negative DML without province dummies, but weak/mixed once province dummies are included.

### `min_wage_growth`

Main DML:

- 89 percent of the 9 main runs are negative.
- Only 67 percent of fold-level estimates are negative.
- K sweeps show only 56 percent negative signs.
- Average p-value is approximately `0.3797`.
- Confidence intervals contain zero in all main runs.

Interpretation:

`min_wage_growth` remains exploratory only. It should not be a main treatment.

## Research Implication

The updated DML results strengthen, rather than weaken, the cautious interpretation:

- DML without province dummies is relatively stable and negative.
- TWFE is positive for `log_real_min_wage`.
- DML with province dummies is weak and mixed.

Therefore, the key conclusion is not "DML proves a negative effect." The key conclusion is:

> The estimated relationship is sensitive to variation source and model specification.

## Suggested Paper Wording

The DML robustness check produces stable negative estimates for the log real minimum wage when the nuisance functions include observed controls and year dummies. This stability holds across learners, seeds, folds, and K choices. However, when province dummies are added to make the DML specification closer to a within-province design, the estimate becomes small, statistically weak, and sign-unstable. This indicates that the DML signal relies heavily on between-province variation and should be interpreted as a flexible-control robustness diagnostic rather than as definitive causal evidence.

## Source Files Used

- `reports/tables/dml_main_results.csv`
- `reports/tables/dml_theta_stability.csv`
- `reports/tables/dml_theta_by_fold.csv`
- `reports/tables/dml_theta_by_k.csv`
- `reports/tables/dml_convergence_interpretation.csv`
- `reports/tables/dml_theta_province_fe.csv`
- `reports/tables/method_comparison_summary.csv`
