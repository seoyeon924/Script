---
tags: #P03 #CH03 #OpenClaw #파이프라인 #크론 #자동화
time: 12분
part: Part 03
chapter: CH03
clip: 02
slides: s8,s21,s13,s23,s14,s15,s29
status: ✅ 대본완성
---

## 🎬 CLIP 02 촬영 가이드
**슬라이드 순서:** s8 → s21 → s13 → s23 → s14 → s15 → s29

#### s8~s13 — 슬라이드만

---

#### s23 — 크론 message 프롬프트 `[데모 — 터미널]`

복붙용:
```bash
# 매주 월요일 오전 9시
openclaw cron add \
  --cron "0 9 * * 1" \
  --message "~/Projects/openclaw-pipeline-kit/runs/latest/input/ 에 있는 CSV 파일로 /run-pipeline 을 실행하세요. 완료 후 생성된 파일 목록을 알려주세요." \
  --agent main

# 매일 오전 8시
openclaw cron add \
  --every 1d \
  --message "~/Projects/openclaw-pipeline-kit/runs/latest/input/ 최신 파일 분석해서 지표 3개와 전일 대비 변화 요약해줘." \
  --agent main
```

등록 확인:
```bash
openclaw cron list
```

---

#### s14 — /run-pipeline 실행 `[데모 — 텔레그램 + 터미널]`

**열 것:** 텔레그램 Echo 봇 DM + 터미널

텔레그램 복붙:
```
~/Projects/openclaw-pipeline-kit/runs/latest/input/ 에 있는 CSV 파일로
파이프라인 실행해줘.
완료되면 생성된 파일 목록 알려줘.
```

로그 확인:
```bash
openclaw logs --follow
```

---

#### s15 — 결과 수신 `[텔레그램 화면 보여주기]`

파이프라인 완료 후 텔레그램으로 자동 수신되는 메시지 보여주기.
미리 돌려둔 결과 화면 캡처 또는 녹화본 사용 권장.

---

#### s29 — 파이프라인 전체 실행 라이브 데모 `[핵심 데모]`

**열 것:** 터미널 + 텔레그램 + 브라우저(activity-monitor)

**Step 1.** CSV 확인
```bash
ls ~/Projects/openclaw-pipeline-kit/runs/latest/input/
```

**Step 2.** 텔레그램 Echo 봇에 전송 (복붙):
```
~/Projects/openclaw-pipeline-kit/runs/latest/input/ 에 CSV 있어.
파이프라인 실행해줘.
완료되면 생성된 파일 목록 알려줘.
```

**Step 3.** `localhost:9001/activity-monitor.html` — 10초마다 자동 갱신, 스테이지 ✓ 확인

**Step 4.** 완료 후 결과 확인
```bash
ls ~/Projects/openclaw-pipeline-kit/runs/latest/outputs/
open ~/Projects/openclaw-pipeline-kit/runs/latest/outputs/06_dashboard.html
```

---

## s8 — 에이전트 5종 구조

이번 실습에서 쓸 에이전트는 다섯 명이에요.

Echo가 메인이에요. 크론 잡 대부분은 Echo가 받고, 파이프라인 실행이랑 결과 텔레그램 전송까지 담당해요.

Aria랑 Sam이 분석 서브 에이전트예요. Aria는 STEP 1-2를 담당해요. 데이터 프로파일링이랑 EDA 보고서를 만들어요. Sam은 STEP 3-4예요. 문제 정의랑 KPI 요약을 작성해요.

Min이랑 Evan도 서브 에이전트예요. Min은 데이터 수집 전담이고, Evan은 특정 프로젝트 대시보드 구현을 담당해요.

AGENTS.md 파일에 각자 역할이 정의돼 있어요. Echo가 이 파일을 읽고 각 에이전트한테 일을 나눠요.

---

## s21 — 크론 메시지가 대시보드를 만드는 방법

**[화면: 터미널]**

