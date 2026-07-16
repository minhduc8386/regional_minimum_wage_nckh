# Minimum Wage And Informal Employment In Vietnam

Đề tài nghiên cứu: **Tác động của chính sách lương tối thiểu vùng đến việc làm phi chính thức tại Việt Nam** — panel tỉnh-năm 2018–2024 (63 tỉnh/thành, 441 quan sát).

Repo chứa toàn bộ pipeline: làm sạch dữ liệu → xây panel → diagnostic phi tuyến → baseline OLS/FE/TWFE → DML (kèm stability checks) → Causal Forest DML → bảng so sánh phương pháp → draft paper.

**Khung diễn giải xuyên suốt:** kết quả là *association có kiểm soát* và *robustness diagnostics*, không phải bằng chứng nhân quả cuối cùng. DML/CRF đóng vai trò flexible-control / heterogeneity check, không thay thế identification strategy.

## Cài Đặt Môi Trường

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Yêu cầu Python >= 3.10. Scripts 14–23 cần thêm `scikit-learn`, `econml`, `scipy`, `matplotlib` (đã có trong requirements.txt).

## Cấu Trúc Repo

```text
data/
  raw/                         # Dữ liệu gốc NSO/GSO, policy lương tối thiểu, CPI
  processed/
    nso_employment/            # Panel Y + W
    policy/                    # Minimum wage vùng và mapping tỉnh-vùng
    economy/                   # CPI panel
    final/                     # analysis_panel_2018_2024.csv (panel cuối)
paper/                         # Draft paper + tài liệu tham khảo chính
reports/
  figures/                     # Hình: LOWESS, residualized LOWESS, PDP, DML, CRF
  literature_review/           # Literature review, matrix, research gap
  tables/                      # Toàn bộ bảng validation/kết quả (CSV)
  *.md                         # Các section/note phân tích (xem Catalog bên dưới)
scripts/                       # Pipeline đánh số 01-23, chạy theo thứ tự
archive/                       # File legacy đã thay thế (gitignored)
```

## Panel Cuối

`data/processed/final/analysis_panel_2018_2024.csv` — 441 dòng (63 tỉnh × 7 năm), 0 missing, 0 duplicate, panel cân bằng.

| Vai trò | Biến |
|---|---|
| Y | `informal_rate` (điểm %, khoảng quan sát 28.4–91.1) |
| D chính | `log_real_min_wage`; robustness: `real_min_wage` |
| D exploratory | `min_wage_growth` (không dùng làm kết quả chính — xem `reports/specification_y_d_w.md`) |
| W | `unemployment_rate`, `labour_productivity`, `trained_labour_rate`, `log_employed_persons` |

Quy tắc: không đưa `employed_persons` và `log_employed_persons` vào cùng một specification.

## Pipeline

Chạy theo thứ tự. Nhóm A–C tái lập dữ liệu và baseline; nhóm D–E là diagnostic nâng cao và flexible methods.

**A. Dữ liệu (01–07)**

```bash
python scripts/01_clean_nso_province_panel.py          # Làm sạch panel NSO Y + W
python scripts/03_validate_raw_policy_inputs.py        # Validate input policy thô
python scripts/04_build_min_wage_region_panel.py       # Panel lương tối thiểu theo vùng
python scripts/05_build_province_wage_region_map.py    # Mapping tỉnh -> vùng lương
python scripts/06_build_cpi_panel.py                   # CPI panel (deflator, base 2018)
python scripts/07_merge_final_analysis_panel.py        # Merge panel phân tích cuối
```

**B. Diagnostic ban đầu (08–11)**

```bash
python scripts/08_check_treatment_variation.py         # Variation của treatment theo vùng/năm
python scripts/09_check_nonlinearity_with_treatment.py # LOWESS thô Y vs D/W
python scripts/10_model_comparison_with_treatment.py   # Predictive: Linear vs RF vs GBM
python scripts/11_generate_project_completion_summary.py
```

**C. Baseline + DML gốc (12–13)**

```bash
python scripts/12_run_baseline_ols_fe.py               # Pooled OLS / Year FE / Province FE / TWFE, cluster SE
python scripts/13_run_dml_theta_stability.py           # DML partialling-out, theta stability (learner/seed/fold)
```

**D. Diagnostic nâng cao (14–17)**

