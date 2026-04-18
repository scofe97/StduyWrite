# 제네릭

---

> 제네릭(Generics)은 클래스 내부에서 사용할 타입을 외부에서 지정하는 기법이다. 컴파일 시점에 타입 안전성을 보장하고, 형변환 없이 코드를 재사용할 수 있게 한다.

## 제네릭이 필요한 이유

`Integer`를 담는 박스와 `String`을 담는 박스를 각각 만들면 로직은 동일한데 타입만 다른 클래스가 중복된다. `Object`로 통일하면 중복은 줄지만 두 가지 문제가 생긴다. 값을 꺼낼 때마다 명시적 형변환이 필요하고, 컴파일러가 잘못된 타입 삽입을 막아주지 못해 런타임에 `ClassCastException`이 발생할 수 있다.

제네릭은 이 두 문제를 동시에 해결한다:

```java
// Object 방식: 형변환 필요, 잘못된 타입 삽입을 컴파일러가 막지 못한다
ObjectBox integerBox = new ObjectBox();
integerBox.set(10);
Integer result = (Integer) integerBox.get(); // 명시적 형변환
integerBox.set("문자100");                    // 컴파일 통과, 런타임 예외

// 제네릭 방식: 형변환 불필요, 타입 불일치는 컴파일 오류
GenericBox<Integer> box = new GenericBox<>();
box.setValue(10);
Integer result = box.getValue(); // 형변환 없음
box.setValue("문자100");         // 컴파일 오류
```

## 제네릭 클래스, 메서드, 인터페이스

제네릭은 클래스, 인터페이스, 메서드 단위 모두에 적용할 수 있다. 타입 파라미터 명명 관례는 대문자 한 글자를 사용한다:

- `T`: Type (일반 타입)
- `E`: Element (컬렉션 요소)
- `K` / `V`: Key / Value (맵 키-값)
- `N`: Number
- `S`, `U`, `V`: 두 번째, 세 번째, 네 번째 타입

제네릭 메서드는 클래스 전체가 아닌 특정 메서드에만 타입 파라미터를 선언한다. `static` 메서드에도 적용 가능하며, 호출 시점에 타입이 독립적으로 결정된다:

```java
public class GenericMethod {
    // 타입 파라미터 <T>를 반환 타입 앞에 선언한다
    public static <T> T genericMethod(T obj) {
        System.out.println("generic print = " + obj);
        return obj;
    }

    // 바운디드 타입 파라미터: Number와 그 하위 타입만 허용
    public static <T extends Number> T numberMethod(T t) {
        System.out.println("bound print = " + t);
        return t;
    }
}
```

클래스에 선언된 타입 파라미터와 메서드에 선언된 타입 파라미터가 같은 이름이라면, 메서드의 타입 파라미터가 우선한다. 해당 메서드 내에서 클래스 타입 파라미터는 상한 없는 `Object`로 취급된다.

## 타입 소거(Type Erasure)

제네릭은 컴파일 시점에만 존재한다. 컴파일러는 제네릭 코드를 검증한 뒤 타입 파라미터를 지우고, 필요한 곳에 자동으로 형변환 코드를 삽입한다. 이것이 **타입 소거**다:

```java
// 소스 코드 (.java)
GenericBox<Integer> box = new GenericBox<Integer>();
box.set(10);
Integer result = box.get();

// 바이트코드 (.class) — 타입 정보가 소거된다
GenericBox box = new GenericBox();
box.set(10);
Integer result = (Integer) box.get(); // 컴파일러가 형변환을 대신 추가
```

타입 소거 덕분에 제네릭이 도입되기 전 코드(로 타입)와의 하위 호환성이 유지된다. 그러나 런타임에는 타입 정보가 없기 때문에 두 가지 동작이 불가능하다:

```java
public class EraserBox<T> {
    public boolean instanceCheck(Object param) {
        return param instanceof T; // 컴파일 오류: T는 런타임에 존재하지 않는다
    }

    public T create() {
        return new T(); // 컴파일 오류: T는 런타임에 Object가 된다
    }
}
```

## 바운디드 타입 파라미터

`<T extends Animal>`처럼 타입 파라미터의 범위를 특정 타입의 하위 타입으로 제한할 수 있다. 이를 **바운디드 타입 파라미터(bounded type parameter)**라 한다. 상한을 지정하면 해당 타입의 메서드를 타입 파라미터에 직접 호출할 수 있다:

```java
// 상한 없는 T: Animal 메서드 호출 불가
public class AnimalHospital<T> {
    private T animal;
    public void checkup() {
        animal.getName(); // 컴파일 오류: T에 getName()이 없다
    }
}

// Animal을 상한으로 지정: Animal 메서드 사용 가능
public class AnimalHospital<T extends Animal> {
    private T animal;
    public void checkup() {
        System.out.println(animal.getName()); // 정상
        System.out.println(animal.getSize()); // 정상
        animal.sound();                       // 정상
    }

    public T getBigger(T target) {
        return animal.getSize() > target.getSize() ? animal : target;
    }
}
```

`Comparable`처럼 자기 참조 타입에도 적용할 수 있다. `<T extends Comparable<T>>`는 "T는 같은 타입 T와 비교 가능해야 한다"는 재귀적 타입 바운드(recursive type bound)다:

```java
public static <T extends Comparable<T>> T max(List<T> list) {
    if (list.isEmpty()) throw new IllegalArgumentException("빈 리스트");
    T result = list.get(0);
    for (T t : list) {
        if (t.compareTo(result) > 0) result = t;
    }
    return result;
}
```

