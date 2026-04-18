# 날짜와 시간 API

---

> Java 8 이전의 `Date`와 `Calendar`는 설계 결함으로 인해 실무에서 버그의 온상이었다. Java 8이 도입한 `java.time` 패키지는 불변성과 명확한 책임 분리를 기반으로 이 문제를 근본적으로 해결한다.

## 레거시 API의 문제점

`java.util.Date`와 `java.util.Calendar`는 Java 초창기부터 존재했지만, 설계상 결함이 누적되어 현재는 사용을 권장하지 않는다.

**가변성(mutability)**이 가장 큰 문제다. `Date` 객체는 `setTime()` 메서드로 내부 상태를 변경할 수 있어, 객체를 외부로 전달하면 호출자가 의도치 않게 값을 바꿀 수 있다. 방어적 복사를 항상 수행해야 한다는 부담이 생긴다.

스레드 안전성(thread safety) 문제도 심각하다. `SimpleDateFormat`은 내부 상태를 공유하기 때문에 멀티스레드 환경에서 `static` 필드로 선언하면 날짜 파싱 결과가 뒤섞이는 버그가 발생한다. 이 버그는 부하가 낮을 때는 숨어 있다가 동시 요청이 많아질 때 불규칙적으로 나타나 추적이 어렵다.

`Calendar`의 월(month) 표현도 혼란스럽다. 1월이 `0`이고 12월이 `11`이므로, 상수 없이 숫자를 직접 사용하면 off-by-one 오류가 빈번하게 발생한다.

## java.time 패키지 핵심 클래스

Java 8이 도입한 `java.time` 패키지는 Joda-Time 라이브러리의 설계를 표준으로 수용한 것이다. 모든 클래스는 **불변(immutable)**이며, 변경 메서드는 새 객체를 반환한다.

레거시 API와 `java.time`의 주요 클래스 대응은 다음과 같다:

| 용도 | 레거시 | java.time | 핵심 차이 |
|------|--------|-----------|----------|
| 날짜만 | `Calendar` | `LocalDate` | 시간대 없음, 불변 |
| 시간만 | `Calendar` | `LocalTime` | 시간대 없음, 불변 |
| 날짜 + 시간 | `java.util.Date` | `LocalDateTime` | 시간대 없음, 불변 |
| 시간대 포함 | `Calendar` + `TimeZone` | `ZonedDateTime` | 명시적 `ZoneId` 포함 |
| 기계 시간(epoch) | `Date.getTime()` | `Instant` | UTC 기준 나노초 정밀도 |
| 날짜 간격 | - | `Period` | 년/월/일 단위 |
| 시간 간격 | - | `Duration` | 시/분/초/나노 단위 |

### LocalDate, LocalTime, LocalDateTime

`LocalDate`는 날짜만 표현한다. 생일, 기념일처럼 시간대와 무관한 날짜를 다룰 때 적합하다:

```java
LocalDate today = LocalDate.now();
LocalDate birthday = LocalDate.of(1990, 3, 15);
LocalDate nextWeek = today.plusWeeks(1);       // 불변 — 새 객체 반환
LocalDate firstDayOfMonth = today.withDayOfMonth(1);

System.out.println(today.getDayOfWeek());      // MONDAY 등 DayOfWeek enum
System.out.println(today.isLeapYear());        // 윤년 여부
```

`LocalTime`은 시간만 표현한다. 영업 시작 시간처럼 날짜와 독립적인 시간에 사용한다:

```java
LocalTime openTime = LocalTime.of(9, 0);
LocalTime closeTime = LocalTime.of(18, 30);
LocalTime now = LocalTime.now();

boolean isOpen = now.isAfter(openTime) && now.isBefore(closeTime);
```

`LocalDateTime`은 날짜와 시간을 함께 표현하지만 시간대 정보는 없다. 단일 서버에서만 동작하거나 시간대 변환이 불필요한 상황에 사용한다:

```java
LocalDateTime meeting = LocalDateTime.of(2024, 6, 15, 14, 30);
LocalDateTime oneHourLater = meeting.plusHours(1);

// 날짜와 시간 분리
LocalDate date = meeting.toLocalDate();
LocalTime time = meeting.toLocalTime();
```

### ZonedDateTime

`ZonedDateTime`은 `LocalDateTime`에 `ZoneId`를 결합한 것이다. 서로 다른 시간대 사용자가 접근하는 시스템에서 정확한 시점을 표현할 때 사용한다:

