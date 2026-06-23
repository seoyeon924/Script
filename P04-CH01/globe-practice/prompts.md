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

Scene 설정:
- scene.fog = new THREE.Fog(0x000000, 0, 400)

카메라:
- PerspectiveCamera(45, window.innerWidth/innerHeight, 1, 2000)
- camera.position.z = CONFIG.cameraZ

렌더러:
- WebGLRenderer({antialias:false, alpha:false, powerPreference:'high-performance'})
- setClearColor(0x050508, 1)
- setPixelRatio(Math.min(devicePixelRatio, 2))
- setSize(innerWidth, innerHeight)

지구본 구조:
- rotationObject = new THREE.Group() → scene.add
- earthObject = new THREE.Group(); earthObject.rotation.y = -90 * Math.PI/180 → rotationObject.add

지구 메시 (earthObject에 추가):
① 후면(BackSide) 메시: SphereGeometry(65, 48, 48), color:0x111111, transparent:true, opacity:0.3, depthWrite:false
② 전면(FrontSide) 메시: 같은 지오메트리, transparent:false, opacity:1.0, depthWrite:true
③ 텍스처: https://cdn.jsdelivr.net/gh/mrdoob/three.js@r128/examples/textures/planets/earth_atmos_2048.jpg
  (THREE.TextureLoader()로 로드, 두 메시에 동일하게 적용)

Phong 실드 메시 (scene에 직접 추가):
- MeshPhongMaterial({color:0x1a6680, transparent:true, blending:AdditiveBlending, opacity:0.5, depthWrite:false})
- scene에 add (rotationObject/earthObject 아님)

조명 3개 (PointLight):
- new THREE.PointLight(0x00CCFF, 1.25, 400, 2)
- 위치: (-50, 150, 75), (100, 50, 50), (0, -300, 50)

마우스 드래그 회전 (부드러운 보간):
- isMouseDown, targetRotationX=0.45, targetRotationY=65*PI/180
- mousedown → 현재 targetRotation 저장
- mousemove → targetRotationY += (mouseX - mouseXOnDown) * 0.005
- animate() 루프: rotationObject.rotation.x += (targetRotationX - rotationObject.rotation.x) * 0.1

자동 회전:
- isAutoRotate=true, 드래그 중 아닐 때: targetRotationY += CONFIG.autoRotateSpeed

터치 지원:
- touchstart/touchmove/touchend: 마우스와 동일 감도(0.005), {passive:true}

마우스 휠 줌:
- camera.position.z += e.deltaY * 0.1
- clamp: Math.max(90, Math.min(400, camera.position.z))

window resize:
- camera.aspect 업데이트, camera.updateProjectionMatrix(), renderer.setSize()

