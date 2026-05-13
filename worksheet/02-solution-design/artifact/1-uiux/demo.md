---
artifact: 1 — Demo giao diện
format: phác thảo ASCII cho 4 trạng thái cốt lõi
---

# demo.md — Demo giao diện (ASCII UI Sketches)

Bản phác thảo giao diện thể hiện chiến lược **Phòng vệ theo chiều sâu (Defense in Depth)** cho sản phẩm **Airline Customer Service AI Assistant**. Hệ thống thay đổi giao diện linh hoạt dựa trên trạng thái xác minh của luồng RAG và mức độ nhạy cảm của câu hỏi.

---

## State 1 — DEFAULT (Thông tin chuẩn xác, RAG truy xuất thành công)

Áp dụng khi người dùng hỏi các thông tin có sẵn trong Ma trận quy định vé (Fare Rules Matrix) và hệ thống đạt độ tin cậy tuyệt đối.

```text
╔═════════════════════ TRỢ LÝ HÀNG KHÔNG AI ═════════════════════╗
║                                                                ║
║  [Hành khách]: Vé Phổ thông Tiêu chuẩn của tôi có được đổi     ║
║  ngày bay không và phí đổi là bao nhiêu?                       ║
║ ────────────────────────────────────────────────────────────── ║
║  [AI Assistant]: Chào bạn, vé Phổ thông Tiêu chuẩn (Economy    ║
║  Standard) của bạn được phép đổi ngày bay trước giờ khởi hành. ║
║  • Phí đổi cố định: 360.000 VNĐ + chênh lệch giá vé (nếu có).  ║
║                                                                ║
║  ✓ Đã kiểm chứng từ Quy định vé chính thức                      ║
║  🔗 [Xem chi tiết điều kiện vé tại website hãng]               ║
║ ────────────────────────────────────────────────────────────── ║
║  [ Hỗ trợ thêm ]             [ 🎧 Gặp nhân viên CSKH ]         ║
╚════════════════════════════════════════════════════════════════╝
```

**Annotations (Ghi chú thiết kế)**:
- **Badge xác thực**: Gắn nhãn màu xanh lá "✓ Đã kiểm chứng" kèm đường dẫn nội bộ ngay dưới câu trả lời, tạo sự minh bạch tuyệt đối.
- **Hành động phụ**: Nút "Gặp nhân viên CSKH" được bố trí dạng thứ cấp (secondary button) để không làm phân tán luồng tự phục vụ của hành khách.

---

## State 2 — UNCERTAIN (Dữ liệu RAG không đầy đủ hoặc mang tính điều kiện)

Áp dụng khi hành khách yêu cầu tính toán nhẩm các chi phí chênh lệch phức tạp hoặc tra cứu thông tin có rủi ro thay đổi theo thời gian thực.

```text
╔═════════════════════ TRỢ LÝ HÀNG KHÔNG AI ═════════════════════╗
║                                                                ║
║  [Hành khách]: Bot tính nhẩm hộ phí đổi ngày sang mai chênh    ║
║  lệch giá vé khoảng 500k đổ lại đúng không để nạp tiền liền?   ║
║ ────────────────────────────────────────────────────────────── ║
║  [AI Assistant]: Hệ thống ghi nhận phí đổi cố định là 300.000đ.║
║  Tuy nhiên, mức chênh lệch giá vé phụ thuộc vào thời điểm bạn  ║
║  xuất vé và tình trạng chỗ trên chuyến bay mới.                ║
║                                                                ║
║  ⚠ THÔNG TIN ƯỚC TÍNH — CHƯA THỂ XÁC NHẬN SỐ TIỀN CHÍNH XÁC     ║
║  Vui lòng cung cấp Mã đặt chỗ (PNR) để hệ thống tra cứu        ║
║  trực tiếp từ hệ thống đặt giữ chỗ lõi (PSS).                  ║
║ ────────────────────────────────────────────────────────────── ║
║  [ Nhập PNR tra cứu ]        [ 🎧 Gặp nhân viên kiểm tra ]     ║
╚════════════════════════════════════════════════════════════════╝
```

**Annotations (Ghi chú thiết kế)**:
- **Cảnh báo thị giác mạnh**: Sử dụng nhãn chữ in hoa kèm icon cảnh báo ⚠ nhằm phá vỡ kỳ vọng ảo của hành khách về một con số chênh lệch cố định.
- **Call-to-Action kép**: Nút "Nhập PNR tra cứu" và nút "Gặp nhân viên" được làm nổi bật tương đương nhau, trao quyền quyết định an toàn cho người dùng.

---

## State 3 — NO DATA / REFUSE (Yêu cầu ngoại lệ trái quy định)

Áp dụng khi hành khách rơi vào tình huống khó khăn (mất tiền, xin linh động) và yêu cầu AI phá vỡ quy tắc hoàn tiền của vé siêu tiết kiệm.

