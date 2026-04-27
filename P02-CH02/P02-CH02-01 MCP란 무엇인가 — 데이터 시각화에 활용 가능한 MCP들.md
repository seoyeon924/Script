---
tags: #P02 #CH02 #MCP #외부도구 #에이전트확장
time: 10분
part: Part 02
chapter: CH02
status: ✅ 대본완성
---

# P02-CH02-01 MCP란 무엇인가 — 데이터 시각화에 활용 가능한 MCP들

## 📌 클립 정보
- **예상시간:** 10분
- **유형:** 슬라이드 4장 + 화면 녹화
- **준비물:** Claude Code 설치 완료, Node.js 설치 (npx 사용)

---

## 오프닝 (30초)

Claude Code는 기본적으로 터미널 명령어를 실행하고 파일을 읽고 씁니다.
MCP를 연결하면 데이터베이스, 구글 시트, 웹 크롤링까지 직접 처리할 수 있습니다.

---

## MCP란 무엇인가 (3분)

MCP(Model Context Protocol)는 에이전트에게 새로운 도구를 연결하는 프로토콜입니다.

스마트폰에 앱을 설치하는 것과 같습니다.
스마트폰 자체는 전화와 메시지만 됩니다.
카카오맵을 설치하면 내비게이션이 됩니다.
Claude Code도 MCP 서버를 연결하면 새로운 능력이 생깁니다.

**MCP 작동 구조:**

```
Claude Code (에이전트)
     ↓ 요청
MCP 서버 (파일시스템/DB/Firecrawl 등)
     ↓ 응답
Claude Code (에이전트)
```

---

## 데이터 시각화에 활용 가능한 MCP들 (5분)

| MCP 서버 | 기능 | 시각화 활용 사례 |
|---------|------|--------------|
| `@modelcontextprotocol/server-filesystem` | 파일 읽기/쓰기 | 프로젝트 파일 접근 |
| `@modelcontextprotocol/server-postgres` | PostgreSQL 연결 | DB에서 직접 데이터 추출 |
| `@modelcontextprotocol/server-sqlite` | SQLite 연결 | 로컬 DB 분석 |
| `firecrawl-mcp` | 웹 크롤링 | 경쟁사 데이터 수집 |
| Google Sheets MCP | 스프레드시트 연동 | 팀 공유 데이터 직접 읽기 |

---

## MCP 추가 기본 명령어 (2분)

```bash
claude mcp add --transport stdio filesystem -- npx -y @modelcontextprotocol/server-filesystem ~/Desktop

# 연결된 MCP 목록 확인
claude mcp list
```

`.mcp.json` 파일로도 관리할 수 있습니다:

```json
{
  "mcpServers": {
    "postgres": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-postgres"],
      "env": { "DATABASE_URL": "${DATABASE_URL}" }
    }
  }
}
```

**핵심:** 비밀값은 반드시 환경변수(`${변수명}`)로만 — 코드에 직접 입력 절대 금지.

---

## 핵심 정리 (30초)

MCP는 Claude Code에 새로운 도구를 연결하는 프로토콜입니다.
데이터 시각화에는 파일시스템, DB, Firecrawl, Google Sheets MCP가 특히 유용합니다.
다음 클립에서는 Firecrawl MCP로 웹 크롤링 데이터를 수집합니다.
