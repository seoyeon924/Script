---
tags: #P02 #CH02 #Skills #SKILL.md #워크플로우
time: 15분
part: Part 02
chapter: CH02
clip: 03
slides: s10,s11,s12,s18,s17
status: ✅ 대본완성
---

# P02-CH02-03 Skills 탐색 & 설치 — SKILL.md 구조 · 커뮤니티 설치 · 직접 만들기

---

## s10 — CLIP 03 섹션 브레이크

세 번째 클립, Skills입니다.

MCP가 Claude Code에 새 도구를 연결하는 것이라면, Skills는 반복하는 작업을 `/명령어` 하나로 압축하는 기능이에요.
구조 이해, 커뮤니티 설치, 직접 만들기 순서로 봅니다.

---

## s11 — /명령어 하나로 워크플로우 실행

**[화면: 슬라이드]**

Skills의 핵심은 SKILL.md 파일 하나예요.

이 파일이 `.claude/skills/` 폴더 안에 있으면, Claude가 `/명령어`로 호출할 때 그 지시를 실행합니다.

오른쪽 표에 CLAUDE.md랑 Skills 차이가 정리돼 있어요.

CLAUDE.md는 프로젝트 기본 규칙이고, 항상 자동으로 적용됩니다.
Skills는 특정 워크플로우를 저장하는 거고, 명령어로 호출할 때만 실행돼요.
CLAUDE.md가 규칙·금지사항이라면 Skills는 단계별 작업 지시입니다.

폴더 위치는 두 가지예요.
`~/.claude/skills/`는 어떤 프로젝트에서도 쓸 수 있는 전역 설치이고요.
`my-project/.claude/skills/`는 이 프로젝트에서만 쓰는 전용 설치예요.

---

## s12 — 커뮤니티 Skills & 직접 만들기

**[화면: Antigravity 에디터 - Claude Code 채팅 패널]**

Skills를 쓰는 방법은 두 가지예요.
커뮤니티에서 설치하거나, 직접 만들거나입니다.

커뮤니티 설치 먼저 볼게요.

Claude Code 채팅 패널에서 `/plugin`을 입력합니다.
마켓플레이스를 등록하고 원하는 스킬을 설치하면 돼요.

```
/plugin marketplace add https://github.com/fivetaku/gptaku_plugins.git
/plugin install deep-research
```

설치되면 이렇게 바로 씁니다.

```
/deep-research 2024년 한국 이커머스 트렌드
```

두 번째는 직접 만들기예요.
설치 없이 파일 하나로 끝납니다.

세 단계예요.

1단계, 터미널에서 폴더를 만들고요.
```bash
mkdir -p .claude/skills/data-analyst
```

2단계, Claude Code에 SKILL.md를 만들어달라고 합니다.
"`.claude/skills/data-analyst/SKILL.md` 만들어줘. `/data-analyst` 호출 시 EDA → 차트 3개 → 리포트 생성"

3단계, 이후부터 `/data-analyst`로 바로 호출하면 됩니다.

---

## s18 — 데이터 분석 관련 스킬들

**[화면: 슬라이드]**

Skills를 탐색하기 좋은 곳이 있어요.
skillsmp.com입니다.
직군별로 실무 스킬 템플릿이 모여 있어요.

왼쪽에 데이터 분석 관련 스킬 세 가지가 있는데요.

별점 10만 개가 넘는 `data-analyst`는 SQL·pandas·통계 분석 워크플로우를 담고 있어요.
`data-visualization`은 차트 생성부터 멀티패널 분석 요약까지 다루고요.
matplotlib·seaborn·plotly를 기반으로 한 시각화 전용 스킬도 있습니다.

오른쪽 화면이 skillsmp.com에서 "data visualization"으로 검색한 결과예요.
주소는 skillsmp.com/ko입니다.

---

## s17 — "MCP보다 Skills가 낫다"

**[화면: 슬라이드]**

요즘 커뮤니티에서 자주 나오는 말이 있어요.
"MCP보다 Skills가 낫다"는 말입니다.

왜 이런 말이 나오냐면요.

왼쪽 핵심 문제를 보시면요.
MCP 5개를 연결하면 컨텍스트가 5만 5천 토큰이 사라집니다.
Claude가 기억할 수 있는 공간이 그만큼 줄어드는 거예요.

표를 보시면 차이가 명확해요.

MCP 서버 하나당 토큰 비용이 18,000 토큰인데, Skills는 50 토큰이에요.
설정 시간도 MCP는 2~8시간, Skills는 30초예요. 마크다운 파일 하나거든요.
버전 관리도 Skills는 Git으로 팀이랑 공유할 수 있어요.

결론은 이래요.
웹 크롤링, 데이터베이스, 외부 API 연결이 필요하면 → MCP.
반복하는 분석 워크플로우를 저장하고 싶으면 → Skills.

CLI 명령어나 Skills로 해결되면 MCP는 과설계예요.

다음 클립에서는 이 Skills를 스케줄에 태워서 자동화하는 방법을 봅니다.
