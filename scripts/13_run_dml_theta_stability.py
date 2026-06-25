from __future__ import annotations

import math
from collections.abc import Callable

import numpy as np
import pandas as pd
import statsmodels.api as sm
from PIL import Image, ImageDraw, ImageFont

from policy_pipeline_utils import (
    PROJECT_ROOT,
    SimpleGradientBoosting,
    SimpleRandomForest,
    add_check,
    kfold_indices,
    log,
    print_panel_diagnostics,
    require_no_failed_checks,
    write_checks,
)


STEP = "dml-theta-stability"
INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "final" / "analysis_panel_2018_2024.csv"
BASELINE_PATH = PROJECT_ROOT / "reports" / "tables" / "baseline_ols_fe_results.csv"
OUTPUT_DIR = PROJECT_ROOT / "reports" / "tables"
FIGURE_DIR = PROJECT_ROOT / "reports" / "figures" / "dml"
SUMMARY_PATH = PROJECT_ROOT / "reports" / "dml_results_summary.md"
VALIDATION_PATH = OUTPUT_DIR / "dml_theta_validation.csv"

MAIN_RESULTS_PATH = OUTPUT_DIR / "dml_main_results.csv"
FOLD_RESULTS_PATH = OUTPUT_DIR / "dml_theta_by_fold.csv"
SEED_RESULTS_PATH = OUTPUT_DIR / "dml_theta_by_seed.csv"
LEARNER_RESULTS_PATH = OUTPUT_DIR / "dml_theta_by_learner.csv"
STABILITY_PATH = OUTPUT_DIR / "dml_theta_stability.csv"

Y_COL = "informal_rate"
TREATMENTS = ["real_min_wage", "log_real_min_wage", "min_wage_growth"]
CONTROLS = [
    "unemployment_rate",
    "labour_productivity",
    "trained_labour_rate",
    "log_employed_persons",
]
PANEL_KEYS = ["province", "year"]
SEEDS = [42, 123, 2024]
N_FOLDS = 5


def validate_panel(data: pd.DataFrame) -> None:
    required_columns = [*PANEL_KEYS, Y_COL, *TREATMENTS, *CONTROLS]
    rows: list[dict[str, object]] = []

    missing_columns = [col for col in required_columns if col not in data.columns]
    add_check(
        rows,
        "dml_panel",
        "required_columns",
        not missing_columns,
        f"missing_columns={missing_columns}",
    )
    if missing_columns:
        write_checks(VALIDATION_PATH, rows)
        require_no_failed_checks(rows)

    add_check(rows, "dml_panel", "shape_rows", len(data) == 441, f"rows={len(data)}")
    add_check(
        rows,
        "dml_panel",
        "province_count",
        data["province"].nunique() == 63,
        f"province_count={data['province'].nunique()}",
    )
    years = sorted(data["year"].dropna().astype(int).unique().tolist())
    add_check(
        rows,
        "dml_panel",
        "year_range",
        years == list(range(2018, 2025)),
        f"years={years}",
    )
    duplicate_count = int(data.duplicated(PANEL_KEYS).sum())
    add_check(
        rows,
        "dml_panel",
        "duplicate_province_year",
        duplicate_count == 0,
        f"duplicates={duplicate_count}",
    )
    missing_values = data[required_columns].isna().sum()
    add_check(
        rows,
        "dml_panel",
        "missing_required_values",
        int(missing_values.sum()) == 0,
        f"missing={missing_values.to_dict()}",
    )
    for treatment in TREATMENTS:
        unique_count = int(data[treatment].nunique(dropna=True))
        add_check(
            rows,
            "dml_panel",
            f"variation_{treatment}",
            unique_count > 1,
            f"unique_values={unique_count}",
        )

    write_checks(VALIDATION_PATH, rows)
    require_no_failed_checks(rows)


