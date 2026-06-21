# Kịch Bản Trình Bày Với Thầy

Mục tiêu: trình bày tiến độ hiện tại theo đúng góp ý của thầy, tập trung vào hai vấn đề: bộ dữ liệu và các nghiên cứu trước đã làm gì. Kịch bản này phù hợp cho phần share màn hình khoảng 5-8 phút.

## 1. Mở Đầu

Thưa thầy, sau góp ý buổi trước, nhóm em tập trung vào hai việc chính.

Thứ nhất là hoàn thiện bộ dữ liệu để xác định rõ biến kết quả, biến chính sách và các biến kiểm soát.

Thứ hai là xem các nghiên cứu trước trong chủ đề lương tối thiểu đã làm gì, dùng dữ liệu gì, phương pháp gì, và nhóm em có thể cải tiến ở đâu.

Hiện tại nhóm em chưa chạy DML ngay. Nhóm em mới hoàn thiện dữ liệu và kiểm tra trước xem dữ liệu có dấu hiệu phi tuyến hay không.

## 2. Show Final Dataset

Mở file:

`data/processed/final/analysis_panel_2018_2024.csv`

Nói:

Đây là bộ dữ liệu cuối nhóm em đã tạo. Dữ liệu có dạng panel tỉnh-năm, gồm 63 tỉnh/thành trong 7 năm từ 2018 đến 2024, tổng cộng 441 quan sát.

Sau khi kiểm tra, dữ liệu không có missing value và không có dòng trùng tỉnh-năm.

Trong bộ dữ liệu này:

- Biến kết quả là `informal_rate`, nghĩa là tỷ lệ việc làm phi chính thức.
- Biến chính sách là lương tối thiểu vùng, gồm `min_wage_nominal`, `real_min_wage`, `log_real_min_wage` và `min_wage_growth`.
- Các biến kiểm soát gồm tỷ lệ thất nghiệp, năng suất lao động, tỷ lệ lao động qua đào tạo và số người có việc làm.

Giải thích thêm nếu thầy hỏi:

Lương tối thiểu danh nghĩa là mức lương ghi trong nghị định. Lương tối thiểu thực tế là mức lương đã điều chỉnh theo CPI để đưa về mặt bằng giá năm 2018.

## 3. Show Validation

Mở file:

`reports/tables/final_analysis_panel_validation.csv`

Nói:

Đây là bảng kiểm tra sau khi merge dữ liệu. Panel cuối có đúng 441 dòng, 63 tỉnh, 7 năm, không duplicate tỉnh-năm và không thiếu các biến chính như vùng lương, lương tối thiểu, CPI, lương tối thiểu thực tế.

Nhóm em làm bước này để đảm bảo trước khi phân tích mô hình thì dữ liệu không bị lỗi merge hoặc mất quan sát.

## 4. Show Treatment Variation

Mở hình:

`reports/figures/treatment_variation/real_min_wage_by_region_over_time.png`

Nói:

Đây là biến chính sách của nhóm em, tức lương tối thiểu thực tế theo vùng lương tối thiểu qua thời gian.

Treatment variation đến chủ yếu từ hai nguồn:

- thay đổi theo năm;
- khác biệt giữa bốn vùng lương tối thiểu I, II, III, IV.

Ngoài ra, có một số tỉnh thay đổi vùng lương tối thiểu qua thời gian.

Tuy nhiên nhóm em ghi rõ đây chưa phải variation cấp cá nhân. Vì dữ liệu hiện tại là cấp tỉnh-năm, treatment cũng đang được gán ở cấp tỉnh-năm.

Nếu thầy hỏi về mapping:

Lương tối thiểu vùng thực tế áp dụng theo cấp huyện/quận/thị xã, nhưng dữ liệu nhóm em hiện ở cấp tỉnh-năm. Vì vậy mapping tỉnh sang vùng lương tối thiểu là xấp xỉ. Đây là hạn chế quan trọng của dữ liệu.

## 5. Show LOWESS Với Treatment

Mở hình:

`reports/figures/nonlinearity_final/lowess_informal_rate_vs_log_real_min_wage.png`

Nói:

Theo góp ý của thầy, nhóm em kiểm tra trước xem quan hệ giữa biến kết quả và các biến chính sách/kiểm soát có tuyến tính hay không.

Ở đây biến kết quả là tỷ lệ việc làm phi chính thức, còn biến chính sách là log của lương tối thiểu thực tế.

Đường LOWESS là đường xu hướng linh hoạt, không ép dữ liệu đi theo đường thẳng. Kết quả cho thấy quan hệ có dạng cong, tức là không hoàn toàn tuyến tính.