흐름은 단순해요. 크론이 정해진 시간에 Echo한테 메시지를 보내요. Echo가 메시지를 받아서 파이프라인을 실행하고, 완료되면 텔레그램으로 결과를 보내요.

사람이 직접 채팅하는 것과 완전히 같은 형식이에요. 크론이 정해진 시간에 자동으로 전송할 뿐이에요.

크론 메시지에 파일 경로랑 `/run-pipeline` 명령어를 넣으면 돼요. 그러면 매주 월요일 오전 9시에 알아서 대시보드가 만들어져요.

---

## s13 — 크론 스케줄 종류

**[화면: 터미널]**

크론 스케줄 방식이 두 가지예요.

`--every`는 간단한 주기예요. `1d`면 매일, `2h`면 2시간마다예요.

`--cron`은 cron 표현식이에요. `0 9 * * 1`이면 매주 월요일 오전 9시예요. 시간을 정확하게 지정하고 싶을 때 써요.

크론이 에이전트에게 보내는 건 `message` 필드예요. 사람이 직접 보내는 것과 완전히 같은 형식이에요.

---

## s23 — 크론 message — 바로 쓸 수 있는 프롬프트

**[화면: 터미널]**

프롬프트 작성 팁 세 가지예요.

파일 경로를 절대경로로 명시해요. 상대경로는 실패 가능성 있어요.

완료 조건을 명시해요. "완료 후 파일 목록 출력"처럼 끝내는 조건이 없으면 에이전트가 안 멈출 수 있어요.

슬래시 명령어를 직접 넣어요. `/run-pipeline` 같은 명령어를 프롬프트 안에 직접 넣으면 돼요.

---

## s14 — /run-pipeline 자동 실행 연동

**[화면: 텔레그램 + 터미널]**

openclaw-pipeline-kit을 OpenClaw 크론에 연결하는 거예요.

크론이 매주 월요일 오전 9시에 Echo에게 메시지를 자동 전송해요. Echo가 받아서 `/run-pipeline`을 실행하고, 완료되면 결과를 텔레그램으로 돌려보내요.

사람이 직접 보내는 것과 완전히 같은 형식이에요. 크론이 정해진 시간에 자동으로 전송할 뿐이에요.

---

## s15 — 텔레그램 결과 전송 & delivery

**[화면: 텔레그램]**

파이프라인이 완료되면 텔레그램으로 자동 알림이 와요.

흐름은 세 단계예요. 크론 시간이 되면 OpenClaw가 에이전트를 깨워서 메시지를 전달해요. 에이전트가 작업을 완료하면 텔레그램으로 결과를 자동 전송해요. 컴퓨터 앞에 있을 필요 없이 텔레그램으로 결과를 수신하면 돼요.

작업은 에이전트가, 결과는 텔레그램으로 수신이에요.

---

## s29 — 실전 실행 — CSV 넣고 텔레그램으로 시작하기

**[화면: 터미널 → 텔레그램 → 브라우저]**

실제로 어떻게 돌아가는지 흐름을 정리할게요.

CSV 파일을 `runs/latest/input/` 폴더에 넣어요. 어떤 CSV든 상관없어요.

텔레그램 Echo 봇에 "runs/latest/input/ 에 CSV 있어. 파이프라인 실행해줘." 보내면 돼요.

그러면 다섯 명이 순서대로 일을 나눠요. Aria가 데이터 프로파일링이랑 EDA 보고서를 만들고, Sam이 문제 정의랑 KPI 요약을 써요. Min이 분석 보고서를 완성하면, Evan이 대시보드랑 임원 보고서를 마무리해요.

브라우저에서 `activity-monitor.html` 열어두면 10초마다 자동 갱신되면서 완료된 스테이지가 ✓로 바뀌어요.

다 끝나면 텔레그램으로 결과 파일 목록이 자동으로 와요.

CSV 하나 넣고 메시지 한 줄 보내면 대시보드까지 자동 완성이에요.

다음 클립에서는 이 에이전트 전체를 한 화면에서 모니터링하는 Agent Manager를 Claude Code로 직접 만들어요.
