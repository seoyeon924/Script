#!/usr/bin/env python3
"""
CH01 슬라이드 v3 — 1920×1080 스케일 최적화
- 폰트 전체 1.5× 확대
- 콘텐츠가 슬라이드 80%+ 차지
- 행 높이 / 간격 / 여백 모두 확대
"""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1920, 1080
OUT  = "/tmp/Script-repo/output/ch01_ref"
os.makedirs(OUT, exist_ok=True)

# ── 무채색 팔레트 ───────────────────────────────────────────
WHITE = (255,255,255)
BG    = (255,255,255)
C900  = ( 22, 22, 22)
C700  = ( 55, 55, 55)
C500  = (105,105,105)
C300  = (165,165,165)
C100  = (225,225,225)
C050  = (245,245,245)
BADGE = ( 38, 38, 38)

# ── 폰트 ───────────────────────────────────────────────────
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

def tw(d,t,f): return max(1,d.textbbox((0,0),t,font=f)[2])
def th(d,t,f): b=d.textbbox((0,0),t,font=f); return max(1,b[3]-b[1])

def T(d, x, y, s, sz, wt, color, align="left"):
    if not s: return
    f=F(sz,wt)
    if align=="center": x=x-tw(d,s,f)//2
    if align=="right":  x=x-tw(d,s,f)
    d.text((int(x),int(y)),s,font=f,fill=color)

def wT(d, x, y, s, sz, wt, color, maxw, lh=1.55):
    f=F(sz,wt); words=s.split(); lines=[]; cur=""
    for w in words:
        test=(cur+" "+w).strip()
        if tw(d,test,f)>maxw and cur: lines.append(cur); cur=w
        else: cur=test
    if cur: lines.append(cur)
    for line in lines:
        d.text((int(x),int(y)),line,font=f,fill=color)
        y+=int(th(d,line,f)*lh)
    return y

def HL(d, x, y, w, color=C100, h=1):
    d.rectangle([int(x),int(y),int(x+w),int(y+h)],fill=color)

def VL(d, x, y1, y2, color=C100):
    d.rectangle([int(x),int(y1),int(x+1),int(y2)],fill=color)

def code_block(d, x, y, w, lines):
    """코드 블록 — 큰 폰트, 넉넉한 패딩"""
    PAD=28; LH=46
    bh=PAD*2+len(lines)*LH
    d.rectangle([x,y,x+w,y+bh],fill=C050)
    d.rectangle([x,y,x+4,y+bh],fill=C700)
    f_m=F(26,"mono"); f_k=F(22,"r")
    cy=y+PAD
    for line in lines:
        if "←" in line:
            parts=line.split("←",1)
            main=parts[0].rstrip(); annot="← "+parts[1].strip()
            d.text((x+PAD,cy),main,font=f_m,fill=C700)
            mw=tw(d,main,f_m)
            d.text((x+PAD+mw+12,cy+3),annot,font=f_k,fill=C300)
        else:
            d.text((x+PAD,cy),line,font=f_m,fill=C700)
        cy+=LH
    return y+bh

def badge(d, x, y, s, sz=17):
    f=F(sz,"sb")
    bw=tw(d,s,f)+18; bh=th(d,s,f)+10
    d.rectangle([x,y,x+bw,y+bh],fill=BADGE)
    d.text((x+9,y+5),s,font=f,fill=WHITE)
    return bw, bh

def pg(d, n, total):
    f=F(20,"r"); s=f"{n} / {total}"
    d.text((W-100-tw(d,s,f),H-48),s,font=f,fill=C300)

def new_slide():
    img=Image.new("RGB",(W,H),BG)
    d=ImageDraw.Draw(img)
    return img,d

def save(img,fname):
    p=f"{OUT}/{fname}"; img.save(p); print(f"✓ {p}")

# ── 레이아웃 상수 ────────────────────────────────────────────
MX     = 100          # 외부 마진
LEFT_W = 540          # 좌측 컬럼 (28%)
GAP    = 100          # 좌우 갭
RX     = MX+LEFT_W+GAP  # 우측 콘텐츠 시작 X
RW     = W-RX-MX        # 우측 콘텐츠 너비
FW     = W-MX*2         # 전체 폭

