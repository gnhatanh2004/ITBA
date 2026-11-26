# Prompt cho các agent – khóa học ITBA

Tài liệu này dành cho các agent. Mỗi agent nhận nguyên **mục 1 (prompt chung)**, **mục 2 (schema)** và đúng **một mục prompt riêng** ở mục 3–6. Đường dẫn gốc là `D:/LAPTRINH/crawl extension/TOOL/GR/others/ITBA/` (sau đây gọi là `ITBA/`).

---

## 1. Prompt chung (mọi agent)

Bạn đang làm một phần của khóa học IT Business Analyst. Toàn khóa sẽ thành một file HTML tương tác dành cho người tự học bằng tiếng Việt. Plan đầy đủ ở `ITBA/docs/plan.md`.

**Nguồn và cách đọc**
- `ITBA/docs/nguon.md` liệt kê từng file gốc kèm hai thứ: đường dẫn bản md, và thư mục ảnh trang `ITBA/data/pages/<tên pdf>/p-NNN.jpg`.
- **Đọc kỹ toàn bộ nguồn của mình.**
  - Đọc bản md để lấy chữ.
  - **Mở từng ảnh trang** (Read file .jpg) của mọi trang PDF thuộc bài mình. Ảnh trang là nguồn chuẩn: md bị OCR lỗi, dính chữ và mất sơ đồ.
- **Không Read file .pdf.** Hook sẽ đổi lệnh đó sang bản md lỗi. Không sửa gì trong `ITBA/tai-lieu/`.

**Nội dung**
- Viết tiếng Việt có dấu, câu ngắn, dễ hiểu cho người mới. Thuật ngữ tiếng Anh giữ nguyên, lần đầu ghi kèm nghĩa, ví dụ "Stakeholder (bên liên quan)".
- Bám tài liệu:
  - Mọi ý trong slide phải có mặt trong phần lý thuyết.
  - Được giải thích thêm và lấy ví dụ theo kiến thức BA chuẩn (BABOK v3, UML 2.5, BPMN 2.0) khi slide quá cô đọng, nhưng **không được mâu thuẫn với slide**.
  - Khi slide và kiến thức chuẩn khác nhau, theo slide và ghi chú `<p class="note">` nói rõ chỗ khác.
- Sửa chữ dính, sửa lỗi OCR một cách im lặng. Không chép rác OCR.
- Không bịa số liệu, tên người hay tên công ty ngoài tài liệu. Ví dụ tự đặt phải ghi rõ là "ví dụ".
- Ví dụ và tình huống ưu tiên dùng các case có sẵn trong tài liệu: hệ thống đặt đồ ăn, FoodNow (đặt bàn nhà hàng), quản lý thư viện, SolasMart (chuỗi bán lẻ: bán tại quầy, bán online, kho, nhân sự).

**Luật viết câu trắc nghiệm**
- Mỗi câu kiểm **một** ý và trả lời được từ phần lý thuyết của bài. Trường `src` ghi file và trang làm căn cứ.
- Có đúng một cách hiểu. Không đánh đố bằng chữ. Câu hỏi phủ định phải in đậm `<b>KHÔNG</b>`.
- Option sai phải hợp lý: lấy từ hiểu lầm thường gặp hoặc khái niệm gần nghĩa.
  - Không để đáp án đúng luôn là option dài nhất.
  - "Tất cả đều đúng/sai" dùng ≤ 1 lần mỗi bài.
- Câu một đáp án có 4 option. Câu nhiều đáp án có 4–5 option và 2–3 đáp án đúng. Câu đúng/sai dùng option cố định `d` = "Đúng", `s` = "Sai".
- `explain`: vì sao đáp án đúng, 1–3 câu, có thể kèm mẹo nhớ.
- `why_wrong`: **mỗi** option sai có một lý do riêng, 1 câu.
- Tỉ lệ khoảng 30% `nho` (nhớ), 40% `hieu` (hiểu), 30% `apdung` (tình huống thực tế). Câu `tf` ≤ 20%.
- Không lặp ý với câu khác trong bài. Không chép nguyên câu hỏi gợi ý trên slide làm câu trắc nghiệm.

**Flashcard**
- Mặt trước là khái niệm hoặc câu hỏi ngắn. Mặt sau là định nghĩa ngắn, ví dụ và mẹo nhớ, ≤ 60 từ.

