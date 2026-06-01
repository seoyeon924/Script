---
tags: #P03 #CH03 #OpenClaw #텔레그램 #자동화플랫폼
time: 15분
part: Part 03
chapter: CH03
status: ✅ 대본완성
---

---

## 🎬 실습 & 촬영 가이드

> 슬라이드 순서 기준으로 언제 무엇을 열고 무엇을 타이핑할지 정리.
> 라이브 데모가 필요한 슬라이드에만 `[데모]` 표시.

---

### 촬영 전 — 필수 준비 체크리스트

| 항목 | 확인 |
|------|------|
| OpenClaw 설치 완료 (`openclaw --version`) | ☐ |
| openclaw 게이트웨이 실행 중 (`openclaw status`) | ☐ |
| 텔레그램 Echo 봇 페어링 완료 | ☐ |
| `openclaw-pipeline-kit` 레포 클론 완료 | ☐ |
| `runs/latest/input/` 안에 샘플 CSV 파일 준비 | ☐ |
| `activity-monitor.html` 브라우저에서 미리 열어두기 (`python3 -m http.server 9001` → `localhost:9001/activity-monitor.html`) | ☐ |
| openclaw.json 에 5명 에이전트 설정 확인 (`cat ~/.openclaw/openclaw.json`) | ☐ |

**사전 촬영 권장:** onboard 마법사 전체 흐름은 한 번 미리 해두고, 촬영 때는 이미 설정된 상태에서 `openclaw status`로 보여주거나 녹화본으로 대체.

---

### CLIP 01 — OpenClaw 소개 & 연결
**슬라이드 순서:** s1 → s2 → s3 → s4 → s5 → s26 → s27 → s28

#### s1~s4 — 슬라이드만 진행 (데모 없음)

---

#### s5 — Claude API 키 연결 `[데모 선택]`

**열 것:** 터미널

보여줄 내용 — 이미 설정된 상태라면 아래 명령어로 연결 확인만:
```bash
openclaw status
# → agents: 5 active, gateway: running 확인
```

새로 연결하는 흐름을 보여준다면:
```bash
openclaw onboard
# → Step 1: Anthropic API key 선택
# → API 키 붙여넣기 (platform.anthropic.com에서 발급)
```

---

#### s26 — openclaw onboard 단계별 `[데모 — 터미널 화면 녹화]`

**열 것:** 터미널 전체화면

실행 명령어:
```bash
openclaw onboard
```

단계별 선택 (슬라이드 s26 내용 그대로 따라가기):
```
Welcome to OpenClaw Setup Wizard

? Select setup mode:
  ❯ QuickStart          ← 선택

? Select AI provider:
  ❯ Anthropic API key   ← 선택
  
? Enter your Anthropic API key:
  sk-ant-xxxxxx         ← 붙여넣기

? Workspace directory: (~/.openclaw/workspace)
                        ← Enter 그대로

? Gateway port: (18789)
                        ← Enter 그대로

? Select channels to enable:
  ❯ ◉ Telegram          ← 스페이스로 선택 후 Enter

? Telegram bot token:
  8233034938:AAHr64...  ← BotFather에서 받은 토큰 붙여넣기

? DM policy: (pairing)
                        ← Enter 그대로

? Select daemon type:
  ❯ Node                ← 선택
```

완료 후 확인:
```bash
openclaw status
# agents: 1 active (main/Echo)
# gateway: running on :18789
```

---

#### s27 — Codex 연결 (비용 절감) `[슬라이드만 / 선택적 데모]`

Codex 설치 보여준다면 터미널에서:
```bash
npm install -g @openai/codex
codex --version
```

onboard에서 OpenAI 선택 흐름 보여준다면:
```
? Select AI provider:
  ❯ OpenAI API key      ← 선택
  
? Enter your OpenAI API key:
  sk-xxxxxx             ← platform.openai.com에서 발급한 키
```

---

