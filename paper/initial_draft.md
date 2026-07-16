# Regional Minimum Wages and Informal Employment in Vietnam: Province-Year Evidence from 2018-2024

## Abstract

This paper studies the association between Vietnam's regional minimum wage policy and informal employment rates using a balanced province-year panel covering all 63 provinces from 2018 to 2024. The analysis combines province-level informal employment rates, CPI-adjusted regional minimum wage exposure, and local labor-market controls. The empirical design is intentionally cautious. It first reports transparent OLS, fixed-effects, and two-way fixed-effects (TWFE) baselines, then uses nonlinearity diagnostics, Double/Debiased Machine Learning (DML), and Causal Forest DML (CRF) as robustness and heterogeneity diagnostics rather than as identification strategies. The results are specification-sensitive in an informative way. Pooled OLS and year-FE models estimate significant negative associations between log real minimum wages and informal employment, while province-FE and TWFE models estimate positive associations. Formal specification tests reject linearity in every baseline specification, with the nonlinearity concentrated in the relationship between controls and the outcome. Main DML estimates are negative and relatively stable across learners, seeds, folds, and cross-fitting choices, but the signal weakens sharply when province indicators are added to the nuisance functions, reflecting the fact that roughly 95 percent of treatment variation is between provinces. CRF estimates point in the same broad negative direction as DML but are seed-sensitive and statistically uncertain. The findings are therefore interpreted as specification-sensitive conditional associations rather than definitive causal evidence, and the paper documents precisely which sources of variation drive each result.

## 1. Introduction

Minimum wage policy can affect labor markets through several channels. It may raise wages for workers near the wage floor, change firms' hiring incentives, alter the cost of formal employment relative to informal arrangements, and shift workers between formal employment, informal employment, self-employment, unemployment, and inactivity. These mechanisms are especially important in developing economies, where informal employment absorbs a large share of the workforce and enforcement capacity varies across places and sectors. Whether a higher minimum wage pushes workers into informality (by raising the cost of formal jobs) or pulls them out of it (by raising the attractiveness and wage floor of formal work, or by correlating with broader development) is an empirical question, and the answer may differ by context.

Vietnam provides a relevant setting for this question. Since 2009 Vietnam has set minimum wages by wage region rather than nationally: districts are classified into four wage regions (I to IV), with Region I (major urban centers) receiving the highest floor and Region IV (mostly rural areas) the lowest. Minimum wages are revised at irregular intervals, and the real value of the floor also moves with inflation, including a period of nominal freezes during COVID-19. This creates variation in real minimum wage exposure across provinces and over time. This project studies whether that exposure is associated with province-year informal employment rates during 2018-2024, a recent period that includes the COVID and post-COVID labor-market disruptions.

The paper's contribution is deliberately not a claim to a clean quasi-experimental causal design. The available data are aggregate province-year observations, the policy varies at district level while our treatment is mapped at province level, and there is no untreated control group. Instead, the contribution is a transparent and fully reproducible empirical pipeline built in four layers. First, we construct and validate a balanced province-year panel with CPI-adjusted treatment measures. Second, we document that the data exhibit statistically detectable nonlinearity and diagnose where it is concentrated. Third, we report baseline panel estimates whose sign depends systematically on the fixed-effect structure, and we explain that dependence in terms of variation sources. Fourth, we use DML and CRF as flexible-control and heterogeneity diagnostics, including a DML variant designed specifically to test whether the DML-versus-TWFE disagreement is driven by functional form or by province heterogeneity.

The main finding is that estimates depend strongly on model specification and variation source. Models that rely substantially on between-province variation (pooled OLS, year FE, main DML) produce negative and statistically significant estimates: provinces with higher real minimum wages have lower informal employment rates, conditional on observed controls. Models that absorb province fixed effects and focus on within-province variation (province FE, TWFE) produce positive estimates. A DML variant that adds province indicators to the nuisance functions produces weak, sign-unstable estimates, which shows that the disagreement between DML and TWFE reflects thin within-province treatment variation and province heterogeneity rather than nonlinearity alone. We argue that documenting this pattern honestly is more useful than selecting one specification and presenting it as the causal answer.

