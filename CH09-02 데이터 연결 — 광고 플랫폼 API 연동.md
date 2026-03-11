---
tags: #CH09 #마케팅대시보드 #API연동
time: 18분
chapter: CH09
status: ✅ 대본완성
---

# CH09-02 데이터 연결 — 광고 플랫폼 API 연동

## 📌 클립 정보
- **예상시간:** 18분
- **유형:** 화면 녹화 중심
- **준비물:** CH09-01 선행 필수, API 키 준비

---

## 학습 목표 선언 (30초)

이 클립을 마치면 두 가지를 할 수 있습니다.

첫 번째, Google Ads API에서 캠페인 데이터를 자동으로 가져올 수 있습니다.
두 번째, 여러 광고 플랫폼 데이터를 하나로 통합할 수 있습니다.

---

## API 연동이 필요한 이유 (3분)

**[화면: 수동 vs 자동 비교]**

**수동 방식의 문제:**
- 매일 광고 관리자 접속
- CSV 다운로드
- 엑셀에서 수동 정리
- 대시보드 업데이트

**API 자동화 후:**
- 스크립트 한 번 실행
- 모든 플랫폼 데이터 자동 수집
- 대시보드 자동 갱신

하루 30분 절약 × 250일 = 연간 125시간 절약

---

## Google Ads API 설정 (5분)

**[화면: Google Cloud Console]**

Google Ads API를 사용하려면 세 가지가 필요합니다:

1. **개발자 토큰**: Google Ads 계정에서 발급
2. **OAuth 인증 정보**: Google Cloud Console에서 생성
3. **고객 ID**: 광고 계정 번호

**설정 파일 예시 (config/google-ads.json):**
```json
{
  "developer_token": "YOUR_DEVELOPER_TOKEN",
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET",
  "refresh_token": "YOUR_REFRESH_TOKEN",
  "customer_id": "123-456-7890"
}
```

⚠️ 이 파일은 절대 Git에 커밋하지 않습니다.

---

## Claude Code로 데이터 수집 (5분)

**[화면: Claude Code 실행]**

```bash
claude
```

**클로드에게 이렇게 말합니다:**
```
Google Ads API에서 지난 30일 캠페인 데이터를 가져와줘.
config/google-ads.json에 인증 정보가 있어.
가져올 필드: 캠페인명, 노출, 클릭, 비용, 전환, 매출
data/google-ads-30d.csv로 저장해.
```

Claude Code가 자동으로:
1. API 인증 처리
2. 데이터 요청 쿼리 생성
3. 결과를 CSV로 저장

---

## 여러 플랫폼 데이터 통합 (4분)

**[화면: 데이터 통합 다이어그램]**

Google Ads, Meta Ads, 네이버 광고 데이터를 통합합니다:

**클로드에게 이렇게 말합니다:**
```
아래 3개 데이터를 하나로 통합해줘:
- data/google-ads-30d.csv
- data/meta-ads-30d.csv  
- data/naver-ads-30d.csv

통합 규칙:
- 공통 컬럼: 날짜, 플랫폼, 캠페인명, 노출, 클릭, 비용, 전환, 매출
- ROAS 컬럼 추가 (매출/비용)
- CPA 컬럼 추가 (비용/전환)

결과: data/all-platforms-30d.csv
```

통합된 데이터로 플랫폼 간 비교 분석이 가능해집니다.

---

## 자동 수집 스케줄링 (2분)

**[화면: 크론 설정]**

매일 아침 자동으로 데이터를 수집합니다:

```bash
# scripts/daily-collect.sh
#!/bin/bash
cd ~/marketing-dashboard
claude -p "Google Ads, Meta Ads, 네이버 광고에서 어제 데이터를 가져와서 data/daily/에 저장해"
```

```bash
# 크론탭 설정 (매일 오전 7시)
0 7 * * * ~/marketing-dashboard/scripts/daily-collect.sh
```

출근하면 이미 최신 데이터가 준비되어 있습니다.

---

## 직접 해보기

**목표**: 샘플 데이터로 데이터 통합 과정을 실습합니다.

**준비 (터미널에 복붙)**
```bash
cd ~/marketing-dashboard
mkdir -p data/daily
# 샘플 데이터 복사
cp ~/Downloads/패캠-실습자료/CH09/*.csv data/
claude
```

**클로드에게 이렇게 말합니다**
```
data/ 폴더에 있는 광고 플랫폼별 CSV를 확인하고,
하나의 통합 파일로 만들어줘.
ROAS와 CPA 컬럼도 계산해서 추가해.
data/integrated.csv로 저장해.
```

**확인하기**
```bash
head -20 data/integrated.csv
```

## 핵심 정리 (1분)

광고 플랫폼 API로 데이터 수집을 자동화합니다.
여러 플랫폼 데이터를 통합하면 전체 마케팅 성과를 한눈에 볼 수 있습니다.
크론으로 스케줄링하면 매일 자동 업데이트됩니다.

## 다음 클립 예고 (30초)

다음 클립에서는 통합된 데이터로 실제 대시보드 차트를 만들어봅니다.
