# Main Paper Evaluation: Pérez Pérez (2020)

## 1. Paper information

- Title: "The Minimum Wage in Formal and Informal Sectors: Evidence from an Inflation Shock"
- Author: Jorge Pérez Pérez
- Year: 2020
- Journal: World Development, volume 133, article 104999
- DOI: https://doi.org/10.1016/j.worlddev.2020.104999
- Drafting source: local PDF/OCR copy was used during review, but the repo should cite the public DOI/source rather than commit the source paper file.
- Online sources checked: author page, IDEAS/RePEc, Universidad del Rosario publication page, SCImago/Scopus-based journal ranking pages

## 2. Paper type and ranking

Paper type: peer-reviewed journal article.

The paper is published in World Development by Elsevier. IDEAS/RePEc lists it as World Development, volume 133, with DOI `10.1016/j.worlddev.2020.104999`. The author page also lists it as published in World Development and links to replication files.

Journal/Q ranking: World Development is currently listed as a Q1 journal in SCImago/Scopus-based rankings for development/economics-related categories. For the final manuscript, the Q ranking should be verified one more time through the university library, SCImago, Scopus, or the advisor's required ranking system, because Q labels can vary by year and category.

## 3. Data

- Dataset name: Colombia National Household Survey (Encuesta Nacional de Hogares, ENH).
- Country: Colombia.
- Period: 1996-2000, with the empirical design centered on the unexpected real minimum wage shock in 1999.
- Frequency: quarterly rotating cross-sections.
- Unit of observation: individual workers for wage regressions; city-industry blocks for treatment intensity and employment specifications.
- Geography: 7 cities present in all quarters with sufficient sample size: Barranquilla, Bogotá, Bucaramanga, Cali, Manizales, Medellín and Pasto.
- Additional data: monthly minimum wage from Colombia's Central Bank, city-level CPI from DANE, state-level financial sector GDP from DANE, transportation subsidy information from the Colombian Institute of Tax Law.
- Sample restrictions: wage analysis focuses on occupied workers in private/government sectors, excludes unpaid family workers, self-employed workers, business owners and domestic workers, keeps workers aged 12-65 who report wages and work 30-50 hours per week.
- Formal/informal definition: formal workers are those covered by employer-provided health insurance; informal workers are those without that coverage. The paper discusses possible misclassification in some 1996 quarters.
- Replication data/code: the author's website links to a Harvard Dataverse replication package; direct access still needs manual verification/download.

## 4. Variables: Y, D, W

Main outcomes Y:

- Formal wage distribution, especially unconditional quantiles near the minimum wage.
- Informal wage distribution.
- Formal employment and hours worked.
- Informal employment and hours worked.

Treatment D:

- Minimum wage incidence at the city-industry block level.
- Main incidence measure: fraction of workers whose real wage before the change lies between the old and new minimum wage.
- Alternative measures: fraction at/near the minimum wage, minimum-to-median ratio, violation index.
- Shock timing: post-1998q4 indicator around the 1999 unexpected real minimum wage increase.

Controls W:

- City-industry fixed effects.
- Time fixed effects.
- City-specific trends.
- Industry trends in some specifications.
- Local labor demand shocks, including Bartik price/quantity shocks.
- Local financial sector GDP to address differential exposure to the financial crisis.

Treatment unit:

- City-industry blocks.

Time unit:

- Quarter.

## 5. Method

The paper combines a Difference-in-Differences design with unconditional quantile regression/RIF regression.

Core logic:

- The 1999 inflation forecast error made the real minimum wage rise unexpectedly.
- The national shock affected city-industry blocks differently depending on how many workers were near the old/new minimum wage before the change.
- The key treatment is therefore continuous treatment intensity: minimum wage incidence by city-industry block.
- For wages, the paper estimates RIF regressions to study effects on unconditional wage quantiles.
- For employment, the paper uses a standard DiD-style specification with log employment or hours as outcomes.

Identification:

