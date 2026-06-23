# Baseline OLS and Fixed Effects Summary

## 1. Purpose

This note interprets the baseline OLS and fixed effects estimates for the relationship between regional minimum wage variables and informal employment in the 2018-2024 province-year panel.

The estimates should be read as baseline associations, not as definitive causal effects. The models control for observed covariates and fixed effects, but they do not fully resolve endogeneity, policy selection, or time-varying province-level shocks.

## 2. Key Takeaways

The main pattern is specification-sensitive. `real_min_wage` and `log_real_min_wage` are negatively associated with `informal_rate` in pooled OLS and year-FE models, but positively associated with `informal_rate` once province fixed effects are included.

`min_wage_growth` is less stable. It is positive in the uncontrolled pooled model, becomes small and insignificant after adding controls, turns negative in the province-FE model, and is not statistically significant in the two-way FE model.

The employment-scale robustness check does not materially change these conclusions. Replacing `log_employed_persons` with `employed_persons` leaves the broad sign pattern intact.

## 3. Data and Specifications

The estimates use:

```text
data/processed/final/analysis_panel_2018_2024.csv
```

Validation checks pass: the panel has 441 observations, 63 provinces/cities, seven years from 2018 to 2024, no duplicate `province-year` rows, no missing values in required model variables, and usable variation in the treatment variables.

Outcome:

- `informal_rate`

Treatment variables, estimated separately:

- `real_min_wage`
- `log_real_min_wage`
- `min_wage_growth`

Main control set:

- `unemployment_rate`
- `labour_productivity`
- `trained_labour_rate`
- `log_employed_persons`

Robustness control set:

- `unemployment_rate`
- `labour_productivity`
- `trained_labour_rate`
- `employed_persons`

The final panel contains both `employed_persons` and `log_employed_persons`, but they are not included together because they represent the same employment scale in level and log form.

The no-control pooled OLS model is estimated once. Controlled specifications are estimated with both the main and robustness control sets.

| model | controls | province FE | year FE |
|---|---:|---:|---:|
| `pooled_ols_no_controls` | No | No | No |
| `pooled_ols_controls` | Yes | No | No |
| `province_fe_controls` | Yes | Yes | No |
| `year_fe_controls` | Yes | No | Yes |
| `two_way_fe_controls` | Yes | Yes | Yes |

Pooled OLS is estimated using `statsmodels`. Fixed effects models are estimated using `linearmodels.PanelOLS`. Standard errors are clustered by province.

## 4. Main Results

The estimates below refer to the main control set unless otherwise noted.

### Real Minimum Wage

`real_min_wage` is negative in pooled and year-FE specifications:

- Pooled OLS without controls: coefficient = `-2.66e-05`, p-value `< 0.001`.
- Pooled OLS with controls: coefficient = `-1.38e-05`, p-value = `0.004`.
- Year FE with controls: coefficient = `-1.49e-05`, p-value = `0.005`.

The sign turns positive when province fixed effects are included:

- Province FE with controls: coefficient = `3.93e-06`, p-value = `0.006`.
- Two-way FE with controls: coefficient = `3.69e-06`, p-value = `0.048`.

This sign reversal suggests that cross-province differences and within-province changes are producing different associations.

### Log Real Minimum Wage

`log_real_min_wage` follows the same pattern:

- Pooled OLS without controls: coefficient = `-90.28`, p-value `< 0.001`.
- Pooled OLS with controls: coefficient = `-44.84`, p-value = `0.003`.
- Year FE with controls: coefficient = `-48.18`, p-value = `0.004`.
- Province FE with controls: coefficient = `13.91`, p-value = `0.003`.
- Two-way FE with controls: coefficient = `13.33`, p-value = `0.038`.

Because `log_real_min_wage` is easier to interpret than the level wage variable, it is a useful candidate for the main baseline treatment. However, the sign change across specifications means it should still be interpreted cautiously.

### Minimum Wage Growth

`min_wage_growth` provides weaker baseline evidence:

- Pooled OLS without controls: coefficient = `109.30`, p-value `< 0.001`.
- Pooled OLS with controls: coefficient = `6.50`, p-value = `0.754`.
- Province FE with controls: coefficient = `-21.72`, p-value = `0.004`.
- Year FE with controls: coefficient = `7.60`, p-value = `0.953`.
- Two-way FE with controls: coefficient = `-18.15`, p-value = `0.766`.

The two-way FE estimate is statistically insignificant and has a wide confidence interval. This makes `min_wage_growth` less convincing as a main baseline treatment in the current panel.

## 5. Robustness to Employment-Scale Control

The robustness control set replaces `log_employed_persons` with `employed_persons`.

For `real_min_wage` and `log_real_min_wage`, the sign pattern is almost unchanged: pooled and year-FE estimates remain negative, while province-FE and two-way-FE estimates remain positive.

For `min_wage_growth`, the robustness check also supports the same conclusion as the main specification: the two-way FE association is not statistically meaningful.

This suggests that the main baseline patterns are not driven by choosing the log employment control instead of the level employment control.

## 6. Interpretation and Limits

The central result is not that minimum wages have a clear positive or negative effect on informal employment. Rather, the central result is that the estimated association depends heavily on the fixed effects structure.

Province fixed effects change the interpretation because they absorb time-invariant differences across provinces. The sign flip for `real_min_wage` and `log_real_min_wage` suggests that the negative pooled association may partly reflect cross-sectional province differences rather than within-province policy changes.

Year fixed effects alone preserve the negative association, which suggests that common year shocks and province-level heterogeneity matter in different ways. The two-way FE specification is therefore the most informative baseline specification, but it is still not a complete identification strategy.

The R-squared values should also be interpreted carefully. Pooled OLS reports the standard OLS R-squared, while `PanelOLS` reports within, between, and overall R-squared measures. These should not be used as a simple ranking of model quality across pooled and fixed effects specifications.

## 7. Conclusion

The baseline results do not support a simple, specification-invariant relationship between regional minimum wages and informal employment.

The level and log real minimum wage variables are negative in pooled/year-FE models but positive in province-FE/two-way-FE models. Minimum wage growth is less stable and is not statistically significant in the two-way FE specification.

Overall, these results are useful as baseline association evidence, but they should not be treated as strong causal evidence. The next step is to assess whether the treatment variation supports a credible identification strategy before moving to DiD, Event Study, or DML.
