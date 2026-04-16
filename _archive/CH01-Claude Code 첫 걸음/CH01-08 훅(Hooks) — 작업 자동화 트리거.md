---
title: CH01-06 훅(Hooks) — 작업 자동화 트리거
chapter: CH01
clip: 06
time: 12분
type: 슬라이드 + 실습
---

# CH01-06 훅(Hooks) — 작업 자동화 트리거

## 클립 목표
훅이 무엇인지 이해하고, 기본 훅을 직접 설정할 수 있습니다.

---

## 1. 훅이란 무엇인가 (2분)

훅(Hook)은 클로드 코드가 특정 동작을 수행할 때, 자동으로 실행되는 사용자 정의 스크립트입니다.

비유하자면, 공장의 품질 검수 체크포인트와 같습니다.
제품이 다음 공정으로 넘어가기 전에, 특정 조건을 검사하고 통과시키거나 차단하는 역할입니다.

예를 들어:
- 클로드가 파일을 저장할 때마다 → 백업 자동 생성
- 코드 실행 전 → 위험 명령어 검사
- 작업 완료 후 → 슬랙으로 완료 알림 전송
- 세션 시작 시 → 데이터 최신화 여부 확인

---

## 2. 훅의 종류 (3분)

클로드 코드에는 여러 훅 이벤트가 있습니다.

| 훅 이벤트 | 언제 실행되는가 |
|-----------|--------------|
| `PreToolUse` | 클로드가 도구(파일 읽기, 실행 등)를 사용하기 직전 |
| `PostToolUse` | 클로드가 도구를 사용한 직후 |
| `SessionStart` | 세션이 시작될 때 |
| `SessionEnd` | 세션이 종료될 때 |

데이터 분석에서 가장 많이 쓰는 훅은 `PostToolUse`입니다.
클로드가 파일을 저장하거나 코드를 실행한 후, 자동으로 결과를 확인하거나 알림을 보내는 데 사용합니다.

---

## 3. 훅 설정 방법 (5분)

훅은 `settings.json` 파일에 설정합니다.

**위치:**
- 전체 프로젝트 공통: `~/.claude/settings.json`
- 특정 프로젝트만: `.claude/settings.json`

**기본 구조:**

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "echo '파일이 저장됐습니다: ' && date"
          }
        ]
      }
    ]
  }
}
```

위 설정은 클로드가 파일을 저장할 때마다 터미널에 시간을 출력합니다.

---

## 4. 실용적인 훅 예시 (2분)

### 예시 1: 파일 저장 시 자동 백업

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "cp -r reports/ backups/reports_$(date +%Y%m%d_%H%M%S)/"
          }
        ]
      }
    ]
  }
}
```

클로드가 reports 폴더에 파일을 저장할 때마다, 타임스탬프가 포함된 백업을 자동 생성합니다.

### 예시 2: 위험 명령어 차단

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo $CLAUDE_TOOL_INPUT | grep -q 'rm -rf' && exit 1 || exit 0"
          }
        ]
      }
    ]
  }
}
```

`rm -rf` 명령어가 포함된 실행 요청을 차단합니다.
`exit 1`을 반환하면 클로드가 해당 작업을 중단합니다.

---

## 직접 해보기

**목표**: 공식 `/hooks` 인터랙티브 메뉴로 훅을 설정합니다. settings.json을 직접 수정하지 않아도 됩니다.

### 방법 1 — `/hooks` 메뉴 (공식 방법)

```bash
# 클로드 코드 세션 시작
claude
```

```
/hooks
```

→ 훅 관리 메뉴가 열립니다.
→ "Add new hook" 선택 → 이벤트 선택 (`PostToolUse`) → 매처 입력 (`Write|Edit`) → 실행할 스크립트 경로 입력
→ 설정이 `~/.claude/settings.json`에 자동 저장됩니다.

### 방법 2 — 클로드에게 부탁하기

```
훅을 설정해줘.
내가 파일을 저장할 때마다 어떤 파일을 수정했는지
~/changes.log에 날짜시간과 파일명을 기록하는 PostToolUse 훅이야.
스크립트 파일도 만들고 settings.json에도 등록해줘.
```

→ 클로드가 스크립트를 생성하고 `~/.claude/settings.json`에 아래 형식으로 등록합니다.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          { "type": "command", "command": "~/.claude/hooks/log-changes.sh" }
        ]
      }
    ]
  }
}
```

**훅 동작 확인**
```
test_file.txt를 만들고 "안녕하세요" 내용으로 저장해줘
```

그 다음 터미널에서 `cat ~/changes.log`를 실행합니다.

**훅 목록 확인 / 제거**
```bash
# 세션 안에서
/hooks
# → 등록된 훅 목록 + 삭제 옵션 표시
```

---

## 핵심 정리

- 훅은 클로드의 작업 전후에 자동 실행되는 사용자 스크립트입니다.
- `settings.json`에 설정합니다.
- 가장 유용한 활용: 파일 저장 후 백업, 위험 명령어 차단, 작업 완료 알림.

다음 클립에서는 서브에이전트를 다룹니다. 큰 작업을 여러 전문 에이전트에게 나눠서 처리하는 방법입니다.

---

## 📎 참고 자료

### awesome-claude-skills ★47,861
Claude Skills 공식 큐레이션 목록. 남들이 만들어둔 스킬을 바로 가져다 쓸 수 있습니다.
공식 레포: https://github.com/anthropics/awesome-claude-skills

> Skills와 Hooks는 함께 이해해야 강력해집니다. 이 챕터에서 "직접 만드는 법"을 배웠다면, 이 레포에서는 "이미 만들어진 것 가져다 쓰기"로 이어주세요. skillsmp.com과 함께 소개하면 수강생이 바로 실무에 적용할 수 있습니다.

---

## 슬라이드 추가 — Hook 이벤트 종류와 실행 시점

**[화면: 아래 표]**

Hooks는 Claude Code의 작업 흐름에서 특정 시점에 자동으로 스크립트를 실행합니다.

| Hook 이름 | 실행 시점 | 실무 활용 예시 |
|-----------|-----------|----------------|
| `PreToolUse` | 도구 실행 직전 | 위험 명령어 차단, 비밀값 포함 여부 검사 |
| `PostToolUse` | 도구 실행 직후 | 파일 저장 후 린트 자동 실행 |
| `SessionStart` | 세션 시작 시 | 프로젝트 상태 로드, 환경 체크 |
| `SessionEnd` | 세션 종료 시 | 작업 요약 저장, 로그 기록 |
| `PreCommit` | 커밋 직전 | 시크릿 탐지, 테스트 통과 여부 확인 |
| `Notification` | 알림 발생 시 | Slack 웹훅, 외부 모니터링 연동 |

**settings.json Hook 설정 예시**

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write",
      "hooks": [{
        "type": "command",
        "command": "npm run lint"
      }]
    }],
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "scripts/safety-check.sh"
      }]
    }]
  }
}
```

**동작 원리**

```
Claude가 파일 저장(Write) 실행
    ↓
PostToolUse Hook 발동
    ↓
npm run lint 자동 실행
    ↓
린트 통과 → 계속 진행
린트 실패 → Claude에게 오류 전달 → 자동 수정
```

