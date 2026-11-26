# QA1 – L01 L02 L03 L04 L05 L06

Phạm vi: xem toàn bộ ảnh trang nguồn (L01 25, L02 22, L03 28, L04 25, L05 42+2, L06 25 trang) và mọi ảnh crop; tự giải mẫu 11 câu/bài (random.seed(số bài*7+1)) không nhìn đáp án; kiểm lộ đáp án toàn bộ câu single; đọc 2 thực hành + 2 bài tập/bài; quét chữ dính, NFC, ký tự lỗi.

## Kết quả chung
- Phủ nội dung: cả 6 bài đã phủ mọi slide có nội dung, kể cả các slide "Ví dụ thực hành"/"Hoạt động" (có trong practice/exercises). Không cần thêm theory.
- Đáp án: 66/66 câu mẫu khớp, 0 câu sai đáp án.
  - L01: q3 q6 q9 q13 q14 q15 q16 q24 q25 q33 q42
  - L02: q1 q2 q3 q4 q10 q11 q14 q16 q24 q34 q40
  - L03: q2 q6 q8 q9 q12 q15 q16 q18 q23 q29 q40
  - L04: q5 q6 q19 q23 q26 q27 q33 q36 q39 q41 q42
  - L05: q1 q2 q4 q6 q12 q16 q18 q19 q22 q33 q41
  - L06: q2 q3 q7 q10 q19 q24 q28 q30 q32 q33 q41
- Thực hành/bài tập (p1, p2, x1, x2 mỗi bài): đáp án mẫu đúng và đủ.
- `tf` ≤ 16% mỗi bài; "tất cả đều đúng/sai" không dùng.
- Ảnh: 39 ảnh có crop và 2 ảnh dùng nguyên trang (L05-img7, L06-img5) đều đã mở xem. Crop đúng sơ đồ, không cắt mất phần nào. Không sửa crop.
- Lộ đáp án, tính trên câu single. Cột 1 đếm câu có đáp án là option dài nhất duy nhất. Cột 2 đếm cả câu có đáp án dài bằng option dài nhất.

  | Bài | Dài nhất duy nhất: trước → sau | Dài nhất kể cả bằng: trước → sau |
  |---|---|---|
  | L01 | 5/32 → 1/32 | 11/32 → 4/32 (12%) |
  | L02 | 7/33 → 1/33 | 9/33 → 3/33 (9%) |
  | L03 | 5/33 → 1/33 | 8/33 → 4/33 (12%) |
  | L04 | 9/29 → 1/29 | 11/29 → 3/29 (10%) |
  | L05 | 6/36 → 0/36 | 8/36 → 2/36 (6%) |
  | L06 | 8/33 → 3/33 | 10/33 → 4/33 (12%) |

  Các câu còn lại có option là tên cố định (tên KA, tên khung tranh, mức MoSCoW, tên CSDL, tên cột, tên chứng chỉ). Viết dài thêm sẽ làm sai tên.
- Câu hỏi phủ định dạng "ý nào KHÔNG…" đều đã in đậm.

## Log sửa (id · lỗi · cách sửa)
- L01-q2 · đáp án dài nhất · kéo dài option sai b, d
- L01-q20 · đáp án dài nhất · kéo dài option sai b, c (mô tả đúng khung tranh)
- L01-q21 · đáp án dài nhất · kéo dài option sai b, d
- L01-q31 · đáp án dài nhất · đổi option b thành "Business Analysis Core Concepts", cập nhật why_wrong b
- L01-q5 · đáp án dài bằng option dài nhất · kéo dài option b
- L01-q12 · đáp án dài bằng option dài nhất · kéo dài option b
- L01-q44 · đáp án dài bằng option dài nhất · kéo dài option b
- L06-q40 · đáp án dài bằng option dài nhất · kéo dài option b (vẫn thiếu tên đơn vị và phiên bản)
- L02-q6 · đáp án dài nhất · kéo dài option c
- L02-q8 · đáp án dài nhất · kéo dài option a, d
- L02-q10 · đáp án dài nhất · kéo dài option c
- L02-q23 · đáp án dài nhất · kéo dài option c
- L02-q26 · đáp án dài nhất · kéo dài option b
- L02-q42 · đáp án dài nhất · đổi option a "Java" → "JavaScript", cập nhật why_wrong a
- L03-q12 · đáp án dài nhất · kéo dài option c
- L03-q15 · đáp án dài nhất · kéo dài option a
- L03-q31 · đáp án dài nhất · option b "XP" → "XP (Extreme Programming)"
- L03-q41 · đáp án dài nhất · kéo dài option b
- L04-q1 · đáp án dài nhất · kéo dài option d
- L04-q2 · đáp án dài nhất · option c đổi thành "Requirements Analysis and Design Definition", cập nhật why_wrong c
- L04-q13 · đáp án dài nhất · kéo dài option a
- L04-q16 · đáp án dài nhất · kéo dài option b, c
- L04-q17 · đáp án dài nhất · kéo dài option b
- L04-q32 · đáp án dài nhất · kéo dài option a
- L04-q33 · đáp án dài nhất · kéo dài option c
- L04-q43 · đáp án dài nhất · kéo dài option c
- L05-q3 · đáp án dài nhất · kéo dài option b
- L05-q23 · đáp án dài nhất · kéo dài option d
- L05-q28 · đáp án dài nhất · kéo dài option a
- L05-q36 · đáp án dài nhất · kéo dài option a
- L05-q41 · đáp án dài nhất · kéo dài option c
- L05-q45 · đáp án dài nhất · kéo dài option a
- L06-q6 · đáp án dài nhất · option a "Phê duyệt CR" → "Nghiệm thu và theo dõi", cập nhật why_wrong a
- L06-q15 · đáp án dài nhất · kéo dài option b
- L06-q22 · đáp án dài nhất · kéo dài option d (vẫn là dấu hiệu Must Have)
- L06-q33 · đáp án dài nhất · kéo dài option c
- L06-q36 · đáp án dài nhất · kéo dài option d
- L06-t4, L06-e1, L06-p1, L06-f9 · chữ dính "CR-nămthángngày-" · đổi thành "CR-YYYYMMDD-"

## Ghi chú, không sửa
- L06-img5 dùng đường dẫn tuyệt đối tới folder md (`GR/others/file to md/md/...`), nằm ngoài `ITBA/`. `--check` vẫn qua, nhưng build sẽ hỏng nếu folder md bị dời.
- L01-q23, L02-q43, L03-q28, L04-q34, L06-q19/q20/q23: vẫn có đáp án là option dài nhất vì option là tên cố định; chênh 1–4 ký tự.
