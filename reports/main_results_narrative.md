# Main Results Narrative

## Purpose

This note provides a concise narrative for the current empirical results. It is written for use in the results section of the paper or presentation.

## Core Narrative

The empirical results show that the relationship between regional minimum wage exposure and province-year informal employment rates is sensitive to model specification.

In pooled OLS and year-FE specifications, `log_real_min_wage` is negatively associated with `informal_rate`. However, once province fixed effects are included, the association becomes positive. The two-way fixed effects specification, which controls for both time-invariant province differences and common year shocks, estimates a positive coefficient for `log_real_min_wage`.

This sign change is important. It suggests that cross-sectional differences across provinces are a major part of the raw negative association. Provinces with higher real minimum wages may differ systematically from lower-wage provinces in productivity, employment scale, labor-market structure, and development level. Once the model focuses more on within-province changes over time, the estimated association changes direction.

At the same time, the nonlinearity diagnostics indicate that a purely linear specification may be restrictive. LOWESS plots show curvature for `log_real_min_wage` and several controls, and flexible predictive models fit `informal_rate` better than a linear regression. These diagnostic results do not establish causality, but they motivate the use of flexible-control robustness checks.

The DML results provide such a robustness check. For `log_real_min_wage`, DML estimates are consistently negative across learners, seeds, and most folds. However, this DML result differs in sign from the TWFE estimate. Because the current DML setup does not replace a credible identification strategy, this disagreement should be interpreted as evidence of model sensitivity rather than as proof that one estimate is correct.

## Suggested Results Paragraph

The baseline models reveal substantial specification sensitivity. In pooled OLS and year-FE models, the log real minimum wage is negatively associated with the informal employment rate. After province fixed effects are included, the coefficient becomes positive, and the two-way fixed effects model also estimates a positive association. This pattern suggests that cross-province differences account for an important part of the pooled negative relationship. Nonlinearity diagnostics further indicate that the relationship between informal employment, minimum wages, and local labor-market controls is not fully captured by a simple linear specification. DML robustness checks produce a stable negative theta for the log real minimum wage, but this estimate differs in sign from the TWFE benchmark. Taken together, the results should be interpreted as specification-sensitive baseline evidence rather than definitive causal evidence.

## Treatment-Specific Interpretation

### `log_real_min_wage`

This is the main treatment for reporting. It is interpretable, reduces scale issues, and is the most stable DML treatment.

Current pattern:

- Pooled/year-FE association: negative.
- Province-FE/TWFE association: positive.
- DML theta: negative and relatively stable.

Interpretation:

The evidence is informative but not settled. The sign disagreement between TWFE and DML should be highlighted as a central result.

### `real_min_wage`

This is a useful robustness treatment. It shows a pattern similar to `log_real_min_wage`, but the level coefficient is harder to communicate because it depends on VND/month units.

Interpretation:

Use it to show that the log-treatment conclusion is not purely an artifact of the log transform.

### `min_wage_growth`

This should not be a main treatment. The TWFE estimate is statistically weak, and DML theta stability is poor.

Interpretation:

Use only as exploratory evidence or appendix robustness.

## What Not To Claim

The current results should not be written as:

- "Minimum wages cause informal employment to increase."
- "DML proves that minimum wages reduce informal employment."
- "Machine learning is better than TWFE, so DML should be the main result."
- "The result confirms or contradicts prior literature by coefficient magnitude."

## What To Claim

The safer claim is:

- The current province-year panel shows specification-sensitive associations between regional minimum wage exposure and informal employment rates.
- Province fixed effects materially change the estimated relationship.
- Nonlinearity diagnostics motivate flexible-control robustness checks.
- DML results are stable for `log_real_min_wage`, but differ from TWFE, so the evidence remains cautious.

## Source Files Used

- `reports/model_family_comparison.md`
- `reports/baseline_ols_fe_summary.md`
- `reports/dml_treatment_choice.md`
- `reports/dml_theta_convergence_interpretation.md`
- `reports/why_linear_ols_may_be_limited.md`

