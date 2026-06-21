from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PANEL_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "nso_employment"
    / "province_year_panel_2018_2024.csv"
)
FIGURE_DIR = PROJECT_ROOT / "reports" / "figures" / "nonlinearity"
TABLE_DIR = PROJECT_ROOT / "reports" / "tables"
SUMMARY_PATH = TABLE_DIR / "nonlinearity_summary.csv"
MODEL_PATH = TABLE_DIR / "model_comparison_linear_vs_rf.csv"

Y_COL = "informal_rate"
X_COLS = [
    "unemployment_rate",
    "labour_productivity",
    "trained_labour_rate",
    "employed_persons",
]


def log(message: str) -> None:
    print(f"[nonlinearity] {message}")


def lowess(x: np.ndarray, y: np.ndarray, frac: float = 0.7) -> tuple[np.ndarray, np.ndarray]:
    mask = np.isfinite(x) & np.isfinite(y)
    x = x[mask].astype(float)
    y = y[mask].astype(float)
    if len(x) == 0:
        return np.array([]), np.array([])
    order = np.argsort(x)
    x = x[order]
    y = y[order]
    if len(x) < 3 or np.nanstd(x) == 0:
        return x, y

    k = max(3, int(math.ceil(frac * len(x))))
    yhat = np.empty_like(y, dtype=float)
    for i, x0 in enumerate(x):
        distances = np.abs(x - x0)
        bandwidth = np.partition(distances, min(k - 1, len(distances) - 1))[k - 1]
        if bandwidth <= 0:
            yhat[i] = np.average(y)
            continue
        weights = (1 - (distances / bandwidth) ** 3) ** 3
        weights[distances > bandwidth] = 0
        design = np.column_stack([np.ones(len(x)), x - x0])
        weighted_design = design * weights[:, None]
        try:
            beta = np.linalg.lstsq(weighted_design.T @ design, weighted_design.T @ y, rcond=None)[0]
            yhat[i] = beta[0]
        except np.linalg.LinAlgError:
            yhat[i] = np.average(y, weights=np.maximum(weights, 1e-9))
    return x, yhat


def scale(value: float, low: float, high: float, start: int, end: int, invert: bool = False) -> int:
    if high == low:
        ratio = 0.5
    else:
        ratio = (value - low) / (high - low)
    if invert:
        ratio = 1 - ratio
    return int(round(start + ratio * (end - start)))


def domain(values: np.ndarray) -> tuple[float, float]:
    values = values[np.isfinite(values)]
    if len(values) == 0:
        return 0.0, 1.0
    low = float(values.min())
    high = float(values.max())
    if low == high:
        pad = max(1.0, abs(low) * 0.1)
    else:
        pad = (high - low) * 0.08
    return low - pad, high + pad