```bash
python scripts/14_validate_inputs_enhanced_models.py   # Gate validation trước khi chạy model mới
python scripts/15_residualized_lowess.py               # Residualized LOWESS (FWL), 2 spec
python scripts/16_pdp_feature_importance.py            # PDP + permutation importance (predictive)
python scripts/17_formal_nonlinearity_tests.py         # Ramsey RESET + quadratic Wald tests, cluster SE
```

**E. DML sweeps + CRF (18–23)** — các script 18/19/22 chạy theo chunk qua CLI (xem docstring từng file):

```bash
# DML K-fold sweep (K=2/5/10) + bảng diễn giải
python scripts/18_dml_kfold_sweep_and_interpretation.py run <treatment> <K>   # cho từng cặp
python scripts/18_dml_kfold_sweep_and_interpretation.py combine

# DML variant có province dummies (đối chiếu TWFE)
python scripts/19_dml_province_fe_variant.py run <treatment>
python scripts/19_dml_province_fe_variant.py combine

# Causal Forest DML (econml), GroupKFold theo tỉnh
python scripts/20_run_crf_main.py <treatment>          # chạy cho từng treatment
python scripts/21_crf_cate_distribution_heterogeneity.py
python scripts/22_crf_stability_by_seed.py <treatment> <seed> [leaf]
python scripts/22_crf_stability_by_seed.py summarize

# Bảng so sánh tổng hợp
python scripts/23_method_comparison_table.py
```

`<treatment>` ∈ {`log_real_min_wage`, `real_min_wage`, `min_wage_growth`}. Seeds chuẩn của dự án: 42, 123, 2024 (CRF stability thêm 7, 99).

## Catalog Output Chính

**Bảng kết quả (reports/tables/):**

| File | Nội dung |
|---|---|
| `baseline_ols_fe_results.csv` | Baseline OLS/FE/TWFE, cluster SE |
| `dml_main_results.csv`, `dml_theta_stability.csv`, `dml_theta_by_{fold,learner,seed,k}.csv` | DML gốc (W + year dummies) và stability |
| `dml_convergence_interpretation.csv` | Bảng diễn giải stability tổng hợp (sinh bởi script 18) |
| `dml_theta_province_fe.csv` | DML variant có province dummies (script 19) |
| `crf_ate_results.csv`, `crf_cate_summary.csv`, `crf_stability_by_seed.csv`, `crf_heterogeneity.csv` | Causal Forest DML |
| `method_comparison_summary.csv` | **Bảng so sánh phương pháp chuẩn** (19 dòng, kèm diễn giải tiếng Việt) |
| `nonlinearity_formal_tests.csv`, `residualized_lowess_summary.csv`, `pdp_summary.csv`, `feature_importance.csv` | Bằng chứng phi tuyến |
| `enhanced_model_input_validation.csv` | Gate validation (27 checks) |

**Section/note phân tích (reports/):** `specification_y_d_w.md` (spec chuẩn Y-D-W + FE theo method) · `nonlinearity_evidence.md` · `why_linear_ols_may_be_limited.md` · `dml_theta_convergence_interpretation.md` + `dml_interpretation_vi.md` · `dml_treatment_choice.md` (hierarchy main/robustness/exploratory) · `crf_implementation_note.md` · `model_family_comparison.md` · `literature_comparison_current_results.md` · `main_results_narrative.md` · `limitations_section.md`.

**Paper:** `paper/initial_draft.md`.

## Tóm Tắt Kết Quả (thận trọng)

- Phi tuyến: RESET bác bỏ linearity ở cả 6 spec kiểm tra; phi tuyến tập trung ở quan hệ W–Y (nuisance), không phải quan hệ D–Y — đây là lý do dùng DML làm flexible-control robustness.
- Baseline sign reversal: pooled/year-FE cho hệ số âm; province-FE/TWFE cho hệ số dương. ~95% variance của treatment là between-province.
- DML gốc (W + year): theta âm ổn định tương đối qua learner/seed/fold/K (không phải "hội tụ"). DML thêm province dummies: tín hiệu yếu, dấu không ổn định → khác biệt với TWFE do nguồn variation, không chỉ do phi tuyến.
- CRF: cùng hướng âm với DML nhưng magnitude nhạy seed, CI thường chứa 0 — chỉ là exploratory heterogeneity.
- Kết luận: bằng chứng nhạy với specification và nguồn variation; không kết luận nhân quả mạnh. Chi tiết: `reports/main_results_narrative.md`, hạn chế: `reports/limitations_section.md`.
