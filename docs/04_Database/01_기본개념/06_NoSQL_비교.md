# NoSQL 데이터베이스 비교

---

## 📌 핵심 요약

NoSQL 데이터베이스는 관계형 모델의 제약을 벗어나 다양한 데이터 모델과 확장성을 제공한다. Document, Key-Value, Wide-Column, Graph DB의 특성과 적합한 사용 사례를 비교한다.

---

## 🎯 학습 목표

- [ ] NoSQL 데이터베이스의 4가지 주요 유형을 구분할 수 있다
- [ ] 각 유형의 데이터 모델과 쿼리 패턴을 이해할 수 있다
- [ ] CAP 정리와 BASE 속성을 설명할 수 있다
- [ ] 사용 사례에 따른 적절한 DB를 선택할 수 있다

---

## 📖 본문

### 1. NoSQL의 등장 배경

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SQL vs NoSQL                                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   RDBMS의 한계:                                                      │
│   ├── 수평 확장(샤딩)의 복잡성                                       │
│   ├── 스키마 변경의 어려움                                           │
│   ├── 비정형 데이터 처리의 비효율성                                  │
│   └── 높은 쓰기 처리량 요구 시 병목                                  │
│                                                                     │
│   NoSQL의 해결:                                                      │
│   ├── 수평 확장 용이 (Horizontal Scaling)                           │
│   ├── 유연한 스키마 (Schema-less/Schema-on-read)                    │
│   ├── 다양한 데이터 모델                                             │
│   └── 분산 시스템 설계 (Partition Tolerance)                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

### 2. CAP 정리와 BASE

#### 2.1 CAP 정리

```
         Consistency
            /\
           /  \
          /    \
         /  CA  \
        /________\
       /\        /\
      /  \  CP  /  \
     / AP \    /    \
    /______\  /______\
  Availability   Partition
                 Tolerance
```

| 속성 | 설명 | 선택 예시 |
|------|------|----------|
| **Consistency** | 모든 노드가 같은 데이터 | CP: MongoDB, HBase |
| **Availability** | 항상 응답 가능 | AP: Cassandra, DynamoDB |
| **Partition Tolerance** | 네트워크 분할 시 동작 | 분산 시스템에서 필수 |

> ⚠️ 네트워크 파티션이 발생하면 C와 A 중 하나를 선택해야 함

#### 2.2 ACID vs BASE

| ACID (RDBMS) | BASE (NoSQL) |
|--------------|--------------|
| Atomicity | Basically Available |
| Consistency | Soft state |
| Isolation | Eventually consistent |
| Durability | |

---

### 3. Document Database

#### 3.1 대표 제품

| 제품 | 특징 |
|------|------|
| **MongoDB** | 가장 인기, JSON-like 문서 |
| **CouchDB** | HTTP API, 오프라인 우선 |
| **Amazon DocumentDB** | MongoDB 호환, AWS 관리형 |

#### 3.2 데이터 모델

```json
{
  "_id": "user123",
  "name": "Alice",
  "email": "alice@example.com",
  "orders": [
    {
      "order_id": "ord001",
      "items": [
        {"product": "Laptop", "price": 999},
        {"product": "Mouse", "price": 29}
      ],
      "total": 1028
    }
  ]
}
```

#### 3.3 특징

| 특성 | 설명 |
|------|------|
| **스키마 유연성** | 문서마다 다른 구조 가능 |
| **Nested Documents** | 관련 데이터 함께 저장 (JOIN 불필요) |
| **쿼리 언어** | JSON 기반 쿼리 |
| **인덱스** | 필드, 복합, 전문 검색 |

#### 3.4 적합한 사용 사례

- 콘텐츠 관리 시스템 (CMS)
- 제품 카탈로그
- 사용자 프로필
- 실시간 분석

---

### 4. Key-Value Store

#### 4.1 대표 제품

| 제품 | 특징 |
|------|------|
| **Redis** | 인메모리, 다양한 자료구조 |
| **Amazon DynamoDB** | 서버리스, 자동 확장 |
| **Memcached** | 단순 캐싱, 고성능 |

