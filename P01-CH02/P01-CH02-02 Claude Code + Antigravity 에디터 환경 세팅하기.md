---
tags: #P01 #CH02 #Antigravity #에디터 #환경세팅 #Claude Code Extension
time: 10분
part: Part 01
chapter: CH02
status: ✅ 대본완성
---

# P01-CH02-02 Claude Code + Antigravity 에디터 환경 세팅하기

## 📌 클립 정보
- **예상시간:** 10분
- **유형:** 화면 녹화 (Antigravity 에디터)
- **준비물:** Claude Code 설치 완료 (P01-CH02-01 선행), claude.ai Pro 이상 구독

---

## 오프닝 (1분)

이번 클립은 이 강의에서 가장 중요한 세팅입니다.

Antigravity 에디터를 설치하고, 안에 Claude Code 익스텐션을 연결합니다.
이 환경이 갖춰지면, 이후 모든 실습은 이 에디터 안에서 진행합니다.

잠깐, Antigravity가 뭔지부터 짚겠습니다.

---

## Antigravity란 무엇인가 (2분)

Antigravity는 AI 네이티브 코드 에디터입니다.
VS Code와 비슷하게 생겼지만, AI와의 협업을 기본으로 설계되어 있습니다.

우리가 Antigravity를 쓰는 이유는 세 가지입니다.

**1. 에디터 안에서 Claude Code와 채팅합니다.**
오른쪽 패널에서 자연어로 요청하면, Claude가 파일을 읽고 수정하고 실행합니다.
터미널을 별도로 열 필요가 없습니다.

**2. 파일 변경을 실시간으로 봅니다.**
Claude가 파일을 수정하면, 에디터에서 diff 형태로 바로 보입니다.
수정 내용을 눈으로 확인하면서 승인하거나 되돌릴 수 있습니다.

**3. Claude Pro/Max 구독으로 API 추가 비용 없이 씁니다.**
별도 API 키 없이 구독 내에서 사용할 수 있습니다.

**지원 환경:**
- macOS: Apple Silicon (M1/M2/M3/M4), macOS 12 이상
- Windows: Windows 10 64비트 이상
- Intel Mac: 지원하지 않습니다

---

## Antigravity 설치 (2분)

**[화면: 브라우저]**

`antigravity.google` 에 접속합니다.
macOS 또는 Windows 버전을 내려받아 설치합니다.

설치는 일반 앱 설치와 동일합니다.
macOS는 .dmg 파일 열고 Applications에 드래그, Windows는 .exe 실행입니다.

---

## Claude Code 익스텐션 설치 및 연결 (3분)

**[화면: Antigravity 에디터]**

Antigravity가 실행됐으면, Claude Code 익스텐션을 설치합니다.

**Step 1: 익스텐션 설치**

왼쪽 사이드바에서 퍼즐 조각 모양 익스텐션 아이콘을 클릭합니다.
검색창에 "Claude Code"를 입력합니다.
Install 버튼을 클릭하고, 설치 후 Enable을 클릭합니다.

**Step 2: 계정 연결**

설치 후 익스텐션 패널 상단에 주황색 꽃 모양 아이콘이 생깁니다.
클릭하면 "Connect Account" 버튼이 나타납니다.

클릭하면 브라우저가 열리면서 claude.ai 인증 화면이 나타납니다.
로그인 후 인증 코드를 복사해서 에디터로 돌아와 붙여넣습니다.

연결 완료 메시지가 뜨면 끝입니다.

---

## 작업 환경 구성 (2분)

이제 실제로 쓸 레이아웃을 잡습니다.

**[화면: Antigravity 레이아웃]**

**Step 1: 프로젝트 폴더 열기**

File → Open Folder → 작업할 폴더를 선택합니다.
이 강의에서는 바탕화면에 `data-viz-project` 폴더를 만들어 씁니다.

**Step 2: Claude Code 패널 열기**

오른쪽에 Claude Code 채팅 패널이 나타납니다.
이 패널이 우리의 주 작업 공간입니다.

**Step 3: 내장 터미널 열기 (필요할 때만)**

Ctrl + ` (백틱)으로 하단에 터미널이 열립니다.
Claude가 작업하는 모습을 볼 때, 또는 직접 명령어를 실행해야 할 때 씁니다.

**우리가 쓸 기본 레이아웃:**
- 왼쪽: 파일 탐색기 + 에디터
- 오른쪽: Claude Code 채팅 패널
- 하단: 터미널 (필요 시)

---

## 첫 번째 대화 테스트 (1분)

환경이 제대로 세팅됐는지 확인합니다.

오른쪽 Claude Code 패널에 다음을 입력합니다.

```
안녕. 현재 열려 있는 폴더 이름을 알려줘.
```

폴더 이름이 나오면 정상입니다.

이번에는 파일을 만들어봅니다.

```
hello.txt 파일을 만들어줘. 내용은 "Claude Code + Antigravity 세팅 완료"라고 써줘.
```

에디터 왼쪽 파일 탐색기에 hello.txt가 생기면 환경 세팅이 완료된 겁니다.

---

## 핵심 정리 (30초)

앞으로 이 강의에서 쓸 환경입니다.

- **Claude Code 채팅 패널**: 자연어로 작업 지시
- **에디터**: 파일 내용 확인 및 검토
- **터미널**: 꼭 필요할 때만 사용

터미널 명령어를 외울 필요 없습니다.
채팅 패널에서 말하면, Claude가 알아서 실행합니다.

다음 파트에서 이 환경으로 첫 번째 데이터 시각화를 만들어봅니다.
