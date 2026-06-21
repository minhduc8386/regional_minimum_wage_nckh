# Project Completion Summary

Generated at: `2026-06-21 17:48:37`

## File Inventory

| file | status |
|---|---|
| `data/processed/nso_employment/province_year_panel_2018_2024.csv` | OK |
| `data/processed/policy/min_wage_region_panel.csv` | OK |
| `data/processed/policy/province_wage_region_map.csv` | OK |
| `data/processed/economy/cpi_panel.csv` | OK |
| `data/processed/final/analysis_panel_2018_2024.csv` | OK |
| `reports/tables/final_analysis_panel_validation.csv` | OK |
| `reports/tables/treatment_variation_summary.csv` | OK |
| `reports/tables/nonlinearity_summary_final.csv` | OK |
| `reports/tables/model_comparison_linear_vs_ml_final.csv` | OK |

## Scripts

| script | status |
|---|---|
| `scripts/01_clean_nso_province_panel.py` | OK |
| `scripts/02_check_nonlinearity.py` | OK |
| `scripts/03_validate_raw_policy_inputs.py` | OK |
| `scripts/04_build_min_wage_region_panel.py` | OK |
| `scripts/05_build_province_wage_region_map.py` | OK |
| `scripts/06_build_cpi_panel.py` | OK |
| `scripts/07_merge_final_analysis_panel.py` | OK |
| `scripts/08_check_treatment_variation.py` | OK |
| `scripts/09_check_nonlinearity_with_treatment.py` | OK |
| `scripts/10_model_comparison_with_treatment.py` | OK |
| `scripts/11_generate_project_completion_summary.py` | OK |

## Final Panel

- Path: `data/processed/final/analysis_panel_2018_2024.csv`
- Shape: `441 x 15`
- Provinces: `63`
- Years: `2018, 2019, 2020, 2021, 2022, 2023, 2024`
- Duplicate `province-year`: `0`
- Missing values total: `0`
- Columns: `province`, `year`, `wage_region`, `informal_rate`, `min_wage_nominal`, `cpi_index`, `cpi_2018_base`, `real_min_wage`, `log_real_min_wage`, `min_wage_growth`, `unemployment_rate`, `labour_productivity`, `trained_labour_rate`, `employed_persons`, `log_employed_persons`

Research variables:

- Y: `informal_rate`
- D: `real_min_wage`, `log_real_min_wage`, `min_wage_growth`
- W: `unemployment_rate`, `labour_productivity`, `trained_labour_rate`, `employed_persons`, `log_employed_persons`


## Treatment

- `real_min_wage = min_wage_nominal / cpi_2018_base * 100`
- `log_real_min_wage = log(real_min_wage)`
- `min_wage_growth` is computed by wage region over time; 2018 is filled as 0.

| variable | min | mean | max | std |
|---|---:|---:|---:|---:|
| `min_wage_nominal` | 2760000.000 | 3650839.002 | 4820000.000 | 446520.995 |
| `real_min_wage` | 2760000.000 | 3349193.356 | 4165613.888 | 349965.113 |
| `log_real_min_wage` | 14.831 | 15.019 | 15.242 | 0.102 |
| `min_wage_growth` | -0.018 | 0.003 | 0.029 | 0.014 |

- Mapping rows with `needs verification`: `0`
- Mapping rows flagged as mixed district regions: `385`
- Provinces switching wage region over time: `5`
- Switching provinces: Bac Lieu, Binh Phuoc, Binh Thuan, Ca Mau, Tay Ninh

## Nonlinearity

| variable | type | pattern | conclusion |
|---|---|---|---|
| `min_wage_nominal` | treatment | mildly curved | weak-to-moderate possible non-linearity |
| `real_min_wage` | treatment | mildly curved | weak-to-moderate possible non-linearity |
| `log_real_min_wage` | treatment | visibly curved | possible non-linearity |
| `min_wage_growth` | treatment | mildly curved | weak-to-moderate possible non-linearity |
| `unemployment_rate` | control | visibly curved | possible non-linearity |
| `labour_productivity` | control | visibly curved | possible non-linearity |
| `trained_labour_rate` | control | mildly curved | weak-to-moderate possible non-linearity |
| `employed_persons` | control | visibly curved | possible non-linearity |
| `log_employed_persons` | control | visibly curved | possible non-linearity |

## Model Comparison

Predictive diagnostic only; not a causal estimate.

| model | RMSE | MAE | R2 |
|---|---:|---:|---:|
| `gradient_boosting_custom` | 5.615 | 4.470 | 0.810 |
| `random_forest_custom` | 5.656 | 4.624 | 0.807 |
| `linear_regression` | 7.367 | 5.546 | 0.672 |

Conclusion: ML model has at least 10% lower CV RMSE than linear regression; preliminary evidence of non-linearity.

## Limitations

- Current data are aggregate province-year data, not individual microdata.
- Province-to-wage-region mapping is an approximation.
- Vietnam's regional minimum wage is applied at district/town/provincial-city level, not uniformly at province level.
- LOWESS and model comparison are diagnostics, not causal estimates.
- DML has not been run as a causal model yet.

