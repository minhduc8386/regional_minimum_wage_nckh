# Y-D-W Specification

## 1. Purpose

This note fixes the outcome, treatment, and control specification used in the current project.

The specification is designed for the 2018-2024 province-year panel. It supports the baseline OLS/FE/TWFE models and the DML robustness exercise, but it should not be interpreted as a complete causal identification strategy by itself.

## 2. Analysis Unit and Sample

Data file:

```text
data/processed/final/analysis_panel_2018_2024.csv
```

Analysis unit:

- Province-year.

Sample:

- 441 observations.
- 63 provinces/cities.
- Seven years, 2018-2024.
- No duplicate `province-year` rows.
- No missing values in the required Y-D-W variables.

## 3. Outcome Y

Main outcome:

| role | variable | definition | unit / scale | use |
|---|---|---|---|---|
| Y | `informal_rate` | Informal employment rate at province-year level. | Percentage points | Main outcome in all baseline and DML specifications. |

`informal_rate` is an aggregate province-year outcome. Results should not be interpreted as individual-worker-level effects.

## 4. Treatment D

The treatment hierarchy is:

| role | variable | status | definition | use |
|---|---|---|---|---|
| D main | `log_real_min_wage` | Main treatment | Log of CPI-adjusted regional minimum wage. | Preferred treatment for interpretation because it reduces scale issues and is easier to compare across specifications. |
| D robustness | `real_min_wage` | Robustness treatment | CPI-adjusted regional minimum wage, 2018 base. | Used to check whether conclusions are similar in the level wage scale. |
| D exploratory | `min_wage_growth` | Exploratory treatment | Growth rate of `real_min_wage` by wage region over time; 2018 is filled as 0. | Reported as a secondary check, not as the main treatment, because DML theta is unstable and two-way FE evidence is weak. |

Additional policy reference variable:

| role | variable | definition | use |
|---|---|---|---|
| Policy reference | `min_wage_nominal` | Nominal regional minimum wage before CPI adjustment. | Used for treatment construction and descriptive/policy context, not as the main causal treatment. |

Rationale:

- `log_real_min_wage` and `real_min_wage` are the main minimum-wage exposure measures.
- `log_real_min_wage` is preferred for the main specification because it handles scale more naturally than the raw VND level.
- `real_min_wage` remains important as a robustness treatment because it is directly interpretable in VND/month.
- `min_wage_growth` should not be presented as the main treatment because the DML stability results show sign instability and confidence intervals often include zero.

## 5. Controls W

Main control set:

| role | variable | definition | use |
|---|---|---|---|
| W | `unemployment_rate` | Province-year unemployment rate. | Main control. |
| W | `labour_productivity` | Province-year labour productivity. | Main control. |
| W | `trained_labour_rate` | Share/rate of trained labour at province-year level. | Main control. |
| W | `log_employed_persons` | Log of employed persons. | Main employment-scale control. |

Available robustness control:

| role | variable | definition | use |
|---|---|---|---|
| W robustness | `employed_persons` | Number of employed persons. | Used only as robustness alternative to `log_employed_persons`. |

Specification rule:

- Do not include `employed_persons` and `log_employed_persons` in the same main regression.
- They represent the same employment scale in level and log form.
- The main specification uses `log_employed_persons`.
- Robustness checks can replace `log_employed_persons` with `employed_persons`.

## 6. Fixed Effects and Inference

Baseline models should report:

- Pooled OLS without controls.
- Pooled OLS with controls.
- Province fixed effects with controls.
- Year fixed effects with controls.
- Two-way fixed effects with province and year fixed effects.

Main inference rule:

- Cluster standard errors by province when possible.

Reason:

- The data are a province-year panel.
- Errors may be serially correlated within province over time.
- Province fixed effects absorb time-invariant province characteristics.
- Year fixed effects absorb common shocks across all provinces in a given year.

## 7. DML Specification Link

For DML, use:

- Outcome: `informal_rate`.
- Treatments: `log_real_min_wage`, `real_min_wage`, and `min_wage_growth`, estimated separately.
- Main controls: `unemployment_rate`, `labour_productivity`, `trained_labour_rate`, `log_employed_persons`.
- Year dummies can be included in W.

DML role:

- DML is a robustness/flexible-control exercise.
- DML checks whether theta is stable after flexibly partialling out W.
- DML does not replace a credible causal identification strategy.

Current DML interpretation:

- `log_real_min_wage` and `real_min_wage` have relatively stable negative DML theta across learners/seeds, but some confidence intervals include zero and the signs differ from two-way FE.
- `min_wage_growth` is exploratory because theta is unstable across learners/seeds and confidence intervals contain zero.

## 8. Interpretation Guardrails

Use the specification as follows:

- Interpret OLS/FE/TWFE as baseline associations, not definitive causal effects.
- Interpret DML as robustness evidence for flexible controls, not causal proof.
- Do not say that predictive improvement or nonlinear diagnostics prove causality.
- Do not present `min_wage_growth` as the primary treatment.
- Be explicit that the data are aggregate province-year data, not individual microdata.
- Be explicit that province-level wage-region mapping is an approximation.

## 9. Final Chosen Specification

Main reporting specification:

```text
Y = informal_rate
D_main = log_real_min_wage
W_main = unemployment_rate + labour_productivity + trained_labour_rate + log_employed_persons
FE_main = province fixed effects + year fixed effects
SE = clustered by province
```

Robustness treatment:

```text
D_robustness = real_min_wage
```

Exploratory treatment:

```text
D_exploratory = min_wage_growth
```

Employment-scale robustness:

```text
Replace log_employed_persons with employed_persons.
Do not include both in the same main specification.
```
