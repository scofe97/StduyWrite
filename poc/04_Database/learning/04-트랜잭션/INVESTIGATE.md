# Ch.04 - 트랜잭션: 심화 탐구

> LEARN.md를 학습한 뒤, 더 깊이 파고들어야 할 질문들

---

## Q1. 격리 수준별 이상 현상(anomaly)은 구체적으로 어떻게 발생하는가?

### 왜 이 질문이 중요한가
"격리 수준 표"를 암기하는 것과 실제 발생 시나리오를 구체적으로 설명할 수 있는 것은 다른 수준의 이해다. 기술 면접에서 단골로 출제되며, 실무에서 버그의 원인을 진단할 때 이 지식이 직접적으로 쓰인다.

### 답변

**시나리오 1: Read Committed에서의 Read Skew**

은행 잔액 조회를 예로 들면:
```
계좌 A: $500, 계좌 B: $500 (총 $1000)

Alice의 트랜잭션:
  1. Read(A) → $500
  2. (이 사이에 Bob이 A→B로 $100 이체, COMMIT)
  3. Read(B) → $600

Alice가 본 합계: $500 + $600 = $1100 (실제는 $1000)
```
Read Committed에서는 각 SELECT가 "그 시점에 커밋된 최신 값"을 읽으므로, 같은 트랜잭션 내에서도 다른 시점의 데이터를 볼 수 있다. Snapshot Isolation에서는 트랜잭션 시작 시점의 스냅샷을 사용하므로 이 문제가 방지된다.

**시나리오 2: Snapshot Isolation에서의 Write Skew**

병원 당직 의사:
```
규칙: 최소 1명 당직
현재 당직: Alice, Bob (2명)

T1 (Alice): SELECT COUNT(*) WHERE on_call = true → 2
            "2명이니 내가 빠져도 됨"
            UPDATE SET on_call = false WHERE name = 'Alice'

T2 (Bob):   SELECT COUNT(*) WHERE on_call = true → 2  ← 스냅샷이므로 아직 2
            "2명이니 나도 빠져도 됨"
            UPDATE SET on_call = false WHERE name = 'Bob'

두 트랜잭션 모두 COMMIT → 당직 0명!
```

Write Skew가 Lost Update와 다른 점은, 두 트랜잭션이 **서로 다른 행**을 수정한다는 것이다. Lost Update는 같은 행을 수정하므로 DB가 감지할 수 있지만, Write Skew는 각 트랜잭션이 다른 행을 건드리므로 행 수준 잠금으로는 감지할 수 없다.

**시나리오 3: Phantom Read**

회의실 예약:
```
T1: SELECT COUNT(*) FROM bookings WHERE room = 123 AND time = '10:00' → 0
    "빈 시간대네, 예약!"
    INSERT INTO bookings (room, time, user) VALUES (123, '10:00', 'Alice')

T2: SELECT COUNT(*) FROM bookings WHERE room = 123 AND time = '10:00' → 0
    "빈 시간대네, 나도 예약!"
    INSERT INTO bookings (room, time, user) VALUES (123, '10:00', 'Bob')

결과: 같은 방, 같은 시간에 두 예약!
```

Phantom은 아직 존재하지 않는 행에 대한 문제이므로, SELECT FOR UPDATE로도 잠금을 걸 수 없다(잠글 행이 없으므로). Materializing Conflicts 기법으로 빈 슬롯을 미리 생성하거나, Serializable 격리를 사용해야 한다.

### 실무 적용
대부분의 OLTP 애플리케이션은 Read Committed(기본값)에서 시작하되, 금융 계산이나 예약 시스템처럼 정확성이 중요한 부분에만 Serializable이나 SELECT FOR UPDATE를 적용하는 것이 현실적이다. 전체 시스템을 Serializable로 운영하면 성능 비용이 크다.

---

## Q2. MVCC는 내부적으로 어떻게 동작하는가?

### 왜 이 질문이 중요한가
PostgreSQL을 사용하는 개발자라면 MVCC의 동작 원리를 이해해야 VACUUM, 오래된 트랜잭션으로 인한 테이블 비대화(bloat), 가시성 검사(visibility check) 등의 운영 이슈를 진단할 수 있다.

### 답변

**PostgreSQL MVCC의 핵심 구조:**

각 행(tuple)에는 두 개의 숨겨진 컬럼이 있다:
- `xmin`: 이 행을 생성(INSERT)한 트랜잭션 ID
- `xmax`: 이 행을 삭제(DELETE) 또는 수정(UPDATE)한 트랜잭션 ID

UPDATE는 내부적으로 "옛 행에 xmax 설정 + 새 행 INSERT"로 처리된다.

```
행 버전 1: xmin=100, xmax=200, data="Alice"
행 버전 2: xmin=200, xmax=0,   data="Alice Kim"  ← 현재 버전

트랜잭션 150이 읽으면:
- 버전 1의 xmin(100) < 150이고 xmax(200) > 150 → 버전 1이 보임
- 버전 2의 xmin(200) > 150 → 안 보임

트랜잭션 250이 읽으면:
- 버전 1의 xmax(200) < 250 → 이미 삭제됨, 안 보임
- 버전 2의 xmin(200) < 250이고 xmax=0 → 현재 유효, 보임
```

