# Review of Tasks 1 to 6

## Purpose

This note reviews the first six research tasks completed in the current workflow and checks whether the outputs are consistent with the repo's current empirical evidence.

## Task Status

| Task | Output | Status | Review |
|---|---|---|---|
| 1. Finalize Y-D-W specification | `reports/specification_y_d_w.md` and `reports/tables/specification_y_d_w.csv` | Complete | The specification is clear: `informal_rate` as Y, `log_real_min_wage` as main D, and available controls separated from included controls. |
| 2. Summarize nonlinearity evidence | `reports/nonlinearity_evidence.md` and `reports/tables/nonlinearity_key_figures.csv` | Complete | The summary correctly states that LOWESS and ML comparisons are diagnostic, not causal evidence. |
| 3. Explain why linear OLS may be limited | `reports/why_linear_ols_may_be_limited.md` | Complete | The note positions OLS/FE/TWFE as necessary baselines while explaining functional-form limits. |
| 4. Review DML theta stability | `reports/dml_theta_convergence_interpretation.md` and `reports/tables/dml_theta_convergence_interpretation.csv` | Complete | The note correctly distinguishes stable DML direction from causal proof and flags `min_wage_growth` as unstable. |
| 5. Choose main DML treatment | `reports/dml_treatment_choice.md` and `reports/tables/dml_treatment_choice.csv` | Complete | `log_real_min_wage` is selected as main DML treatment, `real_min_wage` as robustness, and `min_wage_growth` as exploratory. |
| 6. Compare OLS/FE/TWFE vs DML | `reports/model_family_comparison.md` and `reports/tables/model_family_comparison.csv` | Complete | The comparison is framed by model role rather than claiming one model is automatically causal. (Update: CRF has since been implemented; the comparison table now includes CRF and the DML province-dummies variant. See `reports/tables/method_comparison_summary.csv` for the canonical 19-row comparison.) |

## Consistency Check

The completed tasks are internally consistent.

The project now has a clear sequence:

1. Define Y-D-W.
2. Document nonlinearity diagnostics.
3. Explain why linear OLS may be limited.
4. Check DML theta stability.
5. Choose the main DML treatment.
6. Compare model families by research role.

The main empirical tension is also clear:

- Linear panel benchmark: TWFE with `log_real_min_wage` is positive and statistically significant.
- DML robustness: `log_real_min_wage` theta is negative and relatively stable.

This disagreement should not be hidden. It should become part of the paper's central limitation and interpretation.

## Recommended Adjustment to Later Tasks

The later tasks should be adjusted slightly:

- Task 7 should compare the current evidence with literature in terms of method, identification, and outcome definition, not just coefficient signs.
- Task 8 should write a cautious result narrative around specification sensitivity.
- Task 9 should explicitly list sample size, identification limits, DML limitations, and disagreement between TWFE and DML.
- Task 10 should draft the paper as a transparent empirical study with robustness diagnostics, not as a paper claiming a clean causal estimate.

## Files Created Across Tasks 1 to 6

- `reports/specification_y_d_w.md`
- `reports/tables/specification_y_d_w.csv`
- `reports/nonlinearity_evidence.md`
- `reports/tables/nonlinearity_key_figures.csv`
- `reports/why_linear_ols_may_be_limited.md`
- `reports/dml_theta_convergence_interpretation.md`
- `reports/tables/dml_theta_convergence_interpretation.csv`
- `reports/dml_treatment_choice.md`
- `reports/tables/dml_treatment_choice.csv`
- `reports/model_family_comparison.md`
- `reports/tables/model_family_comparison.csv`
