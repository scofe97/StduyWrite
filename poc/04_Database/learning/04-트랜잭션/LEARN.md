# Ch.04 - 트랜잭션

> **이론 매핑**: `docs/04_Database/01_기본개념/04_트랜잭션.md`

---

## 핵심 요약
> 트랜잭션은 여러 읽기/쓰기 작업을 하나의 논리적 단위로 묶어, 전체가 성공하거나 전체가 실패하도록 보장하는 추상화다. 동시에 여러 사용자가 같은 데이터에 접근할 때 발생하는 경쟁 조건(race condition)을 방지하기 위해 격리 수준이라는 개념이 존재하며, 각 격리 수준은 성능과 정확성 사이의 트레이드오프를 표현한다. 분산 환경에서는 2PC(Two-Phase Commit) 프로토콜이 원자성을 보장하지만, 가용성과 성능에 대가를 치러야 한다.

---

## 학습 목표
1. ACID의 각 속성이 무엇을 보장하는지 정확히 설명할 수 있다
2. Dirty Read, Lost Update, Write Skew, Phantom 등 경쟁 조건을 구분할 수 있다
3. Read Committed, Snapshot Isolation, Serializable 격리 수준의 차이를 설명할 수 있다
4. MVCC(다중 버전 동시성 제어)의 동작 원리를 이해할 수 있다
5. Serializable 격리의 세 가지 구현 방식을 비교할 수 있다
6. 2PC(Two-Phase Commit)의 동작 원리와 한계를 설명할 수 있다

---

## 본문

### 1. 트랜잭션의 기본 개념

트랜잭션은 "All or Nothing" 보장을 제공한다. 송금 시 A 계좌에서 출금하고 B 계좌에 입금하는 두 작업은 반드시 함께 성공하거나 함께 실패해야 한다. 출금만 성공하고 입금이 실패하면 돈이 사라진 것처럼 보인다.

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 'A';
UPDATE accounts SET balance = balance + 100 WHERE id = 'B';
COMMIT;  -- 두 UPDATE가 모두 성공해야 반영됨
-- 도중에 오류 발생 시 ROLLBACK → 첫 번째 UPDATE도 취소
```

트랜잭션이 없다면, 애플리케이션 코드에서 모든 실패 시나리오를 직접 처리해야 한다. 네트워크 장애, 디스크 꽉 참, 동시 쓰기 충돌 등 수십 가지 예외 상황을 일일이 코드로 대응하는 것은 현실적으로 불가능에 가깝다. 트랜잭션이 이 복잡성을 추상화해준다.

---

### 2. ACID 속성

ACID는 트랜잭션이 보장하는 네 가지 속성의 약자다. 하지만 각 속성의 실제 의미는 이름에서 직관적으로 유추되는 것과 다른 부분이 있다.

**Atomicity (원자성)**: "All or Nothing"이다. 트랜잭션 도중 오류가 발생하면 이미 수행된 모든 변경을 롤백한다. 주의할 점은 원자성이 동시성(concurrency)과는 무관하다는 것이다. 동시성 제어는 Isolation의 영역이다.

**Consistency (일관성)**: 애플리케이션의 불변식(invariant)이 트랜잭션 전후에 유지되어야 한다. 예를 들어 "모든 계좌 잔액의 합은 일정해야 한다"는 규칙이다. 이 속성은 데이터베이스 혼자서 보장할 수 없고, 애플리케이션이 올바른 트랜잭션을 작성해야 달성된다.

**Isolation (격리성)**: 동시에 실행되는 트랜잭션 간에 서로 간섭하지 않는다. 이상적으로는 직렬 실행(Serializability)과 같은 결과를 보장하지만, 성능을 위해 다양한 격리 수준을 제공한다.

**Durability (지속성)**: 커밋된 데이터는 하드웨어 장애가 발생해도 유실되지 않는다. fsync, WAL, 복제 등으로 구현한다. 다만 디스크 전체가 손상되거나 모든 복제본이 동시에 소실되면 완벽한 지속성은 보장할 수 없다.

#### "Consistency"라는 단어의 함정

데이터베이스 분야에서 "Consistency"는 맥락에 따라 다른 의미를 가진다:

| 맥락 | 의미 |
|------|------|
| ACID의 C | 애플리케이션 불변식 유지 |
| 복제(Replication) | 복제본 간 데이터 동기화 (Eventually Consistent) |
| CAP 정리 | Linearizability (모든 노드가 같은 값을 보는 것) |
| Consistent Hashing | 샤딩을 위한 해시 알고리즘 |

면접이나 기술 토론에서 "Consistency"를 언급할 때는 어떤 맥락인지 명확히 해야 혼동을 피할 수 있다.

---

### 3. 경쟁 조건(Race Condition) 유형

동시에 여러 트랜잭션이 같은 데이터에 접근할 때 발생하는 문제들이다.

**Dirty Read**: 커밋되지 않은 데이터를 다른 트랜잭션이 읽는 현상이다. T1이 값을 3으로 변경했지만 아직 커밋하지 않은 상태에서, T2가 이 값 3을 읽었다가 T1이 롤백하면 T2는 존재하지 않았던 값을 사용하게 된다.

**Lost Update**: 두 트랜잭션이 동시에 같은 값을 읽고 수정할 때, 하나의 수정이 다른 수정을 덮어쓰는 현상이다. 카운터를 42에서 43으로 올리는 두 트랜잭션이 동시에 실행되면, 결과가 44가 아닌 43이 될 수 있다.

**Write Skew**: 두 트랜잭션이 같은 조건을 검사한 뒤 각각 다른 행을 수정하는 현상이다. 대표적인 예가 병원 당직 의사 스케줄이다. 최소 1명이 당직이어야 하는데, 현재 2명이 당직이다. 두 의사가 동시에 "2명이니 내가 빠져도 된다"고 판단하여 각각 퇴근하면, 당직 의사가 0명이 된다.

**Phantom**: 한 트랜잭션이 검색 조건에 맞는 행이 없음을 확인하고 새 행을 삽입하는 사이에, 다른 트랜잭션도 같은 작업을 수행하는 현상이다. 회의실 예약에서 같은 시간대에 두 예약이 동시에 들어가는 사례다.

```
Write Skew 예시:
T1: SELECT COUNT(*) FROM doctors WHERE on_call = true → 2명
    → "나 빠져도 됨" → UPDATE SET on_call = false WHERE name = 'Alice'