The remainder of the paper proceeds as follows. Section 2 positions the project in the literature. Section 3 describes the data. Section 4 fixes the specification. Section 5 presents nonlinearity evidence. Sections 6-8 report baseline, DML, and CRF results. Section 9 compares methods, Section 10 discusses limitations, and Section 11 concludes.

## 2. Literature and Research Gap

The minimum wage literature in developing economies studies wages, employment, hours, poverty, welfare, formal employment, informal employment, and self-employment. Common identification approaches include fixed-effects panel models, difference-in-differences and event studies around discrete policy changes, border-discontinuity comparisons, distributional and RIF-regression methods, and, more recently, causal machine learning used for flexible nuisance adjustment.

Perez Perez (2020, *World Development*) is the closest international methodological benchmark for this project. It studies minimum wages in the formal and informal sectors in Colombia, exploiting an unexpected real minimum wage increase in 1999 driven by an inflation forecast error, with treatment intensity varying across city-industry cells. Its identification rests on a shock-based design over 1996-2000 household survey data. The current project has no equivalent shock: Vietnamese minimum wage revisions are anticipated and announced, and our unit of observation is the province-year rather than the city-industry cell. We therefore borrow the treatment-intensity framing and the formal/informal outcome focus, but we do not compare coefficient magnitudes with Colombia, and we do not claim comparable identification strength.

For Vietnam, Del Carpio et al. study minimum wages, employment, wages, self-employment, and household welfare using enterprise surveys and VHLSS data from 2006-2010. Their work establishes that minimum wage changes in Vietnam operate through wage employment, self-employment, and welfare channels, and it documents the institutional structure of regional wage setting. Nguyen Viet Cuong provides more recent evidence using Labor Force Survey data and fixed-effects designs over 2012-2020. Both strands motivate our covariates and mechanisms, but neither centers the province-year informal employment rate over 2018-2024, which covers the most recent minimum wage revisions and the COVID period.

The gap this project addresses is therefore threefold. First, it provides recent aggregate evidence: a complete 63-province panel for 2018-2024 with CPI-adjusted regional minimum wage exposure. Second, it tests explicitly for nonlinearity before choosing estimators, rather than assuming a linear specification. Third, it asks a methodological question of independent interest: when flexible methods (DML, CRF) and standard panel methods (TWFE) disagree, is the disagreement attributable to functional form or to the source of identifying variation? Our DML province-dummies variant is designed to answer exactly this. A structured comparison with the three benchmark papers is provided in `reports/literature_comparison_current_results.md`.

## 3. Data

### 3.1 Panel construction

The analysis panel is a balanced province-year panel assembled from four sources: (i) National Statistics Office (NSO/GSO) province-level workbooks for the informal employment rate, employed persons, unemployment rate, trained labour rate, and labour productivity; (ii) the statutory regional minimum wage schedule by wage region and year; (iii) a province-to-wage-region mapping constructed from the district-level decree classifications; and (iv) a CPI panel used to deflate nominal minimum wages to 2018 prices. The full construction pipeline (scripts 01-07 in the repository) validates each intermediate product; the final panel passes 27 automated checks covering structure, completeness, ranges, and internal consistency (`reports/tables/enhanced_model_input_validation.csv`).

The resulting panel has 441 observations: 63 provinces/cities observed in each of the 7 years from 2018 to 2024, with no missing values in any modeling variable and no duplicate province-year rows.

### 3.2 Variables

The outcome `informal_rate` is the province-year informal employment rate, measured in percentage points. It ranges from 28.4 to 91.1 across the panel, which already indicates very large and persistent cross-province differences in informality.

The treatment family measures real regional minimum wage exposure. `real_min_wage` is the statutory minimum wage of the province's assigned wage region, deflated by CPI to 2018 prices; it ranges from about 2.76 to 4.17 million VND per month. `log_real_min_wage` is its natural logarithm and is the preferred treatment for reporting because proportional changes are easier to interpret. `min_wage_growth` is the year-over-year change of the log real minimum wage and is retained only as an exploratory treatment (Section 4 explains why). Provinces containing districts in multiple wage regions are assigned a single region, which introduces measurement error discussed in Section 10.

