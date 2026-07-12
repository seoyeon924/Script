---
tags: #P03 #CH03 #OpenClaw #AgentManager #Tauri #ClaudeCode #디자인토큰
time: 55분
part: Part 03
chapter: CH03
clip: 03
slides: s17,s18,s19,s20,s40
status: ✅ 대본완성
---

## 🎬 CLIP 03 촬영 가이드

> **촬영 환경:** 본 계정에서 촬영. Agent Manager 빌드 데모를 처음 상태부터 보여주려면 `manager/` 안의 생성된 앱 파일(src/, package.json 등)만 지우고 PROMPT.md·README.md·src-tauri/만 남긴 뒤 시작 — OpenClaw 설정과는 무관해서 안전함.
**슬라이드 순서:** s17 → s18 → s19 → s20 → s40

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

지금까지 클립 01에서 OpenClaw와 에이전트 구조를 살펴봤고, 클립 02에서는 파이프라인과 크론 자동화를 직접 실행해봤습니다.

클립 01에서는 OpenClaw를 설치하고 텔레그램 봇을 연결했어요. 클립 02에서는 Echo가 Aria, Sam, Min, Evan을 순서대로 지휘하는 파이프라인을 직접 돌려봤습니다.

크론 잡으로 매주 월요일 자동 실행까지 연결했고, 결과 파일이 `runs/latest/outputs/` 안에 일곱 개 쌓이는 것도 확인했죠.

이제 세 번째 클립입니다. 지금까지는 터미널로만 에이전트를 관리했어요. 명령어 치고, 출력 보고, 다시 명령어 치고. 에이전트가 한 명일 때는 그게 편한데요. 다섯 명이 동시에 움직일 때는 얘기가 달라집니다.

Echo가 뭐 하고 있는지, Min이 오류 났는지, 크론 잡이 제대로 돌고 있는지를 터미널에서 하나씩 확인하려면 명령어를 네다섯 번 따로 실행해야 해요. 상태가 흩어져 있으니까요.

이 클립에서는 그 문제를 해결하는 도구를 직접 만들어요. 이름이 **Agent Manager**입니다. 에이전트 상태, 실행 결과물, 크론 잡을 전부 한 화면에서 볼 수 있는 네이티브 데스크탑 앱이에요.

앱 예시는 Echo, Min, Evan 세 명 기준으로 만들어요. PROMPT.md의 에이전트 배열에 두 명을 추가하면 다섯 명 전부로 확장할 수 있어요. 그 방법도 뒤에서 알려드릴게요.

만드는 방법이 좀 특이해요. 코드를 직접 짜지 않아요. `manager/` 폴더 안에 **PROMPT.md** 파일이 있습니다. 이 파일 하나에 앱 전체 설계가 다 담겨있어요. Claude Code에 이 파일 내용을 붙여넣으면 React와 Tauri로 된 앱이 자동으로 생성됩니다.

앱 개발 경험이 없어도 됩니다. Tauri가 뭔지 몰라도 됩니다. 프롬프트를 붙여넣고 기다리면 돼요.

그게 이 클립이 보여주고 싶은 것입니다. Claude Code는 "코드 작성 도구"가 아니에요. **설계서를 받아서 앱을 만들어주는 자동화 파트너**입니다. 어떻게 되는지 지금 바로 보겠습니다.

---

## s18 — Dashboard 뷰

**[화면: 터미널 → 앱]**

먼저 터미널을 열어주세요. `manager/` 폴더로 이동합니다.

```bash
cd ~/Projects/openclaw-pipeline-kit/manager
```

이 폴더 안에는 지금 앱 설계서인 `PROMPT.md`, 간단한 안내 `README.md`, 그리고 Tauri 설정이 담긴 `src-tauri/` 폴더만 있어요. 앱 소스 코드는 아직 없습니다. 여기서 Claude Code를 실행할 거예요.

```bash
claude
```

Claude Code가 실행됩니다. 프롬프트 입력창이 뜨면 이제 PROMPT.md 파일을 열어야 해요. 여기서 잠깐, 이 파일에 뭐가 담겨있는지 같이 읽어볼게요.

