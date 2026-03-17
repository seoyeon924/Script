"""
강의 슬라이드 디자인 시스템 — Gray & Orange 두 테마만 유지

=== 공통 레이아웃 규칙 ===

캔버스: 1920×1080 (16:9, 150% 확대 렌더)
기준 설계: 1280×720 → ×1.5 스케일

레이아웃 타입 A: 상단 배너 + 2컬럼 콘텐츠 (Painpoint/Process 슬라이드)
  - 타이틀 배너: y=0..160 (full width, bg_strip)
    - category label: x=60, y=40, 14px gray
    - main title: x=60, y=68, 26px bold
    - description: x=60, y=118, 13px gray (2줄)
  - 콘텐츠: y=180..H
    - 좌 패널: x=60..860 (800px)
    - 우 패널: x=960..1860 (900px)
    - 중앙 커넥터: x=860..960 (100px)

레이아웃 타입 B: 좌측 사이드바 + 우측 콘텐츠 (Research/Journey 슬라이드)
  - 사이드바: x=0..380 (20% = 22% 기준)
    - category label: x=52, y=56, 14px gray
    - main title: x=52, y=88, 28px bold (멀티라인)
    - body text: x=52, y=250, 13px
    - 구분선: y=330
    - meta items: y=348
  - 콘텐츠: x=420..1860
    - 상단 패딩: y=60

레이아웃 타입 C: 좌측 사이드바 + 우측 섹션분리 (Painpoint comparison)
  - 사이드바: 동일
  - 우측 상단: 태그 + 질문 헤딩 + 구분선
  - 우측 하단: 말풍선 + 2컬럼 비교

=== 컴포넌트 스펙 ===

태그 pill (dark filled):
  bg: accent | text: white | padding: 8px 20px | radius: 4px | 13px medium

태그 pill (outline):
  bg: transparent | text: accent | border: 1.5px | padding: 8px 20px | radius: 4px | 13px

번호 리스트 (01/02/03):
  번호컬럼: 50px | gap: 32px | 제목컬럼: 180px | gap: 48px | 설명컬럼: 나머지
  구분선: 1px #D9D9D9 | row_h(기본): 80px | 번호: 17px bold | 제목: 15px semibold | 설명: 13px regular
  nested_table: 다크헤더(#333) + 데이터행

카드 (icon card):
  size: 240×160px | bg: bg_card | radius: 4px | border: none | shadow: none
  icon: 40px, center-top(y+30) | text: 13px center | 카드간 gap: 24px

커넥터 (수평 연결):
  색: border | 두께: 1px | 도트: 8px filled text_dim | 중간레이블: 13px text_dim

여정맵 행:
  행라벨: 80px col, 13px gray | 내용영역: 나머지
  행: Mission/Action/Feeling/Painpoint
  타임라인 화살표: 1px, 끝 삼각형

말풍선 (quote):
  bg: quote_bg | radius: 8px | text: 17px bold white | padding: 28px 36px
  꼬리: 우측 중앙, 삼각형

결과 테이블:
  헤더: bg=accent, text=white, 14px bold | 데이터: 36px bold | 단위: 14px
  교대배경: bg_card vs bg

여백 시스템:
  slide margin: 60px | section gap: 40px | element gap: 20px | micro gap: 12px
"""

# ── 스케일 팩터 (1280×720 설계 → 1920×1080 렌더) ─────────────
S = 1.5
W = int(1280 * S)   # 1920
H = int(720  * S)   # 1080

def s(v): return int(v * S)   # 스케일 변환 헬퍼

# ── 레이아웃 상수 ─────────────────────────────────────────────
MARGIN       = s(60)
SIDEBAR_W    = s(300)      # 22.5% of 1280 = 288 → s(300)=450
CONTENT_X    = SIDEBAR_W + s(60)
CONTENT_W    = W - CONTENT_X - MARGIN
STRIP_H      = s(120)      # 타입A 타이틀 배너 높이

# 번호리스트 컬럼 너비
NUM_COL      = s(50)
NUM_GAP      = s(32)
TITLE_COL    = s(180)
TITLE_GAP    = s(48)
ROW_H        = s(80)

CARD_W       = s(240)
CARD_H       = s(160)
CARD_GAP     = s(24)

PILL_PX      = s(20)    # pill 좌우 패딩
PILL_PY      = s(8)     # pill 상하 패딩
PILL_R       = s(4)     # pill radius

# ── Pretendard 폰트 경로 ─────────────────────────────────────
FONTS = {
    "regular":  "/Users/sy/Library/Fonts/Pretendard-Regular.otf",
    "semibold": "/Users/sy/Library/Fonts/Pretendard-SemiBold.otf",
    "bold":     "/Users/sy/Library/Fonts/Pretendard-Bold.otf",
    "fallback": "/System/Library/Fonts/AppleSDGothicNeo.ttc",
}

