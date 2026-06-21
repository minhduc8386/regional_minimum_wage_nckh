from __future__ import annotations

import numpy as np

from policy_pipeline_utils import (
    PROJECT_ROOT,
    YEARS,
    add_check,
    numeric_series,
    print_panel_diagnostics,
    read_csv_with_header_detection,
    require_no_failed_checks,
    write_checks,
)


STEP = "build-cpi"
RAW_PATH = PROJECT_ROOT / "data" / "raw" / "economy" / "cpi_raw_2018_2024.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "economy" / "cpi_panel.csv"
VALIDATION_PATH = PROJECT_ROOT / "reports" / "tables" / "cpi_panel_validation.csv"


def main() -> None:
    data = read_csv_with_header_detection(RAW_PATH, ["year", "cpi_index"])
    data["year"] = numeric_series(data["year"]).astype("Int64")
    data["cpi_index"] = numeric_series(data["cpi_index"])

    cpi_2018 = data.loc[data["year"] == 2018, "cpi_index"]
    if len(cpi_2018) != 1 or cpi_2018.isna().any() or float(cpi_2018.iloc[0]) <= 0:
        raise RuntimeError("CPI panel must contain exactly one valid CPI value for 2018.")
    data["cpi_2018_base"] = data["cpi_index"] / float(cpi_2018.iloc[0]) * 100

    columns = ["year", "cpi_index", "cpi_2018_base"]
    for optional in ["source", "note"]:
        if optional in data.columns:
            columns.append(optional)
    data = data[columns].sort_values("year").reset_index(drop=True)

    rows: list[dict[str, object]] = []
    add_check(rows, "cpi_panel", "shape", len(data) == 7, f"rows={len(data)}")
    add_check(rows, "cpi_panel", "year_set", set(data["year"].dropna().astype(int)) == set(YEARS), f"years={sorted(data['year'].dropna().unique().tolist())}")
    add_check(rows, "cpi_panel", "missing", data[["year", "cpi_index", "cpi_2018_base"]].isna().sum().sum() == 0, f"missing={data[['year', 'cpi_index', 'cpi_2018_base']].isna().sum().to_dict()}")
    add_check(rows, "cpi_panel", "duplicate_year", data.duplicated(["year"]).sum() == 0, f"duplicates={int(data.duplicated(['year']).sum())}")
    base_2018 = float(data.loc[data["year"] == 2018, "cpi_2018_base"].iloc[0])
    add_check(rows, "cpi_panel", "base_2018_equals_100", np.isclose(base_2018, 100.0), f"cpi_2018_base={base_2018}")

    require_no_failed_checks(rows)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(OUTPUT_PATH, index=False)
    write_checks(VALIDATION_PATH, rows)
    print_panel_diagnostics(data, ["year"], STEP)
    print(f"Wrote {OUTPUT_PATH.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
