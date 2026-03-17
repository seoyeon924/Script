#!/usr/bin/env python3
"""
v2 — Pretendard 폰트 + 레퍼런스 위계 정확 적용
라벨(14 Regular #888) / 타이틀(30 Bold #111) / 서브(18 SemiBold #1A1A1A)
본문(14 Regular #333) / 메타(12 Regular #888)
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from design_systems import DESIGN_SYSTEMS, W, H, s, FS, FW, FONTS
from design_systems import GRAY_COLOR, ORANGE_COLOR
from PIL import Image, ImageDraw, ImageFont

OUT = "/tmp/Script-repo/output/v2"

# ── 폰트 캐시 ─────────────────────────────────────────────────
_fc = {}
def F(size, weight="regular"):
    key = (size, weight)
    if key not in _fc:
        path = FONTS.get(weight, FONTS["fallback"])
        if not os.path.exists(path):
            path = FONTS["fallback"]
        try:
            _fc[key] = ImageFont.truetype(path, size)
        except:
            _fc[key] = ImageFont.load_default()
    return _fc[key]

def Fk(key):
    """FS 키로 폰트 반환"""
    return F(FS[key], FW[key])

# ── 색상 헬퍼 ─────────────────────────────────────────────────
def C(ds, key):
    """디자인 시스템에서 텍스트 색상 반환"""
    cmap = GRAY_COLOR if ds["name"]=="Gray" else ORANGE_COLOR
    return cmap.get(key, ds["text_primary"])

# ── 텍스트 유틸 ───────────────────────────────────────────────
def tw(d, t, key):
    return d.textbbox((0,0), t, font=Fk(key))[2]

def th(d, t, key):
    b = d.textbbox((0,0), t, font=Fk(key))
    return b[3] - b[1]

def put(d, x, y, text, key, color):
    d.text((x,y), text, font=Fk(key), fill=color)
    return th(d, text, key)

def wrap(d, text, key, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur+" "+w).strip()
        if d.textbbox((0,0),test,font=Fk(key))[2] > max_w and cur:
            lines.append(cur); cur = w
        else: cur = test
    if cur: lines.append(cur)
    return lines

def put_wrap(d, x, y, text, key, color, max_w, lh_mul=1.7):
    for line in wrap(d, text, key, max_w):
        d.text((x,y), line, font=Fk(key), fill=color)
        y += int(th(d, line, key) * lh_mul)
    return y

def hrule(d, x, y, w, color, h=s(1)):
    d.rectangle([x, y, x+w, y+h], fill=color)

# ── Pill 태그 ──────────────────────────────────────────────────
def pill(d, x, y, text, ds, filled=True):
    px, py, r = s(18), s(8), s(4)
    pw = tw(d,text,"tag") + px*2
    ph = th(d,text,"tag") + py*2
    if filled:
        d.rounded_rectangle([x,y,x+pw,y+ph], radius=r, fill=ds["tag_fill_bg"])
        d.text((x+px, y+py), text, font=Fk("tag"), fill=ds["tag_fill_txt"])
    else:
        d.rounded_rectangle([x,y,x+pw,y+ph], radius=r, outline=ds["accent"], width=s(2))
        d.text((x+px, y+py), text, font=Fk("tag"), fill=ds["tag_out_txt"])
    return pw, ph

# ── 사이드바 ──────────────────────────────────────────────────
SIDEBAR_W = s(300)
CONTENT_X = s(370)
MARGIN    = s(52)

def sidebar(d, ds, category, title_lines, body="", meta=None):
    d.rectangle([0,0,SIDEBAR_W,H], fill=ds["bg_sidebar"])
    d.rectangle([SIDEBAR_W,0,SIDEBAR_W+s(1),H], fill=ds["border"])

    x, y = MARGIN, s(52)
    # 카테고리 라벨 — Regular 14px #888
    put(d, x, y, category, "category", C(ds,"category"))
    y += int(th(d,category,"category") * 1.5) + s(10)

    # 메인 타이틀 — Bold 30px #111  line-height 1.4
    for line in title_lines:
        put(d, x, y, line, "h1", C(ds,"h1"))
        y += int(th(d,line,"h1") * 1.4)
    y += s(16)

    # 본문 — Regular 14px #333  line-height 1.75
    if body:
        y = put_wrap(d, x, y, body, "body", C(ds,"body"),
                     SIDEBAR_W-x-s(16), lh_mul=1.75)
        y += s(14)

    # 구분선
    hrule(d, x, y, SIDEBAR_W-x-s(16), ds["border"])
    y += s(16)

    # 메타 — Regular 12px #888
    if meta:
        for k,v in meta.items():
            put(d, x, y, k, "xs", C(ds,"meta"))
            y += th(d,k,"xs") + s(4)
            y = put_wrap(d, x, y, v, "sm", C(ds,"body"),
                         SIDEBAR_W-x-s(16), lh_mul=1.6)
            y += s(12)

def footer(d, ds):
    put(d, MARGIN, H-s(36),
        "DataBridge × Fastcampus — Claude Code 실무 완성",
        "xs", C(ds,"xs"))

# ════════════════════════════════════════════════════════════════
# SLIDE 01 — 챗지피티 vs 클로드 코드 (사이드바 + 2컬럼 비교)
# ════════════════════════════════════════════════════════════════
def slide_01(ds):
    img = Image.new("RGB",(W,H), ds["bg"])
    d   = ImageDraw.Draw(img)
    sidebar(d, ds,
        category="Chapter 01",
        title_lines=["두 도구의", "차이"],
        body="같은 AI처럼 보이지만\n구조가 완전히 다릅니다.",
        meta={"핵심": "조언 vs 실행"})
    footer(d, ds)

    cx = CONTENT_X
    cy = s(52)
    cw = W - cx - MARGIN

    # 태그 + 헤딩
    _, ph = pill(d, cx, cy, "도구 비교", ds, filled=True)
    cy += ph + s(18)
    put(d, cx, cy, "챗지피티 vs 클로드 코드", "h2", C(ds,"h2"))
    cy += int(th(d,"챗지피티 vs 클로드 코드","h2")*1.4) + s(6)
    hrule(d, cx, cy, cw, ds["border"])
    cy += s(28)

    # 2컬럼
    col_gap = s(56)
    col_w   = (cw - col_gap) // 2
    c1x     = cx
    c2x     = cx + col_w + col_gap

    # 수직 구분선 범위 기록
    vline_top = cy

    # 컬럼 헤딩 — SemiBold 18px
    put(d, c1x, cy, "챗지피티", "h3", C(ds,"meta"))
    put(d, c2x, cy, "클로드 코드", "h3", ds["accent"])
    cy += int(th(d,"A","h3")*1.4) + s(12)

    rows = [
        ("실행 환경",  "웹 브라우저 / 앱",      "터미널 (로컬 환경)"),
        ("파일 접근",  "불가능",                "직접 읽기·쓰기·실행"),
        ("작업 결과",  "텍스트 답변 생성",       "실제 파일·코드 변경"),
        ("기억 유지",  "세션 내에서만",          "CLAUDE.md 영구 보존"),
        ("주요 용도",  "정보 검색·아이디어",     "데이터 분석·자동화"),
    ]
    row_h = s(68)
    for i, (attr, v1, v2) in enumerate(rows):
        ry = cy + i*row_h
        # 교대 배경
        if i%2 == 0:
            d.rectangle([c1x, ry, c1x+col_w, ry+row_h], fill=ds["bg_card"])
            d.rectangle([c2x, ry, c2x+col_w, ry+row_h], fill=ds["bg_card"])
        # 항목명 — xs Regular #888
        put(d, c1x+s(14), ry+s(10), attr, "xs", C(ds,"meta"))
        # 값 — body Regular #333
        put(d, c1x+s(14), ry+s(28), v1, "body", C(ds,"body"))
        put(d, c2x+s(14), ry+s(10), attr, "xs", C(ds,"meta"))
        put(d, c2x+s(14), ry+s(28), v2, "body", C(ds,"h3"))
        hrule(d, c1x, ry+row_h, col_w, ds["border"])
        hrule(d, c2x, ry+row_h, col_w, ds["border"])

    cy += len(rows)*row_h
    # 수직 구분선 (그리기)
    mid_x = c2x - col_gap//2
    d.rectangle([mid_x, vline_top, mid_x+s(1), cy], fill=ds["border"])

    # 결론 바
    cy += s(20)
    bar_h = s(64)
    d.rounded_rectangle([cx, cy, cx+cw, cy+bar_h], radius=s(6), fill=ds["accent"])
    msg = "핵심 — 클로드 코드는 조언자가 아니라 직접 실행하는 도구입니다."
    mw  = d.textbbox((0,0),msg,font=Fk("sm"))[2]
    d.text((cx+(cw-mw)//2, cy+(bar_h-th(d,msg,"sm"))//2),
           msg, font=Fk("sm"), fill=ds["tag_fill_txt"])
    return img

# ════════════════════════════════════════════════════════════════
# SLIDE 02 — 에이전트 루프 4단계 (사이드바 + 번호리스트)
# ════════════════════════════════════════════════════════════════
def slide_02(ds):
    img = Image.new("RGB",(W,H), ds["bg"])
    d   = ImageDraw.Draw(img)
    sidebar(d, ds,
        category="Chapter 01",
        title_lines=["에이전트", "루프"],
        body="지시를 받아서 완료까지\n스스로 처리하는 사이클입니다.",
        meta={"비유": "실무자가 일하는 방식"})
    footer(d, ds)

    cx = CONTENT_X
    cy = s(52)
    cw = W - cx - MARGIN

    _, ph = pill(d, cx, cy, "작동 방식", ds, filled=True)
    cy += ph + s(18)
    put(d, cx, cy, "사용자 지시를 받으면 어떻게 처리하는가", "h2", C(ds,"h2"))
    cy += int(th(d,"A","h2")*1.4) + s(6)
    put_wrap(d, cx, cy, "에이전트는 이 사이클을 자동 반복하며 복잡한 작업도 단계별로 처리합니다.",
             "sm", C(ds,"body"), cw, lh_mul=1.6)
    cy += th(d,"A","sm") + s(28)

    # 번호 리스트
    NUM_W     = s(52)
    GAP1      = s(28)
    TITLE_W   = s(195)
    GAP2      = s(40)
    DESC_X    = cx + NUM_W + GAP1 + TITLE_W + GAP2
    DESC_W    = cw - (DESC_X - cx)
    ROW_H     = s(96)

    steps = [
        ("01", "사용자 지시",
         "자연어로 목표를 전달합니다.\n예: \"data.csv 분석해서 리포트 만들어줘\""),
        ("02", "계획 수립",
         "어떤 순서로 할지 스스로 결정합니다.\n파일 읽기 → 분석 코드 실행 → 결과 저장 순으로 계획합니다."),
        ("03", "도구 실행",
         "파일 읽기, 코드 실행, 파일 저장 등\n필요한 도구를 선택해 직접 수행합니다."),
        ("04", "결과 확인",
         "실행 결과를 확인하고 완료하거나,\n오류 시 원인을 파악해 자동으로 재시도합니다."),
    ]

    hrule(d, cx, cy, cw, ds["border"])
    for num, title, desc in steps:
        row_y = cy + s(1) + s(20)

        # 번호 — SemiBold 18px #1A1A1A
        put(d, cx, row_y, num, "num", C(ds,"h3"))

        # 제목 — SemiBold 18px #1A1A1A
        tx = cx + NUM_W + GAP1
        put(d, tx, row_y, title, "h3", C(ds,"h3"))

        # 설명 — Regular 14px #333, line-height 1.75
        dx = tx + TITLE_W + GAP2
        dy = row_y
        for line in desc.split("\n"):
            d.text((dx, dy), line, font=Fk("sm"), fill=C(ds,"body"))
            dy += int(th(d,line,"sm") * 1.75)

        cy += ROW_H
        hrule(d, cx, cy, cw, ds["border"])

    cy += s(22)
    put(d, cx, cy, "↺  이 사이클이 반복되는 것을 에이전트 루프라고 합니다.",
        "sm", C(ds,"meta"))
    return img

# ════════════════════════════════════════════════════════════════
# SLIDE 03 — 내장 도구 목록 (사이드바 + 카드 그리드 3×2)
# ════════════════════════════════════════════════════════════════
def slide_03(ds):
    img = Image.new("RGB",(W,H), ds["bg"])
    d   = ImageDraw.Draw(img)
    sidebar(d, ds,
        category="Chapter 01",
        title_lines=["내장", "도구 목록"],
        body="에이전트는 도구를 조합해 작업합니다.\n기본 6가지 도구를 제공합니다.",
        meta={"확장": "MCP로 추가 가능"})
    footer(d, ds)

    cx = CONTENT_X
    cy = s(52)
    cw = W - cx - MARGIN

    _, ph = pill(d, cx, cy, "기본 도구", ds, filled=True)
    cy += ph + s(18)
    put(d, cx, cy, "클로드 코드가 기본으로 탑재한 6가지 도구", "h2", C(ds,"h2"))
    cy += int(th(d,"A","h2")*1.4) + s(8)
    hrule(d, cx, cy, cw, ds["border"])
    cy += s(28)

    cards = [
        ("파일 읽기",     "텍스트·CSV·코드 파일을\n직접 열어서 내용 확인"),
        ("파일 쓰기",     "새 파일 생성 또는\n기존 파일 수정·저장"),
        ("파일 검색",     "특정 내용이 담긴\n파일을 프로젝트에서 탐색"),
        ("터미널 실행",   "셸 명령어 및\nPython 스크립트 실행"),
        ("코드베이스 검색","프로젝트 전체에서\n함수·변수·패턴 탐색"),
        ("웹 검색",       "MCP 설정 시\n외부 정보 실시간 수집"),
    ]

    COLS      = 3
    CARD_GAPX = s(20)
    CARD_GAPY = s(18)
    card_w    = (cw - CARD_GAPX*(COLS-1)) // COLS
    card_h    = s(158)

    for i, (title, desc) in enumerate(cards):
        col = i % COLS
        row = i // COLS
        bx  = cx + col*(card_w+CARD_GAPX)
        by  = cy + row*(card_h+CARD_GAPY)

        d.rounded_rectangle([bx,by,bx+card_w,by+card_h],
                             radius=s(6), fill=ds["bg_card"], outline=ds["border"], width=s(1))

        # 인덱스 — xs Regular #888
        put(d, bx+s(16), by+s(14), f"{i+1:02d}", "xs", C(ds,"meta"))

        # 제목 — SemiBold 18px #1A1A1A
        ty = by + s(14) + th(d,"A","xs") + s(12)
        put(d, bx+s(16), ty, title, "h3", C(ds,"h3"))

        # 설명 — Regular 13px #444, line-height 1.7
        dy = ty + th(d,title,"h3") + s(12)
        for line in desc.split("\n"):
            if dy + th(d,line,"sm") < by+card_h-s(10):
                d.text((bx+s(16), dy), line, font=Fk("sm"), fill=C(ds,"sm"))
                dy += int(th(d,line,"sm") * 1.7)

    return img

# ── 실행 ──────────────────────────────────────────────────────
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
