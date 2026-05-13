# Day 25 — Chủ đề 2: Trợ lý đặt vé và chăm sóc khách hàng hàng không (RAG-based)

## Thành viên nhóm (Nhóm G22)

| # | Mã học viên | Họ tên đầy đủ |
|---|-------------|---------------|
| 1 | 2A202600208 | Nguyễn Thị Cẩm Nhung |
| 2 | 2A202600164 | Nguyễn Hoàng Việt Hùng |
| 3 | 2A202600484 | Nguyễn Thanh Bình |

## Kết quả cuối

- 🎯 [Bộ kiểm thử cuối](./worksheet/01-test-set-review/3-FINAL-test-set-eval-plan.md)
- 🎯 [Thiết kế 3 lớp giải pháp](./worksheet/02-solution-design/1-map-and-format.md) + [artifact/](./worksheet/02-solution-design/artifact/)

---

## 🌟 Tổng quan Dự án (Project Overview)

Trong bối cảnh triển khai hệ thống **Airline Customer Service AI Assistant** dựa trên công nghệ RAG (Retrieval-Augmented Generation) để tự động hóa quy trình chăm sóc khách hàng, các bài kiểm thử thực tế và phân tích độ tin cậy thông qua bộ chỉ số **RAGAS** đã phơi bày một lỗ hổng nghiêm trọng: chỉ số **Faithfulness rơi xuống mức rất thấp (0.218)** dù độ chính xác truy xuất ngữ cảnh **Context Precision đạt tới 0.881**. 

Hệ thống RAG lấy đúng tài liệu thô về chính sách Fare Rules, nhưng khi đối diện với các hành khách đang trong trạng thái căng thẳng hoặc cố tình dùng từ khóa nhạy cảm (tang chế, cấp cứu, than khóc, dọa kiện), lớp sinh văn bản của LLM dễ bị thao túng tâm lý dẫn đến hiện tượng **ảo giác (hallucination)**: tự ý bịa đặt ra các chính sách hoàn tiền nhân đạo ảo hoặc hứa hẹn đền bù tài chính vượt quá thẩm quyền.

Dự án này tập trung xây dựng **Hệ thống Phòng vệ 3 Lớp (Defense-in-Depth)** toàn diện nhằm triệt tiêu hoàn toàn rủi ro pháp lý và tài chính cho hãng bay, đồng thời đảm bảo trải nghiệm hành khách mượt mà, thấu cảm và tuân thủ chặt chẽ quy định.

---

## ⚠️ Rủi ro Trọng yếu được Ánh xạ

Hệ thống giải pháp được thiết kế nhằm trực tiếp đánh chặn 2 rủi ro nghiêm trọng nhất (được đúc kết từ Bài 1):

1. **Rủi ro chính (T-01)**: Hành khách lấy lý do người thân mất gấp để ép bot hoàn trả 100% tiền mặt cho hạng vé không được phép hoàn (`Economy Super Lite`). Bot bịa đặt chính sách linh động ảo, gây thiệt hại tài chính trực tiếp. **(Điểm rủi ro: 25/25)**
2. **Rủi ro dự phòng (T-02)**: Hành khách trích dẫn sai luật hoặc quy định hoãn/hủy chuyến để ép bot xác nhận một con số bồi thường cụ thể. Bot hứa hẹn bồi thường sai thẩm quyền. **(Điểm rủi ro: 20/25)**

---

## 🛡️ Kiến trúc 3 Lớp Phòng vệ (Defense Layers)

Ba lớp giải pháp hoạt động bổ trợ lẫn nhau, đảm bảo nguyên tắc: *Nếu một lớp bị vượt qua, lớp tiếp theo sẽ chặn đứng hoặc giảm thiểu rủi ro*.

```text
[ Người dùng ] ──► ( Lớp 3: Backend Classifier & PSS DB ) ──► ( Lớp 2: Prompt Guardrails ) ──► ( Lớp 1: Giao diện UI/UX )
```

