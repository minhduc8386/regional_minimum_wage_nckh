"""Task 15 (cr7.xlsx): CRF stability across seeds + light tuning.

Rule from the work split: report ALL seeds, never pick the prettiest one.
Compares sign of every CRF ATE with the DML theta sign (negative).

usage: python 22_crf_stability_by_seed.py <treatment> <seed> [leaf]
       python 22_crf_stability_by_seed.py summarize

Output: reports/tables/crf_stability_by_seed.csv
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
from econml.dml import CausalForestDML
from sklearn.ensemble import RandomForestRegressor

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "final" / "analysis_panel_2018_2024.csv"
OUT_PATH = PROJECT_ROOT / "reports" / "tables" / "crf_stability_by_seed.csv"

Y_COL = "informal_rate"
CONTROLS = [
    "unemployment_rate",
    "labour_productivity",
    "trained_labour_rate",
    "log_employed_persons",
]

df = pd.read_csv(INPUT_PATH)
X = df[CONTROLS].to_numpy()
W = pd.concat(
    [df[CONTROLS], pd.get_dummies(df["year"], prefix="yr", drop_first=True, dtype=float)],
    axis=1,
).to_numpy()
y = df[Y_COL].to_numpy()

if sys.argv[1] == "summarize":
    out = pd.read_csv(OUT_PATH)
    for d_col, g in out.groupby("treatment"):
        print(f"\n{d_col}: {len(g)} runs")
        print(f"  ATE range [{g['ate'].min():.4g}, {g['ate'].max():.4g}], "
              f"share negative = {(g['ate'] < 0).mean():.0%}, "
              f"share CI contains 0 = {g['ci_contains_zero'].mean():.0%}")
        print(f"  same sign as DML theta (negative): {(g['ate'] < 0).all()}")
    sys.exit(0)

d_col, seed = sys.argv[1], int(sys.argv[2])
leaf = int(sys.argv[3]) if len(sys.argv) > 3 else 10
t = df[d_col].to_numpy()

est = CausalForestDML(
    model_y=RandomForestRegressor(n_estimators=200, min_samples_leaf=5, random_state=seed, n_jobs=-1),
    model_t=RandomForestRegressor(n_estimators=200, min_samples_leaf=5, random_state=seed, n_jobs=-1),
    n_estimators=1000, min_samples_leaf=leaf, cv=5, random_state=seed,
    discrete_treatment=False,
)
est.fit(y, t, X=X, W=W, groups=df["province"].values)
cate = est.effect(X).ravel()
ate = float(est.ate(X))
lb, ub = (float(v) for v in est.ate_interval(X, alpha=0.05))

row = pd.DataFrame([{
    "treatment": d_col, "seed": seed, "min_samples_leaf": leaf,
    "ate": ate, "ci_lower": lb, "ci_upper": ub,
    "ci_contains_zero": lb <= 0 <= ub,
    "cate_share_negative": float((cate < 0).mean()),
    "same_sign_as_dml": ate < 0,
}])
if OUT_PATH.exists():
    old = pd.read_csv(OUT_PATH)
    old = old[~((old["treatment"] == d_col) & (old["seed"] == seed)
                & (old["min_samples_leaf"] == leaf))]
    row = pd.concat([old, row], ignore_index=True)
row.to_csv(OUT_PATH, index=False)
print(f"{d_col} seed={seed} leaf={leaf}: ATE={ate:.4g} CI=[{lb:.4g},{ub:.4g}] "
      f"share_cate_neg={(cate < 0).mean():.0%}")