**Thực hành và bài tập**
- Thực hành: làm mẫu từng bước (`steps`), người học làm theo được ngay, có đáp án mẫu.
- Bài tập: tự làm, có 1–3 gợi ý mở dần, đáp án mẫu đầy đủ.
  - Mức `de` (dễ), `tb` (trung bình), `kho` (khó).
  - Bài khó thường là tình huống tổng hợp trên case.
- Bài tập trên slide ("Ví dụ thực hành", "Nhiệm vụ", "Hoạt động") phải có mặt. Thêm đáp án mẫu cho chúng.

**Đầu ra và tự kiểm**
- Ghi đúng file được giao, UTF-8, theo schema ở mục 2.
- Sau mỗi lần ghi, chạy `python -B "ITBA/script/build.py" --check "<file json>"` và sửa tới khi in `OK`.
- Báo cáo cuối (≤ 10 dòng) gồm:
  - số lượng từng phần;
  - trang nào không đọc được;
  - chỗ nào bạn không chắc, hoặc slide mâu thuẫn với kiến thức chuẩn.

---

## 2. Schema (cố định, `build.py` kiểm)

### 2.1. File bài học `data/lessons/<ID>.json`

```json
{
  "id": "L07",
  "session": 7,
  "module": "M2",
  "title": "BACCM – Mô hình 6 khái niệm lõi",
  "goals": ["Nêu được 6 khái niệm lõi của BACCM", "..."],
  "sources": [{"file": "7. BACCM.pdf", "pages": "1-18"}],
  "theory": [
    {"id": "L07-t1", "h": "BACCM là gì", "html": "<p>...</p>{{img:L07-img1}}", "src": "7. BACCM.pdf tr.2-3"}
  ],
  "examples": [
    {"id": "L07-e1", "title": "Áp BACCM vào app đặt đồ ăn", "html": "<table>...</table>", "src": "7. BACCM.pdf tr.10"}
  ],
  "practice": [
    {"id": "L07-p1", "title": "...", "task": "<p>Đề</p>", "steps": ["<p>Bước 1 ...</p>", "<p>Bước 2 ...</p>"], "answer": "<p>Đáp án mẫu</p>", "src": "..."}
  ],
  "exercises": [
    {"id": "L07-x1", "title": "...", "level": "tb", "task": "<p>...</p>", "hints": ["...", "..."], "answer": "<p>...</p>", "src": "..."}
  ],
  "flashcards": [
    {"id": "L07-f1", "front": "Need (Nhu cầu)", "back": "<p>Vấn đề hoặc cơ hội cần giải quyết...</p>"}
  ],
  "quiz": [
    {"id": "L07-q1", "type": "single", "level": "hieu",
     "q": "<p>...</p>",
     "options": [{"id": "a", "t": "..."}, {"id": "b", "t": "..."}, {"id": "c", "t": "..."}, {"id": "d", "t": "..."}],
     "answer": ["b"],
     "explain": "<p>...</p>",
     "why_wrong": {"a": "...", "c": "...", "d": "..."},
     "src": "7. BACCM.pdf tr.5"}
  ],
  "summary": {"points": ["Ý chính 1", "..."], "html": "<p>Đoạn tổng kết ngắn, sơ đồ tư duy dạng bảng nếu cần</p>"},
  "images": [
    {"id": "L07-img1", "path": "data/pages/7. BACCM/p-003.jpg", "caption": "Sơ đồ 6 khái niệm lõi", "crop": [0.05, 0.15, 0.95, 0.9]}
  ]
}
```

**Luật**
- `id` bài là một trong: L01 L02 L03 L04 L05 L06 L07 L09 L11a L11b L11c L12 L13a L13b L14 L16 L20 L21 L23. Mọi id con có tiền tố `<ID>-` và không trùng nhau.
- `module` theo bảng ở plan §3.
- `type`:
  - `single`: `answer` có 1 phần tử.
  - `multi`: `answer` có ≥ 2 phần tử.
  - `tf`: `options` đúng bằng `[{"id":"d","t":"Đúng"},{"id":"s","t":"Sai"}]`, `answer` có 1 phần tử.