- The design compares high-incidence versus low-incidence city-industry blocks before and after the shock.
- The key identifying assumption is that blocks with different minimum wage incidence were not differentially affected by the 1999 financial crisis in ways correlated with the outcomes.
- The paper addresses this with city-specific trends, local labor demand controls and local financial sector GDP.

Inference:

- The paper reports clustered standard errors in tables and uses wild bootstrap-t procedures in several checks, especially because treatment variation is at grouped city/industry levels.

## 6. Main results

The main findings are:

- Wages close to the minimum wage respond to the shock.
- The wage response appears in both formal and informal sectors.
- The response is larger in the formal sector: around 3 percent higher formal wages near the minimum wage for a 10 percentage point higher minimum wage incidence.
- The informal wage response is smaller, around 1 to 1.3 percent near the minimum wage.
- The implied effects are smaller than full compliance, suggesting partial compliance and possible "lighthouse" or reference-wage effects.
- The paper finds slight negative employment effects in the informal sector, but not in the formal sector.
- Cross-sectoral tests suggest the informal-sector effects are not mainly driven by spillovers from the formal sector.

These results are useful for the project, but they should not be used to predict the magnitude for Vietnam because Colombia's institutions, shock source, informality definition and period are different.

## 7. Limitations

- The context is Colombia, not Vietnam.
- The identifying shock is an inflation forecast error in 1999; Vietnam's regional minimum wage changes are different policy processes.
- The minimum wage shock happened during a financial crisis, so identification depends on the assumption that high- and low-incidence city-industry blocks were not differentially affected by the crisis after controls.
- The paper's formal/informal definition is based on employer-provided health insurance, while Vietnam's informal employment measures may follow different labor-statistics definitions.
- The empirical unit and treatment are city-industry blocks, not province-year units.
- Results may not generalize to larger minimum wage changes, other countries, or periods with different enforcement.
- The method is DiD/RIF-DiD, not DML.

## 8. What we learn

The project can learn five concrete lessons:

- Define formal/informal status explicitly and discuss measurement limitations.
- Treat minimum wage exposure as intensity, not only as a binary treatment, when all units are affected by the policy to different degrees.
- Use a policy/institutional shock carefully, and state the identifying assumption clearly.
- Control for time-varying local shocks when a macro shock overlaps with the policy change.
- Present limitations directly instead of overstating causal certainty.

## 9. How our project extends this paper

Our project extends this literature in a cautious way:

- Country: Vietnam instead of Colombia.
- Period: 2018-2024 province-year panel, a more recent period including COVID/post-COVID years and recent regional minimum wage updates.
- Outcome: `informal_rate` at province-year level, rather than individual wage distributions by formal/informal status.
- Treatment: `real_min_wage`, `log_real_min_wage`, and `min_wage_growth`, mapped to province-year regional minimum wage exposure.
- Baseline: OLS, province FE, year FE and two-way FE before any DML.
- Diagnostic: LOWESS and predictive comparison are used only to motivate flexible controls, not as causal evidence.
- DML: used only as robustness/flexible-control extension to examine theta stability after controlling for nonlinear nuisance relationships.

The project should not say DML replaces the DiD/RIF-DiD identification in Pérez Pérez (2020). A safer statement is: DML can be a supplementary robustness exercise if replication data are accessible and if the original identification logic is preserved.

## 10. Backtest feasibility

Backtest is conceptually feasible if the Harvard Dataverse replication package can be downloaded and contains usable data/code.

Possible backtest pipeline:

- Reproduce the paper's core DiD/RIF-DiD results first.
- Define Y/D/W in the replication data.
- Visualize nonlinear relationships between outcomes, minimum wage incidence and controls.
- Run DML partialling-out as a robustness extension, not as a replacement for the original design.
- Compare DML theta stability with the original DiD estimates.

Current status: replication package is linked from the author's website, but local download/access has not yet been completed. The backtest should therefore be marked as feasible in principle, pending replication-data access.
