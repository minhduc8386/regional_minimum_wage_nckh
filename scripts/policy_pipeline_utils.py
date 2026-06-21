from __future__ import annotations

import csv
import math
import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[1]
YEARS = list(range(2018, 2025))
WAGE_REGIONS = ["I", "II", "III", "IV"]


def log(step: str, message: str) -> None:
    print(f"[{step}] {message}")


def clean_column_name(name: object) -> str:
    text = str(name).strip().lstrip("\ufeff").lower()
    text = re.sub(r"\s+", "_", text)
    return text


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [clean_column_name(col) for col in out.columns]
    return out


def read_csv_with_header_detection(path: Path, required_columns: list[str]) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")

    required = {clean_column_name(col) for col in required_columns}
    try:
        df = normalize_columns(pd.read_csv(path))
        if required.issubset(df.columns):
            return df
    except Exception:
        df = None

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        for row_idx, row in enumerate(reader):
            normalized = {clean_column_name(col) for col in row}
            if required.issubset(normalized):
                df = normalize_columns(pd.read_csv(path, skiprows=row_idx))
                return df

    raise ValueError(
        f"Could not find a valid CSV header in {path}. "
        f"Required columns: {sorted(required)}"
    )


def normalize_region(value: object) -> str:
    text = str(value).strip().upper()
    text = text.replace("REGION", "").replace("VUNG", "").replace("VÙNG", "")
    text = re.sub(r"[^IVX0-9]", "", text)
    number_to_roman = {"1": "I", "2": "II", "3": "III", "4": "IV"}
    return number_to_roman.get(text, text)


def numeric_series(series: pd.Series) -> pd.Series:
    return pd.to_numeric(
        series.astype(str).str.replace(",", "", regex=False).str.strip(),
        errors="coerce",
    )


def add_check(rows: list[dict[str, object]], dataset: str, check: str, passed: bool, detail: str) -> None:
    status = "PASS" if passed else "FAIL"
    rows.append({"dataset": dataset, "check": check, "status": status, "detail": detail})
    print(f"{status:4} | {dataset:28} | {check:34} | {detail}")


