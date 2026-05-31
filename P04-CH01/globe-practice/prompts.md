# 3D Globe 실습 — 단계별 프롬프트

Claude Code에 아래 순서대로 붙여넣기 하세요.
각 단계가 완성되면 브라우저에서 확인 후 다음 단계로 넘어가요.

---

## Step 1 — 지구본 뼈대

```
Three.js r128 + GSAP 3.12.2로 3D 지구본 만들어줘.
텍스처: https://cdn.jsdelivr.net/gh/mrdoob/three.js@r128/examples/textures/planets/earth_atmos_2048.jpg
SphereGeometry(1, 64, 64), WebGLRenderer, PerspectiveCamera.
마우스 드래그로 회전 가능하게. index.html 하나로.
```

---

## Step 2 — 아크 데이터 연결

```
unhcr_data.csv 로드해서 아크 추가해줘.
Origin ISO → Asylum ISO 방향으로 CatmullRomCurve3 곡선 아크.
Refugees 컬럼 값에 비례해서 아크 굵기 조정.
```

---

## Step 3 — 디자인 토큰 적용

```
아래 디자인 토큰으로 스타일 통일해줘.
배경: radial-gradient(#0d1a2d 0%, #0a0a12 60%, #000 100%)
강조색: #00CCFF
아크: rgba(0,204,255,0.7) → rgba(255,100,100,0.7)
glow: rgba(0,204,255,0.15)
GLSL 파티클 셰이더로 별 추가. 지구 대기 glow 레이어 추가.
아크는 흐르는 대시 애니메이션으로.
```

---

## Step 4 — 인터랙션

```
상단에 국가명 검색 필터 UI 추가.
입력하면 해당 국가 관련 아크만 표시.
클릭 시 인트로 오버레이 닫히게.
```

---

## Step 5 — 모바일

```
터치 드래그 회전 지원 추가. canvas 반응형으로.
```

---

## 완성본 참고

https://github.com/seoyeon924/globe
