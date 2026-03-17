#!/usr/bin/env python3
"""
클로드 코드 워크플로우 치트시트 v3 — 가독성 최우선
2560 × 2340px / Pretendard 전용 / 폰트 22-16px
"""
from PIL import Image, ImageDraw, ImageFont
import os

# ── 캔버스 & 레이아웃 ────────────────────────────────────────
W, H      = 2560, 2340
OUTER_M   = 72
COL_GAP   = 28
HEADER_H  = 150
CONTENT_Y = HEADER_H + 32

COL_W = (W - OUTER_M*2 - COL_GAP*2) // 3   # 780
X1 = OUTER_M                                 # 72
X2 = OUTER_M + COL_W + COL_GAP             # 880
X3 = OUTER_M + (COL_W + COL_GAP)*2         # 1688

H1  = 740    # Row1
H2  = 920    # Row2
H3  = 360    # Row3
S1H = 340    # 시작하기
S4H = H1-S1H-24               # 376
S6H = 620    # 스킬 추가
S7H = H2-S6H-24               # 276
S8H = 600    # 훅 설정
S9H = H2-S8H-24               # 296

R1Y = CONTENT_Y
R2Y = R1Y + H1 + 24
R3Y = R2Y + H2 + 24

# ── 색상 ─────────────────────────────────────────────────────
BG      = (253, 245, 235)
CARD_BG = (255, 255, 255)
CARD_BD = (228, 216, 200)
CODE_BG = (237, 226, 210)
ORANGE  = (243, 123, 28)
ORANGE_D= (210, 90, 8)
BLK     = (20, 20, 20)
BODY    = (55, 55, 55)
DIM     = (140, 125, 110)
CODE_TX = (38, 38, 38)
WHITE   = (255, 255, 255)
LIGHT_O = (255, 240, 222)

# ── 폰트 크기 (대폭 업사이즈) ────────────────────────────────
SZ = {
    "h_title": 58,   # 메인 헤더 타이틀
    "h_sub":   16,   # 메인 헤더 서브
    "s_title": 22,   # 섹션 카드 타이틀
    "badge":   16,   # 번호 배지
    "body":    17,   # 본문
    "code":    16,   # 코드 블록 (Pretendard SemiBold 사용)
    "bullet":  17,   # 불릿 리스트
    "pill":    15,   # pill 태그
    "dim":     15,   # 흐린 텍스트
    "label":   16,   # 소제목
}

# ── 폰트 로더 ─────────────────────────────────────────────────
FP = {
    "r":  "/Users/sy/Library/Fonts/Pretendard-Regular.otf",
    "sb": "/Users/sy/Library/Fonts/Pretendard-SemiBold.otf",
    "b":  "/Users/sy/Library/Fonts/Pretendard-Bold.otf",
}
_fc = {}

def F(sz, wt="r"):
    k = (sz, wt)
    if k not in _fc:
        try: _fc[k] = ImageFont.truetype(FP.get(wt, FP["r"]), sz)
        except: _fc[k] = ImageFont.load_default()
    return _fc[k]

def tw(d, t, f): return d.textbbox((0,0), t, font=f)[2]
def th(d, t, f): b = d.textbbox((0,0), t, font=f); return b[3]-b[1]

def put(d, x, y, text, sz_key, wt, color):
    sz = SZ[sz_key]; f = F(sz, wt)
    d.text((x, y), text, font=f, fill=color)
    return th(d, text, f)

def put_sz(d, x, y, text, sz, wt, color):
    f = F(sz, wt)
    d.text((x, y), text, font=f, fill=color)
    return th(d, text, f)

def wrap_put_sz(d, x, y, text, sz, wt, color, max_w, lh=1.72):
    f = F(sz, wt); words = text.split(); lines, cur = [], ""
    for w in words:
        test = (cur+" "+w).strip()
        if tw(d, test, f) > max_w and cur: lines.append(cur); cur = w
        else: cur = test
    if cur: lines.append(cur)
    for line in lines:
        d.text((x, y), line, font=f, fill=color); y += int(th(d, line, f)*lh)
    return y

def hrule(d, x, y, w, color=CARD_BD, h=1):
    d.rectangle([x, y, x+w, y+h], fill=color)

# ── 컴포넌트 ─────────────────────────────────────────────────
BADGE_R = 20

