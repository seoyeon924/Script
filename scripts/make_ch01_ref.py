#!/usr/bin/env python3
"""
CH01 슬라이드 — 레퍼런스 디자인 적용
- 순백 배경, 좌측 텍스트 컬럼(~28%), 우측 콘텐츠
- 무채색 전용 (포인트 컬러 없음)
- 극적인 여백, 그림자 없음, 얇은 선만
- 텍스트 오버랩 절대 금지
"""
from PIL import Image, ImageDraw, ImageFont
import os, textwrap

W, H = 1920, 1080
OUT  = "/tmp/Script-repo/output/ch01_ref"
os.makedirs(OUT, exist_ok=True)

# ── 색상 (무채색 전용) ─────────────────────────────────────
WHITE   = (255, 255, 255)
BG      = (255, 255, 255)
C900    = ( 24,  24,  24)   # 제목
C700    = ( 60,  60,  60)   # 본문
C500    = (110, 110, 110)   # 서브
C300    = (170, 170, 170)   # 보조/주석
C100    = (230, 230, 230)   # 구분선
C050    = (245, 245, 245)   # 카드 배경
BADGE   = ( 40,  40,  40)   # 라벨 배지 배경

# ── 폰트 ──────────────────────────────────────────────────
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

def tw(d,t,f): return max(1, d.textbbox((0,0),t,font=f)[2])
def th(d,t,f): b=d.textbbox((0,0),t,font=f); return max(1,b[3]-b[1])

def T(d, x, y, s, sz, wt, color, align="left"):
    if not s: return 0
    f=F(sz,wt)
    if align=="center": x=x-tw(d,s,f)//2
    if align=="right":  x=x-tw(d,s,f)
    d.text((int(x),int(y)), s, font=f, fill=color)
    return th(d,s,f)

def wT(d, x, y, s, sz, wt, color, maxw, lh=1.55):
    """자동 줄바꿈 — 겹침 방지를 위해 항상 y 반환"""
    f=F(sz,wt); words=s.split(); lines=[]; cur=""
    for w in words:
        test=(cur+" "+w).strip()
        if tw(d,test,f)>maxw and cur: lines.append(cur); cur=w
        else: cur=test
    if cur: lines.append(cur)
    for line in lines:
        d.text((int(x),int(y)), line, font=f, fill=color)
        y+=int(th(d,line,f)*lh)
    return y

def hline(d, x, y, w, color=C100, h=1):
    d.rectangle([int(x),int(y),int(x+w),int(y+h)], fill=color)

def code_block(d, x, y, w, lines):
    PAD=20; LH=32
    bh=PAD*2+len(lines)*LH
    d.rectangle([x,y,x+w,y+bh], fill=C050)
    hline(d,x,y,2,C500,bh)  # 왼쪽 얇은 선
    f_m=F(19,"mono"); f_k=F(17,"r")
    cy=y+PAD
    for line in lines:
        if "←" in line:
            parts=line.split("←",1)
            main=parts[0].rstrip()
            annot="← "+parts[1].strip()
            d.text((x+PAD,cy),main,font=f_m,fill=C700)
            mw=tw(d,main,f_m)
            d.text((x+PAD+mw+10,cy+2),annot,font=f_k,fill=C300)
        else:
            d.text((x+PAD,cy),line,font=f_m,fill=C700)
        cy+=LH
    return y+bh

# ── 레이아웃 상수 ──────────────────────────────────────────
LEFT_W  = 480       # 좌측 텍스트 컬럼 너비 (~25%)
LEFT_X  = 72        # 좌측 시작
GAP     = 80        # 좌우 갭
RIGHT_X = LEFT_X + LEFT_W + GAP
RIGHT_W = W - RIGHT_X - 72

def new_slide():
    img=Image.new("RGB",(W,H),BG)
    d=ImageDraw.Draw(img)
    return img,d

