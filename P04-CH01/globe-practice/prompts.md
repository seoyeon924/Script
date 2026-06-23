# 3D Globe 실습 — 단계별 정밀 프롬프트

각 단계를 Claude Code에 붙여넣고, 브라우저 확인 후 다음 단계로 넘어가세요.
완성 예시: https://migrationtrack.netlify.app/

---

## Step 1 — 지구본 뼈대

```
Three.js r128 + GSAP 3.12.2로 3D 지구본을 만들어줘. index.html 하나로.

CONFIG 객체를 먼저 정의해:
var CONFIG = {
  globeRadius: 65,
  arcDivisions: 12,
  arcAnimSpeed: 0.04,
  autoRotateSpeed: 0.001,
  cameraZ: 250
};

지구본 구성:
- SphereGeometry(CONFIG.globeRadius, 48, 48)
- 텍스처: https://cdn.jsdelivr.net/gh/mrdoob/three.js@r128/examples/textures/planets/earth_atmos_2048.jpg
  THREE.TextureLoader()로 로드
- 전면 mesh(FrontSide): 텍스처 적용, transparent:false, opacity:1
- 후면 mesh(BackSide): 동일 텍스처, color:#111111, transparent:true, opacity:0.3

카메라:
- PerspectiveCamera(45, window.innerWidth/innerHeight, 1, 2000)
- camera.position.z = CONFIG.cameraZ

렌더러:
- WebGLRenderer({antialias:false, alpha:false, powerPreference:'high-performance'})
- setClearColor(0x000000)
- setPixelRatio(window.devicePixelRatio)
- setSize(window.innerWidth, window.innerHeight)

마우스 드래그 회전:
- mousedown → isDragging=true, lastX/lastY 저장
- mousemove → isDragging일 때 deltaX/deltaY로 earthObject.rotation.y/x 변경 (감도 0.005)
- mouseup/mouseleave → isDragging=false

자동 회전:
- 드래그 중이 아닐 때 animate()에서 earthObject.rotation.y += CONFIG.autoRotateSpeed

window resize 대응:
- camera.aspect 업데이트, renderer.setSize 재호출
```

---

## Step 2 — 아크 데이터 연결

```
unhcr_data.csv를 로드해서 나라 간 이동 아크를 추가해줘.

CSV 파싱:
async function loadUNHCRData():
- fetch('unhcr_data.csv') → text → split('\n')
- 헤더(lines[0]) 스킵, lines[1]부터 파싱
- 각 줄을 parseCSVLine(line)으로 파싱 (쉼표+큰따옴표 처리하는 함수 직접 구현)
- fields[0]=Year, fields[3]=Country of Asylum ISO, fields[4]=Country of Origin ISO
  fields[5]=Refugees, fields[6]=Asylum-seekers
- currentYear = 2025로 필터: year !== currentYear → skip
- total = parseInt(fields[5])||0 + parseInt(fields[6])||0
- total < 100 → skip (소규모 흐름 제외)
- originISO === asylumISO → skip (내부 이동 제외)

COUNTRY_COORDS 객체:
각 ISO 코드별 {lat, lng, name} 정의 (200개 이상 국가).
COUNTRY_COORDS에 없는 ISO는 skip.
주요 국가 예시:
  SYR:{lat:34.8,lng:38.9,name:'Syria'},
  VEN:{lat:6.4,lng:-66.5,name:'Venezuela'},
  AFG:{lat:33.9,lng:67.7,name:'Afghanistan'},
  UKR:{lat:48.4,lng:31.2,name:'Ukraine'},
  SDN:{lat:12.9,lng:30.2,name:'Sudan'},
  MMR:{lat:21.9,lng:95.9,name:'Myanmar'}
  (나머지 국가도 모두 채워줘)

flowsByOrigin 구조:
if (!flowsByOrigin[originISO]) flowsByOrigin[originISO] = {total:0, destinations:{}};
flowsByOrigin[originISO].total += total;
flowsByOrigin[originISO].destinations[asylumISO] = (flowsByOrigin[originISO].destinations[asylumISO]||0) + total;

latLngToVec3(lat, lng, r, h):
  phi = (90-lat) * Math.PI/180
  theta = (lng+180) * Math.PI/180
  rad = r + (h||0)
  return new THREE.Vector3(
    -rad * Math.sin(phi) * Math.cos(theta),
     rad * Math.cos(phi),
     rad * Math.sin(phi) * Math.sin(theta)
  )

아크 생성 (createArcs()):
flowsByOrigin 순회 → 각 destination으로 아크:
  start = latLngToVec3(sLat, sLng, CONFIG.globeRadius, 0.5)
  end   = latLngToVec3(eLat, eLng, CONFIG.globeRadius, 0.5)
  dist  = start.distanceTo(end)
  h  = 1 + dist * 0.0065
  h2 = 1 + dist * 0.0065 * 0.5
  mid   = new THREE.Vector3().addVectors(start,end).normalize().multiplyScalar(CONFIG.globeRadius * h)
  ctrl1 = new THREE.Vector3().addVectors(start,mid).normalize().multiplyScalar(CONFIG.globeRadius * h2)
  ctrl2 = new THREE.Vector3().addVectors(mid,end).normalize().multiplyScalar(CONFIG.globeRadius * h2)
  curve = new THREE.CubicBezierCurve3(start, ctrl1, ctrl2, end)
  pts   = curve.getPoints(CONFIG.arcDivisions)

아크 Geometry:
- BufferGeometry + LineSegments (TubeGeometry 쓰지 말 것)
- vertexColors:true로 그라디언트
- 출발색 rgb(255,51,51), 도착색 rgb(0,229,255)
- 총 난민 수(total) 비례로 linewidth 조정

mesh.userData = {iso: originISO, country: originISO}
arcSnakeObject.add(mesh)
arcsByCountry[originISO] = mesh
```

