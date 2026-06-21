from __future__ import annotations

import pandas as pd

from policy_pipeline_utils import (
    PROJECT_ROOT,
    WAGE_REGIONS,
    draw_distribution_by_region,
    draw_line_chart,
    log,
    print_panel_diagnostics,
)


STEP = "treatment-variation"
INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "final" / "analysis_panel_2018_2024.csv"
FIGURE_DIR = PROJECT_ROOT / "reports" / "figures" / "treatment_variation"
SUMMARY_PATH = PROJECT_ROOT / "reports" / "tables" / "treatment_variation_summary.csv"


def main() -> None:
    data = pd.read_csv(INPUT_PATH)
    print_panel_diagnostics(data, ["province", "year"], STEP)

    unique_region_year = data[
        ["year", "wage_region", "min_wage_nominal", "real_min_wage", "log_real_min_wage", "min_wage_growth"]
    ].drop_duplicates()

    draw_line_chart(
        unique_region_year,
        "min_wage_nominal",
        "Nominal minimum wage by wage region over time",
        FIGURE_DIR / "min_wage_nominal_by_region_over_time.png",
    )
    draw_line_chart(
        unique_region_year,
        "real_min_wage",
        "Real minimum wage by wage region over time, 2018 CPI base",
        FIGURE_DIR / "real_min_wage_by_region_over_time.png",
    )
    draw_distribution_by_region(
        data,
        "real_min_wage",
        "Real minimum wage distribution by wage region",
        FIGURE_DIR / "real_min_wage_distribution_by_region.png",
    )

    rows: list[dict[str, object]] = []
    for variable in ["min_wage_nominal", "real_min_wage", "log_real_min_wage", "min_wage_growth"]:
        values = unique_region_year[variable]
        rows.extend(
            [
                {"section": "summary_stats", "variable": variable, "metric": "min", "value": values.min(), "note": "computed on unique wage_region-year values"},
                {"section": "summary_stats", "variable": variable, "metric": "max", "value": values.max(), "note": "computed on unique wage_region-year values"},
                {"section": "summary_stats", "variable": variable, "metric": "mean", "value": values.mean(), "note": "computed on unique wage_region-year values"},
                {"section": "summary_stats", "variable": variable, "metric": "std", "value": values.std(), "note": "computed on unique wage_region-year values"},
            ]
        )

    rows.append(
        {
            "section": "variation_source",
            "variable": "real_min_wage",
            "metric": "unique_values_by_year",
            "value": unique_region_year.groupby("year")["real_min_wage"].nunique().to_dict(),
            "note": "within each year, variation comes from wage_region differences",
        }
    )
    rows.append(
        {
            "section": "variation_source",
            "variable": "real_min_wage",
            "metric": "unique_values_by_region",
            "value": unique_region_year.groupby("wage_region")["real_min_wage"].nunique().to_dict(),
            "note": "within each wage_region, variation comes from year changes and CPI adjustment",
        }
    )
    rows.append(
        {
            "section": "variation_source",
            "variable": "wage_region",
            "metric": "province_count_by_region",
            "value": data.drop_duplicates(["province", "wage_region"]).groupby("wage_region")["province"].nunique().reindex(WAGE_REGIONS).to_dict(),
            "note": "province-region pairs across all years; counts are not mutually exclusive if a province changes region",
        }
    )
    switching = data.groupby("province")["wage_region"].nunique()
    switching_provinces = sorted(switching.loc[switching > 1].index.tolist())
    rows.append(
        {
            "section": "variation_source",
            "variable": "wage_region",
            "metric": "provinces_switching_region",
            "value": len(switching_provinces),
            "note": f"province-level wage_region changes over time: {switching_provinces}",
        }
    )
    region_counts_by_year = (
        data.groupby(["year", "wage_region"])["province"]
        .nunique()
        .unstack(fill_value=0)
        .reindex(columns=WAGE_REGIONS)
        .to_dict(orient="index")
    )
    rows.append(
        {
            "section": "variation_source",
            "variable": "wage_region",
            "metric": "region_counts_by_year",
            "value": region_counts_by_year,
            "note": "province counts assigned to each wage_region by year",
        }
    )
    rows.append(
        {
            "section": "interpretation",
            "variable": "treatment",
            "metric": "main_source",
            "value": "year and wage_region",
            "note": "Treatment variation is mainly by policy year and minimum-wage region, not by individuals.",
        }
    )

    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(SUMMARY_PATH, index=False)
    log(STEP, f"Wrote {SUMMARY_PATH.relative_to(PROJECT_ROOT)}")
    log(STEP, f"Wrote figures to {FIGURE_DIR.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
