# Avengers Network Graph 실습

데이터 파일: `avengers_network_data.csv` (80행)
컬럼: Source, Target, Strength, Type, Source_Group, Source_Importance, Target_Group, Target_Importance
완성 예시: https://avengers-network.netlify.app

---

## Step 1 — 기초 네트워크

```
D3.js v7으로 어벤져스 캐릭터 네트워크 그래프 만들어줘.
데이터: avengers_network_data.csv (Source→Target, Strength=선 굵기)
D3 Force Simulation으로 노드 배치. index.html 하나로.
```

---

## Step 2 — 디자인

```
배경: 우주 느낌 (검정 + GLSL 별 파티클)
노드 색상: Source_Group별로 구분 (Asgardians, Guardians, Avengers, Wakanda, Villains)
노드 크기: Source_Importance에 비례
선 굵기: Strength에 비례
폰트: Google Fonts Cinzel
```

---

## Step 3 — 인터랙션

```
노드 드래그 가능하게.
호버 시 연결된 캐릭터만 강조, 나머지 흐리게.
클릭 시 캐릭터 이름 + 그룹 + 연결 수 표시.
```

---

## Step 4 — Tableau Extension 연결 (선택)

```
Tableau Extensions API 추가해줘.
Tableau 워크시트에서 Source/Target 필드 받아서 해당 캐릭터 관계만 필터링.
manifest 파일(.trex)도 만들어줘.
```
