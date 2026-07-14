# Literature Matrix Summary

## 1. Overview

The updated matrix includes 12 papers/references covering four groups:

- Vietnam minimum wage studies.
- Minimum wage and informality in developing countries.
- Distributional/event-study minimum wage studies.
- DML/causal ML methodology.

The selected main paper is Pérez Pérez (2020), because it combines minimum wage, formal/informal sectors, a clear shock-based identification strategy and a Q-ranked journal outlet. Nguyen Cuong Viet (2023/2025) is kept as the Vietnam data/method benchmark, while Del Carpio et al. is kept as the Vietnam context benchmark.

## 2. What previous studies have done

Vietnam minimum wage studies:

- Del Carpio et al. study employment, wages and welfare in Vietnam using Vietnam Enterprise Survey and VHLSS data from 2006, 2008 and 2010.
- Nguyen Cuong Viet studies Vietnam minimum wage effects using annual Labor Force Surveys from 2012 to 2020 and regional/district minimum wage variation.
- These studies provide useful fixed effects and Vietnam policy-context benchmarks, but they do not use the current project's exact outcome: `informal_rate` in a province-year panel from 2018 to 2024.

Minimum wage and informality in developing countries:

- Pérez Pérez (2020) directly estimates effects on formal and informal wages/employment in Colombia.
- Comola and de Mello (2009) study decentralized minimum wage setting, formal employment and informality in Indonesia.
- Lemos (2009), Dinkelman and Ranchhod (2012), Hohberg and Lay (2015), and Maloney and Nunez (2004) show that in developing countries, minimum wages can affect informal wages, informal employment, formal/informal allocation or wage distributions.

Distributional and event-study studies:

- Card and Krueger (1994), Dube et al. (2010), and Cengiz et al. (2019) show why credible comparison groups, local controls and event-style diagnostics matter in minimum-wage research.
- These studies are mostly developed-country benchmarks, so they are method references rather than direct Vietnam comparisons.

DML / causal ML methodology:

- Chernozhukov et al. (2018) provides the theoretical basis for DML, cross-fitting and orthogonal scores.
- The DML paper is methodological. It does not solve identification problems by itself and should not be cited as evidence that machine learning proves a causal effect.

## 3. Common data sources

Common data sources in the literature include:

- Labor Force Survey or household labor survey data.
- Household living standards surveys.
- Enterprise or firm surveys.
- Administrative minimum wage decree data.
- CPI/inflation data for real minimum wage construction.
- Local economic controls such as GDP, local demand shocks or industry employment shares.

The current project uses a province-year panel for Vietnam from 2018 to 2024, combining informal employment data, regional minimum wage policy data and CPI adjustment.

## 4. Common methods

Common methods include:

- OLS and fixed effects.
- Province/district/firm fixed effects.
- Difference-in-Differences and event-study logic.
- Border-pair comparisons.
- Distributional/bunching methods.
- Quantile and RIF/unconditional quantile regression.
- DML/causal ML for flexible nuisance adjustment.

The appropriate sequence for the current project is therefore:

1. Define Y, D and W clearly.
2. Visualize nonlinearity.
3. Run OLS/FE/TWFE baseline.
4. Check whether DiD/Event Study is feasible.
5. Use DML only as a robustness/flexible-control exercise after baseline.

## 5. Research gap for our project

The research gap is not simply "we use DML." The stronger and safer gap is:

- Recent Vietnam province-year evidence on `informal_rate` is still limited.
- Existing Vietnam studies often use older VHLSS/enterprise data or LFS microdata, while the current project builds a 2018-2024 province-year panel.
- Many studies examine employment, wages, hours or welfare; fewer directly center informal employment rate at the province-year level.
- Minimum wage effects may be nonlinear through unemployment, productivity, training and employment scale, so the project first documents nonlinearity before using DML.
- The project explicitly acknowledges that DiD/Event Study is not clean with the current data because treatment is continuous and all provinces are exposed to the policy.

Thus, the contribution is a cautious empirical extension: a recent Vietnam province-year panel, transparent baseline models, identification feasibility checks and DML theta-stability diagnostics as robustness rather than as standalone causal proof.
