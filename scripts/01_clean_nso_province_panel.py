from __future__ import annotations

import re
from functools import reduce
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_CANDIDATES = [
    PROJECT_ROOT / "data" / "raw" / "nso_employment",
    PROJECT_ROOT / "data" / "raw",
]
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "nso_employment"
OUTPUT_PATH = OUTPUT_DIR / "province_year_panel_2018_2024.csv"
TARGET_YEARS = list(range(2018, 2025))

AGGREGATE_ROWS = {
    "WHOLE COUNTRY",
    "RED RIVER DELTA",
    "NORTHERN MIDLANDS AND MOUNTAIN AREAS",
    "NORTH CENTRAL AND CENTRAL COASTAL AREAS",
    "NORTHERN CENTRAL AREA AND CENTRAL COASTAL AREA",
    "CENTRAL HIGHLANDS",
    "SOUTH EAST",
    "MEKONG RIVER DELTA",
}

DATASETS = {
    "informal_rate": [
        "17_informal_employment_rate_by_province_2018_2024.xlsx",
        "informal_employment_rate_by_province_2018_2024.xlsx",
        "*informal*employment*rate*province*2018*2024*.xlsx",
    ],
    "unemployment_rate": [
        "29_unemployment_rate_by_province_2018_2024.xlsx",
        "*unemployment*rate*province*2018*2024*.xlsx",
    ],
    "labour_productivity": [
        "24_labour_productivity_by_province_2018_2024.xlsx",
        "*labour*productivity*province*2018*2024*.xlsx",
    ],
    "trained_labour_rate": [
        "21_trained_labour_force_by_province_2018_2024.xlsx",
        "21_trained_labour_force_by_province_2008_2024.xlsx",
        "*trained*labour*force*province*.xlsx",
    ],
    "employed_persons": [
        "11_employed_persons_by_province_2018_2024.xlsx",
        "*employed*persons*province*2018*2024*.xlsx",
    ],
}


def log(message: str) -> None:
    print(f"[clean-nso] {message}")


def normalize_space(value: object) -> str:
    return re.sub(r"\s+", " ", str(value).strip())


def row_key(value: object) -> str:
    return normalize_space(value).upper()


def parse_year(value: object) -> int | None:
    if pd.isna(value):
        return None
    if isinstance(value, (int, np.integer)):
        return int(value)
    if isinstance(value, (float, np.floating)) and float(value).is_integer():
        return int(value)
    text = normalize_space(value)
    match = re.search(r"(20\d{2})", text)
    return int(match.group(1)) if match else None


def parse_number(value: object) -> float:
    if pd.isna(value):
        return np.nan
    if isinstance(value, (int, float, np.integer, np.floating)):
        return float(value)
    text = normalize_space(value)
    if text in {"", "..", ".", "-", "--", "—", "–", "NA", "N/A"}:
        return np.nan
    text = text.replace(",", "")
    try:
        return float(text)
    except ValueError:
        return np.nan


def locate_raw_dir() -> Path:
    for directory in RAW_CANDIDATES:
        if directory.exists() and any(directory.glob("*.xlsx")):
            return directory
    raise FileNotFoundError(
        "No Excel files found in data/raw/nso_employment or data/raw."
    )


def resolve_file(raw_dir: Path, candidates: list[str]) -> Path:
    for candidate in candidates:
        exact = raw_dir / candidate
        if exact.exists():
            return exact
        matches = sorted(raw_dir.glob(candidate))
        if matches:
            return matches[0]
    raise FileNotFoundError(f"Could not resolve any candidate: {candidates}")


def detect_header(raw: pd.DataFrame) -> tuple[int, int, dict[int, int]]:
    best: tuple[int, int, dict[int, int]] | None = None
    best_count = -1

    for row_idx, row in raw.iterrows():
        all_year_cols: dict[int, int] = {}
        year_cols: dict[int, int] = {}
        for col_idx, value in row.items():
            year = parse_year(value)
            if year is not None:
                all_year_cols[year] = int(col_idx)
                if year in TARGET_YEARS and year not in year_cols:
                    year_cols[year] = int(col_idx)
        if len(year_cols) > best_count:
            first_year_col = min(all_year_cols.values()) if all_year_cols else -1
            province_col = max(0, first_year_col - 1)
            best = (int(row_idx), province_col, year_cols)
            best_count = len(year_cols)

    if best is None or best_count < 3:
        raise ValueError("Could not detect a header row with enough target years.")
    return best


