# Backtest Feasibility: Pérez Pérez (2020)

## 1. Dataset used by the paper

Pérez Pérez (2020) uses Colombia's National Household Survey (ENH) for 1996-2000, centered on the unexpected real minimum wage increase in 1999.

Main data features:

- Country: Colombia.
- Survey: National Household Survey (ENH).
- Period: 1996q2-2000q2 in the working paper/local text; the design focuses on the 1999 shock.
- Geography: 7 cities with consistent quarterly coverage and sufficient sample sizes.
- Unit: individual workers for wage analysis; city-industry blocks for treatment intensity and employment cells.
- Formal/informal definition: employer-provided health insurance coverage.
- Treatment: minimum wage incidence at city-industry block level.
- Identification shock: nominal minimum wage was set using expected inflation, but actual inflation in 1999 was lower, producing an unexpected real minimum wage increase.

## 2. Replication files

The author's website links to "Replication Files" on Harvard Dataverse:

- Author page: https://jorgeperezperez.com/research/2019-04-15-minimum-wages-formal-informal
- Dataverse DOI shown in the link: `10.7910/DVN/15E3RK`

Current status:

- Replication package appears to exist.
- Direct local access/download has not yet been completed in this repo.
- Browser access to Dataverse may require JavaScript/manual download steps.

Therefore, mark replication access as: pending download/manual verification.

## 3. Can we apply our pipeline?

Yes, conceptually, if the replication package contains usable data and code.

However:

- The pipeline should first reproduce the original paper's DiD/RIF-DiD results.
- DML should be added only as a robustness/flexible-control extension.
- The Colombia results should not be compared directly in magnitude with Vietnam results.
- The DML extension should preserve the original paper's identification logic rather than replacing it.

## 4. Proposed pipeline

If replication files are accessible:

1. Download and inspect the replication package.
2. Identify raw data, processed data, code language and construction scripts.
3. Reproduce the baseline DiD/RIF-DiD tables or at least the main wage/employment estimates.
4. Define Y:
   - Formal wage quantiles or employment.
   - Informal wage quantiles or employment.
5. Define D:
   - Minimum wage incidence by city-industry block.
6. Define W:
   - City-industry fixed effects.
   - Time fixed effects.
   - City trends.
   - Bartik/local labor demand shocks.
   - Local financial sector GDP.
7. Visualize possible nonlinear relationships between outcomes, treatment intensity and controls.
8. Run DML partialling-out as a robustness extension.
9. Report theta, standard error, p-value, confidence interval and theta stability by fold/learner/seed.
10. Compare DML theta direction/stability with the original DiD estimates, without claiming DML supersedes the paper's design.

## 5. Feasibility conclusion

Backtest is feasible in principle because the paper has a clear identification design, explicit Y/D/W structure and a linked replication package.

The current blocker is practical, not conceptual: the replication files must be downloaded and inspected first. Until then, the status should be:

"Feasible pending replication-data access. DML can be tested only as a robustness/flexible-control extension after reproducing the original DiD/RIF-DiD logic."
