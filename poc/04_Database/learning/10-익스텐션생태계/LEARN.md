# Ch.10 - 익스텐션 생태계

> **이론 매핑**: `docs/04_Database/04_PostgreSQL/07_익스텐션.md`

---

## 핵심 요약

PostgreSQL의 확장(Extension) 시스템은 "Just Use Postgres"를 가능하게 하는 핵심 메커니즘이다. pgvector로 AI 벡터 검색을, PostGIS로 지리공간 쿼리를, TimescaleDB로 시계열 데이터를 처리할 수 있으며, 이 모두가 하나의 PostgreSQL 인스턴스 안에서 동작한다. 별도의 전문 데이터베이스를 도입하는 대신 확장을 활용하면 아키텍처 복잡도를 줄이고 데이터 일관성을 유지할 수 있다.

---

## 학습 목표

1. PostgreSQL Extension의 구성요소(control, sql, shared library)와 관리 명령어를 이해할 수 있다
2. pgcrypto로 비밀번호 해싱과 데이터 암호화를 구현할 수 있다
3. pgvector의 벡터 유사도 검색 원리와 인덱스 전략을 설명할 수 있다
4. PostGIS의 지리공간 쿼리 기본 개념을 이해할 수 있다
5. Foreign Data Wrapper(FDW)로 외부 데이터 소스를 연결할 수 있다
6. 확장 선택 시 클라우드 지원, 버전 호환성, 라이선스를 고려할 수 있다

---

## 본문

### 1. Extension 시스템 이해

Extension은 PostgreSQL에 새로운 데이터 타입, 함수, 연산자, 인덱스 타입을 추가하는 플러그인 시스템이다. 세 가지 구성요소로 이루어진다.

```
Extension 구성
┌─────────────────────────────────────────────┐
│  control file (.control)                     │
│  - 이름, 버전, 의존성 정보                   │
├─────────────────────────────────────────────┤
│  script file (.sql)                          │
│  - 타입, 함수, 연산자 정의                   │
├─────────────────────────────────────────────┤
│  shared library (.so/.dll) - 선택            │
│  - C로 구현된 고성능 함수                    │
└─────────────────────────────────────────────┘
```

확장 관리는 SQL 명령어로 수행한다.

```sql
-- 사용 가능한 확장 목록
SELECT name, default_version, comment
FROM pg_available_extensions ORDER BY name;

-- 설치된 확장 확인
SELECT * FROM pg_extension;

-- 확장 설치
CREATE EXTENSION pgcrypto;

-- 특정 스키마에 설치
CREATE EXTENSION postgis WITH SCHEMA geo;

-- 확장 업그레이드
ALTER EXTENSION pgcrypto UPDATE TO '1.4';

-- 확장 제거 (의존 객체와 함께)
DROP EXTENSION pgcrypto CASCADE;
```

### 2. pgcrypto: 암호화와 해싱

pgcrypto는 데이터베이스 레벨에서 암호화 기능을 제공하는 확장이다. 비밀번호 해싱, 데이터 암호화, UUID 생성에 사용한다.

```sql
CREATE EXTENSION pgcrypto;

-- 비밀번호 해싱 (bcrypt 사용)
-- 저장
INSERT INTO users (email, password_hash)
VALUES ('user@example.com', crypt('my_password', gen_salt('bf', 10)));

-- 검증
SELECT * FROM users
WHERE email = 'user@example.com'
  AND password_hash = crypt('input_password', password_hash);
```

`crypt()` + `gen_salt('bf')`는 bcrypt 알고리즘을 사용한다. bcrypt는 의도적으로 느린 해시 함수로, brute-force 공격을 어렵게 만든다. 두 번째 인자(10)는 cost factor로, 높을수록 계산이 오래 걸린다.

```sql
-- 대칭키 암호화 (AES) - 민감 데이터 보호
-- 암호화
UPDATE customers SET
    ssn_encrypted = pgp_sym_encrypt(ssn_plain, 'encryption_key');

-- 복호화
SELECT pgp_sym_decrypt(ssn_encrypted, 'encryption_key') AS ssn
FROM customers;

-- UUID v4 생성
SELECT gen_random_uuid();
-- 결과: 550e8400-e29b-41d4-a716-446655440000
```

암호화 키는 데이터베이스에 저장하면 안 된다. 환경변수나 외부 키 관리 서비스(AWS KMS, HashiCorp Vault)를 통해 관리해야 한다.

