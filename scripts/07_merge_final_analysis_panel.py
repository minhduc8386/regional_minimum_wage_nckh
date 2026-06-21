from __future__ import annotations

import numpy as np
import pandas as pd

from policy_pipeline_utils import PROJECT_ROOT, add_check, print_panel_diagnostics, require_no_failed_checks, write_checks


STEP = "merge-final-panel"
PANEL_PATH = PROJECT_ROOT / "data" / "processed" / "nso_employment" / "province_year_panel_2018_2024.csv"
MAP_PATH = PROJECT_ROOT / "data" / "processed" / "policy" / "province_wage_region_map.csv"
MIN_WAGE_PATH = PROJECT_ROOT / "data" / "processed" / "policy" / "min_wage_region_panel.csv"
CPI_PATH = PROJECT_ROOT / "data" / "processed" / "economy" / "cpi_panel.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "final" / "analysis_panel_2018_2024.csv"
VALIDATION_PATH = PROJECT_ROOT / "reports" / "tables" / "final_analysis_panel_validation.csv"

FINAL_COLUMNS = [
    "province",
    "year",
    "wage_region",
    "informal_rate",
    "min_wage_nominal",
    "cpi_index",
    "cpi_2018_base",
    "real_min_wage",
    "log_real_min_wage",
    "min_wage_growth",
    "unemployment_rate",
    "labour_productivity",
    "trained_labour_rate",
    "employed_persons",
    "log_employed_persons",
]


def main() -> None:
    panel = pd.read_csv(PANEL_PATH)
    mapping = pd.read_csv(MAP_PATH)
    min_wage = pd.read_csv(MIN_WAGE_PATH)
    cpi = pd.read_csv(CPI_PATH)

    for frame in [panel, mapping, min_wage, cpi]:
        frame["year"] = frame["year"].astype(int)

    if (panel["employed_persons"] <= 0).any():
        bad = panel.loc[panel["employed_persons"] <= 0, ["province", "year", "employed_persons"]]
        raise RuntimeError(f"Cannot log employed_persons because non-positive values exist:\n{bad.to_string(index=False)}")

    wage_region_year = min_wage.merge(cpi[["year", "cpi_index", "cpi_2018_base"]], on="year", how="left", validate="many_to_one")
    wage_region_year["real_min_wage"] = wage_region_year["min_wage_nominal"] / wage_region_year["cpi_2018_base"] * 100
    wage_region_year = wage_region_year.sort_values(["wage_region", "year"]).reset_index(drop=True)
    wage_region_year["min_wage_growth"] = wage_region_year.groupby("wage_region")["real_min_wage"].pct_change()
    wage_region_year["min_wage_growth"] = wage_region_year["min_wage_growth"].fillna(0.0)

    merged = panel.merge(
        mapping[["province", "year", "wage_region"]],
        on=["province", "year"],
        how="left",
        validate="one_to_one",
    )
    merged = merged.merge(
        wage_region_year[["year", "wage_region", "min_wage_nominal", "cpi_index", "cpi_2018_base", "real_min_wage", "min_wage_growth"]],
        on=["year", "wage_region"],
        how="left",
        validate="many_to_one",
    )
    merged["log_real_min_wage"] = np.log(merged["real_min_wage"])
    merged["log_employed_persons"] = np.log(merged["employed_persons"])
    merged = merged[FINAL_COLUMNS].sort_values(["province", "year"]).reset_index(drop=True)

    rows: list[dict[str, object]] = []
    add_check(rows, "analysis_panel", "shape_rows", len(merged) == 441, f"rows={len(merged)}")
    add_check(rows, "analysis_panel", "province_count", merged["province"].nunique() == 63, f"province_count={merged['province'].nunique()}")
    add_check(rows, "analysis_panel", "year_count", merged["year"].nunique() == 7, f"year_count={merged['year'].nunique()}")
    add_check(rows, "analysis_panel", "duplicate_province_year", merged.duplicated(["province", "year"]).sum() == 0, f"duplicates={int(merged.duplicated(['province', 'year']).sum())}")
    for col in ["wage_region", "min_wage_nominal", "cpi_2018_base", "real_min_wage", "log_real_min_wage", "log_employed_persons"]:
        missing = int(merged[col].isna().sum())
        add_check(rows, "analysis_panel", f"missing_{col}", missing == 0, f"missing={missing}")
    add_check(rows, "analysis_panel", "missing_min_wage_growth", merged["min_wage_growth"].isna().sum() == 0, f"missing={int(merged['min_wage_growth'].isna().sum())}; 2018 filled with 0 by wage_region")

    failed = [row for row in rows if row["status"] == "FAIL"]
    if failed:
        bad_cols = ["province", "year", "wage_region", "min_wage_nominal", "cpi_2018_base", "real_min_wage"]
        bad = merged.loc[merged[bad_cols].isna().any(axis=1), bad_cols]
        if not bad.empty:
            print("\nProblem province-year rows:")
            print(bad.to_string(index=False))
        write_checks(VALIDATION_PATH, rows)
        require_no_failed_checks(rows)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(OUTPUT_PATH, index=False)
    write_checks(VALIDATION_PATH, rows)
    print_panel_diagnostics(merged, ["province", "year"], STEP)
    print(f"Wrote {OUTPUT_PATH.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
