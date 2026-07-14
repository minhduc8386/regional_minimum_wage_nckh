# Project Completion Summary

Updated at: `2026-06-25`

This summary reflects the current status of the project after completing literature review updates, nonlinearity diagnostics, baseline OLS/FE/TWFE models, DiD/Event Study feasibility assessment, and DML theta-stability checks.

## 1. Research Question

Project title:

"Tác động nhân quả của chính sách lương tối thiểu vùng đến việc làm phi chính thức tại Việt Nam"

Main research question:

Does Vietnam's regional minimum wage policy relate to changes in province-year informal employment rates during 2018-2024?

Important positioning:

- The project does not claim strong causal identification from DML alone.
- Baseline FE/TWFE estimates are treated as controlled associations, not definitive causal effects.
- DML is used as a robustness/flexible-control exercise after baseline, not as a replacement for identification.

## 2. Final Analysis Panel

Main data file:

`data/processed/final/analysis_panel_2018_2024.csv`

Panel structure:

- Unit: province-year.
- Provinces: 63.
- Years: 2018-2024.
- Observations: 441.
- Missing values in required variables: 0.
- Duplicate province-year rows: 0.

Main variables:

- Outcome Y: `informal_rate`.
- Treatments D: `real_min_wage`, `log_real_min_wage`, `min_wage_growth`.
- Policy reference: `min_wage_nominal`.
- Controls W: `unemployment_rate`, `labour_productivity`, `trained_labour_rate`, `log_employed_persons`.

Treatment construction:

- `real_min_wage = min_wage_nominal / cpi_2018_base * 100`.
- `log_real_min_wage = log(real_min_wage)`.
- `min_wage_growth` is computed by wage region over time.

Treatment limitations:

- Actual regional minimum wages are applied at district/town/provincial-city level.
- The project uses a province-level approximation.
- There are many mixed district-region cases in the mapping notes, so measurement error remains a limitation.

## 3. Literature Work

Completed literature outputs:

| output | status |
|---|---|
| `reports/literature_review/main_paper_selection.md` | OK |
| `reports/literature_review/main_paper_evaluation.md` | OK |
| `reports/literature_review/delcarpio_paper_evaluation.md` | OK |
| `reports/literature_review/literature_matrix_minimum_wage.csv` | OK |
| `reports/literature_review/literature_matrix_summary.md` | OK |
| `reports/literature_review/research_gap_updated.md` | OK |
| `reports/literature_review/backtest_feasibility_perez2020.md` | OK |

Current literature positioning:

- Pérez Pérez (2020), "The Minimum Wage in Formal and Informal Sectors: Evidence from an Inflation Shock", is used as the main academic/method benchmark.
- Nguyen Cuong Viet (2023/2025) is used as the Vietnam data/method benchmark.
- Del Carpio et al. is used as a Vietnam context benchmark, not as the main Q-ranked paper if only the MPRA version is verified.

The updated research gap emphasizes:

- Recent Vietnam province-year data for 2018-2024.
- Direct focus on `informal_rate`.
- Baseline FE/TWFE before DML.
- Nonlinearity diagnostics before flexible methods.
- Explicit recognition that DML is not an identification strategy.

## 4. Nonlinearity Diagnostics

Completed outputs:

| output | status |
|---|---|
| `reports/nonlinearity_diagnostic_summary.md` | OK |
| `reports/tables/nonlinearity_summary_final.csv` | OK |
| `reports/tables/model_comparison_linear_vs_ml_final.csv` | OK |
| `reports/figures/nonlinearity_final/` | OK |

LOWESS findings:

- `log_real_min_wage`: visibly curved.
- `real_min_wage`: mildly curved.
- `min_wage_growth`: mildly curved.
- `unemployment_rate`: visibly curved.
- `labour_productivity`: visibly curved.
- `trained_labour_rate`: mildly curved.
- `log_employed_persons`: visibly curved.

Predictive diagnostics:

| model | RMSE | R2 |
|---|---:|---:|
| Linear Regression | 7.367 | 0.672 |
| Random Forest | 5.656 | 0.807 |
| Gradient Boosting | 5.615 | 0.810 |

Interpretation:

ML models predict `informal_rate` better than the linear benchmark, and LOWESS suggests nonlinearity. This motivates flexible-control checks, but it is not causal evidence.

## 5. Baseline Models

Completed outputs:

| output | status |
|---|---|
| `scripts/12_run_baseline_ols_fe.py` | OK |
| `reports/tables/baseline_ols_fe_results.csv` | OK |
| `reports/tables/baseline_ols_fe_validation.csv` | OK |
| `reports/baseline_ols_fe_summary.md` | OK |

Models estimated:

- Pooled OLS.
- Pooled OLS with controls.
- Province fixed effects.
- Year fixed effects.
- Two-way fixed effects.

Inference:

- Standard errors are clustered by province.
- Results include coefficient, standard error, p-value, confidence interval, number of observations and R-squared measures where applicable.

