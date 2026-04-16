---
tags: #P05 #CH03 #PM대시보드 #CLAUDE-md #제작실습
time: 15분
part: Part 05
chapter: CH03
status: 📝 작성필요
---

# P05-CH03-02 PM 대시보드 전용 CLAUDE.md + Skill로 제작 실습

## 📌 클립 정보
- **예상시간:** 15분
- **유형:** 슬라이드 + 화면녹화

---

## 오프닝 (30초)

(PM 대시보드 전용 CLAUDE.md와 Product Analyst Skill을 설계하고 실제 대시보드 제작 실습)

## 본문

### PM 전용 CLAUDE.md

```markdown
# PM KPI 대시보드

## 핵심 지표 계산식
- DAU: count(distinct user_id) per day
- D1 리텐션: (D+1에 재방문한 Day 0 가입자 수) / (Day 0 가입자 수)
- Stickiness: DAU / MAU × 100
- 피처 사용률: (피처 사용 사용자) / (전체 DAU) × 100

## 대시보드 구성
1. KPI 카드 (DAU, D7 리텐션, Stickiness)
2. DAU 추이 라인 차트 (30일)
3. 코호트 리텐션 히트맵
4. 피처별 사용률 비교 막대 차트
5. 이상 탐지 알림 패널

## 이상 탐지 기준
- DAU가 7일 이동 평균 대비 20% 이상 하락
- D1 리텐션이 30% 미만
- 핵심 피처 사용률이 전주 대비 15% 이상 하락
```

### 대시보드 제작 실습

```bash
cd ~/pm-project
claude
```

```
data/raw/user_logs.csv로 PM KPI 대시보드를 만들어줘.

포함 내용:
1. 일별 DAU 계산 및 추이 차트
2. D1/D7/D30 리텐션율 계산
3. 코호트 리텐션 히트맵
4. 피처별 사용률 비교
5. 이상치 탐지 (DAU 급락 포인트 강조)

charts/pm_dashboard.html로 저장
```

### 주간 PM 리포트 자동화

```
지난 주 PM KPI를 분석하고
마크다운 형식으로 주간 리포트를 작성해줘.

포함:
- 이번 주 핵심 지표 요약
- 전주 대비 변화
- 주목할 이슈 2~3개
- 다음 주 권고 액션

reports/weekly_pm_report.md로 저장
```

---

## 핵심 정리 (30초)

PM 전용 CLAUDE.md에 이상 탐지 기준을 정의하면 지표 하락을 자동으로 감지합니다.
주간 리포트까지 자동화하면 매주 월요일 아침 준비 시간이 크게 줄어듭니다.