- `why_wrong` có **đúng** các key là option không nằm trong `answer`.
- `level` ∈ `nho`, `hieu`, `apdung`. Mức bài tập ∈ `de`, `tb`, `kho`.
- HTML chỉ dùng các thẻ: `p br ul ol li b strong i em u code pre table thead tbody tr th td h4 h5 blockquote mark span div`.
  - Thuộc tính chỉ có `class` (`note`, `tip`, `warn`, `key`), cùng `colspan`/`rowspan` trên `td`/`th`.
  - Không có `style`, không có `script`, không có link.
  - Flashcard `front` và option `t` là chữ thường, không chứa HTML.
- Ảnh:
  - Chèn ảnh bằng `{{img:<id>}}` trong bất kỳ trường html nào. `id` phải khai báo trong `images`.
  - `path` tính từ `ITBA/`, có thể là ảnh trang trong `data/pages/…`, ảnh trong folder md, hoặc file trong `tai-lieu/`.
  - `crop` là tùy chọn, dạng `[x0, y0, x1, y1]` theo tỉ lệ 0–1, dùng để cắt riêng sơ đồ khỏi slide.
  - Mỗi bài ≤ 8 ảnh, chỉ lấy sơ đồ hoặc hình có giá trị học: mô hình, quy trình, UML, BPMN, ERD, bảng mẫu.
- Định mức số lượng theo plan §5. `--check` sẽ báo thiếu.

### 2.2. File khóa học `data/course/course.json`

```json
{
  "title": "IT Business Analyst – Khóa học tương tác",
  "intro_html": "<p>...</p>",
  "modules": [{"id": "M1", "title": "Nền tảng BA và IT", "lessons": ["L01", "L02", "L03"], "summary_html": "<p>...</p>"}],
  "course_summary_html": "<h4>...</h4><p>...</p>",
  "glossary": [{"term": "Stakeholder", "vi": "Bên liên quan", "def": "...", "lesson": "L04"}],
  "case_study": {"title": "SolasMart", "html": "<p>Bối cảnh...</p>", "exercises": [{"id": "CS-x1", "...": "như exercise"}]},
  "quiz": [{"id": "C-q1", "module": "M3", "lessons": ["L09", "L11a"], "...": "như quiz của bài"}],
  "exams": [{"id": "D1", "title": "Đề 1", "minutes": 60, "questions": ["L01-q3", "C-q12", "..."]}]
}
```

Luật cho phần đề thi:
- Có 6 đề, mỗi đề 40 câu. Số câu mỗi module tỉ lệ với số câu trong ngân hàng của module đó, mỗi module ≥ 3 câu.
- Mỗi đề có ≥ 25% câu `apdung`. Một câu xuất hiện trong ≤ 2 đề. Các id phải tồn tại.

---

## 3. Prompt riêng – agent bài học (T2, 17 agent)

> Nhiệm vụ: viết `ITBA/data/lessons/<ID>.json` cho bài **<ID> – <tên>** thuộc module **<M>**, buổi **<số>**. Nguồn: các file ở cột "Nguồn" (tra đường dẫn md và ảnh trang trong `docs/nguon.md`). <Lưu ý riêng>. Làm theo mục 1 và mục 2 của `ITBA/docs/prompt.md`.

