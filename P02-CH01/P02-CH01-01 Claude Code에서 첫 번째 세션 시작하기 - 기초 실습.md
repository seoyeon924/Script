---
tags: #P02 #CH01 #첫세션 #기초실습
time: 10분
part: Part 02
chapter: CH01
status: ✅ 대본완성
---

# P02-CH01-01 Claude Code에서 첫 번째 세션 시작하기 - 기초 실습

## 📌 클립 정보
- **예상시간:** 10분
- **유형:** 슬라이드 2~3장 + 화면 녹화
- **준비물:** Claude Code 설치 완료 (P01-CH02-01 선행 필수)

---

## 오프닝 (30초)

Claude Code가 설치됐습니다. 이제 실제로 어떻게 동작하는지 확인해봅니다.
파일을 만들고, 코드를 실행하고, 결과를 저장하는 전 과정을 처음부터 직접 해봅니다.

---

## Claude Code의 구조 (2분)

Claude Code는 터미널에서 실행하는 AI 에이전트입니다.

ChatGPT와 구조적으로 다른 점:
- ChatGPT: 텍스트를 주고받는 대화 도구
- Claude Code: 실제 파일을 읽고 쓰고 실행하는 에이전트

Claude Code가 사용하는 세 가지 기본 도구:

| 도구 | 역할 |
|------|------|
| Read | 파일 내용을 읽어 Claude에 전달 |
| Write / Edit | 파일 생성 또는 수정 |
| Bash | 터미널 명령어 실행 |

---

## 첫 번째 세션 실행 (5분)

```bash
mkdir my-first-session && cd my-first-session
claude
```

프롬프트가 뜨면 바로 요청합니다.

```
안녕. 현재 폴더 경로를 알려줘.
그리고 hello.txt 파일을 만들어서 "Claude Code 시작!"이라고 저장해줘.
```

Claude가 어떤 도구를 쓰는지, 어떤 명령어를 실행하는지 전 과정을 터미널에서 볼 수 있습니다.
결과만 보여주는 게 아니라 과정이 투명하게 보이는 것이 Claude Code의 특징입니다.

---

## 데이터 분석 첫 실습 (3분)

데이터 분석 맛보기를 해봅니다.

```bash
python3 -c "
import pandas as pd
data = {'channel': ['SNS', '검색', '이메일'], 'revenue': [5000000, 3000000, 1500000]}
pd.DataFrame(data).to_csv('sales.csv', index=False)
print('샘플 데이터 생성 완료')
"
```

Claude에게:
```
sales.csv를 읽어서 채널별 매출 막대 그래프를 만들어줘.
PNG로 저장해줘.
```

---

## 핵심 정리 (30초)

Claude Code는 파일을 직접 읽고, 코드를 실행하고, 결과 파일을 저장하는 에이전트입니다.
"이 CSV 분석해줘"라고 하면 읽기→코드 작성→실행→저장이 자동으로 연결됩니다.
다음 클립에서는 프로젝트 폴더 구조를 파악하는 방법을 배웁니다.