def write_checks(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(path, index=False)


def require_no_failed_checks(rows: list[dict[str, object]]) -> None:
    failed = [row for row in rows if row["status"] == "FAIL"]
    if failed:
        details = "\n".join(
            f"- {row['dataset']} / {row['check']}: {row['detail']}" for row in failed
        )
        raise RuntimeError(f"Validation failed:\n{details}")


def print_panel_diagnostics(df: pd.DataFrame, key_cols: list[str], step: str) -> None:
    log(step, f"shape={df.shape}")
    if "province" in df.columns:
        log(step, f"province_count={df['province'].nunique()}")
    if "year" in df.columns:
        log(step, f"years={sorted(df['year'].dropna().unique().tolist())}")
    if key_cols:
        log(step, f"duplicate_{'-'.join(key_cols)}={int(df.duplicated(key_cols).sum())}")
    log(step, "missing_count=" + str(df.isna().sum().to_dict()))


def pad_domain(values: np.ndarray, pad_ratio: float = 0.08) -> tuple[float, float]:
    values = values[np.isfinite(values)]
    if len(values) == 0:
        return 0.0, 1.0
    low = float(values.min())
    high = float(values.max())
    if low == high:
        pad = max(1.0, abs(low) * pad_ratio)
    else:
        pad = (high - low) * pad_ratio
    return low - pad, high + pad


def scale(value: float, low: float, high: float, start: int, end: int, invert: bool = False) -> int:
    ratio = 0.5 if high == low else (value - low) / (high - low)
    if invert:
        ratio = 1 - ratio
    return int(round(start + ratio * (end - start)))


def format_number(value: float) -> str:
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if abs(value) >= 1_000:
        return f"{value / 1_000:.1f}K"
    return f"{value:.2f}".rstrip("0").rstrip(".")


def lowess(x: np.ndarray, y: np.ndarray, frac: float = 0.65) -> tuple[np.ndarray, np.ndarray]:
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
        weighted = design * weights[:, None]
        try:
            beta = np.linalg.lstsq(weighted.T @ design, weighted.T @ y, rcond=None)[0]
            yhat[i] = beta[0]
        except np.linalg.LinAlgError:
            yhat[i] = np.average(y, weights=np.maximum(weights, 1e-9))
    return x, yhat


def classify_lowess_pattern(x: np.ndarray, y: np.ndarray, lx: np.ndarray, ly: np.ndarray) -> str:
    if len(y) < 20:
        return "insufficient complete observations"
    if np.nanstd(y) < 1e-9:
        return "flat outcome; no observed variation"
    if len(lx) < 3 or np.nanstd(x) < 1e-9:
        return "not enough variation for LOWESS"
    beta = np.linalg.lstsq(np.column_stack([np.ones(len(x)), x]), y, rcond=None)[0]
    linear_on_lx = beta[0] + beta[1] * lx
    curvature = np.nanmax(np.abs(ly - linear_on_lx)) / max(np.nanstd(y), 1e-9)
    if curvature >= 0.45:
        return "visibly curved"
    if curvature >= 0.2:
        return "mildly curved"
    return "approximately linear"


def draw_lowess_plot(data: pd.DataFrame, y_col: str, x_col: str, output_path: Path) -> dict[str, object]:
    complete = data[[y_col, x_col]].dropna()
    x = complete[x_col].to_numpy(dtype=float)
    y = complete[y_col].to_numpy(dtype=float)
    lx, ly = lowess(x, y)

    width, height = 980, 680
    left, right, top, bottom = 115, 45, 70, 105
    plot_w = width - left - right
    plot_h = height - top - bottom
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    x_low, x_high = pad_domain(x)
    y_low, y_high = pad_domain(y)
    draw.text((left, 24), f"{y_col} vs {x_col} with LOWESS", fill=(20, 20, 20), font=font)
    draw.text((left, height - 45), x_col, fill=(30, 30, 30), font=font)
    draw.text((22, top + plot_h // 2), y_col, fill=(30, 30, 30), font=font)

    for i in range(6):
        tx = x_low + (x_high - x_low) * i / 5
        px = scale(tx, x_low, x_high, left, left + plot_w)
        draw.line((px, top, px, top + plot_h), fill=(235, 235, 235))
        draw.text((px - 20, top + plot_h + 12), format_number(tx), fill=(80, 80, 80), font=font)
        ty = y_low + (y_high - y_low) * i / 5
        py = scale(ty, y_low, y_high, top, top + plot_h, invert=True)
        draw.line((left, py, left + plot_w, py), fill=(235, 235, 235))
        draw.text((52, py - 6), format_number(ty), fill=(80, 80, 80), font=font)

    draw.rectangle((left, top, left + plot_w, top + plot_h), outline=(35, 35, 35), width=2)
    for xi, yi in zip(x, y):
        px = scale(xi, x_low, x_high, left, left + plot_w)
        py = scale(yi, y_low, y_high, top, top + plot_h, invert=True)
        draw.ellipse((px - 3, py - 3, px + 3, py + 3), fill=(32, 96, 168), outline=(20, 60, 110))
    if len(lx) >= 2:
        points = [
            (scale(xi, x_low, x_high, left, left + plot_w), scale(yi, y_low, y_high, top, top + plot_h, invert=True))
            for xi, yi in zip(lx, ly)
        ]
        draw.line(points, fill=(205, 55, 55), width=3)

    pattern = classify_lowess_pattern(x, y, lx, ly)
    draw.text((left, height - 75), f"complete observations: {len(complete)} | pattern: {pattern}", fill=(90, 90, 90), font=font)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)
    return {"n_complete": len(complete), "lowess_pattern": pattern}


REGION_COLORS = {
    "I": (45, 95, 170),
    "II": (210, 90, 55),
    "III": (60, 140, 95),
    "IV": (150, 90, 165),
}


def draw_line_chart(data: pd.DataFrame, y_col: str, title: str, output_path: Path) -> None:
    frame = data[["year", "wage_region", y_col]].dropna().drop_duplicates()
    width, height = 980, 660
    left, right, top, bottom = 115, 150, 70, 95
    plot_w = width - left - right
    plot_h = height - top - bottom
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    x_values = np.array(sorted(frame["year"].unique()), dtype=float)
    y_values = frame[y_col].to_numpy(dtype=float)
    x_low, x_high = pad_domain(x_values, 0.02)
    y_low, y_high = pad_domain(y_values)

    draw.text((left, 24), title, fill=(20, 20, 20), font=font)
    for year in sorted(frame["year"].unique()):
        px = scale(year, x_low, x_high, left, left + plot_w)
        draw.line((px, top, px, top + plot_h), fill=(238, 238, 238))
        draw.text((px - 12, top + plot_h + 12), str(int(year)), fill=(80, 80, 80), font=font)
    for i in range(6):
        ty = y_low + (y_high - y_low) * i / 5
        py = scale(ty, y_low, y_high, top, top + plot_h, invert=True)
        draw.line((left, py, left + plot_w, py), fill=(238, 238, 238))
        draw.text((42, py - 6), format_number(ty), fill=(80, 80, 80), font=font)
    draw.rectangle((left, top, left + plot_w, top + plot_h), outline=(35, 35, 35), width=2)

    for idx, region in enumerate(WAGE_REGIONS):
        sub = frame[frame["wage_region"] == region].sort_values("year")
        color = REGION_COLORS[region]
        points = [
            (scale(float(row.year), x_low, x_high, left, left + plot_w), scale(float(getattr(row, y_col)), y_low, y_high, top, top + plot_h, invert=True))
            for row in sub.itertuples(index=False)
        ]
        if len(points) >= 2:
            draw.line(points, fill=color, width=3)
        for px, py in points:
            draw.ellipse((px - 4, py - 4, px + 4, py + 4), fill=color, outline=(40, 40, 40))
        ly = top + 24 + idx * 24
        draw.line((left + plot_w + 28, ly + 5, left + plot_w + 58, ly + 5), fill=color, width=3)
        draw.text((left + plot_w + 66, ly), f"Region {region}", fill=(30, 30, 30), font=font)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)


def draw_distribution_by_region(data: pd.DataFrame, value_col: str, title: str, output_path: Path) -> None:
    frame = data[["wage_region", value_col]].dropna()
    width, height = 900, 620
    left, right, top, bottom = 95, 45, 70, 90
    plot_w = width - left - right
    plot_h = height - top - bottom
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    values = frame[value_col].to_numpy(dtype=float)
    y_low, y_high = pad_domain(values)

    draw.text((left, 24), title, fill=(20, 20, 20), font=font)
    for i in range(6):
        ty = y_low + (y_high - y_low) * i / 5
        py = scale(ty, y_low, y_high, top, top + plot_h, invert=True)
        draw.line((left, py, left + plot_w, py), fill=(238, 238, 238))
        draw.text((32, py - 6), format_number(ty), fill=(80, 80, 80), font=font)
    draw.rectangle((left, top, left + plot_w, top + plot_h), outline=(35, 35, 35), width=2)

    slot_w = plot_w / len(WAGE_REGIONS)
    for idx, region in enumerate(WAGE_REGIONS):
        sub = frame[frame["wage_region"] == region][value_col].to_numpy(dtype=float)
        cx = int(left + slot_w * (idx + 0.5))
        color = REGION_COLORS[region]
        for j, value in enumerate(sub):
            jitter = ((j % 15) - 7) * 2
            py = scale(float(value), y_low, y_high, top, top + plot_h, invert=True)
            draw.ellipse((cx + jitter - 3, py - 3, cx + jitter + 3, py + 3), fill=color, outline=(40, 40, 40))
        if len(sub):
            q1, med, q3 = np.quantile(sub, [0.25, 0.5, 0.75])
            py1 = scale(float(q1), y_low, y_high, top, top + plot_h, invert=True)
            pym = scale(float(med), y_low, y_high, top, top + plot_h, invert=True)
            py3 = scale(float(q3), y_low, y_high, top, top + plot_h, invert=True)
            draw.rectangle((cx - 34, py3, cx + 34, py1), outline=color, width=2)
            draw.line((cx - 40, pym, cx + 40, pym), fill=color, width=3)
        draw.text((cx - 24, top + plot_h + 18), f"Region {region}", fill=(60, 60, 60), font=font)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)


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
    def __init__(self, max_depth: int = 4, min_leaf: int = 5, max_splits: int = 14, seed: int = 0):
        self.max_depth = max_depth
        self.min_leaf = min_leaf
        self.max_splits = max_splits
        self.rng = np.random.default_rng(seed)
        self.root: TreeNode | None = None

    def fit(self, x: np.ndarray, y: np.ndarray) -> "SimpleRegressionTree":
        self.root = self._build(x, y, 0)
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
                thresholds = np.unique(np.quantile(values, np.linspace(0.05, 0.95, self.max_splits)))
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
    def __init__(self, n_estimators: int = 100, seed: int = 2026):
        self.n_estimators = n_estimators
        self.rng = np.random.default_rng(seed)
        self.trees: list[SimpleRegressionTree] = []

    def fit(self, x: np.ndarray, y: np.ndarray) -> "SimpleRandomForest":
        self.trees = []
        for _ in range(self.n_estimators):
            idx = self.rng.integers(0, len(y), size=len(y))
            tree = SimpleRegressionTree(seed=int(self.rng.integers(0, 1_000_000)))
            tree.fit(x[idx], y[idx])
            self.trees.append(tree)
        return self

    def predict(self, x: np.ndarray) -> np.ndarray:
        return np.mean(np.column_stack([tree.predict(x) for tree in self.trees]), axis=1)


