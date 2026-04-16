---
tags: #CH03 #Harness #에이전트팀 #자동설계 #ClaudeCode
time: 12분
chapter: CH03
status: ✅ 대본완성
---

# CH03-05 Harness — 에이전트 팀 자동 설계

## 📌 클립 정보
- **예상시간:** 12분
- **유형:** 화면 녹화 + 실습
- **준비물:** Claude Code 설치, Harness 플러그인

---

## 오프닝 (1분)

지금까지 에이전트 팀을 직접 설계하는 방법을 배웠습니다.

이번 클립에서는 그 설계 과정 자체를 자동화하는 도구를 소개합니다.
이름은 Harness입니다. 에이전트 팀 구조를 한 마디로 만들어주는 Claude Code 플러그인입니다.

---

## Harness란? (2분)

**[화면: GitHub 레포 revfactory/harness]**

Harness는 "에이전트 팀 설계를 위한 메타 스킬"입니다.

복잡한 작업을 어떤 에이전트들이 어떻게 나눠서 처리할지 — 이 설계 자체를 Claude Code가 자동으로 해줍니다.

"build a harness for this project" 한 마디를 입력하면:
- `.claude/agents/` — 에이전트 정의 파일 자동 생성
- `.claude/skills/` — 각 에이전트가 쓸 스킬 파일 자동 생성

6단계로 진행됩니다.

```
1단계: 도메인 분석
2단계: 팀 아키텍처 설계
3단계: 에이전트 정의 생성
4단계: 스킬 생성
5단계: 오케스트레이션 연결
6단계: 검증 & 테스트
```

---

## 6가지 아키텍처 패턴 (3분)

**[화면: 패턴 다이어그램]**

Harness는 6가지 팀 구조 중 프로젝트에 맞는 걸 자동으로 선택합니다.

### Pipeline (순차)
Echo → Evan → Min처럼 앞 단계 결과가 다음 단계 입력이 되는 구조.
데이터 분석 파이프라인, 보고서 생성에 적합합니다.

### Fan-out / Fan-in (병렬)
여러 에이전트가 동시에 작업하고 마지막에 결과를 하나로 합칩니다.
각 챕터를 동시에 분석하거나 여러 데이터 소스를 병렬로 처리할 때 씁니다.

### Producer-Reviewer (생성 + 검토)
한 에이전트가 만들고, 다른 에이전트가 검토합니다.
코드 작성 후 코드 리뷰, 대시보드 생성 후 지표 검증에 적합합니다.

### Expert Pool (전문가 풀)
상황에 따라 필요한 전문가 에이전트를 선택적으로 호출합니다.
문제 유형에 따라 다른 분석 방법론을 적용할 때 유용합니다.

### Supervisor (중앙 관리)
중앙 에이전트가 작업을 동적으로 배분합니다.
예측 불가한 작업량이나 우선순위가 계속 바뀌는 상황에 적합합니다.

### Hierarchical Delegation (계층적 위임)
최상위 에이전트가 중간 관리자 에이전트에게 위임하고, 중간 관리자가 실무 에이전트에게 다시 위임합니다.

---

## 설치 방법 (2분)

**[화면: 터미널]**

### 방법 1 — Claude Code 플러그인 마켓플레이스

```
/plugin marketplace add revfactory/harness
/plugin install harness@harness
```

### 방법 2 — 직접 복사

```bash
git clone https://github.com/revfactory/harness.git
cp -r harness/skills/harness ~/.claude/skills/harness/
```

설치 확인:
```bash
ls ~/.claude/skills/harness/
# SKILL.md  references/
```

---

## 실습 — 마케팅 데이터 분석 팀 자동 생성 (3분)

**[화면: 프로젝트 폴더에서 Claude Code 실행]**

마케팅 대시보드 프로젝트 폴더에서 Claude Code를 열고 입력합니다.

```
Build a harness for marketing data analysis.
I need an agent team that can analyze campaign performance,
segment audiences, and generate a dashboard report.
```

Harness가 자동으로 만들어주는 파일들:

```
.claude/
├── agents/
│   ├── data-analyst.md       # 데이터 분석 에이전트
│   ├── campaign-analyst.md   # 캠페인 성과 분석
│   ├── dashboard-builder.md  # 대시보드 생성
│   └── reviewer.md           # 검토 에이전트
└── skills/
    ├── analyze-data/
    │   └── skill.md
    └── build-dashboard/
        └── skill.md
```

이전 클립에서 직접 손으로 만들었던 것과 비교해보세요.
구조가 비슷하지만 만드는 시간이 훨씬 짧습니다.

---

## 직접 해보기

### 실습 — 본인 프로젝트에 적용

프로젝트 폴더에서 Claude Code를 열고:

```
Build a harness for [본인 프로젝트 설명].
I need an agent team that can [주요 작업 설명].
```

자동 생성된 에이전트 파일을 열어서 내용을 확인하고,
실제로 실행해보세요.

---

## 핵심 정리 (1분)

Harness는 에이전트 팀 설계를 자동화합니다.

6가지 아키텍처 패턴 중 프로젝트에 맞는 것을 자동 선택하고,
에이전트 정의와 스킬 파일을 한 번에 생성합니다.

직접 설계하는 방법을 알면 자동 생성 결과를 더 잘 검토하고 수정할 수 있습니다.
앞에서 배운 내용이 여기서 진가를 발휘합니다.

## 다음 클립 예고 (30초)

다음 챕터에서는 멀티 환경 활용을 다룹니다.
로컬 환경과 클라우드 환경을 어떻게 함께 쓰는지 알아봅니다.
