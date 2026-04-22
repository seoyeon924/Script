---
tags: #P01 #CH02 #설치 #환경세팅 #Antigravity
time: 10분
part: Part 01
chapter: CH02
status: ✅ 대본완성
---

# P01-CH02-01 Claude Code 설치하기

## 📌 클립 정보
- **예상시간:** 10분
- **유형:** 슬라이드 + 화면녹화
- **준비물:** 맥 또는 윈도우 PC, claude.ai 계정 (Pro $20 또는 Max $100 구독)

---

## 오프닝 (1분)

이번 파트에서는 Claude Code를 설치하고, 우리가 강의 내내 쓸 작업 환경을 세팅합니다.

잠깐, 여기서 중요한 이야기를 먼저 하겠습니다.

많은 분들이 Claude Code를 "터미널에서 쓰는 도구"로 알고 계세요.
맞습니다. 하지만 이 강의에서는 다르게 접근합니다.

**우리는 Antigravity 에디터 안에서 Claude Code를 씁니다.**

에디터 오른쪽 채팅 패널에서 Claude와 자연어로 대화하고,
터미널은 Claude가 실제로 코드를 실행할 때, 또는 꼭 필요한 명령어를 입력할 때만 씁니다.

이렇게 하면 뭐가 좋냐고요?
화면 분할 없이 에디터 한 곳에서 파일 보면서, 채팅하고, 결과를 바로 확인합니다.
데이터 시각화에 딱 맞는 환경입니다.

그러면 지금 바로 설치부터 시작합니다.

---

## Claude Code가 뭔지 30초 정리 (1분)

설치 전에 Claude Code가 정확히 뭔지만 짚고 넘어갑니다.

Claude Code는 AI 에이전트입니다.
단순히 질문에 답하는 게 아니라, 내 컴퓨터 파일을 직접 읽고, 코드를 실행하고, 결과물을 저장합니다.

ChatGPT와 뭐가 다르냐면:

| | ChatGPT (웹) | Claude Code |
|--|--|--|
| 파일 처리 | 업로드한 파일만 | 폴더 전체를 자동으로 읽음 |
| 코드 실행 | 직접 안 함 | 내 컴퓨터에서 직접 실행 |
| 결과 저장 | 복사해서 붙여넣기 | 파일로 자동 저장 |
| 기억 | 대화가 끝나면 초기화 | CLAUDE.md로 영구 기억 |

CSV 파일을 던져주면, 읽고, 분석하고, 차트 만들고, 저장까지 혼자 합니다.
그게 Claude Code입니다.

---

## 설치 전 준비 (1분)

두 가지만 확인합니다.

**1. claude.ai 계정**
Pro ($20/월) 또는 Max ($100/월) 구독이 필요합니다.
Pro는 하루 사용 한도가 꽤 빨리 찹니다.
본격적으로 쓸 거라면 Max를 추천합니다. Max $100이 가장 균형이 좋습니다.

**2. 운영체제 확인**
- macOS 13 (Ventura) 이상
- Windows 10 (64비트) 이상
- 리눅스는 Ubuntu 20.04 이상

macOS 버전은 왼쪽 상단 사과 → 이 Mac에 관하여에서 확인할 수 있습니다.

---

## 설치 (3분)

### macOS

터미널을 열고 아래 명령어를 그대로 붙여넣습니다.

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Homebrew가 설치되어 있다면 이 방법도 됩니다.

```bash
brew install --cask claude-code
```

설치가 끝나면 버전을 확인합니다.

```bash
claude --version
```

숫자가 나오면 설치 완료입니다.

### Windows

PowerShell을 관리자 권한으로 열고:

```powershell
irm https://claude.ai/install.ps1 | iex
```

또는 winget으로:

```powershell
winget install Anthropic.ClaudeCode
```

**주의:** npm으로 설치하는 방법은 공식적으로 deprecated입니다. 위 방법을 쓰세요.

---

## 로그인 (2분)

설치 후 처음 `claude`를 실행하면 브라우저가 자동으로 열립니다.

```bash
claude
```

claude.ai 계정으로 로그인하면 인증이 완료됩니다.
터미널로 돌아오면 프롬프트가 뜨면서 바로 사용 가능합니다.

로그인 확인 겸, 간단한 첫 명령을 해봅니다.

```
현재 폴더 경로를 알려줘.
```

경로가 출력되면 Claude Code가 정상 동작하는 겁니다.

---

## 설치가 안 될 때 (1분)

**"command not found" 오류**
PATH 설정이 안 된 경우입니다. 터미널을 닫고 다시 열거나, 아래를 실행합니다.

```bash
source ~/.zshrc
```

**로그인이 안 되는 경우**
네트워크 문제일 수 있습니다. claude doctor 명령으로 진단합니다.

```bash
claude doctor
```

---

## 핵심 정리 (30초)

Claude Code 설치는 명령어 하나, 브라우저 로그인으로 끝납니다.
다음 클립에서는 Antigravity 에디터를 설치하고, 우리가 강의 내내 쓸 작업 환경을 완성합니다.
