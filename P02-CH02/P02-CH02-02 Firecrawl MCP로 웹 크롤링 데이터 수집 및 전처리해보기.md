---
tags: #P02 #CH02 #Firecrawl #웹크롤링 #데이터수집
time: 15분
part: Part 02
chapter: CH02
status: ✅ 대본완성
---

# P02-CH02-02 Firecrawl MCP로 웹 크롤링 데이터 수집 및 전처리해보기

## 📌 클립 정보
- **예상시간:** 15분
- **유형:** 슬라이드 2장 + 화면 녹화 (Antigravity 에디터)
- **준비물:** Claude Code 설치, firecrawl.dev 계정 (무료 가입), API 키

---

## 오프닝 (1분)

데이터 분석을 하다 보면 이런 상황이 자주 생깁니다.

"경쟁사 사이트 가격 정보를 수집해야 해."
"업계 최신 뉴스 트렌드를 분석하고 싶어."
"공공 데이터 사이트에서 수치를 긁어와야 해."

예전이라면 BeautifulSoup이나 Selenium 코드를 직접 짜야 했습니다.
Firecrawl MCP를 연결하면 채팅 패널에서 자연어로 웹 데이터를 수집할 수 있습니다.

이번 클립에서는 Firecrawl MCP 설치부터 실제 데이터 수집, 전처리까지 연결합니다.

---

## Firecrawl이 하는 일 (2분)

**[화면: 슬라이드]**

Firecrawl은 웹 페이지를 Claude가 읽을 수 있는 마크다운 텍스트로 변환해주는 도구입니다.

일반 웹 크롤링의 문제:
- 광고, 메뉴, 쿠키 배너가 데이터에 섞임
- 자바스크립트로 동적으로 렌더링된 내용은 못 읽음
- HTML 태그 정리가 번거로움

Firecrawl이 해결하는 방법:
- 동적 렌더링 포함해서 전체 페이지 읽기
- 불필요한 태그 제거, 핵심 텍스트만 추출
- 표, 리스트 구조를 마크다운으로 정리

결과적으로 Claude가 바로 분석할 수 있는 형태로 데이터를 넘겨줍니다.

**Firecrawl 주요 기능:**

| 기능 | 명령어 | 활용 사례 |
|------|---------|----------|
| 단일 페이지 스크래핑 | firecrawl_scrape | 특정 제품 페이지 |
| 사이트 전체 크롤링 | firecrawl_crawl | 블로그 전체 수집 |
| 웹 검색 + 수집 | firecrawl_search | 뉴스, 논문 검색 |
| 사이트 맵 파악 | firecrawl_map | 사이트 구조 이해 |

---

## API 키 발급 및 MCP 연결 (4분)

**[화면: 브라우저 → firecrawl.dev/app]**

먼저 API 키를 발급받습니다.

1. firecrawl.dev 접속
2. 무료 계정 가입 (신용카드 불필요)
3. 대시보드 → **API Keys** 탭에서 키 복사

무료 티어 제한:
- 스크래핑: 분당 10회
- 크롤링: 분당 1회
- 월 500페이지

강의 실습 수준으로는 무료로 충분합니다.

**[화면: Antigravity 에디터 - 터미널]**

이제 Claude Code에 연결합니다. 터미널에서 입력합니다.

```bash
claude mcp add --transport stdio firecrawl -- npx -y firecrawl-mcp
```

그다음 API 키를 환경변수로 등록합니다.

```bash
# macOS / Linux - ~/.zshrc 또는 ~/.bashrc에 추가
export FIRECRAWL_API_KEY="fc-여기에_발급받은_키_입력"
source ~/.zshrc
```

> ⚠️ **절대 하지 말 것:** API 키를 CLAUDE.md나 코드 파일에 직접 쓰지 마세요. 환경변수로만 관리합니다. 키가 GitHub에 올라가면 즉시 악용될 수 있습니다.

MCP 연결 확인:

```bash
claude mcp list
# firecrawl 항목이 보이면 정상
```

---

## 실전: 뉴스 트렌드 데이터 수집 (5분)

**[화면: Antigravity 에디터 - Claude Code 채팅 패널]**

이제 실제로 데이터를 수집해봅니다.

마케팅 데이터 분석 프로젝트를 가정합니다.
"SNS 마케팅 최신 트렌드를 수집해서 분석하고 싶다."

채팅 패널에 입력합니다.

```
2024년 마케팅 자동화 트렌드와 관련된 최신 글을 웹에서 5~10개 검색해서 수집해줘.
각 글의 제목, URL, 핵심 요약(3줄)을 정리해서
data/raw/marketing_trends.md 파일로 저장해줘.
```

Claude가 firecrawl_search → firecrawl_scrape를 조합해서 처리합니다.
페이지를 읽고 있는 과정이 채팅 패널에 표시됩니다.

완료되면 data/raw/marketing_trends.md를 열어 내용을 확인합니다.

이제 이 데이터를 분석합니다.

```
방금 저장한 marketing_trends.md를 읽고:
1. 가장 많이 언급된 키워드 상위 10개
2. 글별 주요 인사이트 요약
3. 우리가 활용할 수 있는 액션 포인트 3가지
를 정리해서 reports/trend_analysis.md로 저장해줘.
```

**포인트**: 웹 수집 → 분석 → 리포트 저장이 채팅 한 번에 연결됩니다.

---

## 경쟁사 가격 데이터 수집 패턴 (2분)

**[화면: 슬라이드]**

이커머스나 마케팅 업무에서 자주 쓰는 패턴입니다.

```
[경쟁사 URL]의 제품 목록 페이지를 스크래핑해줘.
제품명, 가격, 카테고리를 추출해서
data/raw/competitor_prices.csv로 저장해줘.
```

수집 후 전처리:

```
방금 수집한 competitor_prices.csv를 전처리해줘:
- 가격 칼럼에서 원화 기호, 쉼표 제거 후 숫자 타입으로 변환
- 결측값 있는 행 제거
- 카테고리 이름 공백 제거, 소문자 통일
전처리 결과를 data/processed/prices_cleaned.csv로 저장해줘.
```

이렇게 수집 → 전처리 → 시각화로 파이프라인이 자연스럽게 이어집니다.

---

## 핵심 정리 (1분)

Firecrawl MCP를 연결하면 웹 데이터를 자연어로 수집할 수 있습니다.

정리하면:
- API 키 발급 → 환경변수 등록 → MCP 연결 3단계
- 검색(firecrawl_search) + 스크래핑(firecrawl_scrape) 조합으로 원하는 데이터 수집
- 수집 직후 Claude에게 전처리까지 한 번에 지시
- 키는 절대 파일에 직접 쓰지 말 것

다음 클립에서는 Firecrawl 포함, 여러 MCP를 조합하는 실전 분석 워크플로우를 다룹니다.