The control set W contains four province-year variables: `unemployment_rate` (mean 2.36, SD 1.32), `labour_productivity` (mean 147, SD 92, in millions VND per worker), `trained_labour_rate` (mean 22.5, SD 8.4, percent), and `log_employed_persons` (mean 6.51, SD 0.59). The level variable `employed_persons` is available as a robustness alternative to its log; the two are never included together.

### 3.3 Treatment variation structure

A feature of the data that shapes every result in this paper is the decomposition of treatment variation. For `log_real_min_wage`, the overall standard deviation is 0.102; the within-year standard deviation is 0.101, but the within-province standard deviation is only 0.022. In other words, roughly 95 percent of treatment variance is between provinces (driven by the four wage regions), and only a thin slice reflects within-province changes over time. For `min_wage_growth` the structure is the opposite: its variation is almost entirely a common time series (within-year SD is 0.001 against an overall SD of 0.014), so year fixed effects absorb nearly all of it. The panel composition by wage region is 49 observations in Region I, 115 in Region II, 235 in Region III, and 42 in Region IV.

### 3.4 Data caveats

Two caveats deserve early mention. First, the official citation and definitional details for the `informal_rate` series still require final verification before submission; the repository records the raw workbook and sheet, but the paper must cite the official publication. Second, as noted, wage-region classification is a district-level policy mapped here to provinces, so treatment is measured with error, most plausibly of an attenuating kind.

## 4. Specification

### 4.1 Y-D-W structure

The specification, fixed in `reports/specification_y_d_w.md`, is:

```text
Y  = informal_rate
D  = log_real_min_wage (main); real_min_wage (robustness); min_wage_growth (exploratory)
W  = unemployment_rate + labour_productivity + trained_labour_rate + log_employed_persons
Unit = province-year, 2018-2024, N = 441
```

`min_wage_growth` is excluded from the main treatment family on pre-specified empirical grounds: its variation is almost entirely absorbed by year effects (Section 3.3), its TWFE estimate is insignificant (p = 0.766), and its DML estimates are sign-unstable (only 56 percent of cross-fitting sweep runs are negative, and all main-run confidence intervals include zero).

### 4.2 Baseline linear models

The linear benchmark family estimates, for one treatment at a time:

```text
informal_rate_it = beta * D_it + gamma' W_it + alpha_i + delta_t + e_it
```

in four nested variants: pooled OLS (no fixed effects), year FE only, province FE only, and TWFE (both). All standard errors are clustered by province. TWFE is treated as the main linear panel benchmark, not as causal proof.

### 4.3 DML

DML uses the partialling-out estimator: nuisance functions g(W) = E[Y|W] and m(W) = E[D|W] are estimated by machine learners with K-fold cross-fitting, and theta is estimated from the residual-on-residual regression. The main DML specification includes the four controls plus year dummies in W, but no province dummies, and is evaluated for stability across three learners (ridge, random forest, gradient boosting), three seeds (42, 123, 2024), fold-level estimates, and K in {2, 5, 10}. Inference uses cluster-robust (by province) standard errors based on the influence function. A second variant adds the 62 province dummies to W, making the DML nuisance structure comparable to TWFE; comparing the two variants is our test of whether DML-TWFE disagreement is about functional form or variation source.

### 4.4 CRF

Causal Forest DML (`econml.dml.CausalForestDML`) is used strictly as exploratory heterogeneity analysis. The implementation supports a continuous treatment, uses orthogonalization consistent with the DML pipeline, and applies grouped cross-fitting by province (GroupKFold) so that no province appears in both nuisance training and evaluation folds. The main run uses 1,000 trees with a minimum leaf size of 10, random-forest nuisance models with 200 trees, and the same W as the main DML; heterogeneity features X are the four controls. Settings and interpretation constraints are documented in `reports/crf_implementation_note.md`.

## 5. Nonlinearity Evidence

Before interpreting flexible methods, we establish that the data actually exhibit nonlinearity, and we locate it.

**Raw LOWESS.** Scatterplots with LOWESS smoothing show visible curvature between `informal_rate` and `log_real_min_wage`, `unemployment_rate`, `labour_productivity`, and the employment-scale variables (`reports/figures/nonlinearity_final/`).

