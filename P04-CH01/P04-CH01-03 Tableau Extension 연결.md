---
tags: #P04 #CH01 #Tableau #Extension #trex
time: 10분
part: Part 04
chapter: CH01
clip: 03
slides: s14,s15,s16
status: ✅ 대본완성
---

# P04-CH01-03 Tableau Extension 연결

> **촬영 전 준비**
> - [ ] 슬라이드 s14에 커서
> - [ ] Tableau Desktop 열어두기
> - [ ] `avengers-practice/avengers_network_data.csv` 파일 위치 확인
> - [ ] `avengers-complete/tableau-extension/avengers-network.trex` 파일 위치 확인

---

## s14 — CLIP 03 섹션 브레이크

이번 클립에서는 두 가지를 배워보도록 하겠습니다.

첫 번째, **.trex 파일이 어떤 구조로 생겼는지** 이해하는 거예요.

두 번째, **Tableau에서 Extension을 불러오는 방법**입니다.

앞에서 만든 D3.js 시각화를 **.trex 파일로 패키징**해서, Tableau 대시보드 안에 직접 임베드해볼게요.

---

## s15 — Tableau Extension 파일 구조

**[화면: 슬라이드]**

왼쪽 파일 트리를 먼저 살펴볼게요.

폴더가 두 개로 나뉘어 있습니다.

**`index.html`** 은 브라우저에서 바로 실행하는 독립 실행 파일이에요.

**`tableau-extension/`** 폴더 안에는 Tableau에서 쓸 파일들이 모여 있습니다.

여기서 중요한 건, **같은 D3.js 코드가 두 가지 방식으로 동작**한다는 거예요.

브라우저에서는 `index.html`로, Tableau 안에서는 `tableau-extension/` 폴더로 실행됩니다.

---

이제 오른쪽 설명을 볼게요.

**.trex 파일**은 Tableau Extension 패키지입니다.

`manifest.trex`와 웹앱 파일을 묶어 놓은 건데요.

Tableau Desktop에서 이 파일을 바로 불러와서 쓸 수 있습니다.

---

**`manifest.trex`** 는 Extension의 메타데이터예요.

Extension 이름, 버전, 권한, 그리고 URL을 여기서 선언합니다.

앱 정보를 Claude Code에게 주면 **자동으로 생성해줍니다.**

---

변환 흐름은 간단합니다.

브라우저용 D3.js 코드를 → Tableau Extension 파일로 바꾸고 → Tableau API 형식으로 변환하면 끝이에요.

---

## s16 — Tableau Viz Extension — 사용 방법

**[화면: 슬라이드]**

실제로 Tableau에서 Extension을 사용하는 방법을 세 단계로 살펴볼게요.

---

**1단계, 데이터 연결입니다.**

Tableau Desktop을 열고 → Connect → Text file 순서로 들어가요.

`avengers_network_data.csv` 파일을 선택하면 됩니다.

필수 컬럼은 **Source**, **Target**, **Strength** 세 개예요.

선택 컬럼으로 **Type**, **Source_Image**, **Target_Image** 도 있습니다.

---

**2단계, Extension을 추가해보도록 하겠습니다.**

Marks 카드에서 Mark 타입 드롭다운을 열어요.

**Add Extension** 을 선택하고 → **Access Local Extensions** 클릭합니다.

`avengers-network.trex` 파일을 선택하면 끝이에요.

---

**3단계, 필드를 할당합니다.**

Marks 카드에 인코딩 네 개를 연결하면 돼요.

- **source** 인코딩 → Source 필드 (Dimension)
- **target** 인코딩 → Target 필드 (Dimension)
- **strength** 인코딩 → Strength 필드 (Measure)
- **type** 인코딩 → Type 필드 (Dimension, 선택 사항)

---

한 가지 더 강조할 점이 있습니다.

**로컬 서버가 필요 없어요.**

`.trex` 파일만 있으면, 인터넷 연결만으로 실행됩니다.

Netlify에 배포된 URL이 `manifest.trex`에 이미 등록되어 있기 때문이에요.

---

그리고 내 데이터에 적용하는 것도 아주 간단합니다.

**Source, Target, Strength** 컬럼만 있으면 어떤 네트워크 데이터든 바로 쓸 수 있어요.

구조를 바꿀 필요 없이 CSV만 교체하면 됩니다.

---

다음 클립에서는 **Three.js로 3D Globe 시각화**를 만들어볼게요.

완전히 다른 차원의 인터랙티브 시각화입니다.

---

## ▶ 화면 전환 — Tableau Desktop 실습

**[화면: Tableau Desktop]**

슬라이드에서 설명한 걸 실제로 연결해보도록 하겠습니다.

---

### 1단계 — 데이터 연결

Tableau Desktop을 열면 왼쪽에 Connect 패널이 있습니다.
**Text file**을 클릭합니다.

`avengers-practice/avengers_network_data.csv` 파일을 선택합니다.

> 확인: Source, Target, Strength, Type 컬럼이 보이면 됩니다.

---

### 2단계 — 워크시트로 이동

Sheet 1로 이동합니다.
왼쪽 Data 패널에 컬럼들이 올라와 있어요.

Marks 카드를 봐주세요.
Mark 타입 드롭다운을 클릭합니다. 기본값은 Automatic인데요.

맨 아래 **Add Extension**을 선택합니다.

> 확인: "Add Extension" 항목이 안 보이면 Tableau 버전 확인 — 2021.3 이상이어야 합니다.

---

### 3단계 — .trex 파일 불러오기

**Access Local Extensions**를 클릭합니다.

`avengers-complete/tableau-extension/avengers-network.trex` 파일을 선택합니다.

Allow 버튼을 클릭하면 Extension이 로드됩니다.

> 확인: 워크시트 안에 네트워크 그래프 영역이 생기면 OK

---

### 4단계 — 필드 매핑

Marks 카드에 인코딩 슬롯이 생겼습니다.

- **source** 슬롯에 → `Source` 필드 드래그
- **target** 슬롯에 → `Target` 필드 드래그
- **strength** 슬롯에 → `Strength` 필드 드래그
- **type** 슬롯에 → `Type` 필드 드래그 (선택)

> 확인: 필드를 드롭하면 네트워크 그래프가 바로 업데이트됩니다.

---

### 완성 확인

어벤져스 네트워크 차트가 Tableau 워크시트 안에 들어와 있습니다.

Tableau 필터를 추가하면 워크시트 필터와 네트워크 그래프가 연동됩니다.
예를 들어 `Source_Group` 필터를 넣으면 특정 파벌만 골라볼 수 있어요.

이게 Tableau Extension의 핵심입니다. D3.js로 만든 커스텀 시각화를 Tableau 생태계 안에 그대로 가져올 수 있는 거예요.

다음 클립에서는 **Three.js로 3D Globe 시각화**를 만들어보도록 하겠습니다.
