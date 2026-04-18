# Ch.02 - 저장소와 검색

> **이론 매핑**: `docs/04_Database/01_기본개념/02_저장소와_검색.md`, `docs/04_Database/01_기본개념/05_인덱스_이론.md`

---

## 핵심 요약
> 데이터베이스의 본질적인 역할은 "데이터를 저장하고 다시 찾아오는 것"이다. 이 단순한 요구사항을 효율적으로 충족하기 위해 LSM-Tree, B-Tree, Hash Index 등 서로 다른 설계 철학의 자료구조가 발전해왔다. 각 자료구조의 내부 동작을 이해하면, 워크로드 특성에 맞는 스토리지 엔진을 선택하고 튜닝할 수 있는 판단력을 갖추게 된다.

---

## 학습 목표
1. Log-Structured Storage와 LSM-Tree의 쓰기/읽기 경로를 설명할 수 있다
2. B-Tree의 페이지 기반 구조와 분할 과정을 이해할 수 있다
3. LSM-Tree와 B-Tree의 성능 트레이드오프를 워크로드별로 비교할 수 있다
4. Bloom Filter의 동작 원리와 False Positive/Negative 개념을 설명할 수 있다
5. WAL(Write-Ahead Log)의 역할과 크래시 복구 원리를 이해할 수 있다
6. Column-Oriented Storage가 분석 쿼리에 유리한 이유를 설명할 수 있다

---

## 본문

### 1. 세상에서 가장 간단한 데이터베이스

인덱스 없이 데이터를 저장하는 가장 원시적인 방법을 생각해보자.

```bash
db_set () { echo "$1,$2" >> database; }     # 파일 끝에 추가
db_get () { grep "^$1," database | tail -n 1; }  # 마지막 값 조회
```

쓰기는 O(1)로 빠르다. 파일 끝에 한 줄을 추가하기만 하면 되기 때문이다. 하지만 읽기는 O(n)이다. 원하는 키를 찾으려면 파일 전체를 스캔해야 한다. 데이터가 100만 건이면 100만 줄을 전부 읽어야 하므로, 읽기 성능을 개선하기 위해 "인덱스"라는 추가 자료구조가 필요하다.

인덱스의 핵심 트레이드오프는 명확하다: 읽기가 빨라지는 대신, 쓰기가 느려진다(인덱스도 업데이트해야 하므로). 그래서 데이터베이스는 모든 컬럼에 인덱스를 만들지 않고, 애플리케이션의 쿼리 패턴에 맞춰 선택적으로 생성한다.

---

### 2. Hash Index

가장 단순한 인덱스는 인메모리 해시 맵이다. 키와 해당 데이터의 디스크 오프셋을 매핑한다.

```
In-Memory Hash Map              Log File (Append-only)
┌───────┬────────┐              ┌──────────────────────────┐
│  Key  │ Offset │              │ [42, {"name":"SF"}]      │
│  42   │   0    │ ───────────→ │ [12, {"name":"London"}]  │
│  12   │  24    │              │ [42, {"name":"SF v2"}]   │
└───────┴────────┘              └──────────────────────────┘
```

쓰기 시 파일 끝에 append하고 해시 맵을 갱신한다. 읽기 시 해시 맵에서 오프셋을 찾아 디스크에서 직접 seek한다. Bitcask(Riak의 스토리지 엔진)가 이 방식을 사용한다.

한계점이 분명하다: (1) 해시 맵이 메모리에 맞아야 하므로 키 수에 제한이 있고, (2) 범위 쿼리(WHERE age BETWEEN 20 AND 30)를 지원할 수 없다(키가 정렬되어 있지 않으므로). 이 한계를 극복하기 위해 SSTable과 LSM-Tree가 등장했다.

---

### 3. SSTable과 LSM-Tree

#### 3.1 SSTable (Sorted String Table)

SSTable은 키를 정렬된 순서로 저장한 파일이다. 정렬 덕분에 모든 키를 해시 맵에 올리지 않아도 된다. 블록의 첫 번째 키만 인덱스(Sparse Index)에 저장하면 이진 탐색으로 원하는 블록을 찾고, 블록 내에서 순차 스캔하면 된다.

