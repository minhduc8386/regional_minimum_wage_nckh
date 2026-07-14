# DML Decision Note

## 1. Mục Tiêu

Ghi chú này giải thích vì sao nhóm cân nhắc chạy Double/Debiased Machine Learning (DML) sau khi đã hoàn thành baseline OLS/Fixed Effects/Two-way Fixed Effects.

DML chỉ được dùng sau baseline và không thay thế chiến lược nhận diện nhân quả. Trong project này, DML được xem như một robustness/flexible-control exercise nhằm kiểm tra liệu hệ số theta có ổn định hơn khi kiểm soát linh hoạt các quan hệ phi tuyến trong dữ liệu hay không.

## 2. Cơ Sở Để Cân Nhắc DML

Nhóm đã có bằng chứng diagnostic cho thấy quan hệ giữa `informal_rate` và một số biến treatment/control có dấu hiệu phi tuyến:

- LOWESS cho thấy `log_real_min_wage`, `unemployment_rate`, `labour_productivity`, `employed_persons`, và `log_employed_persons` có dạng visibly curved.
- `real_min_wage`, `min_wage_growth`, và `trained_labour_rate` có dạng mildly curved.
- Random Forest và Gradient Boosting dự báo `informal_rate` tốt hơn Linear Regression trong cross-validation.

Tuy nhiên, các kết quả này chỉ là predictive/diagnostic evidence. Chúng không phải causal evidence và không chứng minh chính sách lương tối thiểu gây thay đổi tỷ lệ việc làm phi chính thức.

## 3. DML Có Thể Giúp Gì?

DML có thể hỗ trợ kiểm soát linh hoạt các nuisance functions:

- `E[Y | W]`: phần kỳ vọng của `informal_rate` theo các biến kiểm soát.
- `E[D | W]`: phần kỳ vọng của treatment theo các biến kiểm soát.

Cách tiếp cận partialling-out giúp giảm phụ thuộc vào giả định tuyến tính trong phần kiểm soát W. Khi dùng nhiều learners khác nhau, nhóm có thể kiểm tra liệu theta có ổn định qua learner, seed và fold hay không.

## 4. DML Không Giải Quyết Được Gì?

DML không tự tạo ra exogenous variation.

DML cũng không tự xử lý hoàn toàn:

- Policy endogeneity.
- Policy selection theo điều kiện kinh tế địa phương.
- Các time-varying shocks cấp tỉnh.
- Việc thiếu một nhóm control sạch cho DiD/Event Study.
- Hạn chế của dữ liệu aggregate province-year.
- Sai số do province-level wage-region approximation.

Vì vậy, DML không thay thế DiD, IV, RDD, natural experiment hoặc một thiết kế nhận diện nhân quả mạnh hơn.

## 5. Điều Kiện Để Chạy DML

Nhóm chỉ chạy DML sau khi các điều kiện sau đã được đáp ứng:

- Baseline OLS/FE/TWFE đã hoàn thành.
- DiD/Event Study feasibility đã được đánh giá.
- DML được xác định là robustness/flexible-control approach, không phải identification chính.
- Kết quả DML phải báo cáo theta, standard error, p-value, confidence interval và stability theo fold, learner, seed.

## 6. Quyết Định

Nhóm sẽ chạy DML như một robustness/flexible-control exercise sau baseline. Kết quả DML sẽ được diễn giải thận trọng và chỉ dùng để xem theta có ổn định khi kiểm soát phi tuyến hay không.

Nếu theta ổn định và cùng hướng với baseline FE/TWFE, kết quả chỉ được xem là bằng chứng gợi ý hỗ trợ robustness. Nếu theta không ổn định, khác dấu giữa learners/seeds/folds, hoặc confidence interval thường chứa 0, nhóm sẽ ghi rõ rằng DML chưa cung cấp bằng chứng đủ mạnh để đưa ra kết luận chắc chắn.
