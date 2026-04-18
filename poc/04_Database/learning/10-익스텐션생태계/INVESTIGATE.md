# Ch.10 - 익스텐션 생태계: 심화 탐구

> LEARN.md를 학습한 뒤, 더 깊이 파고들어야 할 질문들

---

## Q1. pgvector vs 전용 벡터 DB(Pinecone, Milvus): 어디서 경계가 갈리는가?

### 왜 이 질문이 중요한가

AI/ML 애플리케이션이 늘어나면서 벡터 검색은 필수 기능이 되었다. pgvector로 PostgreSQL 안에서 처리할지, Pinecone 같은 전용 벡터 DB를 도입할지는 아키텍처 결정의 핵심이다. 이 판단을 뒷받침할 수 있는 벤치마크 데이터와 트레이드오프를 이해해야 한다.

### 답변

**pgvector의 현재 위치**:

pgvector는 2024-2025년에 걸쳐 빠르게 성숙해졌다. HNSW 인덱스 도입으로 검색 정확도와 속도가 크게 개선되었다.

**규모별 성능 비교** (대략적 기준):

| 벡터 수 | pgvector (HNSW) | 전용 벡터 DB | 권장 |
|---------|----------------|-------------|------|
| ~100만 | 빠름 (ms 단위) | 빠름 | pgvector |
| 100만~1000만 | 보통 (10-100ms) | 빠름 | 상황에 따라 |
| 1000만 이상 | 느려질 수 있음 | 최적화됨 | 전용 DB 검토 |
| 수억 이상 | 부적합 | 샤딩/분산 지원 | 전용 DB |

**pgvector 선택이 유리한 경우**:

```
1. 벡터 데이터와 메타데이터가 같은 트랜잭션에 있어야 함
   예: "주문 생성 + 벡터 임베딩 저장"이 원자적이어야 함

2. 벡터 검색 + 관계형 필터링이 결합됨
   예: "나와 유사한 취향의 사용자 중 같은 지역에 사는 사람"
   SELECT * FROM users
   WHERE region = 'seoul'
   ORDER BY embedding <=> query_vector
   LIMIT 10;

3. 인프라 단순화가 목표
   예: PostgreSQL 하나로 CRUD + 벡터 검색 + 전문 검색
```

**전용 벡터 DB 선택이 유리한 경우**:

```
1. 벡터 수가 1000만 이상
2. 밀리초 단위 지연 시간이 중요 (실시간 추천)
3. 자주 변경되는 대량 벡터 (실시간 학습)
4. 분산 환경에서 수평 확장 필요
```

**인덱스 전략 비교**:

```sql
-- HNSW: 정확도 높음, 메모리 사용 많음, 빌드 후 업데이트 지원
CREATE INDEX ON items USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);
-- m: 노드당 연결 수 (높을수록 정확, 느림)
-- ef_construction: 빌드 시 탐색 범위 (높을수록 정확, 빌드 느림)

-- IVFFlat: 메모리 효율적, 빌드 빠름, 데이터 분포 의존
CREATE INDEX ON items USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);
-- lists: 클러스터 수 (sqrt(행 수) ~ 행 수/1000 권장)
-- 주의: 빌드 후 데이터 분포가 크게 바뀌면 재빌드 필요
```

### 실무 적용

- RAG 앱, 작은 규모 추천: pgvector로 시작 (아키텍처 단순화)
- 1000만 벡터 이상 또는 밀리초 지연 필수: 전용 벡터 DB 검토
- pgvector 사용 시 HNSW가 기본 선택, IVFFlat은 대량 빌드 시 검토

---

## Q2. PostGIS의 성능은 대규모 환경에서 어느 수준인가?

### 왜 이 질문이 중요한가

배달 앱, 부동산 서비스, 물류 시스템 등에서 지리공간 쿼리는 핵심이다. PostGIS가 "수백만 POI에서 반경 검색"을 얼마나 빠르게 처리할 수 있는지, 성능 한계는 어디인지를 이해해야 인프라 설계에 반영할 수 있다.

### 답변