class SimpleGradientBoosting:
    def __init__(self, n_estimators: int = 120, learning_rate: float = 0.06, seed: int = 2026):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.rng = np.random.default_rng(seed)
        self.base = 0.0
        self.trees: list[SimpleRegressionTree] = []

    def fit(self, x: np.ndarray, y: np.ndarray) -> "SimpleGradientBoosting":
        self.base = float(np.mean(y))
        pred = np.full(len(y), self.base)
        self.trees = []
        for _ in range(self.n_estimators):
            residual = y - pred
            tree = SimpleRegressionTree(max_depth=2, min_leaf=6, seed=int(self.rng.integers(0, 1_000_000)))
            tree.fit(x, residual)
            update = tree.predict(x)
            pred += self.learning_rate * update
            self.trees.append(tree)
        return self

    def predict(self, x: np.ndarray) -> np.ndarray:
        pred = np.full(len(x), self.base)
        for tree in self.trees:
            pred += self.learning_rate * tree.predict(x)
        return pred


def metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    rmse = float(np.sqrt(np.mean((y_true - y_pred) ** 2)))
    mae = float(np.mean(np.abs(y_true - y_pred)))
    ss_tot = float(np.sum((y_true - np.mean(y_true)) ** 2))
    r2 = np.nan if ss_tot <= 1e-12 else 1 - float(np.sum((y_true - y_pred) ** 2)) / ss_tot
    return {"rmse": rmse, "mae": mae, "r2": r2}


def kfold_indices(n: int, folds: int = 5, seed: int = 2026) -> list[np.ndarray]:
    rng = np.random.default_rng(seed)
    return list(np.array_split(rng.permutation(n), min(folds, n)))
