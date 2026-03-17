#!/usr/bin/env python3
"""
CH01 PPT 스타일 슬라이드 생성기
1920×1080 / Orange Design System / Pretendard + Menlo
"""
from PIL import Image, ImageDraw, ImageFont
import os, math

# ── 캔버스 ─────────────────────────────────────────────────
W, H = 1920, 1080
OUT  = "/tmp/Script-repo/output/ch01_slides"
os.makedirs(OUT, exist_ok=True)

# ── 색상 ──────────────────────────────────────────────────
BG      = (245, 240, 232)   # 크림 배경
WHITE   = (255, 255, 255)
ORANGE  = (232, 115, 74)    # 포인트 오렌지
OD      = (200, 80, 40)     # 진한 오렌지
BLACK   = (24, 24, 24)
BODY    = (60, 60, 60)
DIM     = (140, 125, 108)
CARD    = (255, 255, 255)
BORDER  = (220, 208, 194)
CODE_BG = (235, 223, 206)
CODE_C  = (40, 40, 40)
SIDEBAR = (232, 115, 74)    # 왼쪽 사이드바

# ── 폰트 ──────────────────────────────────────────────────
FP = {
    "r":  "/Users/sy/Library/Fonts/Pretendard-Regular.otf",
    "sb": "/Users/sy/Library/Fonts/Pretendard-SemiBold.otf",
    "b":  "/Users/sy/Library/Fonts/Pretendard-Bold.otf",
    "eb": "/Users/sy/Library/Fonts/Pretendard-ExtraBold.otf",
    "mono": "/System/Library/Fonts/Menlo.ttc",
}
_fc = {}
def F(sz, wt="r"):
    k=(sz,wt)
    if k not in _fc:
        try: _fc[k] = ImageFont.truetype(FP.get(wt, FP["r"]), sz)
        except: _fc[k] = ImageFont.load_default()
    return _fc[k]

def tw(d, t, f): return d.textbbox((0,0), t, font=f)[2]
def th(d, t, f): b=d.textbbox((0,0),t,font=f); return b[3]-b[1]

def text(d, x, y, s, sz, wt, color, align="left"):
    f=F(sz,wt)
    if align=="center":
        x = x - tw(d,s,f)//2
    d.text((x,y), s, font=f, fill=color)
    return th(d,s,f)

def wtext(d, x, y, s, sz, wt, color, maxw, lh=1.6):
    """자동 줄바꿈 텍스트, 최종 y 반환"""
    f=F(sz,wt); words=s.split(); lines=[]; cur=""
    for w in words:
        test=(cur+" "+w).strip()
        if tw(d,test,f) > maxw and cur:
            lines.append(cur); cur=w
        else: cur=test
    if cur: lines.append(cur)
    for line in lines:
        d.text((x,y), line, font=f, fill=color)
        y += int(th(d,line,f)*lh)
    return y

def code_block(d, x, y, w, lines, bg=CODE_BG):
    """모노 코드 블록, 최종 y 반환"""
    PAD=24; LH=36
    bh = PAD*2 + len(lines)*LH
    d.rounded_rectangle([x,y,x+w,y+bh], radius=10, fill=bg)
    f_mono = F(22,"mono"); f_ko = F(20,"r")
    cy=y+PAD
    for line in lines:
        if "←" in line:
            parts=line.split("←",1)
            main=parts[0].rstrip()
            annot="← "+parts[1].strip()
            d.text((x+PAD,cy), main, font=f_mono, fill=CODE_C)
            mw=d.textbbox((0,0),main,font=f_mono)[2]
            d.text((x+PAD+mw+8,cy+3), annot, font=f_ko, fill=DIM)
        else:
            d.text((x+PAD,cy), line, font=f_mono, fill=CODE_C)
        cy+=LH
    return y+bh

def bullet_list(d, x, y, items, sz=28, lh=1.8, dot_color=ORANGE):
    """불릿 리스트, 최종 y 반환"""
    f=F(sz,"r"); fd=F(sz,"sb")
    for item in items:
        # 볼드 처리: **text** 패턴
        if item.startswith("**") and "**" in item[2:]:
            end=item.index("**",2)
            bold_part=item[2:end]
            rest=item[end+2:]
            d.text((x,y), "•", font=f, fill=dot_color)
            d.text((x+26,y), bold_part, font=fd, fill=BLACK)
            bw=tw(d,bold_part,fd)
            if rest:
                d.text((x+26+bw,y), rest, font=f, fill=BODY)
        else:
            d.text((x,y), "•", font=f, fill=dot_color)
            d.text((x+26,y), item, font=f, fill=BODY)
        y += int(th(d,item,f)*lh)
    return y

