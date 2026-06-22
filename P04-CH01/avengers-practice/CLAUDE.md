# Avengers Network Graph 실습

데이터 파일: `avengers_network_data.csv` (80행)
컬럼: Source, Target, Strength, Type, Source_Group, Source_Importance, Target_Group, Target_Importance
완성 예시: https://avengers-network.netlify.app

### 폴더에 있는 에셋 (코드에서 이 파일명 그대로 참조)

| 파일 | 용도 |
|---|---|
| `background.jpg` | 배경 이미지 (우주 배경) |
| `avengers-logo2.png` | 좌측 상단 헤더 로고 (권장) |
| `avengers-logo.png` | 로고 대체본 |

> ⚠️ **반드시 로컬 서버로 실행** — `file://`로 열면 CSV 로딩이 차단되어 데이터가 표시되지 않음
> ```
> python3 -m http.server 8080
> ```
> 실행 후 http://localhost:8080 으로 접속

---

## Step 1 — 기초 네트워크

```
D3.js v7으로 어벤져스 캐릭터 네트워크 그래프 만들어줘.
데이터: avengers_network_data.csv (Source→Target, Strength=선 굵기)
D3 Force Simulation으로 노드 배치.
```

---

## Step 2 — 디자인

```
배경: 폴더의 background.jpg를 깔고 그 위에 우주 느낌(검정 + GLSL 별 파티클) 오버레이
로고: 폴더의 avengers-logo2.png를 좌측 상단 헤더에 <img>로 삽입
노드 색상: Source_Group별로 구분 (Asgardians, Guardians, Avengers, Wakanda, Villains)
노드 크기: Source_Importance에 비례
선 굵기: Strength에 비례
폰트: Google Fonts Cinzel
```

---

## Step 3 — 인터랙션 (공통 요소)

> 아래 두 옵션 중 하나를 선택해서 실행하셔도 됩니다.패캠 강의 영상 내 프롬프트와 차이가 있는 이유는 아래 프롬프트가 시행착오를 줄인 최종버전이기 때문입니다! 이 버전 프롬프트를 사용하시면 됩니다.

**공통 요소 (두 옵션 모두 적용):**

```
프로필 사진:
- 각 캐릭터 이름을 키로 하는 FACE 객체에 Wikipedia/Wikia 이미지 URL 매핑
- SVG <image> 요소 + clipPath(원형 크롭) 사용
- preserveAspectRatio="xMidYMin slice" — 머리/얼굴이 잘리지 않도록 상단 기준 크롭
- 이미지 로딩 실패 시 이니셜 텍스트로 폴백
- 노드 내부 및 Spotlight 내부에 이니셜 텍스트(폴백 포함) 절대 표시하지 않음

어벤져스 로고(avengers-logo2.png)를 좌측 상단 헤더에 <img>로 삽입.
좌측에 색깔 범례(legend)는 표시하지 않음 — 로고만 둠.

필터링 (우측 패널, RELATIONS / GROUPS):
- 필터 선택 시 해당 노드+엣지만 남기고 나머지 opacity:0 + pointer-events:none
- 전체(All) 선택 시 모든 노드 복원
- 필터 전환 시 애니메이션 효과 — opacity/위치 변화를 트랜지션으로 부드럽게 (즉시 변경 금지)
```

---

### Step 3(1) — Force Network (거미줄 네트워크 버전)

```
위 공통 요소에 추가:

노드 드래그 가능하게.
호버 시 연결된 캐릭터만 강조, 나머지 흐리게.
클릭 시 캐릭터 이름 + 그룹 + 연결 수 표시.

필터링:
- D3 zoom transform으로 visible 노드 영역에 fit (700ms 트랜지션)
- 전체(All) 선택 시 전체 fit
```

---

### Step 3(2) — 360° Chord Diagram (원형 코드 다이어그램 버전)

