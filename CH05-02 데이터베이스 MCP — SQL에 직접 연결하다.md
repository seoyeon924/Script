---
tags: #CH05 #MCP #SQL #데이터베이스 #SQLite #PostgreSQL
time: 15분
chapter: CH05
status: ✅ 대본완성
---

# CH05-02 데이터베이스 MCP — SQL에 직접 연결하다

## 📌 클립 정보
- **예상시간:** 15분
- **유형:** 슬라이드 2장 + 화면 녹화
- **준비물:** 클로드 코드, 노드 제이에스, (선택) 포스트그레에스큐엘 또는 에스큐라이트

---

## 데이터베이스 MCP가 필요한 이유 (3분)

> 📎 **참고 링크**
> - [SQLite MCP 서버](https://github.com/modelcontextprotocol/servers/tree/main/src/sqlite) — SQLite 연결 공식 코드
> - [PostgreSQL MCP 서버](https://github.com/modelcontextprotocol/servers/tree/main/src/postgres) — PostgreSQL 연결 공식 코드
> - [SQLite 공식 문서](https://sqlite.org/docs.html) — SQLite 문법과 기능

지금까지 씨에스브이 파일로 작업했습니다.
그런데 실무 데이터는 대부분 데이터베이스에 있습니다.

기존 방식은 이렇습니다.

```
데이터베이스 → (수동으로 내보내기) → CSV → 클로드 코드 → 분석
```

데이터베이스 엠씨피를 사용하면 이렇게 됩니다.

```
데이터베이스 → 클로드 코드 → 분석
```

중간 단계가 사라집니다.
항상 최신 데이터로 분석합니다.
매번 파일을 내보낼 필요가 없습니다.

**비유하자면 이렇습니다.**

매번 냉장고에서 재료를 꺼내 식탁에 올려두고 요리하는 대신, 냉장고 문을 열어두고 바로 재료를 사용하는 것입니다.
재료 이동 없이 바로 접근합니다.

---

## SQLite MCP 연결 방법 (5분)

에스큐라이트는 파일 기반 데이터베이스입니다.
별도 서버 없이 파일 하나로 동작합니다.
실습하기에 가장 간편합니다.

**1단계: 샘플 데이터베이스 생성**

파이썬으로 샘플 에스큐라이트 파일을 만듭니다.

```python
# create_db.py
import sqlite3

conn = sqlite3.connect('sales.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS campaigns
             (id INTEGER, date TEXT, channel TEXT, spend REAL, conversions INTEGER, revenue REAL)''')

data = [
    (1, '2024-01-01', 'SNS', 500000, 120, 3600000),
    (2, '2024-01-01', '검색', 300000, 180, 5400000),
    (3, '2024-01-02', 'SNS', 600000, 140, 4200000),
    (4, '2024-01-02', '이메일', 100000, 90, 2700000),
]

c.executemany('INSERT INTO campaigns VALUES (?,?,?,?,?,?)', data)
conn.commit()
conn.close()
print("DB 생성 완료")
```

**2단계: 에스큐라이트 MCP 연결**

```bash
claude mcp add --transport stdio sqlite -- npx -y @modelcontextprotocol/server-sqlite ~/sales.db
```

**3단계: 클로드에게 분석 지시**

```bash
claude
```

> "campaigns 테이블에서 채널별 알오아이를 계산해줘. 알오아이는 (revenue - spend) / spend × 100. 결과를 내림차순으로 정렬해서 보여줘."

클로드 코드가 에스큐엘 쿼리를 작성하고 직접 실행합니다.

---

## PostgreSQL MCP 연결 방법 (4분)

포스트그레에스큐엘은 실무에서 가장 많이 쓰는 데이터베이스입니다.

포스트그레에스큐엘 엠씨피 연결 명령어입니다.

```bash
claude mcp add --transport stdio postgres -- npx -y @modelcontextprotocol/server-postgres "postgresql://user:password@localhost/dbname"
```

따옴표 안의 연결 문자열을 실제 환경에 맞게 수정합니다.
- `user`: 데이터베이스 사용자명
- `password`: 비밀번호
- `localhost`: 서버 주소
- `dbname`: 데이터베이스 이름

연결 후 클로드에게 이렇게 지시합니다.

> "어떤 테이블이 있는지 확인해줘."

> "orders 테이블에서 지난 30일 매출 트렌드를 분석해줘."

에이전트가 테이블 구조를 파악하고 적절한 에스큐엘 쿼리를 작성합니다.

---

## 실전 분석 — DB에서 바로 인사이트 추출 (2분)

데이터베이스 엠씨피가 연결된 상태에서 복잡한 분석도 에이전트에게 맡길 수 있습니다.

예시 지시문입니다.

> "campaigns 테이블을 분석해서 다음 세 가지를 알려줘. 첫 번째, 채널별 총 지출과 총 매출. 두 번째, 알오아이가 가장 높은 채널. 세 번째, 일별 총 매출 트렌드. 결과를 마크다운 리포트로 작성해서 report.md 파일로 저장해줘."

에이전트가 에스큐엘 쿼리를 설계하고, 실행하고, 결과를 분석해서 리포트까지 작성합니다.

---

## 직접 해보기

**목표**: 에스큐라이트 MCP를 연결하고 자연어로 데이터를 분석합니다.

**준비 (터미널에 복붙)**
```bash
cd ~/mcp-test

# 샘플 DB 생성
python3 -c "
import sqlite3
conn = sqlite3.connect('sales.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS sales (date TEXT, product TEXT, qty INT, price REAL)')
c.executemany('INSERT INTO sales VALUES (?,?,?,?)', [
    ('2024-01-01','상품A',10,15000),('2024-01-01','상품B',5,30000),
    ('2024-01-02','상품A',8,15000),('2024-01-02','상품C',12,8000)])
conn.commit(); conn.close(); print('완료')
"

# SQLite MCP 연결
claude mcp add --transport stdio sqlite -- npx -y @modelcontextprotocol/server-sqlite ~/mcp-test/sales.db
```

**클로드에게 이렇게 말합니다**
```
sales 테이블에서 상품별 총 매출 (qty × price)을 계산해서
내림차순으로 정렬해줘. 어떤 상품이 가장 잘 팔리는지 한 줄로 요약도 해줘.
```

→ 에이전트가 에스큐엘 쿼리를 작성하고 결과를 분석합니다.

---

## 핵심 정리 (30초)

데이터베이스 엠씨피를 사용하면 씨에스브이 없이 데이터베이스를 직접 분석합니다.
에스큐라이트는 파일 하나로 바로 실습 가능합니다.
포스트그레에스큐엘도 연결 문자열만 바꾸면 동일하게 사용합니다.

## 다음 클립 예고 (30초)

다음 클립에서는 슬랙 엠씨피를 연결해서 분석 결과를 자동으로 팀에 전달하는 방법을 다룹니다.
분석부터 공유까지 에이전트가 자동으로 처리하는 파이프라인을 만들어보겠습니다.
