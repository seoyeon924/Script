---
tags: #패캠 #CH01 #CLAUDE-md
time: 20분
chapter: CH01
status: ✅ 대본완성
---

# CH01-02 CLAUDE.md — 프로젝트 전용 AI 두뇌 설계

## 📌 클립 정보
- **예상시간:** 20분
- **유형:** 슬라이드 3~4장 + 화면 녹화
- **준비물:** 텍스트 에디터, 샘플 프로젝트 폴더

---

## 오프닝 (1분)

Claude Code를 쓸 때 매 세션마다 프로젝트 맥락을 반복 설명하는 건 비효율적입니다.
CLAUDE.md는 그 맥락을 파일에 저장해두는 방식이에요.
프로젝트 루트에 이 파일이 있으면 Claude가 세션 시작 시 자동으로 읽습니다.

---

## CLAUDE.md에 넣을 내용 (4분)

**① 프로젝트 개요** — 이 프로젝트가 뭘 하는지
**② 폴더 구조** — 데이터, 스크립트 위치
**③ 자주 쓰는 명령어** — 실행, 테스트 명령어
**④ 코딩 규칙** — Python 버전, 라이브러리, 변수명 스타일
**⑤ 금지 사항** — 원본 데이터 수정 금지 등

---

## 직접 작성해보기 (10분)

```markdown
# 프로젝트: 마케팅 캠페인 분석 대시보드

## 개요
마케팅팀 캠페인 성과 데이터 분석 및 Tableau 대시보드 제작 프로젝트.

## 폴더 구조
- data/raw/       : 원본 데이터 (수정 금지)
- data/processed/ : 전처리 데이터
- scripts/        : 분석 스크립트
- output/         : 최종 결과물

## 기술 스택
- Python 3.11
- pandas, matplotlib, seaborn
- Tableau Public 연동

## 실행 명령어
- 전처리: python scripts/preprocess.py
- 분석:   python scripts/analyze.py

## 규칙
- data/raw/ 파일은 절대 수정하지 않는다
- 함수마다 한국어 주석 작성
- 결과물은 output/ 에 저장
```

저장 후 새 세션 열고 맥락 설명 없이 바로 요청해봅니다.

> "데이터 전처리 스크립트 실행해줘"

CLAUDE.md를 읽었기 때문에 폴더 위치, 명령어를 알아서 파악합니다.

---

## 계층적 CLAUDE.md (3분)

폴더마다 별도로 만들 수 있습니다.

- 루트: 전체 프로젝트 공통 규칙
- scripts/: 스크립트 작성 규칙
- data/: 데이터 처리 규칙

Claude는 현재 작업 위치에서 가장 가까운 CLAUDE.md를 우선 적용합니다.

---

## 정리 (2분)

CLAUDE.md 하나로 반복 설명이 사라집니다.
프로젝트 초반에 한 번 잘 써두는 게 이후 작업 효율에 직결돼요.

다음은 기본 워크플로우입니다. 파일 읽기, 수정, 실행 직접 해봅니다.

---

## 🗒️ 서연 메모
- [ ] CLAUDE.md 예시 파일 미리 준비
- [ ] 마케팅 샘플 프로젝트 폴더 구성

---

## 직접 해보기

**목표**: 클로드엠디를 작성하고, 클로드가 자동으로 읽는 것을 확인합니다.

**준비 (터미널에 복붙)**
```bash
mkdir ~/claude-md-test && cd ~/claude-md-test
cat > CLAUDE.md << 'EOF'
# 마케팅 분석 프로젝트

## 프로젝트 개요
이 프로젝트는 마케팅 캠페인 성과를 분석합니다.
타겟: 소셜 채널 알오아이 개선

## 데이터 위치
- data/raw/ : 원본 씨에스브이 (수정 금지)
- output/ : 분석 결과 저장

## 규칙
- 숫자는 반드시 소수점 둘째 자리까지
- 결과는 항상 씨에스브이로 저장
EOF
```

**클로드에게 이렇게 말합니다**
```
이 프로젝트 파악됐어? 어디에 데이터가 있어?
```

→ 클로드가 CLAUDE.md를 자동으로 읽고 프로젝트 구조를 설명합니다.
→ 다음 세션에서도 같은 맥락을 유지합니다.

---

## 📎 참고 자료