def left_col(d, cat, title, desc="", tsz=58):
    """좌측 컬럼 헤더"""
    y=72
    bw,bh=badge(d,MX,y,cat); y+=bh+18
    f_t=F(tsz,"b"); words=title.split(); lines=[]; cur=""
    for w in words:
        test=(cur+" "+w).strip()
        if tw(d,test,f_t)>LEFT_W and cur: lines.append(cur); cur=w
        else: cur=test
    if cur: lines.append(cur)
    for line in lines:
        d.text((MX,y),line,font=f_t,fill=C900); y+=int(th(d,line,f_t)*1.18)
    y+=24
    if desc: y=wT(d,MX,y,desc,20,"r",C500,LEFT_W-20,lh=1.65)
    return y

def top_header(d, cat, title, desc="", tsz=52):
    """전체 폭 레이아웃 상단 헤더"""
    y=64
    bw,bh=badge(d,MX,y,cat); y+=bh+14
    f_t=F(tsz,"b")
    d.text((MX,y),title,font=f_t,fill=C900); y+=th(d,title,f_t)+14
    if desc:
        y=wT(d,MX,y,desc,20,"r",C500,FW*0.56,lh=1.5)
    y+=28; HL(d,MX,y,FW,C100); return y+28

# ══════════════════════════════════════════════════════════════
# SLIDE 01 — 챕터 타이틀 (전용 레이아웃)
# 좌: 블랙 패널 (챕터 번호) / 우: 화이트 패널 (제목 + 클립 목록)
# ══════════════════════════════════════════════════════════════
img,d=new_slide()

LP = 560        # 좌측 블랙 패널 너비
PAD_L = 64      # 블랙 패널 내부 패딩
PAD_R = 72      # 우측 패딩

# ── 좌측 블랙 패널 ──────────────────────────────────────────
d.rectangle([0, 0, LP, H], fill=C900)

# 코스 라벨 (상단)
T(d, PAD_L, 60, "FASTCAMPUS", 15, "sb", C300)
T(d, PAD_L, 86, "× DATABRIDGE", 15, "sb", C300)

# 대형 챕터 번호 — 슬라이드 중앙에 배치
f_num = F(260, "b")
num_str = "01"
nw = tw(d, num_str, f_num)
nh = th(d, num_str, f_num)
nx = PAD_L
ny = (H - nh) // 2 - 40
d.text((nx, ny), num_str, font=f_num, fill=WHITE)

# "CHAPTER" 레이블 (숫자 위)
T(d, PAD_L, ny - 44, "CHAPTER", 20, "sb", C500)

# 총 시간 (하단)
T(d, PAD_L, H - 100, "총 7강  ·  105분", 20, "r", C500)
T(d, PAD_L, H - 66, "클로드 코드 실무 완성", 17, "r", C300)

# ── 우측 화이트 패널 ─────────────────────────────────────────
RX_T = LP + PAD_R   # 우측 콘텐츠 X
RW_T = W - RX_T - 80

# 제목 블록
ty = 72
T(d, RX_T, ty, "클로드 코드", 80, "b", C900)
ty += th(d, "클로드 코드", F(80, "b")) + 4
T(d, RX_T, ty, "첫 걸음", 80, "b", C500)
ty += th(d, "첫 걸음", F(80, "b")) + 28
wT(d, RX_T, ty, "에이전트 구조부터 비용 관리까지 실무에서 바로 쓰는 흐름을 배웁니다.", 21, "r", C500, RW_T)
ty += 56
HL(d, RX_T, ty, RW_T, C100, 1)
ty += 36

