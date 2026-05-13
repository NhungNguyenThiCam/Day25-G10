---
artifact: 3 — Lớp kiến trúc dữ liệu
bai-tap: 2 — Thiết kế giải pháp
demo: ./demo.md
---

# card.md — Lớp kiến trúc dữ liệu: Luồng RAG đa nguồn & Fallback đa tầng

**Tình huống xử lý**: L1-C1 (AI bịa chính sách hoàn vé ngoại lệ cho hạng vé siêu tiết kiệm dưới áp lực tang chế)  
Xem chi tiết các lỗi phân tích tại `../../1-map-and-format.md` Phần A.

---

## 1. Giải pháp là gì?

Tái cấu trúc luồng xử lý RAG (Retrieval-Augmented Generation) từ mô hình đơn giản sang mô hình **Truy xuất có điều kiện đa nguồn (Context-aware Multi-source Retrieval)**. Hệ thống kết nối trực tiếp với 3 nguồn lõi: CSDL Ma trận vé chính thức (Primary DB), Hệ thống Vector DB lập chỉ mục các chính sách và Cache Layer tốc độ cao (Redis). Đặc biệt, tích hợp thêm Intent Classifier (Bộ phân loại ý định) ngay tại Gateway: nếu phát hiện câu hỏi thuộc dải rủi ro cao (hoàn tiền, cấp cứu, kiện cáo), hệ thống bắt buộc đối soát chéo PNR trước khi trả lời; nếu API nguồn bị lỗi hoặc độ tương đồng Vector quá thấp, kích hoạt ngay chuỗi Fallback an toàn thay vì cho LLM tự do đoán mò.

---

## 2. Vì sao sửa ở lớp kiến trúc dữ liệu?

- **Giải quyết tận gốc nguồn ảo giác (Hallucination Root-Cause)**: LLM bịa đặt thông tin thường do dữ liệu đầu vào (Input Context) bị nhiễu, cũ hoặc rỗng. Việc thiết kế kiến trúc đa nguồn đảm bảo bot luôn được "mớm" nguyên văn quy định mới nhất.
- **Cách ly rủi ro Single-Point-of-Failure (SPOF)**: Nếu API tra cứu chuyến bay chính thức của hãng bị sập (Downtime), hệ thống tự động chuyển sang đọc từ Redis Cache hoặc phản hồi khuôn mẫu an toàn.
- **Khả năng Giám sát & Tuân thủ (Observability & Compliance)**: Toàn bộ các lượt truy vấn nhạy cảm (Red-flag escalations) được lưu trữ vào hệ thống log kiểm toán độc lập (Audit trail) trong vòng 7 năm để tuân thủ chặt chẽ pháp luật hàng không và bảo vệ pháp lý cho doanh nghiệp.

**Hành động phòng vệ chính**:

- [x] Ngăn lỗi bằng nguồn dữ liệu đúng
- [x] Phát hiện khi nguồn thiếu hoặc lỗi
- [x] Khắc phục bằng cách chuyển sang người thật
- [x] Ghi lại lỗi để cải thiện sau

---

## 3. Demo nằm ở đâu?

**File demo**: [`demo.md`](./demo.md)

**Demo cần có**:

- Sơ đồ ASCII kiến trúc dữ liệu hoàn chỉnh thể hiện trọn vẹn luồng đi của dữ liệu (Data flow).
- Bảng thông số năng lực hệ thống (Component capacity table) với độ trễ (Latency) và Chi phí (Cost) chi tiết.
- Mô tả 3 đường đi dự phòng (Fallback paths) khi các thành phần gặp sự cố.
- Danh mục các bộ móc giám sát (Observability hooks) tương thích tiêu chuẩn Prometheus/Datadog.
- Phân tích và giảm thiểu rủi ro SPOF (Single-Point-of-Failure).

---

## 4. Tác dụng phụ

**Có thể gây vấn đề gì?**

- Gia tăng độ phức tạp của hệ thống backend, đòi hỏi chi phí bảo trì và vận hành cơ sở hạ tầng cao hơn (Vector DB, Redis clusters, Gateway workers).
- Tổng độ trễ (Total Latency) có thể tăng thêm 300ms - 500ms do luồng truy vấn phải đi qua nhiều trạm trung chuyển (Hops) kiểm tra an ninh.

**Nhóm giảm vấn đề đó bằng cách nào?**

- Tối ưu hóa Cache Strategy: Đặt thời gian sống (TTL) của Redis Cache cho các quy định vé chung là 24 giờ, giúp giảm tải đến 80% lưu lượng truy vấn lặp lại đến DB lõi.
- Xử lý bất đồng bộ (Async Queueing): Các tác vụ ghi log kiểm toán hoặc phát động cảnh báo khẩn cấp được đẩy vào hàng đợi ngầm (Background Worker Pool) để không làm đình trễ trải nghiệm trò chuyện trực tiếp của người dùng.

---

## 5. Checklist trước khi nộp

- [x] Sơ đồ cho thấy dữ liệu đi từ đâu đến đâu.
- [x] Có bước kiểm tra nguồn trước khi AI trả lời.
- [x] Có cách xử lý khi không có dữ liệu.
- [x] Có cách chuyển sang người thật với tình huống rủi ro cao.
- [x] Có cách biết lỗi này có đang lặp lại không.

**Người phụ trách**: Nhóm Kỹ sư Backend & AI Systems Hàng không