```
위 공통 요소에 추가:

레이아웃:
- Force Simulation 제거, 모든 노드를 CIRCLE_R 반경의 원 위에 균등 배치
- 그룹 순서(Avengers→Guardians→Asgardians→Wakanda→Mystic Arts→Black Order→Villain→Supporting)로 정렬 후 baseAngle 할당
- 원 궤도 가이드 라인(opacity 0.07)을 SVG에 배경으로 추가

노드 스타일:
- 모든 노드 동일 크기(NODE_R=18), 드래그 불가
- 테두리(stroke) 색상 없음 — stroke:none
- 링은 흰색 미광(rgba(255,255,255,0.18))만

엣지 스타일:
- 모든 엣지 흰색, <path> 곡선(cubic bezier, 중심 방향 곡률 0.32)
- 관계 타입별 두께/불투명도:
  ally: 0.7px / 0.18  |  enemy: 2.2px / 0.28
  romantic: 1.1px / 0.22  |  family: 1.6px / 0.24
- strength 값에 따라 추가 두께 보정: width * (0.6 + strength * 0.04)

클릭 인터랙션 — 9시 Spotlight:
- 9시 방향(π 라디안) 고정 위치에 Spotlight 레이어(pointer-events:none) 별도 추가
- Spotlight은 SVG 노드 레이어 위에 렌더링(z-order 최상단)
- 노드 클릭 시:
  1. 선택 안 된 노드 opacity: 0.30
  2. 모든 엣지 즉시 숨김(opacity:0) — 스핀 완료 후 뻗어나감
  3. Spotlight에 선택 노드 얼굴 즉시 표시
  4. currentRot을 d3.timer로 애니메이션(950ms, easeCubicInOut)하여 선택 노드가 π에 정확히 위치
  5. 스핀 중: getNodeAt9()로 매 프레임 9시 가장 가까운 노드를 찾아 Spotlight 이미지 교체 → "촤르르" 효과
  6. 스핀 완료 후: 선택 노드 주변 여백 확보(openGap) → shootLines() 실행

선택 노드 주변 여백 (openGap):
- 9시 Spotlight(SL_R)가 인접 노드를 가리면 안 됨 — 메인 노드 양옆으로 빈 공간을 둬야 함
- 스핀 완료 후, 선택 노드는 π에 고정하고 나머지 visible 노드를 gap 바깥 호에 균등 재배치
  → gap 각도 ≈ (SL_R + NODE_R + 여백) / CIRCLE_R, 양옆으로 확보
  → others.forEach((d,i) => d.angle = π + GAP + (i+0.5) * (2π - 2·GAP) / others.length)
- 재배치는 짧은 트랜지션(약 420ms, easeCubicOut)으로 부드럽게

shootLines():
- 선이 뻗는 방향: 선택된 중심 노드(9시 Spotlight)에서 **시작**해 상대 노드로 뻗어나가야 함
  → 연결 엣지의 path를 항상 "선택 노드 → 상대 노드" 순서로 재구성 (선택 노드가 target이면 path를 반전)
  → dashoffset이 length→0이 되면서 선택 노드 쪽에서 그어지기 시작
- stroke-dasharray = length, stroke-dashoffset = length → 0 애니메이션(650ms, easeQuadOut)
- 연결 엣지 밝기: ally 0.75 / enemy 0.95 / romantic 0.80 / family 0.85
- 비연결 엣지: opacity 0.03

정보 카드 (#info-card):
- 캐릭터 이름(대형) + 그룹(그룹 컬러) + 연결 수
- 위치: 9시 Spotlight 왼쪽 (left = (CX - CIRCLE_R) - SL_R - 18 - cardWidth, top = CY - 50)
- text-align: right, width: 185px 고정

필터링:
- 필터 선택 시 visible 노드만으로 360° 원을 새로 구성(baseAngle 재계산)
  visNodes.forEach((d,i) => d.baseAngle = -π/2 + 2π*i/M)
- 확대/축소 없이 같은 CIRCLE_R 반경으로 재배치
- 재배치는 애니메이션으로 — 노드가 새 위치(각도)로 d3.timer/transition(약 600ms, easeCubicInOut)을 통해 부드럽게 이동, 엣지·노드 opacity도 트랜지션
- 전체(All) 선택 시 originalAngle 복원
- 필터 변경 시 currentRot=0, selectedId=null, Spotlight 숨김
```

---

## Step 4 — Tableau Extension 연결 (선택)

```
Tableau Extensions API 추가해줘.
API 스크립트: https://extensionsdk.azureedge.net/1.10/tableau.extensions.1.latest.js
Tableau 워크시트에서 Source/Target 필드 받아서 해당 캐릭터 관계만 필터링.
manifest 파일(.trex)도 만들어줘. source-location URL은 http://localhost:8080으로.
```
