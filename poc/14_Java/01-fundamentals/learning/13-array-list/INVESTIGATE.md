# ArrayList: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. ArrayList vs LinkedList, 실제 벤치마크에서 LinkedList가 거의 항상 지는 이유

### 왜 이 질문이 중요한가
"중간 삽입/삭제가 많으면 LinkedList가 빠르다"는 교과서 지식은 이론적으로 맞지만 실제 벤치마크에서는 틀린 경우가 대부분이다. 왜 그런지 이해하려면 현대 CPU 아키텍처와 메모리 지역성(locality)을 알아야 한다. 이를 모르면 잘못된 자료구조 선택으로 성능을 저하시킨다.

### 답변

이론적 복잡도는 LinkedList가 유리해 보인다. 중간 삽입/삭제가 O(1)이고 ArrayList는 O(n)의 shift 비용이 있다. 그러나 실제 성능은 CPU 캐시 동작 방식에 의해 결정된다.

ArrayList의 내부 배열은 연속된 메모리 공간에 있다. CPU가 배열의 한 원소에 접근하면 캐시 라인(보통 64바이트) 단위로 인접 원소들도 함께 캐시에 적재된다. 다음 원소 접근 시 이미 캐시에 있어 메모리 접근 없이 처리된다. 이를 공간 지역성(spatial locality)이라 한다.

LinkedList의 노드는 각각 `new Node()`로 힙 어딘가에 흩어져 있다. 다음 노드의 주소를 따라가면(pointer chasing) 캐시 미스가 발생하고 메인 메모리에서 데이터를 가져와야 한다. 현대 CPU에서 캐시 미스는 수백 사이클 비용이다.

```java
// JMH 벤치마크 패턴 (실제 실행은 아님, 경향 설명용)
// 1000개 원소 리스트 중간에 500번 삽입
// ArrayList: ~0.5ms (shift 비용 있지만 캐시 친화적)
// LinkedList: ~2ms  (O(1) 삽입이지만 탐색 시 포인터 추적으로 캐시 미스 반복)

// 특히 순차 순회는 차이가 극명
List<Integer> arrayList = new ArrayList<>(1_000_000);
List<Integer> linkedList = new LinkedList<>();
// arrayList 순회: 캐시 라인 단위 프리페치로 매우 빠름
// linkedList 순회: 매 노드마다 포인터 추적 → 캐시 미스 반복
```

LinkedList가 실제로 유리한 경우는 매우 제한적이다. 리스트 양 끝에서만 삽입/삭제하는 경우(`Deque` 용도)이고, 원소 크기가 매우 커서 shift 비용이 캐시 미스 비용을 압도할 때다. 그러나 이 경우에도 `ArrayDeque`가 LinkedList보다 대부분 빠르다.

실무 지침: 기본 선택은 `ArrayList`다. 큐/스택이 필요하면 `ArrayDeque`, 스레드 안전이 필요하면 `CopyOnWriteArrayList`나 동기화 래퍼를 고려한다. `LinkedList`를 선택하는 경우는 거의 없다.

---

## Q2. Java 21 Sequenced Collections 도입 이유

### 왜 이 질문이 중요한가
Java 21에서 `SequencedCollection`, `SequencedSet`, `SequencedMap`이 추가됐다. 이것이 단순한 편의 API 추가가 아니라 기존 컬렉션 계층의 어떤 설계 결함을 해결한 것인지 이해하면 API 설계 원칙에 대한 깊은 통찰을 얻을 수 있다.

### 답변

기존 컬렉션 프레임워크에는 오래된 설계 결함이 있었다. "순서가 있는 컬렉션의 첫 번째/마지막 원소에 접근하는 통일된 방법"이 없었다.

`List`는 `get(0)`과 `get(size()-1)`을 쓴다. `Deque`는 `peekFirst()`와 `peekLast()`를 쓴다. `SortedSet`은 `first()`와 `last()`를 쓴다. `LinkedHashSet`은 순서가 있지만 첫 번째 원소에 접근하는 직접적인 방법이 아예 없었다(`iterator().next()`를 써야 했다). 역순 순회도 타입마다 달랐다.

```java
// Java 21 이전 — 타입마다 다른 API
List<String> list = ...;
String first = list.get(0);                    // List 방식
String last  = list.get(list.size() - 1);

Deque<String> deque = ...;
String first = deque.peekFirst();              // Deque 방식
String last  = deque.peekLast();

SortedSet<String> sorted = ...;
String first = sorted.first();                 // SortedSet 방식
String last  = sorted.last();

LinkedHashSet<String> lhs = ...;
String first = lhs.iterator().next();          // 비직관적
// last는?? 스트림을 써야 함

// Java 21 이후 — SequencedCollection으로 통일
SequencedCollection<String> sc = ...;          // List, Deque, LinkedHashSet 모두 해당
String first = sc.getFirst();
String last  = sc.getLast();
sc.addFirst("x");
sc.addLast("z");
sc.removeFirst();
SequencedCollection<String> reversed = sc.reversed(); // 역순 뷰
```

`SequencedCollection`을 도입함으로써 순서 있는 컬렉션을 다루는 유틸리티 메서드를 하나의 타입으로 작성할 수 있게 됐다.

```java
// 이제 이런 유틸리티 메서드가 가능
public <T> T getFirstOrDefault(SequencedCollection<T> coll, T defaultValue) {
    return coll.isEmpty() ? defaultValue : coll.getFirst();
    // List, LinkedHashSet, ArrayDeque 모두 전달 가능
}
```

이 도입은 "인터페이스는 처음부터 완벽하지 않아도, 나중에 `default` 메서드로 진화할 수 있다"는 Java 8 이후의 API 진화 원칙을 보여주는 사례이기도 하다.
