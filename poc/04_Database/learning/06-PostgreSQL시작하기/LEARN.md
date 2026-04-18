# Ch.06 - PostgreSQL 시작하기

> **이론 매핑**: `docs/04_Database/04_PostgreSQL/01_시작하기.md` + `02_RDBMS_기본기능.md`

---

## 핵심 요약

PostgreSQL은 1996년 출시 이후 "세계에서 가장 진보한 오픈소스 관계형 데이터베이스"라는 슬로건 아래 발전해 왔다. 단순한 CRUD 처리를 넘어 JSONB, 전문 검색, 벡터 검색, 지리공간 처리까지 하나의 데이터베이스로 커버할 수 있다는 점이 핵심 강점이다. 이 챕터에서는 Docker 기반 설치부터 객체 계층 구조, 제약조건, MVCC까지 PostgreSQL의 기반을 다진다.

---

## 학습 목표

1. Docker를 사용해 PostgreSQL을 설치하고 데이터 영속성을 보장하는 볼륨 설정을 할 수 있다
2. PostgreSQL의 객체 계층(Cluster/Database/Schema/Table)을 설명하고 멀티테넌시 전략을 비교할 수 있다
3. PK, FK, UNIQUE, CHECK 등 제약조건을 활용해 데이터 무결성을 보장할 수 있다
4. MVCC의 동작 원리와 VACUUM의 필요성을 설명할 수 있다
5. psql 명령어로 데이터베이스를 탐색하고 기본 작업을 수행할 수 있다
6. 트리거와 뷰를 활용해 비즈니스 로직을 데이터베이스 레벨에서 구현할 수 있다

---

## 본문

### 1. Docker로 PostgreSQL 시작하기

왜 Docker인가? 로컬 환경에 직접 설치하면 OS별 차이, 버전 충돌, 정리 어려움 등의 문제가 생긴다. Docker를 쓰면 동일한 환경을 어디서든 재현할 수 있고, 실습 후 깔끔하게 제거할 수 있다.

```bash
# 기본 실행 (데이터 휘발성 - 학습용)
docker run --name postgres-server \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=password \
    -p 5432:5432 \
    -d postgres:17

# 프로덕션용 (볼륨 마운트로 데이터 영속성 보장)
docker volume create postgres-volume
docker run --name postgres-server \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=password \
    -p 5432:5432 \
    -v postgres-volume:/var/lib/postgresql/data \
    -d postgres:17
```

Docker 컨테이너는 기본적으로 휘발성이다. 컨테이너를 삭제하면 내부 데이터도 함께 사라진다. `/var/lib/postgresql/data`는 PostgreSQL이 모든 데이터 파일을 저장하는 디렉토리인데, 이 경로를 호스트의 볼륨에 마운트하면 컨테이너가 삭제되어도 데이터는 보존된다.

```
Docker 환경 구조
┌────────────────────────────────────────────┐
│              Docker Host                   │
│  ┌────────────────────────────────────┐    │
│  │     postgres-server Container      │    │
│  │  ┌──────────────────────────────┐  │    │
│  │  │     PostgreSQL 17            │  │    │
│  │  │  Port: 5432 (내부)           │  │    │
│  │  │  Data: /var/lib/postgresql   │  │    │
│  │  └──────────────────────────────┘  │    │
│  └────────────────────────────────────┘    │
│              |  포트 매핑                   │
│         localhost:5432                     │
│              |  볼륨 마운트                 │
│        postgres-volume (영속성)            │
└────────────────────────────────────────────┘
```

psql 접속 후 기본 탐색 명령어는 다음과 같다.

