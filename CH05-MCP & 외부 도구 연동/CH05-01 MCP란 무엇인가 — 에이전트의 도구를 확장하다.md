---
tags: #CH05 #MCP #외부도구 #에이전트확장 #개념
time: 15분
chapter: CH05
status: ✅ 대본완성
---

# CH05-01 MCP란 무엇인가 — 에이전트의 도구를 확장하다

## 📌 클립 정보
- **예상시간:** 15분
- **유형:** 슬라이드 4장 + 화면 녹화
- **준비물:** 클로드 코드 설치 완료, 노드 제이에스 설치 (npx 사용)

---

## MCP가 필요한 이유 (4분)

클로드 코드는 기본적으로 터미널에서 명령어를 실행하고 파일을 읽고 쓸 수 있습니다.
그런데 실무에서는 이것만으로는 부족합니다.

예를 들어 이런 작업들이 있습니다.

**데이터베이스에서 직접 데이터를 가져오는 작업입니다.**
에스큐엘 쿼리를 실행해서 테이블을 읽어야 합니다.

**슬랙으로 분석 결과를 자동 전송하는 작업입니다.**
분석이 끝나면 팀 채널에 리포트를 보내야 합니다.

**구글 스프레드시트를 읽고 쓰는 작업입니다.**
씨에스브이 대신 스프레드시트가 데이터 원본인 경우입니다.

이 작업들을 클로드 코드가 직접 하려면 추가 도구가 필요합니다.
그것이 엠씨피입니다.

**엠씨피(Model Context Protocol)란 무엇인가:**

엠씨피는 에이전트에게 새로운 도구를 연결하는 표준 프로토콜입니다.

**실제 상황으로 보면,**

스마트폰에 앱을 설치하는 것과 같습니다.
스마트폰 자체는 전화와 메시지만 됩니다.
카카오맵 앱을 설치하면 내비게이션이 됩니다.
유튜브 앱을 설치하면 동영상을 봅니다.
클로드 코드도 엠씨피 서버를 연결하면 새로운 능력이 생깁니다.

---

## MCP 구조 이해 (4분)

엠씨피는 두 부분으로 구성됩니다.

**엠씨피 서버**: 특정 기능을 제공하는 프로그램입니다.
예: 파일시스템 서버, 데이터베이스 서버, 슬랙 서버

**에이전트 (클라이언트)**: 엠씨피 서버에 요청을 보내는 클로드 코드입니다.

작동 방식입니다.

```
클로드 코드 (에이전트)
     ↓ 요청
MCP 서버 (파일시스템/DB/슬랙 등)
     ↓ 응답
클로드 코드 (에이전트)
```

엠씨피 서버는 보통 엔피엑스(`npx`)로 실행합니다.
별도 설치 없이 명령어 하나로 시작합니다.

현재 사용 가능한 주요 엠씨피 서버입니다.

| 서버 | 기능 |
|------|------|
| `@modelcontextprotocol/server-filesystem` | 파일 읽기/쓰기 |
| `@modelcontextprotocol/server-postgres` | 포스트그레에스큐엘 연결 |
| `@modelcontextprotocol/server-sqlite` | 에스큐라이트 연결 |
| `@modelcontextprotocol/server-slack` | 슬랙 메시지 전송 |
| `@modelcontextprotocol/server-github` | 깃허브 레포 연결 |

---

## MCP 설치 명령어 구조 (4분)

엠씨피 서버 연결 명령어 구조입니다.

```bash
claude mcp add --transport stdio <이름> -- <실행 명령어>
```

각 부분을 설명합니다.

- `claude mcp add`: 엠씨피 서버를 추가하는 명령어입니다
- `--transport stdio`: 서버와 통신하는 방식입니다. 로컬 서버는 `stdio`를 사용합니다
- `<이름>`: 에이전트에서 이 서버를 부를 이름입니다. 자유롭게 설정합니다
- `--`: 이 기호가 중요합니다. 클로드 코드 명령어와 엠씨피 서버 명령어를 구분합니다
- `<실행 명령어>`: 실제 엠씨피 서버를 실행하는 명령어입니다

파일시스템 엠씨피 추가 예시입니다.

```bash
claude mcp add --transport stdio filesystem -- npx -y @modelcontextprotocol/server-filesystem ~/Documents
```

이 명령어는 `~/Documents` 폴더에 대한 파일시스템 접근을 에이전트에게 제공합니다.

**중요:** `--` 구분자가 반드시 있어야 합니다.
없으면 `npx` 이후 옵션이 클로드 코드 명령어로 해석됩니다.

---

## 화면 실습 — 파일시스템 MCP 연결 (2분)

터미널에서 순서대로 실행합니다.

```bash
# 파일시스템 MCP 추가
claude mcp add --transport stdio filesystem -- npx -y @modelcontextprotocol/server-filesystem ~/Desktop

# 연결된 MCP 목록 확인
claude mcp list

# 클로드 코드 실행
claude
```

클로드에게 이렇게 지시합니다.

> "데스크톱에 있는 파일 목록을 가져와줘."

엠씨피를 통해 클로드 코드가 파일 목록을 가져옵니다.

---

## 직접 해보기

**목표**: 파일시스템 MCP를 연결하고 에이전트가 파일을 읽는 것을 확인합니다.

**준비 (터미널에 복붙)**
```bash
# 노드 설치 확인
node --version

# 테스트 폴더와 파일 생성
mkdir ~/mcp-test
printf "날짜,매출\n2024-01-01,1500000\n2024-01-02,2300000" > ~/mcp-test/sales.csv

# 파일시스템 MCP 추가
claude mcp add --transport stdio filesystem -- npx -y @modelcontextprotocol/server-filesystem ~/mcp-test

# 연결 확인
claude mcp list
```

**클로드에게 이렇게 말합니다**
```
mcp-test 폴더에 있는 sales.csv를 읽어서
날짜별 매출 합계를 계산해줘.
```

→ 엠씨피를 통해 에이전트가 파일을 직접 읽습니다.

---

## 핵심 정리 (30초)

엠씨피는 클로드 코드에 새로운 도구를 연결하는 표준 프로토콜입니다.
`claude mcp add --transport stdio <이름> -- <명령어>` 형식으로 추가합니다.
`--` 구분자가 반드시 필요합니다.

## 다음 클립 예고 (30초)

다음 클립에서는 데이터베이스 엠씨피를 연결하는 방법을 다룹니다.
에스큐엘 데이터베이스에 클로드 코드가 직접 접속해서 쿼리를 실행하는 과정을 살펴보겠습니다.

---

## 📎 참고 자료

### modelcontextprotocol/servers ★82,077
Anthropic 공식 MCP 서버 모음. Brave Search, Filesystem, GitHub, Slack, PostgreSQL 등 즉시 사용 가능한 서버들이 정리되어 있습니다.
공식 레포: https://github.com/modelcontextprotocol/servers

> CH05 전체의 핵심 레퍼런스입니다. "MCP 서버 어디서 받아요?"라는 수강생 질문에 이 레포 하나면 답이 됩니다. Anthropic이 직접 관리하는 공식 레포라 내용 신뢰도가 최고이며, 강의 실습에서 쓸 MCP 서버도 여기서 선택하세요.