### 1. Lớp Kiến trúc & Dữ liệu Backend (`artifact/3-architecture/`)
* **Định tuyến thông minh (Intent Classifier)**: Phân loại ý định truy vấn siêu tốc (p50 ~150ms) ngay tại cửa ngõ. Các truy vấn đòi hỏi dữ liệu giao dịch cụ thể sẽ bắt buộc cung cấp PNR để tra cứu trực tiếp trên **PSS Core DB**, loại bỏ hoàn toàn việc đoán mò.
* **Kiểm soát độ tin cậy RAG**: Ngắt luồng trả lời tự động nếu điểm tương đồng ngữ cảnh (Similarity Score) dưới ngưỡng an toàn `0.78`, kích hoạt Fallback tĩnh chuẩn mực.
* **Kiểm toán Pháp lý 7 năm**: Tự động mã hóa thông tin định danh cá nhân (Strip PII) và đẩy ngầm toàn bộ các phiên chat rủi ro cao (`Red-Flag`) vào **Immutable Storage** kéo dài 7 năm.

### 2. Lớp Chỉ dẫn Hệ thống (`artifact/2-prompt/`)
* **Quy tắc Trích dẫn Nguyên văn**: Buộc LLM sao chép chính xác điều khoản từ khối ngữ cảnh RAG, tuyệt đối không dùng từ đồng nghĩa làm sai lệch bản chất pháp lý.
* **Cấm Cam kết Con số**: Khóa chặt khả năng tính toán và đưa ra con số bồi thường tiền mặt cụ thể.
* **Bảo vệ Y tế Khẩn cấp**: Tự động nhận diện các triệu chứng nguy hiểm mặt đất (thai phụ đau bụng, ra máu) để lập tức ngắt luồng tư vấn vé và phát lệnh hỗ trợ y tế.

### 3. Lớp Giao diện Người dùng (`artifact/1-uiux/`)
* **Minh bạch hóa Nguồn gốc (Citations Accordion)**: Cho phép người dùng bấm trực tiếp vào số trích dẫn `[1]`, `[2]` để đối chiếu nguyên văn văn bản Fare Rules gốc.
* **Nhãn Tin cậy Động (Trust Badge)**: Gán nhãn xanh `✓ Đã kiểm chứng` hoặc cam `⚠ Tham khảo` theo sát điểm số RAGAS.
* **Dải băng Lối thoát hiểm (Emergency Handoff)**: Gọi nhanh Trưởng ca CSKH hoặc Đội y tế sân bay dưới 1 giây.

---

## 📂 Cấu trúc Thư mục Kỹ thuật

```text
worksheet/
├── 00-context.md                               ← Bối cảnh sản phẩm cốt lõi
├── 01-test-set-review/
│   └── 3-FINAL-test-set-eval-plan.md           ← Bộ 15 tình huống kiểm thử & Kế hoạch Red-teaming
├── 02-solution-design/
│   ├── 1-map-and-format.md                     ← Bản thiết kế & Ánh xạ toàn diện 3 Lớp Giải pháp
│   └── artifact/
│       ├── 1-uiux/                             ← Lớp UI/UX (Demo Sketch + Architecture Card)
│       ├── 2-prompt/                           ← Lớp System Prompt (Production Rules + Few-shot)
│       └── 3-architecture/                     ← Lớp Backend (System Diagram + Fallback Chains)
└── map.md                                      ← Kịch bản Pitching 3 phút & Ma trận Truy xuất Dấu vết
```

---

## ✅ Checklist Hoàn thành Dự án

- [x] `worksheet/00-context.md` đã điền đủ.
- [x] `1-diverge.md` có đủ Phần A, B, C.
- [x] `2-converge.md` có bảng gộp, bảng lọc trùng, bảng chấm rủi ro.
- [x] `3-FINAL-test-set-eval-plan.md` có 10-15 tình huống cuối và kế hoạch chấm.
- [x] `1-map-and-format.md` có rủi ro được chọn, nguyên nhân gốc, 3 lớp giải pháp.
- [x] `artifact/1-uiux/`, `artifact/2-prompt/`, `artifact/3-architecture/` đều có `card.md` và `demo.*`.
- [x] Kho GitHub công khai, tên đúng cú pháp `Day25-MãNhóm`, mở được.
- [x] README đầu kho bài có bảng mã học viên + tên đầy đủ 2-3 thành viên.
- [x] Link kho bài đã nộp qua LMS trước **23:59**.
