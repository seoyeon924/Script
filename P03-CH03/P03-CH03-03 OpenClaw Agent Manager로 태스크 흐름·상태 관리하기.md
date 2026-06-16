---
tags: #P03 #CH03 #OpenClaw #AgentManager #Tauri #ClaudeCode #디자인토큰
time: 12분
part: Part 03
chapter: CH03
clip: 03
slides: s17,s18,s19,s20,s31
status: ✅ 대본완성
---

## 🎬 CLIP 03 촬영 가이드
**슬라이드 순서:** s17 → s18 → s19 → s20 → s31

#### s17 — 섹션 브레이크 슬라이드만

---

#### s18 — Agent Manager 빌드 데모 `[화면 녹화 — 터미널 → 앱]`

**열 것:** 터미널 + Agent Manager 앱

**Step 1.** manager/ 폴더 이동 + Claude Code 실행
```bash
cd ~/Projects/openclaw-pipeline-kit/manager
claude
```

**Step 2.** PROMPT.md 내용 전체 붙여넣기
```
# PROMPT.md 파일을 열고 내용 전체 복사 → Claude Code에 붙여넣기
```

**Step 3.** Claude Code가 앱 생성 완료 후 실행
```bash
npm install && npm run tauri dev
```

앱이 열리면 Dashboard → Gallery → CronJobs 순서로 보여주기.

---

#### s19 — Gallery 뷰 데모 `[앱 화면]`

Gallery 탭 클릭 → runs/ 폴더 결과 파일 카드 그리드 표시.
카드 클릭 → 파일 내용 모달 미리보기.

---

#### s20 — CronJobs 뷰 데모 + 마무리 `[앱 화면]`

CronJobs 탭 클릭 → `openclaw cron list` 파싱 결과 표시.
ok(초록) / error(빨강) / paused(회색) 상태 보여주기.

---

## s17 — Agent Manager 빌드

마지막 클립이에요. 에이전트 전체를 한 화면에서 모니터링하는 Agent Manager를 Claude Code로 직접 만들어요.

만드는 방법이 특이해요. `manager/` 폴더 안에 PROMPT.md 파일이 있어요. 이 파일에 앱 전체 설계가 담겨있어요. Claude Code에 붙여넣으면 React + Tauri 앱을 자동으로 만들어줘요. 앱 개발 경험 없어도 돼요.

---

## s18 — Dashboard 뷰

**[화면: 터미널 → 앱]**

`manager/` 폴더에 들어가서 `claude`를 실행해요. PROMPT.md 전체를 붙여넣으면 Claude Code가 파일을 자동으로 만들어요.

완료되면 `npm install && npm run tauri dev`로 앱을 실행해요.

Dashboard 탭에서 에이전트 다섯 명 상태를 카드로 볼 수 있어요. `openclaw status` 결과를 실시간으로 가져와서 토큰 사용량까지 보여줘요.

파일 탐색, HEARTBEAT 편집, 세션 히스토리, 메시지 전송까지 에이전트별로 확인할 수 있어요.

---

## s19 — Gallery 뷰

**[화면: 앱]**

Gallery 탭은 파이프라인이 만든 결과 파일을 카드 그리드로 보여줘요.

`runs/` 폴더 안 output 파일들을 자동으로 스캔해요. .md, .html, .csv 파일마다 아이콘이 다르고, 담당 에이전트 태그랑 수정 날짜도 같이 표시돼요.

카드를 클릭하면 파일 내용을 바로 미리볼 수 있어요.

---

## s20 — CronJobs 뷰

**[화면: 앱]**

CronJobs 탭에서는 등록된 크론 잡 상태를 한눈에 볼 수 있어요.

`openclaw cron list` 결과를 자동으로 파싱해서 이름, 스케줄, 다음 실행 시간, 마지막 실행 시간, 상태를 보여줘요. ok는 초록, error는 빨강, paused는 회색이에요.

Agent Manager 하나로 에이전트 상태, 결과물, 크론 잡을 전부 관리할 수 있어요.

---

## s31 — 디자인 토큰으로 대시보드 퀄리티 올리기

**[화면: 슬라이드]**

마지막으로 대시보드를 제대로 만드는 두 가지 방법을 정리할게요.

**PATH A는 키트 그대로 실행**이에요. 레포 클론하고 `bash setup.sh` 하고 파이프라인 실행하면 5분 안에 완성된 대시보드가 나와요. 실습할 때는 이 방법으로 진행해요.

**PATH B는 처음부터 만들기**예요. GitHub 링크 하나를 Claude Code 프롬프트에 붙여넣으면 돼요.

링크는 `github.com/material-foundation/material-tokens`예요. Material Design 3 공식 디자인 토큰 레포예요. 이 링크를 Claude Code에 주면 CSS 변수 시스템을 자동으로 생성해줘요.

프롬프트는 간단해요. "이 레포의 CSS 토큰 구조를 참고해서 대시보드에 적용해줘. `:root`에 MD3 시맨틱 컬러 변수 정의하고, 하드코딩된 색상을 전부 토큰으로 교체하고, 다크 모드도 추가해줘." 이게 전부예요.

그러면 `--md-sys-color-primary`, `--md-sys-color-surface` 같은 변수들이 자동으로 생성돼요. 모든 색상이 토큰 하나로 관리되니까 나중에 브랜드 색상 바꿀 때 한 줄만 수정하면 전체가 바뀌어요.

두 방법 모두 같은 결과가 나와요. 원리를 이해하면 내 브랜드에 맞게 커스텀할 수 있어요.

이것으로 OpenClaw 업무 자동화 챕터가 끝났어요. 에이전트를 등록하고, 파이프라인이랑 크론을 연결하고, Agent Manager로 모니터링까지 완성됐어요.
