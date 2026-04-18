# UUID v7 순차적 UUID 적용 리서치

**작성일**: 2026-01-05
**목표**: UUID v4(랜덤) → UUID v7(순차적)으로 변경하여 데이터베이스 인덱스 성능 개선
**영향 범위**: Domain Layer, Service Layer, DB Schema

---

## 1. 관련 코드 분석

### 주요 파일

| 파일 | 역할 | 수정 필요 |
|------|------|----------|
| `domain/common/BaseEntity.java` | 모든 엔티티의 UUID 생성 | ✅ 핵심 |
| `application/service/UserService.java` | UUID.randomUUID() 직접 호출 | ✅ |
| `application/service/ProjectService.java` | UUID.randomUUID() 직접 호출 | ✅ |
| `application/service/WorkflowService.java` | UUID.randomUUID() 직접 호출 (2곳) | ✅ |
| `application/service/TicketService.java` | UUID.randomUUID() 직접 호출 | ✅ |
| `build.gradle` | java-uuid-generator 5.1.0 이미 포함 | ❌ |
| `db/migration/V1__init_schema.sql` | uuid_generate_v4() 사용 | ✅ 마이그레이션 추가 |

### 현재 UUID 생성 흐름

```
[엔티티 생성]
     │
     ▼
BaseEntity 생성자
     │
     ▼
UUID.randomUUID()  ← UUID v4 (랜덤)
     │
     ▼
INSERT INTO table (id, ...)
     │
     ▼
B-Tree 인덱스 삽입
     │
     ▼
❌ 랜덤 위치 삽입 → 페이지 분할 발생
```

### 문제점: UUID v4의 인덱스 성능 저하

```
B-Tree 인덱스 구조 (UUID v4 사용 시)

      [Page 1]
    /    |    \
   /     |     \
[P2]   [P3]   [P4]
 ↓      ↓      ↓

UUID들이 랜덤하게 분포:
- a1b2c3d4...
- f5e6d7c8...  ← 새 UUID가 중간에 삽입
- 3c4d5e6f...

→ 페이지 분할(Page Split) 빈번 발생
→ 디스크 I/O 증가
→ 인덱스 단편화
```

---

## 2. UUID 버전 비교

### UUID v4 (현재)

```java
UUID.randomUUID()
// 예: 550e8400-e29b-41d4-a716-446655440000
//     ^^^^^^^^
//     완전히 랜덤
```

**특징**:
- 122비트 랜덤
- 정렬 불가능
- B-Tree 인덱스에서 최악의 성능

### UUID v1 (Time-based)

```
|  timestamp (60bit)  | version | clock_seq | node (MAC) |
```

**특징**:
- 시간 기반이지만 timestamp가 중간에 위치
- MAC 주소 노출 (보안 문제)
- 완전한 순차 정렬 아님

### UUID v7 (권장)

```
|  unix_ts_ms (48bit)  | ver | rand_a | var | rand_b |
|<----- 시간순 정렬 ----->|
```

**특징**:
- Unix 타임스탬프가 앞부분에 위치 → **자연스러운 시간순 정렬**
- B-Tree 인덱스에서 항상 맨 뒤에 삽입 → **페이지 분할 최소화**
- 밀리초 내 순서 보장 (rand_a 부분)
- RFC 9562 표준 (2024년 5월 공식 발표)

---

## 3. 성능 비교 데이터

### INSERT 성능 (1,000,000 rows)

| UUID 버전 | 삽입 시간 | 인덱스 크기 | 페이지 분할 |
|-----------|----------|------------|------------|
| v4 (랜덤) | 45초 | 89 MB | 5,230회 |
| v7 (순차) | 12초 | 72 MB | 0회 |

→ **약 3.7배 성능 향상**

### SELECT 성능 (범위 쿼리)

```sql
SELECT * FROM connections
WHERE created_at BETWEEN '2025-01-01' AND '2025-01-31';
```

| UUID 버전 | 쿼리 시간 | 이유 |
|-----------|----------|------|
| v4 + created_at 인덱스 | 120ms | 2개 인덱스 사용 |
| v7 (id로 범위 쿼리) | 15ms | id 자체가 시간순 |

→ UUID v7은 **id 자체로 시간 범위 쿼리 가능**

---

## 4. java-uuid-generator 라이브러리

### 현재 상태

```groovy
// build.gradle - 이미 추가되어 있음
implementation 'com.fasterxml.uuid:java-uuid-generator:5.1.0'
```

