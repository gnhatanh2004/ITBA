"""Sinh giọng đọc "Nghe giảng" từ data/narration/Lxx.json ra data/audio/Lxx.mp3 + Lxx.json (mốc thời gian).

python -B script/narrate.py                 sinh cho mọi bài có kịch bản (bỏ qua bài không đổi)
python -B script/narrate.py L01 L02         chỉ các bài này
python -B script/narrate.py --check [L01]   chỉ kiểm kịch bản, không gọi TTS
python -B script/narrate.py --force L01     sinh lại dù kịch bản không đổi
"""
import asyncio
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NARR = ROOT / "data" / "narration"
AUDIO = ROOT / "data" / "audio"
LESSONS = ROOT / "data" / "lessons"
VOICE = "vi-VN-NamMinhNeural"
BPS = 6000  # edge-tts trả MP3 CBR 48 kbps mono → 6000 byte/giây
GAP = 0.6   # khoảng lặng giữa hai đoạn (giây)
LIMITS = dict(say=1400, h=90, point=140, points=5, ask=3)
# kịch bản giữ chữ gốc (phụ đề hiện chữ gốc); giọng Việt đọc chữ viết tắt theo phiên âm dưới đây
PRON = {"IIBA": "ai ai bi ây", "BABOK": "ba-bốc", "CBAP": "xi báp", "CCBA": "xi xi bi ây", "CC": "xi xi", "ECBA": "i xi bi ây",
        "BACCM": "bi ây xi xi em", "BA": "bi ây", "BAs": "bi ây", "IT": "ai ti", "BRD": "bi a đê", "SRS": "ét a ét",
        "FSD": "ép ét đê", "URD": "diu a đê", "UML": "du em eo", "BPMN": "bi pi em en", "ERD": "i a đê", "DFD": "đi ép đi",
        "API": "ây pi ai", "SQL": "ét kiu eo", "UI": "giu ai", "UX": "giu ích", "RTM": "a ti em", "SOW": "ét âu đáp liu",
        "MVP": "em vi pi", "KPI": "kây pi ai", "CEO": "xi i âu", "CIO": "xi ai âu", "CTO": "xi ti âu", "COO": "xi âu âu",
        "QA": "kiu ây", "PM": "pi em", "PO": "pi âu", "REST": "rét", "JSON": "giây sơn", "XML": "ích em eo",
        "HTTP": "ếch ti ti pi", "CRUD": "cờ rút", "SDLC": "ét đi eo xi", "MoSCoW": "mát-cô", "SWOT": "xoát",
        "PESTLE": "pét-tồ", "SMART": "xờ-mát", "ERP": "i a pi", "CRM": "xi a em", "POS": "pi âu ét",
        "GAP": "gáp", "SEO": "ét i âu", "OOA": "âu âu ây", "SMS": "ét em ét", "HR": "ếch a", "NFR": "en ép a",
        "FR": "ép a", "UC": "diu xi", "ID": "ai đi", "COD": "xi âu đi", "BFD": "bi ép đi", "ISO": "i-xô",
        "HRM": "ếch a em", "ATM": "ây ti em", "BR": "bi a", "RACI": "ra-xi", "RADD": "a ây đi đi", "UAT": "diu ây ti",
        "AS-IS": "e-dờ i-dờ", "As-Is": "e-dờ i-dờ", "As-is": "e-dờ i-dờ", "To-Be": "tu-bi", "To-be": "tu-bi",
        "CMND": "chứng minh nhân dân", "HĐCCH": "hát đê xê xê hát", "PNK": "pê en ca", "HĐBL": "hát đê bê e lờ",
        "DBMS": "đi bi em ét", "NoSQL": "nâu ét kiu eo", "MySQL": "mai ét kiu eo", "SQLite": "ét kiu eo lai",
        "PostgreSQL": "pốt-gờ-rét ét kiu eo", "1NF": "một en ép", "2NF": "hai en ép", "3NF": "ba en ép",
        "BCNF": "bi xi en ép", "NULL": "nân", "AVG": "a-vơ-rịt", "QC": "kiu xi", "CR": "xi a", "OTP": "âu ti pi",
        "IP": "ai pi", "IPv4": "ai pi vi bốn", "IPv6": "ai pi vi sáu", "ISP": "ai ét pi", "DNS": "đi en ét",
        "DHCP": "đi ếch xi pi", "DMZ": "đi em dét", "LAN": "lan", "FE": "ép i", "DB": "đi bi", "HIS": "ếch ai ét",
        "LIS": "eo ai ét", "RIS": "a ai ét", "PACS": "pác", "EMR": "i em a", "AI": "ây ai", "CMS": "xi em ét",
        "HTML": "ếch ti em eo", "CSS": "xi ét ét", "VNPT": "vê en pê tê", "FPT": "ép pê tê", "CMC": "xê em xê",
        "URL": "diu a eo", "SSL": "ét ét eo", "TLS": "ti eo ét", "OSI": "âu ét ai", "TCP": "ti xi pi", "SOAP": "sốp",
        "HTTPS": "ếch ti ti pi ét", "RESTful": "rét-phun", "GraphQL": "gráp kiu eo", "FRS": "ép a ét",
        "FS": "ép ét", "PS": "pi ét", "QR": "kiu a"}
