# Java 메모리 모델: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. happens-before를 실무 코드에서 위반하는 흔한 패턴은 무엇인가

### 왜 이 질문이 중요한가
happens-before는 JMM의 핵심 개념이지만 추상적으로만 알면 실제 코드에서 위반 사례를 식별할 수 없다. 흔한 위반 패턴을 알아야 코드 리뷰에서 잠재적 동시성 버그를 잡을 수 있다.

### 답변
happens-before(HB)는 "A HB B"이면 A의 모든 메모리 쓰기가 B에서 보인다는 JMM의 보장이다. HB 관계를 형성하는 주요 규칙은 프로그램 순서(같은 스레드 내), 모니터 락(unlock HB lock), volatile 쓰기(write HB read), 스레드 시작(start() HB 첫 동작), 스레드 종료(마지막 동작 HB join()) 등이다.

실무에서 HB를 위반하는 흔한 패턴 세 가지를 살펴본다.

첫째, 초기화 안전성 위반이다. 생성자에서 초기화를 완료하기 전에 `this`를 외부로 노출(escape)하면, 다른 스레드가 초기화 중인 객체를 볼 수 있다.

```java
// this 탈출 — 초기화 안전성 위반
class UnsafePublication {
    int value;
    static UnsafePublication instance;

    UnsafePublication() {
        value = 42;
        instance = this; // 생성자 완료 전에 this 노출!
    }
}
// 다른 스레드에서 instance.value가 0(초기값)으로 보일 수 있음
```

둘째, 안전하지 않은 게시(unsafe publication)다. 동기화 없이 객체를 공유 변수에 쓰면 다른 스레드가 부분적으로 초기화된 객체를 볼 수 있다.

```java
// 안전하지 않은 게시
Map<String, String> map = new HashMap<>(); // 비동시성 컬렉션
map.put("key", "value");
sharedReference = map; // volatile 없음 — HB 관계 없음

// 다른 스레드: sharedReference가 null이 아니더라도
//              map 내부 구조가 일관되지 않을 수 있음
```

셋째, 조건부 체크 후 행동(check-then-act) 패턴이다. volatile로 가시성은 보장되지만 원자성이 없어 두 스레드가 동시에 조건을 통과할 수 있다.

```java
volatile boolean initialized = false;
Resource resource;

// Thread 1
if (!initialized) {       // false 확인
    resource = new Resource();
    initialized = true;
}

// Thread 2 — Thread 1이 initialized=true로 쓰기 전에 동일 체크 통과 가능
if (!initialized) {
    resource = new Resource(); // 중복 초기화!
}
```

---

## Q2. Double-Checked Locking이 volatile 없이 깨지는 이유는 무엇인가

### 왜 이 질문이 중요한가
Double-Checked Locking(DCL)은 지연 초기화 싱글톤의 고전적 패턴이고 인터뷰 단골 주제다. volatile 없이 깨지는 이유를 JMM 수준에서 설명할 수 있어야 `volatile`이 왜 필요한지 설득력 있게 설명할 수 있다.

### 답변
DCL의 의도는 동기화 비용을 줄이기 위해 첫 번째 null 체크를 synchronized 밖에서 수행하는 것이다.

```java
// volatile 없는 DCL — 깨진 패턴
class BrokenSingleton {
    private static BrokenSingleton instance; // volatile 없음

    public static BrokenSingleton getInstance() {
        if (instance == null) {              // 1차 체크 (동기화 없음)
            synchronized (BrokenSingleton.class) {
                if (instance == null) {      // 2차 체크
                    instance = new BrokenSingleton(); // 문제 지점
                }
            }
        }
        return instance;
    }
}
```

`instance = new BrokenSingleton()`은 JVM 수준에서 세 단계다.
1. 메모리 할당
2. 생성자 실행(필드 초기화)
3. `instance` 변수에 참조 저장

JIT 컴파일러와 CPU는 명령어 재배치(reordering)를 최적화를 위해 수행한다. JMM은 단일 스레드 내에서 결과가 동일하면 재배치를 허용한다. 따라서 3번(참조 저장)이 2번(생성자 실행)보다 먼저 실행될 수 있다.

이때 Thread B가 1차 체크(`instance == null`)를 수행하면 `instance`가 null이 아닌 미완성 객체를 가리키는 참조를 보게 된다. Thread B는 synchronized 블록에 들어가지 않고 미초기화된 객체를 반환받는다.

`volatile`은 두 가지로 이 문제를 해결한다. 첫째, volatile 쓰기 이전의 모든 연산은 HB 관계에 의해 volatile 쓰기보다 먼저 완료됨이 보장된다. 따라서 생성자 실행이 `instance` 할당보다 반드시 먼저 완료된다. 둘째, volatile 읽기는 항상 가장 최근의 volatile 쓰기 이후 상태를 본다.

```java
// 올바른 DCL — volatile 사용
class CorrectSingleton {
    private static volatile CorrectSingleton instance; // volatile 필수

    public static CorrectSingleton getInstance() {
        if (instance == null) {
            synchronized (CorrectSingleton.class) {
                if (instance == null) {
                    instance = new CorrectSingleton(); // 재배치 방지
                }
            }
        }
        return instance;
    }
}

// 더 간단한 대안 — 클래스 로딩의 HB 보장 활용
class HolderSingleton {
    private static class Holder {
        static final HolderSingleton INSTANCE = new HolderSingleton();
    }
    public static HolderSingleton getInstance() { return Holder.INSTANCE; }
}
```

Initialization-on-demand holder 패턴은 클래스 로더의 초기화가 단일 스레드에서 수행된다는 JVM 보장을 활용해 volatile이나 synchronized 없이 안전한 지연 초기화를 달성한다.