| Agent | Bài | Lưu ý riêng |
|---|---|---|
| A01 | L01 Giới thiệu về BA | Định nghĩa của IIBA; việc BA làm; tầm quan trọng (tranh "how the customer explained it"); 6 knowledge area; năng lực lõi; con đường sự nghiệp. Slide 13–14 và 20–22 là ảnh scan: phải xem ảnh. |
| A02 | L02 Kiến thức cơ bản về IT | Giải thích thuật ngữ IT cho người không chuyên. Mỗi thuật ngữ một flashcard. |
| A03 | L03 Quy trình phát triển phần mềm | So sánh các mô hình (Waterfall, Agile/Scrum…) bằng bảng; vai trò BA ở từng giai đoạn. |
| A04 | L04 Tiếp cận dự án và Stakeholder | Dạy cách điền Stakeholder Register theo từng cột của template xlsx; thực hành điền cho SolasMart. |
| A05 | L05 Kỹ thuật khai thác yêu cầu | Từng kỹ thuật: khi nào dùng, ưu và nhược, các bước (bảng so sánh); cách lập Elicitation activity plan; cách dùng phiếu khảo sát và Observation note (mẫu điền sẵn). |
| A06 | L06 Quản lý yêu cầu | RTM (cách đọc và điền theo template xlsx), MoSCoW, kỹ thuật gửi email, quản lý thay đổi, quản lý tài liệu (đặt tên file, phiên bản), quy trình Log task. |
| A07 | L07 BACCM | 6 khái niệm và quan hệ qua lại giữa chúng; áp vào case. |
| A08 | L09 Document Analysis | Cách phân tích tài liệu. **Dùng 13 file SolasMart và "Quy trinh ban hang tai quay" làm bài thực hành chính**: rút actor, quy trình, quy tắc nghiệp vụ, biểu mẫu, vấn đề. Đồng thời viết `ITBA/data/course/solasmart-brief.md` (≤ 150 dòng): bối cảnh, bộ phận, quy trình, biểu mẫu, quy định chính. Agent khóa học (T4) dùng file này. |
| A09 | L11a Yêu cầu chức năng và phi chức năng | FR và NFR, phân tích tổng quan và chi tiết, Functional Decomposition, Permission Matrix, các nhóm NFR. Có nhiều bài tập phân loại FR/NFR. |
| A10 | L11b Phân tích hướng đối tượng + L11c Phân tích GAP | Viết **2 file** `L11b.json` và `L11c.json`. Với L11b: Object và Actor, cách tìm object; các "Nhiệm vụ" hệ thống đặt đồ ăn phải có đáp án mẫu. Với L11c: As-is, To-be, Gap và hành động. |
| A11 | L12 Quy trình nghiệp vụ và BPMN | Giải thích ký hiệu BPMN theo poster `tai-lieu/m4-mo-hinh-hoa/12. BPMN-20-Poster-EN.png` (nhúng ảnh poster, crop từng nhóm ký hiệu); đọc và vẽ quy trình bằng lời (pool, lane, gateway). |
| A12 | L13a UML, Use Case và State Diagram | Các loại sơ đồ UML; Use case diagram (include, extend, generalization); State diagram; giải bài "Quy trình đặt đồ ăn" trong docx. |
| A13 | L13b Đặc tả Use Case + L14 Activity Diagram | Viết **2 file** `L13b.json` và `L14.json`. Hai bài nhỏ, dùng định mức bài nhỏ. Với L13b: dạy từng trường của bảng đặc tả và viết mẫu một use case đầy đủ. Với L14: ký hiệu, swimlane, fork/join, decision. |
| A14 | L16 Các loại tài liệu BA | BRD, SRS, FSD, URD, use case…: mục đích, người đọc, khi nào viết (bảng). Dạy **cấu trúc** BRD, SRS, FSD theo từng mục của template, không chép nguyên văn. Thực hành viết một mục của mỗi template. |
| A15 | L20 ERD | Thực thể, thuộc tính, khóa, quan hệ 1-1/1-n/n-n, ký hiệu; từ nghiệp vụ ra ERD. |
| A16 | L21 Database và kiểu dữ liệu SQL Server | Khái niệm CSDL, bảng, khóa, chuẩn hóa nếu có; bảng kiểu dữ liệu SQL Server (khi nào dùng kiểu nào). Có câu SQL mẫu nếu slide có. |
| A17 | L23 API | API là gì, REST, method, status code, request/response, JSON; cách BA đặc tả API (theo phần API trong FSD nếu liên quan). |

---

## 4. Prompt riêng – agent giao diện (T3)

