# Chapter 2: Standard RDBMS Capabilities - 면접정리

## 핵심 개념 상세 설명

### 1. 데이터베이스 계층 구조

```
PostgreSQL 객체 계층
┌─────────────────────────────────────────────────────────────┐
│                    Postgres Cluster                         │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                   Database                           │    │
│  │  ┌─────────────────────────────────────────────┐    │    │
│  │  │                  Schema                      │    │    │
│  │  │  ┌───────────┐ ┌───────────┐ ┌───────────┐  │    │    │
│  │  │  │  Table    │ │   View    │ │ Function  │  │    │    │
│  │  │  │ ┌───────┐ │ │           │ │           │  │    │    │
│  │  │  │ │Column │ │ │           │ │           │  │    │    │
│  │  │  │ └───────┘ │ │           │ │           │  │    │    │
│  │  │  └───────────┘ └───────────┘ └───────────┘  │    │    │
│  │  └─────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘

계층별 역할:
• Cluster: PostgreSQL 인스턴스 (1개 데이터 디렉토리)
• Database: 독립된 데이터 공간 (Cross-DB 쿼리 불가)
• Schema: 논리적 네임스페이스 (같은 DB 내 테이블 그룹화)
• Table/View/Function: 실제 데이터 객체
```

### 2. 멀티테넌시 전략

```
┌────────────────────────────────────────────────────────────────┐
│                    멀티테넌시 3가지 전략                         │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  【 Level 1: 테이블 수준 】                                     │
│  ┌──────────────────────────────────────┐                      │
│  │  orders 테이블                        │                      │
│  │  ┌──────────┬─────────┬─────────┐    │                      │
│  │  │ tenant_id│ order_id│ amount  │    │                      │
│  │  ├──────────┼─────────┼─────────┤    │                      │
│  │  │    A     │    1    │  100    │    │  WHERE tenant_id=?   │
│  │  │    B     │    2    │  200    │    │                      │
│  │  └──────────┴─────────┴─────────┘    │                      │
│  └──────────────────────────────────────┘                      │
│  장점: 단순함 / 단점: 격리 약함, 쿼리에 조건 필수               │
│                                                                │
│  【 Level 2: 스키마 수준 】                                     │
│  ┌──────────────────────────────────────┐                      │
│  │  Database: myapp                      │                      │
│  │  ├── schema: tenant_a                 │                      │
│  │  │   └── orders (tenant A 전용)       │  SET search_path    │
│  │  ├── schema: tenant_b                 │  TO tenant_a;       │
│  │  │   └── orders (tenant B 전용)       │                      │
│  │  └── schema: shared                   │                      │
│  │       └── common_codes                │                      │
│  └──────────────────────────────────────┘                      │
│  장점: 중간 격리, 공유 스키마 가능 / 단점: 스키마 관리 필요      │
│                                                                │
│  【 Level 3: 데이터베이스 수준 】                               │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐                  │
│  │ DB: corp_a │ │ DB: corp_b │ │ DB: corp_c │                  │
│  │ (독립 DB)  │ │ (독립 DB)  │ │ (독립 DB)  │                  │
│  └────────────┘ └────────────┘ └────────────┘                  │
│  장점: 완전 격리, 보안 우수 / 단점: 리소스 오버헤드, Cross 불가  │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### 3. 트랜잭션과 ACID

```
ACID 속성
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  【 Atomicity (원자성) 】                                    │
│  트랜잭션 내 모든 작업이 성공하거나 모두 실패                 │
│  BEGIN → 작업1 → 작업2 → COMMIT/ROLLBACK                    │
│                                                             │
│  【 Consistency (일관성) 】                                  │
│  트랜잭션 전후로 데이터 무결성 유지                          │
│  제약조건 (PK, FK, CHECK) 항상 충족                         │
│                                                             │
│  【 Isolation (격리성) 】                                    │
│  동시 트랜잭션 간 간섭 방지                                  │
│  격리 수준: Read Uncommitted → Read Committed               │
│            → Repeatable Read → Serializable                 │
│                                                             │
│  【 Durability (지속성) 】                                   │
│  커밋된 데이터는 영구 저장                                   │
│  WAL (Write-Ahead Logging) 사용                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4. MVCC (Multi-Version Concurrency Control)

