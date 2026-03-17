#!/usr/bin/env python3
"""
디자인 시스템별 슬라이드 3장 생성 → 비교용 캡처
"""

import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from design_systems import DESIGN_SYSTEMS
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
OUT = "/tmp/Script-repo/output/comparison"
os.makedirs(OUT, exist_ok=True)

# ── 폰트 ─────────────────────────────────────────────────────
def load_font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        "/System/Library/Fonts/Supplemental/AppleGothic.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                continue
    return ImageFont.load_default()

FNT = {
    "xl":    load_font(80),
    "lg":    load_font(52),
    "md":    load_font(38),
    "sm":    load_font(28),
    "xs":    load_font(22),
    "tag":   load_font(18),
}

# ── 헬퍼 ─────────────────────────────────────────────────────
def cx(draw, text, font, y, color, img_w=W):
    bbox = draw.textbbox((0,0), text, font=font)
    x = (img_w - (bbox[2]-bbox[0])) // 2
    draw.text((x, y), text, font=font, fill=color)
    return bbox[3] - bbox[1]

def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur+" "+w).strip()
        if draw.textbbox((0,0),test,font=font)[2] > max_w and cur:
            lines.append(cur); cur = w
        else:
            cur = test
    if cur: lines.append(cur)
    return lines

def draw_lines(draw, lines, font, x, y, color, gap=12, max_w=W-200):
    for line in lines:
        for sub in wrap(draw, line, font, max_w):
            draw.text((x, y), sub, font=font, fill=color)
            y += draw.textbbox((0,0),sub,font=font)[3] + gap
        y += 4
    return y

def pill(draw, x, y, w, h, color, radius=10):
    draw.rounded_rectangle([x, y, x+w, y+h], radius=radius, fill=color)

