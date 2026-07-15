"""Task 4 (cr7.xlsx): Residualized LOWESS (Frisch-Waugh style visual check).

Two specifications:
  spec1: residualize Y and D on W + year dummies          (matches current DML)
  spec2: residualize Y and D on W + year + province dummies (matches TWFE)

Interpretation guard: these plots show partial (non)linear ASSOCIATION after
controls. They are NOT causal dose-response curves.

Outputs:
  reports/figures/nonlinearity_residualized/residualized_lowess_<D>_<spec>.png
  reports/tables/residualized_lowess_summary.csv
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.nonparametric.smoothers_lowess import lowess

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "final" / "analysis_panel_2018_2024.csv"
FIG_DIR = PROJECT_ROOT / "reports" / "figures" / "nonlinearity_residualized"
OUT_PATH = PROJECT_ROOT / "reports" / "tables" / "residualized_lowess_summary.csv"

Y_COL = "informal_rate"
TREATMENTS = {
    "log_real_min_wage": "main",
    "real_min_wage": "robustness",
    "min_wage_growth": "exploratory",
}
CONTROLS = [
    "unemployment_rate",
    "labour_productivity",
    "trained_labour_rate",
    "log_employed_persons",
]
LOWESS_FRAC = 0.5

df = pd.read_csv(INPUT_PATH)


def design(spec: str) -> pd.DataFrame:
    X = df[CONTROLS].copy()
    X = pd.concat([X, pd.get_dummies(df["year"], prefix="year", drop_first=True, dtype=float)], axis=1)
    if spec == "w_year_province":
        X = pd.concat(
            [X, pd.get_dummies(df["province"], prefix="prov", drop_first=True, dtype=float)], axis=1
        )
    return sm.add_constant(X)


def residualize(series: pd.Series, X: pd.DataFrame) -> np.ndarray:
    return sm.OLS(series.astype(float), X).fit().resid.to_numpy()


def classify(departure: float) -> str:
    if departure < 0.05:
        return "near-linear"
    if departure < 0.15:
        return "mild curvature"
    return "visible curvature"


rows = []
FIG_DIR.mkdir(parents=True, exist_ok=True)

for spec, spec_label in [
    ("w_year", "W + year dummies (DML spec)"),
    ("w_year_province", "W + year + province dummies (TWFE spec)"),
]:
    X = design(spec)
    ry = residualize(df[Y_COL], X)
    for d_col, role in TREATMENTS.items():
        rd = residualize(df[d_col], X)

        # linear fit on residuals (= partialled-out OLS coefficient)
        slope, intercept = np.polyfit(rd, ry, 1)
        lin_pred = intercept + slope * rd

        smoothed = lowess(ry, rd, frac=LOWESS_FRAC, return_sorted=True)
        # departure of lowess from linear fit, scaled by sd of residualized Y
        lin_at_grid = intercept + slope * smoothed[:, 0]
        departure = float(np.sqrt(np.mean((smoothed[:, 1] - lin_at_grid) ** 2)) / np.std(ry))
        verdict = classify(departure)

        rows.append(
            {
                "treatment": d_col,
                "role": role,
                "spec": spec,
                "partial_slope": slope,
                "sd_resid_D": float(np.std(rd)),
                "sd_resid_Y": float(np.std(ry)),
                "share_D_variance_absorbed": float(1 - np.var(rd) / np.var(df[d_col])),
                "lowess_departure_ratio": departure,
                "conclusion": verdict,
                "note": "partial association after controls; not a causal dose-response",
            }
        )

        fig, ax = plt.subplots(figsize=(7, 5))
        ax.scatter(rd, ry, s=14, alpha=0.45, color="#4878a8", label="residualized obs")
        ax.plot(smoothed[:, 0], smoothed[:, 1], color="#c44e52", lw=2.2, label=f"LOWESS (frac={LOWESS_FRAC})")
        ax.plot(np.sort(rd), intercept + slope * np.sort(rd), color="#333333", lw=1.4, ls="--",
                label=f"linear fit (slope={slope:.3g})")
        ax.axhline(0, color="grey", lw=0.6)
        ax.axvline(0, color="grey", lw=0.6)
        ax.set_xlabel(f"{d_col} residual")
        ax.set_ylabel(f"{Y_COL} residual")
        ax.set_title(f"Residualized LOWESS - {d_col}\n{spec_label} | {verdict}")
        ax.legend(fontsize=8)
        fig.tight_layout()
        fig.savefig(FIG_DIR / f"residualized_lowess_{d_col}_{spec}.png", dpi=150)
        plt.close(fig)

out = pd.DataFrame(rows)
out.to_csv(OUT_PATH, index=False)
print(out[["treatment", "spec", "partial_slope", "share_D_variance_absorbed",
           "lowess_departure_ratio", "conclusion"]].to_string(index=False))
print(f"\nFigures -> {FIG_DIR}")