#### s28 — 수강생 셋업 `[데모 — 터미널]`

**열 것:** 터미널, `openclaw-pipeline-kit/` 폴더

순서대로 타이핑:
```bash
# 1. 클론
git clone https://github.com/seoyeon924/openclaw-pipeline-kit.git
cd openclaw-pipeline-kit

# 2. 셋업 스크립트
bash setup.sh
# → ✓ echo → ~/.openclaw/workspace/AGENTS.md
# → ✓ aria → ~/.openclaw/workspace-aria/AGENTS.md
# → ✓ sam  → ~/.openclaw/workspace-sam/AGENTS.md
# → ✓ min  → ~/.openclaw/workspace-min/AGENTS.md
# → ✓ evan → ~/.openclaw/workspace-evan/AGENTS.md

# 3. 온보딩 (수강생이 직접)
openclaw onboard
```

---

### CLIP 02 — 에이전트 만들기
**슬라이드 순서:** s6 → s7 → s24 → s8 → s9 → s22 → s21 → s10

#### s6~s7 — 슬라이드만 진행

---

#### s24 — BotFather 봇 만들기 `[데모 — 텔레그램 앱]`

**열 것:** 텔레그램 앱 → @BotFather 검색

순서:
```
1. @BotFather 채팅 열기
2. /newbot 입력
3. 봇 표시 이름: "Echo Agent" 입력
4. username: sy_echo_agent_bot 입력 (반드시 bot으로 끝나야 함)
5. 토큰 발급 → 복사해두기
6. 같은 창에서 /newbot 다시 → Aria, Sam, Min, Evan 반복
```

토큰 openclaw.json에 등록하는 명령어:
```bash
openclaw configure telegram --agent main --token "발급받은토큰"
```

또는 `~/.openclaw/openclaw.json` 직접 열어서 해당 agent botToken 값에 붙여넣기:
```bash
open ~/.openclaw/openclaw.json
```

---

#### s22 — SOUL.md 자동 생성 `[데모 — 텔레그램]`

**열 것:** 텔레그램 → Echo 봇 DM

보낼 프롬프트 (복붙):
```
너는 데이터 분석 팀장 Echo야.
팀원은 Aria(데이터수집), Sam(문제정의/지표), Min(분석), Evan(대시보드/보고서).
분석 요청이 오면 팀원에게 순서대로 위임하고 결과를 나한테 보고하게 해줘.
이 내용을 SOUL.md에 저장해줘.
```

결과 확인:
```bash
cat ~/.openclaw/workspace/SOUL.md
```

---

#### s21 — 프롬프트 한 마디로 SOUL.md `[슬라이드만]`

---

#### s10 — 치트시트 `[슬라이드만]`

---

### CLIP 03 — 크론 자동화 파이프라인 연동
**슬라이드 순서:** s11 → s12 → s13 → s23 → s14 → s15 → s25

#### s11~s12 — 슬라이드만

---

#### s13 — 크론 스케줄 종류 `[슬라이드 + 터미널 확인]`

```bash
# 등록된 크론 목록 확인
openclaw cron list
```

---

#### s23 — 크론 message 프롬프트 `[데모 — 터미널]`

크론 등록 실제 명령어 (복붙용):
```bash
# 매주 월요일 오전 9시 — 주간 분석 자동 실행
openclaw cron add \
  --schedule "0 9 * * 1" \
  --message "~/Projects/openclaw-pipeline-kit/runs/latest/input/ 에 있는 CSV 파일로 /run-pipeline 을 실행하세요. 완료 후 생성된 파일 목록을 알려주세요." \
  --agent main

# 매일 오전 8시 — 데이터 요약
openclaw cron add \
  --every 1d \
  --message "~/Projects/openclaw-pipeline-kit/runs/latest/input/ 최신 파일 분석해서 핵심 지표 3개와 전일 대비 변화 요약해줘." \
  --agent main
```

---

#### s14 — /run-pipeline 연동 `[데모 — 텔레그램 + 터미널]`

