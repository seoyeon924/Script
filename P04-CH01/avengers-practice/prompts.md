# Avengers Network — 정밀 프롬프트 참조

CLAUDE.md의 각 Step을 정확하게 재현하기 위한 코드 기반 상세 스펙.
시행착오를 줄이고 완성 예시와 동일한 결과를 얻고 싶을 때 사용하세요.

완성 예시: https://avengers-network.netlify.app

---

## Step 1 — 기초 네트워크

```
D3.js v7 CDN으로 avengers_network_data.csv 를 로드해서 Force Simulation 네트워크를 만들어줘.
컬럼: Source, Target, Strength, Type, Source_Group, Source_Importance, Target_Group, Target_Importance
노드 = Source+Target 유니크 값, 링크 = 각 행.
파일 하나(index.html)로 완성. 외부 라이브러리는 CDN만 사용.
```

---

## Step 2 — 디자인

```
아래 디자인 스펙으로 index.html을 업데이트해줘.

배경:
- <img id="bg"> 로 background.jpg 를 position:fixed, inset:0, z-index:0, object-fit:cover 로 깔기
- 그 위에 <canvas id="stars"> 를 position:fixed, inset:0, z-index:1 로 겹치기
- GLSL 별 파티클: WebGL vertexShader/fragmentShader 로 별 800개, 반짝임(sin(time)) 적용
- SVG는 position:relative, z-index:2

로고:
- <img src="avengers-logo2.png"> 를 좌측 상단 position:fixed, z-index:10, width:120px

노드 색상 (Source_Group 기준):
  Avengers → #e8603c
  Asgardians → #f5c518
  Guardians → #00b4d8
  Wakanda → #6aac98
  Mystic Arts → #9b5de5
  Black Order / Villain → #ef5350
  Supporting / 기타 → #aaa

노드 크기: r = 4 + Source_Importance * 2 (min 6, max 18)
링크 굵기: Strength 에 비례 (scaleLinear domain[1,10] range[0.5,4])
폰트: Google Fonts Cinzel, weight 400/700
```

---

## Step 3 공통 — 프로필 사진 · 로고 · 필터

```
아래 공통 요소를 index.html에 추가해줘.

── 프로필 사진 ──
FACE 객체: 캐릭터 이름(Source 컬럼 값) → images/ 폴더 내 로컬 파일 경로 매핑
  예: "Iron Man" → "images/iron_man.jpg"
  (images/ 폴더에 있는 파일명 기준으로 매핑)

SVG defs 안에 캐릭터별 clipPath(원형) + <image> 선언:
  <clipPath id="clip-{id}"><circle cx="0" cy="0" r="{NODE_R}"/></clipPath>
  <image href="{FACE[id]}" x="-{NODE_R}" y="-{NODE_R}" width="{NODE_R*2}" height="{NODE_R*2}"
         clip-path="url(#clip-{id})" preserveAspectRatio="xMidYMin slice"/>
이니셜 텍스트 폴백 없음 — 이미지 로딩 실패 시 해당 노드는 그냥 빈 원

── 로고 헤더 ──
avengers-logo2.png 를 position:fixed, top:16px, left:20px, width:110px, z-index:10 으로 고정

── 필터 패널 ──
우측 position:fixed, top:50%, transform:translateY(-50%), z-index:10 패널
RELATIONS 그룹: All / ally / enemy / romantic / family 버튼
GROUPS 그룹: All / Avengers / Asgardians / Guardians / Wakanda / Mystic Arts / Villain 버튼
필터 선택 시: 해당 조건을 만족하는 노드+엣지만 opacity:1, 나머지 opacity:0 + pointer-events:none
트랜지션: 모든 opacity 변화는 300ms ease 트랜지션으로 부드럽게
전체(All) 선택 시 모든 노드 복원
```

---

## Step 3(1) — Force Network

```
위 공통 요소에 추가:

드래그:
  d3.drag() — start: alphaTarget(0.3).restart(), d.fx=d.x / drag: d.fx=e.x / end: alphaTarget(0), d.fx=null

호버:
  mouseover → 연결된 노드 opacity:1, 나머지 opacity:0.1 (링크도 동일)
  mouseout → 전체 opacity:1 복원
  트랜지션: 150ms

클릭 정보 카드:
  클릭 시 position:fixed 카드에 이름(Cinzel bold 18px) + 그룹(그룹 컬러) + 연결 수 표시
  카드 위치: 클릭한 노드 좌표 기준 우측 16px, 상단 정렬

필터링:
  필터 변경 시 visible 노드 bounding box 계산
  → d3.zoom().transform 으로 해당 영역에 fit (700ms easeCubicInOut)
  전체(All) 복원 시 전체 그래프에 fit
```

