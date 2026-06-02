---
tags: #P03 #CH03 #OpenClaw #Dashboard #모니터링
time: 10분
part: Part 03
chapter: CH03
clip: 04
slides: s16,s17,s18,s19,s20
status: ✅ 대본완성
---

## 🎬 CLIP 04 촬영 가이드
**슬라이드 순서:** s16 → s17 → s18 → s19 → s20

#### s16~s17 — 슬라이드만

---

#### s18~s20 — Dashboard / Gallery / CronJobs 뷰 `[데모 — 브라우저]`

**열 것:** 브라우저 두 탭

탭 1 — activity-monitor (파이프라인 모니터):
```bash
cd ~/Projects/openclaw-pipeline-kit
python3 -m http.server 9001
# → localhost:9001/activity-monitor.html
```

탭 2 — openclaw-manager:
```bash
openclaw manager
# 또는 슬라이드 내장 영상으로 대체
```

보여줄 포인트:
- **s18 Dashboard 뷰** — Echo/Min/Evan 에이전트 상태 카드
- **s19 Gallery 뷰** — 생성된 파일 썸네일 + 담당 에이전트 태그
- **s20 CronJobs 뷰** — 크론 목록, 다음 실행 시간, ok/error 상태
- **activity-monitor** — 7단계 파이프라인 스테이지 + 에이전트 출력 카드

---

## s16 — 조감도

Clip 01~03에서 연결, 에이전트 생성, 파이프라인 자동화까지 했어요. 마지막 클립이에요. Manager Dashboard로 전체 에이전트 활동을 한 화면에서 모니터링해요.

---

## s17 — CLIP 04 섹션 브레이크

Manager Dashboard예요. Dashboard, Gallery, CronJobs 세 뷰로 구성돼 있어요.

---

## s18 — Manager Dashboard — Dashboard 뷰

**[화면: openclaw-manager 앱]**

Dashboard 뷰에서 에이전트 상태를 카드로 확인해요.

Echo는 메인 에이전트로 파이프라인 전체를 지휘해요. active 상태면 정상이에요. Min은 비즈니스 분석 전담, Evan은 대시보드·보고서 전담이에요.

`openclaw status` 결과를 실시간으로 조회하는 거예요.

---

## s19 — Gallery 뷰

**[화면: openclaw-manager 앱]**

Gallery 뷰는 에이전트가 작업한 프로젝트 히스토리예요.

카테고리별로 정리돼서 썸네일 + 담당 에이전트 + 상태를 한눈에 확인할 수 있어요. 어떤 에이전트가 어떤 프로젝트를 언제 처리했는지 추적이 돼요.

---

## s20 — CronJobs 뷰

**[화면: openclaw-manager 앱]**

CronJobs 뷰는 등록된 크론 잡 전체를 한 화면에서 확인해요.

weekly-dashboard-run, daily-data-summary 같은 크론들의 다음 실행 시간과 마지막 결과 상태를 볼 수 있어요. ok면 정상, error면 실패라서 원인 확인이 필요해요. paused면 일시 정지 상태예요.

이걸로 전체 자동화 파이프라인이 잘 돌아가고 있는지 매일 체크할 수 있어요.
