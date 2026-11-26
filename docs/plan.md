# Plan: khóa học ITBA thành 1 file HTML tương tác

## 1. Mục tiêu

Gom toàn bộ tài liệu khóa IT Business Analyst (35 file trong `tai-lieu/`, 415 trang slide và 14 file Word/Excel) thành **một file HTML mở offline**. File chia theo bài học. Mỗi bài có:

- lý thuyết, ví dụ kèm giải thích;
- thực hành có hướng dẫn từng bước, bài tập có gợi ý và đáp án mẫu;
- flashcard, trắc nghiệm có giải thích ngay sau khi trả lời.

Phần chung của cả khóa gồm tổng kết từng module, tổng kết khóa, bảng thuật ngữ, case study SolasMart, nhiều đề thi luyện tập và sổ câu sai.

Kiểm được bằng:
- `python script/build.py` chạy qua mà không lỗi;
- mở được `result/ITBA-khoa-hoc.html` bằng file://, khi không có mạng;
- tất cả 19 bài đủ định mức ở mục 5;
- QA đối chiếu mẫu với slide và không còn câu sai đáp án.

## 2. Giả định (sửa khi duyệt nếu sai)

1. **Vị trí.** Mọi thứ làm trong `GR/others/ITBA/`. Để giữ luật "folder chỉ chứa toàn file hoặc toàn folder", 35 file gốc **đã được dời vào `ITBA/tai-lieu/`**, giữ nguyên tên. Muốn hoàn tác thì dời ngược ra.
2. **Buổi học bị thiếu.** Không có tài liệu cho buổi 8, 10, 15, 17, 18, 19 và 22. Khóa học chỉ dạy những gì có tài liệu, không bịa thêm bài.
3. **Nội dung bám tài liệu.** Lý thuyết và đáp án lấy từ slide/tài liệu. Được thêm giải thích và ví dụ theo kiến thức BA chuẩn (BABOK, UML, BPMN 2.0) khi slide quá ngắn, nhưng không được mâu thuẫn với slide.
4. **Ngôn ngữ.** Tiếng Việt có dấu. Giữ thuật ngữ tiếng Anh gốc kèm nghĩa, ví dụ "Stakeholder (bên liên quan)".
5. **Case study.** SolasMart (13 file trong zip) và "Quy trình bán hàng tại quầy" là case study xuyên suốt, dùng cho thực hành, bài tập và câu hỏi tình huống. Không làm thành bài riêng.
6. **Template BRD/SRS/FSD** (88K và 47K ký tự) chỉ dạy cấu trúc và cách viết từng mục, không chép nguyên văn.

## 3. Nguồn → bài học

| Bài | Tên | Nguồn (trong `tai-lieu/`) | Trang |
|---|---|---|---|
| L01 | Giới thiệu về BA | Buổi 1_Giới thiệu về BA.pdf | 25 |
| L02 | Kiến thức cơ bản về IT | 2. Kien thuc co ban ve IT.pdf | 22 |
| L03 | Quy trình phát triển phần mềm | 3. Quy trinh phat trien phan mem.pdf | 28 |
| L04 | Tiếp cận dự án và Stakeholder | 4. Tiep can du an.pdf, 4. Stakeholder_Register_Template.xlsx | 25 |
| L05 | Kỹ thuật khai thác yêu cầu | 5. Ky thuat khai thac yeu cau.pdf, 5. Elicitation activity plan.pdf, 5. Mau phieu khao sat.docx, 5. Observation_Note_Template.docx | 44 |
| L06 | Quản lý yêu cầu | 6. Quan ly yeu cau.pdf, 6. MaTranTuyVet-RTM.xlsx, 6. Quan ly thay doi.docx, 6. Quan ly tai lieu.docx, 6. HƯỚNG DẪN QUY TRÌNH SỬ DỤNG LOG TASK.docx | 25 |
| L07 | BACCM (6 khái niệm lõi) | 7. BACCM.pdf | 18 |
| L09 | Phân tích tài liệu (Document Analysis) | 9. Document Analysis.pdf, Tai lieu SolasMart.zip, Quy trinh ban hang tai quay.docx | 10 |
| L11a | Yêu cầu chức năng và phi chức năng | 11. Yeu cau chuc nang va yeu cau phi chuc nang.pdf | 35 |
| L11b | Phân tích hướng đối tượng | 11. Phan tich huong doi tuong.pdf | 24 |
| L11c | Phân tích GAP | 11. Phan tich GAP.pdf | 8 |
| L12 | Quy trình nghiệp vụ và BPMN | 12. Business Process.pdf, 12. BPMN-20-Poster-EN.png | 19 |
| L13a | UML, Use Case và State Diagram | 13. UML.pdf, 13. Vẽ UseCase và State Diagram - Quy trình Đặt đồ ăn.docx | 20 |
| L13b | Đặc tả Use Case | 13. Đặc tả UseCase.pdf | 3 |
| L14 | Activity Diagram | 14. Activity Diagram.pdf | 5 |
| L16 | Các loại tài liệu BA | 16. Cac loai tai lieu BA.pdf, BRD_Template.docx, SRS_Template.docx, FSD_Template.docx | 31 |
| L20 | ERD | 20. ERD.pdf | 15 |
| L21 | Database và kiểu dữ liệu SQL Server | 21. Database.pdf, 21. Kieu du lieu trong Sql Server.pdf | 33 |
| L23 | API | 23. Api - Ly Thuyet.pdf | 25 |

