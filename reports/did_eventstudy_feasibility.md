# Kiểm Tra Tính Phù Hợp Của DiD/Event Study

## 1. Mục Tiêu Kiểm Tra

Mục tiêu của ghi chú này là đánh giá liệu panel tỉnh-năm hiện tại có phù hợp để chạy Difference-in-Differences (DiD) hoặc Event Study như một chiến lược nhận diện nhân quả chính hay không.

Kết luận cần được đọc thận trọng: đây là kiểm tra tính phù hợp của thiết kế, không phải kết quả tác động nhân quả.

## 2. Dữ Liệu Sử Dụng

File dữ liệu:

```text
data/processed/final/analysis_panel_2018_2024.csv
```

Đơn vị quan sát:

- Province-year panel.
- 63 tỉnh/thành.
- 7 năm từ 2018 đến 2024.
- 441 quan sát.

Outcome:

- `informal_rate`

Treatment/policy variables:

- `real_min_wage`
- `log_real_min_wage`
- `min_wage_growth`
- `min_wage_nominal` được dùng như biến policy reference.

## 3. Treatment Hiện Tại Là Continuous Hay Binary?

Treatment hiện tại không phải binary treatment.

Trong dữ liệu, mỗi tỉnh-năm đều có một mức lương tối thiểu vùng. Sự khác biệt treatment đến từ:

- Khác biệt giữa các wage region I, II, III, IV.
- Thay đổi theo năm của mức lương tối thiểu danh nghĩa.
- Điều chỉnh CPI để tạo `real_min_wage`.
- Một số ít tỉnh thay đổi wage region theo thời gian.

Số giá trị duy nhất trong final panel:

- `min_wage_nominal`: 23 giá trị.
- `real_min_wage`: 28 giá trị.
- `log_real_min_wage`: 28 giá trị.
- `min_wage_growth`: 23 giá trị.

Vì vậy, treatment phù hợp hơn với mô hình continuous treatment/fixed effects hơn là DiD cổ điển với biến treated = 0/1.

## 4. Có Nhóm Treated/Control Rõ Không?

Không có nhóm untreated/control sạch theo nghĩa DiD cổ điển.

Tất cả các tỉnh/thành đều chịu chính sách lương tối thiểu vùng. Điểm khác nhau là mức độ exposure: tỉnh thuộc vùng I có mức lương tối thiểu cao hơn vùng II, III, IV; các năm sau có mức danh nghĩa cao hơn các năm trước, trừ 2021 không tăng danh nghĩa so với 2020.

Điều này làm DiD cổ điển yếu vì:

- Không có nhóm tỉnh hoàn toàn không bị policy tác động.
- Khác biệt giữa các wage region có thể gắn với khác biệt có sẵn về cơ cấu kinh tế, đô thị hóa, năng suất và thị trường lao động.
- Các yếu tố này cũng có thể ảnh hưởng trực tiếp đến `informal_rate`.

Có 5 tỉnh thay đổi wage region theo thời gian:

- Bac Lieu
- Binh Phuoc
- Binh Thuan
- Ca Mau
- Tay Ninh

Tuy nhiên, số tỉnh switching quá ít để dùng làm thiết kế DiD chính một cách thuyết phục.

## 5. Có Policy Shock Rõ Không?

Mức lương tối thiểu danh nghĩa thay đổi theo năm và theo vùng:

| năm | Region I | Region II | Region III | Region IV |
|---:|---:|---:|---:|---:|
| 2018 | 3,980,000 | 3,530,000 | 3,090,000 | 2,760,000 |
| 2019 | 4,180,000 | 3,710,000 | 3,250,000 | 2,920,000 |
| 2020 | 4,420,000 | 3,920,000 | 3,430,000 | 3,070,000 |
| 2021 | 4,420,000 | 3,920,000 | 3,430,000 | 3,070,000 |
| 2022 | 4,550,000 | 4,040,000 | 3,535,000 | 3,160,000 |
| 2023 | 4,680,000 | 4,160,000 | 3,640,000 | 3,250,000 |
| 2024 | 4,820,000 | 4,285,000 | 3,750,000 | 3,350,000 |

Các thay đổi này là thay đổi policy toàn hệ thống, khác nhau về mức theo wage region. Không có một mốc shock duy nhất chỉ tác động đến một nhóm treated trong khi một nhóm control sạch không bị tác động.

