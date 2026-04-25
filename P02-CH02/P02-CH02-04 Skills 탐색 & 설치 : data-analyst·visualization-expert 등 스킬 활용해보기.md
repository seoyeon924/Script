---
tags: #P02 #CH02 #Skills #data-analyst #visualization-expert
time: 10분
part: Part 02
chapter: CH02
status: ✅ 대본완성
---

# P02-CH02-04 Skills 탐색 & 설치 : data-analyst·visualization-expert 등 스킬 활용해보기

## 📌 클립 정보
- **예상시간:** 10분
- **유형:** 슬라이드 2장 + 화면 녹화
- **준비물:** Claude Code 설치, CLAUDE.md 세팅 완료

---

## 오프닝 (1분)

앞에서 CLAUDE.md로 Claude에게 프로젝트 규칙을 알려줬습니다.
MCP로 외부 도구를 연결했습니다.

Skills는 여기서 한 단계 더 나아갑니다.

**반복적으로 쓰는 분석 워크플로우를 `/명령어` 하나로 만들어두는 것입니다.**

예를 들어:
- `/분석시작` 입력 → 데이터 로드 → EDA → 인사이트 초안 자동 생성
- `/리포트` 입력 → 분석 결과를 정해진 형식으로 Markdown 리포트 생성
- `/경쟁사체크` 입력 → 경쟁사 3곳 크롤링 → 비교 분석 → 요약

이 클립에서는 Skills가 무엇인지, 어떻게 설치하고 직접 만드는지 배웁니다.

---

## Skills 구조 이해 (2분)

**[화면: 슬라이드]**

Skill은 SKILL.md 파일 하나입니다.
이 파일이 특정 폴더에 있으면, Claude가 `/명령어`로 호출할 때 해당 지시를 실행합니다.

```
~/.claude/skills/           - 전체 프로젝트에서 쓸 수 있는 Skills
├── data-analyst/
│   └── SKILL.md
└── viz-report/
    └── SKILL.md

my-project/.claude/skills/  - 이 프로젝트에서만 쓸 수 있는 Skills
└── weekly-check/
    └── SKILL.md
```

SKILL.md 기본 구조 예시:

```markdown
---
name: data-analyst
description: CSV 데이터를 받아 EDA + 시각화까지 자동 수행
---

데이터 파일을 받으면 아래 순서로 실행합니다:

1. 파일 읽기 및 기본 정보 출력 (shape, dtypes, head)
2. 결측값, 이상치 확인
3. 주요 수치 컬럼 분포 히스토그램 저장
4. 상관관계 히트맵 저장
5. 인사이트 3가지 요약

차트는 charts/ 에, 요약은 reports/ 에 저장합니다.
```

Skills와 CLAUDE.md의 차이:

| | CLAUDE.md | Skills |
|---|---|---|
| 역할 | 프로젝트 기본 규칙 | 특정 작업 워크플로우 |
| 적용 | 항상 자동 적용 | 명령어로 호출 |
| 내용 | 규칙, 금지사항, 스타일 | 단계별 작업 지시 |

둘은 함께 씁니다. CLAUDE.md가 기반 규칙, Skills가 반복 작업 자동화입니다.

---

## 커뮤니티 Skills 설치해보기 (3분)

**[화면: Antigravity 에디터 - Claude Code 채팅 패널]**

Claude Code에는 `/plugin` 명령으로 커뮤니티 플러그인과 Skills를 탐색할 수 있습니다.

채팅 패널에 입력합니다:

```
/plugin
```

Discover 탭에서 공식 마켓플레이스의 플러그인 목록이 나타납니다.

한국 입문자용으로 잘 만들어진 커뮤니티 플러그인이 있습니다.
gptaku_plugins입니다. 먼저 마켓플레이스를 등록합니다:

```
/plugin marketplace add https://github.com/fivetaku/gptaku_plugins.git
```

우리 강의에서 데이터 분석에 유용한 Skill을 설치합니다:

```
/plugin install deep-research
```

`deep-research`는 웹 + 학술 출처를 병렬로 수집해서 종합 보고서를 만드는 Skill입니다.
데이터 분석 전 시장 리서치에 바로 활용할 수 있습니다.

사용 방법:
```
/deep-research 2024년 한국 이커머스 시장 트렌드
```

---

## 직접 만들기: 데이터 분석 전용 Skill (3분)

**[화면: Antigravity 에디터]**

우리 프로젝트에 맞는 Skill을 직접 만듭니다.

채팅 패널에 입력합니다:

```
현재 프로젝트 폴더(.claude/skills/data-analyst/)에
데이터 분석 전용 SKILL.md를 만들어줘.

이 Skill이 /data-analyst 명령어로 호출되면:
1. 지정된 CSV 파일을 읽고 기본 EDA 수행
2. CLAUDE.md의 차트 규칙대로 시각화 3개 생성
3. 인사이트와 이상치를 요약한 Markdown 리포트 생성
결과는 charts/와 reports/ 폴더에 저장되도록 해줘.
```

Claude가 SKILL.md를 만들어줍니다.
내용을 확인하고 필요하면 규칙을 추가하거나 수정합니다.

이제 테스트합니다:

```
/data-analyst data/raw/marketing_data.csv를 분석해줘.
```

직접 만든 Skill이 동작하는 걸 확인합니다.

---

## 핵심 정리 (30초)

Skills는 반복 워크플로우를 `/명령어`로 저장하는 기능입니다.

- 커뮤니티 Skills: `/plugin marketplace add`로 설치
- 직접 만들기: `.claude/skills/이름/SKILL.md` 파일 생성
- CLAUDE.md와 함께 쓰면 프로젝트 전용 분석 환경 완성

다음 챕터에서는 여러 에이전트가 역할을 나눠서 협업하는 구조를 배웁니다.
