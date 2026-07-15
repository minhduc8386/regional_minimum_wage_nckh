# Regional Minimum Wages and Informal Employment in Vietnam: Province-Year Evidence from 2018-2024

## Abstract

This paper studies the association between Vietnam's regional minimum wage policy and informal employment rates using a balanced province-year panel from 2018 to 2024. The analysis combines province-level informal employment rates, CPI-adjusted regional minimum wage exposure, and local labor-market controls. The empirical design is intentionally cautious. It first reports transparent OLS, fixed-effects, and two-way fixed-effects baselines, then uses nonlinearity diagnostics, Double/Debiased Machine Learning (DML), and Causal Forest DML (CRF) as robustness and heterogeneity diagnostics. The results are specification-sensitive. Pooled OLS and year-FE models estimate negative associations between log real minimum wages and informal employment, while province-FE and TWFE models estimate positive associations. Main DML estimates are negative and relatively stable across learners, seeds, folds, and K choices, but the signal weakens when province dummies are added. CRF estimates point in the same broad negative direction as DML but are seed-sensitive and statistically uncertain. The findings are therefore interpreted as specification-sensitive associations rather than definitive causal evidence.

## 1. Introduction

Minimum wage policy can affect labor markets through several channels. It may raise wages for workers close to the minimum wage, change firms' hiring incentives, alter formal employment, and shift workers between formal employment, informal employment, self-employment, unemployment, and inactivity. These mechanisms are especially important in developing economies where informal employment is large and enforcement can vary across places and sectors.

Vietnam provides a relevant setting because minimum wages are set by region and vary across space and time. This project studies whether regional minimum wage exposure is associated with province-year informal employment rates during 2018-2024. This period is recent and includes COVID and post-COVID labor-market disruptions, which makes careful interpretation especially important.

The paper's contribution is not a clean quasi-experimental causal design. Instead, the contribution is a transparent empirical pipeline. The project builds a balanced province-year panel, defines the outcome-treatment-control specification clearly, documents nonlinear patterns, reports baseline panel models, and uses DML and CRF only as robustness and diagnostic tools.

The main finding is that estimates depend strongly on model specification and variation source. Models that rely substantially on between-province variation tend to produce negative estimates. Models that absorb province fixed effects and focus on within-province variation tend to produce positive estimates. Main DML estimates are negative and relatively stable, but when province dummies are added to the DML specification, the signal weakens. CRF results are broadly negative but exploratory and statistically uncertain.

## 2. Literature And Research Gap

The minimum wage literature studies wages, employment, hours, poverty, welfare, formal employment, informal employment, and self-employment. Common methods include OLS, fixed effects, Difference-in-Differences, event studies, border comparisons, RIF regressions, distributional methods, and more recently causal machine learning for flexible nuisance adjustment.

Perez Perez (2020) is the closest international benchmark because it studies minimum wages in formal and informal sectors using an unexpected real minimum wage shock in Colombia. Its strength is identification: the paper uses shock-based treatment intensity across city-industry cells. The current project does not have an equivalent shock and should not compare coefficient magnitudes directly with Colombia.

Vietnam studies provide policy context. Del Carpio et al. study minimum wages, employment, wages, self-employment, and welfare in Vietnam using enterprise and household survey data. Nguyen Viet Cuong studies Vietnam minimum wage effects using more recent labor-force data and fixed-effects approaches. These papers motivate the Vietnam context and mechanisms, but the current project differs by focusing on province-year `informal_rate` from 2018 to 2024.

The current project contributes recent aggregate evidence and a structured diagnostic workflow. It asks whether regional minimum wage exposure is associated with informal employment rates, how sensitive the estimates are to fixed effects, and whether flexible nuisance adjustment changes the pattern.

Recommended comparison table for the paper:

```text
Use reports/literature_comparison_current_results.md
```

## 3. Data

The analysis uses a balanced province-year panel:

- Unit: province-year.
- Period: 2018-2024.
- Observations: 441.
- Provinces/cities: 63.
- Years: 7.
- Duplicate province-year rows: none.
- Missing values in required modeling variables: none.

