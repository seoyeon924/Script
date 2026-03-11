---
tags: #패캠 #CH01 #설치
time: 15분
chapter: CH01
status: ✅ 대본완성
---

# CH01-01 Claude Code 설치 & 첫 번째 세션

## 📌 클립 정보
- **예상시간:** 15분
- **유형:** 슬라이드 2~3장 + 화면 녹화
- **준비물:** 터미널, Anthropic 콘솔 접속

---

## 오프닝 (1분)

이번 클립에서는 Claude Code 설치부터 첫 세션 실행까지 진행합니다.
설치는 5분이면 끝나고, 이후 실제로 Claude Code가 어떻게 동작하는지 직접 확인해볼게요.

---

## 사전 준비 (3분)

두 가지 확인해주세요.

**Node.js 18 이상**
```bash
node -v
```
18 미만이거나 없으면 nodejs.org에서 LTS 버전 설치하면 됩니다.

**Anthropic API 키**
console.anthropic.com → API Keys → 키 발급 후 복사해두세요.

---

## 설치 (4분)

```bash
npm install -g @anthropic-ai/claude-code
```

설치 후 확인:
```bash
claude --version
```

API 키 환경 변수 설정:
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

`.zshrc` 또는 `.bashrc`에 추가하면 매번 입력하지 않아도 됩니다.

---

## 첫 번째 세션 실행 (5분)

```bash
mkdir my-first-session
cd my-first-session
claude
```

프롬프트가 뜨면 바로 요청할 수 있습니다.

> "이 폴더에 hello.txt 파일 만들어줘. 내용은 'Claude Code 시작!'"

Claude가 어떤 도구를 쓰는지, 어떤 명령어를 실행하는지 전 과정을 터미널에서 볼 수 있어요.
결과만 보여주는 게 아니라 과정이 투명하게 보이는 게 Claude Code의 특징입니다.

---

## 정리 (2분)

Claude Code는 터미널에서 실행하는 AI 에이전트입니다.
파일을 만들고, 코드를 실행하고, 터미널 명령어를 직접 수행합니다.

다음 클립에서는 CLAUDE.md를 다룹니다.
프로젝트 컨텍스트를 저장해두는 파일인데, 이게 있으면 매 세션마다 반복 설명을 안 해도 됩니다.

---

## 🗒️ 서연 메모
- [ ] 터미널 폰트 크기 키우기 (화면 녹화 전)
- [ ] Anthropic 콘솔 미리 로그인
- [ ] Node.js 버전 확인 화면 캡처
