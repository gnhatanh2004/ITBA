"""Kiểm dữ liệu khóa học và build 1 file HTML.

  python -B build.py                 kiểm toàn bộ + build result/ITBA-khoa-hoc.html
  python -B build.py --check <json>  kiểm 1 bài (agent tự kiểm)
  python -B build.py --demo          build dữ liệu mẫu ra data/course/demo.html (cho agent UI)
  python -B build.py --selftest      tự kiểm bộ kiểm
"""
import base64, copy, difflib, html, io, json, re, sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LESSONS_DIR, COURSE = ROOT / "data" / "lessons", ROOT / "data" / "course" / "course.json"
TEMPLATE, OUT = ROOT / "script" / "template.html", ROOT / "result" / "ITBA-khoa-hoc.html"
NARR_DIR, AUDIO_DIR = ROOT / "data" / "narration", ROOT / "data" / "audio"

MODULE_OF = {"L01": "M1", "L02": "M1", "L03": "M1", "L04": "M2", "L05": "M2", "L06": "M2", "L07": "M2",
             "L09": "M3", "L11a": "M3", "L11b": "M3", "L11c": "M3", "L12": "M4", "L13a": "M4", "L13b": "M4",
             "L14": "M4", "L16": "M5", "L20": "M6", "L21": "M6", "L23": "M6"}
ORDER = list(MODULE_OF)
SMALL = {"L09", "L11c", "L13b", "L14"}  # < 15 trang slide → định mức bài nhỏ (plan §5)
QUOTA = {"big": dict(examples=4, practice=3, exercises=5, flashcards=25, quiz=40),
         "small": dict(examples=2, practice=2, exercises=3, flashcards=12, quiz=20)}
TAGS = set("p br ul ol li b strong i em u code pre table thead tbody tr th td h4 h5 blockquote mark span div".split())
CLASSES = {"note", "tip", "warn", "key"}
TF = [{"id": "d", "t": "Đúng"}, {"id": "s", "t": "Sai"}]
IMG_RE = re.compile(r"\{\{img:([\w-]+)\}\}")
NEAR = 0.9


class _Html(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.bad = []

    def handle_starttag(self, tag, attrs):
        if tag not in TAGS:
            self.bad.append(f"thẻ <{tag}>")
        for k, v in attrs:
            if k == "class" and set((v or "").split()) <= CLASSES:
                continue
            if k in ("colspan", "rowspan") and tag in ("td", "th") and (v or "").isdigit():
                continue
            self.bad.append(f"thuộc tính {k}= trên <{tag}>")

    handle_startendtag = handle_starttag

    def handle_endtag(self, tag):
        if tag not in TAGS:
            self.bad.append(f"thẻ </{tag}>")


def html_errors(s):
    p = _Html()
    p.feed(s)
    p.close()
    return p.bad


def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html.unescape(s))).strip().lower()


