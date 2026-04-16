---
tags: #P05 #CH04 #리텐션대시보드 #CLAUDE-md #제작실습
time: 15분
part: Part 05
chapter: CH04
status: 📝 작성필요
---

# P05-CH04-02 리텐션 대시보드 전용 CLAUDE.md + Skill로 제작 실습

## 📌 클립 정보
- **예상시간:** 15분
- **유형:** 슬라이드 + 화면녹화

---

## 오프닝 (30초)

(리텐션 분석 전용 CLAUDE.md와 Retention Analyst Skill로 대시보드 제작 실습)

## 본문

### 리텐션 전용 CLAUDE.md

```markdown
# 리텐션 & 매출 분석 대시보드

## 핵심 계산식
- 코호트 리텐션: 코호트 내 Month N 재구매 사용자 / Month 0 코호트 크기 × 100
- LTV = 평균 주문금액 × 구매 빈도 × 고객 수명
- LTV 간이 계산: Avg Revenue per User × (1 / Churn Rate)

## 대시보드 구성
1. 코호트 리텐션 히트맵
2. LTV 분포 차트
3. 이탈률 추이 라인 차트
4. What-if 시뮬레이터 (리텐션 개선 시 매출 변화)

## 이탈 위험 기준
- Month 1 리텐션 < 40%: 고위험
- Month 3 리텐션 < 20%: 즉각 대응 필요
```

### 대시보드 제작 실습

```
data/raw/orders.csv로 리텐션 분석 대시보드를 만들어줘.

포함:
1. 코호트 리텐션 히트맵 (가입월 × Month 0~6)
2. 코호트별 LTV 계산 및 비교
3. What-if 시뮬레이터:
   - "리텐션 5% 개선 시 연간 추가 매출 = ?"
4. 이탈 위험 코호트 강조 표시

charts/retention_dashboard.html로 저장
```

---

## 핵심 정리 (30초)

리텐션 전용 CLAUDE.md에 이탈 위험 기준과 LTV 계산식을 정의합니다.
What-if 시뮬레이터로 리텐션 개선의 비즈니스 가치를 정량화할 수 있습니다.
