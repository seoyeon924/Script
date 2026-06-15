# Avengers Network Graph 실습

데이터 파일: `avengers_network_data.csv` (80행)
컬럼: Source, Target, Strength, Type, Source_Group, Source_Importance, Target_Group, Target_Importance
※ Source/Target 값은 코드에서 snake_case ID로 변환 — `"Iron Man"` → `"iron_man"` (toLowerCase + 공백→언더스코어)
완성 예시: https://avengers-network.netlify.app

> ⚠️ **반드시 로컬 서버로 실행** — `file://`로 열면 CSV 로딩이 차단되어 데이터가 표시되지 않음
> ```
> python3 -m http.server 8080
> ```
> 실행 후 http://localhost:8080 으로 접속

---

## Step 1 — 원형 배치 기초

```
D3.js v7으로 어벤져스 캐릭터 네트워크 만들어줘.
데이터: avengers_network_data.csv

노드 ID: Source/Target 컬럼 값을 toLowerCase() + 공백→언더스코어로 변환. 예: "Iron Man" → "iron_man"

레이아웃: Force Simulation 사용하지 말 것.
모든 노드를 원 위에 고정 배치 (fixed circular layout).
그룹 정렬 순서: Avengers → Guardians → Asgardians → Wakanda → Mystic Arts → Black Order → Villain → Supporting
같은 그룹 안에서는 Source_Importance 내림차순.
초기 선택 노드: thanos (항상 왼쪽 9시 방향 = Math.PI 각도에 위치).

calculateLayout(selId) 함수:
- padding = Math.min(W,H)*0.16
- R = (H/2) - padding (landscape 기준)
- cx = Math.max(W*0.2 + R, padding+R)
- 선택 노드를 기준으로 나머지 노드를 상대 인덱스(relIdx)로 배치
- angle = Math.PI + relIdx * slotAngle (slotAngle = 2π/N)
- 선택되지 않은 연결 노드: 반지름 안쪽에 큐빅 베지어 곡선 엣지

노드: 모든 노드 동일 크기 원(r = min(W,H)*0.013), 그룹별 구분색.
엣지: 두 노드 중심 간 cubic bezier 곡선, 중심 방향 곡률.
index.html 하나로. W=window.innerWidth, H=window.innerHeight.
```

---

## Step 2 — 디자인

```
1. OGL WebGL 갤럭시 배경 추가.
   CDN: https://esm.sh/ogl@1.0.8 (type="module"로 로드)
   별 4레이어(NUM_LAYER=4.0), 성운(purple #350555 / blue #081072 / gold #804010 / pink #720020),
   마우스 반응(uMouseRepulsion=true, uRepulsionStrength=2), 트윙클(uTwinkleIntensity=0.3),
   자동 회전(uRotationSpeed=0.05). 배경 canvas: position:fixed, top:0, left:0, z-index:-1.
   별은 순수 흰색. 배경은 검정(vec3(0.0)).

2. 엣지 색상 (Type 컬럼 기준):
   ally: #00c8ff  |  enemy: #ff2020  |  romantic: #c040ff  |  family: #c0c8d0

   SVG defs에 makeLineGlow(id, color, stdDev, opacity) 함수로 glow 필터 생성:
   feGaussianBlur(stdDev, result=blur1)
   → feFlood(color, opacity, result=color1)
   → feComposite(in=color1, in2=blur1, operator=in, result=glow1)
   → feGaussianBlur(stdDev*0.4, result=blur2)
   → feMerge(glow1 + blur2 + SourceGraphic)
   filter x="-60%" y="-60%" width="220%" height="220%"

   호출:
   makeLineGlow("glow-line-ally",     "#00c8ff", 7, 0.55)
   makeLineGlow("glow-line-enemy",    "#ff2020", 8, 0.60)
   makeLineGlow("glow-line-romantic", "#c040ff", 7, 0.55)
   makeLineGlow("glow-line-family",   "#c0c8d0", 6, 0.50)

3. 폰트: Google Fonts Cinzel (400/500/600/700) + Inter (300/400/500/600).
   캐릭터 이름 레이블: Cinzel, uppercase, letter-spacing 0.1em.

4. 전체 배경: #0a0a0f. 화면 가장자리 vignette (position:fixed, radial-gradient 검정 테두리).
```

