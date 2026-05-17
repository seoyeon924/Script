#!/bin/bash
# 챕터별 슬라이드 HTML → PDF 변환

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUTPUT="/Users/sy/Projects/Script/output/pdf"
SCRIPT_DIR="/Users/sy/Projects/Script"

mkdir -p "$OUTPUT"

PRINT_CSS='
<style id="print-override">
@media print {
  body { margin: 0; background: #F2F2EF; }
  .deck {
    position: relative !important;
    transform: none !important;
    width: 1280px !important;
    height: auto !important;
    top: auto !important;
    left: auto !important;
  }
  .slide {
    display: flex !important;
    position: relative !important;
    inset: auto !important;
    width: 1280px !important;
    height: 800px !important;
    page-break-after: always !important;
    break-after: page !important;
  }
  .slide:last-child { page-break-after: avoid !important; break-after: avoid !important; }
  .nav, .progress, .clip-dots { display: none !important; }
}
</style>'

convert_to_pdf() {
  local html_file="$1"
  local pdf_name="$2"
  local tmp_file="/tmp/print_$(basename $html_file)"

  # print CSS 주입
  sed "s|</head>|${PRINT_CSS}</head>|" "$html_file" > "$tmp_file"

  "$CHROME" \
    --headless \
    --disable-gpu \
    --print-to-pdf="$OUTPUT/$pdf_name.pdf" \
    --print-to-pdf-no-header \
    --no-margins \
    --paper-size=custom \
    --paper-width=13.33 \
    --paper-height=8.33 \
    "file://$tmp_file" 2>/dev/null

  rm -f "$tmp_file"
  echo "✓ $pdf_name.pdf"
}

echo "=== 챕터별 PDF 생성 ==="
echo ""
echo "Part 0 — 왜 AI 데이터 시각화인가"
convert_to_pdf "$SCRIPT_DIR/P01-CH01/P01-CH01-slides.html" "P0-CH1-데이터시각화기초관점잡기"
convert_to_pdf "$SCRIPT_DIR/P01-CH02/P01-CH02-slides.html" "P0-CH2-바이브코딩환경세팅"

echo ""
echo "Part 1 — Claude Code 핵심 빠르게 익히기"
convert_to_pdf "$SCRIPT_DIR/P02-CH01/P02-CH01-slides.html" "P1-CH1-ClaudeCode첫걸음"
convert_to_pdf "$SCRIPT_DIR/P02-CH02/P02-CH02-slides.html" "P1-CH2-MCP_Skills도구확장"
convert_to_pdf "$SCRIPT_DIR/P02-CH03/P02-CH03-slides.html" "P1-CH3-데이터분석협업구조"

echo ""
echo "=== 완료 ==="
ls -lh "$OUTPUT"/*.pdf
