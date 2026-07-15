"""Tasks 5+6 (cr7.xlsx): Partial dependence plots + feature importance from
predictive RF/GBM models.

Design notes:
- One model per treatment (D + W + year as features). log_real_min_wage and
  real_min_wage are deterministic transforms of each other, so they are never
  put in the same model (importance would be split arbitrarily).
- PDP describes the PREDICTIVE surface of the fitted model. It is NOT a
  treatment effect and must not be labelled as one.
- Importance reported two ways: impurity-based (fast, biased toward
  high-cardinality features) and permutation (preferred).

Outputs:
  reports/figures/pdp/pdp_<treatment>_<model>.png
  reports/tables/feature_importance.csv
  reports/tables/pdp_summary.csv
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.inspection import partial_dependence, permutation_importance

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "final" / "analysis_panel_2018_2024.csv"
FIG_DIR = PROJECT_ROOT / "reports" / "figures" / "pdp"
IMP_PATH = PROJECT_ROOT / "reports" / "tables" / "feature_importance.csv"
PDP_PATH = PROJECT_ROOT / "reports" / "tables" / "pdp_summary.csv"

Y_COL = "informal_rate"
TREATMENTS = ["log_real_min_wage", "real_min_wage", "min_wage_growth"]
CONTROLS = [
    "unemployment_rate",
    "labour_productivity",
    "trained_labour_rate",
    "log_employed_persons",
]
SEED = 42

MODELS = {
    "random_forest": lambda: RandomForestRegressor(
        n_estimators=500, min_samples_leaf=5, random_state=SEED, n_jobs=-1
    ),
    "gradient_boosting": lambda: GradientBoostingRegressor(
        n_estimators=300, learning_rate=0.05, max_depth=3, random_state=SEED
    ),
}

df = pd.read_csv(INPUT_PATH)
y = df[Y_COL].to_numpy()

imp_rows, pdp_rows = [], []
FIG_DIR.mkdir(parents=True, exist_ok=True)

for d_col in TREATMENTS:
    features = [d_col, *CONTROLS, "year"]
    X = df[features].astype(float)

    for model_name, make in MODELS.items():
        model = make().fit(X, y)

        # --- importance ---
        impurity = dict(zip(features, model.feature_importances_))
        perm = permutation_importance(model, X, y, n_repeats=30, random_state=SEED, n_jobs=-1)
        for i, f in enumerate(features):
            imp_rows.append(
                {
                    "treatment_model": d_col,
                    "model": model_name,
                    "feature": f,
                    "impurity_importance": impurity[f],
                    "permutation_importance_mean": perm.importances_mean[i],
                    "permutation_importance_std": perm.importances_std[i],
                    "is_treatment": f == d_col,
                }
            )

        # --- PDP for the treatment ---
        pd_res = partial_dependence(
            model, X, features=[d_col], kind="average", grid_resolution=40
        )
        grid = pd_res["grid_values"][0]
        avg = pd_res["average"][0]
        pdp_range = float(avg.max() - avg.min())

        # crude shape check: correlation between PDP curve and its linear fit
        lin = np.polyval(np.polyfit(grid, avg, 1), grid)
        shape_departure = float(np.sqrt(np.mean((avg - lin) ** 2)) / (np.std(avg) + 1e-12))
        pdp_rows.append(
            {
                "treatment": d_col,
                "model": model_name,
                "pdp_range_pp": pdp_range,
                "monotonic_decreasing": bool(np.all(np.diff(avg) <= 1e-9)),
                "departure_from_linear": shape_departure,
                "note": "predictive surface only, not a treatment effect",
            }
        )

        fig, ax = plt.subplots(figsize=(7, 4.5))
        ax.plot(grid, avg, color="#c44e52", lw=2.2)
        ax.plot(grid, lin, color="#333333", lw=1.2, ls="--", label="linear reference")
        rug = X[d_col].to_numpy()
        ax.plot(rug, np.full_like(rug, avg.min() - 0.03 * (avg.max() - avg.min() + 1e-9)),
                "|", color="#4878a8", alpha=0.3, ms=8)
        ax.set_xlabel(d_col)
        ax.set_ylabel(f"predicted {Y_COL} (avg)")
        ax.set_title(f"Partial dependence - {d_col} ({model_name})\npredictive association, NOT a causal effect")
        ax.legend(fontsize=8)
        fig.tight_layout()
        fig.savefig(FIG_DIR / f"pdp_{d_col}_{model_name}.png", dpi=150)
        plt.close(fig)

imp = pd.DataFrame(imp_rows)
imp.to_csv(IMP_PATH, index=False)
pdp = pd.DataFrame(pdp_rows)
pdp.to_csv(PDP_PATH, index=False)

print("=== PDP summary ===")
print(pdp.to_string(index=False))
print("\n=== Permutation importance (treatment rows) ===")
t = imp[imp["is_treatment"]]
print(t[["treatment_model", "model", "permutation_importance_mean"]].to_string(index=False))
print("\n=== Top-3 features per model (permutation) ===")
for (d, m), g in imp.groupby(["treatment_model", "model"]):
    top = g.nlargest(3, "permutation_importance_mean")[["feature", "permutation_importance_mean"]]
    print(d, "|", m, "->", ", ".join(f"{r.feature}={r.permutation_importance_mean:.3f}" for r in top.itertuples()))
