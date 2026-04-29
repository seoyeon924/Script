# CH01 슬라이드 리뷰 피드백
> 작성일: 2026-04-29  
> 목적: 교육적 피드백 + 공식 문서 대조 정정 내역 보존

---

## 1. 교육적 피드백 — 전체 총평

**핵심 한 줄:**  
"개념 정리는 잘 했는데, 학습자가 '쓸 수 있게' 만드는 구조는 부족함"

| 항목 | 평가 |
|------|------|
| 개념 | ✅ 있음 |
| 구조 | ✅ 있음 |
| 실행 가능성 | ❌ 부족 |
| 실습 연결 | ❌ 약함 |
| 실제 Claude Code UX 반영 | ⚠️ 일부 부족 |

---

## 2. 가장 큰 문제 3가지

### ① "왜 쓰는지"보다 "무엇인지" 설명이 많다
- Read / Write / Bash 설명은 있음
- "언제 써야 하는지" 없음
- **지금 상태:** "도구 설명서"
- **교육 기준:** "의사결정 기준 + 사용 타이밍"

### ② Plan Mode 설명이 너무 얕음
- 빠진 것: 실패 방지 구조, hallucination 제어, large change 관리
- **실제 핵심:** Plan Mode = "AI 리스크 관리 장치"

### ③ CLAUDE.md = "파일 설명" 수준에 머물러 있음
- 빠진 것: 좋은 예 vs 나쁜 예 비교, 실제 효과 차이, before/after

---

## 3. 파트별 피드백

### CLIP 01 — 도구 + Plan Mode

**좋은 점**
- Read → Write → Bash 흐름 명확함
- 초보자 이해는 쉬움

**문제**
- 너무 이상적인 흐름 (에러 → 수정 → 반복 루프 없음)
- Bash 위험성 설명 없음 (rm, overwrite 등)
- Glob/Grep 설명은 있는데 "언제 쓰는지" 없음

**개선 방향 (추가된 것)**
- s24: 실제 작업 시나리오 (Bash ls → Glob → Read → Write → Bash → 에러 → 수정 루프)
- s26: 실패 사례 (파일 덮어쓰기 / hallucination / 컨텍스트 초과)

---

### 실행 모드

**문제**
- "언제 어떤 모드를 선택해야 하는지" 없음

**추가된 것 (s25)**
| 상황 | 추천 모드 |
|------|---------|
| 처음 보는 코드 | plan |
| 빠른 수정 | acceptEdits |
| 위험 작업 | plan |
| 자동화 파이프라인 | bypass |

---

### 컨텍스트 관리

**문제**
- "언제 해야 하는지 감각 없음"

**추가된 것 (s15 수정)**
- 컨텍스트 70% 초과 → /compact
- 100턴 이상 → /compact
- 속도 느려지면 → /compact

---

### CLIP 02 — 폴더 구조

**좋은 점**
- 구조 설명 좋음
- 실제 프로젝트 예시 있음

**문제**
- "나쁜 구조 vs 좋은 구조" 비교 없음

**추가된 것 (s29)**
- ❌ 나쁜 구조: data_final2.csv, script_new_v3.py, analysis_copy.ipynb
- ✅ 좋은 구조: data/raw/, data/processed/, scripts/, outputs/

---

### CLIP 03 — CLAUDE.md

**좋은 점**
- 200줄 제한, 구체성 강조

**문제**
- "효과 체감"이 없음

**추가된 것 (s27)**
- BEFORE: 영어 레이블, 기본 색상, 임의 경로
- AFTER: 한국어 레이블, 팀 색상, 지정 경로 자동 적용

---

## 4. 반드시 추가해야 할 5가지 (→ 모두 반영 완료)

| # | 항목 | 슬라이드 | 반영 |
|---|------|---------|------|
| 1 | 실제 워크플로우 | s24 | ✅ |
| 2 | 모드 선택 기준표 | s25 | ✅ |
| 3 | CLAUDE.md before/after | s27 | ✅ |
| 4 | 실패 사례 | s26 | ✅ |
| 5 | 실습 1개 | s28 | ✅ |

---

## 5. 공식 문서 정정 내역

> 출처: code.claude.com/docs (공식 문서 대조)

### 🔴 수정 완료

| 슬라이드 | 오류 내용 | 수정 내용 |
|---------|---------|---------|
| s4/s12/s18 | `rules/` 폴더 제거 | 복원 — 공식 `.claude/` 하위 폴더임 |
| s19 | `LS` 도구로 표기 | `Bash (ls)` 로 수정 — 공식 Tools reference에 LS 없음 |
| s8 | 4가지 모드, "Edit automatically = 기본값" | 5가지 모드, 기본값은 `default` (Ask permissions), `auto` 모드 추가 |
| s9 | Fork/Rewind 비공식 명칭 | 공식 명칭으로 교체: Restore code and conversation / Restore conversation / Restore code / Summarize from here |
| s16 | `/effort low·mid·high` | `low·medium·high·max·auto` (`mid` → `medium`) |
| s20 | "충돌 시 나중 파일 우선" | "모든 파일 concatenate, 충돌 시 Claude 임의 선택" |
| s4/s12/s18 | `│` 사용한 트리 들여쓰기 (└── 다음 │ = 잘못된 표기) | 공백으로 수정 |

### ✅ 원래부터 정확했던 것들

- 슬라이드 3 (Read/Write/Bash 도구 이름)
- 슬라이드 7 (컨텍스트 관리 — /compact, /resume, /context, /rename)
- 슬라이드 10 (프로젝트 폴더 파악)
- 슬라이드 13·14·15 (.claude 탐색·편집·확장)
- 슬라이드 17 (CLAUDE.md vs 자동 메모리)
- 슬라이드 20 (작성 가이드 4가지)

---

## 6. 목표 상태

**지금 상태:** "Claude Code를 이해하게 하는 슬라이드"  
**목표 상태:** "Claude Code를 바로 쓰게 만드는 슬라이드"

차이: ❌ 설명 중심 → ✅ 행동 유도 중심
