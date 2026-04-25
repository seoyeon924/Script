# CH02 참고 리서치 — 외부 교육 자료 분석
> 조사 일자: 2026-04-25 | 출처: 5개 URL 직접 분석

---

## 1. Anthropic Academy — Claude 101
**출처:** https://anthropic.skilljar.com/claude-101/

### 커리큘럼 구성
- 섹션 1: Claude 만나기 (첫 대화, 더 나은 결과 얻기)
- 섹션 2: Claude 데스크탑 앱 (채팅·협업·코드 통합 소개)
- 섹션 3: 작업 정리 (프로젝트, 아티팩트, 스킬)
- 섹션 4: Claude 확장 (외부 도구 연결, 리서치 모드)
- 섹션 5: 종합 (역할별 활용 사례)
- 섹션 6: 수료증 발급

### CH02 관련 내용
- Claude Code는 섹션 2에 이름만 언급 — 전용 모듈 없음
- 비기술 비즈니스 사용자 대상, 코딩 선수지식 불필요
- 무료 수강, Anthropic 계정 없이도 등록 가능
- 수료증 발급 → 학습 완료 동기 부여 설계

---

## 2. Anthropic Academy — Claude Code in Action
**출처:** https://anthropic.skilljar.com/claude-code-in-action

### 핵심 학습 목표 (공식 명시)
1. 파일 조작·명령 실행·코드 분석 핵심 도구 활용
2. `/init`, CLAUDE.md 파일, `@` 멘션으로 컨텍스트 관리
3. 핫키·명령어로 대화 흐름 제어
4. Plan Mode·Thinking Mode 활용 (복잡한 작업)
5. 반복 작업 자동화를 위한 커스텀 명령어 제작
6. MCP 서버로 Claude Code 확장 (브라우저 자동화 등)
7. GitHub 연동으로 PR 리뷰·이슈 처리 자동화
8. 훅(Hook)으로 추가 동작 삽입

### 강의 구조
- 총 10강, 약 1시간 분량, 퀴즈 1개
- 사전 조건: 커맨드라인 기본 지식 + Claude Code 설치 완료 + API 키
- 대상: 개발 워크플로우를 AI로 가속하려는 엔지니어

### CH02 관련 핵심 포인트
- 설치 과정은 다루지 않음 — 이미 설치된 상태 가정
- **CLAUDE.md 파일을 "핵심 컨텍스트 관리 도구"로 강조** → 우리 강의에서 더 앞당겨 소개할 가치 있음
- `@` 파일 멘션, Plan Mode는 선택 기능이 아닌 핵심 기능으로 취급

---

## 3. CC101 — 커뮤니티 한국어 가이드
**출처:** https://cc101.axwith.com/ko

### 설치 관련 핵심 정보 (섹션 04)

**현재 공식 설치 명령어:**
```bash
# macOS / Linux
curl -fsSL https://claude.ai/install.sh | bash

# macOS Homebrew 대안
brew install --cask claude-code

# Windows PowerShell
irm https://claude.ai/install.ps1 | iex

# Windows WinGet
winget install Anthropic.ClaudeCode
```

**⚠️ 중요 경고:**
- `npm install -g @anthropic-ai/claude-code` → **deprecated, 사용 금지**
- Node.js 별도 설치 불필요 (네이티브 인스톨러)
- Windows는 Git for Windows 필요

**인증 방식:** `claude` 실행 → 브라우저 자동 오픈 → claude.ai 계정 로그인 → 터미널 자동 복귀

**확인 명령어:**
```bash
claude --version
claude doctor  # 진단
```

### 입문자 워크플로우 (섹션 05)
1. 프로젝트 폴더로 이동 (`cd ~/Desktop/my-project`)
2. `claude` 실행 (인터랙티브 모드 진입)
3. CLAUDE.md 자동 생성 요청
4. 자연어로 작업 지시
5. 결과 검토 후 피드백
6. `/quit` 또는 `Ctrl+D`로 종료

### 효과적인 프롬프팅 규칙
- **구체적으로**: "코드 고쳐줘" ❌ → "login.js 42번 줄 TypeError 고쳐줘" ✅
- 한 번에 하나씩 요청
- 출력 형식 명시 ("파일로 저장" vs "텍스트로 설명")
- `@파일명` 으로 특정 파일 직접 참조
- 큰 작업 전에 Plan Mode 활용 (`Shift+Tab` 두 번 또는 `/plan`)

### 보안 주의사항 (명시적)
- API 키, 비밀번호, 개인키 절대 채팅에 입력 금지
- `sudo` 요청 시 이유 먼저 확인
- 대규모 변경 전 `git commit` 필수

### 구독 플랜 현실적 설명
| 플랜 | 월 요금 | 적합도 |
|------|---------|--------|
| Pro | $20 | 체험용 — 집중 사용 시 약 1시간이면 한도 도달 |
| Max | $100 | 실무 추천 (Pro 대비 5배 한도) |
| Max | $200 | 헤비 유저 (Pro 대비 20배 한도) |

