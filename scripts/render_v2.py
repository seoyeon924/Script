#!/usr/bin/env python3
"""
v2 — Pretendard + 6종 슬라이드 레이아웃
01 2컬럼비교 / 02 번호리스트 / 03 카드그리드 /
04 Painpoint→Solution 테이블 / 05 스크린샷 카드 / 06 참가자 인용행
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from design_systems import DESIGN_SYSTEMS, W, H, s, FS, FW, FONTS
from design_systems import GRAY_COLOR, ORANGE_COLOR
from PIL import Image, ImageDraw, ImageFont

OUT = "/tmp/Script-repo/output/v2"

# ── 폰트 ──────────────────────────────────────────────────────
_fc = {}
def F(size, weight="regular"):
    key = (size, weight)
    if key not in _fc:
        path = FONTS.get(weight, FONTS["fallback"])
        if not os.path.exists(path): path = FONTS["fallback"]
        try: _fc[key] = ImageFont.truetype(path, size)
        except: _fc[key] = ImageFont.load_default()
    return _fc[key]
def Fk(key): return F(FS[key], FW[key])

def C(ds, key):
    cmap = GRAY_COLOR if ds["name"]=="Gray" else ORANGE_COLOR
    return cmap.get(key, ds["text_primary"])

# ── 텍스트 유틸 ───────────────────────────────────────────────
def tw(d,t,key): return d.textbbox((0,0),t,font=Fk(key))[2]
def th(d,t,key): b=d.textbbox((0,0),t,font=Fk(key)); return b[3]-b[1]
def twf(d,t,sz,w="regular"): return d.textbbox((0,0),t,font=F(sz,w))[2]
def thf(d,t,sz,w="regular"): b=d.textbbox((0,0),t,font=F(sz,w)); return b[3]-b[1]

def put(d,x,y,text,key,color):
    d.text((x,y),text,font=Fk(key),fill=color)
    return th(d,text,key)

def putf(d,x,y,text,sz,wt,color):
    d.text((x,y),text,font=F(sz,wt),fill=color)
    return thf(d,text,sz,wt)

def wrap(d,text,key,max_w):
    words=text.split(); lines,cur=[],""
    for w in words:
        test=(cur+" "+w).strip()
        if twf(d,test,FS[key],FW[key])>max_w and cur: lines.append(cur); cur=w
        else: cur=test
    if cur: lines.append(cur)
    return lines

def wrapf(d,text,sz,wt,max_w):
    words=text.split(); lines,cur=[],""
    for w in words:
        test=(cur+" "+w).strip()
        if twf(d,test,sz,wt)>max_w and cur: lines.append(cur); cur=w
        else: cur=test
    if cur: lines.append(cur)
    return lines

def put_wrap(d,x,y,text,key,color,max_w,lh=1.72):
    for line in wrap(d,text,key,max_w):
        d.text((x,y),line,font=Fk(key),fill=color)
        y+=int(th(d,line,key)*lh)
    return y

def put_wrapf(d,x,y,text,sz,wt,color,max_w,lh=1.72):
    for line in wrapf(d,text,sz,wt,max_w):
        d.text((x,y),line,font=F(sz,wt),fill=color)
        y+=int(thf(d,line,sz,wt)*lh)
    return y

def hrule(d,x,y,w,color,h=s(1)):
    d.rectangle([x,y,x+w,y+h],fill=color)

# ── Pill 태그 (2종) ───────────────────────────────────────────
def pill_filled(d,x,y,text,ds):
    px,py,r=s(18),s(8),s(4)
    pw=twf(d,text,FS["tag"],FW["tag"])+px*2
    ph=thf(d,text,FS["tag"],FW["tag"])+py*2
    d.rounded_rectangle([x,y,x+pw,y+ph],radius=r,fill=ds["tag_fill_bg"])
    d.text((x+px,y+py),text,font=Fk("tag"),fill=ds["tag_fill_txt"])
    return pw,ph

def pill_outline(d,x,y,text,ds,radius=s(20)):
    """완전 라운드 outline pill (레퍼런스 슬라이드2 스타일)"""
    px,py=s(18),s(8)
    pw=twf(d,text,FS["tag"],FW["tag"])+px*2
    ph=thf(d,text,FS["tag"],FW["tag"])+py*2
    d.rounded_rectangle([x,y,x+pw,y+ph],radius=radius,outline=ds["accent"],width=s(2))
    d.text((x+px,y+py),text,font=Fk("tag"),fill=ds["tag_out_txt"])
    return pw,ph

# ── 사이드바 ──────────────────────────────────────────────────
SIDEBAR_W = s(300)
CONTENT_X = s(370)
MARGIN    = s(52)

def sidebar(d,ds,category,title_lines,body="",meta=None):
    d.rectangle([0,0,SIDEBAR_W,H],fill=ds["bg_sidebar"])
    d.rectangle([SIDEBAR_W,0,SIDEBAR_W+s(1),H],fill=ds["border"])
    x,y=MARGIN,s(52)
    putf(d,x,y,category,FS["category"],"regular",C(ds,"category"))
    y+=int(thf(d,category,FS["category"],"regular")*1.5)+s(10)
    for line in title_lines:
        putf(d,x,y,line,FS["h1"],"bold",C(ds,"h1"))
        y+=int(thf(d,line,FS["h1"],"bold")*1.4)
    y+=s(16)
    if body:
        y=put_wrapf(d,x,y,body,FS["body"],"regular",C(ds,"body"),
                    SIDEBAR_W-x-s(16),lh=1.75)
        y+=s(14)
    hrule(d,x,y,SIDEBAR_W-x-s(16),ds["border"])
    y+=s(16)
    if meta:
        for k,v in meta.items():
            putf(d,x,y,k,FS["xs"],"regular",C(ds,"meta"))
            y+=thf(d,k,FS["xs"],"regular")+s(4)
            y=put_wrapf(d,x,y,v,FS["sm"],"regular",C(ds,"body"),
                        SIDEBAR_W-x-s(16),lh=1.6)
            y+=s(12)

def footer(d,ds):
    putf(d,MARGIN,H-s(36),"DataBridge × Fastcampus — Claude Code 실무 완성",
         FS["xs"],"regular",C(ds,"xs"))

# ════════════════════════════════════════════════════════════════
# SLIDE 01 — 2컬럼 비교 (기존 유지)
# ════════════════════════════════════════════════════════════════
def slide_01(ds):
    img=Image.new("RGB",(W,H),ds["bg"]); d=ImageDraw.Draw(img)
    sidebar(d,ds,"Chapter 01",["두 도구의","차이"],
            "같은 AI처럼 보이지만\n구조가 완전히 다릅니다.",
            {"핵심":"조언 vs 실행"})
    footer(d,ds)
    cx=CONTENT_X; cy=s(52); cw=W-cx-MARGIN
    _,ph=pill_filled(d,cx,cy,"도구 비교",ds); cy+=ph+s(18)
    putf(d,cx,cy,"챗지피티 vs 클로드 코드",FS["h2"],"bold",C(ds,"h2"))
    cy+=int(thf(d,"A",FS["h2"],"bold")*1.4)+s(6)
    hrule(d,cx,cy,cw,ds["border"]); cy+=s(28)
    col_gap=s(56); col_w=(cw-col_gap)//2; c1x=cx; c2x=cx+col_w+col_gap
    vline_top=cy
    putf(d,c1x,cy,"챗지피티",FS["h3"],"semibold",C(ds,"meta"))
    putf(d,c2x,cy,"클로드 코드",FS["h3"],"semibold",ds["accent"])
    cy+=int(thf(d,"A",FS["h3"],"semibold")*1.4)+s(12)
    rows=[("실행 환경","웹 브라우저 / 앱","터미널 (로컬 환경)"),
          ("파일 접근","불가능","직접 읽기·쓰기·실행"),
          ("작업 결과","텍스트 답변 생성","실제 파일·코드 변경"),
          ("기억 유지","세션 내에서만","CLAUDE.md 영구 보존"),
          ("주요 용도","정보 검색·아이디어","데이터 분석·자동화")]
    row_h=s(68)
    for i,(attr,v1,v2) in enumerate(rows):
        ry=cy+i*row_h
        if i%2==0:
            d.rectangle([c1x,ry,c1x+col_w,ry+row_h],fill=ds["bg_card"])
            d.rectangle([c2x,ry,c2x+col_w,ry+row_h],fill=ds["bg_card"])
        putf(d,c1x+s(14),ry+s(10),attr,FS["xs"],"regular",C(ds,"meta"))
        putf(d,c1x+s(14),ry+s(28),v1,FS["body"],"regular",C(ds,"body"))
        putf(d,c2x+s(14),ry+s(10),attr,FS["xs"],"regular",C(ds,"meta"))
        putf(d,c2x+s(14),ry+s(28),v2,FS["body"],"regular",C(ds,"h3"))
        hrule(d,c1x,ry+row_h,col_w,ds["border"])
        hrule(d,c2x,ry+row_h,col_w,ds["border"])
    cy+=len(rows)*row_h
    mid_x=c2x-col_gap//2
    d.rectangle([mid_x,vline_top,mid_x+s(1),cy],fill=ds["border"])
    cy+=s(20)
    bar_h=s(64)
    d.rounded_rectangle([cx,cy,cx+cw,cy+bar_h],radius=s(6),fill=ds["accent"])
    msg="핵심 — 클로드 코드는 조언자가 아니라 직접 실행하는 도구입니다."
    mw=twf(d,msg,FS["sm"],"regular")
    d.text((cx+(cw-mw)//2,cy+(bar_h-thf(d,msg,FS["sm"],"regular"))//2),
           msg,font=F(FS["sm"],"regular"),fill=ds["tag_fill_txt"])
    return img

# ════════════════════════════════════════════════════════════════
# SLIDE 02 — 에이전트 루프 번호리스트 (기존 유지)
# ════════════════════════════════════════════════════════════════
def slide_02(ds):
    img=Image.new("RGB",(W,H),ds["bg"]); d=ImageDraw.Draw(img)
    sidebar(d,ds,"Chapter 01",["에이전트","루프"],
            "지시를 받아서 완료까지\n스스로 처리하는 사이클입니다.",
            {"비유":"실무자가 일하는 방식"})
    footer(d,ds)
    cx=CONTENT_X; cy=s(52); cw=W-cx-MARGIN
    _,ph=pill_filled(d,cx,cy,"작동 방식",ds); cy+=ph+s(18)
    putf(d,cx,cy,"사용자 지시를 받으면 어떻게 처리하는가",FS["h2"],"bold",C(ds,"h2"))
    cy+=int(thf(d,"A",FS["h2"],"bold")*1.4)+s(6)
    put_wrapf(d,cx,cy,"에이전트는 이 사이클을 자동 반복하며 복잡한 작업도 단계별로 처리합니다.",
              FS["sm"],"regular",C(ds,"body"),cw,lh=1.6)
    cy+=thf(d,"A",FS["sm"],"regular")+s(28)
    NUM_W=s(52); GAP1=s(28); TITLE_W=s(195); GAP2=s(40)
    DESC_X=cx+NUM_W+GAP1+TITLE_W+GAP2; DESC_W=cw-(DESC_X-cx); ROW_H=s(96)
    steps=[("01","사용자 지시","자연어로 목표를 전달합니다.\n예: \"data.csv 분석해서 리포트 만들어줘\""),
           ("02","계획 수립","어떤 순서로 할지 스스로 결정합니다.\n파일 읽기 → 분석 코드 실행 → 결과 저장 순으로 계획합니다."),
           ("03","도구 실행","파일 읽기, 코드 실행, 파일 저장 등\n필요한 도구를 선택해 직접 수행합니다."),
           ("04","결과 확인","실행 결과를 확인하고 완료하거나,\n오류 시 원인을 파악해 자동으로 재시도합니다.")]
    hrule(d,cx,cy,cw,ds["border"])
    for num,title,desc in steps:
        ry=cy+s(1)+s(20)
        putf(d,cx,ry,num,FS["num"],"semibold",C(ds,"h3"))
        putf(d,cx+NUM_W+GAP1,ry,title,FS["h3"],"semibold",C(ds,"h3"))
        dy=ry
        for line in desc.split("\n"):
            d.text((DESC_X,dy),line,font=F(FS["sm"],"regular"),fill=C(ds,"body"))
            dy+=int(thf(d,line,FS["sm"],"regular")*1.75)
        cy+=ROW_H; hrule(d,cx,cy,cw,ds["border"])
    cy+=s(22)
    putf(d,cx,cy,"↺  이 사이클이 반복되는 것을 에이전트 루프라고 합니다.",
         FS["sm"],"regular",C(ds,"meta"))
    return img

# ════════════════════════════════════════════════════════════════
# SLIDE 03 — 카드 그리드 3×2 (기존 유지)
# ════════════════════════════════════════════════════════════════
def slide_03(ds):
    img=Image.new("RGB",(W,H),ds["bg"]); d=ImageDraw.Draw(img)
    sidebar(d,ds,"Chapter 01",["내장","도구 목록"],
            "에이전트는 도구를 조합해 작업합니다.\n기본 6가지 도구를 제공합니다.",
            {"확장":"MCP로 추가 가능"})
    footer(d,ds)
    cx=CONTENT_X; cy=s(52); cw=W-cx-MARGIN
    _,ph=pill_filled(d,cx,cy,"기본 도구",ds); cy+=ph+s(18)
    putf(d,cx,cy,"클로드 코드가 기본으로 탑재한 6가지 도구",FS["h2"],"bold",C(ds,"h2"))
    cy+=int(thf(d,"A",FS["h2"],"bold")*1.4)+s(8)
    hrule(d,cx,cy,cw,ds["border"]); cy+=s(28)
    cards=[("파일 읽기","텍스트·CSV·코드 파일을\n직접 열어서 내용 확인"),
           ("파일 쓰기","새 파일 생성 또는\n기존 파일 수정·저장"),
           ("파일 검색","특정 내용이 담긴\n파일을 프로젝트에서 탐색"),
           ("터미널 실행","셸 명령어 및\nPython 스크립트 실행"),
           ("코드베이스 검색","프로젝트 전체에서\n함수·변수·패턴 탐색"),
           ("웹 검색","MCP 설정 시\n외부 정보 실시간 수집")]
    COLS=3; CGAPX=s(20); CGAPY=s(18)
    card_w=(cw-CGAPX*(COLS-1))//COLS; card_h=s(158)
    for i,(title,desc) in enumerate(cards):
        col=i%COLS; row=i//COLS
        bx=cx+col*(card_w+CGAPX); by=cy+row*(card_h+CGAPY)
        d.rounded_rectangle([bx,by,bx+card_w,by+card_h],radius=s(6),
                             fill=ds["bg_card"],outline=ds["border"],width=s(1))
        putf(d,bx+s(16),by+s(14),f"{i+1:02d}",FS["xs"],"regular",C(ds,"meta"))
        ty=by+s(14)+thf(d,"A",FS["xs"],"regular")+s(12)
        putf(d,bx+s(16),ty,title,FS["h3"],"semibold",C(ds,"h3"))
        dy=ty+thf(d,title,FS["h3"],"semibold")+s(12)
        for line in desc.split("\n"):
            if dy+thf(d,line,FS["sm"],"regular")<by+card_h-s(10):
                d.text((bx+s(16),dy),line,font=F(FS["sm"],"regular"),fill=C(ds,"sm"))
                dy+=int(thf(d,line,FS["sm"],"regular")*1.7)
    return img

# ════════════════════════════════════════════════════════════════
# SLIDE 04 — Painpoint → Solution 비대칭 테이블 (NEW)
# 레퍼런스: Overview 슬라이드 / full-width 헤더 + 3행 테이블
# Painpoint(작은회색) : Solution(큰볼드블랙) : 목업박스
# ════════════════════════════════════════════════════════════════
def slide_04(ds):
    img=Image.new("RGB",(W,H),ds["bg"]); d=ImageDraw.Draw(img)
    footer(d,ds)

    # ── 좌상단 타이틀 블록 (sidebar 없음, full-width 헤더) ──
    hx,hy=MARGIN,s(44)
    putf(d,hx,hy,"Chapter 01 · Overview",FS["category"],"regular",C(ds,"category"))
    hy+=thf(d,"A",FS["category"],"regular")+s(10)
    putf(d,hx,hy,"클로드 코드 도입의 효과",FS["h1"],"bold",C(ds,"h1"))
    hy+=int(thf(d,"A",FS["h1"],"bold")*1.4)
    put_wrapf(d,hx,hy,
              "기존 방식의 문제점을 파악하고, 클로드 코드로 어떻게 해결되는지 살펴봅니다.\n각 Painpoint에 대응하는 Solution을 확인하세요.",
              FS["sm"],"regular",C(ds,"meta"),W//2-MARGIN*2,lh=1.65)
    
    # ── 3열 테이블 시작 위치 ──
    table_x = int(W*0.38)   # 테이블이 슬라이드 우측 60%에 배치
    table_w = W - table_x - MARGIN
    header_y = s(56)

    # 열 너비 — Painpoint:Solution:Mockup = 3:3:4 비율
    p_w = int(table_w * 0.28)
    s_w = int(table_w * 0.35)
    m_w = table_w - p_w - s_w

    p_x = table_x
    s_x = table_x + p_w
    m_x = table_x + p_w + s_w

    # 열 헤더
    putf(d,p_x,header_y,"Painpoint",FS["xs"],"regular",C(ds,"meta"))
    putf(d,s_x,header_y,"Solution",FS["xs"],"bold",C(ds,"h1"))
    hrule(d,p_x,header_y+thf(d,"A",FS["xs"],"regular")+s(12),
          table_w,ds["border"])

    # ── 3행 데이터 ──
    rows=[
        ("매번 명령어를\n직접 입력하는\n반복 작업",
         "CLAUDE.md로\n프로젝트 컨텍스트\n자동 로드"),
        ("코드 실행 후\n오류 원인을 직접\n분석해야 함",
         "에이전트가 오류를\n감지하고 스스로\n수정 후 재실행"),
        ("여러 파일을 일일이\n열어서 확인하는\n시간 낭비",
         "하나의 명령으로\n전체 파일 탐색·\n분석·저장 자동화"),
    ]

    row_h = s(130)
    ry = header_y + thf(d,"A",FS["xs"],"regular") + s(24)

    for pain_txt, sol_txt, in [(r[0],r[1]) for r in rows]:
        # Painpoint — Regular 13px #555 (억제된 표현)
        pain_sz = FS["sm"]
        put_wrapf(d,p_x+s(8),ry+s(16),pain_txt,pain_sz,"regular",
                  C(ds,"meta"),p_w-s(16),lh=1.7)

        # Solution — Bold 18px #000 (강조)
        sol_sz = FS["h3"]
        put_wrapf(d,s_x+s(8),ry+s(16),sol_txt,sol_sz,"bold",
                  C(ds,"h1"),s_w-s(16),lh=1.5)

        # 목업 박스 (회색 placeholder)
        mock_pad=s(12)
        d.rounded_rectangle([m_x+mock_pad, ry+mock_pad,
                              m_x+m_w-mock_pad, ry+row_h-mock_pad],
                             radius=s(4),fill=ds["bg_card"],
                             outline=ds["border"],width=s(1))
        # placeholder 텍스트
        ph_txt="[ 화면 캡처 ]"
        ph_w=twf(d,ph_txt,FS["xs"],"regular")
        ph_x=m_x+mock_pad+(m_w-mock_pad*2-ph_w)//2
        ph_y=ry+mock_pad+(row_h-mock_pad*2-thf(d,ph_txt,FS["xs"],"regular"))//2
        putf(d,ph_x,ph_y,ph_txt,FS["xs"],"regular",C(ds,"meta"))

        ry+=row_h
        hrule(d,p_x,ry,table_w,ds["border"])

    return img

# ════════════════════════════════════════════════════════════════
# SLIDE 05 — 사이드바 + 스크린샷 카드 4개 (NEW)
# 레퍼런스: Painpoint 1-1 / 카드4개 + 번호캡션 + 하단 사이드바 표
# ════════════════════════════════════════════════════════════════
def slide_05(ds):
    img=Image.new("RGB",(W,H),ds["bg"]); d=ImageDraw.Draw(img)
    footer(d,ds)

    # 사이드바 (하단에 데이터 테이블 포함)
    d.rectangle([0,0,SIDEBAR_W,H],fill=ds["bg_sidebar"])
    d.rectangle([SIDEBAR_W,0,SIDEBAR_W+s(1),H],fill=ds["border"])
    sx,sy=MARGIN,s(52)
    putf(d,sx,sy,"Chapter 01",FS["category"],"regular",C(ds,"category"))
    sy+=thf(d,"A",FS["category"],"regular")+s(10)
    for line in ["실습으로","확인하는","클로드 코드"]:
        putf(d,sx,sy,line,FS["h1"],"bold",C(ds,"h1"))
        sy+=int(thf(d,line,FS["h1"],"bold")*1.4)
    sy+=s(12)
    put_wrapf(d,sx,sy,"직접 실행하면서 에이전트 루프가 어떻게 동작하는지 관찰합니다.",
              FS["sm"],"regular",C(ds,"body"),SIDEBAR_W-sx-s(16),lh=1.75)
    sy+=thf(d,"A",FS["sm"],"regular")*2+s(20)
    hrule(d,sx,sy,SIDEBAR_W-sx-s(16),ds["border"]); sy+=s(20)

    # 사이드바 하단 — Mission + 데이터 테이블
    putf(d,sx,sy,"Mission",FS["xs"],"bold",C(ds,"h3")); sy+=thf(d,"A",FS["xs"],"bold")+s(6)
    put_wrapf(d,sx,sy,"각 단계에서 클로드 코드가\n수행하는 작업 확인",
              FS["sm"],"bold",C(ds,"h2"),SIDEBAR_W-sx-s(16),lh=1.5)
    sy+=thf(d,"A",FS["sm"],"bold")*2+s(14)

    # 데이터 테이블 (마지막 열 다크 강조)
    t_headers=["단계","A","B","C","D (최종)"]
    t_data=[["파일읽기","1s","2s","1s",""],
            ["코드실행","3s","8s","5s",""],
            ["파일저장","1s","2s","1s",""],
            ["총 시간","5s","12s","7s","자동"]]
    col_ws=[s(72),s(38),s(38),s(38),s(60)]
    cell_h=s(30)
    DARK_COL=4  # 마지막 열 다크

    hdr_y=sy
    for ci,(hdr,cw2) in enumerate(zip(t_headers,col_ws)):
        cx2=sx+sum(col_ws[:ci])
        bg=ds["accent"] if ci==DARK_COL else ds["bg_card"]
        tc=ds["tag_fill_txt"] if ci==DARK_COL else C(ds,"body")
        d.rectangle([cx2,hdr_y,cx2+cw2,hdr_y+cell_h],fill=bg)
        d.rectangle([cx2,hdr_y,cx2+cw2,hdr_y+cell_h],outline=ds["border"],width=s(1))
        hw=twf(d,hdr,FS["xs"],"semibold")
        d.text((cx2+(cw2-hw)//2,hdr_y+s(8)),hdr,font=F(FS["xs"],"semibold"),fill=tc)
    sy=hdr_y+cell_h

    for row in t_data:
        for ci,(val,cw2) in enumerate(zip(row,col_ws)):
            cx2=sx+sum(col_ws[:ci])
            bg=ds["accent"] if ci==DARK_COL else ds["bg"]
            tc=ds["tag_fill_txt"] if ci==DARK_COL else C(ds,"body")
            d.rectangle([cx2,sy,cx2+cw2,sy+cell_h],fill=bg)
            d.rectangle([cx2,sy,cx2+cw2,sy+cell_h],outline=ds["border"],width=s(1))
            vw=twf(d,val,FS["xs"],"regular")
            d.text((cx2+(cw2-vw)//2,sy+s(8)),val,font=F(FS["xs"],"regular"),fill=tc)
        sy+=cell_h

    # ── 우측 콘텐츠: outline pill + 서브타이틀 + 4개 스크린샷 카드 ──
    cx=CONTENT_X; cy=s(52); cw=W-cx-MARGIN

    # 중앙 정렬 outline pill (완전 라운드)
    pill_txt="실습 진행 흐름"
    pw,ph2=pill_outline(d,cx+(cw-twf(d,pill_txt,FS["tag"],FW["tag"])-s(36))//2,
                        cy,pill_txt,ds,radius=s(16))
    cy+=ph2+s(14)

    sub="클로드 코드가 파일을 읽고 분석하고 저장하는 과정을 직접 확인합니다"
    sub_w=twf(d,sub,FS["h3"],"bold")
    if sub_w>cw:
        put_wrapf(d,cx,cy,sub,FS["h3"],"bold",C(ds,"h2"),cw,lh=1.4)
        cy+=int(thf(d,"A",FS["h3"],"bold")*1.4)*2+s(4)
    else:
        sw=twf(d,sub,FS["h3"],"bold")
        putf(d,cx+(cw-sw)//2,cy,sub,FS["h3"],"bold",C(ds,"h2"))
        cy+=int(thf(d,"A",FS["h3"],"bold")*1.4)+s(4)

    hrule(d,cx,cy,cw,ds["border"]); cy+=s(28)

    # 4개 스크린샷 카드
    CARD_COLS=4; card_gap=s(16)
    card_w2=(cw-card_gap*(CARD_COLS-1))//CARD_COLS
    card_h2=s(200)

    captions=[
        (None, "claude 실행","터미널에서 claude 명령어\n입력 후 세션 시작"),
        ("01","파일 읽기","data.csv를 자동으로\n열어서 내용 확인"),
        ("02","분석 실행","Python 코드를 작성하고\n직접 실행해 집계"),
        ("03","결과 저장","분석 결과를 result.csv로\n자동 저장 완료"),
    ]

    for i,(num,ctitle,cdesc) in enumerate(captions):
        bx=cx+i*(card_w2+card_gap)
        # 카드 박스
        d.rounded_rectangle([bx,cy,bx+card_w2,cy+card_h2],radius=s(6),
                             fill=ds["bg_card"],outline=ds["border"],width=s(1))
        # placeholder 이미지 영역
        img_pad=s(10)
        d.rectangle([bx+img_pad,cy+img_pad,bx+card_w2-img_pad,cy+card_h2-img_pad],
                    fill=ds["bg_strip"] if ds["name"]=="Gray" else ds["bg_sidebar"])
        iw=twf(d,"[ 화면 ]",FS["xs"],"regular")
        d.text((bx+(card_w2-iw)//2,cy+card_h2//2-thf(d,"A",FS["xs"],"regular")//2),
               "[ 화면 ]",font=F(FS["xs"],"regular"),fill=C(ds,"meta"))

        # 캡션
        cap_y=cy+card_h2+s(12)
        # 번호+제목 (같은 줄)
        if num:
            full=f"{num}  {ctitle}"
        else:
            full=ctitle
        putf(d,bx,cap_y,full,FS["sm"],"bold",C(ds,"h3"))
        cap_y+=int(thf(d,"A",FS["sm"],"bold")*1.4)+s(2)
        # 설명
        for line in cdesc.split("\n"):
            putf(d,bx,cap_y,line,FS["xs"],"regular",C(ds,"body"))
            cap_y+=int(thf(d,line,FS["xs"],"regular")*1.65)

    return img

# ════════════════════════════════════════════════════════════════
# SLIDE 06 — 참가자 인용 행 + Lesson Learn (NEW)
# 레퍼런스: Usability Test / 좌측 4행 인용, 우측 하단 텍스트
# ════════════════════════════════════════════════════════════════
def slide_06(ds):
    img=Image.new("RGB",(W,H),ds["bg"]); d=ImageDraw.Draw(img)
    footer(d,ds)

    # ── 상단 2컬럼 헤더 (좌: 타이틀, 우: lesson learn 라벨) ──
    hx,hy=MARGIN,s(44)
    # 좌측
    putf(d,hx,hy,"Chapter 01 · Feedback",FS["category"],"regular",C(ds,"category"))
    hy+=thf(d,"A",FS["category"],"regular")+s(8)
    putf(d,hx,hy,"수강생 반응",FS["h1"],"bold",C(ds,"h1"))
    hy+=int(thf(d,"A",FS["h1"],"bold")*1.4)
    put_wrapf(d,hx,hy,"클로드 코드 실습 후\n4명의 반응을 수집했습니다.",
              FS["sm"],"regular",C(ds,"body"),W//2-MARGIN,lh=1.65)

    # 우측 — Lesson Learn 라벨
    rx=W//2
    putf(d,rx,s(44),"Lesson Learn",FS["category"],"regular",C(ds,"category"))
    putf(d,rx,s(44)+thf(d,"A",FS["category"],"regular")+s(8),
         "'직접 해봐야 안다'",FS["h1"],"bold",C(ds,"h1"))

    hrule(d,MARGIN,s(130),W-MARGIN*2,ds["border"])

    # ── 참가자 4행 ──
    AVATAR_W=s(72); AVATAR_H=s(72)
    NAME_W=s(220); META_COL_W=s(260); QUOTE_X=MARGIN+AVATAR_W+s(20)+NAME_W+s(20)+META_COL_W+s(20)
    QUOTE_W=W//2-QUOTE_X-s(10)
    ROW_H2=s(148)
    participants=[
        ("수강생 A","5년차 데이터 분석가",
         "파일을 직접 열어서 분석까지 해주는 게 신기했어요. 처음에 반신반의했는데 실제로 되니까 놀랐습니다."),
        ("수강생 B","UX 리서처",
         "에이전트 루프 개념을 배우고 나니 왜 이게 강력한지 이해됐어요. 명령 한 줄로 반복 작업이 끝나네요."),
        ("수강생 C","3년차 마케터",
         "클로드엠디 파일 하나로 매번 설명 안 해도 되는 게 제일 편했어요. 실무에 바로 쓸 수 있을 것 같아요."),
        ("수강생 D","기획자",
         "오류가 나도 스스로 고치는 걸 보고 깜짝 놀랐어요. AI가 일을 한다는 게 체감됐습니다."),
    ]

    BASE_Y=s(148)
    for i,(name,meta,quote) in enumerate(participants):
        ry=BASE_Y+i*ROW_H2

        # 아바타 원 (회색 placeholder)
        ax,ay=MARGIN,ry+ROW_H2//2-AVATAR_H//2
        d.ellipse([ax,ay,ax+AVATAR_W,ay+AVATAR_H],
                  fill=ds["bg_card"],outline=ds["border"],width=s(2))
        iw=twf(d,name[0],FS["h3"],"bold")
        d.text((ax+(AVATAR_W-iw)//2,ay+(AVATAR_H-thf(d,name[0],FS["h3"],"bold"))//2),
               name[0],font=F(FS["h3"],"bold"),fill=C(ds,"meta"))

        # 이름
        nx=MARGIN+AVATAR_W+s(20)
        putf(d,nx,ry+s(24),name,FS["h3"],"semibold",C(ds,"h3"))
        # 메타 (직업) — xs Regular #888
        putf(d,nx,ry+s(24)+thf(d,"A",FS["h3"],"semibold")+s(8),
             meta,FS["xs"],"regular",C(ds,"meta"))

        # 인용 텍스트
        qx=nx+NAME_W+s(20)
        qw=W//2-qx-s(16)
        put_wrapf(d,qx,ry+s(20),quote,FS["body"],"regular",C(ds,"body"),qw,lh=1.72)

        # 행 구분선 (마지막 행 제외)
        if i<len(participants)-1:
            hrule(d,MARGIN,ry+ROW_H2-s(1),W//2-MARGIN,ds["border"])

    # ── 우측 하단 — Lesson Learn 본문 ──
    ll_x=W//2+s(40)
    ll_y=H//2
    ll_w=W-ll_x-MARGIN
    lesson=[
        "실습을 진행하면서 '직접 해봐야 느낀다'는 것을 확인했습니다.",
        "에이전트가 실제로 파일을 열고 코드를 실행하는 것을 보고 나서야 그 강력함을 체감합니다.",
    ]
    for i,para in enumerate(lesson):
        ll_y=put_wrapf(d,ll_x,ll_y,para,FS["sm"],"regular",C(ds,"body"),ll_w,lh=1.72)
        if i<len(lesson)-1: ll_y+=s(20)

    return img

# ── 생성 실행 ──────────────────────────────────────────────────
for key,ds in DESIGN_SYSTEMS.items():
    out=os.path.join(OUT,key); os.makedirs(out,exist_ok=True)
    print(f"\n[{ds['name']}]")
    slides=[("01_compare",slide_01),("02_process",slide_02),("03_tools",slide_03),
            ("04_ps_table",slide_04),("05_screenshot",slide_05),("06_quotes",slide_06)]
    for slug,fn in slides:
        try:
            img=fn(ds)
            p=os.path.join(out,f"{slug}.png"); img.save(p)
            print(f"  ✓ {slug}.png")
        except Exception as e:
            print(f"  ✗ {slug}: {e}")
print("\n완료")
