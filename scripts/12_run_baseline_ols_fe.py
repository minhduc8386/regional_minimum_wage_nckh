from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm
from linearmodels.panel import PanelOLS

from policy_pipeline_utils import (
    PROJECT_ROOT,
    add_check,
    log,
    print_panel_diagnostics,
    require_no_failed_checks,
    write_checks,
)


STEP = "baseline-ols-fe"
INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "final" / "analysis_panel_2018_2024.csv"
OUTPUT_PATH = PROJECT_ROOT / "reports" / "tables" / "baseline_ols_fe_results.csv"
VALIDATION_PATH = PROJECT_ROOT / "reports" / "tables" / "baseline_ols_fe_validation.csv"

Y_COL = "informal_rate"
TREATMENTS = ["real_min_wage", "log_real_min_wage", "min_wage_growth"]
BASE_CONTROLS = [
    "unemployment_rate",
    "labour_productivity",
    "trained_labour_rate",
    "log_employed_persons",
]
ROBUSTNESS_CONTROLS = [
    "unemployment_rate",
    "labour_productivity",
    "trained_labour_rate",
    "employed_persons",
]
CONTROL_SETS = {
    "log_employment_scale": BASE_CONTROLS,
    "level_employment_scale": ROBUSTNESS_CONTROLS,
}
PANEL_KEYS = ["province", "year"]

MODEL_SPECS = [
    {
        "model": "pooled_ols_no_controls",
        "estimator": "statsmodels_ols",
        "controls_included": False,
        "province_fe": False,
        "year_fe": False,
    },
    {
        "model": "pooled_ols_controls",
        "estimator": "statsmodels_ols",
        "controls_included": True,
        "province_fe": False,
        "year_fe": False,
    },
    {
        "model": "province_fe_controls",
        "estimator": "linearmodels_panelols",
        "controls_included": True,
        "province_fe": True,
        "year_fe": False,
    },
    {
        "model": "year_fe_controls",
        "estimator": "linearmodels_panelols",
        "controls_included": True,
        "province_fe": False,
        "year_fe": True,
    },
    {
        "model": "two_way_fe_controls",
        "estimator": "linearmodels_panelols",
        "controls_included": True,
        "province_fe": True,
        "year_fe": True,
    },
]


def validate_panel(data: pd.DataFrame) -> None:
    control_columns = sorted({col for controls in CONTROL_SETS.values() for col in controls})
    required_columns = [*PANEL_KEYS, Y_COL, *TREATMENTS, *control_columns]
    rows: list[dict[str, object]] = []

    missing_columns = [col for col in required_columns if col not in data.columns]
    add_check(
        rows,
        "baseline_panel",
        "required_columns",
        not missing_columns,
        f"missing_columns={missing_columns}",
    )
    if missing_columns:
        write_checks(VALIDATION_PATH, rows)
        require_no_failed_checks(rows)

    add_check(rows, "baseline_panel", "shape_rows", len(data) == 441, f"rows={len(data)}")
    add_check(
        rows,
        "baseline_panel",
        "province_count",
        data["province"].nunique() == 63,
        f"province_count={data['province'].nunique()}",
    )
    years = sorted(data["year"].dropna().astype(int).unique().tolist())
    add_check(
        rows,
        "baseline_panel",
        "year_range",
        years == list(range(2018, 2025)),
        f"years={years}",
    )
    duplicate_count = int(data.duplicated(PANEL_KEYS).sum())
    add_check(
        rows,
        "baseline_panel",
        "duplicate_province_year",
        duplicate_count == 0,
        f"duplicates={duplicate_count}",
    )
    missing_values = data[required_columns].isna().sum()
    add_check(
        rows,
        "baseline_panel",
        "missing_required_values",
        int(missing_values.sum()) == 0,
        f"missing={missing_values.to_dict()}",
    )
    for treatment in TREATMENTS:
        unique_count = int(data[treatment].nunique(dropna=True))
        add_check(
            rows,
            "baseline_panel",
            f"variation_{treatment}",
            unique_count > 1,
            f"unique_values={unique_count}",
        )

    write_checks(VALIDATION_PATH, rows)
    require_no_failed_checks(rows)


def regressors(treatment: str, controls_included: bool, control_set: str) -> list[str]:
    return [treatment, *(CONTROL_SETS[control_set] if controls_included else [])]


def model_columns(treatment: str, controls_included: bool, control_set: str) -> list[str]:
    return [Y_COL, *regressors(treatment, controls_included, control_set), "province", "year"]