def build_controls(data: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    year_dummies = pd.get_dummies(data["year"].astype(int), prefix="year", drop_first=True, dtype=float)
    controls = pd.concat([data[CONTROLS].astype(float), year_dummies], axis=1)
    return controls, controls.columns.tolist()


def standardize_train_test(x_train: np.ndarray, x_test: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    mean = x_train.mean(axis=0)
    std = x_train.std(axis=0)
    std[std < 1e-12] = 1.0
    return (x_train - mean) / std, (x_test - mean) / std


class RidgeRegressor:
    def __init__(self, alpha: float = 1.0) -> None:
        self.alpha = alpha
        self.coef_: np.ndarray | None = None

    def fit(self, x: np.ndarray, y: np.ndarray) -> "RidgeRegressor":
        design = np.column_stack([np.ones(len(x)), x])
        penalty = np.eye(design.shape[1]) * self.alpha
        penalty[0, 0] = 0.0
        self.coef_ = np.linalg.pinv(design.T @ design + penalty) @ design.T @ y
        return self

    def predict(self, x: np.ndarray) -> np.ndarray:
        if self.coef_ is None:
            raise RuntimeError("RidgeRegressor must be fitted before predict.")
        design = np.column_stack([np.ones(len(x)), x])
        return design @ self.coef_


def make_model(learner: str, seed: int):
    if learner == "ridge_numpy":
        return RidgeRegressor(alpha=1.0)
    if learner == "random_forest_custom":
        return SimpleRandomForest(n_estimators=35, seed=seed)
    if learner == "gradient_boosting_custom":
        return SimpleGradientBoosting(n_estimators=60, learning_rate=0.06, seed=seed)
    raise ValueError(f"Unknown learner: {learner}")


def estimate_theta(y_res: np.ndarray, d_res: np.ndarray, clusters: pd.Series) -> tuple[dict[str, float | str], object]:
    x = sm.add_constant(d_res, has_constant="add")
    try:
        result = sm.OLS(y_res, x).fit(cov_type="cluster", cov_kwds={"groups": clusters})
        se_type = "cluster_province"
        se = float(result.bse[1])
        if not np.isfinite(se):
            raise RuntimeError("Cluster standard error is not finite.")
    except Exception as exc:
        result = sm.OLS(y_res, x).fit(cov_type="HC1")
        se_type = f"HC1_fallback_after_cluster_error: {type(exc).__name__}"

    conf_int = result.conf_int()
    theta = float(result.params[1])
    se = float(result.bse[1])
    p_value = float(result.pvalues[1])
    ci_lower = float(conf_int[1, 0])
    ci_upper = float(conf_int[1, 1])
    return (
        {
            "theta": theta,
            "std_error": se,
            "p_value": p_value,
            "ci_lower": ci_lower,
            "ci_upper": ci_upper,
            "se_type": se_type,
        },
        result,
    )


def slope_only(y: np.ndarray, d: np.ndarray) -> float:
    if len(y) < 3 or np.nanstd(d) < 1e-12:
        return float("nan")
    x = np.column_stack([np.ones(len(d)), d])
    return float(np.linalg.lstsq(x, y, rcond=None)[0][1])


def run_dml_for(
    data: pd.DataFrame,
    x_controls: np.ndarray,
    treatment: str,
    learner: str,
    seed: int,
    control_names: list[str],
) -> tuple[dict[str, object], list[dict[str, object]]]:
    y = data[Y_COL].to_numpy(dtype=float)
    d = data[treatment].to_numpy(dtype=float)
    n = len(data)
    y_hat = np.full(n, np.nan)
    d_hat = np.full(n, np.nan)
    fold_ids = np.full(n, -1)
    folds = kfold_indices(n, folds=N_FOLDS, seed=seed)

    for fold_idx, test_idx in enumerate(folds, start=1):
        train_idx = np.setdiff1d(np.arange(n), test_idx)
        x_train = x_controls[train_idx]
        x_test = x_controls[test_idx]
        x_train_scaled, x_test_scaled = standardize_train_test(x_train, x_test)

        y_model = make_model(learner, seed + fold_idx * 17 + 1)
        d_model = make_model(learner, seed + fold_idx * 17 + 2)
        y_model.fit(x_train_scaled, y[train_idx])
        d_model.fit(x_train_scaled, d[train_idx])
        y_hat[test_idx] = y_model.predict(x_test_scaled)
        d_hat[test_idx] = d_model.predict(x_test_scaled)
        fold_ids[test_idx] = fold_idx

    if np.isnan(y_hat).any() or np.isnan(d_hat).any() or (fold_ids < 0).any():
        raise RuntimeError(f"Cross-fitting failed for treatment={treatment}, learner={learner}, seed={seed}.")

    y_res = y - y_hat
    d_res = d - d_hat
    theta_stats, _ = estimate_theta(y_res, d_res, data["province"])
    note = (
        "Partialling-out DML with year dummies in W; no province dummies. "
        "Custom learners are used because scikit-learn is not in requirements.txt."
    )
    main_row: dict[str, object] = {
        "treatment": treatment,
        "learner": learner,
        "seed": seed,
        **theta_stats,
        "n_obs": n,
        "n_folds": len(folds),
        "controls": ";".join(control_names),
        "note": note,
    }

    fold_rows: list[dict[str, object]] = []
    for fold in sorted(set(fold_ids.tolist())):
        mask = fold_ids == fold
        fold_rows.append(
            {
                "treatment": treatment,
                "learner": learner,
                "seed": seed,
                "fold": int(fold),
                "theta_fold": slope_only(y_res[mask], d_res[mask]),
                "n_fold": int(mask.sum()),
            }
        )
    return main_row, fold_rows


def summarize_by_learner(main_results: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (treatment, learner), group in main_results.groupby(["treatment", "learner"], sort=False):
        theta = group["theta"].astype(float)
        rows.append(
            {
                "treatment": treatment,
                "learner": learner,
                "theta_mean": theta.mean(),
                "theta_std": theta.std(ddof=0),
                "theta_min": theta.min(),
                "theta_max": theta.max(),
                "n_runs": len(group),
            }
        )
    return pd.DataFrame(rows)


def stability_interpretation(stable_sign: bool, share_ci_contains_zero: float, theta_std: float, theta_mean: float) -> str:
    if not stable_sign:
        return "Theta changes sign across learners/seeds; treat as unstable exploratory evidence."
    rel_std = abs(theta_std / theta_mean) if abs(theta_mean) > 1e-12 else np.inf
    if share_ci_contains_zero >= 0.5:
        return "Sign is stable but many confidence intervals include zero; statistical evidence is weak."
    if rel_std > 0.5:
        return "Sign is stable but magnitude varies materially across learners/seeds."
    return "Theta is relatively stable across learners/seeds, but remains a robustness check, not causal proof."


def summarize_stability(main_results: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for treatment, group in main_results.groupby("treatment", sort=False):
        theta = group["theta"].astype(float)
        signs = np.sign(theta.to_numpy())
        nonzero_signs = signs[signs != 0]
        stable_sign = bool(len(set(nonzero_signs.tolist())) <= 1) if len(nonzero_signs) else False
        ci_contains_zero = (group["ci_lower"].astype(float) <= 0) & (group["ci_upper"].astype(float) >= 0)
        theta_mean = float(theta.mean())
        theta_std = float(theta.std(ddof=0))
        rows.append(
            {
                "treatment": treatment,
                "theta_mean": theta_mean,
                "theta_std": theta_std,
                "theta_min": float(theta.min()),
                "theta_max": float(theta.max()),
                "share_positive": float((theta > 0).mean()),
                "share_negative": float((theta < 0).mean()),
                "stable_sign": stable_sign,
                "avg_p_value": float(group["p_value"].astype(float).mean()),
                "share_ci_contains_zero": float(ci_contains_zero.mean()),
                "interpretation": stability_interpretation(
                    stable_sign=stable_sign,
                    share_ci_contains_zero=float(ci_contains_zero.mean()),
                    theta_std=theta_std,
                    theta_mean=theta_mean,
                ),
            }
        )
    return pd.DataFrame(rows)


def baseline_twfe() -> pd.DataFrame:
    if not BASELINE_PATH.exists():
        return pd.DataFrame(columns=["treatment", "twfe_coefficient", "twfe_p_value", "twfe_ci_lower", "twfe_ci_upper"])
    baseline = pd.read_csv(BASELINE_PATH)
    mask = (
        (baseline["model"] == "two_way_fe_controls")
        & (baseline["control_set"] == "log_employment_scale")
        & (baseline["treatment"].isin(TREATMENTS))
    )
    out = baseline.loc[
        mask,
        ["treatment", "coefficient", "p_value", "ci_lower_95", "ci_upper_95"],
    ].copy()
    out = out.rename(
        columns={
            "coefficient": "twfe_coefficient",
            "p_value": "twfe_p_value",
            "ci_lower_95": "twfe_ci_lower",
            "ci_upper_95": "twfe_ci_upper",
        }
    )
    return out


def compare_with_baseline(stability: pd.DataFrame) -> pd.DataFrame:
    comparison = stability.merge(baseline_twfe(), on="treatment", how="left")
    comparison["same_sign_as_twfe"] = np.sign(comparison["theta_mean"]) == np.sign(comparison["twfe_coefficient"])
    comparison["magnitude_ratio_abs"] = (
        comparison["theta_mean"].abs() / comparison["twfe_coefficient"].abs().replace(0, np.nan)
    )
    return comparison


def format_float(value: object, digits: int = 4) -> str:
    try:
        number = float(value)
    except Exception:
        return str(value)
    if not np.isfinite(number):
        return "NA"
    if abs(number) >= 1000 or (0 < abs(number) < 0.001):
        return f"{number:.3e}"
    return f"{number:.{digits}f}"


def draw_faceted_points(
    data: pd.DataFrame,
    category_col: str,
    value_col: str,
    output_path,
    title: str,
    subtitle_col: str | None = None,
) -> None:
    treatments = TREATMENTS
    width, panel_h = 1100, 300
    left, right, top, bottom = 120, 40, 60, 70
    height = top + bottom + panel_h * len(treatments)
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    draw.text((left, 24), title, fill=(20, 20, 20), font=font)

    colors = {
        "ridge_numpy": (45, 95, 170),
        "random_forest_custom": (210, 90, 55),
        "gradient_boosting_custom": (60, 140, 95),
    }
    label_map = {
        "ridge_numpy": "ridge",
        "random_forest_custom": "rf",
        "gradient_boosting_custom": "gb",
    }

    for panel_idx, treatment in enumerate(treatments):
        sub = data[data["treatment"] == treatment].copy()
        panel_top = top + panel_idx * panel_h
        plot_top = panel_top + 36
        plot_bottom = panel_top + panel_h - 54
        plot_left = left
        plot_right = width - right
        values = sub[value_col].astype(float).to_numpy()
        finite = values[np.isfinite(values)]
        if len(finite) == 0:
            low, high = -1.0, 1.0
        else:
            low = min(float(finite.min()), 0.0)
            high = max(float(finite.max()), 0.0)
            pad = (high - low) * 0.12 if high > low else max(abs(high), 1.0) * 0.12
            low -= pad
            high += pad
        draw.text((left, panel_top + 8), treatment, fill=(30, 30, 30), font=font)
        zero_y = int(plot_bottom - (0 - low) / (high - low) * (plot_bottom - plot_top)) if high != low else (plot_top + plot_bottom) // 2
        draw.line((plot_left, zero_y, plot_right, zero_y), fill=(160, 160, 160), width=2)
        draw.rectangle((plot_left, plot_top, plot_right, plot_bottom), outline=(50, 50, 50), width=1)
        draw.text((34, plot_top - 4), format_float(high, 3), fill=(80, 80, 80), font=font)
        draw.text((34, zero_y - 6), "0", fill=(80, 80, 80), font=font)
        draw.text((34, plot_bottom - 10), format_float(low, 3), fill=(80, 80, 80), font=font)

        categories = list(dict.fromkeys(sub[category_col].astype(str).tolist()))
        if not categories:
            continue
        slot = (plot_right - plot_left) / max(1, len(categories))
        for cat_idx, cat in enumerate(categories):
            cat_rows = sub[sub[category_col].astype(str) == cat]
            x_center = int(plot_left + slot * (cat_idx + 0.5))
            display_cat = label_map.get(cat, cat[:12])
            draw.text((x_center - 18, plot_bottom + 16), display_cat, fill=(70, 70, 70), font=font)
            for row_idx, row in enumerate(cat_rows.itertuples(index=False)):
                value = float(getattr(row, value_col))
                if not np.isfinite(value):
                    continue
                jitter = ((row_idx % 7) - 3) * 5
                y = int(plot_bottom - (value - low) / (high - low) * (plot_bottom - plot_top)) if high != low else zero_y
                learner = getattr(row, "learner", "")
                color = colors.get(str(learner), (45, 95, 170))
                draw.ellipse((x_center + jitter - 4, y - 4, x_center + jitter + 4, y + 4), fill=color, outline=(30, 30, 30))
                if subtitle_col and hasattr(row, subtitle_col):
                    draw.text((x_center + jitter + 6, y - 5), str(getattr(row, subtitle_col))[:8], fill=(90, 90, 90), font=font)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)


def write_figures(
    main_results: pd.DataFrame,
    fold_results: pd.DataFrame,
    learner_results: pd.DataFrame,
) -> None:
    draw_faceted_points(
        learner_results,
        category_col="learner",
        value_col="theta_mean",
        output_path=FIGURE_DIR / "dml_theta_by_learner.png",
        title="DML theta by learner (mean across seeds)",
    )
    draw_faceted_points(
        main_results,
        category_col="seed",
        value_col="theta",
        output_path=FIGURE_DIR / "dml_theta_by_seed.png",
        title="DML theta by seed and learner",
    )
    draw_faceted_points(
        fold_results,
        category_col="fold",
        value_col="theta_fold",
        output_path=FIGURE_DIR / "dml_theta_by_fold.png",
        title="DML theta by held-out fold",
    )


def write_summary(
    main_results: pd.DataFrame,
    stability: pd.DataFrame,
    comparison: pd.DataFrame,
) -> None:
    lines: list[str] = []
    lines.append("# DML Results Summary")
    lines.append("")
    lines.append("## 1. Mục Tiêu")
    lines.append("")
    lines.append(
        "DML được chạy như một robustness/flexible-control exercise sau baseline OLS/FE/TWFE. "
        "Mục tiêu là kiểm tra theta có ổn định khi kiểm soát linh hoạt các nuisance functions hay không, "
        "không phải chứng minh tác động nhân quả."
    )
    lines.append("")
    lines.append("## 2. Specification")
    lines.append("")
    lines.append(f"- Outcome: `{Y_COL}`.")
    lines.append("- Treatments: `" + "`, `".join(TREATMENTS) + "`.")
    lines.append("- Controls W: `" + "`, `".join(CONTROLS) + "` plus year dummies.")
    lines.append("- Province dummies are not included in the main DML because the sample is small.")
    lines.append("- Cross-fitting: 5 folds with seeds 42, 123, 2024.")
    lines.append("- Learners: `ridge_numpy`, `random_forest_custom`, `gradient_boosting_custom`.")
    lines.append("- Standard errors: clustered by province when available; fallback is reported if used.")
    lines.append("")
    lines.append("## 3. Main Findings")
    lines.append("")
    for row in stability.itertuples(index=False):
        lines.append(
            f"- `{row.treatment}`: theta_mean = `{format_float(row.theta_mean)}`, "
            f"theta_std = `{format_float(row.theta_std)}`, "
            f"share_positive = `{format_float(row.share_positive, 2)}`, "
            f"share_ci_contains_zero = `{format_float(row.share_ci_contains_zero, 2)}`. "
            f"{row.interpretation}"
        )
    lines.append("")
    lines.append("## 4. So Sánh Với Baseline Two-way FE")
    lines.append("")
    for row in comparison.itertuples(index=False):
        same_sign = "cùng dấu" if bool(row.same_sign_as_twfe) else "khác dấu"
        lines.append(
            f"- `{row.treatment}`: DML theta_mean = `{format_float(row.theta_mean)}`, "
            f"two-way FE coefficient = `{format_float(row.twfe_coefficient)}`; "
            f"DML {same_sign} với two-way FE. "
            f"TWFE p-value = `{format_float(row.twfe_p_value)}`."
        )
    lines.append("")
    lines.append(
        "So sánh này chỉ mang tính định hướng vì DML main specification kiểm soát year dummies và W linh hoạt, "
        "nhưng không đưa province dummies vào nuisance functions. Two-way FE vẫn là benchmark kinh tế lượng truyền thống."
    )
    lines.append("")
    lines.append("## 5. Diễn Giải Thận Trọng")
    lines.append("")
    if bool(stability["stable_sign"].all()):
        lines.append(
            "Các theta có dấu tương đối ổn định trong bảng stability. Tuy nhiên, cần kiểm tra confidence interval, "
            "p-value và độ nhạy theo learner/seed/fold trước khi xem đây là bằng chứng gợi ý."
        )
    else:
        lines.append(
            "Một số theta chưa ổn định về dấu hoặc độ lớn giữa learners/seeds. Điều này cho thấy dữ liệu hiện tại "
            "chưa cung cấp bằng chứng đủ mạnh để dùng DML đưa ra kết luận chắc chắn."
        )
    if float(stability["share_ci_contains_zero"].mean()) > 0:
        lines.append(
            "Một số confidence intervals chứa 0, vì vậy bằng chứng thống kê về theta chưa đồng nhất giữa các specification DML."
        )
    lines.append("")
    lines.append(
        "DML cung cấp kiểm tra bổ sung về tính ổn định của theta sau khi kiểm soát linh hoạt các quan hệ phi tuyến. "
        "Kết quả cần diễn giải thận trọng do hạn chế identification, dữ liệu aggregate province-year, "
        "và province-level wage-region approximation."
    )
    lines.append("")
    lines.append("Không diễn giải các kết quả này như bằng chứng DML chứng minh lương tối thiểu gây ra thay đổi informal employment.")
    lines.append("")
    lines.append("## 6. Output Files")
    lines.append("")
    for path in [MAIN_RESULTS_PATH, FOLD_RESULTS_PATH, SEED_RESULTS_PATH, LEARNER_RESULTS_PATH, STABILITY_PATH]:
        lines.append(f"- `{path.relative_to(PROJECT_ROOT)}`")
    for path in [
        FIGURE_DIR / "dml_theta_by_learner.png",
        FIGURE_DIR / "dml_theta_by_seed.png",
        FIGURE_DIR / "dml_theta_by_fold.png",
    ]:
        lines.append(f"- `{path.relative_to(PROJECT_ROOT)}`")

    SUMMARY_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    data = pd.read_csv(INPUT_PATH)
    print_panel_diagnostics(data, PANEL_KEYS, STEP)
    validate_panel(data)
    controls, control_names = build_controls(data)
    x_controls = controls.to_numpy(dtype=float)

    learners = ["ridge_numpy", "random_forest_custom", "gradient_boosting_custom"]
    main_rows: list[dict[str, object]] = []
    fold_rows: list[dict[str, object]] = []
    for treatment in TREATMENTS:
        for learner in learners:
            for seed in SEEDS:
                log(STEP, f"Running treatment={treatment}, learner={learner}, seed={seed}")
                main_row, fold_result = run_dml_for(data, x_controls, treatment, learner, seed, control_names)
                main_rows.append(main_row)
                fold_rows.extend(fold_result)

    main_results = pd.DataFrame(main_rows)
    fold_results = pd.DataFrame(fold_rows)
    seed_results = main_results[
        ["treatment", "learner", "seed", "theta", "std_error", "p_value", "ci_lower", "ci_upper"]
    ].copy()
    learner_results = summarize_by_learner(main_results)
    stability = summarize_stability(main_results)
    comparison = compare_with_baseline(stability)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    main_results.to_csv(MAIN_RESULTS_PATH, index=False)
    fold_results.to_csv(FOLD_RESULTS_PATH, index=False)
    seed_results.to_csv(SEED_RESULTS_PATH, index=False)
    learner_results.to_csv(LEARNER_RESULTS_PATH, index=False)
    stability.to_csv(STABILITY_PATH, index=False)
    write_figures(main_results, fold_results, learner_results)
    write_summary(main_results, stability, comparison)

    log(STEP, f"Wrote {MAIN_RESULTS_PATH.relative_to(PROJECT_ROOT)}")
    log(STEP, f"Wrote {FOLD_RESULTS_PATH.relative_to(PROJECT_ROOT)}")
    log(STEP, f"Wrote {LEARNER_RESULTS_PATH.relative_to(PROJECT_ROOT)}")
    log(STEP, f"Wrote {STABILITY_PATH.relative_to(PROJECT_ROOT)}")
    log(STEP, f"Wrote {SUMMARY_PATH.relative_to(PROJECT_ROOT)}")
    print(stability.to_string(index=False))
    print(comparison[["treatment", "theta_mean", "twfe_coefficient", "same_sign_as_twfe"]].to_string(index=False))


if __name__ == "__main__":
    main()
