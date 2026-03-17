#!/usr/bin/env python3
"""
클로드 코드 워크플로우 치트시트 v4 — 최대 가독성
2880 × 2500px  /  Pretendard  /  섹션타이틀 30px / 본문 22px / 코드 20px
"""
from PIL import Image, ImageDraw, ImageFont
import os

# ── 캔버스 ────────────────────────────────────────────────────
W, H      = 2880, 2500
MARGIN    = 80
COL_GAP   = 32
HEADER_H  = 168

COL_W = (W - MARGIN*2 - COL_GAP*2) // 3   # 912
X1 = MARGIN                                 # 80
X2 = MARGIN + COL_W + COL_GAP              # 1024
X3 = MARGIN + (COL_W + COL_GAP)*2          # 1968

# ── 폰트 크기 ─────────────────────────────────────────────────
HT   = 68   # 헤더 타이틀
HS   = 18   # 헤더 서브
ST   = 28   # 섹션 카드 타이틀
BD   = 22   # 본문
CD   = 20   # 코드 블록
BL   = 22   # 불릿
DM   = 18   # 흐린 텍스트 / 설명
LB   = 20   # 소제목
PL   = 18   # pill 태그
BG_N = 18   # 배지 번호

# ── 색상 ─────────────────────────────────────────────────────
BG_C    = (253, 245, 235)   # 전체 배경
CARD    = (255, 255, 255)   # 카드 배경
BORDER  = (226, 214, 198)   # 카드 테두리
CODE_BG = (235, 223, 206)   # 코드 블록 배경
ORANGE  = (243, 123, 28)    # 오렌지
OD      = (206, 84, 6)      # 진한 오렌지
BLACK   = (18, 18, 18)      # 제목
BODY_C  = (52, 52, 52)      # 본문
DIM_C   = (138, 122, 104)   # 흐린 텍스트
CODE_C  = (36, 36, 36)      # 코드 텍스트
WHITE   = (255, 255, 255)
LIGHT_O = (255, 239, 218)   # 연한 오렌지 배경

# ── 폰트 로더 ─────────────────────────────────────────────────
FP = {
    "r":  "/Users/sy/Library/Fonts/Pretendard-Regular.otf",
    "sb": "/Users/sy/Library/Fonts/Pretendard-SemiBold.otf",
    "b":  "/Users/sy/Library/Fonts/Pretendard-Bold.otf",
    "mono": "/System/Library/Fonts/Menlo.ttc",
}
_fc = {}
def F(sz, wt="r"):
    k = (sz, wt)
    if k not in _fc:
        path = FP.get(wt, FP["r"])
        try: _fc[k] = ImageFont.truetype(path, sz)
        except: _fc[k] = ImageFont.load_default()
    return _fc[k]

def tw(d, t, f): return d.textbbox((0,0), t, font=f)[2]
def th(d, t, f): b = d.textbbox((0,0), t, font=f); return b[3]-b[1]

def text(d, x, y, s, sz, wt, color):
    f = F(sz, wt); d.text((x,y), s, font=f, fill=color)
    return th(d, s, f)

def wtext(d, x, y, s, sz, wt, color, maxw, lh=1.7):
    f = F(sz, wt); words = s.split(); lines, cur = [], ""
    for w in words:
        test = (cur+" "+w).strip()
        if tw(d,test,f) > maxw and cur: lines.append(cur); cur=w
        else: cur=test
    if cur: lines.append(cur)
    for line in lines:
        d.text((x,y), line, font=f, fill=color); y += int(th(d,line,f)*lh)
    return y

def rule(d, x, y, w, c=BORDER, h=1):
    d.rectangle([x,y,x+w,y+h], fill=c)

# ── 컴포넌트 ─────────────────────────────────────────────────
BR = 24   # 배지 반지름