The outcome is:

```text
informal_rate
```

The main treatment variables are:

```text
log_real_min_wage
real_min_wage
```

The exploratory treatment is:

```text
min_wage_growth
```

The main controls are:

```text
unemployment_rate
labour_productivity
trained_labour_rate
log_employed_persons
```

The level employment variable, `employed_persons`, is available only as a robustness alternative to `log_employed_persons`. They should not be used together in the same main model.

Two data limitations are important. First, the official citation for the `informal_rate` source still needs final verification. The repo identifies the raw workbook and sheet, but the final paper should cite the official publisher, table, URL or publication source, and access date. Second, minimum wage exposure is mapped at province-year level, even though official wage-region classifications can vary at district level. This creates possible treatment measurement error.

## 4. Specification

The main Y-D-W specification is:

```text
Y = informal_rate
D_main = log_real_min_wage, real_min_wage
D_exploratory = min_wage_growth
W = unemployment_rate + labour_productivity + trained_labour_rate + log_employed_persons
Unit = province-year
Period = 2018-2024
```

The main linear benchmark is TWFE:

```text
informal_rate_it = beta D_it + gamma W_it + province FE_i + year FE_t + error_it
```

Standard errors are clustered by province where possible.

DML is used after the baseline models. The original DML specification uses W controls and year dummies, but not province dummies. A second DML variant adds province dummies to check whether the DML result survives a TWFE-comparable within-province structure.

CRF is used only as exploratory heterogeneity analysis. It is not the main causal estimator.

## 5. Nonlinearity Evidence

The nonlinearity diagnostics suggest that a purely linear specification is restrictive, especially for the nuisance relationship between controls W and outcome Y.

Raw LOWESS plots show curvature between `informal_rate` and `log_real_min_wage`, `unemployment_rate`, `labour_productivity`, and employment-scale variables. Residualized LOWESS adds more detail. In the DML-like specification with W controls and year effects, the LOWESS departure ratio is about `0.275` for `log_real_min_wage` and about `0.312` for `real_min_wage`. In the TWFE-like residualized specification with W, year effects, and province effects, the departure ratios fall to about `0.127` and `0.117`.

Formal RESET tests reject linearity in all six tested treatment/specification combinations, with p-values below or around `0.003`. However, treatment-only squared terms are not strong. Squared-control tests are stronger in pooled and year-FE models. This suggests that nonlinearity is mainly in the W-Y nuisance relationship, not a simple quadratic treatment effect.

Recommended figures:

- `reports/figures/nonlinearity_final/lowess_informal_rate_vs_log_real_min_wage.png`
- `reports/figures/nonlinearity_residualized/residualized_lowess_log_real_min_wage_w_year.png`
- `reports/figures/nonlinearity_residualized/residualized_lowess_log_real_min_wage_w_year_province.png`
- `reports/figures/pdp/pdp_log_real_min_wage_random_forest.png`
- `reports/figures/pdp/pdp_log_real_min_wage_gradient_boosting.png`

These figures should be presented as diagnostics only.

## 6. Baseline Results

The baseline results show a clear sign reversal.

For `log_real_min_wage`:

| model | estimate | p-value | interpretation |
|---|---:|---:|---|
| Pooled OLS + W | `-44.84` | `0.0035` | negative association using between + within variation |
| Year FE + W | `-48.18` | `0.0039` | negative association net of common year shocks |
| Province FE + W | `13.91` | `0.0034` | positive within-province association |
| TWFE + W | `13.33` | `0.0375` | positive within-province association net of year shocks |

The negative pooled/year-FE estimates rely heavily on between-province comparisons. The positive province-FE/TWFE estimates absorb time-invariant province heterogeneity and focus on within-province changes. This indicates that province heterogeneity is central to the empirical pattern.

For `real_min_wage`, the sign pattern is similar. For `min_wage_growth`, evidence is weaker and less stable. The TWFE estimate for `min_wage_growth` is statistically insignificant.

## 7. DML Results

The main DML result for `log_real_min_wage` is negative and relatively stable.

