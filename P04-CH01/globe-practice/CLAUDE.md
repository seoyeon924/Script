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

## 단계 순서

| Step | 내용 |
|---|---|
| 1 | Three.js 지구본 뼈대 — 텍스처, 카메라, 드래그 회전 |
| 2 | UNHCR CSV 로드 → 국가 간 이동 아크 |
| 3 | 디자인 토큰·별 파티클·glow 레이어·아크 애니메이션 |
| 4 | 인트로 오버레이 + 국가 검색 필터 |
| 5 | 모바일 터치 지원 |

단계별 상세 프롬프트는 **`prompts.md`** 참고.
