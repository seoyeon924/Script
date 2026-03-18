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

# ── 컬러 팔레트 (연하늘색 계열) ──────────────────────────────
LBLUE  = (228, 241, 252)   # 연하늘색 — 섹션 배경
LBLUE2 = (208, 228, 247)   # 중간 연하늘색 — 강조 행/셀
BLUE_T = ( 42, 110, 180)   # 텍스트 블루 — 레이블, 아이콘
LGRAY  = (240, 240, 242)   # 연회색 — 교차 행

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

def wT_para(d, x, y, s, sz, wt, color, maxw, lh=1.65, gap=14):
    """문장 단위 줄바꿈 — 원칙: 2-3문장은 반드시 줄 분리.
    '. '(마침표+공백) 기준으로 문장을 나눠 각각 wT() 렌더링.
    엄청 긴 단일 문장이면 일반 wT()와 동일하게 동작."""
    parts = [p.strip() for p in s.split('. ')]
    sentences = [p + '.' if i < len(parts)-1 else p for i,p in enumerate(parts) if p]
    if len(sentences) <= 1:
        return wT(d, x, y, s, sz, wt, color, maxw, lh=lh)
    for sent in sentences:
        y = wT(d, x, y, sent, sz, wt, color, maxw, lh=lh)
        y += gap
    return y - gap

def HL(d, x, y, w, color=C100, h=1):
    d.rectangle([int(x),int(y),int(x+w),int(y+h)],fill=color)

def VL(d, x, y1, y2, color=C100):
    d.rectangle([int(x),int(y1),int(x+1),int(y2)],fill=color)

def _code_mixed(d, x, y, line, f_mono, f_kr, color):
    """코드블록 내 한글/영문 혼합 렌더링 — Menlo는 한글 미지원이므로 분리 처리"""
    if not any('\uac00' <= c <= '\ud7a3' for c in line):
        d.text((int(x), int(y)), line, font=f_mono, fill=color)
        return
    segs = []; cur = ""; cur_kr = None
    for c in line:
        kr = '\uac00' <= c <= '\ud7a3' or '\u3131' <= c <= '\u314e'
        if cur_kr is None: cur_kr = kr; cur = c
        elif kr == cur_kr: cur += c
        else: segs.append((cur, cur_kr)); cur = c; cur_kr = kr
    if cur: segs.append((cur, cur_kr))
    cx = x
    for seg, kr in segs:
        f = f_kr if kr else f_mono
        d.text((int(cx), int(y)), seg, font=f, fill=color)
        cx += tw(d, seg, f)

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
            _code_mixed(d,x+PAD,cy,line,f_m,f_k,C700)
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
    """전체 폭 레이아웃 상단 헤더
    원칙: 제목-부제목 간격 최소 22px, 부제목은 wT_para()로 문장 분리"""
    y=64
    bw,bh=badge(d,MX,y,cat); y+=bh+14
    f_t=F(tsz,"b")
    d.text((MX,y),title,font=f_t,fill=C900); y+=th(d,title,f_t)+22   # ← 14→22
    if desc:
        y=wT_para(d,MX,y,desc,20,"r",C500,int(FW*0.56),lh=1.55)
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
wT(d, RX_T, ty, "에이전트 루프부터 비용 관리까지, 실무에서 바로 써먹는 핵심만 담았어요.", 21, "r", C500, RW_T)
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
# SLIDE 02 — ChatGPT vs Claude Code (풀와이드)
# ══════════════════════════════════════════════════════════════
img,d=new_slide()
cy_s=top_header(d,"CH01-01","두 가지 도구의 차이","겉보기엔 둘 다 AI인데, 동작 방식이 완전히 달라요.")

# 3열 헤더: 구분 / ChatGPT / Claude Code
COL0=MX; COL1=MX+340; COL2=MX+340+int(FW*0.38)
T(d,COL0,cy_s,"구분",18,"sb",C300)
T(d,COL1,cy_s,"ChatGPT",22,"sb",C500)
# Claude Code 헤더 배경 + 텍스트
d.rectangle([COL2-16,cy_s-6,MX+FW,cy_s+32],fill=LBLUE)
T(d,COL2,cy_s,"Claude Code",22,"sb",BLUE_T)
cy_s+=30; HL(d,MX,cy_s,FW,C900,1); ry=cy_s+12

