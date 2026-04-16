---
tags: #P05 #CH04 #리텐션 #코호트 #LTV #대시보드기획
time: 15분
part: Part 05
chapter: CH04
status: ✅ 대본완성
---

# P05-CH04-01 리텐션 분석 대시보드 기획안 (코호트 & What-if & LTV)

## 📌 클립 정보
- **예상시간:** 15분
- **유형:** 슬라이드 2장 + 화면 녹화
- **준비물:** Claude Code

---

## 오프닝 (30초)

고객이 왜 떠나는지 아세요? 대부분 "그냥 안 오더라고요"라고 합니다.
이번 챕터에서는 코호트 분석으로 언제, 어떤 그룹이 이탈하는지 데이터로 찾아냅니다.
LTV(고객 생애 가치)와 What-if 시뮬레이션까지 포함합니다.

---

## 코호트 리텐션이란 (3분)

코호트(Cohort)는 같은 시기에 특정 행동을 한 사용자 그룹입니다.

**쉽게 보면:**
2024년 1월에 학원에 등록한 학생들(1월 코호트)이 2월에 몇 명이나 계속 다니는지 추적합니다.
2월 코호트와 비교하면 어느 달에 등록한 학생들이 더 오래 다니는지 알 수 있습니다.

---

## 대시보드 기획 — 3개 레이어 (7분)

**레이어 1 — 코호트 리텐션 히트맵**
- 행: 가입 월 코호트
- 열: Month 0~12
- 색상: 낮을수록 빨강, 높을수록 파랑
- 어느 코호트에서 이탈이 많은가

**레이어 2 — What-if 시뮬레이션**
- 인터랙티브 슬라이더: "리텐션 5% 개선 시 매출은?"
- 코호트별 LTV 변화 시뮬레이션
- 이탈 방어 비용 vs 기대 수익 비교

**레이어 3 — LTV 분석**
- 코호트별 평균 LTV
- LTV 상위 20% 고객 특성 분석
- LTV 기반 고객 세그먼트 분류

---

## 샘플 데이터 생성 (2분)

```bash
mkdir -p ~/retention-project/data/raw ~/retention-project/charts ~/retention-project/reports
cd ~/retention-project
python3 -c "
import pandas as pd, random; random.seed(42); rows = []
for uid in range(2000):
    cohort = random.randint(1,12)
    for month in range(cohort, 13):
        age = month - cohort
        ret = 1.0 if age==0 else max(0.05, 0.6*(0.9**(age-1)))
        if random.random() < ret:
            rows.append({'user_id':f'U{uid:04d}','cohort_month':f'2024-{cohort:02d}','order_month':f'2024-{month:02d}','revenue':random.randint(15000,80000)})
pd.DataFrame(rows).to_csv('data/raw/orders.csv',index=False); print('생성 완료:', len(rows), '행')
"
claude
```

---

## 핵심 정리 (30초)

리텐션 대시보드는 코호트 히트맵 → What-if 시뮬레이션 → LTV 분석의 3개 레이어로 구성합니다.
다음 클립에서는 전용 CLAUDE.md와 Skill로 리텐션 대시보드를 제작합니다.
