#!/usr/bin/env python3
"""
Gray 디자인 시스템 강의 슬라이드 3장 생성
- 좌측 사이드바(22%) + 우측 콘텐츠(78%) 레이아웃
- 순백 배경 + 차콜 #333 액센트
- Korean PPT Minimal 스타일
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
OUT = "/tmp/Script-repo/output/comparison/gray"
os.makedirs(OUT, exist_ok=True)

# ── 디자인 토큰 ──────────────────────────────────────────────
BG          = (255, 255, 255)
BG_CARD     = (242, 242, 242)
BG_SIDEBAR  = (250, 250, 250)   # 사이드바 극연회
TEXT_H1     = (26, 26, 26)
TEXT_H2     = (34, 34, 34)
TEXT_BODY   = (68, 68, 68)
TEXT_LABEL  = (119, 119, 119)
TEXT_DIM    = (170, 170, 170)
ACCENT      = (51, 51, 51)      # #333 차콜 다크
BORDER      = (217, 217, 217)
SIDEBAR_W   = int(W * 0.22)     # 422px
CONTENT_X   = SIDEBAR_W + 60   # 콘텐츠 시작 X
CONTENT_W   = W - CONTENT_X - 80

# ── 폰트 ─────────────────────────────────────────────────────
def fnt(size, bold=False):
    candidates = ["/System/Library/Fonts/AppleSDGothicNeo.ttc"]
    for p in candidates:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: pass
    return ImageFont.load_default()

F = {
    "h1":    fnt(56),
    "h2":    fnt(38),
    "h3":    fnt(28),
    "label": fnt(22),
    "body":  fnt(24),
    "sm":    fnt(20),
    "xs":    fnt(16),
    "num":   fnt(64),
}

# ── 헬퍼 ─────────────────────────────────────────────────────
def tw(draw, text, font):
    return draw.textbbox((0,0), text, font=font)[2]

def th(draw, text, font):
    b = draw.textbbox((0,0), text, font=font)
    return b[3] - b[1]

def pill_tag(draw, x, y, text, font, filled=True):
    """다크 fill 또는 outline 태그"""
    padding_x, padding_y = 18, 7
    w = tw(draw, text, font) + padding_x*2
    h = th(draw, text, font) + padding_y*2
    if filled:
        draw.rounded_rectangle([x, y, x+w, y+h], radius=4, fill=ACCENT)
        draw.text((x+padding_x, y+padding_y), text, font=font, fill=(255,255,255))
    else:
        draw.rounded_rectangle([x, y, x+w, y+h], radius=4, outline=ACCENT, width=2)
        draw.text((x+padding_x, y+padding_y), text, font=font, fill=ACCENT)
    return w, h

def sidebar_layout(draw, category, title_lines, meta=None):
    """좌측 사이드바 공통 레이아웃"""
    # 사이드바 배경 (극연회)
    draw.rectangle([(0,0),(SIDEBAR_W, H)], fill=BG_SIDEBAR)
    # 사이드바↔콘텐츠 구분선
    draw.rectangle([(SIDEBAR_W, 0),(SIDEBAR_W+1, H)], fill=BORDER)

    # 카테고리 라벨 (영문 소문자, 회색)
    sx, sy = 52, 60
    draw.text((sx, sy), category, font=F["label"], fill=TEXT_LABEL)

    # 메인 타이틀 (굵고 큰 한글)
    ty = sy + 42
    for line in title_lines:
        draw.text((sx, ty), line, font=F["h2"], fill=TEXT_H1)
        ty += th(draw, line, F["h2"]) + 8

    # 구분선
    ty += 20
    draw.rectangle([(sx, ty),(SIDEBAR_W - 40, ty+1)], fill=BORDER)
    ty += 20

    # 메타 정보
    if meta:
        for k, v in meta.items():
            draw.text((sx, ty), k, font=F["xs"], fill=TEXT_LABEL)
            ty += th(draw, k, F["xs"]) + 4
            draw.text((sx, ty), v, font=F["sm"], fill=TEXT_BODY)
            ty += th(draw, v, F["sm"]) + 18

def divider(draw, x, y, w):
    draw.rectangle([(x, y),(x+w, y+1)], fill=BORDER)

# ════════════════════════════════════════════════════════
# SLIDE 01 — 타이틀 (챕터 오프닝)
# 좌: 챕터 정보 / 우: 핵심 메시지 + 숫자 강조
# ════════════════════════════════════════════════════════
def slide_01():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # 사이드바
    sidebar_layout(draw,
        category="Chapter 01",
        title_lines=["클로드 코드란", "무엇인가"],
        meta={
            "섹션": "에이전트 구조 이해",
            "예상시간": "15분",
        }
    )

    # 우측 콘텐츠 — 핵심 포인트 3개
    cx = CONTENT_X
    cy = 80

    # 상단 질문형 헤딩
    q = "챗지피티와 뭐가 다른가요?"
    draw.text((cx, cy), q, font=F["h1"], fill=TEXT_H1)
    cy += th(draw, q, F["h1"]) + 12
    draw.text((cx, cy), "에이전트 구조를 이해하면 답이 보입니다.", font=F["body"], fill=TEXT_BODY)
    cy += 56

    divider(draw, cx, cy, CONTENT_W)
    cy += 40

    # 3개 포인트 카드 (가로 배열)
    cards = [
        ("01", "파일 직접 접근", "터미널에서 실행\n파일 읽기·쓰기·실행"),
        ("02", "에이전트 루프", "계획 → 도구 선택\n→ 실행 → 확인 반복"),
        ("03", "컨텍스트 유지", "CLAUDE.md로\n프로젝트 기억 보존"),
    ]
    card_w = (CONTENT_W - 60) // 3
    for i, (num, title, desc) in enumerate(cards):
        cx2 = cx + i * (card_w + 30)
        cy2 = cy
        # 카드 박스
        card_h = 260
        draw.rounded_rectangle([cx2, cy2, cx2+card_w, cy2+card_h], radius=6,
                                fill=BG_CARD, outline=BORDER, width=1)
        # 번호
        draw.text((cx2+24, cy2+24), num, font=F["h2"], fill=ACCENT)
        # 구분선
        draw.rectangle([(cx2+24, cy2+74),(cx2+card_w-24, cy2+75)], fill=BORDER)
        # 제목
        draw.text((cx2+24, cy2+90), title, font=F["h3"], fill=TEXT_H1)
        # 설명
        dy = cy2 + 132
        for line in desc.split("\n"):
            draw.text((cx2+24, dy), line, font=F["sm"], fill=TEXT_BODY)
            dy += th(draw, line, F["sm"]) + 8

    cy += 300

    # 하단 핵심 메시지 (다크 배경)
    bar_h = 90
    draw.rectangle([(cx, cy),(cx+CONTENT_W, cy+bar_h)], fill=ACCENT)
    msg = "클로드 코드 = 조언하는 AI가 아니라, 직접 실행하는 AI"
    msg_w = tw(draw, msg, F["body"])
    draw.text((cx + (CONTENT_W - msg_w)//2, cy + (bar_h - th(draw, msg, F["body"]))//2),
              msg, font=F["body"], fill=(255,255,255))

    # 각주
    draw.text((cx, H-40), "패스트캠퍼스 × DataBridge — Claude Code 실무 완성", font=F["xs"], fill=TEXT_DIM)

    return img

# ════════════════════════════════════════════════════════
# SLIDE 02 — 콘텐츠 (에이전트 구조 비교)
# 좌: 섹션 정보 / 우: 2컬럼 비교 (챗지피티 vs 클로드 코드)
# ════════════════════════════════════════════════════════
def slide_02():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    sidebar_layout(draw,
        category="Slide 01",
        title_lines=["두 도구의", "구조적 차이"],
        meta={
            "핵심": "에이전트 vs 챗봇",
        }
    )

    cx = CONTENT_X
    cy = 60

    # 상단 태그 + 질문
    pill_tag(draw, cx, cy, "도구 비교", F["xs"], filled=True)
    cy += 44
    draw.text((cx, cy), "챗지피티와 클로드 코드, 어떻게 다른가?", font=F["h2"], fill=TEXT_H1)
    cy += th(draw, "챗지피티와 클로드 코드, 어떻게 다른가?", F["h2"]) + 8
    draw.text((cx, cy), "같은 AI처럼 보이지만 작동 방식 자체가 다릅니다.", font=F["body"], fill=TEXT_BODY)
    cy += 52

    divider(draw, cx, cy, CONTENT_W)
    cy += 36

    # 2컬럼 비교
    col_w = (CONTENT_W - 48) // 2
    col1_x = cx
    col2_x = cx + col_w + 48

    # 컬럼 헤딩
    for colx, label, color in [(col1_x, "챗지피티", TEXT_LABEL), (col2_x, "클로드 코드", ACCENT)]:
        draw.text((colx, cy), label, font=F["h3"], fill=color)

    cy += 52
    divider(draw, col1_x, cy, CONTENT_W)
    # 중간 수직 구분선
    mid = col2_x - 24
    draw.rectangle([(mid, cy-30),(mid+1, H-60)], fill=BORDER)
    cy += 28

    # 비교 항목
    rows = [
        ("실행 환경", "웹 브라우저 / 앱", "터미널 (로컬 환경)"),
        ("파일 접근", "불가능", "직접 읽기·쓰기·실행"),
        ("작업 방식", "텍스트 답변 생성", "실제 작업 수행"),
        ("기억 유지", "세션 내에서만", "CLAUDE.md로 영구 보존"),
        ("적합한 용도", "정보 검색, 조언", "데이터 분석, 자동화"),
    ]
    for attr, v1, v2 in rows:
        # 항목명 (회색, 좌)
        draw.text((col1_x, cy), attr, font=F["sm"], fill=TEXT_LABEL)
        cy2 = cy + 30
        # 챗지피티 값
        draw.text((col1_x, cy2), v1, font=F["body"], fill=TEXT_BODY)
        # 클로드 코드 값
        draw.text((col2_x, cy2), v2, font=F["body"], fill=TEXT_H1)
        cy += 88
        divider(draw, col1_x, cy-8, CONTENT_W)

    # 하단 인사이트
    ins = '"클로드 코드는 조언자가 아니라 실행자입니다."'
    ins_w = tw(draw, ins, F["h3"])
    ins_x = cx + (CONTENT_W - ins_w) // 2
    draw.text((ins_x, H - 80), ins, font=F["h3"], fill=TEXT_LABEL)

    return img

# ════════════════════════════════════════════════════════
# SLIDE 03 — 에이전트 루프 다이어그램
# 좌: 섹션 정보 / 우: 플로우 다이어그램 + 결과 표
# ════════════════════════════════════════════════════════
def slide_03():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    sidebar_layout(draw,
        category="Slide 02",
        title_lines=["에이전트는", "어떻게", "작동하는가"],
        meta={
            "핵심 개념": "에이전트 루프",
            "비유": "사람이 일하는 방식",
        }
    )

    cx = CONTENT_X
    cy = 60

    # 태그
    pill_tag(draw, cx, cy, "에이전트 구조", F["xs"], filled=True)
    cy += 46

    # 헤딩
    draw.text((cx, cy), "사용자 지시를 받으면 스스로 계획하고 실행합니다", font=F["h2"], fill=TEXT_H1)
    cy += th(draw, "사용자 지시를 받으면 스스로 계획하고 실행합니다", F["h2"]) + 8
    draw.text((cx, cy), "이 사이클이 반복되는 것을 에이전트 루프라고 합니다.", font=F["body"], fill=TEXT_BODY)
    cy += 56

    divider(draw, cx, cy, CONTENT_W)
    cy += 44

    # 플로우 다이어그램 (5단계)
    steps = [
        ("사용자\n지시", "목표 전달"),
        ("계획", "순서 결정"),
        ("도구\n선택", "파일/코드/검색"),
        ("실행", "작업 수행"),
        ("결과\n확인", "완료 또는 반복"),
    ]
    box_w, box_h = 190, 110
    arrow_w = 44
    total = len(steps) * box_w + (len(steps)-1) * arrow_w
    sx = cx + (CONTENT_W - total) // 2
    by = cy

    for i, (label, sub) in enumerate(steps):
        bx = sx + i * (box_w + arrow_w)
        # 첫번째·마지막 = 다크, 나머지 = 카드 회색
        fill = ACCENT if i in (0, 4) else BG_CARD
        txt_color = (255,255,255) if i in (0, 4) else TEXT_H1
        sub_color = (200,200,200) if i in (0, 4) else TEXT_LABEL
        draw.rounded_rectangle([bx, by, bx+box_w, by+box_h], radius=6,
                                fill=fill, outline=BORDER, width=1)
        # 라벨 중앙
        for j, l in enumerate(label.split("\n")):
            lw = tw(draw, l, F["h3"])
            draw.text((bx+(box_w-lw)//2, by+16+j*34), l, font=F["h3"], fill=txt_color)
        # 서브
        sw = tw(draw, sub, F["xs"])
        draw.text((bx+(box_w-sw)//2, by+box_h-26), sub, font=F["xs"], fill=sub_color)

        # 화살표
        if i < len(steps)-1:
            ax = bx + box_w + 4
            ay = by + box_h//2
            draw.polygon([(ax,ay-8),(ax+36,ay),(ax,ay+8)], fill=TEXT_DIM)

    cy += box_h + 50

    # 설명 텍스트
    note = "클로드 코드는 이 루프를 자동으로 반복하며 복잡한 작업도 단계별로 처리합니다."
    draw.text((cx, cy), note, font=F["sm"], fill=TEXT_BODY)
    cy += 52

    divider(draw, cx, cy, CONTENT_W)
    cy += 32

    # 결과 표 (도구 목록)
    table_data = [
        ("파일 읽기·쓰기",    "텍스트, CSV, 코드 등 직접 접근"),
        ("터미널 실행",       "Shell 명령어, Python 스크립트"),
        ("코드베이스 검색",   "특정 내용 담긴 파일 탐색"),
        ("웹 검색 (선택)",   "MCP 연동 시 외부 정보 수집"),
    ]
    row_h = 50
    col1w = 320
    # 헤더
    draw.rectangle([(cx, cy),(cx+CONTENT_W, cy+row_h)], fill=ACCENT)
    draw.text((cx+20, cy+14), "도구", font=F["sm"], fill=(255,255,255))
    draw.text((cx+col1w+20, cy+14), "설명", font=F["sm"], fill=(255,255,255))
    cy += row_h
    for i, (tool, desc) in enumerate(table_data):
        fill = BG_CARD if i % 2 == 0 else BG
        draw.rectangle([(cx, cy),(cx+CONTENT_W, cy+row_h)], fill=fill)
        draw.rectangle([(cx, cy),(cx+CONTENT_W, cy+row_h)], outline=BORDER, width=1)
        draw.text((cx+20, cy+14), tool, font=F["sm"], fill=TEXT_H1)
        draw.text((cx+col1w+20, cy+14), desc, font=F["sm"], fill=TEXT_BODY)
        cy += row_h

    draw.text((cx, H-40), "패스트캠퍼스 × DataBridge — Claude Code 실무 완성",
              font=F["xs"], fill=TEXT_DIM)
    return img

# ── 생성 & 저장 ──────────────────────────────────────────────
print("Gray 슬라이드 생성 중...")
slides = [
    ("01_title.png",   slide_01()),
    ("02_content.png", slide_02()),
    ("03_section.png", slide_03()),
]
for fname, img in slides:
    path = os.path.join(OUT, fname)
    img.save(path)
    print(f"  ✓ {fname}")

print(f"\n완료 → {OUT}")
