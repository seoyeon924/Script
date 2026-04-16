---
tags: #P03 #CH02 #GoogleSheets #연동 #파이프라인실전
time: 10분
part: Part 03
chapter: CH02
status: 📝 작성필요
---

# P03-CH02-03 Google Sheets 연동 & 파이프라인 실전 실행하기

## 📌 클립 정보
- **예상시간:** 10분
- **유형:** 슬라이드 + 화면녹화

---

## 오프닝 (30초)

(팀 공유 Google Sheets에서 직접 데이터를 읽어 대시보드를 생성하는 실전 시연)

## 본문

### Google Sheets MCP 연동

많은 팀이 Google Sheets를 데이터 원본으로 사용합니다.
MCP를 통해 Claude Code가 직접 Sheets를 읽고 쓸 수 있습니다.

```bash
# Google Sheets MCP 연결
claude mcp add --transport stdio gsheets -- npx -y @anthropic/mcp-google-sheets

# 인증 설정
export GOOGLE_SHEETS_CREDENTIALS="path/to/credentials.json"
```

### Sheets → 대시보드 파이프라인

```
Google Sheets [스프레드시트 ID]의 '마케팅 성과' 시트를 읽어서
채널별 주간 ROI 대시보드를 만들어줘.

새 시트 '분석 결과'에 KPI 요약 표도 추가해줘.
차트는 charts/weekly_dashboard.html로도 저장해줘.
```

### 실시간 데이터 갱신 파이프라인

```markdown
## 자동 갱신 규칙 (CLAUDE.md)

Google Sheets 데이터가 업데이트되면:
1. Sheets에서 최신 데이터 읽기
2. data/processed/에 임시 저장
3. 8단계 파이프라인 실행
4. 대시보드 갱신
5. 팀 채널에 "대시보드 업데이트됨" 알림
```

### 실전 실행 시연

```bash
claude
```

```
Google Sheets에서 이번 주 마케팅 데이터를 가져와서
지난 주 대비 성과 변화를 분석하고
대시보드를 업데이트해줘.
주요 변화 3가지를 슬랙으로 알려줘.
```

---

## 핵심 정리 (30초)

Google Sheets MCP를 연결하면 팀 공유 데이터를 직접 읽어 대시보드를 자동 생성합니다.
실시간 갱신 규칙을 CLAUDE.md에 정의하면 데이터 변경 시 자동으로 파이프라인이 실행됩니다.
이것으로 Part 03 CH02 에이전트 팀 대시보드 자동 생성을 마칩니다.
