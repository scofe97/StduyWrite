# java.lang과 Object: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. equals/hashCode 계약 위반 시 HashMap에서 어떤 문제가 발생하는가?

### 왜 이 질문이 중요한가
equals/hashCode는 Java 컬렉션의 동작 기반이다. 계약을 위반하면 데이터 손실이나 조회 실패가 발생하는데 원인을 찾기 매우 어렵다. 면접에서는 이론적 계약뿐 아니라 "실제로 어떤 증상이 나타나는가"까지 묻는 경우가 많다.

### 답변

HashMap은 버킷 배열로 구성된다. `put(key, value)` 시 `key.hashCode()`로 버킷 인덱스를 결정하고, 같은 버킷 내에서 `equals()`로 동일 키를 찾는다. 이 두 메서드가 일관성 없이 구현되면 세 가지 증상이 나타난다.

첫 번째는 `hashCode`를 재정의하지 않고 `equals`만 재정의한 경우다. 논리적으로 같은 객체가 서로 다른 버킷에 저장되어 `get()`이 항상 `null`을 반환한다. `put(key1, v1)` 후 `get(key2)`를 호출할 때 `key1.equals(key2) == true`임에도 `hashCode`가 달라 다른 버킷을 탐색하기 때문이다.

```java
// hashCode 재정의 누락 예시
class Point {
    int x, y;
    @Override
    public boolean equals(Object o) {
        Point p = (Point) o;
        return x == p.x && y == p.y;
    }
    // hashCode 없음 — Object의 기본 구현(주소 기반) 사용
}

Map<Point, String> map = new HashMap<>();
map.put(new Point(1, 2), "A");
map.get(new Point(1, 2)); // null 반환! 두 Point는 다른 버킷에 있음
```

두 번째는 `hashCode`를 재정의했지만 가변 필드를 기반으로 계산하는 경우다. 키를 맵에 넣은 후 해당 필드를 변경하면 `hashCode`가 달라져 버킷이 바뀐다. 이전 버킷에 여전히 존재하지만 새 해시로 탐색하면 찾지 못한다. 이 경우 맵에서 해당 키로 `get()`도, `remove()`도 실패하고 메모리 누수가 발생한다.

세 번째는 `hashCode`는 같지만 `equals`가 비대칭인 경우다. `a.equals(b) == true`이지만 `b.equals(a) == false`이면 `containsKey(b)`가 false를 반환할 수 있다. 이는 상속 관계에서 `equals`를 잘못 재정의할 때 자주 발생한다.

계약의 핵심은 두 가지다. "equals가 true면 hashCode도 같아야 한다"(필수), 그리고 "hashCode가 같아도 equals는 false일 수 있다"(허용). 실무에서는 Lombok `@EqualsAndHashCode`나 Java 14+ Record를 쓰면 이 계약을 자동으로 지킬 수 있다.

---

## Q2. Record가 equals/hashCode를 대체할 수 있는 범위

### 왜 이 질문이 중요한가
Java 16에서 정식 도입된 Record는 equals/hashCode/toString을 자동 생성한다. 그러나 "모든 클래스를 Record로 바꾸면 되지 않나"라는 단순한 생각은 실무에서 문제를 일으킨다. Record가 적합한 경우와 그렇지 않은 경우를 구분하는 것이 중요하다.

### 답변

Record의 equals/hashCode는 모든 컴포넌트 필드를 기반으로 자동 생성된다. 값 기반 동등성이 필요한 순수 데이터 홀더에는 완벽한 선택이다. DTO, 좌표 같은 값 객체, 복합 맵 키로 쓰는 경우가 대표적이다.

```java
record Point(int x, int y) {}
record CacheKey(String tenantId, long userId) {}

// 자동 생성된 equals — 모든 필드 비교
// new Point(1,2).equals(new Point(1,2)) == true
// Map<CacheKey, Data> 에서 키로 안전하게 사용 가능
```

그러나 Record가 적합하지 않은 네 가지 상황이 있다. 첫째, JPA Entity다. JPA는 프록시 객체를 생성하는데, Record는 상속이 불가하므로 프록시를 만들 수 없다. 또한 JPA Entity의 동등성은 보통 ID 필드 하나만으로 판단하지만 Record는 모든 필드를 비교한다.

둘째, 일부 필드만으로 동등성을 정의해야 하는 경우다. 비즈니스 키(예: 이메일)로만 비교해야 하는 도메인 객체는 Record의 전체 필드 비교가 맞지 않는다.

셋째, 필드가 배열인 경우다. Record의 자동 생성 equals는 배열에 대해 `Arrays.equals()`가 아닌 `==`를 사용하므로 배열 내용이 같아도 false를 반환한다. 이 경우 명시적으로 재정의해야 한다.

```java
record ArrayHolder(int[] values) {
    // 기본 equals는 배열 참조 비교 — 재정의 필요
    @Override
    public boolean equals(Object o) {
        if (!(o instanceof ArrayHolder other)) return false;
        return Arrays.equals(values, other.values);
    }
    @Override
    public int hashCode() {
        return Arrays.hashCode(values);
    }
}
```

넷째, 지연 계산 필드(lazy field)나 캐시 필드가 있는 경우다. Record의 모든 필드는 생성자에서 초기화해야 하며 나중에 변경할 수 없으므로 lazy initialization 패턴을 적용할 수 없다. 요약하면 Record는 불변 값 객체의 equals/hashCode를 완전히 대체할 수 있지만, 도메인 엔티티나 특수한 동등성 정책이 필요한 경우에는 여전히 직접 구현이 필요하다.
