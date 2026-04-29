# Claude Code 세션 컨텍스트
> 이 파일을 다른 컴퓨터/세션에서 읽으면 작업 맥락이 바로 이어집니다.
> 새 세션 시작 시: "CLAUDE-SESSION.md 읽고 이어서 작업해줘"

---

## 프로젝트 개요

**경로:** `/Users/sy/Projects/Script`  
**GitHub:** `https://github.com/seoyeon924/Script.git`  
**목적:** Claude Code 입문 강의 슬라이드 + 스크립트 제작

### 파일 구조
```
Script/
├── P02-CH01/
│   ├── P02-CH01-slides.html          ← CH01 슬라이드 (메인 작업)
│   └── P02-CH01-03 파일 읽기·쓰기·실행 & Plan Mode (...).md
├── P02-CH02/
│   └── P02-CH02-slides.html
├── _docs/
│   ├── ppt_design_rules.md           ← PPT 디자인 규칙
│   └── slide-review-feedback.md      ← 교육적 피드백 + 공식 문서 정정 내역
└── CLAUDE-SESSION.md                 ← 이 파일
```

---

## CH01 슬라이드 구조 (최신)

**파일:** `P02-CH01/P02-CH01-slides.html`  
**기술 스펙:** 1280×800px, 단일 HTML, CSS variables, JS로 슬라이드 제어

### JS 상수 (현재 값)
```js
const TOTAL = 29;
const ORDER = [1,6,7,19,24,8,25,9,26,15,16,28, 2,3,4,12,29,21,22,23, 10,11,18,20,13,27,5,17,14];
const CLIP_MAP = {
  1:0,6:0,7:0,19:0,24:0,8:0,25:0,9:0,26:0,15:0,16:0,28:0,  // Clip 0 (12장)
  2:1,3:1,4:1,12:1,29:1,21:1,22:1,23:1,                     // Clip 1 (8장)
  10:2,11:2,18:2,20:2,13:2,27:2,5:2,17:2,14:2               // Clip 2 (9장)
};
```

### 클립 구성
| Clip | 제목 | 슬라이드 ID |
|------|------|------------|
| Clip 0 | 파일 읽기·쓰기·실행 & Plan Mode | s1,6,7,19,24,8,25,9,26,15,16,28 |
| Clip 1 | 프로젝트 폴더 구조 파악하기 | s2,3,4,12,29,21,22,23 |
| Clip 2 | CLAUDE.md | s10,11,18,20,13,27,5,17,14 |

### 슬라이드 목록 (ID → 내용)
| ID | 내용 | Clip |
|----|------|------|
| s1 | 챕터 표지 | 0 |
| s6 | Clip01 섹션 브레이크 | 0 |
| s7 | Read·Write·Bash (언제 써야 하는지 포함) | 0 |
| s19 | Glob·Grep·Bash(ls)·WebFetch | 0 |
| s24 | **[신규]** 실제 워크플로우 — 도구가 연결되는 순간 | 0 |
| s8 | 5가지 실행 모드 (default·acceptEdits·plan·auto·bypass) | 0 |
| s25 | **[신규]** 모드 선택 기준표 — 상황별 추천 모드 | 0 |
| s9 | 취소 & 되돌리기 (공식 rewind 옵션명 수정) | 0 |
| s26 | **[신규]** 실패 사례 — Claude가 틀릴 때 | 0 |
| s15 | /compact Before/After (70% 기준 수치 추가) | 0 |
| s16 | 슬래시 명령어 치트시트 (/effort medium 수정) | 0 |
| s28 | **[신규]** 실습 — 직접 해보기 | 0 |
| s2 | Clip02 섹션 브레이크 | 1 |
| s3 | Claude가 보는 것들 | 1 |
| s4 | Claude Code 폴더 구조 (트리 들여쓰기 표준화) | 1 |
| s12 | 프로젝트 기본 폴더 구조 (CLAUDE.local.md 포함) | 1 |
| s29 | **[신규]** 나쁜 구조 vs 좋은 구조 비교 | 1 |
| s21 | 숨김 폴더 탐색 (Mac: Cmd+Shift+. / Windows) | 1 |
| s22 | CLAUDE.md & settings.json 편집 | 1 |
| s23 | 확장 기능 개요 (Skills/Subagents/MCP/Hooks) | 1 |
| s10 | Clip03 섹션 브레이크 (CLAUDE.md) | 2 |
| s11 | CLAUDE.md vs 자동 메모리 비교표 | 2 |
| s18 | CLAUDE.md 적용 범위 2가지 | 2 |
| s20 | 로드 순서 & @ Import 문법 (충돌 표현 완화) | 2 |
| s13 | CLAUDE.md 작성 시기 + 효과적인 지침 4가지 | 2 |
| s27 | **[신규]** CLAUDE.md before/after 효과 차이 | 2 |
| s5 | CLAUDE.md 직접 만들어보기 | 2 |
| s17 | 실무 예시 (ai-pipeline-kit) | 2 |
| s14 | 챕터 요약 | 2 |

