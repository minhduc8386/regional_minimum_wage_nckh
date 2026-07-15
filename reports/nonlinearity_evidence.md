# Nonlinearity Evidence

## 1. Purpose

This note summarizes the existing evidence that the relationship between `informal_rate` and the main policy/control variables may be nonlinear.

The purpose is diagnostic. LOWESS plots and predictive model comparison are used to understand the shape of the data and motivate flexible-control robustness checks. They should not be interpreted as causal evidence.

## 2. Source Files

The evidence comes from existing project outputs:

- `reports/tables/nonlinearity_summary_final.csv`
- `reports/tables/model_comparison_linear_vs_ml_final.csv`
- `reports/figures/nonlinearity_final/`

The underlying dataset is:

```text
data/processed/final/analysis_panel_2018_2024.csv
```

The panel has 441 province-year observations from 63 provinces/cities over 2018-2024.

## 3. LOWESS Evidence

LOWESS diagnostics suggest that several bivariate relationships are not well approximated by a straight line.

Variables with visibly curved LOWESS patterns:

| variable | group | LOWESS pattern | interpretation |
|---|---|---|---|
| `log_real_min_wage` | treatment | visibly curved | Nonlinear association with `informal_rate` is visually clear. |
| `unemployment_rate` | control | visibly curved | Nonlinear association with `informal_rate` is visually clear. |
| `labour_productivity` | control | visibly curved | Nonlinear association with `informal_rate` is visually clear. |
| `employed_persons` | control | visibly curved | Nonlinear association with `informal_rate` is visually clear. |
| `log_employed_persons` | control | visibly curved | Nonlinear association with `informal_rate` is visually clear. |

Variables with mildly curved LOWESS patterns:

| variable | group | LOWESS pattern | interpretation |
|---|---|---|---|
| `min_wage_nominal` | policy reference | mildly curved | Weak-to-moderate possible nonlinearity. |
| `real_min_wage` | treatment | mildly curved | Weak-to-moderate possible nonlinearity. |
| `min_wage_growth` | treatment | mildly curved | Weak-to-moderate possible nonlinearity. |
| `trained_labour_rate` | control | mildly curved | Weak-to-moderate possible nonlinearity. |

The most important point for the research narrative is that `log_real_min_wage`, `unemployment_rate`, `labour_productivity`, and employment-scale variables show visible departures from a simple linear pattern.

## 4. Predictive Model Comparison

The predictive diagnostic compares Linear Regression with custom Random Forest and Gradient Boosting models using five-fold cross-validation.

| model | n | folds | RMSE | MAE | R2 |
|---|---:|---:|---:|---:|---:|
| Gradient Boosting custom | 441 | 5 | 5.615 | 4.470 | 0.810 |
| Random Forest custom | 441 | 5 | 5.656 | 4.624 | 0.807 |
| Linear Regression | 441 | 5 | 7.367 | 5.546 | 0.672 |

Relative to Linear Regression:

- Gradient Boosting reduces RMSE by about 23.8%.
- Random Forest reduces RMSE by about 23.2%.

This suggests that flexible predictive models capture empirical patterns in `informal_rate` that the linear benchmark misses.

## 5. Figures to Show

The most useful figures for the report are:

| priority | figure | reason |
|---:|---|---|
| 1 | `reports/figures/nonlinearity_final/lowess_informal_rate_vs_log_real_min_wage.png` | Main treatment variable with visible curvature. |
| 2 | `reports/figures/nonlinearity_final/lowess_informal_rate_vs_real_min_wage.png` | Robustness treatment in level scale. |
| 3 | `reports/figures/nonlinearity_final/lowess_informal_rate_vs_unemployment_rate.png` | Key labour-market control with visible curvature. |
| 4 | `reports/figures/nonlinearity_final/lowess_informal_rate_vs_labour_productivity.png` | Key economic control with visible curvature. |
| 5 | `reports/figures/nonlinearity_final/lowess_informal_rate_vs_log_employed_persons.png` | Main employment-scale control with visible curvature. |

These figures are enough for the main text. The remaining LOWESS plots can be kept as appendix or supporting diagnostics.

## 6. Suggested Narrative

The diagnostic results suggest that a purely linear specification may be restrictive for this province-year panel. LOWESS plots show visible curvature for `log_real_min_wage` and several important controls, especially unemployment, labour productivity, and employment scale. In addition, flexible predictive models such as Random Forest and Gradient Boosting reduce cross-validated RMSE by more than 20% relative to Linear Regression.

This does not mean that OLS, FE, or TWFE are invalid. These models remain necessary as transparent baseline specifications. The point is narrower: the data show enough nonlinear structure to justify robustness checks that allow more flexible nuisance functions, such as DML.

## 7. Interpretation Guardrails

Do not overstate this evidence:

- LOWESS is descriptive and bivariate; it does not control for all confounders.
- Random Forest and Gradient Boosting are predictive diagnostics; they do not estimate causal effects.
- Lower RMSE or higher R2 does not imply that minimum wage changes cause changes in informal employment.
- Nonlinearity evidence motivates flexible specifications, but it does not replace a credible identification strategy.
