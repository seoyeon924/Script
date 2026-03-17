#!/usr/bin/env python3
"""
Gray & Orange 디자인 시스템 — 3가지 레이아웃 슬라이드 생성
레퍼런스 PPT와 동일한 레이아웃/타이포/정보구조 구현
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
from design_systems import DESIGN_SYSTEMS, W, H, S, s, FS
from design_systems import MARGIN, SIDEBAR_W, CONTENT_X, CONTENT_W
from design_systems import STRIP_H, NUM_COL, NUM_GAP, TITLE_COL, TITLE_GAP, ROW_H
from design_systems import CARD_W, CARD_H, CARD_GAP, PILL_PX, PILL_PY, PILL_R
from PIL import Image, ImageDraw, ImageFont

OUT_BASE = "/tmp/Script-repo/output/final"

# ══════════════════════════════════════════════════════════════
# 폰트 로더
# ══════════════════════════════════════════════════════════════
_font_cache = {}
def fnt(size, bold=False):
    key = (size, bold)
    if key not in _font_cache:
        paths = ["/System/Library/Fonts/AppleSDGothicNeo.ttc"]
        for p in paths:
            if os.path.exists(p):
                try:
                    _font_cache[key] = ImageFont.truetype(p, size)
                    break
                except: pass
        if key not in _font_cache:
            _font_cache[key] = ImageFont.load_default()
    return _font_cache[key]

# ══════════════════════════════════════════════════════════════
# 드로잉 헬퍼
# ══════════════════════════════════════════════════════════════
def tw(draw, text, size): return draw.textbbox((0,0), text, font=fnt(size))[2]
def th(draw, text, size): b=draw.textbbox((0,0),text,font=fnt(size)); return b[3]-b[1]

def text_cx(draw, text, size, y, color, x0=0, x1=W):
    """수평 중앙 정렬 텍스트"""
    w = tw(draw, text, size)
    draw.text(((x0+x1-w)//2, y), text, font=fnt(size), fill=color)
    return th(draw, text, size)

def text_at(draw, x, y, text, size, color):
    draw.text((x, y), text, font=fnt(size), fill=color)
    return th(draw, text, size)

def wrap_text(draw, text, size, max_w):
    """텍스트 줄바꿈"""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur+" "+w).strip()
        if tw(draw, test, size) > max_w and cur:
            lines.append(cur); cur = w
        else: cur = test
    if cur: lines.append(cur)
    return lines

def draw_wrapped(draw, x, y, text, size, color, max_w, line_gap=6):
    for line in wrap_text(draw, text, size, max_w):
        draw.text((x, y), line, font=fnt(size), fill=color)
        y += th(draw, line, size) + line_gap
    return y

def hrule(draw, x, y, w, color, thick=1):
    draw.rectangle([x, y, x+w, y+thick], fill=color)

def pill(draw, x, y, text, size, ds, filled=True):
    """태그 pill — filled or outline"""
    pw = tw(draw, text, size) + PILL_PX*2
    ph = th(draw, text, size) + PILL_PY*2
    if filled:
        draw.rounded_rectangle([x,y,x+pw,y+ph], radius=PILL_R,
                                fill=ds["tag_fill_bg"])
        draw.text((x+PILL_PX, y+PILL_PY), text, font=fnt(size), fill=ds["tag_fill_txt"])
    else:
        draw.rounded_rectangle([x,y,x+pw,y+ph], radius=PILL_R,
                                outline=ds["accent"], width=2)
        draw.text((x+PILL_PX, y+PILL_PY), text, font=fnt(size), fill=ds["tag_out_txt"])
    return pw, ph

def sidebar(img, draw, ds, category, title_lines, body_text="", meta=None):
    """사이드바 공통 렌더 (레이아웃 B, C)"""
    draw.rectangle([0,0,SIDEBAR_W,H], fill=ds["bg_sidebar"])
    draw.rectangle([SIDEBAR_W,0,SIDEBAR_W+1,H], fill=ds["border"])

    sx, sy = MARGIN, s(56)
    # 카테고리 라벨
    draw.text((sx, sy), category, font=fnt(FS["category"]), fill=ds["text_label"])
    sy += th(draw, category, FS["category"]) + s(12)

    # 메인 타이틀 (멀티라인)
    for line in title_lines:
        draw.text((sx, sy), line, font=fnt(FS["h1"]), fill=ds["text_primary"])
        sy += th(draw, line, FS["h1"]) + s(6)
    sy += s(12)

    # 본문
    if body_text:
        sy = draw_wrapped(draw, sx, sy, body_text, FS["sm"], ds["text_body"],
                          SIDEBAR_W - sx - s(20), line_gap=s(6))
        sy += s(16)

    # 구분선
    hrule(draw, sx, sy, SIDEBAR_W - sx - s(20), ds["border"])
    sy += s(20)

    # 메타 항목
    if meta:
        for k, v in meta.items():
            draw.text((sx, sy), k, font=fnt(FS["xs"]), fill=ds["text_label"])
            sy += th(draw, k, FS["xs"]) + s(4)
            draw.text((sx, sy), v, font=fnt(FS["sm"]), fill=ds["text_body"])
            sy += th(draw, v, FS["sm"]) + s(18)

def title_strip(img, draw, ds, category, title, description=""):
    """상단 배너 (레이아웃 A)"""
    draw.rectangle([0,0,W,STRIP_H], fill=ds["bg_strip"])
    draw.rectangle([0,STRIP_H,W,STRIP_H+1], fill=ds["border"])

    x, y = MARGIN, s(36)
    draw.text((x, y), category, font=fnt(FS["category"]), fill=ds["text_label"])
    y += th(draw, category, FS["category"]) + s(8)
    draw.text((x, y), title, font=fnt(FS["h1"]), fill=ds["text_primary"])
    y += th(draw, title, FS["h1"]) + s(10)
    if description:
        draw_wrapped(draw, x, y, description, FS["sm"], ds["text_label"], W-MARGIN*2)

def num_row(draw, ds, x, y, w, num, title, desc, row_h=None,
            nested=None, first=True):
    """번호 리스트 행 (01/02/03)"""
    rh = row_h or ROW_H
    if first:
        hrule(draw, x, y, w, ds["border"])
    y += s(16)

    # 번호
    draw.text((x, y), num, font=fnt(FS["num"]), fill=ds["num_txt"])

    # 제목
    tx = x + NUM_COL + NUM_GAP
    draw.text((tx, y), title, font=fnt(FS["h3"]), fill=ds["text_primary"])

    # 설명
    dx = tx + TITLE_COL + TITLE_GAP
    dw = w - (dx - x)
    cy = y
    for line in wrap_text(draw, desc, FS["sm"], dw):
        draw.text((dx, cy), line, font=fnt(FS["sm"]), fill=ds["text_body"])
        cy += th(draw, line, FS["sm"]) + s(4)

    # nested 테이블
    if nested:
        ny = cy + s(12)
        ny = mini_table(draw, ds, dx, ny, nested)
        y_end = ny + s(16)
    else:
        y_end = y + rh

    hrule(draw, x, y_end, w, ds["border"])
    return y_end + 1

def mini_table(draw, ds, x, y, data):
    """내부 작은 테이블 (헤더행 + 데이터행)"""
    cols = data["cols"]
    rows = data["rows"]
    col_w = s(60)
    row_h = s(36)
    label_w = s(80)
    total_w = label_w + col_w * len(cols)

    # 헤더행 (다크)
    draw.rectangle([x, y, x+total_w, y+row_h], fill=ds["table_header"])
    for i, c in enumerate(cols):
        cx = x + label_w + i*col_w
        cw = tw(draw, c, FS["sm"])
        draw.text((cx+(col_w-cw)//2, y+s(10)), c, font=fnt(FS["sm"]),
                  fill=ds["table_h_txt"])
    y += row_h

    # 데이터행
    for ri, row in enumerate(rows):
        bg = ds["bg_card"] if ri%2==0 else ds["bg"]
        draw.rectangle([x, y, x+total_w, y+row_h], fill=bg)
        draw.rectangle([x, y, x+total_w, y+row_h], outline=ds["border"], width=1)
        # 첫번째 컬럼 (레이블)
        draw.text((x+s(8), y+s(10)), row[0], font=fnt(FS["sm"]), fill=ds["text_label"])
        for i, val in enumerate(row[1:]):
            cx = x + label_w + i*col_w
            vw = tw(draw, val, FS["sm"])
            draw.text((cx+(col_w-vw)//2, y+s(10)), val, font=fnt(FS["sm"]),
                      fill=ds["text_body"])
        y += row_h
    return y

def icon_card(draw, ds, x, y, icon_char, line1, line2=""):
    """아이콘 카드"""
    draw.rounded_rectangle([x,y,x+CARD_W,y+CARD_H], radius=s(4),
                            fill=ds["bg_card"], outline=ds["border"], width=1)
    # 아이콘 (텍스트 심볼 사용)
    icon_size = FS["h2"]
    iw = tw(draw, icon_char, icon_size)
    draw.text((x+(CARD_W-iw)//2, y+s(22)), icon_char, font=fnt(icon_size),
              fill=ds["text_label"])
    # 텍스트
    ty = y + s(82)
    for line in [line1, line2]:
        if line:
            lw = tw(draw, line, FS["sm"])
            draw.text((x+(CARD_W-lw)//2, ty), line, font=fnt(FS["sm"]),
                      fill=ds["text_body"])
            ty += th(draw, line, FS["sm"]) + s(6)

def quote_bubble(draw, ds, x, y, w, text, speaker=""):
    """말풍선 (다크 배경 인용구)"""
    lines = wrap_text(draw, text, FS["h3"], w - s(72))
    bh = len(lines) * (th(draw, "가", FS["h3"]) + s(8)) + s(56)
    draw.rounded_rectangle([x,y,x+w,y+bh], radius=s(8), fill=ds["quote_bg"])
    ty = y + s(28)
    for line in lines:
        draw.text((x+s(36), ty), line, font=fnt(FS["h3"]), fill=ds["quote_txt"])
        ty += th(draw, line, FS["h3"]) + s(8)
    # 꼬리 (우측 중앙)
    my = y + bh//2
    draw.polygon([(x+w, my-s(10)),(x+w+s(24), my),(x+w, my+s(10))],
                 fill=ds["quote_bg"])
    # 화자
    if speaker:
        draw.text((x+w+s(32), my-th(draw, speaker, FS["xs"])//2),
                  speaker, font=fnt(FS["xs"]), fill=ds["text_label"])
    return bh

def result_row(draw, ds, x, y, w, labels, values, units):
    """결과 테이블 (큰 숫자)"""
    col_w = w // len(labels)
    row1_h = s(44)
    row2_h = s(70)

    # 헤더
    for i, label in enumerate(labels):
        cx = x + i*col_w
        draw.rectangle([cx,y,cx+col_w,y+row1_h], fill=ds["table_header"])
        draw.rectangle([cx,y,cx+col_w,y+row1_h], outline=ds["border"], width=1)
        lw = tw(draw, label, FS["sm"])
        draw.text((cx+(col_w-lw)//2, y+s(13)), label, font=fnt(FS["sm"]),
                  fill=ds["table_h_txt"])
    y += row1_h

    # 데이터
    for i, (val, unit) in enumerate(zip(values, units)):
        cx = x + i*col_w
        draw.rectangle([cx,y,cx+col_w,y+row2_h], fill=ds["bg"])
        draw.rectangle([cx,y,cx+col_w,y+row2_h], outline=ds["border"], width=1)
        full = val+unit
        fw = tw(draw, val, FS["num_big"]) + tw(draw, unit, FS["h3"])
        ox = cx + (col_w - fw)//2
        draw.text((ox, y+s(14)), val, font=fnt(FS["num_big"]), fill=ds["text_primary"])
        draw.text((ox+tw(draw, val, FS["num_big"]), y+s(28)), unit,
                  font=fnt(FS["h3"]), fill=ds["text_label"])
    return y + row2_h

def connector_h(draw, ds, x, y, w, label=""):
    """수평 커넥터 라인 + 도트 + 레이블"""
    draw.rectangle([x,y,x+w,y+1], fill=ds["connector"])
    dot_r = s(5)
    draw.ellipse([x+w//2-dot_r, y-dot_r, x+w//2+dot_r, y+dot_r],
                 fill=ds["connector_dot"])
    if label:
        for i, line in enumerate(label.split("\n")):
            lw = tw(draw, line, FS["xs"])
            draw.text((x+w//2-lw//2, y+dot_r+s(6)+i*th(draw,"가",FS["xs"])),
                      line, font=fnt(FS["xs"]), fill=ds["text_label"])

def arrow_h(draw, ds, x, y, w):
    """수평 화살표"""
    draw.rectangle([x,y,x+w-s(10),y+1], fill=ds["connector"])
    draw.polygon([(x+w-s(10),y-s(5)),(x+w,y),(x+w-s(10),y+s(5))],
                 fill=ds["connector"])

# ══════════════════════════════════════════════════════════════
# SLIDE 1 — Layout A: 상단 배너 + 번호리스트 + 카드플로우
# 레퍼런스: "정보가 분산되어 불필요한 이동을 반복..." (Painpoint 2)
# ══════════════════════════════════════════════════════════════
def make_slide_1(ds):
    img = Image.new("RGB", (W, H), ds["bg"])
    draw = ImageDraw.Draw(img)

    # ── 상단 배너 ──
    title_strip(draw, draw, ds,
        category="Chapter 01 · Concept",
        title="클로드 코드와 챗지피티는 어떻게 다른가",
        description="두 도구의 작동 방식 차이를 이해하면 언제, 어떻게 써야 하는지 명확해집니다.")

    # 배너를 img 위에 그려야 하므로 재사용
    draw_g = draw
    draw.rectangle([0,0,W,STRIP_H], fill=ds["bg_strip"])
    draw.rectangle([0,STRIP_H,W,STRIP_H+1], fill=ds["border"])
    x, y0 = MARGIN, s(34)
    draw.text((x, y0), "Chapter 01 · Concept", font=fnt(FS["category"]), fill=ds["text_label"])
    draw.text((x, y0+th(draw,"A",FS["category"])+s(8)),
              "클로드 코드와 챗지피티는 어떻게 다른가",
              font=fnt(FS["h1"]), fill=ds["text_primary"])
    desc = "두 도구의 작동 방식 차이를 이해하면 언제, 어떻게 써야 하는지 명확해집니다."
    draw.text((x, y0+th(draw,"A",FS["category"])+s(10)+th(draw,"A",FS["h1"])+s(12)),
              desc, font=fnt(FS["sm"]), fill=ds["text_label"])

    # ── 콘텐츠 영역 ──
    cy = STRIP_H + s(32)
    left_x  = MARGIN
    left_w  = int(W * 0.44) - MARGIN
    right_x = int(W * 0.52)
    right_w = W - right_x - MARGIN
    mid_x   = int(W * 0.44)
    mid_w   = int(W * 0.52) - int(W * 0.44)

    # ── 좌측: 태그 + 설명 + 번호리스트 ──
    tag_w, tag_h = pill(draw, left_x, cy, "탐색 여정 1", FS["tag"], ds, filled=True)
    cy_l = cy + tag_h + s(16)
    draw.text((left_x, cy_l), "챗지피티처럼 텍스트로 묻고 텍스트로 받는 방식",
              font=fnt(FS["sm"]), fill=ds["text_body"])
    cy_l += th(draw, "가", FS["sm"]) + s(24)

    cy_l = num_row(draw, ds, left_x, cy_l, left_w,
                   "01", "대화형 AI",
                   "텍스트 입력 → 텍스트 출력. 파일에 접근하지 않음.",
                   first=True)
    cy_l = num_row(draw, ds, left_x, cy_l, left_w,
                   "02", "세션 한계",
                   "대화가 끊기면 이전 내용을 기억하지 못함.",
                   first=False,
                   nested={
                       "cols": ["A", "B", "C", "D"],
                       "rows": [["한계", "파일", "기억", "컨텍스트", "없음"]]
                   })
    cy_l = num_row(draw, ds, left_x, cy_l, left_w,
                   "03", "용도",
                   "정보 검색, 초안 작성, 아이디어 탐색에 적합.",
                   first=False)

    # ── 중앙 커넥터 ──
    conn_y = cy + (cy_l - cy) // 2
    connector_h(draw, ds, mid_x+s(8), conn_y, mid_w-s(16),
                "두 도구의\n핵심 차이")

    # ── 우측: 태그 + 설명 + 카드 3개 ──
    cy_r = cy
    pill(draw, right_x, cy_r, "에이전트 방식", FS["tag"], ds, filled=False)
    cy_r += tag_h + s(16)
    draw.text((right_x, cy_r), "클로드 코드처럼 실제로 파일을 열고 코드를 실행하는 방식",
              font=fnt(FS["sm"]), fill=ds["text_body"])
    cy_r += th(draw, "가", FS["sm"]) + s(28)

    cards = [
        ("◻", "파일 직접 접근", "읽기·쓰기·실행"),
        ("◈", "에이전트 루프", "계획→실행→확인"),
        ("◉", "컨텍스트 유지", "CLAUDE.md 연동"),
    ]
    for i, (icon, l1, l2) in enumerate(cards):
        cx2 = right_x + i*(CARD_W+CARD_GAP)
        if cx2 + CARD_W <= W - MARGIN:
            icon_card(draw, ds, cx2, cy_r, icon, l1, l2)

    # ── ㄷ자 카드 커넥터 ──
    c1x = right_x + CARD_W//2
    c3x = right_x + 2*(CARD_W+CARD_GAP) + CARD_W//2
    top_y = cy_r - s(16)
    draw.rectangle([c1x, top_y, c3x, top_y+1], fill=ds["connector"])
    draw.rectangle([c1x, top_y, c1x+1, cy_r], fill=ds["connector"])
    draw.rectangle([c3x, top_y, c3x+1, cy_r], fill=ds["connector"])

    # 하단 풋노트
    draw.text((MARGIN, H-s(36)), "DataBridge × Fastcampus — Claude Code 실무 완성",
              font=fnt(FS["xs"]), fill=ds["text_dim"])
    return img

# ══════════════════════════════════════════════════════════════
# SLIDE 2 — Layout B: 좌측 사이드바 + 저니맵
# 레퍼런스: "관찰 조사를 통해 문제 발견" (Research 저니맵)
# ══════════════════════════════════════════════════════════════
def make_slide_2(ds):
    img = Image.new("RGB", (W, H), ds["bg"])
    draw = ImageDraw.Draw(img)

    # 사이드바
    sidebar(img, draw, ds,
        category="Chapter 01 · Flow",
        title_lines=["클로드 코드", "에이전트 루프", "작동 과정"],
        body_text="사용자 지시를 받은 후 계획, 실행, 확인을 반복하며 작업을 완료합니다.",
        meta={"핵심 개념": "에이전트 루프", "비유": "실무자가\n일하는 방식"})

    # ── 우측 저니맵 ──
    cx = CONTENT_X
    row_label_w = s(90)
    map_x = cx + row_label_w + s(24)
    map_w = W - map_x - MARGIN
    map_step_w = map_w // 5
    steps = ["시작", "파일 탐색", "코드 실행", "결과 확인", "완료 보고"]

    y = s(52)

    # ── Mission 행 ──
    draw.text((cx, y+s(4)), "Mission", font=fnt(FS["sm"]), fill=ds["text_label"])
    hrule(draw, map_x, y+s(18), map_w, ds["border"])
    mission = "claude 실행 → data.csv 읽기 → 분석 → 결과 저장"
    draw.text((map_x, y), mission, font=fnt(FS["sm"]), fill=ds["text_body"])
    y += s(44)
    hrule(draw, cx, y, W-cx-MARGIN, ds["border"])
    y += s(12)

    # ── Action 행 ──
    draw.text((cx, y+s(4)), "Action", font=fnt(FS["sm"]), fill=ds["text_label"])
    for i, step in enumerate(steps):
        sx = map_x + i*map_step_w
        sw = tw(draw, step, FS["sm"])
        draw.text((sx+(map_step_w-sw)//2, y), step, font=fnt(FS["sm"]), fill=ds["text_body"])
        if i < len(steps)-1:
            arrow_h(draw, ds, sx+map_step_w-s(30), y+s(9), s(30))
    y += s(38)
    hrule(draw, cx, y, W-cx-MARGIN, ds["border"])
    y += s(12)

    # ── Feeling 행 (감정선) ──
    draw.text((cx, y), "Feeling", font=fnt(FS["sm"]), fill=ds["text_label"])
    feel_y_base = y + s(80)
    feel_h = s(80)
    feel_points = [0.4, 0.6, 0.3, 0.55, 0.8]   # 0=bottom, 1=top
    pts = []
    for i, fp in enumerate(feel_points):
        px = map_x + i*map_step_w + map_step_w//2
        py = int(feel_y_base + feel_h * (1 - fp))
        pts.append((px, py))

    # 선
    for i in range(len(pts)-1):
        draw.line([pts[i], pts[i+1]], fill=ds["connector"], width=s(2))

    # 도트 + 말풍선
    bubbles = [
        (0, "파일을 직접\n열다니 신기해요!"),
        (2, "오류가 나서\n조금 당황했어요"),
        (4, "완성! 생각보다\n빠르게 끝났어요"),
    ]
    for idx, text in bubbles:
        px, py = pts[idx]
        draw.ellipse([px-s(8),py-s(8),px+s(8),py+s(8)], fill=ds["accent"])
        # 작은 말풍선
        blines = text.split("\n")
        bw = max(tw(draw,l,FS["xs"]) for l in blines) + s(24)
        bh = len(blines)*th(draw,"가",FS["xs"]) + s(16)
        bx = px - bw//2
        by = py - bh - s(16)
        draw.rounded_rectangle([bx,by,bx+bw,by+bh], radius=s(4),
                                fill=ds["bg_card"], outline=ds["border"], width=1)
        for bi, bl in enumerate(blines):
            draw.text((bx+s(12), by+s(8)+bi*th(draw,"가",FS["xs"])),
                      bl, font=fnt(FS["xs"]), fill=ds["text_body"])

    # 하이라이트 영역 (문제 구간)
    prob_x = pts[1][0]
    prob_x2 = pts[3][0]
    draw.rectangle([prob_x, y+s(4), prob_x2, y+s(172)], fill=ds["bg_highlight"])

    y += s(180)
    hrule(draw, cx, y, W-cx-MARGIN, ds["border"])
    y += s(12)

    # ── Painpoint 행 ──
    draw.text((cx, y+s(8)), "Painpoint", font=fnt(FS["sm"]), fill=ds["text_label"])
    arrow_h(draw, ds, map_x, y+s(12), map_w)
    draw.text((map_x+map_w//2-tw(draw,"오류 발생 시 원인 파악 시간 소요",FS["sm"])//2,
               y+s(20)), "오류 발생 시 원인 파악 시간 소요",
              font=fnt(FS["sm"]), fill=ds["text_body"])
    y += s(52)
    hrule(draw, cx, y, W-cx-MARGIN, ds["border"])
    y += s(20)

    # ── 결과 표 ──
    draw.text((cx, y), "Result", font=fnt(FS["sm"]), fill=ds["text_label"])
    y += s(32)
    result_row(draw, ds, map_x, y,
               map_w-s(8),
               ["참가자 A\n기본 사용", "참가자 B\n중급 사용", "참가자 C\n고급 사용", "참가자 D\n자동화"],
               ["3", "7", "12", "28"],
               ["분", "분", "분", "분"])

    draw.text((MARGIN, H-s(36)), "DataBridge × Fastcampus — Claude Code 실무 완성",
              font=fnt(FS["xs"]), fill=ds["text_dim"])
    return img

# ══════════════════════════════════════════════════════════════
# SLIDE 3 — Layout C: 사이드바 + 말풍선 + 2컬럼 비교
# 레퍼런스: "제품에 따라 제공하는 콘텐츠 포맷의 간격" (Painpoint 1-2)
# ══════════════════════════════════════════════════════════════
def make_slide_3(ds):
    img = Image.new("RGB", (W, H), ds["bg"])
    draw = ImageDraw.Draw(img)

    # 사이드바
    sidebar(img, draw, ds,
        category="Chapter 01 · Key Insight",
        title_lines=["에이전트가", "일반 AI와", "다른 이유"],
        body_text="단순한 대화를 넘어 실제 파일 시스템에서 작업을 수행하기 때문입니다.",
        meta={"핵심 차이": "실행 vs 조언"})

    cx = CONTENT_X
    cy = s(52)

    # ── 태그 + 질문 헤딩 ──
    pill(draw, cx, cy, "핵심 인사이트", FS["tag"], ds, filled=True)
    cy += FS["tag"] + PILL_PY*2 + s(16)
    q = "왜 클로드 코드는 단순한 챗봇과 다른가?"
    draw.text((cx, cy), q, font=fnt(FS["h2"]), fill=ds["text_primary"])
    cy += th(draw, q, FS["h2"]) + s(8)
    hrule(draw, cx, cy, CONTENT_W, ds["border"])
    cy += s(28)

    # ── 말풍선 인용구 ──
    quote = '"파일을 직접 열고, 코드를 실행하고, 결과까지 저장한다. 그게 에이전트다."'
    bubble_w = int(CONTENT_W * 0.72)
    bh = quote_bubble(draw, ds, cx, cy, bubble_w, quote, speaker="서연 / DataBridge")
    cy += bh + s(36)

    # ── 2컬럼 비교 ──
    col_w = (CONTENT_W - s(60)) // 2
    col1_x = cx
    col2_x = cx + col_w + s(60)

    # 컬럼 헤딩
    draw.text((col1_x, cy), "일반 챗봇 방식", font=fnt(FS["h3"]), fill=ds["text_label"])
    draw.text((col2_x, cy), "클로드 코드 에이전트", font=fnt(FS["h3"]), fill=ds["accent"])
    cy += th(draw, "가", FS["h3"]) + s(16)
    hrule(draw, cx, cy, CONTENT_W, ds["border"])

    # 중간 수직 구분선
    mid_x = col2_x - s(30)
    draw.rectangle([mid_x, cy, mid_x+1, cy+s(200)], fill=ds["border"])
    cy += s(20)

    pairs = [
        ("텍스트로 답변 생성", "실제 파일 열기·수정·저장"),
        ("파일 접근 불가", "터미널 명령어 직접 실행"),
        ("세션 종료 시 망각", "CLAUDE.md로 기억 영구화"),
        ("조언·정보 제공", "작업 완료까지 자동 처리"),
    ]
    for left, right in pairs:
        draw.text((col1_x, cy), left, font=fnt(FS["body"]), fill=ds["text_body"])
        draw.text((col2_x, cy), right, font=fnt(FS["body"]), fill=ds["text_primary"])
        cy += th(draw, "가", FS["body"]) + s(12)
        hrule(draw, cx, cy, CONTENT_W, ds["border"])
        cy += s(8)

    # 하단 결론
    cy += s(12)
    conclusion = "클로드 코드는 조언자가 아닙니다. 직접 실행하는 동료입니다."
    cw = tw(draw, conclusion, FS["h3"])
    draw.text((cx+(CONTENT_W-cw)//2, cy), conclusion,
              font=fnt(FS["h3"]), fill=ds["text_label"])

    draw.text((MARGIN, H-s(36)), "DataBridge × Fastcampus — Claude Code 실무 완성",
              font=fnt(FS["xs"]), fill=ds["text_dim"])
    return img

# ══════════════════════════════════════════════════════════════
# 생성 실행
# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    makers = [
        ("01_process",  make_slide_1),
        ("02_journey",  make_slide_2),
        ("03_compare",  make_slide_3),
    ]
    for theme_key, ds in DESIGN_SYSTEMS.items():
        out_dir = os.path.join(OUT_BASE, theme_key)
        os.makedirs(out_dir, exist_ok=True)
        print(f"\n[{ds['name']}] 슬라이드 생성 중...")
        for slug, maker in makers:
            img = maker(ds)
            path = os.path.join(out_dir, f"{slug}.png")
            img.save(path)
            print(f"  ✓ {slug}.png")
    print("\n완료!")
