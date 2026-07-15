"""Task 2 (cr7.xlsx): Validate analysis panel before running enhanced
nonlinearity checks and Causal Random Forest.

Gate rule (per work-split note): do NOT run CRF if variables are missing,
treatment has no variation, or panel has duplicates/missing values.

Output: reports/tables/enhanced_model_input_validation.csv
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "final" / "analysis_panel_2018_2024.csv"
OUTPUT_PATH = PROJECT_ROOT / "reports" / "tables" / "enhanced_model_input_validation.csv"

Y_COL = "informal_rate"
TREATMENTS = ["real_min_wage", "log_real_min_wage", "min_wage_growth"]
CONTROLS = [
    "unemployment_rate",
    "labour_productivity",
    "trained_labour_rate",
    "log_employed_persons",
]
KEYS = ["province", "year"]
REQUIRED = [*KEYS, "wage_region", Y_COL, *TREATMENTS, *CONTROLS]

rows: list[dict[str, object]] = []


def check(name: str, passed: bool, value: object, requirement: str, note: str = "") -> None:
    rows.append(
        {
            "check": name,
            "status": "PASS" if passed else "FAIL",
            "value": value,
            "requirement": requirement,
            "note": note,
        }
    )


df = pd.read_csv(INPUT_PATH)

# --- structure ---
missing_cols = [c for c in REQUIRED if c not in df.columns]
check("required_columns_present", not missing_cols, missing_cols or "all present",
      "Y, D, W, keys, wage_region all in panel")

check("n_obs", len(df) == 441, len(df), "441 obs (63 provinces x 7 years)")
check("n_provinces", df["province"].nunique() == 63, df["province"].nunique(), "63")
check("years", sorted(df["year"].unique().tolist()) == list(range(2018, 2025)),
      f"{df['year'].min()}-{df['year'].max()}", "2018-2024")

dups = int(df.duplicated(subset=KEYS).sum())
check("duplicate_province_year", dups == 0, dups, "0 duplicates")

balance = df.groupby("province")["year"].count()
check("balanced_panel", bool((balance == 7).all()),
      f"min={balance.min()}, max={balance.max()}", "every province has 7 years")

# --- missing values ---
for col in [Y_COL, *TREATMENTS, *CONTROLS]:
    n_miss = int(df[col].isna().sum())
    check(f"missing[{col}]", n_miss == 0, n_miss, "0 missing")

# --- ranges / scale ---
check("informal_rate_range",
      bool(df[Y_COL].between(0, 100).all()),
      f"[{df[Y_COL].min():.2f}, {df[Y_COL].max():.2f}]",
      "0-100 (percentage points)")
check("real_min_wage_positive", bool((df["real_min_wage"] > 0).all()),
      f"[{df['real_min_wage'].min():.0f}, {df['real_min_wage'].max():.0f}]", "> 0 VND/month")

log_consistent = np.allclose(df["log_real_min_wage"], np.log(df["real_min_wage"]), atol=1e-6)
check("log_real_min_wage_consistent", log_consistent, log_consistent,
      "log_real_min_wage == ln(real_min_wage)")

growth_2018_zero = bool((df.loc[df["year"] == 2018, "min_wage_growth"] == 0).all())
check("min_wage_growth_base_year", growth_2018_zero, growth_2018_zero,
      "2018 = 0 (base year)", "growth is year-over-year change of log real wage" )

# --- treatment variation (critical gate for CRF) ---
for t in TREATMENTS:
    overall_sd = df[t].std()
    within_year_sd = df.groupby("year")[t].transform(lambda s: s - s.mean()).std()
    within_prov_sd = df.groupby("province")[t].transform(lambda s: s - s.mean()).std()
    n_unique = df[t].nunique()
    check(
        f"variation[{t}]",
        overall_sd > 0 and n_unique > 10,
        f"sd={overall_sd:.4g}, within-year sd={within_year_sd:.4g}, "
        f"within-province sd={within_prov_sd:.4g}, n_unique={n_unique}",
        "non-degenerate variation",
        "within-year variation comes from 4 wage regions; within-province from time changes",
    )

# --- scale summary for W (documentation, always PASS) ---
for col in CONTROLS:
    s = df[col]
    check(f"scale[{col}]", True,
          f"mean={s.mean():.3g}, sd={s.std():.3g}, range=[{s.min():.3g}, {s.max():.3g}]",
          "documented for learner scaling")

# --- collinearity guard ---
corr = df["employed_persons"].corr(np.exp(df["log_employed_persons"]))
check("employed_vs_log_not_both", True, f"corr(level, exp(log))={corr:.4f}",
      "main spec must use only log_employed_persons",
      "level variable exists in panel but is excluded from W")

out = pd.DataFrame(rows)
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
out.to_csv(OUTPUT_PATH, index=False)

n_fail = int((out["status"] == "FAIL").sum())
print(out.to_string(index=False, max_colwidth=70))
print(f"\nFAILED checks: {n_fail}")
print("GATE:", "OK to run enhanced nonlinearity + CRF" if n_fail == 0 else "DO NOT run CRF - fix failures first")
