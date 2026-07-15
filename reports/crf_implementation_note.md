# Ghi chú lựa chọn Causal Random Forest implementation (Task 10)

## Lựa chọn: `econml.dml.CausalForestDML` (Python, econml 0.16)

## Vì sao

| Tiêu chí | CausalForestDML (econml) | grf (R) | CausalForestDML được chọn vì |
|---|---|---|---|
| Continuous treatment | Có (`discrete_treatment=False`) | Có | Bắt buộc — D là continuous, không có treated/control nhị phân |
| Orthogonalization | DML residualization tích hợp (model_y, model_t, cross-fitting) | Local centering tương đương | Nhất quán với pipeline DML nhóm đã chạy — CRF và DML dùng chung logic partialling-out, dễ so sánh theta/ATE |
| Cluster theo tỉnh | `groups=province` → GroupKFold khi cross-fitting | `clusters=` | Tôn trọng cấu trúc panel: không để obs cùng tỉnh nằm cả train lẫn test |
| Inference | Bootstrap-of-little-bags CI cho ATE/CATE | Tương tự | Có `ate_interval`, `effect_interval` |
| Ngôn ngữ | Python — cùng stack với toàn bộ scripts của repo | R — thêm dependency mới | Không phá pipeline hiện có |

Đã smoke-test API (fit + ate + ate_interval + effect với groups) trên panel thật: chạy được, không lỗi.

## Setting chính (dùng cho scripts 20–22)

- `model_y`, `model_t`: RandomForestRegressor(n_estimators=200, min_samples_leaf=5) — nuisance learners.
- `n_estimators=1000` (forest chính), `min_samples_leaf=10` — lá to để chống overfit với n=441.
- `cv=5`, `groups=province` (GroupKFold), `discrete_treatment=False`.
- `X` (biến heterogeneity): unemployment_rate, labour_productivity, trained_labour_rate, log_employed_persons.
- `W` (confounders cho residualization): X + year dummies. KHÔNG có province dummies trong main run — để nhất quán với DML gốc; hệ quả (ước lượng dựa trên between-variation) ghi rõ trong limitation.
- Seeds: 42, 123, 2024 (+ 7, 99 cho stability run).

## Ràng buộc diễn giải (bắt buộc)

1. Đây là **exploratory heterogeneity analysis**, không phải bằng chứng nhân quả — identification vẫn là selection-on-observables.
2. n = 441 là rất nhỏ cho forest → CATE nhiễu, chỉ đọc pattern tổng thể (phân phối, dấu), không đọc CATE từng tỉnh.
3. Không cắt heterogeneity theo `wage_region` làm chiều chính — wage_region gần trùng với chính mức treatment. Nếu trình bày, phải kèm caveat này.
4. ATE của CRF với continuous T là **trung bình marginal effect** (đơn vị: điểm % informal_rate trên 1 đơn vị log real min wage), so sánh được với theta của DML.
