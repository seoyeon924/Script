#!/usr/bin/env python3
import os, re, subprocess, tempfile

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUTPUT = "/Users/sy/Projects/Script/output/pdf"
os.makedirs(OUTPUT, exist_ok=True)

SLIDE_STYLE = (
    "display:flex!important;position:relative!important;"
    "inset:auto!important;width:1280px!important;height:800px!important;"
    "flex-shrink:0!important;page-break-after:always!important;"
    "break-after:page!important;"
)

OVERRIDE_CSS = """<style id="pdf-override">
@page { size: 1280px 800px; margin: 0; }
html, body { width: 1280px !important; height: auto !important; overflow: visible !important; }
.deck { width: 1280px !important; height: auto !important; position: relative !important; transform: none !important; top: auto !important; left: auto !important; }
.slide, .slide.active { display: flex !important; position: relative !important; inset: auto !important; width: 1280px !important; height: 800px !important; flex-shrink: 0 !important; page-break-after: always !important; break-after: page !important; }
.slide:last-child { page-break-after: avoid !important; break-after: avoid !important; }
.nav, .progress, .clip-dots { display: none !important; }
</style>
"""


def extract_order(html):
    """Extract ORDER array from JS before it's removed."""
    m = re.search(r'const\s+ORDER\s*=\s*\[([^\]]+)\]', html)
    if not m:
        return None
    raw = m.group(1)
    items = re.findall(r"'([^']+)'|(\d+)", raw)
    return [s if s else n for s, n in items]


def find_closing_div(html, start):
    """Find the end position of a <div> tag opening at start."""
    pos = html.index('>', start) + 1
    depth = 1
    while depth > 0 and pos < len(html):
        next_open = html.find('<div', pos)
        next_close = html.find('</div>', pos)
        if next_close == -1:
            break
        if next_open != -1 and next_open < next_close:
            depth += 1
            pos = next_open + 4
        else:
            depth -= 1
            pos = next_close + 6
    return pos


def reorder_slides(html, order):
    """Reorder slide divs in the HTML according to ORDER array."""
    if not order:
        return html

    # Extract each slide's HTML by ID
    slides = {}
    for item in order:
        sid = 's' + str(item)
        if sid in slides:
            continue
        pattern = re.compile(r'<div\s[^>]*\bid="' + re.escape(sid) + r'"[^>]*>')
        m = pattern.search(html)
        if m:
            start = m.start()
            end = find_closing_div(html, start)
            slides[sid] = html[start:end]

    # Find the range of all slides in the source HTML
    all_slides = list(re.finditer(r'<div\s+class="slide(?:\s+active)?"\s+id="s', html))
    if not all_slides:
        return html

    range_start = all_slides[0].start()
    last_start = all_slides[-1].start()
    range_end = find_closing_div(html, last_start)

    # Reconstruct with slides in ORDER
    ordered = '\n\n'.join(slides[f's{item}'] for item in order if f's{item}' in slides)
    return html[:range_start] + ordered + '\n' + html[range_end:]


def convert(html_path, out_name):
    html_dir = os.path.dirname(os.path.abspath(html_path))

    with open(html_path, encoding="utf-8") as f:
        html = f.read()

    # Resolve relative paths → absolute file:// (temp file location independence)
    def to_abs(m):
        attr, q, path = m.group(1), m.group(2), m.group(3)
        if path.startswith(('http', 'data:', 'file:', '//', '#')):
            return m.group(0)
        abs_path = os.path.normpath(os.path.join(html_dir, path))
        return f'{attr}={q}file://{abs_path}{q}'

    html = re.sub(r'(src|href)=(["\'])(?!http|data:|file:|//|#)([^"\'>\s]+)\2', to_abs, html)

    # Extract ORDER before removing JS
    order = extract_order(html)

    # Remove all JS
    html = re.sub(r'<script\b[^>]*>[\s\S]*?</script>', '', html, flags=re.IGNORECASE)

    # Reorder slides to match presentation ORDER
    if order:
        html = reorder_slides(html, order)

    # Inject override CSS
    html = html.replace('</head>', OVERRIDE_CSS + '</head>', 1)

    # Add inline styles on each slide element
    html = re.sub(
        r'<div\s+class="slide(?:\s+active)?"',
        f'<div class="slide" style="{SLIDE_STYLE}"',
        html
    )

    with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w", encoding="utf-8") as tmp:
        tmp.write(html)
        tmp_path = tmp.name

    out_path = os.path.join(OUTPUT, out_name + ".pdf")
    subprocess.run([
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        f"--print-to-pdf={out_path}",
        "--no-pdf-header-footer",
        f"file://{tmp_path}"
    ], capture_output=True)

    os.unlink(tmp_path)
    size = os.path.getsize(out_path)
    print(f"  ✓ {out_name}.pdf  ({size//1024}KB)")


BASE = "/Users/sy/Projects/Script"

chapters = [
    ("Part 0 — 왜 AI 데이터 시각화인가", [
        (f"{BASE}/P01-CH01/P01-CH01-slides.html", "P0-CH1-데이터시각화기초관점잡기"),
        (f"{BASE}/P01-CH02/P01-CH02-slides.html", "P0-CH2-바이브코딩환경세팅"),
    ]),
    ("Part 1 — Claude Code 핵심 빠르게 익히기", [
        (f"{BASE}/P02-CH01/P02-CH01-slides.html", "P1-CH1-ClaudeCode첫걸음"),
        (f"{BASE}/P02-CH02/P02-CH02-slides.html", "P1-CH2-MCP_Skills도구확장"),
        (f"{BASE}/P02-CH03/P02-CH03-slides.html", "P1-CH3-데이터분석협업구조"),
    ]),
]

for part_name, files in chapters:
    print(f"\n{part_name}")
    for html_path, out_name in files:
        if os.path.exists(html_path):
            convert(html_path, out_name)
        else:
            print(f"  ✗ 파일 없음: {html_path}")

print("\n=== 완료 ===")
for f in sorted(os.listdir(OUTPUT)):
    if f.endswith(".pdf"):
        sz = os.path.getsize(os.path.join(OUTPUT, f))
        print(f"  {f}  ({sz//1024}KB)")