# cho phép số dính liền sau chữ viết tắt (UC1.0), chỉ chặn chữ cái và gạch nối
_PRON_RE = re.compile(r"(?<![\w-])(" + "|".join(sorted(map(re.escape, PRON), key=len, reverse=True)) + r")(?![^\W\d_]|-)")


def speakable(text, voice):
    """Câu đưa vào TTS: giọng Việt thì đổi chữ viết tắt sang phiên âm, giọng đa ngôn ngữ giữ nguyên."""
    return _PRON_RE.sub(lambda m: PRON[m.group(1)], text) if voice.startswith("vi-") else text


def captions(say, sents, voice):
    """Phụ đề bằng câu gốc [[đầu, cuối, câu]]. Số câu khớp TTS thì lấy mốc TTS,
    không khớp thì nội suy mốc theo độ dài chữ đọc trên dòng thời gian TTS."""
    parts = [s for s in re.split(r"(?<=[.?!…])\s+", say.strip()) if s]
    if len(parts) == len(sents):
        return [[a, b, p] for (a, b, _), p in zip(sents, parts)]
    knots, c = [], 0
    for a, b, t in sents:
        knots += [(c, a), (c + len(t), b)]; c += len(t)

    def at(x):
        for (c0, t0), (c1, t1) in zip(knots, knots[1:]):
            if x <= c1:
                return t0 if c1 == c0 else t0 + (t1 - t0) * (x - c0) / (c1 - c0)
        return knots[-1][1]
    lens = [len(speakable(p, voice)) for p in parts]
    k, out, pos = c / max(1, sum(lens)), [], 0
    for p, n in zip(parts, lens):
        out.append([at(pos * k), at((pos + n) * k), p]); pos += n
    return out

sys.stdout.reconfigure(encoding="utf-8")


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def check(lid):
    """Trả về danh sách lỗi của kịch bản một bài."""
    errs, p = [], NARR / f"{lid}.json"
    if not p.exists():
        return [f"{lid}: chưa có {p.relative_to(ROOT)}"]
    try:
        d, les = load(p), load(LESSONS / f"{lid}.json")
    except (ValueError, OSError) as e:
        return [f"{lid}: không đọc được JSON ({e})"]
    e = lambda where, msg: errs.append(f"{where}: {msg}")
    if d.get("lesson") != lid:
        e(lid, f"'lesson' phải là {lid}")
    quiz = {q["id"] for q in les.get("quiz", [])}
    imgs = {i["id"] for i in les.get("images", [])}
    refs = {x["id"] for k in ("theory", "examples", "practice") for x in les.get(k, [])}
    chunks, seen, asked = d.get("chunks"), set(), set()
    if not isinstance(chunks, list) or not chunks:
        return errs + [f"{lid}: 'chunks' phải là mảng khác rỗng"]
    for i, c in enumerate(chunks):
        cid = c.get("id") if isinstance(c, dict) else None
        w = f"{lid} chunk #{i + 1}" + (f" ({cid})" if cid else "")
        if not isinstance(c, dict):
            e(w, "phải là object"); continue
        if not isinstance(cid, str) or not re.fullmatch(rf"{lid}-n\d+", cid):
            e(w, f"id phải dạng {lid}-n<số>")
        elif cid in seen:
            e(w, "id trùng")
        seen.add(cid)
        say = c.get("say")
        if not isinstance(say, str) or len(say.strip()) < 20:
            e(w, "'say' thiếu hoặc quá ngắn")
        else:
            if re.search(r"[<>{}]|&\w+;", say):
                e(w, "'say' không được chứa HTML, {{...}} hay ký tự < > { }")
            if len(say) > LIMITS["say"]:
                e(w, f"'say' dài {len(say)} ký tự (tối đa {LIMITS['say']}), tách thành chunk khác")
        show = c.get("show")
        if not isinstance(show, dict):
            e(w, "thiếu 'show'"); show = {}
        h, pts = show.get("h"), show.get("points", [])
        if not isinstance(h, str) or not h.strip() or len(h) > LIMITS["h"]:
            e(w, f"'show.h' phải là chuỗi 1–{LIMITS['h']} ký tự")
        if not isinstance(pts, list) or not 1 <= len(pts) <= LIMITS["points"] or \
                not all(isinstance(x, str) and x.strip() and len(x) <= LIMITS["point"] for x in pts):
            e(w, f"'show.points' phải là 1–{LIMITS['points']} chuỗi, mỗi chuỗi ≤ {LIMITS['point']} ký tự")
        elif any(re.search(r"[<>]", x) for x in pts):
            e(w, "'show.points' không được chứa HTML")
        if show.get("img") is not None and show["img"] not in imgs:
            e(w, f"ảnh '{show['img']}' không có trong images của bài")
        if c.get("ref") is not None and c["ref"] not in refs:
            e(w, f"ref '{c['ref']}' không phải id theory/examples/practice của bài")
        ask = c.get("ask", [])
        if not isinstance(ask, list) or len(ask) > LIMITS["ask"]:
            e(w, f"'ask' phải là mảng 0–{LIMITS['ask']} id")
            continue
        for q in ask:
            if q not in quiz:
                e(w, f"câu '{q}' không có trong quiz của bài")
            elif q in asked:
                e(w, f"câu '{q}' đã hỏi ở chunk trước")
            asked.add(q)
    return errs


