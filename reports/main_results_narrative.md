# Main Results Narrative

## Purpose

This section provides a 1-2 page narrative for the main empirical results. It follows the required structure:

1. The data show nonlinear patterns.
2. Baseline models show sign reversal: between-province estimates are negative, while within-province estimates are positive.
3. DML is negative and relatively stable, but mainly uses between-province variation.
4. DML with province dummies becomes weak, suggesting the disagreement with TWFE is driven by province heterogeneity and thin within variation, not simply by nonlinearity.
5. CRF has the same broad sign as DML but is seed-sensitive.
6. The conclusion must remain cautious.

## 1. Nonlinearity Evidence

The first result is diagnostic. The relationship between informal employment, minimum wages, and local controls is not well summarized by a purely linear specification.

The evidence comes from several sources. Raw LOWESS plots show curvature for `log_real_min_wage`, `labour_productivity`, `unemployment_rate`, and employment-scale variables. Residualized LOWESS strengthens this point: in the DML-like specification with controls and year effects, `log_real_min_wage` has a LOWESS departure ratio of about `0.275`, while `real_min_wage` has a departure ratio of about `0.312`. Formal RESET tests reject linearity in all six tested treatment/specification combinations, with p-values below or around `0.003`. However, the squared treatment-only tests are weak, while squared-control tests are stronger in pooled and year-FE models.

This implies that the main nonlinearity is likely in the nuisance relationship between W and Y, rather than a simple nonlinear treatment effect of D on Y. Therefore, flexible methods such as DML are useful as robustness checks for nuisance adjustment, not as proof of causality.

## 2. Baseline Sign Reversal

The baseline models show a clear sign reversal.

For `log_real_min_wage`:

- Pooled OLS + W: `-44.84`, p = `0.0035`.
- Year FE + W: `-48.18`, p = `0.0039`.
- Province FE + W: `13.91`, p = `0.0034`.
- TWFE + W: `13.33`, p = `0.0375`.

The negative pooled/year-FE estimates use substantial between-province variation. The positive province-FE/TWFE estimates use within-province variation over time. The sign reversal therefore suggests that province heterogeneity is central. Provinces with higher wage regions may differ systematically in productivity, employment structure, urbanization, informality, and labor-market composition.

This is why TWFE should be treated as the main linear panel benchmark, but still not as final causal proof.

## 3. Main DML Result

The main DML specification uses W controls and year dummies. It does not include province dummies.

For `log_real_min_wage`, the main DML theta is approximately `-33.34`. The sign is stable across learners, seeds, folds, and K choices:

- 100% of 9 main runs are negative.
- 98% of 45 fold-level estimates are negative.
- K=2, K=5, and K=10 sweeps all have 100% negative signs.

This is an important robustness result, but it should be described carefully. The correct wording is **relatively stable**, not **converged**. Confidence intervals still contain zero in about 22% of main runs, mainly in Gradient Boosting specifications, and magnitude depends on learner.

In magnitude terms, theta around `-33` implies that a 10% increase in real minimum wages is associated with roughly:

```text
-33 x 0.10 = -3.3 percentage points
```

lower `informal_rate` in the main DML specification. This is a specification-conditional association, not a definitive causal effect.

## 4. DML With Province Dummies

The key enhanced result comes from the DML variant with province dummies.

When province dummies are added, the DML result weakens sharply:

- Mean theta for `log_real_min_wage` becomes about `-1.87`.
- The theta range is approximately `[-14.63, 14.09]`.
- The p-value rises to about `0.3096`.
- Confidence intervals contain zero in about 78% of runs.
- Signs flip across learners.

This result changes the interpretation. The disagreement between main DML and TWFE should not be described simply as "DML captures nonlinearity while TWFE does not." A better interpretation is:

> The main DML result relies heavily on between-province variation. When province heterogeneity is absorbed, the DML signal becomes weak because within-province treatment variation is thin.

The method-comparison output notes that roughly 95% of D variation is between provinces. Therefore, the difference between DML and TWFE is mainly about variation source and province heterogeneity, not only about nonlinearity.

## 5. CRF Result

CRF is now implemented and should be used as exploratory heterogeneity analysis.

For `log_real_min_wage`, CRF estimates are broadly negative across seeds. For example, the ATE estimates range roughly from `-17.21` to `-1.86` across reported seeds. The CRF direction is consistent with the main DML direction.

However, CRF should not be a main causal result:

- Confidence intervals usually contain zero.
- Magnitudes are seed-sensitive.
- The sample has only 441 observations.
- Individual CATEs are noisy.
- CRF uses controls and year dummies, but not province dummies in the main run.

Thus, CRF should be described as exploratory heterogeneity evidence that broadly aligns with DML, but is too uncertain for strong claims.

## 6. Main Conclusion

The main conclusion is cautious:

> The evidence is specification-sensitive and variation-source-sensitive. Between-province specifications tend to produce negative estimates, while within-province linear specifications produce positive estimates. Main DML and CRF point negative, but DML with province dummies weakens substantially. Therefore, the current evidence should be interpreted as robust diagnostics and baseline associations, not as definitive causal evidence.

## Suggested Results Paragraph

The results reveal substantial sensitivity to both specification and variation source. Pooled OLS and year-FE models estimate a negative association between log real minimum wages and informal employment, while province-FE and TWFE models estimate a positive association. Nonlinearity diagnostics indicate that linear nuisance adjustment may be restrictive, especially for the relationship between controls and informal employment. Main DML estimates are negative and relatively stable across learners, seeds, folds, and K choices, but they rely mainly on between-province variation. When province dummies are added to the DML specification, the estimate becomes weak and sign-unstable, suggesting that the disagreement with TWFE is driven by province heterogeneity and limited within-province treatment variation rather than by nonlinearity alone. CRF estimates have the same broad negative direction as DML but are exploratory and seed-sensitive. Overall, the evidence does not support a definitive causal conclusion.

## Source Files Used

- `reports/tables/method_comparison_summary.csv`
- `reports/tables/residualized_lowess_summary.csv`
- `reports/tables/nonlinearity_formal_tests.csv`
- `reports/tables/dml_convergence_interpretation.csv`
- `reports/tables/dml_theta_province_fe.csv`
- `reports/tables/crf_stability_by_seed.csv`
- `reports/tables/crf_ate_results.csv`

