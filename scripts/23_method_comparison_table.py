"""Task 16 (cr7.xlsx, phan Duc): Method comparison table.

One row per (treatment x method). The `interpretation_vi` column is left
as a draft placeholder for Hoang to finalize (task 16 is shared).

Sources:
  baseline_ols_fe_results.csv        (pooled/year FE/province FE/TWFE, log_employment_scale)
  dml_theta_stability.csv + dml_theta_by_k.csv      (DML, W + year)
  dml_theta_province_fe.csv          (DML + province FE)
  crf_stability_by_seed.csv          (CRF, all seeds, leaf=10)

Output: reports/tables/method_comparison_summary.csv
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
T = PROJECT_ROOT / "reports" / "tables"
OUT = T / "method_comparison_summary.csv"

base = pd.read_csv(T / "baseline_ols_fe_results.csv")
dml_stab = pd.read_csv(T / "dml_theta_stability.csv")
dml_main = pd.read_csv(T / "dml_main_results.csv")
dml_k = pd.read_csv(T / "dml_theta_by_k.csv")
dml_pfe = pd.read_csv(T / "dml_theta_province_fe.csv")
crf = pd.read_csv(T / "crf_stability_by_seed.csv")
crf = crf[crf["min_samples_leaf"] == 10]

TREATMENTS = ["log_real_min_wage", "real_min_wage", "min_wage_growth"]
BASE_MODELS = {
    "pooled_ols_controls": ("Pooled OLS + W", "between + within variation, no FE"),
    "year_fe_controls": ("Year FE + W", "between-province variation (net of common shocks)"),
    "province_fe_controls": ("Province FE + W", "within-province variation over time"),
    "two_way_fe_controls": ("TWFE + W", "within-province, net of common shocks"),
}

rows = []
for d in TREATMENTS:
    for model, (label, variation) in BASE_MODELS.items():
        b = base[(base["treatment"] == d) & (base["model"] == model)
                 & (base["control_set"] == "log_employment_scale")].iloc[0]
        rows.append({
            "treatment": d, "method": label, "role": "baseline (linear)",
            "variation_used": variation,
            "estimate": b["coefficient"],
            "ci_95": f"[{b['ci_lower_95']:.4g}, {b['ci_upper_95']:.4g}]",
            "p_value": round(b["p_value"], 4),
            "sign": "+" if b["coefficient"] > 0 else "-",
            "stability": "single spec, cluster SE by province",
            "interpretation_vi": "HOANG_DIEN",
        })

    m = dml_main[dml_main["treatment"] == d]
    s = dml_stab[dml_stab["treatment"] == d].iloc[0]
    k = dml_k[dml_k["treatment"] == d]
    rows.append({
        "treatment": d, "method": "DML (W + year dummies)", "role": "flexible-control robustness",
        "variation_used": "between-province variation (same as year FE)",
        "estimate": m["theta"].mean(),
        "ci_95": f"theta range [{m['theta'].min():.4g}, {m['theta'].max():.4g}] (9 runs)",
        "p_value": round(m["p_value"].mean(), 4),
        "sign": "+" if m["theta"].mean() > 0 else "-",
        "stability": (f"sign {'stable' if s['stable_sign'] else 'UNSTABLE'}; "
                      f"CI contains 0 in {s['share_ci_contains_zero']:.0%} of runs; "
                      f"K=2/5/10 share negative {(k['theta'] < 0).mean():.0%}"),
        "interpretation_vi": "HOANG_DIEN",
    })

    if d in dml_pfe["treatment"].unique():
        p = dml_pfe[dml_pfe["treatment"] == d]
        rows.append({
            "treatment": d, "method": "DML (+ province dummies)", "role": "robustness (TWFE-comparable)",
            "variation_used": "within-province variation",
            "estimate": p["theta"].mean(),
            "ci_95": f"theta range [{p['theta'].min():.4g}, {p['theta'].max():.4g}] (9 runs)",
            "p_value": round(p["p_value"].mean(), 4),
            "sign": "mixed" if ((p["theta"] > 0).any() and (p["theta"] < 0).any())
            else ("+" if p["theta"].mean() > 0 else "-"),
            "stability": (f"sign flips across learners; CI contains 0 in "
                          f"{p['ci_contains_zero'].mean():.0%} of runs -> "
                          "little within variation left (95% of D variance is between)"),
            "interpretation_vi": "HOANG_DIEN",
        })

    if d in crf["treatment"].unique():
        c = crf[crf["treatment"] == d]
        rows.append({
            "treatment": d, "method": "Causal Forest DML (CRF)", "role": "exploratory heterogeneity",
            "variation_used": "between-province variation (W = controls + year)",
            "estimate": c["ate"].median(),
            "ci_95": f"ATE range [{c['ate'].min():.4g}, {c['ate'].max():.4g}] ({len(c)} seeds)",
            "p_value": None,
            "sign": "-" if (c["ate"] < 0).all() else "mixed",
            "stability": (f"sign stable across {len(c)} seeds, magnitude seed-sensitive; "
                          f"CI contains 0 in {c['ci_contains_zero'].mean():.0%} of runs"),
            "interpretation_vi": "HOANG_DIEN",
        })

out = pd.DataFrame(rows)
out.to_csv(OUT, index=False)
pd.set_option("display.width", 220)
pd.set_option("display.max_colwidth", 60)
print(out[out["treatment"] == "log_real_min_wage"][
    ["method", "role", "estimate", "sign", "stability"]].to_string(index=False))
print(f"\nFull table ({len(out)} rows) -> {OUT}")
