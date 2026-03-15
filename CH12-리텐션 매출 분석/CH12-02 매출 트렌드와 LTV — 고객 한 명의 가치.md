---
tags: #CH12 #매출트렌드 #LTV #엘티브이 #고객가치
time: 16분
chapter: CH12
status: ✅ 대본완성
---

# CH12-02 매출 트렌드와 LTV — 고객 한 명의 가치

## 📌 클립 정보
- **예상시간:** 16분
- **유형:** 화면 녹화
- **준비물:** CH12-01에서 생성한 orders.csv (없으면 아래 스니펫으로 생성)

---

## LTV(고객 생애 가치)란 무엇인가 (3분)

엘티브이(LTV, Lifetime Value)는 고객 한 명이 서비스를 이용하는 동안 발생시키는 총 매출입니다.

**계산 공식:**
`LTV = 평균 월 구독료 × 평균 구독 기간(월)`

엘티브이가 높을수록 한 명의 고객이 더 많은 가치를 가집니다.
엘티브이 > 고객 획득 비용(씨에이씨)이어야 비즈니스가 지속 가능합니다.

---

## 매출 분석 지시 방법 (7분)

> "data/raw/subscriptions.csv를 읽어서 매출 분석을 해줘.
>
> 먼저 월별 총 매출 계산. 구독 단가 29,900원 기준. data/output/monthly_revenue.csv.
>
> 다음으로 코호트별 평균 구독 기간과 엘티브이 계산. 코호트별로 평균 몇 달 구독하는지, 엘티브이는 얼마인지. data/output/ltv_by_cohort.csv.
>
> 세 번째로 차트 세 개 생성. 월별 매출 라인 차트. 코호트별 엘티브이 막대 차트. 신규 고객 vs 기존 고객 매출 비중 스택 막대. charts/ 저장."

---

## 직접 해보기

> **💡 이 클립만 따로 시작한다면** — 먼저 실행해서 데이터 생성
> ```bash
> mkdir -p ~/retention-project/data/raw ~/retention-project/data/output ~/retention-project/charts ~/retention-project/reports && cd ~/retention-project
> python3 -c "
> import pandas as pd, random; random.seed(42); rows = []
> for uid in range(2000):
>     cohort = random.randint(1,12)
>     for month in range(cohort, 13):
>         age = month - cohort
>         ret = 1.0 if age==0 else max(0.05, 0.6*(0.9**(age-1)))
>         if random.random() < ret:
>             rows.append({'user_id':f'U{uid:04d}','cohort_month':f'2024-{cohort:02d}','order_month':f'2024-{month:02d}','revenue':random.randint(15000,80000)})
> pd.DataFrame(rows).to_csv('data/raw/orders.csv',index=False); print('생성 완료:', len(rows), '행')
> "
> ```



**준비**
```bash
cd ~/retention-project
claude
```

**클로드에게 이렇게 말합니다**
```
data/raw/subscriptions.csv로 매출 분석해줘.
구독 단가: 월 29,900원

1. 월별 총 매출 → data/output/monthly_revenue.csv
2. 코호트별 평균 구독기간 + LTV → data/output/ltv_by_cohort.csv
3. 차트 3개:
   - 월별 매출 라인 → charts/monthly_revenue.png
   - 코호트별 LTV 막대 → charts/ltv_cohort.png
   - 신규vs기존 매출 스택 → charts/revenue_stack.png
```

---

## 핵심 정리 (30초)

엘티브이는 고객 한 명의 비즈니스 가치를 수치화합니다.
코호트별 엘티브이를 비교하면 어느 시기 고객이 더 오래, 더 많이 구독하는지 파악합니다.

## 챕터 마무리 (30초)

이것으로 CH12 리텐션 & 매출 분석을 마칩니다.
다음 챕터에서는 인사(HR) 데이터 자동화를 다룹니다.