Main baseline interpretation:

- Pooled OLS tends to show negative associations for `real_min_wage` and `log_real_min_wage`.
- Province FE and TWFE results for `real_min_wage` and `log_real_min_wage` become positive and statistically significant or close to significant.
- `min_wage_growth` is negative in province FE, but weak and imprecise in TWFE.

Key caution:

The sign reversal between pooled OLS/year FE and province FE/TWFE suggests results are sensitive to specification and unobserved province-level differences. Baseline estimates should not be interpreted as strong causal proof.

## 6. DiD/Event Study Feasibility

Completed output:

`reports/did_eventstudy_feasibility.md`

Conclusion:

Classic DiD/Event Study is not suitable as the main causal design with the current data.

Reasons:

- Treatments are continuous, not binary.
- All provinces are exposed to the regional minimum wage policy.
- There is no clean untreated control group.
- Policy changes are national/regional-intensity changes rather than a clean shock to one treated group.
- The panel starts in 2018, so pre-treatment periods are limited for several possible shocks.

Recommended use:

- Do not force a causal DiD/Event Study.
- If needed, use event-style plots only as descriptive visualization.
- Continue with FE/TWFE baseline and DML robustness checks while stating identification limitations.

## 7. DML Decision and Results

Completed outputs:

| output | status |
|---|---|
| `reports/decision_note_dml.md` | OK |
| `scripts/13_run_dml_theta_stability.py` | OK |
| `reports/tables/dml_main_results.csv` | OK |
| `reports/tables/dml_theta_stability.csv` | OK |
| `reports/tables/dml_theta_by_fold.csv` | OK |
| `reports/tables/dml_theta_by_seed.csv` | OK |
| `reports/tables/dml_theta_by_learner.csv` | OK |
| `reports/tables/dml_theta_validation.csv` | OK |
| `reports/figures/dml/` | OK |
| `reports/dml_results_summary.md` | OK |

DML specification:

- Outcome: `informal_rate`.
- Treatments: `real_min_wage`, `log_real_min_wage`, `min_wage_growth`.
- Controls: `unemployment_rate`, `labour_productivity`, `trained_labour_rate`, `log_employed_persons`, plus year dummies.
- Cross-fitting: 5 folds.
- Seeds: 42, 123, 2024.
- Learners: `ridge_numpy`, `random_forest_custom`, `gradient_boosting_custom`.
- Standard errors: clustered by province.

Summary of DML theta stability:

| treatment | theta_mean | sign stability | CI issue | comparison with TWFE |
|---|---:|---|---|---|
| `real_min_wage` | -1.014e-05 | stable negative | CI contains 0 in 3/9 runs | different sign from TWFE |
| `log_real_min_wage` | -33.3366 | stable negative | CI contains 0 in 2/9 runs | different sign from TWFE |
| `min_wage_growth` | -67.9913 | unstable | CI contains 0 in 9/9 runs | same sign as TWFE but weak |

DML interpretation:

- `real_min_wage` and `log_real_min_wage` are stable within DML but differ in sign from TWFE.
- `min_wage_growth` is unstable and exploratory.
- DML does not provide strong causal evidence; it shows sensitivity to flexible nuisance adjustment.

## 8. Current Workplan Status

| step | task | status |
|---:|---|---|
| 1 | Main paper selection | Complete |
| 2 | Main paper evaluation | Complete |
| 3 | Del Carpio role | Complete |
| 4 | Literature matrix | Complete |
| 5 | Updated research gap | Complete |
| 6 | Nonlinearity summary | Complete |
| 7 | Baseline OLS/FE/TWFE | Complete |
| 8 | Baseline interpretation | Complete |
| 9 | DiD/Event Study feasibility | Complete |
| 10 | DML decision note | Complete |
| 11 | DML theta stability | Complete |
| 12 | DML interpretation | Complete |
| 13 | Final synthesis | Needs final writing |
| 14 | Final advisor presentation/report | Draft updated in `reports/advisor_presentation_script.md` |

## 9. Main Limitations

- Data are aggregate province-year observations, not individual worker-level microdata.
- Treatment assignment is approximated at province level, while policy implementation can vary within province by district-level wage region.
- No clean untreated control group is available for classic DiD/Event Study.
- Baseline and DML estimates are sensitive to specification.
- DML does not solve policy endogeneity or identification by itself.
- Pérez Pérez replication/backtest remains pending until replication data are downloaded and inspected.

## 10. Bottom Line

The project is technically complete through baseline, identification feasibility and DML robustness checks. The strongest defensible conclusion is cautious:

Vietnam's regional minimum wage exposure is associated with province-year informal employment rates in ways that are sensitive to model specification. Nonlinearity diagnostics justify flexible-control checks, but DML results do not establish a strong causal effect. Further causal identification would require cleaner exogenous variation, microdata, or a stronger design such as credible DiD, IV, RDD or threshold-based policy variation.