## 와일드카드와 PECS 원칙

`?`는 알 수 없는 타입을 나타내는 **와일드카드(wildcard)**다. 제네릭 메서드와 달리 와일드카드 메서드는 호출 시 타입을 고정하지 않고 어떤 타입의 컨테이너든 받을 수 있다:

```java
// 제네릭 메서드: 호출 시점에 T가 Dog으로 고정된다
static <T extends Animal> T printAndReturnGeneric(Box<T> box) {
    T t = box.getValue();
    System.out.println(t.getName());
    return t;
}

// 와일드카드 메서드: Box<Dog>, Box<Cat> 모두 받을 수 있다. 반환 타입은 Animal
static Animal printAndReturnWildcard(Box<? extends Animal> box) {
    Animal animal = box.getValue();
    System.out.println(animal.getName());
    return animal;
}
```

와일드카드에는 상한과 하한을 지정할 수 있다. 어느 쪽을 쓸지 결정하는 원칙이 **PECS(Producer Extends Consumer Super)**다:

- `<? extends T>` (상한 와일드카드): 컨테이너에서 T를 **꺼낼(produce)** 때 사용한다. 쓰기는 불가능하다.
- `<? super T>` (하한 와일드카드): 컨테이너에 T를 **넣을(consume)** 때 사용한다. 읽기는 `Object`로만 가능하다.

```java
// 상한: List에서 읽기만 한다 (Producer)
public static double sumOfList(List<? extends Number> list) {
    double sum = 0;
    for (Number n : list) sum += n.doubleValue();
    return sum;
}

// 하한: List에 쓰기만 한다 (Consumer)
public static void addNumbers(List<? super Integer> list) {
    for (int i = 0; i < 10; i++) list.add(i);
}
```

## 제네릭과 배열의 비호환성

Java 배열과 제네릭은 타입 규칙이 근본적으로 다르다. 배열은 **공변(covariant)**이고 런타임에 타입 정보를 유지(실체화)한다. 제네릭은 **불공변(invariant)**이고 타입 정보가 소거된다:

```java
// 배열은 공변: Long[]을 Object[]에 대입할 수 있다
// 그러나 런타임에 ArrayStoreException이 발생한다
Object[] objectArray = new Long[1];
objectArray[0] = "타입이 달라 넣을 수 없다"; // 런타임 예외

// 제네릭은 불공변: List<Long>을 List<Object>에 대입할 수 없다
// 컴파일 오류로 사전에 차단된다
List<Object> ol = new ArrayList<Long>(); // 컴파일 오류
```

이 차이 때문에 `new T[]`, `new List<T>[]` 같은 제네릭 배열 생성은 허용되지 않는다. 배열 대신 `List<T>`를 사용하면 컴파일 시점에 타입 안전성을 보장받을 수 있다.

## 타입 토큰과 수퍼 타입 토큰

타입 소거로 인해 런타임에 제네릭 타입 정보가 사라지는 문제를 우회하는 기법이 **타입 토큰(type token)**이다. `Class<T>` 리터럴을 메서드에 전달하면 런타임에도 타입 정보를 활용할 수 있다:

```java
// 타입 토큰: Class<T>를 넘겨 런타임 타입 정보를 보존한다
public <T> T getFavorite(Class<T> type) {
    return type.cast(favorites.get(type));
}

// 사용
String s = getFavorite(String.class);
Integer i = getFavorite(Integer.class);
```

그러나 `List<String>.class`처럼 파라미터화된 타입의 `Class` 리터럴은 존재하지 않는다. 이 한계를 극복하기 위해 **수퍼 타입 토큰(super type token)** 기법을 사용한다. 익명 서브클래스를 생성해 제네릭 상위 타입 정보를 리플렉션으로 추출하는 방식으로, Spring의 `ParameterizedTypeReference`가 이 패턴으로 구현되어 있다:

```java
// 익명 서브클래스를 생성하면 제네릭 타입 정보가 바이트코드에 남는다
TypeReference<List<String>> typeRef = new TypeReference<List<String>>() {};
Type type = typeRef.getType(); // java.util.List<java.lang.String>

// Spring에서의 활용
ResponseEntity<List<User>> response = restTemplate.exchange(
        url
        , HttpMethod.GET
        , null
        , new ParameterizedTypeReference<List<User>>() {}
);
```

## 로 타입(Raw Type)은 사용하지 않는다

제네릭 타입에서 타입 파라미터를 생략한 것을 **로 타입(raw type)**이라 한다. `List<Object>`와 달리 로 타입은 제네릭의 타입 안전성을 완전히 포기한다. 하위 호환성을 위해 언어 사양에는 남아 있지만 새 코드에서는 절대 사용하지 않는다:

```java
// 로 타입: 컴파일 통과, 런타임 예외 위험
GenericBox integerBox = new GenericBox();
integerBox.setValue(10);
Integer result = (Integer) integerBox.getValue(); // 명시적 형변환 필요

// List<Object>: 제네릭 이점 일부 유지. 그러나 List<String>을 넘길 수 없다
// List<?> (비한정 와일드카드): 어떤 타입이든 받되, 타입 안전성 유지
```

제네릭 타입이 무엇인지 신경 쓰지 않는다면 로 타입 대신 비한정 와일드카드 `<?>`를 사용한다.
