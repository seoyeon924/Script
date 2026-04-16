---
title: CH01-10 MCP — 외부 도구 연결
chapter: CH01
clip: 10
time: 10분
type: 슬라이드 + 실습
---

# CH01-10 MCP — 외부 도구 연결

## 클립 목표

서브에이전트로 역할 분리하는 방법을 익혔습니다.
이번엔 클로드 코드가 외부 서비스(데이터베이스, 슬랙 등)와 연결되는 방법입니다.
이게 엠씨피(MCP)예요.

MCP가 무엇인지 이해하고, 자주 쓰는 MCP 서버를 연결할 수 있습니다.

---

## 1. MCP란 무엇인가 (3분)

MCP(Model Context Protocol)는 클로드 코드가 외부 도구와 데이터 소스에 연결하는 표준 방식입니다.

비유하자면, USB 포트와 같습니다.
클로드 코드가 노트북이라면, MCP는 USB 규격입니다. MCP를 지원하는 도구라면 무엇이든 연결할 수 있습니다.

기본 상태의 클로드 코드는 내 컴퓨터 파일만 다룰 수 있습니다.
MCP를 통해 연결하면:
- 구글 스프레드시트에서 직접 데이터를 읽고 쓸 수 있습니다
- 슬랙으로 결과를 직접 전송할 수 있습니다
- 데이터베이스에 직접 쿼리를 실행할 수 있습니다
- 웹 브라우저를 제어할 수 있습니다

---

## 2. MCP 서버 연결 방법 (3분)

MCP 서버는 `~/.claude.json` 또는 `.mcp.json` 파일에 설정합니다.

**전체 공통 설정:** `~/.claude.json`
**프로젝트별 설정:** `.mcp.json` (프로젝트 폴더 최상단)

```json
{
  "mcpServers": {
    "google-sheets": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-google-sheets"]
    },
    "sqlite": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sqlite",
               "--db-path", "./data/analysis.db"]
    }
  }
}
```

설정 후 클로드 코드를 재시작하면 해당 도구가 활성화됩니다.

---

## 3. 데이터 분석에서 유용한 MCP 서버 (4분)

### 구글 스프레드시트

```bash
npx -y @modelcontextprotocol/server-google-sheets
```

"구글 시트 sales_2026 파일에서 2월 데이터 읽어줘"처럼 직접 접근 가능합니다.
파일 다운로드 없이 시트 데이터를 바로 분석합니다.

### SQLite / PostgreSQL

```bash
npx -y @modelcontextprotocol/server-sqlite --db-path ./data/db.sqlite
```

"customers 테이블에서 지난달 신규 가입자 수 집계해줘"처럼 SQL 쿼리를 자연어로 실행합니다.

### 파일시스템 확장

```bash
npx -y @modelcontextprotocol/server-filesystem /Users/sy/Documents
```

지정한 폴더 외부 경로에도 접근할 수 있도록 범위를 확장합니다.

### 브라우저 제어 (Playwright)

```bash
npx -y @modelcontextprotocol/server-playwright
```

"네이버 쇼핑에서 경쟁사 가격 수집해줘"처럼 웹 자동화가 가능합니다.

---

## 직접 해보기

**목표**: 파일시스템 MCP 서버를 정확한 명령어로 연결합니다.

**파일시스템 MCP 서버 설치 (터미널에 복붙)**
```bash
# stdio 방식 — 로컬에서 npx로 실행
claude mcp add --transport stdio filesystem -- npx -y @modelcontextprotocol/server-filesystem ~/Documents
```

→ `~/Documents` 폴더를 클로드가 접근할 수 있는 엠씨피 서버로 등록합니다.
→ `--transport stdio`: 로컬 프로세스 방식 (로컬 파일 접근 시 사용)
→ `--`: 이 뒤는 엠씨피 서버 실행 명령어 (클로드 옵션과 구분)

**설치 확인**
```bash
# 등록된 서버 목록 조회
claude mcp list

# 상세 정보 확인
claude mcp get filesystem
```

**클로드 코드 세션에서 상태 확인**
```
/mcp
```

**MCP 서버 활용**
```
Documents 폴더에 있는 파일 목록을 보여줘
```

**서버 제거**
```bash
claude mcp remove filesystem
```

**원격 HTTP 서버 연결 (노션 예시)**
```bash
# 원격 서버는 --transport http 사용
claude mcp add --transport http notion https://mcp.notion.com/mcp
```

---

## 핵심 정리

- MCP는 클로드 코드를 외부 도구에 연결하는 표준 방식입니다.
- `.mcp.json` 파일에 사용할 서버를 설정합니다.
- 구글 시트, 데이터베이스, 웹 브라우저 등 다양한 도구를 연결할 수 있습니다.

---

## CH01 챕터 전체 정리

이번 챕터에서 다룬 내용을 요약합니다.

| 클립 | 핵심 개념 | 핵심 명령어/파일 |
|------|---------|----------------|
| 01 | 클로드 코드 = 에이전틱 AI | `curl -fsSL https://claude.ai/install.sh \| bash` |
| 02 | CLAUDE.md = 프로젝트 메모리 | `CLAUDE.md` 파일 작성 |
| 03 | Plan 모드 = 계획 먼저 확인 | `--permission-mode plan` |
| 04 | 슬래시 커맨드 | `/compact`, `/clear`, `/diff` |
| 05 | 토큰 절약 | `--model haiku`, `/compact` |
| 06 | 훅 = 자동화 트리거 | `settings.json` |
| 07 | 서브에이전트 = 역할 분리 | `.claude/agents/` |
| 08 | MCP = 외부 도구 연결 | `.mcp.json` |

다음 클립에서는 데스크탑 앱과 클라우드 환경을 다룹니다.
로컬 맥북 말고, 클라우드에서 클로드 코드를 돌리는 방법입니다.
