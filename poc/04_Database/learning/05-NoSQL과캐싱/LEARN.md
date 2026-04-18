# Ch.05 - NoSQL과 캐싱

> **이론 매핑**: `docs/04_Database/01_기본개념/06_NoSQL_비교.md`, `docs/04_Database/01_기본개념/07_캐싱_전략.md`

---

## 핵심 요약
> NoSQL 데이터베이스는 관계형 모델의 한계를 넘어 수평 확장, 유연한 스키마, 다양한 데이터 모델을 제공한다. Document, Key-Value, Wide-Column, Graph의 네 가지 유형은 각각 다른 데이터 접근 패턴에 최적화되어 있다. 캐싱은 데이터베이스 부하를 줄이고 응답 속도를 10~100배 개선하는 핵심 기법으로, Cache-Aside, Write-Through, Write-Behind 패턴과 캐시 무효화 전략을 이해해야 안정적인 시스템을 구축할 수 있다.

---

## 학습 목표
1. NoSQL의 네 가지 유형(Document, Key-Value, Wide-Column, Graph)을 구분하고 적합한 사용 사례를 판단할 수 있다
2. CAP 정리와 ACID vs BASE의 차이를 설명할 수 있다
3. Cache-Aside, Write-Through, Write-Behind 패턴을 구분하고 상황별로 선택할 수 있다
4. Cache Stampede, Hot Key, Cache Penetration 문제를 이해하고 해결 방안을 제시할 수 있다
5. Redis의 자료구조와 활용 패턴을 이해할 수 있다

---

## 본문

### 1. NoSQL의 등장 배경

관계형 데이터베이스는 수십 년간 데이터 저장의 표준이었지만, 웹 규모(web-scale) 서비스가 등장하면서 한계가 드러났다. 수평 확장(샤딩)의 복잡성, 스키마 변경의 어려움, 비정형 데이터 처리의 비효율성, 그리고 초당 수십만 건의 쓰기 처리 요구가 그 한계다.

NoSQL은 "Not Only SQL"의 약자로, 관계형 모델을 대체하는 것이 아니라 보완하는 선택지다. 수평 확장이 용이하고, 유연한 스키마를 제공하며, 특정 접근 패턴에 최적화된 다양한 데이터 모델을 제공한다.

---

### 2. CAP 정리와 BASE

분산 시스템의 설계 원칙을 이해하는 데 CAP 정리가 기본 프레임워크를 제공한다.

**CAP 정리**: 네트워크 파티션(P)이 발생하면, 일관성(C)과 가용성(A) 중 하나를 선택해야 한다. 분산 시스템에서 네트워크 파티션은 피할 수 없으므로, 실질적인 선택은 CP(일관성 우선)와 AP(가용성 우선) 사이에서 이루어진다.

| 선택 | 의미 | 예시 |
|------|------|------|
| CP | 파티션 시 일관성 유지, 일부 요청 거부 | MongoDB, HBase |
| AP | 파티션 시 가용성 유지, 일시적 불일치 허용 | Cassandra, DynamoDB |

**ACID vs BASE**:

| ACID (RDBMS) | BASE (NoSQL) |
|--------------|--------------|
| Atomicity: 전체 성공/전체 실패 | Basically Available: 기본적으로 가용 |
| Consistency: 불변식 유지 | Soft state: 시간에 따라 상태 변화 가능 |
| Isolation: 트랜잭션 간 격리 | Eventually consistent: 결국 일관성 달성 |
| Durability: 영구 저장 | |

CAP 정리를 적용할 때 흔한 오해가 있다. "평상시에도 C와 A를 동시에 가질 수 없다"는 것은 틀린 해석이다. 네트워크가 정상일 때는 C와 A를 모두 만족할 수 있으며, 파티션이 발생했을 때만 선택이 강제된다.

---

### 3. NoSQL 네 가지 유형

#### 3.1 Document Database

JSON/BSON 형태의 문서를 저장한다. MongoDB가 대표적이며, 유연한 스키마와 중첩 데이터 구조를 지원한다.

