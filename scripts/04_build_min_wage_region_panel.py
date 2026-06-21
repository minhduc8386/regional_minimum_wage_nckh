from __future__ import annotations

import pandas as pd

from policy_pipeline_utils import (
    PROJECT_ROOT,
    WAGE_REGIONS,
    YEARS,
    add_check,
    normalize_region,
    numeric_series,
    print_panel_diagnostics,
    read_csv_with_header_detection,
    require_no_failed_checks,
    write_checks,
)


STEP = "build-min-wage"
RAW_PATH = PROJECT_ROOT / "data" / "raw" / "policy" / "min_wage_region_raw_2018_2024.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "policy" / "min_wage_region_panel.csv"
VALIDATION_PATH = PROJECT_ROOT / "reports" / "tables" / "min_wage_region_panel_validation.csv"


def main() -> None:
    data = read_csv_with_header_detection(
        RAW_PATH,
        ["year", "wage_region", "min_wage_nominal", "effective_date", "decree", "note"],
    )
    data["year"] = numeric_series(data["year"]).astype("Int64")
    data["wage_region"] = data["wage_region"].map(normalize_region)
    data["min_wage_nominal"] = numeric_series(data["min_wage_nominal"]).round().astype("Int64")

    columns = ["year", "wage_region", "min_wage_nominal", "effective_date", "decree", "note"]
    if "source" in data.columns:
        columns.append("source")
    data = data[columns].sort_values(["year", "wage_region"]).reset_index(drop=True)

    rows: list[dict[str, object]] = []
    add_check(rows, "min_wage_panel", "shape", len(data) == 28, f"rows={len(data)}")
    add_check(rows, "min_wage_panel", "year_count", data["year"].nunique() == 7, f"year_count={data['year'].nunique()}")
    add_check(rows, "min_wage_panel", "year_set", set(data["year"].dropna().astype(int)) == set(YEARS), f"years={sorted(data['year'].dropna().unique().tolist())}")
    region_counts = data.groupby("year")["wage_region"].apply(lambda s: sorted(set(s))).to_dict()
    add_check(rows, "min_wage_panel", "four_regions_each_year", all(v == WAGE_REGIONS for v in region_counts.values()), f"regions_by_year={region_counts}")
    add_check(rows, "min_wage_panel", "duplicate_year_region", data.duplicated(["year", "wage_region"]).sum() == 0, f"duplicates={int(data.duplicated(['year', 'wage_region']).sum())}")
    add_check(rows, "min_wage_panel", "required_missing", data[["year", "wage_region", "min_wage_nominal"]].isna().sum().sum() == 0, f"missing={data[['year', 'wage_region', 'min_wage_nominal']].isna().sum().to_dict()}")
    invalid = sorted(set(data["wage_region"]) - set(WAGE_REGIONS))
    add_check(rows, "min_wage_panel", "valid_wage_regions", len(invalid) == 0, f"invalid={invalid}")

    require_no_failed_checks(rows)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(OUTPUT_PATH, index=False)
    write_checks(VALIDATION_PATH, rows)
    print_panel_diagnostics(data, ["year", "wage_region"], STEP)
    print(f"Wrote {OUTPUT_PATH.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
