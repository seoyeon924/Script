---
tags: #P03 #CH03 #OpenClaw #AgentManager #태스크관리
time: 10분
part: Part 03
chapter: CH03
status: ✅ 대본완성
---

# P03-CH03-03 OpenClaw Agent Manager로 태스크 흐름·상태 관리하기

## 📌 클립 정보
- **예상시간:** 10분
- **유형:** 화면 녹화
- **준비물:** OpenClaw, 전 챕터 실습 환경

---

## 통합 파이프라인 구성 (3분)

지금까지 만든 파이프라인들을 OpenClaw에서 통합 운영합니다.

```
OpenClaw 자동화 스케줄
│
├── 매일 오전 9시
│   ├── 마케팅: 어제 광고 데이터 분석 + ROI 알림
│   └── PM: 어제 DAU 확인 + 이상 탐지
│
├── 매주 월요일
│   ├── 마케팅 주간 리포트
│   ├── PM KPI 주간 현황
│   └── HR 이직 위험군 업데이트
│
└── 매월 1일
    ├── 마케팅 월간 예산 추천
    ├── 코호트 리텐션 분석
    └── HR 월간 인사 리포트
```

---

## Agent Manager 태스크 상태 관리 (4분)

**[화면: OpenClaw Agent Manager UI]**

Agent Manager에서 각 에이전트의 상태를 확인합니다:
- 실행 중 / 대기 중 / 완료 / 실패
- 마지막 실행 시간
- 결과 파일 위치

**태스크 상태 확인:**
```bash
openclaw status --all
openclaw logs --agent marketing --last 24h
```

**실패한 작업 재실행:**
```bash
openclaw retry --task task_id
```

---

## 통합 운영 지시 (3분)

```
HEARTBEAT.md에 세 가지 반복 임무를 추가해줘.

매일 임무: 마케팅 data/raw/ 새 파일 확인 후 분석, PM 로그 DAU 계산.

매주 임무 (월요일): 마케팅 주간 리포트, PM 주간 KPI, HR 위험군 업데이트.
세 개 통합 요약을 텔레그램으로 전송.

매월 임무 (1일): 마케팅 예산 추천, 리텐션 분석, HR 월간 리포트.
통합 월간 요약 전송.
```

---

## 핵심 정리 (30초)

OpenClaw Agent Manager로 여러 에이전트의 태스크 흐름과 상태를 한 곳에서 관리합니다.
실패한 작업을 재실행하고 로그를 확인해서 안정적으로 운영합니다.
이것으로 Part 03 시각화 전략 자동 설계를 마칩니다.
