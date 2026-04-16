---
tags: #P01 #CH02 #설치 #환경세팅 #터미널
time: 10분
part: Part 01
chapter: CH02
status: ✅ 대본완성
---

# P01-CH02-01 Claude Code 설치하기

## 📌 클립 정보
- **예상시간:** 10분
- **유형:** 슬라이드 + 화면녹화
- **준비물:** 터미널, 클로드 닷에이아이 계정 (프로 또는 맥스 구독)

---

## 오프닝 (30초)

이번 클립에서는 Claude Code 설치부터 첫 세션 실행까지 진행합니다.
설치는 5분이면 끝납니다.

---

## 사전 준비 (2분)

**Node.js 별도 설치 불필요합니다.**
Claude Code는 네이티브 설치 방식을 사용합니다.

**claude.ai 계정 준비**
프로($20/월) 또는 맥스($100/월) 구독이 필요합니다.
계정 로그인은 설치 후 브라우저 OAuth 방식으로 진행합니다.

---

## 설치 (4분)

[화면: 터미널 실행]

터미널을 열고 아래 명령어를 입력합니다.

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

맥에서 홈브루를 사용한다면:

```bash
brew install --cask claude-code
```

설치 후 버전을 확인합니다.

```bash
claude --version
```

버전 번호가 나오면 설치 완료입니다.

---

## 설치가 안 될 때 — npm 대안 방법 (2분)

회사 맥처럼 보안 정책이 있는 환경에서 실패하는 경우가 있습니다.

```bash
npm install -g @anthropic-ai/claude-code
```

---

## 로그인 및 첫 실행 (2분)

처음 실행하면 브라우저가 열리면서 로그인 화면이 나타납니다.

```bash
mkdir my-first-session && cd my-first-session
claude
```

프롬프트가 뜨면 바로 요청할 수 있습니다.

```
안녕. 현재 폴더 경로를 알려줘.
그리고 hello.txt 파일을 만들어서 "Claude Code 첫 실행 완료"라고 저장해줘.
```

---

## 핵심 정리 (30초)

Claude Code는 터미널에서 실행하는 AI 에이전트입니다.
파일을 만들고, 코드를 실행하고, 결과를 저장합니다.
다음 클립에서는 Antigravity 에디터와 함께 세팅합니다.