def left_col(d, category, title, desc="", title_sz=42):
    """좌/우 분할용 좌측 컬럼: 소라벨 → 대형 볼드 제목 → 회색 설명"""
    y=72
    f_cat=F(13,"sb")
    cw=tw(d,category,f_cat)+16; ch_=th(d,category,f_cat)+8
    d.rectangle([LEFT_X,y,LEFT_X+cw,y+ch_],fill=BADGE)
    d.text((LEFT_X+8,y+4),category,font=f_cat,fill=WHITE)
    y+=ch_+16
    f_t=F(title_sz,"b")
    words=title.split(); lines=[]; cur=""
    for w in words:
        test=(cur+" "+w).strip()
        if tw(d,test,f_t)>LEFT_W and cur: lines.append(cur); cur=w
        else: cur=test
    if cur: lines.append(cur)
    for line in lines:
        d.text((LEFT_X,y),line,font=f_t,fill=C900); y+=int(th(d,line,f_t)*1.2)
    y+=20
    if desc:
        y=wT(d,LEFT_X,y,desc,16,"r",C500,LEFT_W,lh=1.7)
    return y

# 전체 폭 레이아웃 마진
FULL_X  = 72          # 전체 폭 시작
FULL_W  = W - FULL_X*2

def top_header(d, category, title, desc="", title_sz=38):
    """전체 폭 레이아웃용 상단 헤더: 좌상단 소라벨 + 볼드 제목 + 설명 → 콘텐츠 Y 반환"""
    y=56
    f_cat=F(13,"sb")
    cw=tw(d,category,f_cat)+16; ch_=th(d,category,f_cat)+8
    d.rectangle([FULL_X,y,FULL_X+cw,y+ch_],fill=BADGE)
    d.text((FULL_X+8,y+4),category,font=f_cat,fill=WHITE)
    y+=ch_+10
    f_t=F(title_sz,"b")
    d.text((FULL_X,y),title,font=f_t,fill=C900)
    y+=th(d,title,f_t)+10
    if desc:
        y=wT(d,FULL_X,y,desc,15,"r",C500,FULL_W*0.55,lh=1.5)
    y+=24
    hline(d,FULL_X,y,FULL_W,C100)
    return y+20   # 콘텐츠 시작 Y

def page_num(d, n, total):
    f=F(16,"r")
    s=f"{n} / {total}"
    d.text((W-72-tw(d,s,f), H-44),s,font=f,fill=C300)

def save(img, filename):
    path=f"{OUT}/{filename}"
    img.save(path)
    print(f"✓ {path}")

# ══════════════════════════════════════════════════════════════
# SLIDE 01 — 챕터 타이틀 (전체 폭 레이아웃)
# ══════════════════════════════════════════════════════════════
img,d=new_slide()

# 상단: 대형 제목 블록
y=56
f_cat=F(13,"sb")
cw_=tw(d,"CHAPTER 01",f_cat)+16; ch__=th(d,"CHAPTER 01",f_cat)+8
d.rectangle([FULL_X,y,FULL_X+cw_,y+ch__],fill=BADGE)
d.text((FULL_X+8,y+4),"CHAPTER 01",font=f_cat,fill=WHITE)
y+=ch__+12
f_big=F(72,"b")
d.text((FULL_X,y),"클로드 코드 첫 걸음",font=f_big,fill=C900)
y+=th(d,"클로드 코드 첫 걸음",f_big)+12
wT(d,FULL_X,y,"에이전트 구조 · 설치 · 워크플로우 · 스킬 · 비용 관리까지 실무에서 바로 쓰는 흐름을 배웁니다.",18,"r",C500,FULL_W*0.7)
y+=52
hline(d,FULL_X,y,FULL_W,C100); y+=28

# 클립 목록 — 2열 그리드 전체 폭
clips=[
    ("01","클로드 코드란 무엇인가","에이전트 구조 · 15분"),
    ("02","설치 & 첫 번째 세션","macOS/Linux · 15분"),
    ("03","CLAUDE.md — 프로젝트 메모리","영구 컨텍스트 설정 · 20분"),
    ("04","기본 워크플로우","파일 읽기·쓰기·실행 · 15분"),
    ("05","작업 모드","Plan · Auto · Editor · 10분"),
    ("06","슬래시 커맨드 완전 정리","핵심 커맨드 8개 · 15분"),
    ("07","토큰 절약과 비용 관리","프롬프트 캐싱 · 요금제 · 20분"),
]
COL2=(FULL_W-40)//2; ROW_H2=76
for i,(num,title,sub) in enumerate(clips):
    col=i%2; row=i//2
    cx=FULL_X+col*(COL2+40); cy=y+row*ROW_H2
    T(d,cx,cy+20,num,13,"sb",C300)
    d.text((cx+48,cy+10),title,font=F(22,"sb"),fill=C900)
    d.text((cx+48,cy+38),sub,font=F(15,"r"),fill=C500)
    hline(d,cx+48,cy+ROW_H2-4,COL2-48,C100)

