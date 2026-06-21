from __future__ import annotations

import pandas as pd

from policy_pipeline_utils import PROJECT_ROOT, draw_lowess_plot, log, print_panel_diagnostics


STEP = "nonlinearity-final"
INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "final" / "analysis_panel_2018_2024.csv"
FIGURE_DIR = PROJECT_ROOT / "reports" / "figures" / "nonlinearity_final"
SUMMARY_PATH = PROJECT_ROOT / "reports" / "tables" / "nonlinearity_summary_final.csv"
Y_COL = "informal_rate"
VARIABLES = [
    "min_wage_nominal",
    "real_min_wage",
    "log_real_min_wage",
    "min_wage_growth",
    "unemployment_rate",
    "labour_productivity",
    "trained_labour_rate",
    "employed_persons",
    "log_employed_persons",
]
TREATMENT_VARIABLES = {"min_wage_nominal", "real_min_wage", "log_real_min_wage", "min_wage_growth"}


def interpretation(pattern: str) -> str:
    if "insufficient" in pattern or "not enough" in pattern:
        return "LOWESS is not reliable because the variable has too little usable variation."
    if "flat outcome" in pattern:
        return "The outcome has no observed variation, so curvature cannot be assessed."
    if "visibly curved" in pattern:
        return "LOWESS departs clearly from a straight line, suggesting non-linear association."
    if "mildly curved" in pattern:
        return "LOWESS shows mild curvature, suggesting possible non-linear association."
    return "LOWESS is close to a straight line in the current aggregate panel."


def conclusion(pattern: str) -> str:
    if "visibly curved" in pattern:
        return "possible non-linearity"
    if "mildly curved" in pattern:
        return "weak-to-moderate possible non-linearity"
    if "approximately linear" in pattern:
        return "weak visual evidence of non-linearity"
    return "cannot assess non-linearity"


def main() -> None:
    data = pd.read_csv(INPUT_PATH)
    print_panel_diagnostics(data, ["province", "year"], STEP)

    rows: list[dict[str, object]] = []
    for variable in VARIABLES:
        log(STEP, f"Drawing LOWESS plot: {Y_COL} vs {variable}")
        result = draw_lowess_plot(
            data,
            Y_COL,
            variable,
            FIGURE_DIR / f"lowess_{Y_COL}_vs_{variable}.png",
        )
        relationship_type = "treatment" if variable in TREATMENT_VARIABLES else "control"
        rows.append(
            {
                "variable": variable,
                "relationship_type": relationship_type,
                "lowess_pattern": result["lowess_pattern"],
                "interpretation": interpretation(str(result["lowess_pattern"])),
                "conclusion": conclusion(str(result["lowess_pattern"])),
            }
        )

    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(SUMMARY_PATH, index=False)
    log(STEP, f"Wrote {SUMMARY_PATH.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
