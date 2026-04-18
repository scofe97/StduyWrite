# Ch.06 - PostgreSQL 시작하기: 심화 탐구

> LEARN.md를 학습한 뒤, 더 깊이 파고들어야 할 질문들

---

## Q1. PostgreSQL과 MySQL의 아키텍처는 어떻게 다르며, 이 차이가 실무에 어떤 영향을 주는가?

### 왜 이 질문이 중요한가

백엔드 면접에서 "PostgreSQL과 MySQL의 차이"는 단골 질문이다. 단순히 기능 비교가 아니라 아키텍처 수준의 차이를 설명할 수 있어야 기술적 깊이를 보여줄 수 있다. 실무에서도 DB 선택 시 이 차이가 성능 특성과 운영 방식에 직접 영향을 미친다.

### 답변

두 데이터베이스의 근본적 차이는 **프로세스 모델**과 **MVCC 구현 방식**에 있다.

**프로세스 모델**:

```
PostgreSQL: 프로세스 기반 (Process-per-Connection)
┌──────────┐
│ Postmaster│ (메인 프로세스)
├──────────┤
│ Backend 1│ (클라이언트 1 전용 프로세스)
│ Backend 2│ (클라이언트 2 전용 프로세스)
│ Backend 3│ (클라이언트 3 전용 프로세스)
└──────────┘
- fork()로 프로세스 생성
- 프로세스 간 격리 우수 (한 연결 크래시가 다른 연결에 영향 적음)
- 연결 생성 오버헤드 큼 -> PgBouncer 필요

MySQL (InnoDB): 스레드 기반 (Thread-per-Connection)
┌──────────┐
│  mysqld   │ (단일 프로세스)
├──────────┤
│ Thread 1 │
│ Thread 2 │
│ Thread 3 │
└──────────┘
- 스레드 생성이 프로세스보다 가벼움
- 기본 연결 풀링 효율이 더 좋음
- 하지만 스레드 간 메모리 공유로 격리가 약함
```

**MVCC 구현**:

PostgreSQL은 UPDATE 시 새로운 행 버전(tuple)을 생성하고 이전 버전은 dead tuple로 남긴다. 이 방식은 읽기 성능이 우수하지만 VACUUM이 필수다.

MySQL InnoDB는 Undo Log에 이전 버전을 저장하고, 원본 행을 직접 수정(in-place update)한다. VACUUM이 필요 없지만, Undo Log가 커지면 성능이 저하될 수 있다.

| 측면 | PostgreSQL | MySQL (InnoDB) |
|------|-----------|----------------|
| UPDATE 방식 | 새 tuple 생성 | In-place + Undo Log |
| 정리 작업 | VACUUM 필요 | Purge Thread 자동 |
| Write Amplification | 높음 (전체 행 복사) | 낮음 |
| 읽기 일관성 | tuple 직접 참조 | Undo Log 참조 필요할 수 있음 |

**스토리지 엔진**: MySQL의 독특한 점은 스토리지 엔진이 교체 가능하다는 것이다(InnoDB, MyISAM 등). PostgreSQL은 단일 스토리지 엔진이지만 확장 시스템이 더 유연하다.

### 실무 적용

- UPDATE가 빈번한 워크로드에서는 PostgreSQL의 VACUUM 설정에 신경써야 한다
- 연결 수가 많은 환경에서는 PostgreSQL에 PgBouncer가 사실상 필수다
- 복잡한 쿼리(CTE, 윈도우 함수, JSONB)가 필요하면 PostgreSQL이 유리하다
- 단순 읽기/쓰기 위주이고 팀이 MySQL에 익숙하면 MySQL도 좋은 선택이다

---

## Q2. MVCC의 내부 동작과 xmin/xmax는 실제로 어떻게 작동하는가?

### 왜 이 질문이 중요한가

MVCC는 PostgreSQL의 동시성 제어 핵심이다. xmin/xmax를 이해하면 트랜잭션 격리 수준의 동작, VACUUM의 필요성, 그리고 long-running 트랜잭션이 왜 위험한지를 근본적으로 이해할 수 있다.

