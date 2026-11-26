"""Tải Be Vietnam Pro (fontsource, chỉ woff2 vietnamese/latin/latin-ext) vào data/fonts/ để build nhúng base64.
Chạy 1 lần: python -B fetch_fonts.py"""
import re, urllib.request
from pathlib import Path

VER, WEIGHTS, SUBSETS = "5.2.8", (400, 500, 600, 700), ("vietnamese", "latin-ext", "latin")
BASE = f"https://cdn.jsdelivr.net/npm/@fontsource/be-vietnam-pro@{VER}"
OUT = Path(__file__).resolve().parent.parent / "data" / "fonts"


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "font-fetch"}), timeout=30) as r:
        return r.read()


OUT.mkdir(parents=True, exist_ok=True)
rules = []
for w in WEIGHTS:
    css = get(f"{BASE}/{w}.css").decode()
    for block in re.findall(r"/\*\s*([\w-]+)\s*\*/\s*@font-face\s*{([^}]*)}", css):
        subset, body = block[0].split("-" + str(w))[0].replace("be-vietnam-pro-", ""), block[1]
        if subset not in SUBSETS:
            continue
        woff2 = re.search(r"url\(\.?/?(files/[^)]+\.woff2)\)", body).group(1)
        name = Path(woff2).name
        (OUT / name).write_bytes(get(f"{BASE}/{woff2}"))
        rng = re.search(r"unicode-range:\s*([^;]+);", body).group(1)
        rules.append(f"@font-face{{font-family:'Be Vietnam Pro';font-style:normal;font-display:swap;font-weight:{w};"
                     f"src:url({name}) format('woff2');unicode-range:{rng}}}")
(OUT / "fonts.css").write_text("\n".join(rules) + "\n", encoding="utf-8")
print(len(rules), "font-face,", sum(p.stat().st_size for p in OUT.glob("*.woff2")) // 1024, "KB")
