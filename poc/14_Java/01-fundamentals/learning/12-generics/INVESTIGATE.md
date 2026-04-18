# 제네릭: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. 타입 소거가 런타임에 일으키는 실질적 문제

### 왜 이 질문이 중요한가
"제네릭은 컴파일 타임에만 존재하고 런타임에는 지워진다"는 사실을 알지만, 그것이 실제로 어떤 코드 패턴에서 어떤 에러를 일으키는지 설명하지 못하면 반쪽 지식이다. 타입 소거로 인한 실질적 제약을 이해해야 제네릭 코드를 올바르게 작성할 수 있다.

### 답변

타입 소거(type erasure)란 컴파일러가 제네릭 타입 파라미터를 바이트코드에서 제거하고, `T`를 `Object`로(bounded면 upper bound 타입으로) 바꾸는 과정이다. `List<String>`과 `List<Integer>`는 런타임에 모두 그냥 `List`다.

이로 인한 실질적 문제는 네 가지 형태로 나타난다.

첫째, `instanceof` 검사 불가다. `obj instanceof List<String>`은 컴파일 에러다. 런타임에 타입 파라미터 정보가 없기 때문이다. `instanceof List<?>`는 가능하지만 String인지는 알 수 없다.

둘째, 제네릭 배열 생성 불가다. `new T[10]`은 컴파일 에러다. 배열은 런타임에 타입을 알아야 하는데 `T`가 소거되기 때문이다.

```java
// 타입 소거로 인한 제약들
class Container<T> {
    // 컴파일 에러: Cannot create generic array
    // private T[] array = new T[10];

    // 우회: Object 배열 사용 후 캐스팅 (경고 발생, @SuppressWarnings 필요)
    @SuppressWarnings("unchecked")
    private T[] array = (T[]) new Object[10];

    // 컴파일 에러: Cannot perform instanceof check on erased type
    public boolean isString(Object obj) {
        // return obj instanceof T; // 불가
        return obj instanceof String; // 구체 타입만 가능
    }
}
```

셋째, 오버로딩 충돌이다. `void process(List<String> list)`와 `void process(List<Integer> list)`는 소거 후 둘 다 `void process(List list)`가 되어 컴파일 에러가 난다.

넷째, 리플렉션으로 런타임에 타입 파라미터를 얻기 어렵다. 변수의 실제 타입 파라미터는 소거되지만, 클래스 선언부의 제네릭 정보는 `Type` 메타데이터로 보존된다. Jackson이 `TypeReference<List<User>>`를 사용하는 이유가 이 때문이다.

```java
// Jackson의 TypeReference — 익명 클래스의 슈퍼타입으로 타입 정보 보존
List<User> users = objectMapper.readValue(json,
    new TypeReference<List<User>>() {}); // 익명 클래스로 감싸야 타입 정보 유지
// new TypeReference<List<User>>() {} 의 슈퍼타입 제네릭 파라미터로
// List<User>가 .class 파일에 저장되어 리플렉션으로 읽을 수 있음
```

---

## Q2. PECS를 실무 API 설계에 적용하는 판단 기준

### 왜 이 질문이 중요한가
PECS(Producer Extends, Consumer Super)는 제네릭 와일드카드 사용 원칙이지만 외우기만 하고 실제 API 설계에 적용하는 방법을 모르는 경우가 많다. 라이브러리 API를 설계하거나 유틸리티 메서드를 작성할 때 이 원칙을 적용하면 호출자가 더 다양한 타입을 전달할 수 있어 유연성이 높아진다.

### 답변

PECS 원칙의 의미를 먼저 정확히 이해해야 한다. "Producer Extends"는 데이터를 꺼내기만 하는(생산하는) 컬렉션에는 `? extends T`를 쓴다는 뜻이다. "Consumer Super"는 데이터를 넣기만 하는(소비하는) 컬렉션에는 `? super T`를 쓴다는 뜻이다.

```java
// PECS 적용 전 — 유연성이 낮음
public static void copy(List<Number> src, List<Number> dest) {
    for (Number n : src) dest.add(n);
}
// copy(integers, numbers)도 안 되고 copy(numbers, objects)도 안 됨

// PECS 적용 후 — 유연성 극대화
public static <T> void copy(List<? extends T> src, List<? super T> dest) {
    for (T item : src) dest.add(item);
}
// copy(integers, numbers) OK — Integer extends Number
// copy(integers, objects) OK — Object super Integer
// copy(numbers, objects)  OK

// 실무 예시 1: 컬렉션을 읽기만 하는 메서드
public double sum(List<? extends Number> numbers) {
    return numbers.stream().mapToDouble(Number::doubleValue).sum();
    // List<Integer>, List<Double>, List<Long> 모두 전달 가능
}

// 실무 예시 2: 컬렉션에 쓰기만 하는 메서드
public void addDefaults(List<? super Integer> list) {
    list.add(0);
    list.add(1);
    // List<Integer>, List<Number>, List<Object> 모두 전달 가능
}
```

실무 판단 기준은 세 가지 질문으로 정리된다. 첫째, "이 파라미터에서 값을 꺼내기만 하는가?" → `? extends T`. 둘째, "이 파라미터에 값을 넣기만 하는가?" → `? super T`. 셋째, "둘 다 하는가?" → 경계 와일드카드 없이 `T`를 직접 사용한다.

주의할 점은 반환 타입에 와일드카드를 쓰지 않는 것이다. `List<? extends Number> getNumbers()`는 호출자가 반환값으로 아무것도 할 수 없게 만든다. 와일드카드는 메서드 파라미터에만 쓰는 것이 원칙이다. Java 표준 라이브러리의 `Collections.copy(List<? super T> dest, List<? extends T> src)`가 PECS의 교과서적 예다.
