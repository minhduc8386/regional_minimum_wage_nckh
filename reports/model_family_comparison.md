# OLS, FE, TWFE, DML, and CRF Comparison After Main Merge

## Purpose

This note updates the model-family comparison after the main branch added enhanced DML checks and Causal Forest DML outputs.

The comparison should be read by model role, not as a competition where one model automatically wins.

## Main Comparison For `log_real_min_wage`

| Method | Estimate | Direction | Role | Interpretation |
|---|---:|---|---|---|
| Pooled OLS + W | `-44.84` | negative | Descriptive baseline | Uses between and within variation, no FE. |
| Year FE + W | `-48.18` | negative | Common-shock-adjusted baseline | Still mainly between-province variation after year shocks. |
| Province FE + W | `13.91` | positive | Within-province baseline | Sign flips after absorbing province heterogeneity. |
| TWFE + W | `13.33` | positive | Main linear panel benchmark | Within-province, net of common year shocks. |
| DML, W + year dummies | `-33.34` | negative | Flexible-control robustness | Stable across seeds/folds/K, but closer to year-FE variation. |
| DML + province dummies | `-1.87` | mixed/weak | TWFE-comparable robustness | Weak and sign-unstable; little within-province D variation remains. |
| Causal Forest DML | about `-7.86` to `-17.21` depending on seed | negative but uncertain | Exploratory heterogeneity | Sign broadly negative, but seed-sensitive and CIs contain zero. |

## Updated Interpretation

The updated evidence makes the core message sharper:

> Results are both specification-sensitive and variation-source-sensitive.

The negative estimates come mainly from pooled/year-FE/DML specifications that rely substantially on between-province variation. The positive estimates come from province-FE/TWFE specifications that focus on within-province changes. When DML is modified to include province dummies, the negative signal becomes weak and unstable.

## Role Of CRF

CRF is now implemented in the repo. It should no longer be treated as blank.

However, CRF should be framed narrowly:

- It is exploratory heterogeneity analysis.
- It uses `CausalForestDML` with grouped cross-fitting by province.
- It reports average marginal effects and CATE distributions.
- It does not provide standalone causal proof.
- With only 441 observations, CATE estimates are noisy.

For `log_real_min_wage`, CRF estimates are negative across reported seeds, but confidence intervals contain zero in the main stability runs and magnitudes are seed-sensitive. This supports a cautious heterogeneity narrative, not a main result.

## Recommendation For Results Section

The results section should use this hierarchy:

1. TWFE is the main linear panel benchmark.
2. DML without province dummies is flexible-control robustness, but not TWFE-equivalent.
3. DML with province dummies is a critical sensitivity check showing weak within-province DML evidence.
4. CRF is exploratory heterogeneity only.

## Suggested Paper Wording

The model comparison shows that estimates depend strongly on both specification and variation source. Pooled OLS, year-FE, and main DML specifications produce negative estimates for the log real minimum wage, while province-FE and TWFE specifications produce positive estimates. A DML variant with province dummies weakens the negative DML signal, suggesting that the main DML estimate relies heavily on between-province variation. CRF estimates are broadly negative but exploratory, seed-sensitive, and statistically uncertain. Overall, the evidence should be interpreted as specification-sensitive rather than as a single definitive causal estimate.

## Source Files Used

- `reports/tables/method_comparison_summary.csv`
- `reports/tables/baseline_ols_fe_results.csv`
- `reports/tables/dml_convergence_interpretation.csv`
- `reports/tables/dml_theta_province_fe.csv`
- `reports/tables/crf_ate_results.csv`
- `reports/tables/crf_stability_by_seed.csv`
- `reports/tables/crf_cate_summary.csv`
- `reports/crf_implementation_note.md`