### 3. pgvector: 벡터 유사도 검색

pgvector는 벡터 임베딩을 저장하고 유사도 검색을 수행하는 확장이다. AI/ML 애플리케이션에서 RAG(Retrieval-Augmented Generation), 추천 시스템, 이미지 검색에 활용된다.

```sql
CREATE EXTENSION vector;

-- 벡터 컬럼 생성 (3차원 예시)
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding vector(3)  -- 실제로는 1536차원(OpenAI) 등
);

-- 데이터 삽입
INSERT INTO items (content, embedding)
VALUES
    ('PostgreSQL tutorial', '[0.1, 0.2, 0.3]'),
    ('Machine learning basics', '[0.8, 0.1, 0.5]');

-- 유사도 검색 (코사인 거리)
SELECT content, embedding <=> '[0.1, 0.2, 0.35]' AS distance
FROM items
ORDER BY embedding <=> '[0.1, 0.2, 0.35]'
LIMIT 5;
```

pgvector가 지원하는 거리 연산자:

| 연산자 | 거리 타입 | 용도 |
|--------|----------|------|
| `<->` | L2 (유클리드) | 일반적인 거리 |
| `<=>` | 코사인 | 텍스트 임베딩 (방향 유사도) |
| `<#>` | 내적 (음수) | 정규화된 벡터 |

인덱스는 IVFFlat과 HNSW 두 가지를 선택할 수 있다. HNSW가 검색 정확도가 높고 빌드 후 업데이트에 강하지만, 메모리를 더 사용한다.

```sql
-- HNSW 인덱스 (권장)
CREATE INDEX ON items USING hnsw (embedding vector_cosine_ops);

-- IVFFlat 인덱스 (대용량에서 빌드 빠름)
CREATE INDEX ON items USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);
```

### 4. PostGIS: 지리공간 데이터

PostGIS는 PostgreSQL에 지리공간 데이터 타입과 함수를 추가한다. 위치 기반 서비스, 배달 앱, 부동산 검색 등에 활용된다.

```sql
CREATE EXTENSION postgis;

-- 공간 데이터 저장
CREATE TABLE stores (
    id SERIAL PRIMARY KEY,
    name TEXT,
    location geography(POINT, 4326)  -- WGS84 좌표
);

INSERT INTO stores (name, location)
VALUES ('Store A', ST_MakePoint(127.0276, 37.4979));  -- 강남역

-- 반경 검색: 현재 위치에서 1km 이내 매장
SELECT name,
       ST_Distance(location, ST_MakePoint(127.03, 37.50)::geography) AS distance_m
FROM stores
WHERE ST_DWithin(location, ST_MakePoint(127.03, 37.50)::geography, 1000)
ORDER BY distance_m;
```

PostGIS는 GiST 인덱스를 활용하여 공간 검색을 최적화한다. `ST_DWithin`은 인덱스를 활용하지만 `ST_Distance < 1000` 형태의 조건은 인덱스를 활용하지 못하므로, 항상 `ST_DWithin`을 사용해야 한다.

### 5. pg_stat_statements와 pg_cron

**pg_stat_statements**는 쿼리별 실행 통계를 수집하는 확장이다. 느린 쿼리 식별에 필수적이다.

```sql
-- postgresql.conf에서 활성화
-- shared_preload_libraries = 'pg_stat_statements'

CREATE EXTENSION pg_stat_statements;

-- 총 실행 시간 기준 상위 쿼리
SELECT query, calls,
       round(total_exec_time::numeric, 2) AS total_ms,
       round(mean_exec_time::numeric, 2) AS avg_ms
FROM pg_stat_statements
ORDER BY total_exec_time DESC LIMIT 10;
```

**pg_cron**은 데이터베이스 내에서 크론 작업을 스케줄링하는 확장이다.

```sql
CREATE EXTENSION pg_cron;

-- 매일 새벽 2시에 오래된 세션 정리
SELECT cron.schedule('cleanup-sessions',
    '0 2 * * *',
    $$DELETE FROM sessions WHERE expires_at < NOW()$$
);

-- 매 시간 Materialized View 갱신
SELECT cron.schedule('refresh-dashboard',
    '0 * * * *',
    $$REFRESH MATERIALIZED VIEW CONCURRENTLY dashboard_stats$$
);
```

### 6. Foreign Data Wrapper (FDW)