Năm 2021 không có tăng lương danh nghĩa so với 2020. Tuy nhiên, điều này không tạo ra một nhóm treated/control rõ ràng, vì tất cả vùng đều cùng không tăng danh nghĩa trong năm đó.

## 6. Có Đủ Pre-treatment Observations Không?

Panel bắt đầu từ 2018, nên số pre-period phụ thuộc vào mốc shock giả định:

- Nếu chọn 2019 làm shock: chỉ có 1 năm pre-period là 2018.
- Nếu chọn 2020 làm shock: có 2 năm pre-period là 2018-2019.
- Nếu chọn 2022 làm shock: có 4 năm pre-period là 2018-2021, nhưng không có nhóm control sạch.
- Nếu chọn 2023 làm shock: có 5 năm pre-period, nhưng chỉ có 2 năm post-period đến 2024.
- Nếu chọn 2024 làm shock: không có post-period sau shock.

Do đó, việc kiểm tra pre-trend đáng tin cậy bị hạn chế. Ngay cả khi có một vài pre-period, dữ liệu vẫn thiếu nhóm control sạch để so sánh xu hướng.

## 7. Có Nên Chạy DiD/Event Study Không?

Không nên chạy DiD/Event Study cổ điển như causal design chính với dữ liệu hiện tại.

Lý do:

- Treatment là continuous, không phải binary adoption.
- Tất cả tỉnh đều chịu chính sách lương tối thiểu vùng.
- Không có nhóm control hoàn toàn không bị tác động.
- Các wage region khác nhau có thể khác nhau sẵn về mức độ phát triển, cơ cấu việc làm và tỷ lệ phi chính thức.
- Số tỉnh đổi wage region chỉ là 5, chưa đủ mạnh để làm thiết kế switching/event study chính.
- Panel 2018-2024 ngắn, gây hạn chế cho kiểm tra pre-trend và dynamic effects.

Nếu cần minh họa, có thể vẽ event-style descriptive plot quanh các năm điều chỉnh lương tối thiểu, nhưng phải ghi rõ đây là descriptive visualization, không phải causal event study.

## 8. Hướng Thay Thế Phù Hợp Hơn

Trong giai đoạn hiện tại, nên ưu tiên:

1. Fixed Effects baseline

   - OLS.
   - Province FE.
   - Year FE.
   - Two-way FE.
   - Cluster standard errors theo province.

2. Continuous treatment model

   - Dùng `real_min_wage`, `log_real_min_wage`, và `min_wage_growth` như biến treatment liên tục.
   - Diễn giải như association có kiểm soát FE, không quá lời thành causal effect mạnh.

3. Robustness với DML nếu cần

   - Chỉ chạy sau baseline.
   - DML dùng để xử lý nonlinear controls/flexible nuisance functions.
   - Báo cáo theta, standard error, p-value, confidence interval, theta by fold, theta by learner và theta by seed.

4. Event-style descriptive visualization

   - Có thể vẽ xu hướng `informal_rate` theo wage region quanh các năm 2020, 2022, 2023 hoặc 2024.
   - Không gọi đây là causal event study nếu không có identification rõ.

5. Dữ liệu cần bổ sung nếu muốn DiD mạnh hơn

   - Nhóm control rõ ràng không bị policy tác động.
   - Variation do threshold/eligibility hoặc thay đổi địa bàn áp dụng chính sách.
   - Dữ liệu cấp huyện, doanh nghiệp, người lao động, hoặc microdata có thông tin formal/informal và wage exposure.
   - Nhiều năm pre-treatment và post-treatment hơn để kiểm tra pre-trend.

## 9. Kết Luận Ngắn Cho Advisor

Với dữ liệu province-year 2018-2024 hiện tại, DiD/Event Study cổ điển chưa phù hợp làm chiến lược nhận diện chính vì chính sách lương tối thiểu vùng áp dụng cho tất cả tỉnh, treatment là liên tục theo mức lương vùng-năm, và không có nhóm control sạch. Nhóm nên trình bày OLS/FE/TWFE như baseline truyền thống, tiếp tục diễn giải thận trọng, và chỉ dùng DML sau baseline như một robustness/flexible-control approach để kiểm tra phi tuyến, không thay thế identification nhân quả.
