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


STEP = "build-region-map"
RAW_PATH = PROJECT_ROOT / "data" / "raw" / "policy" / "province_wage_region_map_raw_2018_2024.csv"
PANEL_PATH = PROJECT_ROOT / "data" / "processed" / "nso_employment" / "province_year_panel_2018_2024.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "policy" / "province_wage_region_map.csv"
VALIDATION_PATH = PROJECT_ROOT / "reports" / "tables" / "province_wage_region_map_validation.csv"
NOTE_PATH = PROJECT_ROOT / "reports" / "province_wage_region_mapping_notes.md"


def main() -> None:
    panel = pd.read_csv(PANEL_PATH)
    panel["year"] = numeric_series(panel["year"]).astype("Int64")

    data = read_csv_with_header_detection(
        RAW_PATH, ["province", "year", "wage_region", "mapping_note", "source"]
    )
    data["year"] = numeric_series(data["year"]).astype("Int64")
    data["wage_region"] = data["wage_region"].map(normalize_region)
    data = data[["province", "year", "wage_region", "mapping_note", "source"]]
    data = data.sort_values(["province", "year"]).reset_index(drop=True)

    rows: list[dict[str, object]] = []
    add_check(rows, "province_wage_region_map", "shape", len(data) == 441, f"rows={len(data)}")
    add_check(rows, "province_wage_region_map", "province_count", data["province"].nunique() == 63, f"province_count={data['province'].nunique()}")
    add_check(rows, "province_wage_region_map", "year_count", data["year"].nunique() == 7, f"year_count={data['year'].nunique()}")
    add_check(rows, "province_wage_region_map", "year_set", set(data["year"].dropna().astype(int)) == set(YEARS), f"years={sorted(data['year'].dropna().unique().tolist())}")
    add_check(rows, "province_wage_region_map", "duplicate_province_year", data.duplicated(["province", "year"]).sum() == 0, f"duplicates={int(data.duplicated(['province', 'year']).sum())}")
    add_check(rows, "province_wage_region_map", "missing_wage_region", data["wage_region"].isna().sum() == 0, f"missing={int(data['wage_region'].isna().sum())}")
    invalid = sorted(set(data["wage_region"]) - set(WAGE_REGIONS))
    add_check(rows, "province_wage_region_map", "invalid_wage_region", len(invalid) == 0, f"invalid={invalid}")

    panel_keys = set(zip(panel["province"], panel["year"].astype(int)))
    map_keys = set(zip(data["province"], data["year"].astype(int)))
    panel_not_in_map = sorted(panel_keys - map_keys)
    map_not_in_panel = sorted(map_keys - panel_keys)
    add_check(rows, "province_wage_region_map", "panel_keys_not_in_mapping", len(panel_not_in_map) == 0, f"count={len(panel_not_in_map)}; examples={panel_not_in_map[:10]}")
    add_check(rows, "province_wage_region_map", "mapping_keys_not_in_panel", len(map_not_in_panel) == 0, f"count={len(map_not_in_panel)}; examples={map_not_in_panel[:10]}")

    needs_verification = data["mapping_note"].astype(str).str.contains("needs verification", case=False, na=False)
    mixed = data["mapping_note"].astype(str).str.contains("mixed district regions", case=False, na=False)
    add_check(rows, "province_wage_region_map", "needs_verification_rows_reported", True, f"rows={int(needs_verification.sum())}")
    add_check(rows, "province_wage_region_map", "mixed_district_rows_reported", True, f"rows={int(mixed.sum())}")

    require_no_failed_checks(rows)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(OUTPUT_PATH, index=False)
    write_checks(VALIDATION_PATH, rows)

    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.write_text(
        "# Province Wage Region Mapping Notes\n\n"
        "- This mapping is a province-level approximation used to merge regional minimum wages into the province-year panel.\n"
        "- Vietnam's regional minimum wage is officially applied at district/urban district/town/provincial-city areas, not always at the whole-province level.\n"
        "- Because the current research dataset is province-year aggregate data, this mapping assigns one wage region to each province-year.\n"
        "- If a province contains districts in multiple wage regions, the assigned wage region is an approximation and should be treated as a data limitation.\n"
        f"- Rows with `needs verification` in `mapping_note`: {int(needs_verification.sum())}.\n"
        f"- Rows flagged as mixed district regions: {int(mixed.sum())}.\n",
        encoding="utf-8",
    )

    print_panel_diagnostics(data, ["province", "year"], STEP)
    print(f"Wrote {OUTPUT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {NOTE_PATH.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