Các bài được gom thành 6 module:

| Module | Tên | Bài |
|---|---|---|
| M1 | Nền tảng BA và IT | L01, L02, L03 |
| M2 | Dự án và yêu cầu | L04, L05, L06, L07 |
| M3 | Phân tích yêu cầu | L09, L11a, L11b, L11c |
| M4 | Mô hình hóa | L12, L13a, L13b, L14 |
| M5 | Tài liệu BA | L16 |
| M6 | Dữ liệu và tích hợp | L20, L21, L23 |

## 4. Vì sao không viết thẳng từ bản md

Bản md do tool "file to md" tạo ra bị mất nhiều thông tin:

- Slide scan bị OCR thành chữ tiếng Anh lỗi, ví dụ "Cac khai niém co' ban vé".
- Nhiều slide chỉ còn một dãy ảnh nhỏ.
- Chữ tiếng Việt bị dính nhau, ví dụ "nghiệp vụtrong", "sựnghiệp".
- Có link ảnh trỏ vào thư mục tạm đã bị xóa.

Vì vậy **T0 chụp mọi trang PDF thành ảnh** và lưu vào `data/pages/`. Agent đọc md để lấy chữ và **xem ảnh từng trang** để lấy đúng nội dung và sơ đồ. Ảnh trang mới là nguồn chuẩn. Agent không Read file PDF, vì hook sẽ đổi lệnh đó sang bản md lỗi.

## 5. Định mức mỗi bài

| Loại | Bài lớn (≥ 15 trang) | Bài nhỏ (< 15 trang) |
|---|---|---|
| Phần lý thuyết | phủ **mọi** slide có nội dung | như bài lớn |
| Ví dụ và giải thích | ≥ 4 | ≥ 2 |
| Thực hành có hướng dẫn | ≥ 3 | ≥ 2 |
| Bài tập (dễ, trung bình, khó) | ≥ 5 | ≥ 3 |
| Flashcard | ≥ 25 | ≥ 12 |
| Trắc nghiệm | ≥ 40 | ≥ 20 |

Trắc nghiệm có tỉ lệ khoảng 30% câu nhớ, 40% câu hiểu và 30% câu áp dụng (tình huống). Có ba dạng: một đáp án, nhiều đáp án, và đúng/sai. Câu đúng/sai chiếm ≤ 20%.

Tổng ước tính: khoảng 650 câu trắc nghiệm trong các bài, khoảng 120 câu tình huống liên bài, khoảng 400 flashcard và 6 đề thi.

## 6. Kiến trúc

