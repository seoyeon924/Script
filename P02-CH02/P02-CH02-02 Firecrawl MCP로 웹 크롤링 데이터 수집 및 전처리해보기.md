---
tags: #P02 #CH02 #Firecrawl #웹크롤링 #데이터수집
time: 15분
part: Part 02
chapter: CH02
status: 📝 작성필요
---

# P02-CH02-02 Firecrawl MCP로 웹 크롤링 데이터 수집 및 전처리해보기

## 📌 클립 정보
- **예상시간:** 15분
- **유형:** 슬라이드 + 화면녹화

---

## 오프닝 (30초)

(Firecrawl MCP로 웹에서 데이터를 수집하고 분석하는 워크플로우 소개)

## 본문

### Firecrawl MCP란

Firecrawl은 웹 페이지를 크롤링해서 구조화된 데이터로 변환하는 도구입니다.
Claude Code에 Firecrawl MCP를 연결하면 자연어로 웹 데이터를 수집할 수 있습니다.

### 설치 및 연결

```bash
# Firecrawl MCP 연결
claude mcp add --transport stdio firecrawl -- npx -y firecrawl-mcp

# API 키 설정
export FIRECRAWL_API_KEY="your-api-key"
```

### 실전 활용 예시

**경쟁사 가격 데이터 수집:**
```
firecrawl로 [사이트 URL]에서 제품별 가격 정보를 수집해줘.
표 형태로 정리해서 data/raw/competitor_prices.csv로 저장해줘.
```

**뉴스 트렌드 데이터 수집:**
```
지난 주 [키워드] 관련 뉴스 헤드라인을 수집하고
워드 클라우드 데이터로 정리해줘.
```

### 수집 후 전처리

```
방금 수집한 데이터에서:
1. 결측값 처리
2. 날짜 형식 통일 (YYYY-MM-DD)
3. 수치 데이터 타입 변환
4. data/processed/cleaned_data.csv 저장
```

---

## 핵심 정리 (30초)

Firecrawl MCP를 연결하면 웹 데이터를 자연어로 수집할 수 있습니다.
수집 → 전처리 → 시각화 파이프라인을 Claude Code가 자동으로 처리합니다.
다음 클립에서는 MCP 실전 활용 — 웹 리서치·파일 처리·분석 자동화를 다룹니다.
