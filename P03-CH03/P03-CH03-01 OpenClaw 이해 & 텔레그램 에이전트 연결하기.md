---
tags: #P03 #CH03 #OpenClaw #텔레그램 #자동화플랫폼
time: 15분
part: Part 03
chapter: CH03
clip: 01
slides: s1,s2,s3,s4,s5,s26,s27,s28
status: ✅ 대본완성
---

## 🎬 촬영 전 — 전체 준비 체크리스트

> 4개 클립 모두 촬영 시작 전에 한 번만 확인.

| 항목 | 확인 |
|------|------|
| OpenClaw 설치 완료 (`openclaw --version`) | ☐ |
| openclaw 게이트웨이 실행 중 (`openclaw status`) | ☐ |
| 텔레그램 Echo 봇 페어링 완료 | ☐ |
| `openclaw-pipeline-kit` 레포 클론 완료 | ☐ |
| `runs/latest/input/` 안에 샘플 CSV 파일 준비 | ☐ |
| `activity-monitor.html` 브라우저 탭 미리 열기 (`python3 -m http.server 9001`) | ☐ |
| `~/.openclaw/openclaw.json` 에 5명 에이전트 설정 확인 | ☐ |

**사전 촬영 권장:** onboard 마법사는 미리 한 번 해두고, 촬영 때는 완료된 상태에서 `openclaw status`로 보여주거나 녹화본으로 대체.

---

## 🎬 CLIP 01 촬영 가이드
**슬라이드 순서:** s1 → s2 → s3 → s4 → s5 → s26 → s27 → s28

#### s1~s4 — 슬라이드만

---

#### s5 — Claude API 키 연결 `[데모 선택]`

**열 것:** 터미널

```bash
openclaw status
# → agents: 5 active, gateway: running 확인
```

새로 연결하는 흐름을 보여준다면:
```bash
openclaw onboard
# Step 1: Anthropic API key 선택 → 키 붙여넣기
```

---

#### s26 — openclaw onboard 단계별 `[데모 — 터미널 전체화면]`

**⚠ 보안 주의:** API 키와 봇 토큰은 반드시 터미널 마법사에서만 입력. AI 채팅창에 붙여넣으면 Anthropic 서버로 전송됨.

**열 것:** 터미널 전체화면

```bash
# 1. Echo (메인) 설정
openclaw onboard
```
```
? Mode:       ❯ QuickStart
? Auth:       ❯ Anthropic API key
? API key:    sk-ant-xxxxxx  ← 붙여넣기
? Workspace:  Enter 그대로
? Gateway:    Enter 그대로
? Channels:   ◉ Telegram
? Bot token:  [Echo 봇 토큰]  ← BotFather에서 복사한 것
? DM policy:  pairing → Enter
? Daemon:     ❯ Node
```

```bash
# 2. 나머지 4명 — token-file 사용 (shell 히스토리에 토큰 안 남음)
echo "Aria봇토큰" > /tmp/t.txt && openclaw channels add --channel telegram --account aria --token-file /tmp/t.txt && rm /tmp/t.txt
echo "Sam봇토큰"  > /tmp/t.txt && openclaw channels add --channel telegram --account sam  --token-file /tmp/t.txt && rm /tmp/t.txt
echo "Min봇토큰"  > /tmp/t.txt && openclaw channels add --channel telegram --account min  --token-file /tmp/t.txt && rm /tmp/t.txt
echo "Evan봇토큰" > /tmp/t.txt && openclaw channels add --channel telegram --account evan --token-file /tmp/t.txt && rm /tmp/t.txt
```

완료 확인:
```bash
openclaw status
# agents: 5 active / gateway: running on :18789
```

---

#### s27 — Codex 연결 `[선택적 데모]`

```bash
npm install -g @openai/codex
codex --version
```

onboard에서 OpenAI 선택 시:
```
? Select AI provider:  ❯ OpenAI API key
? API key:             sk-xxxxxx  ← platform.openai.com 발급
```

---

#### s28 — 수강생 셋업 `[데모 — 터미널]`

```bash
git clone https://github.com/seoyeon924/openclaw-pipeline-kit.git
cd openclaw-pipeline-kit
bash setup.sh
# ✓ echo → ~/.openclaw/workspace/AGENTS.md
# ✓ aria → ~/.openclaw/workspace-aria/AGENTS.md
# ✓ sam  → ~/.openclaw/workspace-sam/AGENTS.md
# ✓ min  → ~/.openclaw/workspace-min/AGENTS.md
# ✓ evan → ~/.openclaw/workspace-evan/AGENTS.md
openclaw onboard
```

---

## s1 — 챕터 표지

