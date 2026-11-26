"""T0: chụp trang PDF, giải nén SolasMart, chuyển md, sinh docs/nguon.md. Chạy lại chỉ làm phần thiếu."""
import subprocess, sys
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
SRC, PAGES = ROOT / "tai-lieu", ROOT / "data" / "pages"
SOLAS = SRC / "solasmart"
TOMD = Path(r"D:/LAPTRINH/crawl extension/TOOL/GR/file to md/script/tomd.py")

LESSONS = [  # (id, tên, [file gốc]) — khớp plan.md §3
    ("L01", "Giới thiệu về BA", ["Buổi 1_Giới thiệu về BA.pdf"]),
    ("L02", "Kiến thức cơ bản về IT", ["2. Kien thuc co ban ve IT.pdf"]),
    ("L03", "Quy trình phát triển phần mềm", ["3. Quy trinh phat trien phan mem.pdf"]),
    ("L04", "Tiếp cận dự án và Stakeholder", ["4. Tiep can du an.pdf", "4. Stakeholder_Register_Template.xlsx"]),
    ("L05", "Kỹ thuật khai thác yêu cầu", ["5. Ky thuat khai thac yeu cau.pdf", "5. Elicitation activity plan.pdf",
                                         "5. Mau phieu khao sat.docx", "5. Observation_Note_Template.docx"]),
    ("L06", "Quản lý yêu cầu", ["6. Quan ly yeu cau.pdf", "6. MaTranTuyVet-RTM.xlsx", "6. Quan ly thay doi.docx",
                               "6. Quan ly tai lieu.docx", "6. HƯỚNG DẪN QUY TRÌNH SỬ DỤNG LOG TASK.docx"]),
    ("L07", "BACCM", ["7. BACCM.pdf"]),
    ("L09", "Document Analysis", ["9. Document Analysis.pdf", "Quy trinh ban hang tai quay.docx", "SOLASMART"]),
    ("L11a", "Yêu cầu chức năng và phi chức năng", ["11. Yeu cau chuc nang va yeu cau phi chuc nang.pdf"]),
    ("L11b", "Phân tích hướng đối tượng", ["11. Phan tich huong doi tuong.pdf"]),
    ("L11c", "Phân tích GAP", ["11. Phan tich GAP.pdf"]),
    ("L12", "Quy trình nghiệp vụ và BPMN", ["12. Business Process.pdf", "12. BPMN-20-Poster-EN.png"]),
    ("L13a", "UML, Use Case và State Diagram", ["13. UML.pdf", "13. Vẽ UseCase và State Diagram - Quy trình Đặt đồ ăn.docx"]),
    ("L13b", "Đặc tả Use Case", ["13. Đặc tả UseCase.pdf"]),
    ("L14", "Activity Diagram", ["14. Activity Diagram.pdf"]),
    ("L16", "Các loại tài liệu BA", ["16. Cac loai tai lieu BA.pdf", "BRD_Template.docx", "SRS_Template.docx", "FSD_Template.docx"]),
    ("L20", "ERD", ["20. ERD.pdf"]),
    ("L21", "Database và kiểu dữ liệu SQL Server", ["21. Database.pdf", "21. Kieu du lieu trong Sql Server.pdf"]),
    ("L23", "API", ["23. Api - Ly Thuyet.pdf"]),
]


def render(pdf):
    out = PAGES / pdf.stem
    doc = pymupdf.open(pdf)
    out.mkdir(parents=True, exist_ok=True)
    for i, page in enumerate(doc, 1):
        f = out / f"p-{i:03d}.jpg"
        if not f.exists():
            page.get_pixmap(dpi=110).save(f, jpg_quality=80)
    return out, doc.page_count


def to_md(files):
    """Gọi tomd (dùng cache của tool); trả {tên file: đường dẫn md}."""
    if not files:
        return {}
    r = subprocess.run([sys.executable, "-B", str(TOMD), *map(str, files)], capture_output=True, text=True, encoding="utf-8")
    res = {}
    for line in r.stdout.splitlines():
        status, _, path = line.partition(" ")
        path = path.strip()
        name = Path(path).parent.name.rsplit("-", 1)[0] if status in ("ok", "cache") else None
        if name:
            res[name] = path
    missing = [f.name for f in files if f.name not in res]
    if missing:
        sys.exit(f"tomd lỗi: {missing}\n{r.stdout}\n{r.stderr}")
    return res


def main():
    solas = sorted(SOLAS.iterdir())
    # tai-lieu/ chia theo module; tìm file theo tên (solasmart có bản trùng tên, bỏ ra)
    where = {p.name: p for p in SRC.rglob("*") if p.is_file() and SOLAS not in p.parents}
    docs = [p for p in where.values() if p.suffix.lower() in (".docx", ".xlsx", ".pdf")]
    md = to_md(docs + solas)
    lines = ["# Nguồn theo bài (sinh bởi script/render.py)", "",
             f"Gốc ITBA: `{ROOT.as_posix()}/`. Ảnh trang: `data/pages/<tên pdf>/p-NNN.jpg`.", ""]
    total = 0
    for lid, title, files in LESSONS:
        lines += [f"## {lid} – {title}", ""]
        for name in files:
            if name == "SOLASMART":
                lines.append(f"- Case study SolasMart (`{SOLAS.relative_to(ROOT).as_posix()}/`):")
                lines += [f"  - {p.name} → md: `{md[p.name]}`" for p in solas]
                continue
            p = where[name]
            row = f"- `{p.relative_to(ROOT).as_posix()}`"
            if p.suffix.lower() == ".pdf":
                folder, n = render(p)
                total += n
                row += f" ({n} trang) → ảnh: `data/pages/{folder.name}/p-001..{n:03d}.jpg`"
            if name in md:
                row += f" → md: `{md[name]}`"
            if p.suffix.lower() == ".png":
                row += " (ảnh gốc, xem trực tiếp)"
            lines.append(row)
        lines.append("")
    (ROOT / "docs" / "nguon.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"pages={total} md={len(md)}")


if __name__ == "__main__":
    main()