```
ITBA/
  tai-lieu/        file gốc (không sửa), chia theo module: m1-nen-tang/ m2-du-an-yeu-cau/ m3-phan-tich/
                   m4-mo-hinh-hoa/ m5-tai-lieu-ba/ m6-du-lieu-tich-hop/ solasmart/ (case study, 13 file)
  docs/            plan.md, prompt.md, tasks.md, nguon.md (T0 sinh)
  script/          render.py, build.py, template.html
  data/
    pages/<tên pdf>/p-001.jpg   ảnh từng trang (T0)
    lessons/L01.json …          nội dung từng bài (agent)
    course/course.json          tổng kết, thuật ngữ, case study, ngân hàng tình huống, đề thi
  result/ITBA-khoa-hoc.html     file duy nhất giao cho người học
```

- **Dữ liệu tách khỏi giao diện.** Agent chỉ viết JSON theo một schema cố định (trong `prompt.md`). `template.html` chứa CSS và JS. `build.py` kiểm dữ liệu rồi nhúng JSON và ảnh vào template, tạo ra một file HTML.
- **`build.py` từ chối dữ liệu xấu** và in rõ lỗi ở bài nào, câu nào. Các lỗi bị bắt:
  - id trùng;
  - đáp án không khớp option nào;
  - thiếu giải thích, hoặc thiếu lý do sai cho từng option sai;
  - câu hỏi gần trùng giữa các bài (difflib ≥ 0.9);
  - thẻ HTML ngoài danh sách cho phép;
  - ảnh không tồn tại;
  - bài thiếu định mức.

  Lệnh `--check <file>` dùng để agent tự kiểm bài của mình.
- **Ảnh.** Chỉ nhúng sơ đồ quan trọng, mỗi bài ≤ 8 ảnh. Ảnh được Pillow thu về ≤ 1200 px và lưu dạng webp. Mục tiêu file HTML < 8 MB.
- **Không dùng CDN, không dùng thư viện ngoài.** File phải chạy được từ file:// khi không có mạng.

## 7. Giao diện (template.html)

- **Bố cục.**
  - Thanh bên liệt kê module → bài, có % tiến độ.
  - URL dạng `#/L05/quiz` để tải lại trang vẫn ở đúng chỗ.
  - Có dark mode theo hệ thống và chạy được trên điện thoại.
- **Trang chủ.**
  - Giới thiệu khóa, lộ trình 6 module, tiến độ chung.
  - Lối tắt: Luyện đề, Flashcard toàn khóa, Sổ câu sai, Thuật ngữ, Tổng kết khóa.
- **Trang bài.** Gồm các tab: Tổng quan (mục tiêu, nguồn) · Lý thuyết · Ví dụ · Thực hành · Bài tập · Flashcard · Trắc nghiệm · Tổng kết.
- **Trắc nghiệm luyện tập.**
  - Option được xáo thứ tự mỗi lần hiển thị.
  - Chọn xong là báo đúng hay sai ngay. Câu nhiều đáp án có nút "Kiểm tra".
  - Sau khi trả lời, hiện giải thích, lý do từng option sai, và nguồn (file, trang).
  - Có điểm, nút "Làm lại" và nút "Chỉ làm câu sai".
- **Bài tập và thực hành.**
  - Đề bài, gợi ý mở dần từng cái, nút "Xem đáp án mẫu".
  - Đánh dấu "Đã làm".
- **Flashcard.**
  - Bấm hoặc nhấn Space để lật, ←/→ để chuyển thẻ.
  - Nút "Đã thuộc" / "Chưa thuộc", nút xáo bài, lọc chỉ thẻ chưa thuộc.
  - Có chế độ toàn khóa hoặc theo module.
- **Luyện đề.**
  - Có 6 đề cố định, mỗi đề 40 câu trong 60 phút.
  - "Đề ngẫu nhiên" lấy 40 câu, lọc được theo module.
  - Trong lúc làm không hiện đáp án. Nộp bài xong hiện điểm, điểm theo module, và xem lại từng câu kèm giải thích.
  - Lưu điểm cao nhất của từng đề.
- **Sổ câu sai.** Gom mọi câu từng trả lời sai, cho làm lại. Câu nào làm đúng 2 lần liên tiếp thì rời sổ.
- **Thuật ngữ.** Có ô lọc. Bấm vào thuật ngữ thì mở bài chứa nó.
- **Lưu tiến độ.** Dùng localStorage, mọi lệnh đọc/ghi bọc try/catch, có nút "Xóa tiến độ". Không có localStorage thì trang vẫn chạy được.

