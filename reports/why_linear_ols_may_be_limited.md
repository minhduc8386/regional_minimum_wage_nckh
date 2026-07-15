# Why Linear OLS May Be Limited

## Purpose

This section explains why linear OLS/FE/TWFE models may be limited in this project. It does not argue that OLS is wrong. OLS, FE, and TWFE remain necessary baseline models.

The main concern is that a linear model may misspecify the nuisance relationship between controls W and outcome Y.

## Core Logic

The current diagnostics suggest that nonlinearity is concentrated more in the relationship between W and Y than in a simple nonlinear D-Y treatment effect.

This matters because the baseline linear model assumes:

```text
informal_rate = linear function of D + linear function of W + FE + error
```

If the true relationship between `informal_rate` and controls such as `labour_productivity`, `trained_labour_rate`, `unemployment_rate`, or `log_employed_persons` is nonlinear, then the linear baseline may leave systematic structure in the residuals.

DML is useful here not because it magically proves causality, but because it can estimate nuisance functions flexibly:

```text
g(W) = E[Y | W]
m(W) = E[D | W]
```

This makes DML a reasonable robustness check after OLS/FE/TWFE.

## Evidence

The evidence comes from:

- raw LOWESS curvature;
- residualized LOWESS curvature in DML-like specifications;
- RESET tests rejecting linearity;
- formal tests showing stronger nonlinear evidence in W terms than in D-only squared terms;
- PDPs showing non-flat predictive relationships;
- ML predictive models fitting `informal_rate` better than linear regression.

Important nuance:

After province fixed effects are included, the residualized LOWESS curvature becomes milder. This suggests that part of the apparent nonlinearity is related to province-level structure and between-province differences.

## Correct Interpretation

Do not write:

```text
OLS is wrong.
```

Write:

```text
OLS/FE/TWFE are transparent baseline associations, but diagnostics suggest that linear nuisance adjustment may be restrictive. DML is used as an additional robustness check for flexible control adjustment.
```

## Suggested Paper Paragraph

The baseline OLS/FE/TWFE models are retained because they provide transparent and auditable panel estimates. However, the nonlinearity diagnostics suggest that a purely linear specification may be restrictive, especially for the nuisance relationship between local controls and informal employment. RESET tests reject linearity in several specifications, and squared-control tests indicate that nonlinearities are stronger in the controls than in the treatment-only quadratic terms. For this reason, DML is used as a supplementary robustness exercise that flexibly learns the nuisance functions. This does not imply that OLS is invalid or that DML provides causal identification; it only addresses whether the estimated relationship is sensitive to linear control-function assumptions.

