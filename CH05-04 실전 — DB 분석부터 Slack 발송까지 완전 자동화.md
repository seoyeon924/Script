---
tags: #CH05 #실전 #자동화 #파이프라인 #MCP통합
time: 15분
chapter: CH05
status: ✅ 대본완성
---

# CH05-04 실전 — DB 분석부터 Slack 발송까지 완전 자동화

## 📌 클립 정보
- **예상시간:** 15분
- **유형:** 화면 녹화 위주 (실전 실습)
- **준비물:** 앞 클립들의 MCP 설정 완료 (에스큐라이트 + 슬랙)

---

## 완전 자동화 파이프라인이란 (3분)

지금까지 엠씨피를 하나씩 연결해보았습니다.
이 클립에서는 여러 엠씨피를 동시에 사용합니다.

완전 자동화 파이프라인 흐름입니다.

```
[에스큐라이트 MCP]          [파일시스템 MCP]       [슬랙 MCP]
데이터베이스 쿼리 → 데이터 수신 → 리포트 파일 저장 → 슬랙 전송
```

클로드 코드 하나가 세 개의 엠씨피를 조율합니다.
에이전트가 상황에 따라 필요한 도구를 골라서 사용합니다.

**구체적으로 말하면,**

요리사가 냉장고, 칼, 오븐을 필요에 따라 순서대로 사용하는 것과 같습니다.
도구가 다양할수록 더 복잡한 요리를 만들 수 있습니다.
에이전트도 엠씨피가 많을수록 더 복잡한 자동화를 처리합니다.

---

## 실전 시나리오 설계 (3분)

마케팅팀 주간 리포트 자동화를 시나리오로 진행합니다.

**목표:**
매주 월요일 아침, 지난 주 광고 성과를 데이터베이스에서 자동 분석하고 슬랙으로 발송합니다.

**사용 MCP:**
- 에스큐라이트 MCP: 광고 성과 데이터베이스 접근
- 파일시스템 MCP: 리포트 파일 저장
- 슬랙 MCP: 마케팅팀 채널에 전송

**에이전트 지시 구조:**

하나의 지시로 전체 파이프라인을 실행합니다.

> "campaigns 데이터베이스에서 지난 7일 데이터를 가져와. 채널별 지출, 전환수, 알오아이를 계산하고, 알오아이 기준 상위 3개 채널과 하위 3개 채널을 파악해. 리포트를 마크다운으로 작성해서 reports/weekly_report.md에 저장하고, 슬랙 #마케팅팀 채널에 주요 인사이트 3줄 요약과 함께 전송해줘."

이 하나의 지시로 에이전트가 여러 도구를 조율해서 전체 과정을 처리합니다.

---

## 실전 구현 — 단계별 화면 실습 (7분)

**1단계: MCP 목록 확인**

```bash
claude mcp list
```

에스큐라이트와 슬랙 엠씨피가 모두 등록되어 있는지 확인합니다.

**2단계: 테스트 데이터베이스 준비**

```bash
python3 -c "
import sqlite3, random, datetime
conn = sqlite3.connect('~/mcp-test/campaigns.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS campaigns (date TEXT, channel TEXT, spend REAL, conversions INT, revenue REAL)')

channels = ['SNS', '검색', '디스플레이', '이메일', '유튜브']
for i in range(14):
    date = (datetime.date.today() - datetime.timedelta(days=i)).strftime('%Y-%m-%d')
    for ch in channels:
        spend = random.randint(100000, 1000000)
        conv = random.randint(20, 300)
        revenue = conv * random.randint(10000, 50000)
        c.execute('INSERT INTO campaigns VALUES (?,?,?,?,?)', (date, ch, spend, conv, revenue))

conn.commit(); conn.close(); print('완료')
"
```

**3단계: 에이전트 실행**

```bash
claude
```

> "campaigns.db 의 campaigns 테이블에서 지난 7일 데이터를 가져와. 채널별 알오아이를 계산하고 (revenue - spend) / spend × 100, 리포트를 reports/weekly.md에 저장한 다음, 슬랙 #general에 상위 3채널 요약을 전송해줘."

**4단계: 결과 확인**

슬랙 채널에 메시지가 도착합니다.
`reports/weekly.md` 파일이 생성됩니다.

---

## 자동화 주기 설정 (1분)

맥에서 크론탭으로 매주 실행합니다.

```bash
crontab -e
```

```
# 매주 월요일 오전 9시 실행
0 9 * * 1 cd ~/mcp-test && claude --print "campaigns.db 분석해서 weekly.md 저장하고 슬랙 전송" >> logs/weekly.log 2>&1
```

`--print` 옵션은 대화 없이 한 번 실행하고 종료합니다.
로그 파일에 실행 결과가 저장됩니다.

---

## 직접 해보기

**목표**: 두 개의 MCP를 동시에 활용해서 분석 + 전송을 자동화합니다.

**준비 확인 (터미널)**
```bash
# MCP 연결 상태 확인
claude mcp list
# sqlite, slack 두 개가 보여야 합니다

claude
```

**클로드에게 이렇게 말합니다**
```
다음 순서로 처리해줘.
1. campaigns.db 에서 채널별 총 매출과 총 지출을 조회해
2. 알오아이 계산해서 순위 매겨
3. 결과를 reports/weekly.md로 저장해
4. 슬랙 #general에 "이번주 광고 성과 요약" 제목으로 상위 3개 채널 전송해
```

→ 에이전트가 DB 조회 → 분석 → 파일 저장 → 슬랙 전송을 자동으로 처리합니다.

---

## 핵심 정리 (30초)

여러 엠씨피를 동시에 사용하면 복잡한 자동화 파이프라인이 가능합니다.
하나의 지시로 데이터베이스 분석, 파일 저장, 슬랙 전송을 순서대로 처리합니다.
크론탭으로 주기를 설정하면 사람이 개입 없이 반복 실행됩니다.

## 챕터 마무리 (30초)

이것으로 CH05 엠씨피 & 외부 도구 연동을 마칩니다.
다음 챕터에서는 시각화 전략 자동 설계를 다룹니다.
데이터 구조를 분석해서 가장 적합한 차트 유형을 에이전트가 자동으로 선택하는 방법을 배웁니다.
