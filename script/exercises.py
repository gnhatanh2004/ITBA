"""Bài tập tương tác (kéo thả, sắp xếp, trắc nghiệm) cho tab Bài tập – dữ liệu ở data/exercises/<ID>.json.

  python -B script/exercises.py --check L01   kiểm 1 file (agent tự chạy tới khi in OK)
  python -B script/exercises.py --check       kiểm mọi file đang có

File gắn thêm cách làm cho bài tập đã có (không sửa data/lessons). Schema: docs/prompt.md §8.
  {"lesson": "L01", "items": {"L01-x1": {...}, "L01-p1": {"lead": "...", "parts": [part, ...]}}}  (x = bài tập, p = thực hành)
  part kéo thả vào nhóm / ghép cặp: {"kind": "sort", "q": "...", "bins": [nhãn...], "items": [{"t": "...", "a": [chỉ số bin đúng...], "why": "..."}]}
  part sắp xếp thứ tự:              {"kind": "order", "q": "...", "items": [mục theo ĐÚNG thứ tự...], "why": "..."}
  part trắc nghiệm:                 {"kind": "choice", "q": "...", "options": [...], "answer": [chỉ số đúng...], "multi": false, "why": "..."}
Mọi chuỗi là văn bản thường (giao diện tự escape), được xuống dòng bằng \\n.
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EX_DIR, LESSONS_DIR, COURSE = ROOT / "data" / "exercises", ROOT / "data" / "lessons", ROOT / "data" / "course" / "course.json"
KINDS = {"sort", "order", "choice"}


def _load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def exercise_ids(lid, kinds=("exercises", "practice")):
    """id bài tập + bài thực hành gốc của bài (CS = case study trong course.json, chỉ có bài tập)."""
    if lid == "CS":
        return [x["id"] for x in _load(COURSE)["case_study"]["exercises"]] if "exercises" in kinds else []
    p = LESSONS_DIR / f"{lid}.json"
    if not p.exists():
        return []
    d = _load(p)
    return [x["id"] for k in kinds for x in d.get(k, [])]


def _s(v, n=600):
    return isinstance(v, str) and v.strip() and len(v) <= n


def check_part(w, p):
    e = []
    if not isinstance(p, dict) or p.get("kind") not in KINDS:
        return [f"{w}: kind phải là sort|order|choice"]
    k = p["kind"]
    if not _s(p.get("q"), 900):
        e.append(f"{w}.q rỗng hoặc dài quá 900 ký tự")
    if "why" in p and not _s(p["why"], 1500):
        e.append(f"{w}.why rỗng hoặc dài quá 1500 ký tự")
    if k == "sort":
        bins, items = p.get("bins"), p.get("items")
        if not isinstance(bins, list) or not 2 <= len(bins) <= 8 or not all(_s(b, 120) for b in bins) or len(set(bins)) != len(bins):
            e.append(f"{w}.bins: 2–8 nhãn, không trùng, mỗi nhãn ≤ 120 ký tự")
            bins = []
        if not isinstance(items, list) or not 2 <= len(items) <= 16:
            return e + [f"{w}.items: 2–16 mục"]
        ts = []
        for i, it in enumerate(items):
            wi = f"{w}.items[{i}]"
            if not isinstance(it, dict) or not _s(it.get("t"), 400):
                e.append(f"{wi}.t rỗng hoặc dài quá 400 ký tự"); continue
            ts.append(it["t"])
            a = it.get("a")
            if not isinstance(a, list) or not a or len(set(a)) != len(a) or not all(isinstance(x, int) and 0 <= x < len(bins) for x in a):
                e.append(f"{wi}.a phải là mảng chỉ số bin hợp lệ (0..{len(bins) - 1}), không rỗng, không trùng")
            if "why" in it and not _s(it["why"], 600):
                e.append(f"{wi}.why rỗng hoặc dài quá 600 ký tự")
        if len(set(ts)) != len(ts):
            e.append(f"{w}.items có mục trùng chữ")
        if bins and items and all(isinstance(it, dict) and it.get("a") == [0] for it in items) and len(bins) > 1:
            e.append(f"{w}: mọi mục đều thuộc bin 0 – kiểm lại đáp án")
    elif k == "order":
        items = p.get("items")
        if not isinstance(items, list) or not 3 <= len(items) <= 10 or not all(_s(x, 300) for x in items):
            e.append(f"{w}.items: 3–10 chuỗi theo đúng thứ tự, mỗi chuỗi ≤ 300 ký tự")
        elif len(set(items)) != len(items):
            e.append(f"{w}.items có mục trùng chữ")
    else:
        opts, ans = p.get("options"), p.get("answer")
        if not isinstance(opts, list) or not 2 <= len(opts) <= 8 or not all(_s(o, 500) for o in opts):
            return e + [f"{w}.options: 2–8 chuỗi, mỗi chuỗi ≤ 500 ký tự"]
        if len(set(opts)) != len(opts):
            e.append(f"{w}.options có phương án trùng chữ")
        if not isinstance(ans, list) or not ans or len(set(ans)) != len(ans) or not all(isinstance(x, int) and 0 <= x < len(opts) for x in ans):
            e.append(f"{w}.answer phải là mảng chỉ số đúng (0..{len(opts) - 1}), không rỗng")
        elif not isinstance(p.get("multi"), bool):
            e.append(f"{w}.multi phải là true/false")
        elif not p["multi"] and len(ans) != 1:
            e.append(f"{w}: multi=false thì answer có đúng 1 chỉ số")
        elif p["multi"] and len(ans) == len(opts):
            e.append(f"{w}: mọi phương án đều đúng – thêm phương án sai")
        if not _s(p.get("why"), 1500):
            e.append(f"{w}.why (giải thích) bắt buộc với choice")
    return e


def check(lid):
    p = EX_DIR / f"{lid}.json"
    if not p.exists():
        return [f"{p}: chưa có"]
    try:
        d = _load(p)
    except Exception as ex:
        return [f"{p}: JSON lỗi – {ex}"]
    w0 = f"exercises/{lid}"
    if d.get("lesson") != lid or not isinstance(d.get("items"), dict):
        return [f"{w0}: cần {{\"lesson\": \"{lid}\", \"items\": {{...}}}}"]
    ids, e = set(exercise_ids(lid)), []
    for xid, x in d["items"].items():
        w = f"{w0}:{xid}"
        if xid not in ids:
            e.append(f"{w}: không có bài tập / bài thực hành id này trong bài {lid}"); continue
        if not isinstance(x, dict):
            e.append(f"{w}: phải là object"); continue
        if "lead" in x and not _s(x["lead"], 400):
            e.append(f"{w}.lead rỗng hoặc dài quá 400 ký tự")
        parts = x.get("parts")
        if not isinstance(parts, list) or not 1 <= len(parts) <= 6:
            e.append(f"{w}.parts: 1–6 phần"); continue
        for i, pt in enumerate(parts):
            e += check_part(f"{w}.parts[{i}]", pt)
    return e


def attach(lid, exercises):
    """Gắn x['auto'] vào danh sách bài tập; trả số bài được gắn."""
    p = EX_DIR / f"{lid}.json"
    if not p.exists():
        return 0
    items = _load(p)["items"]
    n = 0
    for x in exercises:
        if x["id"] in items:
            x["auto"] = items[x["id"]]; n += 1
    return n


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    if a[:1] != ["--check"]:
        sys.exit(__doc__)
    lids = a[1:] or sorted(p.stem for p in EX_DIR.glob("*.json"))
    bad = 0
    for lid in lids:
        errs = check(lid)
        if errs:
            bad = 1
            print(f"{lid}: {len(errs)} lỗi"); [print("  -", x) for x in errs[:80]]
        else:
            d = _load(EX_DIR / f"{lid}.json")["items"]
            ex_ids, pr_ids = exercise_ids(lid, ("exercises",)), exercise_ids(lid, ("practice",))
            n_ex, n_pr = sum(i in d for i in ex_ids), sum(i in d for i in pr_ids)
            print(f"{lid}: OK (bài tập {n_ex}/{len(ex_ids)}" + (f", thực hành {n_pr}/{len(pr_ids)}" if pr_ids else "") + " có cách làm tương tác)")
    sys.exit(bad)