#### 4.2 데이터 모델

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Key-Value 모델                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   Key                    Value                                      │
│   ─────────────────────────────────────────────                    │
│   "user:123"       →    {"name": "Alice", "email": "..."}          │
│   "session:abc"    →    {"user_id": 123, "expires": 3600}          │
│   "counter:views"  →    42                                          │
│                                                                     │
│   API: GET, SET, DELETE, EXISTS                                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

#### 4.3 Redis 자료구조

| 타입 | 설명 | 사용 사례 |
|------|------|----------|
| String | 기본 key-value | 캐싱, 세션 |
| Hash | 필드-값 쌍 | 객체 저장 |
| List | 순서 있는 문자열 | 큐, 타임라인 |
| Set | 중복 없는 집합 | 태그, 팔로워 |
| Sorted Set | 점수 기반 정렬 | 리더보드, 랭킹 |

#### 4.4 적합한 사용 사례

- 세션 관리
- 캐싱 (Cache-aside)
- 실시간 리더보드
- Rate Limiting
- Pub/Sub 메시징

---

### 5. Wide-Column Store

#### 5.1 대표 제품

| 제품 | 특징 |
|------|------|
| **Apache Cassandra** | 링 아키텍처, 높은 가용성 |
| **HBase** | Hadoop 생태계, HDFS 기반 |
| **Google Bigtable** | GCP 관리형, 대규모 분석 |

#### 5.2 데이터 모델

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Wide-Column 모델                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   Row Key         Column Family: user_info    CF: activity         │
│   ─────────────────────────────────────────────────────────────    │
│   user:123        name: "Alice"               login: "2024-01-15"  │
│                   email: "alice@..."          views: 150           │
│                                               clicks: 42           │
│                                                                     │
│   user:456        name: "Bob"                 login: "2024-01-14"  │
│                   phone: "+1..."              views: 80            │
│                                                                     │
│   특징: 열마다 다른 컬럼 가질 수 있음 (Sparse Matrix)               │
└─────────────────────────────────────────────────────────────────────┘
```

#### 5.3 Cassandra CQL

```sql
-- 테이블 생성
CREATE TABLE user_activity (
    user_id uuid,
    activity_date date,
    activity_type text,
    details text,
    PRIMARY KEY ((user_id), activity_date, activity_type)
) WITH CLUSTERING ORDER BY (activity_date DESC);

-- 파티션 키로 조회 (효율적)
SELECT * FROM user_activity WHERE user_id = ?;

-- 클러스터링 키로 범위 조회
SELECT * FROM user_activity
WHERE user_id = ? AND activity_date >= '2024-01-01';
```

#### 5.4 적합한 사용 사례

- 시계열 데이터
- IoT 센서 데이터
- 로그/이벤트 저장
- 대규모 분석 워크로드

---

### 6. Graph Database

#### 6.1 대표 제품

| 제품 | 특징 |
|------|------|
| **Neo4j** | 가장 인기, Cypher 쿼리 |
| **Amazon Neptune** | AWS 관리형, RDF/Property Graph |
| **TigerGraph** | 대규모 분석, 병렬 처리 |

#### 6.2 데이터 모델

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Graph 모델                                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│        ┌─────────┐                    ┌─────────┐                  │
│        │  Alice  │ ──FOLLOWS──────→   │   Bob   │                  │
│        │ (User)  │ ←──FOLLOWS────     │ (User)  │                  │
│        └────┬────┘                    └────┬────┘                  │
│             │                              │                        │
│        PURCHASED                      PURCHASED                    │
│             │                              │                        │
│             ▼                              ▼                        │
│        ┌─────────┐                    ┌─────────┐                  │
│        │ Laptop  │                    │ Laptop  │                  │
│        │(Product)│                    │(Product)│                  │
│        └─────────┘                    └─────────┘                  │
│                                                                     │
│   노드(Node): 엔티티                                                 │
│   엣지(Edge): 관계 (방향, 속성 포함 가능)                            │
│   속성(Property): 노드/엣지의 메타데이터                             │
└─────────────────────────────────────────────────────────────────────┘
```

#### 6.3 Neo4j Cypher

