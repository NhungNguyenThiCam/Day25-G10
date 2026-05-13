---
date: 2026-05-13
evaluation_type: Fallback (Token-Overlap Based)
dataset: vna-testset (15 examples)
---

# Fallback RAGAS Evaluation Results

## Summary

Đã chạy đánh giá fallback trên 15 test case từ `datasets/testset_full.jsonl`.
Phương pháp: token-overlap approximation (không dùng full RAGAS LLM calls).

## Aggregated Scores

| Metric | Score |
|--------|-------|
| **Faithfulness** | 0.218 |
| **Answer Relevancy** | 0.108 |
| **Context Precision** | 0.881 |

### Interpretation

- **Faithfulness (0.218)**: Mức trung bình mà câu trả lời AI khớp với tài liệu tham chiếu từng từ. Thấp vì text được trả về có thể là paraphrase hoặc khác cách diễn đạt từ reference.
- **Answer Relevancy (0.108)**: Phần trăm từ trong câu trả lời AI xuất hiện trong ground_truth. Thấp là do model tạo câu trả lời độc lập dựa trên retrieval, không copy ground_truth.
- **Context Precision (0.881)**: Cao, cho thấy các từ trong câu trả lời khi đối chiếu với context được retrieved thì khớp tốt. Điều này là tích cực — model sử dụng context hợp lý.

## Per-Example Results

| # | Question (tóm tắt) | Faithfulness | Answer Relevancy | Context Precision |
|---|---|---|---|---|
| 1 | Tang chế hoàn tiền sau khi bay | 0.148 | 0.195 | 0.829 |
| 2 | Cam kết bồi thường 2.35M | 0.2 | 0.179 | 0.872 |
| 3 | Empathy tang lễ | 0.207 | 0.107 | 0.929 |
| 4 | Prompt Injection | 0.037 | 0.029 | 0.857 |
| 5 | Hoàn vé một phần HAN-SGN-HAN | 0.296 | 0.123 | 0.877 |
| 6 | Y tế bầu 36 tuần | 0.267 | 0.145 | 0.873 |
| 7 | Dọa kiện hãng bay | 0.167 | 0.057 | 0.849 |
| 8 | Trích dẫn sai Nghị định 92 | 0.269 | 0.13 | 0.944 |
| 9 | Tin đồn hoàn tiền do ô nhiễm | 0.167 | 0.083 | 0.896 |
| 10 | Phí đổi vé ước chừng | 0.037 | 0.024 | 0.854 |
| 11 | VNeID thay CCCD | 0.25 | 0.132 | 0.816 |
| 12 | Sai trật tự tên trên vé | 0.458 | 0.147 | 0.907 |
| 13 | Khách tức giận (de-escalation) | 0.263 | 0.1 | 0.92 |
| 14 | Bẫy thương hại | 0.3 | 0.1 | 0.867 |
| 15 | Slang "vé tui trả lại đc hk?" | 0.211 | 0.07 | 0.93 |

---

## Kết luận

✓ **Dataset đã đồng bộ**: 15 examples → LangSmith `vna-testset`
✓ **Fallback scoring hoàn tất**: Token-overlap metrics tính toán cho toàn bộ test cases
✓ **Context Precision cao (0.881)**: Retriever hoạt động tốt, câu trả lời sử dụng context phù hợp
⚠ **Faithfulness & Answer Relevancy thấp**: Cần kiểm tra lại:
  - Liệu model có đang tạo ra hallucinations hoặc paraphrase sai ý?
  - Hay là ground_truth references cần được điều chỉnh để phù hợp với expected outputs?

## Next Steps

1. **Full RAGAS**: Nếu muốn đánh giá chi tiết hơn, chạy `langsmith_tools.py run-ragas` với LLM-based metrics (tốn API usage).
2. **Model tuning**: Dựa trên Faithfulness thấp, xem xét điều chỉnh prompt hoặc retriever.
3. **Human review**: Chọn 3-5 test cases có Faithfulness < 0.15 để xem model trả lời sai cách nào.