def draw_lowess_plot(data: pd.DataFrame, x_col: str, output_path: Path) -> dict[str, object]:
    complete = data[[Y_COL, x_col]].dropna()
    x = complete[x_col].to_numpy(dtype=float)
    y = complete[Y_COL].to_numpy(dtype=float)
    lx, ly = lowess(x, y)

    width, height = 980, 680
    left, right, top, bottom = 110, 40, 70, 105
    plot_w = width - left - right
    plot_h = height - top - bottom
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    x_low, x_high = domain(x)
    y_low, y_high = domain(y)

    draw.text((left, 22), f"{Y_COL} vs {x_col} with LOWESS", fill=(20, 20, 20), font=font)
    draw.text((left, height - 45), x_col, fill=(30, 30, 30), font=font)
    draw.text((18, top + plot_h // 2), Y_COL, fill=(30, 30, 30), font=font)

    for i in range(6):
        tx = x_low + (x_high - x_low) * i / 5
        px = scale(tx, x_low, x_high, left, left + plot_w)
        draw.line((px, top, px, top + plot_h), fill=(235, 235, 235))
        draw.text((px - 20, top + plot_h + 12), f"{tx:.1f}", fill=(80, 80, 80), font=font)

        ty = y_low + (y_high - y_low) * i / 5
        py = scale(ty, y_low, y_high, top, top + plot_h, invert=True)
        draw.line((left, py, left + plot_w, py), fill=(235, 235, 235))
        draw.text((42, py - 6), f"{ty:.1f}", fill=(80, 80, 80), font=font)

    draw.rectangle((left, top, left + plot_w, top + plot_h), outline=(35, 35, 35), width=2)

    for xi, yi in zip(x, y):
        px = scale(xi, x_low, x_high, left, left + plot_w)
        py = scale(yi, y_low, y_high, top, top + plot_h, invert=True)
        draw.ellipse((px - 4, py - 4, px + 4, py + 4), fill=(32, 96, 168), outline=(20, 60, 110))

    if len(lx) >= 2:
        points = [
            (
                scale(xi, x_low, x_high, left, left + plot_w),
                scale(yi, y_low, y_high, top, top + plot_h, invert=True),
            )
            for xi, yi in zip(lx, ly)
        ]
        draw.line(points, fill=(205, 55, 55), width=3)

    note = f"complete observations: {len(complete)}"
    draw.text((left, height - 75), note, fill=(90, 90, 90), font=font)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)

    visual_pattern = classify_visual_pattern(x, y, lx, ly)
    return {
        "n_complete": len(complete),
        "visual_pattern": visual_pattern,
        "lowess_interpretation": lowess_interpretation(len(complete), y, visual_pattern),
    }


def classify_visual_pattern(x: np.ndarray, y: np.ndarray, lx: np.ndarray, ly: np.ndarray) -> str:
    if len(y) < 15:
        return "insufficient complete observations"
    if np.nanstd(y) < 1e-9:
        return "flat outcome; no observed variation"
    if len(lx) < 3:
        return "not enough points for LOWESS"
    linear_beta = np.linalg.lstsq(
        np.column_stack([np.ones(len(x)), x]), y, rcond=None
    )[0]
    linear_on_lx = linear_beta[0] + linear_beta[1] * lx
    curvature = np.nanmax(np.abs(ly - linear_on_lx)) / max(np.nanstd(y), 1e-9)
    if curvature >= 0.45:
        return "visibly curved"
    if curvature >= 0.2:
        return "mildly curved"
    return "approximately linear or flat"


def lowess_interpretation(n: int, y: np.ndarray, pattern: str) -> str:
    if n < 15:
        return (
            f"Only {n} complete observations; LOWESS is not reliable for judging "
            "non-linearity."
        )
    if np.nanstd(y) < 1e-9:
        return "The outcome has no observed variation, so curvature cannot be assessed."
    if "curved" in pattern:
        return "LOWESS departs from a straight line, suggesting possible non-linear association."
    return "LOWESS does not show strong curvature in the current aggregate panel."


def train_linear(x_train: np.ndarray, y_train: np.ndarray):
    design = np.column_stack([np.ones(len(x_train)), x_train])
    coef = np.linalg.lstsq(design, y_train, rcond=None)[0]
    return lambda x: np.column_stack([np.ones(len(x)), x]) @ coef


@dataclass
class TreeNode:
    prediction: float
    feature: int | None = None
    threshold: float | None = None
    left: "TreeNode | None" = None
    right: "TreeNode | None" = None


class SimpleRegressionTree:
    def __init__(self, max_depth: int = 4, min_leaf: int = 3, max_splits: int = 12, seed: int = 0):
        self.max_depth = max_depth
        self.min_leaf = min_leaf
        self.max_splits = max_splits
        self.rng = np.random.default_rng(seed)
        self.root: TreeNode | None = None

    def fit(self, x: np.ndarray, y: np.ndarray) -> "SimpleRegressionTree":
        self.root = self._build(x, y, depth=0)
        return self

    def _build(self, x: np.ndarray, y: np.ndarray, depth: int) -> TreeNode:
        prediction = float(np.mean(y))
        if depth >= self.max_depth or len(y) < 2 * self.min_leaf or np.var(y) < 1e-12:
            return TreeNode(prediction=prediction)

        n_features = x.shape[1]
        feature_count = max(1, int(round(math.sqrt(n_features))))
        features = self.rng.choice(n_features, size=feature_count, replace=False)
        best: tuple[float, int, float, np.ndarray] | None = None

        for feature in features:
            values = np.unique(x[:, feature])
            values = values[np.isfinite(values)]
            if len(values) <= 1:
                continue
            if len(values) > self.max_splits:
                qs = np.linspace(0.05, 0.95, self.max_splits)
                thresholds = np.unique(np.quantile(values, qs))
            else:
                thresholds = (values[:-1] + values[1:]) / 2
            for threshold in thresholds:
                left_mask = x[:, feature] <= threshold
                right_mask = ~left_mask
                if left_mask.sum() < self.min_leaf or right_mask.sum() < self.min_leaf:
                    continue
                sse = (
                    np.sum((y[left_mask] - np.mean(y[left_mask])) ** 2)
                    + np.sum((y[right_mask] - np.mean(y[right_mask])) ** 2)
                )
                if best is None or sse < best[0]:
                    best = (float(sse), int(feature), float(threshold), left_mask)

        if best is None:
            return TreeNode(prediction=prediction)
        _, feature, threshold, left_mask = best
        return TreeNode(
            prediction=prediction,
            feature=feature,
            threshold=threshold,
            left=self._build(x[left_mask], y[left_mask], depth + 1),
            right=self._build(x[~left_mask], y[~left_mask], depth + 1),
        )

    def predict_one(self, row: np.ndarray) -> float:
        node = self.root
        while node and node.feature is not None and node.threshold is not None:
            node = node.left if row[node.feature] <= node.threshold else node.right
        return float(node.prediction if node else np.nan)

    def predict(self, x: np.ndarray) -> np.ndarray:
        return np.array([self.predict_one(row) for row in x], dtype=float)


class SimpleRandomForest:
    def __init__(self, n_estimators: int = 80, seed: int = 42):
        self.n_estimators = n_estimators
        self.rng = np.random.default_rng(seed)
        self.trees: list[SimpleRegressionTree] = []

    def fit(self, x: np.ndarray, y: np.ndarray) -> "SimpleRandomForest":
        self.trees = []
        for i in range(self.n_estimators):
            sample_idx = self.rng.integers(0, len(y), size=len(y))
            tree = SimpleRegressionTree(seed=int(self.rng.integers(0, 1_000_000)))
            tree.fit(x[sample_idx], y[sample_idx])
            self.trees.append(tree)
        return self

    def predict(self, x: np.ndarray) -> np.ndarray:
        predictions = np.column_stack([tree.predict(x) for tree in self.trees])
        return np.mean(predictions, axis=1)


def metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    rmse = float(np.sqrt(np.mean((y_true - y_pred) ** 2)))
    mae = float(np.mean(np.abs(y_true - y_pred)))
    ss_tot = float(np.sum((y_true - np.mean(y_true)) ** 2))
    r2 = np.nan if ss_tot <= 1e-12 else 1 - float(np.sum((y_true - y_pred) ** 2)) / ss_tot
    return {"rmse": rmse, "mae": mae, "r2": r2}


def cross_validate_models(data: pd.DataFrame) -> list[dict[str, object]]:
    complete = data[[Y_COL, *X_COLS]].dropna().reset_index(drop=True)
    rows: list[dict[str, object]] = []
    n = len(complete)
    note = ""

    if n < 6:
        note = "not enough complete observations for cross-validation"
        for model in ["linear_regression", "random_forest_custom"]:
            rows.append({"model": model, "n_complete": n, "folds": 0, "rmse": np.nan, "mae": np.nan, "r2": np.nan, "note": note})
        return rows

    x = complete[X_COLS].to_numpy(dtype=float)
    y = complete[Y_COL].to_numpy(dtype=float)
    folds = min(5, n)
    rng = np.random.default_rng(2026)
    indices = rng.permutation(n)
    split_indices = np.array_split(indices, folds)

    all_predictions = {
        "linear_regression": np.full(n, np.nan),
        "random_forest_custom": np.full(n, np.nan),
    }
    for fold, test_idx in enumerate(split_indices, start=1):
        train_idx = np.setdiff1d(indices, test_idx)
        linear_predict = train_linear(x[train_idx], y[train_idx])
        all_predictions["linear_regression"][test_idx] = linear_predict(x[test_idx])

        forest = SimpleRandomForest(seed=2026 + fold)
        forest.fit(x[train_idx], y[train_idx])
        all_predictions["random_forest_custom"][test_idx] = forest.predict(x[test_idx])

    if np.nanstd(y) < 1e-12:
        note = "informal_rate has no observed variation in complete cases; predictive comparison cannot identify non-linearity"

    for model, prediction in all_predictions.items():
        row = {"model": model, "n_complete": n, "folds": folds, **metrics(y, prediction), "note": note}
        rows.append(row)
    return rows


def model_evidence_text(model_rows: list[dict[str, object]]) -> str:
    valid = [row for row in model_rows if np.isfinite(row.get("rmse", np.nan))]
    if not valid:
        return "Model comparison was not run because complete observations are insufficient."
    notes = {str(row.get("note", "")) for row in valid if row.get("note")}
    if notes:
        return "; ".join(sorted(notes))
    by_model = {row["model"]: row for row in valid}
    linear = by_model.get("linear_regression")
    forest = by_model.get("random_forest_custom")
    if linear and forest and forest["rmse"] < 0.9 * linear["rmse"]:
        return "Custom RF has at least 10% lower CV RMSE than linear regression."
    if linear and forest:
        return "Custom RF does not materially improve CV RMSE over linear regression."
    return "Model comparison is incomplete."


def main() -> None:
    if not PANEL_PATH.exists():
        raise FileNotFoundError(f"Missing panel file: {PANEL_PATH}")

    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    panel = pd.read_csv(PANEL_PATH)
    log(f"Loaded panel with {len(panel)} rows and {panel['province'].nunique()} provinces")

    model_rows = cross_validate_models(panel)
    pd.DataFrame(model_rows).to_csv(MODEL_PATH, index=False)
    log(f"Wrote {MODEL_PATH.relative_to(PROJECT_ROOT)}")

    evidence = model_evidence_text(model_rows)
    summary_rows = []
    for variable in X_COLS:
        output_name = f"lowess_{Y_COL}_vs_{variable}.png"
        log(f"Drawing LOWESS plot for {Y_COL} vs {variable}")
        result = draw_lowess_plot(panel, variable, FIGURE_DIR / output_name)
        if result["n_complete"] < 15 or panel[Y_COL].dropna().nunique() <= 1:
            conclusion = "cannot assess non-linearity with the current informal-rate file"
        elif "curved" in str(result["visual_pattern"]) and "lower CV RMSE" in evidence:
            conclusion = "possible non-linearity"
        elif "curved" in str(result["visual_pattern"]):
            conclusion = "visual non-linearity needs stronger model evidence"
        else:
            conclusion = "weak evidence of non-linearity"

        summary_rows.append(
            {
                "variable": variable,
                "visual_pattern": result["visual_pattern"],
                "lowess_interpretation": result["lowess_interpretation"],
                "model_evidence": evidence,
                "conclusion": conclusion,
            }
        )

    with SUMMARY_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "variable",
                "visual_pattern",
                "lowess_interpretation",
                "model_evidence",
                "conclusion",
            ],
        )
        writer.writeheader()
        writer.writerows(summary_rows)
    log(f"Wrote {SUMMARY_PATH.relative_to(PROJECT_ROOT)}")

    print("\nModel comparison:")
    print(pd.DataFrame(model_rows).to_string(index=False))
    print("\nNon-linearity summary:")
    print(pd.DataFrame(summary_rows).to_string(index=False))


if __name__ == "__main__":
    main()