**VACUUM의 역할:**
더 이상 어떤 트랜잭션도 참조하지 않는 옛 행 버전(dead tuple)을 정리한다. VACUUM이 제대로 실행되지 않으면 테이블 크기가 계속 증가하는 "테이블 비대화(table bloat)"가 발생한다.

**오래된 트랜잭션의 위험:**
한 트랜잭션이 장시간 열려 있으면, 그 트랜잭션의 스냅샷 시점 이후에 삭제된 모든 dead tuple을 VACUUM이 정리할 수 없다. 이는 디스크 공간 낭비와 쿼리 성능 저하로 이어진다.

### 실무 적용
PostgreSQL에서는 `autovacuum`을 비활성화하지 않아야 한다. `pg_stat_activity`로 오래된 트랜잭션을 모니터링하고, `idle_in_transaction_session_timeout`을 설정하여 장시간 열린 트랜잭션을 자동 종료해야 한다. `pg_stat_user_tables`의 `n_dead_tup` 지표로 dead tuple 누적을 감시한다.

---

## Q3. PostgreSQL의 SSI(Serializable Snapshot Isolation)는 2PL과 어떻게 다른가?

### 왜 이 질문이 중요한가
Serializable 격리가 필요할 때, 2PL과 SSI 중 어느 구현을 선택하느냐에 따라 시스템 처리량이 수 배 차이날 수 있다. PostgreSQL을 쓴다면 SSI의 동작 방식을 이해해야 적절히 활용할 수 있다.

### 답변

**2PL의 동작 방식:**
- 읽기 시 Shared Lock, 쓰기 시 Exclusive Lock을 획득
- 트랜잭션 끝까지 모든 잠금 유지
- **Writers block Readers**: 다른 트랜잭션이 쓰고 있으면 읽기도 대기해야 한다
- 데드락 발생 가능 → 데드락 감지 후 하나를 중단

**SSI의 동작 방식:**
- Snapshot Isolation을 기반으로 동작 → **Readers never block Writers**
- 읽기 시 잠금 없이 진행하되, "이 트랜잭션이 무엇을 읽었는지"를 추적
- 커밋 시점에 직렬화 충돌(serialization conflict) 검사
- 충돌이 감지되면 트랜잭션을 중단하고 재시도를 요구

```
SSI 충돌 감지 예시:

T1: Read(doctors WHERE on_call = true) → {Alice, Bob}
T2: Read(doctors WHERE on_call = true) → {Alice, Bob}
T1: Update(Alice.on_call = false), COMMIT ← 성공

T2: Update(Bob.on_call = false), COMMIT 시도
    → SSI 감지: "T2가 읽은 데이터를 T1이 변경했다"
    → T2 ABORT → 재시도 필요
```

**성능 비교:**

| 측면 | 2PL | SSI |
|------|-----|-----|
| 읽기-쓰기 블로킹 | O (Writers block Readers) | X (MVCC 기반) |
| 데드락 | 발생 가능 | 발생 불가 |
| 충돌 시 비용 | 대기 (잠금 경합) | 중단 + 재시도 |
| 충돌이 적은 경우 | 잠금 오버헤드 있음 | 거의 SI와 동일한 성능 |
| 충돌이 많은 경우 | 대기 시간 증가 | 재시도 비용 증가 |

### 실무 적용
PostgreSQL에서 Serializable이 필요한 로직에는 반드시 재시도 로직을 구현해야 한다. SSI는 커밋 시점에 충돌을 감지하여 트랜잭션을 중단하므로, 애플리케이션이 `serialization_failure` 에러를 받으면 트랜잭션 전체를 재시도해야 한다. 충돌이 빈번한 핫스팟 데이터에서는 SSI의 재시도 비용이 커질 수 있으므로, SELECT FOR UPDATE로 비관적 잠금을 사용하는 것이 더 효율적일 수 있다.

---

## Q4. 분산 트랜잭션은 왜 피하라고 하는가? 대안은 무엇인가?

### 왜 이 질문이 중요한가
마이크로서비스 아키텍처에서 여러 서비스에 걸친 데이터 일관성은 핵심 과제다. 2PC의 한계를 이해하고, Saga 패턴 같은 대안을 알아야 현실적인 아키텍처를 설계할 수 있다.

### 답변

**2PC/XA의 문제점:**
1. **Coordinator가 Single Point of Failure**: Coordinator 장애 시 모든 Participant가 In-Doubt 상태에 빠진다
2. **잠금 유지**: In-Doubt 동안 해당 행의 잠금이 해제되지 않아 다른 트랜잭션을 차단한다
3. **성능**: 두 번의 네트워크 왕복(Prepare + Commit)이 필요하고, 모든 Participant의 응답을 기다려야 한다
4. **Lowest Common Denominator**: 참여하는 모든 시스템이 XA를 지원해야 하며, 각 시스템의 고유 최적화를 활용할 수 없다