# ── 슬라이드 1: 타이틀 ───────────────────────────────────────
def slide_title(ds, name):
    img = Image.new("RGB", (W, H), ds["bg"])
    draw = ImageDraw.Draw(img)

    # 상단 액센트 바
    draw.rectangle([(0,0),(W,8)], fill=ds["bar_top"])

    # 챕터 태그 pill
    tag = "CH01-01"
    tag_w = draw.textbbox((0,0),tag,font=FNT["tag"])[2] + 32
    pill(draw, (W-tag_w)//2, 80, tag_w, 36, ds["accent"], radius=18)
    draw.text(((W-tag_w)//2+16, 88), tag, font=FNT["tag"], fill=ds["bg"])

    # 메인 타이틀
    title1 = "클로드 코드란"
    title2 = "무엇인가"
    h1 = cx(draw, title1, FNT["xl"], H//2 - 110, ds["text_primary"])
    cx(draw, title2, FNT["xl"], H//2 - 110 + h1 + 12, ds["text_primary"])

    # 서브타이틀
    sub = "에이전트 구조 이해"
    cx(draw, sub, FNT["md"], H//2 + 80, ds["accent"])

    # 하단 브랜드
    brand = "DataBridge × Fastcampus"
    draw.rectangle([(0,H-8),(W,H)], fill=ds["bar_top"])
    bbox = draw.textbbox((0,0),brand,font=FNT["xs"])
    draw.text((64, H-52), brand, font=FNT["xs"], fill=ds["text_secondary"])

    # 디자인 시스템 이름 (우하단)
    ds_label = f"Design: {name}"
    bbox2 = draw.textbbox((0,0),ds_label,font=FNT["xs"])
    draw.text((W-bbox2[2]-64, H-52), ds_label, font=FNT["xs"], fill=ds["text_dim"])

    return img

# ── 슬라이드 2: 콘텐츠 (불릿 리스트) ────────────────────────
def slide_content(ds, name):
    img = Image.new("RGB", (W, H), ds["bg"])
    draw = ImageDraw.Draw(img)

    draw.rectangle([(0,0),(W,8)], fill=ds["bar_top"])
    draw.rectangle([(0,H-8),(W,H)], fill=ds["bar_top"])

    # 좌상단 챕터
    draw.text((80, 40), "CH01-01", font=FNT["xs"], fill=ds["text_dim"])
    brand = "DataBridge × Fastcampus"
    bbox = draw.textbbox((0,0),brand,font=FNT["xs"])
    draw.text((W-bbox[2]-80, 40), brand, font=FNT["xs"], fill=ds["text_dim"])

    # 섹션 타이틀
    sec_title = "챗지피티 vs 클로드 코드"
    draw.text((80, 110), sec_title, font=FNT["lg"], fill=ds["accent"])

    # 구분선
    draw.rectangle([(80, 180), (W-80, 183)], fill=ds["border"])

    # 두 컬럼 비교
    col_w = (W - 240) // 2
    col1_x, col2_x = 80, 80 + col_w + 80

    # 컬럼 헤딩
    draw.text((col1_x, 210), "챗지피티", font=FNT["md"], fill=ds["text_secondary"])
    draw.text((col2_x, 210), "클로드 코드", font=FNT["md"], fill=ds["text_primary"])

    # 구분선 (컬럼 사이)
    mid_x = col1_x + col_w + 40
    draw.rectangle([(mid_x, 200), (mid_x+2, H-80)], fill=ds["border"])

    # 불릿 아이템 - 챗지피티
    items1 = [
        "대화 인터페이스",
        "텍스트 입력 → 텍스트 출력",
        "파일 시스템 접근 불가",
        "세션 간 기억 없음",
        "조언을 주는 도구",
    ]
    items2 = [
        "에이전트 구조",
        "터미널에서 직접 실행",
        "파일 읽기/쓰기/실행 가능",
        "CLAUDE.md로 컨텍스트 유지",
        "실제 작업을 수행하는 도구",
    ]

    y = 290
    for item in items1:
        # 불릿 원
        draw.ellipse([(col1_x, y+8), (col1_x+10, y+18)], fill=ds["text_secondary"])
        draw.text((col1_x+22, y), item, font=FNT["sm"], fill=ds["text_secondary"])
        y += 54

    y = 290
    for item in items2:
        draw.ellipse([(col2_x, y+8), (col2_x+10, y+18)], fill=ds["accent"])
        draw.text((col2_x+22, y), item, font=FNT["sm"], fill=ds["text_primary"])
        y += 54

    # 하단 핵심 메시지 카드
    card_y = H - 170
    draw.rounded_rectangle([(80, card_y), (W-80, card_y+100)], radius=14, fill=ds["bg_card"])
    msg = "핵심:  챗지피티는 조언 / 클로드 코드는 실행"
    cx(draw, msg, FNT["sm"], card_y + 36, ds["text_primary"])

    return img

# ── 슬라이드 3: 섹션 인트로 / 에이전트 구조 ─────────────────
def slide_section(ds, name):
    img = Image.new("RGB", (W, H), ds["bg"])
    draw = ImageDraw.Draw(img)

    draw.rectangle([(0,0),(W,8)], fill=ds["bar_top"])
    draw.rectangle([(0,H-8),(W,H)], fill=ds["bar_top"])

    # 배경 카드
    draw.rounded_rectangle([(120, 60),(W-120, H-60)], radius=20, fill=ds["bg_card"])

    # 상단 섹션 번호
    cx(draw, "SECTION 02", FNT["tag"], 110, ds["text_dim"])

    # 중앙 타이틀
    cx(draw, "에이전트 구조", FNT["xl"], 200, ds["text_primary"])
    cx(draw, "어떻게 작동하는가", FNT["md"], 310, ds["accent"])

    # 플로우 다이어그램 (간단한 박스)
    boxes = [
        ("사용자 지시", 0),
        ("계획", 1),
        ("도구 선택", 2),
        ("실행", 3),
        ("완료", 4),
    ]
    box_w, box_h = 220, 70
    total_w = len(boxes) * box_w + (len(boxes)-1) * 60
    start_x = (W - total_w) // 2
    box_y = H//2 + 20

    for i, (label, _) in enumerate(boxes):
        bx = start_x + i * (box_w + 60)
        # 박스
        color = ds["accent"] if i == 0 or i == 4 else ds["bg_section"]
        text_color = ds["bg"] if i == 0 or i == 4 else ds["text_primary"]
        draw.rounded_rectangle([(bx, box_y),(bx+box_w, box_y+box_h)], radius=10, fill=color, outline=ds["border"], width=2)
        bbox = draw.textbbox((0,0),label,font=FNT["sm"])
        draw.text((bx + (box_w-(bbox[2]-bbox[0]))//2, box_y + (box_h-(bbox[3]-bbox[1]))//2), label, font=FNT["sm"], fill=text_color)
        # 화살표
        if i < len(boxes)-1:
            ax = bx + box_w + 10
            ay = box_y + box_h//2
            draw.polygon([(ax,ay-8),(ax+40,ay),(ax,ay+8)], fill=ds["text_dim"])

    # 설명
    desc = "이 사이클이 반복되는 것을 에이전트 루프라고 합니다"
    cx(draw, desc, FNT["sm"], box_y + box_h + 40, ds["text_secondary"])

    # 하단
    draw.text((80, H-52), "CH01-01", font=FNT["xs"], fill=ds["text_dim"])
    bbox2 = draw.textbbox((0,0), f"Design: {name}", font=FNT["xs"])
    draw.text((W-bbox2[2]-80, H-52), f"Design: {name}", font=FNT["xs"], fill=ds["text_dim"])

    return img

# ── 전체 생성 ─────────────────────────────────────────────────
paths = {}
for key, ds in DESIGN_SYSTEMS.items():
    name = ds["name"]
    d = os.path.join(OUT, key)
    os.makedirs(d, exist_ok=True)

    s1 = slide_title(ds, name)
    s2 = slide_content(ds, name)
    s3 = slide_section(ds, name)

    p1 = os.path.join(d, "01_title.png")
    p2 = os.path.join(d, "02_content.png")
    p3 = os.path.join(d, "03_section.png")

    s1.save(p1); s2.save(p2); s3.save(p3)
    paths[key] = [p1, p2, p3]
    print(f"[{name}] ✓ 3장 생성 → {d}")

# ── 비교 그리드 (5×3 = 15장을 하나의 이미지로) ───────────────
print("\n비교 그리드 생성 중...")
ROWS = len(DESIGN_SYSTEMS)   # 5
COLS = 3
THUMB_W, THUMB_H = 600, 338  # 16:9 썸네일
PAD = 20
LABEL_H = 50

grid_w = COLS * THUMB_W + (COLS+1) * PAD
grid_h = ROWS * (THUMB_H + LABEL_H) + (ROWS+1) * PAD + 60  # 상단 제목 여백

grid = Image.new("RGB", (grid_w, grid_h), (30, 32, 36))
draw_g = ImageDraw.Draw(grid)

# 상단 제목
cx(draw_g, "강의 슬라이드 디자인 시스템 비교", load_font(32), 14, (220,220,220), grid_w)

slide_labels = ["01 타이틀", "02 콘텐츠", "03 섹션"]
systems_order = list(DESIGN_SYSTEMS.keys())

for row, key in enumerate(systems_order):
    ds = DESIGN_SYSTEMS[key]
    name = ds["name"]
    desc = ds["desc"]
    gy = 60 + PAD + row * (THUMB_H + LABEL_H + PAD)

    for col, slide_path in enumerate(paths[key]):
        gx = PAD + col * (THUMB_W + PAD)

        # 썸네일
        thumb = Image.open(slide_path).resize((THUMB_W, THUMB_H), Image.LANCZOS)
        grid.paste(thumb, (gx, gy + LABEL_H))

        # 슬라이드 레이블
        label = f"{name} — {slide_labels[col]}"
        label_fnt = load_font(18)
        draw_g.text((gx + 8, gy + 14), label, font=label_fnt, fill=(180, 185, 195))

grid_path = os.path.join(OUT, "_comparison_grid.png")
grid.save(grid_path)
print(f"비교 그리드 → {grid_path}")
print(f"크기: {grid.size}")
