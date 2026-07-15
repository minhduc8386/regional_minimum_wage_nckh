# Our Approach vs Previous Studies

## Purpose

This section positions the current project relative to three main literature benchmarks. The goal is not to compare coefficient magnitudes directly. The goal is to explain what the project learns from prior studies and what its own contribution is.

## Comparison Table

| Dimension | Perez Perez (2020) | Del Carpio et al. | Nguyen Viet Cuong | Our project |
|---|---|---|---|---|
| Country/context | Colombia | Vietnam | Vietnam | Vietnam |
| Period | 1996-2000 | 2006, 2008, 2010 | 2012-2020 | 2018-2024 |
| Data | Household survey, city-industry cells | Enterprise Survey and VHLSS | Labor Force Survey | Province-year aggregate panel |
| Main outcome | Formal/informal wages and employment | Employment, wages, welfare, self-employment | Employment, earnings, hours | `informal_rate` |
| Treatment | Minimum wage incidence around inflation shock | Minimum wage changes / exposure | Regional/district minimum wage variation | CPI-adjusted regional minimum wage exposure |
| Identification | Shock-based DiD/RIF-DiD | OLS and fixed effects | Fixed effects | OLS/FE/TWFE baseline + DML/CRF diagnostics |
| Strength | Stronger quasi-experimental benchmark | Vietnam policy context and mechanisms | Recent Vietnam labor-market benchmark | Recent province-year informality focus |
| Limitation relative to our goal | Different country, older period, different unit | Older data; not centered on province-year `informal_rate` | Not centered on province-year `informal_rate` | Aggregate data; no clean untreated group; treatment mapping approximation |
| How we use it | Learn treatment-intensity and formal/informal framing | Learn Vietnam minimum-wage mechanisms | Learn recent Vietnam FE approach | Build cautious updated evidence |

## Interpretation

Perez Perez (2020) is the strongest method benchmark because it uses an unexpected real minimum wage shock and treatment intensity across city-industry cells. The current project should not compare its coefficient magnitude directly with Colombia because the country, period, unit of observation, treatment construction, and identification design are different.

Del Carpio et al. is useful as a Vietnam context benchmark. It shows that minimum wage changes in Vietnam can affect wage employment, self-employment, wages, and welfare channels. The current project should use it to motivate mechanisms, not to claim direct coefficient comparability.

Nguyen Viet Cuong is useful as a recent Vietnam data and fixed-effects benchmark. It is closer in period and policy context, but the current project differs by centering `informal_rate` in a province-year panel and adding flexible diagnostic methods.

## Contribution Of The Current Project

The contribution is:

1. A recent Vietnam province-year panel for 2018-2024.
2. Direct focus on province-year informal employment rate.
3. Clear Y-D-W specification.
4. Nonlinearity diagnostics before flexible methods.
5. Baseline OLS/FE/TWFE before DML and CRF.
6. DML and CRF used as robustness/diagnostic tools, not as substitutes for identification.

## Suggested Paper Paragraph

Relative to prior work, this project contributes recent aggregate evidence on Vietnam's regional minimum wage exposure and province-year informal employment rates. Perez Perez (2020) provides the closest formal/informal-sector method benchmark, but its shock-based Colombian design should not be compared directly with the current estimates. Vietnam studies such as Del Carpio et al. and Nguyen Viet Cuong provide important policy and fixed-effects context, but they do not center the same province-year `informal_rate` outcome for 2018-2024. The contribution of this project is therefore a cautious empirical extension: it documents recent Vietnam patterns, tests for nonlinear nuisance relationships, and compares transparent panel baselines with DML and CRF diagnostics.

## Source Files Used

- `reports/literature_review/main_paper_evaluation.md`
- `reports/literature_review/delcarpio_paper_evaluation.md`
- `reports/literature_review/literature_matrix_summary.md`
- `reports/literature_review/research_gap_updated.md`