class Checker:
    def __init__(self):
        self.errors = []

    def err(self, where, msg):
        self.errors.append(f"{where}: {msg}")

    def text(self, where, v, required=True):
        if not isinstance(v, str) or (required and not v.strip()):
            self.err(where, "thiếu hoặc rỗng (phải là chuỗi)")
        elif re.search(r"<[a-zA-Z/]", v):
            self.err(where, "chuỗi thường, không được chứa HTML")

    def html(self, where, v, imgs):
        if not isinstance(v, str) or not v.strip():
            return self.err(where, "html thiếu hoặc rỗng")
        for b in sorted(set(html_errors(v))):
            self.err(where, f"HTML không cho phép: {b}")
        for ref in IMG_RE.findall(v):
            if ref not in imgs:
                self.err(where, f"{{{{img:{ref}}}}} chưa khai báo trong images")

    def ids(self, where, items, prefix, seen):
        if not isinstance(items, list):
            self.err(where, "phải là mảng")
            return []
        good = []
        for i, it in enumerate(items):
            if not isinstance(it, dict):
                self.err(f"{where}[{i}]", "phải là object")
                continue
            iid = it.get("id")
            if not isinstance(iid, str) or not iid.startswith(prefix + "-"):
                self.err(f"{where}[{i}]", f"id phải bắt đầu bằng '{prefix}-' (đang là {iid!r})")
            elif iid in seen:
                self.err(iid, "id trùng")
            else:
                seen.add(iid)
            good.append(it)
        return good

    def question(self, q, imgs):
        w = q.get("id", "?")
        t = q.get("type")
        if t not in ("single", "multi", "tf"):
            return self.err(w, f"type phải là single|multi|tf (đang là {t!r})")
        if q.get("level") not in ("nho", "hieu", "apdung"):
            self.err(w, "level phải là nho|hieu|apdung")
        self.html(f"{w}.q", q.get("q"), imgs)
        self.html(f"{w}.explain", q.get("explain"), imgs)
        self.text(f"{w}.src", q.get("src"))
        opts = q.get("options")
        if not isinstance(opts, list) or not all(isinstance(o, dict) for o in opts):
            return self.err(w, "options phải là mảng object {id,t}")
        oids = [o.get("id") for o in opts]
        if len(set(oids)) != len(oids):
            self.err(w, "id option trùng")
        for o in opts:
            self.text(f"{w}.option {o.get('id')}", o.get("t"))
        ans = q.get("answer")
        if not isinstance(ans, list) or not ans or len(set(ans)) != len(ans):
            return self.err(w, "answer phải là mảng id option, không trùng")
        if t == "tf" and opts != TF:
            self.err(w, 'tf: options phải đúng [{"id":"d","t":"Đúng"},{"id":"s","t":"Sai"}]')
        if t == "single" and len(opts) != 4:
            self.err(w, "single: cần đúng 4 option")
        if t == "multi" and not 4 <= len(opts) <= 5:
            self.err(w, "multi: cần 4–5 option")
        if t in ("single", "tf") and len(ans) != 1:
            self.err(w, f"{t}: answer phải có đúng 1 phần tử")
        if t == "multi" and not 2 <= len(ans) <= 3:
            self.err(w, "multi: answer phải có 2–3 phần tử")
        for a in ans:
            if a not in oids:
                self.err(w, f"đáp án {a!r} không khớp option nào")
        wrong = {o for o in oids if o not in ans}
        ww = q.get("why_wrong")
        if not isinstance(ww, dict) or set(ww) != wrong:
            self.err(w, f"why_wrong phải có đúng các key {sorted(wrong)}")
        else:
            for k, v in ww.items():
                if not isinstance(v, str) or not v.strip():
                    self.err(w, f"why_wrong[{k}] rỗng")

    def exercise(self, x, imgs, practice=False):
        w = x.get("id", "?")
        self.text(f"{w}.title", x.get("title"))
        self.html(f"{w}.task", x.get("task"), imgs)
        self.html(f"{w}.answer", x.get("answer"), imgs)
        self.text(f"{w}.src", x.get("src"))
        key = "steps" if practice else "hints"
        arr = x.get(key)
        if not isinstance(arr, list) or not arr:
            return self.err(w, f"{key} phải là mảng không rỗng")
        for i, s in enumerate(arr):
            self.html(f"{w}.{key}[{i}]", s, imgs)
        if not practice and x.get("level") not in ("de", "tb", "kho"):
            self.err(w, "level phải là de|tb|kho")

    def lesson(self, d, quota=True, seen=None):
        seen = set() if seen is None else seen
        lid = d.get("id")
        if lid not in MODULE_OF:
            self.err("id", f"id bài không hợp lệ: {lid!r}")
            return
        if d.get("module") != MODULE_OF[lid]:
            self.err(lid, f"module phải là {MODULE_OF[lid]}")
        if not isinstance(d.get("session"), int):
            self.err(lid, "session phải là số")
        self.text(f"{lid}.title", d.get("title"))
        if not isinstance(d.get("goals"), list) or not d["goals"]:
            self.err(lid, "goals phải là mảng không rỗng")
        else:
            for i, g in enumerate(d["goals"]):
                self.text(f"{lid}.goals[{i}]", g)
        if not isinstance(d.get("sources"), list) or not d["sources"]:
            self.err(lid, "sources phải là mảng không rỗng")
        imgs = {}
        for im in self.ids(f"{lid}.images", d.get("images", []), lid, seen):
            imgs[im.get("id")] = im
            self.text(f"{im.get('id')}.caption", im.get("caption"))
            p = img_path(im.get("path", ""))
            if not p or not p.is_file():
                self.err(im.get("id"), f"ảnh không tồn tại: {im.get('path')!r}")
            c = im.get("crop")
            if c is not None and not (isinstance(c, list) and len(c) == 4 and all(isinstance(v, (int, float)) for v in c)
                                      and 0 <= c[0] < c[2] <= 1 and 0 <= c[1] < c[3] <= 1):
                self.err(im.get("id"), "crop phải là [x0,y0,x1,y1] trong 0–1, x0<x1, y0<y1")
        if len(imgs) > 8:
            self.err(lid, f"tối đa 8 ảnh (đang {len(imgs)})")
        for t in self.ids(f"{lid}.theory", d.get("theory"), lid, seen):
            self.text(f"{t.get('id')}.h", t.get("h"))
            self.html(f"{t.get('id')}.html", t.get("html"), imgs)
            self.text(f"{t.get('id')}.src", t.get("src"))
        for e in self.ids(f"{lid}.examples", d.get("examples"), lid, seen):
            self.text(f"{e.get('id')}.title", e.get("title"))
            self.html(f"{e.get('id')}.html", e.get("html"), imgs)
            self.text(f"{e.get('id')}.src", e.get("src"))
        for p in self.ids(f"{lid}.practice", d.get("practice"), lid, seen):
            self.exercise(p, imgs, practice=True)
        for x in self.ids(f"{lid}.exercises", d.get("exercises"), lid, seen):
            self.exercise(x, imgs)
        for f in self.ids(f"{lid}.flashcards", d.get("flashcards"), lid, seen):
            self.text(f"{f.get('id')}.front", f.get("front"))
            self.html(f"{f.get('id')}.back", f.get("back"), imgs)
        quiz = self.ids(f"{lid}.quiz", d.get("quiz"), lid, seen)
        for q in quiz:
            self.question(q, imgs)
        s = d.get("summary")
        if not isinstance(s, dict) or not isinstance(s.get("points"), list) or not s["points"]:
            self.err(lid, "summary.points phải là mảng không rỗng")
        else:
            self.html(f"{lid}.summary.html", s.get("html"), imgs)
        if quota:
            for k, n in QUOTA["small" if lid in SMALL else "big"].items():
                have = len(d.get(k) or [])
                if have < n:
                    self.err(lid, f"thiếu định mức {k}: có {have}, cần ≥ {n}")
            if quiz:
                tf = sum(q.get("type") == "tf" for q in quiz)
                if tf > 0.2 * len(quiz):
                    self.err(lid, f"câu tf {tf}/{len(quiz)} > 20%")
                all_of = sum(bool(re.search(r"tất cả (đều|các)", plain(" ".join(o.get("t", "") for o in q.get("options", [])
                                                                                    if isinstance(o, dict))))) for q in quiz)
                if all_of > 1:
                    self.err(lid, f"'tất cả đều…' dùng {all_of} lần (≤ 1)")

    def near_dupes(self, quiz):
        # so cả câu hỏi lẫn option: câu ngắn kiểu "X là viết tắt của gì?" chỉ khác nhau ở X
        items = [(q.get("id"), plain(q.get("q", "") + " " + " ".join(o.get("t", "") for o in q.get("options", [])
                                                                   if isinstance(o, dict))))
                 for q in quiz if isinstance(q.get("q"), str)]
        for i, (a, sa) in enumerate(items):
            for b, sb in items[i + 1:]:
                m = difflib.SequenceMatcher(None, sa, sb, autojunk=False)
                if m.real_quick_ratio() >= NEAR and m.quick_ratio() >= NEAR and m.ratio() >= NEAR:
                    self.err(f"{a} ~ {b}", "câu hỏi gần trùng")

    def course(self, c, lessons, strict=True):
        by_id = {d["id"]: d for d in lessons}
        qmod = {q["id"]: (MODULE_OF[d["id"]], q.get("level")) for d in lessons for q in d.get("quiz", [])}
        mods = c.get("modules")
        if not isinstance(mods, list):
            return self.err("course.modules", "phải là mảng")
        for m in mods:
            self.text(f"{m.get('id')}.title", m.get("title"))
            self.html(f"{m.get('id')}.summary_html", m.get("summary_html"), {})
            for lid in m.get("lessons", []):
                if MODULE_OF.get(lid) != m.get("id"):
                    self.err(m.get("id"), f"bài {lid} không thuộc module này")
        self.text("course.title", c.get("title"))
        self.html("course.intro_html", c.get("intro_html"), {})
        self.html("course.course_summary_html", c.get("course_summary_html"), {})
        gl = c.get("glossary", [])
        terms = set()
        for i, g in enumerate(gl):
            for k in ("term", "def"):
                self.text(f"glossary[{i}].{k}", g.get(k))
            if g.get("lesson") not in by_id:
                self.err(f"glossary[{i}]", f"lesson {g.get('lesson')!r} không có")
            t = (g.get("term") or "").strip().lower()
            if t in terms:
                self.err(f"glossary[{i}]", f"thuật ngữ trùng: {g.get('term')}")
            terms.add(t)
        seen = set(qmod)
        cs = c.get("case_study") or {}
        self.text("case_study.title", cs.get("title"))
        self.html("case_study.html", cs.get("html"), {})
        for x in self.ids("case_study.exercises", cs.get("exercises", []), "CS", seen):
            self.exercise(x, {})
        cq = self.ids("course.quiz", c.get("quiz", []), "C", seen)
        for q in cq:
            self.question(q, {})
            if q.get("module") not in set(MODULE_OF.values()):
                self.err(q.get("id"), "module không hợp lệ")
            qmod[q.get("id")] = (q.get("module"), q.get("level"))
        exams = c.get("exams", [])
        used = {}
        for e in exams:
            w = e.get("id", "?")
            qs = e.get("questions", [])
            if len(set(qs)) != len(qs):
                self.err(w, "câu trùng trong đề")
            for q in qs:
                if q not in qmod:
                    self.err(w, f"câu {q} không tồn tại")
                used[q] = used.get(q, 0) + 1
            if strict:
                if len(qs) != 40:
                    self.err(w, f"cần 40 câu (đang {len(qs)})")
                lv = sum(qmod.get(q, (0, 0))[1] == "apdung" for q in qs)
                if lv < 0.25 * len(qs):
                    self.err(w, f"câu apdung {lv} < 25%")
                for m in sorted(set(MODULE_OF.values())):
                    k = sum(qmod.get(q, (0,))[0] == m for q in qs)
                    if k < 3:
                        self.err(w, f"module {m} chỉ có {k} câu (≥ 3)")
        for q, n in used.items():
            if n > 2:
                self.err(q, f"xuất hiện trong {n} đề (≤ 2)")
        if strict:
            for what, have, need in (("exams", len(exams), 6), ("quiz C-q", len(cq), 120), ("glossary", len(gl), 120),
                                     ("case_study.exercises", len(cs.get("exercises", [])), 6)):
                if have < need:
                    self.err("course", f"thiếu {what}: có {have}, cần ≥ {need}")
        return cq


