---
tags: #CH05 #MCP #Slack #자동전달 #팀협업
time: 15분
chapter: CH05
status: ✅ 대본완성
---

# CH05-03 Slack MCP — 분석 결과를 팀에 자동 전달하다

## 📌 클립 정보
- **예상시간:** 15분
- **유형:** 슬라이드 2장 + 화면 녹화
- **준비물:** 슬랙 워크스페이스 (무료 가능), 슬랙 봇 토큰

---

## 왜 Slack 자동화가 필요한가 (3분)

분석이 끝나면 결과를 팀에 공유해야 합니다.
보통 이 과정이 번거롭습니다.

기존 방식입니다.
분석 완료 → 결과 파일 열기 → 내용 복사 → 슬랙 열기 → 채널 찾기 → 붙여넣기 → 전송

슬랙 엠씨피를 사용하면 이렇게 됩니다.
분석 완료 → (에이전트가 자동으로 슬랙 전송)

**직접 비교해볼게요.**

분석 결과를 보고서로 인쇄해서 직접 자리마다 돌리는 대신, 이메일 자동 발송 시스템이 동시에 보내는 것과 같습니다.
에이전트가 분석과 공유를 한 번에 처리합니다.

---

## Slack 봇 토큰 발급 방법 (4분)

> 📎 **참고 링크**
> - [Slack API 앱 생성](https://api.slack.com/apps) — 봇 토큰 발급 시작점
> - [Slack MCP 서버](https://github.com/modelcontextprotocol/servers/tree/main/src/slack) — 공식 코드와 설정법
> - [Slack Bot Scopes 가이드](https://api.slack.com/scopes) — 권한 종류 설명

슬랙 엠씨피 연결에는 봇 토큰이 필요합니다.

**1단계: Slack App 생성**

브라우저에서 [api.slack.com/apps](https://api.slack.com/apps)에 접속합니다.
`Create New App` → `From scratch` 선택합니다.
앱 이름과 워크스페이스를 선택합니다.

**2단계: 권한 설정**

왼쪽 메뉴에서 `OAuth & Permissions`를 선택합니다.
`Bot Token Scopes`에서 다음 권한을 추가합니다.
- `channels:read`: 채널 목록 읽기
- `chat:write`: 메시지 전송
- `files:write`: 파일 전송

**3단계: 앱 설치 및 토큰 복사**

`Install to Workspace` 버튼을 클릭합니다.
`Bot User OAuth Token`을 복사합니다.
`xoxb-`로 시작하는 긴 문자열입니다.

**4단계: 채널에 봇 초대**

슬랙 채널에서 `/invite @앱이름`을 입력합니다.
봇이 채널에 참가해야 메시지를 보낼 수 있습니다.

---

## Slack MCP 연결 및 사용 방법 (5분)

토큰을 환경 변수로 설정하고 엠씨피를 연결합니다.

```bash
# 슬랙 토큰 환경 변수 설정
export SLACK_BOT_TOKEN="xoxb-본인토큰"

# 슬랙 MCP 추가
claude mcp add --transport stdio slack -- npx -y @modelcontextprotocol/server-slack
```

클로드 코드를 실행하고 슬랙 메시지를 전송합니다.

```bash
claude
```

> "슬랙 #데이터팀 채널에 '오늘 분석이 완료되었습니다. 결과: SNS 알오아이 80%, 검색 알오아이 150%'라는 메시지를 전송해줘."

에이전트가 슬랙 채널에 메시지를 전송합니다.

---

## 분석 + 슬랙 자동 전송 파이프라인 (2분)

분석부터 슬랙 전송까지 한 번에 지시할 수 있습니다.

> "data/output/result.json을 읽어서 채널별 알오아이 상위 3개를 요약하고, 슬랙 #마케팅팀 채널에 '주간 광고 성과 리포트'라는 제목으로 정리해서 전송해줘."

에이전트가 세 단계를 자동으로 처리합니다.
첫 번째, 결과 파일 읽기.
두 번째, 요약 작성.
세 번째, 슬랙 전송.

---

## 직접 해보기

**목표**: 슬랙에 자동으로 분석 결과를 전송합니다.

**준비 (터미널에 복붙)**
```bash
# 슬랙 토큰 설정 (본인 토큰으로 교체)
export SLACK_BOT_TOKEN="xoxb-YOUR-TOKEN-HERE"

# 슬랙 MCP 연결
claude mcp add --transport stdio slack -- npx -y @modelcontextprotocol/server-slack

# MCP 연결 확인
claude mcp list

claude
```

**클로드에게 이렇게 말합니다**
```
슬랙에서 내가 속한 채널 목록을 보여줘.
그리고 #general 채널에 "클로드 코드 자동 분석 테스트 완료" 메시지를 보내줘.
```

→ 슬랙 채널에 메시지가 자동으로 전송됩니다.

---

## 핵심 정리 (30초)

슬랙 엠씨피를 연결하면 에이전트가 분석 결과를 자동으로 팀에 전달합니다.
봇 토큰 발급과 채널 초대가 선행되어야 합니다.
분석, 요약, 전송까지 하나의 지시로 처리할 수 있습니다.

## 다음 클립 예고 (30초)

다음 클립에서는 지금까지 배운 엠씨피들을 조합해서 완전 자동화 데이터 리포팅 파이프라인을 만듭니다.
데이터베이스에서 가져와서 분석하고, 슬랙으로 전달하는 전 과정을 자동화합니다.
