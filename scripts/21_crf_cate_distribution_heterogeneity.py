"""Tasks 13+14 (cr7.xlsx): CATE distribution plots + heterogeneity cuts.

Task 13: histogram + density of CATE per treatment, zero reference line.
Task 14: mean CATE by tercile of productivity / unemployment / trained labour,
         by year, and by wage_region (with the explicit caveat that
         wage_region nearly coincides with treatment intensity itself).

All outputs are exploratory heterogeneity description, not causal proof.

Outputs:
  reports/figures/crf/cate_distribution_<treatment>.png
  reports/figures/crf/cate_heterogeneity_log_real_min_wage.png
  reports/tables/crf_heterogeneity.csv
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TABLES = PROJECT_ROOT / "reports" / "tables"
FIG_DIR = PROJECT_ROOT / "reports" / "figures" / "crf"
FIG_DIR.mkdir(parents=True, exist_ok=True)

obs = pd.read_csv(TABLES / "crf_cate_by_observation.csv")
TREATMENTS = ["log_real_min_wage", "real_min_wage", "min_wage_growth"]
HET_VARS = ["labour_productivity", "unemployment_rate", "trained_labour_rate"]

# ---------------- Task 13: distributions ----------------
for d_col in TREATMENTS:
    g = obs[obs["treatment"] == d_col]
    cate = g["cate"].to_numpy()
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.hist(cate, bins=40, density=True, alpha=0.55, color="#4878a8", edgecolor="white")
    xs = np.linspace(cate.min(), cate.max(), 300)
    ax.plot(xs, gaussian_kde(cate)(xs), color="#c44e52", lw=2)
    ax.axvline(0, color="black", lw=1.4, ls="--", label="0")
    ax.axvline(cate.mean(), color="#55a868", lw=1.4, label=f"mean = {cate.mean():.3g}")
    ax.set_xlabel(f"CATE ({d_col})")
    ax.set_ylabel("density")
    ax.set_title(f"CATE distribution - {d_col}\nexploratory heterogeneity, share<0 = {(cate<0).mean():.0%}")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG_DIR / f"cate_distribution_{d_col}.png", dpi=150)
    plt.close(fig)

# ---------------- Task 14: heterogeneity cuts ----------------
rows = []
for d_col in TREATMENTS:
    g = obs[obs["treatment"] == d_col].copy()
    for var in HET_VARS:
        g["_grp"] = pd.qcut(g[var], 3, labels=["low", "mid", "high"])
        for lvl, sub in g.groupby("_grp", observed=True):
            rows.append({"treatment": d_col, "cut_by": var, "group": str(lvl),
                         "n": len(sub), "cate_mean": sub["cate"].mean(),
                         "cate_sd": sub["cate"].std(),
                         "share_negative": (sub["cate"] < 0).mean(),
                         "caveat": ""})
    for lvl, sub in g.groupby("year"):
        rows.append({"treatment": d_col, "cut_by": "year", "group": str(lvl),
                     "n": len(sub), "cate_mean": sub["cate"].mean(),
                     "cate_sd": sub["cate"].std(),
                     "share_negative": (sub["cate"] < 0).mean(), "caveat": ""})
    for lvl, sub in g.groupby("wage_region"):
        rows.append({"treatment": d_col, "cut_by": "wage_region", "group": str(lvl),
                     "n": len(sub), "cate_mean": sub["cate"].mean(),
                     "cate_sd": sub["cate"].std(),
                     "share_negative": (sub["cate"] < 0).mean(),
                     "caveat": "wage_region ~ treatment intensity itself; descriptive only"})

het = pd.DataFrame(rows)
het.to_csv(TABLES / "crf_heterogeneity.csv", index=False)

# figure: heterogeneity for the main treatment
g = obs[obs["treatment"] == "log_real_min_wage"].copy()
fig, axes = plt.subplots(1, 3, figsize=(13, 4.2), sharey=True)
for ax, var in zip(axes, HET_VARS):
    g["_grp"] = pd.qcut(g[var], 3, labels=["low", "mid", "high"])
    data = [g.loc[g["_grp"] == lvl, "cate"] for lvl in ["low", "mid", "high"]]
    ax.boxplot(data, tick_labels=["low", "mid", "high"], showmeans=True)
    ax.axhline(0, color="black", lw=1, ls="--")
    ax.set_title(var, fontsize=10)
    ax.set_xlabel("tercile")
axes[0].set_ylabel("CATE (log_real_min_wage)")
fig.suptitle("CATE heterogeneity by tercile - exploratory, not causal proof", fontsize=11)
fig.tight_layout()
fig.savefig(FIG_DIR / "cate_heterogeneity_log_real_min_wage.png", dpi=150)
plt.close(fig)

main_het = het[(het["treatment"] == "log_real_min_wage") & (het["cut_by"] != "year")]
print(main_het[["cut_by", "group", "n", "cate_mean", "share_negative"]].to_string(index=False))
print(f"\nFigures -> {FIG_DIR}")
