---
tags: #P03 #CH03 #OpenClaw #텔레그램 #자동화플랫폼
time: 15분
part: Part 03
chapter: CH03
status: ✅ 대본완성
---

# P03-CH03-01 OpenClaw 이해 & 텔레그램 에이전트 연결하기

## 📌 클립 정보
- **예상시간:** 15분
- **유형:** 슬라이드 3장 + 화면 녹화
- **준비물:** OpenClaw 설치 완료

---

## OpenClaw란 무엇인가 (4분)

OpenClaw는 AI 에이전트를 서비스처럼 운영하는 플랫폼입니다.

지금까지 배운 Claude Code는 직접 터미널에서 실행하고 지시를 입력했습니다.
OpenClaw는 이 과정을 자동화합니다.

| 항목 | Claude Code | OpenClaw |
|------|-----------|---------|
| 실행 방식 | 터미널에서 직접 입력 | 스케줄에 따라 자동 실행 |
| 트리거 | 사람이 지시 | 시간, 이벤트, 메시지 |
| 결과 전달 | 터미널 출력 | 텔레그램, 슬랙, 이메일 |
| 운영 | 사람이 항상 켜둬야 함 | 백그라운드 자동 실행 |

**비유:**
Claude Code는 직접 고용한 직원입니다. 지시를 내리면 일합니다.
OpenClaw는 그 직원에게 자동화 시스템을 붙인 것입니다.
매일 오전 9시에 자동으로 출근해서 정해진 일을 하고 결과를 보고합니다.

---

## OpenClaw 핵심 기능 (4분)

**크론(Cron) 스케줄러**
"매일 오전 8시에 실행" 같은 반복 작업을 등록합니다.

**텔레그램 연동**
텔레그램으로 결과를 자동 전송합니다.
"분석 완료됐습니다. SNS ROI 143%"처럼 직접 알림이 옵니다.

**메시지 트리거**
텔레그램에서 "분석 실행"이라고 보내면 즉시 실행됩니다.

**워크스페이스 격리**
마케팅 분석 에이전트와 HR 분석 에이전트가 섞이지 않습니다.

---

## 텔레그램 에이전트 연결하기 (5분)

```bash
# OpenClaw 상태 확인
openclaw status

# 텔레그램 봇 연결
openclaw connect telegram --token YOUR_BOT_TOKEN

# 첫 번째 자동화 크론 작업 등록
openclaw cron add --every 1d --message "data/raw/ 최신 파일로 8단계 파이프라인 실행해줘" --announce
```

텔레그램에서 이렇게 보내면 즉시 실행됩니다:
```
지금 마케팅 파이프라인 실행해줘.
```

---

## 직접 해보기

```bash
# 크론 작업 목록 확인
openclaw cron list

# 텔레그램으로 테스트 메시지
# → 텔레그램 봇에 "안녕" 전송
```

---

## 핵심 정리 (30초)

OpenClaw는 Claude Code 에이전트를 자동화 서비스로 운영하는 플랫폼입니다.
크론 스케줄, 텔레그램 연동, 워크스페이스 격리가 핵심 기능입니다.
다음 클립에서는 대시보드 자동 생성과 주간 리포트 운영을 다룹니다.

---

## s26 — openclaw onboard 단계별 선택

터미널에서 `openclaw onboard` 실행하면 마법사가 시작돼요.

**Step 0 — Mode**: QuickStart 선택하세요. 기본값 자동 적용돼요.

**Step 1 — Auth**: `Anthropic API key` 선택하고 콘솔에서 발급한 키 붙여넣기. API 키는 `platform.anthropic.com`에서 발급해요.

**Step 2, 3 — Workspace / Gateway**: 전부 Enter. 건드릴 것 없어요.

**Step 4 — Channels**: Telegram 선택하고 BotFather에서 받은 토큰 붙여넣기. DM policy는 `pairing` 그대로 Enter.

**Step 5 — Daemon**: Node 선택.

여기까지 하면 OpenClaw가 백그라운드 서비스로 자동 실행돼요.

---

## s27 — 비용 고려 — Codex 연결하기

Claude Code 크레딧으로 운영하면 파이프라인 1회에 $1~1.5 수준이에요. 자주 돌리면 비용이 쌓이죠.

요즘은 **OpenAI Codex CLI**를 연결해서 쓰는 분들도 많아요. GPT-4o-mini 기준으로 1회에 $0.1~0.3 수준이라 반복 실행에 유리해요.

연결 방법은 세 단계예요.

```bash
# 1. Codex 설치
npm install -g @openai/codex
```

2단계는 `platform.openai.com`에서 API 키 발급. GPT-4o-mini 권장해요.

3단계는 `openclaw onboard` Step 1에서 `OpenAI API key` 선택하고 키 붙여넣기.

품질이 중요한 작업은 Claude, 반복 실행 크론은 Codex로 나눠 쓰는 것도 방법이에요.

---

## s28 — 수강생 셋업 — 따라하기

실습 시작 전에 레포 클론하고 명령어 두 개만 실행하면 돼요.

```bash
# 1. 레포 클론
git clone [강의 자료 링크]
cd openclaw-pipeline-kit

# 2. 셋업 스크립트 — AGENTS.md 자동 복사
bash setup.sh

# 3. 온보딩
openclaw onboard
```

`bash setup.sh` 한 번이면 Echo, Aria, Sam, Min, Evan 워크스페이스 폴더가 자동으로 생성되고 AGENTS.md가 복사돼요. 수강생은 온보딩이랑 BotFather 봇 만들기만 직접 하면 돼요.

데이터 파일은 `runs/latest/input/`에 CSV 넣고, 텔레그램 Echo 봇에 "파이프라인 실행해줘. input/ 에 파일 있어." 보내면 바로 시작돼요.
