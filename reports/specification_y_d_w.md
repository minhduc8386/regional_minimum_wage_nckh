# Y-D-W Specification

## Purpose

This note fixes the outcome, treatment, control, unit, and fixed-effect structure used in the current project.

The specification is designed for the Vietnam province-year panel from 2018 to 2024. It supports transparent baseline models and flexible robustness checks, but it does not by itself create a clean causal identification strategy.

## Analysis Unit

| item | specification |
|---|---|
| Unit | province-year |
| Period | 2018-2024 |
| Observations | 441 |
| Provinces/cities | 63 |
| Years | 7 |
| Panel status | balanced |
| Duplicate province-year rows | none |
| Required-variable missing values | none |

Source panel:

```text
data/processed/final/analysis_panel_2018_2024.csv
```

Validation source:

```text
reports/tables/enhanced_model_input_validation.csv
```

## Outcome Y

| role | variable | definition | unit | use |
|---|---|---|---|---|
| Y | `informal_rate` | Informal employment rate at province-year level | percentage points | Main outcome |

Interpretation guardrail:

`informal_rate` is an aggregate province-year measure. The estimates should not be interpreted as individual-worker transition effects.

## Treatment D

| role | variable | definition | unit | use |
|---|---|---|---|---|
| Main D | `log_real_min_wage` | Log of CPI-adjusted regional minimum wage | log VND/month | Main treatment for reporting and DML interpretation |
| Main D | `real_min_wage` | CPI-adjusted regional minimum wage, 2018 base | VND/month | Main robustness treatment in level scale |
| Exploratory D | `min_wage_growth` | Year-over-year growth of real minimum wage by wage region | proportion | Exploratory only |

`log_real_min_wage` is preferred in the main text because it is easier to interpret proportionally. `real_min_wage` remains a main treatment family member because it measures the same policy exposure in level form and is useful for robustness.

`min_wage_growth` is not a main treatment. The enhanced validation shows that its within-year standard deviation is extremely small relative to its overall/time variation:

```text
sd = 0.01409
within-year sd = 0.0009614
within-province sd = 0.01409
n_unique = 23
```

This means `min_wage_growth` is driven strongly by time changes common across wage regions. Once year dummies enter the model, much of the useful variation is absorbed. Empirically, its TWFE and DML results are weak or unstable:

- TWFE p-value is approximately `0.7656`.
- DML average p-value is approximately `0.3797`.
- DML K-sweep share negative is only `56%`.
- Main DML confidence intervals contain zero in `100%` of runs.

Therefore, `min_wage_growth` should be reported only as exploratory or appendix robustness.

## Controls W

The main control set contains four variables:

| role | variable | definition | use |
|---|---|---|---|
| W | `unemployment_rate` | province-year unemployment rate | labor-market condition |
| W | `labour_productivity` | province-year labor productivity | economic structure/productivity |
| W | `trained_labour_rate` | province-year trained labor share/rate | human-capital control |
| W | `log_employed_persons` | log employed persons | employment-scale control |

Available robustness control:

| role | variable | use |
|---|---|---|
| W robustness | `employed_persons` | Alternative to `log_employed_persons` |

Rule:

Do not include `employed_persons` and `log_employed_persons` in the same main regression because they represent the same employment-scale concept in level and log form.

## FE Structure By Method

| method | Y | D | W | fixed effects / dummies | variation emphasized | role |
|---|---|---|---|---|---|---|
| Pooled OLS + W | `informal_rate` | one D at a time | 4 controls | none | between + within | descriptive baseline |
| Year FE + W | `informal_rate` | one D at a time | 4 controls | year FE | between-province net of common shocks | baseline |
| Province FE + W | `informal_rate` | one D at a time | 4 controls | province FE | within-province over time | baseline |
| TWFE + W | `informal_rate` | one D at a time | 4 controls | province FE + year FE | within-province net of common shocks | main linear panel benchmark |
| DML original | `informal_rate` | one D at a time | 4 controls + year dummies | year dummies only; no province dummies | mostly between-province / year-FE-like variation | flexible-control robustness |
| DML + province dummies | `informal_rate` | one D at a time | 4 controls + year dummies + province dummies | province dummies + year dummies | within-province sensitivity | TWFE-comparable robustness |
| CRF | `informal_rate` | one D at a time | W = controls + year dummies; X = heterogeneity controls | grouped cross-fitting by province; no province dummies in main run | exploratory between-province heterogeneity | heterogeneity diagnostic |

## Inference Rule

For OLS/FE/TWFE:

```text
Cluster standard errors by province.
```

Reason:

The data are panel data, and errors may be correlated within province over time.

For DML/CRF:

Use stability diagnostics across learners, seeds, folds, and K choices. Do not describe sign stability as convergence proof.

## Final Specification Summary

Main reporting family:

```text
Y = informal_rate
D_main = log_real_min_wage, real_min_wage
W = unemployment_rate + labour_productivity + trained_labour_rate + log_employed_persons
Unit = province-year
Period = 2018-2024
```

Main linear benchmark:

```text
TWFE + W
province FE + year FE
cluster SE by province
```

Main flexible robustness:

```text
DML with W + year dummies
```

Key sensitivity:

```text
DML with W + year dummies + province dummies
```

Exploratory:

```text
min_wage_growth
CRF heterogeneity diagnostics
```