```
psql 주요 명령어
┌──────────────┬────────────────────────────────┐
│ 명령어        │ 설명                            │
├──────────────┼────────────────────────────────┤
│ \l           │ 데이터베이스 목록                │
│ \c dbname    │ 데이터베이스 연결                │
│ \dn          │ 스키마 목록                     │
│ \dt          │ 테이블 목록                     │
│ \d tablename │ 테이블 구조 (컬럼, 인덱스, 제약)│
│ \di          │ 인덱스 목록                     │
│ \x           │ 확장 출력 토글                  │
│ \timing      │ 실행 시간 표시 토글             │
│ \i file.sql  │ SQL 파일 실행                   │
└──────────────┴────────────────────────────────┘
```

### 2. PostgreSQL 객체 계층 구조

PostgreSQL의 객체는 4단계 계층으로 구성된다. 이 구조를 이해하는 것이 멀티테넌시, 권한 관리, 데이터 설계의 출발점이 된다.

```
PostgreSQL 객체 계층
┌─────────────────────────────────────────────────────┐
│  Cluster (PostgreSQL 인스턴스)                        │
│  ├── Database A                                      │
│  │   ├── Schema: public                              │
│  │   │   ├── Table: users                            │
│  │   │   ├── Table: orders                           │
│  │   │   └── View: active_orders                     │
│  │   └── Schema: auth                                │
│  │       ├── Table: sessions                         │
│  │       └── Function: verify_token()                │
│  └── Database B (별도 데이터 공간)                    │
│      └── Schema: public                              │
│          └── ...                                     │
└─────────────────────────────────────────────────────┘
```

각 계층의 역할은 다음과 같다.

- **Cluster**: 하나의 PostgreSQL 인스턴스이며, 하나의 데이터 디렉토리를 소유한다. `postmaster` 프로세스가 관리한다.
- **Database**: 독립된 데이터 공간이다. 중요한 제약이 있는데, Cross-Database 쿼리가 불가능하다. Database A에서 Database B의 테이블을 직접 JOIN할 수 없다.
- **Schema**: 하나의 Database 안에서 객체를 논리적으로 그룹화하는 네임스페이스다. 같은 이름의 테이블이 서로 다른 스키마에 존재할 수 있다.
- **Table/View/Function**: 실제 데이터를 담는 객체들이다.

이 계층 구조는 **멀티테넌시** 설계에 직접 영향을 준다.

| 전략 | 격리 수준 | 복잡도 | 리소스 효율 | Cross 쿼리 |
|------|----------|--------|------------|-----------|
| 테이블 수준 (`tenant_id` 컬럼) | 낮음 | 낮음 | 높음 | 용이 |
| 스키마 수준 (테넌트별 스키마) | 중간 | 중간 | 중간 | 가능 |
| DB 수준 (테넌트별 DB) | 높음 | 높음 | 낮음 | 불가 |

SaaS 서비스에서 고객 간 데이터 격리가 필수라면 스키마 수준이 균형 잡힌 선택이다. `SET search_path TO tenant_a, shared;`로 스키마를 전환하면 애플리케이션 코드 변경 없이 테넌트를 분리할 수 있기 때문이다.

### 3. 제약조건으로 데이터 무결성 보장하기

제약조건은 잘못된 데이터가 들어오는 것을 데이터베이스 레벨에서 차단한다. 애플리케이션에서만 검증하면 버그나 직접 SQL 실행으로 무결성이 깨질 수 있는데, DB 제약조건은 이를 물리적으로 방지한다.

```sql
CREATE TABLE orders (
    -- PRIMARY KEY: 고유 식별자, NOT NULL + UNIQUE 자동 적용
    order_id SERIAL PRIMARY KEY,

    -- FOREIGN KEY: 참조 무결성, 부모 삭제 시 동작 정의
    customer_id INT REFERENCES customers(id)
                    ON DELETE CASCADE,

    -- NOT NULL: 필수 값 강제
    order_date DATE NOT NULL DEFAULT CURRENT_DATE,

    -- CHECK: 비즈니스 규칙을 선언적으로 표현
    amount NUMERIC CHECK (amount > 0),
    status TEXT CHECK (status IN ('pending', 'completed', 'cancelled')),

    -- UNIQUE: 중복 방지
    order_number TEXT UNIQUE
);
```