def num_badge(d, x, y, num):
    r = BADGE_R
    d.ellipse([x, y, x+r*2, y+r*2], fill=ORANGE)
    f = F(SZ["badge"], "b"); ns = str(num)
    nw = tw(d, ns, f); nh = th(d, ns, f)
    d.text((x+r-nw//2, y+r-nh//2), ns, font=f, fill=WHITE)
    return r*2  # 40px

def pill(d, x, y, text, sz=None, bg=ORANGE, fg=WHITE, r=6):
    sz = sz or SZ["pill"]
    f = F(sz, "sb")
    pw = tw(d, text, f)+22; ph = th(d, text, f)+12
    d.rounded_rectangle([x, y, x+pw, y+ph], radius=r, fill=bg)
    d.text((x+11, y+6), text, font=f, fill=fg)
    return pw+8, ph+4

def section_card(d, x, y, w, h, num, title):
    """카드 + 헤더 → (콘텐츠 시작 y, 내부 패딩)"""
    PAD = 22
    d.rounded_rectangle([x, y, x+w, y+h], radius=12, fill=CARD_BG, outline=CARD_BD, width=1)
    bh = num_badge(d, x+PAD, y+PAD, num)
    put(d, x+PAD+bh+12, y+PAD+6, title, "s_title", "b", BLK)
    hy = y+PAD+bh+14
    hrule(d, x+PAD, hy, w-PAD*2)
    return hy+14, PAD

def code_block(d, x, y, w, lines, bg=CODE_BG):
    """코드 블록 — Pretendard SemiBold 16px, line_h=26"""
    SZ_C = SZ["code"]; WT_C = "sb"; LH = 28; PAD = 16
    bh = PAD*2 + len(lines)*LH
    d.rounded_rectangle([x, y, x+w, y+bh], radius=6, fill=bg)
    cy = y+PAD
    for line in lines:
        f = F(SZ_C, WT_C)
        d.text((x+PAD, cy), line, font=f, fill=CODE_TX)
        cy += LH
    return y+bh

def bullets(d, x, y, items, gap=1.85):
    f = F(SZ["bullet"], "r"); lh = int(th(d, "A", f)*gap)
    for item in items:
        d.text((x, y),    "○", font=f, fill=ORANGE)
        d.text((x+24, y), item, font=f, fill=BODY)
        y += lh
    return y

# ════════════════════════════════════════════════════════════════
# 캔버스
# ════════════════════════════════════════════════════════════════
img = Image.new("RGB", (W, H), BG)
d   = ImageDraw.Draw(img)

# ── 헤더 ──────────────────────────────────────────────────────
tx, ty = OUTER_M, 40
put_sz(d, tx, ty, "클로드 코드", SZ["h_title"], "b", BLK)
cx2 = tw(d, "클로드 코드", F(SZ["h_title"], "b")) + tx + 14
put_sz(d, cx2, ty, "워크플로우 치트시트", SZ["h_title"], "b", ORANGE_D)
sy = ty + th(d, "A", F(SZ["h_title"], "b")) + 12
put_sz(d, tx, sy,
    "시작하기  ·  프로젝트 설정  ·  파일 구조  ·  스킬  ·  훅  ·  메모리  ·  워크플로우  ·  2026 Edition",
    SZ["h_sub"], "r", DIM)
hrule(d, OUTER_M, HEADER_H-2, W-OUTER_M*2, CARD_BD, h=1)

# ════════════════════════════════════════════════════════════════
# ① 시작하기  (Col1, R1, h=340)
# ════════════════════════════════════════════════════════════════
cy, PAD = section_card(d, X1, R1Y, COL_W, S1H, 1, "시작하기")
x = X1+PAD; w = COL_W-PAD*2

cy = code_block(d, x, cy, w,
    ["curl -fsSL https://claude.ai/install.sh | bash"])+14

cy = code_block(d, x, cy, w,
    ["cd your-project",
     "claude",
     "/init"])+14

put_sz(d, x, cy, "코드베이스를 스캔하고 스타터 메모리 파일을 생성합니다.",
       SZ["body"], "r", BODY)

# ════════════════════════════════════════════════════════════════
# ④ CLAUDE.md 모범 사례  (Col1, R1 하단, h=376)
# ════════════════════════════════════════════════════════════════
cy4 = R1Y+S1H+24
cy4, PAD4 = section_card(d, X1, cy4, COL_W, S4H, 4, "CLAUDE.md 모범 사례")
x4 = X1+PAD4

bullets(d, x4, cy4, [
    "/init 실행 후 출력 다듬기",
    "지시사항 구체적으로 작성",
    "클로드가 추론 불가한 주의사항 추가",
    "@파일명으로 문서 참조",
    "워크플로우 규칙 추가",
    "메모리 간결하게 유지",
    "팀 공유를 위해 Git에 커밋",
])

# ════════════════════════════════════════════════════════════════
# ② CLAUDE.md 이해하기  (Col2, R1, h=740)
# ════════════════════════════════════════════════════════════════
cy2, PAD2 = section_card(d, X2, R1Y, COL_W, H1, 2, "CLAUDE.md 이해하기")
x2 = X2+PAD2; w2 = COL_W-PAD2*2

put_sz(d, x2, cy2,
    "CLAUDE.md = 클로드의 프로젝트 영구 메모리.",
    SZ["body"], "r", BODY); cy2 += 28
put_sz(d, x2, cy2,
    "매 세션 시작 시 자동으로 로드됩니다.",
    SZ["body"], "r", BODY); cy2 += 34

# WHAT / WHY / HOW 배지
bx2 = x2
for tag in ["WHAT","WHY","HOW"]:
    pw, ph = pill(d, bx2, cy2, tag, bg=ORANGE); bx2 += pw+6
cy2 += ph+16

# 3컬럼 서브항목 (열별로 독립 y축)
col3_w = w2//3
col_data = [
    ("WHAT", ["기술 스택","디렉토리 맵","아키텍처"]),
    ("WHY",  ["각 모듈 목적","디자인 결정"]),
    ("HOW",  ["빌드/테스트","lint 명령어","워크플로우","주의사항"]),
]
max_col_h = 0
for i, (lbl, items) in enumerate(col_data):
    bx = x2 + i*col3_w; iy = cy2
    put_sz(d, bx, iy, lbl, SZ["label"], "sb", ORANGE); iy += 24
    for it in items:
        put_sz(d, bx, iy, "· "+it, SZ["dim"], "r", BODY); iy += 22
    max_col_h = max(max_col_h, iy-cy2)
cy2 += max_col_h+14
hrule(d, x2, cy2, w2); cy2 += 16

code_block(d, x2, cy2, w2, [
    "# Project: MyApp",
    "FastAPI REST API + React SPA + Postgres",
    "",
    "## Commands",
    "npm run dev",
    "npm run test",
    "npm run lint",
    "",
    "## Architecture",
    "/app    Next.js App Router pages",
    "/lib    shared utilities",
    "/prisma DB schema & migrations",
])

# ════════════════════════════════════════════════════════════════
# ③ 메모리 파일 계층 구조  (Col3, R1, h=740)
# ════════════════════════════════════════════════════════════════
cy3, PAD3 = section_card(d, X3, R1Y, COL_W, H1, 3, "메모리 파일 계층 구조")
x3 = X3+PAD3; w3 = COL_W-PAD3*2

tree_items = [
    ("~/.claude/CLAUDE.md", "전역 — 모든 프로젝트"),
    ("~/CLAUDE.md",          "부모 — 모노레포 루트"),
    ("./CLAUDE.md",          "프로젝트 — git에 공유"),
    ("./frontend/CLAUDE.md", "서브폴더 — 범위 제한"),
]
for path, desc in tree_items:
    cy3 = code_block(d, x3, cy3, w3, [path])+6
    put_sz(d, x3+14, cy3, "  " + desc, SZ["dim"], "r", DIM); cy3 += 26

cy3 += 10; hrule(d, x3, cy3, w3); cy3 += 16

bullets(d, x3, cy3, [
    "각 파일 200줄 이하 유지",
    "서브폴더 파일은 컨텍스트 추가",
    "부모 컨텍스트 덮어쓰기 금지",
])

# ════════════════════════════════════════════════════════════════
# ⑤ 프로젝트 파일 구조  (Col1, R2, h=920)
# ════════════════════════════════════════════════════════════════
cy5, PAD5 = section_card(d, X1, R2Y, COL_W, H2, 5, "프로젝트 파일 구조")
x5 = X1+PAD5; w5 = COL_W-PAD5*2

# 트리 문자 대신 Pretendard로 표현 가능한 ASCII 방식 사용
code_block(d, x5, cy5, w5, [
    "your project/",
    "  CLAUDE.md",
    "  .claude/",
    "    settings.json",
    "    settings.local.json",
    "    skills/",
    "      code-review/",
    "        SKILL.md",
    "      testing/",
    "        SKILL.md",
    "      helpers.py",
    "  commands/",
    "    deploy.md",
    "  agents/",
    "    security-reviewer.md",
    "  .gitignore",
])

# ════════════════════════════════════════════════════════════════
# ⑥ 스킬 추가 — 슈퍼파워  (Col2, R2 상단, h=620)
# ════════════════════════════════════════════════════════════════
cy6, PAD6 = section_card(d, X2, R2Y, COL_W, S6H, 6, "스킬 추가 (슈퍼파워)")
x6 = X2+PAD6; w6 = COL_W-PAD6*2

put_sz(d, x6, cy6,
    "스킬 = 클로드가 자연어로 자동 호출하는 마크다운 가이드",
    SZ["body"], "r", BODY); cy6 += 30

for label, path in [("프로젝트 스킬", ".claude/skills/<name>/SKILL.md"),
                    ("개인 스킬",     "~/.claude/skills/<name>/SKILL.md")]:
    put_sz(d, x6, cy6, label, SZ["label"], "sb", BLK); cy6 += 24
    cy6 = code_block(d, x6, cy6, w6, [path])+10

cy6 += 6; hrule(d, x6, cy6, w6); cy6 += 14

put_sz(d, x6, cy6,
    "Description 필드가 자동 활성화에 핵심입니다.",
    SZ["body"], "r", ORANGE_D); cy6 += 30

cy6 = code_block(d, x6, cy6, w6, [
    "name: testing patterns",
    "description: Jest testing patterns",
    "allowed tools: Read, Grep, Glob",
])+12

code_block(d, x6, cy6, w6, [
    "# Testing Patterns",
    "Use describe + it + AAA pattern",
    "Use factory mocks",
])

# ════════════════════════════════════════════════════════════════
# ⑦ AI 엔지니어를 위한 스킬 아이디어  (Col2, R2 하단, h=276)
# ════════════════════════════════════════════════════════════════
cy7, PAD7 = section_card(d, X2, R2Y+S6H+24, COL_W, S7H, 7, "AI 엔지니어를 위한 스킬 아이디어")
x7 = X2+PAD7; half7 = (COL_W-PAD7*2)//2

f_body = F(SZ["bullet"], "r")
for i, (a, b) in enumerate([("code-review", "docker-deploy"),
                              ("testing patterns", "codebase-visualizer"),
                              ("commit messages", "api-design")]):
    iy = cy7 + i*34
    d.text((x7,       iy), "○ "+a, font=f_body, fill=BODY)
    d.text((x7+half7, iy), "○ "+b, font=f_body, fill=BODY)

# ════════════════════════════════════════════════════════════════
# ⑧ 훅 설정하기  (Col3, R2 상단, h=600)
# ════════════════════════════════════════════════════════════════
cy8, PAD8 = section_card(d, X3, R2Y, COL_W, S8H, 8, "훅 설정하기")
x8 = X3+PAD8; w8 = COL_W-PAD8*2

put_sz(d, x8, cy8, "훅 = 결정론적 콜백", SZ["body"], "r", BODY); cy8 += 28

bx8 = x8
for tag in ["PreToolUse", "PostToolUse", "Notification"]:
    pw, ph = pill(d, bx8, cy8, tag); bx8 += pw+6
cy8 += ph+14

cy8 = code_block(d, x8, cy8, w8, [
    '"hooks": {',
    '  "PreToolUse": [{',
    '    "matcher": "Bash",',
    '    "hooks": [{',
    '      "type": "command",',
    '      "command": "scripts/sec.sh",',
    '      "timeout": 5',
    '    }]',
    '  }]',
    '}',
])+14

put_sz(d, x8, cy8, "Exit codes:", SZ["body"], "sb", BLK)
ex8 = x8 + tw(d, "Exit codes:", F(SZ["body"],"sb")) + 10
for txt, bg in [("0  allow", (165,165,165)), ("2  block", ORANGE)]:
    pw2, ph2 = pill(d, ex8, cy8-4, txt, bg=bg); ex8 += pw2+6

# ════════════════════════════════════════════════════════════════
# ⑨ 권한 & 안전  (Col3, R2 하단, h=296)
# ════════════════════════════════════════════════════════════════
cy9, PAD9 = section_card(d, X3, R2Y+S8H+24, COL_W, S9H, 9, "권한 & 안전")
x9 = X3+PAD9; w9 = COL_W-PAD9*2

code_block(d, x9, cy9, w9, [
    '{',
    '  "permissions": {',
    '    "allow": [',
    '      "Read:*",',
    '      "Bash:git:*",',
    '      "Write:*:*.md"],',
    '    "deny": [',
    '      "Read:env:*",',
    '      "Bash:sudo:*"]',
    '  }',
    '}',
])

# ════════════════════════════════════════════════════════════════
# ⑩ 4계층 아키텍처  (Col1, R3, h=360)
# ════════════════════════════════════════════════════════════════
cy10, PAD10 = section_card(d, X1, R3Y, COL_W, H3, 10, "4계층 아키텍처")
x10 = X1+PAD10; w10 = COL_W-PAD10*2

layers = [
    ("L1 – CLAUDE.md",   "영구 컨텍스트와 규칙"),
    ("L2 – 스킬",         "자동 호출 지식 팩"),
    ("L3 – 훅",           "안전 게이트와 자동화"),
    ("L4 – 에이전트",     "자체 컨텍스트를 가진 서브에이전트"),
]
LH10 = 58
for i, (lbl, desc) in enumerate(layers):
    ly = cy10 + i*LH10
    bg10 = LIGHT_O if i%2==0 else CARD_BG
    d.rounded_rectangle([x10, ly, x10+w10, ly+LH10-4], radius=6, fill=bg10)
    put_sz(d, x10+12, ly+8,  lbl,  SZ["label"],  "b",  ORANGE_D)
    put_sz(d, x10+12, ly+32, desc, SZ["body"]-1, "r",  BODY)

# ════════════════════════════════════════════════════════════════
# ⑪ 일일 워크플로우 패턴  (Col2, R3, h=360)
# ════════════════════════════════════════════════════════════════
cy11, PAD11 = section_card(d, X2, R3Y, COL_W, H3, 11, "일일 워크플로우 패턴")
x11 = X2+PAD11; w11 = COL_W-PAD11*2

steps11 = [
    "cd project && claude",
    "Shift + Tab + Tab  →  Plan Mode",
    "기능 의도 서술",
    "Shift + Tab  →  Auto Accept",
    "/compact",
    "Esc Esc + rewind",
    "자주 커밋",
    "기능마다 새 세션 시작",
]
LH11 = 32
for i, step in enumerate(steps11):
    sy11 = cy11 + i*LH11
    bg11 = CODE_BG if i%2==0 else (248,241,232)
    d.rounded_rectangle([x11, sy11, x11+w11, sy11+LH11-2], radius=4, fill=bg11)
    put_sz(d, x11+14, sy11+7, step, SZ["body"]-1,
           "r" if i%2==0 else "sb", BLK)

# ════════════════════════════════════════════════════════════════
# ⑫ 빠른 참조  (Col3, R3, h=360)
# ════════════════════════════════════════════════════════════════
cy12, PAD12 = section_card(d, X3, R3Y, COL_W, H3, 12, "빠른 참조")
x12 = X3+PAD12; w12 = COL_W-PAD12*2

ref12 = [
    ("/init",       "CLAUDE.md 생성"),
    ("/doccat",     "설치 확인"),
    ("/compact",    "컨텍스트 압축"),
    ("Shift+Tab",   "자동 수락 전환"),
    ("Tab",         "확장 사고 전환"),
    ("Esc Esc",     "메뉴 되감기"),
]
split12 = w12//2
LH12 = 38
for i, (cmd, desc) in enumerate(ref12):
    ry = cy12 + i*LH12
    bg12 = CODE_BG if i%2==0 else CARD_BG
    d.rounded_rectangle([x12, ry, x12+w12, ry+LH12-2], radius=4, fill=bg12)
    d.rectangle([x12+split12-1, ry, x12+split12, ry+LH12-2], fill=CARD_BD)
    put_sz(d, x12+12,          ry+10, cmd,  SZ["label"], "b",  ORANGE_D)
    put_sz(d, x12+split12+12,  ry+10, desc, SZ["body"],  "r",  BODY)

# ── 최하단 서명 ───────────────────────────────────────────────
put_sz(d, OUTER_M, H-38,
    "DataBridge × Fastcampus  —  Claude Code 실무 완성  |  Pretendard · Orange Theme",
    SZ["dim"], "r", DIM)

# ── 저장 ─────────────────────────────────────────────────────
os.makedirs("/tmp/Script-repo/output/v2", exist_ok=True)
out = "/tmp/Script-repo/output/v2/cheatsheet.png"
img.save(out)
print(f"✓  {out}  ({W}×{H})")