FDW는 외부 데이터 소스를 PostgreSQL 테이블처럼 쿼리할 수 있게 하는 기능이다. 데이터 통합, 마이그레이션, 분석에 활용된다.

```
FDW 아키텍처
┌───────────────────────┐      ┌─────────────────────┐
│  Local PostgreSQL     │      │  Remote PostgreSQL   │
│                       │      │                      │
│  Foreign Table -------│----->│  users 테이블        │
│  (remote_users)       │  네트워크  │                │
│                       │      │                      │
│  FDW Extension        │      │                      │
│  (postgres_fdw)       │      │                      │
└───────────────────────┘      └─────────────────────┘
```

```sql
-- 설정 단계
CREATE EXTENSION postgres_fdw;

CREATE SERVER remote_server
    FOREIGN DATA WRAPPER postgres_fdw
    OPTIONS (host 'db.example.com', port '5432', dbname 'remote_db');

CREATE USER MAPPING FOR local_user
    SERVER remote_server
    OPTIONS (user 'remote_user', password 'password');

-- 외부 테이블 정의 (또는 스키마 전체 가져오기)
IMPORT FOREIGN SCHEMA public
FROM SERVER remote_server INTO local_schema;

-- 로컬 테이블처럼 쿼리
SELECT * FROM local_schema.users WHERE id = 1;
```

FDW 사용 시 네트워크 지연을 고려해야 한다. WHERE 절이 원격 서버로 푸시다운되는지 EXPLAIN으로 확인하는 것이 중요하다.

### 7. 확장 선택 시 고려사항

확장을 도입하기 전에 다섯 가지를 점검해야 한다.

| 항목 | 확인 내용 |
|------|----------|
| 클라우드 지원 | RDS/Cloud SQL에서 해당 확장을 지원하는가? |
| 버전 호환성 | PostgreSQL 버전에 맞는 확장 버전이 있는가? |
| 라이선스 | AGPL, 상용 라이선스 등 제약이 없는가? |
| 성능 영향 | Hook 기반 확장은 모든 쿼리에 오버헤드를 추가하는가? |
| 커뮤니티 | 활발히 유지보수되고 있는가? 마지막 업데이트는 언제인가? |

클라우드 환경에서 확장 제한은 실무에서 자주 만나는 문제다. AWS RDS는 pgvector, PostGIS, pg_stat_statements 등 주요 확장을 지원하지만, 커스텀 C 확장이나 shared_preload_libraries가 필요한 일부 확장은 사용할 수 없다.

### 8. PostgreSQL 호환 솔루션 비교

PostgreSQL 생태계에는 원본 외에도 여러 호환 솔루션이 있다.

| 솔루션 | 유형 | 분산 | 확장 호환성 | 선택 시점 |
|--------|------|------|-----------|----------|
| Vanilla PostgreSQL | 원본 | 불가 | 100% | 단일 노드로 충분할 때 |
| Aurora PostgreSQL | Fork | 가능 | 높음 | AWS에서 관리형 필요 시 |
| Citus | 확장 | 가능 | 높음 | 수평 샤딩 필요 시 |
| YugabyteDB | 호환 | 가능 | 제한적 | 글로벌 분산 필요 시 |
| Neon | 호환 | - | 높음 | Serverless 필요 시 |

선택 흐름: 단일 노드 충분하면 표준 PostgreSQL, 읽기 확장이 필요하면 Aurora/읽기 레플리카, 쓰기 확장이 필요하면 Citus 또는 분산 SQL을 고려한다.

---

## 핵심 정리

| 개념 | 한 줄 요약 |
|------|-----------|
| Extension 시스템 | control + sql + shared library로 구성, CREATE EXTENSION으로 설치 |
| pgcrypto | bcrypt 해싱, AES 암호화, UUID 생성 제공 |
| pgvector | 벡터 임베딩 저장/유사도 검색, HNSW 인덱스 권장 |
| PostGIS | 지리공간 타입+함수, ST_DWithin으로 반경 검색, GiST 인덱스 |
| pg_stat_statements | 쿼리별 실행 통계 수집, 느린 쿼리 식별 필수 도구 |
| FDW | 외부 데이터 소스를 로컬 테이블처럼 쿼리, 네트워크 지연 주의 |
| 확장 선택 | 클라우드 지원, 버전 호환성, 라이선스, 성능, 커뮤니티 점검 |