| 제약조건 | 역할 | 인덱스 자동 생성 |
|---------|------|----------------|
| PRIMARY KEY | 행 고유 식별, NOT NULL + UNIQUE | O (B-tree) |
| FOREIGN KEY | 테이블 간 참조 무결성 | X (수동 생성 권장) |
| NOT NULL | NULL 값 방지 | X |
| UNIQUE | 중복 값 방지 (NULL은 여러 개 허용) | O (B-tree) |
| CHECK | 컬럼 값 범위/패턴 제한 | X |
| EXCLUDE | 범위 중복 방지 (예약 시스템 등) | O (GiST) |

FK에 인덱스가 자동 생성되지 않는 점을 주의해야 한다. JOIN이나 CASCADE DELETE 성능을 위해 FK 컬럼에 인덱스를 수동으로 생성하는 것이 실무에서 일반적이다.

### 4. MVCC와 트랜잭션

PostgreSQL은 MVCC(Multi-Version Concurrency Control)를 사용해 동시성을 관리한다. 핵심 아이디어는 간단하다: UPDATE는 기존 행을 직접 수정하지 않고, 새 버전의 행을 생성한다.

```
MVCC 동작 원리
┌──────────────────────────────────────────────────┐
│  UPDATE users SET name='Bob' WHERE id=1;         │
│                                                  │
│  Heap Page:                                      │
│  ┌─────────────────────────────────────────────┐ │
│  │ Tuple V1: id=1, name='Alice'                │ │
│  │           xmin=100, xmax=150 (삭제 마킹)    │ │
│  ├─────────────────────────────────────────────┤ │
│  │ Tuple V2: id=1, name='Bob'  <-- 새 버전     │ │
│  │           xmin=150, xmax=null               │ │
│  └─────────────────────────────────────────────┘ │
│                                                  │
│  xmin: 이 행을 생성한 트랜잭션 ID                │
│  xmax: 이 행을 삭제/수정한 트랜잭션 ID           │
│  각 트랜잭션은 자신의 스냅샷에 맞는 버전을 본다  │
└──────────────────────────────────────────────────┘
```

이 방식의 장점은 **Reader와 Writer가 서로를 블로킹하지 않는다**는 것이다. 읽기 트랜잭션이 진행 중이어도 쓰기가 가능하고, 그 반대도 마찬가지다.

단점도 있다. 오래된 버전의 행(dead tuple)이 누적되면 테이블이 비대해지고 성능이 저하된다. 이것이 **VACUUM**이 필요한 이유다. PostgreSQL의 autovacuum 데몬이 주기적으로 dead tuple을 정리하지만, 대량 UPDATE/DELETE 후에는 수동으로 `VACUUM ANALYZE`를 실행하는 것이 좋다.

트랜잭션 격리 수준은 4단계가 있다.

| 격리 수준 | Dirty Read | Non-Repeatable Read | Phantom Read |
|-----------|------------|---------------------|-------------|
| Read Uncommitted | 가능 | 가능 | 가능 |
| **Read Committed** (기본값) | 방지 | 가능 | 가능 |
| Repeatable Read | 방지 | 방지 | 방지* |
| Serializable | 방지 | 방지 | 방지 |

*PostgreSQL은 Repeatable Read에서도 MVCC 덕분에 Phantom Read를 방지한다. 이 점이 SQL 표준과 다른 PostgreSQL의 특징이다.

### 5. 뷰와 Materialized View

뷰는 복잡한 쿼리를 캡슐화하는 가상 테이블이다. 실제 데이터를 저장하지 않고, 조회 시마다 정의된 쿼리를 실행한다.

