---
tags: #P06 #CH01 #포트폴리오 #Antigravity #빌드
time: 15분
part: Part 06
chapter: CH01
status: 📝 작성필요
---

# P06-CH01-02 Antigravity + Claude Code로 포트폴리오 페이지 빌드하기

## 📌 클립 정보
- **예상시간:** 15분
- **유형:** 화면녹화

---

## 오프닝 (30초)

(Stitch에서 내보낸 디자인 시안을 Antigravity + Claude Code로 실제 동작하는 페이지로 빌드)

## 본문

### Antigravity에서 Stitch 시안 임포트

```
Stitch에서 내보낸 portfolio-design.html을 기반으로
실제 동작하는 포트폴리오 페이지를 빌드해줘.

작업:
1. Stitch 시안의 레이아웃과 색상 유지
2. 프로젝트 카드에 실제 대시보드 iframe 임베드
   - charts/marketing_dashboard.html
   - charts/ab_test_dashboard.html
   - charts/pm_dashboard.html
   - charts/retention_dashboard.html
   - charts/hr_dashboard.html
3. 각 카드에 프로젝트 설명 추가:
   - 사용 기술, 데이터 규모, 핵심 인사이트

index.html로 저장
```

### 프로젝트 카드 데이터 구성

```
포트폴리오 프로젝트 카드 5개를 작성해줘.

각 카드:
- 제목
- 설명 (2~3문장, 비즈니스 임팩트 중심)
- 사용 기술 태그
- 대시보드 링크

프로젝트:
1. 마케팅 ROI 대시보드 — 채널별 성과 분석 + 시계열 예측
2. A/B 테스트 분석 대시보드 — 통계적 유의성 + 세그먼트 분석
3. PM KPI 대시보드 — DAU, 리텐션, 이상 탐지 자동화
4. 리텐션 & LTV 분석 — 코호트 히트맵 + What-if 시뮬레이터
5. HR 인사 대시보드 — 이직 예측 + 성과 분포 분석
```

---

## 핵심 정리 (30초)

Antigravity에서 Stitch 시안을 불러와 Claude Code로 실제 대시보드를 임베드합니다.
프로젝트 카드는 비즈니스 임팩트 중심으로 작성해 채용 담당자에게 어필합니다.
