# Why a Purely Linear OLS Specification May Be Limited

## Purpose

This note explains why a purely linear OLS specification may be too restrictive for the current province-year panel. The goal is not to reject OLS, FE, or TWFE models. These models remain necessary transparent baselines. The point is narrower: the existing diagnostic evidence suggests that the relationship between regional minimum wages, local labor-market controls, and informal employment may not be well summarized by a single constant linear slope.

All evidence in this note should be interpreted as diagnostic evidence only. It does not establish a causal effect of minimum wage policy on informal employment.

## Current Evidence

The nonlinearity diagnostic suggests visible curvature in the LOWESS relationships between `informal_rate` and several key variables:

| Variable | Diagnostic implication |
|---|---|
| `log_real_min_wage` | The relationship with informal employment does not look fully linear across the observed support. |
| `unemployment_rate` | The association appears to vary across different unemployment levels. |
| `labour_productivity` | The relationship may differ between lower-productivity and higher-productivity provinces. |
| `employed_persons` | The level form shows curvature and may be affected by scale differences across provinces. |
| `log_employed_persons` | The log form is more interpretable, but still shows nonlinearity in the diagnostic plots. |

The predictive model comparison points in the same direction. In the current diagnostic outputs:

| Model | RMSE | R2 |
|---|---:|---:|
| Linear Regression | 7.367 | 0.672 |
| Random Forest custom | 5.656 | 0.807 |
| Gradient Boosting custom | 5.615 | 0.810 |

Relative to the linear model, the two machine-learning diagnostic models reduce RMSE by more than 20 percent. This does not mean that the machine-learning models are causal models. It only suggests that flexible functional forms capture additional predictive structure in `informal_rate` that a linear specification does not fully capture.

## Why This Matters for Baseline OLS

A standard linear OLS model imposes a constant marginal association between each regressor and the outcome. For example, it assumes that a one-unit increase in `log_real_min_wage` is associated with the same change in `informal_rate` across all provinces and years, conditional on the included controls.

That assumption may be restrictive in this setting for four reasons.

First, the policy variable may have different associations at different parts of the wage distribution. A wage increase in a low-wage region may not map to informal employment in the same way as a wage increase in a higher-wage region.

Second, several control variables are themselves strongly related to province size and development level. Variables such as `labour_productivity`, `employed_persons`, and `log_employed_persons` may proxy for broader structural differences across provinces. If those relationships are nonlinear, a linear control term may leave systematic residual patterns.

Third, province and year fixed effects address some forms of omitted heterogeneity, but they do not automatically solve functional-form misspecification. Province fixed effects absorb time-invariant province differences. Year fixed effects absorb common national shocks. They do not guarantee that the slope of `log_real_min_wage` or the controls is linear over the observed support.

Fourth, the relationship may involve interactions. The association between minimum wages and informal employment may differ depending on productivity, unemployment, training, or province scale. A simple linear additive model does not capture those interactions unless they are explicitly added.

## How To Use OLS Despite These Limits

OLS, FE, and TWFE should still be reported because they are transparent and easy to audit. They provide a useful baseline association and allow comparison with standard empirical approaches in the literature.

However, the interpretation should be cautious:

- Treat pooled OLS as a descriptive association.
- Treat FE and TWFE as stronger baseline specifications, but still not final causal proof.
- Avoid claiming that a single linear coefficient fully summarizes the policy relationship.
- Use flexible diagnostics and DML-style robustness checks to test whether the baseline direction is sensitive to functional-form assumptions.

## Suggested Paper Wording

The diagnostic evidence indicates that several relationships in the province-year panel are not well described by a purely linear functional form. LOWESS plots show visible curvature for `log_real_min_wage` and several labor-market controls, while flexible predictive models reduce RMSE relative to a linear regression. These results do not provide causal evidence, but they suggest that linear OLS estimates should be interpreted as transparent baseline associations rather than as a complete description of the underlying relationship. For this reason, the analysis should report OLS/FE/TWFE baselines and then examine whether the conclusions are robust to more flexible control functions.

## Source Files Used

- `reports/tables/nonlinearity_summary_final.csv`
- `reports/tables/model_comparison_linear_vs_ml_final.csv`
- `reports/nonlinearity_evidence.md`
- `reports/nonlinearity_diagnostic_summary.md`
- `reports/baseline_ols_fe_summary.md`