```json
{
  "_id": "user123",
  "name": "Alice",
  "orders": [
    {"order_id": "ord001", "items": [{"product": "Laptop", "price": 999}]}
  ]
}
```

적합한 경우: 콘텐츠 관리 시스템, 제품 카탈로그, 사용자 프로필처럼 문서 단위로 조회하는 패턴. 스키마가 자주 변하거나 엔티티마다 구조가 다른 경우에 유리하다.

#### 3.2 Key-Value Store

가장 단순한 데이터 모델로, 키를 주면 값을 반환한다. Redis가 대표적이며, 인메모리 기반으로 수 마이크로초 수준의 응답 속도를 제공한다.

Redis는 단순 key-value를 넘어 다양한 자료구조를 지원한다:

| 타입 | 용도 | 사용 사례 |
|------|------|----------|
| String | 기본 key-value | 캐싱, 세션 |
| Hash | 필드-값 쌍 | 객체 저장 |
| List | 순서 있는 문자열 | 큐, 타임라인 |
| Set | 중복 없는 집합 | 태그, 팔로워 |
| Sorted Set | 점수 기반 정렬 | 리더보드, 랭킹 |

적합한 경우: 세션 관리, 캐싱, 실시간 리더보드, Rate Limiting, Pub/Sub 메시징.

#### 3.3 Wide-Column Store

행(Row Key)과 열 패밀리(Column Family)로 구성된 희소 행렬(Sparse Matrix) 구조다. Cassandra와 HBase가 대표적이다.

```
Row Key         Column Family: user_info    CF: activity
user:123        name: "Alice"               login: "2024-01-15"
                email: "alice@..."          views: 150

user:456        name: "Bob"                 login: "2024-01-14"
                phone: "+1..."              views: 80
```

각 행이 서로 다른 컬럼을 가질 수 있다는 점이 관계형 테이블과 근본적으로 다르다. 파티션 키로 데이터를 분산하고, 클러스터링 키로 파티션 내 정렬을 제어한다.

적합한 경우: 시계열 데이터, IoT 센서 데이터, 로그/이벤트 저장, 대규모 분석 워크로드. 쓰기 처리량이 중요하고 데이터 양이 수 TB 이상인 경우에 강점이 있다.

#### 3.4 Graph Database

노드(Node)와 엣지(Edge)로 관계를 직접 모델링한다. Neo4j가 대표적이며, Cypher 쿼리 언어를 사용한다.

```cypher
// 친구의 친구가 구매한 제품 추천
MATCH (me:User {name: 'Alice'})-[:FOLLOWS*2]->(fof)-[:PURCHASED]->(product)
WHERE NOT (me)-[:PURCHASED]->(product)
RETURN product.name, COUNT(*) AS score ORDER BY score DESC
```

적합한 경우: 소셜 네트워크, 추천 엔진, 사기 탐지, 지식 그래프. "관계 자체가 데이터"인 도메인에서 관계형 DB의 JOIN보다 수십 배 빠른 관계 탐색이 가능하다.

---

### 4. DB 선택 가이드

```
"ACID 트랜잭션 필수?"      → Yes → PostgreSQL (RDBMS)
    │ No
"데이터 관계가 복잡?"      → Yes → Neo4j (Graph)
    │ No
"단순 조회/캐싱?"          → Yes → Redis (Key-Value)
    │ No
"시계열/대용량 쓰기?"      → Yes → Cassandra (Wide-Column)
    │ No
"유연한 스키마 필요?"      → Yes → MongoDB (Document)
    │ No
    └→ PostgreSQL (범용 선택)
```

실무에서는 하나의 DB만 사용하는 것이 아니라, 목적에 맞게 여러 DB를 조합하는 **Polyglot Persistence** 전략이 일반적이다. PostgreSQL을 주 데이터베이스로, Redis를 캐시로, Elasticsearch를 검색 엔진으로 조합하는 식이다.

---

### 5. 캐싱의 필요성

