# Đầu việc – khóa học ITBA

Ký hiệu: `[ ]` chưa làm, `[x]` xong. Mỗi việc ghi rõ cách kiểm.

## Đã làm (lúc lập plan, 25/11/2026)

- [x] Dời 35 file gốc vào `tai-lieu/` để `ITBA/` chỉ chứa folder con.
- [x] Chuyển 33 file sang md bằng tool "file to md". Bản md cũ theo đường dẫn trước khi dời đã được xóa.
- [x] Viết `docs/plan.md`, `docs/prompt.md`, `docs/tasks.md`.

## Pha 0: chuẩn bị (mình làm)

- [x] **T0a `script/render.py`**: 415 ảnh (27,5 MB), 45 bản md. Zip SolasMart đã được giải nén sẵn ở `tai-lieu/solasmart/`.
  - Chụp mọi trang của 21 file PDF thành `data/pages/<tên pdf>/p-NNN.jpg` (110 dpi, JPEG q80).
  - Chuyển 13 file SolasMart sang md.
  - Sinh `docs/nguon.md`: mỗi bài → file gốc → đường dẫn md và thư mục ảnh trang, số trang.
  - Chạy lại không làm lại phần đã có.
  - **Kiểm:** đủ 415 ảnh; `nguon.md` có đủ 19 bài và 48 file nguồn (35 trong `tai-lieu/` trừ zip, cộng 13 file SolasMart).
- [x] **T1 `script/build.py`**: selftest PASS, `--demo` build được.
  - `--check <json>`: kiểm một bài theo schema `prompt.md` §2.1 và định mức plan §5. In `OK` hoặc danh sách lỗi có id.
  - Build mặc định:
    - kiểm toàn bộ bài và `course.json`, gồm cả lỗi câu gần trùng giữa các bài và đề thi trỏ tới id không tồn tại;
    - cắt và thu nhỏ ảnh, lưu dạng webp;
    - đổi `{{img:id}}` thành `<figure>`;
    - nhúng tất cả vào `template.html`, có escape `</`;
    - ghi `result/ITBA-khoa-hoc.html` và in kích thước file.
  - `--demo`: build từ bộ dữ liệu mẫu nhúng sẵn trong script, ra `data/course/demo.html`, dùng cho agent UI.
  - `--selftest`: dữ liệu mẫu hợp lệ phải qua. 8 lỗi cố ý phải bị bắt: id trùng, đáp án không khớp, thiếu `why_wrong`, `tf` sai option, thẻ HTML lạ, ảnh thiếu, câu gần trùng, thiếu định mức.
  - **Kiểm:** `python -B script/build.py --selftest` in PASS.

## Pha 1: nội dung và giao diện (18 agent chạy song song)

Prompt: `prompt.md` §1 + §2 + dòng của agent trong §3. Mỗi agent tự chạy `--check` tới khi qua.

- [x] T2-A01 → `data/lessons/L01.json`
- [x] T2-A02 → `L02.json`
- [x] T2-A03 → `L03.json`
- [x] T2-A04 → `L04.json`
- [x] T2-A05 → `L05.json`
- [x] T2-A06 → `L06.json`
- [x] T2-A07 → `L07.json`
- [x] T2-A08 → `L09.json` + `data/course/solasmart-brief.md`
- [x] T2-A09 → `L11a.json`
- [x] T2-A10 → `L11b.json` + `L11c.json`
- [x] T2-A11 → `L12.json`
- [x] T2-A12 → `L13a.json`
- [x] T2-A13 → `L13b.json` + `L14.json`
- [x] T2-A14 → `L16.json`
- [x] T2-A15 → `L20.json`
- [x] T2-A16 → `L21.json`
- [x] T2-A17 → `L23.json`
- [x] T3-UI → `script/template.html` (`prompt.md` §4). **Kiểm:** `--demo` mở được, `node --check` qua.
- **Kiểm cả pha:**
  - 19 file đều `--check OK`;
  - đọc báo cáo của từng agent, ghi các trang không đọc được và chỗ không chắc vào mục "Ghi chú" bên dưới.

## Pha 2: khóa học và QA (4 agent song song)

- [x] **T4** → `data/course/course.json` (`prompt.md` §5). **Kiểm:** build đầy đủ qua; ≥ 120 câu `C-q`; ≥ 120 thuật ngữ; 6 đề × 40 câu.
- [x] **T5-QA1** → L01–L06, log ở `data/course/qa-QA1.md`
- [x] **T5-QA2** → L07, L09, L11a, L11b, L11c, L12, log ở `qa-QA2.md`
- [x] **T5-QA3** → L13a, L13b, L14, L16, L20, L21, L23, log ở `qa-QA3.md`
- **Kiểm cả pha:**
  - tỉ lệ câu sai đáp án mà QA tìm thấy ≤ 5% mẫu kiểm;
  - nếu vượt 5% thì cho QA kiểm toàn bộ bài đó.

