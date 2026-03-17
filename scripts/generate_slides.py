#!/usr/bin/env python3
"""
스크립트 .md → 섹션별 슬라이드 PNG 생성
사용: python3 generate_slides.py <script.md> <output_dir>
"""

import sys, re, os
from PIL import Image, ImageDraw, ImageFont

# ── 디자인 토큰 ──────────────────────────────────────────────
BG_DARK    = (13, 17, 23)        # #0D1117
BG_CARD    = (22, 28, 38)        # #161C26
ACCENT     = (74, 122, 181)      # #4A7AB5  DataBridge blue
TEXT_WHITE = (245, 246, 247)
TEXT_GRAY  = (140, 150, 165)
TEXT_DIM   = (90, 100, 115)
W, H       = 1920, 1080

# ── 폰트 로드 (시스템 한글 폰트) ────────────────────────────
def load_font(size):
    candidates = [
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        "/System/Library/Fonts/Supplemental/AppleGothic.ttf",
        "/Library/Fonts/NanumGothic.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                continue
    return ImageFont.load_default()

FONT_CHAPTER = load_font(28)
FONT_TITLE   = load_font(72)
FONT_SUBTITLE= load_font(42)
FONT_BODY    = load_font(36)
FONT_LABEL   = load_font(24)

# ── 텍스트 줄바꿈 ────────────────────────────────────────────
def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        bbox = draw.textbbox((0,0), test, font=font)
        if bbox[2] > max_width and cur:
            lines.append(cur)
            cur = w
        else:
            cur = test
    if cur:
        lines.append(cur)
    return lines

def draw_multiline(draw, text, font, x, y, max_width, color, line_gap=12):
    lines = wrap_text(draw, text, font, max_width)
    cy = y
    for line in lines:
        draw.text((x, cy), line, font=font, fill=color)
        bbox = draw.textbbox((0,0), line, font=font)
        cy += (bbox[3] - bbox[1]) + line_gap
    return cy

# ── 공통 베이스 레이아웃 ─────────────────────────────────────
def make_base(chapter_label="CH01-01", clip_title="클로드 코드란 무엇인가"):
    img = Image.new("RGB", (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)

    # 상단 액센트 바
    draw.rectangle([(0, 0), (W, 6)], fill=ACCENT)

    # 좌상단 챕터 레이블
    draw.text((64, 36), chapter_label, font=FONT_LABEL, fill=TEXT_DIM)

    # 우상단 DataBridge
    brand_text = "DataBridge × Fastcampus"
    bbox = draw.textbbox((0,0), brand_text, font=FONT_LABEL)
    draw.text((W - bbox[2] - 64, 36), brand_text, font=FONT_LABEL, fill=TEXT_DIM)

    # 하단 라인
    draw.rectangle([(0, H - 6), (W, H)], fill=ACCENT)

    return img, draw

# ── 슬라이드 타입별 생성 ─────────────────────────────────────

def slide_title(chapter_label, clip_title, clip_subtitle=""):
    """타이틀 슬라이드"""
    img, draw = make_base(chapter_label, clip_title)

    # 중앙 타이틀
    title_y = H // 2 - 80
    bbox = draw.textbbox((0,0), clip_title, font=FONT_TITLE)
    title_w = bbox[2] - bbox[0]
    draw.text(((W - title_w) // 2, title_y), clip_title, font=FONT_TITLE, fill=TEXT_WHITE)

    if clip_subtitle:
        sub_y = title_y + (bbox[3] - bbox[1]) + 28
        bbox2 = draw.textbbox((0,0), clip_subtitle, font=FONT_SUBTITLE)
        draw.text(((W - (bbox2[2]-bbox2[0])) // 2, sub_y), clip_subtitle, font=FONT_SUBTITLE, fill=ACCENT)

    # 하단 챕터 번호
    draw.text((64, H - 64), chapter_label, font=FONT_CHAPTER, fill=TEXT_DIM)

    return img

def slide_section(section_title, body_lines, chapter_label="CH01-01"):
    """섹션 콘텐츠 슬라이드"""
    img, draw = make_base(chapter_label)

    # 섹션 타이틀
    title_y = 120
    draw.text((80, title_y), section_title, font=FONT_SUBTITLE, fill=ACCENT)

    # 구분선
    draw.rectangle([(80, title_y + 62), (W - 80, title_y + 64)], fill=(40, 50, 65))

    # 본문
    body_y = title_y + 90
    for line in body_lines[:12]:  # 최대 12줄
        if line.startswith("→") or line.startswith("-"):
            color = TEXT_GRAY
        else:
            color = TEXT_WHITE
        body_y = draw_multiline(draw, line, FONT_BODY, 80, body_y, W - 160, color, line_gap=14)
        body_y += 8
        if body_y > H - 120:
            break

    draw.text((64, H - 64), chapter_label, font=FONT_CHAPTER, fill=TEXT_DIM)
    return img

def slide_outro(chapter_label, next_clip_title=""):
    """마무리 슬라이드"""
    img, draw = make_base(chapter_label)

    msg = "이번 클립 완료"
    bbox = draw.textbbox((0,0), msg, font=FONT_TITLE)
    draw.text(((W - (bbox[2]-bbox[0])) // 2, H//2 - 100), msg, font=FONT_TITLE, fill=TEXT_WHITE)

    if next_clip_title:
        sub = f"다음 → {next_clip_title}"
        bbox2 = draw.textbbox((0,0), sub, font=FONT_SUBTITLE)
        draw.text(((W - (bbox2[2]-bbox2[0])) // 2, H//2 + 30), sub, font=FONT_SUBTITLE, fill=ACCENT)

    draw.text((64, H - 64), chapter_label, font=FONT_CHAPTER, fill=TEXT_DIM)
    return img

# ── 스크립트에서 섹션 파싱 ───────────────────────────────────
SKIP_SECTIONS_RE = re.compile(
    r"(📌\s*클립\s*정보|🗒️\s*서연\s*메모|직접\s*해보기|준비물)",
    re.IGNORECASE
)

def parse_sections(md_text):
    """마크다운에서 섹션 타이틀 + 첫 본문 추출"""
    text = re.sub(r"^---[\s\S]+?---\n", "", md_text.strip())
    parts = re.split(r"\n(#{1,3} .+)\n", text)

    sections = []
    i = 0
    while i < len(parts):
        chunk = parts[i]
        hm = re.match(r"#{1,3} (.+)", chunk.strip())
        if hm:
            title = hm.group(1).strip()
            # 제목 정리 (괄호 시간 제거)
            title_clean = re.sub(r"\s*\(\d+분\)", "", title).strip()
            i += 1
            if i < len(parts):
                body = parts[i]
            else:
                body = ""

            if not SKIP_SECTIONS_RE.search(title):
                # 본문 정제
                body = re.sub(r"```[\s\S]+?```", "", body)
                body = re.sub(r"(>.*\n?)+", "", body)
                body = re.sub(r"\[화면:.*?\]", "", body)
                body = re.sub(r"\*\*(.+?)\*\*", r"\1", body)
                body = re.sub(r"\*(.+?)\*", r"\1", body)
                body = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", body)
                lines = [l.strip() for l in body.split("\n") if l.strip() and not l.strip().startswith("|")]
                lines = [l for l in lines if not re.match(r"^(mkdir|cd |printf|claude|python|pip|npm|curl|git )", l)]
                if lines:
                    sections.append({"title": title_clean, "lines": lines[:10]})
        i += 1

    return sections

# ── 메인 ─────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("사용법: python3 generate_slides.py <script.md> <output_dir>")
        sys.exit(1)

    md_path = sys.argv[1]
    out_dir  = sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)

    # 챕터/클립 정보
    base = os.path.basename(md_path)
    ch_match = re.match(r"(CH\d+-\d+)\s+(.+?)\.md", base)
    chapter_label = ch_match.group(1) if ch_match else "CH01-01"
    clip_title    = ch_match.group(2) if ch_match else "강의"

    with open(md_path, encoding="utf-8") as f:
        raw = f.read()

    # 클립 부제목 추출 (— 이후)
    subtitle = ""
    if "—" in clip_title:
        parts = clip_title.split("—", 1)
        clip_title = parts[0].strip()
        subtitle   = parts[1].strip()

    sections = parse_sections(raw)

    slides = []

    # 1. 타이틀 슬라이드
    s = slide_title(chapter_label, clip_title, subtitle)
    path = os.path.join(out_dir, "00_title.png")
    s.save(path)
    slides.append(path)
    print(f"[슬라이드 00] 타이틀 → {path}")

    # 2. 섹션 슬라이드
    for i, sec in enumerate(sections):
        s = slide_section(sec["title"], sec["lines"], chapter_label)
        path = os.path.join(out_dir, f"{i+1:02d}_{sec['title'][:20]}.png")
        s.save(path)
        slides.append(path)
        print(f"[슬라이드 {i+1:02d}] {sec['title']} → {path}")

    # 3. 아웃트로
    s = slide_outro(chapter_label, "설치 & 첫 번째 세션")
    path = os.path.join(out_dir, f"{len(sections)+1:02d}_outro.png")
    s.save(path)
    slides.append(path)
    print(f"[슬라이드 outro] → {path}")

    print(f"\n총 {len(slides)}장 생성 완료")
    print("\n".join(slides))
