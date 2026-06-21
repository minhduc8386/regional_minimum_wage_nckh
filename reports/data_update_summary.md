# Data Update Summary

## 1. Data Added

The project now includes three processed policy/economy inputs:

- `data/processed/policy/min_wage_region_panel.csv`
- `data/processed/policy/province_wage_region_map.csv`
- `data/processed/economy/cpi_panel.csv`

Raw inputs passed validation:

- Minimum wage region panel: 28 rows = 7 years x 4 wage regions.
- Province wage-region mapping: 441 rows = 63 provinces x 7 years.
- CPI panel: 7 rows = 2018-2024.

## 2. Final Dataset

Final analysis panel:

- Path: `data/processed/final/analysis_panel_2018_2024.csv`
- Shape: 441 rows x 15 columns
- Provinces: 63
- Years: 2018-2024
- Duplicate `province-year`: 0
- Missing values in required variables: 0

Columns:

`province`, `year`, `wage_region`, `informal_rate`, `min_wage_nominal`, `cpi_index`, `cpi_2018_base`, `real_min_wage`, `log_real_min_wage`, `min_wage_growth`, `unemployment_rate`, `labour_productivity`, `trained_labour_rate`, `employed_persons`, `log_employed_persons`

## 3. Research Variables

- Y: `informal_rate`
- D: `real_min_wage`, `log_real_min_wage`, with `min_wage_nominal` and `min_wage_growth` as related policy variables.
- W: `unemployment_rate`, `labour_productivity`, `trained_labour_rate`, `employed_persons`, `log_employed_persons`

## 4. Treatment Construction

- `min_wage_nominal` comes from the wage-region policy panel.
- 2022 and 2024 values are already annualized in the raw file as 6 months old level + 6 months new level.
- `cpi_2018_base = cpi_index / cpi_index_2018 * 100`
- `real_min_wage = min_wage_nominal / cpi_2018_base * 100`
- `log_real_min_wage = log(real_min_wage)`
- `min_wage_growth` is computed from `real_min_wage` by `wage_region` over time; 2018 is filled as 0.

## 5. Treatment Variation

Summary from `reports/tables/treatment_variation_summary.csv`:

- Nominal minimum wage ranges from 2,760,000 to 4,820,000 VND/month across wage-region-year cells.
- Real minimum wage, 2018 CPI base, ranges from 2,760,000 to about 4,165,614 VND/month.
- Each year has 4 real minimum wage values, corresponding to wage regions I-IV.
- Each wage region has 7 annual real minimum wage values.
- Five provinces switch assigned wage region over time in the province-level mapping: Bac Lieu, Binh Phuoc, Binh Thuan, Ca Mau, Tay Ninh.
- Rows with `needs verification` in the mapping note: 0.
- Rows flagged as mixed district regions: 385.

Treatment variation is mainly from policy year and wage region. It is not individual-level treatment variation.

## 6. Nonlinearity Final Summary

Summary from `reports/tables/nonlinearity_summary_final.csv`:

- `min_wage_nominal`: mildly curved
- `real_min_wage`: mildly curved
- `log_real_min_wage`: visibly curved
- `min_wage_growth`: mildly curved
- `unemployment_rate`: visibly curved
- `labour_productivity`: visibly curved
- `trained_labour_rate`: mildly curved
- `employed_persons`: visibly curved
- `log_employed_persons`: visibly curved

The LOWESS diagnostics suggest possible non-linear associations between `informal_rate` and both treatment-related variables and controls, especially `log_real_min_wage`, `unemployment_rate`, `labour_productivity`, and employment scale variables.

## 7. Model Comparison Final

Summary from `reports/tables/model_comparison_linear_vs_ml_final.csv`:

| model | RMSE | MAE | R2 |
|---|---:|---:|---:|
| Gradient Boosting custom | 5.615 | 4.470 | 0.810 |
| Random Forest custom | 5.656 | 4.624 | 0.807 |
| Linear Regression | 7.367 | 5.546 | 0.672 |

The best ML model has more than 10% lower cross-validated RMSE than linear regression. This is preliminary predictive evidence of non-linearity, not causal evidence.

## 8. Data Limitations

- The current dataset is aggregate province-year data, not individual-level microdata.
- The province wage-region mapping is a province-level approximation.
- Vietnam's regional minimum wage is officially applied at district/urban district/town/provincial-city areas, not always uniformly at the province level.
- Many province-year rows are flagged as mixed district regions in the mapping notes, so treatment assignment should be interpreted carefully.
- Visualization and model comparison are diagnostic exercises, not causal estimates.
- DML has not been run at this step.
- No conclusion should be made at the individual-worker level from this aggregate panel alone.
