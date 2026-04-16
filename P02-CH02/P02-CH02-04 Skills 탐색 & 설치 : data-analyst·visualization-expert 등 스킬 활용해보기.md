---
tags: #P02 #CH02 #Skills #data-analyst #visualization-expert
time: 10분
part: Part 02
chapter: CH02
status: 📝 작성필요
---

# P02-CH02-04 Skills 탐색 & 설치 : data-analyst·visualization-expert 등 스킬 활용해보기

## 📌 클립 정보
- **예상시간:** 10분
- **유형:** 슬라이드 + 화면녹화

---

## 오프닝 (30초)

(Claude Code Skills 시스템 소개 — 특정 작업에 특화된 에이전트 설정 모음)

## 본문

### Skills란 무엇인가

Skills는 특정 작업 유형에 최적화된 지시 묶음입니다.
특정 폴더에서 작업할 때 자동으로 활성화됩니다.

**Skills 구조:**
```
skills/
├── data-analyst/
│   ├── SKILL.md           ← 분석 에이전트 규칙
│   └── references/        ← 참고 자료
└── visualization-expert/
    ├── SKILL.md           ← 시각화 에이전트 규칙
    └── templates/         ← 차트 템플릿
```

### data-analyst Skill 예시

```markdown
# Data Analyst Skill

## 역할
데이터 분석 전문가로서 작업합니다.

## 분석 원칙
1. 데이터 구조 파악 먼저
2. 결측값, 이상치 처리 후 분석
3. 인사이트는 수치 기반으로 명확하게
4. 시각화 규칙 준수

## 자주 쓰는 분석 패턴
- 집계: groupby + agg
- 시계열: resample + rolling
- 상관관계: corr() + heatmap
```

### Skills 설치 방법

```bash
# 커뮤니티 Skills 설치
claude skills install data-analyst
claude skills install visualization-expert

# 설치된 Skills 확인
claude skills list
```

### 직접 해보기

```
data-analyst 스킬을 활성화하고
data/raw/sales.csv를 분석해줘.
```

---

## 핵심 정리 (30초)

Skills는 특정 작업에 특화된 에이전트 규칙 묶음입니다.
data-analyst, visualization-expert 같은 스킬을 설치하면 해당 작업에 최적화된 분석을 받습니다.
이것으로 Part 02 CH02 MCP & Skills 섹션을 마칩니다.