```
MVCC 작동 원리
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  시점 T1: UPDATE users SET name='Bob' WHERE id=1;          │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Heap Page                                           │   │
│  │  ┌────────────────────────────────────────────────┐ │   │
│  │  │ Tuple V1: id=1, name='Alice'                   │ │   │
│  │  │           xmin=100, xmax=150 (삭제 마킹)       │ │   │
│  │  ├────────────────────────────────────────────────┤ │   │
│  │  │ Tuple V2: id=1, name='Bob'   ← 새 버전        │ │   │
│  │  │           xmin=150, xmax=null                  │ │   │
│  │  └────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  • xmin: 생성한 트랜잭션 ID                                 │
│  • xmax: 삭제/수정한 트랜잭션 ID                            │
│  • 읽는 시점의 스냅샷에 따라 보이는 버전 결정                │
│  • VACUUM이 오래된 버전 정리                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 5. 제약조건 (Constraints)

```sql
-- 테이블 생성 시 제약조건 정의
CREATE TABLE orders (
    -- PRIMARY KEY: 고유 식별자, NOT NULL + UNIQUE
    order_id SERIAL PRIMARY KEY,

    -- FOREIGN KEY: 참조 무결성
    customer_id INT REFERENCES customers(id)
                    ON DELETE CASCADE,

    -- NOT NULL: 필수 값
    order_date DATE NOT NULL DEFAULT CURRENT_DATE,

    -- CHECK: 비즈니스 규칙
    amount NUMERIC CHECK (amount > 0),
    status TEXT CHECK (status IN ('pending', 'completed', 'cancelled')),

    -- UNIQUE: 중복 방지
    order_number TEXT UNIQUE
);

-- 테이블 수준 제약조건
ALTER TABLE orders
ADD CONSTRAINT valid_date
CHECK (order_date <= CURRENT_DATE);
```

```
제약조건 유형 및 용도
┌─────────────┬────────────────────────────────────────────┐
│   유형      │              용도 및 특징                   │
├─────────────┼────────────────────────────────────────────┤
│ PRIMARY KEY │ 행 고유 식별, 자동으로 인덱스 생성          │
│ FOREIGN KEY │ 테이블 간 참조 무결성, CASCADE 옵션        │
│ NOT NULL    │ NULL 값 방지, 필수 필드 강제               │
│ UNIQUE      │ 중복 값 방지, NULL은 여러 개 허용          │
│ CHECK       │ 컬럼 값 범위/패턴 제한                     │
│ EXCLUDE     │ 범위 중복 방지 (예약 시스템)               │
└─────────────┴────────────────────────────────────────────┘
```

### 6. 함수와 트리거

```sql
-- 함수 생성 예시
CREATE OR REPLACE FUNCTION calculate_total(
    price NUMERIC,
    quantity INT
) RETURNS NUMERIC AS $$
BEGIN
    RETURN price * quantity;
END;
$$ LANGUAGE plpgsql;

-- 트리거 함수
CREATE OR REPLACE FUNCTION update_modified_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.modified_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 트리거 생성
CREATE TRIGGER set_modified_at
    BEFORE UPDATE ON orders
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_at();
```

```
트리거 타이밍 및 용도
┌───────────────────────────────────────────────────────────┐
│                                                           │
│  【 BEFORE 트리거 】                                       │
│  • 실제 작업 전에 실행                                    │
│  • NEW 값 수정 가능 (입력 검증, 기본값 설정)              │
│  • NULL 반환 시 작업 취소                                 │
│                                                           │
│  【 AFTER 트리거 】                                        │
│  • 실제 작업 후에 실행                                    │
│  • 감사 로그, 알림 발송, 연관 테이블 업데이트             │
│  • NEW 수정 불가                                          │
│                                                           │
│  【 INSTEAD OF 트리거 】                                   │
│  • VIEW에서만 사용                                        │
│  • INSERT/UPDATE/DELETE를 대체                           │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

### 7. 뷰 (Views)

```sql
-- 일반 뷰: 쿼리 저장 (가상 테이블)
CREATE VIEW active_orders AS
SELECT o.order_id, c.name, o.amount
FROM orders o
JOIN customers c ON o.customer_id = c.id
WHERE o.status = 'active';

-- Materialized View: 결과 물리적 저장
CREATE MATERIALIZED VIEW monthly_sales AS
SELECT
    DATE_TRUNC('month', order_date) AS month,
    SUM(amount) AS total_sales
FROM orders
GROUP BY 1;

-- Materialized View 갱신
REFRESH MATERIALIZED VIEW monthly_sales;
REFRESH MATERIALIZED VIEW CONCURRENTLY monthly_sales;  -- 읽기 차단 없이
```

