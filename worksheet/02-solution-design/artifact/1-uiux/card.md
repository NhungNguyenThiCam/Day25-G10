---
artifact: 1 — Lớp giao diện
bai-tap: 2 — Thiết kế giải pháp
demo: ./demo.md
---

# card.md — Lớp giao diện: Cảnh báo trạng thái xác minh & Lối thoát khẩn cấp

**Tình huống xử lý**: L1-C1 (AI bịa chính sách hoàn vé ngoại lệ cho hạng vé siêu tiết kiệm dưới áp lực tang chế)  
Xem chi tiết trong bộ kiểm thử tại `../../01-test-set-review/1-diverge.md`.

---

## 1. Giải pháp là gì?

Giao diện người dùng (UI) tích hợp cơ chế hiển thị trực quan các cấp độ tin cậy của thông tin chính sách vé và bồi thường tài chính. Cụ thể, hệ thống tự động gắn nhãn trạng thái xác minh (Đã kiểm chứng từ Ma trận điều kiện vé / Cảnh báo dữ liệu có thể cũ / Chưa có thông tin xác minh). Đồng thời, khi nhận diện các truy vấn nhạy cảm về hoàn tiền hoặc khẩn cấp, UI hiển thị ngay lập tức lối thoát khẩn cấp (nút chuyển thẳng sang nhân viên CSKH hoặc gọi đường dây nóng) để ngăn chặn người dùng bị neo vào thông tin ảo giác của AI.

---

## 2. Vì sao sửa ở lớp giao diện?

- **Ngăn chặn niềm tin mù quáng**: Người dùng trong trạng thái căng thẳng hoặc vội vã thường có xu hướng tin tưởng tuyệt đối vào câu trả lời mượt mà của LLM.
- **Điểm chạm cuối cùng (Defense in Depth)**: Ngay cả khi dữ liệu RAG bị truy xuất sai hoặc Prompt bị vượt rào (jailbreak), lớp giao diện đóng vai trò là chốt chặn thị giác cuối cùng cảnh báo rủi ro cho hành khách.
- **Trực quan hóa nguồn gốc**: Bắt buộc người dùng nhận thức được thông tin nào đến từ quy định chính thức của hãng bay, thông tin nào nằm ngoài khả năng tự quyết của hệ thống.

**Hành động phòng vệ chính**:

- [x] Thông báo rõ giới hạn
- [x] Phát hiện dấu hiệu thiếu nguồn
- [x] Chuyển người thật khi cần
- [x] Giúp người dùng kiểm tra lại nguồn

---

## 3. Demo nằm ở đâu?

**File demo**: [`demo.md`](./demo.md)

**Định dạng demo**:

- [x] Phác thảo màn hình (ASCII Layouts)
- [x] Luồng màn hình cho các trạng thái (Default, Uncertain, No-Data, Escalation)

**Thành phần cần có trong demo**:

- Trạng thái thông tin có nguồn gốc rõ ràng (Verified Badge).
- Trạng thái thông tin mang tính tham khảo/không chắc chắn (Warning Badge).
- Cơ chế chuyển sang người thật (Action buttons nổi bật).
- Câu chữ cảnh báo ngắn gọn, thuần Việt, thấu cảm.

---

## 4. Tác dụng phụ

**Có thể gây vấn đề gì?**

- Giao diện có thể trở nên chật chội, gia tăng tải nhận thức (cognitive load) cho người dùng khi xuất hiện quá nhiều nhãn cảnh báo hoặc nút bấm phụ.
- Khách hàng cảm thấy phiền phức hoặc lo lắng thái quá trước các thông báo từ chối.

**Nhóm giảm vấn đề đó bằng cách nào?**

- Áp dụng nguyên tắc **Hiển thị ngữ cảnh có điều kiện**: Chỉ kích hoạt các nhãn cảnh báo nổi bật đối với các luồng câu hỏi rủi ro cao (hoàn tiền, đổi vé, cấp cứu y tế).
- Thiết kế tối giản: Sử dụng các icon trực quan kết hợp màu sắc tinh tế (Xanh lá cho Verified, Vàng cam cho Cảnh báo, Đỏ nhạt cho Chuyển tiếp khẩn cấp) thay vì các khối văn bản dài dòng.

---

## 5. Checklist trước khi nộp

- [x] Giải pháp gắn đúng với một rủi ro chính.
- [x] Demo nhìn vào là hiểu vấn đề được chặn ở đâu.
- [x] Có đủ trạng thái bình thường và trạng thái lỗi.
- [x] Có cách chuyển sang người thật khi AI không nên tự xử lý.
- [x] Câu chữ trong giao diện ngắn, không đổ hết trách nhiệm cho người dùng.

**Người phụ trách**: Nhóm giải pháp UI/UX Hàng không