T2: SELECT COUNT(*) FROM doctors WHERE on_call = true → 2명
    → "나도 빠져도 됨" → UPDATE SET on_call = false WHERE name = 'Bob'

결과: on_call = 0명 (최소 1명이어야 하는 불변식 위반)
```

---

### 4. 격리 수준 (Isolation Levels)

각 격리 수준은 어떤 경쟁 조건을 방지하는지가 다르다.

| 격리 수준 | Dirty Read | Read Skew | Lost Update | Write Skew | Phantom |
|-----------|------------|-----------|-------------|------------|---------|
| Read Committed | 방지 | 가능 | 가능 | 가능 | 가능 |
| Snapshot Isolation | 방지 | 방지 | DB마다 다름 | 가능 | 방지 |
| Serializable | 방지 | 방지 | 방지 | 방지 | 방지 |

**Read Committed**는 대부분의 DB(PostgreSQL, Oracle, SQL Server)의 기본 격리 수준이다. 커밋된 데이터만 읽을 수 있으므로 Dirty Read를 방지하지만, 같은 트랜잭션 내에서 다른 시점의 데이터를 읽을 수 있다(Read Skew).

**Snapshot Isolation**은 트랜잭션 시작 시점의 일관된 스냅샷을 본다. 같은 트랜잭션 내에서 반복 읽기가 항상 같은 결과를 반환한다. PostgreSQL에서는 "Repeatable Read"라는 이름으로 제공되지만, SQL 표준의 Repeatable Read보다 강력하다.

주의할 점은 데이터베이스별로 같은 이름이 다른 구현을 의미한다는 것이다:

| DB | "Repeatable Read" 실제 구현 |
|----|-----------------------------|
| PostgreSQL | Snapshot Isolation |
| MySQL/InnoDB | 약한 MVCC (SI보다 약함) |
| Oracle | "Serializable"라고 부르지만 실제로는 SI |

---

### 5. MVCC (Multi-Version Concurrency Control)

MVCC는 하나의 데이터에 대해 여러 버전을 유지하여, 읽기와 쓰기가 서로 블로킹하지 않도록 하는 기법이다. PostgreSQL의 핵심 동시성 제어 메커니즘이다.

핵심 원칙: **Readers never block Writers, Writers never block Readers.** 동일한 행을 동시에 수정하려는 경우에만 블로킹이 발생한다.

각 행에는 생성 트랜잭션 ID(xmin)와 삭제 트랜잭션 ID(xmax)가 기록된다. 트랜잭션은 자신의 시작 시점에 커밋된 버전만 볼 수 있다. 이를 통해 각 트랜잭션이 마치 자기만의 데이터베이스 스냅샷에서 작업하는 것처럼 동작한다.

---

### 6. Lost Update 방지 기법

Lost Update는 Read-Modify-Write 사이클에서 발생한다. 방지 기법은 네 가지다.

**1. 원자적 연산 (Atomic Operation)**
```sql
UPDATE counters SET value = value + 1 WHERE key = 'foo';
```
Read-Modify-Write를 DB 내부에서 원자적으로 수행한다. 가장 단순하고 효율적이다.

**2. 명시적 잠금 (SELECT FOR UPDATE)**
```sql
SELECT * FROM figures WHERE id = 1234 FOR UPDATE;
-- 비즈니스 로직 수행 (애플리케이션 코드)
UPDATE figures SET position = 'c4' WHERE id = 1234;
COMMIT;
```
조회 시 해당 행에 잠금을 걸어 다른 트랜잭션의 수정을 차단한다.

**3. 자동 감지 (Automatic Detection)**
PostgreSQL과 Oracle은 Snapshot Isolation에서 Lost Update를 자동으로 감지하고, 충돌 시 트랜잭션을 중단한다. 애플리케이션은 재시도 로직만 구현하면 된다. 주의: MySQL/InnoDB는 이 자동 감지를 지원하지 않는다.

**4. Compare-and-Set**
```sql
UPDATE wiki SET content = 'new' WHERE id = 1234 AND content = 'old';
-- 0 rows affected → 다른 누군가가 이미 수정함 → 재시도
```
현재 값이 읽었을 때의 값과 같을 때만 수정하는 조건부 쓰기다.

---

### 7. Serializable 격리 구현

모든 경쟁 조건을 방지하는 Serializable 격리는 세 가지 방식으로 구현할 수 있다.

**Actual Serial Execution (VoltDB, Redis)**
모든 트랜잭션을 단일 스레드에서 순차 실행한다. 구현이 단순하고 동시성 문제가 원천 차단되지만, 단일 코어에 병목이 생기므로 트랜잭션이 짧고 인메모리에서 완료되어야 한다.

**Two-Phase Locking - 2PL (MySQL, SQL Server)**
읽기에는 Shared Lock, 쓰기에는 Exclusive Lock을 걸고, 트랜잭션이 끝날 때까지 모든 잠금을 유지한다. Writers block Readers이므로 MVCC보다 동시성이 떨어지고, 데드락(deadlock)이 발생할 수 있다.

**Serializable Snapshot Isolation - SSI (PostgreSQL)**
"일단 진행하고, 커밋 시 충돌을 검사"하는 낙관적(optimistic) 접근이다. Snapshot Isolation 위에 직렬화 충돌 감지 로직을 추가한 것이다.

| 기법 | 처리량 | 지연 시간 | 확장성 |
|------|--------|-----------|--------|
| Serial Execution | 낮음 | 낮음 | 샤딩 필요 |
| 2PL | 중간 | 높음 | 제한적 |
| SSI | 높음 | 낮음 | 좋음 |

SSI는 Readers never block Writers를 유지하면서 Serializable을 달성하므로, 2PL보다 처리량이 높다. PostgreSQL에서 `SET TRANSACTION ISOLATION LEVEL SERIALIZABLE`로 사용할 수 있다.

---

### 8. 분산 트랜잭션: Two-Phase Commit (2PC)

여러 데이터베이스나 서비스에 걸친 트랜잭션을 원자적으로 처리하기 위한 프로토콜이다. 이름은 비슷하지만 2PL(Two-Phase Locking)과는 완전히 다른 개념이다.

```
Coordinator           Participant A       Participant B
    │                     │                    │
    │── Prepare ────────→ │                    │
    │── Prepare ──────────────────────────→    │
    │← Yes ───────────── │                    │
    │← Yes ────────────────────────────── │
    │ [Commit Point: WAL에 결정 기록]          │
    │── Commit ──────────→│                    │
    │── Commit ────────────────────────────→   │
