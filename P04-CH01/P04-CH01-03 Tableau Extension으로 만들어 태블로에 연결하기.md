---
tags: #P04 #CH01 #Tableau #Extension #태블로연동 #trex
time: 15분
part: Part 04
chapter: CH01
status: ✅ 대본완성
---

# P04-CH01-03 Tableau Extension으로 만들어 태블로에 연결하기

## 📌 클립 정보
- **예상시간:** 15분
- **유형:** 슬라이드 2장 + 화면 녹화
- **준비물:** Tableau Public 또는 Tableau Desktop, Claude Code

---

## 오프닝 (30초)

D3.js로 만든 인터랙티브 차트를 Tableau 대시보드 안에서 직접 실행하는 방법을 배웁니다.
기존 Tableau 환경을 유지하면서 커스텀 시각화를 추가합니다.

---

## Tableau Extension이란 (3분)

Tableau Extension은 Tableau 대시보드 안에 외부 웹 앱을 embed하는 기능입니다.

**활용 사례:**
- D3.js 네트워크 그래프를 Tableau에 삽입
- 커스텀 인터랙티브 차트 추가
- Tableau가 지원하지 않는 시각화 타입 구현

**Extension 구조:**
```
.trex 파일 (Tableau Extension 패키지)
├── manifest.trex   ← Extension 메타데이터
├── index.html      ← D3.js 시각화
└── extension.js    ← Tableau API 연동
```

---

## TWB 파일 자동 생성 (4분)

Tableau 워크북 파일(.twb)은 XML 형식입니다.
Claude Code가 이 구조를 분석하고 새 데이터에 맞게 자동 생성합니다.

```
data/campaigns.csv를 분석해서 Tableau 워크북 파일을 생성해줘.
- 시트 1: 채널별 총 매출 막대 차트
- 시트 2: 월별 매출 트렌드 라인 차트
- 시트 3: 채널별 ROI 비교
charts/analysis.twb로 저장해줘.
```

---

## D3.js → Tableau Extension 변환 (5분)

```
이 네트워크 그래프를 로컬 Tableau Extension으로 만들어줘.
.trex 파일로 패키징하고,
Tableau 대시보드에서 바로 실행할 수 있게 해줘.
```

변환 후 Tableau Desktop에서:
1. 대시보드 → Extension 객체 추가
2. .trex 파일 선택
3. Extension이 대시보드 안에서 실행됨

---

## 기존 템플릿 재활용 전략 (2분)

기존에 잘 만들어진 Tableau 대시보드가 있다면:

```
기존 analysis_template.twb 파일을 참고해서
새 데이터 campaigns_2024.csv에 맞게 수정한 워크북을 생성해줘.
색상과 레이아웃은 기존 템플릿과 동일하게 유지해줘.
```

---

## 핵심 정리 (30초)

Tableau 워크북(.twb)은 XML 구조이기 때문에 Claude Code가 자동 생성할 수 있습니다.
D3.js 시각화를 .trex로 패키징하면 Tableau 대시보드에서 직접 사용합니다.
다음 클립에서는 3D Globe 시각화를 만듭니다.