def badge(d, x, y, n):
    d.ellipse([x,y,x+BR*2,y+BR*2], fill=ORANGE)
    f = F(BG_N, "b"); ns = str(n)
    nw=tw(d,ns,f); nh=th(d,ns,f)
    d.text((x+BR-nw//2, y+BR-nh//2), ns, font=f, fill=WHITE)
    return BR*2   # 48

def pill(d, x, y, s, sz=PL, bg=ORANGE, fg=WHITE, r=7):
    f = F(sz,"sb")
    pw=tw(d,s,f)+26; ph=th(d,s,f)+14
    d.rounded_rectangle([x,y,x+pw,y+ph], radius=r, fill=bg)
    d.text((x+13,y+7), s, font=f, fill=fg)
    return pw+8, ph+4

CARD_PAD = 26

def card(d, x, y, w, h, n, title):
    """카드 그리기 → (콘텐츠 시작 y, 내부 패딩값)"""
    d.rounded_rectangle([x,y,x+w,y+h], radius=14, fill=CARD, outline=BORDER, width=1)
    bh = badge(d, x+CARD_PAD, y+CARD_PAD, n)
    text(d, x+CARD_PAD+bh+14, y+CARD_PAD+7, title, ST, "b", BLACK)
    hy = y+CARD_PAD+bh+16
    rule(d, x+CARD_PAD, hy, w-CARD_PAD*2)
    return hy+16, CARD_PAD

CODE_LH = 34   # 코드 라인 높이
CODE_PAD= 20   # 코드 블록 패딩

def code(d, x, y, w, lines, bg=CODE_BG):
    """코드 블록: 트리/ASCII는 Menlo, ← 이후 한글 주석은 Pretendard로 분리 렌더링"""
    bh = CODE_PAD*2 + len(lines)*CODE_LH
    d.rounded_rectangle([x,y,x+w,y+bh], radius=8, fill=bg)
    cy = y+CODE_PAD
    f_mono = F(CD, "mono")
    f_ko   = F(CD-2, "r")   # Pretendard, 한글 주석용
    for line in lines:
        if "←" in line:
            parts = line.split("←", 1)
            main  = parts[0].rstrip()
            annot = "← " + parts[1].strip()
            d.text((x+CODE_PAD, cy), main, font=f_mono, fill=CODE_C)
            main_w = d.textbbox((0,0), main, font=f_mono)[2]
            d.text((x+CODE_PAD + main_w + 6, cy+2), annot, font=f_ko, fill=DIM_C)
        else:
            d.text((x+CODE_PAD, cy), line, font=f_mono, fill=CODE_C)
        cy += CODE_LH
    return y+bh

BL_LH = 40   # 불릿 라인 높이

def bullets(d, x, y, items):
    f = F(BL,"r")
    for item in items:
        d.text((x,    y), "○",    font=f, fill=ORANGE)
        d.text((x+28, y), item,   font=f, fill=BODY_C)
        y += BL_LH
    return y

# ── 행 높이 계산 ──────────────────────────────────────────────
# S1 시작하기
S1H = (CARD_PAD + BR*2 + 16 + CODE_PAD*2 + CODE_LH      # header + code1(1줄)
       + 18                                                # gap
       + CODE_PAD*2 + CODE_LH*3                           # code2(3줄)
       + 18                                                # gap
       + th(Image.new("RGB",(1,1)), "", "xy")[0] if False else  # dummy
       0) or 390   # 직접 설정

S1H = 440
# S4 = 7 bullets × 40 + card header
S4_CONTENT = 7*BL_LH
S4H = CARD_PAD + BR*2 + 16 + S4_CONTENT + CARD_PAD + 20
S4H = 440

H1 = S1H + 28 + S4H   # 390+28+440 = 858

# S6 = 스킬, S7 = 아이디어
S6H = 750
S7H = 522
H2  = S6H + 28 + S7H   # col2 기준
S8H = 760
S9H = H2 - S8H - 28    # col3 기준

H3 = 420

CONTENT_Y = HEADER_H + 36
R1Y = CONTENT_Y
R2Y = R1Y + H1 + 28
R3Y = R2Y + H2 + 28

TOTAL_H = R3Y + H3 + 80
print(f"레이아웃: {W}×{TOTAL_H}  (H1={H1} H2={H2} H3={H3})")

# ── 실제 이미지 크기 재조정 ───────────────────────────────────
H_ACTUAL = TOTAL_H
img = Image.new("RGB", (W, H_ACTUAL), BG_C)
d   = ImageDraw.Draw(img)

# ════════════════════════════════════════════════════════════════
# 헤더
# ════════════════════════════════════════════════════════════════
tx = MARGIN; ty = 44
_f_ht = F(HT, "b")
w1 = tw(d, "클로드 코드", _f_ht)
text(d, tx, ty, "클로드 코드", HT, "b", BLACK)
text(d, tx+w1+20, ty, "워크플로우 치트시트", HT, "b", OD)

sy = ty + th(d,"A",F(HT,"b")) + 14
text(d, tx, sy,
     "시작하기  ·  프로젝트 설정  ·  파일 구조  ·  스킬  ·  훅  ·  메모리  ·  워크플로우  ·  2026 Edition",
     HS, "r", DIM_C)
rule(d, MARGIN, HEADER_H-2, W-MARGIN*2, BORDER)

# ════════════════════════════════════════════════════════════════
# ① 시작하기
# ════════════════════════════════════════════════════════════════
cy, P = card(d, X1, R1Y, COL_W, S1H, 1, "시작하기")
x = X1+P; w = COL_W-P*2

cy = code(d, x, cy, w,
    ["curl -fsSL https://claude.ai/install.sh | bash"]) + 10

text(d, x, cy, "한 번 설치 후 어떤 프로젝트에서나 claude 명령 사용 가능", DM, "r", DIM_C); cy+=28

cy = code(d, x, cy, w,
    ["cd your-project   ← 프로젝트 폴더 이동",
     "claude            ← 클로드 세션 시작",
     "/init             ← CLAUDE.md 자동 생성"]) + 14

text(d, x, cy, "코드베이스를 스캔해 프로젝트 구조·명령어·규칙을 CLAUDE.md에 자동 저장. 매 세션 시작 시 자동 로드.",
     BD, "r", BODY_C)

# ════════════════════════════════════════════════════════════════
# ④ CLAUDE.md 모범 사례
# ════════════════════════════════════════════════════════════════
cy4, P4 = card(d, X1, R1Y+S1H+28, COL_W, S4H, 4, "CLAUDE.md 모범 사례")
bullets(d, X1+P4, cy4, [
    "/init 생성 후 불필요한 줄 직접 정리",
    "Python 3.11, 탭 2칸 등 구체적으로 명시",
    "원본 데이터 수정 금지 등 명시적 금지 추가",
    "@파일명으로 설계 문서·설정 파일 참조",
    "PR→리뷰→커밋 순서 등 워크플로우 기록",
    "항목 최소화 · 200줄 이하로 유지",
    "팀 공유 규칙은 Git에 커밋해 동기화",
])

# ════════════════════════════════════════════════════════════════
# ② CLAUDE.md 이해하기
# ════════════════════════════════════════════════════════════════
cy2, P2 = card(d, X2, R1Y, COL_W, H1, 2, "CLAUDE.md 이해하기")
x2 = X2+P2; w2 = COL_W-P2*2

text(d, x2, cy2, "CLAUDE.md = 클로드의 프로젝트 영구 메모리.", BD, "r", BODY_C); cy2+=32
text(d, x2, cy2, "매 세션 시작 시 자동으로 로드됩니다.",        BD, "r", BODY_C); cy2+=42

# WHAT / WHY / HOW
bx2=x2
for tag in ["WHAT","WHY","HOW"]:
    pw,ph = pill(d, bx2, cy2, tag); bx2+=pw+8
cy2 += ph+18

# 3컬럼 항목
col3 = w2//3
col_data=[("WHAT",["기술 스택","디렉토리 맵","아키텍처"]),
          ("WHY", ["각 모듈 목적","디자인 결정"]),
          ("HOW", ["빌드/테스트","lint 명령어","워크플로우","주의사항"])]
max_h=0
for i,(lbl,items) in enumerate(col_data):
    bx=x2+i*col3; iy=cy2
    text(d, bx, iy, lbl, LB, "sb", ORANGE); iy+=28
    for it in items:
        text(d, bx, iy, "· "+it, DM, "r", BODY_C); iy+=26
    max_h=max(max_h, iy-cy2)
cy2+=max_h+18
rule(d, x2, cy2, w2); cy2+=18

code(d, x2, cy2, w2, [
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
# ③ 메모리 파일 계층 구조
# ════════════════════════════════════════════════════════════════
cy3, P3 = card(d, X3, R1Y, COL_W, H1, 3, "메모리 파일 계층 구조")
x3=X3+P3; w3=COL_W-P3*2

tree=[("~/.claude/CLAUDE.md","전역 — 모든 프로젝트"),
      ("~/CLAUDE.md",         "부모 — 모노레포 루트"),
      ("./CLAUDE.md",         "프로젝트 — git에 공유"),
      ("./frontend/CLAUDE.md","서브폴더 — 범위 제한")]
for path,desc in tree:
    cy3=code(d, x3, cy3, w3, [path])+8
    text(d, x3+16, cy3, desc, DM, "r", DIM_C); cy3+=32

cy3+=12; rule(d, x3, cy3, w3); cy3+=18
bullets(d, x3, cy3, [
    "각 파일 200줄 이하 유지",
    "서브폴더 파일은 컨텍스트 추가",
    "부모 컨텍스트 덮어쓰기 금지",
])

# ════════════════════════════════════════════════════════════════
# ⑤ 프로젝트 파일 구조
# ════════════════════════════════════════════════════════════════
cy5, P5 = card(d, X1, R2Y, COL_W, H2, 5, "프로젝트 파일 구조")
x5=X1+P5; w5=COL_W-P5*2

# 설정 스코프 4단계 라벨
cy5+=4
scope_data = [
    ("Managed", "server / plist", "조직 전체 강제 적용"),
    ("User",    "~/.claude/",     "개인, 모든 프로젝트"),
    ("Project", ".claude/",       "팀 공유 (git 커밋)"),
    ("Local",   "settings.local.json", "개인 × 이 프로젝트"),
]
for lbl, path, desc in scope_data:
    lx = x5
    pw, ph = pill(d, lx, cy5, lbl, sz=16, bg=CODE_BG, fg=OD, r=5)
    lx += pw + 10
    text(d, lx, cy5+2, path, CD, "sb", BLACK)
    path_w = tw(d, path, F(CD, "sb"))
    text(d, lx + path_w + 10, cy5+4, "← "+desc, 16, "r", DIM_C)
    cy5 += ph + 8
cy5 += 14
rule(d, x5, cy5, w5); cy5 += 18

# 터미널 트리
cy5 += 8
cy5 = code(d, x5, cy5, w5, [
    "your-project/",
    "├── CLAUDE.md              ← 프로젝트 메모리",
    "├── .claude/",
    "│   ├── settings.json      ← 팀 설정 (git 공유)",
    "│   ├── settings.local.json  ← 개인 (gitignore)",
    "│   ├── rules/             ← 파일 유형별 규칙",
    "│   │   ├── *.test.ts.md",
    "│   │   └── api-routes.md",
    "│   ├── skills/",
    "│   │   ├── code-review/",
    "│   │   │   ├── SKILL.md   ← 핵심 지침서 (필수)",
    "│   │   │   └── reference.md",
    "│   │   └── testing/",
    "│   │       └── SKILL.md",
    "│   └── commands/          ← 커스텀 슬래시 커맨드",
    "│       ├── deploy.md      ← /deploy",
    "│       └── review.md      ← /review",
    "└── .gitignore",
]) + 18

rule(d, x5, cy5, w5); cy5 += 18
text(d, x5, cy5, "⚑  settings.local.json 은 반드시 .gitignore 에 추가", BD, "r", OD)

# ════════════════════════════════════════════════════════════════
# ⑥ 스킬 추가
# ════════════════════════════════════════════════════════════════
cy6, P6 = card(d, X2, R2Y, COL_W, S6H, 6, "스킬 추가 (슈퍼파워)")
x6=X2+P6; w6=COL_W-P6*2

text(d, x6, cy6,
     "스킬 = 클로드가 자연어로 자동 호출하는 마크다운 가이드",
     BD, "r", BODY_C); cy6+=36

for lbl,path in [("프로젝트 스킬", ".claude/skills/<name>/SKILL.md"),
                  ("개인 스킬",    "~/.claude/skills/<name>/SKILL.md")]:
    text(d, x6, cy6, lbl, LB, "sb", BLACK); cy6+=28
    cy6=code(d, x6, cy6, w6, [path])+12

cy6+=8; rule(d, x6, cy6, w6); cy6+=16

text(d, x6, cy6,
     "Description 필드가 자동 활성화에 핵심입니다.",
     BD, "r", OD); cy6+=36

cy6=code(d, x6, cy6, w6, [
    "name: code-review-guide",
    "description: PR review automation patterns",
    "allowed tools: Read, Grep, Glob",
])+14

code(d, x6, cy6, w6, [
    "├── SKILL.md        ← 핵심 지침서 (필수, 1개)",
    "├── reference.md    ← 참고 자료 (선택)",
    "└── scripts/",
    "    └── helper.py   ← 실행 스크립트",
])

# ════════════════════════════════════════════════════════════════
# ⑦ AI 엔지니어 스킬 아이디어
# ════════════════════════════════════════════════════════════════
cy7, P7 = card(d, X2, R2Y+S6H+28, COL_W, S7H, 7, "유용한 스킬 아이디어")
x7=X2+P7; half7=(COL_W-P7*2)//2
f_bl=F(BL,"r")
for i,(a,b) in enumerate([("코드 리뷰 자동화", "도커 배포 가이드"),
                           ("테스트 패턴 모음", "코드베이스 시각화"),
                           ("커밋 메시지 규칙", "API 설계 표준")]):
    iy=cy7+i*44
    d.text((x7,       iy), "○ "+a, font=f_bl, fill=BODY_C)
    d.text((x7+half7, iy), "○ "+b, font=f_bl, fill=BODY_C)

# ════════════════════════════════════════════════════════════════
# ⑧ 훅 설정하기
# ════════════════════════════════════════════════════════════════
cy8, P8 = card(d, X3, R2Y, COL_W, S8H, 8, "훅 설정하기")
x8=X3+P8; w8=COL_W-P8*2

text(d, x8, cy8, "특정 이벤트 발생 시 셸 커맨드를 자동 실행하는 트리거.", BD, "r", BODY_C); cy8+=36

# 훅 타입 설명
hook_types = [
    ("PreToolUse",    "도구 실행 전  · 승인·차단 가능"),
    ("PostToolUse",   "도구 실행 후  · 결과 검증·후처리"),
    ("Notification",  "완료·오류 알림 · 슬랙 등 연동"),
]
for tag, desc in hook_types:
    pw, ph = pill(d, x8, cy8, tag)
    text(d, x8+pw+12, cy8+3, desc, DM, "r", DIM_C)
    cy8 += ph + 10
cy8 += 8

cy8=code(d, x8, cy8, w8, [
    '"hooks": {',
    '  "PreToolUse": [{',
    '    "matcher": "Bash",  ← Bash 도구에만 적용',
    '    "hooks": [{',
    '      "type": "command",',
    '      "command": "scripts/sec.sh",',
    '      "timeout": 5',
    '    }]',
    '  }]',
    '}',
])+14

text(d, x8, cy8, "Exit code  0 = 계속 진행   /   2 = 실행 차단", DM, "r", BODY_C); cy8+=30
text(d, x8, cy8, "matcher 생략 시 모든 도구에 적용됩니다.", DM, "r", DIM_C)

# ════════════════════════════════════════════════════════════════
# ⑨ 권한 & 안전
# ════════════════════════════════════════════════════════════════
cy9, P9 = card(d, X3, R2Y+S8H+28, COL_W, S9H, 9, "권한 & 안전")
x9=X3+P9; w9=COL_W-P9*2

text(d, x9, cy9, "settings.json 에서 허용·차단 규칙 설정.", BD, "r", BODY_C); cy9+=34

code(d, x9, cy9, w9, [
    '"permissions": {',
    '  "allow": [',
    '    "Read:*",         ← 모든 파일 읽기 허용',
    '    "Bash:git:*",     ← git 명령어만 실행 가능',
    '    "Write:*:*.md"    ← .md 파일만 쓰기 허용',
    '  ],',
    '  "deny": [',
    '    "Read:env:*",     ← 환경변수 읽기 금지',
    '    "Bash:sudo:*"     ← sudo 명령어 전면 차단',
    '  ]',
    '}',
])

# ════════════════════════════════════════════════════════════════
# ⑩ 4계층 아키텍처
# ════════════════════════════════════════════════════════════════
cy10, P10 = card(d, X1, R3Y, COL_W, H3, 10, "4계층 아키텍처")
x10=X1+P10; w10=COL_W-P10*2

layers=[("L1  CLAUDE.md",  "매 세션 자동 로드 — 팀 전체 규칙·컨텍스트 공유"),
        ("L2  스킬",        "자연어로 자동 호출 — 도구·프레임워크 전문 지식 패키지"),
        ("L3  훅",          "도구 실행 전·후 자동 검증 — 보안 게이트·알림"),
        ("L4  에이전트",    "독립 컨텍스트로 복잡한 작업을 병렬 처리")]
LH10=68
for i,(lbl,desc) in enumerate(layers):
    ly=cy10+i*LH10
    bg10=LIGHT_O if i%2==0 else CARD
    d.rounded_rectangle([x10,ly,x10+w10,ly+LH10-4], radius=7, fill=bg10)
    text(d, x10+14, ly+10,  lbl,  LB, "b",  OD)
    text(d, x10+14, ly+38,  desc, DM, "r",  BODY_C)

# ════════════════════════════════════════════════════════════════
# ⑪ 일일 워크플로우 패턴
# ════════════════════════════════════════════════════════════════
cy11, P11 = card(d, X2, R3Y, COL_W, H3, 11, "일일 워크플로우 패턴")
x11=X2+P11; w11=COL_W-P11*2

steps=[
    ("cd project && claude",         "프로젝트 폴더에서 세션 시작"),
    ("Shift+Tab+Tab  → Plan Mode",   "실행 전 계획 먼저 검토·수정"),
    ("기능 의도를 명확히 설명",        "원하는 결과 + 맥락 함께 전달"),
    ("Shift+Tab  → Auto Accept",     "파일 수정 자동 수락 ON"),
    ("/compact",                      "긴 대화 요약 — 토큰 절약"),
    ("Esc Esc  → rewind",            "직전 작업 취소·되감기"),
    ("자주 커밋 (기능 단위)",          "복구 가능한 체크포인트 확보"),
    ("기능마다 새 세션 시작",          "컨텍스트 오염 방지"),
]
LH11=38
sp11 = int(w11 * 0.52)
for i,(step, hint) in enumerate(steps):
    sy11=cy11+i*LH11
    bg11=CODE_BG if i%2==0 else (248,240,230)
    d.rounded_rectangle([x11,sy11,x11+w11,sy11+LH11-2], radius=5, fill=bg11)
    d.rectangle([x11+sp11-1,sy11,x11+sp11,sy11+LH11-2], fill=BORDER)
    text(d, x11+12, sy11+9, step, 18, "sb", BLACK)
    text(d, x11+sp11+12, sy11+9, hint, 18, "r", DIM_C)

# ════════════════════════════════════════════════════════════════
# ⑫ 빠른 참조
# ════════════════════════════════════════════════════════════════
cy12, P12 = card(d, X3, R3Y, COL_W, H3, 12, "빠른 참조")
x12=X3+P12; w12=COL_W-P12*2

ref=[("/init",      "프로젝트 분석 후 CLAUDE.md 자동 생성"),
     ("/compact",   "대화 요약 — 토큰·비용 절약"),
     ("/config",    "설정 화면 열기"),
     ("Shift+Tab",  "파일 수정 자동 수락 ON/OFF"),
     ("Tab",        "확장 사고(Extended Thinking) 전환"),
     ("Esc Esc",    "현재 작업 되감기·취소")]
sp12=w12//2; LH12=46
for i,(cmd,desc) in enumerate(ref):
    ry=cy12+i*LH12
    bg12=CODE_BG if i%2==0 else CARD
    d.rounded_rectangle([x12,ry,x12+w12,ry+LH12-2], radius=5, fill=bg12)
    d.rectangle([x12+sp12-1,ry,x12+sp12,ry+LH12-2], fill=BORDER)
    text(d, x12+14,      ry+12, cmd,  LB, "b", OD)
    text(d, x12+sp12+14, ry+12, desc, BD, "r", BODY_C)

# ── 서명 ─────────────────────────────────────────────────────
text(d, MARGIN, H_ACTUAL-44,
     "DataBridge × Fastcampus  —  Claude Code 실무 완성  |  Pretendard · Orange Theme",
     DM, "r", DIM_C)

# ── 저장 ─────────────────────────────────────────────────────
os.makedirs("/tmp/Script-repo/output/v2", exist_ok=True)
out="/tmp/Script-repo/output/v2/cheatsheet.png"
img.save(out)
print(f"✓  {out}  ({W}×{H_ACTUAL})")