**Residualized LOWESS.** Raw curvature can reflect omitted controls, so we apply Frisch-Waugh residualization: Y and D are each residualized on W plus year dummies (the DML-comparable specification) and, separately, on W plus year and province dummies (the TWFE-comparable specification), and LOWESS is fit to the residuals. In the DML-like specification, curvature survives partialling-out: the LOWESS departure ratio is 0.275 for `log_real_min_wage` and 0.312 for `real_min_wage`. In the TWFE-like specification the ratios fall to 0.127 and 0.117, but this must be read together with the fact that province dummies absorb about 97 percent of the variance of D, leaving little variation from which to detect anything. As an internal validity check, the linear slope in each residualized plot exactly reproduces the corresponding panel coefficient (-48.18 for the year-FE specification; +13.33 for TWFE), confirming the residualization is correct and reproducing the sign reversal graphically.

**Formal tests.** Ramsey RESET tests (powers 2 and 3 of fitted values, cluster-robust) reject linearity in all six treatment-by-specification combinations: for `log_real_min_wage`, p = 0.000076 (pooled), 0.000066 (year FE), and 0.0035 (TWFE); for `real_min_wage`, p = 0.000036, 0.000028, and 0.0034. Wald tests on added quadratic terms locate the nonlinearity: squared-treatment terms alone are never significant (p between 0.20 and 0.55), while squared-control terms are jointly significant in the pooled and year-FE specifications (p between 0.0018 and 0.0072). In the TWFE specification the squared-control block loses significance (p ≈ 0.79), indicating that province effects absorb part of the nonlinear structure, though RESET still rejects.

**Predictive diagnostics.** Consistent with the tests, flexible learners fit the outcome substantially better than a linear model (RMSE 5.62-5.66 versus 7.37; R² 0.81 versus 0.67), and partial dependence plots for the treatment are curved and non-monotonic (range 1.8 percentage points for random forest, 4.2 for gradient boosting). Permutation importance attributes most predictive power to `labour_productivity` (0.78-0.85) rather than the treatment (0.02-0.05), which is expected given that treatment variation is coarse (four wage regions), and which reinforces that these are prediction diagnostics, not effect estimates.

**Reading.** The nonlinearity is real, statistically detectable, and concentrated in the nuisance relationship between W and Y rather than in a curved D-Y treatment relationship. This is precisely the setting in which DML is well-motivated as a robustness check — it learns g(W) and m(W) flexibly — and it is not a setting in which nonlinearity by itself would explain a sign difference between DML and TWFE.

## 6. Baseline Results

The baseline results show a clear sign reversal across fixed-effect structures. For `log_real_min_wage` (cluster-robust p-values in parentheses):

| Model | Estimate | p-value | Variation used |
|---|---:|---:|---|
| Pooled OLS + W | -44.84 | 0.0035 | between + within |
| Year FE + W | -48.18 | 0.0039 | between, net of common shocks |
| Province FE + W | +13.91 | 0.0034 | within-province |
| TWFE + W | +13.33 | 0.0375 | within-province, net of common shocks |

For `real_min_wage` the pattern is identical in sign and significance (pooled -1.38e-05, p = 0.0044; year FE -1.49e-05, p = 0.0047; province FE +3.93e-06, p = 0.0062; TWFE +3.69e-06, p = 0.0481). For `min_wage_growth`, the TWFE estimate is -18.15 with p = 0.766: no reliable evidence.

The negative pooled and year-FE estimates rely on between-province comparisons: provinces in higher wage regions have systematically lower informal employment conditional on W. The positive province-FE and TWFE estimates use only within-province changes over time. Given that within-province treatment variation is roughly 5 percent of the total (Section 3.3), the within estimates are identified from a thin margin, and the between estimates are exposed to any province-level confounding not captured by W (urbanization, industrial structure, enforcement, migration). Neither is automatically the causal answer; the reversal itself is the empirically robust fact, and it indicates that time-invariant province heterogeneity is central to this setting.

## 7. DML Results

### 7.1 Main specification (W + year dummies)

