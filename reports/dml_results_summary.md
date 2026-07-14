# DML Results Summary

## 1. Mục Tiêu

DML được chạy như một robustness/flexible-control exercise sau baseline OLS/FE/TWFE. Mục tiêu là kiểm tra theta có ổn định khi kiểm soát linh hoạt các nuisance functions hay không, không phải chứng minh tác động nhân quả.

## 2. Specification

- Outcome: `informal_rate`.
- Treatments: `real_min_wage`, `log_real_min_wage`, `min_wage_growth`.
- Controls W: `unemployment_rate`, `labour_productivity`, `trained_labour_rate`, `log_employed_persons` plus year dummies.
- Province dummies are not included in the main DML because the sample is small.
- Cross-fitting: 5 folds with seeds 42, 123, 2024.
- Learners: `ridge_numpy`, `random_forest_custom`, `gradient_boosting_custom`.
- Standard errors: clustered by province when available; fallback is reported if used.

## 3. Main Findings

- `real_min_wage`: theta_mean = `-1.014e-05`, theta_std = `3.921e-06`, share_positive = `0.00`, share_ci_contains_zero = `0.33`. Theta is relatively stable across learners/seeds, but remains a robustness check, not causal proof.
- `log_real_min_wage`: theta_mean = `-33.3366`, theta_std = `12.3548`, share_positive = `0.00`, share_ci_contains_zero = `0.22`. Theta is relatively stable across learners/seeds, but remains a robustness check, not causal proof.
- `min_wage_growth`: theta_mean = `-67.9913`, theta_std = `59.4457`, share_positive = `0.11`, share_ci_contains_zero = `1.00`. Theta changes sign across learners/seeds; treat as unstable exploratory evidence.

## 4. So Sánh Với Baseline Two-way FE

- `real_min_wage`: DML theta_mean = `-1.014e-05`, two-way FE coefficient = `3.688e-06`; DML khác dấu với two-way FE. TWFE p-value = `0.0481`.
- `log_real_min_wage`: DML theta_mean = `-33.3366`, two-way FE coefficient = `13.3251`; DML khác dấu với two-way FE. TWFE p-value = `0.0375`.
- `min_wage_growth`: DML theta_mean = `-67.9913`, two-way FE coefficient = `-18.1496`; DML cùng dấu với two-way FE. TWFE p-value = `0.7656`.

So sánh này chỉ mang tính định hướng vì DML main specification kiểm soát year dummies và W linh hoạt, nhưng không đưa province dummies vào nuisance functions. Two-way FE vẫn là benchmark kinh tế lượng truyền thống.

## 5. Diễn Giải Thận Trọng

Một số theta chưa ổn định về dấu hoặc độ lớn giữa learners/seeds. Điều này cho thấy dữ liệu hiện tại chưa cung cấp bằng chứng đủ mạnh để dùng DML đưa ra kết luận chắc chắn.
Một số confidence intervals chứa 0, vì vậy bằng chứng thống kê về theta chưa đồng nhất giữa các specification DML.

DML cung cấp kiểm tra bổ sung về tính ổn định của theta sau khi kiểm soát linh hoạt các quan hệ phi tuyến. Kết quả cần diễn giải thận trọng do hạn chế identification, dữ liệu aggregate province-year, và province-level wage-region approximation.

Không diễn giải các kết quả này như bằng chứng DML chứng minh lương tối thiểu gây ra thay đổi informal employment.

## 6. Output Files

- `reports/tables/dml_main_results.csv`
- `reports/tables/dml_theta_by_fold.csv`
- `reports/tables/dml_theta_by_seed.csv`
- `reports/tables/dml_theta_by_learner.csv`
- `reports/tables/dml_theta_stability.csv`
- `reports/figures/dml/dml_theta_by_learner.png`
- `reports/figures/dml/dml_theta_by_seed.png`
- `reports/figures/dml/dml_theta_by_fold.png`
