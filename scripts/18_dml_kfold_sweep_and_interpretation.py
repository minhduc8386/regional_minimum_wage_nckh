"""Task 8 (cr7.xlsx, phan Duc): DML theta stability.

Part 1 - K-fold sweep: re-run partialling-out DML with K in {2, 5, 10}
         (advisor asked whether theta "converges" across K-fold choices).
         Learners: ridge / random forest / gradient boosting (sklearn),
         seeds {42, 123, 2024}, W = controls + year dummies (same as repo DML).
Part 2 - Interpretation table: combine existing dml_* tables + new K sweep
         into one "DML convergence interpretation" per treatment, separating
         sign stability / fold stability / learner / seed / CI-contains-0 /
         comparison with TWFE sign.

Wording rule: say "relatively stable", never "converged" (asymptotic claim).

Outputs:
  reports/tables/dml_theta_by_k.csv
  reports/tables/dml_convergence_interpretation.csv
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

Y_COL = "informal_rate"
TREATMENTS = ["log_real_min_wage", "real_min_wage", "min_wage_growth"]
CONTROLS = [
    "unemployment_rate",
    "labour_productivity",
    "trained_labour_rate",
    "log_employed_persons",
]
SEEDS = [42, 123, 2024]
K_LIST = [2, 5, 10]

df = pd.read_csv(INPUT_PATH)
year_dummies = pd.get_dummies(df["year"], prefix="year", drop_first=True, dtype=float)
W = pd.concat([df[CONTROLS].astype(float), year_dummies], axis=1).to_numpy()
provinces = df["province"].to_numpy()


def make_learner(name: str, seed: int):
    if name == "ridge":
        return make_pipeline(StandardScaler(), Ridge(alpha=1.0))
    if name == "random_forest":
        return RandomForestRegressor(n_estimators=200, min_samples_leaf=5,
                                     random_state=seed, n_jobs=-1)
    return GradientBoostingRegressor(n_estimators=200, learning_rate=0.07,
                                     max_depth=3, random_state=seed)


def dml_partialling_out(y: np.ndarray, d: np.ndarray, learner_name: str,
                        seed: int, k: int) -> dict[str, float]:
    ry = np.zeros_like(y)
    rd = np.zeros_like(d)
    kf = KFold(n_splits=k, shuffle=True, random_state=seed)
    for tr, te in kf.split(W):
        my = make_learner(learner_name, seed).fit(W[tr], y[tr])
        md = make_learner(learner_name, seed).fit(W[tr], d[tr])
        ry[te] = y[te] - my.predict(W[te])
        rd[te] = d[te] - md.predict(W[te])
    theta = float(np.sum(rd * ry) / np.sum(rd**2))
    # cluster-robust SE via influence function, clustered by province
    denom = np.mean(rd**2)
    psi = rd * (ry - theta * rd) / denom
    n = len(y)
    cluster_sum = pd.Series(psi).groupby(pd.Series(provinces)).sum().to_numpy()
    se = float(np.sqrt(np.sum(cluster_sum**2)) / n)
    z = theta / se
    p = float(2 * (1 - stats.norm.cdf(abs(z))))
    return {"theta": theta, "se": se, "p_value": p,
            "ci_lower": theta - 1.96 * se, "ci_upper": theta + 1.96 * se}


# ---------------- Part 1: K sweep (chunked via CLI) ----------------
# usage: python 18_... run <treatment> <K>     -> append chunk to dml_theta_by_k.csv
#        python 18_... combine                 -> build interpretation table
BY_K_PATH = TABLES / "dml_theta_by_k.csv"
mode = sys.argv[1] if len(sys.argv) > 1 else "combine"

if mode == "run":
    d_col, k = sys.argv[2], int(sys.argv[3])
    y_arr = df[Y_COL].to_numpy(dtype=float)
    d_arr = df[d_col].to_numpy(dtype=float)
    rows = []
    for learner in ["ridge", "random_forest", "gradient_boosting"]:
        for seed in SEEDS:
            r = dml_partialling_out(y_arr, d_arr, learner, seed, k)
            rows.append({"treatment": d_col, "K": k, "learner": learner,
                         "seed": seed, **r,
                         "ci_contains_zero": r["ci_lower"] <= 0 <= r["ci_upper"]})
    chunk = pd.DataFrame(rows)
    if BY_K_PATH.exists():
        old = pd.read_csv(BY_K_PATH)
        old = old[~((old["treatment"] == d_col) & (old["K"] == k))]
        chunk = pd.concat([old, chunk], ignore_index=True)
    chunk.to_csv(BY_K_PATH, index=False)
    print(f"done {d_col} K={k}: share negative = {(pd.DataFrame(rows)['theta'] < 0).mean():.0%}")
    sys.exit(0)

by_k = pd.read_csv(BY_K_PATH)

# ---------------- Part 2: interpretation table ----------------
main = pd.read_csv(TABLES / "dml_main_results.csv")
fold = pd.read_csv(TABLES / "dml_theta_by_fold.csv")
baseline = pd.read_csv(TABLES / "baseline_ols_fe_results.csv")

interp = []
for d_col in TREATMENTS:
    m = main[main["treatment"] == d_col]
    f = fold[fold["treatment"] == d_col]
    bk = by_k[by_k["treatment"] == d_col]
    twfe = baseline[(baseline["treatment"] == d_col)
                    & (baseline["model"] == "two_way_fe_controls")
                    & (baseline["control_set"] == "log_employment_scale")]
    twfe_sign = "+" if twfe["coefficient"].iloc[0] > 0 else "-"
    ci0 = ((m["ci_lower"] <= 0) & (m["ci_upper"] >= 0)).mean()
    k_sign_neg = (bk.groupby("K")["theta"].apply(lambda s: (s < 0).mean()))
    interp.append({
        "treatment": d_col,
        "sign_stability_9runs": f"{(m['theta'] < 0).mean():.0%} negative",
        "fold_sign_stability": f"{(f['theta_fold'] < 0).mean():.0%} of {len(f)} folds negative",
        "learner_range": f"[{m['theta'].min():.4g}, {m['theta'].max():.4g}]",
        "share_ci_contains_zero": f"{ci0:.0%} (mainly gradient boosting)" if ci0 > 0 else "0%",
        "avg_p_value": round(float(m["p_value"].mean()), 4),
        "k_sweep_share_negative": "; ".join(f"K={k}: {v:.0%}" for k, v in k_sign_neg.items()),
        "k_sweep_theta_range": f"[{bk['theta'].min():.4g}, {bk['theta'].max():.4g}]",
        "twfe_sign": twfe_sign,
        "sign_conflict_with_twfe": ("yes" if (m["theta"].mean() < 0) == (twfe_sign == "+") else "no"),
        "verdict": ("relatively stable sign across folds/learners/seeds/K; "
                    "NOT convergence proof; conflicts with TWFE sign -> flexible-control "
                    "robustness only" if (m["theta"] < 0).all() or (m["theta"] > 0).all()
                    else "unstable across runs; exploratory only"),
    })

interp_df = pd.DataFrame(interp)
interp_df.to_csv(TABLES / "dml_convergence_interpretation.csv", index=False)

pd.set_option("display.width", 200)
print("=== K sweep summary (mean theta by treatment x K x learner) ===")
print(by_k.groupby(["treatment", "K", "learner"])["theta"].mean().unstack("K").to_string())
print("\n=== Interpretation table ===")
print(interp_df.to_string(index=False))
