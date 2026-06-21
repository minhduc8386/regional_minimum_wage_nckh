from __future__ import annotations

import numpy as np
import pandas as pd

from policy_pipeline_utils import (
    PROJECT_ROOT,
    SimpleGradientBoosting,
    SimpleRandomForest,
    kfold_indices,
    log,
    metrics,
    print_panel_diagnostics,
    train_linear,
)


STEP = "model-comparison-final"
INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "final" / "analysis_panel_2018_2024.csv"
OUTPUT_PATH = PROJECT_ROOT / "reports" / "tables" / "model_comparison_linear_vs_ml_final.csv"
Y_COL = "informal_rate"
FEATURES = [
    "real_min_wage",
    "log_real_min_wage",
    "min_wage_growth",
    "unemployment_rate",
    "labour_productivity",
    "trained_labour_rate",
    "employed_persons",
    "log_employed_persons",
]


def standardize_train_test(x_train: np.ndarray, x_test: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    mean = x_train.mean(axis=0)
    std = x_train.std(axis=0)
    std[std == 0] = 1.0
    return (x_train - mean) / std, (x_test - mean) / std


def main() -> None:
    data = pd.read_csv(INPUT_PATH)
    print_panel_diagnostics(data, ["province", "year"], STEP)
    complete = data[[Y_COL, *FEATURES]].dropna().reset_index(drop=True)
    if len(complete) != len(data):
        missing_rows = data.loc[data[[Y_COL, *FEATURES]].isna().any(axis=1), ["province", "year", *FEATURES]]
        raise RuntimeError(f"Missing values in model features/target:\n{missing_rows.to_string(index=False)}")

    x = complete[FEATURES].to_numpy(dtype=float)
    y = complete[Y_COL].to_numpy(dtype=float)
    n = len(y)
    folds = kfold_indices(n, folds=5, seed=2026)
    predictions = {
        "linear_regression": np.full(n, np.nan),
        "random_forest_custom": np.full(n, np.nan),
        "gradient_boosting_custom": np.full(n, np.nan),
    }

    for fold_num, test_idx in enumerate(folds, start=1):
        train_idx = np.setdiff1d(np.arange(n), test_idx)
        x_train, x_test = x[train_idx], x[test_idx]
        y_train = y[train_idx]
        x_train_scaled, x_test_scaled = standardize_train_test(x_train, x_test)

        linear_predict = train_linear(x_train_scaled, y_train)
        predictions["linear_regression"][test_idx] = linear_predict(x_test_scaled)

        rf = SimpleRandomForest(seed=2026 + fold_num)
        rf.fit(x_train, y_train)
        predictions["random_forest_custom"][test_idx] = rf.predict(x_test)

        gb = SimpleGradientBoosting(seed=3026 + fold_num)
        gb.fit(x_train, y_train)
        predictions["gradient_boosting_custom"][test_idx] = gb.predict(x_test)

    rows = []
    for model, pred in predictions.items():
        row = {
            "model": model,
            "n_complete": n,
            "folds": len(folds),
            **metrics(y, pred),
            "note": "Predictive diagnostic only; not a causal estimate.",
        }
        rows.append(row)

    result = pd.DataFrame(rows).sort_values("rmse").reset_index(drop=True)
    linear_rmse = float(result.loc[result["model"] == "linear_regression", "rmse"].iloc[0])
    best_rmse = float(result["rmse"].min())
    if best_rmse < 0.9 * linear_rmse:
        conclusion = "ML model has at least 10% lower CV RMSE than linear regression; preliminary evidence of non-linearity."
    else:
        conclusion = "ML model does not materially improve CV RMSE; non-linearity evidence is not strong."
    result["overall_conclusion"] = conclusion

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT_PATH, index=False)
    log(STEP, f"Wrote {OUTPUT_PATH.relative_to(PROJECT_ROOT)}")
    print(result.to_string(index=False))


if __name__ == "__main__":
    main()