> Nhiệm vụ: viết `ITBA/script/template.html`. Đây là ứng dụng một trang, không thư viện ngoài, không CDN, chạy được từ file://.
>
> **Dữ liệu.** `build.py` thay chuỗi `__COURSE_DATA__` trong `<script>const COURSE = __COURSE_DATA__;</script>` bằng một object dạng:
> - `course` (schema 2.2);
> - `lessons` (mảng bài theo schema 2.1, đúng thứ tự);
> - `images`, dạng `{id: "data:image/webp;base64,..."}`.
>
> Trong các trường html, build đã đổi `{{img:id}}` thành `<figure><img data-img="id" alt="..."><figcaption>...</figcaption></figure>`. Sau khi render, bạn gán `src` cho ảnh từ `COURSE.images`.
>
> **Tính năng.** Đúng như plan §7: trang chủ, thanh bên, routing `#/...`, 8 tab mỗi bài, trắc nghiệm luyện tập (xáo option, báo ngay, giải thích, why_wrong, nguồn, làm lại, chỉ làm câu sai), bài tập (gợi ý mở dần, đáp án mẫu, đánh dấu đã làm), flashcard (lật, phím tắt, đã thuộc/chưa thuộc, xáo, theo bài/module/toàn khóa), luyện đề (6 đề cố định cùng đề ngẫu nhiên lọc theo module, đồng hồ, nộp bài, điểm theo module, xem lại kèm giải thích, điểm cao nhất), sổ câu sai, thuật ngữ có lọc, tổng kết module và khóa, case study.
>
> **Giao diện.**
> - Màu khai báo dạng biến CSS trên `:root`, có dark mode theo `prefers-color-scheme`.
> - Chạy được ở bề ngang 360 px, không có thanh cuộn ngang.
> - Font hệ thống.
> - Dùng được bằng bàn phím: thấy rõ focus, các nút là thẻ `<button>`.
>
> **Lưu tiến độ.** Mọi truy cập localStorage bọc try/catch, khóa là `itba:v1:*`. Có nút "Xóa tiến độ".
>
> **Kiểm.** Chạy `python -B ITBA/script/build.py --demo` để build bản demo từ dữ liệu mẫu vào `ITBA/data/course/demo.html`. Chạy `node --check` cho phần JS đã tách ra. Tự rà từng luồng theo plan §7. Báo cáo ≤ 10 dòng.

---

## 5. Prompt riêng – agent khóa học (T4)

> Nhiệm vụ: viết `ITBA/data/course/course.json` theo schema 2.2. Nguồn:
> - toàn bộ `ITBA/data/lessons/*.json`;
> - `ITBA/data/course/solasmart-brief.md` và md các file SolasMart (xem `docs/nguon.md`).
>
> Cần viết:
> 1. `intro_html`: khóa học dạy gì, học theo thứ tự nào, cách dùng file (tab, flashcard, đề).
> 2. `summary_html` cho từng module. Mỗi cái gồm ý chính, sơ đồ liên kết các bài dạng bảng, và lỗi hay gặp.
> 3. `course_summary_html`: bức tranh toàn khóa. Nêu công việc BA theo vòng đời dự án (tiếp cận, khai thác, phân tích, mô hình hóa, tài liệu, quản lý thay đổi), mỗi bước dùng kỹ thuật và tài liệu nào (bảng), kèm checklist năng lực cuối khóa.
> 4. `glossary`: ≥ 120 thuật ngữ, gom từ flashcard và lý thuyết, không trùng, mỗi thuật ngữ trỏ về đúng bài.
> 5. `case_study`: bối cảnh SolasMart cùng ≥ 6 bài tập tổng hợp đi theo vòng đời BA: stakeholder, kế hoạch khai thác, FR/NFR, BPMN, use case và đặc tả, ERD, một mục BRD.
> 6. `quiz`: ≥ 120 câu tình huống **liên bài**, cùng luật như mục 1, phần lớn ở mức `apdung`, dùng bối cảnh SolasMart hoặc FoodNow. Không trùng ý với câu trong các bài.
> 7. `exams`: 6 đề theo luật 2.2, trộn câu trong các bài và câu `C-q`.
>
> Chạy `python -B ITBA/script/build.py` (build đầy đủ) tới khi qua. Báo cáo ≤ 10 dòng.

---

## 6. Prompt riêng – agent QA (T5, 3 agent)

> Nhiệm vụ: kiểm và sửa tại chỗ các bài: <danh sách ID>. Với mỗi bài:
> 1. **Phủ nội dung.** Xem lần lượt mọi ảnh trang của nguồn. Ý nào có trên slide mà thiếu trong `theory` thì thêm vào.
> 2. **Đáp án.** Lấy ngẫu nhiên ≥ 20% số câu trắc nghiệm (≥ 10 câu). Tự giải mà **không nhìn** `answer`, rồi so sánh. Câu nào lệch hoặc mơ hồ thì sửa câu, đáp án, `explain`, `why_wrong`.
> 3. **Lộ đáp án.** Kiểm toàn bộ câu: đáp án đúng có phải luôn dài nhất không, có quá nhiều "tất cả đều đúng" không, câu `tf` có vượt 20% không. Sửa chỗ vi phạm.
> 4. **Đáp án mẫu.** Đọc 2 bài thực hành và 2 bài tập: đáp án mẫu có đúng và đủ không.
> 5. **Chữ.** Chính tả, chữ dính, rác OCR còn sót.
>
> Chạy `--check` sau khi sửa. Ghi log vào `ITBA/data/course/qa-<agent>.md`: mỗi dòng gồm id, lỗi và cách sửa. Báo cáo ≤ 10 dòng gồm tỉ lệ câu sai đáp án tìm thấy.

