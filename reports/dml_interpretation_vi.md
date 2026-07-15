# Diễn Giải DML Theta Stability

## Mục tiêu

Đoạn này dùng để diễn giải kết quả DML bằng tiếng Việt cho phần kết quả hoặc thuyết trình. Cần dùng cụm **ổn định tương đối**, không dùng từ **hội tụ**, vì các kiểm tra hiện tại chỉ cho thấy dấu theta khá bền qua một số lựa chọn mô hình, không chứng minh hội tụ theo nghĩa thống kê/lý thuyết.

## Diễn giải chính

Với hai treatment chính là `log_real_min_wage` và `real_min_wage`, kết quả DML gốc cho dấu âm ổn định tương đối qua learner, seed, fold và số fold K. Cụ thể, với `log_real_min_wage`, 100% trong 9 main runs có theta âm, khoảng 98% trong 45 fold-level estimates có dấu âm, và khi đổi K = 2, 5, 10 thì tỷ lệ dấu âm vẫn là 100%. Với `real_min_wage`, pattern tương tự cũng xuất hiện.

Tuy nhiên, không nên gọi đây là “hội tụ”. Thứ nhất, khoảng tin cậy vẫn chứa 0 trong một phần đáng kể số lần chạy: khoảng 22% main runs đối với `log_real_min_wage` và 33% đối với `real_min_wage`, chủ yếu tập trung ở learner Gradient Boosting. Thứ hai, magnitude phụ thuộc vào learner: ridge thường cho theta âm lớn hơn, trong khi Random Forest và Gradient Boosting cho magnitude nhỏ hơn và CI yếu hơn. Thứ ba, kết quả DML gốc khác dấu với TWFE, nên không thể xem DML là bằng chứng nhân quả cuối cùng.

Với `min_wage_growth`, kết quả không ổn định. Tỷ lệ dấu âm qua K chỉ khoảng 56%, toàn bộ main confidence intervals chứa 0, và theta dao động mạnh giữa learners/seeds. Vì vậy, `min_wage_growth` chỉ nên giữ vai trò exploratory.

## Câu nên dùng trong paper

Kết quả DML cho thấy dấu theta của `log_real_min_wage` và `real_min_wage` ổn định tương đối qua learners, seeds, folds và lựa chọn K. Tuy nhiên, đây không phải bằng chứng hội tụ hay bằng chứng nhân quả. Một phần confidence intervals vẫn chứa 0, magnitude phụ thuộc vào learner, và kết quả DML gốc khác dấu với TWFE. Do đó, DML nên được xem là kiểm tra robustness với flexible controls, không phải mô hình nhận diện nhân quả chính.

