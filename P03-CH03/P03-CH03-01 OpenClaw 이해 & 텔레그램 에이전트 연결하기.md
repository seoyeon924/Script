---
tags: #P03 #CH03 #OpenClaw #텔레그램 #자동화플랫폼
time: 12분
part: Part 03
chapter: CH03
clip: 01
slides: s1,s2,s3,s4,s5,s26,s30,s28
status: ✅ 대본완성
---

## 🎬 촬영 전 — 전체 준비 체크리스트

> 3개 클립 모두 촬영 시작 전에 한 번만 확인.

| 항목 | 확인 |
|------|------|
| OpenClaw 설치 완료 (`openclaw --version`) | ☐ |
| openclaw 게이트웨이 실행 중 (`openclaw status`) | ☐ |
| 텔레그램 Echo 봇 페어링 완료 | ☐ |
| `openclaw-pipeline-kit` 레포 클론 완료 | ☐ |
| `runs/latest/input/` 안에 샘플 CSV 파일 준비 | ☐ |
| `activity-monitor.html` 브라우저 탭 미리 열기 (`python3 -m http.server 9001`) | ☐ |
| `~/.openclaw/openclaw.json` 에 Echo 에이전트 설정 확인 | ☐ |
| **파이프라인 1회 미리 실행 → s15용 텔레그램 결과 화면 캡처 저장** | ☐ |
| **Node.js 18+ 설치 확인 (`node --version`)** | ☐ |
| **Rust 설치 확인 (`rustc --version`) → CLIP 03 Tauri 빌드 필요** | ☐ |
| **`manager/PROMPT.md` 파일 존재 확인** | ☐ |

**사전 촬영 권장:** onboard 마법사는 미리 한 번 해두고, 촬영 때는 완료된 상태에서 `openclaw status`로 보여주거나 녹화본으로 대체.

---

## 🎬 CLIP 01 촬영 가이드
**슬라이드 순서:** s1 → s2 → s3 → s4 → s5 → s26 → s30 → s28

#### s1~s4 — 슬라이드만

---

#### s5 — Claude API 키 연결 `[데모 선택]`

**열 것:** 터미널

```bash
openclaw status
# → agents: active, gateway: running 확인
```

---

#### s26 — openclaw onboard 단계별 `[데모 — 터미널 전체화면]`

**⚠ 보안 주의:** API 키와 봇 토큰은 반드시 터미널 마법사에서만 입력. AI 채팅창에 붙여넣으면 Anthropic 서버로 전송됨.

**열 것:** 터미널 전체화면

```bash
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
```

---

#### s30 — Daemon 선택 + 완료 확인 `[데모 — 터미널]`

```
? Daemon:     ❯ Node
```

완료 확인:
```bash
openclaw status
# agents: active / gateway: running on :18789
```

텔레그램 Echo 봇에 "안녕" 전송 → 답장 오면 연결 완료.

---

#### s28 — 수강생 셋업 `[데모 — 터미널]`

```bash
git clone https://github.com/seoyeon924/openclaw-pipeline-kit.git
cd openclaw-pipeline-kit
bash setup.sh
openclaw onboard      # Echo 봇 토큰만 입력
```

텔레그램 Echo 봇에 메시지 전송 → 답장 확인으로 마무리.

---

## s1 — 챕터 표지

OpenClaw 업무 자동화 챕터 시작이에요.

이번 챕터에서는 Claude Code 에이전트를 24시간 자동으로 돌리는 방법을 배워요. 클립 세 개로 구성돼 있어요.

---

## s2 — 조감도

Clip 01에서 OpenClaw 소개랑 연결을 해요. Clip 02에서 파이프라인 실행이랑 크론 자동화를 연결해요. Clip 03에서 Claude Code로 Agent Manager 앱을 직접 만들어요.

---

## s3 — CLIP 01 섹션 브레이크

첫 번째 클립이에요. OpenClaw가 뭔지, Claude Code랑 어떻게 다른지, 텔레그램이랑 어떻게 연결되는지 다뤄요.

---

## s4 — OpenClaw란?

OpenClaw는 AI 에이전트를 서비스처럼 운영하는 플랫폼이에요.

Claude Code는 직접 터미널에서 실행하고 지시를 입력해야 했어요. OpenClaw는 이 과정을 자동화해요.

Claude Code는 직접 고용한 직원이에요. 지시를 내리면 일합니다. OpenClaw는 그 직원에게 자동화 시스템을 붙인 거예요. 매일 오전 9시에 자동으로 출근해서 정해진 일을 하고 결과를 텔레그램으로 보고해요.

기능은 세 가지예요. 크론 스케줄러로 반복 작업을 등록하고, 텔레그램으로 결과를 자동 전송하고, 워크스페이스 격리로 에이전트끼리 섞이지 않아요.

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

텔레그램 봇은 Echo 하나만 만들면 돼요. 나머지 서브 에이전트는 Echo가 내부적으로 호출해요.

---

## s30 — Daemon 선택 & 연결 완료

**[화면: 터미널]**

마지막 단계예요. Daemon은 Node 선택하면 돼요.

완료되면 `openclaw status`로 확인해요. gateway running이랑 agent Echo active가 뜨면 됩니다.

텔레그램 Echo 봇에 "안녕"이라고 보내보세요. 에이전트가 답장하면 연결이 완료된 거예요.

텔레그램 봇은 Echo 하나만 만들면 돼요. 서브 에이전트 Aria·Sam·Min·Evan은 별도 봇 없이 Echo가 내부적으로 호출해요.

다음 슬라이드에서는 수강생 셋업 전체 흐름을 정리할게요.

---

## s28 — 수강생 셋업 — 따라하기

**[화면: 터미널]**

실습 시작 전에 레포 클론하고 명령어 두 개만 실행하면 돼요.

`bash setup.sh` 한 번이면 Echo·Aria·Sam·Min·Evan 다섯 개 워크스페이스 폴더가 자동으로 생성되고 AGENTS.md가 복사돼요.

이후 `openclaw onboard`로 Echo 봇 토큰만 입력하면 끝이에요. 서브 에이전트는 별도 봇 없이 Echo가 내부적으로 호출해요.

텔레그램 Echo 봇에 "안녕"이라고 보내보세요. 에이전트가 답장하면 연결 완료예요.

다음 클립에서는 파이프라인 실행이랑 크론 자동화를 연결해요.