---

## Step 3 — 얼굴 이미지 + 클릭 스핀

```
얼굴 이미지 및 클릭 스핀 인터랙션 추가.

faceImages 객체 (key = Step 1의 snake_case ID):
const faceImages = {
  "thanos":           "https://www.fxguide.com/wp-content/uploads/2019/05/thanos3.jpg",
  "gamora":           "https://upload.wikimedia.org/wikipedia/en/5/54/Zoe_Saldana_as_Gamora.jpeg",
  "iron_man":         "https://upload.wikimedia.org/wikipedia/en/4/47/Robert_Downey_Jr_as_Tony_Stark.jpg",
  "thor":             "https://upload.wikimedia.org/wikipedia/en/3/3c/Chris_Hemsworth_as_Thor.jpg",
  "doctor_strange":   "https://upload.wikimedia.org/wikipedia/en/1/18/Benedict_Cumberbatch_as_Doctor_Strange.jpeg",
  "star_lord":        "https://upload.wikimedia.org/wikipedia/en/b/b2/Chris_Pratt_as_Peter_Quill.jpeg",
  "vision":           "https://upload.wikimedia.org/wikipedia/en/f/fc/Paul_Bettany_as_Vision.jpg",
  "scarlet_witch":    "https://upload.wikimedia.org/wikipedia/en/d/d9/Elizabeth_Olsen_as_Wanda_Maximoff.jpg",
  "hulk":             "https://upload.wikimedia.org/wikipedia/en/7/7b/Mark_Ruffalo_as_Bruce_Banner.jpg",
  "spider_man":       "https://upload.wikimedia.org/wikipedia/en/0/0f/Tom_Holland_as_Spider-Man.jpg",
  "captain_america":  "https://upload.wikimedia.org/wikipedia/en/6/6b/Chris_Evans_as_Steve_Rogers_Captain_America.jpg",
  "rocket":           "https://upload.wikimedia.org/wikipedia/en/f/fc/Rocket_Raccoon_singing_in_a_spaceship%2C_from_Guardians_of_the_Galaxy_Vol_3%2C_2023.png",
  "black_widow":      "https://upload.wikimedia.org/wikipedia/en/f/f6/Scarlett_Johansson_as_Black_Widow.jpg",
  "drax":             "https://upload.wikimedia.org/wikipedia/en/3/3d/Dave_Bautista_as_Drax.jpg",
  "mantis":           "https://static.wikia.nocookie.net/heroes-and-villain/images/d/d5/Profile_-_Mantis.png/revision/latest?cb=20200422010329",
  "ebony_maw":        "https://upload.wikimedia.org/wikipedia/en/9/9d/Ebony_Maw.jpg",
  "proxima_midnight": "https://static.wikia.nocookie.net/marvelcinematicuniverse/images/7/7e/Proxima_Midnight_Infobox.jpg/revision/latest?cb=20210525191820",
  "cull_obsidian":    "https://static.wikia.nocookie.net/marvelcinematicuniverse/images/f/f5/Cull_Obsidian.JPG/revision/latest?cb=20210525191742",
  "corvus_glaive":    "https://static.wikia.nocookie.net/marvelcinematicuniverse/images/0/0f/Corvus_Glaive_Infobox.png/revision/latest?cb=20180604193419",
  "black_panther":    "https://upload.wikimedia.org/wikipedia/en/1/1a/Chadwick_Boseman_as_T%27Challa.jpg",
  "groot":            "https://static.wikia.nocookie.net/marvelmovies/images/4/4c/GOTG_Groot_Poster.jpg/revision/latest?cb=20160512212218",
  "nebula":           "https://upload.wikimedia.org/wikipedia/en/0/0c/Karen_Gillan_as_Nebula.png",
  "okoye":            "https://static.wikia.nocookie.net/disney/images/6/6f/Okoye_-_Profile.png/revision/latest?cb=20230224222454",
  "loki":             "https://static0.srcdn.com/wordpress/wp-content/uploads/2022/06/Tom-Hiddleston-as-Loki.jpg",
  "war_machine":      "https://static.wikia.nocookie.net/marvelcinematicuniverse/images/7/77/WarMachine-EndgameProfile.jpg/revision/latest?cb=20231025163822",
  "eitri":            "https://static.wikia.nocookie.net/marvelcinematicuniverse/images/a/ac/Eitri.png/revision/latest?cb=20220205165648",
  "wong":             "https://upload.wikimedia.org/wikipedia/en/d/d7/Benedict_Wong_as_Wong.jpg",
  "falcon":           "https://static.wikia.nocookie.net/ultimatepopculture/images/d/d6/Falcon_MCU.png/revision/latest?cb=20201230161754",
  "winter_soldier":   "https://upload.wikimedia.org/wikipedia/en/4/4b/Sebastian_Stan_as_Bucky_Barnes.jpg",
  "pepper_potts":     "https://upload.wikimedia.org/wikipedia/en/9/92/Gwyneth_Paltrow_as_Pepper_Potts.jpg",
  "red_skull":        "https://static.wikia.nocookie.net/marvelcinematicuniverse/images/6/6d/Red_Skull_Infobox.png/revision/latest?cb=20190808103105",
  "shuri":            "https://upload.wikimedia.org/wikipedia/en/5/5b/Letitia_Wright_as_Shuri_in_Black_Panther_Wakanda_Forever_poster.jpg",
  "mbaku":            "https://static.wikia.nocookie.net/heroes-and-villain/images/5/59/MCU_Man-Ape.jpg/revision/latest?cb=20181127195837",
  "thaddeus_ross":    "https://static.wikia.nocookie.net/characters-in-fiction/images/f/f2/Thaddeus_Ross_%28Earth-199999%29_from_Captain_America-_Civil_War_001.jpg/revision/latest?cb=20200414221123",
  "nick_fury":        "https://static.wikia.nocookie.net/marvelcinematicuniverse/images/e/e4/Nick_Fury_Profile.png/revision/latest?cb=20240802141551",
  "maria_hill":       "https://static.wikia.nocookie.net/marvelcinematicuniverse/images/f/f4/Maria_Hill_Infobox.jpg/revision/latest?cb=20250203210426",
  "heimdall":         "https://static.wikia.nocookie.net/marvelcinematicuniverse/images/e/ea/Heimdall_Infobox.jpg/revision/latest?cb=20250203022212",
  "collector":        "https://static.wikia.nocookie.net/marvelcinematicuniverse/images/d/df/CollectorGotgTextlessPoster.jpg/revision/latest?cb=20231022154628",
  "ned_leeds":        "https://static.wikia.nocookie.net/marvelcinematicuniverse/images/e/e8/Ned_Leeds_Infobox.jpg/revision/latest?cb=20211217044601"
};
const facePositions = { "spider_man": "top center", "star_lord": "top center" };

노드에 얼굴 이미지 적용:
- SVG foreignObject + xhtml:div + xhtml:img
- border-radius:50%, overflow:hidden, object-fit:cover
- object-position: facePositions[id] || 'center'
- 이미지 로딩 실패 시 이니셜 텍스트 폴백

클릭 스핀 인터랙션 (spinTo(targetId)):
- 노드 클릭 시 isTransitioning 체크 후 spinTo 실행
- 회전 방향: 최단 경로 (fwd = (targetIdx-curIdx+N)%N, bwd = N-fwd, 더 작은 쪽)
- 소요 시간: Math.min(1200, 300 + steps * 40) ms
- 이징: easeOutQuint = t => 1 - Math.pow(1-t, 5)
- mainGroup 전체를 SVG rotate(deg, cx, cy)로 회전 (원의 크기 유지)
- 스핀 중: 매 프레임 9시 방향(Math.PI 라디안)에 가장 가까운 노드 찾아 스포트라이트 얼굴 교체
- 스포트라이트: 앵커 위치(선택 노드 좌표)에 bigR=min(W,H)*0.038 원 + 얼굴 이미지
  SVG 최상단에 동적 append (mainGroup 바깥)
- 스핀 완료 후:
  1. mainGroup rotate 제거, selectedId = targetId로 업데이트
  2. 스포트라이트 100ms fade out 후 remove
  3. 연결 엣지 dashoffset 애니메이션으로 뻗어나옴 (650ms, easeQuadOut)
  4. 엣지 opacity는 strength 기반 동적 계산:
     - 선택 노드 연결 엣지: 0.5 + Math.pow(d.strength/10, 2) * 2 (선 굵기도 동일 공식)
     - 비연결 엣지: opacity 0.03 (거의 투명)
     - 초기 상태(노드 미선택): 0.02 + Math.pow(d.strength/10, 3.5) * 5
```