```java
ZoneId seoulZone = ZoneId.of("Asia/Seoul");
ZoneId utcZone = ZoneId.of("UTC");

ZonedDateTime seoulTime = ZonedDateTime.now(seoulZone);
ZonedDateTime utcTime = seoulTime.withZoneSameInstant(utcZone);

// 동일한 물리적 시점 — 표현만 다름
System.out.println(seoulTime);   // 2024-06-15T14:30:00+09:00[Asia/Seoul]
System.out.println(utcTime);     // 2024-06-15T05:30:00Z[UTC]
```

## Instant와 Duration, Period

### Instant

`Instant`는 UTC 기준 Unix epoch(1970-01-01T00:00:00Z)로부터의 경과 시간을 나노초 단위로 표현한다. 로그 타임스탬프, DB 저장 시점처럼 "언제 발생했는가"를 기록할 때 적합하다:

```java
Instant now = Instant.now();
Instant past = Instant.ofEpochMilli(System.currentTimeMillis());

// Instant ↔ ZonedDateTime 변환
ZonedDateTime zdt = now.atZone(ZoneId.of("Asia/Seoul"));
Instant backToInstant = zdt.toInstant();
```

### Duration

`Duration`은 시간 기반 간격을 표현한다. 두 시점 사이의 경과 시간을 시/분/초/나노초 단위로 계산할 때 사용한다:

```java
Instant start = Instant.now();
// ... 작업 수행 ...
Instant end = Instant.now();

Duration elapsed = Duration.between(start, end);
System.out.println(elapsed.toMillis() + "ms");
System.out.println(elapsed.toSeconds() + "s");

// 명시적 생성
Duration timeout = Duration.ofSeconds(30);
Duration halfDay = Duration.ofHours(12);
```

### Period

`Period`는 날짜 기반 간격을 표현한다. "3개월 뒤", "1년 2개월 10일 후"처럼 달력 기준 간격에 사용한다:

```java
LocalDate startDate = LocalDate.of(2024, 1, 1);
LocalDate endDate = LocalDate.of(2024, 6, 15);

Period period = Period.between(startDate, endDate);
System.out.println(period.getMonths() + "개월 " + period.getDays() + "일");

// 날짜 계산
LocalDate threeMonthsLater = startDate.plus(Period.ofMonths(3));
LocalDate nextYear = startDate.plus(Period.ofYears(1));
```

`Duration`과 `Period`의 구분 기준은 단순하다. 두 `Instant` 사이의 물리적 시간 차이는 `Duration`, 두 `LocalDate` 사이의 달력 간격은 `Period`를 사용한다.

## DateTimeFormatter

`DateTimeFormatter`는 날짜/시간을 문자열로 포맷하거나 문자열을 날짜/시간으로 파싱한다. `SimpleDateFormat`과 달리 **불변이며 스레드 안전**하므로 `static final` 상수로 선언해도 안전하다:

```java
// 미리 정의된 포맷터
DateTimeFormatter isoFormatter = DateTimeFormatter.ISO_LOCAL_DATE;
String isoDate = LocalDate.now().format(isoFormatter);  // 2024-06-15

// 커스텀 패턴
DateTimeFormatter customFormatter = DateTimeFormatter.ofPattern("yyyy년 MM월 dd일");
String koreanDate = LocalDate.now().format(customFormatter);  // 2024년 06월 15일

// 로케일 적용
DateTimeFormatter localizedFormatter = DateTimeFormatter
        .ofPattern("MMMM d, yyyy", Locale.ENGLISH);
String englishDate = LocalDate.now().format(localizedFormatter);  // June 15, 2024

// 파싱
LocalDate parsed = LocalDate.parse("2024-06-15", DateTimeFormatter.ISO_LOCAL_DATE);
LocalDateTime parsedDt = LocalDateTime.parse(
        "2024-06-15 14:30:00"
        , DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")
);
```

## TemporalAdjusters

`TemporalAdjusters`는 "다음 월요일", "이번 달 마지막 날"처럼 상대적 날짜 계산을 깔끔하게 표현하는 팩토리 클래스다. 직접 `plusDays()` 루프를 작성하지 않아도 된다:

```java
LocalDate today = LocalDate.now();

// 다음 월요일
LocalDate nextMonday = today.with(TemporalAdjusters.next(DayOfWeek.MONDAY));

// 이번 달 마지막 날
LocalDate lastDayOfMonth = today.with(TemporalAdjusters.lastDayOfMonth());

// 다음 달 첫째 날
LocalDate firstDayOfNextMonth = today.with(TemporalAdjusters.firstDayOfNextMonth());

// 이번 달 첫 번째 화요일
LocalDate firstTuesday = today.with(
        TemporalAdjusters.firstInMonth(DayOfWeek.TUESDAY)
);

// 이번 달 마지막 금요일
LocalDate lastFriday = today.with(
        TemporalAdjusters.lastInMonth(DayOfWeek.FRIDAY)
);
```