캐싱이 필요한 이유는 레이턴시 차이에 있다:

| 작업 | 지연 시간 |
|------|----------|
| Redis 조회 | 100~500us |
| PostgreSQL 단순 쿼리 | 1~10ms |
| PostgreSQL 복잡 쿼리 | 10~1000ms |

Redis는 DB보다 10~100배 빠르다. 동일한 데이터를 반복 조회하는 패턴에서 캐시를 도입하면, DB 부하가 줄고 응답 시간이 개선된다. 단, 캐시는 새로운 복잡성(일관성, 무효화, 장애 처리)을 추가하므로 무조건적인 해결책은 아니다.

---

### 6. 캐싱 패턴

#### 6.1 Cache-Aside (Lazy Loading)

가장 널리 사용되는 패턴이다. 애플리케이션이 직접 캐시와 DB를 관리한다.

```
읽기:
1. 캐시 확인 → Hit → 반환
2. Miss → DB 조회 → 캐시에 저장 → 반환

쓰기:
1. DB에 쓰기
2. 캐시 무효화 (삭제)
```

```python
def get_user(user_id):
    cached = redis.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)
    user = db.query("SELECT * FROM users WHERE id = %s", user_id)
    redis.setex(f"user:{user_id}", 3600, json.dumps(user))
    return user
```

장점: 필요한 데이터만 캐싱하므로 메모리 효율적이다. 구현이 단순하다.
단점: 첫 요청은 항상 Cache Miss. 캐시와 DB 사이에 일시적 불일치가 발생할 수 있다.

#### 6.2 Write-Through

쓰기 시 캐시와 DB를 동기적으로 함께 업데이트한다.

```
쓰기: App → Cache → DB (동기)
```

장점: 캐시와 DB가 항상 일관적이다.
단점: 쓰기 지연이 증가한다. 읽히지 않는 데이터도 캐시에 올라간다.

#### 6.3 Write-Behind (Write-Back)

쓰기 시 캐시에만 즉시 반영하고, DB에는 비동기로 나중에 반영한다.

```
쓰기: App → Cache → 즉시 응답 → (비동기) → DB
```

장점: 쓰기 응답이 빠르다. 여러 쓰기를 배치로 묶어 DB에 반영할 수 있다.
단점: 구현이 복잡하다. 캐시 장애 시 아직 DB에 반영되지 않은 데이터가 유실될 수 있다.

---

### 7. 캐시 무효화 전략

캐시에서 가장 어려운 문제는 "언제 캐시를 갱신하는가?"이다.

**TTL (Time-To-Live)**: 일정 시간 후 자동 만료. 설정이 단순하지만, 만료 전까지 옛 데이터가 노출될 수 있다.

```python
CACHE_TTL = {
    "user_profile": 3600,    # 1시간 (변경 빈도 낮음)
    "product_list": 300,     # 5분 (중간 빈도)
    "stock_price": 5,        # 5초 (실시간 데이터)
}
```

TTL 결정 기준은 "데이터가 얼마 동안 옛 상태여도 괜찮은가?"이다. 비즈니스 요구사항에 따라 달라진다.

**Event-Driven Invalidation**: 데이터 변경 시 관련 캐시를 즉시 삭제한다. TTL보다 일관성이 높지만, 어떤 캐시 키가 영향을 받는지 추적해야 한다.

```python
def update_product(product_id, data):
    db.execute("UPDATE products SET ... WHERE id = %s", product_id)
    redis.delete(f"product:{product_id}")
    redis.delete(f"product_list:category:{data['category']}")
```

**Cache Tagging**: 관련 캐시 키에 태그를 붙여, 태그 기반으로 그룹 삭제한다. "electronics" 태그가 붙은 모든 제품 캐시를 한 번에 삭제하는 식이다.

---

### 8. 캐시 관련 문제와 해결

#### 8.1 Cache Stampede (Thundering Herd)

인기 있는 캐시 키가 만료되는 순간, 수백 개의 요청이 동시에 DB로 몰리는 현상이다. DB에 순간적으로 과부하가 걸린다.

