---
tags: #P02 #CH02 #Firecrawl #웹크롤링 #데이터수집
time: 15분
part: Part 02
chapter: CH02
clip: 02
slides: s5,s15,s6,s7,s19
status: ✅ 대본완성
---

# P02-CH02-02 Firecrawl MCP로 웹 크롤링 데이터 수집 및 전처리해보기

---

## s5 — CLIP 02 섹션 브레이크

두 번째 클립, Firecrawl MCP입니다.

데이터 분석을 하다 보면 웹에서 데이터를 가져와야 하는 상황이 생겨요.
이번 클립에서는 Firecrawl MCP를 연결해서 웹 크롤링을 자동화하는 방법을 봅니다.

---

## s15 — Claude는 URL을 직접 못 읽는다

**[화면: 슬라이드]**

Firecrawl이 왜 필요한지부터 짚어볼게요.

Claude에게 URL을 주면 방문한 것처럼 답해줄 때가 있어요.
근데 실제로는 그 페이지를 읽은 게 아닙니다.

왼쪽 문제 상황을 보시면요.
"이 사이트 분석해줘" 하고 URL을 입력합니다.
Claude가 실제로 읽지 않고 학습된 정보로 그럴싸하게 꾸며서 답해요.
그걸 모르고 보고서에 그대로 쓰면 낭패를 봐요.

해결책이 Firecrawl MCP예요.
연결하면 Claude가 실제로 페이지를 크롤링해서 진짜 내용을 읽습니다.

---

## s6 — 웹 페이지를 마크다운으로

**[화면: 슬라이드]**

Firecrawl이 하는 일은 단순해요.

웹 페이지를 Claude가 읽을 수 있는 마크다운으로 바꿔줍니다.
광고, 메뉴, 쿠키 배너 같은 불필요한 요소는 제거하고요.
자바스크립트로 동적으로 로딩되는 내용도 포함해서 읽어요.

오른쪽 표에 4개 함수가 있는데요.

`firecrawl_scrape`는 단일 페이지 하나를 읽고요.
`firecrawl_crawl`은 사이트 전체를 크롤링합니다.
`firecrawl_search`는 웹 검색하면서 동시에 내용을 수집해요.
`firecrawl_map`은 사이트 구조 파악용입니다.

무료 티어는 월 500페이지예요. 강의 실습 수준에서는 충분해요.

---

## s7 — API 키 발급 & MCP 연결

**[화면: 슬라이드]**

설치는 세 단계예요.

**1단계**는 firecrawl.dev에서 무료 계정을 만들고 API 키를 복사합니다.
신용카드는 필요 없어요.

**2단계**는 Claude Code에 MCP를 연결하고 API 키를 환경변수로 등록해요.

```bash
claude mcp add --transport stdio firecrawl -- npx -y firecrawl-mcp

export FIRECRAWL_API_KEY="fc-..."
```

**3단계**가 가장 중요합니다. 보안 주의사항이에요.
API 키를 채팅창에 직접 입력하면 절대 안 돼요.
환경변수로만 관리합니다.

---

## s19 — 영화 캐릭터 관계망 수집

**[화면: Antigravity 에디터 - Claude Code 채팅 패널]**

이제 실습을 해볼게요.

MCU 어벤져스 캐릭터들의 관계 데이터를 웹에서 수집해서 CSV로 저장하는 실습입니다.

왼쪽에 목표 결과물이 있어요.
source, target, relationship, weight 컬럼으로 구성된 CSV예요.
Iron Man과 Captain America는 alliance 관계고 강도는 0.85, Thor와 Loki는 conflict고 0.72, 이런 식이에요.

오른쪽 프롬프트를 그대로 Claude Code에 붙여넣으면 됩니다.

```
firecrawl_search로
"MCU Avengers characters relationships allies enemies"
검색해서 등장인물 관계를 정리해줘.

컬럼: source, target, relationship, weight
relationship 값: alliance / conflict / romance / family
weight는 0~1 사이 관계 강도
파일명: data/avengers_network.csv
```

Claude가 firecrawl_search로 관련 페이지들을 검색하고, 내용을 읽어서 관계 데이터를 CSV로 정리해줍니다.

이 CSV가 나오면 D3.js로 시각화해서 인터랙티브 네트워크 차트를 만들 수 있어요.

다음 클립에서는 Skills를 다룹니다. 반복 작업을 `/명령어` 하나로 저장하는 방법이에요.