# ── 폰트 크기 위계 (레퍼런스 분석 기반, ×S 스케일)
# 라벨:타이틀:서브라벨:본문:메타 = 14:30:18:14:12
# ────────────────────────────────────────────────────────────
FS = {
    "category": s(14),    # "Chapter 01" — Regular, #888
    "h1":       s(30),    # 메인 타이틀 — Bold, #1A1A1A  (레퍼런스: 28-32px)
    "h2":       s(22),    # 섹션 헤딩 — Bold, #1A1A1A
    "h3":       s(18),    # 서브라벨/번호제목 — SemiBold, #1A1A1A  (레퍼런스: 16-18px)
    "body":     s(14),    # 본문 — Regular, #333333  (레퍼런스: 14-15px)
    "sm":       s(13),    # 설명/캡션 — Regular, #333-#444
    "tag":      s(13),    # pill 태그 — SemiBold
    "num":      s(18),    # 01/02/03 번호 — SemiBold
    "num_big":  s(42),    # 결과 테이블 숫자 — Bold
    "xs":       s(12),    # 메타/각주 — Regular, #888  (레퍼런스: 12-13px)
}

# ── 타이포 스타일 매핑 ────────────────────────────────────────
# weight: "regular" | "semibold" | "bold"
FW = {
    "category": "regular",
    "h1":       "bold",
    "h2":       "bold",
    "h3":       "semibold",
    "body":     "regular",
    "sm":       "regular",
    "tag":      "semibold",
    "num":      "semibold",
    "num_big":  "bold",
    "xs":       "regular",
}

# ── 색상 위계 (레퍼런스 분석 기반) ───────────────────────────
GRAY_COLOR = {
    "category": (136, 136, 136),   # #888888 — 라벨
    "h1":       (17, 17, 17),      # #111111 — 타이틀
    "h2":       (26, 26, 26),      # #1A1A1A
    "h3":       (26, 26, 26),      # #1A1A1A — 서브라벨
    "body":     (51, 51, 51),      # #333333 — 본문
    "sm":       (68, 68, 68),      # #444444 — 설명
    "meta":     (136, 136, 136),   # #888888 — 메타
    "xs":       (170, 170, 170),   # #AAAAAA — 각주
}

ORANGE_COLOR = {
    "category": (152, 136, 118),   # 웜톤 그레이
    "h1":       (26, 20, 14),      # 딥 웜 블랙
    "h2":       (34, 28, 20),
    "h3":       (34, 28, 20),
    "body":     (68, 56, 46),      # 웜 다크 그레이
    "sm":       (85, 72, 60),
    "meta":     (152, 136, 118),
    "xs":       (176, 162, 148),
}

DESIGN_SYSTEMS = {

    # ── GRAY ─────────────────────────────────────────────────
    "gray": {
        "name": "Gray",
        "desc": "Korean PPT Minimal — 순백 배경, 차콜 #333 액센트, 사이드바 레이아웃",

        # 색상
        "bg":           (255, 255, 255),
        "bg_strip":     (247, 247, 247),   # 타이틀 배너 배경
        "bg_card":      (242, 242, 242),   # 카드 배경
        "bg_sidebar":   (250, 250, 250),
        "bg_highlight": (235, 240, 248),   # 저니맵 하이라이트 영역

        "text_primary": (26, 26, 26),      # #1A1A1A
        "text_h2":      (34, 34, 34),
        "text_body":    (68, 68, 68),
        "text_label":   (119, 119, 119),   # category label
        "text_dim":     (170, 170, 170),

        "accent":       (51, 51, 51),      # #333 차콜
        "accent_light": (242, 242, 242),

        "border":       (217, 217, 217),   # #D9D9D9
        "border_dark":  (180, 180, 180),

        "tag_fill_bg":  (51, 51, 51),
        "tag_fill_txt": (255, 255, 255),
        "tag_out_txt":  (51, 51, 51),

        "table_header": (51, 51, 51),
        "table_h_txt":  (255, 255, 255),

        "quote_bg":     (60, 60, 60),
        "quote_txt":    (255, 255, 255),

        "connector":    (200, 200, 200),
        "connector_dot":(130, 130, 130),

        "num_txt":      (26, 26, 26),
        "bullet_fill":  (200, 200, 200),
    },

    # ── ORANGE ───────────────────────────────────────────────
    "orange": {
        "name": "Orange",
        "desc": "Warm Minimalist — 크림 배경 #F5F0E8, 오렌지 #E8734A 액센트",

        # 색상
        "bg":           (245, 240, 232),   # #F5F0E8 크림
        "bg_strip":     (237, 231, 222),   # 배너: 약간 더 어두운 크림
        "bg_card":      (255, 255, 255),   # 카드: 순백
        "bg_sidebar":   (240, 235, 226),
        "bg_highlight": (255, 240, 230),   # 저니맵 하이라이트

        "text_primary": (26, 26, 26),
        "text_h2":      (34, 34, 34),
        "text_body":    (68, 68, 68),
        "text_label":   (119, 107, 95),    # 웜톤 그레이
        "text_dim":     (176, 162, 148),

        "accent":       (232, 115, 74),    # #E8734A
        "accent_light": (250, 222, 208),   # #FADED0

        "border":       (220, 213, 204),   # #DCD5CC
        "border_dark":  (190, 178, 165),

        "tag_fill_bg":  (232, 115, 74),
        "tag_fill_txt": (255, 255, 255),
        "tag_out_txt":  (232, 115, 74),

        "table_header": (232, 115, 74),
        "table_h_txt":  (255, 255, 255),

        "quote_bg":     (181, 82, 42),     # 더 진한 오렌지
        "quote_txt":    (255, 255, 255),

        "connector":    (210, 196, 182),
        "connector_dot":(160, 140, 120),

        "num_txt":      (26, 26, 26),
        "bullet_fill":  (220, 200, 180),
    },
}