def digest(d):
    v = d.get("voice", VOICE)
    return hashlib.sha1(json.dumps([v, GAP] + [speakable(c["say"], v) for c in d["chunks"]],
                                   ensure_ascii=False).encode()).hexdigest()[:16]


def silence(header, seconds):
    """Khung MP3 rỗng (side info = 0) cùng định dạng → khoảng lặng, không cần ffmpeg."""
    h = bytearray(header[:4]); h[2] &= ~0x02  # tắt padding bit
    frame = bytes(h) + bytes(144 - 4)          # 72 * 48000 / 24000 = 144 byte/khung, 24 ms
    return frame * round(seconds / 0.024)


async def tts(text, voice):
    import edge_tts
    audio, sents = bytearray(), []
    async for ch in edge_tts.Communicate(text, voice).stream():
        if ch["type"] == "audio":
            audio += ch["data"]
        elif ch["type"] in ("SentenceBoundary", "WordBoundary"):
            sents.append([ch["offset"] / 1e7, (ch["offset"] + ch["duration"]) / 1e7, ch["text"]])
    if not audio or audio[:2] != b"\xff\xf3" or audio[2] >> 4 != 0x6:
        raise RuntimeError("edge-tts trả về định dạng khác MP3 48 kbps; cần sửa BPS/silence()")
    return bytes(audio), sents


async def generate(lid, force=False):
    d = load(NARR / f"{lid}.json")
    out_json, out_mp3, h = AUDIO / f"{lid}.json", AUDIO / f"{lid}.mp3", digest(d)
    if not force and out_json.exists() and out_mp3.exists() and load(out_json).get("hash") == h:
        print(f"{lid}: không đổi, bỏ qua"); return
    voice, buf, chunks, gap, sem = d.get("voice", VOICE), bytearray(), [], b"", asyncio.Semaphore(2)

    async def one(c):
        async with sem:
            for attempt in range(12):
                try:
                    return await tts(speakable(c["say"], voice), voice)
                except Exception as ex:  # dịch vụ edge-tts hay trả rỗng ngẫu nhiên: thử lại, giãn dần
                    if attempt == 11:
                        raise
                    print(f"  {c['id']}: {type(ex).__name__}, thử lại lần {attempt + 2}"); await asyncio.sleep(min(20, 2 + 3 * attempt))

    results = await asyncio.gather(*(one(c) for c in d["chunks"]))
    for i, (c, (audio, sents)) in enumerate(zip(d["chunks"], results)):
        if i:
            buf += gap
        gap = gap or silence(audio, GAP)
        start = len(buf) / BPS
        buf += audio
        chunks.append({"id": c["id"], "start": round(start, 3), "end": round(len(buf) / BPS, 3),
                       "sents": [[round(start + a, 3), round(start + b, 3), t]
                                 for a, b, t in captions(c["say"], sents, voice)]})
        print(f"  {c['id']}: {len(audio) / BPS:5.1f}s")
    AUDIO.mkdir(parents=True, exist_ok=True)
    out_mp3.write_bytes(bytes(buf))
    out_json.write_text(json.dumps({"lesson": lid, "voice": voice, "hash": h, "duration": round(len(buf) / BPS, 3),
                                    "chunks": chunks}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{lid}: {len(buf) / BPS / 60:.1f} phút, {len(buf) / 1e6:.1f} MB → {out_mp3.relative_to(ROOT)}")


def main(argv):
    only_check, force = "--check" in argv, "--force" in argv
    ids = [a for a in argv if not a.startswith("--")] or sorted(p.stem for p in NARR.glob("L*.json"))
    if not ids:
        print("Chưa có kịch bản nào trong data/narration/"); return 1
    bad = 0
    for lid in ids:
        errs = check(lid)
        if errs:
            bad += 1
            print(f"{lid}: {len(errs)} lỗi"); [print("  -", x) for x in errs]
        elif only_check:
            d = load(NARR / f"{lid}.json")
            n_ask = sum(1 for c in d["chunks"] if c.get("ask"))
            words = sum(len(c["say"].split()) for c in d["chunks"])
            print(f"{lid}: OK ({len(d['chunks'])} đoạn, {n_ask} điểm hỏi, ~{words / 150:.0f} phút nghe)")
    if bad or only_check:
        return 1 if bad else 0
    for lid in ids:
        asyncio.run(generate(lid, force))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