Điều này gợi ý rằng nếu chỉ dùng hồi quy tuyến tính đơn giản thì có thể chưa kiểm soát tốt quan hệ giữa Y và biến chính sách.

## 6. Show LOWESS Với Biến Kiểm Soát

Mở lần lượt 2-3 hình tiêu biểu:

`reports/figures/nonlinearity_final/lowess_informal_rate_vs_unemployment_rate.png`

`reports/figures/nonlinearity_final/lowess_informal_rate_vs_labour_productivity.png`

`reports/figures/nonlinearity_final/lowess_informal_rate_vs_log_employed_persons.png`

Nói:

Nhóm em cũng kiểm tra quan hệ giữa tỷ lệ việc làm phi chính thức và các biến kiểm soát.

Một số quan hệ cũng có dạng cong rõ, ví dụ với tỷ lệ thất nghiệp, năng suất lao động và quy mô việc làm.

Điều này quan trọng vì DML có ý nghĩa khi các quan hệ giữa biến kết quả, biến chính sách và biến nhiễu không đơn giản là tuyến tính.

## 7. Show Nonlinearity Summary

Mở file:

`reports/tables/nonlinearity_summary_final.csv`

Nói:

Bảng này tổng hợp kết quả LOWESS.

Với biến chính sách:

- `log_real_min_wage` có quan hệ cong rõ với tỷ lệ việc làm phi chính thức.
- `min_wage_nominal`, `real_min_wage` và `min_wage_growth` có quan hệ cong nhẹ.

Với biến kiểm soát:

- tỷ lệ thất nghiệp, năng suất lao động, số người có việc làm và log số người có việc làm đều có quan hệ cong rõ.

Vì vậy nhóm em kết luận ở mức diagnostic rằng dữ liệu có dấu hiệu phi tuyến.

Nhóm em chưa xem đây là bằng chứng nhân quả.

## 8. Show Model Comparison

Mở file:

`reports/tables/model_comparison_linear_vs_ml_final.csv`

Nói:

Ngoài LOWESS, nhóm em so sánh khả năng dự báo tỷ lệ việc làm phi chính thức giữa hồi quy tuyến tính và các mô hình học máy phi tuyến.

Kết quả:

- Hồi quy tuyến tính có RMSE khoảng 7.37 và R2 khoảng 0.67.
- Random Forest có RMSE khoảng 5.66 và R2 khoảng 0.81.
- Gradient Boosting có RMSE khoảng 5.62 và R2 khoảng 0.81.

RMSE càng thấp càng tốt, còn R2 càng cao càng tốt. Như vậy mô hình học máy dự báo tốt hơn hồi quy tuyến tính khá rõ.

Điều này củng cố thêm nhận định rằng dữ liệu có quan hệ phi tuyến.

Nhưng nhóm em hiểu đây chỉ là predictive diagnostic, không phải causal estimate.

## 9. Show Paper Del Carpio Et Al.

Mở PDF:

`paper/MPRA_paper_83677.pdf`

Nên show trang abstract hoặc phần data/method.

Nói:

Nhóm em cũng bắt đầu kiểm tra các nghiên cứu trước. Một paper nền quan trọng là bài của Del Carpio, Nguyen, Nguyen và Wang về tác động của lương tối thiểu ở Việt Nam.

Paper này dùng Vietnam Enterprise Survey và VHLSS giai đoạn 2006-2010. Họ nghiên cứu tác động của lương tối thiểu đến việc làm, lương, tự làm và phúc lợi hộ gia đình.

Phương pháp họ dùng gồm OLS, province fixed effects, district fixed effects và firm fixed effects.

Kết quả chính của họ là tăng lương tối thiểu làm giảm wage employment, đặc biệt ở doanh nghiệp trong nước, và một phần lao động chuyển sang tự làm. Paper cũng có đề cập informal contracts và informal workers.

Tuy nhiên, paper này chưa lấy tỷ lệ việc làm phi chính thức cấp tỉnh-năm làm biến kết quả chính, chưa dùng dữ liệu giai đoạn mới 2018-2024, và chưa dùng DML hoặc causal machine learning.

## 10. Gap Và Điểm Mới Của Nhóm

Nói:

Từ paper này, nhóm em học được cách xây dựng lương tối thiểu thực tế, cách dùng variation theo vùng và thời gian, và cách chạy fixed effects làm baseline.

Điểm nhóm em muốn mở rộng là:

Thứ nhất, dùng dữ liệu mới hơn, giai đoạn 2018-2024.

Thứ hai, tập trung trực tiếp vào tỷ lệ việc làm phi chính thức ở cấp tỉnh-năm.