**[화면: PROMPT.md 파일 열기]**

파일을 열면 맨 위에 이렇게 써있습니다.

```
# OpenClaw Agent Manager — 빌드 프롬프트
아래 내용을 Claude Code에 그대로 붙여넣으세요.
manager/ 폴더 안에서 실행하면 Agent Manager 앱이 자동으로 만들어집니다.
```

그리고 그 아래에 실제 프롬프트가 있어요. 처음 시작 부분입니다.

```
이 폴더(manager/)에 React + TypeScript + Vite + Tauri 2 앱을 만들어줘.
완성되면 npm install && npm run tauri dev 로 바로 실행되게 해줘.
```

기술 스택이 적혀있어요. **Vite 5, React 18, TypeScript, Tauri 2**. Tauri는 Rust로 만든 경량 데스크탑 프레임워크예요. Electron이랑 비슷하지만 훨씬 가볍습니다. 여기서 한 가지만 기억하시면 돼요. 외부 CSS 라이브러리가 없어요. 스타일을 전부 인라인 `style` 객체로 처리합니다.

그 다음에 **디자인 토큰** 섹션이 있습니다.

```
배경: #F9FAFB
텍스트 기본: #191F28
서브 텍스트: #6B7684
비활성: #B0B8C1
테두리: #E5E8EB
파란 accent: #3182F6
활성 배경: #EBF3FE
카드 배경: #FFFFFF
카드 그림자: 0 1px 6px rgba(0,0,0,0.07)
카드 radius: 12px
버튼 radius: 8px
폰트: system-ui, -apple-system, "Apple SD Gothic Neo", sans-serif
```

색상 값이 구체적으로 다 들어있어요. 배경색, 텍스트 색, 테두리 색, 강조색까지. 이게 왜 중요하냐면, Claude Code는 "예쁘게 만들어줘"라는 지시를 받으면 자기 판단으로 색을 고릅니다. 그 결과가 매번 달라져요. 일관된 UI를 원하면 이렇게 토큰을 직접 명시해줘야 합니다.

**에이전트 목록** 섹션도 있습니다.

```
{ id: "main",  name: "Echo", color: "#818cf8", workspace: "~/.openclaw/workspace",      sessionsDir: "~/.openclaw/agents/main/sessions" }
{ id: "min",   name: "Min",  color: "#34d399", workspace: "~/.openclaw/workspace-min",  sessionsDir: "~/.openclaw/agents/min/sessions" }
{ id: "evan",  name: "Evan", color: "#fb923c", workspace: "~/.openclaw/workspace-evan", sessionsDir: "~/.openclaw/agents/evan/sessions" }
```

Echo, Min, Evan 세 명의 에이전트 정보예요. 각자 색상, 워크스페이스 경로, 세션 디렉토리가 지정돼있어요. 이 정보가 `constants.ts` 파일에 딱 한 곳만 들어갑니다. 앱 어디서든 이 파일 하나를 참조해요.

그 다음은 **레이아웃 구조**가 나와요.

```
display:flex; height:100vh
- 왼쪽: Sidebar (width:220px, background:#FFFFFF, borderRight:1px solid #E5E8EB)
- 오른쪽: main (flex:1, overflow:auto, paddingTop:32px)
```

사이드바 너비, 배경색, 테두리까지 픽셀 단위로 다 들어있습니다. 그리고 각 뷰가 어떻게 전환되는지도 써있어요.

```
dashboard → <Dashboard onSelectAgent={fn} />
agent     → <AgentDetail agent={selectedAgent} />
gallery   → <Gallery />
cron      → <CronJobs />
git-sync  → <GitSync />
settings  → <Settings />
```

이 프롬프트에 무려 여섯 개 뷰의 설계가 다 들어있어요. 사이드바 구조, 각 탭, 버튼 클릭 시 동작, 데이터를 어떤 CLI 명령어로 가져오는지까지. 이 파일 하나로 Claude Code가 앱 전체를 만드는 거예요.

이 파일 내용을 전체 선택해서 복사합니다. Claude Code 입력창에 붙여넣어요.

**[화면: Claude Code에 프롬프트 붙여넣기]**

