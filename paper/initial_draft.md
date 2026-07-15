# The Association Between Regional Minimum Wages and Informal Employment in Vietnam: Province-Year Evidence from 2018-2024

## Abstract

This paper studies the relationship between Vietnam's regional minimum wage policy and informal employment rates using a province-year panel for 2018-2024. The analysis combines informal employment outcomes, province-level exposure to regional minimum wages, CPI-adjusted real minimum wage measures, and local labor-market controls. The empirical strategy proceeds in stages: first defining outcome, treatment, and control variables; then documenting treatment variation and nonlinear diagnostic patterns; then estimating OLS, fixed-effects, and two-way fixed-effects baselines; and finally using Double/Debiased Machine Learning as a flexible-control robustness exercise. The results are specification-sensitive. Pooled and year-FE models show a negative association between log real minimum wages and informal employment, while province-FE and TWFE models show a positive association. DML estimates for log real minimum wages are stable and negative, but differ in sign from TWFE. The findings are therefore interpreted as cautious baseline and robustness evidence rather than definitive causal evidence.

## 1. Introduction

Minimum wage policy can affect labor markets through several channels. It may raise wages for covered workers, change hiring incentives for firms, affect formal employment, and shift workers across formal jobs, informal jobs, self-employment, unemployment, and inactivity. These channels are especially important in developing economies where informal employment is large and enforcement may vary across sectors and regions.

Vietnam provides a relevant setting because minimum wages are set regionally and vary across space and time. This project studies whether regional minimum wage exposure is associated with province-year informal employment rates during 2018-2024. The period is recent and includes COVID and post-COVID labor-market disruptions, making careful interpretation necessary.

The paper makes three contributions. First, it constructs a recent Vietnam province-year panel linking informal employment rates, regional minimum wage exposure, CPI-adjusted real minimum wages, and local labor-market controls. Second, it reports transparent OLS, fixed-effects, and two-way fixed-effects baseline associations before using more flexible methods. Third, it uses nonlinearity diagnostics and DML theta-stability checks as robustness evidence, while explicitly avoiding the claim that DML alone provides causal identification.

The main finding is that the estimated relationship is sensitive to specification. Pooled OLS and year-FE specifications estimate a negative association between the log real minimum wage and informal employment. Province-FE and TWFE specifications estimate a positive association. DML produces a stable negative theta for the log real minimum wage, but this result differs from the TWFE benchmark. This disagreement suggests that province heterogeneity, functional form, and flexible controls matter for interpretation.

## 2. Literature and Research Gap

The minimum wage literature studies a wide range of outcomes, including wages, employment, hours, poverty, welfare, formal employment, informal employment, and self-employment. International studies use OLS, fixed effects, Difference-in-Differences, event-study designs, border comparisons, RIF regressions, and distributional methods.

Perez Perez (2020) is a key benchmark because it studies minimum wages in formal and informal sectors using an unexpected real minimum wage shock in Colombia. The paper uses treatment intensity across city-industry cells and provides a stronger quasi-experimental benchmark than the current project can claim. Its main relevance here is methodological: it shows how formal and informal labor-market outcomes can be studied with careful treatment-intensity logic and explicit identification assumptions.

Vietnam studies are also important. Del Carpio et al. study minimum wages, employment, wages, and welfare in Vietnam using enterprise and household survey data from 2006, 2008, and 2010. Nguyen Cuong Viet studies more recent Vietnam Labor Force Survey data from 2012 to 2020. These papers provide important Vietnam context and fixed-effects benchmarks, but they do not use the exact province-year `informal_rate` outcome for 2018-2024.

The current project therefore fills a narrower gap. It provides recent aggregate evidence on province-year informal employment rates in Vietnam, combines transparent panel baselines with nonlinearity diagnostics, and uses DML only as a flexible-control robustness check.

## 3. Data

The analysis uses a balanced province-year panel for Vietnam from 2018 to 2024. The current panel contains 441 observations, covering 63 provinces over 7 years. There are no duplicate province-year rows and no missing values in the final analysis panel.

The outcome variable is:

- `informal_rate`: informal employment rate.

The main treatment variable is:

- `log_real_min_wage`: log CPI-adjusted regional minimum wage.

The secondary treatment variables are:

- `real_min_wage`: CPI-adjusted regional minimum wage in level form.
- `min_wage_growth`: growth rate of real minimum wage by wage region.