```

Phase 1 (Prepare): Coordinator가 모든 Participant에게 "커밋할 수 있나?"를 묻는다. 각 Participant는 커밋 가능하면 Yes, 불가능하면 No를 응답한다.

Phase 2 (Commit/Abort): 모든 Participant가 Yes라면 Coordinator가 WAL에 "Commit" 결정을 기록한 뒤 모든 Participant에게 커밋을 지시한다. 하나라도 No면 전체를 Abort한다.

**핵심 문제: Coordinator 장애**
Coordinator가 Phase 1 후, Phase 2 전에 장애가 발생하면 Participant는 커밋할지 롤백할지 알 수 없는 In-Doubt 상태에 빠진다. 이 동안 잠금이 유지되어 다른 트랜잭션을 차단하고, Coordinator가 복구될 때까지 기다려야 한다. 이것이 2PC의 가장 큰 약점이다.

대안으로 CockroachDB, TiDB, Spanner 같은 NewSQL 데이터베이스는 단일 DB 내부에서 분산 트랜잭션을 처리하여 2PC의 한계를 우회한다.

---

## 핵심 정리
| 개념 | 한 줄 요약 |
|------|-----------|
| ACID | 원자성(장애 복구), 일관성(앱 책임), 격리성(동시성 제어), 지속성(영구 저장) |
| Dirty Read | 커밋되지 않은 데이터를 읽는 현상, Read Committed로 방지한다 |
| Lost Update | 동시 수정으로 하나의 업데이트가 유실, 원자적 연산이나 FOR UPDATE로 방지한다 |
| Write Skew | 읽기 결과에 기반한 쓰기가 충돌, Serializable 격리로만 완전히 방지한다 |
| MVCC | 다중 버전을 유지하여 읽기와 쓰기가 서로 블로킹하지 않도록 하는 기법이다 |
| SSI | 낙관적 동시성 제어로, Snapshot Isolation 위에 직렬화 충돌을 감지한다 |
| 2PC | 분산 트랜잭션의 원자성을 보장하지만, Coordinator 장애 시 In-Doubt 문제가 있다 |
