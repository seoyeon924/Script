# 3D Globe 실습

데이터 파일: `unhcr_data.csv` (UNHCR 난민 데이터, 35,472행)
※ 컬럼명에 공백 포함 — 코드에서 반드시 `data["Country of Origin ISO"]` 형태로 접근할 것 (Origin ISO 아님)
완성 예시: https://github.com/seoyeon924/globe

> ⚠️ **반드시 로컬 서버로 실행** — `file://`로 열면 CSV 로딩이 차단되어 아크가 표시되지 않음
> ```
> python3 -m http.server 8080
> ```
> 실행 후 http://localhost:8080 으로 접속

---

## Step 1 — 지구본 뼈대

```
Three.js r128 + GSAP 3.12.2로 3D 지구본 만들어줘.
텍스처: https://cdn.jsdelivr.net/gh/mrdoob/three.js@r128/examples/textures/planets/earth_atmos_2048.jpg
SphereGeometry(1, 64, 64), WebGLRenderer, PerspectiveCamera.
마우스 드래그로 회전 가능하게. index.html 하나로.
```

---

## Step 2 — 아크 데이터 연결

```
unhcr_data.csv 로드해서 아크 추가해줘.
Origin ISO → Asylum ISO 방향으로 CubicBezierCurve3 곡선 아크.
높이: dist * 0.0065 비례 동적 계산. Refugees 수에 비례해서 아크 굵기 조정.
출발 빨강(0xff3333) → 도착 시안(0x00E5FF) 그라디언트.
```

---

## Step 3 — 디자인 토큰 적용

```
아래 디자인 토큰으로 스타일 통일해줘.
배경: radial-gradient(#0d1a2d 0%, #0a0a12 60%, #000 100%)
강조색: #00CCFF
아크: rgba(0,204,255,0.7) → rgba(255,100,100,0.7)
glow: rgba(0,204,255,0.15)
GLSL 파티클 셰이더로 별 추가. 지구 대기 glow 레이어 추가.
아크는 흐르는 대시 애니메이션으로.
```

---

## Step 4 — 인트로 오버레이 + 검색 필터

```
1. 인트로 오버레이 추가 (div#intro-overlay, 전체 화면 덮개).
   내용: 제목 "Migration Atlas", 부제목 "An interactive visualization of global displacement journeys",
   설명 "Explore how forced migration flows reshape our world.",
   버튼 "Click to start" (id=introStartButton).
   버튼 클릭 또는 화면 클릭 시 오버레이 숨김(opacity:0, visibility:hidden).

2. 상단에 국가명 검색 필터 UI 추가.
   input#countrySearch (placeholder: "Search country...") + div#searchDropdown.
   데이터 로드 완료 후 flowsByOrigin에서 상위 30개 출발국을 countryList 배열로 구성.
   국가명은 COUNTRY_COORDS 객체에서 ISO3 코드로 lookup (없으면 ISO 코드 그대로 표시).
   
   setupCountrySearch():
   - input focus/input 이벤트 → showSearchResults(query) 호출
   - blur 이벤트 → 200ms 후 dropdown 닫기
   - Enter → 첫 번째 결과 선택, Escape → dropdown 닫기
   
   showSearchResults(query):
   - countryList에서 query 포함 항목 필터링
   - dropdown에 .search-item div 목록 렌더링
   - 클릭 시 countrySearch.value = 국가명, filterArcsByCountry(iso) 호출
   
   filterArcsByCountry(iso):
   - iso='all' → 모든 arc mesh visible=true
   - iso 지정 → mesh.userData.iso === iso.toUpperCase()인 것만 visible=true, 나머지 false
```

---

## Step 5 — 모바일

```
터치 드래그 회전 지원 추가. canvas 반응형으로.
```