```
Sparse Index (메모리)        Data Blocks (디스크)
┌──────────┬────────┐       ┌────────────────────┐
│ handbag  │ offset │ ────→ │ handbag: {...}     │
│ handsome │ offset │       │ handcraft: {...}   │
└──────────┴────────┘       │ handiwork: {...}   │
                            └────────────────────┘
```

"handiwork" 검색: handbag < handiwork < handsome → handbag 블록으로 이동 → 블록 내 순차 스캔. 범위 쿼리도 효율적으로 처리할 수 있게 되었다.

#### 3.2 LSM-Tree 아키텍처

LSM-Tree(Log-Structured Merge-Tree)는 SSTable 위에 구축된 완성된 스토리지 엔진 아키텍처다.

```
┌─────────────────────────────────────────────────────┐
│                 LSM-Tree 구조                        │
│                                                     │
│  ┌──────────────┐                                   │
│  │  Memtable    │ ← 쓰기 (인메모리, 정렬된 트리)    │
│  │ (Red-Black   │                                   │
│  │  Tree)       │                                   │
│  └──────┬───────┘                                   │
│         │ 임계치 초과 시 flush                       │
│         ▼                                           │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐      │
│  │ SSTable 1  │ │ SSTable 2  │ │ SSTable 3  │      │
│  │ (newest)   │ │            │ │ (oldest)   │      │
│  └────────────┘ └────────────┘ └────────────┘      │
│         └────────────┴────────────┘                 │
│              Background Compaction                   │
│                     ↓                                │
│          ┌──────────────────┐                       │
│          │ Merged SSTable   │                       │
│          │ (중복 제거, 정렬) │                       │
│          └──────────────────┘                       │
└─────────────────────────────────────────────────────┘
```

**쓰기 경로**: (1) Memtable(인메모리 정렬 트리)에 삽입 → (2) Memtable이 임계치를 초과하면 SSTable로 디스크에 flush → (3) 백그라운드에서 Compaction(병합, 중복/삭제 제거)

**읽기 경로**: (1) Memtable 확인 → (2) 최신 SSTable부터 오래된 순으로 검색 → (3) 키를 찾거나 모든 SSTable을 확인할 때까지 반복

**삭제**: 실제로 데이터를 지우지 않고 Tombstone(삭제 마커)을 추가한다. Compaction 과정에서 Tombstone과 해당 데이터가 함께 제거된다.

#### 3.3 Compaction 전략

| 전략 | 방식 | 장점 | 단점 |
|------|------|------|------|
| Size-Tiered | 비슷한 크기의 SSTable을 합침 | 높은 쓰기 처리량 | 임시로 큰 공간 필요 |
| Leveled | 레벨별 고정 크기, 점진적 병합 | 읽기 효율적, 공간 절약 | 쓰기 작업이 더 많음 |

RocksDB는 기본적으로 Leveled Compaction을, Cassandra는 Size-Tiered를 사용한다. 워크로드에 따라 전략을 선택할 수 있다.

---

### 4. Bloom Filter

LSM-Tree의 읽기 경로에서 "존재하지 않는 키"를 검색하면, 모든 SSTable을 순차적으로 확인해야 하므로 비효율적이다. Bloom Filter는 이 문제를 해결하는 확률적 자료구조다.

```
Bit Array: [0,0,1,0,1,0,0,0,0,1,0,0,0,0,0,0]
            0 1 2 3 4 5 6 7 8 9 ...

"handbag" 추가: hash → (2, 4, 9) → 해당 비트를 1로 설정

"handheld" 검색: hash → (2, 6, 11)
→ bit[6]=0 → 하나라도 0이면 확실히 없음! (SSTable skip)
```

**False Negative는 불가능하다**: 비트가 0이면 그 키를 추가한 적이 없다는 뜻이므로, "없다"는 판단은 100% 정확하다.

**False Positive는 가능하다**: 모든 비트가 1이어도 다른 키들이 우연히 같은 비트를 설정했을 수 있다. 이 경우 SSTable을 확인하면 되므로 정확성에 문제가 없다.