Chia QA:
- QA1: L01 L02 L03 L04 L05 L06.
- QA2: L07 L09 L11a L11b L11c L12.
- QA3: L13a L13b L14 L16 L20 L21 L23.

## 7. Prompt riêng – agent kịch bản "Nghe giảng" (T9)

Mỗi agent viết kịch bản đọc cho 1 bài. File ra: `data/narration/<ID>.json`. Bản mẫu đã được duyệt: `data/narration/L01.json`, đọc nó trước khi viết.

**Đầu vào:**
- `data/lessons/<ID>.json`, gồm theory, examples, practice, quiz và images.
- Ảnh trang trong `data/pages/` khi cần xem lại hình.

**Không sửa file bài học**, chỉ tạo file kịch bản.

**Schema:**
```json
{ "lesson": "L01", "chunks": [
  { "id": "L01-n1", "ref": "L01-t1",
    "say": "lời đọc, văn nói thuần, không HTML",
    "show": { "h": "tiêu đề trên sân khấu", "points": ["ý chính 1", "ý chính 2"], "img": "L01-img1" },
    "ask": ["L01-q3", "L01-q7"] } ] }
```

| Trường | Bắt buộc | Ghi chú |
|---|---|---|
| `id` | có | `<ID>-n1`, `<ID>-n2`… liên tiếp. |
| `ref` | không | id theory/examples/practice mà đoạn này giảng. |
| `say` | có | 3–8 câu nói, tối đa 1400 ký tự. |
| `show.h` | có | tối đa 90 ký tự. |
| `show.points` | có | 1–5 dòng, mỗi dòng tối đa 140 ký tự. Hiện dần theo lời đọc. |
| `show.img` | không | id ảnh đã có trong `images` của bài. |
| `ask` | không | 0–3 id câu **đã có** trong quiz của bài. Không tạo id mới, mỗi câu chỉ hỏi 1 lần. |

**Luật viết `say`:**
- Viết như giảng viên nói, xưng "mình", gọi "bạn". Câu ngắn.
- Mở đoạn đầu bằng giới thiệu buổi. Đoạn cuối là tổng kết, không hỏi.
- Không đọc nguyên bảng. Tóm bảng thành 2–4 nhóm ý để dễ nghe.
- **Giữ nguyên chữ gốc** cho thuật ngữ tiếng Anh và chữ viết tắt (IIBA, BABOK, BRD, Stakeholder, Use case…), vì phụ đề hiện đúng `say`. Không tự phiên âm. `narrate.py` tự đổi chữ viết tắt sang cách đọc khi sinh giọng (bảng `PRON`). Gặp chữ viết tắt chưa có trong `PRON` thì ghi vào báo cáo cuối để mình bổ sung.
- Mỗi câu kết thúc bằng `.` `?` `!` để phụ đề tách câu khớp với giọng đọc. Không dùng `...` giữa câu.
- Không dùng ký tự `< > { }` và không dùng HTML. Số viết bằng chữ khi đứng đầu câu.
- Mục `note` nói slide khác chuẩn thì nói ngắn "slide ghi X, tên chuẩn là Y".

**Luật `show`:**
- `h` và `points` là chữ hiện trên màn hình, được dùng ký hiệu (→, ·) và tên tiếng Anh gốc.
- `points` là ý khung, không chép nguyên câu đọc.
- Có hình minh họa đúng ý thì gắn `img`.

**Luật `ask`:** đọc xong một ý chính thì hỏi 1–3 câu, ưu tiên mức hiểu và áp dụng, đúng nội dung vừa đọc. Mỗi bài 6–12 điểm hỏi. Bài nhỏ (L09, L11c, L13b, L14) 3–6 điểm hỏi.

**Độ dài:** bài lớn 12–18 đoạn, bài nhỏ 6–10 đoạn.

**Tự kiểm:** `python -B script/narrate.py --check <ID>` tới khi in `OK`. **Không chạy** sinh audio, việc đó mình làm sau.

**Báo cáo cuối** (≤ 120 từ): số đoạn, số điểm hỏi, ước số phút, chỗ nào không chắc.