```
View vs Materialized View
┌──────────────────┬─────────────────┬─────────────────────┐
│      구분        │      View       │  Materialized View  │
├──────────────────┼─────────────────┼─────────────────────┤
│ 데이터 저장      │ 저장 안 함      │ 물리적 저장         │
│ 조회 성능        │ 매번 쿼리 실행  │ 빠름 (사전 계산)    │
│ 데이터 신선도    │ 항상 최신       │ REFRESH 필요        │
│ 인덱스           │ 불가            │ 가능                │
│ 디스크 사용      │ 없음            │ 있음                │
│ 용도             │ 복잡 쿼리 캡슐화│ 분석/리포트         │
└──────────────────┴─────────────────┴─────────────────────┘
```

### 8. 역할 기반 접근 제어 (RBAC)

```sql
-- 역할 생성
CREATE ROLE app_readonly;
CREATE ROLE app_readwrite;
CREATE ROLE app_admin;

-- 권한 부여
GRANT CONNECT ON DATABASE myapp TO app_readonly;
GRANT USAGE ON SCHEMA public TO app_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_readonly;

GRANT app_readonly TO app_readwrite;  -- 상속
GRANT INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_readwrite;

-- 로그인 사용자 생성
CREATE USER api_user WITH PASSWORD 'secret';
GRANT app_readwrite TO api_user;

-- Row Level Security (RLS)
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON orders
    USING (tenant_id = current_setting('app.tenant_id')::int);
```

---

## 비교표

### 격리 수준 비교

| 격리 수준 | Dirty Read | Non-Repeatable Read | Phantom Read | 성능 |
|-----------|------------|---------------------|--------------|------|
| Read Uncommitted | 가능 | 가능 | 가능 | 높음 |
| Read Committed | 방지 | 가능 | 가능 | 높음 |
| Repeatable Read | 방지 | 방지 | 가능* | 보통 |
| Serializable | 방지 | 방지 | 방지 | 낮음 |

*PostgreSQL은 Repeatable Read에서도 Phantom Read 방지

### 멀티테넌시 전략 비교

| 전략 | 격리 수준 | 복잡도 | 리소스 효율 | Cross 쿼리 |
|------|----------|--------|------------|-----------|
| 테이블 수준 | 낮음 | 낮음 | 높음 | 용이 |
| 스키마 수준 | 중간 | 중간 | 중간 | 가능 |
| DB 수준 | 높음 | 높음 | 낮음 | 불가 |

---

## 면접 예상 질문 및 모범 답안

### Q1. PostgreSQL에서 Schema의 역할과 활용 방안을 설명해주세요.

**모범 답안:**

Schema는 데이터베이스 내에서 객체들을 논리적으로 그룹화하는 네임스페이스입니다.

**역할:**
1. **이름 충돌 방지**: 같은 이름의 테이블이 다른 스키마에 존재 가능
2. **권한 관리**: 스키마 단위로 권한 부여 가능
3. **논리적 분리**: 관련 객체들을 그룹화

**활용 방안:**
1. **멀티테넌시**: 테넌트별 스키마 분리 (tenant_a.orders, tenant_b.orders)
2. **기능별 분리**: auth 스키마, billing 스키마, reporting 스키마
3. **버전 관리**: v1 스키마와 v2 스키마로 API 버전 분리

```sql
SET search_path TO tenant_a, shared;
-- tenant_a.orders와 shared.common_codes 접근 가능
```

### Q2. MVCC가 무엇이고, PostgreSQL에서 어떻게 동작하나요?

**모범 답안:**

MVCC(Multi-Version Concurrency Control)는 동시성 제어 메커니즘으로, 읽기와 쓰기가 서로를 블로킹하지 않도록 합니다.

**동작 원리:**
1. **UPDATE 시**: 기존 행을 삭제 마킹하고 새 버전 생성
2. **버전 관리**: xmin(생성 트랜잭션), xmax(삭제 트랜잭션) 메타데이터
3. **스냅샷 격리**: 각 트랜잭션은 시작 시점의 데이터 스냅샷을 봄

**장점:**
- Reader와 Writer가 서로 블로킹하지 않음
- 높은 동시성 처리 가능

**단점:**
- 오래된 버전이 누적됨 → VACUUM 필요
- UPDATE가 INSERT처럼 동작하여 Write Amplification 발생

### Q3. CHECK 제약조건과 트리거의 차이점 및 사용 시점을 설명해주세요.

**모범 답안:**