**PostGIS의 강점**: PostGIS는 GiST 인덱스 기반의 R-tree 구조를 사용한다. 공간 데이터의 bounding box를 계층적으로 관리하여 범위 검색을 효율적으로 수행한다.

**성능 벤치마크** (일반적 수준):

```sql
-- 100만 POI에서 반경 1km 검색
-- GiST 인덱스 사용 시: 1-5ms
-- 인덱스 없을 시: 500ms+

-- 1000만 POI에서 반경 검색
-- GiST 인덱스 사용 시: 5-20ms
```

**성능 최적화 포인트**:

```sql
-- 1. 올바른 타입 선택
-- geography: 구면 좌표 (정확하지만 느림)
-- geometry: 평면 좌표 (빠르지만 장거리에서 부정확)

-- 근거리 검색(도시 내): geometry + SRID 변환이 더 빠름
-- 장거리 검색(국가 간): geography 사용

-- 2. ST_DWithin이 필수 (인덱스 활용)
-- 좋음: 인덱스 사용
WHERE ST_DWithin(location, query_point, 1000)

-- 나쁨: 인덱스 사용 안 됨
WHERE ST_Distance(location, query_point) < 1000

-- 3. 클러스터링으로 I/O 최적화
CLUSTER stores USING idx_stores_location;
-- 물리적으로 인접한 데이터를 같은 페이지에 배치
```

**스케일링 전략**:

- 파티셔닝: 지역별로 테이블 파티셔닝 (`PARTITION BY LIST(region)`)
- 읽기 레플리카: 검색 쿼리를 레플리카로 분산
- 캐싱: 자주 검색되는 영역의 결과를 Materialized View로 사전 계산

### 실무 적용

- 100만 POI 이하: PostGIS 단일 인스턴스로 충분
- 100만-1000만: 파티셔닝 + 읽기 레플리카
- 1000만 이상: Citus(분산) 또는 전용 GIS 시스템 검토
- 항상 `ST_DWithin` 사용, `ST_Distance` 조건은 피함

---

## Q3. Extension의 보안 고려사항은 무엇인가?

### 왜 이 질문이 중요한가

Extension은 PostgreSQL 프로세스 내부에서 실행되므로, 악의적이거나 버그가 있는 확장은 데이터 손상이나 보안 침해로 이어질 수 있다. 프로덕션 환경에서 확장 도입 전 보안 검토가 필수적이다.

### 답변

**보안 위험 수준별 분류**:

```
Level 1: SQL-only Extension (저위험)
- SQL과 PL/pgSQL로만 구현
- PostgreSQL의 권한 모델 안에서 동작
- 예: 커스텀 함수, 뷰 기반 확장

Level 2: C Extension with trusted functions (중위험)
- C로 구현되었지만 PostgreSQL API 준수
- 공식 확장(pgcrypto, pg_trgm 등)이 여기에 해당
- 코드 리뷰와 커뮤니티 검증을 거침

Level 3: C Extension with untrusted functions (고위험)
- OS 레벨 접근 가능
- 파일 시스템, 네트워크 접근 가능
- 검증되지 않은 서드파티 확장
```

**보안 체크리스트**:

```
확장 도입 전 점검:
[ ] 소스 코드가 공개되어 있는가?
[ ] 활발한 커뮤니티/유지보수가 있는가?
[ ] CVE(보안 취약점) 기록을 확인했는가?
[ ] superuser 권한이 필요한가? (필요하면 왜?)
[ ] shared_preload_libraries에 추가되는가? (PostgreSQL 재시작 필요)
[ ] 테스트 환경에서 충분히 검증했는가?
```

**superuser 권한 문제**: 많은 확장이 `CREATE EXTENSION`에 superuser 권한을 요구한다. 클라우드 환경(RDS, Cloud SQL)에서는 superuser가 제한되므로, 클라우드 제공자가 사전 승인한 확장만 사용할 수 있다.

**신뢰할 수 있는 확장 목록** (프로덕션 검증):

