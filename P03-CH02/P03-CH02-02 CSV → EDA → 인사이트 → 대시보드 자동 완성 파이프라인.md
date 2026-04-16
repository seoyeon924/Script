---
tags: #P03 #CH02 #CSV #EDA #대시보드자동생성 #파이프라인
time: 15분
part: Part 03
chapter: CH02
status: 📝 작성필요
---

# P03-CH02-02 CSV → EDA → 인사이트 → 대시보드 자동 완성 파이프라인

## 📌 클립 정보
- **예상시간:** 15분
- **유형:** 슬라이드 + 화면녹화

---

## 오프닝 (30초)

(CSV 하나를 넣으면 EDA → 인사이트 → 대시보드가 자동으로 완성되는 파이프라인 시연)

## 본문

### 파이프라인 전체 흐름

```
1. CSV 입력
   data/raw/campaigns.csv

2. EDA (탐색적 데이터 분석)
   - 컬럼 타입, 결측값, 분포
   - 이상치 탐지
   - 기초 통계

3. KPI 계산
   - ROI, CTR, CVR, CPA, CPC
   - 채널별, 기간별 집계

4. 인사이트 도출
   - 패턴 발견
   - 비즈니스 의미 해석
   - 권고 액션 생성

5. 대시보드 생성
   - KPI 카드 (상단)
   - 시계열 차트
   - 채널 비교 차트
   - charts/dashboard.html

6. 리포트 저장
   - reports/analysis_report.md
```

### 한 번의 지시로 전체 실행

```
data/raw/campaigns.csv로 전체 파이프라인을 실행해줘.

순서:
1. EDA → 데이터 구조 파악
2. 마케팅 KPI 계산 (ROI/CTR/CVR)
3. 채널별 인사이트 3개 도출
4. Plotly 인터랙티브 대시보드 생성
5. 경영진 요약 리포트 작성

저장:
- data/processed/cleaned.csv
- charts/dashboard.html
- reports/report.md
```

### 에이전트 팀으로 실행

```
에이전트 팀으로 파이프라인을 실행해줘.
- 분석가: EDA + KPI 계산
- BI: 대시보드 생성
- 작성가: 리포트 생성
동시에 실행 가능한 작업은 병렬로 처리해줘.
```

---

## 핵심 정리 (30초)

CSV → EDA → 인사이트 → 대시보드 파이프라인을 에이전트 팀으로 자동화합니다.
CLAUDE.md에 파이프라인이 정의되어 있으면 파일 경로만 알려줘도 자동 실행됩니다.
다음 클립에서는 Google Sheets 연동을 배웁니다.
