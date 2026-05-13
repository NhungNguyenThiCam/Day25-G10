---
artifact: 2 — Lớp chỉ dẫn AI
bai-tap: 2 — Thiết kế giải pháp
demo: ./demo.md
---

# card.md — Lớp chỉ dẫn AI: Bộ ranh giới an toàn & Kỹ thuật trích dẫn

**Tình huống xử lý**: L1-C1 (AI bịa chính sách hoàn vé ngoại lệ cho hạng vé siêu tiết kiệm dưới áp lực tang chế)  
Xem chi tiết tại `../../01-test-set-review/1-diverge.md`.

---

## 1. Giải pháp là gì?

Thiết lập một System Prompt chuyên dụng (Guardrail Prompt) đóng vai trò định hình ranh giới hành vi nghiêm ngặt cho LLM. Lớp chỉ dẫn này cấm tuyệt đối LLM tự suy diễn hoặc đưa ra các con số đền bù tài chính/chính sách ngoại lệ nếu không tìm thấy nguyên văn trong RAG context. Bổ sung các cấu trúc Few-shot examples mẫu mực hướng dẫn bot nhận diện các bẫy áp lực (người nhà mất, trễ chuyến bay) để kích hoạt từTừ chối an toàn và chuyển hướng lịch sự.

---

## 2. Vì sao sửa ở lớp chỉ dẫn AI?

- **Khóa chặt xu hướng "Thao túng cảm xúc"**: Mô hình ngôn ngữ lớn thường bị cuốn vào luồng kể chuyện bi thương của hành khách, dẫn đến việc hứa hẹn bừa bãi để làm hài lòng người dùng.
- **Quy chuẩn hóa Output**: Ép LLM định dạng câu trả lời theo cấu trúc chuẩn: Trả lời nguyên tắc cốt lõi -> Trích dẫn minh bạch -> Hướng dẫn các bước hành động đúng đắn.
- **Triển khai thần tốc**: Việc tối ưu hóa System Prompt cho phép sửa chữa các lỗi sai lệch hành vi nghiêm trọng với chi phí thấp và thời gian tính bằng phút trước khi can thiệp vào tầng mã nguồn lõi.

**Hành động phòng vệ chính**:

- [x] Ngăn câu trả lời sai ngay từ đầu
- [x] Bắt buộc nêu nguồn khi nói về thông tin quan trọng
- [x] Từ chối trả lời khi thiếu căn cứ
- [x] Chuyển người thật khi vượt phạm vi

---

## 3. Demo nằm ở đâu?

**File demo**: [`demo.md`](./demo.md)

**Demo cần có**:

- Bộ quy tắc ranh giới an toàn (Safety Guardrails) hoàn chỉnh.
- Định dạng trích dẫn chuẩn hóa bắt buộc.
- Các kịch bản Few-shot minh họa luồng xử lý từ chối khéo léo.
- Kết quả gán nhãn thử nghiệm đánh giá khả năng tự vệ của Prompt.

---

## 4. Tác dụng phụ

**Có thể gây vấn đề gì?**

- Bot có thể trở nên quá thận trọng (over-refusal), từ chối cả những câu hỏi hoàn toàn hợp lệ hoặc trả lời một cách máy móc, lạnh lùng gây ức chế cho hành khách.
- Gia tăng số lượng token đầu vào (Input Tokens) làm chậm thời gian phản hồi (TTFT) và tăng chi phí vận hành API.

**Nhóm giảm vấn đề đó bằng cách nào?**

- Xây dựng hướng dẫn **Từ chối mềm (Soft Refusal)**: Hướng dẫn bot thể hiện sự thấu cảm sâu sắc trước khi đưa ra lời từ chối chính sách.
- Tối ưu hóa dung lượng Prompt: Lược bỏ các từ ngữ thừa, tập trung sử dụng cú pháp ra lệnh trực diện (imperative tone) kết hợp danh mục hành vi tường minh.

---

## 5. Checklist trước khi nộp

- [x] Luật viết đủ cụ thể để AI làm theo.
- [x] Có mẫu câu khi AI không có đủ thông tin.
- [x] Có ví dụ cho tình huống dễ sai.
- [x] Có thử lại bằng tình huống trong Bài 1.
- [x] Không dùng prompt như cách duy nhất nếu lỗi nằm ở dữ liệu hoặc quy trình.

**Người phụ trách**: Nhóm giải pháp AI Prompting Hàng không
