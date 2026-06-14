#!/usr/bin/env python3
"""HTML 슬라이드 → PDF (Playwright, 벡터, 슬라이드 사이즈 정확히)"""

import re, io
from pathlib import Path
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

W, H = 1280, 800   # 슬라이드 픽셀 크기

OUTPUT = Path(__file__).parent / "output/pdf"
OUTPUT.mkdir(parents=True, exist_ok=True)

FILES = [
    ("P03-CH02/P03-CH02-slides.html", "P2-CH2-실데이터투입실행"),
]

# @page 사이즈로 슬라이드 크기 고정, 여백 0
PRINT_CSS = f"""
@page {{
  size: {W}px {H}px;
  margin: 0;
}}

* {{
  -webkit-print-color-adjust: exact !important;
  print-color-adjust: exact !important;
}}

html, body {{
  width: {W}px !important;
  height: auto !important;
  overflow: visible !important;
}}

.deck {{
  position: static !important;
  width: {W}px !important;
  height: auto !important;
  transform: none !important;
  display: block !important;
}}

.slide {{
  display: flex !important;
  position: relative !important;
  width: {W}px !important;
  height: {H}px !important;
  overflow: hidden !important;
  flex-shrink: 0 !important;
  page-break-after: always !important;
  break-after: page !important;
}}

.slide:last-child {{
  page-break-after: avoid !important;
  break-after: avoid !important;
}}

.nav, .nav-btn {{ display: none !important; }}
"""

def extract_order(html_text):
    m = re.search(r"const ORDER\s*=\s*\[([^\]]+)\]", html_text)
    if not m:
        return None
    return [int(x.strip()) for x in m.group(1).split(",") if x.strip().isdigit()]

def build_print_html(src_path):
    html_text = Path(src_path).read_text(encoding="utf-8")
    order = extract_order(html_text)
    soup = BeautifulSoup(html_text, "html.parser")

    style_tag = soup.new_tag("style")
    style_tag.string = PRINT_CSS
    soup.head.append(style_tag)

    if order:
        deck = soup.find(class_="deck")
        if deck:
            slides = {tag["id"]: tag for tag in deck.find_all(class_="slide") if tag.get("id")}
            for tag in list(deck.find_all(class_="slide")):
                tag.extract()
            for idx in order:
                sid = f"s{idx}"
                if sid in slides:
                    slide = slides[sid]
                    classes = slide.get("class", [])
                    if "active" not in classes:
                        slide["class"] = classes + ["active"]
                    deck.append(slide)

    return str(soup)

BASE = Path(__file__).parent
print("=== HTML → PDF (Playwright 벡터) ===\n")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": W, "height": H})

    for rel, name in FILES:
        src = BASE / rel
        out = OUTPUT / f"{name}.pdf"

        print(f"변환 중: {rel} ...", end=" ", flush=True)

        html_content = build_print_html(src)
        import tempfile, os
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w", encoding="utf-8") as f:
            f.write(html_content)
            tmp = f.name
        page.goto(f"file://{tmp}")
        page.wait_for_load_state("networkidle")

        page.pdf(
            path=str(out),
            width=f"{W}px",
            height=f"{H}px",
            print_background=True,
        )

        os.unlink(tmp)
        size = out.stat().st_size
        print(f"완료 — {size // 1024}K → {out.name}")

    browser.close()

print("\n=== 완료 ===")
