from __future__ import annotations

from pathlib import Path

import pandas as pd

from policy_pipeline_utils import (
    PROJECT_ROOT,
    WAGE_REGIONS,
    YEARS,
    add_check,
    normalize_region,
    numeric_series,
    read_csv_with_header_detection,
    require_no_failed_checks,
    write_checks,
)


STEP = "validate-raw-policy"
PANEL_PATH = PROJECT_ROOT / "data" / "processed" / "nso_employment" / "province_year_panel_2018_2024.csv"
MIN_WAGE_RAW = PROJECT_ROOT / "data" / "raw" / "policy" / "min_wage_region_raw_2018_2024.csv"
MAP_RAW = PROJECT_ROOT / "data" / "raw" / "policy" / "province_wage_region_map_raw_2018_2024.csv"
CPI_RAW = PROJECT_ROOT / "data" / "raw" / "economy" / "cpi_raw_2018_2024.csv"
VALIDATION_PATH = PROJECT_ROOT / "reports" / "tables" / "raw_policy_input_validation.csv"


def same_set(values: set, expected: set) -> tuple[bool, str]:
    missing = sorted(expected - values)
    extra = sorted(values - expected)
    return not missing and not extra, f"missing={missing}; extra={extra}"


def main() -> None:
    rows: list[dict[str, object]] = []
    panel = pd.read_csv(PANEL_PATH)
    min_wage = read_csv_with_header_detection(
        MIN_WAGE_RAW,
        ["year", "wage_region", "min_wage_nominal", "effective_date", "decree", "note"],
    )
    mapping = read_csv_with_header_detection(
        MAP_RAW, ["province", "year", "wage_region", "mapping_note", "source"]
    )
    cpi = read_csv_with_header_detection(CPI_RAW, ["year", "cpi_index"])

    panel["year"] = numeric_series(panel["year"]).astype("Int64")
    min_wage["year"] = numeric_series(min_wage["year"]).astype("Int64")
    min_wage["wage_region"] = min_wage["wage_region"].map(normalize_region)
    min_wage["min_wage_nominal"] = numeric_series(min_wage["min_wage_nominal"])
    mapping["year"] = numeric_series(mapping["year"]).astype("Int64")
    mapping["wage_region"] = mapping["wage_region"].map(normalize_region)
    cpi["year"] = numeric_series(cpi["year"]).astype("Int64")
    cpi["cpi_index"] = numeric_series(cpi["cpi_index"])

    print("\nRaw policy input validation")
    print("=" * 80)

    add_check(rows, "panel", "shape", panel.shape == (441, 7), f"shape={panel.shape}")
    add_check(rows, "panel", "province_count", panel["province"].nunique() == 63, f"province_count={panel['province'].nunique()}")
    add_check(rows, "panel", "year_set", set(panel["year"].dropna().astype(int)) == set(YEARS), f"years={sorted(panel['year'].dropna().unique().tolist())}")
    add_check(rows, "panel", "duplicate_province_year", panel.duplicated(["province", "year"]).sum() == 0, f"duplicates={int(panel.duplicated(['province', 'year']).sum())}")
    add_check(rows, "panel", "missing", panel.isna().sum().sum() == 0, f"missing_total={int(panel.isna().sum().sum())}")

    required_mw = {"year", "wage_region", "min_wage_nominal", "effective_date", "decree", "note"}
    add_check(rows, "min_wage_raw", "required_columns", required_mw.issubset(min_wage.columns), f"columns={list(min_wage.columns)}")
    add_check(rows, "min_wage_raw", "shape", len(min_wage) == 28, f"rows={len(min_wage)}")
    ok, detail = same_set(set(min_wage["year"].dropna().astype(int)), set(YEARS))
    add_check(rows, "min_wage_raw", "year_set", ok, detail)
    region_counts = min_wage.groupby("year")["wage_region"].apply(lambda s: sorted(set(s))).to_dict()
    add_check(rows, "min_wage_raw", "four_regions_each_year", all(v == WAGE_REGIONS for v in region_counts.values()), f"regions_by_year={region_counts}")
    invalid_regions = sorted(set(min_wage["wage_region"]) - set(WAGE_REGIONS))
    add_check(rows, "min_wage_raw", "valid_wage_regions", len(invalid_regions) == 0, f"invalid_regions={invalid_regions}")
    add_check(rows, "min_wage_raw", "min_wage_numeric_nonmissing", min_wage["min_wage_nominal"].notna().all(), f"missing={int(min_wage['min_wage_nominal'].isna().sum())}")
    add_check(rows, "min_wage_raw", "duplicate_year_region", min_wage.duplicated(["year", "wage_region"]).sum() == 0, f"duplicates={int(min_wage.duplicated(['year', 'wage_region']).sum())}")

    required_map = {"province", "year", "wage_region", "mapping_note", "source"}
    add_check(rows, "mapping_raw", "required_columns", required_map.issubset(mapping.columns), f"columns={list(mapping.columns)}")
    add_check(rows, "mapping_raw", "shape", len(mapping) == 441, f"rows={len(mapping)}")
    add_check(rows, "mapping_raw", "province_count", mapping["province"].nunique() == 63, f"province_count={mapping['province'].nunique()}")
    ok, detail = same_set(set(mapping["year"].dropna().astype(int)), set(YEARS))
    add_check(rows, "mapping_raw", "year_set", ok, detail)
    add_check(rows, "mapping_raw", "duplicate_province_year", mapping.duplicated(["province", "year"]).sum() == 0, f"duplicates={int(mapping.duplicated(['province', 'year']).sum())}")
    add_check(rows, "mapping_raw", "missing_wage_region", mapping["wage_region"].isna().sum() == 0, f"missing={int(mapping['wage_region'].isna().sum())}")
    invalid_regions = sorted(set(mapping["wage_region"]) - set(WAGE_REGIONS))
    add_check(rows, "mapping_raw", "valid_wage_regions", len(invalid_regions) == 0, f"invalid_regions={invalid_regions}")
    panel_provinces = set(panel["province"])
    mapping_provinces = set(mapping["province"])
    add_check(rows, "mapping_raw", "province_names_match_panel", panel_provinces == mapping_provinces, f"panel_not_in_mapping={sorted(panel_provinces - mapping_provinces)}; mapping_not_in_panel={sorted(mapping_provinces - panel_provinces)}")
    panel_keys = set(zip(panel["province"], panel["year"].astype(int)))
    mapping_keys = set(zip(mapping["province"], mapping["year"].astype(int)))
    add_check(rows, "mapping_raw", "province_year_keys_match_panel", panel_keys == mapping_keys, f"panel_not_in_mapping={len(panel_keys - mapping_keys)}; mapping_not_in_panel={len(mapping_keys - panel_keys)}")

    required_cpi = {"year", "cpi_index"}
    add_check(rows, "cpi_raw", "required_columns", required_cpi.issubset(cpi.columns), f"columns={list(cpi.columns)}")
    add_check(rows, "cpi_raw", "shape", len(cpi) == 7, f"rows={len(cpi)}")
    ok, detail = same_set(set(cpi["year"].dropna().astype(int)), set(YEARS))
    add_check(rows, "cpi_raw", "year_set", ok, detail)
    add_check(rows, "cpi_raw", "cpi_numeric_nonmissing", cpi["cpi_index"].notna().all(), f"missing={int(cpi['cpi_index'].isna().sum())}")
    add_check(rows, "cpi_raw", "duplicate_year", cpi.duplicated(["year"]).sum() == 0, f"duplicates={int(cpi.duplicated(['year']).sum())}")

    write_checks(VALIDATION_PATH, rows)
    print(f"\nWrote {VALIDATION_PATH.relative_to(PROJECT_ROOT)}")
    require_no_failed_checks(rows)


if __name__ == "__main__":
    main()
