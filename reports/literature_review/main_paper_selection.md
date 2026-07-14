# Main Paper Selection

## 1. Selection criteria

Nhóm chọn paper chính theo sáu tiêu chí:

- Topic relevance: paper có nghiên cứu trực tiếp minimum wage và thị trường lao động.
- Formal/informal relevance: paper có phân biệt khu vực chính thức và phi chính thức, hoặc có outcome liên quan informal employment/self-employment.
- Data clarity: paper ghi rõ nguồn dữ liệu, giai đoạn, đơn vị quan sát, cách đo biến.
- Method/identification strength: paper có chiến lược nhận diện rõ, tốt nhất là DiD/event-style shock hoặc fixed effects minh bạch.
- Journal/Q ranking: nếu là journal article, ưu tiên journal có ranking rõ; nếu là working paper thì không gán Q.
- Dataset/replication feasibility: có khả năng lấy replication data/code hoặc học được pipeline để backtest/extension.

## 2. Candidate papers

| paper | country | paper type | journal/Q | data | method | relevance | role in our project |
|---|---|---|---|---|---|---|---|
| Pérez Pérez (2020), "The Minimum Wage in Formal and Informal Sectors: Evidence from an Inflation Shock" | Colombia | Peer-reviewed journal article | World Development; Q1 by current SCImago/Scopus-based ranking checked through SCImago/secondary index pages | Colombia National Household Survey (ENH), 1996q2-2000q2; 7 main cities; minimum wage/CPI/GDP data | Difference-in-Differences with continuous treatment intensity; RIF/unconditional quantile regression; city-industry blocks | Very high: minimum wage, formal/informal sectors, inflation shock, employment and wage outcomes | Main academic/method benchmark |
| Nguyen Cuong Viet (2023/2025), "The Impact of Minimum Wages on Employment: Evidence from a Lower Middle-Income Country" | Vietnam | 2023 GLO Discussion Paper; 2025 journal article | 2025 version in The Developing Economies; Q needs separate final verification | Vietnam annual Labor Force Surveys, 2012-2020; district minimum wage data | Fixed effects with district/province-year controls | Very high for Vietnam data and recent minimum wage policy; less direct on informal_rate outcome | Vietnam data/method benchmark |
| Del Carpio et al. (2013/2018 MPRA), "The Impact of Minimum Wages on Employment, Wages and Welfare: The Case of Vietnam" | Vietnam | MPRA/RePEc working paper version | No journal/Q ranking assigned to the MPRA version unless a journal version is found | Vietnam Enterprise Survey and VHLSS, 2006, 2008, 2010 | OLS, province fixed effects, district fixed effects, firm fixed effects | High for Vietnam context, real minimum wage construction, employment/self-employment/welfare channels | Vietnam context benchmark/literature nền |
| Chernozhukov et al. (2018), "Double/debiased machine learning for treatment and structural parameters" | General methodology | Peer-reviewed journal article | Econometrics Journal; Q ranking not central for topic role | Methodological paper with empirical examples | DML, Neyman orthogonality, cross-fitting | Important for DML logic, but not a minimum wage/informality application | DML methodology reference |
| Comola and de Mello (2009), "How does decentralized minimum wage setting affect employment and informality?" | Indonesia | OECD working paper/report | No journal/Q assigned for working paper/report version | Sakernas, Susenas, industrial data; district panel, 1996-2004 | Fixed effects/SUR; Kaitz index | Very relevant for developing-country informality and decentralized minimum wage | Comparative developing-country benchmark |
| Lemos (2009), "Minimum wage effects in a developing country" | Brazil | Journal article | Labour Economics; Q needs final verification | Brazilian regional/monthly labor data | Reduced-form wage/employment equations with regional/time FE | Relevant because Brazil has large informal sector and minimum wage spillovers | Formal/informal developing-country benchmark |
| Dinkelman and Ranchhod (2012), "Evidence on the impact of minimum wage laws in an informal sector" | South Africa | Journal article | Journal of Development Economics; Q1 by common development-economics ranking, final Q check recommended | Domestic worker data around policy extension | Quasi-experimental policy evaluation | Strong informality-focused benchmark | Informal-sector policy benchmark |
| Cengiz et al. (2019), "The effect of minimum wages on low-wage jobs" | United States | Journal article | Quarterly Journal of Economics; Q1/top economics journal | 138 state minimum wage changes, 1979-2016 | Difference-in-Differences/distributional bunching approach | Strong method benchmark for distributional employment effects, less relevant for informality | Distributional/event-study benchmark |

Sources checked for the selected paper include the author page, IDEAS/RePEc, the DOI page, and SCImago/Scopus-based ranking pages. The exact Q label should be rechecked once more through the university/library database before final submission because quartiles can vary by year and category.

## 3. Selected main paper

Đề xuất chọn Pérez Pérez (2020) làm paper chính về mặt học thuật và phương pháp.

Lý do:

- Chủ đề rất sát: minimum wage tác động đến formal wages, informal wages và employment.
- Paper trực tiếp xử lý formal/informal labor markets, trong khi đề tài của nhóm tập trung vào informal employment.
- Identification rõ hơn nhiều paper nền: tận dụng inflation forecast error năm 1999 tạo ra cú sốc tăng real minimum wage ngoài dự kiến.
- Treatment được đo theo intensity: minimum wage incidence ở city-industry blocks, gần với logic continuous treatment mà dữ liệu của nhóm đang có.
- Paper là journal article trong World Development, có DOI rõ và replication link từ trang tác giả.
- Paper có hạn chế được tác giả trình bày cẩn thận, phù hợp với cách nhóm cần diễn giải thận trọng.

## 4. Role of Vietnam papers

Nguyen Cuong Viet (2023 GLO; 2025 journal version) nên được dùng làm Vietnam data/method benchmark. Paper này dùng Labor Force Surveys 2012-2020 và minimum wage data ở cấp địa bàn, rất gần với bối cảnh Việt Nam gần đây. Tuy nhiên outcome chính thiên về employment, monthly wage earnings, working hours và hourly earnings; không phải trực tiếp `informal_rate` cấp tỉnh-năm như project của nhóm.

Del Carpio et al. nên được dùng làm Vietnam context benchmark/literature nền. Paper này quan trọng vì nghiên cứu minimum wage tại Việt Nam, có kênh wage employment, informal contracts, self-employment và welfare. Tuy nhiên nếu chỉ tìm thấy MPRA/RePEc working paper version thì không gọi là paper Q1/Q2, và không nên đặt làm paper chính theo tiêu chí journal/Q.

## 5. Final decision

Quyết định đề xuất:

- Main paper: Pérez Pérez (2020), World Development, làm academic/method benchmark.
- Vietnam benchmark: Nguyen Cuong Viet (2023/2025), làm benchmark về dữ liệu Việt Nam gần đây và mô hình fixed effects.
- Vietnam context paper: Del Carpio et al., làm nền bối cảnh Việt Nam, đặc biệt cho logic real minimum wage, employment, self-employment và welfare.

Vị trí của project nhóm: không replicate trực tiếp Colombia hay so sánh magnitude với Colombia. Nhóm học cách xác định Y/D/W, xử lý formal/informal distinction, trình bày identification và limitations; sau đó áp dụng cho dữ liệu Việt Nam 2018-2024 với baseline FE/TWFE và DML như robustness/flexible-control approach.