def sidebar(d, clip_num, clip_title, chapter="CH01"):
    """왼쪽 오렌지 사이드바"""
    SW=56
    d.rectangle([0,0,SW,H], fill=ORANGE)
    # 챕터 번호 (세로 텍스트처럼 작은 글씨)
    f=F(18,"b")
    for i,ch in enumerate(chapter):
        d.text((SW//2-9, 40+i*20), ch, font=f, fill=WHITE)

def footer(d, slide_no, total, clip_id, clip_name):
    """하단 푸터"""
    FH=64
    d.rectangle([0,H-FH,W,H], fill=(60,50,42))
    # 왼쪽: 클립 ID
    f_sb=F(20,"sb"); f_r=F(20,"r")
    d.text((80, H-FH+22), clip_id, font=f_sb, fill=ORANGE)
    d.text((80+tw(d,clip_id,f_sb)+16, H-FH+22), clip_name, font=f_r, fill=(200,190,180))
    # 오른쪽: 슬라이드 번호
    pg=f"{slide_no} / {total}"
    d.text((W-80-tw(d,pg,f_r), H-FH+22), pg, font=f_r, fill=(180,170,160))
    # DataBridge 브랜드
    br="DataBridge × Fastcampus"
    d.text((W//2-tw(d,br,f_r)//2, H-FH+22), br, font=f_r, fill=(160,150,140))

def new_slide():
    img=Image.new("RGB",(W,H),BG)
    d=ImageDraw.Draw(img)
    return img, d

def save(img, filename):
    path=f"{OUT}/{filename}"
    img.save(path)
    print(f"✓ {path}")
    return path

# ══════════════════════════════════════════════════════════════
# SLIDE 01 — CH01 타이틀
# ══════════════════════════════════════════════════════════════
img,d = new_slide()
sidebar(d, 1, "", "CH01")

# 배경 대각선 장식
for i in range(0,H,60):
    d.line([(W-400,i),(W,i+400)], fill=(220,210,198), width=1)

# 중앙 콘텐츠
CX=W//2+40
d.rectangle([CX-320,300,CX+320,316], fill=ORANGE)
text(d, CX, 340, "CH01", 36, "b", ORANGE, "center")
text(d, CX, 395, "클로드 코드 첫 걸음", 78, "eb", BLACK, "center")
text(d, CX, 498, "에이전트 구조 · 설치 · 워크플로우 · 스킬 · 비용 관리", 28, "r", DIM, "center")

# 클립 목록 카드
items=[
    ("01", "클로드 코드란 무엇인가"),
    ("02", "설치 & 첫 번째 세션"),
    ("03", "CLAUDE.md — 프로젝트 메모리"),
    ("04", "기본 워크플로우"),
    ("05", "작업 모드"),
    ("06", "슬래시 커맨드 완전 정리"),
]
cx_card=240; cy_card=330; cw=480; ch_h=56
for num,title in items:
    d.rounded_rectangle([cx_card,cy_card,cx_card+cw,cy_card+ch_h], radius=10, fill=WHITE, outline=BORDER, width=1)
    f_num=F(20,"b"); f_t=F(22,"r")
    d.rounded_rectangle([cx_card+10,cy_card+10,cx_card+50,cy_card+46], radius=6, fill=ORANGE)
    d.text((cx_card+20,cy_card+14), num, font=f_num, fill=WHITE)
    d.text((cx_card+66,cy_card+16), title, font=f_t, fill=BODY)
    cy_card+=68

footer(d, 1, 10, "CH01", "클로드 코드 첫 걸음")
save(img, "01_title.png")

# ══════════════════════════════════════════════════════════════
# SLIDE 02 — CH01-01 / 두 가지 도구의 차이
# ══════════════════════════════════════════════════════════════
img,d = new_slide()
sidebar(d, 2, "", "CH01")
ML=100  # 메인 콘텐츠 좌측 여백

# 헤더 구역
d.rectangle([ML,0,W,120], fill=ORANGE)
text(d, ML+20, 28, "CH01-01  ·  클로드 코드란 무엇인가", 24, "r", WHITE)
text(d, ML+20, 62, "두 가지 도구의 차이", 42, "b", WHITE)

# 두 카드 비교
CW2=720; CH2=680; GAP=40
lx=ML+20; rx=lx+CW2+GAP; cy_c=150

# 챗GPT 카드
d.rounded_rectangle([lx,cy_c,lx+CW2,cy_c+CH2], radius=16, fill=WHITE, outline=BORDER, width=2)
d.rounded_rectangle([lx,cy_c,lx+CW2,cy_c+72], radius=16, fill=(220,210,200))
d.rectangle([lx,cy_c+56,lx+CW2,cy_c+72], fill=(220,210,200))
text(d, lx+CW2//2, cy_c+18, "ChatGPT", 32, "b", BODY, "center")
text(d, lx+CW2//2, cy_c+56, "대화 인터페이스", 20, "r", DIM, "center")
bullet_list(d, lx+40, cy_c+100, [
    "텍스트 입력 → 텍스트 응답",
    "파일 시스템 직접 접근 불가",
    "세션 종료 시 기억 초기화",
    "복사·붙여넣기로 코드 전달",
    "결과를 사람이 직접 적용",
], sz=26, lh=1.9, dot_color=(160,150,140))

# 클로드 코드 카드
d.rounded_rectangle([rx,cy_c,rx+CW2,cy_c+CH2], radius=16, fill=WHITE, outline=ORANGE, width=2)
d.rounded_rectangle([rx,cy_c,rx+CW2,cy_c+72], radius=16, fill=ORANGE)
d.rectangle([rx,cy_c+56,rx+CW2,cy_c+72], fill=ORANGE)
text(d, rx+CW2//2, cy_c+18, "Claude Code", 32, "b", WHITE, "center")
text(d, rx+CW2//2, cy_c+56, "에이전트 (Agent)", 20, "r", (255,230,215), "center")
bullet_list(d, rx+40, cy_c+100, [
    "터미널에서 실행 — 파일 직접 접근",
    "파일 읽기 · 쓰기 · 코드 실행",
    "CLAUDE.md로 프로젝트 맥락 유지",
    "코드 수정부터 실행까지 자동화",
    "결과를 스스로 검증하고 완료 보고",
], sz=26, lh=1.9)

# 핵심 요약 배너
d.rounded_rectangle([ML+20,H-180,W-60,H-80], radius=12, fill=CODE_BG)
text(d, W//2+40, H-164, "핵심 차이 —  ChatGPT는 '조언'을 주고,  Claude Code는 '직접 작업'을 수행합니다.", 26, "sb", OD, "center")

footer(d, 2, 10, "CH01-01", "클로드 코드란 무엇인가")
save(img, "02_comparison.png")

# ══════════════════════════════════════════════════════════════
# SLIDE 03 — 에이전트 구조 (루프)
# ══════════════════════════════════════════════════════════════
img,d = new_slide()
sidebar(d, 3, "", "CH01")

d.rectangle([ML,0,W,120], fill=ORANGE)
text(d, ML+20, 28, "CH01-01  ·  클로드 코드란 무엇인가", 24, "r", WHITE)
text(d, ML+20, 62, "에이전트 구조 — 에이전트 루프", 42, "b", WHITE)

# 루프 스텝 카드들 (가로 플로우)
steps=[
    ("사용자\n지시","요청을 전달받습니다"),
    ("계획","순서와 방법 결정"),
    ("도구\n선택","파일? 코드? 검색?"),
    ("실행","실제 작업 수행"),
    ("결과\n확인","성공 여부 검증"),
    ("완료","보고 또는 반복"),
]
nsteps=len(steps)
SW_s=220; SH_s=200; GAP_s=36
total_w=nsteps*SW_s+(nsteps-1)*GAP_s
sx=(W-ML-total_w)//2+ML
sy=200

for i,(title,desc) in enumerate(steps):
    x=sx+i*(SW_s+GAP_s)
    # 카드
    is_first = (i==0)
    bg_c=ORANGE if is_first else WHITE
    bd_c=ORANGE
    tc=WHITE if is_first else BLACK
    dc=WHITE if is_first else BODY
    d.rounded_rectangle([x,sy,x+SW_s,sy+SH_s], radius=14, fill=bg_c, outline=bd_c, width=2)
    # 번호
    d.ellipse([x+SW_s//2-16,sy+20,x+SW_s//2+16,sy+52], fill=bd_c if not is_first else WHITE)
    f_n=F(22,"b")
    nd=str(i+1); nw=tw(d,nd,f_n)
    d.text((x+SW_s//2-nw//2,sy+26), nd, font=f_n, fill=WHITE if not is_first else ORANGE)
    # 제목 (다중행)
    lines=title.split("\n")
    ty=sy+76
    for ln in lines:
        f_t=F(26,"b")
        d.text((x+SW_s//2-tw(d,ln,f_t)//2,ty), ln, font=f_t, fill=tc)
        ty+=34
    # 설명
    f_d=F(20,"r")
    d.text((x+SW_s//2-tw(d,desc,f_d)//2,sy+160), desc, font=f_d, fill=dc)
    # 화살표 (마지막 제외)
    if i < nsteps-1:
        ax=x+SW_s+8; ay=sy+SH_s//2
        d.polygon([(ax,ay-10),(ax+GAP_s-8,ay),(ax,ay+10)], fill=ORANGE)

# "이 과정이 반복된다" 레이블
text(d, W//2+40, sy+SH_s+30, "↑  이 과정이 반복되는 것을 에이전트 루프(Agent Loop)라고 합니다", 24, "r", DIM, "center")

# 하단 — 클로드 코드 도구 빠른 요약
cy_b=sy+SH_s+90
d.rounded_rectangle([ML+20,cy_b,W-60,cy_b+200], radius=12, fill=WHITE, outline=BORDER, width=1)
text(d, ML+60, cy_b+24, "클로드 코드가 루프에서 사용하는 도구", 26, "sb", BLACK)
d.line([ML+20,cy_b+66,W-60,cy_b+66], fill=BORDER, width=1)
cols=[
    ("파일 관련", ["파일 읽기 (Read)", "파일 쓰기 (Write)", "파일 검색 (Glob)"]),
    ("실행 관련", ["터미널 명령어 (Bash)", "코드 실행 (Python/Shell)"]),
    ("검색 관련", ["코드베이스 검색", "웹 검색 (설정 시)"]),
]
col_w=(W-60-ML-20-60)//3
for i,(title,items) in enumerate(cols):
    cx=ML+60+i*col_w
    text(d, cx, cy_b+80, title, 22, "sb", ORANGE)
    for j,item in enumerate(items):
        text(d, cx, cy_b+114+j*34, "· "+item, 22, "r", BODY)

footer(d, 3, 10, "CH01-01", "클로드 코드란 무엇인가")
save(img, "03_agent_loop.png")

# ══════════════════════════════════════════════════════════════
# SLIDE 04 — 설치 (CH01-02)
# ══════════════════════════════════════════════════════════════
img,d = new_slide()
sidebar(d, 4, "", "CH01")

d.rectangle([ML,0,W,120], fill=OD)
text(d, ML+20, 28, "CH01-02  ·  설치 & 첫 번째 세션", 24, "r", WHITE)
text(d, ML+20, 62, "클로드 코드 설치 — 명령어 한 줄", 42, "b", WHITE)

# 사전 준비 체크리스트
cy_s=148
text(d, ML+40, cy_s, "사전 준비", 30, "b", BLACK); cy_s+=46
checks=[
    ("claude.ai 계정", "Pro ($20/월) 또는 Max ($100/월) 구독 필요"),
    ("macOS / Linux", "Windows는 WSL2 환경 사용"),
    ("터미널 앱", "macOS 기본 터미널 또는 iTerm2"),
]
for label,desc in checks:
    d.rounded_rectangle([ML+40,cy_s,ML+40+760,cy_s+58], radius=10, fill=WHITE, outline=BORDER, width=1)
    d.rounded_rectangle([ML+40,cy_s,ML+40+8,cy_s+58], radius=4, fill=ORANGE)
    f_l=F(24,"sb"); f_d=F(20,"r")
    d.text((ML+62,cy_s+8), label, font=f_l, fill=BLACK)
    d.text((ML+62,cy_s+34), desc, font=f_d, fill=DIM)
    cy_s+=68
cy_s+=20

# 설치 명령어
text(d, ML+40, cy_s, "설치 명령어", 30, "b", BLACK); cy_s+=46
cy_s=code_block(d, ML+40, cy_s, 860, [
    "curl -fsSL https://claude.ai/install.sh | bash",
])+20
text(d, ML+40, cy_s, "macOS (Homebrew 사용 시)", 22, "r", DIM); cy_s+=32
cy_s=code_block(d, ML+40, cy_s, 860, [
    "brew install --cask claude-code",
])+20
text(d, ML+40, cy_s, "설치 확인", 22, "r", DIM); cy_s+=32
code_block(d, ML+40, cy_s, 860, ["claude --version"])

# 오른쪽: 설치 후 첫 실행 플로우
rx=ML+940; ry=148; rw=W-rx-60
text(d, rx, ry, "첫 실행 순서", 30, "b", BLACK); ry+=46
flow=[
    ("1", "터미널에서  claude  입력", "클로드 세션 시작"),
    ("2", "브라우저 로그인 창 뜸", "OAuth 방식 — 비밀번호 입력 없음"),
    ("3", "프로젝트 폴더 이동", "cd your-project"),
    ("4", "/init  입력", "CLAUDE.md 자동 생성"),
    ("5", "첫 요청 입력", "\"data.csv 읽어서 요약해줘\""),
]
for num,step,desc in flow:
    d.rounded_rectangle([rx,ry,rx+rw,ry+82], radius=12, fill=WHITE, outline=BORDER, width=1)
    d.rounded_rectangle([rx,ry,rx+52,ry+82], radius=12, fill=ORANGE)
    d.rectangle([rx+40,ry,rx+52,ry+82], fill=ORANGE)
    f_n=F(28,"b"); f_s=F(24,"sb"); f_d=F(20,"r")
    d.text((rx+14,ry+26), num, font=f_n, fill=WHITE)
    d.text((rx+64,ry+12), step, font=f_s, fill=BLACK)
    d.text((rx+64,ry+46), desc, font=f_d, fill=DIM)
    ry+=94

footer(d, 4, 10, "CH01-02", "설치 & 첫 번째 세션")
save(img, "04_install.png")

# ══════════════════════════════════════════════════════════════
# SLIDE 05 — CLAUDE.md 개요 (CH01-03)
# ══════════════════════════════════════════════════════════════
img,d = new_slide()
sidebar(d, 5, "", "CH01")

d.rectangle([ML,0,W,120], fill=(80,60,50))
text(d, ML+20, 28, "CH01-03  ·  CLAUDE.md — 프로젝트 메모리", 24, "r", WHITE)
text(d, ML+20, 62, "클로드에게 내 프로젝트를 영구 기억시키는 파일", 42, "b", WHITE)

# 왼쪽: CLAUDE.md 구조
cy_l=148
text(d, ML+40, cy_l, "CLAUDE.md 에 담을 내용", 30, "b", BLACK); cy_l+=50
sections=[
    ("프로젝트 개요", "이 프로젝트가 무엇인지 — 목적·스택 한 줄 요약"),
    ("폴더 구조",    "데이터, 스크립트, 결과물 위치"),
    ("자주 쓰는 명령어", "실행·테스트·배포 명령어"),
    ("코딩 규칙",    "Python 버전, 라이브러리, 변수명 스타일"),
    ("금지 사항",    "원본 데이터 수정 금지 등 주의사항"),
]
for title,desc in sections:
    d.rounded_rectangle([ML+40,cy_l,ML+40+760,cy_l+80], radius=10, fill=WHITE, outline=BORDER, width=1)
    d.rounded_rectangle([ML+40,cy_l,ML+48,cy_l+80], radius=5, fill=ORANGE)
    f_t=F(24,"sb"); f_d=F(20,"r")
    d.text((ML+66,cy_l+10), title, font=f_t, fill=BLACK)
    d.text((ML+66,cy_l+44), desc, font=f_d, fill=DIM)
    cy_l+=90

# 오른쪽: CLAUDE.md 예시
rx=ML+860; ry=148; rw=W-rx-60
text(d, rx, ry, "CLAUDE.md 예시", 30, "b", BLACK); ry+=46
code_block(d, rx, ry, rw, [
    "# 프로젝트: DataBridge 분석 툴",
    "FastAPI + React + PostgreSQL",
    "",
    "## 자주 쓰는 명령어",
    "pip install -r requirements.txt",
    "python app.py          ← 서버 실행",
    "pytest tests/          ← 테스트",
    "",
    "## 규칙",
    "- Python 3.11 사용",
    "- data/raw/ 폴더 수정 금지",
    "- 결과는 data/output/ 에 저장",
])

# 하단: /init 팁
d.rounded_rectangle([ML+40,H-164,W-60,H-84], radius=10, fill=CODE_BG)
text(d, W//2+40, H-150, "💡  /init 명령어 입력 시 클로드가 프로젝트를 스캔해 CLAUDE.md를 자동 생성합니다.", 24, "sb", OD, "center")

footer(d, 5, 10, "CH01-03", "CLAUDE.md — 프로젝트 메모리")
save(img, "05_claude_md.png")

# ══════════════════════════════════════════════════════════════
# SLIDE 06 — 슬래시 커맨드 (CH01-06)
# ══════════════════════════════════════════════════════════════
img,d = new_slide()
sidebar(d, 6, "", "CH01")

d.rectangle([ML,0,W,120], fill=ORANGE)
text(d, ML+20, 28, "CH01-06  ·  슬래시 커맨드 완전 정리", 24, "r", WHITE)
text(d, ML+20, 62, "자주 쓰는 커맨드 한눈에 보기", 42, "b", WHITE)

commands=[
    ("/init",     "프로젝트 분석 후 CLAUDE.md 자동 생성",        "처음 시작할 때 한 번"),
    ("/compact",  "긴 대화를 요약해 토큰·비용 절약",             "대화가 길어질 때"),
    ("/clear",    "대화 기록 초기화 — 새 작업 시작",             "새 기능 작업 전"),
    ("/config",   "설정 화면 열기 (모델·권한 등)",               "설정 변경 필요 시"),
    ("/doctor",   "설치 상태·버전·인증 상태 확인",               "오류 발생 시 첫 번째로"),
    ("/help",     "사용 가능한 커맨드 전체 목록",                 "모르는 게 있을 때"),
    ("/review",   "현재 변경사항 코드 리뷰 요청",                 "커밋 전 검토"),
    ("/memory",   "메모리 파일 목록 확인 및 편집",               "CLAUDE.md 관리"),
]
CW_c=[(500,1),(380,0.6),(370,0.6)]  # 각 컬럼 너비·비율
col1_x=ML+40; col2_x=ML+40+560; col3_x=ML+40+560+440
cy_cmd=148
text(d, col1_x, cy_cmd, "커맨드", 22,"sb",DIM)
text(d, col2_x, cy_cmd, "기능 설명", 22,"sb",DIM)
text(d, col3_x, cy_cmd, "언제 쓰나", 22,"sb",DIM)
cy_cmd+=36
d.line([ML+40,cy_cmd,W-60,cy_cmd], fill=BORDER, width=1); cy_cmd+=12

for cmd,desc,when in commands:
    bg=WHITE if commands.index((cmd,desc,when))%2==0 else (250,246,240)
    d.rounded_rectangle([ML+40,cy_cmd,W-60,cy_cmd+54], radius=8, fill=bg)
    f_cmd=F(24,"mono"); f_d=F(22,"r"); f_w=F(20,"r")
    d.text((col1_x+8,cy_cmd+14), cmd, font=f_cmd, fill=OD)
    d.text((col2_x,cy_cmd+16), desc, font=f_d, fill=BODY)
    d.text((col3_x,cy_cmd+18), when, font=f_w, fill=DIM)
    cy_cmd+=58

footer(d, 6, 10, "CH01-06", "슬래시 커맨드 완전 정리")
save(img, "06_commands.png")

# ══════════════════════════════════════════════════════════════
# SLIDE 07 — 비용 관리 (CH01-07)
# ══════════════════════════════════════════════════════════════
img,d = new_slide()
sidebar(d, 7, "", "CH01")

d.rectangle([ML,0,W,120], fill=(70,110,160))
text(d, ML+20, 28, "CH01-07  ·  토큰 절약과 비용 관리", 24, "r", WHITE)
text(d, ML+20, 62, "효율적으로 쓰고 비용은 줄이는 방법", 42, "b", WHITE)

# 왼쪽: 비용 절약 전략
cy_l=148
text(d, ML+40, cy_l, "비용 절약 전략 5가지", 30, "b", BLACK); cy_l+=50
tips=[
    ("1", "/compact 자주 사용",      "긴 대화 요약 → 토큰 소비 대폭 감소"),
    ("2", "기능마다 새 세션",          "컨텍스트 누적 방지 → 불필요한 토큰 없앰"),
    ("3", "CLAUDE.md 간결하게",       "200줄 이하 유지 → 매 세션 로드 비용 절감"),
    ("4", "프롬프트 캐싱 활용",        "반복 컨텍스트 90% 할인 자동 적용됨"),
    ("5", "Haiku 모델 병행",           "단순 작업은 저렴한 모델에 위임"),
]
for num,tip,desc in tips:
    d.rounded_rectangle([ML+40,cy_l,ML+40+800,cy_l+80], radius=10, fill=WHITE, outline=BORDER, width=1)
    d.ellipse([ML+50,cy_l+20,ML+86,cy_l+56], fill=ORANGE)
    f_n=F(22,"b"); f_t=F(24,"sb"); f_d=F(20,"r")
    d.text((ML+60,cy_l+26), num, font=f_n, fill=WHITE)
    d.text((ML+100,cy_l+10), tip, font=f_t, fill=BLACK)
    d.text((ML+100,cy_l+46), desc, font=f_d, fill=DIM)
    cy_l+=90

# 오른쪽: 프롬프트 캐싱 설명
rx=ML+900; ry=148; rw=W-rx-60
text(d, rx, ry, "프롬프트 캐싱이란?", 30, "b", BLACK); ry+=50
d.rounded_rectangle([rx,ry,rx+rw,ry+260], radius=12, fill=CODE_BG)
wtext(d, rx+30, ry+24, "같은 컨텍스트(CLAUDE.md, 파일 내용 등)를 반복해서 보낼 때 Anthropic이 자동으로 캐시하여 비용을 대폭 절감해주는 기능입니다.", 22, "r", BODY, rw-60)
d.line([rx,ry+130,rx+rw,ry+130], fill=BORDER, width=1)
stats=[("입력 토큰 비용", "90% 할인"), ("캐시 저장 비용", "25% 추가"), ("자동 적용 여부", "별도 설정 불필요")]
for i,(label,val) in enumerate(stats):
    sy_s=ry+148+i*36
    text(d, rx+24, sy_s, label, 20, "r", DIM)
    text(d, rx+rw-24-tw(d,val,F(22,"b")), sy_s, val, 22, "b", ORANGE)

ry+=280
text(d, rx, ry+10, "구독 요금제 비교", 30, "b", BLACK); ry+=54
plans=[("Pro", "$20/월", "개인 실습용"),("Max", "$100/월", "실무·팀 협업"),("API", "사용량 과금", "프로그래밍 연동")]
pw_p=(rw-20)//3
for i,(plan,price,desc) in enumerate(plans):
    px=rx+i*(pw_p+10)
    is_rec=(i==1)
    bg_p=ORANGE if is_rec else WHITE
    d.rounded_rectangle([px,ry,px+pw_p,ry+130], radius=12, fill=bg_p, outline=ORANGE, width=2)
    f_pl=F(26,"b"); f_pr=F(22,"sb"); f_pd=F(18,"r")
    tc=WHITE if is_rec else BLACK
    dc=WHITE if is_rec else DIM
    text(d, px+pw_p//2, ry+14, plan, 26, "b", tc, "center")
    text(d, px+pw_p//2, ry+52, price, 22, "sb", tc, "center")
    text(d, px+pw_p//2, ry+88, desc, 18, "r", dc, "center")
    if is_rec:
        text(d, px+pw_p//2, ry-28, "추천", 18, "b", ORANGE, "center")

footer(d, 7, 10, "CH01-07", "토큰 절약과 비용 관리")
save(img, "07_cost.png")

print(f"\n✅ CH01 슬라이드 {len(os.listdir(OUT))}장 생성 완료 → {OUT}")