def estimate_pooled_ols(
    data: pd.DataFrame,
    treatment: str,
    spec: dict[str, object],
    control_set: str,
) -> dict[str, object]:
    controls_included = bool(spec["controls_included"])
    x_cols = regressors(treatment, controls_included, control_set)
    model_data = data[model_columns(treatment, controls_included, control_set)].dropna().copy()

    y = model_data[Y_COL].astype(float)
    x = sm.add_constant(model_data[x_cols].astype(float), has_constant="add")
    result = sm.OLS(y, x).fit(
        cov_type="cluster",
        cov_kwds={"groups": model_data["province"]},
    )
    conf_int = result.conf_int().loc[treatment]

    return {
        "treatment": treatment,
        "model": spec["model"],
        "estimator": spec["estimator"],
        "control_set": control_set if controls_included else "none",
        "controls": ";".join(CONTROL_SETS[control_set]) if controls_included else "",
        "controls_included": controls_included,
        "province_fe": bool(spec["province_fe"]),
        "year_fe": bool(spec["year_fe"]),
        "coefficient": float(result.params[treatment]),
        "standard_error": float(result.bse[treatment]),
        "t_stat": float(result.tvalues[treatment]),
        "p_value": float(result.pvalues[treatment]),
        "ci_lower_95": float(conf_int.iloc[0]),
        "ci_upper_95": float(conf_int.iloc[1]),
        "n_obs": int(result.nobs),
        "n_provinces": int(model_data["province"].nunique()),
        "n_years": int(model_data["year"].nunique()),
        "r_squared": float(result.rsquared),
        "r_squared_within": np.nan,
        "r_squared_between": np.nan,
        "r_squared_overall": np.nan,
        "design_rank": int(np.linalg.matrix_rank(x.to_numpy())),
        "n_parameters": int(len(result.params)),
        "cluster": "province",
        "inference_note": "Cluster-robust standard errors by province from statsmodels.",
    }


def estimate_panel_ols(
    data: pd.DataFrame,
    treatment: str,
    spec: dict[str, object],
    control_set: str,
) -> dict[str, object]:
    controls_included = bool(spec["controls_included"])
    x_cols = regressors(treatment, controls_included, control_set)
    model_data = data[model_columns(treatment, controls_included, control_set)].dropna().copy()
    panel_data = model_data.set_index(["province", "year"])

    y = panel_data[Y_COL].astype(float)
    x = panel_data[x_cols].astype(float)
    x = sm.add_constant(x, has_constant="add")

    model = PanelOLS(
        y,
        x,
        entity_effects=bool(spec["province_fe"]),
        time_effects=bool(spec["year_fe"]),
        drop_absorbed=True,
        check_rank=True,
    )
    result = model.fit(cov_type="clustered", cluster_entity=True)
    conf_int = result.conf_int().loc[treatment]

    return {
        "treatment": treatment,
        "model": spec["model"],
        "estimator": spec["estimator"],
        "control_set": control_set if controls_included else "none",
        "controls": ";".join(CONTROL_SETS[control_set]) if controls_included else "",
        "controls_included": controls_included,
        "province_fe": bool(spec["province_fe"]),
        "year_fe": bool(spec["year_fe"]),
        "coefficient": float(result.params[treatment]),
        "standard_error": float(result.std_errors[treatment]),
        "t_stat": float(result.tstats[treatment]),
        "p_value": float(result.pvalues[treatment]),
        "ci_lower_95": float(conf_int.iloc[0]),
        "ci_upper_95": float(conf_int.iloc[1]),
        "n_obs": int(result.nobs),
        "n_provinces": int(model_data["province"].nunique()),
        "n_years": int(model_data["year"].nunique()),
        "r_squared": float(result.rsquared),
        "r_squared_within": float(result.rsquared_within),
        "r_squared_between": float(result.rsquared_between),
        "r_squared_overall": float(result.rsquared_overall),
        "design_rank": int(np.linalg.matrix_rank(x.to_numpy())),
        "n_parameters": int(len(result.params)),
        "cluster": "province",
        "inference_note": "Entity-clustered standard errors from linearmodels.PanelOLS.",
    }


def estimate_model(
    data: pd.DataFrame,
    treatment: str,
    spec: dict[str, object],
    control_set: str,
) -> dict[str, object]:
    if spec["estimator"] == "statsmodels_ols":
        return estimate_pooled_ols(data, treatment, spec, control_set)
    if spec["estimator"] == "linearmodels_panelols":
        return estimate_panel_ols(data, treatment, spec, control_set)
    raise ValueError(f"Unknown estimator: {spec['estimator']}")


def control_sets_for_spec(spec: dict[str, object]) -> list[str]:
    if not bool(spec["controls_included"]):
        return ["log_employment_scale"]
    return list(CONTROL_SETS)


def main() -> None:
    data = pd.read_csv(INPUT_PATH)
    print_panel_diagnostics(data, PANEL_KEYS, STEP)
    validate_panel(data)

    rows: list[dict[str, object]] = []
    for treatment in TREATMENTS:
        for spec in MODEL_SPECS:
            for control_set in control_sets_for_spec(spec):
                log(
                    STEP,
                    f"Estimating {spec['model']} with treatment={treatment}, control_set={control_set}",
                )
                rows.append(estimate_model(data, treatment, spec, control_set))

    result = pd.DataFrame(rows)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT_PATH, index=False)
    log(STEP, f"Wrote {OUTPUT_PATH.relative_to(PROJECT_ROOT)}")
    print(result.to_string(index=False))


if __name__ == "__main__":
    main()
