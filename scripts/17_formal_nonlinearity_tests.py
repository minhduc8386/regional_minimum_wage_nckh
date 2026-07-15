"""Task bo sung A: Formal statistical tests for nonlinearity.

Two families of tests, all with province-clustered SEs:
  1. Ramsey RESET (powers 2,3 of fitted values) on each linear spec.
  2. Wald tests on added quadratic terms:
     a. D^2 alone            -> is the treatment relation curved?
     b. all W^2 jointly      -> are control relations curved?
     c. D^2 + all W^2 jointly

Specs mirror the baseline table:
  pooled:      Y ~ D + W
  year_fe:     Y ~ D + W + year dummies          (DML-comparable)
  twfe:        Y ~ D + W + year + province dummies

Output: reports/tables/nonlinearity_formal_tests.csv
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.diagnostic import linear_reset

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "final" / "analysis_panel_2018_2024.csv"
OUT_PATH = PROJECT_ROOT / "reports" / "tables" / "nonlinearity_formal_tests.csv"

Y_COL = "informal_rate"
TREATMENTS = ["log_real_min_wage", "real_min_wage"]  # main + robustness; growth is exploratory
CONTROLS = [
    "unemployment_rate",
    "labour_productivity",
    "trained_labour_rate",
    "log_employed_persons",
]

df = pd.read_csv(INPUT_PATH)
groups = df["province"]
cluster_kw = dict(cov_type="cluster", cov_kwds={"groups": groups})


def zscore(s: pd.Series) -> pd.Series:
    return (s - s.mean()) / s.std()


def build_X(d_col: str, spec: str, quad_of: list[str]) -> pd.DataFrame:
    """Standardize continuous vars first so squared terms are well-scaled."""
    base = {d_col: zscore(df[d_col])}
    for c in CONTROLS:
        base[c] = zscore(df[c])
    X = pd.DataFrame(base)
    for c in quad_of:
        X[f"{c}_sq"] = X[c] ** 2
    if spec in ("year_fe", "twfe"):
        X = pd.concat([X, pd.get_dummies(df["year"], prefix="yr", drop_first=True, dtype=float)], axis=1)
    if spec == "twfe":
        X = pd.concat([X, pd.get_dummies(df["province"], prefix="pv", drop_first=True, dtype=float)], axis=1)
    return sm.add_constant(X)


rows = []
y = df[Y_COL].astype(float)

for d_col in TREATMENTS:
    for spec in ["pooled", "year_fe", "twfe"]:
        # --- Ramsey RESET (manual: add yhat^2, yhat^3, cluster-robust Wald) ---
        X_lin = build_X(d_col, spec, [])
        res_lin = sm.OLS(y, X_lin).fit(**cluster_kw)
        fitted = res_lin.fittedvalues
        fz = (fitted - fitted.mean()) / fitted.std()
        X_reset = X_lin.copy()
        X_reset["yhat_p2"] = fz**2
        X_reset["yhat_p3"] = fz**3
        res_reset = sm.OLS(y, X_reset).fit(**cluster_kw)
        R = np.zeros((2, len(res_reset.params)))
        idx = list(res_reset.params.index)
        R[0, idx.index("yhat_p2")] = 1.0
        R[1, idx.index("yhat_p3")] = 1.0
        wald_reset = res_reset.wald_test(R, use_f=True, scalar=True)
        rows.append({"treatment": d_col, "spec": spec, "test": "RESET(fitted^2,^3)",
                     "stat": float(wald_reset.statistic),
                     "p_value": float(wald_reset.pvalue),
                     "reject_linearity_5pct": float(wald_reset.pvalue) < 0.05})

        # --- quadratic-term Wald tests ---
        variants = {
            "D_squared_only": [d_col],
            "W_squared_joint": CONTROLS,
            "D_and_W_squared_joint": [d_col, *CONTROLS],
        }
        for label, quad_of in variants.items():
            res_q = sm.OLS(y, build_X(d_col, spec, quad_of)).fit(**cluster_kw)
            sq_names = [f"{c}_sq" for c in quad_of]
            R = np.zeros((len(sq_names), len(res_q.params)))
            for i, name in enumerate(sq_names):
                R[i, list(res_q.params.index).index(name)] = 1.0
            wald = res_q.wald_test(R, use_f=True, scalar=True)
            rows.append({"treatment": d_col, "spec": spec, "test": f"Wald[{label}]",
                         "stat": float(wald.statistic), "p_value": float(wald.pvalue),
                         "reject_linearity_5pct": float(wald.pvalue) < 0.05,
                         "d_sq_coef": float(res_q.params.get(f"{d_col}_sq", np.nan))
                         if d_col in quad_of else np.nan})

out = pd.DataFrame(rows)
out.to_csv(OUT_PATH, index=False)
pd.set_option("display.width", 160)
print(out.to_string(index=False))
n_rej = out["reject_linearity_5pct"].fillna(False).sum()
print(f"\nTests rejecting linearity at 5%: {int(n_rej)}/{len(out)}")
