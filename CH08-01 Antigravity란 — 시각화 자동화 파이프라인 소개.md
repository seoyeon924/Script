---
tags: #CH08 #Antigravity #시각화자동화
time: 15분
chapter: CH08
status: ✅ 대본완성
---

# CH08-01 Antigravity란 — 시각화 자동화 파이프라인 소개

## 📌 클립 정보
- **예상시간:** 15분
- **유형:** 슬라이드 3장 + 화면 녹화
- **준비물:** CH06, CH07 선행 권장

---

## 학습 목표 선언 (30초)

이 클립을 마치면 두 가지를 할 수 있습니다.

첫 번째, Antigravity가 무엇이고 왜 사용하는지 설명할 수 있습니다.
두 번째, Claude Code와 Antigravity를 연결해서 시각화를 자동 생성하는 워크플로우를 이해합니다.

---

## Antigravity란 무엇인가 (5분)

**[화면: Antigravity 로고 및 소개]**

Antigravity는 데이터 시각화를 자동으로 생성하고 배포하는 파이프라인 도구입니다.

기존 워크플로우의 문제점을 먼저 살펴봅니다.

**기존 방식의 한계:**
1. 데이터 분석 → 수동으로 차트 생성
2. 디자인 수정 → 매번 수작업
3. 배포 → 파일 복사, FTP 업로드 등

**Antigravity가 해결하는 것:**
1. 데이터 → 자동으로 적절한 차트 타입 선택
2. 브랜드 가이드에 맞게 자동 스타일링
3. 웹 배포까지 원클릭

---

## Claude Code + Antigravity 조합의 힘 (5분)

**[화면: 워크플로우 다이어그램]**

Claude Code와 Antigravity를 함께 사용하면 더 강력해집니다.

```
데이터 분석 요청
    ↓
Claude Code: 데이터 로드 및 분석
    ↓
Claude Code: 인사이트 도출
    ↓
Antigravity: 시각화 자동 생성
    ↓
Antigravity: 웹 배포
    ↓
결과 URL 공유
```

이 전체 과정을 하나의 프롬프트로 실행할 수 있습니다.

**비유하자면:**
Claude Code는 데이터를 이해하고 분석하는 두뇌입니다.
Antigravity는 분석 결과를 시각적으로 표현하는 손입니다.
둘을 연결하면 "생각하고 그리는" 전체 과정이 자동화됩니다.

---

## Antigravity 설치 확인 (3분)

**[화면: 터미널]**

Antigravity가 설치되어 있는지 확인합니다.

```bash
antigravity --version
```

설치되어 있지 않다면:

```bash
npm install -g @antigravity/cli
```

설치 후 초기 설정:

```bash
antigravity init
```

프로젝트 폴더에 `antigravity.config.json` 파일이 생성됩니다.

---

## 직접 해보기

**목표**: Antigravity 설치를 확인하고 첫 번째 프로젝트를 초기화합니다.

**터미널에서 실행**
```bash
mkdir ~/antigravity-test && cd ~/antigravity-test
antigravity init
```

→ 설정 파일이 생성되면 성공입니다.

**확인하기**
```bash
cat antigravity.config.json
```

## 핵심 정리 (1분)

Antigravity는 시각화 자동 생성 및 배포 도구입니다.
Claude Code와 함께 사용하면 데이터 분석부터 시각화 배포까지 완전 자동화됩니다.
다음 클립에서 실제로 데이터를 시각화하는 과정을 실습합니다.

## 다음 클립 예고 (30초)

다음 클립에서는 실제 씨에스브이 데이터를 Antigravity로 시각화하는 실습을 진행합니다.