The main DML estimate for `log_real_min_wage` is negative and relatively stable. The mean theta across the nine main runs (3 learners × 3 seeds, K = 5) is -33.34, with an average cluster-robust p-value of 0.029. Stability evidence: 9 of 9 main runs are negative; 44 of 45 fold-level estimates are negative; and re-running the full grid at K = 2, 5, and 10 yields negative point estimates in 100 percent of the 27 runs per treatment, with learner-level means essentially unchanged across K (ridge: -51.0, -49.7, -49.5). The level treatment `real_min_wage` shows the same pattern (mean -1.01e-05; 9/9 negative; 100 percent negative across the K sweep; average p = 0.033).

In magnitude terms, theta ≈ -33 implies that a 10 percent higher real minimum wage is associated with roughly 3.3 percentage points lower informal employment in this specification. Two qualifications are mandatory. First, "relatively stable" is the correct description, not "converged": confidence intervals still include zero in 22 percent of main runs for the log treatment (33 percent for the level treatment), concentrated in the gradient-boosting learner, and the magnitude depends on the learner (ridge around -50, gradient boosting around -6 to -8 for the log treatment). Second, this is a specification-conditional association, not a causal effect.

For `min_wage_growth`, DML is unstable in every dimension examined (89 percent of main runs negative but only 56 percent across the K sweep; all main confidence intervals include zero; average p = 0.38), confirming its exploratory status.

### 7.2 Province-dummies variant

The most consequential result of the enhanced analysis is the DML variant that adds province dummies to the nuisance functions. For `log_real_min_wage`, the mean theta collapses to -1.87, the range across learners and seeds spans [-14.63, +14.09] with signs flipping across learners (ridge turns positive, matching TWFE; tree-based learners stay mildly negative), the average p-value rises to 0.31, and confidence intervals include zero in 78 percent of runs. The level treatment behaves identically (89 percent of CIs include zero).

The interpretation is sharp: the stable negative main DML signal is carried by between-province variation. Once province heterogeneity is absorbed, too little treatment variation remains for any learner to estimate a reliable effect. The disagreement between main DML and TWFE is therefore driven by the source of identifying variation and province heterogeneity — not by DML's ability to model nonlinearity. This finding disciplines the narrative: it would be incorrect to present DML as "correcting" TWFE.

## 8. CRF Results

CRF is reported as exploratory heterogeneity analysis. For `log_real_min_wage`, the main run (seed 42) yields an average marginal effect (ATE) of -17.2 with a 95 percent confidence interval of [-37.8, +3.4]; 96 percent of observation-level CATEs are negative, but only 29 percent of individual CATE intervals exclude zero. Across five seeds and light tuning (twelve runs in total), every ATE is negative — consistent in direction with the main DML — but the magnitude is seed-sensitive, ranging from -17.2 to -1.9, and confidence intervals include zero in all seed runs at the main leaf size. We report the full seed grid (`reports/tables/crf_stability_by_seed.csv`) and do not select favorable runs. The level treatment behaves analogously (ATE -4.9e-06, CI [-1.14e-05, +1.7e-06], 93 percent of CATEs negative). For `min_wage_growth`, the CRF interval is enormous ([-1971, +2077]) and the CATE distribution is centered on zero, closing the case for treating it as exploratory only.

The exploratory heterogeneity cuts show an economically coherent gradient: the negative association is stronger in less-developed provinces. Mean CATEs by tercile are -20.0 (low) versus -13.9 (high) for labour productivity, -21.1 versus -12.1 for unemployment, and -18.3 versus -12.2 for trained labour rate. By wage region, Region IV is weakest (-7.8) while Regions I-III are similar (-17.6 to -19.3); this cut is reported with the explicit caveat that wage region nearly coincides with treatment intensity itself, so it is descriptive only. With 441 observations, individual CATEs are noisy and only group-level patterns are read.

CRF thus supports the qualitative direction of the main DML while inheriting its identification limits: the main CRF run, like the main DML, uses controls and year dummies without province indicators, and therefore also leans on between-province variation.

## 9. Method Comparison

The methods are best organized by the variation they exploit, not ranked by sophistication. For `log_real_min_wage`:

