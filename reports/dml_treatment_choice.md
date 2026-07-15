# Treatment Hierarchy For DML And Robustness

## Purpose

This note finalizes the treatment hierarchy after the enhanced DML and CRF outputs.

## Final Hierarchy

| level | variable | role | reason |
|---|---|---|---|
| Main | `log_real_min_wage` | Main treatment for reporting | Interpretable in proportional terms; stable DML sign across learners/seeds/folds/K; supported by CRF direction as exploratory evidence |
| Robustness | `real_min_wage` | Level-scale robustness | Same policy exposure in VND/month; broadly similar sign pattern to log treatment |
| Exploratory | `min_wage_growth` | Appendix/exploratory only | Weak TWFE, unstable DML, all main DML CIs include zero, K-sweep only 56% negative |

## Main Treatment: `log_real_min_wage`

`log_real_min_wage` is the preferred treatment for the main DML discussion.

Evidence:

- Main DML theta mean is approximately `-33.34`.
- 9/9 main DML runs are negative.
- 98% of fold-level estimates are negative.
- K=2, K=5, and K=10 sweeps are all 100% negative.
- CRF estimates are broadly negative across seeds, although confidence intervals usually contain zero.

Interpretation of magnitude:

A one-unit increase in `log_real_min_wage` is approximately a 100 log-point increase. For a smaller change, a 10% increase in real minimum wage corresponds approximately to `0.10` log points. Therefore:

```text
theta ≈ -33
10% real minimum wage increase ≈ -33 x 0.10 ≈ -3.3 percentage points in informal_rate
```

This should be written as an association/robustness interpretation, not as a causal effect:

> In the main DML specification, a 10% increase in real minimum wages is associated with an approximately 3.3 percentage point lower informal employment rate, conditional on the DML specification. This should not be interpreted as a definitive causal effect.

## Robustness Treatment: `real_min_wage`

`real_min_wage` remains useful because it checks whether the log-treatment result is purely a transformation artifact.

Evidence:

- Main DML theta mean is approximately `-1.01e-05`.
- 9/9 main DML runs are negative.
- K=2, K=5, and K=10 sweeps are all 100% negative.
- CRF estimates are also broadly negative.

Caution:

The coefficient is harder to communicate because it is measured per one VND/month. It should not be presented as a separate independent causal result.

## Exploratory Treatment: `min_wage_growth`

`min_wage_growth` should not be a main treatment.

Evidence:

- TWFE p-value is approximately `0.7656`.
- Main DML average p-value is approximately `0.3797`.
- All main DML confidence intervals contain zero.
- K-sweep share negative is only `56%`.
- CRF CATEs are highly dispersed.
- Enhanced validation shows that within-year variation is very small relative to time variation, so year dummies absorb much of the relevant policy timing.

## Final Wording

The main treatment is `log_real_min_wage`, with `real_min_wage` used as a level-scale robustness check. `min_wage_growth` is kept as exploratory only because it is weak and unstable across TWFE, DML, and K-sweep diagnostics. The DML magnitude for `log_real_min_wage` can be interpreted approximately as a 3.3 percentage point lower informal employment rate for a 10% increase in real minimum wages, but only as a specification-conditional association, not as a causal effect.

## Source Files Used

- `reports/tables/dml_theta_by_k.csv`
- `reports/tables/dml_convergence_interpretation.csv`
- `reports/tables/crf_ate_results.csv`
- `reports/tables/crf_stability_by_seed.csv`
- `reports/tables/enhanced_model_input_validation.csv`