The main controls are:

- `unemployment_rate`
- `labour_productivity`
- `trained_labour_rate`
- `log_employed_persons`

The level employment variable, `employed_persons`, is used only as a robustness control because it should not be included simultaneously with `log_employed_persons`.

## 4. Empirical Strategy

The empirical strategy follows a staged structure.

First, the analysis validates the province-year panel, treatment variation, missing values, and duplicate keys. Second, it uses LOWESS diagnostics and predictive model comparisons to check whether the relationship between informal employment, treatment variables, and controls appears nonlinear. Third, it estimates baseline OLS, province-FE, year-FE, and TWFE models with province-clustered standard errors. Fourth, it uses DML partialling-out as a robustness exercise for flexible nuisance adjustment.

The main linear panel benchmark is the TWFE specification with province and year fixed effects. This model controls for time-invariant province differences and common national year shocks. However, it remains a linear additive baseline and should not be treated as definitive causal proof.

DML is used only after the baseline models. It is motivated by the nonlinearity diagnostics, which show visible curvature for `log_real_min_wage` and several controls. The DML results are interpreted as robustness evidence about flexible control functions, not as a replacement for identification.

## 5. Results

The baseline results are specification-sensitive. In pooled OLS and year-FE specifications, `log_real_min_wage` is negatively associated with `informal_rate`. In province-FE and TWFE specifications, the association becomes positive.

The TWFE coefficient for `log_real_min_wage` is approximately `13.33`, with a p-value around `0.0375`. This suggests a positive within-province association after controlling for common year shocks. However, this should still be interpreted cautiously because treatment assignment is not quasi-random and the model imposes a linear functional form.

The DML robustness results point in a different direction. For `log_real_min_wage`, the mean DML theta is approximately `-33.34`, with stable negative signs across learners, seeds, and most cross-fitting folds. This is the most coherent DML result. However, because it differs in sign from TWFE, it should be interpreted as evidence that the results are sensitive to flexible control choices rather than as definitive evidence of a negative causal effect.

The growth treatment, `min_wage_growth`, is weaker. Its TWFE estimate is statistically insignificant, and its DML theta is unstable across folds. It should therefore be treated as exploratory rather than a main treatment.

## 6. Discussion

The current evidence suggests that the relationship between regional minimum wage exposure and informal employment is complex. Cross-sectional and within-province comparisons tell different stories. Flexible-control DML also differs from the linear TWFE benchmark. These patterns imply that a single linear coefficient is unlikely to summarize the relationship fully.

The most defensible interpretation is not that one model has proven the causal effect. Rather, the evidence shows that baseline associations are sensitive to province heterogeneity, year shocks, and functional-form choices. This is still useful for research because it clarifies where the identification and modeling challenges are.

## 7. Limitations

The study has several limitations. The data are aggregate province-year data, not worker-level or firm-level microdata. The design does not have a clean untreated control group because all provinces are exposed to Vietnam's regional minimum wage policy. Treatment assignment is approximated at the province level, even though minimum wage regions may vary at more detailed administrative levels.

The sample is also small for machine-learning-based causal estimation. The current DML implementation does not fully include province fixed effects in the nuisance functions and uses row-level rather than province-grouped cross-fitting. These choices limit causal interpretation.

Finally, the results are specification-sensitive. TWFE and DML estimates for `log_real_min_wage` differ in sign. This disagreement should be presented directly as a limitation and as motivation for future work with stronger identification or richer microdata.

## 8. Conclusion

This paper provides recent province-year evidence on the association between regional minimum wages and informal employment in Vietnam from 2018 to 2024. The analysis shows that OLS, FE, TWFE, and DML do not produce a single unambiguous conclusion. Instead, the results are sensitive to model specification and functional form.

The preferred reporting approach is therefore cautious. TWFE should be presented as the main linear panel benchmark, while DML should be presented as a flexible-control robustness exercise. The paper should not claim a definitive causal effect. Its contribution is to build a transparent data and modeling pipeline, document specification sensitivity, and identify the limitations that future causal work must address.

## Items Still Needed Before Final Submission

- Final citation formatting and bibliography.
- A precise data-source citation for `informal_rate`.
- A clearer note on how province-level wage-region mapping handles district-level minimum wage variation.
- Final verification of the publication status of key Vietnam benchmark papers.
- Optional robustness improvement: province-grouped cross-fitting for DML.

