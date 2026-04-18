# Set과 Map 심화: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. ConcurrentHashMap vs Collections.synchronizedMap 내부 차이

### 왜 이 질문이 중요한가
멀티스레드 환경에서 Map을 사용할 때 둘 중 무엇을 선택할지는 단순한 "ConcurrentHashMap이 빠르다"로 끝나지 않는다. 내부 잠금 전략의 차이가 어떤 상황에서 어떤 결과를 만드는지 이해해야 올바른 선택과 올바른 사용이 가능하다.

### 답변

`Collections.synchronizedMap(map)`은 래퍼 패턴으로 동작한다. 모든 메서드에 `synchronized(mutex)`로 전체 맵을 잠근다. 한 번에 하나의 스레드만 맵에 접근할 수 있다. 구현이 단순하고 기존 Map을 감싸는 것이라 모든 Map 구현체에 적용 가능하다.

```java
// synchronizedMap 내부 — 메서드 전체를 단일 락으로 직렬화
public V get(Object key) {
    synchronized (mutex) { return m.get(key); }
}
public V put(K key, V value) {
    synchronized (mutex) { return m.put(key, value); }
}
// 읽기와 쓰기가 모두 같은 락 — 읽기가 많아도 직렬화됨
```

`ConcurrentHashMap`은 세그먼트 잠금(Java 7) 또는 버킷 단위 잠금(Java 8+)을 사용한다. Java 8+ 구현에서는 쓰기 시 해당 버킷(배열 인덱스)의 첫 번째 노드에만 `synchronized`를 걸고, 읽기는 대부분 잠금 없이 `volatile` 읽기로 처리한다. 다른 버킷에 대한 쓰기는 병렬로 진행 가능하다.

```java
// ConcurrentHashMap의 핵심 차이
ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();

// 원자적 복합 연산 제공 — synchronizedMap에는 없음
map.computeIfAbsent("key", k -> expensiveCompute(k));
map.merge("counter", 1, Integer::sum); // 원자적 카운터 증가

// synchronizedMap의 함정 — 복합 연산이 원자적이지 않음
Map<String, Integer> syncMap = Collections.synchronizedMap(new HashMap<>());
synchronized (syncMap) { // 복합 연산은 명시적 동기화 필요
    if (!syncMap.containsKey("key")) {
        syncMap.put("key", compute());
    }
}
```

중요한 차이는 반복(iteration)이다. `synchronizedMap`의 반복은 호출자가 외부에서 직접 `synchronized` 블록으로 감싸야 한다. 그렇지 않으면 `ConcurrentModificationException`이 발생할 수 있다. `ConcurrentHashMap`의 반복은 weakly consistent하다. 반복 중 다른 스레드가 수정해도 예외가 발생하지 않지만 수정된 내용이 반복에 반영될 수도, 안 될 수도 있다.

선택 기준: 읽기가 많고 쓰기가 가끔인 환경에서는 `ConcurrentHashMap`, 기존 비스레드 안전 Map을 간단히 보호해야 한다면 `synchronizedMap`이지만 성능이 문제라면 `ConcurrentHashMap`으로 교체한다.

---

## Q2. EnumSet이 비트 벡터인 이유와 성능 이점

### 왜 이 질문이 중요한가
`EnumSet`이 내부적으로 비트 벡터를 사용한다는 사실은 알려져 있지만, 왜 가능한지(enum의 어떤 특성 덕분인지), 실제로 얼마나 빠른지, 어떤 상황에서 써야 하는지를 설명하지 못하는 경우가 많다.

### 답변

`EnumSet`이 비트 벡터를 쓸 수 있는 이유는 enum의 두 가지 특성 때문이다. 첫째, enum 상수의 수는 컴파일 타임에 고정된다. 둘째, 각 상수는 고유한 `ordinal()`을 가지며 0부터 시작하는 연속된 정수다. 이 두 조건이 비트 위치와 상수를 1:1로 매핑할 수 있게 한다.

```java
enum Day { MON, TUE, WED, THU, FRI, SAT, SUN }
// ordinal: 0    1    2    3    4    5    6

EnumSet<Day> weekdays = EnumSet.of(Day.MON, Day.WED, Day.FRI);
// 내부 비트 표현: 0b0010101 (이진수, bit 0=MON, bit 2=WED, bit 4=FRI)
// long 하나로 최대 64개 enum 상수 표현 가능 (RegularEnumSet)
// 64개 초과 시 long[] 사용 (JumboEnumSet)

// contains() — 비트 AND 연산 한 번
weekdays.contains(Day.WED); // (bits & (1L << WED.ordinal())) != 0

// addAll(other EnumSet) — 비트 OR 연산 한 번
// removeAll(other EnumSet) — 비트 AND NOT 연산 한 번
// retainAll(other EnumSet) — 비트 AND 연산 한 번
```

성능 이점은 집합 연산에서 극명하게 드러난다. `HashSet<Day>`로 합집합/교집합을 구하면 O(n) 루프가 필요하지만, `EnumSet`은 단일 비트 연산(O(1))으로 처리된다. Day enum 기준으로 7개 원소이므로 long 하나의 비트 조작으로 모든 집합 연산이 끝난다.

```java
// 실무 사용 예: 권한 시스템
enum Permission { READ, WRITE, DELETE, ADMIN }

// 역할별 권한 정의
EnumSet<Permission> readerPerms  = EnumSet.of(Permission.READ);
EnumSet<Permission> editorPerms  = EnumSet.of(Permission.READ, Permission.WRITE);
EnumSet<Permission> adminPerms   = EnumSet.allOf(Permission.class);

// 권한 확인 — 비트 AND 한 번
boolean canWrite = editorPerms.contains(Permission.WRITE); // 즉시

// 권한 합산 — 비트 OR 한 번
EnumSet<Permission> combined = EnumSet.copyOf(readerPerms);
combined.addAll(editorPerms); // O(1)
```

`EnumSet.noneOf()`, `allOf()`, `complementOf()`, `range()` 등 풍부한 팩토리 메서드도 제공되며, null을 허용하지 않아 NPE 위험도 없다. enum 상수 집합을 다루는 모든 경우에서 `HashSet<EnumType>` 대신 `EnumSet`을 쓰는 것이 기본 원칙이다.