```sql
-- 일반 뷰: 항상 최신 데이터
CREATE VIEW active_orders AS
SELECT o.order_id, c.name, o.amount
FROM orders o
JOIN customers c ON o.customer_id = c.id
WHERE o.status = 'active';

-- Materialized View: 결과를 물리적으로 저장
CREATE MATERIALIZED VIEW monthly_sales AS
SELECT
    DATE_TRUNC('month', order_date) AS month,
    SUM(amount) AS total_sales
FROM orders
GROUP BY 1;

-- Materialized View 갱신
REFRESH MATERIALIZED VIEW CONCURRENTLY monthly_sales;
```

| 구분 | View | Materialized View |
|------|------|-------------------|
| 데이터 저장 | 안 함 | 물리적 저장 |
| 조회 성능 | 매번 쿼리 실행 | 빠름 (사전 계산) |
| 데이터 신선도 | 항상 최신 | REFRESH 필요 |
| 인덱스 | 불가 | 가능 |
| 용도 | 쿼리 캡슐화, 권한 제어 | 대시보드, 리포트 |

`CONCURRENTLY` 옵션은 REFRESH 중에도 읽기를 허용하지만, Materialized View에 UNIQUE 인덱스가 필요하다.

### 6. 트리거와 함수

트리거는 INSERT/UPDATE/DELETE 이벤트에 자동으로 실행되는 함수다. 감사 로그, 자동 타임스탬프 갱신, 연관 테이블 동기화 등에 활용한다.

```sql
-- 자동 updated_at 갱신 트리거
CREATE OR REPLACE FUNCTION update_modified_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.modified_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_modified_at
    BEFORE UPDATE ON orders
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_at();
```

BEFORE 트리거는 실제 작업 전에 실행되어 NEW 값을 수정할 수 있고, AFTER 트리거는 작업 완료 후 실행되어 감사 로그 기록 등에 적합하다. 트리거는 강력하지만 남용하면 디버깅이 어려워지므로, 단순한 값 검증은 CHECK 제약조건으로, 복잡한 로직만 트리거로 구현하는 것이 좋다.

### 7. 역할 기반 접근 제어 (RBAC)

PostgreSQL은 Role 기반으로 권한을 관리한다. Role은 사용자와 그룹의 통합 개념이다.

```sql
-- 읽기 전용 역할
CREATE ROLE app_readonly;
GRANT CONNECT ON DATABASE myapp TO app_readonly;
GRANT USAGE ON SCHEMA public TO app_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_readonly;

-- 읽기/쓰기 역할 (읽기 역할 상속)
CREATE ROLE app_readwrite;
GRANT app_readonly TO app_readwrite;
GRANT INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_readwrite;

-- 실제 로그인 사용자
CREATE USER api_user WITH PASSWORD 'secret';
GRANT app_readwrite TO api_user;
```

Row Level Security(RLS)를 사용하면 행 단위 접근 제어도 가능하다. 멀티테넌시에서 `tenant_id` 기반 격리를 DB 레벨에서 강제할 수 있어, 애플리케이션 버그로 인한 데이터 유출을 방지한다.

---

## 핵심 정리

| 개념 | 한 줄 요약 |
|------|-----------|
| Docker Volume | 컨테이너 삭제 후에도 데이터를 보존하는 영속성 메커니즘 |
| 객체 계층 | Cluster > Database > Schema > Table, Cross-DB 쿼리 불가 |
| 멀티테넌시 | 테이블/스키마/DB 수준 격리, 스키마 수준이 균형 잡힌 선택 |
| 제약조건 | DB 레벨 무결성 보장, FK에는 수동 인덱스 생성 권장 |
| MVCC | UPDATE가 새 버전 생성, Reader/Writer 비블로킹, VACUUM 필요 |
| Materialized View | 쿼리 결과 물리적 저장, REFRESH로 갱신, 대시보드에 적합 |
| RBAC | Role 기반 권한 관리, RLS로 행 단위 접근 제어 가능 |