키당 10비트를 할당하면 약 1%의 False Positive Rate, 15비트면 약 0.1%의 False Positive Rate를 달성한다.

---

### 5. B-Tree

B-Tree는 1970년부터 사용된, 가장 오래되고 검증된 인덱스 자료구조다. PostgreSQL, MySQL, Oracle 등 대부분의 관계형 DB가 B-Tree(실제로는 B+Tree) 기반이다.

```
                    ┌─────────────┐
                    │    Root     │
                    │ [100][200]  │
                    └──────┬──────┘
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
     ┌──────────┐   ┌──────────┐   ┌──────────┐
     │  <100    │   │ 100-200  │   │  >200    │
     │ [50][75] │   │[150][175]│   │[250][275]│
     └────┬─────┘   └────┬─────┘   └────┬─────┘
          ▼              ▼              ▼
      Leaf Pages     Leaf Pages     Leaf Pages
```

**핵심 특징:**
- 고정 크기 페이지(보통 4KB~16KB) 단위로 데이터를 저장하고 읽는다
- In-place Update: LSM-Tree와 달리 기존 페이지를 직접 덮어쓴다
- 항상 균형(Balanced)을 유지하여 O(log n) 깊이를 보장한다
- Branching Factor(한 페이지의 자식 참조 수)가 보통 수백 개이므로, 4단계만으로 수백 테라바이트의 데이터를 탐색할 수 있다

**B-Tree vs B+Tree**: 대부분의 실제 DB는 B+Tree를 사용한다. B+Tree는 데이터를 리프 노드에만 저장하고, 리프 노드를 Linked List로 연결한다. 이 구조 덕분에 범위 쿼리 시 리프 노드를 순차적으로 따라가면 되어 효율적이다.

**페이지 분할(Page Split)**: 새 키를 삽입할 때 페이지가 꽉 차 있으면, 페이지를 둘로 나누고 부모에 새 경계값을 추가한다. 이 과정에서 여러 페이지를 동시에 수정해야 하므로, 크래시 시 데이터 손상을 방지하기 위해 WAL이 필요하다.

---

### 6. Write-Ahead Log (WAL)

B-Tree는 페이지를 직접 덮어쓰기 때문에, 쓰기 도중 크래시가 발생하면 페이지가 반쯤 수정된 상태(corrupted state)로 남을 수 있다. WAL은 이 문제를 해결한다.

```
쓰기 순서:
1. WAL에 "무엇을 할 것인지" 먼저 기록 (append-only, sequential)
2. B-Tree 페이지 실제 수정 (random write)
3. 크래시 발생 시 → WAL을 재생하여 복구
```

WAL은 append-only 파일이므로 순차 쓰기(sequential write)로 빠르게 기록된다. B-Tree 페이지 수정은 랜덤 쓰기(random write)이므로 상대적으로 느리다. 크래시가 발생하면 WAL의 기록을 확인하여, 완료되지 않은 작업을 다시 실행하거나 롤백한다.

PostgreSQL에서 WAL은 `pg_wal/` 디렉토리에 저장되며, 복제(replication)의 기반이기도 하다. 스트리밍 복제는 WAL 레코드를 실시간으로 대기 서버에 전송하여 동기화한다.

---

### 7. LSM-Tree vs B-Tree 비교

| 특성 | B-Tree | LSM-Tree |
|------|--------|----------|
| 읽기 성능 | 빠르고 예측 가능 | 여러 SSTable 확인 필요 |
| 쓰기 패턴 | Random Write (페이지 덮어쓰기) | Sequential Write (append) |
| 쓰기 처리량 | 보통 | 높음 (sequential I/O 이점) |
| Write Amplification | WAL + 전체 페이지 재작성 | WAL + flush + Compaction N회 |
| 디스크 공간 | Fragmentation 발생 가능 | Compaction으로 정리 |
| 범위 쿼리 | 빠름 (리프 Linked List) | 여러 SSTable 병렬 스캔 |
| 적합한 워크로드 | 읽기 중심 OLTP | 쓰기 중심 OLTP |

