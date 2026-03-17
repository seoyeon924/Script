#!/usr/bin/env python3
"""
CH01 PPT 슬라이드 — Gray Design System (Korean PPT Minimal)
1920×1080 / Pretendard + Menlo
bg=#FFFFFF, accent=#2B2B2B, sidebar 22%
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1920, 1080
OUT  = "/tmp/Script-repo/output/ch01_gray"
os.makedirs(OUT, exist_ok=True)

# ── Gray 디자인 토큰 ──────────────────────────────────────────
BG       = (255, 255, 255)
BG_CARD  = (245, 245, 245)
BG_CODE  = (238, 238, 238)
SIDEBAR  = (32,  32,  32)    # 사이드바 진한 차콜
ACC      = (32,  32,  32)    # 기본 액센트
ACC2     = (80,  80,  80)    # 서브 액센트
POINT    = (50, 100, 200)    # 포인트 컬러 (인디고)
POINT_LT = (225, 232, 248)   # 포인트 연하게
WHITE    = (255, 255, 255)
BODY     = (50,  50,  50)
DIM      = (130, 130, 130)
BORDER   = (218, 218, 218)
CODE_C   = (30,  30,  30)
SIDEBAR_W = int(W * 0.22)    # 22%

# ── 폰트 ──────────────────────────────────────────────────────
FP = {
    "r":    "/Users/sy/Library/Fonts/Pretendard-Regular.otf",
    "sb":   "/Users/sy/Library/Fonts/Pretendard-SemiBold.otf",
    "b":    "/Users/sy/Library/Fonts/Pretendard-Bold.otf",
    "mono": "/System/Library/Fonts/Menlo.ttc",
}
_fc = {}
def F(sz, wt="r"):
    k=(sz,wt)
    if k not in _fc:
        try: _fc[k]=ImageFont.truetype(FP.get(wt,FP["r"]),sz)
        except: _fc[k]=ImageFont.load_default()
    return _fc[k]

def tw(d,t,f): return d.textbbox((0,0),t,font=f)[2]
def th(d,t,f): b=d.textbbox((0,0),t,font=f); return b[3]-b[1]

def T(d, x, y, s, sz, wt, color, align="left"):
    f=F(sz,wt)
    if align=="center": x=x-tw(d,s,f)//2
    if align=="right":  x=x-tw(d,s,f)
    d.text((x,y), s, font=f, fill=color)
    return th(d,s,f)

def wT(d, x, y, s, sz, wt, color, maxw, lh=1.6):
    f=F(sz,wt); words=s.split(); lines=[]; cur=""
    for w in words:
        test=(cur+" "+w).strip()
        if tw(d,test,f)>maxw and cur: lines.append(cur); cur=w
        else: cur=test
    if cur: lines.append(cur)
    for line in lines:
        d.text((x,y),line,font=f,fill=color); y+=int(th(d,line,f)*lh)
    return y

def code_block(d, x, y, w, lines):
    PAD=22; LH=34
    bh=PAD*2+len(lines)*LH
    d.rounded_rectangle([x,y,x+w,y+bh], radius=6, fill=BG_CODE)
    d.rectangle([x,y,x+4,y+bh], fill=POINT)  # 왼쪽 포인트 바
    f_m=F(20,"mono"); f_k=F(18,"r")
    cy=y+PAD
    for line in lines:
        if "←" in line:
            parts=line.split("←",1)
            main=parts[0].rstrip()
            annot="← "+parts[1].strip()
            d.text((x+PAD,cy),main,font=f_m,fill=CODE_C)
            mw=d.textbbox((0,0),main,font=f_m)[2]
            d.text((x+PAD+mw+8,cy+2),annot,font=f_k,fill=DIM)
        else:
            d.text((x+PAD,cy),line,font=f_m,fill=CODE_C)
        cy+=LH
    return y+bh

def pill(d, x, y, s, bg=POINT, fg=WHITE, sz=16):
    f=F(sz,"sb")
    pw=tw(d,s,f)+20; ph=th(d,s,f)+10
    d.rounded_rectangle([x,y,x+pw,y+ph], radius=4, fill=bg)
    d.text((x+10,y+5),s,font=f,fill=fg)
    return pw, ph

def new_slide():
    img=Image.new("RGB",(W,H),BG)
    d=ImageDraw.Draw(img)
    # 기본 사이드바
    d.rectangle([0,0,SIDEBAR_W,H], fill=SIDEBAR)
    return img,d

def draw_sidebar_label(d, chapter, clip_num, clip_title):
    """사이드바 챕터·클립 정보"""
    # 챕터 배지
    cx=SIDEBAR_W//2
    T(d, cx, 48, chapter, 22, "b", DIM, "center")
    T(d, cx, 78, str(clip_num), 56, "b", WHITE, "center")
    # 구분선
    d.rectangle([24,160,SIDEBAR_W-24,161], fill=(60,60,60))
    # 클립 타이틀 (세로 좁은 공간에 줄바꿈)
    words=clip_title.split()
    lines=[]; cur=""
    f=F(18,"r")
    for w in words:
        test=(cur+" "+w).strip()
        if tw(d,test,f)>SIDEBAR_W-48 and cur: lines.append(cur); cur=w
        else: cur=test
    if cur: lines.append(cur)
    ty=180
    for line in lines:
        d.text((24,ty),line,font=f,fill=(160,160,160)); ty+=28

def footer(d, slide_no, total, clip_id, clip_name):
    FH=52
    d.rectangle([SIDEBAR_W,H-FH,W,H], fill=(245,245,245))
    d.rectangle([SIDEBAR_W,H-FH,W,H-FH+1], fill=BORDER)
    f_sb=F(18,"sb"); f_r=F(18,"r")
    d.text((SIDEBAR_W+32,H-FH+17), clip_id, font=f_sb, fill=POINT)
    d.text((SIDEBAR_W+32+tw(d,clip_id,f_sb)+14,H-FH+17), clip_name, font=f_r, fill=DIM)
    pg=f"{slide_no} / {total}"
    d.text((W-80,H-FH+17), pg, font=f_r, fill=DIM)

def save(img, filename):
    path=f"{OUT}/{filename}"
    img.save(path, optimize=True)
    print(f"✓ {path}")
    return path

ML = SIDEBAR_W + 60   # 메인 콘텐츠 시작 X
MW = W - ML - 60      # 메인 콘텐츠 너비

# ══════════════════════════════════════════════════════════════
# SLIDE 01 — 챕터 타이틀
# ══════════════════════════════════════════════════════════════
img,d=new_slide()
draw_sidebar_label(d,"CH",1,"챕터 개요")

# 오른쪽 메인: 대형 타이틀
T(d, ML, 120, "CHAPTER 01", 20, "sb", POINT)
d.rectangle([ML,158,ML+MW,160], fill=BORDER)
T(d, ML, 178, "클로드 코드", 86, "b", ACC)
T(d, ML, 280, "첫 걸음", 86, "b", ACC2)
T(d, ML, 380, "에이전트 구조 · 설치 · 워크플로우 · 스킬 · 비용 관리", 24, "r", DIM)

# 클립 목록
clips=[
    ("01","클로드 코드란 무엇인가","15분"),
    ("02","설치 & 첫 번째 세션","15분"),
    ("03","CLAUDE.md — 프로젝트 메모리","20분"),
    ("04","기본 워크플로우 — 파일 읽기·쓰기","15분"),
    ("05","작업 모드 — Plan, Auto, Editor","10분"),
    ("06","슬래시 커맨드 완전 정리","15분"),
]
cy=450; cw=(MW-20)//2; ch_h=66
for i,(num,title,dur) in enumerate(clips):
    cx=ML+(i%2)*(cw+20); row=i//2
    cy_c=cy+row*74
    d.rounded_rectangle([cx,cy_c,cx+cw,cy_c+ch_h],radius=6,fill=BG_CARD,outline=BORDER,width=1)
    f_n=F(18,"b"); f_t=F(20,"r"); f_d=F(16,"r")
    d.rounded_rectangle([cx,cy_c,cx+44,cy_c+ch_h],radius=6,fill=ACC)
    d.rectangle([cx+38,cy_c,cx+44,cy_c+ch_h],fill=ACC)
    d.text((cx+10,cy_c+22),num,font=f_n,fill=WHITE)
    d.text((cx+54,cy_c+12),title,font=f_t,fill=BODY)
    d.text((cx+54,cy_c+42),dur,font=f_d,fill=DIM)

footer(d,1,7,"CH01","클로드 코드 첫 걸음")
save(img,"01_title.png")

# ══════════════════════════════════════════════════════════════
# SLIDE 02 — ChatGPT vs Claude Code
# ══════════════════════════════════════════════════════════════
img,d=new_slide()
draw_sidebar_label(d,"CH01",1,"클로드 코드란 무엇인가")

# 헤더
T(d, ML, 48, "두 가지 도구의 차이", 44, "b", ACC)
d.rectangle([ML,102,ML+MW,103], fill=BORDER)

CW2=(MW-40)//2; CH2=580; cy_c=120
lx=ML; rx=ML+CW2+40

# ChatGPT 카드
d.rounded_rectangle([lx,cy_c,lx+CW2,cy_c+CH2],radius=8,fill=BG_CARD,outline=BORDER,width=1)
d.rectangle([lx,cy_c,lx+CW2,cy_c+58],fill=(200,200,200))
d.rectangle([lx,cy_c,lx+CW2,cy_c+3],fill=(150,150,150))
T(d,lx+CW2//2,cy_c+14,"ChatGPT",30,"b",ACC,"center")
T(d,lx+CW2//2,cy_c+48,"대화 인터페이스",18,"r",(100,100,100),"center")
items_l=["텍스트 입력 → 텍스트 응답","파일 시스템 직접 접근 불가","세션 종료 시 기억 초기화","복사·붙여넣기로 코드 전달","결과를 사람이 직접 적용"]
iy=cy_c+80
for item in items_l:
    d.text((lx+30,iy),"–",font=F(24,"r"),fill=(160,160,160))
    d.text((lx+56,iy),item,font=F(24,"r"),fill=ACC2); iy+=54

# Claude Code 카드
d.rounded_rectangle([rx,cy_c,rx+CW2,cy_c+CH2],radius=8,fill=BG_CARD,outline=POINT,width=2)
d.rectangle([rx,cy_c,rx+CW2,cy_c+58],fill=POINT)
d.rectangle([rx,cy_c,rx+CW2,cy_c+3],fill=POINT)
T(d,rx+CW2//2,cy_c+14,"Claude Code",30,"b",WHITE,"center")
T(d,rx+CW2//2,cy_c+48,"에이전트 (Agent)",18,"sb",(200,215,255),"center")
items_r=["터미널에서 실행 — 파일 직접 접근","파일 읽기 · 쓰기 · 코드 실행","CLAUDE.md로 프로젝트 맥락 유지","코드 수정부터 실행까지 자동화","결과를 스스로 검증하고 완료 보고"]
iy=cy_c+80
for item in items_r:
    d.text((rx+30,iy),"→",font=F(24,"sb"),fill=POINT)
    d.text((rx+56,iy),item,font=F(24,"r"),fill=BODY); iy+=54

# 핵심 배너
d.rounded_rectangle([ML,cy_c+CH2+20,ML+MW,cy_c+CH2+84],radius=6,fill=POINT_LT)
T(d,ML+MW//2+ML,cy_c+CH2+44,"핵심 차이 —  ChatGPT는 '조언',  Claude Code는 '직접 실행'",26,"sb",POINT,"center")

footer(d,2,7,"CH01-01","클로드 코드란 무엇인가")
save(img,"02_comparison.png")

# ══════════════════════════════════════════════════════════════
# SLIDE 03 — 에이전트 루프
# ══════════════════════════════════════════════════════════════
img,d=new_slide()
draw_sidebar_label(d,"CH01",1,"클로드 코드란 무엇인가")

T(d,ML,48,"에이전트 구조 — 에이전트 루프",44,"b",ACC)
d.rectangle([ML,102,ML+MW,103],fill=BORDER)

steps=[
    ("사용자\n지시","요청을 전달받습니다"),
    ("계획","순서와 방법 결정"),
    ("도구\n선택","파일? 코드? 검색?"),
    ("실행","실제 작업 수행"),
    ("결과\n확인","성공 여부 검증"),
    ("완료","보고 또는 반복"),
]
n=len(steps); SW_s=190; SH_s=200; GAP_s=30
total_w=n*SW_s+(n-1)*GAP_s; sx=ML+(MW-total_w)//2; sy=136

for i,(title,desc) in enumerate(steps):
    x=sx+i*(SW_s+GAP_s)
    is_first=(i==0)
    bg_c=POINT if is_first else BG_CARD
    bd_c=POINT
    d.rounded_rectangle([x,sy,x+SW_s,sy+SH_s],radius=10,fill=bg_c,outline=bd_c,width=2)
    # 번호 원
    cx2=x+SW_s//2
    d.ellipse([cx2-16,sy+16,cx2+16,sy+48],fill=bd_c if not is_first else WHITE)
    nd=str(i+1); f_n=F(20,"b")
    d.text((cx2-tw(d,nd,f_n)//2,sy+22),nd,font=f_n,fill=WHITE if not is_first else POINT)
    # 타이틀
    tc=WHITE if is_first else ACC
    dc=(200,215,255) if is_first else DIM
    lines=title.split("\n"); ty=sy+70
    for ln in lines:
        f_t=F(26,"b"); d.text((cx2-tw(d,ln,f_t)//2,ty),ln,font=f_t,fill=tc); ty+=32
    # 설명
    f_d=F(18,"r"); d.text((cx2-tw(d,desc,f_d)//2,sy+168),desc,font=f_d,fill=dc)
    # 화살표
    if i<n-1:
        ax=x+SW_s+4; ay=sy+SH_s//2
        d.polygon([(ax,ay-8),(ax+GAP_s-4,ay),(ax,ay+8)],fill=POINT)

T(d,ML+MW//2+ML,sy+SH_s+18,"↑  이 과정이 반복되는 것을 에이전트 루프(Agent Loop)라고 합니다",22,"r",DIM,"center")

# 도구 요약
cy_b=sy+SH_s+60
d.rounded_rectangle([ML,cy_b,ML+MW,cy_b+210],radius=8,fill=BG_CARD,outline=BORDER,width=1)
T(d,ML+28,cy_b+22,"클로드 코드가 루프에서 사용하는 도구",24,"sb",ACC)
d.rectangle([ML,cy_b+60,ML+MW,cy_b+61],fill=BORDER)
cols=[
    ("파일 관련",["파일 읽기 (Read)","파일 쓰기 (Write)","파일 검색 (Glob)"]),
    ("실행 관련",["터미널 명령어 (Bash)","코드 실행 (Python/Shell)"]),
    ("검색 관련",["코드베이스 검색","웹 검색 (설정 시)"]),
]
cw3=MW//3
for i,(title,items) in enumerate(cols):
    cx3=ML+28+i*cw3
    T(d,cx3,cy_b+76,title,20,"sb",POINT)
    for j,item in enumerate(items):
        T(d,cx3,cy_b+106+j*32,"· "+item,20,"r",BODY)
    if i<2: d.rectangle([ML+i*cw3+cw3,cy_b+62,ML+i*cw3+cw3+1,cy_b+210],fill=BORDER)

footer(d,3,7,"CH01-01","클로드 코드란 무엇인가")
save(img,"03_agent_loop.png")

# ══════════════════════════════════════════════════════════════
# SLIDE 04 — 설치
# ══════════════════════════════════════════════════════════════
img,d=new_slide()
draw_sidebar_label(d,"CH01",2,"설치 & 첫 번째 세션")

T(d,ML,48,"설치 — 명령어 한 줄로 완료",44,"b",ACC)
d.rectangle([ML,102,ML+MW,103],fill=BORDER)

# 왼쪽: 설치
lw=int(MW*0.52); rx2=ML+lw+40; rw2=MW-lw-40

T(d,ML,120,"사전 준비",26,"sb",ACC); cy_l=156
for label,desc in [
    ("claude.ai 계정","Pro ($20/월) 또는 Max ($100/월)"),
    ("macOS / Linux","Windows는 WSL2 환경"),
    ("터미널 앱","기본 터미널 또는 iTerm2"),
]:
    d.rounded_rectangle([ML,cy_l,ML+lw,cy_l+62],radius=6,fill=BG_CARD,outline=BORDER,width=1)
    d.rectangle([ML,cy_l,ML+4,cy_l+62],fill=POINT)
    T(d,ML+20,cy_l+8,label,22,"sb",ACC)
    T(d,ML+20,cy_l+38,desc,18,"r",DIM)
    cy_l+=70
cy_l+=16

T(d,ML,cy_l,"설치 명령어",26,"sb",ACC); cy_l+=40
cy_l=code_block(d,ML,cy_l,lw,["curl -fsSL https://claude.ai/install.sh | bash"])+16
T(d,ML,cy_l,"Homebrew 사용 시",18,"r",DIM); cy_l+=28
cy_l=code_block(d,ML,cy_l,lw,["brew install --cask claude-code"])+16
T(d,ML,cy_l,"버전 확인",18,"r",DIM); cy_l+=28
code_block(d,ML,cy_l,lw,["claude --version"])

# 오른쪽: 첫 실행 순서
T(d,rx2,120,"첫 실행 순서",26,"sb",ACC)
ry=156
for num,step,desc in [
    ("1","claude  입력","터미널에서 클로드 세션 시작"),
    ("2","브라우저 로그인","OAuth 방식 — 비밀번호 없음"),
    ("3","프로젝트 폴더 이동","cd your-project"),
    ("4","/init  입력","CLAUDE.md 자동 생성"),
    ("5","첫 요청 입력",'"data.csv 읽어서 요약해줘"'),
]:
    d.rounded_rectangle([rx2,ry,rx2+rw2,ry+74],radius=8,fill=BG_CARD,outline=BORDER,width=1)
    d.ellipse([rx2+12,ry+18,rx2+48,ry+54],fill=POINT)
    f_n=F(22,"b"); T(d,rx2+20,ry+24,num,22,"b",WHITE)
    T(d,rx2+60,ry+10,step,22,"sb",ACC)
    T(d,rx2+60,ry+42,desc,18,"r",DIM)
    ry+=82

footer(d,4,7,"CH01-02","설치 & 첫 번째 세션")
save(img,"04_install.png")

# ══════════════════════════════════════════════════════════════
# SLIDE 05 — CLAUDE.md
# ══════════════════════════════════════════════════════════════
img,d=new_slide()
draw_sidebar_label(d,"CH01",3,"CLAUDE.md")

T(d,ML,48,"CLAUDE.md — 프로젝트를 영구 기억시키는 파일",44,"b",ACC)
d.rectangle([ML,102,ML+MW,103],fill=BORDER)

lw2=int(MW*0.48); rx3=ML+lw2+40; rw3=MW-lw2-40

T(d,ML,120,"담을 내용 5가지",24,"sb",ACC); cy_l=156
for title,desc in [
    ("프로젝트 개요","목적·기술 스택 한 줄 요약"),
    ("폴더 구조","데이터·스크립트·결과물 위치"),
    ("자주 쓰는 명령어","실행·테스트·배포 명령어"),
    ("코딩 규칙","Python 버전·라이브러리·변수명 스타일"),
    ("금지 사항","원본 데이터 수정 금지 등 주의사항"),
]:
    d.rounded_rectangle([ML,cy_l,ML+lw2,cy_l+72],radius=6,fill=BG_CARD,outline=BORDER,width=1)
    d.rectangle([ML,cy_l,ML+4,cy_l+72],fill=POINT)
    T(d,ML+20,cy_l+10,title,22,"sb",ACC)
    T(d,ML+20,cy_l+44,desc,18,"r",DIM)
    cy_l+=80

T(d,rx3,120,"CLAUDE.md 예시",24,"sb",ACC)
code_block(d,rx3,156,rw3,[
    "# 프로젝트: DataBridge 분석 툴",
    "FastAPI + React + PostgreSQL",
    "",
    "## 자주 쓰는 명령어",
    "pip install -r requirements.txt",
    "python app.py   ← 서버 실행",
    "pytest tests/   ← 테스트 실행",
    "",
    "## 규칙",
    "- Python 3.11 사용",
    "- data/raw/ 폴더 수정 금지",
    "- 결과는 data/output/ 에 저장",
])

# 팁 배너
d.rounded_rectangle([ML,H-130,ML+MW,H-66],radius=6,fill=POINT_LT)
T(d,ML+MW//2+ML,H-112,"💡  /init 입력 시 클로드가 프로젝트를 스캔해 CLAUDE.md를 자동 생성합니다.",22,"sb",POINT,"center")

footer(d,5,7,"CH01-03","CLAUDE.md — 프로젝트 메모리")
save(img,"05_claude_md.png")

# ══════════════════════════════════════════════════════════════
# SLIDE 06 — 슬래시 커맨드
# ══════════════════════════════════════════════════════════════
img,d=new_slide()
draw_sidebar_label(d,"CH01",6,"슬래시 커맨드")

T(d,ML,48,"슬래시 커맨드 — 자주 쓰는 것 모음",44,"b",ACC)
d.rectangle([ML,102,ML+MW,103],fill=BORDER)

cmds=[
    ("/init",    "프로젝트 분석 후 CLAUDE.md 자동 생성",   "처음 시작 시 한 번"),
    ("/compact", "대화 요약 — 토큰·비용 절약",            "대화가 길어질 때"),
    ("/clear",   "대화 초기화 — 새 작업 시작",            "새 기능 작업 전"),
    ("/config",  "설정 화면 열기 (모델·권한 등)",          "설정 변경 필요 시"),
    ("/doctor",  "설치 상태·버전·인증 확인",               "오류 발생 시 첫 점검"),
    ("/help",    "커맨드 전체 목록 표시",                  "모르는 게 있을 때"),
    ("/review",  "현재 변경사항 코드 리뷰",                "커밋 전 검토"),
    ("/memory",  "메모리 파일 목록 확인 및 편집",          "CLAUDE.md 관리"),
]
col1=ML; col2=ML+360; col3=ML+360+520
T(d,col1,120,"커맨드",20,"sb",DIM); T(d,col2,120,"기능",20,"sb",DIM); T(d,col3,120,"언제",20,"sb",DIM)
d.rectangle([ML,146,ML+MW,147],fill=BORDER)
cy_cmd=156
for i,(cmd,desc,when) in enumerate(cmds):
    bg=BG if i%2==0 else BG_CARD
    d.rectangle([ML,cy_cmd,ML+MW,cy_cmd+52],fill=bg)
    d.text((col1+4,cy_cmd+14),cmd,font=F(22,"mono"),fill=POINT)
    T(d,col2,cy_cmd+16,desc,21,"r",BODY)
    T(d,col3,cy_cmd+18,when,19,"r",DIM)
    cy_cmd+=54
d.rectangle([ML,cy_cmd,ML+MW,cy_cmd+1],fill=BORDER)

footer(d,6,7,"CH01-06","슬래시 커맨드 완전 정리")
save(img,"06_commands.png")

# ══════════════════════════════════════════════════════════════
# SLIDE 07 — 비용 관리
# ══════════════════════════════════════════════════════════════
img,d=new_slide()
draw_sidebar_label(d,"CH01",7,"토큰·비용 관리")

T(d,ML,48,"토큰 절약 — 비용을 줄이는 5가지 방법",44,"b",ACC)
d.rectangle([ML,102,ML+MW,103],fill=BORDER)

lw4=int(MW*0.52); rx4=ML+lw4+40; rw4=MW-lw4-40

tips=[
    ("/compact 자주 사용",    "긴 대화 요약 → 토큰 소비 대폭 감소"),
    ("기능마다 새 세션 시작",  "컨텍스트 누적 방지 → 불필요한 토큰 없앰"),
    ("CLAUDE.md 간결하게",    "200줄 이하 유지 → 매 세션 로드 비용 절감"),
    ("프롬프트 캐싱 활용",    "반복 컨텍스트 90% 할인 자동 적용"),
    ("Haiku 모델 병행",       "단순 작업은 저렴한 모델에 위임"),
]
T(d,ML,120,"비용 절약 전략",24,"sb",ACC); cy_t=156
for i,(tip,desc) in enumerate(tips):
    d.rounded_rectangle([ML,cy_t,ML+lw4,cy_t+76],radius=6,fill=BG_CARD,outline=BORDER,width=1)
    d.ellipse([ML+12,cy_t+18,ML+46,cy_t+52],fill=POINT)
    T(d,ML+21,cy_t+24,str(i+1),22,"b",WHITE)
    T(d,ML+60,cy_t+10,tip,22,"sb",ACC)
    T(d,ML+60,cy_t+44,desc,18,"r",DIM)
    cy_t+=84

# 오른쪽: 캐싱 + 요금제
T(d,rx4,120,"프롬프트 캐싱",24,"sb",ACC)
d.rounded_rectangle([rx4,156,rx4+rw4,156+160],radius=8,fill=BG_CARD,outline=BORDER,width=1)
d.rectangle([rx4,156,rx4+4,316],fill=POINT)
T(d,rx4+20,168,"같은 컨텍스트 반복 시 Anthropic이 자동 캐시 — 별도 설정 불필요",20,"r",BODY)
for i,(k,v) in enumerate([("입력 토큰 비용","90% 할인"),("자동 적용 여부","설정 없이 자동")]):
    T(d,rx4+20,220+i*38,k,19,"r",DIM); T(d,rx4+rw4-16,220+i*38,v,19,"sb",POINT,"right")

T(d,rx4,336,"구독 요금제",24,"sb",ACC)
pw4=(rw4-20)//3
for i,(plan,price,desc) in enumerate([("Pro","$20/월","개인 실습"),("Max","$100/월","실무·팀"),("API","사용량 과금","프로그래밍")]):
    px=rx4+i*(pw4+10)
    is_rec=(i==1)
    d.rounded_rectangle([px,368,px+pw4,368+130],radius=8,fill=POINT if is_rec else BG_CARD, outline=POINT,width=2)
    tc=WHITE if is_rec else ACC; dc=(200,215,255) if is_rec else DIM
    T(d,px+pw4//2,380,plan,22,"b",tc,"center")
    T(d,px+pw4//2,414,price,20,"sb",tc,"center")
    T(d,px+pw4//2,448,desc,16,"r",dc,"center")

footer(d,7,7,"CH01-07","토큰 절약·비용 관리")
save(img,"07_cost.png")

print(f"\n✅ Gray 슬라이드 {len([f for f in os.listdir(OUT) if f.endswith('.png')])}장 → {OUT}")
