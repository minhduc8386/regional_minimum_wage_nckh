# Minimum Wage And Informal Employment In Vietnam

Project nghiên cứu: **Tác động nhân quả của chính sách lương tối thiểu vùng đến việc làm phi chính thức tại Việt Nam**.

Mục tiêu hiện tại của repo là hoàn thiện dữ liệu panel tỉnh-năm 2018-2024, bổ sung treatment lương tối thiểu vùng thực tế, kiểm tra treatment variation và kiểm tra phi tuyến trước khi cân nhắc các mô hình nhân quả như OLS/Fixed Effects/DiD/Event Study/DML.

## Cấu Trúc Repo

```text
data/
  raw/                         # Dữ liệu gốc NSO/GSO, policy, CPI
  processed/
    nso_employment/            # Panel Y + W
    policy/                    # Minimum wage và mapping tỉnh-vùng
    economy/                   # CPI panel
    final/                     # Final analysis panel
paper/                         # Paper tham khảo chính
reports/
  figures/                     # Biểu đồ LOWESS và treatment variation
  literature_review/           # Literature review và research gap
  tables/                      # Validation/model summary tables
scripts/                       # Pipeline xử lý dữ liệu và diagnostic
```

## Dữ Liệu Cuối

Final panel:

```text
data/processed/final/analysis_panel_2018_2024.csv
```

Kiểm tra hiện tại:

- 441 dòng = 63 tỉnh/thành x 7 năm
- Giai đoạn: 2018-2024
- 15 cột
- Duplicate `province-year`: 0
- Missing value: 0

Các biến chính:

- `informal_rate`: tỷ lệ việc làm phi chính thức, biến kết quả Y
- `real_min_wage`, `log_real_min_wage`, `min_wage_growth`: biến treatment D
- `unemployment_rate`, `labour_productivity`, `trained_labour_rate`, `employed_persons`, `log_employed_persons`: biến kiểm soát W

## Pipeline

Chạy lại pipeline chính theo thứ tự:

```bash
python scripts/01_clean_nso_province_panel.py
python scripts/02_check_nonlinearity.py
python scripts/03_validate_raw_policy_inputs.py
python scripts/04_build_min_wage_region_panel.py
python scripts/05_build_province_wage_region_map.py
python scripts/06_build_cpi_panel.py
python scripts/07_merge_final_analysis_panel.py
python scripts/08_check_treatment_variation.py
python scripts/09_check_nonlinearity_with_treatment.py
python scripts/10_model_comparison_with_treatment.py
python scripts/11_generate_project_completion_summary.py
```

Ghi chú: scripts hiện dùng `pandas`, `numpy`, `openpyxl`, `pillow`, `pypdf`; các biểu đồ diagnostic được vẽ bằng PIL để tránh phụ thuộc vào matplotlib.

## Output Chính

Validation và bảng kết quả:

```text
reports/tables/raw_policy_input_validation.csv
reports/tables/final_analysis_panel_validation.csv
reports/tables/treatment_variation_summary.csv
reports/tables/nonlinearity_summary_final.csv
reports/tables/model_comparison_linear_vs_ml_final.csv
```

Biểu đồ:

```text
reports/figures/treatment_variation/
reports/figures/nonlinearity/
reports/figures/nonlinearity_final/
```

Tổng hợp:

```text
reports/data_update_summary.md
reports/project_completion_summary.md
reports/advisor_presentation_script.md
```

## Kết Quả Diagnostic Hiện Tại

LOWESS cho thấy một số quan hệ giữa `informal_rate` và treatment/control variables có dấu hiệu phi tuyến, đặc biệt với:

- `log_real_min_wage`
- `unemployment_rate`
- `labour_productivity`
- `employed_persons`
- `log_employed_persons`

Model comparison predictive diagnostic:

- Linear Regression: RMSE khoảng 7.367, R2 khoảng 0.672
- Random Forest custom: RMSE khoảng 5.656, R2 khoảng 0.807
- Gradient Boosting custom: RMSE khoảng 5.615, R2 khoảng 0.810

Các kết quả này chỉ là diagnostic, chưa phải bằng chứng nhân quả.

## Hạn Chế

- Dữ liệu hiện tại là aggregate province-year, chưa phải microdata cá nhân.
- Mapping tỉnh sang vùng lương tối thiểu là province-level approximation.
- Lương tối thiểu vùng thực tế áp dụng theo huyện/quận/thị xã/thành phố thuộc tỉnh, không hoàn toàn đồng nhất ở cấp tỉnh.
- Nhiều province-year rows có ghi chú mixed district regions.
- Chưa chạy OLS/FE/DiD/Event Study/DML chính thức để kết luận nhân quả.
- DML không thay thế chiến lược nhận diện nhân quả; cần baseline causal models và kiểm tra theta stability trước.

## Việc Tiếp Theo

- Đánh giá paper tham khảo chính Del Carpio et al. và kiểm tra loại tài liệu/Q ranking nếu có journal version.
- Làm literature matrix: `paper | data | period | Y | D | W | method | result | limitation | our improvement`.
- Kiểm tra khả năng backtest pipeline DML trên dữ liệu cũ VHLSS/VES 2006-2010.
- Chạy baseline OLS/FE/two-way FE trên dữ liệu mới 2018-2024.
- Nếu chạy DML, tập trung báo cáo `theta`, standard error, p-value, confidence interval và theta stability qua folds/learners/seeds; không chỉ báo RMSE.
