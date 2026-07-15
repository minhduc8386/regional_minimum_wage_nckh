# Limitations

## Main Limitations

This study has several limitations.

First, the data are aggregate province-year data rather than worker-level or firm-level microdata. The panel can document regional associations, but it cannot observe individual transitions between formal employment, informal employment, self-employment, unemployment, and inactivity.

Second, the current design does not provide a clean untreated control group. Vietnam's regional minimum wage policy applies nationally, with provinces differing by wage-region exposure and intensity. This makes classic binary Difference-in-Differences and event-study designs difficult to justify.

Third, treatment measurement is approximate. Official minimum wage regions can vary by district, while the project maps wage-region exposure at province-year level. For provinces containing districts in multiple wage regions, assigning one wage region to the whole province can introduce measurement error. This likely attenuates or distorts estimated treatment associations.

Fourth, within-province treatment variation is thin. The enhanced model outputs indicate that roughly 95% of treatment variation is between provinces or wage-region groups. When province dummies are added to DML, the theta estimate becomes weak and sign-unstable. This limits the strength of within-province causal interpretation.

Fifth, the 2018-2024 period includes COVID and post-COVID disruptions, especially 2020-2021. COVID may have affected informal employment, unemployment, labor mobility, firm behavior, and local reporting in ways not fully captured by year fixed effects or available controls.

Sixth, DML is a robustness exercise, not a stand-alone identification strategy. The main DML specification uses observed controls and year dummies, but no province dummies. When province dummies are added, the result weakens. This suggests that the stable negative main DML result should be read as flexible-control robustness using mainly between-province variation.

Seventh, CRF is exploratory. Although CRF estimates are broadly negative for `log_real_min_wage`, confidence intervals usually contain zero and magnitudes are seed-sensitive. The sample size of 441 observations is small for precise CATE estimation, so individual CATEs should not be interpreted as reliable province-level treatment effects.

Eighth, `min_wage_growth` is not a strong treatment in the current panel. It is unstable across DML learners/folds/K choices and is strongly affected by year structure. It should remain exploratory.

Ninth, the official citation and definition for `informal_rate` still need final verification. The repo identifies the raw workbook and sheet, but the final paper should cite the official data source and definition.

## Data Wishlist

The strongest future improvements would require richer data:

- VHLSS microdata to observe household/worker outcomes and informal employment definitions more directly.
- LFS microdata to study worker-level employment status, informality, hours, wages, and sector transitions.
- District-year wage-region mapping from official decrees.
- District population, labor force, or employment weights to construct weighted province-year treatment exposure.
- Longer pre-2018 wage and labor-market data to improve `min_wage_growth` and pre-trend checks.

## Bottom Line

The current evidence is valuable as a transparent province-year empirical analysis. However, the results should be interpreted as specification-sensitive associations and robustness diagnostics, not as definitive causal estimates.