body 스타일:
- background: radial-gradient(ellipse at 30% 20%, #0d1a2d 0%, #0a0a12 35%, #050508 70%, #000 100%)
- font-family: 'Michroma', system-ui (Google Fonts import)
- text-transform: uppercase
- overflow: hidden
```

---

## Step 2 — CSV 파싱 + 아크 연결

```
unhcr_data.csv를 fetch로 로드해서 나라 간 이동 아크를 추가해줘.

CSV 파싱 (parseCSVLine 함수 직접 구현 — 큰따옴표+쉼표 처리):
function parseCSVLine(line) {
  var result=[], current='', inQuotes=false;
  for (var i=0; i<line.length; i++) {
    var c=line[i];
    if (c==='"') { inQuotes=!inQuotes; }
    else if (c===',' && !inQuotes) { result.push(current.trim()); current=''; }
    else { current+=c; }
  }
  result.push(current.trim());
  return result;
}

컬럼 인덱스:
- fields[0]=Year, fields[3]=Country of Asylum ISO, fields[4]=Country of Origin ISO
- fields[5]=Refugees, fields[6]=Asylum-seekers

loadUNHCRData() async 함수:
- currentYear = 2025로 필터: year !== currentYear → skip
- total = parseInt(fields[5])||0 + parseInt(fields[6])||0
- total < 100 → skip (소규모 흐름 제외)
- originISO === asylumISO → skip (내부 이동 제외)
- COUNTRY_COORDS에 없는 ISO → skip

flowsByOrigin 집계:
if (!flowsByOrigin[originISO]) flowsByOrigin[originISO] = {total:0, destinations:{}};
flowsByOrigin[originISO].total += total;
flowsByOrigin[originISO].destinations[asylumISO] = (flowsByOrigin[originISO].destinations[asylumISO]||0) + total;

flowsByAsylum 집계도 동일하게:
if (!flowsByAsylum[asylumISO]) flowsByAsylum[asylumISO] = {total:0, origins:{}};
flowsByAsylum[asylumISO].total += total;
flowsByAsylum[asylumISO].origins[originISO] = (flowsByAsylum[asylumISO].origins[originISO]||0) + total;

COUNTRY_COORDS 객체 (ISO3 → {lat, lng, name}, 최소 100개국 이상):
주요 국가 예시:
  AFG:{lat:34.5,lng:69.2,name:'Afghanistan'}, SYR:{lat:35.0,lng:38.0,name:'Syria'},
  UKR:{lat:50.4,lng:30.5,name:'Ukraine'}, VEN:{lat:10.5,lng:-66.9,name:'Venezuela'},
  SDN:{lat:15.5,lng:32.5,name:'Sudan'}, MMR:{lat:16.0,lng:96.0,name:'Myanmar'},
  TUR:{lat:41.0,lng:29.0,name:'Turkey'}, DEU:{lat:52.5,lng:13.4,name:'Germany'},
  POL:{lat:52.2,lng:21.0,name:'Poland'}, COL:{lat:4.6,lng:-74.1,name:'Colombia'},
  ... (나머지 국가도 모두 채워줘)

latLngToVec3(lat, lng, r, h):
  phi = (90-lat) * Math.PI/180
  theta = (lng+180) * Math.PI/180
  rad = r + (h||0)
  return new THREE.Vector3(
    -rad * Math.sin(phi) * Math.cos(theta),
     rad * Math.cos(phi),
     rad * Math.sin(phi) * Math.sin(theta)
  )

아크 생성 (createArcsFromFlows()):
arcSnakeObject = new THREE.Group(); earthObject.add(arcSnakeObject)

- var colorStart = new THREE.Color(0xff3333)  // 출발지 빨강
- var colorEnd   = new THREE.Color(0x00E5FF)  // 도착지 하늘색
- maxFlow = Math.max(...FLOWS.map(f=>f.total)) || 1

origin별로 그룹핑, 상위 8개 목적지만:
  flows.sort((a,b)=>b.total-a.total); topFlows = flows.slice(0, 8)

각 flow당 numArcs = Math.max(2, Math.min(8, Math.ceil(flow.total / maxFlow * 8)))
각 아크마다:
  sLat = origin.lat + (Math.random()-0.5)*0.8  // 출발지 약간 분산
  eLat = dest.lat   + (Math.random()-0.5)*0.5  // 도착지 약간 분산

아크 곡선 공식 (CubicBezierCurve3):
  start = latLngToVec3(sLat, sLng, CONFIG.globeRadius, 0.5)
  end   = latLngToVec3(eLat, eLng, CONFIG.globeRadius, 0.5)
  dist  = start.distanceTo(end)
  h  = 1 + dist * 0.0065
  h2 = 1 + dist * 0.0065 * 0.5
  mid   = addVectors(start,end).normalize() * CONFIG.globeRadius * h
  ctrl1 = addVectors(start,mid).normalize() * CONFIG.globeRadius * h2
  ctrl2 = addVectors(mid,end).normalize()   * CONFIG.globeRadius * h2
  curve = new THREE.CubicBezierCurve3(start, ctrl1, ctrl2, end)
  pts   = curve.getPoints(CONFIG.arcDivisions)

vertex 데이터 (LineSegments 용 — TubeGeometry 쓰지 말 것):
- position: pts[i] + pts[i+1] 쌍 (12 세그먼트 → 24 vertex)
- arcColor: lerpColors(colorStart, colorEnd, t1/t2) 그라디언트
- alpha: 1.0
- lineIndex: t1, t2 (0→1, 각 vertex의 아크상 위치 — 셰이더 애니메이션용)

아크 셰이더 (GLSL로 흐르는 대시 효과 — 버텍스/프래그먼트 셰이더 직접 작성):

vertex shader:
  attribute float alpha;
  attribute vec3 arcColor;
  attribute float lineIndex;
  varying float vAlpha;
  varying vec3 vColor;
  varying float vLineIndex;
  void main() {
    vAlpha = alpha; vColor = arcColor; vLineIndex = lineIndex;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
  }

fragment shader:
  varying float vAlpha; varying vec3 vColor; varying float vLineIndex;
  uniform float uTime;
  void main() {
    float dashSize = 0.15;
    float gapSize  = 0.10;
    float pattern  = mod(vLineIndex - uTime * 0.11, dashSize + gapSize);
    float edgeSoftness = 0.02;
    float dash = smoothstep(0.0, edgeSoftness, pattern) *
                 (1.0 - smoothstep(dashSize - edgeSoftness, dashSize, pattern));
    if (dash < 0.1) discard;
    gl_FragColor = vec4(vColor, vAlpha * dash);
  }

ShaderMaterial 설정:
  uniforms: { uTime: {value: 0} }
  blending: THREE.AdditiveBlending
  transparent: true
  depthTest: false

각 originISO별 mesh를 arcSnakeObject.add(mesh)
arcsByCountry[countryKey] = mesh  // 필터링용

아크 애니메이션 객체:
arcSnakeAnim = { time:0, speed:2.0, running:true }

animate() 루프에서:
  arcSnakeAnim.time += 0.016 * arcSnakeAnim.speed
  arcSnakeObject.children.forEach(function(mesh) {
    if (!mesh.visible) return;
    if (mesh.material.uniforms && mesh.material.uniforms.uTime)
      mesh.material.uniforms.uTime.value = arcSnakeAnim.time;
    // alpha 업데이트 (필터 상태 반영)
    var baseAlpha = (currentFilterISO === 'ALL') ? 0.85 : (mesh.userData.filtered ? 1.0 : 0.3);
    var alphaArr = mesh.geometry.attributes.alpha.array;
    for (var i=0; i<alphaArr.length; i++) alphaArr[i] = baseAlpha;
    mesh.geometry.attributes.alpha.needsUpdate = true;
  });
```

---

## Step 3 — 비주얼 효과 (별 + glow + dots)

```
아래 순서로 비주얼 레이어를 추가해줘.

① 별 파티클 (ShaderMaterial — PointsMaterial 쓰지 말 것):
- 별 2,000개, 반경 300~700 (300 + Math.random() * 400) 구형 분포
- sizes[i] = 10 + Math.random() * 20  (size attribute)
- 카메라 반대편 별은 크기 1/3로 축소 (dot product로 판별)
- 색상 (color attribute, 4가지 비율):
  40%: 흰색 (0.9, 0.95, 1.0)
  30%: 청록 (0.4, 0.85, 1.0)
  20%: 하늘색 (0.6, 0.75, 1.0)
  10%: 밝은 청록 (0.0, 0.9, 1.0)

vertex shader:
  attribute float size; attribute vec3 color; varying vec3 vColor;
  void main() {
    vColor = color;
    vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
    gl_PointSize = size * (450.0 / -mvPosition.z);
    gl_Position = projectionMatrix * mvPosition;
  }
fragment shader:
  varying vec3 vColor;
  void main() {
    float d = length(gl_PointCoord - vec2(0.5));
    if (d > 0.5) discard;
    float alpha = smoothstep(0.5, 0.0, d) * 0.9;
    gl_FragColor = vec4(vColor, alpha);
  }
blending: AdditiveBlending, depthWrite: false
scene.add (rotationObject 아님, 고정 배경)

② 지구 대기권 glow 3레이어 (earthObject에 추가):
- 1.06×: SphereGeometry(65*1.06, 48, 48), color:0x66ffff, opacity:0.25
- 1.15×: SphereGeometry(65*1.15, 48, 48), color:0x00e5ff, opacity:0.18
- 1.25×: SphereGeometry(65*1.25, 48, 48), color:0x00aaff, opacity:0.12
공통: MeshBasicMaterial, transparent:true, blending:AdditiveBlending, side:BackSide, depthWrite:false

③ 국가 위치 표시 dots (earthObject에 추가):
buildLocationsFromData()로 상위 30개 outflow + 상위 30개 inflow 국가 목록 구성
  - type 2 = outflow (빨강 #ff3333)
  - type 1 = inflow (하늘색 #00e5ff)
  - type 3 = both (빨강)

각 국가마다 PlaneGeometry(1,1) + MeshBasicMaterial, blending:AdditiveBlending, side:DoubleSide
- dot.position = latLngToVec3(lat, lng, CONFIG.globeRadius, 0.5)
- dot.lookAt(new THREE.Vector3(0,0,0))
- intensity 비례로 scale 조정 (0.6~1.4배)
- intensity > 0.3이면 흰색 core dot 추가
- intensity > 0.5이면 medium glow + outer glow dot 추가 (각각 opacity * intensity)

Canvas 텍스처로 radial gradient glow texture 만들기 (64×64):
function createGlowTexture(color, softness) {
  var canvas = document.createElement('canvas'); canvas.width=canvas.height=64;
  var ctx = canvas.getContext('2d');
  var g = ctx.createRadialGradient(32,32,0, 32,32,32);
  g.addColorStop(0, color); g.addColorStop(softness||0.3, color.replace(',1)',',.5)'));
  g.addColorStop(1, 'rgba(255,255,255,0)');
  ctx.fillStyle=g; ctx.fillRect(0,0,64,64);
  return new THREE.CanvasTexture(canvas);
}
```

---

## Step 4 — 인트로 오버레이 + 데이터 패널

```
1. 인트로 오버레이:

body에 intro-active 클래스를 추가 → 헤더/패널/HUD를 opacity:0으로 숨김
body.intro-active #header, #data-panel, #hud-left { opacity:0; pointer-events:none; }

#intro-overlay (z-index:1000):
- position:fixed; inset:0
- background: radial-gradient(circle at center, rgba(5,10,18,0.5) 0%, rgba(0,0,0,0.92) 70%)
- transition: opacity 0.8s ease, visibility 0.8s ease
- .hidden { opacity:0; visibility:hidden; pointer-events:none }

.intro-card (max-width:760px, text-align:center):
- h1.intro-title: "Migration Atlas" (Michroma, 42px, letter-spacing:3px)
- p.intro-subtitle: "An interactive visualization of global displacement journeys"
- p.intro-description: 설명 3줄
- button#introStartButton (원형, 185×185px, border-radius:50%):
  - border:1px solid rgba(0,204,255,0.5)
  - background: radial-gradient(circle at 30% 30%, rgba(0,204,255,0.45), rgba(0,36,82,0.8) 55%, rgba(0,0,0,0.9) 100%)
  - 텍스트: "Click\nto start"
  - box-shadow: 0 0 28px rgba(0,204,255,0.35)
- p.intro-footnote: "Data source: UNHCR (2020-2025)"

버튼 클릭 시 startExperience():
  document.body.classList.remove('intro-active')
  document.getElementById('intro-overlay').classList.add('hidden')

---

2. 헤더 (position:fixed, top:40px, left:40px):
- strong: "MIGRATION\nATLAS" (Michroma, 48px, letter-spacing:4px)
- .subtitle: "Global refugee and displacement flows. Data: UNHCR 2020-2025" (10px)

---

3. 왼쪽 HUD 패널 (#hud-left):
position:fixed, top:50%, left:20px, transform:translateY(-50%)
border:1px solid rgba(0,204,255,0.3), clip-path 모서리 깎인 패널 스타일

내용:
- [ SYS_INTEL ] (레이블, 깜빡이는 언더바 포함)
- ─────────────── (구분선)
- DISPLACED: 값 (loadUNHCRData 완료 후 업데이트)
- REFUGEES:  값
- ASYLUM:    값

---

4. 오른쪽 데이터 패널 (#data-panel):
position:fixed, top:50%, right:20px, transform:translateY(-50%)
width:240px, padding:12px 14px
border:1px solid rgba(0,204,255,0.25), background:rgba(0,0,0,0.85)
font-family:Michroma, font-size:8px, text-transform:uppercase

패널 구성 (위에서 아래 순서):

[A] KPI 카드 2개 (.kpi-grid):
  <div id="kpi-outflow">숫자</div> OUTFLOW — red (#FF1313)
  <div id="kpi-inflow">숫자</div>  INFLOW  — cyan (#00E5FF)
  → loadUNHCRData 완료 후 실제 CSV 집계값으로 채움

[B] 국가 검색 (.search-container):
  input#countrySearch (.hud-search): placeholder="Search country..."
  div#searchDropdown (.search-dropdown): 드롭다운, 최대 150px 높이

  setupCountrySearch():
  - countryList = [{iso:'all', name:'ALL REGIONS'}, ...topOrigins 30개]
  - input.value = 'ALL REGIONS' (초기값)
  - focus → 전체 선택 + showSearchResults('')
  - input → showSearchResults(this.value)
  - blur → 200ms 후 dropdown.classList.remove('active')
  - keydown Enter → 첫 번째 항목 클릭
  - keydown Escape → dropdown 닫기

  showSearchResults(query):
  - countryList 필터 (name.toLowerCase().indexOf(q) !== -1)
  - .search-item div 목록 렌더
  - 클릭 시 filterCountry(item.iso)

[C] OUTFLOW 바 차트 (클릭가능):
  CSV 집계 후 상위 5개 outflow 국가 동적 생성
  각 .bar-row.outflow-row: onclick="filterCountry('iso_lowercase')"
  구성: .bar-rank | .bar-label | .bar-track>.bar-fill.outflow | .bar-value
  .bar-fill.outflow: background:#FF4444
  .bar-fill.inflow:  background:#00E5FF

[D] INFLOW 바 차트:
  기본: 상위 5개 inflow 목적지 (INFLOW (IMMIGRATION))
  국가 선택 시: 해당 출발지의 목적지 상위 5개로 교체 (DESTINATIONS FROM XXX)

SOURCE: UNHCR MID-2024 (우측 하단, 7px)

---

5. filterCountry(countryInput) 핵심 동작:

iso = countryInput.toUpperCase()

'all' 또는 COUNTRY_COORDS에 없는 경우:
  gsap.to(camera.position, {z:250, duration:1, ease:'power2.out'})
  targetRotationX = 0.3; targetRotationY = 0;
  updateBarCharts()    // 글로벌 차트로 리셋
  filterArcsByCountry('all')
  inflow-title = 'INFLOW (IMMIGRATION)'

유효한 ISO인 경우:
  filterArcsByCountry(iso)
  targetRotationY = -coords.lng * Math.PI/180   // 지구를 해당 국가로 회전
  targetRotationX =  coords.lat * Math.PI/180 * 0.8
  gsap.to(camera.position, {z:140, duration:1, ease:'power2.out'})   // 줌인
  
  // 인플로우 차트 → 해당 국가의 목적지 상위 5개로 교체
  inflow-title = 'DESTINATIONS FROM ' + coords.name.toUpperCase()
  inflowChart.innerHTML = flowsByOrigin[iso].destinations 상위 5개 bar rows
  
  // KPI 업데이트
  kpi-outflow = formatNumber(flowsByOrigin[iso]?.total || 0)
  kpi-outflow-label = 'FROM ' + coords.name.toUpperCase()

filterArcsByCountry(iso):
  currentFilterISO = iso.toUpperCase()   (또는 'ALL')
  arcSnakeObject.children.forEach:
    mesh.visible = (iso==='all') ? true : (mesh.userData.iso === iso)
    mesh.userData.filtered = mesh.visible
```

---

## Step 5 — 모바일 반응형

```
터치 드래그 회전 지원 + 반응형 레이아웃.

이미 Step 1에서 touchstart/touchmove/touchend 추가했으면 생략 가능.

모바일 CSS (@media max-width:768px):
- #header strong: font-size:18px
- #hud-left: display:none (숨김)
- #data-panel: position:fixed; bottom:20px; right:12px; top:auto; transform:none
  width:150px; max-height:65vh; overflow-y:auto; border-radius:8px
- .settings: display:none
- .kpi-num: font-size:12px
- .bar-label: width:40px; font-size:6px
- .bar-value: font-size:8px; width:28px

canvas: 100vw × 100vh, overflow:hidden
window resize: camera.aspect, updateProjectionMatrix(), renderer.setSize()
```

---

## 완성본 참고

- 라이브: https://migrationtrack.netlify.app/
- 코드: https://github.com/seoyeon924/globe