### CSS 주요 변수
```css
--bg: #E8E6E2    /* 크림 배경 */
--white: #1C1A18 /* 본문 텍스트 (실제 검정) */
--border: #E0DDD9
--p01: #E8603C   /* 주황 포인트 */

.code-wrap { background: #0A0C10; border: 1px solid #1E2028; }
.code-hi   { color: rgba(255,255,255,0.88); }
.code-comment { color: rgba(255,255,255,0.52); }
.code-accent  { color: #E8603C; }
```

---

## PPT 디자인 규칙 (필수)

1. **최소 폰트 16px** — 모든 텍스트 최소 16px 유지
2. **문장형 어미 금지** — "~합니다", "~됩니다" → 명사/키워드로
3. **추상·마케팅 타이틀 금지** — "기본부터 잡고 시작" ✗ → "Claude Code 폴더 구조" ✓
4. **설명 중간 줄바꿈 금지** — 20~24자 이내, white-space:nowrap 활용
5. **마케팅 말투 금지** — "검색 한 번으로 발견" ✗ → 구체적 사실로
6. **새 슬라이드 추가 시** — TOTAL, ORDER, CLIP_MAP 모두 업데이트 필수

---

## 스크립트 말투 규칙 (필수)

- 구어체 자연스러운 한국어 (번역체 금지)
- "이 도구들은 꼭 외워야 하는 건 아닌데요" 같은 인간적인 말투
- 어미: "~거든요", "~이에요", "~더라고요"
- 호칭: "여러분" 사용 가능, 격식 과하지 않게

---

## 공식 Claude Code 사실 (정확한 것만)

- **hooks 위치:** `.claude/settings.json`의 `"hooks"` 키 — 별도 폴더 없음
- **CLAUDE.md lazy-load:** 하위 폴더는 해당 폴더 파일 접근 시에만 로드
- **/init:** 코드베이스 분석 후 CLAUDE.md 초안 생성 (이미 있으면 개선 제안)
- **settings.local.json:** 자동으로 .gitignore 처리
- **CLAUDE.local.md:** 수동으로 .gitignore 추가 필요
- **.claude/ 공식 하위 폴더:** `rules/` (경로별 규칙), `commands/` (슬래시 커맨드), `agents/` (서브에이전트), `skills/` (스킬)
- **rules/:** paths frontmatter로 path-scoped rules, ~/.claude/rules/ user-level rules 모두 공식 지원
- **LS 도구:** 공식 도구 목록에 없음. 폴더 탐색은 Bash(ls) 또는 Glob으로 처리
- **실행 모드 5가지:** default(기본값/Ask) → acceptEdits → plan → auto(Team/Enterprise) → bypass
- **Shift+Tab 전환 순서:** default → acceptEdits → plan → auto
- **/effort 옵션:** low | medium | high | max | auto ("mid" 아님)
- **VS Code rewind 공식 옵션:** Restore code and conversation / Restore conversation / Restore code / Summarize from here
- **CLAUDE.md 로드 방식:** 모든 파일을 순서대로 concatenate. 충돌 시 Claude가 임의 선택 (명시적 우선순위 없음)

---

## 작업 중 미완성 항목

- [ ] CH01 s14 챕터 요약 내용 업데이트 (신규 슬라이드 반영)
- [ ] CH01 스크립트 대본 전체 검토 (슬라이드 변경 반영 — 새 슬라이드 6개 대본 작성)
- [ ] CH02 슬라이드 전체 검토

---

## 다른 컴퓨터에서 이어받는 방법

```bash
# 1. 레포 클론
git clone https://github.com/seoyeon924/Script.git
cd Script

# 2. 이 파일 읽고 Claude에게 전달
# Claude Code 열고 첫 메시지:
# "CLAUDE-SESSION.md 읽고 이어서 작업해줘"
```

---

## 주요 변경 이력

### 2026-04-29 — 대규모 업데이트
**공식 문서 정정 (6건):**
- rules/ 복원 — 공식 .claude/ 하위 폴더 맞음
- LS 도구 제거 → Bash(ls)로 수정 (공식 Tools reference에 LS 없음)
- s8 실행 모드: 4가지 → 5가지, 기본값 수정 (default=Ask), auto 모드 추가
- s9 VS Code rewind 옵션명 공식 명칭으로 교체
- s16 /effort: "mid" → "medium"
- s20 로드 충돌 표현: "나중 파일 우선" → "concatenate, Claude 임의 선택"

**신규 슬라이드 6개 추가:**
- s24: 실제 워크플로우 (Bash ls → Glob → Read → Write → Bash → Edit 루프)
- s25: 모드 선택 기준표 (상황별 추천 모드 표)
- s26: 실패 사례 (파일 덮어쓰기 / hallucination / 컨텍스트 초과)
- s27: CLAUDE.md before/after (효과 차이 시각화)
- s28: 실습 (마케팅 데이터 분석 파이프라인)
- s29: 나쁜 구조 vs 좋은 구조 비교

**기존 슬라이드 보강:**
- s7: Read/Write/Bash에 "언제 써야 하는지" 추가
- s15: /compact에 70%·100턴 기준 수치 추가
- 트리 들여쓰기 표준화 (└── 다음 │ → 공백으로)
