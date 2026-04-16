---
tags: #P05 #CH01 #마케팅대시보드 #CLAUDE-md #Skill #제작실습
time: 15분
part: Part 05
chapter: CH01
status: 📝 작성필요
---

# P05-CH01-02 캠페인 성과 대시보드 전용 CLAUDE.md + Skill로 제작 실습

## 📌 클립 정보
- **예상시간:** 15분
- **유형:** 슬라이드 + 화면녹화

---

## 오프닝 (30초)

(마케팅 대시보드 전용 CLAUDE.md와 Skill을 설계하고 실제 대시보드를 제작하는 실습)

## 본문

### 마케팅 대시보드 전용 CLAUDE.md

```markdown
# 마케팅 캠페인 성과 분석 대시보드

## 프로젝트 개요
마케팅 채널별 성과를 분석하고 예산 배분을 최적화합니다.

## 핵심 KPI
- ROI = (매출 - 광고비) / 광고비 × 100
- CTR = 클릭수 / 노출수 × 100
- CVR = 전환수 / 클릭수 × 100
- CPA = 광고비 / 전환수

## 대시보드 구성
1. KPI 카드 (상단): ROI, 총 광고비, 총 전환수, 최고 채널
2. 채널별 성과 비교 (막대 차트)
3. ROI 시계열 추이 (라인 차트)
4. 클러스터 분석 (스캐터 플롯)
5. 예산 배분 권고 (표)

## 시각화 규칙
- 최고 성과 채널: 진한 파랑(#1E3A5F)
- 평균 이하 채널: 연한 회색(#CCCCCC)
- 대시보드: charts/marketing_dashboard.html
```

### Marketing Analyst Skill 정의

```markdown
# Marketing Analyst Skill

## 역할
마케팅 데이터 분석 전문가로 작업합니다.

## 분석 순서
1. 데이터 로딩 및 EDA
2. KPI 계산 (ROI/CTR/CVR/CPA/CPC)
3. 채널별 성과 순위 도출
4. 시계열 트렌드 분석
5. 클러스터 분석으로 채널 그룹화
6. 예산 배분 권고 생성
7. 인터랙티브 대시보드 생성
```

### 대시보드 제작 실습

```bash
cd ~/marketing-project
claude
```

```
data/raw/campaigns.csv로 마케팅 대시보드를 만들어줘.

CLAUDE.md의 대시보드 구성 규칙을 따르고
charts/marketing_dashboard.html로 저장해줘.

추가로:
- 채널별 예산 배분 권고 표 포함
- 다음 달 ROI 예측선 추가
```

---

## 핵심 정리 (30초)

전용 CLAUDE.md와 Skill을 설계하면 새 데이터가 들어올 때마다 일관된 품질의 대시보드가 자동 생성됩니다.
다음 클립에서는 이 대시보드에서 인사이트를 도출하는 방법을 배웁니다.