### 답변

모든 PostgreSQL 행(tuple)에는 숨겨진 시스템 컬럼이 있다.

```sql
-- 시스템 컬럼 직접 확인
SELECT xmin, xmax, ctid, * FROM users WHERE id = 1;
-- xmin: 100 (이 행을 생성한 트랜잭션 ID)
-- xmax: 0   (아직 삭제/수정되지 않음)
-- ctid: (0,1) (물리적 위치: 페이지 0, 오프셋 1)
```

**가시성 판단 규칙** (Visibility Check):

트랜잭션 T가 tuple을 볼 수 있는 조건:
1. `xmin`이 T 시작 전에 커밋됨 (생성된 것이 확인됨)
2. `xmax`가 없거나, T 시작 전에 커밋되지 않음 (삭제가 아직 보이지 않음)

```
시나리오: Transaction ID 200에서 조회

Tuple A: xmin=100(커밋됨), xmax=0       -> 보임 (생성 확인, 삭제 없음)
Tuple B: xmin=100(커밋됨), xmax=150(커밋됨) -> 안 보임 (삭제 확인됨)
Tuple C: xmin=250(미커밋),  xmax=0       -> 안 보임 (미래 트랜잭션)
Tuple D: xmin=100(커밋됨), xmax=300(미커밋) -> 보임 (삭제가 아직 미확정)
```

**Transaction ID Wraparound 문제**: PostgreSQL의 트랜잭션 ID는 32비트(약 42억)로 유한하다. ID가 순환하면 과거 데이터가 "미래"로 보이는 재앙이 발생할 수 있다. 이를 방지하기 위해 autovacuum은 오래된 행의 xmin을 "frozen" 상태로 변경한다. `autovacuum_freeze_max_age` 설정이 이를 관리한다.

**Long-running 트랜잭션이 위험한 이유**: 오래 실행되는 트랜잭션이 있으면, 그 트랜잭션 시작 시점 이후의 dead tuple을 VACUUM이 정리할 수 없다. 결과적으로 테이블이 비대해지고 성능이 저하된다. 이것이 프로덕션에서 idle-in-transaction 연결을 모니터링하고 타임아웃을 설정하는 이유다.

### 실무 적용

- `idle_in_transaction_session_timeout`을 설정하여 방치된 트랜잭션 자동 종료
- `autovacuum_freeze_max_age` 모니터링으로 wraparound 방지
- pg_stat_activity에서 `state = 'idle in transaction'`인 연결을 정기적으로 점검

---

## Q3. 커넥션 풀링 전략은 어떻게 결정하는가? PgBouncer vs Pgpool-II vs 애플리케이션 풀

### 왜 이 질문이 중요한가

PostgreSQL의 프로세스 기반 모델 때문에 커넥션 관리는 실무에서 반드시 다뤄야 하는 주제다. 마이크로서비스 아키텍처에서 서비스 수가 늘어나면 DB 연결 고갈이 발생할 수 있으며, 풀링 전략 선택이 시스템 안정성에 직접적으로 영향을 미친다.

### 답변

풀링에는 세 가지 레이어가 있다.

```
Layer 1: 애플리케이션 풀 (HikariCP, SQLAlchemy)
 - 각 애플리케이션 인스턴스 내부에서 연결 재사용
 - 장점: 별도 인프라 불필요
 - 한계: 서비스 수 x 인스턴스 수 x 풀 크기 = 총 연결 수 폭발

Layer 2: 프록시 풀 (PgBouncer, Odyssey)
 - DB 앞단에서 여러 앱의 연결을 집계
 - 장점: 총 DB 연결 수를 제어 가능
 - 한계: 추가 인프라, 네트워크 홉

Layer 3: DB 내장 (PostgreSQL 15+ 옵션 검토 중)
 - 아직 본격적인 내장 풀링은 없음
```

**PgBouncer vs Pgpool-II**:

