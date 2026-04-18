# Ch.02 - 저장소와 검색: 심화 탐구

> LEARN.md를 학습한 뒤, 더 깊이 파고들어야 할 질문들

---

## Q1. LSM-Tree vs B-Tree, 실제 벤치마크에서는 어떤 차이가 나는가?

### 왜 이 질문이 중요한가
이론적인 트레이드오프는 명확하지만, 실제 워크로드에서의 성능 차이를 수치로 이해해야 DB 선택을 근거 있게 할 수 있다. 면접에서도 "왜 RocksDB를 선택했는가?" 같은 질문에 정량적으로 답할 수 있어야 한다.

### 답변

Mark Callaghan(Facebook)의 "Read, Write & Space Amplification" 분석에 따르면, 세 가지 증폭(amplification) 지표 중 최대 두 가지만 최적화할 수 있다.

```
              Read Amp
              /    \
             /      \
            /  Pick  \
           /   Two    \
          /____________\
    Write Amp      Space Amp
```

**쓰기 중심 워크로드 (예: 로그 수집, IoT)**
- LSM-Tree(RocksDB): 쓰기 처리량이 B-Tree 대비 3~10배 높다
- 이유: Sequential Write는 Random Write보다 SSD에서 3배, HDD에서 100배 이상 빠르다
- 단점: Compaction이 백그라운드 I/O를 소비하여 읽기 지연의 p99가 불안정해질 수 있다

**읽기 중심 워크로드 (예: OLTP, 웹 서비스)**
- B-Tree(PostgreSQL): 읽기 지연이 안정적이고 예측 가능하다
- 이유: 인덱스 탐색이 O(log n)이고 추가 SSTable 검색이 불필요하다
- 단점: 페이지 분할과 WAL로 인한 Write Amplification이 높다

**혼합 워크로드 (예: 실시간 분석)**
- 정답이 하나가 아니다. RocksDB의 Leveled Compaction으로 읽기를 개선하거나, B-Tree에서 부분 페이지 업데이트를 활성화하는 등 튜닝이 필요하다

### 실무 적용
대부분의 웹 서비스 백엔드(읽기 70~90%)에서는 B-Tree 기반 DB(PostgreSQL, MySQL)가 무난하다. 로그/이벤트 저장, 시계열 데이터, 메시지 큐처럼 쓰기 비중이 높은 시스템에서는 LSM-Tree 기반(RocksDB, Cassandra)을 검토해야 한다. 선택 전에 실제 워크로드 패턴으로 벤치마크를 돌려보는 것이 가장 정확하다.

---

## Q2. Write Amplification은 실무에서 얼마나 심각한 문제인가?

### 왜 이 질문이 중요한가
클라우드 환경에서 I/O 비용은 직접적인 금전 비용이고, SSD 환경에서 Write Amplification은 디스크 수명과 직결된다. 비용 최적화와 하드웨어 계획에 필수적인 지식이다.

### 답변

**B-Tree의 Write Amplification**
- 1바이트를 변경해도 4KB~16KB 페이지 전체를 재작성한다
- WAL에도 같은 내용을 한 번 더 쓴다
- 결과: Write Amplification이 수십 배에 달할 수 있다

**LSM-Tree의 Write Amplification**
- Size-Tiered Compaction: 데이터가 각 레벨을 거치며 10~30배 재작성될 수 있다
- Leveled Compaction: 더 빈번한 병합으로 Write Amplification이 10~50배에 달한다

**SSD 수명에 미치는 영향**
- 일반 엔터프라이즈 SSD의 쓰기 수명(TBW)은 수백 TB ~ 수 PB 수준이다
- Write Amplification이 30배라면, 논리적으로 1TB를 쓸 때 실제 30TB가 쓰인다
- 고쓰기 워크로드에서는 SSD 수명이 예상보다 10배 이상 빠르게 소진될 수 있다

**최적화 방법**
- LSM-Tree: WiscKey 방식으로 Key와 Value를 분리 저장하면 Compaction 시 Value 이동이 줄어든다
- B-Tree: Copy-on-Write(LMDB 방식)로 in-place update 대신 새 페이지에 쓰면 WAL이 불필요해진다
- 공통: 압축을 활성화하면 디스크 쓰기량 자체가 줄어든다

### 실무 적용
Write Amplification을 모니터링하는 습관이 중요하다. RocksDB는 `rocksdb.stats`에서 각 레벨의 쓰기량을 확인할 수 있고, PostgreSQL은 `pg_stat_bgwriter`의 buffers_checkpoint 지표로 간접 측정할 수 있다. 클라우드에서는 프로비전된 IOPS 대비 실제 사용량을 비교하여 오버프로비저닝 여부를 판단한다.

---

## Q3. Bloom Filter의 파라미터는 어떻게 설정하는가?

### 왜 이 질문이 중요한가
Bloom Filter는 LSM-Tree뿐 아니라 캐시, CDN, 네트워크 패킷 필터링 등 다양한 시스템에서 사용된다. False Positive Rate를 제어하는 파라미터 설정 원리를 이해하면 여러 도메인에 응용할 수 있다.

### 답변

Bloom Filter의 성능을 결정하는 파라미터는 세 가지다:
- **n**: 저장할 키의 수
- **m**: 비트 배열의 크기
- **k**: 해시 함수의 수

False Positive Rate(FPR) 공식:

```
FPR ≈ (1 - e^(-kn/m))^k
```

