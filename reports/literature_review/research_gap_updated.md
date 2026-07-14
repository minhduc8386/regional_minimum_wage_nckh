# Updated Research Gap

## 1. What previous studies have done

The minimum wage literature has studied many outcomes: employment, wages, working hours, wage distributions, poverty, household welfare, formal employment, informal employment and self-employment.

Internationally, papers use OLS, fixed effects, Difference-in-Differences, event studies, border comparisons, RIF/unconditional quantile regressions and distributional approaches. Pérez Pérez (2020) is especially close to our topic because it studies minimum wage effects in formal and informal sectors using an inflation shock in Colombia.

In Vietnam, Del Carpio et al. study minimum wage effects on employment, wages and welfare using Vietnam Enterprise Survey and VHLSS data from 2006, 2008 and 2010. Nguyen Cuong Viet studies more recent Vietnam Labor Force Survey data from 2012 to 2020, with outcomes such as employment, monthly earnings, working hours and hourly earnings.

## 2. Data gap

Many Vietnam studies use older data or microdata that may be difficult to access and replicate.

The current project builds a province-year panel for Vietnam covering 2018-2024. This period is more recent and includes years around COVID/post-COVID disruptions and recent regional minimum wage updates.

The project combines:

- Informal employment outcome data.
- Regional minimum wage policy data.
- CPI adjustment to construct real minimum wages.
- Province-year economic and labor controls.

This gives the project a clear, recent aggregate-data contribution, while still requiring caution because province-year data cannot replace worker-level microdata.

## 3. Outcome gap

Many previous papers focus on:

- Employment or wage employment.
- Monthly wages or hourly wages.
- Hours worked.
- Welfare, poverty, income and expenditure.
- Formal-sector jobs, informal contracts or self-employment.

Fewer studies focus directly on `informal_rate` as the main outcome at the province-year level in Vietnam during 2018-2024.

The project's outcome contribution is therefore:

- Outcome Y: `informal_rate`.
- Unit: province-year.
- Question: whether regional minimum wage exposure is associated with changes in informal employment rate after controlling for province/year structure and observed W variables.

## 4. Method gap

The literature mostly uses traditional econometric designs:

- OLS and fixed effects.
- Difference-in-Differences/event-study designs.
- Quantile/RIF regression.
- Border-pair comparisons.

DML is less common in the minimum wage-informality literature. However, the contribution is not just using DML. The methodological contribution is the sequence:

1. Define Y/D/W clearly.
2. Check missing values, duplicates and treatment variation.
3. Visualize scatter + LOWESS to examine possible nonlinearity.
4. Compare linear and ML prediction only as diagnostic evidence.
5. Run OLS/FE/TWFE baseline before DML.
6. Evaluate DiD/Event Study feasibility before claiming any causal design.
7. Run DML theta stability only as robustness/flexible-control analysis.

This sequence is important because DML should be motivated by nonlinear nuisance relationships, not by predictive RMSE alone.

## 5. Identification concern

The current data do not provide a clean classic DiD/Event Study design.

Key reasons:

- Treatment is continuous: `real_min_wage`, `log_real_min_wage`, and `min_wage_growth`.
- All provinces are exposed to Vietnam's regional minimum wage policy; they differ mainly by wage region and intensity.
- There is no clean untreated control group.
- The panel starts in 2018, so pre-period length is limited for some possible policy shocks.
- Wage region mapping is a province-level approximation, while actual minimum wage regions can vary by district-level administrative units.

Therefore, the project does not claim that DML alone identifies a causal effect. Identification remains a limitation unless stronger exogenous variation, a cleaner control group, or microdata with policy thresholds becomes available.

## 6. Our contribution

The project contributes by:

- Building a Vietnam province-year panel for 2018-2024.
- Combining informal employment data, minimum wage policy data and CPI adjustment.
- Constructing real minimum wage variables: `real_min_wage`, `log_real_min_wage`, and `min_wage_growth`.
- Using `informal_rate` as the main outcome.
- Running nonlinearity diagnostics before choosing flexible methods.
- Running baseline OLS/FE/TWFE before DML.
- Checking DiD/Event Study feasibility and explicitly stating why classic DiD is weak for the current data.
- Running DML theta-stability diagnostics after baseline, reporting theta, standard error, p-value, confidence interval and stability by learner/seed/fold.
- Positioning DML as robustness/flexible-control analysis, not as a replacement for research design.

## 7. Cautious positioning

The safest positioning is:

This project studies whether Vietnam's regional minimum wage exposure is associated with province-year informal employment rates after controlling for observed economic and labor-market factors, province/year structure and nonlinear nuisance relationships.

This project does not claim that DML alone identifies a causal effect. Instead, DML is used to examine whether the estimated treatment parameter remains stable after flexibly controlling for nonlinear nuisance relationships.

Any causal interpretation must remain cautious because the current data are aggregate province-year data, treatment assignment is approximated at province level, and classic DiD/Event Study identification is not clean.