---

## Step 3(2) — 360° Chord Diagram

```
위 공통 요소에 추가.
index.html의 Force Simulation을 제거하고 원형 배치로 교체.

── 레이아웃 ──
CIRCLE_R = Math.min(W, H) * 0.36
그룹 정렬 순서: Avengers → Guardians → Asgardians → Wakanda → Mystic Arts → Black Order → Villain → Supporting
같은 그룹 내에서는 Source_Importance 내림차순
baseAngle = -π/2 + 2π * i / N (균등 배치)
원 궤도 가이드: <circle r={CIRCLE_R} fill="none" stroke="rgba(255,255,255,0.07)"/>

── 노드 ──
NODE_R = 18, 모든 노드 동일 크기, 드래그 불가
stroke: none, 흰색 미광 링 rgba(255,255,255,0.18) stroke-width:1

── 엣지 ──
모든 엣지 흰색 <path>, cubic bezier (중심 방향 곡률 0.32)
  cp = 중심(CX, CY) 쪽으로 0.32 비율 이동한 두 제어점
  d = `M ${x1} ${y1} C ${cp1x} ${cp1y} ${cp2x} ${cp2y} ${x2} ${y2}`
타입별 두께/opacity:
  ally 0.7px / 0.18 | enemy 2.2px / 0.28 | romantic 1.1px / 0.22 | family 1.6px / 0.24
strength 보정: strokeWidth * (0.6 + strength * 0.04)

── Spotlight ──
9시(π) 고정. pointer-events:none. SVG 최상단 레이어.
SL_R = NODE_R * 3.2
흰 테두리 링 + <image> clipPath(원형) 으로 얼굴 표시

── 클릭 인터랙션 ──
노드 클릭 시:
1. 미선택 노드 opacity:0.30
2. 모든 엣지 opacity:0 즉시
3. Spotlight 이미지 선택 노드 얼굴로 즉시 교체
4. d3.timer(950ms, easeCubicInOut)로 currentRot 애니메이션 → 선택 노드가 π 위치
5. 스핀 중 매 프레임: getNodeAt9() → 9시 가장 가까운 노드 얼굴로 Spotlight 교체
6. 스핀 완료 → openGap() → shootLines()

openGap():
GAP = Math.asin((SL_R + NODE_R + 12) / CIRCLE_R)
선택 노드는 π 고정, 나머지 노드를 π+GAP ~ π-GAP 바깥 호에 균등 재배치
  others[i].angle = π + GAP + (i + 0.5) * (2π - 2*GAP) / others.length
420ms easeCubicOut 트랜지션

shootLines():
각 연결 엣지의 path를 "선택 노드 → 상대 노드" 방향으로 재구성
stroke-dasharray = totalLength, stroke-dashoffset: totalLength → 0 (650ms easeQuadOut)
연결 엣지 opacity: ally 0.75 / enemy 0.95 / romantic 0.80 / family 0.85
비연결 엣지: opacity 0.03

── 정보 카드 ──
left = (CX - CIRCLE_R) - SL_R - 18 - 185, top = CY - 50
width: 185px, text-align: right
이름(Cinzel bold 22px) + 그룹(그룹 컬러 14px) + "연결 수: N" (회색 13px)

── 필터링 ──
visible 노드만으로 baseAngle 재계산
  visNodes[i].baseAngle = -π/2 + 2π*i/M
600ms easeCubicInOut 트랜지션으로 노드 이동, 엣지 opacity도 트랜지션
전체(All): originalAngle 복원
필터 변경 시: currentRot=0, selectedId=null, Spotlight 숨김
```

---

## Step 4 — Tableau Extension (정밀 버전)

