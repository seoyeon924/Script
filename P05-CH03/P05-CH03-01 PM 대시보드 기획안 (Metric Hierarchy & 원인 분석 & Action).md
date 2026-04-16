---
tags: #P05 #CH03 #PM #대시보드기획 #MetricHierarchy
time: 15분
part: Part 05
chapter: CH03
status: ✅ 대본완성
---

# P05-CH03-01 PM 대시보드 기획안 (Metric Hierarchy & 원인 분석 & Action)

## 📌 클립 정보
- **예상시간:** 15분
- **유형:** 슬라이드 3장 + 화면 녹화
- **준비물:** Claude Code

---

## 오프닝 (30초)

PM이라면 매일 보는 지표가 있습니다. DAU, 리텐션, 피처 사용률.
이번 챕터에서는 이 지표들을 Claude Code가 자동 집계하고 시각화까지 해주는 파이프라인을 만듭니다.

---

## PM이 보는 핵심 지표 (4분)

**DAU (Daily Active Users)**
하루에 서비스를 사용한 고유 사용자 수.

**리텐션율 (Retention Rate)**
- Day 1: 가입 다음날 다시 온 비율
- Day 7: 가입 후 7일째 다시 온 비율
- Day 30: 가입 후 30일째 다시 온 비율

**피처 사용률 (Feature Adoption Rate)**
전체 사용자 중 특정 기능을 사용한 비율.

**Stickiness**
`DAU / MAU × 100` — 매달 활성 사용자 중 매일 오는 비율.

---

## 대시보드 기획 — Metric Hierarchy 구조 (6분)

**레벨 1 — 북극성 지표 (North Star Metric)**
- 서비스 핵심 가치를 반영하는 1개 지표
- 예: 주간 활성 사용자 × 평균 세션 시간

**레벨 2 — 핵심 KPI (5~7개)**
- DAU/WAU/MAU
- D1/D7/D30 리텐션
- 피처 사용률 (핵심 기능 3개)

**레벨 3 — 진단 지표 (드릴다운)**
- 코호트별 리텐션 차이
- 피처별 Funnel 분석
- 이탈 패턴 분석

**레벨 4 — 액션 레이어**
- KPI 하락 원인 자동 진단
- 개선 실험 제안
- 담당자 알림 설정

---

## 샘플 데이터 생성 (3분)

```bash
mkdir -p ~/pm-project/data/raw ~/pm-project/charts ~/pm-project/reports
cd ~/pm-project
python3 -c "
import pandas as pd, random; from datetime import date, timedelta; random.seed(42)
features = ['검색','추천','즐겨찾기','공유','설정']; start = date(2024,1,1); rows = []
for uid in range(1000):
    for day in range(90):
        rate = 0.6 if day<3 else (max(0.2, 0.6-(day-3)*0.012) if day<30 else 0.2)
        if random.random() < rate:
            rows.append({'user_id':f'U{uid:04d}','date':str(start+timedelta(days=day)),'feature_used':random.choice(features)})
pd.DataFrame(rows).to_csv('data/raw/user_logs.csv',index=False); print('생성 완료:', len(rows), '행')
"
claude
```

---

## 핵심 정리 (30초)

PM 대시보드는 북극성 지표 → 핵심 KPI → 진단 지표 → 액션의 4레벨 Metric Hierarchy로 구성합니다.
다음 클립에서는 전용 CLAUDE.md와 Skill로 PM 대시보드를 제작합니다.