### claude-mem ★40,601
Claude Code가 작업하는 동안 자동으로 모든 것을 캡처하는 플러그인. 세션이 끝나도 컨텍스트를 보존합니다.
공식 레포: https://github.com/thedotmack/claude-mem

> CLAUDE.md를 수동으로 관리하는 것에서 한 단계 나아가, 자동으로 메모리를 관리해주는 도구도 존재합니다. "이런 도구로 CLAUDE.md를 자동화할 수도 있어요"로 소개하면 수강생의 응용 의지를 높일 수 있습니다.

---

## 슬라이드 추가 — CLAUDE.md 계층 구조 한눈에 보기

**[화면: 아래 다이어그램]**

CLAUDE.md 파일은 한 군데만 있는 게 아닙니다.
위치마다 역할이 다르고, 아래로 갈수록 범위가 좁고 우선순위가 높습니다.

```
📁 ~/ (홈 폴더)
│
└── .claude/
    └── CLAUDE.md        ← ① 글로벌 — 내 컴퓨터 전체, 모든 프로젝트에 적용
                            예: "항상 한국어로 대답해줘"

📁 my-project/ (프로젝트 폴더)
│
├── CLAUDE.md            ← ② 프로젝트 — 팀 공유, Git 커밋
│                           예: "이 프로젝트는 pnpm 사용"
│
├── CLAUDE.local.md      ← ③ 로컬 개인 — 나만 적용, .gitignore 자동 처리
│
└── .claude/
    └── rules/           ← ④ 규칙 분리 — CLAUDE.md 200줄 넘으면
        ├── code-style.md
        ├── testing.md
        └── security.md

📁 my-project/src/auth/
│
└── CLAUDE.md            ← ⑤ 하위 폴더 — 이 폴더 작업 시에만 자동 로드
                            모노레포, 대형 프로젝트에서 유용

🧠 Auto-memory          ← Claude가 알아서 기록 · /memory 로 확인·수정 가능
```

---

**[화면: 3개 카드]**

**겹치면?**
좁은 범위가 이깁니다.
글로벌에서 "탭 4칸" vs 프로젝트에서 "2칸"
→ **2칸 적용**

**뭐부터?**
프로젝트 폴더에 CLAUDE.md 하나만 만드세요.
세 줄이면 됩니다.
`/init` 치면 자동으로 초안도 만들어줘요.

**길어지면?**
200줄 넘으면 `.claude/rules/`로 분리.
주제별 파일로 관리하면 됩니다.

---

## 🗒️ 서연 메모 (업데이트)
- [ ] 슬라이드에 폴더 트리 다이어그램 SVG 삽입 (아래 파일 참고)
- [ ] "겹치면 / 뭐부터 / 길어지면" 3카드 하단 배치
- [ ] Auto-memory 개념: `/memory` 명령어 직접 시연으로 연결
- [ ] 출처: @unclejobs.ai 스레드 (공식 docs 기반 정리)

---

## 슬라이드 추가 — CLAUDE.md 실전 템플릿

**[화면: 아래 코드블록]**

처음 만들 때 이 구조를 그대로 복사해서 채우세요.

```markdown
# Project: [프로젝트명]

## Tech Stack
- [프레임워크]: Next.js 14, TypeScript
- [데이터베이스]: Supabase (PostgreSQL)
- [스타일링]: Tailwind CSS
- [테스트]: Vitest, Playwright

## Architecture
- src/components — React 컴포넌트
- src/services — 비즈니스 로직
- src/utils — 공통 유틸
- src/types — 타입 정의

## Conventions
- 커밋 메시지: Conventional Commits (feat/fix/chore)
- 브랜치: feature/이름, fix/이름
- PR 전에 반드시: lint + typecheck + test 통과
- main 브랜치 직접 커밋 금지

## Testing
- 새 기능은 반드시 단위 테스트 작성
- 테스트 파일: [파일명].test.ts
- 통합 테스트: tests/integration/

## Security
- 환경변수는 .env.local, 코드에 하드코딩 절대 금지
- 모든 사용자 입력 검증 필수
- SQL은 Prepared Statement만 사용
- 의존성 월 1회 보안 업데이트 확인

## Review Checklist
- [ ] 테스트 작성 & 통과
- [ ] 타입 오류 없음
- [ ] 린트 통과
- [ ] 환경변수 .env.example 업데이트
- [ ] README 변경 사항 반영
```

**팁:** `/init` 을 치면 Claude가 현재 프로젝트를 분석해서 이 구조를 자동으로 채워줍니다.