| 확장 | 위험도 | 비고 |
|------|-------|------|
| pgcrypto | 낮음 | PostgreSQL contrib에 포함 |
| pg_stat_statements | 낮음 | 공식 모듈 |
| PostGIS | 낮음 | 20년+ 역사 |
| pgvector | 낮음 | 활발한 커뮤니티 |
| pg_cron | 중간 | 신뢰할 수 있지만 스케줄링 권한 주의 |
| 커스텀 C 확장 | 높음 | 반드시 코드 리뷰 |

### 실무 적용

- 공식 contrib 확장은 별도 보안 검토 없이 사용 가능
- 서드파티 확장은 GitHub 스타 수/이슈/마지막 커밋 확인
- 프로덕션 배포 전 스테이징에서 부하 테스트 + 보안 검토
- shared_preload_libraries 추가는 PostgreSQL 재시작이 필요하므로 배포 계획에 반영

---

## Q4. TimescaleDB는 어떤 문제를 풀며, 일반 PostgreSQL 파티셔닝과 어떻게 다른가?

### 왜 이 질문이 중요한가

시계열 데이터(IoT 센서, 로그, 메트릭)는 시간이 지남에 따라 급격히 증가한다. PostgreSQL의 기본 파티셔닝으로도 처리할 수 있지만, TimescaleDB가 제공하는 자동화와 최적화가 있다. 두 접근의 차이를 이해해야 올바른 선택을 할 수 있다.

### 답변

**PostgreSQL 기본 파티셔닝**:

```sql
-- 수동 파티셔닝 (월별)
CREATE TABLE metrics (
    time TIMESTAMPTZ NOT NULL,
    sensor_id INT,
    value DOUBLE PRECISION
) PARTITION BY RANGE (time);

-- 파티션 수동 생성 (매월 반복 필요)
CREATE TABLE metrics_2025_01 PARTITION OF metrics
    FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');
CREATE TABLE metrics_2025_02 PARTITION OF metrics
    FOR VALUES FROM ('2025-02-01') TO ('2025-03-01');
-- ... 매월 수동 또는 pg_cron으로 자동화
```

**TimescaleDB**:

```sql
CREATE EXTENSION timescaledb;

-- 일반 테이블 생성 후 hypertable로 변환
CREATE TABLE metrics (
    time TIMESTAMPTZ NOT NULL,
    sensor_id INT,
    value DOUBLE PRECISION
);

SELECT create_hypertable('metrics', 'time');
-- 자동으로 시간 기반 청크(파티션) 생성/관리
```

**핵심 차이**:

| 기능 | PostgreSQL 파티셔닝 | TimescaleDB |
|------|-------------------|-------------|
| 파티션 생성 | 수동/스크립트 | 자동 |
| 파티션 전략 | 선언적 (RANGE, LIST, HASH) | 시간 기반 자동 최적화 |
| 데이터 보존 | 수동 DROP PARTITION | `add_retention_policy` |
| 연속 집계 | Materialized View 수동 | Continuous Aggregates |
| 압축 | 없음 | 자동 컬럼 압축 (90%+ 절감) |
| 쿼리 최적화 | 기본 파티션 프루닝 | 시계열 전용 최적화 |

**TimescaleDB의 킬러 피처: Continuous Aggregates**

```sql
-- 시간별 평균값을 자동으로 사전 계산하고 갱신
CREATE MATERIALIZED VIEW hourly_metrics
WITH (timescaledb.continuous) AS
SELECT time_bucket('1 hour', time) AS bucket,
       sensor_id,
       AVG(value), MAX(value), MIN(value)
FROM metrics
GROUP BY 1, 2;

-- 자동 갱신 정책
SELECT add_continuous_aggregate_policy('hourly_metrics',
    start_offset => INTERVAL '3 hours',
    end_offset => INTERVAL '1 hour',
    schedule_interval => INTERVAL '1 hour');
```

### 실무 적용

- 시계열 데이터가 핵심이면 TimescaleDB가 운영 부담을 크게 줄임
- 파티션 관리, 데이터 보존, 압축을 자동화
- 라이선스 주의: TimescaleDB는 Timescale License (일부 기능 제한)
- 클라우드에서 사용 제한이 있을 수 있으므로 사전 확인 필요