def clean_one_file(path: Path, variable: str) -> pd.DataFrame:
    log(f"Reading {variable}: {path.relative_to(PROJECT_ROOT)}")
    excel = pd.ExcelFile(path)
    frames: list[pd.DataFrame] = []

    for sheet_name in excel.sheet_names:
        raw = pd.read_excel(path, sheet_name=sheet_name, header=None, dtype=object)
        raw = raw.dropna(how="all").dropna(axis=1, how="all")
        if raw.empty:
            log(f"  - Sheet {sheet_name}: skipped empty sheet")
            continue

        header_row, province_col, year_cols = detect_header(raw)
        selected_years = sorted(year_cols)
        log(
            "  - Sheet "
            f"{sheet_name}: header row={header_row}, province col={province_col}, "
            f"years={selected_years}"
        )

        records: list[dict[str, object]] = []
        for row_idx in range(header_row + 1, len(raw)):
            province_raw = raw.iat[row_idx, province_col]
            if pd.isna(province_raw):
                continue
            province = normalize_space(province_raw)
            if not province:
                continue
            key = row_key(province)
            if key in AGGREGATE_ROWS:
                continue
            if key.startswith(("NOTE", "SOURCE", "UNIT")) or "(*)" in key:
                continue

            values = {
                year: parse_number(raw.iat[row_idx, col_idx])
                for year, col_idx in year_cols.items()
            }
            if all(pd.isna(v) for v in values.values()):
                continue
            for year in TARGET_YEARS:
                if year in values:
                    records.append(
                        {"province": province, "year": year, variable: values[year]}
                    )

        frame = pd.DataFrame.from_records(records)
        log(
            f"  - Sheet {sheet_name}: kept {frame['province'].nunique() if not frame.empty else 0} "
            f"province(s), {len(frame)} province-year rows"
        )
        frames.append(frame)

    if not frames:
        raise ValueError(f"No usable data found for {variable} in {path}")

    data = pd.concat(frames, ignore_index=True)
    duplicated = data.duplicated(["province", "year"], keep=False)
    if duplicated.any():
        duplicate_count = int(duplicated.sum())
        log(f"  - Warning: {duplicate_count} duplicate rows; averaging duplicates")
        data = (
            data.groupby(["province", "year"], as_index=False)[variable]
            .mean(numeric_only=True)
        )

    missing_share = data[variable].isna().mean()
    log(
        f"  - Final {variable}: rows={len(data)}, provinces={data['province'].nunique()}, "
        f"missing={missing_share:.1%}"
    )
    return data


def print_panel_diagnostics(panel: pd.DataFrame) -> None:
    variables = [col for col in panel.columns if col not in {"province", "year"}]
    log("Merged panel diagnostics")
    print(f"rows: {len(panel)}")
    print(f"columns: {len(panel.columns)}")
    print(f"province_count: {panel['province'].nunique()}")
    print(f"year_count: {panel['year'].nunique()}")
    print(f"years: {sorted(panel['year'].dropna().unique().tolist())}")

    print("\nMissing share by variable:")
    print(panel[variables].isna().mean().sort_values(ascending=False).to_string())

    duplicate_count = int(panel.duplicated(["province", "year"]).sum())
    print(f"\nDuplicate province-year rows: {duplicate_count}")

    expected_years = set(TARGET_YEARS)
    missing_year_rows = []
    for province, group in panel.groupby("province"):
        observed = set(group.loc[group[variables].notna().any(axis=1), "year"])
        missing = sorted(expected_years - observed)
        if missing:
            missing_year_rows.append((province, missing))
    print("\nProvinces missing any year in the merged province-year skeleton:")
    if missing_year_rows:
        for province, missing in missing_year_rows:
            print(f"- {province}: {missing}")
    else:
        print("None")

    print("\nVariable-specific provinces with all values missing:")
    for variable in variables:
        empty_provinces = (
            panel.groupby("province")[variable]
            .apply(lambda s: s.isna().all())
            .loc[lambda s: s]
            .index.tolist()
        )
        preview = ", ".join(empty_provinces[:12])
        suffix = " ..." if len(empty_provinces) > 12 else ""
        print(f"- {variable}: {len(empty_provinces)} province(s){': ' + preview + suffix if preview else ''}")

    print("\nDescriptive statistics:")
    print(panel[variables].describe().T.to_string())

    print("\nPreview:")
    print(panel.head(12).to_string(index=False))


def main() -> None:
    raw_dir = locate_raw_dir()
    log(f"Using raw directory: {raw_dir.relative_to(PROJECT_ROOT)}")

    cleaned_frames = []
    for variable, candidates in DATASETS.items():
        path = resolve_file(raw_dir, candidates)
        cleaned_frames.append(clean_one_file(path, variable))

    panel = reduce(
        lambda left, right: pd.merge(left, right, on=["province", "year"], how="outer"),
        cleaned_frames,
    )

    provinces = sorted(panel["province"].dropna().unique().tolist())
    full_index = pd.MultiIndex.from_product(
        [provinces, TARGET_YEARS], names=["province", "year"]
    ).to_frame(index=False)
    panel = full_index.merge(panel, on=["province", "year"], how="left")
    panel = panel.sort_values(["province", "year"]).reset_index(drop=True)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    panel.to_csv(OUTPUT_PATH, index=False)
    log(f"Wrote {OUTPUT_PATH.relative_to(PROJECT_ROOT)}")
    print_panel_diagnostics(panel)

    expected_rows = 63 * len(TARGET_YEARS)
    if len(panel) != expected_rows:
        log(
            f"Warning: panel has {len(panel)} rows, expected {expected_rows} "
            "for 63 provinces x 7 years."
        )
    if panel["province"].nunique() != 63:
        log(
            f"Warning: panel has {panel['province'].nunique()} provinces, expected 63."
        )


if __name__ == "__main__":
    main()
