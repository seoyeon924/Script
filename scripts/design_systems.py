"""
강의 슬라이드 디자인 시스템 정의
각 시스템: title, content, section 슬라이드 3장 생성
"""

DESIGN_SYSTEMS = {

    "orange": {
        "name": "Orange",
        "desc": "Warm Minimalist — 크림 배경, 오렌지 액센트, Serif 헤딩",
        "bg":           (245, 240, 232),   # #F5F0E8 크림
        "bg_card":      (255, 255, 255),   # #FFFFFF
        "bg_section":   (249, 245, 239),   # #F9F5EF
        "text_primary": (26, 26, 26),      # #1A1A1A
        "text_secondary":(107, 107, 107),  # #6B6B6B
        "text_dim":     (176, 176, 176),   # #B0B0B0
        "accent":       (232, 115, 74),    # #E8734A
        "accent_light": (250, 222, 208),   # #FADED0
        "border":       (232, 227, 219),   # #E8E3DB
        "bar_top":      (232, 115, 74),    # accent bar
        "font_style":   "serif_mix",       # heading=serif feel
    },

    "dark_navy": {
        "name": "Dark Navy",
        "desc": "DataBridge Brand — 다크 네이비, 블루 액센트",
        "bg":           (13, 17, 23),      # #0D1117
        "bg_card":      (22, 28, 38),      # #161C26
        "bg_section":   (18, 24, 32),      # #121820
        "text_primary": (245, 246, 247),   # #F5F6F7
        "text_secondary":(140, 150, 165),  # #8C96A5
        "text_dim":     (70, 80, 95),      # #46505F
        "accent":       (74, 122, 181),    # #4A7AB5
        "accent_light": (74, 122, 181, 30),
        "border":       (35, 45, 60),      # #232D3C
        "bar_top":      (74, 122, 181),
        "font_style":   "modern_sans",
    },

    "midnight": {
        "name": "Midnight",
        "desc": "Terminal Vibe — 블랙 배경, 민트/시안 액센트",
        "bg":           (10, 10, 15),      # #0A0A0F
        "bg_card":      (18, 20, 28),      # #12141C
        "bg_section":   (14, 16, 22),      # #0E1016
        "text_primary": (230, 237, 243),   # #E6EDF3
        "text_secondary":(125, 140, 160),  # #7D8CA0
        "text_dim":     (60, 70, 85),      # #3C4655
        "accent":       (0, 198, 174),     # #00C6AE mint
        "accent_light": (0, 198, 174),
        "border":       (30, 35, 48),      # #1E2330
        "bar_top":      (0, 198, 174),
        "font_style":   "mono_mix",
    },

    "clean_white": {
        "name": "Clean White",
        "desc": "Pure Minimal — 화이트 배경, 블랙 타이포, 포인트 없음",
        "bg":           (255, 255, 255),
        "bg_card":      (248, 249, 250),   # #F8F9FA
        "bg_section":   (243, 244, 246),   # #F3F4F6
        "text_primary": (17, 24, 39),      # #111827
        "text_secondary":(107, 114, 128),  # #6B7280
        "text_dim":     (209, 213, 219),   # #D1D5DB
        "accent":       (17, 24, 39),      # 액센트도 블랙
        "accent_light": (243, 244, 246),
        "border":       (229, 231, 235),   # #E5E7EB
        "bar_top":      (17, 24, 39),
        "font_style":   "modern_sans",
    },

    "gray": {
        "name": "Gray",
        "desc": "Korean PPT Minimal — 화이트 배경, 차콜 액센트, 좌측 사이드바 레이아웃",
        "bg":           (255, 255, 255),   # #FFFFFF
        "bg_card":      (242, 242, 242),   # #F2F2F2
        "bg_section":   (247, 247, 247),   # #F7F7F7
        "bg_sidebar":   (255, 255, 255),   # 사이드바도 순백
        "text_primary": (26, 26, 26),      # #1A1A1A
        "text_secondary":(119, 119, 119),  # #777777
        "text_dim":     (170, 170, 170),   # #AAAAAA
        "text_label":   (119, 119, 119),   # 카테고리 라벨
        "accent":       (51, 51, 51),      # #333333 차콜
        "accent_light": (242, 242, 242),   # 연한 회색
        "border":       (217, 217, 217),   # #D9D9D9
        "bar_top":      (51, 51, 51),      # 없거나 미세한 라인
        "sidebar_ratio": 0.22,             # 좌측 22%
        "font_style":   "korean_ppt",
        "layout":       "sidebar",         # 사이드바 레이아웃
    },

    "gradient": {
        "name": "Gradient",
        "desc": "Bold Gradient — 퍼플→블루 그라디언트, 글로우 효과",
        "bg":           (15, 12, 30),      # #0F0C1E 딥 퍼플-블랙
        "bg_card":      (25, 20, 48),      # #191430
        "bg_section":   (20, 16, 38),      # #141026
        "text_primary": (240, 238, 255),   # #F0EEFF
        "text_secondary":(170, 160, 210),  # #AAA0D2
        "text_dim":     (90, 80, 130),     # #5A5082
        "accent":       (130, 100, 255),   # #8264FF
        "accent_light": (130, 100, 255),
        "border":       (50, 40, 90),      # #32285A
        "bar_top":      (130, 100, 255),
        "font_style":   "modern_sans",
    },
}
