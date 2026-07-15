# Nonlinearity Evidence

## Purpose

This section consolidates the nonlinearity evidence from the original LOWESS diagnostics and the enhanced diagnostics added in the latest main-branch update. All evidence here is diagnostic. It motivates flexible robustness checks, but it does not provide causal evidence.

## Evidence Sources

The section uses four groups of evidence:

1. Raw LOWESS plots from the original nonlinearity diagnostics.
2. Residualized LOWESS from `reports/tables/residualized_lowess_summary.csv`.
3. Formal nonlinearity tests from `reports/tables/nonlinearity_formal_tests.csv`.
4. Partial dependence plots from `reports/tables/pdp_summary.csv` and `reports/figures/pdp/`.

## Raw LOWESS

The original LOWESS diagnostics show visible curvature in the relationship between `informal_rate` and:

- `log_real_min_wage`
- `unemployment_rate`
- `labour_productivity`
- `employed_persons`
- `log_employed_persons`

This suggests that a purely linear additive model may be restrictive in the full province-year panel.

## Residualized LOWESS

The residualized LOWESS results are especially useful because they ask whether curvature remains after partialling out controls and fixed-effect structures.

For the DML-like specification with W controls and year effects:

| treatment | spec | partial slope | LOWESS departure ratio | conclusion |
|---|---|---:|---:|---|
| `log_real_min_wage` | W + year | `-48.18` | `0.275` | visible curvature |
| `real_min_wage` | W + year | `-1.49e-05` | `0.312` | visible curvature |
| `min_wage_growth` | W + year | `7.60` | `0.158` | visible curvature |

For the TWFE-like residualized specification with W controls, year effects, and province effects:

| treatment | spec | partial slope | LOWESS departure ratio | conclusion |
|---|---|---:|---:|---|
| `log_real_min_wage` | W + year + province | `13.33` | `0.127` | mild curvature |
| `real_min_wage` | W + year + province | `3.69e-06` | `0.117` | mild curvature |
| `min_wage_growth` | W + year + province | `-18.15` | `0.121` | mild curvature |

Interpretation:

Curvature is clearer in the DML-like specification than in the TWFE-like specification. This suggests that province fixed effects absorb part of the nonlinear structure.

## Formal Tests

The formal tests reinforce the functional-form concern.

RESET rejects linearity for all six tested treatment/specification combinations:

- `log_real_min_wage`, pooled: p approximately `0.000076`
- `log_real_min_wage`, year FE: p approximately `0.000066`
- `log_real_min_wage`, TWFE: p approximately `0.00345`
- `real_min_wage`, pooled: p approximately `0.000036`
- `real_min_wage`, year FE: p approximately `0.000028`
- `real_min_wage`, TWFE: p approximately `0.00343`

However, the squared treatment-only tests are not strong. The stronger evidence in pooled and year-FE specifications comes from squared controls and joint W nonlinearities. This matters for interpretation:

> The main nonlinearity appears to be concentrated in the nuisance relationship between W and Y, rather than in a simple quadratic treatment effect.

This is exactly the setting where DML is useful as a robustness check: it can flexibly learn nuisance functions such as `E[Y|W]` and `E[D|W]`.

## PDP Evidence

The PDP outputs show non-flat predictive surfaces, but they should be read only as prediction diagnostics.

For `log_real_min_wage`:

- Random Forest PDP range is about `1.78` percentage points.
- Gradient Boosting PDP range is about `4.22` percentage points.
- The PDP is not monotonic decreasing.

For `min_wage_growth`, PDP ranges are smaller or noisier and should not be used as treatment-effect evidence.

## Recommended Figures

Use 3-5 figures in the paper or appendix. Recommended choices:

1. `reports/figures/nonlinearity_final/lowess_informal_rate_vs_log_real_min_wage.png`
2. `reports/figures/nonlinearity_residualized/residualized_lowess_log_real_min_wage_w_year.png`
3. `reports/figures/nonlinearity_residualized/residualized_lowess_log_real_min_wage_w_year_province.png`
4. `reports/figures/pdp/pdp_log_real_min_wage_random_forest.png`
5. `reports/figures/pdp/pdp_log_real_min_wage_gradient_boosting.png`

If the body is short, include only the first three and move PDP figures to appendix.

## Conclusion

The nonlinearity evidence supports the following statement:

> Linear OLS/FE/TWFE models remain necessary transparent baselines, but the diagnostics suggest that the nuisance relationship between controls and informal employment is nonlinear. DML is therefore a reasonable robustness check for flexible control adjustment. This does not mean OLS is wrong, and it does not mean DML is causal proof.

## Source Files Used

- `reports/tables/residualized_lowess_summary.csv`
- `reports/tables/nonlinearity_formal_tests.csv`
- `reports/tables/pdp_summary.csv`
- `reports/tables/feature_importance.csv`
- `reports/figures/nonlinearity_final/`
- `reports/figures/nonlinearity_residualized/`
- `reports/figures/pdp/`

