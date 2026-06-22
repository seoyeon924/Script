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
> - [ ] `avengers-practice/starwars_network_data.csv` 파일 위치 확인
> - [ ] `avengers-complete/avengers-network.trex` 파일 위치 확인

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

**Extension** 을 선택합니다. 그러면 팝업이 열리는데, **Access Local Extensions** 를 클릭합니다.

`avengers-network.trex` 파일을 선택하면 끝이에요.

---

**3단계, 필드를 할당합니다.**

Marks 카드에 인코딩 네 개를 연결하면 돼요.

- **source** 인코딩 → Source 필드 (Dimension)
- **target** 인코딩 → Target 필드 (Dimension)
- **strength** 인코딩 → Strength 필드 (Measure)
- **type** 인코딩 → Type 필드 (Dimension, 선택 사항)

---

여기서 한 가지 중요한 포인트가 있어요.

지금 불러온 `avengers-network.trex`는 **완성본 파일**이에요.

안에 등록된 URL이 이미 Netlify에 배포된 주소를 가리키고 있어서, **로컬 서버를 켤 필요가 없습니다.**

인터넷 연결만 있으면 어디서든 바로 실행돼요.

---

반면에 Claude Code로 Extension을 **직접 만들면** 상황이 조금 달라요.

Claude Code가 생성하는 `manifest.trex`의 URL은 `http://localhost:8080`을 가리키기 때문에, `python3 -m http.server 8080`을 켜둔 상태에서만 작동합니다.

다른 사람과 공유하거나 실제로 배포하려면, 만든 파일을 Netlify 같은 곳에 올리고 `manifest.trex` 안의 URL을 배포된 주소로 바꿔줘야 해요.

강의 실습에서는 완성본 `.trex`를 그대로 쓰는 게 가장 간편합니다.

---

그리고 내 데이터에 적용하는 것도 아주 간단합니다.

**Source, Target, Strength** 컬럼만 있으면 어떤 네트워크 데이터든 바로 쓸 수 있어요.

구조를 바꿀 필요 없이 CSV만 교체하면 됩니다.

---

직접 확인해보도록 하겠습니다.

---

## ▶ 화면 전환 — Tableau Desktop 실습

**[화면: Tableau Desktop]**

슬라이드에서 설명한 걸 실제로 연결해보도록 하겠습니다.

그런데 데이터는 어벤져스가 아니라 **스타워즈**로 해볼 거예요.

아까 만든 `.trex` 파일은 그대로 씁니다. 데이터만 바꾸는 거예요.
`Source`, `Target`, `Strength` 컬럼만 있으면 어떤 데이터든 된다고 했는데, 지금 바로 확인해보겠습니다.

---

### 1단계 — 스타워즈 데이터 연결

Tableau Desktop → Connect → **Text file**을 클릭합니다.

`avengers-practice/starwars_network_data.csv` 파일을 선택합니다.

> 확인: Source, Target, Strength, Type, Source_Group 컬럼이 보이면 됩니다.
> 어벤져스 데이터와 핵심 컬럼(Source, Target, Strength, Type)이 동일해요. Extension이 이 4개만 읽기 때문에 그대로 동작합니다.

---

### 2단계 — Extension 불러오기

Sheet 1로 이동합니다.

Marks 카드 → Mark 타입 드롭다운 → **Extension** 선택합니다.

팝업에서 **Access Local Extensions** → `avengers-complete/avengers-network.trex` 파일을 선택합니다.

Allow를 클릭하면 Extension이 로드됩니다.

> 어벤져스용으로 만든 .trex 파일을 그대로 씁니다. 파일을 새로 만들 필요가 없어요.

---

### 3단계 — 필드 매핑

Marks 카드 인코딩 슬롯에 스타워즈 데이터 필드를 연결합니다.

- **source** → `Source` 드래그
- **target** → `Target` 드래그
- **strength** → `Strength` 드래그
- **type** → `Type` 드래그

> 확인: 필드를 드롭하는 순간 스타워즈 캐릭터 네트워크가 그려집니다.

---

### 완성 확인

루크 스카이워커, 다스 베이더, 한 솔로, 레아 공주가 네트워크로 연결돼 있습니다.

어벤져스랑 완전히 다른 데이터인데, Extension은 그대로예요.

`Source_Group` 필터를 추가해볼게요. Rebels·Empire·Jedi·Sith·Bounty Hunters 파벌별로 필터링이 됩니다.

이게 재사용의 힘입니다. **`.trex` 파일 하나로 데이터만 바꿔서 전혀 다른 네트워크 시각화**를 만들 수 있어요.

다음 클립에서는 **Three.js로 3D Globe 시각화**를 만들어보도록 하겠습니다.
