#!/usr/bin/env python3
"""
v2 — 내용-레이아웃 일치 원칙
- 텍스트/도식 겹침 없음
- 레이아웃은 내용에 복무
- 안전 여백 철저 준수
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from design_systems import DESIGN_SYSTEMS, W, H, s, FS
from PIL import Image, ImageDraw, ImageFont

OUT = "/tmp/Script-repo/output/v2"

# ── 폰트 ──────────────────────────────────────────────────────
_fc = {}
def F(size):
    if size not in _fc:
        for p in ["/System/Library/Fonts/AppleSDGothicNeo.ttc"]:
            if os.path.exists(p):
                try: _fc[size] = ImageFont.truetype(p, size); break
                except: pass
        if size not in _fc: _fc[size] = ImageFont.load_default()
    return _fc[size]

def tw(d, t, sz): return d.textbbox((0,0),t,font=F(sz))[2]
def th_fn(d, t, sz): b=d.textbbox((0,0),t,font=F(sz)); return b[3]-b[1]

def draw_text(d, x, y, text, sz, color):
    d.text((x,y), text, font=F(sz), fill=color)
    return th_fn(d, text, sz)

def draw_wrapped(d, x, y, text, sz, color, max_w, gap=s(6)):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur+" "+w).strip()
        if tw(d,test,sz) > max_w and cur: lines.append(cur); cur=w
        else: cur=test
    if cur: lines.append(cur)
    for line in lines:
        d.text((x,y), line, font=F(sz), fill=color)
        y += th_fn(d,line,sz) + gap
    return y

def hrule(d, x, y, w, color, h=1):
    d.rectangle([x,y,x+w,y+h], fill=color)

def pill_tag(d, x, y, text, sz, ds, filled=True):
    pw = tw(d,text,sz)+s(20)*2
    ph = th_fn(d,text,sz)+s(8)*2
    if filled:
        d.rounded_rectangle([x,y,x+pw,y+ph], radius=s(4), fill=ds["tag_fill_bg"])
        d.text((x+s(20),y+s(8)), text, font=F(sz), fill=ds["tag_fill_txt"])
    else:
        d.rounded_rectangle([x,y,x+pw,y+ph], radius=s(4), outline=ds["accent"], width=2)
        d.text((x+s(20),y+s(8)), text, font=F(sz), fill=ds["tag_out_txt"])
    return pw, ph

# ── 공통 사이드바 ──────────────────────────────────────────────
SIDEBAR_W  = s(310)
CONTENT_X  = s(380)
MARGIN     = s(52)

def sidebar(d, ds, category, title_lines, body="", meta=None):
    d.rectangle([0,0,SIDEBAR_W,H], fill=ds["bg_sidebar"])
    d.rectangle([SIDEBAR_W,0,SIDEBAR_W+s(1),H], fill=ds["border"])
    x, y = MARGIN, s(52)

    # 카테고리
    draw_text(d, x, y, category, FS["category"], ds["text_label"])
    y += th_fn(d,category,FS["category"]) + s(10)

    # 타이틀 — 줄별
    for line in title_lines:
        draw_text(d, x, y, line, FS["h1"], ds["text_primary"])
        y += th_fn(d,line,FS["h1"]) + s(6)
    y += s(12)

    # 본문
    if body:
        y = draw_wrapped(d, x, y, body, FS["sm"], ds["text_body"],
                         SIDEBAR_W - x - s(16), gap=s(7))
        y += s(14)

    # 구분선
    hrule(d, x, y, SIDEBAR_W-x-s(16), ds["border"])
    y += s(18)

    # 메타
    if meta:
        for k,v in meta.items():
            draw_text(d, x, y, k, FS["xs"], ds["text_label"])
            y += th_fn(d,k,FS["xs"]) + s(4)
            y = draw_wrapped(d, x, y, v, FS["sm"], ds["text_body"],
                             SIDEBAR_W-x-s(16), gap=s(5))
            y += s(14)

# ── 공통 푸터 ──────────────────────────────────────────────────
def footer(d, ds):
    d.text((MARGIN, H-s(32)), "DataBridge × Fastcampus — Claude Code 실무 완성",
           font=F(FS["xs"]), fill=ds["text_dim"])

# ════════════════════════════════════════════════════════════════
# SLIDE 01 — 챗지피티 vs 클로드 코드 (사이드바 + 2컬럼 비교)
# 레이아웃 근거: 레퍼런스 Painpoint 1-2의 좌우 비교 구조
#               대비가 뚜렷한 2개 대상 비교에 최적
# ════════════════════════════════════════════════════════════════
def slide_01(ds):
    img = Image.new("RGB",(W,H), ds["bg"])
    d = ImageDraw.Draw(img)

    sidebar(d, ds,
        category="Chapter 01",
        title_lines=["두 도구의", "차이"],
        body="같은 AI처럼 보이지만 구조가 완전히 다릅니다.",
        meta={"핵심": "조언 vs 실행"})
    footer(d, ds)

    # ── 우측 콘텐츠 ──
    cx = CONTENT_X
    cy = s(52)
    cw = W - cx - MARGIN

    # 태그 + 헤딩
    _, ph = pill_tag(d, cx, cy, "도구 비교", FS["tag"], ds, filled=True)
    cy += ph + s(18)
    draw_text(d, cx, cy, "챗지피티 vs 클로드 코드", FS["h2"], ds["text_primary"])
    cy += th_fn(d,"챗지피티 vs 클로드 코드",FS["h2"]) + s(8)
    hrule(d, cx, cy, cw, ds["border"])
    cy += s(28)

    # 2컬럼 — 컬럼 너비 계산
    col_gap = s(48)
    col_w   = (cw - col_gap) // 2
    c1x, c2x = cx, cx + col_w + col_gap

    # 수직 구분선
    mid_x = cx + col_w + col_gap//2
    line_top = cy - s(8)

    # 헤딩
    draw_text(d, c1x, cy, "챗지피티", FS["h3"], ds["text_label"])
    draw_text(d, c2x, cy, "클로드 코드", FS["h3"], ds["accent"])
    cy += th_fn(d,"A",FS["h3"]) + s(20)

    rows = [
        ("실행 환경", "웹 브라우저 / 앱",       "터미널 (로컬 환경)"),
        ("파일 접근", "불가능",                 "직접 읽기·쓰기·실행"),
        ("작업 결과", "텍스트 답변 생성",        "실제 파일·코드 변경"),
        ("기억 유지", "세션 내에서만",           "CLAUDE.md 영구 보존"),
        ("주요 용도", "정보 검색, 아이디어",     "데이터 분석, 자동화"),
    ]
    row_h = s(64)
    for i, (attr, v1, v2) in enumerate(rows):
        row_y = cy + i*row_h
        # 교대 배경
        if i%2==0:
            d.rectangle([c1x, row_y, c1x+col_w, row_y+row_h], fill=ds["bg_card"])
            d.rectangle([c2x, row_y, c2x+col_w, row_y+row_h], fill=ds["bg_card"])
        # 항목명 (위)
        draw_text(d, c1x+s(12), row_y+s(8), attr, FS["xs"], ds["text_label"])
        # 값
        draw_text(d, c1x+s(12), row_y+s(28), v1, FS["sm"], ds["text_body"])
        draw_text(d, c2x+s(12), row_y+s(8), attr, FS["xs"], ds["text_label"])
        draw_text(d, c2x+s(12), row_y+s(28), v2, FS["sm"], ds["text_primary"])
        hrule(d, c1x, row_y+row_h, col_w, ds["border"])
        hrule(d, c2x, row_y+row_h, col_w, ds["border"])

    cy += len(rows)*row_h + s(8)

    # 수직 구분선 (행 범위 한정)
    d.rectangle([mid_x, line_top, mid_x+s(1), cy], fill=ds["border"])

    # 결론 바
    cy += s(18)
    bar_h = s(66)
    d.rounded_rectangle([cx,cy,cx+cw,cy+bar_h], radius=s(6), fill=ds["accent"])
    msg = "핵심: 클로드 코드는 조언자가 아니라 실제로 실행하는 도구입니다."
    mw = tw(d,msg,FS["sm"])
    d.text((cx+(cw-mw)//2, cy+(bar_h-th_fn(d,msg,FS["sm"]))//2),
           msg, font=F(FS["sm"]), fill=ds["tag_fill_txt"])

    return img

# ════════════════════════════════════════════════════════════════
# SLIDE 02 — 에이전트 루프 구조 (사이드바 + 번호리스트 01~04)
# 레이아웃 근거: 레퍼런스 번호리스트(01/02/03) 구조
#               순서가 있는 단계별 프로세스에 최적
# ════════════════════════════════════════════════════════════════
def slide_02(ds):
    img = Image.new("RGB",(W,H), ds["bg"])
    d = ImageDraw.Draw(img)

    sidebar(d, ds,
        category="Chapter 01",
        title_lines=["에이전트", "루프"],
        body="클로드 코드가 지시를 받아서 완료까지 처리하는 내부 사이클입니다.",
        meta={"비유": "실무자가\n일하는 방식", "반복": "완료 또는\n다음 단계로"})
    footer(d, ds)

    cx = CONTENT_X
    cy = s(52)
    cw = W - cx - MARGIN

    # 태그 + 헤딩
    _, ph = pill_tag(d, cx, cy, "작동 방식", FS["tag"], ds, filled=True)
    cy += ph + s(18)
    draw_text(d, cx, cy, "사용자 지시를 받으면 어떻게 처리하는가", FS["h2"], ds["text_primary"])
    cy += th_fn(d,"A",FS["h2"]) + s(8)
    d.text((cx, cy), "에이전트는 이 사이클을 자동으로 반복하며 복잡한 작업도 완료합니다.",
           font=F(FS["sm"]), fill=ds["text_body"])
    cy += th_fn(d,"A",FS["sm"]) + s(28)

    # ── 번호 리스트 ──
    NUM_W    = s(48)    # "01" 컬럼
    TITLE_W  = s(200)   # 단계명 컬럼
    TITLE_GAP= s(36)
    DESC_X   = cx + NUM_W + s(24) + TITLE_W + TITLE_GAP
    DESC_W   = cw - (DESC_X - cx)

    steps = [
        ("01", "사용자 지시",  "자연어로 목표를 전달합니다.\n예: \"data.csv 분석해서 리포트 만들어줘\""),
        ("02", "계획 수립",    "어떤 순서로 할지 스스로 결정합니다.\n파일 읽기 → 분석 → 저장 순으로 계획합니다."),
        ("03", "도구 실행",    "파일 읽기, 코드 실행, 파일 저장 등\n필요한 도구를 선택해 직접 수행합니다."),
        ("04", "결과 확인",    "실행 결과를 확인하고 완료하거나\n오류 시 원인을 파악해 재시도합니다."),
    ]
    row_h = s(100)

    hrule(d, cx, cy, cw, ds["border"])

    for i, (num, title, desc) in enumerate(steps):
        row_y = cy + s(1)
        row_y_start = row_y + s(18)

        # 번호
        draw_text(d, cx, row_y_start, num, FS["num"], ds["num_txt"])

        # 제목
        tx = cx + NUM_W + s(24)
        draw_text(d, tx, row_y_start, title, FS["h3"], ds["text_primary"])

        # 설명 — 2줄 최대, DESC_W 내에서 wrap
        dx = tx + TITLE_W + TITLE_GAP
        dy = row_y_start
        for line in desc.split("\n"):
            d.text((dx, dy), line, font=F(FS["sm"]), fill=ds["text_body"])
            dy += th_fn(d, line, FS["sm"]) + s(5)

        cy += row_h
        hrule(d, cx, cy, cw, ds["border"])

    # 루프 화살표 힌트
    cy += s(20)
    hint = "↺  이 사이클이 반복되는 것을 에이전트 루프라고 합니다."
    draw_text(d, cx, cy, hint, FS["sm"], ds["text_label"])

    return img

# ════════════════════════════════════════════════════════════════
# SLIDE 03 — 클로드 코드 도구 목록 (사이드바 + 카드 그리드)
# 레이아웃 근거: 레퍼런스 카드 + 플로우 다이어그램 구조
#               병렬로 존재하는 도구들, 위계 없는 나열에 최적
# ════════════════════════════════════════════════════════════════
def slide_03(ds):
    img = Image.new("RGB",(W,H), ds["bg"])
    d = ImageDraw.Draw(img)

    sidebar(d, ds,
        category="Chapter 01",
        title_lines=["내장", "도구 목록"],
        body="에이전트는 도구를 조합해 작업을 수행합니다. 클로드 코드가 기본으로 가진 도구들입니다.",
        meta={"도구 수": "6개 기본 제공", "확장": "MCP로 추가 가능"})
    footer(d, ds)

    cx = CONTENT_X
    cy = s(52)
    cw = W - cx - MARGIN

    _, ph = pill_tag(d, cx, cy, "기본 도구", FS["tag"], ds, filled=True)
    cy += ph + s(18)
    draw_text(d, cx, cy, "클로드 코드가 기본으로 탑재한 6가지 도구", FS["h2"], ds["text_primary"])
    cy += th_fn(d,"A",FS["h2"]) + s(8)
    hrule(d, cx, cy, cw, ds["border"])
    cy += s(30)

    # 카드 그리드 — 3×2
    cards = [
        ("파일 읽기",      "텍스트·CSV·코드 파일을\n직접 열어서 내용 확인"),
        ("파일 쓰기",      "새 파일 생성 또는\n기존 파일 수정·저장"),
        ("파일 검색",      "특정 내용이 담긴\n파일을 프로젝트에서 탐색"),
        ("터미널 실행",    "셸 명령어 및\nPython 스크립트 실행"),
        ("코드베이스 검색","프로젝트 전체에서\n함수·변수·패턴 탐색"),
        ("웹 검색",        "MCP 설정 시\n외부 정보 실시간 수집"),
    ]

    COLS  = 3
    CARD_GAP_X = s(24)
    CARD_GAP_Y = s(20)
    card_w = (cw - CARD_GAP_X*(COLS-1)) // COLS
    card_h = s(148)

    for i, (title, desc) in enumerate(cards):
        col = i % COLS
        row = i // COLS
        bx = cx + col*(card_w + CARD_GAP_X)
        by = cy + row*(card_h + CARD_GAP_Y)

        # 카드 박스
        d.rounded_rectangle([bx,by,bx+card_w,by+card_h], radius=s(6),
                             fill=ds["bg_card"], outline=ds["border"], width=s(1))

        # 인덱스 번호 (작게)
        idx = f"{i+1:02d}"
        d.text((bx+s(18), by+s(14)), idx, font=F(FS["xs"]), fill=ds["text_label"])

        # 제목
        draw_text(d, bx+s(18), by+s(38), title, FS["h3"], ds["text_primary"])

        # 설명 (줄바꿈 안전)
        desc_y = by + s(38) + th_fn(d, title, FS["h3"]) + s(12)
        for line in desc.split("\n"):
            if desc_y + th_fn(d,line,FS["sm"]) < by+card_h-s(10):
                d.text((bx+s(18), desc_y), line, font=F(FS["sm"]), fill=ds["text_body"])
                desc_y += th_fn(d, line, FS["sm"]) + s(5)

    return img

# ── 생성 ──────────────────────────────────────────────────────
for key, ds in DESIGN_SYSTEMS.items():
    out = os.path.join(OUT, key)
    os.makedirs(out, exist_ok=True)
    print(f"\n[{ds['name']}]")
    for slug, fn in [("01_compare", slide_01),
                     ("02_process", slide_02),
                     ("03_tools",   slide_03)]:
        img = fn(ds)
        p = os.path.join(out, f"{slug}.png")
        img.save(p)
        print(f"  ✓ {slug}.png")
print("\n완료")