---

## Step 4 — 필터 패널 + 정보 카드

```
우측 고정 필터 패널 추가 (position:fixed, right:16px, top:50%, transform:translateY(-50%)).

HTML 구조:
<div id="filters">
  <div class="filter-label">RELATIONS</div>
  <button class="filter-btn rel-btn active" data-type="all">All</button>
  <button class="filter-btn rel-btn" data-type="ally">Alliance</button>
  <button class="filter-btn rel-btn" data-type="enemy">Conflict</button>
  <button class="filter-btn rel-btn" data-type="romantic">Romance</button>
  <button class="filter-btn rel-btn" data-type="family">Family</button>
  <div class="filter-divider"></div>
  <div class="filter-label">GROUPS</div>
  <button class="filter-btn group-btn active" data-group="all">All</button>
  <button class="filter-btn group-btn" data-group="Avengers">Avengers</button>
  <button class="filter-btn group-btn" data-group="Guardians">Guardians</button>
  <button class="filter-btn group-btn" data-group="Asgardians">Asgardians</button>
  <button class="filter-btn group-btn" data-group="Wakanda">Wakanda</button>
  <button class="filter-btn group-btn" data-group="Mystic Arts">Mystic Arts</button>
  <button class="filter-btn group-btn" data-group="Black Order">Black Order</button>
  <button class="filter-btn group-btn" data-group="Villain">Villain</button>
  <button class="filter-btn group-btn" data-group="Supporting">Supporting</button>
</div>

getFilteredNodeIds(filterType, groupFilter):
- filterType='all' → 전체 노드
- filterType 지정 → 해당 type 엣지에 연결된 노드만
- groupFilter 지정 → 해당 그룹 노드와 교집합

필터 클릭 시:
- activeFilter / activeGroupFilter 업데이트
- calculateLayout(selectedId) 재실행
- visible 노드만 원에 균등 배치, hidden 노드는 center(cx, cy)로 collapse
- 선택 상태 초기화 (selectedId='thanos', 스포트라이트 숨김)

캐릭터 정보 카드 (#selected-info):
- 선택 노드 이름(Cinzel, 대형) + 그룹명
- landscape: 선택 노드 오른쪽 (left = selPos.x + selR + 16, top = selPos.y - selR*0.3)
- portrait: 원 상단 (left = cx, top = cy - R - 24, transform: translate(-50%, -100%))
```

---

## Step 5 — Tableau Extension (선택)

```
Tableau Extensions API 추가해줘.
API 스크립트: https://extensionsdk.azureedge.net/1.10/tableau.extensions.1.latest.js
Tableau 워크시트에서 Source/Target 필드 받아서 해당 캐릭터 관계만 필터링.
manifest 파일(.trex)도 만들어줘. source-location URL은 http://localhost:8080으로.
```