OpenClaw 업무 자동화 챕터 시작이에요.

이번 챕터에서는 Claude Code 에이전트를 24시간 자동으로 돌리는 방법을 배워요. 클립 네 개로 구성돼 있어요.

---

## s2 — 조감도

Clip 01에서 OpenClaw 소개랑 연결을 하고, Clip 02에서 에이전트를 직접 만들어요. Clip 03에서 크론 스케줄로 자동 실행을 연결하고, Clip 04에서 Manager Dashboard로 전체를 모니터링해요.

---

## s3 — CLIP 01 섹션 브레이크

첫 번째 클립이에요. OpenClaw가 뭔지, Claude Code랑 어떻게 다른지, 텔레그램이랑 어떻게 연결되는지 다뤄요.

---

## s4 — OpenClaw란?

OpenClaw는 AI 에이전트를 서비스처럼 운영하는 플랫폼이에요.

Claude Code는 직접 터미널에서 실행하고 지시를 입력해야 했어요. OpenClaw는 이 과정을 자동화해요.

Claude Code는 직접 고용한 직원이에요. 지시를 내리면 일합니다. OpenClaw는 그 직원에게 자동화 시스템을 붙인 거예요. 매일 오전 9시에 자동으로 출근해서 정해진 일을 하고 결과를 텔레그램으로 보고해요.

핵심 기능 세 가지예요. 크론 스케줄러로 반복 작업을 등록하고, 텔레그램으로 결과를 자동 전송하고, 워크스페이스 격리로 에이전트끼리 섞이지 않아요.

---

## s5 — Claude API 키 연결

**[화면: 터미널]**

OpenClaw를 처음 쓰려면 API 키 연결이 필요해요. `openclaw onboard`로 마법사를 실행하면 돼요. Anthropic API 키는 `platform.anthropic.com`에서 발급해요. Claude.ai 구독이랑 별개로 API 크레딧이 따로 필요해요.

---

## s26 — openclaw onboard 단계별 선택

**[화면: 터미널 전체화면]**

API 키랑 봇 토큰은 AI 채팅창에 절대 넣으면 안 돼요. Anthropic 서버로 전송돼요. 터미널 마법사에서만 입력하면 로컬에서만 처리돼요.

터미널에서 `openclaw onboard` 실행하면 마법사가 시작돼요.

**Mode** — QuickStart 선택.

**Auth** — Anthropic API key 선택하고 `platform.anthropic.com`에서 발급한 키 붙여넣기.

**Workspace / Gateway** — 전부 Enter.

**Channels** — Telegram 선택하고 Echo 봇 토큰 붙여넣기. DM policy는 pairing 그대로 Enter.

**Daemon** — Node 선택.

Echo 설정이 끝나면 나머지 4명도 같은 방식으로 등록해요.

```bash
# token-file 방식 — 토큰이 shell 히스토리에 안 남음
echo "Aria봇토큰" > /tmp/t.txt && openclaw channels add --channel telegram --account aria --token-file /tmp/t.txt && rm /tmp/t.txt
# sam / min / evan 동일하게 반복
```

`--token-file`에 임시 파일을 쓰고 바로 삭제해요. 토큰이 `~/.zsh_history`에 남지 않아요.

---

## s27 — 비용 고려 — Codex 연결하기

Claude Code 크레딧으로 운영하면 파이프라인 1회에 $1~1.5 수준이에요. 자주 돌리면 비용이 쌓이죠.

요즘은 OpenAI Codex CLI를 연결해서 쓰는 분들도 많아요. GPT-4o-mini 기준으로 1회에 $0.1~0.3 수준이라 반복 실행에 유리해요.

설치는 `npm install -g @openai/codex` 한 줄이에요. `platform.openai.com`에서 API 키 발급하고, `openclaw onboard` Step 1에서 OpenAI API key 선택하고 키 붙여넣기.

품질이 중요한 작업은 Claude, 반복 실행 크론은 Codex로 나눠 쓰는 것도 방법이에요.

---

## s28 — 수강생 셋업 — 따라하기

**[화면: 터미널]**

실습 시작 전에 레포 클론하고 명령어 두 개만 실행하면 돼요.

`bash setup.sh` 한 번이면 Echo, Aria, Sam, Min, Evan 워크스페이스 폴더가 자동으로 생성되고 AGENTS.md가 복사돼요. 수강생은 온보딩이랑 BotFather 봇 만들기만 직접 하면 돼요.

데이터 파일은 `runs/latest/input/`에 CSV 넣고, 텔레그램 Echo 봇에 "파이프라인 실행해줘. input/ 에 파일 있어." 보내면 바로 시작돼요.