```cypher
// 노드 생성
CREATE (alice:User {name: 'Alice', email: 'alice@example.com'})
CREATE (bob:User {name: 'Bob'})
CREATE (laptop:Product {name: 'Laptop', price: 999})

// 관계 생성
CREATE (alice)-[:FOLLOWS]->(bob)
CREATE (alice)-[:PURCHASED {date: '2024-01-15'}]->(laptop)

// 친구의 친구 찾기 (2단계)
MATCH (alice:User {name: 'Alice'})-[:FOLLOWS*2]->(fof)
RETURN DISTINCT fof.name

// 추천: 내가 구매한 것을 구매한 다른 사용자가 구매한 것
MATCH (me:User {name: 'Alice'})-[:PURCHASED]->(p)<-[:PURCHASED]-(other)
      -[:PURCHASED]->(rec)
WHERE NOT (me)-[:PURCHASED]->(rec)
RETURN rec.name, COUNT(*) AS score
ORDER BY score DESC
```

#### 6.4 적합한 사용 사례

- 소셜 네트워크
- 추천 엔진
- 사기 탐지
- 지식 그래프
- 네트워크 분석

---

### 7. 비교 요약

| 유형 | 데이터 모델 | 강점 | 약점 | 대표 제품 |
|------|------------|------|------|----------|
| **Document** | JSON 문서 | 유연한 스키마, 개발 생산성 | 복잡한 JOIN | MongoDB |
| **Key-Value** | 키-값 쌍 | 매우 빠름, 단순함 | 복잡한 쿼리 불가 | Redis |
| **Wide-Column** | 행-열 패밀리 | 대용량, 높은 쓰기 처리량 | 학습 곡선 | Cassandra |
| **Graph** | 노드-엣지 | 관계 탐색 최적화 | 전체 집계 비효율 | Neo4j |

---

### 8. 선택 가이드

```
┌─────────────────────────────────────────────────────────────────────┐
│                    어떤 DB를 선택할까?                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   "ACID 트랜잭션 필수?" ──Yes──→ PostgreSQL (RDBMS)                 │
│         │                                                           │
│        No                                                           │
│         │                                                           │
│   "데이터 관계가 복잡?" ──Yes──→ Neo4j (Graph)                      │
│         │                                                           │
│        No                                                           │
│         │                                                           │
│   "단순 조회/캐싱?" ──Yes──→ Redis (Key-Value)                      │
│         │                                                           │
│        No                                                           │
│         │                                                           │
│   "시계열/대용량 쓰기?" ──Yes──→ Cassandra (Wide-Column)            │
│         │                                                           │
│        No                                                           │
│         │                                                           │
│   "유연한 스키마 필요?" ──Yes──→ MongoDB (Document)                 │
│         │                                                           │
│        No                                                           │
│         ▼                                                           │
│   PostgreSQL (범용 선택)                                            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 💡 실무 적용

### NewSQL: RDBMS + NoSQL

| 제품 | 특징 |
|------|------|
| CockroachDB | PostgreSQL 호환, 분산 SQL |
| TiDB | MySQL 호환, HTAP |
| YugabyteDB | PostgreSQL 호환, 분산 SQL |
| Spanner | Google, 전역 분산 |

### Polyglot Persistence

```
┌─────────────────────────────────────────────────────────────────────┐
│   실제 아키텍처에서 여러 DB 조합 사용                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐               │
│   │ PostgreSQL  │  │    Redis    │  │  MongoDB    │               │
│   │  (주 데이터) │  │   (캐시)    │  │  (로그/분석) │               │
│   └─────────────┘  └─────────────┘  └─────────────┘               │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## ✅ 체크리스트

- [ ] Document, Key-Value, Wide-Column, Graph DB를 구분할 수 있다
- [ ] CAP 정리를 설명할 수 있다
- [ ] ACID와 BASE의 차이를 이해한다
- [ ] 각 NoSQL 유형의 적합한 사용 사례를 알고 있다
- [ ] Polyglot Persistence 전략을 이해한다

---

## 🔗 참고 자료

- 📚 Designing Data-Intensive Applications (Martin Kleppmann)
- 📄 MongoDB Documentation: https://docs.mongodb.com/
- 📄 Redis Documentation: https://redis.io/docs/
- 📄 Cassandra Documentation: https://cassandra.apache.org/doc/
- 📄 Neo4j Documentation: https://neo4j.com/docs/