---

## Step 3 — 디자인 토큰 + 비주얼 효과

```
아래 디자인 토큰 기반으로 비주얼을 완성해줘.

색상 토큰:
var colorPrimary = '#00CCFF';
var colorHighlight = '#FF1313';

배경:
body { background: radial-gradient(ellipse at center, #0d1a2d 0%, #0a0a12 60%, #000 100%); }

지구 glow 레이어 3개 (안쪽→바깥쪽):
- SphereGeometry(CONFIG.globeRadius * 1.06, 48, 48) — 가장 안쪽 glow
- SphereGeometry(CONFIG.globeRadius * 1.15, 48, 48) — 중간 glow
- SphereGeometry(CONFIG.globeRadius * 1.25, 48, 48) — 외곽 glow
각각 MeshBasicMaterial({transparent:true, side:THREE.BackSide}), 색상 #00CCFF, opacity 점점 낮게

GLSL 별 파티클 셰이더:
- vertex shader: attribute float alpha → varying vAlpha 전달
- fragment shader: uniform sampler2D texture (원형 마스크), vAlpha로 투명도
- 별 3,000개, 구 반경 800~1200 랜덤 배치
- PointsMaterial 대신 ShaderMaterial 사용

아크 대시 애니메이션:
- BufferGeometry에 drawRange를 매 프레임 업데이트해서 아크가 흘러가는 효과
- CONFIG.arcAnimSpeed(0.04) 속도로 drawCount 증가, 끝에 도달하면 리셋
- 아크별로 offset을 다르게 줘서 동시에 흐르지 않도록
```

---

## Step 4 — 인트로 오버레이 + 검색 필터

```
1. 인트로 오버레이 (div#intro-overlay):
   - position:fixed; inset:0; z-index:1000
   - background: radial-gradient(circle at center, rgba(5,10,18,0.5) 0%, rgba(0,0,0,0.92) 70%)
   - 폰트: Google Fonts 'Michroma' (sans-serif)
   - 내부 .intro-card (max-width:760px, text-align:center):
     · .intro-title: "MIGRATION ATLAS" (Michroma, 42px, letter-spacing:3px, uppercase)
     · .intro-subtitle: "An interactive visualization of global displacement journeys"
     · .intro-description: "Explore how forced migration flows reshape our world."
     · 버튼 id=introStartButton: "CLICK TO START"
   - 버튼 클릭 또는 canvas 클릭 시: overlay에 .hidden 클래스 추가
     .hidden { opacity:0; visibility:hidden; pointer-events:none; transition:0.8s }

2. 국가 검색 필터 (데이터 로드 완료 후 실행):

   countryList 구성 (updateCountryFilter() 안에서):
   - flowsByOrigin을 total 내림차순 정렬 → 상위 30개
   - countryList = [{iso:'all', name:'ALL REGIONS'}]
   - topOrigins.forEach → iso 소문자, name = COUNTRY_COORDS[iso].name.toUpperCase()
   - countryList.push({iso, name})

   setupCountrySearch():
   - input#countrySearch, div#searchDropdown
   - focus/input 이벤트 → showSearchResults(query)
   - blur → 200ms setTimeout 후 dropdown 숨김
   - Enter → 첫 번째 항목 선택, Escape → dropdown 닫기
   - 초기값: input.value = 'ALL REGIONS'

   showSearchResults(query):
   - countryList에서 name.includes(query.toUpperCase()) 필터
   - .search-item div 목록 dropdown에 렌더
   - 클릭 시 input.value = item.name, filterArcsByCountry(item.iso)

   filterArcsByCountry(countryISO):
   - currentFilterISO = countryISO ? countryISO.toUpperCase() : 'ALL'
   - arcSnakeObject.children.forEach:
     · meshISO = mesh.userData.iso || mesh.userData.country (대문자)
     · currentFilterISO === 'ALL' → mesh.visible = true
     · 그 외 → mesh.visible = (meshISO === currentFilterISO)
```

---

## Step 5 — 모바일

```
터치 드래그 회전 지원 추가. canvas 반응형으로.

touchstart → 드래그 시작, lastX/lastY 저장
touchmove  → deltaX/deltaY로 earthObject.rotation.y/x 변경 (마우스와 동일 감도)
touchend   → isDragging=false

canvas / renderer: 100vw × 100vh, overflow hidden
window resize: camera.aspect, camera.updateProjectionMatrix(), renderer.setSize() 재호출
```

---

## 완성본 참고

- 라이브: https://migrationtrack.netlify.app/
- 코드: https://github.com/seoyeon924/globe
