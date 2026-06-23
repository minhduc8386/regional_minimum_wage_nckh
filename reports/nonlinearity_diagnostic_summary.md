# Nonlinearity Diagnostic Summary

## 1. Purpose

This note summarizes the diagnostic evidence on potential nonlinear relationships between `informal_rate` and the main policy, treatment, and control variables in the 2018-2024 province-year panel.

The purpose is exploratory. These results help describe the data and motivate later model choices, but they should not be interpreted as causal evidence on the effect of regional minimum wages on informal employment.

## 2. Data and Variables

The diagnostic exercise uses the final analysis panel:

```text
data/processed/final/analysis_panel_2018_2024.csv
```

The panel contains 441 observations, covering 63 provinces/cities over seven years from 2018 to 2024.

Outcome variable (Y):

- `informal_rate`: informal employment rate.

Primary treatment variables (D):

- `real_min_wage`
- `log_real_min_wage`
- `min_wage_growth`

Additional policy variable included in the LOWESS diagnostic:

- `min_wage_nominal`: nominal regional minimum wage before CPI adjustment.

Control variables (W):

- `unemployment_rate`
- `labour_productivity`
- `trained_labour_rate`
- `employed_persons`
- `log_employed_persons`

## 3. LOWESS Results

The LOWESS summary is reported in:

```text
reports/tables/nonlinearity_summary_final.csv
```

The LOWESS diagnostics suggest that several relationships between `informal_rate` and the explanatory variables are not well described by a simple straight line.

Variables with visibly curved LOWESS patterns:

| variable | group | pattern | interpretation |
|---|---|---|---|
| `log_real_min_wage` | treatment | visibly curved | Suggests a nonlinear association with `informal_rate`. |
| `unemployment_rate` | control | visibly curved | Suggests a nonlinear association with `informal_rate`. |
| `labour_productivity` | control | visibly curved | Suggests a nonlinear association with `informal_rate`. |
| `employed_persons` | control | visibly curved | Suggests a nonlinear association with `informal_rate`. |
| `log_employed_persons` | control | visibly curved | Suggests a nonlinear association with `informal_rate`. |

Variables with mildly curved LOWESS patterns:

| variable | group | pattern | interpretation |
|---|---|---|---|
| `min_wage_nominal` | policy reference | mildly curved | Suggests weak-to-moderate possible nonlinearity. |
| `real_min_wage` | treatment | mildly curved | Suggests weak-to-moderate possible nonlinearity. |
| `min_wage_growth` | treatment | mildly curved | Suggests weak-to-moderate possible nonlinearity. |
| `trained_labour_rate` | control | mildly curved | Suggests weak-to-moderate possible nonlinearity. |

The main takeaway from the LOWESS plots is that the association between `informal_rate` and several predictors appears to contain nonlinear components. This is most evident for `log_real_min_wage`, `unemployment_rate`, `labour_productivity`, and employment-scale variables.

## 4. Predictive Model Comparison

The predictive model comparison is reported in:

```text
reports/tables/model_comparison_linear_vs_ml_final.csv
```

This comparison uses `informal_rate` as the target variable and the following predictors: `real_min_wage`, `log_real_min_wage`, `min_wage_growth`, `unemployment_rate`, `labour_productivity`, `trained_labour_rate`, `employed_persons`, and `log_employed_persons`. It does not include `min_wage_nominal`, which is used only in the LOWESS diagnostic as a policy-level reference variable.

Five-fold cross-validation results:

| model | n | folds | RMSE | MAE | R2 |
|---|---:|---:|---:|---:|---:|
| Gradient Boosting custom | 441 | 5 | 5.615 | 4.470 | 0.810 |
| Random Forest custom | 441 | 5 | 5.656 | 4.624 | 0.807 |
| Linear Regression | 441 | 5 | 7.367 | 5.546 | 0.672 |

Relative to Linear Regression, Gradient Boosting reduces RMSE by approximately 23.8%, while Random Forest reduces RMSE by approximately 23.2%. This suggests that more flexible predictive models capture patterns in `informal_rate` that are missed by the linear benchmark.

## 5. Interpretation

Taken together, the LOWESS results and predictive model comparison suggest that the relationship between `informal_rate` and the policy, treatment, and control variables may include nonlinear structure. A purely linear specification may therefore miss part of the empirical pattern in the data.

This interpretation should remain cautious:

- LOWESS describes bivariate patterns and does not fully control for confounding factors.
- Random Forest and Gradient Boosting are used here only to predict `informal_rate`; they do not estimate causal effects.
- Better RMSE or R2 does not imply that minimum wage changes cause changes in informal employment.
- These diagnostics do not replace baseline models such as OLS, province fixed effects, year fixed effects, or two-way fixed effects.

## 6. Implications for Baseline and DML

The diagnostic evidence suggests that a purely linear specification may be restrictive. However, the next step should still be to estimate transparent baseline models, including OLS and fixed effects specifications, before moving to more flexible methods.

If DML is considered later, it should be used as a robustness or complementary approach for handling flexible controls and nonlinear patterns, not as a substitute for a clear identification strategy.
