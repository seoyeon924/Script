---
tags: #P03 #CH03 #OpenClaw #텔레그램 #자동화플랫폼
time: 12분
part: Part 03
chapter: CH03
clip: 01
slides: s1,s2,s3,s4,s28,s33,s26,s30,s35
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
**슬라이드 순서:** s1 → s2 → s3 → s4 → s28 → s33 → s26 → s30 → s35

#### s1~s4 — 슬라이드만

---

#### s28 — 수강생 셋업 진입점 `[데모 — 터미널 + Claude Code]`

**열 것:** 터미널 + Claude Code (새 세션)

```bash
# Step 1: zip 압축 해제
mkdir -p ~/Projects && cd ~/Projects
unzip ~/Downloads/openclaw-pipeline-kit.zip

# Step 2: Claude Code로 열기
cd ~/Projects/openclaw-pipeline-kit
claude
```

Claude Code 채팅창에 입력:
```
처음 세팅 시작해줘
```

→ Claude가 CLAUDE.md 읽고 설치 확인 → setup.sh 자동 실행 → onboard는 별도 터미널 안내

> 촬영 팁: openclaw가 이미 설치된 상태에서 찍어도 됨. Claude가 "이미 설치됨" 확인하고 다음 단계로 안내하는 흐름 보여주기

---

#### s33 — 텔레그램 Echo 봇 생성 `[화면: 텔레그램 앱]`

BotFather에서 봇 만드는 흐름 보여주기.
@BotFather → /newbot → 이름 → 유저네임(_bot 필수) → 토큰 복사 보관.

⚠ 토큰은 채팅창·AI 채팅창에 절대 붙여넣기 금지.

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

#### s35 — OpenClaw 대시보드 `[슬라이드만]`

화면 전환 없이 슬라이드만 보여주며 한 줄 언급.

---

#### s28 — 수강생 셋업 `[데모 — 터미널 + Claude Code]`

**열 것:** 터미널 + Claude Code (새 세션)

**Step 1.** zip 압축 해제
```bash
mkdir -p ~/Projects && cd ~/Projects
unzip ~/Downloads/openclaw-pipeline-kit.zip
```

**Step 2.** Claude Code로 폴더 열기
```bash
cd ~/Projects/openclaw-pipeline-kit
claude
```
Claude Code 채팅창에 입력:
```
처음 세팅 시작해줘
```
→ Claude가 CLAUDE.md 읽고 STEP 1 (설치 확인) → STEP 2 (setup.sh 실행) 순서로 안내 시작

**Step 3.** openclaw onboard — 별도 터미널에서 직접 실행
```bash
openclaw onboard
```
⚠ Claude Code 채팅창에서 실행 금지 — API 키·봇 토큰이 Anthropic 서버로 전송됨

**Step 4.** 완료 확인 → 텔레그램 Echo 봇에 파이프라인 실행 요청
```
runs/latest/input/ 에 CSV 있어. 파이프라인 실행해줘.
```

> 촬영 팁: onboard는 미리 해둔 상태에서 `openclaw status`로 완료 화면 보여주고 넘어가도 됨

---

## s1 — 챕터 표지

OpenClaw 업무 자동화 챕터 시작이에요.

이번 챕터에서는 Claude Code 에이전트를 24시간 자동으로 돌리는 방법을 배워요. 클립 세 개로 구성돼 있어요.

---

## s2 — 조감도

Clip 01에서는 OpenClaw 소개랑 텔레그램 연결. Clip 02에서는 파이프라인 실행이랑 크론 자동화. Clip 03에서는 Claude Code로 Agent Manager 앱을 직접 만들어요.

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

## s28 — 수강생 셋업 — 시작하기

**[화면: 터미널 → Claude Code]**

실습 준비 흐름을 정리할게요.

강의자료 페이지에서 `openclaw-pipeline-kit.zip`을 다운받고 `~/Projects/` 안에 압축 해제해요. 에이전트 설정 파일이 이 경로를 기준으로 잡혀있어서 위치를 정확하게 지켜야 해요.

그다음 터미널에서 `cd ~/Projects/openclaw-pipeline-kit` 이동한 다음 `claude`라고 입력해서 Claude Code를 열어요. 그리고 채팅창에 "처음 세팅 시작해줘"라고 입력하면, Claude가 폴더 안에 있는 `CLAUDE.md` 파일을 자동으로 읽고 STEP 1부터 단계별로 안내해줘요. 설치 확인이랑 `setup.sh` 실행까지 Claude가 직접 해줘요.

여기서 딱 한 가지 — `openclaw onboard`는 반드시 Claude Code 채팅창이 아니라 별도 터미널에서 직접 실행해야 해요. API 키랑 텔레그램 봇 토큰을 AI 채팅창에 입력하면 Anthropic 서버로 전송됩니다. 터미널 마법사에서 입력해야 로컬에서만 처리돼요.

그 전에 텔레그램 봇 토큰이 필요한데, 지금 바로 만들어볼게요.

---

## s33 — 텔레그램 Echo 봇 생성 — BotFather

**[화면: 텔레그램 앱]**

텔레그램 봇은 BotFather에서 만들어요.

텔레그램 앱에서 @BotFather를 검색하고 채팅을 열어요. START를 누르고 `/newbot`을 입력하면 봇 이름을 물어봐요. "Echo Agent" 같은 이름 넣으면 돼요.

다음으로 봇 유저네임을 입력해요. 반드시 `_bot`으로 끝나야 해요. `my_echo_agent_bot`처럼요.

유저네임이 승인되면 BotFather가 봇 토큰을 발급해줘요. 이 토큰은 복사해서 안전한 곳에 보관하세요.

중요한 거 하나 — 봇 토큰은 봇의 비밀번호예요. 채팅창, 노션, 슬랙 어디에도 붙여넣으면 안 돼요. AI 채팅창에 입력하면 Anthropic 서버로 전송돼요.

봇은 Echo 하나만 만들면 돼요. Aria·Sam·Min·Evan은 서브에이전트로 Echo가 내부적으로 호출해요. 별도로 만들 필요 없어요.

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

봇은 Echo 하나만 만들면 돼요. 서브 에이전트 Aria·Sam·Min·Evan은 별도 봇 없이 Echo가 내부적으로 호출해요.

다음 클립에서는 파이프라인을 실제로 실행해서 대시보드가 자동으로 만들어지는 과정을 보여드릴게요.

---

## s35 — OpenClaw 대시보드 참고

참고로 OpenClaw 앱을 열면 이런 화면이 나와요.

터미널에서 한 설정을 여기서 GUI로 확인하거나, 나중에 모델이나 채널을 바꾸고 싶을 때 쓸 수 있어요.

지금 당장 안 열어도 되고, 파이프라인 실행하는 데도 필요 없어요.