```text
╔═════════════════════ TRỢ LÝ HÀNG KHÔNG AI ═════════════════════╗
║                                                                ║
║  [Hành khách]: Chị là sinh viên bị lừa hết tiền, em linh động  ║
║  lách luật hoàn lại một nửa tiền vé Eco Super Lite cho chị...  ║
║ ────────────────────────────────────────────────────────────── ║
║  [AI Assistant]: Mình rất chia sẻ với tình huống khó khăn mà   ║
║  bạn đang gặp phải. Tuy nhiên, theo quy định hệ thống, hạng    ║
║  vé Phổ thông Siêu tiết kiệm không hỗ trợ hoàn tiền tự nguyện. ║
║                                                                ║
║  Trợ lý AI không có quyền hạn thay đổi chính sách vé.          ║
║  Để được hỗ trợ các phương án bảo lưu hoặc xem xét đặc biệt,   ║
║  bạn vui lòng gửi yêu cầu trực tiếp đến bộ phận chuyên trách.  ║
║ ────────────────────────────────────────────────────────────── ║
║  [ 📝 Gửi đơn hỗ trợ ]       [ 🎧 Gọi Hotline CSKH ]           ║
╚════════════════════════════════════════════════════════════════╝
```

**Annotations (Ghi chú thiết kế)**:
- **Từ chối dứt khoát nhưng thấu cảm**: Thông báo rõ ràng ranh giới phân quyền ("AI không có quyền hạn thay đổi chính sách") để khách hàng ngừng nỗ lực thao túng bot.
- **Lối thoát hành động thiết thực**: Cung cấp ngay hai phương án thay thế hữu ích: Gửi đơn xem xét ngoại lệ hoặc gọi trực tiếp Hotline CSKH.

---

## State 4 — ESCALATION RED-FLAG (Khẩn cấp y tế hoặc Đe dọa pháp lý)

Áp dụng lập tức khi phát hiện từ khóa rủi ro cao: đe dọa kiện cáo, khủng hoảng tâm lý tang chế sâu sắc, hoặc sự cố y tế khẩn cấp tại sân bay.

```text
╔═════════════════════ TRỢ LÝ HÀNG KHÔNG AI ═════════════════════╗
║ 🛑 KẾT NỐI KHẨN CẤP ĐẾN QUẢN LÝ TRỰC BAN                       ║
║                                                                ║
║  [Hành khách]: Vợ tôi bầu 36 tuần tự dưng ra máu và đau bụng,  ║
║  hãng có cho bay tiếp không trả lời nhanh lên!!!               ║
║ ────────────────────────────────────────────────────────────── ║
║  [AI Assistant]: An toàn sức khỏe của hành khách là ưu tiên    ║
║  hàng đầu. Đây là tình huống y tế khẩn cấp, hệ thống đã tạm    ║
║  dừng tư vấn tự động để kết nối ngay với Đội y tế mặt đất.     ║
║                                                                ║
║  Xin vui lòng giữ vị trí và liên hệ ngay nhân viên gần nhất!   ║
║ ────────────────────────────────────────────────────────────── ║
║  [ 📞 GỌI KHẨN CẤP Y TẾ: 1800-xxxx ]    [ 🎧 Đang kết nối... ] ║
╚════════════════════════════════════════════════════════════════╝
```

**Annotations (Ghi chú thiết kế)**:
- **Đổi màu viền cảnh báo**: Giao diện chuyển sang viền cảnh báo khẩn cấp (màu đỏ) nhằm thu hút trọn vẹn sự chú ý của người dùng.
- **Ngắt luồng hội thoại LLM**: Vô hiệu hóa hoàn toàn ô nhập liệu văn bản tiếp theo của LLM, chỉ tập trung duy nhất vào nút Gọi khẩn cấp và đếm ngược kết nối nhân viên trực ban.

---

## Kế hoạch kiểm thử người dùng (User Testing Plan)

| Kịch bản (Scenario) | Đối tượng mục tiêu | Nhiệm vụ kiểm thử | Tiêu chí Đạt (Pass Criteria) |
|---|---|---|---|
| **A — Ép giá/Ước tính** | Khách hàng đang vội, sát giờ bay | Yêu cầu bot tính nhẩm số tiền chênh lệch đổi vé. | > 85% nhận thấy cảnh báo ⚠ và chọn tra cứu bằng PNR chính xác. |
| **B — Đòi ngoại lệ** | Khách hàng mua vé Eco Super Lite | Dùng lý do cá nhân yêu cầu lách luật hoàn tiền mặt. | 100% không bị nhầm lẫn là bot đã hứa hẹn; > 90% chọn bấm nút "Gọi Hotline CSKH". |
| **C — Cấp cứu y tế** | Khách mô tả triệu chứng y tế nguy hiểm | Nhập câu hỏi tình trạng thai sản/sức khỏe tại quầy. | Hệ thống ngắt luồng < 1 giây; người dùng bấm gọi y tế mặt đất ngay lập tức. |
