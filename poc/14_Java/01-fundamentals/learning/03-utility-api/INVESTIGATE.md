# 유틸리티 API: Deep Investigation

> 본 문서의 학습 자료를 읽은 뒤, 실무와 면접에서 깊이 있게 다뤄야 할 질문들

## Q1. ThreadLocalRandom vs Random 성능 차이의 원인

### 왜 이 질문이 중요한가
멀티스레드 환경에서 `Random`을 공유하면 성능 저하가 발생하는 이유를 이해하지 못하면 잘못된 코드를 작성하고도 원인을 파악하지 못한다. 면접에서는 단순히 "ThreadLocalRandom이 빠르다"가 아니라 왜 빠른지, 내부 메커니즘을 묻는다.

### 답변

`java.util.Random`은 내부 상태로 `AtomicLong seed`를 사용한다. 난수를 생성할 때마다 `compareAndSet()`으로 seed를 업데이트한다. 단일 스레드에서는 문제없지만, 다수의 스레드가 동시에 같은 `Random` 인스턴스에 접근하면 CAS(Compare-And-Swap) 경합이 발생한다. 여러 스레드가 동시에 seed를 바꾸려 하면 실패한 스레드가 재시도하는 스핀 루프에 들어가 CPU 낭비와 처리량 저하가 생긴다.

```java
// Random 내부 (단순화)
protected int next(int bits) {
    long oldseed, nextseed;
    AtomicLong seed = this.seed;
    do {
        oldseed = seed.get();
        nextseed = (oldseed * multiplier + addend) & mask;
    } while (!seed.compareAndSet(oldseed, nextseed)); // 경합 발생 지점
    return (int)(nextseed >>> (48 - bits));
}
```

`ThreadLocalRandom`은 근본적으로 다른 설계를 택했다. 각 스레드의 `Thread` 객체 내부에 seed를 직접 저장하여 스레드 간 공유 상태 자체를 없앤다. 경합할 대상이 없으므로 CAS가 필요 없고 일반 필드 읽기/쓰기로 동작한다. Java 8 이후에는 `Unsafe`를 통해 Thread 객체의 특정 오프셋에 직접 접근하여 오버헤드를 최소화했다.

```java
// 올바른 사용 — 인스턴스를 저장하지 않는다
int value = ThreadLocalRandom.current().nextInt(100);

// 잘못된 사용 — ThreadLocalRandom 인스턴스를 변수에 저장해 공유하면
// Random처럼 동작하며 스레드 안전하지 않다
ThreadLocalRandom rng = ThreadLocalRandom.current(); // 저장 금지
```

성능 차이는 경합이 심할수록 커진다. 스레드 수가 늘어날수록 `Random`은 기하급수적으로 느려지는 반면 `ThreadLocalRandom`은 선형에 가깝게 확장된다. 실무 기준으로 멀티스레드 코드에서는 항상 `ThreadLocalRandom.current()`를 사용하고, 보안이 필요한 경우(토큰 생성 등)에만 `SecureRandom`을 사용한다.

---

## Q2. 정적 유틸리티 클래스 vs Spring Bean

### 왜 이 질문이 중요한가
`StringUtils`, `DateUtils` 같은 유틸리티를 정적 메서드로 만들지, Spring Bean으로 만들지 판단하는 것은 실무에서 자주 부딪히는 설계 결정이다. 잘못 선택하면 테스트가 어려워지거나 불필요한 복잡성이 생긴다. 면접에서도 "정적 메서드의 단점"과 연결해서 묻는다.

### 답변

정적 유틸리티 클래스가 적합한 경우는 세 가지 조건을 모두 만족할 때다. 첫째, 외부 의존성이 없다(DB, 네트워크, 파일 I/O 없음). 둘째, 상태가 없다(인스턴스 변수 없음). 셋째, 행동이 항상 동일하다(입력이 같으면 출력이 항상 같음). 문자열 파싱, 수학 연산, 날짜 포맷팅이 이에 해당한다.

```java
// 정적 유틸리티 클래스가 적합한 예
public final class StringUtils {
    private StringUtils() {} // 인스턴스화 방지

    public static boolean isBlank(String s) {
        return s == null || s.trim().isEmpty();
    }

    public static String truncate(String s, int maxLength) {
        return s.length() <= maxLength ? s : s.substring(0, maxLength) + "...";
    }
}
```

반면 Spring Bean이 적합한 경우는 외부 의존성이 있을 때다. `@Value`로 설정값을 주입받거나, 다른 Bean에 의존하거나, 구현체를 교체해야 한다면 Bean으로 만들어야 한다. 정적 메서드는 Mock으로 교체할 수 없지만 Bean은 테스트에서 Mock 구현체로 쉽게 대체된다.

```java
// 설정값에 의존 → Bean이 적합
@Component
public class PasswordEncoder {
    private final int rounds;

    public PasswordEncoder(@Value("${bcrypt.rounds:12}") int rounds) {
        this.rounds = rounds;
    }

    public String encode(String raw) {
        return BCrypt.hashpw(raw, BCrypt.gensalt(rounds));
    }
}
// 정적 메서드로 만들면 rounds를 어디서 가져와야 하는지 불명확해지고
// 테스트마다 설정값을 바꾸기도 어려워진다
```

판단 기준을 하나로 정리하면, "이 메서드를 테스트할 때 행동을 다르게 하고 싶은 순간이 올 것인가?"이다. 올 것 같다면 Bean, 그럴 일이 없다면 정적 유틸리티다. Spring 자체도 `StringUtils`, `CollectionUtils`, `Assert` 등을 정적 유틸리티로 제공하면서 설정이나 외부 의존이 필요한 기능만 Bean으로 만드는 원칙을 따르고 있다.
