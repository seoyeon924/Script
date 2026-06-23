# 3D Globe 실습

**프로젝트**: UNHCR 난민 데이터를 3D 지구본 위에 이동 경로 아크로 시각화
**완성 예시**: https://migrationtrack.netlify.app/
**완성 코드**: https://github.com/seoyeon924/globe

---

## 파일 구성

| 파일 | 설명 |
|---|---|
| `unhcr_data.csv` | UNHCR 난민 데이터 (35,472행, 2020–2025) |
| `CLAUDE.md` | 프로젝트 개요·주의사항 (이 파일) |
| `prompts.md` | 단계별 복붙 프롬프트 (정밀 버전) |

---

## 실행 주의사항

> ⚠️ **반드시 로컬 서버로 실행** — `file://`로 열면 CSV fetch가 차단돼 아크가 아무것도 안 나옴
> ```
> python3 -m http.server 8080
> ```
> → http://localhost:8080 으로 접속

---

## CSV 컬럼 구조

```
fields[0] = Year
fields[1] = Country of Asylum (국가명)
fields[2] = Country of Origin (국가명)
fields[3] = Country of Asylum ISO
fields[4] = Country of Origin ISO
fields[5] = Refugees
fields[6] = Asylum-seekers
```

> ⚠️ 컬럼명에 공백·따옴표 포함 → 이름으로 접근하지 말고 **인덱스(fields[3], fields[4]…)**로 접근할 것

---

## Step 1 — 지구본 뼈대

```
Three.js로 3D 지구본 만들어줘.
검정 우주 배경에 지구 텍스처 입히고, 마우스로 드래그해서 돌릴 수 있게 해줘.
자동으로도 천천히 회전하면 좋겠어.
index.html 파일 하나로 만들어줘.
```

---

## Step 2 — 아크 데이터 연결

```
unhcr_data.csv 파일에 난민 이동 데이터가 있어.
출발 국가에서 도착 국가로 곡선 아크를 그려줘.
난민 수가 많을수록 아크를 굵게, 출발지는 빨간색 도착지는 하늘색으로 그라디언트 줘.
```

---

## Step 3 — 디자인 다듬기

```
우주 느낌으로 디자인 다듬어줘.
배경은 어두운 우주색, 지구 주변에 파란 glow 레이어 추가하고,
별도 배경에 깔아줘 (GLSL 셰이더로).
아크가 흘러가는 애니메이션도 추가해줘.
```

---

## Step 4 — 인트로 + 검색

```
처음 들어왔을 때 인트로 화면이 뜨게 해줘.
제목은 "MIGRATION ATLAS", 클릭하면 사라지고 지구본이 나오게.
그리고 상단에 국가 검색 필터도 추가해줘.
나라 이름 치면 그 나라 아크만 보이게.
```

---

## Step 5 — 모바일

```
모바일에서도 손가락으로 드래그해서 지구를 돌릴 수 있게 해줘.
```

---

> 단계별 정밀 프롬프트(코드 구조 지정 버전)는 **`prompts.md`** 참고.
