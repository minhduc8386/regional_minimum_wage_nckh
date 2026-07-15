"""Tasks 11+12 (cr7.xlsx): Causal Random Forest via econml CausalForestDML.

Task 11: main treatments log_real_min_wage (first), real_min_wage.
Task 12: min_wage_growth, exploratory only.

Framing: exploratory heterogeneity analysis under selection-on-observables.
ATE here = average marginal effect of a one-unit change in T (continuous).

usage: python 20_run_crf_main.py <treatment>

Outputs (appended per treatment):
  reports/tables/crf_ate_results.csv
  reports/tables/crf_cate_summary.csv
  reports/tables/crf_cate_by_observation.csv   (input for tasks 13/14)
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from econml.dml import CausalForestDML
from sklearn.ensemble import RandomForestRegressor

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "final" / "analysis_panel_2018_2024.csv"
TABLES = PROJECT_ROOT / "reports" / "tables"

Y_COL = "informal_rate"
ROLES = {"log_real_min_wage": "main", "real_min_wage": "robustness",
         "min_wage_growth": "exploratory"}
CONTROLS = [
    "unemployment_rate",
    "labour_productivity",
    "trained_labour_rate",
    "log_employed_persons",
]
SEED = 42

df = pd.read_csv(INPUT_PATH)
X = df[CONTROLS].to_numpy()
W = pd.concat(
    [df[CONTROLS], pd.get_dummies(df["year"], prefix="yr", drop_first=True, dtype=float)],
    axis=1,
).to_numpy()
y = df[Y_COL].to_numpy()

d_col = sys.argv[1]
t = df[d_col].to_numpy()

est = CausalForestDML(
    model_y=RandomForestRegressor(n_estimators=200, min_samples_leaf=5, random_state=SEED, n_jobs=-1),
    model_t=RandomForestRegressor(n_estimators=200, min_samples_leaf=5, random_state=SEED, n_jobs=-1),
    n_estimators=1000,
    min_samples_leaf=10,
    cv=5,
    random_state=SEED,
    discrete_treatment=False,
)
est.fit(y, t, X=X, W=W, groups=df["province"].values)

cate = est.effect(X).ravel()
cate_lb, cate_ub = (a.ravel() for a in est.effect_interval(X, alpha=0.05))
ate = float(est.ate(X))
ate_lb, ate_ub = (float(v) for v in est.ate_interval(X, alpha=0.05))

# --- ATE row ---
ate_row = pd.DataFrame([{
    "treatment": d_col, "role": ROLES[d_col], "seed": SEED,
    "ate": ate, "ci_lower": ate_lb, "ci_upper": ate_ub,
    "ci_contains_zero": ate_lb <= 0 <= ate_ub,
    "n_obs": len(y), "estimator": "CausalForestDML(1000 trees, leaf>=10, cv=5 GroupKFold by province)",
    "note": "average marginal effect, exploratory; selection-on-observables, W=controls+year dummies",
}])

# --- CATE summary row ---
q = np.percentile(cate, [5, 25, 50, 75, 95])
cate_row = pd.DataFrame([{
    "treatment": d_col, "role": ROLES[d_col], "seed": SEED,
    "cate_mean": cate.mean(), "cate_sd": cate.std(),
    "p5": q[0], "p25": q[1], "median": q[2], "p75": q[3], "p95": q[4],
    "share_negative": float((cate < 0).mean()),
    "share_ci_excludes_zero": float(((cate_lb > 0) | (cate_ub < 0)).mean()),
    "note": "individual CATEs are noisy at n=441; read distribution shape only",
}])

# --- obs-level CATE for tasks 13/14 ---
obs = df[["province", "year", "wage_region", *CONTROLS]].copy()
obs["treatment"] = d_col
obs["cate"] = cate
obs["cate_lb"] = cate_lb
obs["cate_ub"] = cate_ub


def append(path: Path, new: pd.DataFrame, key: str = "treatment") -> None:
    if path.exists():
        old = pd.read_csv(path)
        new = pd.concat([old[old[key] != d_col], new], ignore_index=True)
    new.to_csv(path, index=False)


append(TABLES / "crf_ate_results.csv", ate_row)
append(TABLES / "crf_cate_summary.csv", cate_row)
append(TABLES / "crf_cate_by_observation.csv", obs)

print(f"{d_col} ({ROLES[d_col]}): ATE = {ate:.4g}, 95% CI = [{ate_lb:.4g}, {ate_ub:.4g}], "
      f"CI contains 0: {ate_lb <= 0 <= ate_ub}")
print(f"CATE: mean={cate.mean():.4g}, sd={cate.std():.4g}, share<0 = {(cate < 0).mean():.0%}, "
      f"share indiv CI excl 0 = {((cate_lb > 0) | (cate_ub < 0)).mean():.0%}")