T4 đọc các bài trong lúc QA đang sửa. Nếu QA sửa nội dung câu hỏi mà id không đổi thì đề thi vẫn đúng. QA không được xóa id câu hỏi, chỉ được sửa nội dung.

## Pha 3: ghép và nghiệm thu (mình làm)

- [x] **T6** Chạy `python -B script/build.py`, ra `result/ITBA-khoa-hoc.html`.
  - **Kiểm:**
    - build qua, file < 8 MB;
    - `node --check` cho JS;
    - mở bằng file:// và đi hết các luồng: 1 bài đủ 8 tab, làm 5 câu trắc nghiệm (có câu sai để thấy giải thích), lật flashcard, làm và nộp 1 đề, sổ câu sai, thuật ngữ, tổng kết khóa;
    - tải lại trang vẫn còn tiến độ.
- [x] **T7** Dọn file:
  - xóa `data/course/demo.html`;
  - giữ `data/pages` (QA và sửa sau này còn dùng);
  - cập nhật `tasks.md`.
- [x] **T8** Báo cáo cho user: số liệu từng bài, các trang nguồn không đọc được, chỗ slide khác kiến thức chuẩn, cách mở file.

## Pha 4: Nghe giảng (plan §10, prompt §7)

- [x] **T9a** `script/narrate.py`: `--check`, sinh MP3 và mốc thời gian, bỏ qua bài không đổi, chạy TTS song song 2 đoạn, thử lại tối đa 12 lần (dịch vụ hay trả rỗng ngẫu nhiên).
- [x] **T9b** Pilot L01:
  - kịch bản 14 đoạn, 12 điểm hỏi, 8,8 phút;
  - tab Nghe giảng trong `template.html`;
  - `build.py` gắn dữ liệu nghe.
  - **Kiểm:** `listen.py` (scratchpad) 20/20 PASS; flows, test.js và final.py cũ vẫn PASS.
- [x] **T9c** User nghe thử L01 và duyệt (26/11): giữ giọng NamMinh, phụ đề chữ gốc, tốc độ 1–3x mặc định 1.5x. Giọng đa ngôn ngữ vẫn đọc tiếng Anh kiểu Việt, ghép 2 giọng thì dịch vụ lỗi nhiều nên bỏ.
- [x] **T9d** 18 agent viết kịch bản L02…L23 theo `prompt.md` §7, cả 19 bài `--check` OK. Bảng `PRON` bổ sung chữ viết tắt agent báo thiếu.
- [x] **T9e** (26/11) `python -B script/narrate.py` sinh audio 18 bài rồi chạy `build.py`. Phụ đề khi số câu TTS lệch được nội suy mốc theo độ dài câu, vẫn hiện chữ gốc. **Kiểm:** "Dữ liệu OK (19 bài có Nghe giảng)", `listen.py` PASS.

## Ghi chú (điền trong lúc làm)

- 26/11: Agent chạm giới hạn 5 giờ của API, được cho chạy tiếp sau khi giới hạn reset.
- User dời `ITBA` và `file to md` sang `GR/others/`. Đã sửa đường dẫn trong docs, hook `~/.claude/settings.json` và `~/.claude/CLAUDE.md`.
- Pha 1 xong: cả 19 bài qua `--check`. Toàn khóa có 773 câu trắc nghiệm, 589 flashcard và 107 ảnh.
- Bộ kiểm câu gần trùng báo nhầm các câu kiểu "X là viết tắt của gì?". Đã sửa để so cả câu hỏi lẫn option, selftest vẫn PASS.
- T6: trước khi build cuối, chép các ảnh nằm ngoài ITBA (L06, L16 đang trỏ sang `file to md/md`) vào `data/img/` rồi sửa `path`. Chưa làm vì QA đang sửa các file này.
- 26/11: Làm lại giao diện theo `.claude/tối ưu/uiux` (impeccable craft-floor, mode Operate):
  - Font Be Vietnam Pro: chạy `script/fetch_fonts.py` để tải vào `data/fonts/`, build nhúng base64 vào HTML.
  - Thanh bên màu bảng đen, điểm nhấn bút dạ quang, icon SVG, flashcard lật 3D.
  - Bỏ viền màu dày bên trái và các ký tự ✓/✗ dùng làm icon.
  - `flows.py` và `test.js` (trong scratchpad) đều PASS.
- Các chỗ slide khác kiến thức chuẩn đều có `<p class="note">` trong bài. Danh sách chi tiết nằm trong báo cáo của từng agent.

- Tool "file to md": link ảnh `p4l/p-N-full.png` trỏ vào thư mục tạm đã bị xóa, và slide scan bị OCR bằng tiếng Anh. Đây là lỗi của tool, task này **không sửa**; T0 đi đường riêng bằng ảnh trang. Có sửa tool hay không thì chờ user quyết.