```
캐시 만료 시점:
Request 1 ──→ Cache Miss ──→ DB Query ──┐
Request 2 ──→ Cache Miss ──→ DB Query ──│── DB 과부하!
Request 3 ──→ Cache Miss ──→ DB Query ──│
...                                      │
```

**해결책 1: 락(Lock) 사용**
첫 번째 요청만 DB를 조회하고, 나머지는 대기한 뒤 캐시에서 읽는다.

```python
def get_with_lock(key, fetch_func, ttl=3600):
    value = redis.get(key)
    if value:
        return json.loads(value)
    lock_key = f"lock:{key}"
    if redis.setnx(lock_key, 1):
        redis.expire(lock_key, 30)
        try:
            value = fetch_func()
            redis.setex(key, ttl, json.dumps(value))
            return value
        finally:
            redis.delete(lock_key)
    else:
        time.sleep(0.1)
        return get_with_lock(key, fetch_func, ttl)
```

**해결책 2: Probabilistic Early Expiration**
만료 시각에 가까울수록 확률적으로 미리 갱신하여, 동시 만료를 분산시킨다.

#### 8.2 Hot Key

특정 키에 요청이 집중되어 Redis 단일 노드가 병목이 되는 현상이다.

해결: (1) 키를 복제하여 `hot_key:1`, `hot_key:2`로 분산하고 랜덤 선택. (2) 애플리케이션 로컬 캐시(L1)를 추가하여 Redis 접근 자체를 줄인다.

#### 8.3 Cache Penetration

존재하지 않는 데이터에 대한 반복 요청이 캐시를 통과하여 매번 DB를 조회하는 현상이다. 악의적인 공격에 악용될 수 있다.

해결: (1) Null 캐싱 - 없는 데이터도 짧은 TTL로 캐싱한다. (2) Bloom Filter - 데이터 존재 여부를 사전 확인한다.

```python
def get_with_null_cache(key, fetch_func):
    value = redis.get(key)
    if value == "NULL":
        return None    # 캐시된 null
    if value:
        return json.loads(value)
    result = fetch_func()
    if result is None:
        redis.setex(key, 60, "NULL")    # 1분간 null 캐싱
    else:
        redis.setex(key, 3600, json.dumps(result))
    return result
```

---

### 9. 다단계 캐싱 (Multi-Level Caching)

```
L1: 로컬 캐시 (애플리케이션 메모리)
    → 가장 빠름, 용량 작음, 서버별 분리

L2: 분산 캐시 (Redis)
    → 빠름, 용량 중간, 서버 간 공유

L3: 데이터베이스
    → 느림, 용량 큼, 영구 저장
```

L1은 단일 서버 내에서만 유효하므로 서버 간 데이터 불일치가 생길 수 있다. TTL을 짧게(수 초) 설정하거나, Pub/Sub로 무효화 이벤트를 전파하여 해결한다. L1 + L2 조합은 Hot Key 문제를 완화하는 데도 효과적이다.

---

## 핵심 정리
| 개념 | 한 줄 요약 |
|------|-----------|
| CAP 정리 | 네트워크 파티션 시 일관성과 가용성 중 하나를 선택해야 한다 |
| Document DB | JSON 문서 저장, 유연한 스키마와 문서 단위 조회에 적합하다 |
| Key-Value Store | 가장 빠른 조회, 캐싱과 세션 관리의 표준이다 |
| Wide-Column Store | 대규모 쓰기와 시계열 데이터에 최적화되어 있다 |
| Graph DB | 관계 탐색이 핵심인 도메인에서 관계형 JOIN보다 빠르다 |
| Cache-Aside | 가장 보편적인 캐싱 패턴으로, 필요 시 DB에서 읽어 캐시에 저장한다 |
| Cache Stampede | 캐시 만료 시 동시 DB 조회 폭주 현상, 락이나 확률적 갱신으로 방지한다 |
| Null 캐싱 | 존재하지 않는 데이터도 캐싱하여 DB 보호한다 |