**Write Amplification**은 애플리케이션이 1바이트를 쓸 때 디스크에 실제로 몇 바이트가 쓰이는지의 비율이다. B-Tree는 작은 변경에도 전체 페이지(4KB~16KB)를 재작성하고, LSM-Tree는 Compaction으로 같은 데이터를 여러 번 재작성한다. SSD의 수명과 클라우드 I/O 비용에 직접적인 영향을 미치므로 워크로드에 맞는 선택이 중요하다.

---

### 8. Column-Oriented Storage

OLAP(분석) 워크로드에서는 수백 개 컬럼 중 2~3개만 필요한 쿼리가 대부분이다. Row-Oriented Storage는 불필요한 컬럼까지 모두 디스크에서 읽어야 하므로 비효율적이다.

```
Row-Oriented:
Row 1: [date, product, store, qty, price, ...]  ← 전체 Row 로드
Row 2: [date, product, store, qty, price, ...]

Column-Oriented:
[date]    [product]  [qty]     ← 필요한 컬럼만 로드
[값1]     [값1]      [값1]
[값2]     [값2]      [값2]
```

Column-Oriented Storage의 이점은 세 가지다:
1. **I/O 감소**: 100개 컬럼 중 3개만 읽으면 디스크 I/O가 97% 줄어든다
2. **압축 효율**: 같은 타입의 값이 연속으로 저장되므로 Bitmap Encoding, Run-Length Encoding 등으로 높은 압축률을 달성한다
3. **Vectorized Processing**: 배치 단위로 CPU 캐시와 SIMD 명령어를 활용할 수 있다

```
Bitmap Encoding 예시:
product_sk 컬럼 (값: 31, 68, 69)

product_sk = 31: [1, 0, 1, 0, 1, 0, 1, ...]
product_sk = 68: [0, 1, 0, 0, 0, 1, 0, ...]

WHERE product_sk IN (31, 68)
→ bitmap_31 OR bitmap_68 → bitwise 연산으로 수행
```

Snowflake, ClickHouse, DuckDB 같은 분석 전용 DB가 Column-Oriented Storage를 사용한다.

---

### 9. 특수 인덱스

B-Tree와 LSM-Tree 외에도 특정 워크로드에 최적화된 인덱스들이 존재한다.

| 인덱스 | 용도 | PostgreSQL 지원 |
|--------|------|----------------|
| GIN (Generalized Inverted Index) | 배열, JSON, 전문 검색 | `CREATE INDEX ... USING gin` |
| GiST (Generalized Search Tree) | 공간 데이터, 범위 타입 | `CREATE INDEX ... USING gist` |
| BRIN (Block Range Index) | 시계열, 물리적 정렬 데이터 | `CREATE INDEX ... USING brin` |
| HNSW | 벡터 유사도 검색 | pgvector 확장 |

BRIN은 물리적으로 정렬된 대용량 테이블(시계열 로그 등)에서 인덱스 크기를 극도로 줄여준다. 전체 테이블 인덱스 대신 블록 범위의 최소/최대값만 저장하기 때문이다.

---

## 핵심 정리
| 개념 | 한 줄 요약 |
|------|-----------|
| Hash Index | O(1) 조회지만 범위 쿼리 불가, 메모리에 키 전체를 올려야 한다 |
| SSTable | 정렬된 키-값 파일로, Sparse Index와 범위 쿼리를 지원한다 |
| LSM-Tree | Memtable → SSTable → Compaction 구조로 높은 쓰기 처리량을 제공한다 |
| Bloom Filter | "확실히 없다"는 보장으로 불필요한 SSTable 탐색을 줄인다 |
| B-Tree | 고정 크기 페이지 기반, 예측 가능한 읽기 성능이 강점이다 |
| WAL | 크래시 복구를 위해 실제 수정 전에 먼저 기록하는 로그다 |
| Column Storage | 분석 쿼리에서 필요한 컬럼만 읽어 I/O와 압축 효율을 극대화한다 |
| Write Amplification | 실제 디스크 쓰기량 / 논리적 쓰기량 비율로, SSD 수명과 비용에 영향을 준다 |