Key evidence:

- Mean theta is approximately `-33.34`.
- 100% of 9 main runs are negative.
- 98% of 45 fold-level estimates are negative.
- K=2, K=5, and K=10 sweeps all show 100% negative signs.

In magnitude terms, theta around `-33` implies that a 10% increase in real minimum wages is associated with approximately:

```text
-33 x 0.10 = -3.3 percentage points
```

lower `informal_rate` in the main DML specification.

This should not be described as convergence or as a causal effect. The correct phrase is **relatively stable**. Confidence intervals still contain zero in about 22% of main runs for `log_real_min_wage` and 33% for `real_min_wage`, mainly in Gradient Boosting specifications. Magnitudes also depend on learner.

The most important enhanced result is the DML variant with province dummies. When province dummies are added:

- `log_real_min_wage` theta becomes approximately `-1.87`.
- The theta range is approximately `[-14.63, 14.09]`.
- The p-value rises to about `0.3096`.
- Confidence intervals contain zero in about 78% of runs.
- Signs flip across learners.

This means the original DML result is not TWFE-equivalent. It relies mainly on between-province variation. The disagreement between DML and TWFE is therefore driven by province heterogeneity and thin within-province treatment variation, not simply by the fact that DML can model nonlinearity.

## 8. CRF Results

CRF is implemented as exploratory heterogeneity analysis.

For `log_real_min_wage`, CRF estimates are broadly negative across seeds. The ATE range across reported seeds is roughly `[-17.21, -1.86]`. This direction is consistent with the main DML result.

However, CRF is not a main causal result:

- confidence intervals usually contain zero;
- magnitudes are seed-sensitive;
- the sample has only 441 observations;
- individual CATEs are noisy;
- the main CRF specification uses controls and year dummies, but not province dummies.

Therefore, CRF should be discussed briefly and cautiously. It supports the idea that flexible methods often point negative, but it does not resolve the identification problem.

## 9. Method Comparison

The method comparison should be organized by variation source:

- Pooled OLS uses between and within variation.
- Year FE removes common shocks but still relies heavily on between-province variation.
- Province FE and TWFE focus on within-province variation.
- Main DML uses flexible controls but no province dummies, so it is closer to year-FE/between-province variation.
- DML with province dummies is more TWFE-comparable and becomes weak.
- CRF is exploratory heterogeneity analysis.

No method should be described as mechanically better. They answer related but different questions because they use different sources of variation.

Use:

```text
reports/tables/method_comparison_summary.csv
```

as the main comparison table. Do not put the full raw DML 81-run table in the body; keep detailed runs in appendix or reproducibility files.

## 10. Limitations

The main limitations are:

1. The data are aggregate province-year data, not worker-level microdata.
2. There is no clean untreated control group.
3. Wage-region treatment is mapped at province level, while policy can vary by district.
4. Treatment measurement error may attenuate or distort estimates.
5. Roughly 95% of treatment variation is between provinces/wage regions, leaving limited within-province variation.
6. COVID and post-COVID disruptions in 2020-2021 may affect informal employment in ways not fully captured by controls.
7. DML is robustness, not identification.
8. CRF is exploratory and seed-sensitive.
9. `min_wage_growth` is weak and should remain exploratory.
10. The official citation and definition for `informal_rate` need final verification.

Future work should use VHLSS or LFS microdata, district-year wage-region mapping, and district-level population/employment weights to construct more precise treatment exposure.

## 11. Conclusion

This paper provides recent province-year evidence on regional minimum wage exposure and informal employment in Vietnam from 2018 to 2024. The evidence is informative but cautious.

The core result is not a single definitive causal estimate. Instead, the core result is specification sensitivity. Between-province specifications tend to show negative associations, while within-province linear specifications tend to show positive associations. Main DML and CRF point negative, but DML with province dummies weakens substantially.

Therefore, the safest conclusion is:

> Regional minimum wage exposure is associated with informal employment in ways that are sensitive to model specification and variation source. The current evidence motivates further research with richer data and stronger identification, but it does not establish a definitive causal effect.

