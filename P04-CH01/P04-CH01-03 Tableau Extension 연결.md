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

---

## s14 — CLIP 03 섹션 브레이크

**[화면: 슬라이드]**

이번 클립에서는 두 가지를 배워요.

첫 번째, **.trex 파일이 어떤 구조로 생겼는지** 이해하는 거예요.

두 번째, **Tableau에서 Extension을 불러오는 방법**이에요.

앞에서 만든 D3.js 시각화를 **.trex 파일로 패키징**해서, Tableau 대시보드 안에 직접 임베드해볼게요.

---

## s15 — Tableau Extension 파일 구조

**[화면: 슬라이드]**

왼쪽 파일 트리를 먼저 볼게요.

폴더가 두 개로 나뉘어 있어요.

**`index.html`** 은 브라우저에서 바로 실행하는 독립 실행 파일이에요.

**`tableau-extension/`** 폴더 안에는 Tableau에서 쓸 파일들이 모여 있어요.

여기서 중요한 건, **같은 D3.js 코드가 두 가지 방식으로 동작**한다는 거예요.

브라우저에서는 `index.html`로, Tableau 안에서는 `tableau-extension/` 폴더로 실행돼요.

---

이제 오른쪽 설명을 볼게요.

**.trex 파일**은 Tableau Extension 패키지예요.

`manifest.trex`와 웹앱 파일을 묶어 놓은 거예요.

Tableau Desktop에서 이 파일을 바로 불러와서 쓸 수 있어요.

---

**`manifest.trex`** 는 Extension의 메타데이터예요.

Extension 이름, 버전, 권한, 그리고 URL을 여기서 선언해요.

앱 정보를 Claude Code에게 주면 **자동으로 생성해줘요.**

---

변환 흐름은 간단해요.

브라우저용 D3.js 코드를 → Tableau Extension 파일로 바꾸고 → Tableau API 형식으로 변환하면 끝이에요.

---

## s16 — Tableau Viz Extension — 사용 방법

**[화면: 슬라이드]**

실제로 Tableau에서 Extension을 사용하는 방법을 세 단계로 볼게요.

---

**1단계, 데이터 연결이에요.**

Tableau Desktop을 열고 → Connect → Text file 순서로 들어가요.

`avengers_network_data.csv` 파일을 선택하면 돼요.

필수 컬럼은 **Source**, **Target**, **Strength** 세 개예요.

선택 컬럼으로 **Type**, **Source_Image**, **Target_Image** 도 있어요.

---

**2단계, Extension을 추가해요.**

Marks 카드에서 Mark 타입 드롭다운을 열어요.

**Add Extension** 을 선택하고 → **Access Local Extensions** 클릭해요.

`avengers-network.trex` 파일을 선택하면 끝이에요.

---

**3단계, 필드를 할당해요.**

Marks 카드에 인코딩 네 개를 연결하면 돼요.

- **source** 인코딩 → Source 필드 (Dimension)
- **target** 인코딩 → Target 필드 (Dimension)
- **strength** 인코딩 → Strength 필드 (Measure)
- **type** 인코딩 → Type 필드 (Dimension, 선택 사항)

---

한 가지 더 강조할 점이 있어요.

**로컬 서버가 필요 없어요.**

`.trex` 파일만 있으면, 인터넷 연결만으로 실행돼요.

Netlify에 배포된 URL이 `manifest.trex`에 이미 등록되어 있기 때문이에요.

---

그리고 내 데이터에 적용하는 것도 아주 간단해요.

**Source, Target, Strength** 컬럼만 있으면 어떤 네트워크 데이터든 바로 쓸 수 있어요.

구조를 바꿀 필요 없이 CSV만 교체하면 돼요.

---

다음 클립에서는 **Three.js로 3D Globe 시각화**를 만들어볼게요.

완전히 다른 차원의 인터랙티브 시각화예요.