page_num(d,1,7)
save(img,"01_title.png")

# ══════════════════════════════════════════════════════════════
# SLIDE 02 — ChatGPT vs Claude Code
# ══════════════════════════════════════════════════════════════
img,d=new_slide()
left_col(d,"CH01-01","두 가지\n도구의 차이","ChatGPT와 Claude Code는 같은 AI처럼 보이지만 구조가 완전히 다릅니다.")

# 우측: 2열 비교표 (레퍼런스 1 스타일)
hline(d,RIGHT_X,72,RIGHT_W,C900,2)

# 헤더 행
HALF=(RIGHT_W-40)//2; rx2=RIGHT_X+HALF+40
f_h=F(22,"b")
T(d,RIGHT_X+HALF//2,80,"ChatGPT",22,"b",C500,"center")
T(d,rx2+HALF//2,80,"Claude Code",22,"b",C900,"center")
hline(d,RIGHT_X,114,RIGHT_W,C100)

rows=[
    ("실행 방식","웹 브라우저 대화창","터미널 (명령줄 인터페이스)"),
    ("파일 접근","직접 접근 불가 — 복붙 필요","파일 시스템 직접 읽기·쓰기"),
    ("코드 실행","결과를 텍스트로만 반환","코드를 직접 실행하고 결과 확인"),
    ("프로젝트 기억","세션 종료 시 초기화","CLAUDE.md로 영구 기억 유지"),
    ("작업 자동화","사람이 결과를 직접 적용","계획→실행→검증 루프 자동 처리"),
]
ry=128; ROW_H=80
for label,left,right in rows:
    f_l=F(14,"sb"); f_v=F(19,"r")
    # 라벨
    d.text((RIGHT_X,ry+28),label,font=f_l,fill=C300)
    # ChatGPT 열
    d.text((RIGHT_X+HALF//2-tw(d,left,f_v)//2,ry+24),left,font=f_v,fill=C500)
    # Claude Code 열 (볼드)
    f_vb=F(19,"sb")
    d.text((rx2+HALF//2-tw(d,right,f_vb)//2,ry+24),right,font=f_vb,fill=C900)
    ry+=ROW_H
    hline(d,RIGHT_X,ry,RIGHT_W,C100)

# 핵심 요약
ry+=24
wT(d,RIGHT_X,ry,"→  ChatGPT는 '조언'을 주는 도구이고, Claude Code는 '직접 작업'을 수행하는 에이전트입니다.",20,"r",C700,RIGHT_W)

page_num(d,2,7)
save(img,"02_comparison.png")

# ══════════════════════════════════════════════════════════════
# SLIDE 03 — 에이전트 루프 (전체 폭 · 저니맵 스타일)
# ══════════════════════════════════════════════════════════════
img,d=new_slide()
cy_s=top_header(d,"CH01-01","에이전트 루프","목표를 받아 계획하고, 도구를 선택해 실행한 뒤 결과를 검증하는 과정이 반복됩니다.",title_sz=36)

# ── 저니맵 스타일 라벨 행 ──────────────────────────
T(d,FULL_X,cy_s,"Action",14,"sb",C300)
hline(d,FULL_X+72,cy_s+8,FULL_W-72,C100)
cy_s+=34

# 수평 플로우 (전체 폭)
steps=[
    ("사용자 지시","요청 전달"),
    ("계획","순서·방법 결정"),
    ("도구 선택","파일? 코드? 검색?"),
    ("실행","실제 작업 수행"),
    ("결과 확인","성공 여부 검증"),
    ("완료","보고 또는 반복"),
]
n=len(steps); STEP_W=FULL_W//n; ARR_Y=cy_s+72
for i,(title,desc) in enumerate(steps):
    sx=FULL_X+i*STEP_W; cx=sx+STEP_W//2
    is_first=(i==0); r=22
    fill=C900 if is_first else C050
    d.ellipse([cx-r,ARR_Y-r,cx+r,ARR_Y+r],fill=fill,outline=C900,width=2)
    nd=str(i+1); fn=F(18,"b")
    d.text((cx-tw(d,nd,fn)//2,ARR_Y-th(d,nd,fn)//2),nd,font=fn,fill=WHITE if is_first else C700)
    if i<n-1:
        ax_s=cx+r+4; ax_e=FULL_X+(i+1)*STEP_W+((i+1)*STEP_W//2)-r-4
        ay=ARR_Y
        d.line([(ax_s,ay),(ax_e,ay)],fill=C300,width=1)
        d.polygon([(ax_e,ay-5),(ax_e+8,ay),(ax_e,ay+5)],fill=C300)
    T(d,cx,ARR_Y+r+14,title,18,"sb",C900,"center")
    T(d,cx,ARR_Y+r+40,desc,14,"r",C500,"center")

loop_y=ARR_Y+100
hline(d,FULL_X,loop_y,FULL_W,C100)
T(d,FULL_X+FULL_W//2,loop_y+14,"↑  이 과정이 반복되는 것을 에이전트 루프(Agent Loop)라고 합니다",16,"r",C500,"center")

# ── 도구 요약 3열 (전체 폭) ──────────────────────
tool_y=loop_y+56
hline(d,FULL_X,tool_y,FULL_W,C100)
T(d,FULL_X,tool_y+14,"클로드 코드가 루프에서 사용하는 도구",13,"sb",C300)
CW3=FULL_W//3; ty_base=tool_y+50
for i,(cat,items) in enumerate([
    ("파일 관련",["파일 읽기 (Read)","파일 쓰기 (Write)","파일 검색 (Glob)"]),
    ("실행 관련",["터미널 명령어 (Bash)","코드 실행 (Python/Shell)"]),
    ("검색 관련",["코드베이스 검색","웹 검색 (설정 시)"]),
]):
    cx3=FULL_X+i*CW3; ty3=ty_base
    T(d,cx3,ty3,cat,16,"sb",C700); ty3+=26
    for item in items:
        T(d,cx3,ty3,"·  "+item,15,"r",C500); ty3+=26
    if i<2: hline(d,FULL_X+i*CW3+CW3,tool_y+48,1,C100,H-tool_y-60)

page_num(d,3,7)
save(img,"03_agent_loop.png")

# ══════════════════════════════════════════════════════════════
# SLIDE 04 — 설치 (레퍼런스 3 번호 리스트 스타일)
# ══════════════════════════════════════════════════════════════
img,d=new_slide()
left_col(d,"CH01-02","설치\n& 첫 번째 세션","명령어 한 줄로 5분 안에 완료됩니다. Node.js 별도 설치 불필요.")

hline(d,RIGHT_X,72,RIGHT_W,C900,2)

# 왼쪽: 설치 단계 번호 리스트 (레퍼런스 3)
LW2=int(RIGHT_W*0.5); RX2=RIGHT_X+LW2+48; RW2=RIGHT_W-LW2-48

T(d,RIGHT_X,84,"사전 준비",14,"sb",C300)
hline(d,RIGHT_X,104,LW2,C100)
reqs=[("계정","claude.ai Pro ($20/월) 또는 Max ($100/월)"),("OS","macOS / Linux (Windows: WSL2)"),("터미널","기본 Terminal 또는 iTerm2")]
ry=114
for label,val in reqs:
    f_l=F(14,"sb"); f_v=F(18,"r")
    T(d,RIGHT_X,ry,label,14,"sb",C300)
    T(d,RIGHT_X+80,ry,val,18,"r",C700)
    ry+=34
    hline(d,RIGHT_X,ry,LW2,C100)
ry+=20

T(d,RIGHT_X,ry,"설치 명령어",14,"sb",C300); ry+=24
ry=code_block(d,RIGHT_X,ry,LW2,["curl -fsSL https://claude.ai/install.sh | bash"])+14
T(d,RIGHT_X,ry,"Homebrew 사용 시",14,"r",C300); ry+=22
ry=code_block(d,RIGHT_X,ry,LW2,["brew install --cask claude-code"])+14
T(d,RIGHT_X,ry,"버전 확인",14,"r",C300); ry+=22
code_block(d,RIGHT_X,ry,LW2,["claude --version"])

# 오른쪽: 첫 실행 순서 (레퍼런스 3 플로우 카드)
hline(d,RX2-24,80,1,C100,H-152)  # 수직 구분선
T(d,RX2,84,"첫 실행 순서",14,"sb",C300)
hline(d,RX2,104,RW2,C100)
steps4=[
    ("01","claude  입력","터미널 클로드 세션 시작"),
    ("02","브라우저 로그인","OAuth 방식 — 별도 비밀번호 없음"),
    ("03","cd your-project","프로젝트 폴더로 이동"),
    ("04","/init  입력","CLAUDE.md 자동 생성"),
    ("05","첫 요청 입력","\"data.csv 읽어서 요약해줘\""),
]
ry4=114
for num,step,desc in steps4:
    f_n=F(13,"sb"); f_s=F(20,"sb"); f_d=F(15,"r")
    T(d,RX2,ry4,num,13,"sb",C300)
    d.text((RX2+42,ry4-2),step,font=f_s,fill=C900)
    d.text((RX2+42,ry4+26),desc,font=f_d,fill=C500)
    ry4+=64
    hline(d,RX2+42,ry4-8,RW2-42,C100)

page_num(d,4,7)
save(img,"04_install.png")

# ══════════════════════════════════════════════════════════════
# SLIDE 05 — CLAUDE.md
# ══════════════════════════════════════════════════════════════
img,d=new_slide()
left_col(d,"CH01-03","CLAUDE.md","세션이 끝나도 프로젝트 맥락을 유지하는 영구 메모리 파일. /init으로 자동 생성됩니다.")

hline(d,RIGHT_X,72,RIGHT_W,C900,2)

# 상단: 5가지 항목 (번호 리스트)
T(d,RIGHT_X,84,"CLAUDE.md에 담을 내용",14,"sb",C300)
hline(d,RIGHT_X,104,RIGHT_W,C100)
sections=[
    ("01","프로젝트 개요","이 프로젝트가 무엇인지 — 목적, 기술 스택"),
    ("02","폴더 구조","데이터, 스크립트, 결과물 위치"),
    ("03","자주 쓰는 명령어","실행, 테스트, 배포 명령어"),
    ("04","코딩 규칙","Python 버전, 라이브러리, 변수명 스타일"),
    ("05","금지 사항","원본 데이터 수정 금지 등 주의사항"),
]
ry=114; SEC_H=74
for num,title,desc in sections:
    T(d,RIGHT_X,ry+20,num,13,"sb",C300)
    T(d,RIGHT_X+52,ry+8,title,20,"sb",C900)
    T(d,RIGHT_X+52,ry+38,desc,15,"r",C500)
    ry+=SEC_H
    hline(d,RIGHT_X+52,ry,RIGHT_W-52,C100)
ry+=20

# CLAUDE.md 예시 코드 블록
T(d,RIGHT_X,ry,"CLAUDE.md 작성 예시",14,"sb",C300); ry+=24
code_block(d,RIGHT_X,ry,RIGHT_W,[
    "# 프로젝트: DataBridge 분석 툴",
    "FastAPI + React + PostgreSQL",
    "",
    "## Commands",
    "python app.py      ← 서버 실행",
    "pytest tests/      ← 테스트",
    "",
    "## 규칙",
    "- Python 3.11 / data/raw/ 수정 금지",
])

page_num(d,5,7)
save(img,"05_claude_md.png")

# ══════════════════════════════════════════════════════════════
# SLIDE 06 — 슬래시 커맨드 (전체 폭 테이블)
# ══════════════════════════════════════════════════════════════
img,d=new_slide()
cy_s=top_header(d,"CH01-06","슬래시 커맨드","세션 안에서 동작을 제어하는 명령어. / 로 시작하며 탭 자동완성을 지원합니다.",title_sz=36)

# 3열 헤더
C1=FULL_X; C2=FULL_X+240; C3=FULL_X+900
T(d,C1,cy_s,"커맨드",13,"sb",C300); T(d,C2,cy_s,"기능 설명",13,"sb",C300); T(d,C3,cy_s,"언제 쓰나",13,"sb",C300)
hline(d,FULL_X,cy_s+22,FULL_W,C900,1); ry=cy_s+30

cmds=[
    ("/init",    "프로젝트 분석 후 CLAUDE.md 자동 생성",       "처음 시작 시 한 번"),
    ("/compact", "긴 대화 요약 — 토큰·비용 절약",             "대화가 길어질 때"),
    ("/clear",   "대화 기록 초기화 — 새 작업 시작",           "새 기능 작업 전"),
    ("/config",  "설정 화면 열기 (모델·권한 등)",              "설정 변경 필요 시"),
    ("/doctor",  "설치 상태·버전·인증 상태 확인",              "오류 발생 시 첫 점검"),
    ("/help",    "사용 가능한 커맨드 전체 목록 표시",           "모르는 게 있을 때"),
    ("/review",  "현재 변경사항 코드 리뷰 요청",               "커밋 전 검토"),
    ("/memory",  "메모리 파일 목록 확인 및 편집",             "CLAUDE.md 관리"),
]
ROW_H_C=56
for i,(cmd,desc,when) in enumerate(cmds):
    bg=WHITE if i%2==0 else C050
    d.rectangle([FULL_X,ry,FULL_X+FULL_W,ry+ROW_H_C],fill=bg)
    d.text((C1+4,ry+16),cmd,font=F(21,"mono"),fill=C700)
    T(d,C2,ry+18,desc,19,"r",C900)
    T(d,C3,ry+20,when,16,"r",C500)
    ry+=ROW_H_C
hline(d,FULL_X,ry,FULL_W,C100)

page_num(d,6,7)
save(img,"06_commands.png")

# ══════════════════════════════════════════════════════════════
# SLIDE 07 — 비용 관리
# ══════════════════════════════════════════════════════════════
img,d=new_slide()
left_col(d,"CH01-07","토큰 절약과\n비용 관리","효율적인 사용 습관 하나로 비용을 절반 이하로 줄일 수 있습니다.")

hline(d,RIGHT_X,72,RIGHT_W,C900,2)

LW3=int(RIGHT_W*0.52); RX3=RIGHT_X+LW3+48; RW3=RIGHT_W-LW3-48

T(d,RIGHT_X,84,"비용 절약 전략 5가지",14,"sb",C300)
hline(d,RIGHT_X,104,LW3,C100)
tips=[
    ("/compact 자주 사용",   "긴 대화 요약 → 토큰 소비 대폭 감소"),
    ("기능마다 새 세션 시작", "컨텍스트 누적 방지 → 불필요한 토큰 없앰"),
    ("CLAUDE.md 200줄 이하","매 세션 로드 비용 절감"),
    ("프롬프트 캐싱 활용",   "반복 컨텍스트 90% 할인 자동 적용"),
    ("Haiku 모델 병행",      "단순 작업은 저렴한 모델에 위임"),
]
ry=112
for i,(tip,desc) in enumerate(tips):
    f_n=F(13,"sb"); f_t=F(19,"sb"); f_d=F(15,"r")
    T(d,RIGHT_X,ry+18,f"0{i+1}",13,"sb",C300)
    d.text((RIGHT_X+40,ry+8),tip,font=f_t,fill=C900)
    d.text((RIGHT_X+40,ry+34),desc,font=f_d,fill=C500)
    ry+=62
    hline(d,RIGHT_X+40,ry,LW3-40,C100)

# 오른쪽: 캐싱 설명 + 요금제
hline(d,RX3-24,80,1,C100,H-152)
T(d,RX3,84,"프롬프트 캐싱",14,"sb",C300)
hline(d,RX3,104,RW3,C100)
ry3=116
wT(d,RX3,ry3,"같은 컨텍스트(CLAUDE.md, 파일 내용)를 반복 전송할 때 Anthropic이 자동으로 캐시합니다. 별도 설정 없이 자동 적용됩니다.",16,"r",C700,RW3,lh=1.6)
ry3+=100
for k,v in [("입력 토큰 할인","90%"),("캐시 저장 추가 비용","25%"),("설정 필요 여부","자동 적용")]:
    hline(d,RX3,ry3,RW3,C100)
    T(d,RX3,ry3+12,k,15,"r",C500)
    T(d,RX3+RW3,ry3+10,v,18,"sb",C900,"right")
    ry3+=42
hline(d,RX3,ry3,RW3,C100); ry3+=28

T(d,RX3,ry3,"구독 요금제 비교",14,"sb",C300); ry3+=24
hline(d,RX3,ry3,RW3,C900,1); ry3+=12
for plan,price,desc in [("Pro","$20/월","개인 실습용"),("Max","$100/월","실무·팀 협업"),("API","사용량 과금","프로그래밍 연동")]:
    T(d,RX3,ry3,plan,17,"sb",C900)
    T(d,RX3+RW3,ry3,price,17,"sb",C700,"right")
    T(d,RX3,ry3+26,desc,14,"r",C500)
    ry3+=58
    hline(d,RX3,ry3,RW3,C100)

page_num(d,7,7)
save(img,"07_cost.png")

print(f"\n✅ 레퍼런스 디자인 슬라이드 7장 → {OUT}")