**열 것:** 텔레그램 Echo 봇 DM + 터미널

텔레그램에 직접 보낼 프롬프트 (복붙):
```
~/Projects/openclaw-pipeline-kit/runs/latest/input/ 에 있는 CSV 파일로
파이프라인 실행해줘.
완료되면 생성된 파일 목록 알려줘.
```

파이프라인 실행 시작 후 터미널로 전환해서 실시간 로그 보여주기:
```bash
openclaw logs --agent main --follow
```

---

#### s15 — 텔레그램 결과 수신 `[데모 — 텔레그램]`

파이프라인이 완료되면 텔레그램으로 자동 수신되는 메시지 보여주기.
(미리 돌려둔 결과가 있다면 그 화면 캡처 또는 화면 녹화본 사용 권장)

---

#### s25 — 에이전트 팀 협업 `[데모 — 텔레그램]`

**열 것:** 텔레그램 → Echo 봇 DM

보낼 프롬프트 (복붙):
```
분석 작업 들어오면 이 순서로 처리해줘.
1. 네가 먼저 EDA + 문제 정의
2. Min 호출 → 지표 설계 + 대시보드 피드백
3. Evan 호출 → 대시보드 구현 + 마무리
이 순서를 AGENTS.md에 기본 규칙으로 써줘.
```

---

### CLIP 04 — Manager Dashboard
**슬라이드 순서:** s16 → s17 → s18 → s19 → s20

#### s16~s17 — 슬라이드만

---

#### s18~s20 — Dashboard / Gallery / CronJobs 뷰 `[데모 — 브라우저]`

**열 것:** 브라우저 두 탭

탭 1 — activity-monitor.html (파이프라인 모니터):
```bash
cd ~/Projects/openclaw-pipeline-kit
python3 -m http.server 9001
# → 브라우저 localhost:9001/activity-monitor.html
```

탭 2 — openclaw-manager (앱 or 웹):
```bash
openclaw manager
# 또는 슬라이드 내장 영상으로 대체
```

보여줄 포인트:
- **Dashboard 뷰** — Echo/Min/Evan 에이전트 상태 카드 (s18)
- **Gallery 뷰** — 생성된 파일 썸네일 목록 (s19)
- **CronJobs 뷰** — 등록된 크론 스케줄 + 다음 실행 시간 (s20)
- **activity-monitor** — 7단계 파이프라인 완료 상태 + 각 에이전트 출력 카드

---

### 파이프라인 전체 실행 — 라이브 데모 시나리오

> Clip 03에서 한 번에 보여주는 흐름. 사전에 한 번 돌려서 결과 파일이 있는 상태면 더 좋음.

**Step 1.** 샘플 CSV 넣기
```bash
ls ~/Projects/openclaw-pipeline-kit/runs/latest/input/
# sample_sales.csv 확인
```

**Step 2.** 텔레그램 Echo 봇에 프롬프트 전송
```
~/Projects/openclaw-pipeline-kit/runs/latest/input/ 에 있는 CSV 파일로
파이프라인 실행해줘.
완료되면 생성된 파일 목록 알려줘.
```

**Step 3.** activity-monitor.html 브라우저에서 실시간 확인
- `localhost:9001/activity-monitor.html` 열어두기
- 10초마다 자동 갱신 → 완료된 스테이지 ✓ 표시

**Step 4.** 완료 후 outputs 폴더 확인
```bash
ls ~/Projects/openclaw-pipeline-kit/runs/latest/outputs/
# 01_dataset_profile.md
# 02_eda_report.md
# 03_problem_definition.md
# 04_kpi_summary.md
# 05_analysis_report.md
# 06_dashboard.html
# 07_executive_report.md
```

**Step 5.** 브라우저에서 06_dashboard.html 열기
```bash
open ~/Projects/openclaw-pipeline-kit/runs/latest/outputs/06_dashboard.html
```

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