**대안 1: Saga 패턴**
각 서비스의 로컬 트랜잭션을 순차적으로 실행하고, 실패 시 보상 트랜잭션(compensating transaction)을 역순으로 실행한다.

```
정상 흐름:
주문 생성 → 결제 처리 → 재고 차감 → 배송 요청

결제 실패 시:
주문 생성(완료) → 결제 처리(실패) → 주문 취소(보상)

재고 차감 실패 시:
주문 생성(완료) → 결제 처리(완료) → 재고 차감(실패)
→ 결제 환불(보상) → 주문 취소(보상)
```

Saga는 ACID를 보장하지 않으며 Eventual Consistency를 제공한다. 보상 트랜잭션의 설계가 복잡하고, 중간 상태가 외부에 노출될 수 있다.

**대안 2: Outbox 패턴**
서비스의 로컬 트랜잭션에서 데이터 변경과 이벤트 발행을 하나의 트랜잭션으로 묶는다. 이벤트를 별도 outbox 테이블에 저장하고, CDC(Change Data Capture)로 메시지 브로커에 전달한다.

```sql
BEGIN;
UPDATE orders SET status = 'confirmed' WHERE id = 123;
INSERT INTO outbox (event_type, payload) VALUES ('OrderConfirmed', '{"id": 123}');
COMMIT;
-- CDC(Debezium 등)가 outbox 테이블을 감시하여 Kafka로 전달
```

**대안 3: NewSQL (CockroachDB, TiDB, Spanner)**
단일 데이터베이스 내부에서 분산 트랜잭션을 처리하므로, 애플리케이션 입장에서는 단일 DB 트랜잭션과 동일하게 사용할 수 있다. 2PC의 Coordinator 문제를 내부적으로 해결한다.

### 실무 적용
마이크로서비스 간 데이터 일관성이 필요할 때, 첫 번째로 검토할 것은 "정말 분산 트랜잭션이 필요한가?"이다. 서비스 경계를 재설계하여 관련 데이터를 하나의 서비스로 모을 수 있다면 그것이 가장 단순한 해결책이다. 불가피하게 분산이 필요하면, Saga + Outbox 패턴이 현재 가장 널리 사용되는 접근법이다.

---

## Q5. SELECT FOR UPDATE는 언제 사용하고, 어떤 함정이 있는가?

### 왜 이 질문이 중요한가
SELECT FOR UPDATE는 동시성 문제를 해결하는 강력한 도구이지만, 잘못 사용하면 데드락이나 성능 저하의 원인이 된다. 올바른 사용 시점과 주의사항을 구체적으로 알아야 한다.

### 답변

**올바른 사용 시나리오:**
- Read-Modify-Write 패턴에서 원자적 연산으로 표현할 수 없는 복잡한 비즈니스 로직이 있을 때
- Write Skew를 방지해야 할 때 (조회된 행들을 잠가서 다른 트랜잭션이 수정하지 못하도록)

**함정 1: 데드락**
```sql
-- T1: SELECT * FROM accounts WHERE id = 'A' FOR UPDATE;
-- T2: SELECT * FROM accounts WHERE id = 'B' FOR UPDATE;
-- T1: SELECT * FROM accounts WHERE id = 'B' FOR UPDATE;  ← T2가 잠금 보유, 대기
-- T2: SELECT * FROM accounts WHERE id = 'A' FOR UPDATE;  ← T1이 잠금 보유, 데드락!
```
해결: 항상 같은 순서로 잠금을 획득한다 (예: ID 오름차순).

**함정 2: 잠금 범위 확대**
WHERE 절에 인덱스가 없으면 Full Table Scan이 발생하여, 조건에 맞지 않는 행까지 잠글 수 있다. 반드시 인덱스가 있는 컬럼으로 조건을 지정해야 한다.

**함정 3: 트랜잭션 길어짐**
FOR UPDATE 후 외부 API 호출이나 복잡한 로직을 수행하면, 잠금 보유 시간이 길어져 다른 트랜잭션이 대기하게 된다.

**대안: SKIP LOCKED와 NOWAIT**
```sql
-- NOWAIT: 잠금을 즉시 획득할 수 없으면 에러 반환
SELECT * FROM tasks WHERE status = 'pending' FOR UPDATE NOWAIT;

-- SKIP LOCKED: 이미 잠긴 행을 건너뛰고 다음 행 반환 (큐 패턴)
SELECT * FROM tasks WHERE status = 'pending' FOR UPDATE SKIP LOCKED LIMIT 1;
```

### 실무 적용
FOR UPDATE는 "필요한 행만, 짧은 시간만" 원칙으로 사용한다. 잠금 보유 중에는 외부 API 호출을 피하고, 비즈니스 로직을 최소화한다. 큐 패턴(작업 할당)에서는 SKIP LOCKED가 데드락 없이 동시 처리를 가능하게 하므로 적극 활용할 만하다.