실용적인 경험 법칙:
- 키당 비트 수(m/n) = 10 → FPR ≈ 1%
- 키당 비트 수(m/n) = 15 → FPR ≈ 0.1%
- 최적 해시 함수 수: k = (m/n) * ln(2) ≈ 0.693 * (m/n)

**메모리 사용량 계산 예시:**
- 키 1000만 개, FPR 1% 목표
- 필요 비트: 10 * 10,000,000 = 100,000,000 bits = 약 12MB
- 이 정도면 서버 메모리에 충분히 올릴 수 있다

**RocksDB에서의 Bloom Filter:**
- SSTable마다 Bloom Filter를 생성하여 메타데이터에 저장한다
- 기본값: 키당 10비트 (FPR 약 1%)
- `bloom_bits_per_key` 파라미터로 조절 가능

### 실무 적용
RocksDB에서 Bloom Filter를 키당 10비트로 설정하면, 존재하지 않는 키 조회의 99%를 SSTable 접근 없이 걸러낸다. 읽기 지연에 민감한 서비스라면 15비트로 올려 0.1%까지 낮출 수 있지만, 메모리 사용량이 50% 증가하므로 트레이드오프를 고려해야 한다.

---

## Q4. Column-Oriented Storage는 왜 쓰기에 불리한가?

### 왜 이 질문이 중요한가
OLAP 시스템을 설계할 때 "왜 Column Store를 OLTP에 쓰지 않는가?"라는 질문이 자주 나온다. 읽기 최적화의 대가로 쓰기에서 무엇을 포기하는지를 구체적으로 이해해야 한다.

### 답변

**Row-Oriented 쓰기**: 한 행(row)을 추가할 때 모든 컬럼을 하나의 연속된 블록에 쓴다. 디스크 I/O 1회로 충분하다.

**Column-Oriented 쓰기**: 한 행을 추가할 때 각 컬럼 파일에 해당 컬럼 값을 분산하여 써야 한다. 컬럼이 100개면 100개의 파일에 각각 쓰기가 필요하다.

```
Row Store: 1행 삽입 = 1번 쓰기 (연속 블록)
Column Store: 1행 삽입 = N번 쓰기 (N개 컬럼 파일)
```

추가 비용:
- 압축된 데이터에 새 값을 삽입하려면 해당 블록의 압축을 풀고, 값을 추가하고, 다시 압축해야 한다
- 정렬 순서를 유지하려면 삽입 위치를 찾아야 하므로 append만으로는 불충분하다

**해결 방법**: Column Store도 LSM-Tree의 아이디어를 차용한다. 쓰기를 인메모리 버퍼에 모아두고, 배치로 컬럼 파일에 병합한다. Vertica, ClickHouse 등이 이 방식을 사용한다.

### 실무 적용
Column-Oriented Storage는 "대량 배치 적재(bulk load) + 분석 쿼리" 패턴에 최적화되어 있다. 실시간 단건 삽입이 많은 OLTP에는 적합하지 않다. HTAP(Hybrid Transactional/Analytical Processing)가 필요하면 TiDB나 SingleStore처럼 Row Store와 Column Store를 동시에 제공하는 DB를 검토해야 한다.

---

## Q5. 인덱스를 언제 추가하고, 언제 제거해야 하는가?

### 왜 이 질문이 중요한가
인덱스를 무분별하게 추가하면 쓰기 성능이 저하되고 디스크 공간을 낭비한다. 반대로 인덱스가 없으면 Full Table Scan으로 읽기가 느려진다. 실무에서 인덱스 관리는 지속적인 성능 튜닝의 핵심이다.

### 답변

**인덱스를 추가해야 하는 신호:**
- EXPLAIN ANALYZE에서 Seq Scan이 보이고, 해당 쿼리가 빈번하게 실행된다
- WHERE, JOIN, ORDER BY에 사용되는 컬럼에 인덱스가 없다
- 카디널리티(고유값 비율)가 높은 컬럼이다 (성별처럼 2가지 값만 있는 컬럼에 B-Tree 인덱스는 효과가 적다)

**인덱스를 제거해야 하는 신호:**
- `pg_stat_user_indexes`에서 `idx_scan = 0`인 인덱스가 오랫동안 존재한다
- 테이블 크기 대비 인덱스 크기가 비정상적으로 크다
- 쓰기 성능이 병목이고, 인덱스 업데이트가 원인으로 확인된다

**복합 인덱스 설계 원칙:**
```sql
-- 효과적: 선두 컬럼(customer_id)이 WHERE에 자주 사용됨
CREATE INDEX idx_orders ON orders (customer_id, order_date);

-- 비효과적: order_date 단독 검색에는 이 인덱스를 활용할 수 없음
SELECT * FROM orders WHERE order_date > '2024-01-01';
```

복합 인덱스의 컬럼 순서는 (1) 등가 조건(=) 컬럼 먼저 (2) 범위 조건(>, BETWEEN) 컬럼을 뒤에 배치하는 것이 일반적으로 효율적이다.

### 실무 적용
PostgreSQL에서는 `pg_stat_user_indexes`와 `pg_stat_user_tables`를 정기적으로 확인하여 사용되지 않는 인덱스를 정리해야 한다. 인덱스 추가 시에는 `CREATE INDEX CONCURRENTLY`를 사용하여 테이블 잠금 없이 생성하는 것이 운영 환경에서 안전하다.