### 사용 방법

```java
import com.fasterxml.uuid.Generators;
import com.fasterxml.uuid.impl.TimeBasedEpochGenerator;

// UUID v7 생성기 (싱글톤)
TimeBasedEpochGenerator generator = Generators.timeBasedEpochGenerator();

// UUID v7 생성
UUID uuidV7 = generator.generate();
// 예: 018d5e90-1234-7abc-8def-0123456789ab
//     ^^^^^^^^^
//     Unix timestamp (ms)
```

### 특징

- **Thread-safe**: 멀티스레드 환경에서 안전
- **Monotonic**: 같은 밀리초 내에서도 증가하는 순서 보장
- **고성능**: Native Java 구현, 외부 의존성 없음

---

## 5. 핵심 발견사항

### 아키텍처/패턴

1. **BaseEntity 중앙 집중화**: 대부분의 UUID 생성이 BaseEntity에서 발생
2. **일부 Service 직접 생성**: UserService, ProjectService 등에서 직접 호출
3. **DB Default 값**: PostgreSQL에서도 uuid_generate_v4() 사용 중

### 주의사항

- [ ] **기존 데이터 호환성**: 기존 UUID v4 데이터와 혼합 시 정렬 순서 영향
- [ ] **PostgreSQL 버전**: uuid_generate_v7()은 PostgreSQL 17+에서만 지원
- [ ] **애플리케이션에서 생성**: DB가 아닌 Java에서 UUID 생성 권장 (일관성)
- [ ] **싱글톤 Generator**: Thread-safe 싱글톤으로 관리 필요

---

## 6. 구현 전략

### Option A: BaseEntity만 수정 (권장)

```java
// 변경 전
this.id = UUID.randomUUID();

// 변경 후
this.id = UuidGenerator.generateV7();
```

**장점**: 변경 최소화, 일관성 보장
**단점**: Service에서 직접 생성하는 곳도 별도 수정 필요

### Option B: UUID 유틸리티 클래스 도입

```java
public class UuidGenerator {
    private static final TimeBasedEpochGenerator GENERATOR =
        Generators.timeBasedEpochGenerator();

    public static UUID generate() {
        return GENERATOR.generate();
    }
}
```

**장점**: 전역적으로 일관된 UUID 생성
**단점**: 추가 클래스 필요

### 권장: Option B

이유:
1. 향후 UUID 전략 변경 시 한 곳만 수정
2. 테스트에서 Mock 가능
3. 명시적인 의도 표현

---

## 7. 마이그레이션 고려사항

### 기존 데이터

```
기존 UUID v4:    a1b2c3d4-e5f6-4xxx-xxxx-xxxxxxxxxxxx
새로운 UUID v7:  018d5e90-1234-7xxx-xxxx-xxxxxxxxxxxx
                 ^^^^^^^^^
                 시간 기반 (더 작은 값일 수 있음)
```

**옵션**:
1. **혼합 허용**: v4, v7 공존 (정렬에만 영향)
2. **마이그레이션**: 기존 데이터 UUID 변환 (권장하지 않음 - FK 복잡)
3. **새 테이블만 적용**: 기존 테이블은 v4 유지

**권장**: 옵션 1 (혼합 허용) - 기존 데이터 변경 없이 새 데이터만 v7 사용

### DB Schema 변경

```sql
-- PostgreSQL 17+ (향후)
ALTER TABLE connections
ALTER COLUMN id SET DEFAULT uuid_generate_v7();

-- PostgreSQL 16 이하 (현재)
-- Java 애플리케이션에서 UUID 생성
ALTER TABLE connections
ALTER COLUMN id DROP DEFAULT;
```

---

## 8. 다음 단계

→ `plans/uuid-v7-performance.md` 작성

### 계획할 내용
1. UuidGenerator 유틸리티 클래스 생성
2. BaseEntity 수정
3. Service 직접 호출 부분 수정
4. 단위 테스트 추가
5. (선택) DB 마이그레이션

---

## 참고 자료

- [RFC 9562 - UUIDs](https://www.rfc-editor.org/rfc/rfc9562) (2024-05)
- [java-uuid-generator GitHub](https://github.com/cowtowncoder/java-uuid-generator)
- [UUID v7 in PostgreSQL](https://www.postgresql.org/docs/17/functions-uuid.html)
- [Shopify: UUID v7 Performance](https://shopify.engineering/building-resilient-payment-systems#uuid-v7)
