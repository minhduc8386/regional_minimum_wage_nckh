# DML Treatment Choice

## Purpose

This note closes the treatment choice for the DML robustness exercise. The decision is about which treatment should be emphasized in the DML section, not about proving a final causal effect.

## Decision

The main DML treatment should be:

```text
log_real_min_wage
```

The secondary robustness treatment should be:

```text
real_min_wage
```

The exploratory-only treatment should be:

```text
min_wage_growth
```

## Rationale

### Main Treatment: `log_real_min_wage`

`log_real_min_wage` is the best main treatment for DML reporting because it is economically interpretable, reduces scale issues, and has the most coherent DML stability pattern.

Current DML stability results show:

- Mean theta: approximately `-33.34`.
- Stable sign across main runs: all 9 main estimates are negative.
- Stable sign across folds: 44 out of 45 fold-level estimates are negative.
- Average p-value: approximately `0.029`.
- Confidence interval issue: 2 out of 9 main confidence intervals include zero.

This makes `log_real_min_wage` the strongest DML candidate. However, the DML estimate has the opposite sign from the two-way FE baseline. Therefore, it should be interpreted as flexible-control robustness evidence, not as definitive causal evidence.

### Secondary Robustness Treatment: `real_min_wage`

`real_min_wage` captures the same policy object in level form. It is useful as a robustness check because its DML results are also directionally stable:

- Mean theta: approximately `-0.000010`.
- Stable sign across main runs: all 9 main estimates are negative.
- Stable sign across folds: 44 out of 45 fold-level estimates are negative.
- Average p-value: approximately `0.032`.
- Confidence interval issue: 3 out of 9 main confidence intervals include zero.

The main drawback is interpretation. The level coefficient is harder to communicate than the log specification because it depends on the unit scale of VND/month.

### Exploratory Treatment: `min_wage_growth`

`min_wage_growth` should not be used as the main DML treatment. Its DML stability is weak:

- Mean theta: approximately `-67.99`.
- Stable sign: false.
- Average p-value: approximately `0.380`.
- Confidence interval issue: all 9 main confidence intervals include zero.
- Fold-level sign stability: only 30 out of 45 fold-level estimates are negative, while 15 are positive.

This suggests that the growth treatment is too unstable for the main DML narrative in the current panel.

## Reporting Rule

The DML section should report `log_real_min_wage` first, then use `real_min_wage` as a robustness check. `min_wage_growth` may be shown in an appendix or robustness table, but the text should explicitly state that it is exploratory and unstable.

## Recommended Paper Wording

For the DML robustness exercise, the preferred treatment is the log real regional minimum wage. This specification is easier to interpret than the level wage variable and produces the most stable DML theta estimates across learners, seeds, and folds. The level real minimum wage is retained as a secondary robustness check. The growth rate of the real minimum wage is treated as exploratory because its theta estimates are statistically weak and unstable across folds. Since the preferred DML estimate differs in sign from the TWFE baseline, the DML evidence is interpreted as sensitivity to flexible control functions rather than as definitive causal evidence.

## Source Files Used

- `reports/specification_y_d_w.md`
- `reports/tables/specification_y_d_w.csv`
- `reports/dml_theta_convergence_interpretation.md`
- `reports/tables/dml_theta_convergence_interpretation.csv`
- `reports/tables/dml_theta_stability.csv`
- `reports/tables/dml_theta_by_fold.csv`
- `reports/tables/baseline_ols_fe_results.csv`

