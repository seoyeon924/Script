#!/usr/bin/env python3
"""
클로드 코드 워크플로우 치트시트 — Korean / Orange / Pretendard
1440 × 1640px
"""
from PIL import Image, ImageDraw, ImageFont
import os

# ── 캔버스 ──────────────────────────────────────────────────
W, H      = 1440, 1640
OUTER_M   = 44
COL_GAP   = 18
HEADER_H  = 126
CONTENT_Y = HEADER_H + 28
COL_W     = (W - OUTER_M*2 - COL_GAP*2) // 3   # 438
X1, X2, X3 = OUTER_M, OUTER_M+COL_W+COL_GAP, OUTER_M+(COL_W+COL_GAP)*2

# Row heights
H1 = 526   # S1+S4 / S2 / S3
H2 = 580   # S5 / S6+S7 / S8+S9
H3 = 260   # S10 / S11 / S12
R1Y = CONTENT_Y
R2Y = R1Y + H1 + 16
R3Y = R2Y + H2 + 16

# ── 색상 ─────────────────────────────────────────────────────
BG      = (253, 245, 235)   # #FDF5EB
CARD_BG = (255, 255, 255)
CARD_BD = (232, 221, 208)   # #E8DDD0
CODE_BG = (240, 230, 216)   # #F0E6D8
ORANGE  = (243, 123, 28)    # #F37B1C
ORANGE_D= (224, 106, 15)    # #E06A0F
BLK     = (26, 26, 26)
BODY    = (68, 68, 68)
DIM     = (136, 136, 136)
CODE_TX = (51, 51, 51)
WHITE   = (255, 255, 255)
LIGHT_O = (255, 240, 224)   # 연한 오렌지 배경

# ── 폰트 ─────────────────────────────────────────────────────
FP = {
    "r": "/Users/sy/Library/Fonts/Pretendard-Regular.otf",
    "sb":"/Users/sy/Library/Fonts/Pretendard-SemiBold.otf",
    "b": "/Users/sy/Library/Fonts/Pretendard-Bold.otf",
}
MONO = "/System/Library/Fonts/Courier.ttc"
_fc = {}

def F(sz, wt="r"):
    k=(sz,wt)
    if k not in _fc:
        try: _fc[k]=ImageFont.truetype(FP.get(wt,FP["r"]),sz)
        except: _fc[k]=ImageFont.load_default()
    return _fc[k]

def FM(sz):
    k=("m",sz)
    if k not in _fc:
        try: _fc[k]=ImageFont.truetype(MONO,sz)
        except: _fc[k]=F(sz)
    return _fc[k]

def tw(d,t,f): return d.textbbox((0,0),t,font=f)[2]
def th(d,t,f): b=d.textbbox((0,0),t,font=f); return b[3]-b[1]

def put(d, x, y, text, sz, wt, color):
    d.text((x,y), text, font=F(sz,wt), fill=color)
    return th(d,text,F(sz,wt))

def putm(d, x, y, text, sz, color):
    d.text((x,y), text, font=FM(sz), fill=color)
    return th(d,text,FM(sz))

def wrap_put(d, x, y, text, sz, wt, color, max_w, lh=1.65):
    f=F(sz,wt); words=text.split(); lines,cur=[],""
    for w in words:
        test=(cur+" "+w).strip()
        if tw(d,test,f)>max_w and cur: lines.append(cur); cur=w
        else: cur=test
    if cur: lines.append(cur)
    for line in lines:
        d.text((x,y),line,font=f,fill=color); y+=int(th(d,line,f)*lh)
    return y

def hrule(d, x, y, w, color=CARD_BD, h=1):
    d.rectangle([x,y,x+w,y+h], fill=color)