**CHECK 제약조건:**
- 단일 행의 데이터 유효성 검증
- 선언적이고 단순함
- 다른 테이블 참조 불가
- 예: `CHECK (price > 0)`, `CHECK (status IN ('active', 'inactive'))`

**트리거:**
- 복잡한 비즈니스 로직 실행
- 다른 테이블 참조/수정 가능
- 프로시저적 코드 작성
- 예: 감사 로그 기록, 연관 테이블 업데이트, 알림 발송

**선택 기준:**
- 단순 값 범위/패턴 검증 → CHECK
- 다른 테이블 참조 필요 → 트리거
- 외부 시스템 연동 → 트리거
- 기본값 설정 → 트리거 (BEFORE INSERT)

### Q4. View와 Materialized View의 차이점과 각각의 사용 시나리오를 설명해주세요.

**모범 답안:**

**View (일반 뷰):**
- 쿼리를 저장한 가상 테이블
- 조회 시마다 쿼리 실행
- 항상 최신 데이터 반환
- 인덱스 생성 불가

**Materialized View:**
- 쿼리 결과를 물리적으로 저장
- REFRESH로 갱신 필요
- 인덱스 생성 가능
- 디스크 공간 사용

**사용 시나리오:**

| View | Materialized View |
|------|-------------------|
| 복잡한 JOIN 캡슐화 | 무거운 집계 쿼리 캐싱 |
| 권한 제어 (특정 컬럼만 노출) | 대시보드/리포트 |
| 항상 최신 데이터 필요 | 데이터 신선도 허용 범위 있음 |

### Q5. PostgreSQL에서 Row Level Security(RLS)는 어떻게 동작하나요?

**모범 답안:**

RLS는 테이블 수준이 아닌 행 수준에서 접근을 제어하는 기능입니다.

**설정 방법:**
```sql
-- RLS 활성화
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

-- 정책 생성: 자신의 주문만 조회 가능
CREATE POLICY user_orders ON orders
    FOR SELECT
    USING (user_id = current_user_id());

-- 정책 생성: 테넌트 격리
CREATE POLICY tenant_isolation ON orders
    USING (tenant_id = current_setting('app.tenant_id')::int);
```

**동작:**
- 모든 쿼리에 USING 조건이 자동으로 추가됨
- 테이블 소유자는 기본적으로 RLS 우회 (FORCE ROW LEVEL SECURITY로 적용 가능)
- 여러 정책은 OR로 결합

**활용:**
- 멀티테넌시에서 데이터 격리
- 사용자별 권한 분리
- 애플리케이션 레벨 보안 보완

### Q6. PostgreSQL 트랜잭션에서 SAVEPOINT의 용도를 설명해주세요.

**모범 답안:**

SAVEPOINT는 트랜잭션 내에서 부분 롤백을 가능하게 하는 기능입니다.

```sql
BEGIN;
INSERT INTO orders (...) VALUES (...);  -- 성공

SAVEPOINT before_payment;

UPDATE accounts SET balance = balance - 100 WHERE id = 1;
-- 오류 발생 시

ROLLBACK TO SAVEPOINT before_payment;
-- orders INSERT는 유지, UPDATE만 롤백

INSERT INTO payment_logs (...) VALUES ('failed');
COMMIT;
```

**활용 시나리오:**
1. **부분 실패 허용**: 일부 작업 실패해도 전체 트랜잭션 유지
2. **복잡한 비즈니스 로직**: 단계별로 복구 지점 설정
3. **배치 처리**: 개별 레코드 실패 시 해당 레코드만 롤백

**주의점:**
- SAVEPOINT가 많으면 오버헤드 증가
- 중첩 트랜잭션과 유사하지만 진정한 중첩은 아님

---

## 실무 체크리스트

```
□ 멀티테넌시 전략 결정 (테이블/스키마/DB 수준)
□ 적절한 제약조건으로 데이터 무결성 보장
□ VACUUM 정책 설정 (autovacuum 파라미터 튜닝)
□ 트리거는 필요한 경우에만 사용 (성능 영향 고려)
□ Materialized View는 적절한 REFRESH 주기 설정
□ RLS 사용 시 정책 테스트 철저히
□ 역할 기반 권한 관리로 최소 권한 원칙 적용
```

---

## 참고 자료

- [PostgreSQL 트랜잭션 문서](https://www.postgresql.org/docs/current/tutorial-transactions.html)
- [MVCC 공식 문서](https://www.postgresql.org/docs/current/mvcc.html)
- [Row Level Security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
- 책 GitHub: https://github.com/dmagda/just-use-postgres-book