붙여넣고 엔터를 누르는 순간부터 Claude Code가 작동을 시작합니다. 어떤 순서로 만들어지는지 같이 보겠습니다.

Claude Code가 제일 먼저 하는 일은 **파일 구조를 파악하는 것**입니다. PROMPT.md 끝부분에 파일 구조가 명시돼 있거든요.

```
manager/
  package.json
  vite.config.ts
  tsconfig.json
  index.html
  src/
    main.tsx
    App.tsx
    index.css
    constants.ts
    types/
      index.ts
    hooks/
      useTauri.ts
    views/
      Dashboard.tsx
      AgentDetail.tsx
      Gallery.tsx
      CronJobs.tsx
      GitSync.tsx
      Settings.tsx
    components/
      Sidebar.tsx
      ...
  src-tauri/
    tauri.conf.json
    Cargo.toml
    src/
      main.rs
      lib.rs
```

Claude Code가 이 구조대로 폴더와 파일을 하나씩 만들어요. 화면에서 보면 파일 이름이 하나씩 뜨면서 생성됩니다.

먼저 `package.json`이 생겨요. Vite, React, TypeScript, Tauri API, lucide-react 의존성이 들어가 있어요.

다음에 `constants.ts`가 생깁니다. 에이전트 세 명의 정보가 배열로 들어가는 파일이에요.

`types/index.ts`가 생겨요. `Agent`, `View`, `AgentStatus` 같은 TypeScript 타입 정의가 들어갑니다.

`hooks/useTauri.ts`가 생겨요. 이게 중요한 파일이에요. 세 가지 함수가 있어요. `runCommand`는 터미널 명령어를 실행하고 결과를 돌려줍니다. `readFile`은 파일을 읽어요. `writeFile`은 파일에 씁니다. 이 세 함수 덕분에 앱이 `openclaw status` 같은 CLI 명령어를 바로 실행할 수 있어요.

그 다음에 뷰 파일들이 하나씩 만들어집니다. `Dashboard.tsx`, `Gallery.tsx`, `CronJobs.tsx` 순서로요.

마지막으로 `src-tauri/` 폴더 안에 Rust 관련 파일들이 생깁니다. `tauri.conf.json`에는 앱 이름, 윈도우 크기, 권한 설정이 들어가요.

이 전체 과정이 대략 2~3분 안에 끝납니다. 빈 폴더가 완전한 앱 소스코드로 채워지는 거예요.

Claude Code가 완료 메시지를 내보내면 이제 실행할 차례예요.

```bash
npm install && npm run tauri dev
```

`npm install`이 의존성을 설치해요. 처음이라면 1~2분 걸립니다. 그 다음에 `npm run tauri dev`를 실행하면 Rust 컴파일이 시작됩니다. 처음 빌드는 2~3분 더 걸려요. Rust는 첫 빌드만 오래 걸리고, 이후 변경사항은 훨씬 빠르게 반영됩니다.

**[화면: Agent Manager 앱 실행]**

앱 창이 열립니다. 왼쪽에 사이드바가 있고, 오른쪽에 Dashboard가 기본으로 떠있어요.

사이드바를 먼저 보겠습니다. 맨 위에 OpenClaw 로고가 있고, 그 아래 에이전트 세 명이 리스트로 나와요. Echo는 인디고, Min은 에메랄드, Evan은 오렌지 색상 원형 아바타를 쓰고 있어요.

에이전트 목록 아래에 구분선이 있고, 네비게이션 메뉴가 있습니다. Dashboard, Gallery, CronJobs, Git Sync, Settings 다섯 개예요.

사이드바 맨 아래에는 모니터링 위젯이 있어요. 에이전트 세 명의 토큰 사용량이 프로그레스 바로 표시됩니다. `openclaw status` 결과를 실시간으로 파싱해서 보여주는 거예요.

오른쪽 Dashboard를 보겠습니다. 에이전트 카드가 세 개 있어요. 각 카드에 에이전트 이름, 워크스페이스 경로, Agent ID가 표시돼 있어요. "View Files" 버튼과 "Send Message" 버튼도 있습니다.