# 클립 목록 (단일 열, 세로로 쭉)
clips = [
    ("01", "클로드 코드란 무엇인가",    "에이전트 구조  ·  15분"),
    ("02", "설치 & 첫 번째 세션",       "macOS/Linux  ·  15분"),
    ("03", "CLAUDE.md — 프로젝트 메모리","영구 컨텍스트 설정  ·  20분"),
    ("04", "기본 워크플로우",           "파일 읽기·쓰기·실행  ·  15분"),
    ("05", "작업 모드",                "Plan · Auto · Editor  ·  10분"),
    ("06", "슬래시 커맨드 완전 정리",    "핵심 커맨드 8개  ·  15분"),
    ("07", "토큰 절약과 비용 관리",      "프롬프트 캐싱 · 요금제  ·  20분"),
]
# 가용 높이를 클립 수로 나눠 균등 배분
avail = H - ty - 60
RH_T = avail // len(clips)

for num, title, sub in clips:
    T(d, RX_T, ty + RH_T // 2 - 22, num, 16, "sb", C300)
    d.text((RX_T + 52, ty + RH_T // 2 - 28), title, font=F(24, "sb"), fill=C900)
    d.text((RX_T + 52, ty + RH_T // 2 + 10), sub, font=F(18, "r"), fill=C500)
    HL(d, RX_T, ty + RH_T - 1, RW_T, C100)
    ty += RH_T

pg(d, 1, 7)
save(img, "01_title.png")

# ══════════════════════════════════════════════════════════════
# SLIDE 02 — ChatGPT vs Claude Code
# ══════════════════════════════════════════════════════════════
img,d=new_slide()
left_col(d,"CH01-01","두 가지\n도구의 차이","같은 AI처럼 보이지만 구조가 완전히 다릅니다.")

HL(d,RX,72,RW,C900,2)

HALF=(RW-40)//2; rx2=RX+HALF+40
T(d,RX+HALF//2,82,"ChatGPT",26,"b",C500,"center")
T(d,rx2+HALF//2,82,"Claude Code",26,"b",C900,"center")
HL(d,RX,122,RW,C100); ry=134

rows=[
    ("실행 방식","웹 브라우저 대화창","터미널 (명령줄 인터페이스)"),
    ("파일 접근","직접 접근 불가 — 복붙 필요","파일 시스템 직접 읽기·쓰기"),
    ("코드 실행","결과를 텍스트로만 반환","코드를 직접 실행하고 결과 확인"),
    ("프로젝트 기억","세션 종료 시 초기화","CLAUDE.md로 영구 기억 유지"),
    ("작업 자동화","사람이 결과를 직접 적용","계획→실행→검증 루프 자동 처리"),
]
for label,left_v,right_v in rows:
    T(d,RX,ry+46,label,18,"sb",C300)
    T(d,RX+HALF//2,ry+42,left_v,24,"r",C500,"center")
    T(d,rx2+HALF//2,ry+42,right_v,24,"sb",C900,"center")
    ry+=128; HL(d,RX,ry,RW,C100)

ry+=32
wT(d,RX,ry,"→  ChatGPT는 '조언'을 주는 도구이고, Claude Code는 '직접 작업'을 수행하는 에이전트입니다.",22,"r",C700,RW)

pg(d,2,7); save(img,"02_comparison.png")

# ══════════════════════════════════════════════════════════════
# SLIDE 03 — 에이전트 루프 (전체 폭)
# ══════════════════════════════════════════════════════════════
img,d=new_slide()
cy_s=top_header(d,"CH01-01","에이전트 루프","목표를 받아 계획하고, 도구를 선택해 실행한 뒤 결과를 검증하는 과정이 반복됩니다.")

T(d,MX,cy_s,"Action",18,"sb",C300)
HL(d,MX+80,cy_s+10,FW-80,C100); cy_s+=44

steps=[
    ("사용자 지시","요청 전달"),
    ("계획","순서·방법 결정"),
    ("도구 선택","파일? 코드? 검색?"),
    ("실행","실제 작업 수행"),
    ("결과 확인","성공 여부 검증"),
    ("완료","보고 또는 반복"),
]
n=len(steps); SW=FW//n; ARR_Y=cy_s+200
for i,(title,desc) in enumerate(steps):
    sx=MX+i*SW; cx=sx+SW//2; r=36
    is_first=(i==0)
    fill=C900 if is_first else C050
    d.ellipse([cx-r,ARR_Y-r,cx+r,ARR_Y+r],fill=fill,outline=C900,width=2)
    nd=str(i+1); fn=F(28,"b")
    d.text((cx-tw(d,nd,fn)//2,ARR_Y-th(d,nd,fn)//2),nd,font=fn,fill=WHITE if is_first else C700)
    if i<n-1:
        ax_s=cx+r+6; ax_e=MX+(i+1)*SW+(((i+1)*SW)//2)-r-6
        d.line([(ax_s,ARR_Y),(ax_e,ARR_Y)],fill=C300,width=2)
        d.polygon([(ax_e,ARR_Y-8),(ax_e+12,ARR_Y),(ax_e,ARR_Y+8)],fill=C300)
    T(d,cx,ARR_Y+r+22,title,26,"sb",C900,"center")
    T(d,cx,ARR_Y+r+60,desc,20,"r",C500,"center")

loop_y=ARR_Y+150
HL(d,MX,loop_y,FW,C100)
T(d,MX+FW//2,loop_y+16,"↑  이 과정이 반복되는 것을 에이전트 루프(Agent Loop)라고 합니다",20,"r",C500,"center")

tool_y=loop_y+80
HL(d,MX,tool_y,FW,C100)
T(d,MX,tool_y+22,"클로드 코드가 루프에서 사용하는 도구",20,"sb",C300)
CW3=FW//3; ty_b=tool_y+76
for i,(cat,items) in enumerate([
    ("파일 관련",["파일 읽기 (Read)","파일 쓰기 (Write)","파일 검색 (Glob)"]),
    ("실행 관련",["터미널 명령어 (Bash)","코드 실행 (Python/Shell)"]),
    ("검색 관련",["코드베이스 검색","웹 검색 (설정 시)"]),
]):
    cx3=MX+i*CW3; ty3=ty_b
    T(d,cx3,ty3,cat,22,"sb",C700); ty3+=40
    for item in items:
        T(d,cx3,ty3,"·  "+item,21,"r",C500); ty3+=40
    if i<2: VL(d,MX+i*CW3+CW3,tool_y+74,H-60)

pg(d,3,7); save(img,"03_agent_loop.png")

# ══════════════════════════════════════════════════════════════
# SLIDE 04 — 설치
# ══════════════════════════════════════════════════════════════
img,d=new_slide()
left_col(d,"CH01-02","설치\n& 첫 번째 세션","명령어 한 줄로 5분 안에 완료됩니다.")

HL(d,RX,72,RW,C900,2)

LW2=int(RW*0.5); rx3=RX+LW2+60; rw3=RW-LW2-60

T(d,RX,84,"사전 준비",18,"sb",C300)
HL(d,RX,110,LW2,C100); ry=122
for label,val in [
    ("계정","claude.ai  Pro ($20/월)  또는  Max ($100/월)"),
    ("OS","macOS / Linux   (Windows: WSL2)"),
    ("터미널","기본 Terminal 또는 iTerm2"),
]:
    T(d,RX,ry+2,label,18,"sb",C300)
    T(d,RX+90,ry,val,22,"r",C700)
    ry+=56; HL(d,RX,ry,LW2,C100)
ry+=32

T(d,RX,ry,"설치 명령어",18,"sb",C300); ry+=28
ry=code_block(d,RX,ry,LW2,["curl -fsSL https://claude.ai/install.sh | bash"])+20
T(d,RX,ry,"Homebrew 사용 시",18,"r",C300); ry+=26
ry=code_block(d,RX,ry,LW2,["brew install --cask claude-code"])+20
T(d,RX,ry,"버전 확인",18,"r",C300); ry+=26
code_block(d,RX,ry,LW2,["claude --version"])

VL(d,rx3-30,80,H-60)
T(d,rx3,84,"첫 실행 순서",18,"sb",C300)
HL(d,rx3,110,rw3,C100); ry4=122
for num,step,desc in [
    ("01","claude  입력","터미널에서 클로드 세션 시작"),
    ("02","브라우저 로그인","OAuth 방식 — 별도 비밀번호 없음"),
    ("03","cd your-project","프로젝트 폴더로 이동"),
    ("04","/init  입력","CLAUDE.md 자동 생성"),
    ("05","첫 요청 입력",'"data.csv 읽어서 요약해줘"'),
]:
    T(d,rx3,ry4+12,num,18,"sb",C300)
    d.text((rx3+68,ry4),step,font=F(30,"sb"),fill=C900)
    d.text((rx3+68,ry4+44),desc,font=F(22,"r"),fill=C500)
    ry4+=100; HL(d,rx3+68,ry4-8,rw3-68,C100)

pg(d,4,7); save(img,"04_install.png")

# ══════════════════════════════════════════════════════════════
# SLIDE 05 — CLAUDE.md
# ══════════════════════════════════════════════════════════════
img,d=new_slide()
left_col(d,"CH01-03","CLAUDE.md","세션이 끝나도 프로젝트 맥락을 유지하는 영구 메모리 파일.\n/init으로 자동 생성됩니다.")

HL(d,RX,72,RW,C900,2)
LW3=int(RW*0.46); rx4=RX+LW3+60; rw4=RW-LW3-60

T(d,RX,84,"CLAUDE.md에 담을 내용",18,"sb",C300)
HL(d,RX,110,LW3,C100); ry=122
for num,title,desc in [
    ("01","프로젝트 개요","목적·기술 스택 한 줄 요약"),
    ("02","폴더 구조","데이터·스크립트·결과물 위치"),
    ("03","자주 쓰는 명령어","실행·테스트·배포 명령어"),
    ("04","코딩 규칙","Python 버전·라이브러리 스타일"),
    ("05","금지 사항","원본 데이터 수정 금지 등"),
]:
    T(d,RX,ry+6,num,16,"sb",C300)
    T(d,RX+54,ry,title,26,"sb",C900)
    T(d,RX+54,ry+40,desc,21,"r",C500)
    ry+=96; HL(d,RX+54,ry-8,LW3-54,C100)
ry+=16

T(d,RX,ry,"팁",18,"sb",C300); ry+=28
wT(d,RX,ry,"→  /init 입력 시 클로드가 프로젝트를 스캔해 CLAUDE.md를 자동 생성합니다.",22,"r",C700,LW3)

VL(d,rx4-30,80,H-60)
T(d,rx4,84,"작성 예시",18,"sb",C300)
code_block(d,rx4,110,rw4,[
    "# 프로젝트: DataBridge 분석 툴",
    "FastAPI + React + PostgreSQL",
    "",
    "## Commands",
    "python app.py   ← 서버 실행",
    "pytest tests/   ← 테스트 실행",
    "",
    "## 규칙",
    "- Python 3.11 사용",
    "- data/raw/ 폴더 수정 금지",
    "- 결과는 data/output/ 에 저장",
])

pg(d,5,7); save(img,"05_claude_md.png")

# ══════════════════════════════════════════════════════════════
# SLIDE 06 — 슬래시 커맨드 (전체 폭)
# ══════════════════════════════════════════════════════════════
img,d=new_slide()
cy_s=top_header(d,"CH01-06","슬래시 커맨드","세션 안에서 동작을 제어하는 명령어. / 로 시작하며 탭 자동완성을 지원합니다.")

C1=MX; C2=MX+280; C3=MX+1060
T(d,C1,cy_s,"커맨드",17,"sb",C300)
T(d,C2,cy_s,"기능 설명",17,"sb",C300)
T(d,C3,cy_s,"언제 쓰나",17,"sb",C300)
HL(d,MX,cy_s+26,FW,C900,1); ry=cy_s+36

cmds=[
    ("/init",   "프로젝트 분석 후 CLAUDE.md 자동 생성",    "처음 시작 시 한 번"),
    ("/compact","긴 대화 요약 — 토큰·비용 절약",           "대화가 길어질 때"),
    ("/clear",  "대화 기록 초기화 — 새 작업 시작",         "새 기능 작업 전"),
    ("/config", "설정 화면 열기 (모델·권한 등)",            "설정 변경 필요 시"),
    ("/doctor", "설치 상태·버전·인증 상태 확인",            "오류 발생 시 첫 점검"),
    ("/help",   "사용 가능한 커맨드 전체 목록 표시",         "모르는 게 있을 때"),
    ("/review", "현재 변경사항 코드 리뷰 요청",             "커밋 전 검토"),
    ("/memory", "메모리 파일 목록 확인 및 편집",           "CLAUDE.md 관리"),
]
RH_C=95
for i,(cmd,desc,when) in enumerate(cmds):
    bg=WHITE if i%2==0 else C050
    d.rectangle([MX,ry,MX+FW,ry+RH_C],fill=bg)
    d.text((C1+6,ry+30),cmd,font=F(28,"mono"),fill=C700)
    T(d,C2,ry+32,desc,24,"r",C900)
    T(d,C3,ry+34,when,21,"r",C500)
    ry+=RH_C
HL(d,MX,ry,FW,C100)

pg(d,6,7); save(img,"06_commands.png")

# ══════════════════════════════════════════════════════════════
# SLIDE 07 — 비용 관리
# ══════════════════════════════════════════════════════════════
img,d=new_slide()
left_col(d,"CH01-07","토큰 절약과\n비용 관리","효율적인 사용 습관으로 비용을 절반 이하로 줄일 수 있습니다.")

HL(d,RX,72,RW,C900,2)
LW4=int(RW*0.52); rx5=RX+LW4+60; rw5=RW-LW4-60

T(d,RX,84,"절약 전략 5가지",18,"sb",C300)
HL(d,RX,110,LW4,C100); ry=122
for i,(tip,desc) in enumerate([
    ("/compact 자주 사용",   "긴 대화 요약 → 토큰 소비 대폭 감소"),
    ("기능마다 새 세션 시작", "컨텍스트 누적 방지 → 불필요한 토큰 없앰"),
    ("CLAUDE.md 200줄 이하","매 세션 로드 비용 절감"),
    ("프롬프트 캐싱 활용",   "반복 컨텍스트 90% 할인 자동 적용"),
    ("Haiku 모델 병행",      "단순 작업은 저렴한 모델에 위임"),
]):
    T(d,RX,ry+8,f"0{i+1}",16,"sb",C300)
    d.text((RX+52,ry-2),tip,font=F(26,"sb"),fill=C900)
    d.text((RX+52,ry+38),desc,font=F(22,"r"),fill=C500)
    ry+=96; HL(d,RX+52,ry-8,LW4-52,C100)

VL(d,rx5-30,80,H-60)
T(d,rx5,84,"프롬프트 캐싱",18,"sb",C300)
HL(d,rx5,110,rw5,C100); ry3=130
wT(d,rx5,ry3,"같은 컨텍스트(CLAUDE.md 등)를 반복 전송할 때\nAnthropic이 자동으로 캐시합니다. 별도 설정 불필요.",22,"r",C700,rw5-20,lh=1.7)
ry3+=130
for k,v in [("입력 토큰 할인","90%"),("자동 적용 여부","설정 없이 자동")]:
    HL(d,rx5,ry3,rw5,C100)
    T(d,rx5,ry3+16,k,20,"r",C500)
    T(d,rx5+rw5,ry3+14,v,22,"sb",C900,"right")
    ry3+=56
HL(d,rx5,ry3,rw5,C100); ry3+=40

T(d,rx5,ry3,"구독 요금제",18,"sb",C300); ry3+=28
HL(d,rx5,ry3,rw5,C900,1); ry3+=16
for plan,price,desc in [
    ("Pro","$20 / 월","개인 실습용"),
    ("Max","$100 / 월","실무·팀 협업"),
    ("API","사용량 과금","프로그래밍 연동"),
]:
    T(d,rx5,ry3,plan,22,"sb",C900)
    T(d,rx5+rw5,ry3,price,22,"sb",C700,"right")
    T(d,rx5,ry3+32,desc,18,"r",C500)
    ry3+=72; HL(d,rx5,ry3,rw5,C100)

pg(d,7,7); save(img,"07_cost.png")
print(f"\n✅ v3 슬라이드 7장 완료")
