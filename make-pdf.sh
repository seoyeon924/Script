#!/usr/bin/env python3
# 챕터별 슬라이드 HTML → PDF 변환 (Playwright 방식)
# 실행: python3 make-pdf.sh  또는  bash make-pdf.sh

import os, sys, io
from playwright.sync_api import sync_playwright
from PIL import Image

OUTPUT = os.path.join(os.path.dirname(__file__), "output/pdf")
BASE   = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUTPUT, exist_ok=True)

FILES = [
    ("P01-CH01/P01-CH01-slides.html", "P0-CH1-데이터시각화기초관점잡기"),
    ("P01-CH02/P01-CH02-slides.html", "P0-CH2-바이브코딩환경세팅"),
    ("P02-CH01/P02-CH01-slides.html", "P1-CH1-ClaudeCode첫걸음"),
    ("P02-CH02/P02-CH02-slides.html", "P1-CH2-MCP_Skills도구확장"),
    ("P02-CH03/P02-CH03-slides.html", "P1-CH3-데이터분석협업구조"),
    ("P03-CH01/P03-CH01-slides.html", "P2-CH1-데이터분석파이프라인"),
    ("P03-CH02/P03-CH02-slides.html", "P2-CH2-실데이터투입실행"),
]

print("=== 챕터별 PDF 생성 (Playwright) ===\n")

with sync_playwright() as p:
    browser = p.chromium.launch()

    for rel_path, pdf_name in FILES:
        html_path = os.path.join(BASE, rel_path)
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        page.goto(f"file://{html_path}")
        page.wait_for_load_state("networkidle")

        total = page.evaluate(
            "typeof TOTAL !== 'undefined' ? TOTAL : document.querySelectorAll('.slide').length"
        )

        screenshots = []
        for i in range(total):
            page.evaluate(f"show({i})")
            page.wait_for_timeout(80)
            screenshots.append(page.screenshot(full_page=False))

        page.close()

        images = [Image.open(io.BytesIO(s)).convert("RGB") for s in screenshots]
        out_path = os.path.join(OUTPUT, f"{pdf_name}.pdf")
        images[0].save(out_path, save_all=True, append_images=images[1:], resolution=96)

        size = os.path.getsize(out_path)
        print(f"✓ {pdf_name}.pdf  —  {size//1024}K, {len(images)}페이지")

    browser.close()

print("\n=== 완료 ===")