카드 아래에 **OpenClaw Status** 섹션이 있어요. `openclaw status` 명령어 결과가 그대로 표시됩니다. 옆에 새로고침 버튼이 있어서 클릭하면 최신 상태로 업데이트돼요.

에이전트 카드에서 "View Files"를 클릭해볼게요. 오른쪽 영역이 에이전트 상세 뷰로 바뀝니다. 탭이 네 개 있어요. Files, Heartbeat, History, Send Message. 

**Files 탭**에서는 에이전트 워크스페이스 안 파일 목록이 보여요. 클릭하면 파일 내용이 아래 패널에 바로 미리보기로 표시됩니다.

**Heartbeat 탭**에서는 에이전트의 HEARTBEAT.md 파일 내용을 볼 수 있어요. 편집도 가능하고 저장 버튼도 있어요. 에이전트에게 새 지시를 내려야 할 때 여기서 바로 수정할 수 있습니다.

**History 탭**에서는 세션 기록이 날짜순으로 나와요. 클릭하면 그 세션에서 에이전트가 무슨 대화를 했는지 볼 수 있어요.

**Send Message 탭**에서는 에이전트에게 직접 메시지를 보낼 수 있어요. `openclaw sessions send` 명령어를 앱 안에서 실행하는 거예요.

이제 Gallery 탭으로 넘어가겠습니다.

---

### 💬 썰 타임 — 남들도 대시보드를 만든다 (5분)

> Dashboard 뷰 시연 끝난 직후. 링크 미리 열어두기.

**[화면: 브라우저 — 유튜브]**

- 링크: https://www.youtube.com/watch?v=vPzM2ix4ApM
- 보여줄 것: "오픈클로 200% 활용법" — 에이전트랑 소통하는 커스텀 대시보드를 바이브코딩으로 만든 영상. 완성된 화면 부분 위주로.
- 멘트 포인트: "우리만 이런 걸 만드는 게 아니에요. 이분도 프론트엔드부터 백엔드 연결까지 전부 프롬프트로 만들었어요. 방식이 우리 PROMPT.md 방식이랑 똑같아요. 설계를 글로 쓰면 코드는 AI가 만들어요."

**[화면: 브라우저 — 유튜브]**

- 링크: https://www.youtube.com/watch?v=8Nk9IWhW2Ck
- 보여줄 것: "I built my own OpenClaw" — 메모리 시스템, 하트비트, 채널 어댑터, 스킬을 처음부터 직접 구현한 해외 개발자. 인트로만.
- 멘트 포인트: "이분은 아예 OpenClaw 자체를 자기 버전으로 새로 만들었어요. 구조를 이해하면 여기까지 갈 수 있다는 거예요. 오늘 우리가 만드는 Agent Manager가 그 첫걸음이에요."

---

## s19 — Gallery 뷰

**[화면: 앱]**

사이드바에서 Gallery를 클릭합니다.

**[화면: Gallery 탭 화면]**

화면이 카드 그리드로 채워집니다. 파이프라인이 만든 결과 파일들이에요.

어디서 가져오는 건지 설명할게요. `~/Projects/openclaw-pipeline-kit/runs/` 폴더를 스캔해요. 각 run 폴더 안의 `outputs/` 디렉토리에 있는 파일들을 전부 읽어들입니다.

카드를 하나씩 보겠습니다.

파일 확장자마다 아이콘이 달라요. `.md` 파일은 파란 문서 아이콘, `.html` 파일은 초록 지구본 아이콘, `.csv` 파일은 주황 테이블 아이콘입니다. 이 색 구분 덕분에 어떤 종류의 파일인지 한눈에 보여요.

카드 안에는 파일명이 굵게 써있고, 아래에 수정 날짜가 표시됩니다. 오른쪽 하단에는 담당 에이전트 태그가 있어요. 파일명 번호를 보고 판단합니다. 01, 02로 시작하는 파일은 Aria, 03, 04는 Sam, 05는 Min, 06, 07은 Evan이에요. 클립 02에서 본 파이프라인 순서랑 일치하죠.

카드를 클릭해보겠습니다.

**[화면: 파일 내용 모달 열기]**