커스텀 로직이 필요하면 `TemporalAdjuster` 함수형 인터페이스를 직접 구현한다:

```java
// 다음 영업일 (주말 건너뜀)
TemporalAdjuster nextBusinessDay = temporal -> {
    DayOfWeek dow = DayOfWeek.from(temporal);
    int daysToAdd = switch (dow) {
        case FRIDAY -> 3;
        case SATURDAY -> 2;
        default -> 1;
    };
    return temporal.plus(daysToAdd, ChronoUnit.DAYS);
};

LocalDate nextWorkday = today.with(nextBusinessDay);
```

## 시간대 처리

### ZoneId와 ZoneOffset

`ZoneId`는 "Asia/Seoul"처럼 지역 기반 시간대를 표현한다. 일광 절약 시간(DST) 전환을 자동으로 처리한다. `ZoneOffset`은 "UTC+09:00"처럼 고정 오프셋을 표현하며 DST를 고려하지 않는다:

```java
// 지역 기반 — DST 자동 처리
ZoneId seoulZone = ZoneId.of("Asia/Seoul");
ZoneId newYorkZone = ZoneId.of("America/New_York");

// 고정 오프셋 — DST 미적용
ZoneOffset kst = ZoneOffset.ofHours(9);
ZoneOffset utc = ZoneOffset.UTC;

// 사용 가능한 모든 ZoneId 조회
Set<String> allZones = ZoneId.getAvailableZoneIds();
```

### UTC 변환 패턴

서버 간 시간 비교나 DB 저장에는 항상 UTC를 기준으로 삼는다. 사용자에게 표시할 때만 로컬 시간대로 변환하는 패턴이 가장 안전하다:

```java
// UTC로 현재 시각 얻기
Instant utcNow = Instant.now();

// UTC → 로컬 시간대 변환 (사용자 표시용)
ZonedDateTime seoulTime = utcNow.atZone(ZoneId.of("Asia/Seoul"));
ZonedDateTime tokyoTime = utcNow.atZone(ZoneId.of("Asia/Tokyo"));

// 로컬 시간대 → UTC 변환 (저장/전송용)
LocalDateTime userInput = LocalDateTime.of(2024, 6, 15, 14, 30);
ZonedDateTime seoulZdt = userInput.atZone(ZoneId.of("Asia/Seoul"));
Instant utcForStorage = seoulZdt.toInstant();
```

## 실무 패턴

### DB 저장 시 UTC 변환

데이터베이스에는 UTC로 저장하고, 읽어올 때 사용자의 시간대로 변환하는 것이 표준 패턴이다. 서버가 여러 지역에 분산되거나 시간대가 다른 사용자를 지원할 때 일관성을 유지할 수 있다:

```java
// 저장: 사용자 입력(로컬) → UTC Instant로 변환
public Instant toUtc(LocalDateTime localDt, String userTimeZone) {
    return localDt
            .atZone(ZoneId.of(userTimeZone))
            .toInstant();
}

// 조회: UTC Instant → 사용자 로컬 시간으로 변환
public LocalDateTime toLocalTime(Instant utcInstant, String userTimeZone) {
    return utcInstant
            .atZone(ZoneId.of(userTimeZone))
            .toLocalDateTime();
}
```

JPA 환경에서는 `Instant` 타입을 엔티티 필드로 사용하고, `spring.jpa.properties.hibernate.jdbc.time_zone=UTC`를 설정하면 Hibernate가 DB 저장 시 UTC를 보장한다.

### 날짜 범위 검증

특정 날짜가 유효한 범위에 속하는지 확인할 때 `isBefore`, `isAfter`, `isEqual`을 조합한다:

```java
public boolean isWithinRange(LocalDate target, LocalDate start, LocalDate end) {
    return !target.isBefore(start) && !target.isAfter(end);
}

// 만료 여부 확인
public boolean isExpired(Instant expiresAt) {
    return Instant.now().isAfter(expiresAt);
}

// 비교: compareTo, isBefore, isAfter, isEqual
LocalDate a = LocalDate.of(2024, 1, 1);
LocalDate b = LocalDate.of(2024, 6, 15);
System.out.println(a.isBefore(b));   // true
System.out.println(a.isEqual(b));    // false
```

### Optional 파싱

사용자 입력처럼 형식이 불확실한 문자열을 파싱할 때는 예외 처리를 명시적으로 수행한다:

```java
public Optional<LocalDate> parseDate(String input) {
    try {
        return Optional.of(
                LocalDate.parse(input, DateTimeFormatter.ofPattern("yyyy-MM-dd"))
        );
    } catch (DateTimeParseException e) {
        return Optional.empty();
    }
}
```