```
tableau-extension/ 폴더 안에 두 파일을 만들어줘.
avengers-network.html 과 manifest.trex.

─── tableau-extension/avengers-network.html ───

라이브러리:
  <script src="https://d3js.org/d3.v7.min.js"></script>
  <script src="https://extensionsdk.azureedge.net/1.latest/tableau.extensions.1.latest.js"></script>

스타일:
  html,body: margin:0, padding:0, width:100%, height:100%, background:#000, overflow:hidden
  #net: display:block, width:100vw, height:100vh
  .link: stroke-opacity:0.6
  .node circle: stroke:#fff, stroke-width:1.5px, cursor:pointer
  .node text: fill:#ccc, font-size:11px, text-anchor:middle, pointer-events:none

초기화:
  tableau.extensions.initializeAsync().then(() => {
    worksheet = tableau.extensions.worksheetContent.worksheet
    render()
    worksheet.addEventListener(tableau.TableauEventType.SummaryDataChanged, render)
  }).catch(() => {
    // 폴백: 브라우저에서 직접 열 때
    d3.csv('../avengers_network_data.csv').then(rows => renderNetwork(rows.map(...)))
  })

render() 함수:
  1) getVisualSpecificationAsync() → encMap{ source/target/strength/type → 필드명 }
     (실패해도 계속 — try/catch)
  2) getSummaryDataReaderAsync() → getAllPagesAsync() → releaseAsync()
  3) 컬럼 인덱스 결정:
     pick(encId, ...keywords):
       encMap[encId] 있으면 fieldName으로 정확히 찾기
       없으면 fieldName.toLowerCase().includes(keyword)로 추정
     iS = pick("source", "source","from","출발")
     iT = pick("target", "target","to","도착")
     iW = pick("strength", "strength","weight","value","굵기")
     iY = pick("type", "type","relation","관계")
  4) rows = data.map(r => { Source, Target, Strength:parseFloat, Type }).filter(Source && Target)
  5) renderNetwork(rows)

renderNetwork(data):
  W = window.innerWidth, H = window.innerHeight
  svg.attr("viewBox",[0,0,W,H]).selectAll("*").remove()
  data 없으면 힌트 텍스트 표시

  links = data.map(d => { source, target, strength, type })
  nodeSet = Map으로 중복 제거
  nodes = Array.from(nodeSet.values())

  linkColor: enemy→#ef5350 / romantic→#f06292 / ally→#4fc3f7 / 기타→#aaa
  wScale = d3.scaleLinear().domain([1, max(strength)]).range([1,6])

  sim = d3.forceSimulation(nodes)
    .force("link", d3.forceLink(links).id(d=>d.id).distance(120))
    .force("charge", d3.forceManyBody().strength(-300))
    .force("center", d3.forceCenter(W/2,H/2))

  link: <line class="link">, stroke=linkColor, stroke-width=wScale
  node: <g class="node">, drag 적용
    circle r=8, fill=#e8603c
    text dy=20, text=id (언더스코어→공백)

  sim.on("tick"): link x1/y1/x2/y2, node transform translate

drag():
  start: alphaTarget(0.3).restart(), d.fx=d.x, d.fy=d.y
  drag: d.fx=e.x, d.fy=e.y
  end: alphaTarget(0), d.fx=null, d.fy=null

window resize:
  if (tableau.extensions.worksheetContent) render() else loadFromCsv()

─── tableau-extension/manifest.trex ───
<?xml version="1.0" encoding="utf-8"?>
<manifest manifest-version="0.1" xmlns="http://www.tableau.com/xml/extension_manifest">
  <worksheet-extension id="com.seoyeon924.avengers-network" extension-version="1.0.0">
    <default-locale>ko_KR</default-locale>
    <name resource-id="name">Avengers Network</name>
    <description>D3.js 기반 어벤져스 캐릭터 관계 네트워크 (워크시트 Viz 확장)</description>
    <author name="seoyeon924" email="tjdus92422@gmail.com" organization="fastcampus" website="https://avengers-network.netlify.app"/>
    <min-api-version>1.12</min-api-version>
    <source-location>
      <url>http://localhost:8080/tableau-extension/avengers-network.html</url>
    </source-location>
    <permissions>
      <permission>full data</permission>
    </permissions>
    <default-settings>
      <encodings>
        <encoding id="source" />
        <encoding id="target" />
        <encoding id="strength" />
        <encoding id="type" />
      </encodings>
    </default-settings>
  </worksheet-extension>
</manifest>
```

> **Tableau에서 불러오는 법**:
> 워크시트 → 마크 카드 드롭다운 → "확장 프로그램 추가" → manifest.trex 선택
> → 인코딩 선반(source / target / strength / type)에 해당 필드를 끌어놓으면 렌더됩니다.
> ※ 대시보드 "확장 프로그램" 개체에 넣으면 에러납니다 — 반드시 워크시트 마크 카드에서 추가.
