---
tags: #P05 #CH02 #AB테스트 #대시보드기획 #세그먼트분석
time: 15분
part: Part 05
chapter: CH02
status: ✅ 대본완성
---

# P05-CH02-01 A/B test 대시보드 기획안 (A/B 테스트 & 세그먼트 분석 & 의사결정)

## 📌 클립 정보
- **예상시간:** 15분
- **유형:** 슬라이드 3장 + 화면 녹화
- **준비물:** Claude Code

---

## 오프닝 (30초)

"버튼 색 바꾸면 클릭률 올라갈 것 같은데요"라고 말하면 기획자가 뭐라고 하죠?
"데이터 보여주세요."
A/B 테스트가 그 데이터입니다. 이번 챕터에서 Claude Code로 분석까지 자동화합니다.

---

## A/B 테스트란 무엇인가 (3분)

두 가지 버전 중 어느 것이 더 나은지 데이터로 검증하는 방법입니다.

**예시:**
- 버튼 색상 A(파랑) vs B(초록) — 클릭률 비교
- 이메일 제목 A vs B — 열람률 비교
- 랜딩 페이지 레이아웃 A vs B — 전환율 비교

**핵심 개념:**
- 통계적 유의성: p-value < 0.05 → 차이가 우연이 아닐 가능성 95% 이상
- 신뢰구간: "A그룹 전환율: 3.2% ± 0.4%"
- 샘플 크기: 충분히 많은 대상이 필요

---

## 대시보드 기획 — 3개 레이어 (6분)

**레이어 1 — A/B 테스트 결과 (현황 파악)**
- KPI 카드: A그룹 전환율, B그룹 전환율, 개선율
- 그룹별 전환율 비교 막대 차트
- p-value 및 통계적 유의성 표시

**레이어 2 — 세그먼트 분석**
- 연령대별, 기기별, 채널별 그룹 성과 차이
- 어떤 세그먼트에서 B버전이 특히 효과적인가

**레이어 3 — 의사결정 지원**
- B버전 적용 시 예상 매출 증가 시뮬레이션
- 필요 샘플 크기 계산 (현재 충분한가?)
- 권고: "전환 → 유지 → 추가 실험" 중 선택

---

## 샘플 데이터 생성 (3분)

```bash
mkdir -p ~/ab-test/data/raw ~/ab-test/charts ~/ab-test/reports
cd ~/ab-test
python3 -c "
import pandas as pd, random; random.seed(42); rows = []
for i in range(10000):
    grp = 'A' if i < 5000 else 'B'
    opened = 1 if random.random() < (0.23 if grp=='A' else 0.27) else 0
    converted = 1 if opened and random.random() < (0.032 if grp=='A' else 0.041) else 0
    rows.append({'user_id':f'U{i:05d}','group':grp,'opened':opened,'converted':converted})
pd.DataFrame(rows).to_csv('data/raw/ab_test.csv',index=False); print('생성 완료')
"
claude
```

---

## 핵심 정리 (30초)

A/B 테스트 대시보드는 결과 현황 → 세그먼트 분석 → 의사결정 지원의 3개 레이어로 구성합니다.
다음 클립에서는 전용 CLAUDE.md와 Skill로 대시보드를 제작합니다.