def img_path(p):
    if not isinstance(p, str) or not p:
        return None
    q = Path(p)
    return q if q.is_absolute() else ROOT / q


def encode_image(im):
    from PIL import Image
    with Image.open(img_path(im["path"])) as src:
        src = src.convert("RGB")
        if im.get("crop"):
            x0, y0, x1, y1 = im["crop"]
            w, h = src.size
            src = src.crop((round(x0 * w), round(y0 * h), round(x1 * w), round(y1 * h)))
        src.thumbnail((1200, 1200))
        buf = io.BytesIO()
        src.save(buf, "WEBP", quality=80)
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()


def fonts_css():
    """@font-face từ data/fonts/fonts.css (fetch_fonts.py), file woff2 nhúng base64 để chạy offline."""
    d = ROOT / "data" / "fonts"
    if not (d / "fonts.css").exists():
        return ""
    return re.sub(r"url\(([^)]+\.woff2)\)", lambda m: "url(data:font/woff2;base64,"
                  + base64.b64encode((d / m.group(1)).read_bytes()).decode() + ")", (d / "fonts.css").read_text(encoding="utf-8"))


def place_images(obj, caps):
    """Đổi {{img:id}} thành <figure> trong mọi chuỗi."""
    def fig(m):
        cap = html.escape(caps.get(m.group(1), ""))
        return f'<figure><img data-img="{m.group(1)}" alt="{cap}"><figcaption>{cap}</figcaption></figure>'
    if isinstance(obj, str):
        return IMG_RE.sub(fig, obj)
    if isinstance(obj, list):
        return [place_images(v, caps) for v in obj]
    if isinstance(obj, dict):
        return {k: place_images(v, caps) for k, v in obj.items()}
    return obj