## 8. Workflow và agents

| Pha | Việc | Ai | Chạy song song |
|---|---|---|---|
| 0 | T0: chụp trang, giải nén SolasMart, chuyển md, sinh `docs/nguon.md`. T1: `build.py` (kiểm + build) kèm self-test | mình | – |
| 1 | T2: 17 agent viết 19 file `data/lessons/*.json`. T3: 1 agent UI viết `template.html` | 18 agent | có, cùng lúc |
| 2 | T4: agent khóa học viết `course.json` (tổng kết module và khóa, thuật ngữ, case study, khoảng 120 câu tình huống, 6 đề) | 1 agent | sau pha 1 |
| 2 | T5: 3 agent QA đối chiếu bài với ảnh slide, sửa tại chỗ, ghi log | 3 agent | song song với T4 |
| 3 | T6: build, kiểm JS (`node --check`), mở thử, sửa lỗi, báo cáo | mình | – |

Mỗi agent dùng prompt chung cộng với prompt riêng trong `prompt.md`. Agent bài học tự chạy `build.py --check` tới khi qua.

## 9. Rủi ro

| Rủi ro | Cách chặn |
|---|---|
| Agent bịa nội dung không có trong slide | Bắt buộc trường `src` (file + trang) cho từng câu; QA kiểm mẫu ≥ 20% số câu mỗi bài |
| Đáp án sai | QA giải lại câu hỏi mà không nhìn đáp án, so với đáp án đã ghi, câu nào lệch thì sửa và ghi log |
| Câu hỏi lộ đáp án (đáp án luôn dài nhất, "tất cả đều đúng") | Luật viết câu hỏi trong prompt; giao diện xáo option; QA kiểm |
| JSON hỏng vì agent viết tay | `--check` sau mỗi lần ghi |
| File HTML quá nặng | Giới hạn ảnh; build in kích thước; vượt 8 MB thì giảm chất lượng ảnh |
| Agent tốn token khi xem 415 ảnh trang | Ảnh 110 dpi JPEG; mỗi agent chỉ xem trang của bài mình |

## 10. Nghe giảng (thêm ngày 26/11)

Mỗi bài có thêm tab **Nghe giảng**, đặt đầu tiên và mở mặc định:
- **Sân khấu bảng đen:** tiêu đề ý, các gạch đầu dòng hiện dần, ảnh có sẵn của bài, phụ đề theo câu.
- **Giọng đọc:** edge-tts, giọng `vi-VN-NamMinhNeural` (nam, user chọn 26/11). Mỗi bài 1 MP3.
- **Điểm hỏi:** đọc xong ý chính thì tự dừng và popup 1–3 câu quiz có sẵn. Trả lời xong thấy giải thích, bấm "Nghe tiếp". Câu trả lời tính vào tiến độ và sổ câu sai.
- **Điều khiển:** play/pause, tua có vạch đánh dấu điểm hỏi, tốc độ 1 / 1.5 / 2 / 2.5 / 3x (mặc định 1.5x), đoạn trước/sau, phụ đề, mục lục đoạn. Nhớ chỗ nghe dở.

Dữ liệu:
- Kịch bản `data/narration/<ID>.json` (schema `prompt.md` §7).
- `script/narrate.py` sinh `data/audio/<ID>.mp3` và `<ID>.json`. File json ghi mốc từng đoạn và từng câu, tính từ kích thước byte của MP3 CBR 48 kbps. Lệnh sinh chỉ làm lại bài có kịch bản đổi.
- `build.py` kiểm kịch bản, báo khi audio cũ, nhúng mốc vào HTML. MP3 **không nhúng**: HTML trỏ `../data/audio/`. Phần nghe vì vậy cần giữ nguyên cấu trúc thư mục `result/` cạnh `data/`.
- Lesson JSON đã QA giữ nguyên.

Logic dừng:
- Chỉ dừng khi đang phát mà vượt qua mốc. Tua qua mốc thì không dừng.
- Mỗi mốc hỏi 1 lần mỗi lượt nghe. "Nghe tiếp từ X" coi các mốc trước X là đã hỏi.