### 한국어 입문자 추천 플러그인
- `show-me-the-prd` — 인터뷰 5~6개로 PRD 자동 생성
- `deep-research` — 멀티에이전트 병렬 리서치 보고서
- `git-teacher` — 비개발자용 Git 입문
- `vibe-sunsang` — 요청 품질 분석 (A~D 등급 코칭)

---

## 4. Anthropic 개발자 학습 허브
**출처:** https://www.anthropic.com/learn/build-with-claude

### Claude Code 관련 리소스 목록
- Claude Code 설치 가이드
- IDE 통합 방법
- Google Vertex / Amazon Bedrock 연동
- 일반적인 워크플로우 모음
- 문제 해결 가이드
- 관련 강의: "Claude Code 빠르게 배우기", "서브에이전트 입문", "에이전트 스킬 입문"

**⚠️ 주의:** 해당 페이지 해커톤 섹션에 구버전 `npm install` 명령어가 여전히 노출됨 — cc101 가이드에서 이미 deprecated 경고

---

## 5. Anthropic 업무용 학습 허브
**출처:** https://www.anthropic.com/learn/claude-for-work

### Claude Code vs Claude Cowork 구분
- **Claude Code**: 엔지니어·개발자 대상, 터미널 CLI 도구
- **Claude Cowork**: 비기술 직군 대상, 파일 협업 도구 (터미널 불필요)

### 직무별 활용 사례 제공
마케팅, 인사, PM, 영업, 기획 등 비개발 직군 대상 사용법 제공

---

## CH02에 적용할 수 있는 개선 포인트 (교육 설계자 관점 피드백)

### 🔴 즉시 반영 권장

**1. npm 설치 명령어 경고 추가**
- 많은 블로그·유튜브가 여전히 `npm install -g @anthropic-ai/claude-code` 소개
- 수강생이 혼란스러울 수 있음 → 슬라이드에 "이건 쓰지 마세요" 명시 필요
- 출처: cc101.axwith.com/ko 섹션 04

**2. 구독 플랜 현실적 조언**
- Pro $20은 체험용 — 집중 사용 시 1~2시간이면 한도 도달한다는 사실을 미리 알려야 함
- 수강생이 "강의 중에 한도가 찼다"는 경험을 하면 이탈율 급증
- 출처: cc101.axwith.com/ko 섹션 03

**3. Windows 사용자 WSL 안내**
- 현재 CH02 스크립트에 WSL 옵션 누락
- Windows 환경에서 Claude Code 사용 시 WSL이 권장 환경임
- 출처: cc101.axwith.com/ko 섹션 04

**4. `claude doctor` 진단 명령어 소개**
- 설치 문제 발생 시 첫 번째로 실행해야 할 명령어
- "설치가 안 될 때" 섹션에 추가하면 수강생 혼란 크게 줄어듦

### 🟡 다음 챕터 예고로 연결 권장

**5. CLAUDE.md 개념 조기 언급**
- Anthropic 공식 강의(URL 2)에서 CLAUDE.md를 핵심 기능으로 강조
- 현재 CH02에서 전혀 언급 없음 → 세팅 완료 후 "다음에 이걸 배울 거예요"로 예고하면 학습 동기 유지
- 출처: anthropic.skilljar.com/claude-code-in-action

**6. 첫 대화 예시 품질 향상**
- 현재: "안녕. 현재 열려 있는 폴더 이름을 알려줘"
- 개선안: "data 폴더 안에 있는 CSV 파일 목록 보여줘" → 데이터 시각화 강의 맥락에 더 맞음
- 수강생이 "이게 실제로 쓸 수 있는 도구구나"를 느끼는 첫 경험이 중요

**7. 보안 기초 안내 한 줄**
- API 키·비밀번호를 채팅에 입력하지 말라는 기본 주의사항 추가
- 입문자일수록 이 경계가 모호함
- 출처: cc101.axwith.com/ko 섹션 00 (FAQ 선행 안내 방식)

### 🟢 강의 구조 강화 제안

**8. FAQ 선행 섹션 도입**
- cc101.axwith.com은 설치 전 4개의 FAQ로 시작 — 수강생이 "이거 나한테 맞나?" 먼저 해소
- CH02 오프닝에 3분 분량 Q&A 추가 권장:
  - "Pro vs Max 어떤 걸 써야 하나요?"
  - "맥북 없으면 못 하나요?"
  - "코딩 모르면 쓰기 어렵지 않나요?"

**9. 수료 동기 부여 장치**
- Anthropic Academy는 수료증 발급으로 완주 동기 설계
- CH02 마무리에 "설치 완료 인증샷" 챌린지 또는 커뮤니티 인증 요소 추가 고려

**10. 터미널 vs 에디터 선택 이유 명확히**
- 현재 "Antigravity 에디터 씁니다" → 이유가 약함
- 보강: "터미널 모드도 있지만, 데이터 시각화 작업에서는 파일을 보면서 동시에 수정하는 게 훨씬 편해서요 — 특히 HTML/CSS 결과물을 바로바로 확인할 때"
- 출처: cc101.axwith.com/ko 섹션 00 (터미널 vs 데스크탑 비교표)
