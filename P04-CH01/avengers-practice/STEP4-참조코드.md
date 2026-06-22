# Step 4 참조 코드 — Tableau Viz(워크시트) 확장 (정밀 버전)

> CLAUDE.md Step 4의 정밀 버전. 완성 예시를 세부 수치까지 정확히 재현하고 싶을 때 아래 프롬프트를 그대로 붙여넣으세요.
> 입문용 자연어 버전은 CLAUDE.md Step 4에 있습니다.

```
index.html과 별도로 tableau-extension/ 폴더를 새로 만들고
그 안에 avengers-network.html 과 manifest.trex 두 파일을 생성해줘.

─── tableau-extension/avengers-network.html ───
- D3.js v7 + Tableau Extensions SDK (Viz 확장은 API 1.12+ 필요)
  <script src="https://d3js.org/d3.v7.min.js"></script>
  <script src="https://extensionsdk.azureedge.net/1.latest/tableau.extensions.1.latest.js"></script>
- 배경 #000, SVG 전체 화면, overflow:hidden

초기화 (Viz 확장):
  tableau.extensions.initializeAsync()
    → worksheet = tableau.extensions.worksheetContent.worksheet
    → render()
    → SummaryDataChanged 이벤트 → render 재호출
  .catch → Tableau 밖 개발용: d3.csv('../avengers_network_data.csv').then(renderNetwork)

render(worksheet):
  getVisualSpecificationAsync()로 인코딩(source/target/strength/type)→필드명 매핑
  getSummaryDataReaderAsync() → getAllPagesAsync() → releaseAsync()로 요약 데이터 읽기
  인코딩 매핑 우선, 없으면 컬럼명 소문자 includes로 인덱스 추정
  rows = dataTable.data.map → { Source, Target, Strength: parseFloat, Type }
  .filter(r => r.Source && r.Target)
  → renderNetwork(rows)

renderNetwork(data):
  W = window.innerWidth, H = window.innerHeight
  svg 크기 W×H로 설정, 기존 요소 전부 제거 후 재렌더

  노드: nodeSet으로 중복 제거, nodes/links 구성
  링크 색상: ally → #4fc3f7, enemy → #ef5350, romantic → #f06292, 기타 → #aaa
  선 굵기: d3.scaleLinear domain[1, max(strength)] range[1, 6]
  선 opacity: 0.6

  Force Simulation:
    forceLink distance 120
    forceManyBody strength -300
    forceCenter(W/2, H/2)

  노드: circle r=8, fill #e8603c, stroke #fff, stroke-width 1.5
  드래그 가능 (alphaTarget 0.3 on start, 0 on end)
  레이블: font-size 11, fill #ccc, text-anchor middle, dy 20

window resize → render 재호출

─── tableau-extension/manifest.trex (worksheet-extension) ───
⚠️ manifest 스키마 주의 — 아래를 어기면 "구문 분석 오류(FD722608)"가 난다:
  · 최상위는 반드시 <worksheet-extension> (대시보드용 <dashboard-extension> 아님)
  · <default-settings>·<encodings> 요소는 worksheet-extension에 존재하지 않음 → 절대 넣지 말 것
  · worksheet-extension 자식 요소는 정해진 순서·집합만 허용:
    (default-locale, name, description, author, min-api-version, source-location,
     icon, permissions?, context-menu?, disable-sorting-ui?, encoding*)
    → 인코딩을 쓸 경우 <encoding id="..."/>를 맨 끝에 직접 나열 (감싸지 않음).
  · 이번 버전은 인코딩 선언 없이 컬럼 이름으로 필드를 읽으므로 <encoding>도 생략한다.
  · min-api-version은 1.12 이상 (Viz 확장 지원 버전)

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
    <icon>iVBORw0KGg... (16x16 base64 PNG)</icon>
    <permissions>
      <permission>full data</permission>
    </permissions>
  </worksheet-extension>
</manifest>
```

## 추가 방법 (Viz 확장)

1. 워크시트의 **마크 카드 드롭다운 → "확장 프로그램 추가" → 로컬에서 manifest.trex 선택**
   - ※ 대시보드의 "확장 프로그램" 개체에 넣으면 "비주얼리제이션 확장이 아닙니다(93FB5DF9)" 에러
2. 마크 카드 **'세부 정보(Detail)'에 Source · Target · Strength · Type 필드**를 올리면 렌더됨
   - manifest에 인코딩을 선언하지 않으므로, 코드가 컬럼 이름으로 필드를 찾음
3. source-location URL의 호스트/포트에서 avengers-network.html이 실제로 서빙돼야 함
   - 안 그러면 빈 화면 — 로컬 테스트는 manifest URL과 같은 포트로 서버 실행