모달이 열리면서 파일 내용이 표시됩니다. 마크다운은 그대로 텍스트로, HTML은 미리보기로 볼 수 있어요.

이 기능이 왜 편리하냐면, 터미널에서 결과물을 보려면 `cat` 명령어를 치거나 파일을 직접 열어야 해요. Gallery에서는 클릭 한 번으로 내용을 확인할 수 있어요. 파이프라인이 여러 번 돌아서 결과물이 쌓여있을 때 특히 유용합니다.

오른쪽 상단에 새로고침 버튼도 있어요. 클릭하면 `runs/` 폴더를 다시 스캔해서 최신 파일을 반영합니다.

Gallery 뷰에서 수강생 여러분이 직접 해볼 수 있는 것이 있어요. 파이프라인을 한 번 더 돌리고 Gallery를 새로고침하면, 새로 생긴 결과물이 카드로 나타납니다. 누가 어떤 파일을 만들었는지 에이전트 태그로 바로 구분할 수 있어요.

이제 CronJobs 탭으로 이동하겠습니다.

---

## s20 — CronJobs 뷰

**[화면: 앱]**

사이드바에서 CronJobs를 클릭합니다.

**[화면: CronJobs 탭 화면]**

크론 잡 카드들이 나타납니다. 클립 02에서 등록했던 잡들이 보여요.

어떻게 가져오는지 설명할게요. 앱이 마운트되는 시점에 `openclaw cron list` 명령어를 자동으로 실행합니다. 그 결과를 파싱해서 카드로 표시하는 거예요.

파싱 방법이 조금 특이해요. `openclaw cron list`의 출력 형식은 헤더 줄이 먼저 나오고, 그 아래에 데이터 줄이 나와요. 앱은 헤더 줄에서 각 컬럼의 위치를 먼저 파악합니다. Name, Schedule, Next, Last, Status, Agent ID 컬럼이 몇 번째 글자에서 시작하는지를요. 그런 다음 데이터 줄을 그 위치대로 잘라서 값을 추출합니다.

카드 구조를 보겠습니다. 왼쪽에 상태 아이콘이 있어요. ok는 초록 체크 아이콘, error는 빨간 경고 아이콘, paused는 회색 일시정지 아이콘입니다.

가운데에 크론 잡 이름이 굵게 표시되고, 그 아래에 스케줄이 모노스페이스 폰트로 보여요.

오른쪽에 다음 실행 시간과 마지막 실행 시간이 표시됩니다. 아래에는 담당 에이전트 컬러 배지가 붙어있어요.

상태 색상만으로도 전체 상황을 빠르게 파악할 수 있어요. 카드가 전부 초록이면 정상이에요. 빨간 카드가 보이면 그 잡에 문제가 생긴 겁니다. 회색은 잠시 멈춰둔 상태예요.

새로고침 버튼을 클릭하면 `openclaw cron list`를 다시 실행해서 최신 상태로 갱신됩니다.

이렇게 Agent Manager 하나로 에이전트 상태, 결과물, 크론 잡을 전부 한 화면에서 관리할 수 있어요.

잠깐 지금까지 만든 게 무엇인지 정리해볼게요. 빈 폴더에 PROMPT.md 파일 하나가 있었어요. Claude Code에 그 내용을 붙여넣었더니 React + Tauri 앱이 자동으로 만들어졌습니다. 앱 개발을 한 줄도 직접 짜지 않았는데 대시보드, 갤러리, 크론 뷰가 다 있는 앱이 나왔어요.

이게 가능한 이유가 있습니다. PROMPT.md에 설계가 매우 구체적으로 들어있었거든요. 색상 값, 컴포넌트 이름, 어떤 CLI 명령어로 데이터를 가져오는지, 파일 구조까지. Claude Code는 이 설계서를 코드로 변환하는 역할을 했을 뿐이에요.

이 방식에는 중요한 장점이 있습니다. 나중에 앱을 수정하고 싶을 때 PROMPT.md를 바꾸면 됩니다. "에이전트를 두 명 더 추가해줘"라고 하거나, "Gallery에서 HTML 파일은 실제 렌더링으로 미리보기 해줘"라고 Claude Code에 요청하면 수정해줘요. 코드 구조를 몰라도 자연어로 요청하면 됩니다.

