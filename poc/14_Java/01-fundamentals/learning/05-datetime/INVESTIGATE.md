# 날짜와 시간: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. LocalDateTime vs ZonedDateTime, DB 저장 시 어떤 전략이 맞는가?

### 왜 이 질문이 중요한가
글로벌 서비스나 멀티 타임존 환경에서 날짜 전략을 잘못 선택하면 데이터 불일치나 시간대 혼란이 발생한다. "그냥 UTC로 저장하면 되지"라는 단순한 답변은 실무의 복잡성을 반영하지 못한다. 면접에서는 각 타입의 의미와 DB 컬럼 타입과의 매핑 전략까지 묻는다.

### 답변

`LocalDateTime`은 타임존 정보가 없는 날짜-시간이다. "2024-03-15T10:30:00"은 어느 시간대의 10시 30분인지 알 수 없다. 단일 타임존만 사용하는 서비스(예: 한국 전용 서비스)에서 "서울 시간 기준의 약속 시간"처럼 타임존이 항상 고정인 데이터에 적합하다.

`ZonedDateTime`은 타임존 정보를 포함한다. "2024-03-15T10:30:00+09:00[Asia/Seoul]"처럼 어느 시간대인지 명확하다. 글로벌 사용자가 있거나 타임존이 다양한 이벤트를 다룰 때 필수다.

DB 저장 전략은 세 가지 접근이 있다. 첫 번째는 UTC `TIMESTAMP`에 저장하는 방식이다. 가장 보편적인 접근으로, 모든 시간을 UTC로 변환해서 저장하고 읽을 때 사용자 타임존으로 변환한다. 비교와 정렬이 단순하고 서머타임 혼란이 없다.

```java
// Spring JPA + UTC 전략
@Column(name = "created_at")
private Instant createdAt; // Instant는 항상 UTC — DB의 TIMESTAMP(UTC)에 매핑

// 또는 ZonedDateTime을 UTC로 저장
@Column(name = "event_time")
private ZonedDateTime eventTime; // JPA가 UTC로 변환해서 저장
```

두 번째는 타임존 정보를 별도 컬럼에 저장하는 방식이다. "사용자가 설정한 시간"을 그대로 유지해야 할 때 사용한다. 예를 들어 "뉴욕 기준 오전 9시에 알림"이라는 설정은 UTC로 변환하면 서머타임 전환 시 의미가 달라진다.

```sql
-- 타임존 보존 전략
CREATE TABLE schedules (
    scheduled_local TIMESTAMP,           -- 로컬 날짜시간
    timezone        VARCHAR(50)          -- 'America/New_York'
);
```

세 번째는 `TIMESTAMP WITH TIME ZONE` (PostgreSQL, Oracle)을 사용하는 방식이다. DB가 타임존 정보를 관리한다. 실무 권장 전략: 단일 타임존 서비스는 `LocalDateTime` + DB `DATETIME`, 멀티 타임존 서비스는 `Instant`(UTC) + DB `TIMESTAMP`로 저장하고 애플리케이션 계층에서 변환을 담당한다.

---

## Q2. 서머타임과 시간대 변환 함정

### 왜 이 질문이 중요한가
서머타임(DST)은 한국에 없어서 간과하기 쉽지만, 미국·유럽 사용자가 있는 서비스라면 반드시 고려해야 한다. DST 전환 시점에는 특정 시간이 두 번 존재하거나 아예 존재하지 않는 이상 상황이 발생하며, 이를 코드에서 처리하지 않으면 조용히 잘못된 값을 반환한다.

### 답변

서머타임이 적용되는 지역에서 시계를 앞으로 돌리는 날(예: 미국 봄철)에는 특정 한 시간이 건너뛰어진다. `America/New_York` 기준으로 2024년 3월 10일 02:00가 되는 순간 시계가 03:00로 바뀐다. 이 시간대에서 `ZonedDateTime.of(LocalDate.of(2024, 3, 10), LocalTime.of(2, 30), ZoneId.of("America/New_York"))`를 호출하면 존재하지 않는 시간이다. Java는 이를 자동으로 03:30으로 조정하는데, 이 동작을 모르면 혼란스러운 결과를 만난다.

반대로 시계를 뒤로 돌리는 날(가을철)에는 같은 로컬 시간이 두 번 존재한다. 02:30이 한 번은 EDT(-4), 한 번은 EST(-5) 기준으로 나타나 총 두 번 발생한다.

```java
// 함정 1: 존재하지 않는 시간
ZonedDateTime nonExistent = ZonedDateTime.of(
    LocalDateTime.of(2024, 3, 10, 2, 30),
    ZoneId.of("America/New_York")
);
// 자동으로 03:30 EDT로 조정됨 — 조용한 버그 가능성

// 함정 2: 모호한 시간 (두 번 존재)
// 명시적으로 DST 적용 여부를 지정하려면:
ZonedDateTime beforeTransition = ZonedDateTime.ofLocal(
    LocalDateTime.of(2024, 11, 3, 1, 30),
    ZoneId.of("America/New_York"),
    ZoneOffset.of("-04:00")  // EDT
);
ZonedDateTime afterTransition = ZonedDateTime.ofLocal(
    LocalDateTime.of(2024, 11, 3, 1, 30),
    ZoneId.of("America/New_York"),
    ZoneOffset.of("-05:00")  // EST
);
```

실무 대응 전략은 두 가지다. 첫째, 내부 처리는 항상 `Instant`(UTC 에포크)로 한다. `Instant`는 타임존이 없으므로 DST 전환의 영향을 받지 않는다. 사용자에게 표시할 때만 해당 타임존으로 변환한다. 둘째, 타임존 데이터베이스(TZDB)를 최신 상태로 유지한다. 각국 정부가 서머타임 규칙을 임의로 바꾸기 때문에 JDK와 OS의 시간대 데이터를 정기적으로 업데이트해야 한다. `java.time.zone.ZoneRulesProvider`가 TZDB를 참조하므로 JDK 버전 업데이트만으로도 최신 규칙이 적용된다.