Thứ ba, trước khi dùng DML, nhóm em đã kiểm tra và thấy quan hệ giữa Y, D và W có dấu hiệu phi tuyến.

Thứ tư, nhóm em dự kiến chạy OLS, Fixed Effects, Difference-in-Differences hoặc Event Study làm baseline trước, sau đó mới cân nhắc DML để xử lý phần phi tuyến trong quan hệ giữa Y, D và W.

## 11. Giải Thích DML Bằng Tiếng Việt

Nếu thầy hỏi DML thêm được gì, nói:

DML không thay thế thiết kế nhân quả. Nhóm em vẫn cần chiến lược nhận diện như Fixed Effects, Difference-in-Differences hoặc Event Study.

Điểm DML có thể thêm là dùng học máy để kiểm soát linh hoạt các quan hệ phi tuyến giữa biến kết quả, biến chính sách và các biến nhiễu.

Trong dữ liệu hiện tại, nhóm em đã visualize và thấy nhiều quan hệ phi tuyến. Vì vậy, DML là hướng hợp logic để thử sau khi có baseline causal models.

Nhóm em không kết luận DML chắc chắn tốt hơn OLS về mặt nhân quả ở bước này.

## 12. Hạn Chế Cần Nói Rõ

Nói:

Hiện tại nhóm em có một số hạn chế.

Thứ nhất, dữ liệu là aggregate province-year, chưa phải dữ liệu cá nhân.

Thứ hai, mapping tỉnh sang vùng lương tối thiểu là xấp xỉ, vì chính sách thực tế áp dụng theo cấp huyện/quận/thị xã.

Thứ ba, nhiều tỉnh có mixed district regions, nên treatment assignment có thể có sai số đo lường.

Thứ tư, LOWESS và model comparison chỉ là diagnostic, chưa phải bằng chứng nhân quả.

Thứ năm, nhóm em chưa chạy OLS/FE/DiD/Event Study và chưa chạy DML chính thức.

Thứ sáu, literature review vẫn cần đào sâu hơn bằng Connected Papers và bảng literature matrix.

## 13. Kết Luận Ngắn

Nói:

Tóm lại, đến hiện tại nhóm em đã hoàn thiện dữ liệu Y, D và W; đã kiểm tra dữ liệu không missing, không duplicate; đã xác định treatment variation; đã kiểm tra phi tuyến bằng LOWESS và model comparison; và đã bắt đầu đối chiếu với paper nền ở Việt Nam.

Kết quả hiện tại cho thấy dữ liệu có dấu hiệu phi tuyến, nên DML là một hướng có cơ sở để cân nhắc.

Tuy nhiên, nhóm em chưa kết luận nhân quả. Bước tiếp theo là hoàn thiện literature matrix và chạy các mô hình nền như OLS, Fixed Effects, Difference-in-Differences hoặc Event Study trước khi dùng DML.

## 14. Bản Nói Rất Ngắn Nếu Thời Gian Ít

Thưa thầy, hiện nhóm em đã hoàn thiện panel tỉnh-năm 2018-2024 với 63 tỉnh và 441 quan sát. Biến kết quả là tỷ lệ việc làm phi chính thức, biến chính sách là lương tối thiểu vùng thực tế sau khi điều chỉnh CPI, và biến kiểm soát gồm thất nghiệp, năng suất lao động, lao động qua đào tạo và số người có việc làm.

Nhóm em chưa chạy DML ngay mà kiểm tra trước tính phi tuyến. LOWESS cho thấy tỷ lệ việc làm phi chính thức có quan hệ cong với log lương tối thiểu thực tế, tỷ lệ thất nghiệp, năng suất lao động và quy mô việc làm. Model comparison cũng cho thấy Random Forest và Gradient Boosting dự báo tốt hơn hồi quy tuyến tính.

Nhóm em cũng đã kiểm tra paper Del Carpio và cộng sự về lương tối thiểu ở Việt Nam. Paper này dùng VHLSS và dữ liệu doanh nghiệp giai đoạn 2006-2010, dùng OLS và fixed effects, có xét employment, wages, self-employment và welfare. Điểm nhóm em có thể mở rộng là dùng dữ liệu mới hơn, tập trung trực tiếp vào tỷ lệ việc làm phi chính thức cấp tỉnh-năm, và cân nhắc DML để xử lý quan hệ phi tuyến sau khi chạy các baseline causal models.

Hiện tại nhóm em chưa kết luận nhân quả. Kết quả mới là diagnostic để chứng minh dữ liệu có cơ sở tiếp tục phân tích.