# ── 배지 & 컴포넌트 ───────────────────────────────────────────
def num_badge(d, x, y, num, r=13):
    d.ellipse([x,y,x+r*2,y+r*2], fill=ORANGE)
    f=F(11,"b"); ns=str(num)
    nw=tw(d,ns,f); nh=th(d,ns,f)
    d.text((x+r-nw//2, y+r-nh//2), ns, font=f, fill=WHITE)
    return r*2

def pill(d, x, y, text, sz=10, bg=ORANGE, fg=WHITE, r=4):
    f=F(sz,"sb"); pw=tw(d,text,f)+14; ph=th(d,text,f)+8
    d.rounded_rectangle([x,y,x+pw,y+ph], radius=r, fill=bg)
    d.text((x+7,y+4), text, font=f, fill=fg)
    return pw+6, ph

def section_card(d, x, y, w, h, num, title):
    """카드 박스 + 헤더 → 콘텐츠 시작 y 반환"""
    d.rounded_rectangle([x,y,x+w,y+h], radius=8, fill=CARD_BG, outline=CARD_BD, width=1)
    p=14
    bh=num_badge(d, x+p, y+p, num)
    put(d, x+p+bh+8, y+p+2, title, 13, "b", BLK)
    hy=y+p+bh+10
    hrule(d, x+p, hy, w-p*2)
    return hy+10, p

def code(d, x, y, w, lines, sz=9, mono=True, bg=CODE_BG):
    """코드 블록"""
    lh=16; pad=9; bh=pad*2+len(lines)*lh
    d.rounded_rectangle([x,y,x+w,y+bh], radius=4, fill=bg)
    cy=y+pad
    for line in lines:
        if mono: putm(d,x+pad,cy,line,sz,CODE_TX)
        else: put(d,x+pad,cy,line,sz,"r",CODE_TX)
        cy+=lh
    return y+bh

def bullets(d, x, y, items, sz=11, mark="○", gap=1.8, color=BODY, mcolor=ORANGE):
    f=F(sz,"r"); lh=int(th(d,"A",f)*gap)
    for item in items:
        d.text((x,y), mark, font=f, fill=mcolor)
        d.text((x+16,y), item, font=f, fill=color)
        y+=lh
    return y

def checks(d, x, y, items, sz=11):
    return bullets(d,x,y,items,sz,"○")

# ════════════════════════════════════════════════════════════════
# 캔버스 초기화
# ════════════════════════════════════════════════════════════════
img = Image.new("RGB",(W,H), BG)
d   = ImageDraw.Draw(img)

# ── 최상단 헤더 ──────────────────────────────────────────────
d.rectangle([0,0,W,HEADER_H], fill=BG)
# 타이틀
tx=OUTER_M; ty=34
put(d, tx, ty, "클로드 코드", 36, "b", BLK)
cx=tw(d,"클로드 코드",F(36,"b"))+tx+10
put(d, cx, ty, "워크플로우 치트시트", 36, "b", ORANGE_D)
# 서브타이틀
sy=ty+th(d,"A",F(36,"b"))+8
put(d, tx, sy,
    "시작하기 · 프로젝트 설정 · 파일 구조 · 스킬 · 훅 · 메모리 · 워크플로우 · 2026 Edition",
    11, "r", DIM)
hrule(d, OUTER_M, HEADER_H-2, W-OUTER_M*2, CARD_BD, h=1)

# ════════════════════════════════════════════════════════════════
# ① 시작하기 (Col1, Row1, h=240)
# ════════════════════════════════════════════════════════════════
cy,p = section_card(d,X1,R1Y,COL_W,240,1,"시작하기")
w = COL_W-p*2; x=X1+p

cy=code(d,x,cy,w,[
    "curl -fsSL https://claude.ai/install.sh | bash"
],sz=9)+8

cy=code(d,x,cy,w,[
    "cd your-project",
    "claude",
    "/init",
],sz=9)+8

put(d,x,cy,"코드베이스를 스캔하고",11,"r",BODY); cy+=18
put(d,x,cy,"스타터 메모리 파일을 생성합니다.",11,"r",BODY)

# ════════════════════════════════════════════════════════════════
# ④ CLAUDE.md 모범 사례 (Col1, Row1 하단, h=270)
# ════════════════════════════════════════════════════════════════
cy4=R1Y+240+16
cy4,p4 = section_card(d,X1,cy4,COL_W,270,4,"CLAUDE.md 모범 사례")
x4=X1+p4; w4=COL_W-p4*2

items4=[
    "/init 실행 후 출력 다듬기",
    "지시사항 구체적으로 작성",
    "클로드가 추론 불가한 주의사항 추가",
    "@파일명으로 문서 참조",
    "워크플로우 규칙 추가",
    "메모리 간결하게 유지",
    "팀 공유를 위해 Git에 커밋",
]
checks(d,x4,cy4,items4,sz=11)

# ════════════════════════════════════════════════════════════════
# ② CLAUDE.md 이해하기 (Col2, Row1, h=526)
# ════════════════════════════════════════════════════════════════
cy2,p2 = section_card(d,X2,R1Y,COL_W,H1,2,"CLAUDE.md 이해하기")
x2=X2+p2; w2=COL_W-p2*2

put(d,x2,cy2,
    "CLAUDE.md = 클로드의 프로젝트 영구 메모리.",11,"r",BODY); cy2+=18
put(d,x2,cy2,
    "매 세션 시작 시 자동으로 로드됩니다.",11,"r",BODY); cy2+=22

# WHAT/WHY/HOW 배지
for tag in ["WHAT","WHY","HOW"]:
    pw,ph=pill(d,x2,cy2,tag,10,ORANGE,WHITE); x2+=pw+6
x2=X2+p2; cy2+=22+6

items_w=["기술 스택","디렉토리 맵","아키텍처"]
items_y=["각 모듈 목적","디자인 결정"]
items_h=["빌드/테스트 명령어","lint 명령어","워크플로우","주의사항"]

for i,(col_items,col_title) in enumerate([(items_w,"WHAT"),(items_y,"WHY"),(items_h,"HOW")]):
    bx=x2+i*(w2//3)
    bw=w2//3-4
    put(d,bx,cy2,col_title,9,"sb",ORANGE); by=cy2+14
    for it in col_items:
        put(d,bx,by,"· "+it,9,"r",BODY); by+=15
cy2+=60; hrule(d,x2,cy2,w2); cy2+=10

cy2=code(d,x2,cy2,w2,[
    "# Project: MyApp",
    "FastAPI REST API + React SPA + Postgres",
    "",
    "## Commands",
    "npm run dev",
    "npm run test",
    "npm run lint",
    "",
    "## Architecture",
    "/app  → Next.js App Router pages",
    "/lib  → shared utilities",
    "/prisma → DB schema & migrations",
],sz=9)+8

# ════════════════════════════════════════════════════════════════
# ③ 메모리 파일 계층 구조 (Col3, Row1, h=526)
# ════════════════════════════════════════════════════════════════
cy3,p3 = section_card(d,X3,R1Y,COL_W,H1,3,"메모리 파일 계층 구조")
x3=X3+p3; w3=COL_W-p3*2

tree=[
    ("~/.claude/CLAUDE.md", "전역 — 모든 프로젝트"),
    ("~/CLAUDE.md",         "부모 — 모노레포 루트"),
    ("./CLAUDE.md",         "프로젝트 — git에 공유"),
    ("./frontend/CLAUDE.md","서브폴더 — 범위 제한"),
]
for path,desc in tree:
    cy3=code(d,x3,cy3,w3,[path],sz=9,mono=True)+2
    put(d,x3+10,cy3,desc,10,"r",DIM); cy3+=18

cy3+=6; hrule(d,x3,cy3,w3); cy3+=10
notes=[
    "각 파일 200줄 이하 유지",
    "서브폴더 파일은 컨텍스트 추가",
    "부모 컨텍스트 덮어쓰기 금지",
]
checks(d,x3,cy3,notes,sz=11)

# ════════════════════════════════════════════════════════════════
# ⑤ 프로젝트 파일 구조 (Col1, Row2, h=580)
# ════════════════════════════════════════════════════════════════
cy5,p5 = section_card(d,X1,R2Y,COL_W,H2,5,"프로젝트 파일 구조")
x5=X1+p5; w5=COL_W-p5*2

tree5=[
    "your project/",
    "├ CLAUDE.md",
    "├ .claude/",
    "│ ├ settings.json",
    "│ ├ settings.local.json",
    "│ └ skills/",
    "│   ├ code-review/",
    "│   │ └ SKILL.md",
    "│   ├ testing/",
    "│   │ └ SKILL.md",
    "│   └ helpers.py",
    "├ commands/",
    "│ └ deploy.md",
    "└ agents/",
    "  └ security-reviewer.md",
    "└ .gitignore",
]
code(d,x5,cy5,w5,tree5,sz=9)

# ════════════════════════════════════════════════════════════════
# ⑥ 스킬 추가 — 슈퍼파워 (Col2, Row2, h=380)
# ════════════════════════════════════════════════════════════════
cy6,p6 = section_card(d,X2,R2Y,COL_W,380,6,"스킬 추가 (슈퍼파워)")
x6=X2+p6; w6=COL_W-p6*2

put(d,x6,cy6,
    "스킬 = 클로드가 자연어로 자동 호출하는 마크다운 가이드",10,"r",BODY); cy6+=20

# 스킬 경로
for label,path in [("프로젝트 스킬",".claude/skills/<name>/SKILL.md"),
                   ("개인 스킬","~/.claude/skills/<name>/SKILL.md")]:
    put(d,x6,cy6,label,10,"sb",BLK); cy6+=16
    cy6=code(d,x6,cy6,w6,[path],sz=9)+6

cy6+=4; hrule(d,x6,cy6,w6); cy6+=8
put(d,x6,cy6,"Description 필드가 자동 활성화에 핵심입니다.",10,"r",ORANGE_D); cy6+=20

cy6=code(d,x6,cy6,w6,[
    "name: testing patterns",
    "description: Jest testing patterns",
    "allowed tools: Read, Grep, Glob",
],sz=9)+8

cy6=code(d,x6,cy6,w6,[
    "# Testing Patterns",
    "Use describe + it + AAA 패턴",
    "Use factory mocks",
],sz=9)

# ════════════════════════════════════════════════════════════════
# ⑦ AI 엔지니어를 위한 스킬 아이디어 (Col2, Row2 하단, h=184)
# ════════════════════════════════════════════════════════════════
R2B_Y = R2Y+380+16
cy7,p7 = section_card(d,X2,R2B_Y,COL_W,184,7,"AI 엔지니어를 위한 스킬 아이디어")
x7=X2+p7; w7=COL_W-p7*2

items7a=["code-review","testing patterns","commit messages"]
items7b=["docker-deploy","codebase-visualizer","api-design"]
for i,(a,b) in enumerate(zip(items7a,items7b)):
    bx=x7; bw=w7//2
    d.text((bx,cy7+i*20),"○ "+a,font=F(11,"r"),fill=BODY)
    d.text((bx+bw,cy7+i*20),"○ "+b,font=F(11,"r"),fill=BODY)

# ════════════════════════════════════════════════════════════════
# ⑧ 훅 설정하기 (Col3, Row2, h=380)
# ════════════════════════════════════════════════════════════════
cy8,p8 = section_card(d,X3,R2Y,COL_W,380,8,"훅 설정하기")
x8=X3+p8; w8=COL_W-p8*2

put(d,x8,cy8,"훅 = 결정론적 콜백",10,"r",BODY); cy8+=18

# 훅 타입 배지
for tag in ["PreToolUse","PostToolUse","Notification"]:
    pw,ph=pill(d,x8,cy8,tag,9,ORANGE,WHITE); x8+=pw
x8=X3+p8; cy8+=22+8

cy8=code(d,x8,cy8,w8,[
    '"hooks": {',
    '  "PreToolUse": [',
    '    {',
    '      "matcher": "Bash",',
    '      "hooks": [',
    '        {',
    '          "type": "command",',
    '          "command": "scripts/sec.sh",',
    '          "timeout": 5',
    '        }',
    '      ]',
    '    }',
    '  ]',
    '}',
],sz=9)+8

put(d,x8,cy8,"Exit codes: ",10,"sb",BLK)
ex=x8+tw(d,"Exit codes: ",F(10,"sb"))+2
for code_txt,lbl in [("0","allow"),("2","block")]:
    pw2,ph2=pill(d,ex,cy8-2,f"{code_txt} → {lbl}",9,ORANGE if lbl=="block" else (180,180,180),WHITE); ex+=pw2+4

# ════════════════════════════════════════════════════════════════
# ⑨ 권한 & 안전 (Col3, Row2 하단, h=184)
# ════════════════════════════════════════════════════════════════
R3B_Y=R2Y+380+16
cy9,p9 = section_card(d,X3,R3B_Y,COL_W,184,9,"권한 & 안전")
x9=X3+p9; w9=COL_W-p9*2

code(d,x9,cy9,w9,[
    '{',
    '  "permissions": {',
    '    "allow": [',
    '      "Read:*",',
    '      "Bash:git:*",',
    '      "Write:*:*.md"',
    '    ],',
    '    "deny": [',
    '      "Read:env:*",',
    '      "Bash:sudo:*"',
    '    ]',
    '  }',
    '}',
],sz=9)

# ════════════════════════════════════════════════════════════════
# ⑩ 4계층 아키텍처 (Col1, Row3, h=260)
# ════════════════════════════════════════════════════════════════
cy10,p10 = section_card(d,X1,R3Y,COL_W,H3,10,"4계층 아키텍처")
x10=X1+p10; w10=COL_W-p10*2

layers=[
    ("L1 – CLAUDE.md",  "영구 컨텍스트와 규칙"),
    ("L2 – 스킬",       "자동 호출 지식 팩"),
    ("L3 – 훅",         "안전 게이트와 자동화"),
    ("L4 – 에이전트",   "자체 컨텍스트를 가진 서브에이전트"),
]
lh10=44
for i,(lbl,desc) in enumerate(layers):
    ly=cy10+i*lh10
    # 배경 띠
    bg10 = LIGHT_O if i%2==0 else CARD_BG
    d.rounded_rectangle([x10,ly,x10+w10,ly+lh10-4],radius=4,fill=bg10)
    put(d,x10+8,ly+6,lbl,11,"b",ORANGE_D)
    put(d,x10+8,ly+6+18,desc,10,"r",BODY)

# ════════════════════════════════════════════════════════════════
# ⑪ 일일 워크플로우 패턴 (Col2, Row3, h=260)
# ════════════════════════════════════════════════════════════════
cy11,p11 = section_card(d,X2,R3Y,COL_W,H3,11,"일일 워크플로우 패턴")
x11=X2+p11; w11=COL_W-p11*2

steps11=[
    "cd project && claude",
    "Shift + Tab + Tab → Plan Mode",
    "기능 의도 서술",
    "Shift + Tab → Auto Accept",
    "/compact",
    "Esc Esc + rewind",
    "자주 커밋",
    "기능마다 새 세션 시작",
]
lh11=26
for i,step in enumerate(steps11):
    sy11=cy11+i*lh11
    bg11=CODE_BG if i%2==0 else (248,243,237)
    d.rounded_rectangle([x11,sy11,x11+w11,sy11+lh11-2],radius=3,fill=bg11)
    put(d,x11+10,sy11+5,step,10,"r" if i%2==0 else "sb",BLK)

# ════════════════════════════════════════════════════════════════
# ⑫ 빠른 참조 (Col3, Row3, h=260)
# ════════════════════════════════════════════════════════════════
cy12,p12 = section_card(d,X3,R3Y,COL_W,H3,12,"빠른 참조")
x12=X3+p12; w12=COL_W-p12*2

ref12=[
    ("/init",      "CLAUDE.md 생성"),
    ("/doccat",    "설치 확인"),
    ("/compact",   "컨텍스트 압축"),
    ("Shift+Tab",  "자동 수락 전환"),
    ("Tab",        "확장 사고 전환"),
    ("Esc Esc",    "메뉴 되감기"),
]
col_split=w12//2
for i,(cmd,desc) in enumerate(ref12):
    ry12=cy12+i*30
    bg12=CODE_BG if i%2==0 else CARD_BG
    d.rounded_rectangle([x12,ry12,x12+w12,ry12+28],radius=3,fill=bg12)
    # 구분선
    d.rectangle([x12+col_split-1,ry12,x12+col_split,ry12+28],fill=CARD_BD)
    # 명령어 — bold orange
    put(d,x12+8,ry12+7,cmd,10,"b",ORANGE_D)
    # 설명
    put(d,x12+col_split+8,ry12+7,desc,10,"r",BODY)

# ── 최하단 서명 ───────────────────────────────────────────────
put(d, OUTER_M, H-28,
    "DataBridge × Fastcampus — Claude Code 실무 완성 | Pretendard · Orange Theme",
    10,"r",DIM)

# ── 저장 ─────────────────────────────────────────────────────
os.makedirs("/tmp/Script-repo/output/v2", exist_ok=True)
out="/tmp/Script-repo/output/v2/cheatsheet.png"
img.save(out)
print(f"✓ {out}")