rows=[
    ("실행 방식","웹 브라우저 대화창","터미널 (명령줄 인터페이스)"),
    ("파일 접근","직접 접근 불가 — 복붙 필요","파일 시스템 직접 읽기·쓰기"),
    ("코드 실행","결과를 텍스트로만 반환","코드를 직접 실행하고 결과 확인"),
    ("프로젝트 기억","세션 종료 시 초기화","CLAUDE.md로 영구 기억 유지"),
    ("작업 자동화","사람이 결과를 직접 적용","계획→실행→검증 루프 자동 처리"),
]
RH2=int((H-ry-140)/len(rows))
for i,(label,lv,rv) in enumerate(rows):
    # ChatGPT 쪽: 교차 회색
    gray_bg = WHITE if i%2==0 else LGRAY
    d.rectangle([MX,ry,COL2-16,ry+RH2],fill=gray_bg)
    # Claude Code 쪽: 연하늘색 고정 (강도만 교차)
    blue_bg = LBLUE if i%2==0 else LBLUE2
    d.rectangle([COL2-16,ry,MX+FW,ry+RH2],fill=blue_bg)
    T(d,COL0,ry+RH2//2-12,label,22,"sb",C700)
    T(d,COL1,ry+RH2//2-14,lv,24,"r",C500)
    T(d,COL2,ry+RH2//2-14,rv,24,"sb",BLUE_T)
    ry+=RH2

HL(d,MX,ry,FW,C100); ry+=28
wT(d,MX,ry,"→  ChatGPT는 조언해주는 도구, Claude Code는 직접 손 대는 에이전트예요.",22,"r",C700,FW)

pg(d,2,7); save(img,"02_comparison.png")

# ══════════════════════════════════════════════════════════════
# SLIDE 03 — 에이전트 루프 (전체 폭)
# ══════════════════════════════════════════════════════════════
img,d=new_slide()
cy_s=top_header(d,"CH01-01","에이전트 루프","목표를 받으면 스스로 계획하고, 도구를 골라 실행하고, 결과를 확인하는 과정이 반복돼요.")

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

# ── 에이전트 자율 구간 배경 (steps 2~5, index 1~4) ──────────
ag_x1 = MX + SW; ag_x2 = MX + 5*SW
d.rectangle([ag_x1, ARR_Y-100, ag_x2, ARR_Y+160], fill=LBLUE)
T(d,(ag_x1+ag_x2)//2, ARR_Y-90, "에이전트 자율 실행 구간", 17, "sb", BLUE_T, "center")

for i,(title,desc) in enumerate(steps):
    sx=MX+i*SW; cx=sx+SW//2; r=36
    is_user=(i==0 or i==n-1)
    fill   = C900  if is_user else LBLUE2
    border = C900  if is_user else BLUE_T
    tc     = WHITE if is_user else BLUE_T
    d.ellipse([cx-r,ARR_Y-r,cx+r,ARR_Y+r],fill=fill,outline=border,width=2)
    nd=str(i+1); fn=F(28,"b")
    d.text((cx-tw(d,nd,fn)//2,ARR_Y-th(d,nd,fn)//2),nd,font=fn,fill=tc)
    if i<n-1:
        ax_s=cx+r+6; ax_e=MX+(i+1)*SW+(((i+1)*SW)//2)-r-6
        arr_c = BLUE_T if (0 < i < n-2) else C300
        d.line([(ax_s,ARR_Y),(ax_e,ARR_Y)],fill=arr_c,width=2)
        d.polygon([(ax_e,ARR_Y-8),(ax_e+12,ARR_Y),(ax_e,ARR_Y+8)],fill=arr_c)
    tc2 = BLUE_T if not is_user else C900
    T(d,cx,ARR_Y+r+22,title,26,"sb",tc2,"center")
    T(d,cx,ARR_Y+r+60,desc,20,"r",C500,"center")

loop_y=ARR_Y+150
HL(d,MX,loop_y,FW,C100)
T(d,MX+FW//2,loop_y+16,"↑  이 반복 과정을 에이전트 루프(Agent Loop)라고 해요",20,"r",C500,"center")

tool_y=loop_y+80
HL(d,MX,tool_y,FW,C100)
T(d,MX,tool_y+22,"루프 안에서 쓰는 주요 도구들",20,"sb",C300)
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
# SLIDE 04 — 설치 (풀와이드)
# ══════════════════════════════════════════════════════════════
img,d=new_slide()
cy_s=top_header(d,"CH01-02","설치 & 첫 번째 세션","명령어 하나면 5분 안에 끝나요.")

# 2열: 좌(설치) / 우(첫 실행)
HALF4=int(FW*0.46); VX4=MX+HALF4+40; RX4=VX4+30; RW4=FW-HALF4-80

# 좌 — 설치
T(d,MX,cy_s,"사전 준비",18,"sb",C300); HL(d,MX,cy_s+26,HALF4,C100); ry=cy_s+36
for label,val in [
    ("계정","Pro ($20/월)  또는  Max ($100/월)"),
    ("OS","macOS / Linux   (Windows: WSL2)"),
    ("터미널","기본 Terminal 또는 iTerm2"),
]:
    T(d,MX,ry+2,label,18,"sb",C300)
    T(d,MX+100,ry,val,22,"r",C700)
    ry+=52; HL(d,MX,ry,HALF4,C100)
ry+=28
T(d,MX,ry,"설치 명령어",18,"sb",C300); ry+=26
ry=code_block(d,MX,ry,HALF4,["curl -fsSL https://claude.ai/install.sh | bash"])+16
T(d,MX,ry,"Homebrew 사용 시",18,"r",C300); ry+=22
ry=code_block(d,MX,ry,HALF4,["brew install --cask claude-code"])+16
T(d,MX,ry,"버전 확인",18,"r",C300); ry+=22
code_block(d,MX,ry,HALF4,["claude --version"])

# 구분선
VL(d,VX4,cy_s-10,H-60)

# 우 — 첫 실행
T(d,RX4,cy_s,"첫 실행 순서",18,"sb",C300)
HL(d,RX4,cy_s+26,RW4,C100); ry4=cy_s+36
steps4=[
    ("01","claude  입력","터미널에서 클로드 세션 시작"),
    ("02","브라우저 로그인","OAuth 방식 — 별도 비밀번호 없음"),
    ("03","cd your-project","프로젝트 폴더로 이동"),
    ("04","/init  입력","CLAUDE.md 자동 생성"),
    ("05","첫 요청 입력",'"data.csv 읽어서 요약해줘"'),
]
RH4=int((H-ry4-60)/len(steps4))
for num,step,desc in steps4:
    T(d,RX4,ry4+RH4//2-22,num,18,"sb",C300)
    d.text((RX4+58,ry4+RH4//2-28),step,font=F(30,"sb"),fill=C900)
    d.text((RX4+58,ry4+RH4//2+10),desc,font=F(22,"r"),fill=C500)
    ry4+=RH4; HL(d,RX4+58,ry4-4,RW4-58,C100)

pg(d,4,7); save(img,"04_install.png")

# ══════════════════════════════════════════════════════════════
# SLIDE 05 — CLAUDE.md (풀와이드)
# ══════════════════════════════════════════════════════════════
img,d=new_slide()
cy_s=top_header(d,"CH01-03","CLAUDE.md — 프로젝트 메모리","세션이 끝나도 맥락이 유지돼요. /init 치면 자동으로 만들어줘요.")

HALF5=int(FW*0.44); VX5=MX+HALF5+40; RX5=VX5+30; RW5=FW-HALF5-80

# 좌 — 담을 내용 5항목
T(d,MX,cy_s,"CLAUDE.md에 담을 내용",18,"sb",C300)
HL(d,MX,cy_s+26,HALF5,C100); ry=cy_s+36
items5=[
    ("01","프로젝트 개요","목적·기술 스택 한 줄 요약"),
    ("02","폴더 구조","데이터·스크립트·결과물 위치"),
    ("03","자주 쓰는 명령어","실행·테스트·배포 명령어"),
    ("04","코딩 규칙","Python 버전·라이브러리 스타일"),
    ("05","금지 사항","원본 데이터 수정 금지 등"),
]
RH5=int((H-ry-130)/len(items5))
for num,title,desc in items5:
    T(d,MX,ry+RH5//2-18,num,16,"sb",C300)
    d.text((MX+50,ry+RH5//2-26),title,font=F(26,"sb"),fill=C900)
    d.text((MX+50,ry+RH5//2+10),desc,font=F(21,"r"),fill=C500)
    ry+=RH5; HL(d,MX+50,ry-4,HALF5-50,C100)
ry+=12
wT(d,MX,ry,"→  /init 치면 클로드가 프로젝트 구조를 보고 알아서 만들어줘요.",20,"r",C700,HALF5)

# 구분선
VL(d,VX5,cy_s-10,H-60)

# 우 — 코드블록
T(d,RX5,cy_s,"작성 예시",18,"sb",C300); cy_s+=34
code_block(d,RX5,cy_s,RW5,[
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
cy_s=top_header(d,"CH01-06","슬래시 커맨드","세션 중에 동작을 제어할 때 쓰는 명령어예요. /로 시작하고, 탭으로 자동완성돼요.")

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
KEY_CMDS={"/init","/compact"}
for i,(cmd,desc,when) in enumerate(cmds):
    is_key = cmd in KEY_CMDS
    bg = LBLUE if is_key else (WHITE if i%2==0 else LGRAY)
    d.rectangle([MX,ry,MX+FW,ry+RH_C],fill=bg)
    cmd_c = BLUE_T if is_key else C700
    d.text((C1+6,ry+30),cmd,font=F(28,"mono"),fill=cmd_c)
    T(d,C2,ry+32,desc,24,"r",C900)
    T(d,C3,ry+34,when,21,"r",C500 if not is_key else BLUE_T)
    ry+=RH_C
HL(d,MX,ry,FW,C100)

pg(d,6,7); save(img,"06_commands.png")

# ══════════════════════════════════════════════════════════════
# SLIDE 07 — 비용 관리 (풀와이드)
# ══════════════════════════════════════════════════════════════
img,d=new_slide()
cy_s=top_header(d,"CH01-07","토큰 절약과 비용 관리","습관 몇 가지만 들이면 비용이 확 줄어요.")

HALF7=int(FW*0.52); VX7=MX+HALF7+40; RX7=VX7+30; RW7=FW-HALF7-80

# 좌 — 절약 전략
T(d,MX,cy_s,"절약 전략 5가지",18,"sb",C300)
HL(d,MX,cy_s+26,HALF7,C100); ry=cy_s+36
tips=[
    ("/compact 자주 사용",   "긴 대화 요약 → 토큰 소비 대폭 감소"),
    ("기능마다 새 세션 시작", "컨텍스트 누적 방지 → 불필요한 토큰 없앰"),
    ("CLAUDE.md 200줄 이하","매 세션 로드 비용 절감"),
    ("프롬프트 캐싱 활용",   "반복 컨텍스트 90% 할인 자동 적용"),
    ("Haiku 모델 병행",      "단순 작업은 저렴한 모델에 위임"),
]
RH7=int((H-ry-60)/len(tips))
for i,(tip,desc) in enumerate(tips):
    T(d,MX,ry+RH7//2-18,f"0{i+1}",16,"sb",C300)
    d.text((MX+50,ry+RH7//2-26),tip,font=F(26,"sb"),fill=C900)
    d.text((MX+50,ry+RH7//2+10),desc,font=F(22,"r"),fill=C500)
    ry+=RH7; HL(d,MX+50,ry-4,HALF7-50,C100)

# 구분선
VL(d,VX7,cy_s-10,H-60)

# 우 — 캐싱 섹션 연하늘색 박스
cache_top = cy_s - 10
T(d,RX7,cy_s,"프롬프트 캐싱",18,"sb",BLUE_T)
HL(d,RX7,cy_s+26,RW7,BLUE_T,1); ry3=cy_s+38
wT_para(d,RX7,ry3,"CLAUDE.md 같은 반복 내용은 Anthropic이 자동으로 캐시해줘요. 따로 설정 안 해도 돼요.",22,"r",C700,RW7,lh=1.65,gap=10)
ry3+=106
for k,v in [("입력 토큰 할인","90%"),("자동 적용 여부","설정 없이 자동")]:
    HL(d,RX7,ry3,RW7,C100)
    T(d,RX7,ry3+14,k,20,"r",C500)
    T(d,RX7+RW7,ry3+12,v,22,"sb",BLUE_T,"right")
    ry3+=52
# 캐싱 박스 배경 (내용 그린 뒤 사각형을 먼저 그려야 하지만, 배경 레이어 순서 상 다음에 재그림)
HL(d,RX7,ry3,RW7,C100); ry3+=36

T(d,RX7,ry3,"구독 요금제",18,"sb",C300); ry3+=28
HL(d,RX7,ry3,RW7,C900,1); ry3+=4
for pi,(plan,price,note) in enumerate([
    ("Pro","$20 / 월","개인 실습용"),
    ("Max","$100 / 월","실무·팀 협업"),
    ("API","사용량 과금","프로그래밍 연동"),
]):
    ry3+=20                                          # 행 상단 여백
    T(d,RX7,ry3,plan,22,"sb",C900)
    T(d,RX7+RW7,ry3,price,22,"sb",C700,"right")
    ry3+=34                                          # 제목 아래 여백
    T(d,RX7,ry3,note,18,"r",C500)
    ry3+=38                                          # 부제목 아래 여백
    HL(d,RX7,ry3,RW7,C100)

pg(d,7,7); save(img,"07_cost.png")
print(f"\n✅ v3 슬라이드 7장 완료")