| Method | Estimate | Sign | Variation used | Role |
|---|---:|:---:|---|---|
| Pooled OLS + W | -44.84 | − | between + within | descriptive baseline |
| Year FE + W | -48.18 | − | between, net of shocks | baseline |
| Province FE + W | +13.91 | + | within-province | baseline |
| TWFE + W | +13.33 | + | within, net of shocks | main linear benchmark |
| DML (W + year) | -33.34 | − | between (flexible controls) | flexible-control robustness |
| DML (+ province dummies) | -1.87 | mixed | within (flexible controls) | TWFE-comparable sensitivity |
| CRF (median across seeds) | -7.86 | − | between (flexible controls) | exploratory heterogeneity |

Three consistent lessons emerge. First, every negative estimate comes from a specification that leans on between-province variation, and every positive estimate from one that absorbs it; the flexible methods obey the same logic as the linear ones. Second, DML earns its place not by overturning TWFE but by (i) guarding the between-province estimates against nonlinear confounding in W — which Section 5 showed is real — and (ii) revealing, through the province-dummies variant, that the between/within split rather than functional form drives the disagreement. Third, no method here is "better" in a causal sense; they answer different questions from different variation, and with 95 percent of treatment variance between provinces and seven time periods, the data cannot adjudicate between the between- and within-province stories. The canonical machine-readable version of this comparison, including the level and growth treatments and Vietnamese-language interpretations, is `reports/tables/method_comparison_summary.csv`; detailed run-level grids remain in the reproducibility tables and are not reproduced in the body.

## 10. Limitations

The limitations are documented in full in `reports/limitations_section.md` and summarized here.

The data are aggregate province-year observations rather than worker-level microdata, so the analysis cannot observe individual transitions between formal work, informal work, self-employment, unemployment, and inactivity; compositional channels are invisible. There is no clean untreated control group, since the regional minimum wage applies nationwide with varying intensity, which is why binary DiD and event-study designs were evaluated and rejected as the primary strategy. Treatment is measured with error: wage regions are assigned at district level, while our exposure is mapped at province level, and for provinces spanning multiple wage regions this misclassification plausibly attenuates estimates. Within-province treatment variation is thin — roughly 95 percent of variance is between provinces — which is the single most binding constraint on identification and directly explains both the baseline sign reversal and the collapse of the province-dummies DML variant. The 2018-2024 window includes COVID-era disruptions in 2020-2021 that year effects and the available controls capture only partially. DML is a robustness exercise, not identification: its stable negative signal rides on between-province variation and weakens when province heterogeneity is absorbed. CRF is exploratory: all-seed-negative direction, but seed-sensitive magnitudes and intervals that include zero. `min_wage_growth` is not a viable main treatment in this panel. Finally, the official citation and definition of `informal_rate` must be verified before submission.

Future work would benefit most from VHLSS or LFS microdata, a district-year wage-region mapping from the official decrees, district-level employment weights to build a within-province treatment-intensity measure, and pre-2018 data to enable growth-based and pre-trend designs.

## 11. Conclusion

This paper provides recent province-year evidence on regional minimum wage exposure and informal employment in Vietnam for 2018-2024, built on a validated panel and a layered, fully reproducible empirical pipeline. The core empirical fact is not a single coefficient but a structured pattern: between-province specifications consistently estimate significant negative associations between real minimum wage exposure and informality; within-province specifications estimate positive ones; flexible methods reproduce, rather than resolve, this divide. Nonlinearity is statistically detectable but concentrated in the control-outcome relationship, justifying DML as a robustness layer while ruling it out as an explanation for the sign reversal. The DML variant with province dummies pins the disagreement on province heterogeneity and thin within-province treatment variation.

The safest conclusion is the following. Regional minimum wage exposure is associated with informal employment in ways that are systematically sensitive to model specification and, more fundamentally, to the source of identifying variation. The current evidence motivates further research with richer microdata and stronger identification, but it does not establish a definitive causal effect — and the paper's contribution is to show exactly why, and along which dimension, the existing aggregate evidence falls short.

## Reproducibility Note

All results in this draft are generated by numbered scripts (`scripts/01`-`scripts/23`) from raw inputs, with intermediate validation at each stage. Figures referenced in Section 5 are in `reports/figures/`; all estimate tables are in `reports/tables/`. Environment requirements are pinned in `requirements.txt`; project seeds are 42, 123, and 2024 (plus 7 and 99 for CRF stability). See `README.md` for the exact run order.
