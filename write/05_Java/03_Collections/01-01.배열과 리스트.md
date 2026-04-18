# 배열과 리스트
---
> 자바의 선형 자료구조는 내부 구현에 따라 성능 특성이 완전히 달라진다. 배열 기반은 접근이 빠르고, 노드 기반은 삽입·삭제가 유연하다.

## 1. 배열(Array)의 구조

배열은 동일한 타입의 요소를 연속된 메모리 공간에 저장한다. 각 요소는 인덱스로 식별되며, 인덱스를 알면 `baseAddress + index * elementSize` 계산 한 번으로 위치를 구할 수 있다. 이 덕분에 인덱스 접근은 항상 O(1)이다.

값 검색은 다르다. 특정 값이 어느 위치에 있는지 모르면 처음부터 끝까지 비교해야 하므로 O(n)이 걸린다. 정렬된 배열에서는 이진 탐색(Binary Search)으로 O(log n)으로 줄일 수 있다.

```java
int[] arr = {1, 2, 3, 4, 5};

// 인덱스 접근: O(1)
int value = arr[2]; // 3

// 선형 검색: O(n)
for (int i = 0; i < arr.length; i++) {
    if (arr[i] == 10) break;
}
```

## 2. 배열의 추가와 삭제

배열의 크기는 생성 시점에 고정된다. 중간에 요소를 삽입하면 그 이후 요소를 모두 한 칸씩 오른쪽으로 밀어야 하고, 삭제하면 반대로 당겨야 한다. 이동해야 할 요소가 n개라면 O(n)이 소요된다. 배열 끝에 추가하는 경우만 이동이 없어 O(1)이 된다.

| 연산 | 위치 | 시간 복잡도 |
|------|------|------------|
| 접근 | 인덱스 | O(1) |
| 검색 | 전체 | O(n) |
| 삽입 | 처음·중간 | O(n) |
| 삽입 | 끝 | O(1) |
| 삭제 | 처음·중간 | O(n) |
| 삭제 | 끝 | O(1) |

## 3. ArrayList — 동적 배열

`java.util.ArrayList`는 내부적으로 `Object[]` 배열을 가지며, 용량이 부족하면 2배로 늘린 새 배열에 복사한다. 이 `grow()` 작업은 `Arrays.copyOf()`를 통해 시스템 레벨 메모리 복사로 처리되므로, 요소를 하나씩 이동하는 것보다 수 배 빠르다.

```java
// ArrayList 내부 grow() 핵심 로직
private void grow() {
    int oldCapacity = elementData.length;
    int newCapacity = oldCapacity * 2;
    elementData = Arrays.copyOf(elementData, newCapacity);
}
```

초기 용량(default 10)을 초과하는 순간 리사이징이 발생한다. 저장할 데이터 개수를 미리 알면 `new ArrayList<>(initialCapacity)`로 불필요한 리사이징을 방지할 수 있다. 인덱스 접근은 배열과 동일하게 O(1)이지만, 중간 삽입·삭제는 여전히 O(n)이다.

## 4. LinkedList — 노드 기반 연결 리스트

`java.util.LinkedList`는 `Node` 객체를 연결해 구성한다. 각 노드는 값(item), 이전 노드 참조(prev), 다음 노드 참조(next)를 가진다. 메모리가 연속적이지 않아도 되므로 크기 제한이 없다.

```java
// 단일 연결 리스트 노드 구조 (개념)
class Node<E> {
    E item;
    Node<E> next;
}
```

앞이나 뒤에 삽입·삭제할 때는 참조만 바꾸면 되므로 O(1)이다. 하지만 특정 인덱스에 접근하려면 첫 노드부터 순서대로 따라가야 하므로 O(n)이 걸린다. `java.util.LinkedList`는 앞뒤 참조를 모두 갖는 이중 연결 리스트(Doubly Linked List)로 구현되어 있어, 끝에서의 삽입·삭제도 O(1)이다.

## 5. ArrayList vs LinkedList 시간 복잡도 비교

| 연산 | ArrayList | LinkedList |
|------|-----------|------------|
| 인덱스 접근 | O(1) | O(n) |
| 앞에 삽입·삭제 | O(n) | O(1) |
| 중간 삽입·삭제 | O(n) | O(n)* |
| 끝에 삽입·삭제 | O(1) | O(1) |
| 검색 | O(n) | O(n) |

*LinkedList 중간 삽입은 노드 변경 자체는 O(1)이나, 위치를 찾는 데 O(n)이 든다.

실무에서는 인덱스 접근과 순회가 대부분이므로 ArrayList가 기본 선택이다. LinkedList는 큐(Queue)나 덱(Deque)처럼 양 끝 삽입·삭제가 잦은 경우에 유리하다. 캐시 지역성(cache locality) 측면에서도 연속 메모리인 ArrayList가 CPU 캐시를 효율적으로 활용해 실제 성능이 더 좋은 경우가 많다.

## 6. 불변 리스트 — List.of()와 List.copyOf()

Java 9에서 도입된 `List.of()`는 수정 불가능한(immutable) 리스트를 반환한다. 내부 배열을 외부에 노출하지 않으며, `add()`나 `set()`을 호출하면 `UnsupportedOperationException`이 발생한다.

```java
// List.of() — 불변, null 불허
List<String> fruits = List.of("Apple", "Banana", "Cherry");

// List.copyOf() — 기존 컬렉션을 불변 복사
List<String> mutable = new ArrayList<>(List.of("A", "B"));
List<String> immutable = List.copyOf(mutable);
```

`List.copyOf()`는 기존 가변 컬렉션을 방어적으로 복사해 불변 리스트를 만들 때 사용한다. 두 팩토리 메서드 모두 `null` 요소를 허용하지 않는다.

## 7. Java 21 — SequencedCollection

Java 21은 `SequencedCollection` 인터페이스를 `Collection` 계층에 추가했다. 첫 번째·마지막 요소 접근과 역순 뷰를 표준 API로 통일한다.

```java
List<String> list = new ArrayList<>(List.of("A", "B", "C"));

// Java 21 SequencedCollection API
String first = list.getFirst(); // "A"
String last  = list.getLast();  // "C"

list.addFirst("Z"); // 앞에 추가
list.addLast("W");  // 끝에 추가
list.removeFirst(); // 첫 요소 제거
list.removeLast();  // 마지막 요소 제거

// 역순 뷰 (원본과 연결됨, 복사 아님)
List<String> reversed = list.reversed();
```

`reversed()`는 새 리스트를 복사하지 않고 원본의 역순 뷰를 반환한다. 원본을 수정하면 뷰에도 반영된다. `LinkedList`와 `ArrayList` 모두 이 인터페이스를 구현하므로 타입에 관계없이 동일한 API를 사용할 수 있다.