| 항목 | PgBouncer | Pgpool-II |
|------|-----------|-----------|
| 경량성 | 단일 프로세스, 메모리 2-3MB | 다기능, 무거움 |
| 기능 | 풀링 전용 | 풀링 + 로드밸런싱 + 복제 + 쿼리 캐시 |
| 풀링 모드 | Session/Transaction/Statement | Session 기반 |
| 적합 | 순수 풀링만 필요할 때 | HA + 풀링 통합 필요 시 |

**Transaction 모드에서의 제약과 우회**:

PgBouncer의 Transaction 모드는 Prepared Statement를 지원하지 않는다. Java/Spring 환경에서 이 문제를 만나면 다음 중 하나를 선택한다:
1. Session 모드로 전환 (풀링 효율 감소)
2. `prepareThreshold=0` 설정으로 Prepared Statement 비활성화
3. PgBouncer 1.21+의 `prepared_statement_mode` 옵션 활용

### 실무 적용

- 단일 애플리케이션: 애플리케이션 풀만으로 충분
- 마이크로서비스 3-5개: PgBouncer Transaction 모드 도입
- 10개 이상 서비스 + HA: PgBouncer + 로드밸런서 조합 검토
- `max_connections`는 PgBouncer 뒤에서 50-100 수준으로 유지하는 것이 일반적

---

## Q4. PostgreSQL의 데이터 타입 선택은 성능에 얼마나 영향을 미치는가?

### 왜 이 질문이 중요한가

테이블 설계 시 데이터 타입 선택은 저장 공간, 인덱스 크기, 쿼리 성능에 모두 영향을 준다. 잘못된 타입 선택은 나중에 마이그레이션으로 수정해야 하므로, 초기 설계 단계에서 올바른 결정을 내리는 것이 중요하다.

### 답변

**정수 타입 비교**:

| 타입 | 크기 | 범위 | 용도 |
|------|------|------|------|
| SMALLINT | 2바이트 | -32K ~ 32K | 상태 코드, 작은 열거 |
| INTEGER | 4바이트 | -21억 ~ 21억 | 일반 ID, 수량 |
| BIGINT | 8바이트 | -9경 ~ 9경 | 대형 테이블 ID |

SERIAL/BIGSERIAL은 자동 증가 시퀀스를 만드는 편의 기능이다. PostgreSQL 10+에서는 SQL 표준인 `GENERATED ALWAYS AS IDENTITY`가 권장된다.

**UUID vs BIGSERIAL**:

```sql
-- BIGSERIAL: 순차적, 4-8바이트, B-tree 친화적
id BIGSERIAL PRIMARY KEY

-- UUID: 128비트(16바이트), 분산 환경 적합
id UUID PRIMARY KEY DEFAULT gen_random_uuid()
```

UUID는 인덱스 크기가 BIGINT 대비 2배이고, 랜덤 값이라 B-tree 삽입 시 페이지 분할이 빈번하다. 그러나 분산 시스템에서 ID 충돌 없이 독립적으로 생성할 수 있다는 장점이 크다. UUID v7(시간 기반 정렬)은 순차성을 일부 보장하여 인덱스 성능 문제를 완화한다.

**TEXT vs VARCHAR(n)**:

PostgreSQL에서 `TEXT`와 `VARCHAR(n)`은 내부적으로 동일한 저장 방식을 사용한다. `VARCHAR(n)`의 길이 제한은 CHECK 제약조건과 동일하게 동작한다. PostgreSQL 공식 문서에서도 `TEXT`를 사용하고 필요 시 CHECK로 길이를 제한하는 방식을 권장한다.

**NUMERIC vs FLOAT**:

금액 계산에는 반드시 `NUMERIC`(정확한 소수)을 사용해야 한다. `FLOAT`/`DOUBLE PRECISION`은 부동소수점이므로 금융 계산에서 오차가 발생한다.

### 실무 적용

- PK: 단일 서버이면 BIGSERIAL, 분산 환경이면 UUID v7
- 금액: NUMERIC(precision, scale), FLOAT 사용 금지
- 문자열: TEXT 기본, 길이 제한 필요 시 CHECK 제약조건
- 날짜: TIMESTAMPTZ(타임존 포함)를 기본으로, TIMESTAMP(without tz)는 피함
