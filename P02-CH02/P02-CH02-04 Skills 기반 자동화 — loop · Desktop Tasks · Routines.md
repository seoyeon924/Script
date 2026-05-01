---
tags: #P02 #CH02 #Skills #loop #자동화 #Routines
time: 10분
part: Part 02
chapter: CH02
clip: 04
slides: s20,s21,s22,s13
status: ✅ 대본완성
---

# P02-CH02-04 Skills 기반 자동화 — loop · Desktop Tasks · Routines

---

## s20 — CLIP 04 섹션 브레이크

네 번째 클립, Skills 기반 자동화입니다.

앞에서 Skills를 만들어봤어요.
이번 클립에서는 이 Skills를 스케줄에 태워서 반복 작업을 완전히 자동화하는 방법을 봅니다.

---

## s21 — 세 가지 스케줄 방식

**[화면: 슬라이드]**

Claude Code에는 자동화 방식이 세 가지 있어요.

먼저 각 방식이 어떤 명령어로 실행되는지 왼쪽에 정리돼 있어요.

**첫 번째, `/loop`는 CLI 채팅창에 직접 입력해요.**
`/loop 30m "새 파일 분석 후 리포트"` 이렇게 치면 30분마다 실행됩니다.

**두 번째, Desktop Tasks는 앱 UI에서 설정해요.**
터미널 명령어가 없어요.
앱 상단 메뉴에서 Scheduled Tasks를 선택하고 새 작업을 추가하면 됩니다.

**세 번째, Routines도 CLI 채팅창에서 입력해요.**
`/schedule daily 9am "리포트 생성"` 이렇게 하면 매일 9시에 클라우드에서 돌아가요.

오른쪽 표에 세 가지를 비교해봤어요.

`/loop`는 CLI 세션 안에서 실행되고, 최소 간격은 1분이에요.
개발이나 테스트 중에 모니터링할 때 쓰기 좋아요.
세션이 끊기면 멈춥니다.

Desktop Tasks는 Claude Code 앱이 실행 중일 때 동작하고, 최소 간격도 1분이에요.
일상 반복 작업에 쓰기 좋아요. 앱을 종료하면 멈춰요.

Routines는 Anthropic 클라우드에서 실행돼요.
앱을 꺼도 계속 돌아갑니다.
최소 간격은 1시간이에요.

아래 한 줄 결론이 있어요.
테스트 중이면 `/loop`, 일상 반복이면 Desktop Tasks, 24시간 무인 자동화가 필요하면 Routines입니다.

---

## s22 — Skills + 스케줄 조합

**[화면: 슬라이드]**

Skills와 스케줄을 조합하면 반복 작업이 완전히 자동화돼요.

왼쪽 조합 예시를 보시면요.

```
/loop 1h "/data-analyst 실행해줘"
/schedule weekly monday 9am "/deep-research 주간 트렌드"
```

Skill을 스케줄 명령어 안에 넣으면 됩니다.

오른쪽에 실제 시나리오 세 가지가 있어요.

**시나리오 01, 매일 아침 웹 리서치예요.**
Firecrawl로 뉴스와 트렌드를 수집해서 reports/daily.md로 저장하는 게 매일 08:00에 자동으로 돌아가요.

**시나리오 02, CSV 파일 일괄처리예요.**
data/raw/ 폴더에 새 파일이 생기면 `/data-analyst`가 자동으로 처리해서 processed/ 폴더에 넣어줘요.
`/loop 1h`으로 1시간마다 감지합니다.

**시나리오 03, 주간 분석 리포트예요.**
`/deep-research`가 경쟁사 분석을 해서 reports/weekly.md로 정리하는 게 매주 월요일 9시에 자동으로 실행됩니다.

---

## s13 — 챕터 요약

**[화면: 슬라이드]**

이번 챕터에서 배운 것들을 정리해요.

CLIP 01에서는 MCP 개념과 작동 방식, 활용 가능한 MCP 목록을 봤어요.

CLIP 02에서는 Firecrawl MCP로 웹 크롤링 자동화, API 키와 MCP 연결 방법을 실습했고요.

CLIP 03에서는 반복 워크플로우를 `/명령어`로 저장하는 Skills, 커뮤니티 설치와 직접 제작 방법을 배웠어요.

CLIP 04에서는 `/loop`, Desktop Tasks, Routines 세 가지 스케줄 방식으로 웹 리서치와 파일 처리를 자동화하는 방법까지 봤습니다.

다음 챕터에서는 여러 에이전트가 역할을 나눠서 협업하는 데이터 분석 파이프라인 구조를 만들어봅니다.
