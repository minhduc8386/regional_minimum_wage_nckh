# Literature Comparison and Positioning

## Purpose

This note compares the current project's evidence with the existing minimum wage and informality literature. The comparison focuses on research design, data structure, outcome definition, and interpretation. It should not be used to compare coefficient magnitudes directly across countries or datasets.

## Main Literature Benchmarks

| Benchmark | Country/data | Main method | Relevance for this project | Key difference from current project |
|---|---|---|---|---|
| Perez Perez (2020) | Colombia, household survey and city-industry treatment intensity | DiD/RIF-DiD around an unexpected real minimum wage shock | Main academic and method benchmark for formal/informal labor markets | Stronger shock-based identification; different country, period, unit, and outcome structure |
| Nguyen Cuong Viet (2023/2025) | Vietnam Labor Force Survey, 2012-2020 | Fixed effects with local controls | Vietnam data and recent policy benchmark | Uses LFS microdata and employment/wage outcomes rather than province-year `informal_rate` |
| Del Carpio et al. | Vietnam Enterprise Survey and VHLSS, 2006/2008/2010 | OLS and fixed effects | Vietnam context benchmark for minimum wage, employment, self-employment, and welfare channels | Older data, working-paper version currently verified, not centered on province-year `informal_rate` |
| Chernozhukov et al. (2018) | General econometric methodology | Double/debiased machine learning | Method reference for flexible nuisance adjustment and cross-fitting | Does not provide minimum-wage identification by itself |

## What The Literature Suggests

The broader literature shows that minimum wages can affect several margins:

- Formal and informal wages.
- Formal employment.
- Informal employment.
- Self-employment.
- Hours worked.
- Welfare, poverty, income, and consumption.

The Vietnam literature is especially useful for showing that minimum wage changes can affect wage employment, informal contracts, self-employment, and welfare-related outcomes. The international informality literature shows that minimum wage policy can spill into informal sectors, either through compliance, labor reallocation, or reference-wage effects.

## How The Current Project Fits

The current project contributes differently from the main benchmark papers:

- It builds a recent Vietnam province-year panel for 2018-2024.
- It uses `informal_rate` as the main outcome.
- It maps regional minimum wage exposure to provinces and adjusts minimum wages by CPI.
- It reports transparent OLS/FE/TWFE baseline associations before using DML.
- It uses nonlinearity diagnostics and DML only as robustness/flexible-control analysis.

This is a cautious aggregate-data extension, not a direct replication of the stronger quasi-experimental designs in the literature.

## Comparison With Current Results

The current empirical evidence is specification-sensitive:

- Pooled OLS and year-FE specifications show a negative association between `log_real_min_wage` and `informal_rate`.
- Province-FE and TWFE specifications show a positive association.
- DML produces a stable negative theta for `log_real_min_wage`, but this differs from TWFE.

This pattern should be compared with the literature at the level of mechanisms and research design, not coefficient size.

For example, Del Carpio et al. report that minimum wage changes can reduce wage employment and increase self-employment in Vietnam. That mechanism is consistent with the possibility that minimum wage policy may affect informal labor-market margins. However, the current project uses a different outcome, period, and aggregate unit, so it should not claim that its coefficient directly confirms or contradicts Del Carpio et al.

Perez Perez (2020) provides a stronger identification benchmark because it uses an unexpected real minimum wage shock and treatment intensity across city-industry cells. The current project does not have an equivalent clean shock or untreated control group. Therefore, the current project should use Perez Perez (2020) mainly to justify formal/informal sector relevance, continuous treatment intensity, and careful identification discussion.

## Recommended Literature Positioning

The safest positioning is:

> This project extends the minimum wage and informality literature by constructing recent Vietnam province-year evidence on informal employment rates and by combining transparent panel baselines with nonlinearity and DML robustness diagnostics. Unlike shock-based DiD papers, the current design does not claim a clean quasi-experimental causal estimate. Instead, it documents specification-sensitive associations and shows that flexible-control methods can produce different estimates from linear TWFE baselines.

## Missing Information To Verify

Before final submission, the following items should be verified:

- The final publication status and ranking requirement for Nguyen Cuong Viet's 2025 version.
- Whether a peer-reviewed journal version of Del Carpio et al. exists; if not, cite it as an MPRA/RePEc working paper.
- The advisor's preferred citation style.
- Whether Perez Perez (2020) replication data are accessible if the project wants to include a backtest or replication extension.

## Source Files Used

- `reports/literature_review/literature_matrix_summary.md`
- `reports/literature_review/research_gap_updated.md`
- `reports/literature_review/main_paper_evaluation.md`
- `reports/literature_review/delcarpio_paper_evaluation.md`
- `reports/model_family_comparison.md`