자기 프로젝트에 맞게 바꾸는 방법도 간단해요. PROMPT.md에서 에이전트 목록 부분만 수정하면 됩니다. `AGENTS` 배열에 자기 에이전트 이름과 색상, 워크스페이스 경로를 넣어주면 돼요. 다섯 명이 아니라 세 명이어도 되고, 에이전트 이름을 다르게 써도 됩니다. 파일 하나만 수정하고 Claude Code에 다시 붙여넣으면 새 에이전트에 맞는 앱이 생성됩니다.

마무리로 넘어가겠습니다.

---

이것으로 OpenClaw 업무 자동화 챕터가 끝났습니다.

클립 01에서는 OpenClaw를 이해하고 텔레그램 봇을 연결했어요.

클립 02에서는 파이프라인을 실제로 실행하고, 크론 잡으로 주간 자동화를 연결했어요. CSV 파일 하나를 넣으면 대시보드와 임원 보고서까지 자동으로 나오는 흐름을 만들었습니다.

이번 클립 03에서는 Agent Manager를 Claude Code로 직접 만들었어요. 에이전트 상태, 결과물, 크론 잡을 한 화면에서 모니터링할 수 있는 네이티브 앱입니다.

마무리로 이번 챕터를 끝내고 여러분이 바로 해볼 수 있는 것 세 가지를 드릴게요.

첫 번째는 **자기 데이터로 파이프라인 한 번 돌려보기**입니다. `runs/latest/input/`에 업무 CSV 파일을 넣고 Echo에게 파이프라인 실행을 요청해보세요. 어떤 대시보드가 나오는지 확인해보는 거예요.

두 번째는 **크론 잡 하나 등록하기**예요. 매주 월요일 아침에 자동으로 파이프라인이 돌아가게 설정해두면, 월요일마다 최신 대시보드가 자동으로 생성됩니다.

세 번째는 **Agent Manager를 자기 에이전트에 맞게 수정하기**입니다. PROMPT.md에서 `AGENTS` 배열을 바꾸고 Claude Code에 다시 붙여넣으면, 자기 팀 에이전트 구성에 맞는 Manager가 만들어져요.

챕터 전체를 통해 말하고 싶었던 것은 하나예요. 에이전트 자동화는 코딩 실력의 문제가 아닙니다. 어떻게 역할을 나누고, 어떻게 설계서를 쓰는지의 문제예요. PROMPT.md 파일처럼 설계를 명확하게 적으면 Claude Code가 나머지를 해줍니다.

## s40 — 썰 타임 · 계속 배우려면 (10분)

**[화면: s40 슬라이드 → 브라우저 전환]**

> 챕터 마무리 직전. s40 슬라이드로 학습 리소스 4개 소개 후 브라우저에서 하나씩 열기.

마지막으로, 이 챕터가 끝난 뒤에 어디서 계속 배울 수 있는지 알려드릴게요. 슬라이드에 네 곳을 정리했어요.

- 링크: https://openclaw.ai/showcase/
- 멘트 포인트: "공식 쇼케이스에 새 사례가 계속 올라와요. 아이디어 고갈되면 여기부터 보세요."

- 링크: https://docs.openclaw.ai
- 멘트 포인트: "공식 문서예요. 크론, 채널 연결, 스킬까지 이번 챕터에서 다룬 것들의 상세 옵션이 다 있어요."

- 링크: https://www.youtube.com/watch?v=eaCQ7JO__28
- 멘트 포인트: "『오픈 클로 with GPT, 제미나이, 클로드』 책 저자가 진행하는 한국어 라이브 코딩이에요. 설치는 했는데 뭘 할지 막막할 때 보기 좋아요."

- 커뮤니티: Reddit **r/openclaw** (해외 사례), **지피터스 gpters.org** (한국 사례 공유)
- 멘트 포인트: "막히면 혼자 헤매지 말고 커뮤니티에 검색부터 해보세요. 여러분이 겪는 문제는 대부분 누가 이미 겪었어요."

---

이 챕터에서 배운 구조를 여러분의 업무에 그대로 가져가서 써보세요.
