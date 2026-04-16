---
tags: #P02 #CH01 #파일읽기쓰기 #PlanMode #기본워크플로우
time: 10분
part: Part 02
chapter: CH01
status: ✅ 대본완성
---

# P02-CH01-03 파일 읽기·쓰기·실행 & Plan Mode 기초 사용법 정리하기

## 📌 클립 정보
- **예상시간:** 10분
- **유형:** 슬라이드 2장 + 화면 녹화
- **준비물:** 샘플 CSV 파일

---

## 오프닝 (30초)

파일 읽기, 쓰기, 실행 — 이 세 가지 조합으로 대부분의 분석 작업이 가능합니다.
그리고 실행 전에 계획을 먼저 확인하는 Plan Mode를 함께 배웁니다.

---

## 파일 읽기·쓰기·실행 기본 패턴 (4분)

**파일 읽고 저장하기**

```
data/sales.csv 읽어서 월별 매출 합계 계산하고
output/monthly_summary.csv로 저장해줘
```

Claude 동작 순서:
1. sales.csv 읽기
2. pandas 코드 작성
3. 실행
4. output/에 저장

**시각화 추가**

```
방금 만든 파일로 막대 그래프 만들어서
output/chart.png로 저장해줘
```

**파일 수정**

```
scripts/analyze.py에서 날짜 형식 YYYY-MM-DD로 통일해줘
```

변경 사항은 diff 형태로 보여줍니다. 적용 전 확인 가능합니다.

---

## Plan Mode — 실행 전 계획 확인 (4분)

파일 여러 개가 바뀌는 작업은 Plan Mode를 먼저 사용합니다.

```
전체 파이프라인 리팩토링해줘.
실행 전에 계획 먼저 보여줘.
```

Claude 응답 예시:
```
계획:
1. scripts/preprocess.py — 날짜 처리 함수 분리
2. scripts/analyze.py — 중복 코드 3곳 통합
3. config.py 신규 생성 — 설정값 분리
4. README.md 업데이트

진행할까요?
```

"3번 빼고 나머지만 해줘"처럼 조정한 뒤 실행할 수 있습니다.

**Checkpoint — 중간 상태 저장**

```
여기까지 작업 checkpoint로 저장해줘
```

작업 중간 상태를 저장해두고 문제가 생기면 복구합니다.

---

## 핵심 정리 (30초)

Read → Write → Bash 조합이 Claude Code 작업의 기본 패턴입니다.
Plan Mode는 파일 여러 개를 바꾸는 큰 작업에서 실행 전에 계획을 확인하는 방법입니다.
다음 클립에서는 CLAUDE.md — 데이터 시각화 전용 AI 두뇌 설계를 배웁니다.
