from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = PROJECT_ROOT / "reports" / "project_completion_summary.md"

FILES_TO_CHECK = [
    "data/processed/nso_employment/province_year_panel_2018_2024.csv",
    "data/processed/policy/min_wage_region_panel.csv",
    "data/processed/policy/province_wage_region_map.csv",
    "data/processed/economy/cpi_panel.csv",
    "data/processed/final/analysis_panel_2018_2024.csv",
    "reports/tables/final_analysis_panel_validation.csv",
    "reports/tables/treatment_variation_summary.csv",
    "reports/tables/nonlinearity_summary_final.csv",
    "reports/tables/model_comparison_linear_vs_ml_final.csv",
]

SCRIPTS_TO_CHECK = [
    "scripts/01_clean_nso_province_panel.py",
    "scripts/02_check_nonlinearity.py",
    "scripts/03_validate_raw_policy_inputs.py",
    "scripts/04_build_min_wage_region_panel.py",
    "scripts/05_build_province_wage_region_map.py",
    "scripts/06_build_cpi_panel.py",
    "scripts/07_merge_final_analysis_panel.py",
    "scripts/08_check_treatment_variation.py",
    "scripts/09_check_nonlinearity_with_treatment.py",
    "scripts/10_model_comparison_with_treatment.py",
    "scripts/11_generate_project_completion_summary.py",
]


def exists(path: str) -> str:
    return "OK" if (PROJECT_ROOT / path).exists() else "MISSING"


def read_csv(path: str) -> pd.DataFrame | None:
    full_path = PROJECT_ROOT / path
    if not full_path.exists():
        return None
    return pd.read_csv(full_path)


def inventory_section() -> str:
    lines = ["## File Inventory", "", "| file | status |", "|---|---|"]
    for path in FILES_TO_CHECK:
        lines.append(f"| `{path}` | {exists(path)} |")
    lines.extend(["", "## Scripts", "", "| script | status |", "|---|---|"])
    for path in SCRIPTS_TO_CHECK:
        lines.append(f"| `{path}` | {exists(path)} |")
    return "\n".join(lines)


def final_panel_section() -> str:
    panel = read_csv("data/processed/final/analysis_panel_2018_2024.csv")
    if panel is None:
        return "## Final Panel\n\nFinal panel is missing."

    years = ", ".join(str(int(year)) for year in sorted(panel["year"].unique()))
    columns = ", ".join(f"`{col}`" for col in panel.columns)
    return f"""## Final Panel

- Path: `data/processed/final/analysis_panel_2018_2024.csv`
- Shape: `{panel.shape[0]} x {panel.shape[1]}`
- Provinces: `{panel["province"].nunique()}`
- Years: `{years}`
- Duplicate `province-year`: `{int(panel.duplicated(["province", "year"]).sum())}`
- Missing values total: `{int(panel.isna().sum().sum())}`
- Columns: {columns}

Research variables:

- Y: `informal_rate`
- D: `real_min_wage`, `log_real_min_wage`, `min_wage_growth`
- W: `unemployment_rate`, `labour_productivity`, `trained_labour_rate`, `employed_persons`, `log_employed_persons`
"""


def treatment_section() -> str:
    panel = read_csv("data/processed/final/analysis_panel_2018_2024.csv")
    mapping = read_csv("data/processed/policy/province_wage_region_map.csv")
    if panel is None:
        return "## Treatment\n\nTreatment variables are missing."

    stats = panel[["min_wage_nominal", "real_min_wage", "log_real_min_wage", "min_wage_growth"]].describe().T
    lines = [
        "## Treatment",
        "",
        "- `real_min_wage = min_wage_nominal / cpi_2018_base * 100`",
        "- `log_real_min_wage = log(real_min_wage)`",
        "- `min_wage_growth` is computed by wage region over time; 2018 is filled as 0.",
        "",
        "| variable | min | mean | max | std |",
        "|---|---:|---:|---:|---:|",
    ]
    for variable, row in stats.iterrows():
        lines.append(
            f"| `{variable}` | {row['min']:.3f} | {row['mean']:.3f} | {row['max']:.3f} | {row['std']:.3f} |"
        )

    if mapping is not None:
        needs_verification = mapping["mapping_note"].astype(str).str.contains("needs verification", case=False, na=False).sum()
        mixed = mapping["mapping_note"].astype(str).str.contains("mixed district regions", case=False, na=False).sum()
        switching = panel.groupby("province")["wage_region"].nunique()
        switching_provinces = sorted(switching.loc[switching > 1].index.tolist())
        lines.extend(
            [
                "",
                f"- Mapping rows with `needs verification`: `{int(needs_verification)}`",
                f"- Mapping rows flagged as mixed district regions: `{int(mixed)}`",
                f"- Provinces switching wage region over time: `{len(switching_provinces)}`",
                f"- Switching provinces: {', '.join(switching_provinces) if switching_provinces else 'None'}",
            ]
        )
    return "\n".join(lines)


def nonlinearity_section() -> str:
    summary = read_csv("reports/tables/nonlinearity_summary_final.csv")
    if summary is None:
        return "## Nonlinearity\n\nFinal nonlinearity table is missing."

    lines = ["## Nonlinearity", "", "| variable | type | pattern | conclusion |", "|---|---|---|---|"]
    for row in summary.itertuples(index=False):
        lines.append(f"| `{row.variable}` | {row.relationship_type} | {row.lowess_pattern} | {row.conclusion} |")
    return "\n".join(lines)


def model_section() -> str:
    models = read_csv("reports/tables/model_comparison_linear_vs_ml_final.csv")
    if models is None:
        return "## Model Comparison\n\nModel comparison table is missing."

    lines = [
        "## Model Comparison",
        "",
        "Predictive diagnostic only; not a causal estimate.",
        "",
        "| model | RMSE | MAE | R2 |",
        "|---|---:|---:|---:|",
    ]
    for row in models.itertuples(index=False):
        lines.append(f"| `{row.model}` | {row.rmse:.3f} | {row.mae:.3f} | {row.r2:.3f} |")
    if "overall_conclusion" in models.columns and not models.empty:
        lines.extend(["", f"Conclusion: {models['overall_conclusion'].iloc[0]}"])
    return "\n".join(lines)


def limitations_section() -> str:
    return """## Limitations

- Current data are aggregate province-year data, not individual microdata.
- Province-to-wage-region mapping is an approximation.
- Vietnam's regional minimum wage is applied at district/town/provincial-city level, not uniformly at province level.
- LOWESS and model comparison are diagnostics, not causal estimates.
- DML has not been run as a causal model yet.
"""


def main() -> None:
    content = "\n\n".join(
        [
            "# Project Completion Summary",
            f"Generated at: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`",
            inventory_section(),
            final_panel_section(),
            treatment_section(),
            nonlinearity_section(),
            model_section(),
            limitations_section(),
        ]
    )
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(content + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