def load(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        sys.exit(f"{p}: không đọc được JSON: {e}")


def render(course, lessons, out):
    images = {}
    for d in lessons:
        for im in d.get("images", []):
            images[im["id"]] = encode_image(im)
    caps = {im["id"]: im.get("caption", "") for d in lessons for im in d.get("images", [])}
    data = {"course": course, "lessons": place_images(lessons, caps), "images": images}
    blob = (json.dumps(data, ensure_ascii=False, separators=(",", ":"))
            .replace("</", "<\\/").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029"))
    tpl = TEMPLATE.read_text(encoding="utf-8")
    if tpl.count("__COURSE_DATA__") != 1:
        sys.exit("template.html phải chứa đúng 1 chỗ __COURSE_DATA__")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(tpl.replace("/*__FONTS__*/", fonts_css()).replace("__COURSE_DATA__", blob), encoding="utf-8")
    print(f"→ {out} ({out.stat().st_size / 1e6:.1f} MB, {len(lessons)} bài, {len(images)} ảnh)")


def attach_listen(c, lessons):
    """Gắn phần "Nghe giảng" (kịch bản + mốc thời gian) vào bài; MP3 để ngoài, HTML trỏ ../data/audio/."""
    import narrate
    n = 0
    for d in lessons:
        lid = d["id"]
        if not (NARR_DIR / f"{lid}.json").exists():
            continue
        errs = narrate.check(lid)
        for e in errs:
            c.err("data/narration", e)
        tp, mp = AUDIO_DIR / f"{lid}.json", AUDIO_DIR / f"{lid}.mp3"
        if errs:
            continue
        s = load(NARR_DIR / f"{lid}.json")
        if not tp.exists() or not mp.exists() or load(tp).get("hash") != narrate.digest(s):
            c.err(f"data/narration/{lid}.json", f"audio chưa sinh hoặc đã cũ: chạy python -B script/narrate.py {lid}")
            continue
        t = load(tp)
        tm = {x["id"]: x for x in t["chunks"]}
        d["listen"] = {"src": f"../data/audio/{lid}.mp3", "dur": t["duration"], "chunks": [
            {"id": x["id"], "start": tm[x["id"]]["start"], "end": tm[x["id"]]["end"], "h": x["show"]["h"],
             "points": x["show"]["points"], "img": x["show"].get("img"), "ref": x.get("ref"), "ask": x.get("ask", []),
             "sents": tm[x["id"]]["sents"]} for x in s["chunks"]]}
        n += 1
    return n


def attach_exercises(c, lessons, course=None):
    """Gắn cách làm tương tác (data/exercises/<ID>.json) vào bài tập; trả số bài tập được gắn."""
    import exercises as ex
    n = 0
    targets = [(d["id"], d.get("exercises") or []) for d in lessons]
    if course:
        targets.append(("CS", (course.get("case_study") or {}).get("exercises") or []))
    for lid, arr in targets:
        if not (ex.EX_DIR / f"{lid}.json").exists():
            continue
        errs = ex.check(lid)
        for e in errs:
            c.err("data/exercises", e)
        if not errs:
            n += ex.attach(lid, arr)
    return n


def report(c, ok_msg="OK"):
    if c.errors:
        print(f"{len(c.errors)} lỗi:")
        for e in c.errors[:200]:
            print("  -", e)
        if len(c.errors) > 200:
            print(f"  … và {len(c.errors) - 200} lỗi nữa")
        return 1
    print(ok_msg)
    return 0


def check_one(path):
    d = load(path)
    c = Checker()
    c.lesson(d)
    c.near_dupes(d.get("quiz") or [])
    return report(c)


def preview():
    """Build tạm khi course.json chưa xong: đủ bài, phần khóa học tối giản, chưa có đề thi."""
    lessons = [load(LESSONS_DIR / f"{lid}.json") for lid in ORDER if (LESSONS_DIR / f"{lid}.json").exists()]
    c = Checker()
    for d in lessons:
        c.lesson(d, quota=False)
    attach_listen(c, lessons)
    attach_exercises(c, lessons)
    if report(c, f"{len(lessons)} bài OK"):
        return 1
    course = {"title": "IT Business Analyst – Khóa học tương tác (bản xem trước)",
              "intro_html": "<p>Bản xem trước: đủ bài học, chưa có tổng kết khóa, thuật ngữ và đề thi.</p>",
              "modules": [{"id": m, "title": t, "lessons": [l for l in ORDER if MODULE_OF[l] == m], "summary_html": "<p>Đang soạn.</p>"}
                          for m, t in [("M1", "Nền tảng BA và IT"), ("M2", "Dự án và yêu cầu"), ("M3", "Phân tích yêu cầu"),
                                       ("M4", "Mô hình hóa"), ("M5", "Tài liệu BA"), ("M6", "Dữ liệu và tích hợp")]],
              "course_summary_html": "<p>Đang soạn.</p>", "glossary": [],
              "case_study": {"title": "SolasMart", "html": "<p>Đang soạn.</p>", "exercises": []}, "quiz": [], "exams": []}
    render(course, lessons, OUT)
    return 0


def build():
    lessons = [load(LESSONS_DIR / f"{lid}.json") for lid in ORDER if (LESSONS_DIR / f"{lid}.json").exists()]
    missing = [lid for lid in ORDER if not (LESSONS_DIR / f"{lid}.json").exists()]
    c = Checker()
    if missing:
        c.err("data/lessons", f"thiếu bài: {', '.join(missing)}")
    seen = set()
    for d in lessons:
        c.lesson(d, seen=seen)
    course = load(COURSE) if COURSE.exists() else None
    if course is None:
        c.err("data/course/course.json", "chưa có")
        cq = []
    else:
        cq = c.course(course, lessons) or []
    c.near_dupes([q for d in lessons for q in d.get("quiz") or []] + cq)
    n_listen = attach_listen(c, lessons)
    n_ex = attach_exercises(c, lessons, course)
    if report(c, f"Dữ liệu OK ({n_listen} bài có Nghe giảng, {n_ex} bài tập tương tác)"):
        return 1
    render(course, lessons, OUT)
    return 0


# ---------- dữ liệu mẫu (demo + selftest) ----------

def _q(lid, n, t, level, stem):
    if t == "tf":
        return {"id": f"{lid}-q{n}", "type": "tf", "level": level, "q": f"<p>{stem}</p>", "options": copy.deepcopy(TF),
                "answer": ["d"], "explain": "<p>Đúng theo slide.</p>", "why_wrong": {"s": "Slide nói ngược lại."}, "src": "mẫu tr.1"}
    opts = [{"id": k, "t": f"Phương án {k.upper()} cho câu {n}"} for k in "abcd"]
    ans = ["a", "c"] if t == "multi" else ["b"]
    return {"id": f"{lid}-q{n}", "type": t, "level": level, "q": f"<p>{stem}</p>", "options": opts, "answer": ans,
            "explain": "<p>Giải thích vì sao đúng.</p>", "why_wrong": {k: f"Vì sao {k} sai." for k in "abcd" if k not in ans},
            "src": "mẫu tr.2"}


TOPICS = ["Stakeholder", "Need", "Change", "Solution", "Value", "Context", "Use case", "Actor", "BPMN gateway", "ERD",
          "Khóa chính", "Khóa ngoại", "MoSCoW", "RTM", "API", "REST", "Wireframe", "BRD", "SRS", "FSD"]


def sample_lesson(lid):
    img = next((ROOT / "data" / "pages").glob("*/p-001.jpg"), None)
    imgs = [{"id": f"{lid}-img1", "path": str(img.relative_to(ROOT)).replace("\\", "/"), "caption": "Ảnh mẫu",
             "crop": [0, 0, 1, 0.6]}] if img else []
    fig = f"{{{{img:{lid}-img1}}}}" if img else ""
    levels = ["nho", "hieu", "apdung"]
    types = ["single", "single", "multi", "single", "tf"]
    stems = ["Ai là người hưởng lợi trực tiếp từ dự án?", "Khái niệm nào mô tả vấn đề cần giải quyết?",
             "Chọn các tài liệu BA viết ở giai đoạn phân tích.", "Ký hiệu hình thoi trong BPMN nghĩa là gì?",
             "Khóa chính có thể nhận giá trị NULL.", "Khi khách hàng đổi yêu cầu giữa sprint, BA làm gì đầu tiên?",
             "Phương thức HTTP nào dùng để tạo mới tài nguyên?", "Ma trận truy vết giúp trả lời câu hỏi nào?",
             "Chọn các kỹ thuật khai thác yêu cầu phù hợp với 500 người dùng.", "Thứ tự ưu tiên MoSCoW bắt đầu bằng mức nào?",
             "Use case diagram thể hiện luồng xử lý chi tiết từng bước.", "Wireframe khác mockup ở điểm nào?"]
    quiz = [_q(lid, i + 1, types[i % 5], levels[i % 3], f"{stems[i]} ({lid})") for i in range(12)]
    ex = lambda k, n, lvl=None: dict({"id": f"{lid}-{k}{n}", "title": f"Bài {n}", "task": "<p>Đề bài <b>mẫu</b>.</p>",
                                     "answer": "<ul><li>Ý 1</li><li>Ý 2</li></ul>", "src": "mẫu tr.3"},
                                    **({"hints": ["<p>Gợi ý 1</p>", "<p>Gợi ý 2</p>"], "level": lvl} if lvl else
                                       {"steps": ["<p>Bước 1</p>", "<p>Bước 2</p>"]}))
    return {"id": lid, "session": int(re.sub(r"\D", "", lid)), "module": MODULE_OF[lid], "title": f"Bài mẫu {lid}",
            "goals": ["Mục tiêu 1", "Mục tiêu 2"], "sources": [{"file": "mẫu.pdf", "pages": "1-3"}],
            "theory": [{"id": f"{lid}-t1", "h": "Khái niệm", "html": f"<p>Lý thuyết <b>mẫu</b>.</p>{fig}"
                        "<table><tr><th>A</th><th>B</th></tr><tr><td colspan=\"2\">gộp</td></tr></table>", "src": "mẫu tr.1"},
                       {"id": f"{lid}-t2", "h": "Chi tiết", "html": "<p class=\"note\">Ghi chú.</p><ul><li>x</li></ul>", "src": "mẫu tr.2"}],
            "examples": [{"id": f"{lid}-e1", "title": "Ví dụ", "html": "<p>Ví dụ.</p>", "src": "mẫu tr.2"}],
            "practice": [ex("p", 1)], "exercises": [ex("x", 1, "de"), ex("x", 2, "kho")],
            "flashcards": [{"id": f"{lid}-f{i}", "front": TOPICS[i], "back": f"<p>Định nghĩa {TOPICS[i]}.</p>"} for i in range(5)],
            "quiz": quiz, "summary": {"points": ["Ý chính 1", "Ý chính 2"], "html": "<p>Tổng kết.</p>"}, "images": imgs}


def sample_course(lessons):
    cq = [dict(_q("C", i + 1, "single", "apdung", f"Tình huống SolasMart {i + 1}: cửa hàng {TOPICS[i]} cần làm gì trước tiên?"),
               module="M2", lessons=["L07"]) for i in range(4)]
    return {"title": "IT Business Analyst – Khóa học tương tác (DEMO)", "intro_html": "<p>Giới thiệu.</p>",
            "modules": [{"id": m, "title": f"Module {m}", "lessons": [l for l in ORDER if MODULE_OF[l] == m],
                         "summary_html": "<p>Tổng kết module.</p>"} for m in dict.fromkeys(MODULE_OF.values())],
            "course_summary_html": "<h4>Tổng kết</h4><p>Toàn khóa.</p>",
            "glossary": [{"term": t, "vi": "nghĩa", "def": f"Định nghĩa {t}.", "lesson": lessons[i % len(lessons)]["id"]}
                         for i, t in enumerate(TOPICS)],
            "case_study": {"title": "SolasMart", "html": "<p>Bối cảnh.</p>",
                           "exercises": [{"id": "CS-x1", "title": "Bài case", "level": "kho", "task": "<p>Đề.</p>",
                                          "hints": ["<p>Gợi ý</p>"], "answer": "<p>Đáp án.</p>", "src": "SolasMart"}]},
            "quiz": cq,
            "exams": [{"id": "D1", "title": "Đề 1 (demo)", "minutes": 10,
                       "questions": [q["id"] for d in lessons for q in d["quiz"][:4]] + [q["id"] for q in cq]}]}


def demo():
    lessons = [sample_lesson(l) for l in ("L07", "L12")]
    c = Checker()
    for d in lessons:
        c.lesson(d, quota=False)
    c.course(sample_course(lessons), lessons, strict=False)
    if report(c, "demo data OK"):
        return 1
    render(sample_course(lessons), lessons, ROOT / "data" / "course" / "demo.html")
    return 0


def selftest():
    base = sample_lesson("L07")
    c = Checker()
    c.lesson(base, quota=False)
    c.near_dupes(base["quiz"])
    assert not c.errors, c.errors

    def bad(mutate, expect, quota=False):
        d = copy.deepcopy(base)
        mutate(d)
        c = Checker()
        c.lesson(d, quota=quota)
        c.near_dupes(d["quiz"])
        hit = [e for e in c.errors if expect in e]
        assert hit, f"không bắt được '{expect}': {c.errors}"

    bad(lambda d: d["quiz"][1].update(id=d["quiz"][0]["id"]), "id trùng")
    bad(lambda d: d["quiz"][0].update(answer=["z"]), "không khớp option")
    bad(lambda d: d["quiz"][0]["why_wrong"].pop("a"), "why_wrong")
    bad(lambda d: d["quiz"][4].update(options=[{"id": "d", "t": "Đúng"}, {"id": "s", "t": "sai"}]), "tf: options")
    bad(lambda d: d["theory"][0].update(html="<p style='x'>a</p><script>x</script>"), "HTML không cho phép")
    bad(lambda d: d["images"][0].update(path="khong/co.jpg") if d["images"] else d["theory"][0].update(html="{{img:L07-zz}}"),
        "ảnh không tồn tại" if base["images"] else "chưa khai báo")
    bad(lambda d: d["quiz"][1].update(q=d["quiz"][0]["q"].replace("Câu 1", "Câu  1")), "gần trùng")
    bad(lambda d: None, "thiếu định mức", quota=True)
    print("selftest PASS")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    if a[:1] == ["--check"] and len(a) == 2:
        sys.exit(check_one(a[1]))
    sys.exit({"--demo": demo, "--selftest": selftest, "--preview": preview}.get(a[0] if a else "", build)())
