"""Task bo sung B: DML variant with province dummies added to W.

Purpose: the repo's main DML uses W = controls + year dummies only, so its
negative theta lines up with pooled-OLS/year-FE specs, while province-FE/TWFE
flip the coefficient positive. This variant lets the nuisance learners also
absorb province-level heterogeneity, making DML comparable with TWFE and
telling us whether the DML-vs-TWFE sign conflict is driven by omitted
province effects rather than by functional form.

Spec: partialling-out DML, K=5, learners {ridge, RF, GBM}, seeds {42,123,2024},
W = 4 controls + year dummies + 62 province dummies, cluster SE by province.

usage: python 19_... run <treatment>   |   python 19_... combine

Output: reports/tables/dml_theta_province_fe.csv
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import KFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "final" / "analysis_panel_2018_2024.csv"
TABLES = PROJECT_ROOT / "reports" / "tables"
OUT_PATH = TABLES / "dml_theta_province_fe.csv"

Y_COL = "informal_rate"
TREATMENTS = ["log_real_min_wage", "real_min_wage"]
CONTROLS = [
    "unemployment_rate",
    "labour_productivity",
    "trained_labour_rate",
    "log_employed_persons",
]
SEEDS = [42, 123, 2024]
K = 5

df = pd.read_csv(INPUT_PATH)
W = pd.concat(
    [
        df[CONTROLS].astype(float),
        pd.get_dummies(df["year"], prefix="year", drop_first=True, dtype=float),
        pd.get_dummies(df["province"], prefix="prov", drop_first=True, dtype=float),
    ],
    axis=1,
).to_numpy()
provinces = df["province"].to_numpy()


def make_learner(name: str, seed: int):
    if name == "ridge":
        return make_pipeline(StandardScaler(), Ridge(alpha=1.0))
    if name == "random_forest":
        return RandomForestRegressor(n_estimators=200, min_samples_leaf=5,
                                     random_state=seed, n_jobs=-1)
    return GradientBoostingRegressor(n_estimators=200, learning_rate=0.07,
                                     max_depth=3, random_state=seed)


def dml(y: np.ndarray, d: np.ndarray, learner: str, seed: int) -> dict[str, float]:
    ry, rd = np.zeros_like(y), np.zeros_like(d)
    for tr, te in KFold(n_splits=K, shuffle=True, random_state=seed).split(W):
        ry[te] = y[te] - make_learner(learner, seed).fit(W[tr], y[tr]).predict(W[te])
        rd[te] = d[te] - make_learner(learner, seed).fit(W[tr], d[tr]).predict(W[te])
    theta = float(np.sum(rd * ry) / np.sum(rd**2))
    psi = rd * (ry - theta * rd) / np.mean(rd**2)
    cluster_sum = pd.Series(psi).groupby(pd.Series(provinces)).sum().to_numpy()
    se = float(np.sqrt(np.sum(cluster_sum**2)) / len(y))
    p = float(2 * (1 - stats.norm.cdf(abs(theta / se))))
    return {"theta": theta, "se": se, "p_value": p,
            "ci_lower": theta - 1.96 * se, "ci_upper": theta + 1.96 * se}


mode = sys.argv[1] if len(sys.argv) > 1 else "combine"

if mode == "run":
    d_col = sys.argv[2]
    y_arr = df[Y_COL].to_numpy(dtype=float)
    d_arr = df[d_col].to_numpy(dtype=float)
    rows = []
    for learner in ["ridge", "random_forest", "gradient_boosting"]:
        for seed in SEEDS:
            r = dml(y_arr, d_arr, learner, seed)
            rows.append({"treatment": d_col, "learner": learner, "seed": seed, **r,
                         "ci_contains_zero": r["ci_lower"] <= 0 <= r["ci_upper"],
                         "spec": "W + year dummies + province dummies"})
    chunk = pd.DataFrame(rows)
    if OUT_PATH.exists():
        old = pd.read_csv(OUT_PATH)
        chunk = pd.concat([old[old["treatment"] != d_col], chunk], ignore_index=True)
    chunk.to_csv(OUT_PATH, index=False)
    print(chunk[chunk["treatment"] == d_col][["learner", "seed", "theta", "p_value",
                                              "ci_contains_zero"]].to_string(index=False))
    sys.exit(0)

out = pd.read_csv(OUT_PATH)
base = pd.read_csv(TABLES / "baseline_ols_fe_results.csv")
print("=== DML with province FE vs baseline TWFE ===")
for d_col in TREATMENTS:
    g = out[out["treatment"] == d_col]
    twfe = base[(base["treatment"] == d_col) & (base["model"] == "two_way_fe_controls")
                & (base["control_set"] == "log_employment_scale")]["coefficient"].iloc[0]
    print(f"\n{d_col}: TWFE = {twfe:.4g}")
    print(f"  theta mean = {g['theta'].mean():.4g}, range = [{g['theta'].min():.4g}, {g['theta'].max():.4g}]")
    print(f"  share positive = {(g['theta'] > 0).mean():.0%}, share CI contains 0 = {g['ci_contains_zero'].mean():.0%}")
